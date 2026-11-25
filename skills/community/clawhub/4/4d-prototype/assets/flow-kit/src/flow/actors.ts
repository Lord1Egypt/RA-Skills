/**
 * Actors (who performs a step) — the "Who" readout of the timeline: who is acting at each moment.
 * Human roles match system permissions; machine actors are chosen per project: backend service / scheduler, external system,
 * RPA, message queue, agent (LLM) …
 * "Actor" and "execution mode" (rule code / human judgment / LLM) are separate dimensions: one backend job can mix code rules and model calls.
 * Colors use their own token set (--color-act-*), never mixed with outcome colors (pass / reject / pending).
 */
import type { RoleKey } from '@/state/session';

export type ActorKey = RoleKey | 'system' | 'scheduler' | 'external';

export interface ActorDef {
  key: ActorKey;
  label: string;
  short: string;
  /** human | machine | external (display labels) */
  kind: '人工' | '机器' | '外部';
  desc: string;
  /** CSS color (token) for dots, swimlane borders and the cursor */
  color: string;
}

export const ACTORS: Record<ActorKey, ActorDef> = {
  applicant: { key: 'applicant', label: '申请人', short: '申请人', kind: '人工', desc: '填写并提交采购申请，查看进度', color: 'var(--color-act-applicant)' },
  approver: { key: 'approver', label: '部门审批人', short: '部门审批', kind: '人工', desc: '审批本部门的申请：同意 / 驳回 / 退回修改', color: 'var(--color-act-approver)' },
  finance: { key: 'finance', label: '财务审批人', short: '财务', kind: '人工', desc: '审批超过金额阈值的申请，核对预算科目', color: 'var(--color-act-finance)' },
  admin: { key: 'admin', label: '系统管理员', short: '管理员', kind: '人工', desc: '配置审批规则与阈值，查看报表', color: 'var(--color-act-admin)' },
  system: { key: 'system', label: '后台服务', short: '后台', kind: '机器', desc: '校验、计算审批路径、状态流转、写库、发通知', color: 'var(--color-act-system)' },
  scheduler: { key: 'scheduler', label: '定时任务', short: '定时任务', kind: '机器', desc: '夜间对账、汇总统计', color: 'var(--color-act-scheduler)' },
  external: { key: 'external', label: 'ERP 系统', short: 'ERP', kind: '外部', desc: '接收采购订单并回传订单号（原型中为模拟环境）', color: 'var(--color-act-external)' },
};

/** Human actors: the demo cursor is shown when they perform a sub-step */
export const HUMAN: ActorKey[] = (Object.keys(ACTORS) as ActorKey[]).filter((k) => ACTORS[k].kind === '人工');
