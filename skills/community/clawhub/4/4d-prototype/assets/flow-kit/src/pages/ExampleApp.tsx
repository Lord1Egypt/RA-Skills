/**
 * Integration example: a minimal "purchase request approval" prototype showing how pages hook into the 4D orchestration layer.
 * Replace the domain after copying; real pages are much richer, but the wiring is the same:
 *
 * 1. Each page step calls useFlowStep(stepId, onEnter) in its page; onEnter demonstrates the actions with ctl.click / ctl.hover / ctl.later,
 *    reports sub-steps with ctl.sub(i) and completion with ctl.done();
 * 2. onEnter must supply its own demo data when upstream output is missing (ensureRequestAt), so any step can be switched to at any time
 *    and replayed after finishing;
 * 3. steps that judge completion by processing progress record the object started by this entry (ctl.nonce) and follow only its progress;
 * 4. clickable targets get data-demo, highlight regions get data-flow-anchor (flow.test.ts checks the anchors exist);
 * 5. the shell mounts DemoCursor, the playback capsule, hotkeys and the sub-step spotlight (useFlowSpotlight); the main scroll region is <main id="main">.
 */
import { useEffect, useRef, useState } from 'react';
import { DemoCursor } from '@/components/flow/DemoCursor';
import { PlaybackCapsule, usePlaybackHotkeys } from '@/components/flow/PlaybackControls';
import { ACTORS } from '@/flow/actors';
import { useFlowSpotlight } from '@/flow/spotlight';
import { flowActive, goToStep, startFlow, stepStateOf, useFlow, useFlowStep, type FlowCtl } from '@/flow/director';
import { STEPS } from '@/flow/workflow';
import { navigate, useRoute } from '@/lib/router';
import { useStore } from '@/lib/store';
import { DEMO_DRAFT, approve, ensureRequestAt, publishThreshold, reqStore, ruleStore, runCheck, submitRequest, syncErp, type PurchaseRequest } from '@/state/requests';
import { USERS, setRole, useUser, type RoleKey } from '@/state/session';

const STATE_LABEL = { idle: '', running: '运行中', done: '已完成', assumed: '视为完成', ready: '可执行', waiting: '等待上游' } as const;

/** Minimal navigator: step list + states; clicking any step switches to it (enters it during a demo, opens its page otherwise) */
function MiniFlowList() {
  const f = useFlow((s) => s);
  return (
    <ol className="space-y-1 text-sm">
      {STEPS.map((s, i) => (
        <li key={s.id}>
          <button type="button" onClick={() => goToStep(s.id)} className="flex w-full items-center gap-2 rounded px-2 py-1 text-left hover:bg-ink-950/5">
            <span style={{ color: ACTORS[s.actor].color }}>{String.fromCodePoint(0x2460 + i)}</span>
            <span className="flex-1 truncate">{s.short}</span>
            {s.necessity === 'optional' ? <span className="text-xs text-ink-500">可选</span> : null}
            <span className="text-xs text-ink-500">{STATE_LABEL[stepStateOf(f, s.id)]}</span>
          </button>
        </li>
      ))}
    </ol>
  );
}

function SettingsPage() {
  const rule = useStore(ruleStore, (s) => s);
  const [draft, setDraft] = useState(rule.financeThreshold);
  useFlowStep('config', (c) => {
    c.sub(0);
    c.click('[data-demo="threshold-30000"]', () => setDraft(30000));
    c.later(1800, () => {
      c.sub(1);
      c.click('[data-demo="publish"]', () => {
        publishThreshold(30000);
        c.done();
      });
    });
  });
  return (
    <section data-flow-anchor="rule-form" className="space-y-3">
      <h2 className="text-lg font-semibold">审批规则 v{rule.version}</h2>
      <p>财务审批阈值：{rule.financeThreshold.toLocaleString()} 元 → 草稿 {draft.toLocaleString()} 元</p>
      <button type="button" data-demo="threshold-30000" onClick={() => setDraft(30000)} className="rounded-full bg-ink-950/5 px-3 py-1">
        改为 3 万
      </button>
      <button type="button" data-demo="publish" data-flow-anchor="rule-publish" onClick={() => publishThreshold(draft)} className="ml-2 rounded-full bg-primary-500 px-3 py-1 text-white">
        确认并发布
      </button>
    </section>
  );
}

