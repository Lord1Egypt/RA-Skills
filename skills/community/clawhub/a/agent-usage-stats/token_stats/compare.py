"""Time-range comparison output."""

from __future__ import annotations

from .formatting import is_total_mode


def run_compare(agent, a_label: str, b_label: str, helpers: dict):
    """Compare two time ranges by model and metric."""
    parse_time_label = helpers["parse_time_label"]
    label_to_display = helpers["label_to_display"]
    skip_model = helpers["skip_model"]
    fmt_num = helpers["fmt_num"]
    calc_cache_rate = helpers["calc_cache_rate"]
    get_model_price = helpers["get_model_price"]
    calc_cost = helpers["calc_cost"]
    to_cny = helpers["to_cny"]
    align_rows = helpers["align_rows"]
    display_width = helpers["display_width"]
    strip_ansi = helpers["strip_ansi"]

    a_start, a_end = parse_time_label(a_label)
    b_start, b_end = parse_time_label(b_label)

    print("  ⏳ 正在收集对比数据...", end="\r", flush=True)
    data_a = agent.collect(from_ts=a_start, to_ts=a_end)
    data_b = agent.collect(from_ts=b_start, to_ts=b_end)
    print(" " * 30, end="\r")

    models_a = {pm["model"]: pm for pm in (data_a.per_model or []) if not skip_model(pm)}
    models_b = {pm["model"]: pm for pm in (data_b.per_model or []) if not skip_model(pm)}
    all_models = sorted(set(list(models_a.keys()) + list(models_b.keys())))

    if not all_models:
        print("两个时间段均无数据")
        return

    a_disp = label_to_display(a_label)
    b_disp = label_to_display(b_label)
    print(f"\n📊 对比: {a_disp} vs {b_disp}  [{agent.display_name()}]")

    rows = []

    def _delta(va, vb):
        d = vb - va
        return f"+{fmt_num(d)}" if d > 0 else fmt_num(d) if d < 0 else "0"

    grand_ai = grand_ao = grand_ac = grand_acall = grand_bi = grand_bo = grand_bc = grand_bcall = 0
    for mn in all_models:
        ma = models_a.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
        mb = models_b.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
        ai = ma.get("input", 0) or 0
        ao = ma.get("output", 0) or 0
        ac = ma.get("cache", 0) or 0
        a_calls = ma.get("calls", 0) or 0
        a_total = ai + ao
        a_total_cache = a_total + ac
        bi = mb.get("input", 0) or 0
        bo = mb.get("output", 0) or 0
        bc = mb.get("cache", 0) or 0
        b_calls = mb.get("calls", 0) or 0
        b_total = bi + bo
        b_total_cache = b_total + bc
        if a_total == 0 and b_total == 0 and ac == 0 and bc == 0 and a_calls == 0 and b_calls == 0:
            continue
        grand_ai += ai
        grand_ao += ao
        grand_ac += ac
        grand_acall += a_calls
        grand_bi += bi
        grand_bo += bo
        grand_bc += bc
        grand_bcall += b_calls

        pc = None if is_total_mode(ma) or is_total_mode(mb) else get_model_price(mn)
        a_cost_str = f"≈¥{to_cny(calc_cost(ai, ao, ac, pc), pc.get('currency','CNY')):.2f}" if pc and (ai or ao or ac) else "-"
        b_cost_str = f"≈¥{to_cny(calc_cost(bi, bo, bc, pc), pc.get('currency','CNY')):.2f}" if pc and (bi or bo or bc) else "-"
        metrics = [
            ("入", ai, bi),
            ("出", ao, bo),
            ("缓", ac, bc),
            ("缓存率", f"{calc_cache_rate(ai, ac):.1f}%" if calc_cache_rate(ai, ac) is not None else "-",
                      f"{calc_cache_rate(bi, bc):.1f}%" if calc_cache_rate(bi, bc) is not None else "-"),
            ("总计", a_total, b_total),
            ("总计(含缓存)", a_total_cache, b_total_cache),
            ("调用", a_calls, b_calls),
            ("费用", a_cost_str, b_cost_str),
        ]
        for i, (metric_name, va, vb) in enumerate(metrics):
            d_val = _metric_delta(metric_name, va, vb, _delta)
            rows.append(["" if i != 0 else mn, metric_name, str(va), str(vb), d_val])

    metrics_per_model = 8
    model_count = len(rows) // metrics_per_model if rows else 0
    if model_count > 1:
        _append_grand_total_rows(
            rows,
            all_models,
            models_a,
            models_b,
            grand_ai,
            grand_ao,
            grand_ac,
            grand_acall,
            grand_bi,
            grand_bo,
            grand_bc,
            grand_bcall,
            helpers,
            _delta,
        )

    if not rows:
        print("  (两侧均无有效数据)")
        print()
        return

    headers = ["模型", "指标", f"{a_disp}", f"{b_disp}", "变化"]
    aligned = align_rows([headers] + rows)
    header_row = aligned[0]
    data_rows = aligned[1:]
    sep_w = sum(display_width(strip_ansi(c)) for c in header_row) + 3 * (len(header_row) - 1) + 4
    model_boundaries = set()
    cur_model = None
    for i, row in enumerate(rows):
        mn = row[0]
        if mn and mn != cur_model:
            if cur_model is not None:
                model_boundaries.add(i)
            cur_model = mn
    print("=" * sep_w)
    print(f"  {' | '.join(header_row)}")
    print("─" * sep_w)
    for i, row in enumerate(data_rows):
        if i in model_boundaries:
            print("  " + "·" * (sep_w - 2))
        print(f"  {' | '.join(row)}")
    print("─" * sep_w)
    print()


