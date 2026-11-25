/**
 * End-to-end business workflow (DAG) — the script of the time axis (the fourth dimension) and its "What" readout.
 * Steps are connected by real dependencies (data hand-over or timing); branches without a dependency may run in parallel.
 * Each step states who does it (actor), when (time of day / trigger), on which page, what data goes in and out,
 * what the system / external system / agent does, and where a human checks.
 * "Run the whole flow" is scheduled by the director along the dependencies: a step is ready only when all upstream steps are done.
 *
 * Single source of truth: the navigator, DAG views, swimlanes, the "Flow · Data" dock, the overview page and the docs all read from here;
 * flow.test.ts guards consistency.
 * PHASES / STEPS / EDGES / DAG_POS below are the example (purchase request approval + ERP integration) — rewrite them per project;
 * the types and utilities are generic.
 */
import type { RoleKey } from '@/state/session';
import type { ActorKey } from './actors';
import type { DataKey } from './dataObjects';

export type PhaseKey = 'setup' | 'submit' | 'approve' | 'deliver';

export interface Phase {
  key: PhaseKey;
  title: string;
  when: string;
  desc: string;
}

export const PHASES: Phase[] = [
  { key: 'setup', title: '准备：配置审批规则', when: '上线前 / 制度调整时', desc: '管理员配置金额阈值等审批规则，发布新版本。' },
  { key: 'submit', title: '提交与校验', when: '日间', desc: '申请人提交采购申请，后台校验并计算审批路径。' },
  { key: 'approve', title: '多级审批', when: '提交后', desc: '部门审批，超过阈值再由财务审批。' },
  { key: 'deliver', title: '下单与汇总', when: '审批通过后 / 夜间', desc: '推送 ERP 生成订单；报表汇总；夜间对账（可选）。' },
];

/** Trigger (display labels): manual | auto-chained | scheduled | external submission */
export type Trigger = '人工触发' | '自动衔接' | '定时调度' | '外部提交';

export interface SubStep {
  title: string;
  actor: ActorKey;
  /** Data object this sub-step produces or uses (the "Flow · Data" dock shows its format sample; tests check it is an input or output of the step) */
  data: DataKey;
  /** data-flow-anchor of the matching page region: scrolled to and highlighted during the demo */
  anchor?: string;
  /** Dwell time of this sub-step when the director advances it on a timer (walk steps), in ms of virtual time */
  ms?: number;
}

/** Requirement status: required = explicitly required by the spec; optional = prototype addition (removing it leaves the main flow intact). Unlabeled = a normal step within the spec's scope. */
export type Necessity = 'required' | 'optional';

export const NECESSITY_LABEL: Record<Necessity, string> = { required: '需求必需', optional: '原型补充 · 可选' };

export type StepId = 'config' | 'submit' | 'auto-check' | 'dept-approve' | 'finance-approve' | 'erp-sync' | 'report' | 'reconcile';

export interface FlowStep {
  id: StepId;
  phase: PhaseKey;
  title: string;
  /** Short title for swimlanes / nodes (about 10 CJK characters at most) */
  short: string;
  actor: ActorKey;
  with: ActorKey[];
  /** Demo role to switch to */
  role: RoleKey;
  /** Page route (may include ?tab=) */
  route: string;
  when: string;
  trigger: Trigger;
  /** Narration: what happens in business terms */
  narration: string;
  /** What the system / external system / agent does in this step (the automated part) */
  machine?: string;
  /** Where a human checks */
  human?: string;
  inputs: DataKey[];
  outputs: DataKey[];
  subs: SubStep[];
  /** page: the page performs the actions and reports progress; walk: the director advances by sub-step durations (the page may prepare) */
  drive: 'page' | 'walk';
  /** Continuation of the same backend job: entered right after the previous step (only when the previous step is on the same page) */
  chain?: boolean;
  necessity?: Necessity;
  basis?: string;
}