function RequestsPage() {
  const list = useStore(reqStore, (s) => s.list);
  const [draft, setDraft] = useState({ supplier: '', amount: 0 });

  useFlowStep('submit', (c) => {
    c.sub(0);
    c.click('[data-demo="fill-demo"]', () => setDraft(DEMO_DRAFT));
    c.later(1600, () => {
      c.sub(1);
      c.click('[data-demo="submit"]', () => {
        submitRequest(DEMO_DRAFT);
        setDraft({ supplier: '', amount: 0 });
        c.done();
      });
    });
  });

  // Completion by processing progress: follow only the request whose check was started by this entry (nonce)
  const run = useRef({ nonce: 0, reqNo: '' });
  const checkCtl = useFlowStep('auto-check', (c) => {
    const req = reqStore.get().list.find((r) => r.status === '已提交') ?? ensureRequestAt('已提交');
    run.current = { nonce: c.nonce, reqNo: req.reqNo };
    runCheck(req.reqNo);
  });
  useEffect(() => {
    if (!checkCtl || run.current.nonce !== checkCtl.nonce) return;
    const r = list.find((x) => x.reqNo === run.current.reqNo);
    if (!r) return;
    checkCtl.sub(r.checkStage >= 1 ? 1 : 0);
    if (r.checkStage >= 2) checkCtl.done();
  }, [checkCtl, list]);

  return (
    <section className="space-y-3">
      <div data-flow-anchor="request-form" className="space-y-2">
        <p>
          供应商：{draft.supplier || '—'}　金额：{draft.amount ? `${draft.amount.toLocaleString()} 元` : '—'}
        </p>
        <button type="button" data-demo="fill-demo" onClick={() => setDraft(DEMO_DRAFT)} className="rounded-full bg-ink-950/5 px-3 py-1">
          填入示例
        </button>
        <button type="button" data-demo="submit" disabled={!draft.amount} onClick={() => submitRequest(draft)} className="ml-2 rounded-full bg-primary-500 px-3 py-1 text-white disabled:opacity-40">
          提交
        </button>
      </div>
      <ul data-flow-anchor="check-log" className="space-y-1 text-sm">
        {list.map((r) => (
          <li key={r.reqNo}>
            {r.reqNo} · {r.status} · {r.log.join(' → ')}
          </li>
        ))}
      </ul>
    </section>
  );
}

function ApprovalsPage({ tab }: { tab: 'dept' | 'finance' }) {
  const list = useStore(reqStore, (s) => s.list);
  const [open, setOpen] = useState<string | null>(null);
  const status = tab === 'dept' ? '部门审批中' : '财务审批中';

  const flowApprove = (node: 'dept' | 'finance') => (c: FlowCtl) => {
    const req: PurchaseRequest = ensureRequestAt(node === 'dept' ? '部门审批中' : '财务审批中');
    c.sub(0);
    c.click(`[data-demo="todo-${req.reqNo}"]`, () => setOpen(req.reqNo));
    c.later(2000, () => {
      c.sub(1);
      c.click('[data-demo="approve"]', () => {
        approve(req.reqNo, node);
        setOpen(null);
        c.done();
      });
    });
  };
  useFlowStep('dept-approve', flowApprove('dept'));
  useFlowStep('finance-approve', flowApprove('finance'));

  const cur = list.find((r) => r.reqNo === open);
  return (
    <section className="space-y-3">
      <ul data-flow-anchor="approval-list" className="space-y-1">
        {list
          .filter((r) => r.status === status)
          .map((r) => (
            <li key={r.reqNo}>
              <button type="button" data-demo={`todo-${r.reqNo}`} onClick={() => setOpen(r.reqNo)} className="underline">
                {r.reqNo} · {r.amount.toLocaleString()} 元
              </button>
            </li>
          ))}
      </ul>
      {cur ? (
        <div data-flow-anchor="approval-detail" className="rounded-xl bg-surface p-4 shadow">
          <p>
            {cur.reqNo} · {cur.supplier} · {cur.amount.toLocaleString()} 元 · 路径 {cur.path.join(' → ')}
          </p>
          <button type="button" data-demo="approve" onClick={() => approve(cur.reqNo, tab)} className="mt-2 rounded-full bg-primary-500 px-3 py-1 text-white">
            同意
          </button>
        </div>
      ) : (
        <div data-flow-anchor="approval-detail" className="text-sm text-ink-500">
          选择一条待办
        </div>
      )}
    </section>
  );
}

