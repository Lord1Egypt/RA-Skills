import os
import sys
import pandas as pd
import requests
import time
from datetime import datetime
import io

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_fetcher import BinanceFetcher
from src.strategy import ChoiGPTStrategy
from src.chart_generator import generate_analysis_chart
from config.config import *

class MarketScannerService:
    """폭등(숏) 및 폭락(매집/롱) 종목 통합 분석 서비스"""

    def __init__(self):
        self.fetcher = BinanceFetcher(API_KEY, API_SECRET, use_testnet=False)
        self.strategy = ChoiGPTStrategy(min_confidence=0.60) # 브리핑용으로 약간 완화

    def get_top_opportunities(self):
        """급등주 2개, 매집주 2개 및 분석 차트 생성"""
        print(f"[*] Starting Intelligent Market Scan... ({datetime.now()})")
        
        try:
            resp = requests.get("https://fapi.binance.com/fapi/v1/ticker/24hr", timeout=10)
            tickers = resp.json()
            usdt_tickers = [t for t in tickers if t['symbol'].endswith('USDT')]
            
            # 1. 숏 후보 (급등주)
            high_rise = sorted(usdt_tickers, key=lambda x: float(x['priceChangePercent']), reverse=True)[:15]
            # 2. 롱 후보 (최근 폭락 또는 횡보 매집 - 거래량 상위 중 등락폭 적은 것)
            # 여기서는 최근 24시간 하락폭이 크거나 횡보 중인 종목 위주
            accumulation = sorted(usdt_tickers, key=lambda x: float(x['priceChangePercent']))[:15]
            
            candidate_symbols = list(set([t['symbol'] for t in high_rise] + [t['symbol'] for t in accumulation]))
            candidate_symbols = [s for s in candidate_symbols if s not in EXCLUDED_SYMBOLS]

            results = []
            for symbol in candidate_symbols:
                ticker_info = next(t for t in usdt_tickers if t['symbol'] == symbol)
                change_24h = float(ticker_info['priceChangePercent'])
                
                # 데이터 수집 (1h 메인 분석)
                df_entry = self.fetcher.get_klines(symbol, "15m", limit=300)
                df_chart = self.fetcher.get_klines(symbol, "1h", limit=150)
                df_htf = self.fetcher.get_klines(symbol, "4h", limit=100)
                
                if df_chart.empty: continue
                
                # 전략 분석
                analysis = self.strategy.analyze(df_entry, symbol, df_htf, df_1h=df_chart)
                if not analysis: continue
                
                # 매집/급등 점수 계산 (이전 스크립트 로직 활용)
                score = 0
                pd_pos = analysis.pd_zone.get('current_position', 0.5)
                
                if change_24h > 10 and analysis.signal and analysis.signal.direction == 'SHORT':
                    # 급등주 숏 기회
                    score = change_24h * 0.5 + analysis.signal.confidence * 10
                    cat = "HIGH_RISE"
                elif pd_pos < 0.3 and (analysis.signal and analysis.signal.direction == 'LONG' or analysis.smc_steps.get(2, -1) != -1):
                    # 매집주 롱 기회
                    score = (0.5 - pd_pos) * 20 + (analysis.signal.confidence * 10 if analysis.signal else 5)
                    cat = "ACCUMULATION"
                else:
                    continue

                results.append({
                    'symbol': symbol,
                    'category': cat,
                    'score': score,
                    'analysis': analysis,
                    'change_24h': change_24h,
                    'df_chart': df_chart
                })
                time.sleep(0.05)

            # 카테고리별 TOP 2 추출
            top_shorts = sorted([r for r in results if r['category'] == 'HIGH_RISE'], key=lambda x: x['score'], reverse=True)[:2]
            top_longs = sorted([r for r in results if r['category'] == 'ACCUMULATION'], key=lambda x: x['score'], reverse=True)[:2]
            
            final_targets = top_shorts + top_longs
            
            report_lines = [
                "🚀 <b>실시간 폭등 및 폭락 종목 포진 브리핑</b>",
                f"분석 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
                "현재 시장 상황에서 SMC/ICT 관점으로 가장 '손익비'와 '신뢰도'가 높은 4개 종목을 엄선했습니다.\n"
            ]
            
            charts = []
            
            # 결과 생성
            for i, target in enumerate(final_targets):
                s = target['symbol']
                an = target['analysis']
                cat_name = "🔥 급등 후 반전(SHORT)" if target['category'] == 'HIGH_RISE' else "💎 매집 후 슈팅(LONG)"
                
                # 차트 이미지 생성
                chart_bytes = generate_analysis_chart(
                    df=target['df_chart'],
                    symbol=s,
                    analysis_result=an,
                    signal=an.signal
                )
                charts.append({'symbol': s, 'data': chart_bytes})
                
                # 텍스트 정보
                report_lines.append(f"<b>{i+1}. {s}</b> ({cat_name})")
                report_lines.append(f"• 24h 변동: {target['change_24h']:+.1f}%")
                if an.signal:
                    report_lines.append(f"• 포지션: <b>{an.signal.direction}</b> (Conf {an.signal.confidence:.0%})")
                    report_lines.append(f"• 타점: {an.signal.entry_price:,.6g} | R:R {self._calc_rr(an.signal):.1f}")
                else:
                    report_lines.append(f"• 상태: 매집 진행 중 (구조 분석 중)")
                
                # 요약 내러티브 (HTML 태그 처리 유의)
                narrative = an.narrative.replace('', '').replace('Unknown', 'SMC 구조')
                report_lines.append(f"• 분석: {narrative}\n")

            report_lines.append("<i>* 위 차트 이미지를 통해 구조 변화(MSS) 및 유동성 구간(Sweep)을 확인하십시오.</i>")
            
            return "\n".join(report_lines), charts

        except Exception as e:
            print(f"[X] Briefing error: {e}")
            import traceback
            traceback.print_exc()
            return f"❌ 브리핑 생성 중 오류가 발생했습니다: {e}", []

    def _calc_rr(self, signal):
        risk = abs(signal.entry_price - signal.stop_loss)
        reward = abs(signal.take_profit - signal.entry_price)
        return reward / risk if risk > 0 else 0

if __name__ == "__main__":
    service = MarketScannerService()
    text, charts = service.get_top_opportunities()
    print(text)
    print(f"Captured {len(charts)} charts.")