export const STEPS: FlowStep[] = [
  {
    id: 'config',
    phase: 'setup',
    title: '管理员配置审批规则（财务审批金额阈值），发布新版本',
    short: '配置审批规则',
    actor: 'admin',
    with: [],
    role: 'admin',
    route: '/settings',
    when: '08:30',
    trigger: '人工触发',
    narration: '管理员把财务审批的金额阈值由 5 万调整为 3 万，查看变更前后对比后发布，规则版本 +1。',
    human: '变更需确认后才生效，全程留痕。',
    inputs: ['approvalRule'],
    outputs: ['approvalRule'],
    subs: [
      { title: '修改金额阈值', actor: 'admin', data: 'approvalRule', anchor: 'rule-form' },
      { title: '确认变更并发布', actor: 'admin', data: 'approvalRule', anchor: 'rule-publish' },
    ],
    drive: 'page',
  },
  {
    id: 'submit',
    phase: 'submit',
    title: '申请人填写并提交采购申请',
    short: '提交申请',
    actor: 'applicant',
    with: [],
    role: 'applicant',
    route: '/requests?tab=new',
    when: '10:00',
    trigger: '人工触发',
    narration: '申请人填写供应商、品类、金额（4.2 万元）并上传报价单，提交后申请单状态由“草稿”变为“已提交”。',
    inputs: [],
    outputs: ['purchaseRequest'],
    subs: [
      { title: '填写申请单', actor: 'applicant', data: 'purchaseRequest', anchor: 'request-form' },
      { title: '提交', actor: 'applicant', data: 'purchaseRequest' },
    ],
    drive: 'page',
  },
  {
    id: 'auto-check',
    phase: 'submit',
    title: '后台校验预算并按审批规则计算审批路径',
    short: '校验与定路径',
    actor: 'system',
    with: ['applicant'],
    role: 'applicant',
    route: '/requests?tab=new',
    when: '提交后自动',
    trigger: '自动衔接',
    narration: '后台校验必填项与预算余额，按最新审批规则（阈值 3 万）得出“部门 → 财务”两级审批，申请单进入“部门审批中”并通知审批人。',
    machine: '确定性校验与路径计算；发送待办通知。',
    inputs: ['approvalRule', 'purchaseRequest'],
    outputs: ['approvalPath', 'purchaseRequest'],
    subs: [
      { title: '校验必填项与预算', actor: 'system', data: 'purchaseRequest', anchor: 'check-log' },
      { title: '计算审批路径', actor: 'system', data: 'approvalPath', anchor: 'check-log' },
    ],
    drive: 'page',
    chain: true,
  },
  {
    id: 'dept-approve',
    phase: 'approve',
    title: '部门审批人审批',
    short: '部门审批',
    actor: 'approver',
    with: [],
    role: 'approver',
    route: '/approvals',
    when: '当日',
    trigger: '人工触发',
    narration: '部门审批人在待办中打开申请，查看金额、供应商与报价单，同意后进入财务审批。',
    human: '同意 / 驳回 / 退回修改由审批人决定。',
    inputs: ['approvalPath', 'purchaseRequest'],
    outputs: ['approvalRecord', 'purchaseRequest'],
    subs: [
      { title: '打开待办', actor: 'approver', data: 'purchaseRequest', anchor: 'approval-list' },
      { title: '同意', actor: 'approver', data: 'approvalRecord', anchor: 'approval-detail' },
    ],
    drive: 'page',
  },
  {
    id: 'finance-approve',
    phase: 'approve',
    title: '财务审批人审批（金额超过阈值时）',
    short: '财务审批',
    actor: 'finance',
    with: [],
    role: 'finance',
    route: '/approvals?tab=finance',
    when: '当日',
    trigger: '人工触发',
    narration: '金额 4.2 万超过 3 万阈值，需财务核对预算科目后审批；同意后申请单状态变为“已通过”。',
    human: '财务核对预算科目，可驳回。',
    inputs: ['approvalRecord', 'purchaseRequest'],
    outputs: ['approvalRecord', 'purchaseRequest'],
    subs: [
      { title: '核对预算科目', actor: 'finance', data: 'purchaseRequest', anchor: 'approval-detail' },
      { title: '同意', actor: 'finance', data: 'approvalRecord', anchor: 'approval-detail' },
    ],
    drive: 'page',
  },
  {
    id: 'erp-sync',
    phase: 'deliver',
    title: '推送 ERP 生成采购订单并回写订单号',
    short: '推送 ERP',
    actor: 'system',
    with: ['external'],
    role: 'admin',
    route: '/integration',
    when: '审批通过后自动',
    trigger: '自动衔接',
    narration: '后台把已通过的申请组装成订单报文推送 ERP（模拟环境），收到回执后回写订单号，申请单状态变为“已下单”。',
    machine: '组装报文、调用接口、失败重试、回写。',
    inputs: ['purchaseRequest'],
    outputs: ['erpOrder', 'purchaseRequest'],
    subs: [
      { title: '组装订单报文', actor: 'system', data: 'erpOrder', anchor: 'erp-payload', ms: 2400 },
      { title: 'ERP 返回订单号', actor: 'external', data: 'erpOrder', anchor: 'erp-receipt', ms: 2400 },
      { title: '回写申请单状态', actor: 'system', data: 'purchaseRequest', anchor: 'erp-receipt', ms: 1800 },
    ],
    drive: 'walk',
  },
  {
    id: 'report',
    phase: 'deliver',
    title: '管理员查看采购报表',
    short: '采购报表',
    actor: 'admin',
    with: [],
    role: 'admin',
    route: '/reports',
    when: '日常',
    trigger: '人工触发',
    narration: '按部门、月份查看申请数、金额与平均审批时长。',
    inputs: ['erpOrder'],
    outputs: ['reportAgg'],
    subs: [{ title: '查看部门汇总', actor: 'admin', data: 'reportAgg', anchor: 'report-kpi', ms: 2600 }],
    drive: 'walk',
  },
  {
    id: 'reconcile',
    phase: 'deliver',
    title: '夜间与 ERP 对账',
    short: '夜间对账',
    actor: 'scheduler',
    with: ['external'],
    role: 'admin',
    route: '/integration?tab=reconcile',
    when: '23:00',
    trigger: '定时调度',
    narration: '定时任务拉取 ERP 当日订单，与本系统已下单的申请逐笔核对，差异进入人工处理队列。',
    machine: '拉取、比对、生成差异清单。',
    inputs: ['erpOrder'],
    outputs: ['reportAgg'],
    subs: [{ title: '运行对账', actor: 'scheduler', data: 'erpOrder', anchor: 'reconcile-run', ms: 3000 }],
    drive: 'walk',
    necessity: 'optional',
    basis: '需求未要求；为讨论“接口失败时如何发现与补偿”补充，去掉不影响审批主流程。',
  },
];

