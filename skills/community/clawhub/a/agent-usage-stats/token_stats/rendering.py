"""Terminal rendering for model and agent statistics."""

from __future__ import annotations

from .contexts import detect_context
from .formatting import (
    align_rows,
    display_width,
    fmt_cache_val,
    fmt_num,
    fmt_pct,
    pad_to,
    progress_bar,
    skip_model,
)


def fmt_today_lines(per_model: list, fmt_num_fn, helpers: dict) -> list:
    """Format per-model today data. Returns [first_line, ...] for printing."""
    if not per_model:
        return []
    filtered = [pm for pm in per_model if not skip_model(pm)]
    if not filtered:
        return []
    models = []
    ti = to = tc = tca = 0
    for pm in filtered:
        m = pm.get("model", "unknown")
        i = pm.get("input", 0) or 0
        o = pm.get("output", 0) or 0
        c = pm.get("cache", 0) or 0
        ca = pm.get("calls", 0) or 0
        models.append((m, i, o, c, ca))
        ti += i
        to += o
        tc += c
        tca += ca

    has_price = helpers["has_any_price"](filtered)

    lines = []
    if len(models) == 1:
        m, i, o, c, ca = models[0]
        t = i + o
        parts = [f"入 {fmt_num_fn(i)}",
                 f"出 {fmt_num_fn(o)}",
                 fmt_cache_val(c, i),
                 f"总计/+缓存 {fmt_num_fn(t)}/{fmt_num_fn(t + c)}",
                 f"调用 {ca} 次"]
        if has_price:
            price_cfg = helpers["get_model_price"](m)
            parts.append(helpers["fmt_cost"](i, o, c, price_cfg) if price_cfg else "-")
        lines.append(f"  📅 今日 | {' | '.join(parts)}")
    else:
        rows = []
        for m, i, o, c, ca in models:
            t = i + o
            cols = [
                f"入 {fmt_num_fn(i)}",
                f"出 {fmt_num_fn(o)}",
                fmt_cache_val(c, i),
                f"总计/+缓存 {fmt_num_fn(t)}/{fmt_num_fn(t + c)}",
                f"调用 {ca} 次",
            ]
            if has_price:
                price_cfg = helpers["get_model_price"](m)
                cols.append(helpers["fmt_cost"](i, o, c, price_cfg) if price_cfg else "-")
            rows.append((m, cols))
        cols_total = [
            f"入 {fmt_num_fn(ti)}",
            f"出 {fmt_num_fn(to)}",
            fmt_cache_val(tc, ti),
            f"总计/+缓存 {fmt_num_fn(ti + to)}/{fmt_num_fn(ti + to + tc)}",
            f"调用 {tca} 次",
        ]
        if has_price:
            total_cost_str = helpers["fmt_total_cost"](helpers["calc_total_cost"](filtered))
            if total_cost_str:
                cols_total.append(f"{total_cost_str} (仅供参考)")
        rows.append(("今日合计", cols_total))
        col_count = len(cols_total)
        col_widths = [0] * (col_count + 1)
        col_widths[0] = max(display_width(r[0]) for r in rows)
        for ci in range(col_count):
            col_widths[ci + 1] = max(display_width(r[1][ci]) for r in rows)
        lines.append("  📅 今日")
        for label, cols in rows:
            parts = [pad_to(label, col_widths[0])]
            for ci, col_text in enumerate(cols):
                parts.append(pad_to(col_text, col_widths[ci + 1], ">"))
            lines.append(f"    {' | '.join(parts)}")
    return lines