function IntegrationPage({ tab }: { tab: 'sync' | 'reconcile' }) {
  const list = useStore(reqStore, (s) => s.list);
  const [payload, setPayload] = useState<string>('');
  // Walk step: the director advances by sub-step durations; the page only prepares data and visual effects
  useFlowStep('erp-sync', (c) => {
    const req = ensureRequestAt('已通过');
    setPayload(JSON.stringify({ reqNo: req.reqNo, supplier: req.supplier, amount: req.amount }, null, 2));
    c.later(2400, () => syncErp(req.reqNo, `PO-${req.reqNo.slice(-4)}`));
  });
  const done = list.filter((r) => r.erpOrderNo);
  if (tab === 'reconcile')
    return (
      <section data-flow-anchor="reconcile-run" className="space-y-2">
        <h2 className="font-semibold">夜间对账（模拟环境）</h2>
        <p>已下单 {done.length} 笔，与 ERP 一致 {done.length} 笔，差异 0 笔。</p>
      </section>
    );
  return (
    <section className="space-y-3">
      <pre data-flow-anchor="erp-payload" className="theme-island rounded-xl bg-ink-900 p-3 text-xs text-white">
        POST /erp/api/purchase-orders{'\n'}
        {payload || '{}'}
      </pre>
      <ul data-flow-anchor="erp-receipt" className="text-sm">
        {done.map((r) => (
          <li key={r.reqNo}>
            {r.reqNo} → {r.erpOrderNo}
          </li>
        ))}
      </ul>
    </section>
  );
}

function ReportsPage() {
  const list = useStore(reqStore, (s) => s.list);
  return (
    <section data-flow-anchor="report-kpi" className="grid grid-cols-3 gap-4">
      <div>申请 {list.length} 笔</div>
      <div>金额 {list.reduce((a, r) => a + r.amount, 0).toLocaleString()} 元</div>
      <div>已下单 {list.filter((r) => r.erpOrderNo).length} 笔</div>
    </section>
  );
}

function Page() {
  const { path, query } = useRoute();
  switch (path) {
    case '/settings':
      return <SettingsPage />;
    case '/requests':
      return <RequestsPage />;
    case '/approvals':
      return <ApprovalsPage tab={query.get('tab') === 'finance' ? 'finance' : 'dept'} />;
    case '/integration':
      return <IntegrationPage tab={query.get('tab') === 'reconcile' ? 'reconcile' : 'sync'} />;
    case '/reports':
      return <ReportsPage />;
    default:
      return <p>选择左侧环节，或点“一键运行完整流程”。</p>;
  }
}

export function ExampleApp() {
  const active = useFlow((s) => s.active);
  const user = useUser();
  usePlaybackHotkeys(active);
  useFlowSpotlight();
  return (
    <div className="flex h-screen bg-ink-100 text-ink-900">
      <aside className="w-64 shrink-0 space-y-4 overflow-auto bg-surface/80 p-4">
        <button type="button" onClick={() => void startFlow({ mode: 'auto', reset: true })} className="w-full rounded-full bg-primary-500 px-3 py-2 text-white">
          一键运行完整流程
        </button>
        <MiniFlowList />
      </aside>
      <div className="relative flex min-w-0 flex-1 flex-col">
        <header className="flex items-center gap-3 border-b border-ink-950/5 bg-surface/80 px-6 py-3 text-sm">
          <span className="font-semibold">采购申请（原型）</span>
          <span className="flex-1" />
          演示角色：
          <select value={user.role} onChange={(e) => setRole(e.target.value as RoleKey)} disabled={flowActive()}>
            {Object.values(USERS).map((u) => (
              <option key={u.role} value={u.role}>
                {ACTORS[u.role].label} · {u.name}
              </option>
            ))}
          </select>
          <button type="button" onClick={() => navigate('/')} className="text-primary-600">
            首页
          </button>
        </header>
        <main id="main" className="flex-1 overflow-auto p-6 pb-28">
          <Page />
        </main>
        {/* Playback capsule: centered and floating, nothing on either side; in real projects it sits above the "Flow · Data" dock's top edge */}
        <div className="pointer-events-none absolute inset-x-0 bottom-4 flex justify-center">
          <PlaybackCapsule />
        </div>
      </div>
      <DemoCursor />
    </div>
  );
}
