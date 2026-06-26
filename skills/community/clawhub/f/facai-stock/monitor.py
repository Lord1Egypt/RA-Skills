"""股票价格监控：后台独立子进程，自动读取自选股文件，价格偏离超阈值时通过 openclaw 发送消息。"""

import argparse
import json
import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, time as dtime, timedelta, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

import config as _config

from quote import get_detail

_DEFAULT_INTERVAL = 10              # 秒
_DEFAULT_THRESHOLD = 2.0            # 百分比
_LOG_MAX_BYTES = 2 * 1024 * 1024    # 单个文件上限：2 MB
_LOG_BACKUP_COUNT = 5               # 最多保留 5 个轮转备份
_HERE = Path(__file__).parent
_DATA_DIR = _HERE / "data"
_PID_PATH = _DATA_DIR / "monitor.pid"
_WATCHLIST_PATH = _DATA_DIR / "watchlist.json"

# A股交易时段（北京时间 UTC+8）
_TZ_BEIJING = timezone(timedelta(hours=8))
_MORNING_START = dtime(9, 26)
_MORNING_END   = dtime(11, 31)
_AFTERNOON_START = dtime(12, 57)
_AFTERNOON_END   = dtime(15, 1)
_IDLE_SLEEP = 20   # 非交易时段轮询间隔（秒）

_logger = logging.getLogger("monitor")


# ---------------------------------------------------------------------------
# 内部工具
# ---------------------------------------------------------------------------

def _setup_logger(log_path: Path) -> None:
    """初始化滚动文件日志（仅在子进程中调用）。"""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        log_path,
        maxBytes=_LOG_MAX_BYTES,
        backupCount=_LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(message)s", datefmt="%H:%M:%S"
    ))
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)


def _log(msg: str) -> None:
    _logger.info(msg)


def _send_alert(
    target: str,
    name: str,
    code: str,
    price: float,
    prev: float,
    open_price: float,
) -> None:
    change_pct = (price - prev) / prev * 100
    from_open_pct = (price - open_price) / open_price * 100 if open_price > 0 else 0.0
    direction = "上涨" if change_pct > 0 else "下跌"
    msg = (
        f"【股价提醒】{name}（{code}）价格{direction} {abs(change_pct):.2f}%，"
        f"当前价 {price:.3f} 元（上次 {prev:.3f} 元）｜"
        f"今开 {open_price:.3f} 元，距开盘 {from_open_pct:+.2f}%"
    )
    subprocess.run(
        ["openclaw", "message", "send", "--target", target, "--message", msg],
        check=False,
    )
    _log(f"已发送提醒 → {msg}")


def _is_trading_time() -> bool:
    """判断当前北京时间是否处于A股交易时段（周一至周五，不含法定节假日）。"""
    now = datetime.now(_TZ_BEIJING)
    if now.weekday() >= 5:   # 周六=5，周日=6
        return False
    t = now.time()
    return (
        _MORNING_START <= t <= _MORNING_END
        or _AFTERNOON_START <= t <= _AFTERNOON_END
    )


