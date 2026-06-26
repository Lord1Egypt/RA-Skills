"""Realtime monitoring mode."""

from __future__ import annotations

from datetime import datetime
import signal
import threading
import time

from .contexts import detect_context
from .formatting import display_width, strip_ansi


def _visible_width(text: str) -> int:
    return display_width(strip_ansi(text))


def _render_aligned_monitor_block(rows: list[list[str]], align_rows_fn, *, min_width: int = 60) -> list[str]:
    """Render monitor rows as one aligned block with full-width separators."""
    if not rows:
        return []
    aligned = align_rows_fn(rows)
    content = [f"  {' | '.join(row)}" for row in aligned]
    width = max(min_width, *(_visible_width(line.strip()) for line in content))
    rule = "  " + "╌" * width
    return [rule, *content, rule]


def _render_monitor_section_title(title: str, *, width: int = 60) -> str:
    label = f" {title} "
    side = max(2, (width - _visible_width(label)) // 2)
    return "  " + ("╌" * side) + label + ("╌" * side)


def _print_aligned_monitor_block(rows: list[list[str]], align_rows_fn, *, min_width: int = 60) -> None:
    for line in _render_aligned_monitor_block(rows, align_rows_fn, min_width=min_width):
        print(line)


def watch_agent(agent, interval: int = 5, helpers: dict = None) -> None:
    helpers = helpers or {}
    fmt_num = helpers["fmt_num"]
    calc_cache_rate = helpers["calc_cache_rate"]
    fmt_cache_val = helpers["fmt_cache_val"]
    get_model_price = helpers["get_model_price"]
    calc_cost = helpers["calc_cost"]
    calc_total_cost = helpers["calc_total_cost"]
    fmt_cost = helpers["fmt_cost"]
    fmt_total_cost = helpers["fmt_total_cost"]
    to_cny = helpers["to_cny"]
    has_any_price = helpers["has_any_price"]
    align_rows = helpers["align_rows"]
    progress_bar = helpers["progress_bar"]

    """实时监控模式"""
    # 保护：interval 至少 1 秒，防止负数或零导致疯转
    if interval < 1:
        interval = 5
    stop_event = threading.Event()

    def _on_signal(sig, frame):
        stop_event.set()

    old_sigint = signal.signal(signal.SIGINT, _on_signal)
    old_sigterm = None
    try:
        old_sigterm = signal.signal(signal.SIGTERM, _on_signal)
    except (ValueError, AttributeError):
        pass  # Windows 上 SIGTERM 不可用

    def _interruptible_sleep(seconds: float) -> bool:
        """中断式睡眠，返回 False 表示被中断"""
        return not stop_event.wait(timeout=seconds)

    watch_start = time.time()
    # 今日起始时间戳，用于 📅 今日合计查询
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    yesterday_start = None  # 跨天时记录上一个 today_start，用于汇总拆分
    print(f"\n📡 实时监控 [{agent.display_name()}] — 每 {interval} 秒刷新 (Ctrl+C 停止)\n")

    # ── 首次基线 ──
    try:
        data_first = agent.collect()
    except Exception as e:
        print(f"  ⚠️ 无法读取数据: {e}")
        print("👋 监控已停止")
        return
    bl_models = {}
    data_first_mode = getattr(data_first, 'token_mode', 'split')
    if data_first.per_model:
        for pm in data_first.per_model:
            bl_models[pm["model"]] = {
                "input": pm.get("input", 0),
                "output": pm.get("output", 0),
                "calls": pm.get("calls", 0),
                "cache": pm.get("cache", 0),
                "token_mode": pm.get("token_mode") or data_first_mode,
            }
    else:
        m = data_first.stats.get("model", "")
        if m and m != "?" and data_first.stats.get("input_tokens", 0) > 0:
            bl_models[m] = {
                "input": data_first.stats.get("input_tokens", 0),
                "output": data_first.stats.get("output_tokens", 0),
                "calls": data_first.stats.get("api_calls", 0),
                "cache": data_first.stats.get("cache_read", 0),
                "token_mode": data_first_mode,
            }

    def _row_mode(mv: dict) -> str:
        return mv.get("token_mode") or data_first_mode

    def _is_total_row(mv: dict) -> bool:
        return _row_mode(mv) == "total"

    def _all_rows_total(models: dict) -> bool:
        return bool(models) and all(_is_total_row(mv) for mv in models.values())

    # 纯累计型 agent（仅存 tokens_used）用基线差分计算"今日"。
    # CodeX 可能混合 split JSONL 与 total fallback，混合时仍应使用日期精筛。
    today_start_baseline = {k: dict(v) for k, v in bl_models.items()} if _all_rows_total(bl_models) else None

    # ── 初始状态 ──
    bl_initial = {k: dict(v) for k, v in bl_models.items()}
    print("初始状态:")
    has_data = False
    has_cache = any(mv.get("cache", 0) for mv in bl_models.values())
    # 检查是否有配置了价格的模型
    bl_has_price = any(get_model_price(mn) for mn in bl_models)
    if bl_models:
        init_rows = []
        for mn, mv in bl_models.items():
            total = mv["input"] + mv["output"]
            cols = [mn]
            cache_val = mv.get('cache', 0)
            if agent._has_live_context:
                cw = detect_context(mn)
                pct = round(total / cw * 100, 1) if cw else 0
                cols.append(progress_bar(pct))
                cols.append(f"{fmt_num(total)}/{fmt_num(cw)}")
            if _is_total_row(mv):
                cols.append(f"总计 {fmt_num(total)}")
            else:
                cols.append(f"入 {fmt_num(mv['input'])}")
                cols.append(f"出 {fmt_num(mv['output'])}")
                cols.append(fmt_cache_val(cache_val, mv['input']))
                cols.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache_val)}")
            cols.append(f"调用 {mv['calls']}")
            if bl_has_price:
                pc = get_model_price(mn)
                cols.append(fmt_cost(mv['input'], mv['output'], cache_val, pc) if pc and not _is_total_row(mv) else "-")
            init_rows.append(cols)
            has_data = True
        _print_aligned_monitor_block(init_rows, align_rows)
    if not has_data:
        print("  (暂无数据，等待会话开始...)")
    print()

    # ── 监控循环（先采集再 sleep，保证间隔准确）──
    tick_count = 0
    while not stop_event.is_set():
        tick_start = time.monotonic()
        tick_count += 1
        try:
            data = agent.collect()
        except Exception as e:
            print(f"  ⚠️ {e}")
            if not _interruptible_sleep(interval):
                break
            continue

        now_models = {}
        data_mode = getattr(data, 'token_mode', data_first_mode)
        if data.per_model:
            for pm in data.per_model:
                now_models[pm["model"]] = {
                    "input": pm.get("input", 0),
                    "output": pm.get("output", 0),
                    "calls": pm.get("calls", 0),
                    "cache": pm.get("cache", 0),
                    "token_mode": pm.get("token_mode") or data_mode,
                }
        else:
            m = data.stats.get("model", "?")
            now_models[m] = {
                "input": data.stats.get("input_tokens", 0),
                "output": data.stats.get("output_tokens", 0),
                "calls": data.stats.get("api_calls", 0),
                "cache": data.stats.get("cache_read", 0),
                "token_mode": data_mode,
            }

        # 对比上一次状态，列出增量
        changed_models = []
        total_delta_tok = 0
        total_delta_calls = 0
        for mn, mv in now_models.items():
            bl = bl_models.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
            d_in = mv["input"] - bl["input"]
            d_out = mv["output"] - bl["output"]
            d_calls = mv["calls"] - bl["calls"]
            d_cache = mv["cache"] - bl["cache"]
            d_tok = d_in + d_out
            if d_tok > 0 or d_calls > 0 or d_cache > 0:
                changed_models.append((mn, d_in, d_out, d_tok, d_calls, d_cache))
                total_delta_tok += d_tok
                total_delta_calls += d_calls
            elif d_tok < 0 or d_calls < 0:
                bl_models[mn] = mv

        ts = datetime.now().strftime("%H:%M:%S")

        # 跨天检测：午夜过后自动切换"今日"基准
        new_today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        if new_today_start > today_start:
            yesterday_start = today_start
            today_start = new_today_start
            # 累计型 agent 重置"今日"基线
            if _all_rows_total(now_models) and today_start_baseline is not None:
                today_start_baseline = {k: dict(v) for k, v in now_models.items()}
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print()
            print("  " + "═" * 58)
            print(f"  跨天切换 — 当前时间 {now_str}")
            print("  新的一天开始，\"今日\"数据已重置")
            print("  " + "═" * 58)
            print()

        any_delta = bool(changed_models)
        if any_delta:
            summary_parts = []
            if total_delta_tok > 0:
                summary_parts.append(f"+{fmt_num(total_delta_tok)} tokens")
            elif total_delta_tok < 0:
                summary_parts.append(f"{fmt_num(total_delta_tok)} tokens")
            if total_delta_calls > 0:
                summary_parts.append(f"+{total_delta_calls} 调用")
            elif total_delta_calls < 0:
                summary_parts.append(f"{total_delta_calls} 调用")
            # 增量费用
            delta_cost = 0.0
            delta_currency = "CNY"
            for mn, mv in now_models.items():
                bl = bl_models.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
                d_in = mv["input"] - bl["input"]
                d_out = mv["output"] - bl["output"]
                d_cache = mv.get("cache", 0) - bl.get("cache", 0)
                pc = get_model_price(mn)
                if pc and not _is_total_row(mv) and (d_in or d_out or d_cache):
                    delta_cost += to_cny(calc_cost(d_in, d_out, d_cache, pc), pc.get('currency', 'CNY'))
            if delta_cost > 0:
                summary_parts.append(f"≈¥{delta_cost:.4f}")
            print(f"── [{ts}] {' '.join(summary_parts)} ──")

            # 增量行（仅展示本轮有变化的模型）
            any_cache_now = any(
                mv.get("cache", 0) or (mv.get("cache", 0) - bl_models.get(mn, {}).get("cache", 0))
                for mn, mv in now_models.items()
            )
            delta_has_price = any(get_model_price(mn) for mn in now_models)
            delta_rows = []
            idle_models = []
            for mn, mv in now_models.items():
                bl = bl_models.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
                d_in = mv["input"] - bl["input"]
                d_out = mv["output"] - bl["output"]
                d_tok = d_in + d_out
                d_cache = mv.get("cache", 0) - bl.get("cache", 0)
                d_calls = mv["calls"] - bl["calls"]
                has_delta = d_tok > 0 or d_cache > 0 or d_calls > 0
                total = mv["input"] + mv["output"]

                if total == 0 and mv["calls"] == 0:
                    idle_models.append(mn)
                    bl_models[mn] = mv
                    continue

                if not has_delta:
                    continue

                cols = [mn]
                if agent._has_live_context:
                    cw = detect_context(mn)
                    pct = round(total / cw * 100, 1) if cw else 0
                    cols.append(progress_bar(pct))
                    cols.append(f"{fmt_num(total)}/{fmt_num(cw)}")
                if _is_total_row(mv):
                    cols.append(f"总计 +{fmt_num(d_tok)}")
                else:
                    cols.append(f"入 +{fmt_num(d_in)}")
                    cols.append(f"出 +{fmt_num(d_out)}")
                    if any_cache_now:
                        rate = calc_cache_rate(d_in, d_cache)
                        if rate is not None:
                            cols.append(f"缓 +{fmt_num(d_cache)} ({min(rate, 99.9):.1f}%)")
                        else:
                            cols.append(f"缓 +{fmt_num(d_cache)}")
                    d_total = d_in + d_out
                    cols.append(f"总计/+缓存 +{fmt_num(d_total)}/+{fmt_num(d_total + d_cache)}")
                cols.append(f"调用 +{d_calls}")
                if delta_has_price:
                    pc = get_model_price(mn)
                    if pc and not _is_total_row(mv) and (d_in or d_out or d_cache):
                        dc = to_cny(calc_cost(d_in, d_out, d_cache, pc), pc.get('currency', 'CNY'))
                        cols.append(f"≈¥{dc:.4f}")
                    else:
                        cols.append("-")

                delta_rows.append((cols, mn, mv))

            if delta_rows:
                _print_aligned_monitor_block([r[0] for r in delta_rows], align_rows)
                for cols, mn, mv in delta_rows:
                    bl_models[mn] = mv
            if idle_models:
                print(f"  (未使用: {', '.join(idle_models)})")

            # 📅 今日合计
            try:
                print(_render_monitor_section_title("📅 今日"))
                if _all_rows_total(now_models) and today_start_baseline is not None:
                    # 累计型 agent：用基线差分计算今日增量
                    ti = to = tc = tca = 0
                    today_rows = []
                    today_has_price = any(get_model_price(mn) for mn in now_models)
                    for mn, mv in now_models.items():
                        bl = today_start_baseline.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
                        i = mv["input"] - bl["input"]
                        o = mv["output"] - bl["output"]
                        c = mv.get("cache", 0) - bl.get("cache", 0)
                        ca = mv["calls"] - bl["calls"]
                        if i == 0 and o == 0 and ca == 0:
                            continue
                        ti += i; to += o; tc += c; tca += ca
                        t = i + o
                        cols = [mn, f"总计 {fmt_num(t)}",
                                f"调用 {ca}"]
                        if today_has_price:
                            pc = get_model_price(mn)
                            cols.append(fmt_cost(i, o, c, pc) if pc and not _is_total_row(mv) else "-")
                        today_rows.append(cols)
                    if today_rows:
                        if len(today_rows) > 1:
                            sum_row = ["今日合计", f"总计 {fmt_num(ti + to)}",
                                       f"调用 {tca}"]
                            if today_has_price:
                                # 构造临时 per_model 用于费用计算
                                tmp_models = [{"model": mn, "input": mv["input"] - today_start_baseline.get(mn, {"input":0}).get("input",0),
                                               "output": 0, "cache": 0, "calls": 0, "token_mode": "total"} for mn, mv in now_models.items()]
                                tcs_str = fmt_total_cost(calc_total_cost(tmp_models))
                                if tcs_str:
                                    sum_row.append(f"{tcs_str} (仅供参考)")
                            today_rows.append(sum_row)
                        _print_aligned_monitor_block(today_rows, align_rows)
                else:
                    today_data = agent.collect(from_ts=today_start)
                    ti = to = tc = tca = 0
                    today_models = today_data.per_model or []
                    today_rows = []
                    today_has_price = has_any_price(today_models)
                    today_data_mode = getattr(today_data, 'token_mode', 'split')
                    is_today_total = bool(today_models) and all((pm.get("token_mode") or today_data_mode) == "total" for pm in today_models)
                    for pm in today_models:
                        m = pm.get("model", "?")
                        i = pm.get("input", 0) or 0
                        o = pm.get("output", 0) or 0
                        c = pm.get("cache", 0) or 0
                        ca = pm.get("calls", 0) or 0
                        row_is_total = (pm.get("token_mode") or today_data_mode) == "total"
                        if i == 0 and o == 0 and ca == 0:
                            continue
                        ti += i; to += o; tc += c; tca += ca
                        t = i + o
                        if row_is_total:
                            cols = [m, f"总计 {fmt_num(t)}",
                                    f"调用 {ca}"]
                        else:
                            cols = [m, f"入 {fmt_num(i)}", f"出 {fmt_num(o)}",
                                    fmt_cache_val(c, i),
                                    f"总计/+缓存 {fmt_num(t)}/{fmt_num(t + c)}", f"调用 {ca}"]
                        if today_has_price:
                            pc = get_model_price(m)
                            cols.append(fmt_cost(i, o, c, pc) if pc and not row_is_total else "-")
                        today_rows.append(cols)
                    if today_rows:
                        if len(today_models) > 1:
                            if is_today_total:
                                sum_row = ["今日合计", f"总计 {fmt_num(ti + to)}",
                                           f"调用 {tca}"]
                            else:
                                sum_row = ["今日合计", f"入 {fmt_num(ti)}", f"出 {fmt_num(to)}",
                                           fmt_cache_val(tc, ti),
                                           f"总计/+缓存 {fmt_num(ti + to)}/{fmt_num(ti + to + tc)}", f"调用 {tca}"]
                            if today_has_price:
                                tc_sum_str = fmt_total_cost(calc_total_cost(today_models))
                                if tc_sum_str:
                                    sum_row.append(f"{tc_sum_str} (仅供参考)")
                            today_rows.append(sum_row)
                        _print_aligned_monitor_block(today_rows, align_rows)
            except Exception:
                pass
        else:
            print(f"── [{ts}] 无新活动 ──")

        # 每轮无条件更新 baseline，防止因数据竞态导致 delta 累积假 spike
        for mn, mv in now_models.items():
            bl_models[mn] = mv
        for mn in list(bl_models.keys()):
            if mn not in now_models:
                del bl_models[mn]

        # 精确间隔补偿
        elapsed = time.monotonic() - tick_start
        if elapsed < interval and not stop_event.is_set():
            _interruptible_sleep(interval - elapsed)

    # ── 停止汇总：基于最新累计值 ──
    print()
    print("━" * 60)
    print("  📊 本次监控汇总")
    print("━" * 60)

    # 最终累计状态
    if bl_models:
        print("  最终状态:")
        final_rows = []
        bl_has_price = any(get_model_price(mn) for mn in bl_models)
        for mn, mv in sorted(bl_models.items()):
            total = mv["input"] + mv["output"]
            cache_v = mv.get("cache", 0)
            cols = [mn]
            if agent._has_live_context:
                cw = detect_context(mn)
                pct = round(total / cw * 100, 1) if cw else 0
                cols.append(progress_bar(pct))
                cols.append(f"{fmt_num(total)}/{fmt_num(cw)}")
            if _is_total_row(mv):
                cols.append(f"总计 {fmt_num(total)}")
            else:
                cols.append(f"入 {fmt_num(mv['input'])}")
                cols.append(f"出 {fmt_num(mv['output'])}")
                cols.append(fmt_cache_val(cache_v, mv['input']))
                cols.append(f"总计/+缓存 {fmt_num(total)}/{fmt_num(total + cache_v)}")
            cols.append(f"调用 {mv['calls']}")
            if bl_has_price:
                pc = get_model_price(mn)
                cols.append(fmt_cost(mv['input'], mv['output'], cache_v, pc) if pc and not _is_total_row(mv) else "-")
            final_rows.append(cols)
        _print_aligned_monitor_block(final_rows, align_rows)

        # 📅 今日累计
        try:
            today_label = datetime.fromtimestamp(today_start).strftime("%Y-%m-%d")
            print(f"\n{_render_monitor_section_title(f'📅 今日累计 ({today_label})')}")
            if _all_rows_total(bl_models) and today_start_baseline is not None:
                # 累计型 agent：用基线差分
                ti = to = tc = tca = 0
                today_rows = []
                today_has_price = any(get_model_price(mn) for mn in bl_models)
                for mn, mv in sorted(bl_models.items()):
                    bl = today_start_baseline.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
                    i = mv["input"] - bl["input"]
                    o = mv["output"] - bl["output"]
                    c = mv.get("cache", 0) - bl.get("cache", 0)
                    ca = mv["calls"] - bl["calls"]
                    if i == 0 and o == 0 and ca == 0:
                        continue
                    ti += i; to += o; tc += c; tca += ca
                    t = i + o
                    cols = [mn, f"总计 {fmt_num(t)}", f"调用 {ca}"]
                    if today_has_price:
                        pc = get_model_price(mn)
                        cols.append(fmt_cost(i, o, c, pc) if pc and not _is_total_row(mv) else "-")
                    today_rows.append(cols)
                if today_rows:
                    if len(today_rows) > 1:
                        sum_row = ["今日合计", f"总计 {fmt_num(ti + to)}", f"调用 {tca}"]
                        if today_has_price:
                            tmp_models = [{"model": mn, "input": mv["input"] - today_start_baseline.get(mn, {"input":0}).get("input",0),
                                           "output": 0, "cache": 0, "calls": 0, "token_mode": "total"} for mn, mv in bl_models.items()]
                            tcs_str = fmt_total_cost(calc_total_cost(tmp_models))
                            if tcs_str:
                                sum_row.append(f"{tcs_str} (仅供参考)")
                        today_rows.append(sum_row)
                    _print_aligned_monitor_block(today_rows, align_rows)
            else:
                today_data = agent.collect(from_ts=today_start)
                ti = to = tc = tca = 0
                today_models = today_data.per_model or []
                today_rows = []
                today_has_price = has_any_price(today_models)
                today_data_mode = getattr(today_data, 'token_mode', 'split')
                is_today_total = bool(today_models) and all((pm.get("token_mode") or today_data_mode) == "total" for pm in today_models)
                for pm in today_models:
                    m = pm.get("model", "?")
                    i = pm.get("input", 0) or 0
                    o = pm.get("output", 0) or 0
                    c = pm.get("cache", 0) or 0
                    ca = pm.get("calls", 0) or 0
                    row_is_total = (pm.get("token_mode") or today_data_mode) == "total"
                    if i == 0 and o == 0 and ca == 0:
                        continue
                    ti += i; to += o; tc += c; tca += ca
                    t = i + o
                    if row_is_total:
                        cols = [m, f"总计 {fmt_num(t)}", f"调用 {ca}"]
                    else:
                        cols = [m, f"入 {fmt_num(i)}", f"出 {fmt_num(o)}",
                                fmt_cache_val(c, i),
                                f"总计/+缓存 {fmt_num(t)}/{fmt_num(t + c)}", f"调用 {ca}"]
                    if today_has_price:
                        pc = get_model_price(m)
                        cols.append(fmt_cost(i, o, c, pc) if pc and not row_is_total else "-")
                    today_rows.append(cols)
                if today_rows:
                    if len(today_models) > 1:
                        if is_today_total:
                            sum_row = ["今日合计", f"总计 {fmt_num(ti + to)}", f"调用 {tca}"]
                        else:
                            sum_row = ["今日合计", f"入 {fmt_num(ti)}", f"出 {fmt_num(to)}",
                                       fmt_cache_val(tc, ti),
                                       f"总计/+缓存 {fmt_num(ti + to)}/{fmt_num(ti + to + tc)}", f"调用 {tca}"]
                        if today_has_price:
                            tcs_str = fmt_total_cost(calc_total_cost(today_models))
                            if tcs_str:
                                sum_row.append(f"{tcs_str} (仅供参考)")
                        today_rows.append(sum_row)
                    _print_aligned_monitor_block(today_rows, align_rows)
        except Exception:
            pass

        # 📅 昨日累计（仅在跨天时显示）
        if yesterday_start is not None:
            try:
                yesterday_data = agent.collect(from_ts=yesterday_start, to_ts=today_start - 1)
                yti = yto = ytc = ytca = 0
                yesterday_models = yesterday_data.per_model or []
                yesterday_rows = []
                yest_has_price = has_any_price(yesterday_models)
                yesterday_data_mode = getattr(yesterday_data, 'token_mode', 'split')
                is_yest_total = bool(yesterday_models) and all((pm.get("token_mode") or yesterday_data_mode) == "total" for pm in yesterday_models)
                for pm in yesterday_models:
                    m = pm.get("model", "?")
                    i = pm.get("input", 0) or 0
                    o = pm.get("output", 0) or 0
                    c = pm.get("cache", 0) or 0
                    ca = pm.get("calls", 0) or 0
                    row_is_total = (pm.get("token_mode") or yesterday_data_mode) == "total"
                    if i == 0 and o == 0 and ca == 0:
                        continue
                    yti += i; yto += o; ytc += c; ytca += ca
                    t = i + o
                    if row_is_total:
                        cols = [m, f"总计 {fmt_num(t)}", f"调用 {ca}"]
                    else:
                        cols = [m, f"入 {fmt_num(i)}", f"出 {fmt_num(o)}",
                                fmt_cache_val(c, i),
                                f"总计/+缓存 {fmt_num(t)}/{fmt_num(t + c)}", f"调用 {ca}"]
                    if yest_has_price:
                        pc = get_model_price(m)
                        cols.append(fmt_cost(i, o, c, pc) if pc and not row_is_total else "-")
                    yesterday_rows.append(cols)
                if yesterday_rows:
                    yesterday_label = datetime.fromtimestamp(yesterday_start).strftime("%Y-%m-%d")
                    print(f"\n{_render_monitor_section_title(f'📅 昨日累计 ({yesterday_label})')}")
                    if len(yesterday_rows) > 1:
                        if is_yest_total:
                            sum_row = ["昨日合计", f"总计 {fmt_num(yti + yto)}", f"调用 {ytca}"]
                        else:
                            sum_row = ["昨日合计", f"入 {fmt_num(yti)}", f"出 {fmt_num(yto)}",
                                       fmt_cache_val(ytc, yti),
                                       f"总计/+缓存 {fmt_num(yti + yto)}/{fmt_num(yti + yto + ytc)}", f"调用 {ytca}"]
                        if yest_has_price:
                            ycs_str = fmt_total_cost(calc_total_cost(yesterday_models))
                            if ycs_str:
                                sum_row.append(f"{ycs_str} (仅供参考)")
                        yesterday_rows.append(sum_row)
                    _print_aligned_monitor_block(yesterday_rows, align_rows)
            except Exception:
                pass

        # 总增量（最新累计 - 初始基线）
        total_d_tok = total_d_cache = total_d_calls = 0
        total_d_in = total_d_out = 0
        total_d_cost = 0.0
        any_d_cache = False
        delta_data = []
        for mn, mv in sorted(bl_models.items()):
            init = bl_initial.get(mn, {"input": 0, "output": 0, "cache": 0, "calls": 0})
            d_in = mv["input"] - init["input"]
            d_out = mv["output"] - init["output"]
            d_tok = d_in + d_out
            d_cache = mv.get("cache", 0) - init.get("cache", 0)
            d_calls = mv["calls"] - init["calls"]
            total_d_in += d_in; total_d_out += d_out
            total_d_tok += d_tok; total_d_cache += d_cache; total_d_calls += d_calls
            if d_tok > 0 or d_cache > 0 or d_calls > 0:
                if d_cache:
                    any_d_cache = True
                pc = get_model_price(mn)
                if pc and not _is_total_row(mv):
                    dc = to_cny(calc_cost(d_in, d_out, d_cache, pc), pc.get('currency', 'CNY'))
                    total_d_cost += dc
                delta_data.append((mn, d_tok, d_in, d_out, d_cache, d_calls, pc, _is_total_row(mv)))

        if delta_data:
            print(f"\n  监控期间增量:")
            inc_rows = []
            for (mn, d_tok, d_in, d_out, d_cache, d_calls, pc, row_is_total) in delta_data:
                if row_is_total:
                    cols = [mn, f"总计 {fmt_num(d_tok)}"]
                else:
                    cols = [
                        mn,
                        f"入 {fmt_num(d_in)}",
                        f"出 {fmt_num(d_out)}",
                    ]
                    if any_d_cache:
                        cols.append(fmt_cache_val(d_cache, d_in))
                    cols.append(f"总计/+缓存 {fmt_num(d_tok)}/{fmt_num(d_tok + d_cache)}")
                cols.append(f"调用 {d_calls}")
                if pc and not row_is_total and (d_in or d_out or d_cache):
                    dc = to_cny(calc_cost(d_in, d_out, d_cache, pc), pc.get('currency', 'CNY'))
                    cols.append(f"≈¥{dc:.4f}")
                inc_rows.append(cols)
            _print_aligned_monitor_block(inc_rows, align_rows)
            if len(delta_data) > 1:
                if all(item[7] for item in delta_data):
                    sum_parts = [f"总计 {fmt_num(total_d_tok)}"]
                else:
                    sum_parts = [
                        f"入 {fmt_num(total_d_in)}",
                        f"出 {fmt_num(total_d_out)}",
                    ]
                    if total_d_cache:
                        sum_parts.append(fmt_cache_val(total_d_cache, total_d_in))
                    sum_parts.append(f"总计/+缓存 {fmt_num(total_d_tok)}/{fmt_num(total_d_tok + total_d_cache)}")
                sum_parts.append(f"调用 {total_d_calls}")
                if total_d_cost > 0:
                    sum_parts.append(f"≈¥{total_d_cost:.4f}")
                _print_aligned_monitor_block([["增量合计", *sum_parts]], align_rows)
    else:
        print("  监控期间无数据")

    duration = time.time() - watch_start
    if duration < 60:
        dur_str = f"{duration:.0f} 秒"
    elif duration < 3600:
        dur_str = f"{duration / 60:.0f} 分 {duration % 60:.0f} 秒"
    else:
        dur_str = f"{duration / 3600:.0f} 时 {(duration % 3600) / 60:.0f} 分"
    print(f"  监控时长: {dur_str} | 采集 {tick_count} 轮")
    if yesterday_start is not None:
        yesterday_label = datetime.fromtimestamp(yesterday_start).strftime("%Y-%m-%d")
        today_label = datetime.fromtimestamp(today_start).strftime("%Y-%m-%d")
        print(f"  ⚠️ 监控跨越 {yesterday_label} → {today_label}，跨天时\"今日\"数据已重置")
    print("👋 监控已停止")
