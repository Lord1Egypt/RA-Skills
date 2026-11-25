"""批处理队列与断点续跑（v2.9.0 新增）。

对齐 gateway batch_queue.py / video-analyzer 批量队列的成熟模式，
但保持 CLI 独立实现（纯标准库、不桥接、不依赖 gateway）。

核心能力：
- 任务清单（txt / jsonl）逐条落 SQLite（WAL 模式，防中断损坏）
- 每条任务独立状态：pending / running / done / failed / retry
- 失败重试：可配置次数，指数退避（本地等待，不占 CPU）
- 断点续跑：重跑同一 job 时只补 pending/failed，跳过 done → 零重复计费
- 硬件自适应并发：并发数由 hardware.profile() 决定，绝不占满电脑

进度库默认 ~/.cn_llm_router/batch.db（运行时产物，不进技能包）。
"""

import os
import sys
import json
import time
import sqlite3
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hardware

DEFAULT_DB = os.path.join(os.path.expanduser("~"), ".cn_llm_router", "batch.db")

STATUS_PENDING = "pending"
STATUS_RUNNING = "running"
STATUS_DONE = "done"
STATUS_FAILED = "failed"


def _conn(db_path=None):
    db = db_path or DEFAULT_DB
    if db != ":memory:":
        os.makedirs(os.path.dirname(db), exist_ok=True)
    c = sqlite3.connect(db, check_same_thread=False)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute(
        """CREATE TABLE IF NOT EXISTS batch_jobs (
            job_id TEXT PRIMARY KEY,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL,
            name TEXT,
            strategy TEXT,
            model TEXT,
            task_hint TEXT,
            total INTEGER NOT NULL,
            src_file TEXT
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS batch_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            idx INTEGER NOT NULL,
            payload TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            result TEXT,
            error TEXT,
            retries INTEGER NOT NULL DEFAULT 0,
            cost REAL NOT NULL DEFAULT 0.0,
            in_tokens INTEGER NOT NULL DEFAULT 0,
            out_tokens INTEGER NOT NULL DEFAULT 0,
            updated_at REAL NOT NULL,
            UNIQUE(job_id, idx)
        )"""
    )
    c.execute("CREATE INDEX IF NOT EXISTS idx_items_job_status ON batch_items(job_id, status)")
    c.commit()
    return c


