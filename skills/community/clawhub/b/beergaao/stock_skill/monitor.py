"""轮询监控模式"""
from __future__ import annotations
import logging, signal, time
from datetime import datetime
from typing import Callable, Dict, List
from .config import get_config
from .tools.tools import StockTools

logger = logging.getLogger(__name__)

class PollMonitor:
    def __init__(self, tools: StockTools | None = None):
        self.tools = tools or StockTools()
        self.cfg = get_config()
        self._running = False
        self._callbacks: List[Callable] = []

    def on_alert(self, callback): self._callbacks.append(callback)

    def _emit(self, event, data):
        for cb in self._callbacks:
            try: cb(event, data)
            except Exception as e: logger.error(f"回调失败: {e}")

    def _check_positions(self):
        result = self.tools.get_positions()
        if result.get("status") != "success": return
        for pos in result.get("data", []):
            code = pos.get("code", "")
            if not code: continue
            quote = self.tools.get_quote(code)
            if quote.get("status") != "success": continue
            current = quote["data"].get("price", 0)
            sl = pos.get("stop_loss", 0)
            tgt = pos.get("target_price", 0)
            entry = pos.get("entry_price", 0)
            if current <= 0 or entry <= 0: continue
            pnl = (current - entry) / entry
            if sl > 0 and current <= sl:
                self._emit("stop_loss", {"code": code, "message": f"[止损] {pos.get('name',code)} 价格{current} 触及止损{sl} ({pnl:+.2%})"})
            if tgt > 0 and current >= tgt:
                self._emit("take_profit", {"code": code, "message": f"[止盈] {pos.get('name',code)} 价格{current} 达到目标{tgt} ({pnl:+.2%})"})

    def _check_market(self):
        result = self.tools.circuit_breaker_check()
        if result.get("status") == "success" and result["data"].get("triggered"):
            self._emit("circuit_breaker", {"message": f"[熔断] {', '.join(result['data']['triggers'])}"})

    def start(self, interval=None, once=False):
        interval = interval or self.cfg.poll_interval
        self._running = True
        signal.signal(signal.SIGINT, lambda s,f: setattr(self, '_running', False))
        if not self._callbacks: self.on_alert(lambda e, d: print(d.get("message", str(d))))
        logger.info(f"监控启动，间隔 {interval}秒")
        while self._running:
            try: self._check_positions(); self._check_market()
            except Exception as e: logger.error(f"检查失败: {e}")
            if once: break
            time.sleep(interval)
        logger.info("监控已停止")

    def stop(self): self._running = False