def _append_grand_total_rows(
    rows,
    all_models,
    models_a,
    models_b,
    grand_ai,
    grand_ao,
    grand_ac,
    grand_acall,
    grand_bi,
    grand_bo,
    grand_bc,
    grand_bcall,
    helpers,
    delta_fn,
):
    calc_cache_rate = helpers["calc_cache_rate"]
    get_model_price = helpers["get_model_price"]
    calc_cost = helpers["calc_cost"]
    to_cny = helpers["to_cny"]

    grand_a_total = grand_ai + grand_ao
    grand_b_total = grand_bi + grand_bo
    grand_a_total_cache = grand_a_total + grand_ac
    grand_b_total_cache = grand_b_total + grand_bc
    gt_a_cost = sum(
        to_cny(calc_cost(
            models_a.get(mn, {}).get("input", 0) or 0,
            models_a.get(mn, {}).get("output", 0) or 0,
            models_a.get(mn, {}).get("cache", 0) or 0,
            pc,
        ), pc.get("currency", "CNY"))
        for mn in all_models
        if not is_total_mode(models_a.get(mn, {})) and (pc := get_model_price(mn))
    )
    gt_b_cost = sum(
        to_cny(calc_cost(
            models_b.get(mn, {}).get("input", 0) or 0,
            models_b.get(mn, {}).get("output", 0) or 0,
            models_b.get(mn, {}).get("cache", 0) or 0,
            pc,
        ), pc.get("currency", "CNY"))
        for mn in all_models
        if not is_total_mode(models_b.get(mn, {})) and (pc := get_model_price(mn))
    )
    gt_a_cost_str = f"≈¥{gt_a_cost:.2f}" if gt_a_cost > 0 else "-"
    gt_b_cost_str = f"≈¥{gt_b_cost:.2f}" if gt_b_cost > 0 else "-"
    metrics = [
        ("入", grand_ai, grand_bi),
        ("出", grand_ao, grand_bo),
        ("缓", grand_ac, grand_bc),
        ("缓存率", f"{calc_cache_rate(grand_ai, grand_ac):.1f}%" if calc_cache_rate(grand_ai, grand_ac) is not None else "-",
                  f"{calc_cache_rate(grand_bi, grand_bc):.1f}%" if calc_cache_rate(grand_bi, grand_bc) is not None else "-"),
        ("总计", grand_a_total, grand_b_total),
        ("总计(含缓存)", grand_a_total_cache, grand_b_total_cache),
        ("调用", grand_acall, grand_bcall),
        ("费用", gt_a_cost_str, gt_b_cost_str),
    ]
    for i, (metric_name, va, vb) in enumerate(metrics):
        d_val = _metric_delta(metric_name, va, vb, delta_fn)
        rows.append(["" if i != 0 else "合计", metric_name, str(va), str(vb), d_val])


def _metric_delta(metric_name, va, vb, delta_fn):
    if metric_name == "缓存率":
        return ""
    if metric_name == "费用":
        if isinstance(va, str) and va.startswith("≈¥") and isinstance(vb, str) and vb.startswith("≈¥"):
            try:
                fa = float(va[2:])
                fb = float(vb[2:])
                d = fb - fa
                return f"+¥{d:.2f}" if d > 0 else f"-¥{abs(d):.2f}" if d < 0 else "0"
            except ValueError:
                return ""
        return ""
    return delta_fn(va, vb)
