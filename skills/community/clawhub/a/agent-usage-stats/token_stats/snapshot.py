"""Snapshot and all-agent summary output."""

from __future__ import annotations

from .formatting import is_total_mode


def show_all(all_agents: list, detect_installed, helpers: dict, *, from_ts: float = None, to_ts: float = None):
    skip_model = helpers["skip_model"]
    fmt_num = helpers["fmt_num"]
    fmt_cache_val = helpers["fmt_cache_val"]
    get_model_price = helpers["get_model_price"]
    calc_cost = helpers["calc_cost"]
    fmt_total_cost = helpers["fmt_total_cost"]

    """显示本机所有 Agent 的统计"""
    installed = detect_installed()
    if not installed:
        print("❌ 本机未检测到任何支持的 AI 助手")
        return

    print("\n📊 本机 Agent 统计汇总")
    print("═" * 50)

    any_data = False
    grand_ti = grand_to = grand_tc = grand_tca = 0
    grand_costs: dict[str, float] = {}
    agent_count = 0
    for cls in all_agents:
        detected = cls.detect()
        status = "✅" if detected else "❌"
        name = cls.display_name()
        print(f"\n{status} {name}")

        if detected:
            try:
                agent = cls()
                print(f"  ⏳ 正在收集 {cls.display_name()} 数据...", end="\r", flush=True)
                data = agent.collect(from_ts=from_ts, to_ts=to_ts)
                print(" " * 40, end="\r")
                if data.stats:
                    any_data = True
                    for pm in (data.per_model or []):
                        if skip_model(pm):
                            continue
                        inp = pm.get("input", 0) or 0
                        out = pm.get("output", 0) or 0
                        cache = pm.get("cache", 0) or 0
                        calls = pm.get("calls", 0) or 0
                        grand_ti += inp
                        grand_to += out
                        grand_tc += cache
                        grand_tca += calls
                        pc = None if is_total_mode(pm) else get_model_price(pm.get("model", ""))
                        if pc:
                            cur = pc.get('currency', 'CNY')
                            grand_costs[cur] = grand_costs.get(cur, 0.0) + calc_cost(inp, out, cache, pc)
                    agent_count += 1
                print(data.raw)
            except Exception as e:
                msg = str(e)
                if "locked" in msg.lower():
                    msg = "数据库被锁定（Agent 正在运行，请先关闭 Agent）"
                print(f"  ⚠️ 读取失败: {msg}")
        else:
            print("  (未安装)")

    # Grand Total
    if agent_count > 1:
        gtt = grand_ti + grand_to
        print(f"\n{'═' * 50}")
        print("  全部 Agent 总计")
        parts = f"  入 {fmt_num(grand_ti)} | 出 {fmt_num(grand_to)} | {fmt_cache_val(grand_tc, grand_ti)} | 总计/+缓存 {fmt_num(gtt)}/{fmt_num(gtt + grand_tc)} | 调用 {grand_tca} 次"
        total_cost_str = fmt_total_cost(grand_costs)
        if total_cost_str:
            parts += f" | {total_cost_str} (仅供参考)"
        print(parts)

    if not any_data:
        print("\n（所有 Agent 均无数据）")
    print()
