"""Self-contained vector report for checkpoint activity comparisons."""

from html import escape
import json
import math

from compare_activity import clock, subtract, time_delta
from pace_chart import wrap_text


def numeric(value, digits=0, signed=False):
    if value is None:
        return "—"
    rounded = round(value, digits)
    if rounded == 0:
        rounded = 0.0
    return f"{rounded:+.{digits}f}" if signed and rounded else f"{rounded:.{digits}f}"


def time_status(delta: float, segment=False) -> tuple[str, str, str]:
    """Plan minus actual: positive means the recorded runner is ahead."""
    if abs(delta) < .5:
        return "持平 00:00:00", "#626D79", "#F0F2F5"
    if delta > 0:
        return ("本段快 " if segment else "实际领先 ") + clock(delta), "#087F5B", "#EAF6EF"
    return ("本段慢 " if segment else "实际落后 ") + clock(abs(delta)), "#C23B38", "#FCEEEE"


def split_at_zero(points: list[tuple[float, float]]) -> list:
    """Insert exact zero crossings before assigning a status to each line piece."""
    pieces = []
    for start, end in zip(points, points[1:]):
        if start[1] * end[1] < 0:
            crossing = (start[0] + (end[0] - start[0]) * start[1] / (start[1] - end[1]), 0)
            pieces.extend(((start, crossing), (crossing, end)))
        else:
            pieces.append((start, end))
    return pieces


def axis_limit(values: list[float]) -> float:
    half_minutes = max(1, max(abs(value) for value in values) / 120)
    magnitude = 10 ** math.floor(math.log10(half_minutes))
    step = next(factor * magnitude for factor in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10)
                if factor * magnitude >= half_minutes)
    return step * 120


def metric_limit(values: list[float | None]) -> float:
    maximum = max(1, max((abs(v) for v in values if v is not None), default=0))
    magnitude = 10 ** math.floor(math.log10(maximum))
    return next(factor * magnitude for factor in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10)
                if factor * magnitude >= maximum)


def metric_delta_label(delta: float | None) -> str:
    if delta is None:
        return "差值 —"
    rounded = math.floor(abs(delta) + .5)
    if rounded == 0:
        return "差值 0 m"
    return ("仓库多 " if delta > 0 else "仓库少 ") + f"{rounded} m"


def minute_delta_label(delta: float) -> str:
    if abs(delta) < .5:
        return "持平"
    if abs(delta) < 6:
        return ("快" if delta > 0 else "慢") + str(math.floor(abs(delta) + .5)) + "秒"
    return numeric(delta / 60, 1, signed=True)


