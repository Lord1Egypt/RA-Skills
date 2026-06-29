"""_base.py — 数据源公共基类

所有 fetcher 继承 BaseFetcher，实现三个钩子：fetch_raw / parse / validate。
基类负责：重试、原始存档、_status.json 写入、告警触发。

CLI 模式：python3 <module>.py --today YYYY-MM-DD --output-dir /path
输出 JSON status 到 stdout: {"status":"ok","records":N} 或 {"status":"rejected","reason":"..."}
"""
import os, json, time, logging, sys, argparse
from datetime import datetime, date
from pathlib import Path
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

RESEARCH_DATA_ROOT = os.path.expanduser(os.environ.get("RESEARCH_DATA_ROOT", "~/research-data"))
DATA_DIR = os.path.join(RESEARCH_DATA_ROOT, "data")
STATE_DIR = os.path.join(os.path.dirname(__file__), "..", "state")

# Retry config
MAX_RETRIES = 3
RETRY_DELAYS = [2, 8, 30]  # exponential backoff


class FetchResult:
    """三态结果"""
    def __init__(self, status: str, data=None, reason: str = "", records: int = 0):
        assert status in ("ok", "unavailable", "rejected")
        self.status = status
        self.data = data
        self.reason = reason
        self.records = records

    def to_status_dict(self):
        d = {"status": self.status}
        if self.status == "ok":
            d["records"] = self.records
        else:
            d["reason"] = self.reason
        return d


class BaseFetcher(ABC):
    """所有数据源的基类"""

    name: str = "base"  # override in subclass

    def __init__(self, today: str = None):
        self.today = today or date.today().isoformat()
        self.raw_dir = os.path.join(DATA_DIR, "raw", self.today)
        self.daily_dir = os.path.join(DATA_DIR, "daily", self.today)
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.daily_dir, exist_ok=True)

    @abstractmethod
    def fetch_raw(self) -> str | bytes | None:
        """抓取原始内容。网络失败返回 None。"""
        pass

    @abstractmethod
    def parse(self, raw) -> list[dict]:
        """解析原始内容为结构化数据。解析失败 raise ValueError。"""
        pass

    @abstractmethod
    def validate(self, records: list[dict]) -> bool:
        """校验记录。失败 raise ValueError(reason)。"""
        pass

    def save_raw(self, raw, suffix="json"):
        """保存原始数据到 raw/ 目录"""
        path = os.path.join(self.raw_dir, f"{self.name}.{suffix}")
        mode = "wb" if isinstance(raw, bytes) else "w"
        with open(path, mode) as f:
            f.write(raw)
        return path

    def run(self) -> FetchResult:
        """执行完整流程：fetch → save_raw → parse → validate → 输出"""
        # Step 1: Fetch with retry
        raw = None
        for attempt in range(MAX_RETRIES):
            try:
                raw = self.fetch_raw()
                if raw is not None:
                    break
            except Exception as e:
                logger.warning(f"[{self.name}] fetch attempt {attempt+1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAYS[attempt])

        if raw is None:
            return FetchResult("unavailable", reason=f"Failed after {MAX_RETRIES} retries")

        # Step 2: Save raw
        try:
            suffix = "html" if isinstance(raw, str) and raw.strip().startswith("<") else "json"
            self.save_raw(raw, suffix)
        except Exception as e:
            logger.warning(f"[{self.name}] save_raw failed: {e}")

        # Step 3: Parse (no retry on parse failure)
        try:
            records = self.parse(raw)
        except Exception as e:
            return FetchResult("rejected", reason=f"Parse failed: {e}")

        # Step 4: Validate (no retry)
        try:
            self.validate(records)
        except Exception as e:
            return FetchResult("rejected", reason=f"Validation failed: {e}")

        # Step 5: Save processed data
        output_path = os.path.join(self.daily_dir, f"{self.name}.json")
        with open(output_path, "w") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

        return FetchResult("ok", data=records, records=len(records))


def cli_main(fetcher_class):
    """Standard CLI entry point for subprocess isolation.

    Usage in each module:
        if __name__ == '__main__':
            from _base import cli_main
            cli_main(Fetcher)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--today', default=date.today().isoformat())
    parser.add_argument('--output-dir', default=None)
    args = parser.parse_args()

    fetcher = fetcher_class(today=args.today)
    if args.output_dir:
        fetcher.daily_dir = args.output_dir
        os.makedirs(args.output_dir, exist_ok=True)

    result = fetcher.run()
    status = result.to_status_dict()
    print(json.dumps(status, ensure_ascii=False))
    sys.exit(0 if result.status == "ok" else 1)