export interface Edge {
  from: StepId;
  to: StepId;
  /** Data carried along the edge; omitted = timing dependency (dashed) */
  data?: DataKey;
  label: string;
}

export const EDGES: Edge[] = [
  { from: 'config', to: 'auto-check', data: 'approvalRule', label: '审批规则 v+1' },
  { from: 'submit', to: 'auto-check', data: 'purchaseRequest', label: '申请单（已提交）' },
  { from: 'auto-check', to: 'dept-approve', data: 'approvalPath', label: '审批路径' },
  { from: 'dept-approve', to: 'finance-approve', data: 'approvalRecord', label: '部门已同意' },
  { from: 'finance-approve', to: 'erp-sync', data: 'purchaseRequest', label: '申请单（已通过）' },
  { from: 'erp-sync', to: 'report', data: 'erpOrder', label: '订单回执' },
  { from: 'erp-sync', to: 'reconcile', data: 'erpOrder', label: '当日订单' },
];

/** DAG layout: row = business branch, col = dependency depth (same column may run in parallel; col must exceed every upstream col) */
export const DAG_POS: Record<StepId, { col: number; row: number }> = {
  config: { col: 0, row: 0 },
  submit: { col: 0, row: 1 },
  'auto-check': { col: 1, row: 0.5 },
  'dept-approve': { col: 2, row: 0.5 },
  'finance-approve': { col: 3, row: 0.5 },
  'erp-sync': { col: 4, row: 0.5 },
  report: { col: 5, row: 0 },
  reconcile: { col: 5, row: 1 },
};

