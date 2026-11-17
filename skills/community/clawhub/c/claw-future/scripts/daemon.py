"""
daemon.py

ClawTrader 后台守护进程。

职责：
  1. 连接 CTP 行情（MdGateway）+ 交易（TraderGateway）
  2. 事件循环：持续处理 Tick / 委托回报 / 成交回报
  3. 条件单引擎：Tick 驱动，触发时自动下单或推送告警
  4. 收盘日报定时任务
  5. 监听本地 TCP socket，接受来自 clawtrader.py CLI 的 JSON 指令

启动：
    python daemon.py

停止：
    发送 {"cmd":"stop"} 或 Ctrl-C
"""

import os
import sys
import json
import argparse
import time
import signal
import socket
import logging
import threading
import datetime
import uuid
from pathlib import Path

# ---------- 路径 ----------
_SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(_SCRIPTS))

import state
from accounts import AccountLease, AccountPaths, AccountRegistry
from idempotency import (
    IdempotencyConflict,
    IdempotencyStore,
    is_mutating_command,
    replay_response,
    request_key,
)
from ctp.md_gateway     import MdGateway,    EVT_MD_TICK
from ctp.trader_gateway import TraderGateway, EVT_RTN_ORDER, EVT_RTN_TRADE, \
                                               EVT_FRONT_CONNECTED, EVT_FRONT_DISCONNECTED, \
                                               EVT_RSP_AUTHENTICATE, EVT_RSP_LOGIN, \
                                               EVT_RSP_QRY_POSITION, EVT_RSP_QRY_ACCOUNT, \
                                               EVT_RSP_QRY_ORDER, EVT_RSP_QRY_TRADE, \
                                               EVT_RSP_ERROR, EVT_RSP_SETTLE_CONFIRM

logger = logging.getLogger("clawtrader.daemon")

# ---------- 配置 ----------
def _configure_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
        force=True,
    )


def _load_config(cfg_path: Path) -> dict:
    if not cfg_path.exists():
        raise FileNotFoundError(
            f"配置文件未找到: {cfg_path}\n"
            "请为该账户创建 config.json 并填写账户信息。"
        )
    data = json.loads(cfg_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"配置文件格式无效: {cfg_path}")
    return data


# ====================================================================
#  条件单引擎
# ====================================================================

class ConditionEngine:
    """
    条件单列表，每条 Tick 时检查触发。

    条件结构：
    {
        "id": "c1",
        "instrument": "IF2505",
        "cond_type": "price_ge" | "price_le" | "pct_change_ge" | "pct_change_le",
        "threshold": 6000.0,
        "action": "alert" | "order",
        "order_params": {...},   # 仅 action==order 时
        "msg": "IF触及6000点",   # 仅 action==alert 时
        "triggered": false
    }
    """

    def __init__(self, conditions=None, on_change=None):
        self._conditions: dict[str, dict] = {}
        self._pre_close: dict[str, float] = {}
        self._on_change = on_change
        for cond in conditions or []:
            if isinstance(cond, dict) and cond.get("id"):
                self._conditions[str(cond["id"])] = dict(cond)

    def _changed(self) -> None:
        if self._on_change:
            self._on_change()

    def add(self, cond: dict) -> str:
        cid = cond.get("id") or f"c{int(time.time()*1000)}"
        cond["id"] = cid
        cond["triggered"] = False
        self._conditions[cid] = dict(cond)
        self._changed()
        return cid

    def remove(self, cid: str) -> bool:
        removed = bool(self._conditions.pop(cid, None))
        if removed:
            self._changed()
        return removed

    def list_all(self) -> list:
        return list(self._conditions.values())

    def on_tick(self, tick: dict) -> list:
        """
        传入一条 Tick，返回触发的条件列表（每条只触发一次）。
        """
        inst  = tick.get("instrument", "")
        last  = tick.get("last", 0.0)
        pre_c = tick.get("pre_close", 0.0)
        if pre_c:
            self._pre_close[inst] = pre_c

        triggered = []
        for cid, cond in self._conditions.items():
            if cond["triggered"]:
                continue
            if cond["instrument"] != inst:
                continue

            ct  = cond["cond_type"]
            thr = cond["threshold"]
            hit = False

            if ct == "price_ge"      and last >= thr:
                hit = True
            elif ct == "price_le"    and last <= thr:
                hit = True
            elif ct == "pct_change_ge":
                base = self._pre_close.get(inst, 0)
                if base > 0 and (last - base) / base * 100 >= thr:
                    hit = True
            elif ct == "pct_change_le":
                base = self._pre_close.get(inst, 0)
                if base > 0 and (last - base) / base * 100 <= thr:
                    hit = True

            if hit:
                cond["triggered"] = True
                triggered.append(cond)

        if triggered:
            self._changed()
        return triggered


# ====================================================================
#  定时任务引擎（分钟级精度）
# ====================================================================

