/**
 * Data object catalog — the "Data" readout of the timeline: every data structure flowing through the workflow
 * (fields, types, medium, sensitivity, producer).
 * Fields correspond one-to-one with the TypeScript types in src, so business and engineering agree on
 * "what the data looks like and where it changes".
 * Business objects with a lifecycle (request, ticket, order …) list their states; the lineage view shows transitions from them.
 * Each object also gets an original-look format sample in formats.ts (form / Excel layout / table / API payload / document / log).
 */
import type { ActorKey } from './actors';

export type DataKey = 'approvalRule' | 'purchaseRequest' | 'approvalPath' | 'approvalRecord' | 'erpOrder' | 'reportAgg';

export interface DataField {
  name: string;
  type: string;
  desc: string;
}

export interface DataObj {
  key: DataKey;
  name: string;
  /** Type name in code */
  type: string;
  /** Medium and location (page form / file / table / API payload / memory) */
  carrier: string;
  /** high | medium | low (display labels) */
  sensitivity: '高' | '中' | '低';
  sensNote: string;
  producer: ActorKey;
  desc: string;
  /** Objects with a lifecycle: state values in transition order */
  states?: string[];
  fields: DataField[];
}

const D: DataObj[] = [
  {
    key: 'approvalRule',
    name: '审批规则',
    type: 'ApprovalRule',
    carrier: '业务库（建议表 pr_approval_rule；原型存于浏览器本地）',
    sensitivity: '低',
    sensNote: '内部配置',
    producer: 'admin',
    desc: '按金额、类别决定审批路径的规则与阈值，带版本。',
    fields: [
      { name: 'version', type: 'number', desc: '版本号，每次发布 +1' },
      { name: 'financeThreshold', type: 'number', desc: '超过该金额需财务审批（元）' },
    ],
  },
  {
    key: 'purchaseRequest',
    name: '采购申请单',
    type: 'PurchaseRequest',
    carrier: '页面表单 → 业务库（建议表 pr_request）',
    sensitivity: '中',
    sensNote: '含供应商与金额',
    producer: 'applicant',
    desc: '申请人提交的采购申请；状态随审批推进变化。',
    states: ['草稿', '已提交', '部门审批中', '财务审批中', '已通过', '已下单'],
    fields: [
      { name: 'reqNo', type: 'string', desc: '申请单号' },
      { name: 'amount', type: 'number', desc: '金额（元）' },
      { name: 'status', type: 'RequestStatus', desc: '当前状态' },
    ],
  },
  {
    key: 'approvalPath',
    name: '审批路径',
    type: 'ApprovalPath',
    carrier: '内存 → 业务库（随申请单保存）',
    sensitivity: '低',
    sensNote: '流程信息',
    producer: 'system',
    desc: '后台按审批规则计算出的审批节点序列。',
    fields: [{ name: 'nodes[]', type: "('dept' | 'finance')[]", desc: '依次需要的审批' }],
  },
  {
    key: 'approvalRecord',
    name: '审批记录',
    type: 'ApprovalRecord',
    carrier: '业务库（建议表 pr_approval_log）',
    sensitivity: '中',
    sensNote: '含审批意见',
    producer: 'approver',
    desc: '每个审批节点的结论、意见与时间，全程留痕。',
    fields: [
      { name: 'node', type: "'dept' | 'finance'", desc: '审批节点' },
      { name: 'decision', type: "'approve' | 'reject' | 'return'", desc: '结论' },
    ],
  },
  {
    key: 'erpOrder',
    name: 'ERP 采购订单',
    type: 'ErpOrderPayload',
    carrier: '接口报文（POST /erp/api/purchase-orders，原型中为模拟）',
    sensitivity: '中',
    sensNote: '含供应商与金额',
    producer: 'system',
    desc: '审批通过后推送 ERP 的订单报文与回执。',
    fields: [
      { name: 'reqNo', type: 'string', desc: '来源申请单号' },
      { name: 'erpOrderNo', type: 'string', desc: 'ERP 回传的订单号' },
    ],
  },
  {
    key: 'reportAgg',
    name: '采购报表',
    type: 'ReportAgg',
    carrier: '由业务库实时聚合',
    sensitivity: '低',
    sensNote: '只含统计数字',
    producer: 'scheduler',
    desc: '按部门、月份汇总的申请数、金额、平均审批时长。',
    fields: [{ name: 'byDept[]', type: 'DeptStat[]', desc: '各部门统计' }],
  },
];

export const DATA_OBJECTS: Record<DataKey, DataObj> = Object.fromEntries(D.map((d) => [d.key, d])) as Record<DataKey, DataObj>;
