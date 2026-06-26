"""
🚨 Pump Alert Module v1.0
异动推送模块 - 币安交易机会捕手核心组件

功能:
1. 实时监控币安全币种异动
2. 发现异动立即推送通知
3. 附带风险评级和操作建议

基于 pump_scanner.py 封装，提供 Skill 友好的接口
"""

import json
import time
import logging
import threading
import ssl
from datetime import datetime, timezone, timedelta
from collections import defaultdict, deque
from pathlib import Path
from typing import Optional, Callable
from dataclasses import dataclass, field

from risk_evaluator import evaluate_risk

import requests
import websocket
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ============================================================
# 日志配置
# ============================================================
logger = logging.getLogger("pump-alert")

# ============================================================
# 数据结构
# ============================================================
@dataclass
class PumpSignal:
    """异动信号"""
    symbol: str                    # 交易对 (如 BTCUSDT)
    base_asset: str                # 基础资产 (如 BTC)
    price: float                   # 当前价格
    change_pct: float              # 涨跌幅 (%)
    window_sec: int                # 检测窗口 (秒)
    volume_24h: float              # 24小时成交量 (USDT)
    risk_level: int                # 风险等级 (1-5)
    signal_type: str               # 信号类型: fast_pump / slow_pump
    timestamp: float               # 信号时间戳
    advice: str = ""               # 操作建议
    
    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "base_asset": self.base_asset,
            "price": self.price,
            "change_pct": self.change_pct,
            "window_sec": self.window_sec,
            "volume_24h": self.volume_24h,
            "risk_level": self.risk_level,
            "signal_type": self.signal_type,
            "timestamp": self.timestamp,
            "advice": self.advice,
        }
    
    def format_message(self) -> str:
        """格式化为用户友好的消息"""
        # 风险等级符号
        risk_stars = "⭐" * self.risk_level
        risk_labels = {1: "极低", 2: "低", 3: "中等", 4: "高", 5: "极高"}
        risk_label = risk_labels.get(self.risk_level, "未知")
        
        # 窗口标签
        if self.window_sec < 120:
            window_label = f"{self.window_sec}秒"
        else:
            window_label = f"{self.window_sec // 60}分钟"
        
        # 成交量格式化
        vol = self.volume_24h
        if vol >= 1_000_000_000:
            vol_str = f"${vol/1e9:.1f}B"
        elif vol >= 1_000_000:
            vol_str = f"${vol/1e6:.1f}M"
        elif vol >= 1_000:
            vol_str = f"${vol/1e3:.0f}K"
        else:
            vol_str = f"${vol:.0f}"
        
        # 涨幅 emoji
        if self.change_pct >= 15:
            emoji = "🚀🚀🚀"
        elif self.change_pct >= 10:
            emoji = "🚀🚀"
        elif self.change_pct >= 5:
            emoji = "🚀"
        else:
            emoji = "📈"
        
        # 信号类型
        type_label = "快速拉升" if self.signal_type == "fast_pump" else "持续上涨"
        
        # 时间
        time_str = datetime.fromtimestamp(
            self.timestamp, 
            tz=timezone(timedelta(hours=8))
        ).strftime("%H:%M:%S")
        
        msg = f"""{emoji} 异动信号！

币种：{self.base_asset}/USDT
涨幅：+{self.change_pct:.2f}%（{window_label}）
成交量：{vol_str}
当前价：${self.price:.6g}

风险评级：{risk_stars} {risk_label}
信号类型：{type_label}
操作建议：{self.advice}

💡 回复"买 50U 的 {self.base_asset}"立即下单
🕐 {time_str}"""
        
        return msg


# ============================================================
# 价格追踪器
# ============================================================
class PriceTracker:
    """维护每个币种的滚动价格窗口"""

    def __init__(self, max_window: int = 300):
        self.max_window = max_window
        # symbol -> deque of (timestamp, price)
        self.prices: dict[str, deque] = defaultdict(
            lambda: deque(maxlen=max_window * 2)
        )
        # symbol -> 24h 成交量 (USDT)
        self.volumes: dict[str, float] = {}
        # symbol -> 最新价
        self.latest: dict[str, float] = {}

    def update(self, symbol: str, price: float, volume_usdt: float):
        """更新价格"""
        now = time.time()
        self.prices[symbol].append((now, price))
        self.volumes[symbol] = volume_usdt
        self.latest[symbol] = price

    def get_change(self, symbol: str, seconds: int) -> Optional[float]:
        """计算过去 N 秒的涨幅 (%)"""
        if symbol not in self.prices:
            return None

        history = self.prices[symbol]
        if len(history) < 2:
            return None

        try:
            snapshot = list(history)
        except RuntimeError:
            return None

        if len(snapshot) < 2:
            return None

        now = time.time()
        cutoff = now - seconds
        current_price = snapshot[-1][1]

        old_price = None
        for ts, p in snapshot:
            if ts <= cutoff:
                old_price = p
            else:
                break

        if old_price is None or old_price == 0:
            return None

        return (current_price - old_price) / old_price * 100

    def get_symbol_data(self, symbol: str) -> Optional[dict]:
        """获取指定币种的数据"""
        if symbol not in self.latest:
            return None
        
        return {
            "symbol": symbol,
            "price": self.latest.get(symbol, 0),
            "volume_24h": self.volumes.get(symbol, 0),
            "changes": {
                60: self.get_change(symbol, 60),
                180: self.get_change(symbol, 180),
                300: self.get_change(symbol, 300),
            }
        }