class ScheduleEngine:
    """
    定时任务，每天在指定时间触发一次。

    任务结构：
    {
        "id": "s1",
        "type": "order" | "login",
        "time": "09:25",           # HH:MM 本地时间
        "order_params": {...},     # type==order 时必填
        "triggered_date": ""       # 内部：已触发日期，防当天重复
    }
    """

    def __init__(self, schedules=None, on_change=None):
        self._schedules: dict[str, dict] = {}
        self._on_change = on_change
        for sched in schedules or []:
            if isinstance(sched, dict) and sched.get("id"):
                self._schedules[str(sched["id"])] = dict(sched)

    def _changed(self) -> None:
        if self._on_change:
            self._on_change()

    def add(self, sched: dict) -> str:
        sid = sched.get("id") or f"s{int(time.time()*1000)}"
        sched["id"] = sid
        sched.setdefault("triggered_date", "")
        self._schedules[sid] = dict(sched)
        self._changed()
        return sid

    def remove(self, sid: str) -> bool:
        removed = bool(self._schedules.pop(sid, None))
        if removed:
            self._changed()
        return removed

    def list_all(self) -> list:
        return list(self._schedules.values())

    def check(self, now: datetime.datetime) -> list:
        """返回当前分钟应触发的任务列表（每天每个任务只触发一次）。"""
        cur_time = now.strftime("%H:%M")
        cur_date = now.strftime("%Y%m%d")
        fired = []
        for sched in self._schedules.values():
            if sched.get("time") != cur_time:
                continue
            if sched.get("triggered_date") == cur_date:
                continue
            sched["triggered_date"] = cur_date
            fired.append(sched)
        if fired:
            self._changed()
        return fired


# ====================================================================
#  Pending 查询收集器（收集多条 is_last=false 然后汇总）
# ====================================================================

class QueryCollector:
    def __init__(self):
        self._buffers: dict[str, list] = {}   # qry_id → [rows]
        self._callbacks: dict[str, any] = {}  # qry_id → callback(rows)

    def start(self, qry_id: str, callback) -> None:
        self._buffers[qry_id]   = []
        self._callbacks[qry_id] = callback

    def feed(self, qry_id: str, row: dict) -> None:
        if qry_id not in self._buffers:
            return
        if row:
            self._buffers[qry_id].append(row)
        if row.get("is_last"):
            rows = self._buffers.pop(qry_id)
            cb   = self._callbacks.pop(qry_id)
            cb(rows)


# ====================================================================
#  Daemon 主体
# ====================================================================

