"""
거래 복기 분석 시스템 (Trade Review & Post-Mortem)
완료된 각 거래에 대한 상세 분석 및 개선 제안 제공

Features:
- 이겼을 때 분석: 왜 성공했는가?
- 졌을 때 분석: 어떤 요소가 실패했는가?
- 신호 효율성: 각 진입 근거별 성공률
- 개선 제안: 추후 거래 개선을 위한 방향
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
from collections import defaultdict

from src.trade_journal import CompletedTrade

logger = logging.getLogger(__name__)


class TradeReviewAnalyzer:
    """거래 복기 분석"""

    def __init__(self):
        self.reviews: List[Dict] = []

    def analyze_trade(self, trade: CompletedTrade) -> Dict:
        """개별 거래 복기 분석"""

        is_win = trade.pnl_pct > 0
        win_loss_text = "🟢 **WIN**" if is_win else "🔴 **LOSS**"

        # 1. 거래 개요
        overview = {
            'symbol': trade.symbol,
            'direction': trade.direction,
            'entry_price': trade.entry_price,
            'exit_price': trade.exit_price,
            'quantity': trade.quantity,
            'leverage': trade.leverage,
            'duration_minutes': trade.duration_minutes,
            'exit_type': trade.exit_type,
            'realized_pnl_usdt': trade.realized_pnl,
            'pnl_pct': trade.pnl_pct,
            'confidence_score': trade.confidence_score,
            'rr_ratio': trade.rr_ratio
        }

        # 2. 신호 분석
        signal_analysis = self._analyze_signals(trade)

        # 3. 승패 분석
        win_loss_analysis = self._analyze_win_loss(trade, is_win)

        # 4. 개선 제안
        recommendations = self._generate_recommendations(trade, is_win, signal_analysis)

        review = {
            'timestamp': datetime.now().isoformat(),
            'win_loss': win_loss_text,
            'overview': overview,
            'signal_analysis': signal_analysis,
            'win_loss_analysis': win_loss_analysis,
            'recommendations': recommendations
        }

        self.reviews.append(review)
        return review

    def _analyze_signals(self, trade: CompletedTrade) -> Dict:
        """진입 근거 분석"""

        signal_count = len(trade.reasons)
        signal_types = {
            'IFVG': 0, 'FVG': 0, 'OB': 0, 'BPR': 0,
            'DISCOUNT': 0, 'PREMIUM': 0, 'MSS': 0, 'DOL': 0,
            'RSI': 0, 'SENTIMENT': 0, 'RANGE': 0, 'SWEEP': 0
        }

        for reason in trade.reasons:
            for signal_type in signal_types.keys():
                if signal_type in reason.upper():
                    signal_types[signal_type] += 1

        active_signals = {k: v for k, v in signal_types.items() if v > 0}

        return {
            'total_signal_count': signal_count,
            'unique_signals': active_signals,
            'signal_strength': "Strong 💪" if signal_count >= 3 else "Moderate 👍" if signal_count >= 2 else "Weak ⚠️",
            'confidence_score': trade.confidence_score,
            'details': trade.reasons
        }

    def _analyze_win_loss(self, trade: CompletedTrade, is_win: bool) -> Dict:
        """승패 분석"""

        if is_win:
            return {
                'category': 'Successful Trade',
                'exit_trigger': trade.exit_type,  # TP1, TP2, MANUAL 등
                'key_factors': [
                    f"✅ {trade.exit_type} 달성 - 목표가 도달",
                    f"✅ 신호 {trade.confidence_score:.0%} 정확도로 작동",
                    f"✅ {trade.duration_minutes}분 보유 - 단기 수익"
                ] if trade.duration_minutes < 480 else [
                    f"✅ {trade.exit_type} 달성 - 목표가 도달",
                    f"✅ 신호 {trade.confidence_score:.0%} 정확도로 작동",
                    f"✅ {trade.duration_minutes}분 보유 - 중기 수익"
                ]
            }
        else:
            return {
                'category': 'Loss Trade',
                'exit_trigger': trade.exit_type,  # SL, MANUAL 등
                'key_factors': [
                    f"❌ {trade.exit_type} 타격 - 손실",
                    f"❌ 신호가 부분적 작동 (신뢰도: {trade.confidence_score:.0%})",
                    f"❌ {trade.duration_minutes}분 보유 후 손절"
                ]
            }

    def _generate_recommendations(self, trade: CompletedTrade, is_win: bool,
                                 signal_analysis: Dict) -> List[str]:
        """개선 제안 생성"""

        recommendations = []

        # 신호 강도 기반 제안
        if signal_analysis['signal_strength'] == "Weak ⚠️":
            recommendations.append(
                "🔧 신호가 약했습니다. 다음에는 2개 이상의 신호 확인 후 진입하세요."
            )

        # 보유 시간 기반 제안
        if trade.duration_minutes < 5:
            if is_win:
                recommendations.append(
                    "⚡ 스캘핑 성공! 이러한 패턴을 계속 모니터링하세요."
                )
            else:
                recommendations.append(
                    "⚠️ 매우 짧은 시간에 손절되었습니다. 더 큰 차트에서 구조를 재확인하세요."
                )

        # 손익률 기반 제안
        if not is_win:
            if trade.pnl_pct < -2:
                recommendations.append(
                    "💥 큰 손실입니다. SL 레벨을 더 가깝게 설정하거나 신호 필터를 강화하세요."
                )
            elif trade.pnl_pct < 0:
                recommendations.append(
                    "📉 신호 신뢰도가 낮았을 수 있습니다. 다음 진입 시 Confidence 점수를 높이세요."
                )

        if is_win and trade.pnl_pct > 2:
            recommendations.append(
                "🎯 훌륭한 거래! 이 승리의 요인들을 재현하도록 노력하세요."
            )

        # RR 비율 기반 제안
        if trade.rr_ratio > 0:
            if trade.rr_ratio < 1.0:
                recommendations.append(
                    f"⚠️ RR 비율이 {trade.rr_ratio:.2f}로 낮습니다. 최소 1.5:1 이상을 목표하세요."
                )
            elif trade.rr_ratio > 3.0 and is_win:
                recommendations.append(
                    f"🏆 우수한 RR 비율({trade.rr_ratio:.2f}:1)로 큰 수익을 획득했습니다."
                )

        if not recommendations:
            recommendations.append(
                "💡 표준 거래입니다. 신호와 SL 레벨을 지속적으로 모니터링하세요."
            )

        return recommendations

    def get_signal_effectiveness(self, trades: List[CompletedTrade]) -> Dict:
        """신호별 효율성 분석"""

        signal_stats = defaultdict(lambda: {'count': 0, 'wins': 0, 'losses': 0, 'total_pnl': 0})

        for trade in trades:
            for reason in trade.reasons:
                # 신호 타입 추출 (예: "✅ Discount 구간 (16.1%)" -> "Discount")
                signal_name = reason.split()[1] if len(reason.split()) > 1 else reason

                signal_stats[signal_name]['count'] += 1
                signal_stats[signal_name]['total_pnl'] += trade.pnl_pct

                if trade.pnl_pct > 0:
                    signal_stats[signal_name]['wins'] += 1
                else:
                    signal_stats[signal_name]['losses'] += 1

        # 효율성 계산
        effectiveness = {}
        for signal, stats in signal_stats.items():
            total = stats['count']
            win_rate = (stats['wins'] / total * 100) if total > 0 else 0
            avg_pnl = stats['total_pnl'] / total if total > 0 else 0

            effectiveness[signal] = {
                'count': total,
                'win_rate': win_rate,
                'avg_pnl_pct': avg_pnl,
                'wins': stats['wins'],
                'losses': stats['losses']
            }

        # 효율성 순 정렬
        return dict(sorted(effectiveness.items(),
                          key=lambda x: x[1]['win_rate'],
                          reverse=True))

    def generate_review_report(self, trades: List[CompletedTrade]) -> str:
        """거래 복기 보고서 생성"""

        report_lines = [
            "# 📋 거래 복기 보고서\n",
            f"**생성일시:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"**분석 거래 수:** {len(trades)}\n"
        ]

        if not trades:
            return "\n".join(report_lines) + "\n분석 거래가 없습니다.\n"

        # 1. 신호 효율성
        signal_eff = self.get_signal_effectiveness(trades)

        report_lines.append("\n## 📊 신호 효율성 분석\n")
        report_lines.append("| 신호 | 사용 횟수 | 승률 | 평균 PnL | 승리 | 손실 |")
        report_lines.append("|------|---------|------|---------|------|------|")

        for signal, stats in signal_eff.items():
            report_lines.append(
                f"| {signal} | {stats['count']} | {stats['win_rate']:.1f}% | "
                f"{stats['avg_pnl_pct']:+.2f}% | {stats['wins']} | {stats['losses']} |"
            )

        # 2. 최근 거래 복기
        report_lines.append("\n## 🔍 최근 거래 복기 (최근 5건)\n")

        for trade in trades[-5:]:
            review = self.analyze_trade(trade)
            is_win = trade.pnl_pct > 0

            report_lines.append(f"\n### {trade.symbol} - {review['win_loss']}")
            report_lines.append(f"- **진입:** {trade.entry_price} | **종료:** {trade.exit_price}")
            report_lines.append(
                f"- **손익:** {trade.pnl_pct:+.2f}% ({trade.realized_pnl:+.4f} USDT)"
            )
            report_lines.append(f"- **보유:** {trade.duration_minutes}분 | **종료 유형:** {trade.exit_type}")
            report_lines.append(f"- **신호 강도:** {review['signal_analysis']['signal_strength']}")

            report_lines.append("- **개선 제안:**")
            for rec in review['recommendations']:
                report_lines.append(f"  - {rec}")

        return "\n".join(report_lines)
