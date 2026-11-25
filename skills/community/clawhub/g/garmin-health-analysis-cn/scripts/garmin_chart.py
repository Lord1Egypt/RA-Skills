#!/usr/bin/env python3
"""
Generate Garmin health HTML reports.
样式：纯内联 SVG（无 Chart.js / 无外部依赖，可离线打开），
与 example/ 比赛分析报告同一设计系统，组件来自 report_style.py。

用法（CLI 与旧版完全兼容）：
    garmin_chart.py {sleep,body_battery,hrv,activities,dashboard} --days N --output path
"""

import sys
import argparse
import webbrowser
import tempfile
from pathlib import Path
from datetime import datetime

# Import auth and data helpers
sys.path.insert(0, str(Path(__file__).parent))
from garmin_auth import get_client
from garmin_data import fetch_sleep, fetch_hrv, fetch_body_battery, fetch_heart_rate, fetch_activities
from report_style import (C, esc, hms, ms, short_date, xlabels, svg_line_chart, svg_bar_chart,
                          sleep_bar, sleep_legend, stat, kv, note, card, grid, chart_cap,
                          hero, render_page)

# ================= 通用辅助 =================

RUN_TYPES = ('running', 'trail_running', 'treadmill_running', 'ultra_run', 'track_run')


def _score_color(score):
    """睡眠评分 -> 颜色"""
    if score is None:
        return C['gray']
    if score >= 80:
        return C['green']
    if score >= 60:
        return C['yellow']
    return C['red']


def _level_color(v):
    """身体电量水平 -> 颜色"""
    if v is None:
        return C['gray']
    if v >= 75:
        return C['green']
    if v >= 50:
        return C['yellow']
    if v >= 25:
        return C['orange']
    return C['red']


def _type_color(types, t):
    palette = [C['blue'], C['teal'], C['purple'], C['orange'], C['green'], C['red']]
    return palette[list(types).index(t) % len(palette)]


def _pace_str(avg_speed):
    """m/s -> 配速 min:s/km"""
    if not avg_speed:
        return '—'
    return ms(1000.0 / avg_speed) + '/km'


def _fmt_or_dash(v, fmt='%.0f'):
    return (fmt % v) if v is not None else '—'


# ================= 睡眠 =================