def render_svg(comparison: dict) -> str:
    plan, activity = comparison["plan"], comparison["activity"]
    cps, schedules = comparison["checkpoints"], plan["schedules"]
    count, targets = len(cps) - 1, plan["targets_seconds"]
    width = max(2720, 560 + 500 * (len(targets) + 1))
    table_width = width - 128
    summary_columns = min(4, len(targets) + 1)
    summary_rows = math.ceil((len(targets) + 1) / summary_columns)
    overview_heading = 157 + summary_rows * 150 + 28
    panel_columns = min(3, len(targets))
    panel_rows = math.ceil(len(targets) / panel_columns)
    panel_height, panel_gap, panel_top = 790, 24, overview_heading + 75
    readout_heading = panel_top + panel_rows * (panel_height + panel_gap) + 36
    readout_column_width = (table_width - 600) / (len(targets) + 1)
    station_labels = [f'{cp["name"]} · {metrics["planned_distance_m"] / 1000:.1f} km'
                      for cp, metrics in zip(cps[1:], comparison["terrain"])]
    readout_row_height = max(72, 26 * max(len(wrap_text(name, 46)) for name in station_labels) + 20)
    readout_top = readout_heading + 70
    readout_height = 72 + count * readout_row_height
    terrain_heading = readout_top + readout_height + 48
    elevation_top = terrain_heading + 162
    footer_y = elevation_top + 620
    ink, muted = "#202A35", "#626D79"
    recorded_color, planned_color = "#475569", "#3274AC"
    parts = []

    def rect(x, y, w, h, fill, radius=0):
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"/>')

    def text(x, y, value, size=22, color=ink, weight=400, anchor="start"):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
                     f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')

    def label(x, y, value, units=36, size=23, anchor="start"):
        lines = wrap_text(value, units)
        for i, line in enumerate(lines):
            text(x, y + (i - (len(lines) - 1) / 2) * (size + 3), line, size, anchor=anchor)

    def path(points, color, line_width=3, dash=""):
        d = " ".join(f'{"M" if i == 0 else "L"}{x:.3f} {y:.3f}'
                     for i, (x, y) in enumerate(points))
        attrs = f' stroke-dasharray="{dash}"' if dash else ""
        parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{line_width}" '
                     f'stroke-linecap="round" stroke-linejoin="round"{attrs}/>')

    def focus_group(identifier, description, css_class="inspectable"):
        parts.append(f'<g id="{identifier}" class="{css_class}" tabindex="0" '
                     f'aria-label="{escape(description, quote=True)}">')
        parts.append(f"<title>{escape(description)}</title>")

    rect(0, 0, width, 10000, "#F7F8FA")
    rect(0, 0, width, 6, ink)
    text(64, 78, plan["name"], 45, weight=700)
    text(width - 64, 76, "佳明实际 × 仓库方案", 30, anchor="end")
    label(64, 125, f'{activity["start_time"][:10]} · {activity["activity_name"]}', units=140, size=24)
    card_width = (table_width - 24 * (summary_columns - 1)) / summary_columns
    for j, target in enumerate([None, *targets]):
        x = 64 + (j % summary_columns) * (card_width + 24)
        y = 157 + (j // summary_columns) * 150
        if target is None:
            rect(x, y, card_width, 126, "#ffffff", 13)
            text(x + 24, y + 34, "实际完赛时间", 21, muted)
            text(x + 24, y + 85, clock(activity["totals"]["elapsed_seconds"]), 40, ink, 700)
            text(x + 24, y + 112, "经过时间 · 包含停留", 18, muted)
        else:
            status, color, tint = time_status(target - activity["totals"]["elapsed_seconds"])
            rect(x, y, card_width, 126, tint, 13)
            text(x + 24, y + 34, "对照 " + clock(target).removesuffix(":00") + " 方案", 23, ink, 600)
            text(x + 24, y + 88, status, 31, color, 700)
            parts[-1] = parts[-1].replace("<text ", '<text class="finish-status" ')

    cumulative = [[predicted["arrival_seconds"] - actual["elapsed_seconds"]
                   for predicted, actual in zip(schedule["checkpoints"], cps)]
                  for schedule in schedules]
    segment_deltas = [[segment["plans"][j]["delta_seconds"] for segment in comparison["segments"]]
                      for j in range(len(targets))]
    cumulative_limit = axis_limit([value for values in cumulative for value in values])
    segment_limit = axis_limit([value for values in segment_deltas for value in values])
    panel_width = (table_width - panel_gap * (panel_columns - 1)) / panel_columns
    labels = ["起点"] + [cp["name"].split("-")[0].split("－")[0] for cp in cps[1:-1]] + ["终点"]
    parts.append('<g id="time-advantage">')
    text(64, overview_heading, "01  时间表现", 30, weight=700)
    text(64, overview_heading + 42, "累计差距：绿色领先、红色落后；零线 = 与计划一致", 22, muted)
    text(width - 64, overview_heading + 42, "上图看累计差距，下图看每段快慢 · 同类图共用刻度", 22, muted, anchor="end")

    def axes(left, right, top, height, limit, kind):
        zero, scale = top + height / 2, height / (2 * limit)
        parts.append(f'<g data-kind="{kind}" data-x-min="{left}" data-x-max="{right}" '
                     f'data-y-top="{top}" data-y-bottom="{top + height}" data-zero-y="{zero}" '
                     f'data-pixels-per-second="{scale}" data-limit-seconds="{limit}">')
        rect(left, top, right - left, height / 2, "#F3FAF6")
        rect(left, zero, right - left, height / 2, "#FEF5F5")
        for fraction in (1, .5, 0, -.5, -1):
            y = zero - fraction * height / 2
            path([(left, y), (right, y)], "#A1ABB5" if fraction == 0 else "#E0E6E9",
                 2 if fraction == 0 else 1, "" if fraction == 0 else "4 5")
            if fraction == 0:
                parts[-1] = parts[-1].replace("/>", ' data-role="zero-line"/>')
            text(left - 12, y + 6, "0" if fraction == 0 else numeric(fraction * limit / 60, signed=True),
                 18, muted, anchor="end")
        text(left, top - 14, "分钟", 17, muted)
        return zero, scale

    for j, target in enumerate(targets):
        column, row_index = j % panel_columns, j // panel_columns
        left = 64 + column * (panel_width + panel_gap)
        top = panel_top + row_index * (panel_height + panel_gap)
        parts.append(f'<g class="target-panel" data-target-seconds="{target}" '
                     f'data-column="{column}" data-row="{row_index}">')
        rect(left, top, panel_width, panel_height, "#FFFFFF", 12)
        text(left + 28, top + 43, clock(target).removesuffix(":00") + " 方案 · 累计差距", 26, weight=700)
        text(left + panel_width - 28, top + 43, "上方领先 · 下方落后", 19, muted, anchor="end")
        x0, x1 = left + 80, left + panel_width - 32
        plot_top, plot_height = top + 90, 260
        zero, scale = axes(x0, x1, plot_top, plot_height, cumulative_limit, "cumulative")
        positions = [x0 + cp["distance_m"] / plan["route"]["distance_m"] * (x1 - x0)
                     for cp in plan["checkpoints"]]
        raw_points = list(zip(positions, cumulative[j]))
        for start, end in split_at_zero(raw_points):
            color = time_status((start[1] + end[1]) / 2)[1]
            points = [(x, zero - value * scale) for x, value in (start, end)]
            area = " ".join(f'{"M" if i == 0 else "L"}{x:.3f} {y:.3f}'
                            for i, (x, y) in enumerate([(start[0], zero), *points, (end[0], zero)]))
            parts.append(f'<path d="{area} Z" fill="{color}" opacity=".12"/>')
            path(points, color, 4)
        previous_label = -math.inf
        for i, (x, delta) in enumerate(raw_points):
            status, color, _ = time_status(delta)
            tip = (f'{cps[i]["name"]}：{status}；实际 {clock(cps[i]["elapsed_seconds"])}；'
                   f'计划 {clock(schedules[j]["checkpoints"][i]["arrival_seconds"])}')
            parts.append(f'<circle class="delta-point" tabindex="0" cx="{x:.3f}" cy="{zero - delta * scale:.3f}" '
                         f'r="5" fill="{color}" stroke="#FFFFFF" stroke-width="2" data-delta-seconds="{delta}" '
                         f'aria-label="{escape(tip, quote=True)}"><title>{escape(tip)}</title></circle>')
            if i == count or x - previous_label > 46 and (i == 0 or x1 - x > 46):
                text(x, plot_top + plot_height + 28, labels[i][:10], 17, muted, anchor="middle")
                text(x, plot_top + plot_height + 49, f'{plan["checkpoints"][i]["distance_m"] / 1000:.1f}',
                     15, muted, anchor="middle")
                previous_label = x
        text(x1, plot_top + plot_height + 74, "赛道累计距离 / km →", 17, muted, anchor="end")
        parts.append("</g>")

        text(left + 28, top + 490, "每段快 / 慢了多少", 24, weight=650)
        text(left + panel_width - 28, top + 490, "上方快 · 下方慢", 19, muted, anchor="end")
        bar_top, bar_height = top + 530, 190
        zero, scale = axes(x0, x1, bar_top, bar_height, segment_limit, "segment")
        slot = (x1 - x0) / count
        bar_width = min(38, slot * .55)
        for i, delta in enumerate(segment_deltas[j], 1):
            x = x0 + (i - .5) * slot
            status, color, _ = time_status(delta, True)
            segment = comparison["segments"][i - 1]
            tip = (f'{segment["from_name"]} → {segment["to_name"]}：{status}；'
                   f'实际 {clock(segment["actual_seconds"])}；计划 {clock(segment["plans"][j]["seconds"])}')
            focus_group(f"segment-{j}-{i}", tip)
            parts.append(f'<rect x="{x - bar_width / 2:.3f}" y="{zero - max(0, delta) * scale:.3f}" '
                         f'width="{bar_width:.3f}" height="{abs(delta) * scale:.3f}" fill="{color}" '
                         f'data-delta-seconds="{delta}"><title>{escape(tip)}</title></rect>')
            text(x, zero - delta * scale + (-10 if delta >= 0 else 22), minute_delta_label(delta),
                 min(19, slot / 3), color, 600, "middle")
            text(x, bar_top + bar_height + 32, labels[i][:10], min(18, slot / 3), muted, anchor="middle")
            parts.append("</g>")
        parts.append("</g></g>")
    parts.append("</g>")

    parts.append('<g id="checkpoint-times">')
    text(64, readout_heading, "各站耗时", 28, weight=700)
    text(width - 64, readout_heading, "本段耗时（实际 − 预计）· HH:MM:SS · 含停留", 22, muted, anchor="end")
    text(64, readout_heading + 38, "红色 = 佳明实际更慢；绿色 = 更快或持平 · 差额 + 表示慢，− 表示快", 21, muted)
    rect(64, readout_top, table_width, readout_height, "#FFFFFF", 12)
    rect(64, readout_top, table_width, 72, "#EDF0F4", 8)
    text(88, readout_top + 45, "到达站点 · 累计里程", 24, muted, 600)
    for j in range(len(targets) + 1):
        center = 664 + (j + .5) * readout_column_width
        source_label = "佳明实际" if j == 0 else clock(targets[j - 1]).removesuffix(":00") + " 预计"
        text(center, readout_top + 45, source_label, 26, ink, 650 if j == 0 else 500, "middle")
    for i, (cp, metrics, segment) in enumerate(zip(cps[1:], comparison["terrain"], comparison["segments"]), 1):
        y = readout_top + 72 + (i - 1) * readout_row_height
        baseline = y + readout_row_height / 2 + 9
        cp_id = escape(cp["id"], quote=True)
        parts.append(f'<g class="time-row" data-cp-id="{cp_id}">')
        rect(64, y, table_width, readout_row_height, "#FFFFFF" if i % 2 else "#F2F4F7")
        path([(64, y + readout_row_height), (width - 64, y + readout_row_height)], "#E4E8ED", 1)
        tip = (f'{cp["name"]}：赛道累计 {numeric(metrics["planned_distance_m"] / 1000, 3)} km；'
               f'佳明累计 {numeric(None if metrics["actual_distance_m"] is None else metrics["actual_distance_m"] / 1000, 3)} km')
        focus_group(f"time-header-{i}", tip, "checkpoint-header inspectable")
        parts[-2] = parts[-2].replace(' tabindex=', f' data-cp-id="{cp_id}" '
                                     f'data-distance-m="{metrics["planned_distance_m"]}" tabindex=')
        label(88, baseline, station_labels[i - 1], units=46, size=23)
        parts.append("</g>")
        for j in range(len(targets) + 1):
            center = 664 + (j + .5) * readout_column_width
            source = "actual" if j == 0 else "planned"
            source_label = "佳明实际" if j == 0 else clock(targets[j - 1]).removesuffix(":00") + " 预计"
            target_attribute = "" if j == 0 else f' data-target-seconds="{targets[j - 1]}"'
            elapsed = cp["elapsed_seconds"] if j == 0 else schedules[j - 1]["checkpoints"][i]["arrival_seconds"]
            seconds = segment["actual_seconds"] if j == 0 else segment["plans"][j - 1]["seconds"]
            actual_minus_plan = segment["actual_seconds"] - seconds
            color = ink if j == 0 else time_status(-1 if actual_minus_plan > 0 else 1)[1]
            tip = (f'{source_label} · {cp["name"]}：累计 {clock(elapsed)}；'
                   f'{segment["from_name"]} → {segment["to_name"]} 本段 {clock(seconds)}，含停留')
            if j:
                tip += f"；实际 − 预计 {time_delta(actual_minus_plan)}；"
                tip += "佳明本段更慢" if actual_minus_plan > 0 else "佳明本段不慢于预计"
            focus_group(f"time-cell-{j}-{i}", tip, "time-cell inspectable")
            difference_attribute = "" if j == 0 else f' data-actual-minus-plan-seconds="{actual_minus_plan}"'
            parts[-2] = parts[-2].replace(' tabindex=', f' data-cp-id="{cp_id}" data-series="{source}"{target_attribute} '
                                         f'data-elapsed-seconds="{elapsed}" data-segment-seconds="{seconds}"{difference_attribute} tabindex=')
            difference = "" if j == 0 else (
                f'<tspan data-role="segment-difference" fill="{color}">（{time_delta(actual_minus_plan)}）</tspan>')
            parts.append(f'<text x="{center}" y="{baseline}" font-size="26" fill="{ink}" '
                         f'font-weight="700" text-anchor="middle" data-role="time-values">'
                         f'<tspan data-role="segment-time" fill="{color}">{clock(seconds)}</tspan>{difference}</text>')
            parts.append("</g>")
        parts.append("</g>")
    for x in (664 + j * readout_column_width for j in range(len(targets) + 1)):
        path([(x, readout_top), (x, readout_top + readout_height)], "#E4E8ED", 1)
    parts.append("</g>")

    parts.append('<g id="terrain">')
    text(64, terrain_heading, "02  赛道数据对比", 30, weight=700)
    text(width - 64, terrain_heading, "深灰 = 佳明 · 蓝色 = 仓库 · 爬升 / 下降按相邻 CP 区间比较", 22, muted, anchor="end")
    parts.append('<g id="terrain-summary">')
    summary_width = (table_width - 48) / 3
    for j, (title, key, divisor, unit, digits) in enumerate((
        ("全程距离", "distance_m", 1000, "km", 2),
        ("累计爬升", "ascent_m", 1, "m", 0),
        ("累计下降", "descent_m", 1, "m", 0),
    )):
        left = 64 + j * (summary_width + 24)
        a, p = activity["totals"][key], plan["route"][key]
        rect(left, terrain_heading + 24, summary_width, 110, "#ffffff", 10)
        text(left + 24, terrain_heading + 58, title + " · 佳明 / 仓库", 21, muted)
        value = numeric(None if a is None else a / divisor, digits)
        text(left + 24, terrain_heading + 105, f"{value} / {numeric(p / divisor, digits)} {unit}", 30, weight=650)
        text(left + summary_width - 24, terrain_heading + 105, metric_delta_label(subtract(p, a)),
             22, muted, anchor="end")
    parts.append("</g>")

    elevation_limit = metric_limit([m[source + key] for m in comparison["terrain"]
                                    for source in ("actual_", "planned_") for key in ("ascent_m", "descent_m")])
    chart_width = (table_width - 24) / 2
    for j, (key, heading) in enumerate((("ascent_m", "分段爬升"), ("descent_m", "分段下降"))):
        card_left = 64 + j * (chart_width + 24)
        left, right = card_left + 88, card_left + chart_width - 42
        plot_top, plot_height = elevation_top + 150, 330
        zero, scale = plot_top + plot_height, plot_height / elevation_limit
        parts.append(f'<g id="{key}-chart" data-kind="{key}" data-zero-y="{zero}" data-pixels-per-meter="{scale}">')
        rect(card_left, elevation_top, chart_width, 550, "#FFFFFF", 12)
        text(card_left + 28, elevation_top + 44, heading, 27, weight=700)
        text(card_left + 28, elevation_top + 82, "按相邻 CP 区间比较 · 两张图共用刻度", 20, muted)
        for index, (source, color) in enumerate((("佳明", recorded_color), ("仓库", planned_color))):
            legend_x = card_left + chart_width - 262 + index * 120
            rect(legend_x, elevation_top + 27, 22, 14, color, 2)
            text(legend_x + 32, elevation_top + 41, source, 21, muted)
        text(left - 18, plot_top - 22, "米", 18, muted, anchor="end")
        for tick in range(4):
            value = elevation_limit * tick / 3
            y = zero - value * scale
            path([(left, y), (right, y)], "#A1ABB5" if tick == 0 else "#E2E7ED", 2 if tick == 0 else 1,
                 "" if tick == 0 else "4 5")
            text(left - 16, y + 6, numeric(value), 18, muted, anchor="end")
        slot = (right - left) / count
        bar_width = min(23, slot * .20)
        offset = bar_width * .7
        for i, metrics in enumerate(comparison["terrain"], 1):
            center = left + (i - .5) * slot
            a, p = metrics["actual_" + key], metrics["planned_" + key]
            delta = subtract(p, a)
            tip = (f'{cps[i - 1]["name"]} → {cps[i]["name"]}：{heading}；'
                   f'佳明 {numeric(a)} m；仓库 {numeric(p)} m；{metric_delta_label(delta)}')
            focus_group(f"{key}-cp-{i}", tip)
            parts[-2] = parts[-2].replace(' tabindex=', f' data-actual-available="{str(a is not None).lower()}" tabindex=')
            label_y = [zero - (value or 0) * scale - 12 for value in (a, p)]
            if abs(label_y[0] - label_y[1]) < 28:
                label_y[1] = min(label_y) - 28
            for index, (source, value, color) in enumerate((("actual", a, recorded_color), ("planned", p, planned_color))):
                x = center + (-offset if index == 0 else offset)
                if value is not None:
                    y = zero - value * scale
                    parts.append(f'<rect x="{x - bar_width / 2:.3f}" y="{y:.3f}" width="{bar_width:.3f}" '
                                 f'height="{value * scale:.3f}" rx="2" fill="{color}" data-series="{source}" '
                                 f'data-value-m="{value}"><title>{escape(tip)}</title></rect>')
                text(x, label_y[index], numeric(value), min(21, slot * .21), color, 600, "middle")
            text(center, zero + 36, labels[i][:10], min(21, slot * .25), muted, anchor="middle")
            parts.append("</g>")
        parts.append("</g>")
    parts.append("</g>")

    lap_totals = activity.get("lap_totals") or {}
    notes = [
        f'来源：路线与现有配速模型；实际活动 {activity["start_time"][:10]}「{activity["activity_name"]}」。汇总来源：{activity["totals_source"]}。',
        "CP 经过时间由原始 FIT 轨迹投影或明确指定的实际耗时得到，包含停留，非官方打卡；无法可靠拆分站内停留。",
        "佳明分站累计爬升、下降按 FIT 逐圈距离插值；本段值为相邻站累计值之差。终点使用活动汇总，未按比例调整。",
        f'FIT 逐圈爬升 / 下降：{numeric(lap_totals.get("ascent_m"))} / {numeric(lap_totals.get("descent_m"))} m；'
        f'汇总：{numeric(activity["totals"]["ascent_m"])} / {numeric(activity["totals"]["descent_m"])} m。'
        "差值使用未取整原值；分段显示值之和可能有取整误差；缺失值为 —。",
    ]
    route_diagnostics = plan["route"].get("diagnostics") or {}
    if route_diagnostics.get("distance_source") == "fit_recorded":
        notes.append("方案路线使用 FIT 记录距离与海拔，爬升 / 下降由现有路线算法重算；"
                     "佳明实际侧保留逐圈估算及活动汇总，两侧不强行缩放一致。")
        notes += ["路线提示：" + warning for warning in plan["warnings"]]
    if comparison["warnings"]:
        notes += ["数据提示：" + warning for warning in comparison["warnings"]]
    focus_group("data-notes", "\n".join(notes))
    text(64, footer_y, "口径：时间包含停留，CP 非官方打卡；佳明本段爬升 / 下降由 FIT 逐圈累计估算值相减，未知为 —。", 20, muted)
    text(64, footer_y + 32, "差值先计算再取整；方案停留计入下一段。数据来源与匹配详情可悬停此处查看，也保存在 SVG 元数据中。", 20, muted)
    parts.append("</g>")
    height = footer_y + 70
    metadata = {
        "route_sha256": plan["source"]["sha256"], "config_sha256": comparison.get("config_sha256"),
        "activity_id": activity["activity_id"], "activity_date": activity["start_time"],
        "targets_seconds": targets, **activity.get("source", {}), **comparison["semantics"],
        "warnings": comparison["warnings"], "passage_overrides": comparison["passage_overrides"],
        "route_diagnostics": route_diagnostics,
        "data_notes": notes,
        "time_display": "actual ahead/faster when plan minus actual is positive; behind/slower when negative",
        "checkpoint_matches": [
            {"id": cp["id"], "offset_m": cp["offset_m"], "method": cp["match_method"]}
            for cp in cps
        ],
    }
    heading = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">\n'
        f'<title id="title">{escape(plan["name"])}：佳明实际与仓库方案对比</title>\n'
        '<desc id="description">每个目标上方为累计领先或落后曲线，下方为各区间快慢正负柱图；耗时表以 CP 为行，站名与累计里程合并为首列。'
        '实际列展示本段耗时，各预计列展示本段耗时和实际减预计的差额，均加粗并保留到秒；累计经过时间保留在提示中。'
        '预计本段耗时及差额红色表示佳明实际更慢，绿色表示实际更快或持平。'
        '赛道数据包括全程汇总及分段爬升、下降分组柱图。'
        '绿色表示实际领先或本段更快，红色表示实际落后或本段更慢；累计曲线零线上方领先、下方落后。'
        '分段柱图零线上方快、下方慢；赛道图用深灰表示佳明、蓝色表示仓库。时间含停留，差值先计算再取整。</desc>\n'
        '<metadata>' + escape(json.dumps(metadata, ensure_ascii=False)) + '</metadata>\n'
        '<style>text{font-family:"PingFang SC","Noto Sans CJK SC","Microsoft YaHei",sans-serif;'
        'font-variant-numeric:tabular-nums}'
        '.inspectable,.delta-point{outline:none}'
        '.delta-point:hover,.delta-point:focus{r:8;stroke:#202A35}'
        '.inspectable:hover rect[data-delta-seconds],.inspectable:focus rect[data-delta-seconds]'
        '{stroke:#202A35;stroke-width:2}'
        '.inspectable:hover > rect[data-series],.inspectable:focus > rect[data-series]'
        '{stroke:#202A35;stroke-width:2}'
        '.inspectable:focus > text{text-decoration:underline}'
        '#data-notes:focus text{text-decoration:underline}'
        '</style>\n'
    )
    parts[0] = parts[0].replace('height="10000"', f'height="{height}"')
    return heading + "\n".join(parts) + "\n</svg>\n"
