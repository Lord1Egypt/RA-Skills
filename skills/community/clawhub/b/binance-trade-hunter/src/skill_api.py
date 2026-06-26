"""
🔧 Skill API v1.0
统一接口 - 供 Agent 调用的所有即时指令和后台服务管理

即时调用：返回格式化好的字符串，Agent 直接回复给用户
后台服务：启动/停止长期运行的监控和推送进程
"""

from __future__ import annotations

import os
import sys
import logging
from pathlib import Path
from typing import Optional

import yaml
import requests

# ============================================================
# 路径设置
# ============================================================
_SRC_DIR = Path(__file__).resolve().parent
_CONFIG_PATH = str(_SRC_DIR / "config.yaml")

# 确保 src 目录在 sys.path 中（模块间互相导入）
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))


# ============================================================
# 配置加载
# ============================================================
def _load_config() -> dict:
    """加载配置文件，TG 配置自动从 OpenClaw 读取"""
    if not os.path.exists(_CONFIG_PATH):
        raise FileNotFoundError(
            f"配置文件不存在: {_CONFIG_PATH}\n"
            f"请从 config.yaml.example 复制并填写你的 API 密钥。"
        )
    cfg = yaml.safe_load(open(_CONFIG_PATH, "r", encoding="utf-8"))

    # Auto-fill telegram config from OpenClaw if not set
    tg = cfg.get("telegram", {})
    if not tg.get("bot_token") or not tg.get("chat_id"):
        oc_tg = _load_openclaw_telegram()
        if oc_tg:
            cfg.setdefault("telegram", {})
            if not cfg["telegram"].get("bot_token"):
                cfg["telegram"]["bot_token"] = oc_tg.get("bot_token", "")
            if not cfg["telegram"].get("chat_id"):
                cfg["telegram"]["chat_id"] = oc_tg.get("chat_id", "")
    return cfg


def _load_openclaw_telegram() -> Optional[dict]:
    """从 OpenClaw 配置自动获取 TG bot token + chat_id"""
    import json
    oc_path = Path.home() / ".openclaw" / "openclaw.json"
    if not oc_path.exists():
        return None
    try:
        oc = json.loads(oc_path.read_text(encoding="utf-8"))
        bot_token = oc.get("channels", {}).get("telegram", {}).get("botToken", "")
        # chat_id from env or auto-discover via getUpdates
        chat_id = os.environ.get("OPENCLAW_TG_CHAT_ID", "")
        if bot_token and not chat_id:
            from tg_config import _discover_chat_id
            chat_id = _discover_chat_id(bot_token)
        if bot_token:
            return {"bot_token": bot_token, "chat_id": chat_id}
    except Exception:
        pass
    return None