# ============================================================
# 异动监控器
# ============================================================
class PumpAlertMonitor:
    """异动监控器 - Skill 友好接口"""
    
    def __init__(self, config: dict = None):
        """
        初始化监控器
        
        Args:
            config: 配置字典，包含:
                - thresholds: {60: 5, 180: 8, 300: 10} 时间窗口和阈值
                - min_volume: 最小成交量
                - cooldown: 冷却时间
                - exclude: 排除币种列表
        """
        self.config = config or {}
        
        # 默认配置
        self.thresholds = self.config.get("thresholds", {
            60: 5.0,    # 1分钟涨5%
            180: 8.0,   # 3分钟涨8%
            300: 10.0,  # 5分钟涨10%
        })
        self.min_volume = self.config.get("min_volume", 500_000)
        self.cooldown = self.config.get("cooldown", 300)
        self.exclude = set(self.config.get("exclude", [
            "USDCUSDT", "BUSDUSDT", "TUSDUSDT", "FDUSDUSDT",
        ]))
        
        # 内部状态
        self.tracker = PriceTracker(max_window=max(self.thresholds.keys()))
        self.cooldowns: dict[str, float] = {}
        self.safe_symbols: set = set()
        self.running = False
        self.ws = None
        self.ws_thread = None
        
        # 信号历史
        self.signal_history: list[PumpSignal] = []
        self.max_history = 100
        
        # 回调函数
        self.on_signal: Optional[Callable[[PumpSignal], None]] = None
        
        # HTTP session
        self.http = requests.Session()
        retry = Retry(total=3, backoff_factor=1)
        self.http.mount("https://", HTTPAdapter(max_retries=retry))
        
        logger.info("PumpAlertMonitor 初始化完成")
    
    def set_callback(self, callback: Callable[[PumpSignal], None]):
        """设置信号回调"""
        self.on_signal = callback
    
    def fetch_safe_symbols(self) -> set:
        """获取安全交易对"""
        url = "https://api.binance.com/api/v3/exchangeInfo"
        safe = set()
        
        try:
            resp = self.http.get(url, timeout=30)
            data = resp.json()
            
            for sym in data.get("symbols", []):
                symbol = sym.get("symbol", "")
                status = sym.get("status", "")
                
                if status == "TRADING" and sym.get("quoteAsset") == "USDT":
                    safe.add(symbol)
            
            logger.info(f"获取安全交易对: {len(safe)} 个")
            
        except Exception as e:
            logger.error(f"获取交易对失败: {e}")
        
        return safe
    
    def calculate_risk_level(self, change_pct: float, volume: float) -> int:
        """
        计算风险等级 (1-5)
        
        规则:
        - 成交量越大越安全
        - 涨幅越大风险越高
        """
        # 基础风险 (根据涨幅)
        if change_pct >= 20:
            base_risk = 5
        elif change_pct >= 15:
            base_risk = 4
        elif change_pct >= 10:
            base_risk = 3
        elif change_pct >= 5:
            base_risk = 2
        else:
            base_risk = 1
        
        # 成交量调整
        if volume >= 50_000_000:  # 5000万以上，降1级
            base_risk = max(1, base_risk - 1)
        elif volume >= 10_000_000:  # 1000万以上，不变
            pass
        elif volume >= 1_000_000:  # 100万以上，升1级
            base_risk = min(5, base_risk + 1)
        else:  # 100万以下，升2级
            base_risk = min(5, base_risk + 2)
        
        return base_risk
    
    def generate_advice(self, risk_level: int, change_pct: float) -> str:
        """生成操作建议"""
        if risk_level <= 2:
            return f"相对安全，可适当买入，建议止损 -5%"
        elif risk_level == 3:
            return f"风险中等，小仓位试水，建议止损 -3%"
        elif risk_level == 4:
            return f"风险较高，谨慎操作，建议止损 -2%"
        else:
            return f"风险极高，不建议追高，观望为主"
    
    def check_pumps(self) -> list[PumpSignal]:
        """检查所有币种是否触发阈值，返回信号列表"""
        now = time.time()
        signals = []
        
        for symbol in list(self.tracker.latest.keys()):
            # 排除黑名单
            if symbol in self.exclude:
                continue
            
            # 安全过滤
            if self.safe_symbols and symbol not in self.safe_symbols:
                continue
            
            # 冷却检查
            if symbol in self.cooldowns:
                if now - self.cooldowns[symbol] < self.cooldown:
                    continue
            
            # 成交量过滤
            volume = self.tracker.volumes.get(symbol, 0)
            if volume < self.min_volume:
                continue
            
            # 检查各窗口
            for window_sec, threshold in sorted(self.thresholds.items()):
                change = self.tracker.get_change(symbol, window_sec)
                if change is None:
                    continue
                
                if change >= threshold:
                    price = self.tracker.latest.get(symbol, 0)
                    base_asset = symbol.replace("USDT", "")
                    
                    # 风险评估（统一模块）
                    risk = evaluate_risk(change_pct=change, volume_usdt=volume)
                    risk_level = risk["risk_level"]
                    advice = f"{risk['action']}｜止损 {risk['stop_loss']}"
                    
                    # 信号类型
                    signal_type = "fast_pump" if window_sec <= 60 else "slow_pump"
                    
                    signal = PumpSignal(
                        symbol=symbol,
                        base_asset=base_asset,
                        price=price,
                        change_pct=change,
                        window_sec=window_sec,
                        volume_24h=volume,
                        risk_level=risk_level,
                        signal_type=signal_type,
                        timestamp=now,
                        advice=advice,
                    )
                    
                    signals.append(signal)
                    
                    # 更新冷却
                    self.cooldowns[symbol] = now
                    
                    # 只取最短窗口的信号
                    break
        
        # 保存到历史
        for sig in signals:
            self.signal_history.append(sig)
            if len(self.signal_history) > self.max_history:
                self.signal_history.pop(0)
            
            # 触发回调
            if self.on_signal:
                self.on_signal(sig)
        
        return signals
    
    def get_recent_signals(self, hours: float = 1.0) -> list[PumpSignal]:
        """获取最近 N 小时的信号"""
        cutoff = time.time() - hours * 3600
        return [s for s in self.signal_history if s.timestamp >= cutoff]
    
    def get_symbol_analysis(self, symbol: str) -> Optional[dict]:
        """获取指定币种分析"""
        if not symbol.endswith("USDT"):
            symbol = f"{symbol}USDT"
        
        data = self.tracker.get_symbol_data(symbol)
        if not data:
            return None
        
        # 添加风险分析
        volume = data.get("volume_24h", 0)
        changes = data.get("changes", {})
        max_change = max(filter(None, changes.values()), default=0)
        
        risk_level = self.calculate_risk_level(max_change, volume)
        advice = self.generate_advice(risk_level, max_change)
        
        data["risk_level"] = risk_level
        data["advice"] = advice
        
        return data
    
    # ----------------------------------------------------------
    # WebSocket 连接
    # ----------------------------------------------------------
    def _on_ws_message(self, ws, message):
        """处理 WS 消息"""
        try:
            data = json.loads(message)
            
            for ticker in data:
                symbol = ticker.get("s", "")
                if not symbol.endswith("USDT"):
                    continue
                
                if self.safe_symbols and symbol not in self.safe_symbols:
                    continue
                
                price = float(ticker.get("c", 0))
                volume = float(ticker.get("q", 0))
                
                if price > 0:
                    self.tracker.update(symbol, price, volume)
                    
        except Exception as e:
            logger.error(f"WS 消息处理错误: {e}")
    
    def _on_ws_error(self, ws, error):
        logger.error(f"WS 错误: {error}")
    
    def _on_ws_close(self, ws, close_status_code, close_msg):
        logger.warning(f"WS 关闭: {close_status_code} - {close_msg}")
        self.running = False
    
    def _on_ws_open(self, ws):
        logger.info("WS 连接成功")
    
    def _ws_run(self):
        """WS 运行线程"""
        while self.running:
            try:
                url = "wss://stream.binance.com:9443/ws/!miniTicker@arr"
                self.ws = websocket.WebSocketApp(
                    url,
                    on_message=self._on_ws_message,
                    on_error=self._on_ws_error,
                    on_close=self._on_ws_close,
                    on_open=self._on_ws_open,
                )
                self.ws.run_forever(
                    sslopt={"cert_reqs": ssl.CERT_NONE},
                    ping_interval=30,
                    ping_timeout=10,
                )
            except Exception as e:
                logger.error(f"WS 连接失败: {e}")
                time.sleep(5)
    
    def _check_loop(self):
        """检查循环"""
        while self.running:
            try:
                self.check_pumps()
            except Exception as e:
                logger.error(f"检查异常: {e}")
            time.sleep(1)
    
    def start(self):
        """启动监控"""
        if self.running:
            logger.warning("监控已在运行")
            return
        
        logger.info("启动异动监控...")
        
        # 获取安全交易对
        self.safe_symbols = self.fetch_safe_symbols()
        
        self.running = True
        
        # 启动 WS 线程
        self.ws_thread = threading.Thread(target=self._ws_run, daemon=True)
        self.ws_thread.start()
        
        # 启动检查线程
        self.check_thread = threading.Thread(target=self._check_loop, daemon=True)
        self.check_thread.start()
        
        logger.info("异动监控已启动")
    
    def stop(self):
        """停止监控"""
        logger.info("停止异动监控...")
        self.running = False
        
        if self.ws:
            self.ws.close()
        
        logger.info("异动监控已停止")


