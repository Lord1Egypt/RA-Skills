"""
clawtrader.py

ClawTrader CLI — OpenClaw Agent 调用的统一入口。

所有输出为 UTF-8 JSON（单行），方便 Agent 解析。

用法示例：
    python clawtrader.py setup
    python clawtrader.py config
    python clawtrader.py start
    python clawtrader.py stop
    python clawtrader.py ping
    python clawtrader.py subscribe IF2505,rb2510
    python clawtrader.py order --exchange CFFEX --instrument IF2505 --dir buy --offset open --vol 2 --price-type market
    python clawtrader.py cancel --order-sys-id 123456 --exchange CFFEX --instrument IF2505
    python clawtrader.py position
    python clawtrader.py account
    python clawtrader.py trades
    python clawtrader.py orders
    python clawtrader.py alert --instrument IF2505 --cond price_ge --threshold 6000 --msg "IF触及6000"
    python clawtrader.py alert-order --instrument IF2505 --cond price_le --threshold 5800 --exchange CFFEX --dir sell --offset open --vol 1 --price-type market
    python clawtrader.py list-alerts
    python clawtrader.py remove-alert c123
    python clawtrader.py poll
    python clawtrader.py report
    python clawtrader.py price IF2505
    python clawtrader.py cancel-all
    python clawtrader.py schedule-order --time 09:25 --exchange CFFEX --instrument IF2505 --dir buy --offset open --vol 1 --price-type market
    python clawtrader.py schedule-login --time 08:55
    python clawtrader.py list-schedules
    python clawtrader.py remove-schedule s123
"""

import sys
import json
import os
import socket
import argparse
import subprocess
import platform
import tempfile
import time
from pathlib import Path

_SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(_SCRIPTS))
import state
from accounts import AccountPaths, AccountRegistry, AccountRegistryError

_TIMEOUT = 10.0   # CLI 等待 daemon 响应超时秒数
_REGISTRY: AccountRegistry | None = None
_INSTANCE: AccountPaths | None = None


def _require_instance() -> AccountPaths:
    if _INSTANCE is None:
        raise RuntimeError("尚未选择账户实例")
    return _INSTANCE


# ------------------------------------------------------------------ #
#  与 daemon 通信                                                      #
# ------------------------------------------------------------------ #