def _send_tg(token: str, chat_id: str, text: str, parse_mode: str = None):
    """发送 Telegram 消息"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            logging.getLogger("skill-api").error(f"TG send failed: {resp.status_code} {resp.text}")
    except Exception as e:
        logging.getLogger("skill-api").error(f"TG send error: {e}")


# ============================================================
# 即时调用 - 潜力币分析
# ============================================================
def analyze_top_coins(top_n: int = 3) -> str:
    """
    分析并返回 Top N 潜力币

    Returns:
        格式化的潜力币分析文本
    """
    from coin_analyzer import CoinAnalyzer

    analyzer = CoinAnalyzer()
    results = analyzer.analyze(top_n)

    if not results:
        return "📭 暂无符合条件的潜力币"

    lines = [f"🔍 24h 潜力币 Top {top_n}"]
    for i, r in enumerate(results, 1):
        stars = "⭐" * int(r["risk_level"])
        lines.append(
            f"\n{i}. {r['base_asset']}  总分 {r['score']}"
            f"\n   流动性: {r['liquidity_score']}/40 | 趋势: {r['trend_score']}/35 | 量: {r['volume_score']}/25"
            f"\n   风险: {stars} | {r['suggestion']}"
        )
    lines.append("\n🌊 用 AI 建设加密，和币安一起逐浪 Web3！")
    return "\n".join(lines)


def analyze_coin(symbol: str) -> str:
    """
    分析单个币种

    Args:
        symbol: 币种名称（如 BTC、ETH，不含 USDT）

    Returns:
        格式化的分析文本
    """
    from coin_analyzer import CoinAnalyzer

    symbol = symbol.upper().replace("USDT", "")
    full_symbol = f"{symbol}USDT"

    analyzer = CoinAnalyzer()

    # 获取 24h ticker
    try:
        tickers = analyzer.client.get_ticker_24h()
    except Exception as e:
        return f"❌ 获取行情失败: {e}"

    target = None
    for t in tickers:
        if t.get("symbol") == full_symbol:
            target = t
            break

    if not target:
        return f"❌ 未找到交易对 {full_symbol}"

    try:
        price = float(target.get("lastPrice", 0))
        change = float(target.get("priceChangePercent", 0))
        volume = float(target.get("volume", 0))
        quote_volume = float(target.get("quoteVolume", 0))
        high = float(target.get("highPrice", 0))
        low = float(target.get("lowPrice", 0))
    except Exception:
        return f"❌ 解析 {full_symbol} 数据失败"

    # 风险评估
    from risk_evaluator import evaluate_risk
    risk = evaluate_risk(change_pct=change, volume_usdt=quote_volume)

    # 格式化成交量
    if quote_volume >= 1_000_000_000:
        vol_str = f"${quote_volume/1e9:.1f}B"
    elif quote_volume >= 1_000_000:
        vol_str = f"${quote_volume/1e6:.1f}M"
    elif quote_volume >= 1_000:
        vol_str = f"${quote_volume/1e3:.0f}K"
    else:
        vol_str = f"${quote_volume:.0f}"

    stars = "⭐" * risk["risk_level"]

    return (
        f"📊 {symbol}/USDT 分析\n"
        f"\n"
        f"💰 价格: ${price:.6g}\n"
        f"📈 24h 涨跌: {change:+.2f}%\n"
        f"📊 24h 成交量: {vol_str}\n"
        f"🔺 24h 最高: ${high:.6g}\n"
        f"🔻 24h 最低: ${low:.6g}\n"
        f"\n"
        f"风险评级: {stars} {risk['risk_label']}\n"
        f"建议: {risk['action']}｜止损 {risk['stop_loss']}"
    )


# ============================================================
# 即时调用 - 交易执行
# ============================================================
def _get_executor():
    """获取交易执行器（懒加载）"""
    from trade_exec import get_executor
    return get_executor(_CONFIG_PATH)


def buy(symbol: str, usdt_amount: float) -> str:
    """
    市价买入

    Args:
        symbol: 币种名称（如 BTC、ETH）
        usdt_amount: USDT 金额

    Returns:
        交易结果文本
    """
    symbol = symbol.upper().replace("USDT", "")
    full_symbol = f"{symbol}USDT"
    executor = _get_executor()

    res = executor.market_buy(full_symbol, usdt_amount)
    if res.success:
        return (
            f"✅ 买入成功\n"
            f"币种: {symbol}\n"
            f"数量: {res.qty:.6g}\n"
            f"均价: ${res.price:.4g}\n"
            f"花费: {res.cost:.2f}U"
        )
    else:
        return f"❌ 买入失败: {res.message}"


def sell_all(symbol: str) -> str:
    """
    卖出全部持仓

    Args:
        symbol: 币种名称（如 BTC、ETH）

    Returns:
        交易结果文本
    """
    symbol = symbol.upper().replace("USDT", "")
    full_symbol = f"{symbol}USDT"
    executor = _get_executor()

    res = executor.market_sell_all(full_symbol)
    if res.success:
        return f"✅ 已卖出全部 {symbol}，数量 {res.qty:.6g}"
    else:
        return f"❌ 卖出失败: {res.message}"


def sell_half(symbol: str) -> str:
    """
    卖出一半持仓

    Args:
        symbol: 币种名称（如 BTC、ETH）

    Returns:
        交易结果文本
    """
    symbol = symbol.upper().replace("USDT", "")
    full_symbol = f"{symbol}USDT"
    executor = _get_executor()

    res = executor.market_sell_half(full_symbol)
    if res.success:
        return f"✅ 已卖出一半 {symbol}，数量 {res.qty:.6g}"
    else:
        return f"❌ 卖出失败: {res.message}"


def get_positions(whitelist: list = None) -> str:
    """
    查看持仓

    Args:
        whitelist: 白名单币种列表，如 ["BTC", "ETH"]；为 None 时从配置读取

    Returns:
        格式化的持仓文本
    """
    if whitelist is None:
        cfg = _load_config()
        whitelist = cfg.get("trading", {}).get("whitelist", ["BTC", "ETH"])

    executor = _get_executor()
    symbols = [f"{b.upper()}USDT" for b in whitelist]
    positions = executor.get_positions(symbols)

    if not positions:
        return "📭 当前白名单无持仓"

    lines = ["🔍 当前持仓："]
    for i, p in enumerate(positions, 1):
        line = f"{i}. {p['base']} | 数量 {p['qty']:.6g}"
        if p["price"] > 0:
            line += f" | 现价 ${p['price']:.4g} | 估值 ${p['value']:.2f}"
        lines.append(line)
    return "\n".join(lines)


def get_balance() -> str:
    """
    查看 USDT 余额

    Returns:
        格式化的余额文本
    """
    executor = _get_executor()
    balance = executor.get_balance("USDT")
    return f"💰 USDT 余额: ${balance:.2f}"


# ============================================================
# 后台服务管理 (独立进程 + PID 文件)
# ============================================================

_PID_DIR = _SRC_DIR / "pids"

_SERVICE_DEFS = {
    "pump_alert": {"label": "异动监控", "script": "pump_alert.py"},
    "coin_push": {"label": "定时推送", "script": "coin_analyzer.py"},
}


def _pid_file(name: str) -> Path:
    return _PID_DIR / f"{name}.pid"


def _is_running(name: str) -> bool:
    """Check if service is running via PID file"""
    pf = _pid_file(name)
    if not pf.exists():
        return False
    try:
        pid = int(pf.read_text().strip())
        # Windows: check if process exists
        import ctypes
        kernel32 = ctypes.windll.kernel32
        SYNCHRONIZE = 0x00100000
        handle = kernel32.OpenProcess(SYNCHRONIZE, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return True
        else:
            # process gone, clean up stale pid file
            pf.unlink(missing_ok=True)
            return False
    except Exception:
        pf.unlink(missing_ok=True)
        return False


def _get_pid(name: str) -> Optional[int]:
    pf = _pid_file(name)
    if not pf.exists():
        return None
    try:
        return int(pf.read_text().strip())
    except Exception:
        return None


def _start_service(name: str) -> str:
    """Start a service as independent process"""
    sdef = _SERVICE_DEFS[name]
    label = sdef["label"]
    script = sdef["script"]

    if _is_running(name):
        pid = _get_pid(name)
        return f"⚠️ {label}已在运行中 (PID: {pid})"

    _PID_DIR.mkdir(exist_ok=True)
    script_path = _SRC_DIR / script

    import subprocess
    # Start as background process (no window)
    proc = subprocess.Popen(
        [sys.executable, str(script_path)],
        cwd=str(_SRC_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    # Save PID
    _pid_file(name).write_text(str(proc.pid))

    return f"✅ {label}已启动 (PID: {proc.pid})"


def _stop_service(name: str) -> str:
    """Stop a service by PID"""
    sdef = _SERVICE_DEFS[name]
    label = sdef["label"]

    if not _is_running(name):
        return f"⚠️ {label}未在运行"

    pid = _get_pid(name)
    try:
        import signal
        os.kill(pid, signal.SIGTERM)
    except OSError:
        # force kill on Windows
        try:
            os.kill(pid, 9)
        except Exception:
            pass

    _pid_file(name).unlink(missing_ok=True)
    return f"✅ {label}已停止 (PID: {pid})"


# ---------- Public API ----------

def start_pump_alert() -> str:
    """启动异动监控后台服务"""
    return _start_service("pump_alert")

def stop_pump_alert() -> str:
    """停止异动监控"""
    return _stop_service("pump_alert")

def start_coin_push() -> str:
    """启动定时潜力币推送"""
    return _start_service("coin_push")

def stop_coin_push() -> str:
    """停止定时推送"""
    return _stop_service("coin_push")

def service_status() -> str:
    """查看所有后台服务状态"""
    lines = ["📋 后台服务状态："]
    for name, sdef in _SERVICE_DEFS.items():
        if _is_running(name):
            pid = _get_pid(name)
            status = f"🟢 运行中 (PID: {pid})"
        else:
            status = "🔴 已停止"
        lines.append(f"  {sdef['label']}: {status}")
    return "\n".join(lines)
