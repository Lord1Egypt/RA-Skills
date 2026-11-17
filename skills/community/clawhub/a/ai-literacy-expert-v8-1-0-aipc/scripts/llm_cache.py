"""
llm_cache.py - V7-AIPC LLM 鎺悊缂撳瓨锛圴7.3.2 鏀硅繘4 鍗囩骇鐗堬級锛? 澶?TTL + 涓?work_summary 鑱斿姩璁板綍鍛戒腑鐜?

璁捐鐩爣锛?
  - 鐩稿悓 abstract_data 澶氭鎺悊鏃跺懡涓湰鍦扮紦瀛橈紝閬垮厤閲嶅鏈湴鎺悊
  - SQLite 瀛樺偍锛岄浂渚濊禆锛堟爣鍑嗗簱 sqlite3锛?
  - TTL 榛樿 7 澶紙涓?V7 鍗忚鏁版嵁淇濈暀鏈熶竴鑷达級
  - 璺繘绋嬪畨鍏紙澶?worker 鍚屾椂璇诲啓锛?
  - 缂撳瓨閿?= SHA256(abstract_data + decision_type + model_id)

CLI:
    python llm_cache.py --stats          # 缂撳瓨缁熻
    python llm_cache.py --clear         # 娓呯缂撳瓨
    python llm_cache.py --prune 7       # 娓呯悊 7 澶墠鏉#洰
"""
from __future__ import annotations
__version__ = "8.1.0-aipc"  # V8.1-AIPC: 每次工作自动输出本地/云端对比 + 全互动控件完整性门控

import hashlib
import json
import os
import sqlite3
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

# 寮哄埗 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from log_util import get_logger

log = get_logger("llm_cache")

DEFAULT_DB_DIR = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".openvino" / "cache"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "llm_cache.db"
DEFAULT_TTL_DAYS = 7


