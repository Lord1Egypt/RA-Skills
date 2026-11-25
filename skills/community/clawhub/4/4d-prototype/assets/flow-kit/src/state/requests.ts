import { createStore } from '@/lib/store';
import { vSetTimeout } from '@/flow/clock';

/**
 * Example business state (purchase request approval): demo data persists in localStorage across reloads; "reset demo data" restores it.
 * Every timed operation (backend check, API call) uses the virtual clock vSetTimeout, so it scales with playback speed and freezes on pause.
 */
export type RequestStatus = '草稿' | '已提交' | '部门审批中' | '财务审批中' | '已通过' | '已下单';

export interface PurchaseRequest {
  reqNo: string;
  supplier: string;
  amount: number;
  status: RequestStatus;
  path: ('dept' | 'finance')[];
  /** Backend check progress: 0 not started / 1 checks passed / 2 path computed */
  checkStage: number;
  erpOrderNo?: string;
  log: string[];
}

export const ruleStore = createStore('approval-rule', () => ({ version: 1, financeThreshold: 50000 }));
export const reqStore = createStore('requests', () => ({ list: [] as PurchaseRequest[], seq: 0 }));

export const DEMO_DRAFT = { supplier: '示例办公设备有限公司', amount: 42000 };

function update(reqNo: string, patch: (r: PurchaseRequest) => Partial<PurchaseRequest>) {
  reqStore.set((s) => ({ list: s.list.map((r) => (r.reqNo === reqNo ? { ...r, ...patch(r) } : r)) }));
}

export function publishThreshold(threshold: number) {
  ruleStore.set((s) => ({ version: s.version + 1, financeThreshold: threshold }));
}

export function submitRequest(draft: { supplier: string; amount: number }): PurchaseRequest {
  const seq = reqStore.get().seq + 1;
  const req: PurchaseRequest = { reqNo: `PR2026${String(seq).padStart(4, '0')}`, ...draft, status: '已提交', path: [], checkStage: 0, log: ['申请人提交'] };
  reqStore.set((s) => ({ seq, list: [req, ...s.list] }));
  return req;
}

/** Backend check and path computation; instant = true finishes immediately (used when a page supplies its own upstream) */
export function runCheck(reqNo: string, instant = false) {
  const finish = () =>
    update(reqNo, (r) => {
      const path: PurchaseRequest['path'] = r.amount > ruleStore.get().financeThreshold ? ['dept', 'finance'] : ['dept'];
      return { checkStage: 2, path, status: '部门审批中', log: [...r.log, `审批路径：${path.join(' → ')}`] };
    });
  if (instant) {
    update(reqNo, (r) => ({ checkStage: 1, log: [...r.log, '校验通过'] }));
    finish();
    return;
  }
  vSetTimeout(() => update(reqNo, (r) => ({ checkStage: 1, log: [...r.log, '校验通过'] })), 1200);
  vSetTimeout(finish, 2600);
}

export function approve(reqNo: string, node: 'dept' | 'finance') {
  update(reqNo, (r) => {
    const needFinance = node === 'dept' && r.path.includes('finance');
    return { status: needFinance ? '财务审批中' : '已通过', log: [...r.log, `${node === 'dept' ? '部门' : '财务'}同意`] };
  });
}

export function syncErp(reqNo: string, orderNo: string) {
  update(reqNo, (r) => ({ erpOrderNo: orderNo, status: '已下单', log: [...r.log, `ERP 订单 ${orderNo}`] }));
}

/** Find the latest request in a state; if none, push a demo request to that state (so any step can run on its own) */
export function ensureRequestAt(status: RequestStatus): PurchaseRequest {
  const found = reqStore.get().list.find((r) => r.status === status);
  if (found) return found;
  const order: RequestStatus[] = ['已提交', '部门审批中', '财务审批中', '已通过', '已下单'];
  const target = order.indexOf(status);
  // To reach the finance node, use an amount above the threshold so the path includes finance (whatever the threshold is in the demo)
  const amount = target >= 2 ? Math.max(DEMO_DRAFT.amount, ruleStore.get().financeThreshold + 8000) : DEMO_DRAFT.amount;
  const req = submitRequest({ ...DEMO_DRAFT, amount });
  if (target >= 1) runCheck(req.reqNo, true);
  if (target >= 2) approve(req.reqNo, 'dept');
  if (target >= 3) approve(req.reqNo, 'finance');
  if (target >= 4) syncErp(req.reqNo, 'PO-DEMO-0001');
  return reqStore.get().list.find((r) => r.reqNo === req.reqNo) ?? req;
}
