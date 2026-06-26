"""
ChoiGPT 전략 엔진 (Simplified Edition)
- 핵심 전략: Sweepzone V1 (Ichimoku + 20MA)
- 목적: 24/7 자동 매매 안정성 확보 및 불필요한 복잡성 제거
"""

import logging
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple, Dict
from dataclasses import dataclass, field
import sys
import os

# 프로젝트 루트 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config.config import *
from src.indicators import (
    TradeSignal, MarketStructure, FVG, OrderBlock, BreakerBlock,
    LiquidityLevel, BPR, RejectionBlock, RangeBox, Neckline,
    detect_market_structure, calculate_ma20, calculate_rsi, calculate_atr,
    calculate_mfi, calculate_wavetrend, get_premium_discount_zone
)
from src.strategies.sweepzone_v1 import analyze_sweepzone_v1

logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    symbol: str
    timestamp: str
    current_price: float
    daily_ms: MarketStructure
    htf_ms: MarketStructure
    ltf_ms: MarketStructure
    pd_zone: dict
    rsi_val: float
    atr_val: float
    signal: Optional[TradeSignal] = None
    analysis_text: str = ""
    reasons: List[str] = field(default_factory=list)

class ChoiGPTStrategy:
    def __init__(self, min_confidence: float = 0.7):
        self.logger = logging.getLogger(__name__)
        self.min_confidence = min_confidence

    def analyze(self, df_15m: pd.DataFrame, symbol: str, df_4h: pd.DataFrame, 
                df_1d: pd.DataFrame = None, df_1h: pd.DataFrame = None, 
                df_5m: pd.DataFrame = None) -> Optional[AnalysisResult]:
        """메인 분석 루프: 데이터프레임을 받아 최종 매매 신호 산출"""
        try:
            if df_15m is None or df_15m.empty:
                return None

            current_price = df_15m['close'].iloc[-1]
            timestamp = str(df_15m.index[-1])

            # 1. 기초 지표 및 구조 분석
            daily_ms = detect_market_structure(df_1d) if df_1d is not None else MarketStructure()
            htf_ms = detect_market_structure(df_4h) if df_4h is not None else MarketStructure()
            ltf_ms = detect_market_structure(df_15m)
            
            pd_zone = get_premium_discount_zone(df_15m)
            rsi_val = calculate_rsi(df_15m).iloc[-1]
            atr_val = calculate_atr(df_15m).iloc[-1]

            # 2. 핵심 전략 실행 (Sweepzone V1 우선)
            signal = None
            if df_1d is not None:
                signal = analyze_sweepzone_v1(df_1d, symbol)

            # 3. 결과 정리
            result = AnalysisResult(
                symbol=symbol,
                timestamp=timestamp,
                current_price=current_price,
                daily_ms=daily_ms,
                htf_ms=htf_ms,
                ltf_ms=ltf_ms,
                pd_zone=pd_zone,
                rsi_val=rsi_val,
                atr_val=atr_val,
                signal=signal
            )

            # 4. 분석 텍스트 생성
            result.analysis_text = self._generate_summary(result)
            
            return result

        except Exception as e:
            self.logger.error(f"❌ {symbol} 분석 중 오류 발생: {e}", exc_info=True)
            return None

    def _generate_summary(self, result: AnalysisResult) -> str:
        """분석 결과 요약 텍스트 생성"""
        lines = [
            f"<b>{result.symbol} Analysis Report</b>",
            f"Price: {result.current_price:,.2f}",
            f"Trend: 1D {result.daily_ms.trend} | 4H {result.htf_ms.trend} | 15M {result.ltf_ms.trend}",
            f"RSI: {result.rsi_val:.1f} | ATR: {result.atr_val:.2f}",
            "---"
        ]
        
        if result.signal:
            lines.append(f"<b>SIGNAL: {result.signal.direction}</b>")
            lines.append(f"Mode: {result.signal.mode} | Conf: {result.signal.confidence*100:.1f}%")
            lines.append(f"Entry: {result.signal.entry_price:,.2f}")
            lines.append(f"SL: {result.signal.stop_loss:,.2f}")
            lines.append(f"TP: {result.signal.take_profit:,.2f}")
            lines.append("Reasons:")
            for r in result.signal.reasons:
                lines.append(f"- {r}")
        else:
            lines.append("<b>NO SIGNAL (WAITING)</b>")
            
        return "\n".join(lines)