def format_model_line(model_name: str, inp: int, out: int, cache: int, calls: int,
                      helpers: dict, context_window: int = None, session_count: int = None,
                      extra: str = None) -> str:
    """单行模型输出格式。若全为 0 则返回空字符串。"""
    if inp == 0 and out == 0 and cache == 0 and calls == 0:
        return ""

    parts = []
    total = inp + out
    if context_window:
        pct = round(total / context_window * 100, 1) if context_window else 0
        parts.append(f"上下文 {fmt_num(total)}/{fmt_num(context_window)} ({fmt_pct(pct)})")
        parts.append(f"入 {fmt_num(inp)}")
        parts.append(f"出 {fmt_num(out)}")
        parts.append(fmt_cache_val(cache, inp))
        parts.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache)}")
    else:
        parts.append(f"入 {fmt_num(inp)}")
        parts.append(f"出 {fmt_num(out)}")
        parts.append(fmt_cache_val(cache, inp))
        parts.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache)}")
    if calls > 0 and session_count != calls:
        parts.append(f"调用 {calls} 次")
    if session_count:
        parts.append(f"{session_count} 轮会话")
    if extra:
        parts.append(extra)
    price_cfg = helpers["get_model_price"](model_name)
    if price_cfg:
        parts.append(helpers["fmt_cost"](inp, out, cache, price_cfg))
    if not parts:
        parts.append("无数据")
    return f"  {model_name} | {' | '.join(parts)}"


def build_aligned_raw(agent_display: str, per_model_list: list, helpers: dict,
                      has_context: bool = False, extra_footer: str = None,
                      token_mode: str = "split") -> str:
    """从 per_model 数据构建列对齐的原始输出（含 Agent 合计行）。"""
    per_model_list = [pm for pm in (per_model_list or []) if not skip_model(pm)]
    if not per_model_list:
        return f"📊 {agent_display}"

    rows = []
    ti = to = tc = tca = 0
    has_price = helpers["has_any_price"](per_model_list)
    for pm in per_model_list:
        mn = pm.get("model", "unknown")
        inp = pm.get("input", 0) or 0
        out = pm.get("output", 0) or 0
        cache = pm.get("cache", 0) or 0
        calls = pm.get("calls", 0) or 0
        row_mode = pm.get("token_mode") or token_mode
        total = inp + out
        ti += inp
        to += out
        tc += cache
        tca += calls

        cols = [mn]
        if has_context:
            cw = detect_context(mn)
            if cw:
                pct = round(total / cw * 100, 1) if cw else 0
                cols.append(progress_bar(pct))
                cols.append(f"{fmt_num(total)}/{fmt_num(cw)}")
            else:
                cols.append("")
                cols.append(f"{fmt_num(total)}/-")
        if row_mode == "total":
            cols.append(f"总计 {fmt_num(total)}")
        else:
            cols.append(f"入 {fmt_num(inp)}")
            cols.append(f"出 {fmt_num(out)}")
            cols.append(fmt_cache_val(cache, inp))
            cols.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache)}")
        if calls > 0:
            cols.append(f"调用 {calls} 次")
        if has_price:
            price_cfg = helpers["get_model_price"](mn)
            cols.append(helpers["fmt_cost"](inp, out, cache, price_cfg) if price_cfg and row_mode != "total" else "-")
        rows.append(cols)

    if len(per_model_list) > 1:
        total_all = ti + to
        subtotal_cols = ["合计"]
        if has_context:
            subtotal_cols.append("")
            subtotal_cols.append("")
        if token_mode == "total":
            subtotal_cols.append(f"总计 {fmt_num(total_all)}")
        else:
            subtotal_cols.append(f"入 {fmt_num(ti)}")
            subtotal_cols.append(f"出 {fmt_num(to)}")
            subtotal_cols.append(fmt_cache_val(tc, ti))
            subtotal_cols.append(f"总计/+缓存 {fmt_num(total_all)}/{fmt_num(total_all + tc)}")
        subtotal_cols.append(f"调用 {tca} 次")
        if has_price:
            total_cost_str = helpers["fmt_total_cost"](helpers["calc_total_cost"](per_model_list))
            if total_cost_str:
                subtotal_cols.append(f"{total_cost_str} (仅供参考)")
        rows.append(subtotal_cols)

    aligned = align_rows(rows)
    lines = [f"📊 {agent_display}"]
    for row in aligned:
        lines.append("  " + " | ".join(row))

    if extra_footer:
        lines.append("  " + "─" * 36)
        lines.append(extra_footer)
    return "\n".join(lines)