# ============================================================
# Skill 接口函数
# ============================================================

# 全局监控器实例
_monitor: Optional[PumpAlertMonitor] = None

def get_monitor() -> PumpAlertMonitor:
    """获取或创建监控器实例"""
    global _monitor
    if _monitor is None:
        _monitor = PumpAlertMonitor()
    return _monitor

def start_monitoring(callback: Callable[[PumpSignal], None] = None) -> str:
    """
    启动异动监控
    
    Args:
        callback: 信号回调函数
        
    Returns:
        状态消息
    """
    monitor = get_monitor()
    
    if callback:
        monitor.set_callback(callback)
    
    monitor.start()
    return "✅ 异动监控已启动，发现异动会立即通知你！"

def stop_monitoring() -> str:
    """停止异动监控"""
    monitor = get_monitor()
    monitor.stop()
    return "✅ 异动监控已停止"

def get_recent_alerts(hours: float = 1.0) -> list[dict]:
    """
    获取最近的异动信号
    
    Args:
        hours: 时间范围（小时）
        
    Returns:
        信号列表
    """
    monitor = get_monitor()
    signals = monitor.get_recent_signals(hours)
    return [s.to_dict() for s in signals]

def analyze_symbol(symbol: str) -> Optional[dict]:
    """
    分析指定币种
    
    Args:
        symbol: 币种名称（如 BTC 或 BTCUSDT）
        
    Returns:
        分析结果
    """
    monitor = get_monitor()
    return monitor.get_symbol_analysis(symbol)