export const DAG_ROWS: { row: number; label: string; desc: string }[] = [
  { row: 0, label: '规则', desc: '管理员' },
  { row: 1, label: '申请', desc: '申请人 → 审批人 → ERP' },
];

export const DAG_COLS = 6;

/** Default tab of each page (when the URL has no tab) */
const DEFAULT_TAB: Record<string, string> = { '/requests': 'new', '/approvals': 'dept', '/integration': 'sync' };

export function depsOf(id: StepId): StepId[] {
  return EDGES.filter((e) => e.to === id).map((e) => e.from);
}

export function succOf(id: StepId): StepId[] {
  return EDGES.filter((e) => e.from === id).map((e) => e.to);
}

/** All upstream (ancestor) steps */
export function ancestorsOf(id: StepId): Set<StepId> {
  const out = new Set<StepId>();
  const walk = (x: StepId) =>
    depsOf(x).forEach((d) => {
      if (!out.has(d)) {
        out.add(d);
        walk(d);
      }
    });
  walk(id);
  return out;
}

/** Ready steps: not done and all upstream done, in STEPS order */
export function readySteps(done: Iterable<StepId>): StepId[] {
  const set = new Set(done);
  return STEPS.filter((s) => !set.has(s.id) && depsOf(s.id).every((d) => set.has(d))).map((s) => s.id);
}

/**
 * Priority order of ready steps: STEPS order, optional steps last (they never interrupt the main flow).
 * Write STEPS as a topological order sorted by business time, with optional steps at the end; a run from the start then yields exactly the STEPS order.
 * Do not "continue downstream of the step that just finished first": once parallel branches have several steps each
 * (accept → cook ∥ dispatch → arrive), that plays a 12:05 step before an 11:53 one.
 */
export function orderReady(done: Iterable<StepId>): StepId[] {
  const ready = readySteps(done);
  const optional = (id: StepId) => stepById(id).necessity === 'optional';
  return [...ready.filter((id) => !optional(id)), ...ready.filter(optional)];
}

/** Depth of the longest dependency chain (level, starting at 0) */
export function levelOf(id: StepId): number {
  const d = depsOf(id);
  return d.length ? 1 + Math.max(...d.map(levelOf)) : 0;
}

export const STEP_INDEX: Record<StepId, number> = Object.fromEntries(STEPS.map((s, i) => [s.id, i])) as Record<StepId, number>;

export function stepById(id: StepId): FlowStep {
  return STEPS[STEP_INDEX[id]];
}

export function pathOf(route: string) {
  return route.split('?')[0] || '/';
}

export function tabOf(route: string) {
  return new URLSearchParams(route.split('?')[1] ?? '').get('tab');
}

/** Workflow steps of the current page (path + tab): used by the "this page in the whole flow" header tags and the navigator */
export function stepsForRoute(path: string, tab: string | null): { step: FlowStep; exact: boolean }[] {
  const cur = tab ?? DEFAULT_TAB[path] ?? null;
  return STEPS.filter((s) => pathOf(s.route) === path).map((s) => {
    const t = tabOf(s.route);
    return { step: s, exact: !t || t === cur };
  });
}