class LLMCache:
    """LLM 推理结果缓存（基于 SQLite）."""

    def __init__(
        self,
        db_path: Path | None = None,
        ttl_seconds: int = DEFAULT_TTL_DAYS * 86400,
    ):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds
        self._init_db()
        log.info(f"[llm_cache] 初始化 db={self.db_path} ttl={ttl_seconds}s")

    def _init_db(self) -> None:
        with self._conn() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS cache ("
                "cache_key TEXT PRIMARY KEY, "
                "abstract_hash TEXT NOT NULL, "
                "decision_type TEXT NOT NULL, "
                "model_id TEXT NOT NULL, "
                "result_json TEXT NOT NULL, "
                "cost_usd REAL DEFAULT 0.0, "
                "created_at INTEGER NOT NULL, "
                "last_hit_at INTEGER, "
                "hit_count INTEGER DEFAULT 0)"
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_created ON cache(created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_abstract ON cache(abstract_hash)")

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(str(self.db_path), timeout=10.0, isolation_level=None)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def make_key(abstract_data: dict, decision_type: str, model_id: str) -> tuple[str, str]:
        """生成缓存键 = (cache_key, abstract_hash).
        cache_key 用于精确查找,abstract_hash 用于统计命中率.
        """
        # 排序键保证 dict 顺序无关
        canonical = json.dumps(abstract_data, sort_keys=True, ensure_ascii=False)
        abstract_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
        cache_key_src = f"{abstract_hash}|{decision_type}|{model_id}"
        cache_key = hashlib.sha256(cache_key_src.encode("utf-8")).hexdigest()
        return cache_key, abstract_hash

    def get(self, abstract_data: dict, decision_type: str, model_id: str) -> Optional[dict]:
        """鏌缂撳瓨銆傚懡涓繑鍥?result锛屾湭鍛戒腑杩斿洖 None銆?"""
        cache_key, _ = self.make_key(abstract_data, decision_type, model_id)
        now = int(time.time())
        with self._conn() as conn:
            row = conn.execute(
                "SELECT result_json, created_at FROM cache WHERE cache_key = ?",
                (cache_key,),
            ).fetchone()
            if row is None:
                return None
            result_json, created_at = row
            if now - created_at > self.ttl_seconds:
                log.info(f"[llm_cache] 杩囨湡 key={cache_key[:12]}...")
                conn.execute("DELETE FROM cache WHERE cache_key = ?", (cache_key,))
                return None
            # 鍛戒腑锛氭洿鏂?last_hit_at + hit_count
            conn.execute(
                "UPDATE cache SET last_hit_at = ?, hit_count = hit_count + 1 WHERE cache_key = ?",
                (now, cache_key),
            )
            log.info(f"[llm_cache] 鍛戒腑 key={cache_key[:12]}...")
            return json.loads(result_json)

    def put(
        self,
        abstract_data: dict,
        decision_type: str,
        model_id: str,
        result: dict,
        cost_usd: float = 0.0,
    ) -> None:
        """写入缓存."""
        cache_key, abstract_hash = self.make_key(abstract_data, decision_type, model_id)
        now = int(time.time())
        result_json = json.dumps(result, ensure_ascii=False)
        with self._conn() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO cache
                   (cache_key, abstract_hash, decision_type, model_id,
                    result_json, cost_usd, created_at, last_hit_at, hit_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?, NULL, 0)""",
                (cache_key, abstract_hash, decision_type, model_id,
                 result_json, cost_usd, now),
            )
        log.info(f"[llm_cache] 鍐欏叆 key={cache_key[:12]}... cost=${cost_usd}")

    def prune(self, older_than_seconds: int) -> int:
        """娓呯悊瓒呰繃 N 绉掔殑鏉#洰锛岃繑鍥炴竻鐞嗘潯鏁般?"""
        now = int(time.time())
        cutoff = now - older_than_seconds
        with self._conn() as conn:
            cur = conn.execute("DELETE FROM cache WHERE created_at < ?", (cutoff,))
            return cur.rowcount

    def clear(self) -> int:
        """娓呯鍏儴缂撳瓨锛岃繑鍥炴竻鐞嗘潯鏁般?"""
        with self._conn() as conn:
            cur = conn.execute("DELETE FROM cache")
            return cur.rowcount

    def stats(self) -> dict:
        """杩斿洖缂撳瓨缁熻锛氭潯鐩暟銆佹?hit_count銆佸钩鍧囨垚鏈瓑銆?"""
        with self._conn() as conn:
            row = conn.execute("""
                SELECT
                    COUNT(*) AS total,
                    COALESCE(SUM(hit_count), 0) AS total_hits,
                    COALESCE(AVG(cost_usd), 0.0) AS avg_cost,
                    COALESCE(SUM(cost_usd), 0.0) AS total_cost
                FROM cache
            """).fetchone()
            total, total_hits, avg_cost, total_cost = row
            return {
                "total_entries": total,
                "total_hits": total_hits,
                "hit_rate": total_hits / total if total > 0 else 0.0,
                "avg_cost_usd": round(avg_cost, 6),
                "total_cost_usd": round(total_cost, 6),
                "db_path": str(self.db_path),
                "ttl_days": self.ttl_seconds // 86400,
            }


# 鍏眬鍗曚緥锛堥粯璁?db锛?
_default_cache: Optional[LLMCache] = None


def get_cache() -> LLMCache:
    """获取默认缓存单例."""
    global _default_cache
    if _default_cache is None:
        _default_cache = LLMCache()
    return _default_cache


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LLM 推理缓存管理")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    parser.add_argument("--clear", action="store_true", help="清空全部")
    parser.add_argument("--prune", type=int, metavar="DAYS", help="清理 N 天前的条目")
    args = parser.parse_args()

    cache = get_cache()
    if args.stats:
        s = cache.stats()
        for k, v in s.items():
            print(f"{k:20s} : {v}")
    elif args.clear:
        n = cache.clear()
        print(f"清理 {n} 个条目")
    elif args.prune:
        n = cache.prune(args.prune * 86400)
        print(f"清理 {n} 个超过 {args.prune} 天的条目")
    else:
        parser.print_help()