def format_signal_message(signal: PumpSignal) -> str:
    """格式化信号消息"""
    return signal.format_message()


# ============================================================
# TG 推送辅助
# ============================================================
def _send_tg(token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            logger.error(f"TG send failed: {resp.status_code} {resp.text}")
    except Exception as e:
        logger.error(f"TG send error: {e}")


# ============================================================
# 主入口
# ============================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    import yaml
    from tg_config import get_tg_config

    cfg = yaml.safe_load(open("config.yaml", "r", encoding="utf-8"))
    tg_token, tg_chat = get_tg_config(cfg)

    def on_signal(sig: PumpSignal):
        msg = sig.format_message()
        logger.info(f"Signal: {sig.base_asset} +{sig.change_pct:.1f}%")
        print("\n" + "=" * 50)
        print(msg)
        print("=" * 50 + "\n")
        if tg_token and tg_chat:
            _send_tg(tg_token, tg_chat, msg)

    monitor = PumpAlertMonitor()
    monitor.set_callback(on_signal)
    monitor.start()

    # TG startup notification
    if tg_token and tg_chat:
        safe_count = len(monitor.safe_symbols)
        _send_tg(tg_token, tg_chat,
                 f"🚨 异动雷达已上线\n"
                 f"\n"
                 f"📡 监控范围\n"
                 f"  • {safe_count} 个 USDT 交易对实时扫描\n"
                 f"  • 已排除稳定币和异常币种\n"
                 f"\n"
                 f"⚡ 三档捕捉策略\n"
                 f"  🔴 闪电拉升  1min ≥ 5%\n"
                 f"  🟡 快速异动  3min ≥ 8%\n"
                 f"  🟢 持续上涨  5min ≥ 10%\n"
                 f"\n"
                 f"🛡️ 风控机制\n"
                 f"  • 最小成交量 $500K（过滤垃圾币）\n"
                 f"  • 5级风险评估（涨幅×流动性）\n"
                 f"  • 同币 5min 冷却（防刷屏）\n"
                 f"\n"
                 f"💡 收到信号后直接回复「买 50U 的 XXX」即可下单")
    logger.info("Pump Alert running, press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