def _read_watchlist() -> list[dict]:
    """从自选股文件读取列表，失败返回空列表。"""
    try:
        return json.loads(_WATCHLIST_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# ---------------------------------------------------------------------------
# 公开工具
# ---------------------------------------------------------------------------

def is_running() -> bool:
    """检查监控子进程是否仍在运行。"""
    if not _PID_PATH.exists():
        return False
    try:
        pid = int(_PID_PATH.read_text(encoding="utf-8").strip())
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


def stop_monitor() -> bool:
    """
    停止监控子进程。
    返回 True 表示成功发送终止信号，False 表示进程不存在或已停止。
    """
    if not _PID_PATH.exists():
        return False
    try:
        pid = int(_PID_PATH.read_text(encoding="utf-8").strip())
        os.kill(pid, signal.SIGKILL)
        _log(f"[monitor] 已发送终止信号  PID={pid}")
        return True
    except (OSError, ValueError):
        return False
    finally:
        _PID_PATH.unlink(missing_ok=True)


def restart_monitor(
    target: str = "",
    interval: int = _DEFAULT_INTERVAL,
    threshold: float = _DEFAULT_THRESHOLD,
) -> int:
    """
    重启监控子进程（先停止旧进程，再启动新进程）。
    target 未传时从 data/config.json 的 monitor_target 读取；仍为空则报错退出。
    返回新子进程 PID。
    """
    stop_monitor()
    return start_monitor(target, interval, threshold)


# ---------------------------------------------------------------------------
# 监控循环（运行于子进程）
# ---------------------------------------------------------------------------

def _monitor_loop(interval: int, threshold: float, target: str) -> None:
    last_prices: dict[str, float] = {}
    last_mtime: float = 0.0
    stocks: list[dict] = []
    was_trading = False
    target = target or _config.get("monitor_target") or ""
    if not target:
        raise ValueError(
            "monitor_target 未指定。请传入 target 参数，或预先配置：\n"
            "  import config; config.set('monitor_target', 'user:ou_xxx')"
        )
    _log(f"监控进程已启动，读取自选股文件，异动发送给 {target}")
    trading = _is_trading_time()
    if trading:
        _log("已进入交易时段，开始行情监控")
    else:
        _log("已进入非交易时段，暂停行情查询（等待开盘）")

    while True:
        # --- 交易时段门控 ---
        trading = _is_trading_time()
        if not trading:
            if was_trading:
                _log("循环开始，已进入非交易时段，暂停行情查询（等待开盘）")
                # last_prices.clear()   # 清空历史价，开盘后重新建立基准
            was_trading = False
            time.sleep(_IDLE_SLEEP)
            continue
        if not was_trading:
            _log("循环开始，已进入交易时段，开始行情监控")
        was_trading = True

        # --- 检测自选股文件变化，热加载 ---
        try:
            mtime = _WATCHLIST_PATH.stat().st_mtime
            if mtime != last_mtime:
                new_stocks = _read_watchlist()
                if new_stocks != stocks:
                    stocks = new_stocks
                    names = [s["name"] for s in stocks]
                    _log(f"自选股已更新：{names if names else '（空）'}")
                    # 移除已不在列表中的历史价格记录
                    active_codes = {s["code"] for s in stocks}
                    last_prices = {k: v for k, v in last_prices.items() if k in active_codes}
                last_mtime = mtime
        except FileNotFoundError:
            if stocks:
                stocks = []
                last_prices = {}
                _log("自选股文件已删除，暂停监控")

        if not stocks:
            time.sleep(interval)
            continue

        # --- 逐只查询 ---
        for stock in stocks:
            code = stock["code"]
            name = stock["name"]
            try:
                detail = get_detail(code)
                price = detail["最新价"]
                open_price = detail["今开"]
                from_open_pct = (
                    (price - open_price) / open_price * 100 if open_price > 0 else 0.0
                )

                if code in last_prices:
                    base = last_prices[code]
                    if base > 0:
                        change_pct = (price - base) / base * 100
                        if abs(change_pct) >= threshold:
                            _log(f"⚠  {name}({code}) 偏离基准 {change_pct:+.2f}%，触发提醒")
                            _send_alert(target, name, code, price, base, open_price)
                            last_prices[code] = price   # 以本次提醒价作为新基准
                        else:
                            _log(
                                f"{name}({code})  {price:.3f} 元  "
                                f"距基准 {change_pct:+.2f}%  "
                                f"今开 {open_price:.3f} 元  距开盘 {from_open_pct:+.2f}%"
                            )
                else:
                    _log(
                        f"{name}({code})  基准价 {price:.3f} 元  "
                        f"今开 {open_price:.3f} 元  距开盘 {from_open_pct:+.2f}%"
                    )
                    last_prices[code] = price   # 首次记录基准价

            except Exception as exc:
                _log(f"⚠  {name}({code}) 查询失败: {exc}")

        time.sleep(interval)


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------

def start_monitor(
    target: str = "",
    interval: int = _DEFAULT_INTERVAL,
    threshold: float = _DEFAULT_THRESHOLD,
) -> int:
    """
    启动独立后台子进程持续监控自选股价格。
    股票列表从 watchlist.json 动态读取，文件变化时自动热加载。

    参数：
        target    - openclaw 消息接收目标 ID。
                    未传或为空时从 data/config.json 的 monitor_target 读取；
                    仍为空则抛出 ValueError 退出。
        interval  - 查询间隔（秒），默认 10。
        threshold - 触发提醒的价格偏离幅度（%），默认 2.0。

    返回子进程 PID；日志写入 logs/monitor_<timestamp>.log，
    单文件上限 2 MB，最多保留 5 个轮转备份。
    """
    target = target or _config.get("monitor_target") or ""
    if not target:
        raise ValueError(
            "monitor_target 未指定。请传入 target 参数，或预先配置：\n"
            "  import config; config.set('monitor_target', 'user:ou_xxx')"
        )
    else:
        _config.set("monitor_target", target)
        _log(f"monitor_target 已更新为 {target}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = _HERE / "logs" / f"monitor_{ts}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--interval", str(interval),
        "--threshold", str(threshold),
        "--target", target,
        "--log", str(log_path),
    ]

    if sys.platform == "win32":
        proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        proc = subprocess.Popen(cmd, start_new_session=True)

    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    _PID_PATH.write_text(str(proc.pid), encoding="utf-8")
    _log(f"[monitor] 监控子进程已启动  PID={proc.pid}  日志→ {log_path}")
    return proc.pid


# ---------------------------------------------------------------------------
# 子进程入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    parser = argparse.ArgumentParser(description="股票价格监控后台进程")
    parser.add_argument("--interval", type=int, default=_DEFAULT_INTERVAL, help="查询间隔（秒）")
    parser.add_argument("--threshold", type=float, default=_DEFAULT_THRESHOLD, help="触发提醒的偏离阈值（%%）")
    parser.add_argument("--target", default='', help="openclaw 消息接收目标,没有配置的话需要传入，否则会报错退出")
    parser.add_argument("--log", default=_HERE / "logs" / f"monitor_{ts}.log", help="日志文件路径")
    args = parser.parse_args()

    _setup_logger(Path(args.log))
    _monitor_loop(args.interval, args.threshold, args.target)