def _send(cmd: dict) -> dict:
    instance = _require_instance()
    cmd = {**cmd, "account_id": instance.account_id}
    port = state.get_port()
    if not port:
        return {"ok": False, "account_id": instance.account_id,
                "error": "daemon 未运行，请先执行 start"}
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=_TIMEOUT)
        s.sendall((json.dumps(cmd, ensure_ascii=False) + "\n").encode())
        buf = b""
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
            if buf.endswith(b"\n"):
                break
        s.close()
        return json.loads(buf.decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


# ------------------------------------------------------------------ #
#  配置向导                                                            #
# ------------------------------------------------------------------ #

def _config_wizard() -> None:
    """交互式引导用户填写账户信息并写入 config.json。"""
    import getpass
    instance = _require_instance()
    cfg_path = instance.config_file

    print()
    print("=" * 54)
    print(f"  ClawTrader 账户配置向导 · {instance.display_name}")
    print("  括号内为填写示例，直接回车使用默认值")
    print("=" * 54)

    def ask(prompt: str, default: str = "", secret: bool = False) -> str:
        hint = f" [{default}]" if default else ""
        full = f"  {prompt}{hint}: "
        while True:
            val = (getpass.getpass(full) if secret else input(full)).strip()
            if val:
                return val
            if default:
                return default
            print("    ↑ 此项不能为空，请重新输入")

    cfg: dict = {}
    cfg["broker_id"]   = ask("经纪商代码  (仿真填 9999)")
    cfg["user_id"]     = ask("投资者账号")
    cfg["td_password"] = ask("交易密码", secret=True)
    md_pw = getpass.getpass("  行情密码  (与交易密码相同时直接回车): ").strip()
    cfg["md_password"] = md_pw if md_pw else cfg["td_password"]
    cfg["app_id"]      = ask("AppID      (如 client_test_1)")
    cfg["auth_code"]   = ask("认证码")
    cfg["td_front"]    = ask("交易前置   (如 tcp://180.168.146.187:10201)")
    cfg["md_front"]    = ask("行情前置   (如 tcp://180.168.146.187:10211)")
    default_inst = input("  默认订阅合约 (逗号分隔，不订阅直接回车): ").strip()
    cfg["default_instruments"] = default_inst
    cfg["account_id"] = instance.account_id
    cfg["daemon_port"] = instance.daemon_port or 17777

    payload = json.dumps(cfg, ensure_ascii=False, indent=2) + "\n"
    # Replace atomically so an interrupted configuration cannot leave a
    # partially-written credential file behind.
    if cfg_path.exists():
        try:
            if cfg_path.read_text(encoding="utf-8") == payload:
                print(f"\n  ✓ 配置未变化，保留 {cfg_path.name}")
            else:
                _atomic_write_text(cfg_path, payload)
                print(f"\n  ✓ 配置已保存至 {cfg_path.name}")
        except OSError:
            _atomic_write_text(cfg_path, payload)
            print(f"\n  ✓ 配置已保存至 {cfg_path.name}")
    else:
        _atomic_write_text(cfg_path, payload)
        print(f"\n  ✓ 配置已保存至 {cfg_path.name}")
    print("=" * 54)
    print()


def _atomic_write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


def _try_start_lock() -> bool:
    """Acquire a short-lived cross-process guard for daemon startup."""
    lock_file = _require_instance().start_lock_file
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(2):
        try:
            fd = os.open(
                lock_file,
                os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                0o600,
            )
        except FileExistsError:
            try:
                owner_pid = int(lock_file.read_text(encoding="ascii").strip())
                if owner_pid > 0:
                    os.kill(owner_pid, 0)
                    return False
            except ProcessLookupError:
                pass
            except (FileNotFoundError, ValueError, OSError):
                return False
            try:
                lock_file.unlink()
            except FileNotFoundError:
                pass
            continue
        else:
            try:
                os.write(fd, str(os.getpid()).encode("ascii"))
            finally:
                os.close(fd)
            return True
    return False


def _release_start_lock() -> None:
    lock_file = _require_instance().start_lock_file
    try:
        lock_file.unlink()
    except FileNotFoundError:
        pass


# ------------------------------------------------------------------ #
#  子命令实现                                                          #
# ------------------------------------------------------------------ #

def cmd_start(args) -> None:
    instance = _require_instance()
    if state.is_running():
        _out({"ok": True, "already_running": True, "pid": state.read().get("pid")})
        return

    if not _try_start_lock():
        # Another CLI process is starting.  Wait briefly for its state file,
        # then report the resulting daemon rather than spawning a second one.
        for _ in range(100):
            if state.is_running():
                _out({"ok": True, "already_running": True,
                      "pid": state.read().get("pid")})
                return
            time.sleep(0.1)
        _out({"ok": False, "error": "另一个 start 请求仍在执行，请稍后重试"})
        return

    try:
        # Recheck after acquiring the guard to close the check-then-start race.
        if state.is_running():
            _out({"ok": True, "already_running": True, "pid": state.read().get("pid")})
            return

        # 账户未配置时先运行向导
        cfg_path = instance.config_file
        if not cfg_path.exists():
            print("尚未配置账户，即将启动配置向导...")
            try:
                _config_wizard()
            except (KeyboardInterrupt, EOFError):
                print("\n配置已取消，daemon 未启动。")
                return

        daemon_py = _SCRIPTS / "daemon.py"
        daemon_cmd = [sys.executable, str(daemon_py), "--account", instance.account_id]
        if _REGISTRY and _REGISTRY.path.exists():
            daemon_cmd.extend(["--registry", str(_REGISTRY.path)])
        proc = subprocess.Popen(
            daemon_cmd,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
        )
        # 等待 daemon 写 state 文件
        for _ in range(30):
            time.sleep(0.5)
            if state.is_running():
                _out({"ok": True, "pid": proc.pid, "msg": "daemon 已启动"})
                return
        _out({"ok": False, "account_id": instance.account_id,
              "error": f"daemon 启动超时，请检查日志 {instance.log_file}"})
    finally:
        _release_start_lock()


def cmd_stop(args) -> None:
    if not state.is_running():
        _out({"ok": True, "already_stopped": True})
        return
    cmd = {"cmd": "stop"}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_ping(args) -> None:
    _out(_send({"cmd": "ping"}))


def cmd_accounts(args) -> None:
    registry = _REGISTRY or AccountRegistry()
    rows = []
    for item in registry.public_accounts():
        row = dict(item)
        if row["enabled"]:
            paths = registry.resolve(row["account_id"])
            running = state.is_running_path(paths.state_file)
            daemon_state = state.read_path(paths.state_file)
            row.update({
                "running": running,
                "pid": daemon_state.get("pid") if running else None,
                "port": daemon_state.get("port") if running else paths.daemon_port,
            })
        rows.append(row)
    _out({"ok": True, "accounts": rows})


def cmd_subscribe(args) -> None:
    instruments = args.instruments
    cmd = {"cmd": "subscribe", "instruments": instruments}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_unsubscribe(args) -> None:
    cmd = {"cmd": "unsubscribe", "instruments": args.instruments}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_order(args) -> None:
    cmd = {
        "cmd":        "order",
        "exchange":   args.exchange,
        "instrument": args.instrument,
        "direction":  args.dir,       # buy | sell
        "offset":     args.offset,    # open | close | close_today | close_yesterday
        "price_type": args.price_type,# limit | market
        "price":      args.price,
        "volume":     args.vol,
        "time_cond":  args.time_cond,
        "vol_cond":   args.vol_cond,
    }
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_cancel(args) -> None:
    cmd = {
        "cmd":          "cancel",
        "exchange":     args.exchange,
        "instrument":   args.instrument,
        "order_sys_id": args.order_sys_id or "",
        "order_ref":    args.order_ref    or "",
    }
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_position(args) -> None:
    _out(_send({"cmd": "qry_position", "instrument": args.instrument or ""}))


def cmd_account(args) -> None:
    _out(_send({"cmd": "qry_account"}))


def cmd_trades(args) -> None:
    _out(_send({"cmd": "qry_trades"}))


def cmd_orders(args) -> None:
    _out(_send({"cmd": "qry_orders"}))


def cmd_alert(args) -> None:
    """设置价格告警（只推消息，不下单）"""
    cond = {
        "instrument": args.instrument,
        "cond_type":  args.cond,       # price_ge | price_le | pct_change_ge | pct_change_le
        "threshold":  args.threshold,
        "action":     "alert",
        "msg":        args.msg or f"{args.instrument} 触发条件 {args.cond}={args.threshold}",
    }
    cmd = {"cmd": "add_alert", "condition": cond}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_alert_order(args) -> None:
    """设置条件单（触发时自动下单）"""
    cond = {
        "instrument": args.instrument,
        "cond_type":  args.cond,
        "threshold":  args.threshold,
        "action":     "order",
        "order_params": {
            "exchange":   args.exchange,
            "instrument": args.instrument,
            "direction":  args.dir,
            "offset":     args.offset,
            "price_type": args.price_type,
            "price":      args.price,
            "volume":     args.vol,
        },
    }
    cmd = {"cmd": "add_alert", "condition": cond}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_list_alerts(args) -> None:
    _out(_send({"cmd": "list_alerts"}))


def cmd_remove_alert(args) -> None:
    cmd = {"cmd": "remove_alert", "cond_id": args.cond_id}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_poll(args) -> None:
    """拉取 daemon 推送的事件（告警、成交等）"""
    _out(_send({"cmd": "poll_events", "after_seq": args.after_seq,
                "limit": args.limit}))


def cmd_report(args) -> None:
    _out(_send({"cmd": "report"}))


def cmd_price(args) -> None:
    """查询合约最新行情（来自 Tick 缓存）"""
    _out(_send({"cmd": "qry_price", "instrument": args.instrument}))


def cmd_cancel_all(args) -> None:
    """批量撤销所有未成交委托"""
    cmd = {"cmd": "cancel_all"}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_schedule_order(args) -> None:
    """添加定时报单任务"""
    sched = {
        "type": "order",
        "time": args.time,
        "order_params": {
            "exchange":   args.exchange,
            "instrument": args.instrument,
            "direction":  args.dir,
            "offset":     args.offset,
            "price_type": args.price_type,
            "price":      args.price,
            "volume":     args.vol,
            "time_cond":  args.time_cond,
            "vol_cond":   args.vol_cond,
        },
    }
    cmd = {"cmd": "add_schedule", "schedule": sched}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_schedule_login(args) -> None:
    """添加定时登录任务"""
    sched = {
        "type": "login",
        "time": args.time,
    }
    cmd = {"cmd": "add_schedule", "schedule": sched}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_list_schedules(args) -> None:
    _out(_send({"cmd": "list_schedules"}))


def cmd_remove_schedule(args) -> None:
    cmd = {"cmd": "remove_schedule", "schedule_id": args.schedule_id}
    if args.idempotency_key:
        cmd["idempotency_key"] = args.idempotency_key
    _out(_send(cmd))


def cmd_config(args) -> None:
    """重新配置账户信息（会覆盖已有 config.json）"""
    try:
        _config_wizard()
        _out({"ok": True, "msg": "配置已更新，下次启动 daemon 时生效"})
    except (KeyboardInterrupt, EOFError):
        print("\n配置已取消。")


def cmd_setup(args) -> None:
    """强制重新编译 ctp_bridge（升级 SDK 或修复编译问题后使用）"""
    system = platform.system()
    bridge_dir = _SCRIPTS / "bridge"
    lib_names = {
        "Windows": "ctp_bridge.dll",
        "Darwin": "libctp_bridge.dylib",
        "Linux": "libctp_bridge.so",
    }
    lib_path = _SCRIPTS / lib_names.get(system, "")
    if system in lib_names and not args.force and lib_path.exists():
        _out({"ok": True, "already_configured": True,
              "msg": f"ctp_bridge 已存在: {lib_path.name}"})
        return
    if system == "Windows":
        cmd = ["cmd", "/c", str(bridge_dir / "build.bat")]
    elif system == "Darwin":
        cmd = ["bash", str(bridge_dir / "build_macos.sh")]
    elif system == "Linux":
        cmd = ["bash", str(bridge_dir / "build_linux.sh")]
    else:
        _out({"ok": False, "error": f"不支持的平台: {system}"})
        return

    print(f"[ClawTrader] 正在编译 ctp_bridge ({system})...", flush=True)
    result = subprocess.run(cmd)
    if result.returncode == 0:
        _out({"ok": True, "msg": "ctp_bridge 编译完成"})
    else:
        _out({"ok": False, "error": f"编译失败（exit={result.returncode}），请检查上方输出"})


# ------------------------------------------------------------------ #
#  参数解析                                                            #
# ------------------------------------------------------------------ #

def _add_order_args(p):
    p.add_argument("--exchange",    required=True,  help="交易所: SHFE/DCE/CZCE/CFFEX/INE/GFEX")
    p.add_argument("--instrument",  required=True,  help="合约代码, 如 IF2505")
    p.add_argument("--dir",         required=True,  choices=["buy","sell"])
    p.add_argument("--offset",      default="open", choices=["open","close","close_today","close_yesterday"])
    p.add_argument("--price-type",  dest="price_type", default="limit", choices=["limit","market"])
    p.add_argument("--price",       type=float, default=0.0)
    p.add_argument("--vol",         type=int,   required=True)
    p.add_argument("--time-cond",   dest="time_cond", default="gfd", choices=["gfd","ioc"])
    p.add_argument("--vol-cond",    dest="vol_cond",  default="any", choices=["any","all"])
    p.add_argument("--idempotency-key", dest="idempotency_key", default="",
                   help="幂等键；省略时由规范化请求自动生成")


def _add_alert_trigger_args(p, add_instrument=True):
    if add_instrument:
        p.add_argument("--instrument", required=True)
    p.add_argument("--cond",       required=True,
                   choices=["price_ge","price_le","pct_change_ge","pct_change_le"])
    p.add_argument("--threshold",  required=True, type=float)


def _add_idempotency_arg(p):
    p.add_argument("--idempotency-key", dest="idempotency_key", default="",
                   help="幂等键；省略时由规范化请求自动生成")


def build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="clawtrader", description="ClawTrader CLI")
    root.add_argument("--account", default="", help="账户别名，如 A/B/C")
    root.add_argument("--registry", default="", help="账户注册表路径")
    sub  = root.add_subparsers(dest="subcmd", required=True)

    # setup / config
    p = sub.add_parser("setup", help="编译 ctp_bridge（已存在时默认跳过）")
    p.add_argument("--force", action="store_true", help="明确要求重新编译")
    sub.add_parser("config", help="重新配置账户信息")
    sub.add_parser("accounts", help="列出全部账户及实例状态")

    # start / stop / ping
    sub.add_parser("start", help="启动 daemon（账户未配置时自动引导）")
    p = sub.add_parser("stop", help="停止 daemon")
    _add_idempotency_arg(p)
    sub.add_parser("ping",  help="检测 daemon 状态")

    # subscribe / unsubscribe
    p = sub.add_parser("subscribe", help="订阅行情")
    p.add_argument("instruments", help="逗号分隔合约, 如 IF2505,rb2510")
    _add_idempotency_arg(p)

    p = sub.add_parser("unsubscribe", help="退订行情")
    p.add_argument("instruments")
    _add_idempotency_arg(p)

    # order
    p = sub.add_parser("order", help="报单")
    _add_order_args(p)

    # cancel
    p = sub.add_parser("cancel", help="撤单")
    p.add_argument("--exchange",      default="")
    p.add_argument("--instrument",    default="")
    p.add_argument("--order-sys-id",  dest="order_sys_id", default="", help="通过 OrderSysID 撤单")
    p.add_argument("--order-ref",     dest="order_ref",    default="", help="通过 OrderRef 撤单")
    _add_idempotency_arg(p)

    # position / account
    p = sub.add_parser("position", help="查持仓（实时向 CTP 查询）")
    p.add_argument("--instrument", default="", help="为空则查全部")

    sub.add_parser("account", help="查资金（实时向 CTP 查询）")
    sub.add_parser("trades",  help="查今日成交（实时向 CTP 查询）")
    sub.add_parser("orders",  help="查委托（实时向 CTP 查询）")

    # alert
    p = sub.add_parser("alert", help="设置价格告警")
    _add_alert_trigger_args(p)
    p.add_argument("--msg", default="", help="告警消息文本")
    _add_idempotency_arg(p)

    # alert-order：--instrument 由 _add_order_args 提供，避免重复注册
    p = sub.add_parser("alert-order", help="设置条件单")
    _add_alert_trigger_args(p, add_instrument=False)
    _add_order_args(p)

    sub.add_parser("list-alerts", help="查看所有条件")

    p = sub.add_parser("remove-alert", help="删除条件")
    p.add_argument("cond_id")
    _add_idempotency_arg(p)

    p = sub.add_parser("poll", help="读取指定游标之后的事件")
    p.add_argument("--after-seq", type=int, default=0)
    p.add_argument("--limit", type=int, default=500)
    sub.add_parser("report", help="生成收盘日报")

    # price
    p = sub.add_parser("price", help="查询合约最新行情")
    p.add_argument("instrument", help="合约代码, 如 IF2505")

    # cancel-all
    p = sub.add_parser("cancel-all", help="批量撤销所有未成交委托")
    _add_idempotency_arg(p)

    # schedule-order
    p = sub.add_parser("schedule-order", help="定时报单")
    p.add_argument("--time", required=True, help="触发时间 HH:MM, 如 09:25")
    _add_order_args(p)

    # schedule-login
    p = sub.add_parser("schedule-login", help="定时登录")
    p.add_argument("--time", required=True, help="触发时间 HH:MM, 如 08:55")
    _add_idempotency_arg(p)

    # list-schedules / remove-schedule
    sub.add_parser("list-schedules", help="查看所有定时任务")

    p = sub.add_parser("remove-schedule", help="删除定时任务")
    p.add_argument("schedule_id", help="任务 ID")
    _add_idempotency_arg(p)

    return root


