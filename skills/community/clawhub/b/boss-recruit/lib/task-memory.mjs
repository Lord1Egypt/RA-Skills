/**
 * 任务记忆 / 状态机 (task memory)
 * ───────────────────────────────────────────────────────────────────────────
 * 本地 JSON 持久化每个候选人的处理状态，实现：
 *   - 未读优先 / 去重（已 synced/rejected 且无新消息的不重扫）
 *   - 断点续跑（每个动作后立即回写，崩了能续）
 *   - 附件闭环状态推进
 *
 * 状态机：
 *   pending → resume_read（在线简历已读）
 *           → attachment_requested（已要附件）
 *           → attachment_sent_by_candidate → attachment_received → synced
 *           → resume_read_failed（待补读，下轮优先）
 *           → rejected（不匹配）
 *   异常态见 rhythm.Pause.*
 */
import fs from 'node:fs';
import path from 'node:path';

export const Status = {
  PENDING: 'pending',
  RESUME_READ: 'resume_read',
  ATTACHMENT_REQUESTED: 'attachment_requested',
  ATTACHMENT_SENT: 'attachment_sent_by_candidate',
  ATTACHMENT_RECEIVED: 'attachment_received',
  SYNCED: 'synced',
  RESUME_READ_FAILED: 'resume_read_failed',
  REJECTED: 'rejected',
};

/** 这些状态视为"本轮已完成"，默认不重扫（除非有新未读消息或用户点名）。 */
const TERMINAL = new Set([Status.SYNCED, Status.REJECTED]);
/** 这些状态下轮应"优先"处理（未完成/待补）。 */
const PRIORITY = new Set([
  Status.RESUME_READ_FAILED,
  Status.ATTACHMENT_REQUESTED,
  Status.ATTACHMENT_SENT,
]);

export class TaskMemory {
  /** @param {string} file 记忆文件路径，默认 ~/.opencli/boss-recruit/task-memory.json */
  constructor(file) {
    this.file = file || path.join(process.env.HOME || '.', '.opencli', 'boss-recruit', 'task-memory.json');
    this.data = { version: 1, candidates: {} };
    this._load();
  }
  _load() {
    try {
      if (fs.existsSync(this.file)) this.data = JSON.parse(fs.readFileSync(this.file, 'utf8'));
    } catch { /* 损坏则从空开始，不阻塞 */ }
    if (!this.data.candidates) this.data.candidates = {};
  }
  _save() {
    fs.mkdirSync(path.dirname(this.file), { recursive: true });
    fs.writeFileSync(this.file, JSON.stringify(this.data, null, 2));
  }

  get(uid) { return this.data.candidates[uid] || null; }

  /** upsert 一个候选人的字段，并立即落盘（崩了能续）。 */
  upsert(uid, patch) {
    const prev = this.data.candidates[uid] || { uid, status: Status.PENDING, rounds: 0 };
    const next = { ...prev, ...patch, uid, updated_at: new Date().toISOString() };
    this.data.candidates[uid] = next;
    this._save();
    return next;
  }

  /** 推进状态并落盘。 */
  setStatus(uid, status, extra = {}) { return this.upsert(uid, { status, ...extra }); }

  /**
   * 本轮是否需要处理该候选人。
   * @param {object} c 候选人（含 uid、可选 has_unread）
   * @param {object} opts { force:boolean 用户点名重扫 }
   */
  shouldProcess(c, opts = {}) {
    const rec = this.get(c.uid);
    if (!rec) return true;                         // 没见过 → 处理
    if (opts.force) return true;                   // 用户点名 → 处理
    if (c.has_unread) return true;                 // 有新未读 → 处理
    if (PRIORITY.has(rec.status)) return true;     // 未完成/待补 → 优先处理
    if (TERMINAL.has(rec.status)) return false;    // 已完成且无新消息 → 跳过
    return rec.status === Status.PENDING;          // 仍 pending → 处理
  }

  /** 把候选人列表按"本轮该处理 + 优先级"排序过滤。 */
  selectForRound(candidates, opts = {}) {
    const todo = candidates.filter((c) => this.shouldProcess(c, opts));
    // 优先级状态排前面
    todo.sort((a, b) => {
      const pa = PRIORITY.has(this.get(a.uid)?.status) ? 0 : 1;
      const pb = PRIORITY.has(this.get(b.uid)?.status) ? 0 : 1;
      return pa - pb;
    });
    return todo;
  }

  stats() {
    const all = Object.values(this.data.candidates);
    const by = {};
    for (const c of all) by[c.status] = (by[c.status] || 0) + 1;
    return { total: all.length, by };
  }
}

export default { Status, TaskMemory };