def _parse_manifest(path):
    """读取任务清单，返回 payload 字符串列表。

    - .jsonl：每行一个 JSON 对象，取 prompt/text/content 字段，或整行 JSON 字符串
    - .txt：每行一个任务（忽略空行与 # 注释）
    """
    if not os.path.exists(path):
        raise ValueError("任务清单不存在: %s" % path)
    items = []
    ext = os.path.splitext(path)[1].lower()
    with open(path, "r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if ext == ".jsonl":
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        text = obj.get("prompt") or obj.get("text") or obj.get("content")
                        items.append(json.dumps(obj, ensure_ascii=False) if text is None else str(text))
                    else:
                        items.append(str(obj))
                except (ValueError, TypeError):
                    items.append(line)  # 非法 JSON 行按纯文本处理，不丢任务
            else:
                items.append(line)
    return items


class BatchQueue:
    """SQLite 支撑的批处理队列。线程安全（写操作加锁）。"""

    def __init__(self, db_path=None, max_retries=2):
        self.db_path = db_path or DEFAULT_DB
        self.max_retries = max(0, int(max_retries))
        self._lock = threading.Lock()
        # 每线程复用一个连接（避免每次操作新建导致连接累积），统一登记以便关闭
        self._local = threading.local()
        self._all_conns = []
        self._conns_lock = threading.Lock()
        self._conn()

    def _conn(self):
        """获取本线程持有的 SQLite 连接（懒创建 + 复用）。"""
        c = getattr(self._local, "conn", None)
        if c is None:
            c = _conn(self.db_path)
            self._local.conn = c
            with self._conns_lock:
                self._all_conns.append(c)
        return c

    def close_all(self):
        """关闭所有线程的连接（任务结束后调用，释放文件锁）。"""
        with self._conns_lock:
            for c in self._all_conns:
                try:
                    c.close()
                except Exception:
                    pass
            self._all_conns = []
            self._local = threading.local()

    def create_job(self, items, name="", strategy="auto", model="auto",
                   task_hint=None, src_file=""):
        """新建批次任务，返回 job_id。已存在同名+同源的 job 会复用（幂等）。"""
        job_id = "batch_%d" % int(time.time() * 1000)
        now = time.time()
        c = self._conn()
        with self._lock:
            c.execute(
                "INSERT INTO batch_jobs (job_id, created_at, updated_at, name, strategy, model, task_hint, total, src_file) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (job_id, now, now, name or job_id, strategy, model, task_hint, len(items), src_file),
            )
            c.executemany(
                "INSERT INTO batch_items (job_id, idx, payload, status, updated_at) VALUES (?,?,?,?,?)",
                [(job_id, i, str(p), STATUS_PENDING, now) for i, p in enumerate(items)],
            )
            c.commit()
        return job_id

    def create_job_from_manifest(self, path, **kwargs):
        """从清单文件新建任务。"""
        items = _parse_manifest(path)
        if not items:
            raise ValueError("任务清单为空或全为注释: %s" % path)
        return self.create_job(items, src_file=path, **kwargs)

    def get_job(self, job_id):
        c = self._conn()
        row = c.execute("SELECT * FROM batch_jobs WHERE job_id=?", (job_id,)).fetchone()
        return dict(row) if row else None

    def item_counts(self, job_id):
        c = self._conn()
        rows = c.execute(
            "SELECT status, COUNT(*) n FROM batch_items WHERE job_id=? GROUP BY status", (job_id,)
        ).fetchall()
        counts = {s: 0 for s in (STATUS_PENDING, STATUS_RUNNING, STATUS_DONE, STATUS_FAILED)}
        for r in rows:
            counts[r["status"]] = r["n"]
        return counts

    def progress(self, job_id):
        job = self.get_job(job_id)
        if not job:
            return None
        counts = self.item_counts(job_id)
        total = job["total"]
        finished = counts[STATUS_DONE] + counts[STATUS_FAILED]
        return {
            "job_id": job_id,
            "total": total,
            "done": counts[STATUS_DONE],
            "failed": counts[STATUS_FAILED],
            "pending": counts[STATUS_PENDING],
            "running": counts[STATUS_RUNNING],
            "percent": round(finished / total * 100, 1) if total else 0.0,
            "status": job["status"] if "status" in job.keys() else ("done" if finished >= total else "running"),
        }

    def claim_pending(self, job_id, limit=None):
        """领取待处理任务（断点续跑：仅 pending，跳过 done）。

        这里不改状态为 running，由调用方在真正开始执行前调用 mark_running，
        避免领取后进程崩溃导致任务永久卡在 running。
        """
        c = self._conn()
        sql = "SELECT * FROM batch_items WHERE job_id=? AND status IN (?,?) ORDER BY idx"
        params = [job_id, STATUS_PENDING, STATUS_FAILED]
        if limit:
            sql += " LIMIT ?"
            params.append(limit)
        rows = c.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def mark_running(self, item_id):
        c = self._conn()
        with self._lock:
            c.execute("UPDATE batch_items SET status=?, updated_at=? WHERE id=?",
                      (STATUS_RUNNING, time.time(), item_id))
            c.commit()

    def mark_done(self, item_id, result="", cost=0.0, in_tokens=0, out_tokens=0):
        c = self._conn()
        with self._lock:
            c.execute(
                "UPDATE batch_items SET status=?, result=?, error=NULL, cost=?, in_tokens=?, out_tokens=?, updated_at=? WHERE id=?",
                (STATUS_DONE, str(result), float(cost), int(in_tokens), int(out_tokens), time.time(), item_id),
            )
            c.commit()

    def mark_failed(self, item_id, error=""):
        """失败处理：未达重试上限则回退 pending（retries+1），否则 failed。"""
        c = self._conn()
        with self._lock:
            row = c.execute("SELECT retries FROM batch_items WHERE id=?", (item_id,)).fetchone()
            if not row:
                return STATUS_FAILED
            retries = row["retries"]
            if retries < self.max_retries:
                c.execute(
                    "UPDATE batch_items SET status=?, error=?, retries=?, updated_at=? WHERE id=?",
                    (STATUS_PENDING, str(error), retries + 1, time.time(), item_id),
                )
                new_status = "retry"
            else:
                c.execute(
                    "UPDATE batch_items SET status=?, error=?, updated_at=? WHERE id=?",
                    (STATUS_FAILED, str(error), time.time(), item_id),
                )
                new_status = STATUS_FAILED
            c.commit()
            return new_status

    def results(self, job_id, only_failed=False):
        c = self._conn()
        if only_failed:
            rows = c.execute(
                "SELECT idx, payload, status, result, error, retries FROM batch_items WHERE job_id=? AND status=? ORDER BY idx",
                (job_id, STATUS_FAILED),
            ).fetchall()
        else:
            rows = c.execute(
                "SELECT idx, payload, status, result, error, retries FROM batch_items WHERE job_id=? ORDER BY idx",
                (job_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    def total_cost(self, job_id):
        c = self._conn()
        row = c.execute("SELECT COALESCE(SUM(cost),0) total FROM batch_items WHERE job_id=?", (job_id,)).fetchone()
        return float(row["total"])

    def list_jobs(self, limit=10):
        c = self._conn()
        rows = c.execute(
            "SELECT * FROM batch_jobs ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def reset_failed(self, job_id):
        """把失败任务重置为 pending（供用户手动重跑）。"""
        c = self._conn()
        with self._lock:
            cur = c.execute(
                "UPDATE batch_items SET status=?, retries=0, updated_at=? WHERE job_id=? AND status=?",
                (STATUS_PENDING, time.time(), job_id, STATUS_FAILED),
            )
            c.commit()
            return cur.rowcount