_HANDLERS = {
    "setup":            cmd_setup,
    "config":           cmd_config,
    "accounts":         cmd_accounts,
    "start":            cmd_start,
    "stop":             cmd_stop,
    "ping":             cmd_ping,
    "subscribe":        cmd_subscribe,
    "unsubscribe":      cmd_unsubscribe,
    "order":            cmd_order,
    "cancel":           cmd_cancel,
    "cancel-all":       cmd_cancel_all,
    "position":         cmd_position,
    "account":          cmd_account,
    "trades":           cmd_trades,
    "orders":           cmd_orders,
    "alert":            cmd_alert,
    "alert-order":      cmd_alert_order,
    "list-alerts":      cmd_list_alerts,
    "remove-alert":     cmd_remove_alert,
    "poll":             cmd_poll,
    "report":           cmd_report,
    "price":            cmd_price,
    "schedule-order":   cmd_schedule_order,
    "schedule-login":   cmd_schedule_login,
    "list-schedules":   cmd_list_schedules,
    "remove-schedule":  cmd_remove_schedule,
}


def main():
    global _REGISTRY, _INSTANCE
    parser = build_parser()
    args   = parser.parse_args()
    try:
        _REGISTRY = AccountRegistry(Path(args.registry) if args.registry else None)
        if args.subcmd not in {"setup", "accounts"}:
            _INSTANCE = _REGISTRY.resolve(args.account or None)
            _INSTANCE.ensure_layout()
            state.configure(_INSTANCE.state_file, _INSTANCE.runtime_file)
    except AccountRegistryError as exc:
        _out({"ok": False, "error": str(exc)})
        return
    handler = _HANDLERS.get(args.subcmd)
    if handler:
        handler(args)
    else:
        _out({"ok": False, "error": f"未知子命令: {args.subcmd}"})


if __name__ == "__main__":
    main()