def build_sleep_sections(sleep_data):
    """睡眠分析章节。返回 [(标题, 说明, html), ...]"""
    days = [s for s in sleep_data if s.get('sleep_time_seconds')]
    if not days:
        return []
    dates = [s['date'] for s in days]
    hours = [s['sleep_time_seconds'] / 3600.0 for s in days]
    scores = [s.get('sleep_score') for s in days]
    sc = [x for x in scores if x is not None]
    avg_h = sum(hours) / len(hours)
    avg_sc = (sum(sc) / len(sc)) if sc else None
    best_i = max(range(len(days)), key=lambda i: scores[i] if scores[i] is not None else -1)
    worst_i = min(range(len(days)), key=lambda i: scores[i] if scores[i] is not None else 10**9)

    deep = sum(s.get('deep_sleep_seconds') or 0 for s in days)
    light = sum(s.get('light_sleep_seconds') or 0 for s in days)
    rem = sum(s.get('rem_sleep_seconds') or 0 for s in days)
    awake = sum(s.get('awake_seconds') or 0 for s in days)
    total_sec = sum(s['sleep_time_seconds'] for s in days) or 1

    secs = []
    # ---- 1 总览 ----
    desc = '近 %d 晚有效睡眠记录（%s – %s），数据来自佳明设备自动记录。' % (
        len(days), dates[0], dates[-1])
    stats = [
        stat('平均睡眠时长', '%.1f 小时' % avg_h, '有效记录 %d 晚' % len(days)),
        stat('平均睡眠评分', _fmt_or_dash(avg_sc), '满分 100'),
        stat('最佳之夜', _fmt_or_dash(scores[best_i]), '%s · 时长 %.1f 小时' % (dates[best_i], hours[best_i])),
        stat('最差之夜', _fmt_or_dash(scores[worst_i]), '%s · 时长 %.1f 小时' % (dates[worst_i], hours[worst_i])),
    ]
    good_nights = sum(1 for x in sc if x >= 80)
    bad_nights = sum(1 for x in sc if x < 60)
    if avg_sc is None:
        nt = note('设备未返回睡眠评分，以下仅基于时长与睡眠阶段结构分析。', 'warn')
    elif avg_sc >= 80:
        nt = note('<b>睡眠解读：</b>近 %d 晚平均睡眠 <b>%.1f 小时</b>、平均评分 <b>%.0f</b>，整体质量良好（评分 ≥80 的有 %d 晚）。深睡占比 %.0f%%、REM 占比 %.0f%%（参考：成人深睡约 13-23%%、REM 约 20-25%%）。' %
                  (len(days), avg_h, avg_sc, good_nights, deep / total_sec * 100, rem / total_sec * 100), 'good')
    elif avg_sc >= 60:
        nt = note('<b>睡眠解读：</b>近 %d 晚平均睡眠 <b>%.1f 小时</b>、平均评分 <b>%.0f</b>，质量尚可但有改进空间（≥80 分 %d 晚 / &lt;60 分 %d 晚）。深睡占比 %.0f%%、REM 占比 %.0f%%。可关注就寝规律性与睡前刺激（咖啡因、屏幕）。' %
                  (len(days), avg_h, avg_sc, good_nights, bad_nights, deep / total_sec * 100, rem / total_sec * 100))
    else:
        nt = note('<b>睡眠解读：</b>近 %d 晚平均睡眠 <b>%.1f 小时</b>、平均评分仅 <b>%.0f</b>，存在明显睡眠不足（&lt;60 分有 %d 晚）。深睡占比 %.0f%%、REM 占比 %.0f%%。建议优先保障 7 小时以上睡眠并固定起床时间；若持续偏低请关注压力与训练负荷。' %
                  (len(days), avg_h, avg_sc, bad_nights, deep / total_sec * 100, rem / total_sec * 100), 'warn')
    secs.append(('睡眠总览', desc, grid(stats) + nt))

    # ---- 2 每日趋势 ----
    n = len(days)
    label_every = max(1, (n + 6) // 7)
    show_vals = n <= 20
    dur_bars = [(short_date(dates[i]), hours[i],
                 '%s · 时长 %.1f 小时 · 评分 %s' % (dates[i], hours[i], _fmt_or_dash(scores[i])),
                 _score_color(scores[i])) for i in range(n)]
    sc_bars = [(short_date(dates[i]), scores[i],
                '%s · 评分 %s · 时长 %.1f 小时' % (dates[i], _fmt_or_dash(scores[i]), hours[i]),
                _score_color(scores[i])) for i in range(n) if scores[i] is not None]
    left = card(svg_bar_chart(dur_bars, y_fmt=lambda v: '%.1fh',
                              bar_label_fmt=(lambda v: '%.1f' % v) if show_vals else None,
                              label_every=label_every) +
               chart_cap('每日睡眠时长（小时）· 柱色按评分着色：绿 ≥80 · 黄 60-79 · 红 &lt;60 · 悬停查看详情'),
               '每日睡眠时长')
    right = ''
    if sc_bars:
        right = card(svg_bar_chart(sc_bars, y_fmt=lambda v: '%.0f',
                                   bar_label_fmt=(lambda v: '%.0f' % v) if show_vals else None,
                                   label_every=label_every) +
                     chart_cap('每日睡眠评分（0-100）· 参考：≥90 优秀 · 80-89 良好 · 60-79 一般 · &lt;60 较差'),
                     '每日睡眠评分')
    secs.append(('每日睡眠趋势', '时长与评分的逐日对比，用于发现规律性波动与异常之夜。',
                 grid([left, right], 2) if right else left))

    # ---- 3 睡眠结构 ----
    show_days = days[-30:]
    bars_html = [sleep_legend()]
    for s in show_days:
        bars_html.append(sleep_bar(s['date'], s.get('deep_sleep_seconds'), s.get('light_sleep_seconds'),
                                   s.get('rem_sleep_seconds'), s.get('awake_seconds'), s.get('sleep_score')))
    n_show = len(show_days)
    avg_note = '<div style="margin-top:12px">'
    avg_note += kv('平均深睡', '%s（%.0f%%）' % (hms(deep / len(days)), deep / total_sec * 100))
    avg_note += kv('平均浅睡', '%s（%.0f%%）' % (hms(light / len(days)), light / total_sec * 100))
    avg_note += kv('平均 REM', '%s（%.0f%%）' % (hms(rem / len(days)), rem / total_sec * 100))
    avg_note += kv('平均清醒', '%s（%.0f%%）' % (hms(awake / len(days)), awake / total_sec * 100))
    avg_note += '</div>'
    desc3 = '每晚安表示意图：深睡 / 浅睡 / REM / 清醒四阶段占比' + ('（最近 %d 晚）' % n_show if n_show < len(days) else '') + '。'
    secs.append(('睡眠结构', desc3, card(''.join(bars_html) + avg_note)))

    return secs


# ================= 身体电量 =================

def build_body_battery_sections(bb_data):
    """身体电析章节。"""
    days = [b for b in bb_data if b.get('highest') is not None]
    if not days:
        return []
    dates = [b['date'] for b in days]
    charged = [b.get('charged') or 0 for b in days]
    drained = [b.get('drained') or 0 for b in days]
    highest = [b['highest'] for b in days]
    lowest = [b.get('lowest') for b in days]
    avg_ch = sum(charged) / len(charged)
    avg_dr = sum(drained) / len(drained)
    avg_hi = sum(highest) / len(highest)
    lows = [x for x in lowest if x is not None]
    avg_lo = (sum(lows) / len(lows)) if lows else None
    high_days = sum(1 for x in highest if x >= 75)
    low_days = sum(1 for x in highest if x < 50)

    secs = []
    desc = '近 %d 天身体电量记录（%s – %s）。身体电量（0-100）是佳明基于 HRV、压力、睡眠与活动综合计算的恢复指标。' % (
        len(days), dates[0], dates[-1])
    stats = [
        stat('平均每日充电', '+%.0f' % avg_ch, '睡眠/休息期间的电量恢复'),
        stat('平均每日消耗', '-%.0f' % avg_dr, '活动与压力期间的电量消耗'),
        stat('平均峰值电量', '%.0f / 100' % avg_hi, '峰值 ≥75 的有 %d 天（%d%%）' % (high_days, high_days * 100 // len(days))),
        stat('平均最低电量', '%s / 100' % _fmt_or_dash(avg_lo), '峰值 &lt;50 的有 %d 天' % low_days),
    ]
    if avg_hi >= 75:
        nt = note('<b>电量解读：</b>平均峰值电量 <b>%.0f</b>，大部分时间处于"充分恢复"区间，身体可以承受较高强度训练。' % avg_hi, 'good')
    elif avg_hi >= 50:
        nt = note('<b>电量解读：</b>平均峰值电量 <b>%.0f</b>，恢复水平中等：可支持常规训练，高强度课后注意观察次日峰值是否回升。' % avg_hi)
    else:
        nt = note('<b>电量解读：</b>平均峰值电量仅 <b>%.0f</b>，恢复不足（0-49 = 疲劳区间）：建议以低强度活动为主，优先改善睡眠与恢复，持续偏低需警惕过度训练。' % avg_hi, 'warn')
    secs.append(('身体电量总览', desc, grid(stats) + nt))

    # 趋势折线
    n = len(days)
    xlab = xlabels(dates)
    hi_series = {'data': list(enumerate(highest)), 'color': C['orange'], 'width': '2.5', 'name': '每日峰值'}
    lo_series = {'data': [(i, v) for i, v in enumerate(lowest) if v is not None],
                 'color': C['blue'], 'width': '1.8', 'dash': True, 'name': '每日最低'}
    line = svg_line_chart([hi_series, lo_series], y_min=0, y_max=100,
                          x_labels=xlab, y_fmt=lambda v: '%.0f',
                          legend=[('峰值电量', C['orange']), ('最低电量', C['blue'])])
    secs.append(('每日电量趋势', '峰值反映当天恢复到的最高水平，最低值反映消耗后的谷底。',
                 card(line + chart_cap('峰值 ≥75（绿·充分恢复）· 50-74（黄·中等）· 25-49（橙·疲劳）· &lt;25（红·耗尽）'))))

    # 充电/消耗柱状
    label_every = max(1, (n + 6) // 7)
    show_vals = n <= 20
    ch_bars = [(short_date(dates[i]), charged[i], '%s 充电 +%d' % (dates[i], charged[i]), C['green'])
               for i in range(n)]
    hi_bars = [(short_date(dates[i]), highest[i], '%s 峰值 %d' % (dates[i], highest[i]), _level_color(highest[i]))
               for i in range(n)]
    left = card(svg_bar_chart(ch_bars, y_fmt=lambda v: '%.0f',
                              bar_label_fmt=(lambda v: '+%d' % round(v)) if show_vals else None,
                              label_every=label_every) +
                chart_cap('每日充电量（睡眠/休息恢复的点数）'), '每日充电量')
    right = card(svg_bar_chart(hi_bars, y_fmt=lambda v: '%.0f',
                               bar_label_fmt=(lambda v: '%.0f' % v) if show_vals else None,
                               label_every=label_every) +
                 chart_cap('每日峰值电量 · 按恢复水平着色'), '每日峰值电量')
    secs.append(('充电与消耗', '充电量反映恢复能力，峰值反映当天可用的最大能量储备。',
                 grid([left, right], 2)))

    return secs


# ================= HRV 与静息心率 =================

def build_hrv_sections(hrv_data, hr_data):
    """HRV 与静息心率章节。"""
    days = [h for h in hrv_data if h.get('last_night_avg') is not None]
    if not days:
        return []
    dates = [h['date'] for h in days]
    vals = [h['last_night_avg'] for h in days]
    n = len(days)
    avg = sum(vals) / n
    latest = vals[-1]
    highs = [h.get('last_night_5min_high') for h in days if h.get('last_night_5min_high') is not None]
    avg_high = (sum(highs) / len(highs)) if highs else None
    blows = [h.get('baseline_balanced_low') for h in days if h.get('baseline_balanced_low') is not None]
    bhighs = [h.get('baseline_balanced_high') for h in days if h.get('baseline_balanced_high') is not None]
    band = (sum(blows) / len(blows), sum(bhighs) / len(bhighs)) if blows and bhighs else None

    hr_map = {h['date']: h.get('resting_hr') for h in hr_data}
    rhr = [hr_map.get(d) for d in dates]
    rhr_vals = [x for x in rhr if x is not None]
    avg_rhr = (sum(rhr_vals) / len(rhr_vals)) if rhr_vals else None

    # 趋势：前半 vs 后半
    if n >= 4:
        half = n // 2
        first_avg = sum(vals[:half]) / half
        second_avg = sum(vals[half:]) / (n - half)
        trend_pct = (second_avg - first_avg) / first_avg * 100
        if trend_pct > 5:
            trend_txt = '呈<b>上升</b>趋势（前半段均值 %.0f → 后半段 %.0f，+%.0f%%），恢复能力在改善。' % (first_avg, second_avg, trend_pct)
            trend_kind = 'good'
        elif trend_pct < -5:
            trend_txt = '呈<b>下降</b>趋势（前半段均值 %.0f → 后半段 %.0f，%.0f%%），可能提示恢复不足、压力增加或训练负荷偏高。' % (first_avg, second_avg, trend_pct)
            trend_kind = 'warn'
        else:
            trend_txt = '整体<b>平稳</b>（前半段均值 %.0f → 后半段 %.0f，%+.0f%%），自主神经平衡稳定。' % (first_avg, second_avg, trend_pct)
            trend_kind = 'info'
    else:
        trend_txt = '记录天数较少，暂不足以判断趋势。'
        trend_kind = 'info'

    secs = []
    desc = '近 %d 天晨间 HRV 记录（%s – %s）。HRV（心率变异性，单位毫秒）反映自主神经系统的平衡与恢复能力，应关注长期趋势。' % (
        n, dates[0], dates[-1])
    stats = [
        stat('平均 HRV', '%.0f ms' % avg, '近 %d 天晨间均值' % n),
        stat('最新 HRV', '%.0f ms' % latest, '%s' % dates[-1]),
        stat('平均 5 分钟峰值', _fmt_or_dash(avg_high) + (' ms' if avg_high is not None else ''), '夜间最高 5 分钟均值'),
        stat('平均静息心率', _fmt_or_dash(avg_rhr) + (' bpm' if avg_rhr is not None else ''), '同一时期静息心率'),
    ]
    in_band = 0
    if band:
        in_band = sum(1 for v in vals if band[0] <= v <= band[1])
    band_txt = ('佳明基线平衡区间 <b>%.0f–%.0f ms</b>，处于区间内的有 %d/%d 天。' % (band[0], band[1], in_band, n)) if band else ''
    nt = note('<b>HRV 解读：</b>近 %d 天平均 <b>%.0f ms</b>，%s%s正常范围因人而异，单日波动意义有限，连续偏离基线才值得关注。' %
              (n, avg, trend_txt, band_txt + ' ' if band_txt else ''), trend_kind)
    secs.append(('HRV 总览', desc, grid(stats) + nt))

    # HRV 折线 + 基线带
    series = {'data': list(enumerate(vals)), 'color': C['teal'], 'width': '2.5', 'name': '晨间 HRV'}
    line = svg_line_chart([series], x_labels=xlabels(dates), y_fmt=lambda v: '%.0f',
                          band=band, band_color=C['blue'],
                          legend=[('晨间 HRV (ms)', C['teal'])] + ([('基线平衡区间', C['blue'])] if band else []))
    secs.append(('HRV 趋势', '蓝色区间为佳明基线平衡范围，落在区间内说明身体状态与近期基线一致。',
                 card(line + chart_cap('晨间 HRV（毫秒）· 悬停查看每日数值 · 连续高于基线 = 恢复良好，连续低于基线 = 需要恢复'))))

    # 静息心率柱状
    if rhr_vals:
        label_every = max(1, (n + 6) // 7)
        show_vals = n <= 20
        rhr_bars = [(short_date(dates[i]), rhr[i], '%s 静息心率 %s bpm' % (dates[i], _fmt_or_dash(rhr[i])),
                     C['red'] if rhr[i] is None or rhr[i] >= 60 else C['orange'])
                    for i in range(n) if rhr[i] is not None]
        bar = svg_bar_chart(rhr_bars, y_fmt=lambda v: '%.0f',
                            bar_label_fmt=(lambda v: '%.0f' % v) if show_vals else None,
                            label_every=label_every)
        rhr_min = min(rhr_vals)
        rhr_max = max(rhr_vals)
        kv_html = kv('静息心率范围', '%d – %d bpm' % (rhr_min, rhr_max))
        kv_html += kv('参考', '运动员 40-60 · 有锻炼习惯 60-70 · 普通成年人 70-80（次/分）')
        secs.append(('静息心率', '静息心率越低通常代表心血管功能越好；突然升高可能提示压力、生病或训练过度。',
                     card(bar + chart_cap('每日静息心率（bpm）· 悬停查看详情') + '<div style="margin-top:10px">%s</div>' % kv_html)))

    return secs


# ================= 活动 =================

def build_activities_sections(activities_data):
    """活动汇总章节。"""
    acts = sorted(activities_data, key=lambda a: a.get('date') or '')
    if not acts:
        return []
    total_count = len(acts)
    total_cal = sum(a.get('calories') or 0 for a in acts)
    total_dur_h = sum(a.get('duration_seconds') or 0 for a in acts) / 3600.0
    total_dist_km = sum((a.get('distance_meters') or 0) for a in acts) / 1000.0

    types = {}
    for a in acts:
        t = a.get('activity_type') or 'unknown'
        g = types.setdefault(t, {'count': 0, 'calories': 0, 'duration_h': 0.0, 'distance_km': 0.0})
        g['count'] += 1
        g['calories'] += a.get('calories') or 0
        g['duration_h'] += (a.get('duration_seconds') or 0) / 3600.0
        g['distance_km'] += (a.get('distance_meters') or 0) / 1000.0

    secs = []
    desc = '近 %d 次活动记录（%s – %s），数据来自 Garmin Connect。' % (
        total_count, acts[0].get('date', '—'), acts[-1].get('date', '—'))
    stats = [
        stat('活动总数', '%d 次' % total_count, '覆盖 %d 种运动类型' % len(types)),
        stat('总运动时长', '%.1f 小时' % total_dur_h, '平均每次 %.0f 分钟' % (total_dur_h / total_count * 60)),
        stat('总距离', '%.1f km' % total_dist_km, '含位移类活动'),
        stat('总卡路里', '%s kcal' % format(round(total_cal), ','), '活动期消耗'),
    ]
    biggest = max(acts, key=lambda a: a.get('calories') or 0)
    runs = [a for a in acts if (a.get('activity_type') or '') in RUN_TYPES and a.get('avg_speed')]
    run_txt = ''
    if runs:
        avg_pace = sum(1000.0 / a['avg_speed'] for a in runs) / len(runs)
        run_txt = ' 跑步类活动 %d 次，平均配速约 <b>%s/km</b>。' % (len(runs), ms(avg_pace))
    nt = note('<b>活动解读：</b>共 <b>%d</b> 次活动，累计 <b>%.1f 小时</b>、<b>%s kcal</b>。单次消耗最大：%s（%s kcal）。%s' %
              (total_count, total_dur_h, format(round(total_cal), ','), biggest.get('activity_name') or '未命名',
               format(round(biggest.get('calories') or 0), ','), run_txt))
    secs.append(('活动总览', desc, grid(stats) + nt))

    # 类型分布
    tnames = list(types.keys())
    def tname_cn(t):
        cn = {'running': '跑步', 'trail_running': '越野跑', 'treadmill_running': '跑步机跑',
              'cycling': '骑行', 'indoor_cycling': '室内骑行', 'swimming': '游泳',
              'strength_training': '力量训练', 'yoga': '瑜伽', 'walking': '步行',
              'hiking': '徒步', 'elliptical': '椭圆机', 'cardio_training': '有氧训练'}
        return cn.get(t, t)
    cnt_bars = [(tname_cn(t), types[t]['count'], '%s：%d 次' % (tname_cn(t), types[t]['count']),
                 _type_color(tnames, t)) for t in tnames]
    cal_bars = [(tname_cn(t), types[t]['calories'], '%s：%s kcal' % (tname_cn(t), format(round(types[t]['calories']), ',')),
                 _type_color(tnames, t)) for t in tnames if types[t]['calories'] > 0]
    left = card(svg_bar_chart(cnt_bars, y_fmt=lambda v: '%.0f', bar_label_fmt=lambda v: '%.0f' % v) +
                chart_cap('各类型活动次数'), '活动类型分布')
    right = ''
    if cal_bars:
        right = card(svg_bar_chart(cal_bars, y_fmt=lambda v: '%.0f', bar_label_fmt=lambda v: format(int(v), ',')) +
                     chart_cap('各类型卡路里消耗（kcal）'), '卡路里分布')
    secs.append(('类型分布', '按运动类型统计的次数与卡路里。',
                 grid([left, right], 2) if right else left))

    # 明细表
    rows = []
    for a in acts:
        t = a.get('activity_type') or 'unknown'
        rows.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            esc(a.get('date') or '—'),
            esc(a.get('activity_name') or '未命名'),
            esc(tname_cn(t)),
            hms(a.get('duration_seconds') or 0),
            ('%.2f km' % (a['distance_meters'] / 1000)) if a.get('distance_meters') else '—',
            _pace_str(a.get('avg_speed')) if t in RUN_TYPES else '—',
            _fmt_or_dash(a.get('calories')),
            _fmt_or_dash(a.get('avg_hr')),
            _fmt_or_dash(a.get('max_hr')),
            _fmt_or_dash(a.get('elevation_gain')),
        ))
    table = ('<div class="card tbl-wrap"><table><thead><tr>'
             '<th>日期</th><th>活动名称</th><th>类型</th><th>时长</th><th>距离</th>'
             '<th>配速</th><th>卡路里</th><th>均心率</th><th>最高心率</th><th>爬升 m</th>'
             '</tr></thead><tbody>%s</tbody></table></div>' % ''.join(rows))
    secs.append(('活动明细', '全部 %d 次活动的完整记录字段（表头吸顶，悬停高亮行）。' % total_count, table))

    return secs


# ================= 主流程 =================

def main():
    parser = argparse.ArgumentParser(description="Generate Garmin health charts")
    parser.add_argument("chart", choices=["sleep", "body_battery", "hrv", "activities", "dashboard"],
                        help="Type of chart to generate")
    parser.add_argument("--days", type=int, default=30, help="Number of days (default: 30)")
    parser.add_argument("--output", help="Output HTML file (default: opens in browser)")

    args = parser.parse_args()

    # Get authenticated client
    client = get_client()
    if not client:
        print("❌ Not authenticated. Run: python3 scripts/garmin_auth.py login", file=sys.stderr)
        sys.exit(1)

    print(f"📊 Fetching {args.days} days of data...", file=sys.stderr)

    sections = []
    range_str = ''
    sleep_list, bb_list, hrv_list, hr_list, act_list = [], [], [], [], []

    if args.chart in ["sleep", "dashboard"]:
        print("  - Sleep data", file=sys.stderr)
        result = fetch_sleep(client, args.days)
        sleep_list = result.get("sleep", [])
        range_str = '%s – %s' % (result.get('start', ''), result.get('end', ''))
        sections += build_sleep_sections(sleep_list)

    if args.chart in ["body_battery", "dashboard"]:
        print("  - Body Battery data", file=sys.stderr)
        result = fetch_body_battery(client, args.days)
        bb_list = result.get("body_battery", [])
        sections += build_body_battery_sections(bb_list)

    if args.chart in ["hrv", "dashboard"]:
        print("  - HRV & Heart Rate data", file=sys.stderr)
        result = fetch_hrv(client, args.days)
        hrv_list = result.get("hrv", [])
        hr_list = fetch_heart_rate(client, args.days).get("heart_rate", [])
        sections += build_hrv_sections(hrv_list, hr_list)

    if args.chart in ["activities", "dashboard"]:
        print("  - Activities data", file=sys.stderr)
        result = fetch_activities(client, args.days)
        act_list = result.get("activities", [])
        sections += build_activities_sections(act_list)

    # ---- 组装页面 ----
    period = '近 %d 天（%s）' % (args.days, range_str) if range_str else '近 %d 天' % args.days
    cn_names = {'sleep': '睡眠分析', 'body_battery': '身体电量分析',
                'hrv': '心率变异性分析', 'activities': '活动汇总', 'dashboard': '健康仪表盘'}
    page_title = '佳明%s报告' % cn_names[args.chart]
    badge = None

    if args.chart == 'sleep' and sleep_list:
        sc = [s['sleep_score'] for s in sleep_list if s.get('sleep_score') is not None]
        if sc:
            badge = '平均睡眠评分 %.0f / 100' % (sum(sc) / len(sc))
    elif args.chart == 'body_battery' and bb_list:
        hi = [b['highest'] for b in bb_list if b.get('highest') is not None]
        if hi:
            badge = '平均峰值电量 %.0f / 100' % (sum(hi) / len(hi))
    elif args.chart == 'hrv' and hrv_list:
        hv = [h['last_night_avg'] for h in hrv_list if h.get('last_night_avg') is not None]
        if hv:
            badge = '平均 HRV %.0f ms' % (sum(hv) / len(hv))
    elif args.chart == 'activities' and act_list:
        badge = '%d 次活动 · %s kcal' % (len(act_list), format(round(sum(a.get('calories') or 0 for a in act_list)), ','))
    elif args.chart == 'dashboard':
        badge = '近 %d 天健康数据全景' % args.days

    if not sections:
        sections = [('提示', '', note('未获取到所选类型的健康数据。可能是设备不支持该指标、未佩戴记录，或日期范围内无数据。', 'warn'))]

    hero_html = hero(cn_names[args.chart], '%s · 数据来自 Garmin Connect' % period, badge=badge)
    html = render_page(page_title, hero_html, sections,
                       footer_extra=' · 数据范围 %s' % period if range_str else '')

    # Save or open
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.write_text(html, encoding='utf-8')
        print(f"✅ Chart saved to {output_path}", file=sys.stderr)
    else:
        # Save to temp file and open
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            temp_path = f.name
        print(f"✅ Opening chart in browser...", file=sys.stderr)
        webbrowser.open(f"file://{temp_path}")


if __name__ == "__main__":
    main()
