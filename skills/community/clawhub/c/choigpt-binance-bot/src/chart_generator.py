"""
Nabuk AI 스타일 차트 생성기 - V2.0
깔끔한 SMC 구조 시각화: BPR 박스 + FVG 라인 + 진입/SL/TP
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe

def _fmt_price(p: float) -> str:
    """가격 크기에 따라 소수점을 동적으로 조절하는 포맷 함수"""
    if p >= 1000: return f"{p:,.1f}"
    if p >= 10: return f"{p:,.2f}"
    if p >= 0.1: return f"{p:,.4f}"
    s = f"{p:.6f}"
    return s.rstrip('0').rstrip('.') if '.' in s else s

import pandas as pd
import numpy as np
import io
import threading
from datetime import datetime
from typing import Optional, List

_chart_lock = threading.Lock()

from config.config import CHART_CANDLES, CHART_DPI, CHART_FIGSIZE, CHART_TF

# ============================================================
# 색상 팔레트 (Nabuk AI / TradingView 다크 테마)
# ============================================================
C = {
    'bg':          '#0d1117',   # 배경
    'bg2':         '#161b22',   # 패널
    'grid':        '#21262d',   # 그리드
    'text':        '#e6edf3',   # 텍스트
    'text_dim':    '#8b949e',   # 흐린 텍스트
    'candle_up':   '#26a69a',   # 상승 캔들 (틸)
    'candle_dn':   '#ef5350',   # 하락 캔들 (빨강)
    'bpr':         '#00bcd4',   # BPR 박스 (틸)
    'fvg_bull':    '#26a69a',   # 상승 FVG
    'fvg_bear':    '#ef5350',   # 하락 FVG
    'ob_bull':     '#ab47bc',   # 상승 OB
    'ob_bear':     '#ff9800',   # 하락 OB
    'bsl':         '#42a5f5',   # BSL (파랑)
    'ssl':         '#ef5350',   # SSL (빨강)
    'entry':       '#ffffff',   # 진입가 (흰색)
    'sl':          '#f44336',   # 손절
    'tp':          '#4caf50',   # 익절
    'price':       '#ffd700',   # 현재가 (골드)
    'fib':         '#9c27b0',   # 피보나치 (보라)
}


# ============================================================
# 내부 유틸 함수
# ============================================================

def _price_label(ax, x, y, text, bg_color, text_color='white', fontsize=8, ha='left'):
    """우측 가격 박스 라벨 (TradingView 스타일)"""
    bbox = dict(boxstyle='round,pad=0.25', fc=bg_color, ec='none', alpha=0.92)
    ax.text(x, y, f' {text} ', color=text_color, fontsize=fontsize,
            fontweight='bold', va='center', ha=ha, bbox=bbox, zorder=15,
            clip_on=False)


def _draw_level_line(ax, y, x_start, x_end, color, lw=1.0,
                     ls='--', label=None, x_label=None, fontsize=7.5):
    """수평 레벨 라인 + 우측 라벨"""
    ax.hlines(y, x_start, x_end, colors=color, linewidths=lw,
              linestyles=ls, zorder=4, alpha=0.85)
    if label and x_label is not None:
        _price_label(ax, x_label, y, label, color, fontsize=fontsize)


def _draw_zone_box(ax, x0, x1, y_lo, y_hi, color, alpha_fill=0.10,
                   alpha_edge=0.70, lw=0.8, label=None, x_label=None, fontsize=7.5):
    """SMC 구조 박스 (BPR / FVG / OB)"""
    rect = mpatches.Rectangle(
        (x0, y_lo), x1 - x0, y_hi - y_lo,
        linewidth=lw, edgecolor=color, facecolor=color,
        alpha=alpha_fill, zorder=3
    )
    # 테두리만 별도로 선명하게
    rect_edge = mpatches.Rectangle(
        (x0, y_lo), x1 - x0, y_hi - y_lo,
        linewidth=lw, edgecolor=color, facecolor='none',
        alpha=alpha_edge, zorder=4
    )
    ax.add_patch(rect)
    ax.add_patch(rect_edge)
    if label and x_label is not None:
        mid_y = (y_hi + y_lo) / 2
        _price_label(ax, x_label, mid_y, label, color, fontsize=fontsize)


def _draw_candlesticks(ax, df: pd.DataFrame):
    """인덱스 기반 캔들스틱"""
    w_body = 0.55
    w_wick = 0.08

    up   = df[df['close'] >= df['open']]
    down = df[df['close'] <  df['open']]

    # 상승
    ax.bar(up['idx'],   up['close'] - up['open'],   w_body, bottom=up['open'],
           color=C['candle_up'],   alpha=0.95, zorder=3)
    ax.bar(up['idx'],   up['high']  - up['close'],  w_wick, bottom=up['close'],
           color=C['candle_up'],   alpha=0.95, zorder=3)
    ax.bar(up['idx'],   up['low']   - up['open'],   w_wick, bottom=up['open'],
           color=C['candle_up'],   alpha=0.95, zorder=3)

    # 하락
    ax.bar(down['idx'], down['close'] - down['open'], w_body, bottom=down['open'],
           color=C['candle_dn'],   alpha=0.95, zorder=3)
    ax.bar(down['idx'], down['high']  - down['open'], w_wick, bottom=down['open'],
           color=C['candle_dn'],   alpha=0.95, zorder=3)
    ax.bar(down['idx'], down['low']   - down['close'], w_wick, bottom=down['close'],
           color=C['candle_dn'],   alpha=0.95, zorder=3)


# ============================================================
# 메인 차트 생성
# ============================================================

def generate_analysis_chart(
    df: pd.DataFrame,
    symbol: str,
    analysis_result,
    signal=None,
    save_path: str = None,
    user_position: dict = None
) -> bytes:
    with _chart_lock:
        return _build_chart(df, symbol, analysis_result, signal, save_path, user_position)


def _build_chart(df, symbol, ar, signal, save_path, user_position=None):
    """Nabuk AI 스타일 차트"""
    # 데이터 준비
    plot_df = df.tail(CHART_CANDLES).copy().reset_index(drop=False)
    plot_df['idx'] = range(len(plot_df))
    n = len(plot_df)

    x0       = 0
    x_end    = n - 1
    x_lbl    = x_end + n * 0.11  # 라벨 공간

    # ── 피겨 ──
    fig, ax = plt.subplots(1, 1, figsize=CHART_FIGSIZE, facecolor=C['bg'])
    ax.set_facecolor(C['bg'])
    ax.tick_params(colors=C['text_dim'], labelsize=8.5)
    for sp in ax.spines.values():
        sp.set_color(C['grid'])
    ax.grid(True, color=C['grid'], linewidth=0.4, alpha=0.6, zorder=0)
    ax.set_xlim(-1, x_lbl + 2)

    # ── 캔들스틱 ──
    _draw_candlesticks(ax, plot_df)

    # ── X축 라벨 ──
    step = max(1, n // 7)
    ticks = list(range(0, n, step))
    def _tlbl(i):
        try:
            t = plot_df['timestamp'].iloc[i] if 'timestamp' in plot_df.columns else plot_df.index[i]
            return t.strftime('%m/%d %H:%M') if hasattr(t, 'strftime') else str(t)[:11]
        except:
            return str(i)
    ax.set_xticks(ticks)
    ax.set_xticklabels([_tlbl(i) for i in ticks], rotation=0, ha='center',
                        fontsize=8, color=C['text_dim'])

    # ─────────────────────────────────────────
    # SMC 구조 레이어 그리기
    # ─────────────────────────────────────────

    # 1. BPR (Balanced Price Range) - 틸 박스 ★ 핵심
    if ar and getattr(ar, 'bprs', None):
        for bpr in ar.bprs:
            top = getattr(bpr, 'top', None) or getattr(bpr, 'high', None)
            bot = getattr(bpr, 'bottom', None) or getattr(bpr, 'low', None)
            if top and bot:
                lbl = f"{CHART_TF.upper()} BPR [{_fmt_price(bot)}~{_fmt_price(top)}]"
                _draw_zone_box(ax, x0, x_end, bot, top,
                               C['bpr'], alpha_fill=0.03, alpha_edge=0.15, lw=0.8,
                               label=lbl, x_label=x_end, fontsize=6)

    # 2. FVG (Fair Value Gap)
    if ar and getattr(ar, 'fvgs', None):
        for fvg in ar.fvgs:
            if getattr(fvg, 'filled', False):
                continue
            color = C['fvg_bull'] if fvg.is_bullish else C['fvg_bear']
            tf_tag = 'Bull' if fvg.is_bullish else 'Bear'
            lbl = f"FVG {tf_tag} [{_fmt_price(fvg.bottom)}~{_fmt_price(fvg.top)}]"
            _draw_zone_box(ax, x0, x_end, fvg.bottom, fvg.top,
                           color, alpha_fill=0.02, alpha_edge=0.10, lw=0.5,
                           label=lbl, x_label=x_end, fontsize=6)

    # 3. Order Block
    if ar and getattr(ar, 'order_blocks', None):
        for ob in ar.order_blocks[:3]:   # 최근 3개만
            color = C['ob_bull'] if ob.is_bullish else C['ob_bear']
            lbl = f"{'Bull' if ob.is_bullish else 'Bear'} OB [{_fmt_price(ob.low)}~{_fmt_price(ob.high)}]"
            _draw_zone_box(ax, x0, x_end, ob.low, ob.high,
                           color, alpha_fill=0.03, alpha_edge=0.15, lw=0.5,
                           label=lbl, x_label=x_end, fontsize=6)

    # 4. 유동성 레벨 (BSL / SSL)
    if ar and getattr(ar, 'liquidity_levels', None):
        for lvl in ar.liquidity_levels:
            if getattr(lvl, 'swept', False):
                continue
            is_bsl = lvl.level_type == 'BSL'
            color  = C['bsl'] if is_bsl else C['ssl']
            # 기존 이름 및 라벨을 무시하고 희미하게만 표시 (간소화)
            ax.hlines(lvl.price, x0, x_end, colors=color, linewidths=0.5,
                      linestyles=':', zorder=1, alpha=0.15)
                      
    # 4-0. 다중 타임프레임 강력한 S/R (★ V8.0 핵심)
    if ar and getattr(ar, 'multi_tf_sr', None):
        for sr in ar.multi_tf_sr:
            is_res = sr['type'] == 'R'
            color = '#ff9800' if is_res else '#00e676'  # 오렌지 / 밝은녹색
            name = f"{sr['tf']} {sr['type']} {_fmt_price(sr['price'])}"
            _draw_level_line(ax, sr['price'], x0, x_end, color,
                             lw=1.5, ls='-', label=name, x_label=x_lbl, fontsize=8)

    # 5. SMC 4-Step Markers (❶❷❸❹) ★ 핵심 V8.0
    if ar and getattr(ar, 'smc_steps', None):
        step_map = {
            1: ("❶ Bias", "#26a69a"), # 티파니 블루
            2: ("❷ Sweep", "#ff9800"),# 오렌지
            3: ("❸ MSS", "#ab47bc"),  # 보라
            4: ("❹ Entry", "#00e676") # 밝은 녹색
        }
        for step_num, idx in ar.smc_steps.items():
            if idx <= 0: continue
            
            # plot_df 상의 인덱스로 변환
            # ar.smc_steps의 인덱스는 전체 df 기준이므로 차트 표시용(tail N)으로 변환
            base_len = getattr(ar, 'df_len', 0) or 0
            if base_len == 0: # 백업
                plot_idx = idx - (len(df) - n)
            else:
                plot_idx = idx - (base_len - n)
            
            if 0 <= plot_idx < n:
                label, color = step_map.get(step_num, ("", "white"))
                y_val = plot_df['high'].iloc[plot_idx] if step_num % 2 == 0 else plot_df['low'].iloc[plot_idx]
                va = 'bottom' if step_num % 2 == 0 else 'top'
    # 5. SMC 4-Step 시각화 (NEW: ❶❷❸❹)
    if ar and hasattr(ar, 'smc_steps'):
        plot_start_idx = len(df) - n
        steps_icons = {1: '❶', 2: '❷', 3: '❸', 4: '❹'}
        for step, abs_idx in ar.smc_steps.items():
            if abs_idx < 0: continue
            
            rel_idx = abs_idx - plot_start_idx
            if 0 <= rel_idx < n:
                # 캔들 상/하단 여부 판단 (Sweep과 MSS는 보통 반전 지점이므로 Low/High 근처)
                candle = plot_df.iloc[rel_idx]
                is_bull = ar.ltf_ms.trend == "BULLISH" if ar.ltf_ms else True
                
                if step == 1: # Bias (마지막 봉)
                    y_pos = candle['high'] * 1.002
                    va = 'bottom'
                elif step == 2: # Sweep (저점/고점 돌파)
                    y_pos = candle['low'] * 0.998 if is_bull else candle['high'] * 1.002
                    va = 'top' if is_bull else 'bottom'
                elif step == 3: # MSS (구조 돌파)
                    y_pos = candle['high'] * 1.002 if is_bull else candle['low'] * 0.998
                    va = 'bottom' if is_bull else 'top'
                else: # Entry
                    y_pos = candle['low'] * 0.997 if is_bull else candle['high'] * 1.003
                    va = 'top' if is_bull else 'bottom'

                ax.text(rel_idx, y_pos, steps_icons[step], color=C['price'], 
                        fontsize=14, fontweight='bold', ha='center', va=va, 
                        path_effects=[pe.withStroke(linewidth=2, foreground="black")],
                        zorder=12)

    # 6. 진입 신호 화살표 + TP/SL 라인
    if signal:
        entry = signal.entry_price
        sl_p  = signal.stop_loss
        tp1   = signal.take_profit
        tp2   = getattr(signal, 'take_profit2', None)
        is_long = signal.direction == 'LONG'

        # TP/SL 배경 음영
        ax.axhspan(min(sl_p, entry), max(sl_p, entry),
                   alpha=0.06, color=C['sl'], zorder=2)
        ax.axhspan(min(tp1, entry), max(tp1, entry),
                   alpha=0.06, color=C['tp'], zorder=2)

        # Entry 라인
        ax.hlines(entry, x0, x_end, colors=C['entry'],
                  linewidths=1.6, linestyles='-', zorder=6, alpha=0.95)
        _price_label(ax, x_lbl, entry, f"Entry {entry:,.0f}", '#1565c0', fontsize=8.5)

        # SL 라인
        ax.hlines(sl_p, x0, x_end, colors=C['sl'],
                  linewidths=1.2, linestyles=':', zorder=6, alpha=0.90)
        _price_label(ax, x_lbl, sl_p, f"SL {sl_p:,.0f}", C['sl'], fontsize=8)

        # TP1 라인
        ax.hlines(tp1, x0, x_end, colors=C['tp'],
                  linewidths=1.2, linestyles=':', zorder=6, alpha=0.90)
        _price_label(ax, x_lbl, tp1, f"TP1 {tp1:,.0f}", '#2e7d32', fontsize=8)

        # TP2 라인
        if tp2:
            ax.hlines(tp2, x0, x_end, colors=C['tp'],
                      linewidths=0.9, linestyles=':', zorder=6, alpha=0.70)
            _price_label(ax, x_lbl, tp2, f"TP2 {tp2:,.0f}", '#1b5e20', fontsize=7.5)

        # 방향 화살표 (진입가 위치에)
        arrow_y  = entry
        arrow_dy = (tp1 - entry) * 0.12
        ax.annotate('', xy=(x_end - 2, arrow_y + arrow_dy),
                    xytext=(x_end - 2, arrow_y),
                    arrowprops=dict(arrowstyle='->', color=C['tp'] if is_long else C['sl'],
                                   lw=2.0), zorder=8)

    # 5.5 사용자 계좌 포지션 타점 라인 시각화 (V6.8)
    if user_position:
        u_entry = user_position.get('entry_price', 0)
        u_side = user_position.get('side', 'UNKNOWN')
        
        if u_entry > 0:
            u_color = '#e040fb' # 밝은 보라색 (사용자 고유 라인)
            ax.hlines(u_entry, x0, x_end, colors=u_color,
                      linewidths=2.0, linestyles='-', zorder=9, alpha=0.95)
            # 봇 알고리즘 라벨(우측)과 겹치지 않게, 좌측 끝(x0)에 라벨 배치
            _price_label(ax, x0 + 1, u_entry, f"My {u_side} {u_entry:,.0f}", u_color, fontsize=10, ha='left')

    # 7. 현재 가격 (골드 점선 + 박스)
    cur_price = float(plot_df['close'].iloc[-1])
    ax.hlines(cur_price, x0, x_end, colors=C['price'],
              linewidths=0.9, linestyles=':', zorder=5, alpha=0.75)
    _price_label(ax, x_lbl, cur_price, f"{cur_price:,.1f}", C['price'],
                 text_color='#0d1117', fontsize=9)

    # ─────────────────────────────────────────
    # 헤더 정보 패널
    # ─────────────────────────────────────────
    htf_trend = ''
    ltf_trend = ''
    pd_label  = ''
    if ar:
        htf_trend = getattr(ar.htf_ms, 'trend', '') if ar.htf_ms else ''
        ltf_trend = getattr(ar.ltf_ms, 'trend', '') if ar.ltf_ms else ''
        pd_label  = (ar.pd_zone or {}).get('zone', '')

    # 추세 색상
    def _trend_color(t):
        if 'BULLISH' in t: return '#26a69a'
        if 'BEARISH' in t: return '#ef5350'
        return '#9e9e9e'

    # 제목
    ax.text(0.012, 0.975, f"{symbol}  {CHART_TF.upper()}  SMC Structure",
            transform=ax.transAxes, color=C['text'], fontsize=11,
            fontweight='bold', va='top', zorder=12)

    # HTF / LTF 뱃지
    ax.text(0.012, 0.935,
            f"HTF: {htf_trend[:8]}   LTF: {ltf_trend[:8]}   Zone: {pd_label}",
            transform=ax.transAxes, color=C['text_dim'], fontsize=8.5, va='top')

    # 신호 신뢰도
    if signal:
        dir_color = C['tp'] if signal.direction == 'LONG' else C['sl']
        conf_txt  = f"{signal.direction}  {signal.confidence:.0%}"
        ax.text(0.988, 0.975, conf_txt,
                transform=ax.transAxes, color=dir_color, fontsize=10,
                fontweight='bold', va='top', ha='right',
                bbox=dict(fc=C['bg2'], ec=dir_color, lw=1.2,
                          boxstyle='round,pad=0.35', alpha=0.90))

    # 워터마크
    ax.text(0.988, 0.012, "ChoiGPT Bot  │  Pure SMC/ICT V8.0",
            transform=ax.transAxes, color=C['text_dim'], fontsize=7.5,
            va='bottom', ha='right', alpha=0.60)

    # 상단/우측 테두리 제거
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=CHART_DPI, bbox_inches='tight',
                facecolor=C['bg'], edgecolor='none')
    buf.seek(0)
    data = buf.read()
    plt.close(fig)

    if save_path:
        with open(save_path, 'wb') as f:
            f.write(data)

    return data


# ============================================================
# 하위 호환 함수들
# ============================================================

def draw_candlesticks(ax, df: pd.DataFrame):
    tmp = df.copy().reset_index(drop=False)
    tmp['idx'] = range(len(tmp))
    _draw_candlesticks(ax, tmp)

def draw_candlesticks_by_idx(ax, df: pd.DataFrame):
    _draw_candlesticks(ax, df)

def draw_level_box(ax, x_start, x_end, y_top, y_bottom,
                   color, alpha=0.25, label=None, label_side='right'):
    x_lbl = x_end + (x_end - x_start) * 0.05 if label_side == 'right' else x_start
    _draw_zone_box(ax, x_start, x_end, y_bottom, y_top, color,
                   alpha_fill=alpha, label=label, x_label=x_lbl if label else None)

def draw_horizontal_line(ax, y, x_start, x_end, color, style='--',
                          linewidth=1.0, label=None, label_side='right'):
    x_lbl = x_end if label_side == 'right' else x_start
    _draw_level_line(ax, y, x_start, x_end, color, lw=linewidth, ls=style,
                     label=label, x_label=x_lbl if label else None)

def format_price(price: float, symbol: str = "") -> str:
    if price >= 10000:  return f"${price:,.1f}"
    elif price >= 100:  return f"${price:,.2f}"
    elif price >= 1:    return f"${price:.4f}"
    else:               return f"${price:.6f}"

def generate_analysis_explanation(analysis_result, signal=None) -> str:
    lines = ["━" * 34, "<b>SMC 4-STEP ANALYSIS</b>\n"]

    if analysis_result:
        # HTF/LTF 상태 요약
        htf = getattr(analysis_result.htf_ms, 'trend', 'N/A') if analysis_result.htf_ms else 'N/A'
        ltf = getattr(analysis_result.ltf_ms, 'trend', 'N/A') if analysis_result.ltf_ms else 'N/A'
        
        # 단계별 상태
        sweep_ok = analysis_result.smc_steps.get(2, -1) > 0
        mss_ok = analysis_result.smc_steps.get(3, -1) > 0
        
        # 1-4단계 리포트
        lines.append(f"<b>1. HTF Bias:</b> {htf}")
        lines.append(f"<b>2. Liquidity Sweep:</b> {'감지됨' if sweep_ok else '대기중'}")
        lines.append(f"<b>3. MSS/Displacement:</b> {'발생 확인' if mss_ok else '미발생'}")
        lines.append(f"<b>4. Entry Execution:</b> {'OTE 영역' if signal else '타점 대기중'}\n")

        # 종합 브리핑 생성
        symbol = analysis_result.symbol
        briefing = f"현재 <b>{symbol}</b>는 HTF({htf}) 및 LTF({ltf}) 기준 "
        if htf == 'RANGING':
            briefing += "<b>박스권(Ranging)</b> 상태이며, "
        else:
            briefing += f"<b>{htf} 추세</b> 중이나, "
            
        if not (sweep_ok and mss_ok):
            briefing += "유동성 스윕이나 구조 변화(MSS)가 아직 발견되지 않아 <b>'셋업 대기 중'</b>인 상태입니다."
            briefing += "\n이는 SMC 전략상 무리하게 진입하지 않고 확실한 ❶❷❸ 단계를 기다리는 <b>정상적인 동작</b>입니다. 🧘"
        else:
            briefing += "주요 구조 변화가 확인되어 <b>진입 기회</b>를 포착 중입니다. 🎯"
            
        lines.append(briefing)

        if analysis_result.pd_zone:
            z = analysis_result.pd_zone.get('zone', 'N/A')
            pos = analysis_result.pd_zone.get('current_position', 0)
            lines.append(f"\nMarket Zone: <b>{z}</b> ({pos:.0%})")

    if signal:
        risk = abs(signal.entry_price - signal.stop_loss)
        reward = abs(signal.take_profit - signal.entry_price)
        rr = reward / risk if risk > 0 else 0
        lines.append(f"\n✨ <b>Signal: {signal.direction}</b> {signal.confidence:.0%}")
        lines.append(f"타점: {signal.entry_price:,.2f} | RR 1:{rr:.1f}")
        for r in (signal.reasons or [])[:3]:
            lines.append(f"  • {r}")

    lines.append("\n" + "━" * 34)
    return "\n".join(lines)