class Daemon:
    DAEMON_PORT = 17777

    def __init__(self, cfg: dict, paths: AccountPaths | None = None):
        self.paths = paths or AccountRegistry().resolve()
        self.paths.ensure_layout()
        state.configure(self.paths.state_file, self.paths.runtime_file)
        self.account_id = self.paths.account_id
        self.cfg     = cfg
        self._md     = MdGateway(
            front     = cfg["md_front"],
            flow_path = str(self.paths.md_flow_dir) + "/",
        )
        self._td     = TraderGateway(
            front     = cfg["td_front"],
            flow_path = str(self.paths.td_flow_dir) + "/",
        )
        self._write_lock = threading.RLock()
        self._idempotency = IdempotencyStore(self.paths.idempotency_file)
        self._runtime_lock = threading.RLock()
        runtime = state.read_runtime()
        self._cond   = ConditionEngine(
            runtime.get("conditions", []), self._persist_runtime
        )
        self._sched  = ScheduleEngine(
            runtime.get("schedules", []), self._persist_runtime
        )
        self._qcol   = QueryCollector()
        self._desired_instruments: set[str] = set(
            self._normalise_instruments(",".join(runtime.get("subscriptions", [])))
        )
        self._daemon_session = uuid.uuid4().hex

        # 最新 Tick 缓存（instrument → tick dict）
        self._last_tick: dict[str, dict] = {}

        # 内存中的持仓 / 资金快照（由回调实时更新）
        self._positions:  dict[str, dict] = {}
        self._account:    dict            = {}
        self._active_orders: dict[str, dict] = {}   # order_ref → order
        self._today_trades:  list[dict]       = []

        self._running   = False
        self._event_log = []          # 发往 CLI 的待推送事件队列
        self._ev_lock   = threading.Lock()
        self._event_seq = 0

        # 同步查询等待：socket 线程等待主循环回调完成
        # key: "position" | "account" | "orders" | "trades"
        # value: threading.Event
        self._qry_wait: dict[str, threading.Event] = {}
        self._qry_wait_lock = threading.Lock()
        self._query_lock = threading.RLock()
        # 查询结果临时缓冲（主循环写，socket 线程读）
        self._qry_buf_orders: list[dict] = []
        self._qry_buf_trades: list[dict] = []

        # 收盘日报定时标志
        self._reported_today = ""

        # 交易通道（TD）健康：认证/登录/结算失败自动重建
        self._td_progress_ts  = 0.0     # 最近一次 TD 状态推进时间（连接/认证/结算）
        self._td_rebuild_ts   = 0.0     # 计划执行重建的时刻（0 = 无计划）
        self._td_fail_streak  = 0       # 连续失败次数，用于退避
        self._td_last_rebuild = 0.0     # 最近一次实际重建时间（防风暴）

        # 行情订阅是一个集合状态。重复订阅/退订不会重复调用 CTP。
        self._subscribed_instruments: set[str] = set()

    def _persist_runtime(self) -> None:
        """Persist local conditions and schedules as one atomic snapshot."""
        with self._runtime_lock:
            state.write_runtime({
                "version": 1,
                "conditions": self._cond.list_all(),
                "schedules": self._sched.list_all(),
                "subscriptions": sorted(self._desired_instruments),
            })

    @staticmethod
    def _normalise_instruments(instruments: str) -> list[str]:
        return sorted({
            item.strip()
            for item in str(instruments or "").split(",")
            if item.strip()
        })

    def _subscribe(self, instruments: str) -> int:
        with self._write_lock:
            requested = self._normalise_instruments(instruments)
            desired_changed = not set(requested).issubset(self._desired_instruments)
            self._desired_instruments.update(requested)
            if desired_changed:
                self._persist_runtime()
            pending = [item for item in requested
                       if item not in self._subscribed_instruments]
            if not pending:
                return 0
            ret = self._md.subscribe(",".join(pending))
            if ret == 0:
                self._subscribed_instruments.update(pending)
            return ret

    def _unsubscribe(self, instruments: str) -> int:
        with self._write_lock:
            requested = self._normalise_instruments(instruments)
            desired_changed = bool(set(requested) & self._desired_instruments)
            self._desired_instruments.difference_update(requested)
            if desired_changed:
                self._persist_runtime()
            pending = [item for item in requested
                       if item in self._subscribed_instruments]
            if not pending:
                return 0
            ret = self._md.unsubscribe(",".join(pending))
            if ret == 0:
                self._subscribed_instruments.difference_update(pending)
            return ret

    def _send_order_once(self, operation_key: str, **order_params) -> dict:
        """Submit an order at most once, including internally-triggered ones."""
        cmd = {"cmd": "order", **order_params, "idempotency_key": operation_key}
        with self._write_lock:
            try:
                key, existing = self._idempotency.begin(cmd)
            except IdempotencyConflict as exc:
                return {"ok": False, "error": str(exc),
                        "idempotency_key": request_key(cmd),
                        "account_id": self.account_id}
            if existing is not None:
                response = replay_response(key, existing)
                response.setdefault("account_id", self.account_id)
                return response

            if not self._td.settled:
                response = {"ok": False, "error": "未就绪（结算确认未完成）"}
                self._idempotency.complete(key, response)
                response["idempotency_key"] = key
                return response

            ret, ref = self._td.send_order(**order_params)
            response = {"ok": ret == 0, "order_ref": ref, "ret": ret}
            self._idempotency.complete(key, response)
            response["idempotency_key"] = key
            return response

    def _send_order_after_reservation(self, cmd: dict, **order_params) -> dict:
        """Submit a CLI order whose request journal entry is already reserved."""
        if not self._td.settled:
            return {"ok": False, "error": "未就绪（结算确认未完成）"}
        ret, ref = self._td.send_order(**order_params)
        return {"ok": ret == 0, "order_ref": ref, "ret": ret}

    # ---------------------------------------------------------------- #
    #  事件推送队列（供 CLI 轮询）                                       #
    # ---------------------------------------------------------------- #

    def _push_event(self, evt: dict) -> None:
        with self._ev_lock:
            self._event_seq += 1
            event = {
                **evt,
                "seq": self._event_seq,
                "account_id": self.account_id,
                "emitted_at": time.time(),
            }
            self._event_log.append(event)
            if len(self._event_log) > 2000:
                self._event_log.pop(0)

    def _events_since(self, after_seq: int = 0, limit: int = 500) -> dict:
        with self._ev_lock:
            events = [evt for evt in self._event_log if evt["seq"] > after_seq]
            events = events[:max(1, min(int(limit), 1000))]
            oldest_seq = self._event_log[0]["seq"] if self._event_log else self._event_seq
            return {
                "events": events,
                "next_seq": events[-1]["seq"] if events else self._event_seq,
                "oldest_seq": oldest_seq,
                "cursor_expired": bool(after_seq and after_seq < oldest_seq - 1),
            }

    # ---------------------------------------------------------------- #
    #  CTP 事件处理                                                      #
    # ---------------------------------------------------------------- #

    def _handle_tick(self, tick: dict) -> None:
        inst = tick.get("instrument", "")

        # 缓存最新 Tick
        self._last_tick[inst] = tick
        self._push_event({"type": "tick", "tick": tick})

        # 条件单检查与写命令串行，避免 Tick 线程和 socket 线程同时修改
        # 条件集合导致重复触发或字典迭代异常。
        with self._write_lock:
            triggered_conditions = self._cond.on_tick(tick)
        for cond in triggered_conditions:
            if cond["action"] == "alert":
                msg = cond.get("msg") or f"{inst} 触发条件 {cond['cond_type']}={cond['threshold']}"
                logger.info("[告警] %s", msg)
                self._push_event({"type": "alert", "msg": msg, "tick": tick, "cond_id": cond["id"]})
            elif cond["action"] == "order":
                op = cond.get("order_params", {})
                result = self._send_order_once(f"condition:{cond['id']}", **op)
                logger.info("[条件单触发] cond=%s ret=%s ref=%s",
                            cond["id"], result.get("ret"), result.get("order_ref", ""))
                self._push_event({"type": "cond_order_sent", "cond_id": cond["id"],
                                  "order_ref": result.get("order_ref", ""),
                                  "ret": result.get("ret"),
                                  "idempotency_key": result.get("idempotency_key",
                                                                  f"condition:{cond['id']}")})

    def _handle_order(self, order: dict) -> None:
        ref = order.get("order_ref", "")
        self._active_orders[ref] = order
        self._push_event({"type": "order", **order})
        logger.info("[委托] %s %s %s vol=%s/%s status=%s",
                    order.get("instrument"), order.get("direction"),
                    order.get("offset"), order.get("volume_traded"),
                    order.get("volume_total"), order.get("order_status"))

    def _handle_trade(self, trade: dict) -> None:
        self._today_trades.append(trade)
        self._push_event({"type": "trade", **trade})
        logger.info("[成交] %s %s %s price=%.4f vol=%d",
                    trade.get("instrument"), trade.get("direction"),
                    trade.get("offset"), trade.get("price", 0), trade.get("volume", 0))

    # ---------------------------------------------------------------- #
    #  Socket 命令处理                                                   #
    # ---------------------------------------------------------------- #

    def _handle_cmd(self, cmd: dict) -> dict:
        """Dispatch a command, journaling every state-changing request."""
        target_account = str(cmd.get("account_id") or "").strip()
        if target_account and target_account != self.account_id:
            return {
                "ok": False,
                "error": f"请求账户 {target_account} 与实例 {self.account_id} 不一致",
                "account_id": self.account_id,
            }
        command_name = str(cmd.get("cmd", ""))
        if not is_mutating_command(command_name):
            response = dict(self._handle_cmd_impl(cmd))
            response.setdefault("account_id", self.account_id)
            return response

        journal_command = cmd
        if command_name == "stop" and not cmd.get("idempotency_key"):
            journal_command = {**cmd, "_daemon_session": self._daemon_session}

        with self._write_lock:
            try:
                key, existing = self._idempotency.begin(journal_command)
            except IdempotencyConflict as exc:
                return {"ok": False, "error": str(exc),
                        "idempotency_key": request_key(journal_command),
                        "account_id": self.account_id}
            if existing is not None:
                response = replay_response(key, existing)
                response.setdefault("account_id", self.account_id)
                return response

            # A raised exception leaves the durable record pending.  A retry
            # then returns an "unknown state" response instead of risking a
            # second broker mutation.
            response = self._handle_cmd_impl(cmd)
            self._idempotency.complete(key, response)
            response = dict(response)
            response["idempotency_key"] = key
            response.setdefault("account_id", self.account_id)
            return response

    def _handle_cmd_impl(self, cmd: dict) -> dict:
        c = cmd.get("cmd", "")

        if c == "ping":
            return {
                "ok": True,
                "trading_day": self._td.get_trading_day(),
                "connected": self._td.connected,
                "authenticated": self._td.authenticated,
                "logged_in": self._td.logged_in,
                "settled": self._td.settled,
                "md_connected": self._md.connected,
                "md_logged_in": self._md.logged_in,
            }

        elif c == "stop":
            if not self._running:
                return {"ok": True, "already_stopped": True}
            self._running = False
            return {"ok": True}

        elif c == "subscribe":
            instruments = cmd.get("instruments", "")
            ret = self._subscribe(instruments)
            return {"ok": ret == 0, "ret": ret}

        elif c == "unsubscribe":
            instruments = cmd.get("instruments", "")
            ret = self._unsubscribe(instruments)
            return {"ok": ret == 0, "ret": ret}

        elif c == "order":
            order_params = {
                "exchange":   cmd["exchange"],
                "instrument": cmd["instrument"],
                "direction":  cmd["direction"],
                "offset":     cmd["offset"],
                "price_type": cmd.get("price_type", "limit"),
                "price":      cmd.get("price", 0.0),
                "volume":     cmd["volume"],
                "time_cond":  cmd.get("time_cond", "gfd"),
                "vol_cond":   cmd.get("vol_cond", "any"),
            }
            # The outer dispatcher has already reserved the request.  Reuse
            # its key here so automatic and explicit order paths share one
            # semantic idempotency identity.
            return self._send_order_after_reservation(cmd, **order_params)

        elif c == "cancel":
            order_ref = cmd.get("order_ref", "")
            order_sys_id = cmd.get("order_sys_id", "")
            known_order = self._active_orders.get(order_ref) if order_ref else None
            if known_order and known_order.get("order_status") in {
                "0", "2", "4", "5", "AllTraded", "Canceled"
            }:
                return {"ok": True, "ret": 0, "already_settled": True}
            ret = self._td.cancel_order(
                exchange     = cmd.get("exchange", ""),
                instrument   = cmd.get("instrument", ""),
                order_sys_id = order_sys_id,
                order_ref    = order_ref,
            )
            return {"ok": ret == 0, "ret": ret}

        elif c == "qry_position":
            return self._query_positions(cmd.get("instrument", ""))

        elif c == "qry_account":
            return self._query_account()

        elif c == "qry_orders":
            return self._query_orders(cmd.get("instrument", ""))

        elif c == "qry_trades":
            return self._query_trades(cmd.get("instrument", ""))

        elif c == "add_alert":
            cid = self._cond.add(cmd["condition"])
            return {"ok": True, "cond_id": cid}

        elif c == "remove_alert":
            ok = self._cond.remove(cmd["cond_id"])
            return {"ok": True, "removed": ok, "already_absent": not ok}

        elif c == "list_alerts":
            return {"ok": True, "conditions": self._cond.list_all()}

        elif c == "poll_events":
            return {"ok": True, **self._events_since(
                int(cmd.get("after_seq", 0) or 0),
                int(cmd.get("limit", 500) or 500),
            )}

        elif c == "report":
            self._refresh_for_report()   # 先向交易所刷新资金/持仓/成交
            return {"ok": True, "report": self._gen_report()}

        elif c == "qry_price":
            inst = cmd.get("instrument", "")
            tick = self._last_tick.get(inst)
            if tick:
                return {"ok": True, "tick": tick}
            return {"ok": False, "error": f"暂无 {inst} 行情，请先订阅"}

        elif c == "cancel_all":
            cancelled, failed = 0, 0
            for ref, order in list(self._active_orders.items()):
                status = order.get("order_status", "")
                # 只撤未成交/部分成交的委托
                if status in ("0", "2", "4", "5", "AllTraded", "Canceled"):
                    continue
                ret = self._td.cancel_order(
                    exchange     = order.get("exchange", ""),
                    instrument   = order.get("instrument", ""),
                    order_sys_id = order.get("order_sys_id", ""),
                    order_ref    = ref,
                )
                if ret == 0:
                    cancelled += 1
                else:
                    failed += 1
            return {"ok": True, "cancelled": cancelled, "failed": failed}

        elif c == "add_schedule":
            sid = self._sched.add(cmd["schedule"])
            return {"ok": True, "schedule_id": sid}

        elif c == "list_schedules":
            return {"ok": True, "schedules": self._sched.list_all()}

        elif c == "remove_schedule":
            ok = self._sched.remove(cmd["schedule_id"])
            return {"ok": True, "removed": ok, "already_absent": not ok}

        else:
            return {"ok": False, "error": f"未知指令: {c}"}

    def _query_positions(self, instrument: str = "") -> dict:
        with self._query_lock:
            ev = threading.Event()
            with self._qry_wait_lock:
                self._positions = {}
                self._qry_wait["position"] = ev
            ret = self._td.qry_position(instrument)
            if ret != 0:
                with self._qry_wait_lock:
                    self._qry_wait.pop("position", None)
                return {"ok": False, "error": f"qry_position ret={ret}（流控中，稍后重试）"}
            if not ev.wait(timeout=5.0):
                with self._qry_wait_lock:
                    self._qry_wait.pop("position", None)
                return {"ok": False, "error": "持仓查询超时，未返回旧缓存"}
            rows = list(self._positions.values())
            if instrument:
                rows = [row for row in rows if row.get("instrument") == instrument]
            return {"ok": True, "positions": rows}

    def _query_account(self) -> dict:
        with self._query_lock:
            ev = threading.Event()
            with self._qry_wait_lock:
                self._qry_wait["account"] = ev
            ret = self._td.qry_account()
            if ret != 0:
                with self._qry_wait_lock:
                    self._qry_wait.pop("account", None)
                return {"ok": False, "error": f"qry_account ret={ret}（流控中，稍后重试）"}
            if not ev.wait(timeout=5.0):
                with self._qry_wait_lock:
                    self._qry_wait.pop("account", None)
                return {"ok": False, "error": "资金查询超时，未返回旧缓存"}
            return {"ok": True, "account": self._account}

    def _query_orders(self, instrument: str = "") -> dict:
        with self._query_lock:
            ev = threading.Event()
            with self._qry_wait_lock:
                self._qry_buf_orders = []
                self._qry_wait["orders"] = ev
            ret = self._td.qry_order(instrument)
            if ret != 0:
                with self._qry_wait_lock:
                    self._qry_wait.pop("orders", None)
                return {"ok": False, "error": f"qry_order ret={ret}（流控中，稍后重试）"}
            if not ev.wait(timeout=5.0):
                with self._qry_wait_lock:
                    self._qry_wait.pop("orders", None)
                return {"ok": False, "error": "委托查询超时，未返回旧缓存"}
            rows = list(self._qry_buf_orders)
            for row in rows:
                ref = row.get("order_ref")
                if ref:
                    self._active_orders[ref] = row
            return {"ok": True, "orders": rows}

    def _query_trades(self, instrument: str = "") -> dict:
        with self._query_lock:
            ev = threading.Event()
            with self._qry_wait_lock:
                self._qry_buf_trades = []
                self._qry_wait["trades"] = ev
            ret = self._td.qry_trade(instrument)
            if ret != 0:
                with self._qry_wait_lock:
                    self._qry_wait.pop("trades", None)
                return {"ok": False, "error": f"qry_trade ret={ret}（流控中，稍后重试）"}
            if not ev.wait(timeout=5.0):
                with self._qry_wait_lock:
                    self._qry_wait.pop("trades", None)
                return {"ok": False, "error": "成交查询超时，未返回旧缓存"}
            rows = list(self._qry_buf_trades)
            self._today_trades = rows
            return {"ok": True, "trades": rows}

    def _refresh_for_report(self) -> None:
        """依次向 CTP 查询资金→持仓→成交，等待回调后更新本地缓存。
        必须在非主循环线程中调用（socket 线程或独立线程）。
        三次查询每次间隔 1.1 秒（trader_gateway._wait_qry 强制）。
        """
        with self._query_lock:
            self._query_account()
            self._query_positions()
            self._query_trades()

    def _gen_report(self) -> dict:
        """根据当前本地缓存生成日报 dict（调用前请先 _refresh_for_report）。"""
        return {
            "trading_day": self._td.get_trading_day(),
            "account":     self._account,
            "positions":   list(self._positions.values()),
            "trades":      list(self._today_trades),
        }

    # ---------------------------------------------------------------- #
    #  Socket 服务线程                                                   #
    # ---------------------------------------------------------------- #

    def _socket_server(self, port: int) -> None:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", port))
        srv.listen(5)
        srv.settimeout(1.0)
        logger.info("命令监听端口: %d", port)

        while self._running:
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            threading.Thread(target=self._handle_conn,
                             args=(conn,), daemon=True).start()
        srv.close()

    def _handle_conn(self, conn: socket.socket) -> None:
        try:
            data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b"\n" in data:
                    break
            cmd = json.loads(data.decode())
            resp = self._handle_cmd(cmd)
            conn.sendall((json.dumps(resp, ensure_ascii=False) + "\n").encode())
        except Exception as e:
            try:
                conn.sendall((json.dumps({"ok": False, "error": str(e)}) + "\n").encode())
            except Exception:
                pass
        finally:
            conn.close()

    # ---------------------------------------------------------------- #
    #  收盘日报定时触发                                                   #
    # ---------------------------------------------------------------- #

    def _check_daily_report(self) -> None:
        now = datetime.datetime.now()
        trading_day = self._td.get_trading_day() or now.strftime("%Y%m%d")

        # 15:20 之后触发，每个交易日只触发一次
        if now.hour == 15 and now.minute >= 20:
            if self._reported_today != trading_day:
                self._reported_today = trading_day  # 先标记，防止主循环重复触发
                def _async_report(td_str):
                    self._refresh_for_report()
                    report = self._gen_report()
                    self._push_event({"type": "daily_report", "report": report})
                    logger.info("[日报] 收盘日报已生成，交易日 %s", td_str)
                threading.Thread(target=_async_report, args=(trading_day,),
                                 daemon=True).start()

    # ---------------------------------------------------------------- #
    #  定时任务检查                                                       #
    # ---------------------------------------------------------------- #

    def _check_schedules(self) -> None:
        now = datetime.datetime.now()
        with self._write_lock:
            due_schedules = self._sched.check(now)
        for sched in due_schedules:
            stype = sched.get("type", "")
            sid   = sched["id"]
            if stype == "order":
                op = sched.get("order_params", {})
                if not self._td.settled:
                    logger.warning("[定时单] %s 跳过：交易网关未就绪", sid)
                    self._push_event({"type": "schedule_skip", "schedule_id": sid,
                                      "reason": "交易网关未就绪"})
                    continue
                result = self._send_order_once(
                    f"schedule:{sid}:{now.strftime('%Y%m%d')}", **op
                )
                logger.info("[定时单] %s 已触发，ret=%s ref=%s",
                            sid, result.get("ret"), result.get("order_ref", ""))
                self._push_event({"type": "schedule_order_sent", "schedule_id": sid,
                                  "order_ref": result.get("order_ref", ""),
                                  "ret": result.get("ret"),
                                  "idempotency_key": result.get(
                                      "idempotency_key",
                                      f"schedule:{sid}:{now.strftime('%Y%m%d')}"
                                  )})
            elif stype == "login":
                logger.info("[定时登录] %s 触发，重新连接", sid)
                self._rebuild_td("定时登录")
                self._push_event({"type": "schedule_login", "schedule_id": sid})

    # ---------------------------------------------------------------- #
    #  交易通道（TD）健康：认证/登录/结算失败自动重建                      #
    # ---------------------------------------------------------------- #

    def _touch_td_progress(self) -> None:
        """记录一次 TD 状态机推进（连接成功/认证成功/结算完成）。"""
        self._td_progress_ts = time.time()

    def _schedule_td_rebuild(self, reason: str) -> None:
        """请求在退避后重建 TD 连接。失败越多间隔越长：15s 起，封顶 300s。"""
        if self._td.settled:
            return                      # 已健康，无需重建
        now = time.time()
        if self._td_rebuild_ts > now:
            return                      # 已有待执行计划，不重复计数
        if now - self._td_last_rebuild < 5:
            return                      # 刚重建过，防风暴
        self._td_fail_streak += 1
        if self._td_fail_streak > 4:
            delay = 300.0               # 长期故障，5 分钟重试一次
        else:
            delay = 15.0 * (2 ** (self._td_fail_streak - 1))   # 15/30/60/120
        self._td_rebuild_ts = now + delay
        logger.warning("交易通道异常（%s），%.0f 秒后重建连接（连续第 %d 次）",
                       reason, delay, self._td_fail_streak)

    def _rebuild_td(self, reason: str) -> None:
        """释放旧句柄并重走 连接→认证→登录→结算 全流程（仅主线程调用）。"""
        cfg = self.cfg
        self._td_last_rebuild = time.time()
        self._td_rebuild_ts   = 0.0
        logger.warning("重建交易通道（%s，第 %d 次）", reason, self._td_fail_streak)
        try:
            self._td.release()
        except Exception:
            pass
        self._td.connect(
            broker_id = cfg["broker_id"],
            user_id   = cfg["user_id"],
            password  = cfg["td_password"],
            app_id    = cfg["app_id"],
            auth_code = cfg["auth_code"],
        )
        self._touch_td_progress()       # 观察起点：无进展则由看门狗兜底
        self._push_event({"type": "td_reconnect", "reason": reason,
                          "attempt": self._td_fail_streak})

    def _on_td_lifecycle(self, evt: int, data: dict) -> None:
        """TD 连接/认证/登录/结算事件：失败排入重建，成功推进计时并清零。"""
        if evt == EVT_FRONT_CONNECTED:
            self._touch_td_progress()
            return
        if evt == EVT_FRONT_DISCONNECTED:
            # 交给 CTP 内部自动重连；长时间未恢复由 _td_health_tick 兜底
            logger.warning("交易前置断开: %s", data.get("reason", ""))
            return
        error_id = int(data.get("error_id") or 0)
        if evt in (EVT_RSP_AUTHENTICATE, EVT_RSP_LOGIN):
            if error_id == 0:
                self._touch_td_progress()   # 认证/登录成功（结算由下一步推进）
            else:
                self._schedule_td_rebuild(
                    str(data.get("error_msg") or f"事件 {evt} 失败"))
            return
        if evt == EVT_RSP_SETTLE_CONFIRM:
            if error_id == 0:
                self._td_fail_streak = 0    # 全流程打通，重置退避
                self._td_rebuild_ts  = 0.0
                self._touch_td_progress()
            else:
                self._schedule_td_rebuild(
                    str(data.get("error_msg") or "结算确认失败"))
            return

    def _td_health_tick(self) -> None:
        """看门狗：执行到期重建；兜底“连上但认证/结算悬挂”或“断线久未恢复”。"""
        now = time.time()
        if self._td_rebuild_ts > 0 and now >= self._td_rebuild_ts:
            self._rebuild_td("计划到期")
            return
        if self._td.settled:
            return
        if self._td.connected:
            # 前置已连但长时间未完成认证/结算（含前置静默拒绝、无事件返回）
            if self._td_progress_ts > 0 and now - self._td_progress_ts > 60:
                self._schedule_td_rebuild("已连前置但认证/结算长时间未完成")
        else:
            # 前置断开：CTP 内部会重连，超 90 秒仍未恢复则手动重建
            if self._td_progress_ts > 0 and now - self._td_progress_ts > 90:
                self._schedule_td_rebuild("交易前置长时间未恢复")

    # ---------------------------------------------------------------- #
    #  主循环                                                            #
    # ---------------------------------------------------------------- #

    def run(self) -> None:
        cfg = self.cfg

        # 启动 MD
        self._md.connect(cfg["broker_id"], cfg["user_id"], cfg["md_password"])

        # 启动 TD
        self._td.connect(
            broker_id = cfg["broker_id"],
            user_id   = cfg["user_id"],
            password  = cfg["td_password"],
            app_id    = cfg["app_id"],
            auth_code = cfg["auth_code"],
        )
        self._touch_td_progress()   # 观察起点：连接/认证无进展由看门狗兜底

        # 写 state 文件
        self._running = True
        port = self.paths.daemon_port or cfg.get("daemon_port", self.DAEMON_PORT)
        state.write({"port": port, "pid": os.getpid(),
                     "account_id": self.account_id, "started_at": time.time()})

        # 启动 socket 服务
        sock_thread = threading.Thread(target=self._socket_server,
                                       args=(port,), daemon=True)
        sock_thread.start()

        logger.info("ClawTrader daemon 已启动 account=%s (PID=%d)",
                    self.account_id, os.getpid())

        # 初始订阅
        default_instruments = cfg.get("default_instruments", "")

        # ---- 事件主循环 ----
        while self._running:
            # 处理行情事件
            for _ in range(10):     # 每轮最多消费 10 条 MD 事件
                evt, data = self._md.poll_one(timeout_ms=0)
                if evt == 0:
                    break
                if evt == 101 and default_instruments:  # MD_FRONT_CONNECTED 后订阅
                    pass
                elif evt == 102:
                    self._subscribed_instruments.clear()
                elif evt == 103:    # MD_RSP_LOGIN
                    if data.get("error_id", 0) == 0:
                        requested = set(self._desired_instruments)
                        requested.update(self._normalise_instruments(default_instruments))
                        if requested:
                            instruments = ",".join(sorted(requested))
                            self._subscribe(instruments)
                            logger.info("已恢复订阅合约: %s", instruments)
                elif evt == EVT_MD_TICK:
                    self._handle_tick(data)

            # 处理交易事件
            for _ in range(20):
                evt, data = self._td.poll_one(timeout_ms=0)
                if evt == 0:
                    break
                if evt in (EVT_FRONT_CONNECTED, EVT_FRONT_DISCONNECTED,
                           EVT_RSP_AUTHENTICATE, EVT_RSP_LOGIN,
                           EVT_RSP_SETTLE_CONFIRM):
                    self._on_td_lifecycle(evt, data)
                    continue
                if evt == EVT_RTN_ORDER:
                    self._handle_order(data)
                elif evt == EVT_RTN_TRADE:
                    self._handle_trade(data)
                elif evt == EVT_RSP_QRY_POSITION:
                    inst = data.get("instrument", "")
                    if inst:
                        # CTP 对当日已全部平掉（现无持仓）的合约仍会回一条 position=0 的记录；
                        # 不作为持仓入库，避免“持仓 0”行出现在持仓/日报里
                        if int(data.get("position") or 0) != 0:
                            key = f"{inst}_{data.get('direction','')}"
                            self._positions[key] = data
                    if data.get("is_last"):
                        with self._qry_wait_lock:
                            ev = self._qry_wait.pop("position", None)
                        if ev:
                            ev.set()
                elif evt == EVT_RSP_QRY_ACCOUNT:
                    self._account = data
                    with self._qry_wait_lock:
                        ev = self._qry_wait.pop("account", None)
                    if ev:
                        ev.set()
                elif evt == EVT_RSP_QRY_ORDER:
                    if data.get("order_ref") or data.get("instrument"):
                        with self._qry_wait_lock:
                            self._qry_buf_orders.append(data)
                    if data.get("is_last"):
                        with self._qry_wait_lock:
                            ev = self._qry_wait.pop("orders", None)
                        if ev:
                            ev.set()
                elif evt == EVT_RSP_QRY_TRADE:
                    if data.get("trade_id") or data.get("instrument"):
                        with self._qry_wait_lock:
                            self._qry_buf_trades.append(data)
                    if data.get("is_last"):
                        with self._qry_wait_lock:
                            ev = self._qry_wait.pop("trades", None)
                        if ev:
                            ev.set()
                elif evt == EVT_RSP_ERROR:
                    logger.error("[CTP错误] %s", data)
                    self._push_event({"type": "error", **data})

            # 收盘日报检查
            self._check_daily_report()

            # 定时任务检查
            self._check_schedules()

            # 交易通道健康检查（执行到期重建 / 看门狗兜底）
            self._td_health_tick()

            time.sleep(0.005)   # 避免空转吃 CPU

        # 退出清理
        logger.info("daemon 正在退出...")
        self._md.release()
        self._td.release()
        state.clear()
        logger.info("daemon 已退出")


# ====================================================================
#  入口
# ====================================================================

def main():
    parser = argparse.ArgumentParser(description="ClawTrader account daemon")
    parser.add_argument("--account", default="")
    parser.add_argument("--registry", default="")
    args = parser.parse_args()

    registry = AccountRegistry(Path(args.registry) if args.registry else None)
    paths = registry.resolve(args.account or None)
    paths.ensure_layout()
    state.configure(paths.state_file, paths.runtime_file)
    _configure_logging(paths.log_file)
    cfg = _load_config(paths.config_file)
    lease = AccountLease(cfg["broker_id"], cfg["user_id"])
    lease.acquire()
    try:
        daemon = Daemon(cfg, paths)

        def _sig_handler(signum, frame):
            logger.info("收到信号 %d，停止 daemon", signum)
            daemon._running = False

        signal.signal(signal.SIGINT,  _sig_handler)
        signal.signal(signal.SIGTERM, _sig_handler)
        daemon.run()
    finally:
        lease.release()


if __name__ == "__main__":
    main()
