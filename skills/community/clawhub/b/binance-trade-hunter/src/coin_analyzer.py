"""
🔍 Coin Analyzer v1.0
潜力币智能筛选模块 - 币安交易机会捕手核心组件

功能:
1. 获取币安新币列表
2. 分析流动性/成交量/价格走势
3. 生成潜力币排名 + 风险评级 + 建议
"""

from __future__ import annotations

import time
import logging
from dataclasses import dataclass
from typing import Optional, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import yaml

from risk_evaluator import evaluate_risk

logger = logging.getLogger("coin-analyzer")


def load_config(path: str = "config.yaml") -> dict:
    return yaml.safe_load(open(path, "r", encoding="utf-8"))


def send_message(token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            logger.error(f"TG 返回异常: {resp.status_code} {resp.text}")
    except Exception as e:
        logger.error(f"发送 TG 消息失败: {e}")


# ============================================================
# 数据结构
# ============================================================
@dataclass
class CoinInfo:
    symbol: str
    base_asset: str
    price: float
    change_24h: float
    volume_24h: float
    quote_volume_24h: float
    high_24h: float
    low_24h: float
    list_time: Optional[int] = None  # 上线时间 (epoch ms)


@dataclass
class CoinScore:
    symbol: str
    base_asset: str
    score: float
    risk_level: int
    liquidity_score: float
    trend_score: float
    volume_score: float
    suggestion: str
    reasons: List[str]


# ============================================================
# 币安数据客户端
# ============================================================
class BinanceClient:
    def __init__(self):
        self.http = requests.Session()
        retry = Retry(total=3, backoff_factor=1)
        self.http.mount("https://", HTTPAdapter(max_retries=retry))

    def get_exchange_info(self) -> dict:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        resp = self.http.get(url, timeout=20)
        resp.raise_for_status()
        return resp.json()

    def get_ticker_24h(self) -> list:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        resp = self.http.get(url, timeout=20)
        resp.raise_for_status()
        return resp.json()


# ============================================================
# 评分逻辑
# ============================================================
class CoinAnalyzer:
    def __init__(self, min_volume_usdt: float = 300_000):
        self.client = BinanceClient()
        self.min_volume_usdt = min_volume_usdt
        self.stablecoins = {"USDT", "USDC", "BUSD", "TUSD", "FDUSD", "USDP", "DAI", "USDD"}

    def fetch_new_listings(self) -> dict:
        """获取上线时间 (listTime) 信息"""
        info = self.client.get_exchange_info()
        listings = {}
        for sym in info.get("symbols", []):
            if sym.get("quoteAsset") != "USDT":
                continue
            if sym.get("status") != "TRADING":
                continue
            symbol = sym.get("symbol")
            list_time = sym.get("onboardDate") or sym.get("listTime")
            if list_time:
                listings[symbol] = int(list_time)
        return listings

    def fetch_market_data(self) -> list[CoinInfo]:
        tickers = self.client.get_ticker_24h()
        listings = self.fetch_new_listings()

        coins = []
        for t in tickers:
            symbol = t.get("symbol", "")
            if not symbol.endswith("USDT"):
                continue

            try:
                price = float(t.get("lastPrice", 0))
                change_24h = float(t.get("priceChangePercent", 0))
                volume = float(t.get("volume", 0))
                quote_volume = float(t.get("quoteVolume", 0))
                high = float(t.get("highPrice", 0))
                low = float(t.get("lowPrice", 0))
            except Exception:
                continue

            if quote_volume < self.min_volume_usdt:
                continue

            base_asset = symbol.replace("USDT", "")
            if base_asset in self.stablecoins:
                continue

            coins.append(CoinInfo(
                symbol=symbol,
                base_asset=base_asset,
                price=price,
                change_24h=change_24h,
                volume_24h=volume,
                quote_volume_24h=quote_volume,
                high_24h=high,
                low_24h=low,
                list_time=listings.get(symbol)
            ))
        return coins

    def score_coin(self, coin: CoinInfo) -> CoinScore:
        """综合评分：流动性 + 趋势 + 成交量"""
        reasons = []

        # 流动性评分（0-40）
        qv = coin.quote_volume_24h
        if qv >= 50_000_000:
            liquidity = 40
            reasons.append("流动性极佳")
        elif qv >= 10_000_000:
            liquidity = 30
            reasons.append("流动性良好")
        elif qv >= 3_000_000:
            liquidity = 22
            reasons.append("流动性一般")
        else:
            liquidity = 15
            reasons.append("流动性偏低")

        # 趋势评分（0-35）
        chg = coin.change_24h
        if chg >= 30:
            trend = 30
            reasons.append("涨幅很大，追高风险")
        elif chg >= 15:
            trend = 25
            reasons.append("强势上涨")
        elif chg >= 5:
            trend = 20
            reasons.append("温和上涨")
        elif chg >= -5:
            trend = 15
            reasons.append("震荡区间")
        else:
            trend = 8
            reasons.append("弱势下跌")

        # 成交量评分（0-25）
        if coin.volume_24h >= 50_000_000:
            volume_score = 25
        elif coin.volume_24h >= 10_000_000:
            volume_score = 20
        elif coin.volume_24h >= 3_000_000:
            volume_score = 15
        else:
            volume_score = 10

        score = liquidity + trend + volume_score

        # 风险评估（统一模块）
        risk = evaluate_risk(change_pct=chg, volume_usdt=coin.quote_volume_24h, is_new_coin=False)
        risk_level = risk["risk_level"]
        suggestion = f"{risk['action']}｜止损 {risk['stop_loss']}"

        return CoinScore(
            symbol=coin.symbol,
            base_asset=coin.base_asset,
            score=score,
            risk_level=risk_level,
            liquidity_score=liquidity,
            trend_score=trend,
            volume_score=volume_score,
            suggestion=suggestion,
            reasons=reasons,
        )

    def make_suggestion(self, risk: int, change_24h: float) -> str:
        if risk <= 2:
            return "相对安全，可小仓试水，建议止损 -5%"
        if risk == 3:
            return "风险中等，小仓位为宜，建议止损 -3%"
        if risk == 4:
            return "风险较高，不建议追高，等待回调"
        return "风险极高，观望为主"

    def analyze(self, top_n: int = 5) -> list[dict]:
        coins = self.fetch_market_data()
        scored = [self.score_coin(c) for c in coins]
        scored.sort(key=lambda x: x.score, reverse=True)

        results = []
        for s in scored[:top_n]:
            results.append({
                "symbol": s.symbol,
                "base_asset": s.base_asset,
                "score": round(s.score, 2),
                "risk_level": s.risk_level,
                "liquidity_score": s.liquidity_score,
                "trend_score": s.trend_score,
                "volume_score": s.volume_score,
                "suggestion": s.suggestion,
                "reasons": s.reasons,
            })
        return results


# ============================================================
# Skill 接口函数
# ============================================================
_analyzer: Optional[CoinAnalyzer] = None


def get_analyzer() -> CoinAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = CoinAnalyzer()
    return _analyzer


def get_potential_coins(top_n: int = 5) -> list[dict]:
    """获取潜力币推荐列表"""
    analyzer = get_analyzer()
    return analyzer.analyze(top_n)


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from tg_config import get_tg_config

    cfg = load_config()
    token, chat_id = get_tg_config(cfg)

    analyzer = CoinAnalyzer()
    interval = cfg.get("analyzer", {}).get("interval_seconds", 60)

    logger.info("Coin Analyzer 启动成功，开始循环推送...")
    logger.info(f"推送间隔: {interval}s | ChatID: {chat_id}")

    while True:
        try:
            res = analyzer.analyze(3)
            logger.info(f"分析完成，候选数: {len(res)}")
            if token and chat_id:
                if not res:
                    logger.info("暂无符合条件的潜力币，发送空提示")
                    send_message(token, chat_id, "📭 暂无符合条件的潜力币")
                else:
                    lines = ["🔍 <b>24h 潜力币 Top 3</b>"]
                    for i, r in enumerate(res, 1):
                        stars = "⭐" * int(r["risk_level"])
                        lines.append(
                            f"\n<b>{i}. {r['base_asset']}</b>  总分 <b>{r['score']}</b>"
                            f"\n   流动性: {r['liquidity_score']}/40 | 趋势: {r['trend_score']}/35 | 量: {r['volume_score']}/25"
                            f"\n   风险: {stars} | {r['suggestion']}"
                        )
                    lines.append("\n🌊 用 AI 建设加密，和币安一起逐浪 Web3！")
                    send_message(token, chat_id, "\n".join(lines))
            else:
                for r in res:
                    print(r)
        except Exception as e:
            logger.error(f"分析失败: {e}")

        time.sleep(interval)
