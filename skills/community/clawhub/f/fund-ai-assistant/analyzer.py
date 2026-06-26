#!/usr/bin/env python3
"""
基金追踪分析主脚本
用法:
  python3 analyzer.py                  # 分析所有追踪的基金
  python3 analyzer.py add 161226       # 添加基金到追踪列表
  python3 analyzer.py remove 161226    # 从追踪列表移除
  python3 analyzer.py list             # 显示追踪列表
  python3 analyzer.py single 161226     # 分析单只基金
  python3 analyzer.py ai 161226         # AI 量化分析（MiniMax）
  python3 analyzer.py compare 161226 519  # 对比两只基金
  python3 analyzer.py search 白银      # 搜索基金
  python3 analyzer.py history 161226 30  # 查看历史净值
"""
import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")
ASSETS_DIR = os.path.join(SKILL_DIR, "assets")


def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"tracked_funds": [], "analysis_days": 90}


def save_config(cfg: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def add_fund(code: str) -> dict:
    """添加基金到追踪列表"""
    from fund_api import fetch_otc_fund_valuation, fetch_fund_info
    val = fetch_otc_fund_valuation(code)
    if not val:
        return {"ok": False, "error": f"无法获取基金 {code} 数据，请检查基金代码是否正确"}
    info = fetch_fund_info(code)
    name = info.get("name", "") if info else val.get("name", "")
    cfg = load_config()
    codes = [f["code"] for f in cfg.get("tracked_funds", [])]
    if code in codes:
        return {"ok": False, "error": f"基金 {code} ({name}) 已在追踪列表中"}
    cfg.setdefault("tracked_funds", []).append({
        "code": code,
        "name": name,
    })
    save_config(cfg)
    return {"ok": True, "fund": val, "name": name}


def remove_fund(code: str) -> dict:
    """从追踪列表移除"""
    cfg = load_config()
    funds = cfg.get("tracked_funds", [])
    new_funds = [f for f in funds if f["code"] != code]
    if len(new_funds) == len(funds):
        return {"ok": False, "error": f"基金 {code} 不在追踪列表中"}
    cfg["tracked_funds"] = new_funds
    save_config(cfg)
    return {"ok": True}


def list_funds() -> list:
    """列出追踪基金"""
    cfg = load_config()
    return cfg.get("tracked_funds", [])


def analyze_fund(code: str, macro_data: dict = None) -> dict:
    """对单只基金进行完整分析，可选传入宏观局势数据"""
    from fund_api import fetch_otc_fund_valuation, fetch_otc_fund_history
    from technical import analyze_fund as tech_analyze

    valuation = fetch_otc_fund_valuation(code)
    history = fetch_otc_fund_history(code, days=90)

    if not history:
        return {"ok": False, "error": f"无法获取 {code} 历史数据"}

    analysis = tech_analyze(code, history)

    # 持仓数据
    position = None
    try:
        from positions import get_position_for_fund
        position = get_position_for_fund(code)
    except Exception:
        pass

    # 生成图表
    chart_img = None
    try:
        from chart_generator import generate_fund_analysis_image, PIL_AVAILABLE
        if PIL_AVAILABLE:
            fund_name = valuation.get("name", code) if valuation else code
            nav = valuation.get("nav", history[-1]["nav"]) if valuation else history[-1]["nav"]
            est_change = valuation.get("est_change", 0) if valuation else 0
            chart_img = generate_fund_analysis_image(
                fund_code=code,
                fund_name=fund_name,
                latest_nav=nav,
                nav_change=est_change,
                analysis=analysis,
                position=position,
            )
    except Exception as e:
        print(f"[分析] 图表生成失败: {e}")

    # AI 分析（含持仓数据 + 宏观数据）
    ai_result = {"data": None, "text": ""}
    try:
        from ai_analysis import ai_analyze_fund
        combined = {**analysis, "est_change": valuation.get("est_change", 0) if valuation else 0}
        ai_result = ai_analyze_fund(code, valuation.get("name", "") if valuation else code, combined, valuation, position, macro_data)
    except Exception as e:
        print(f"[分析] AI 分析失败: {e}")

    ai_text = ai_result.get("text", "") if isinstance(ai_result, dict) else ai_result

    return {
        "ok": True,
        "code": code,
        "name": valuation.get("name", "") if valuation else "",
        "valuation": valuation,
        "analysis": {k: v for k, v in analysis.items() if k not in ["prices", "changes"]},
        "prices": [h["nav"] for h in history],
        "dates": [h["date"] for h in history],
        "position": position,
        "chart_img": chart_img,
        "ai_text": ai_text,
        "ai_data": ai_result.get("data") if isinstance(ai_result, dict) else None,
    }


def analyze_all() -> list:
    """分析所有追踪的基金，先获取宏观局势数据"""
    from macro_fetcher import fetch_macro_data

    # 先拉取宏观数据（每个分析周期只查一次）
    macro_data = fetch_macro_data()
    if macro_data.get("ok"):
        print(f"[宏观] 局势数据获取成功 ({macro_data.get('fetch_time', '')})")
    else:
        print(f"[宏观] 局势数据获取失败: {macro_data.get('error', '未知')}")

    cfg = load_config()
    funds = cfg.get("tracked_funds", [])
    results = []
    for fund in funds:
        r = analyze_fund(fund["code"], macro_data)
        results.append(r)

    # 生成 QQ 摘要
    qq_summary = build_qq_summary(results)
    print("\n" + qq_summary)

    return results


def build_qq_summary(results: list) -> str:
    """
    生成发送给 QQ 的丰富摘要文字
    每只基金两行：首行关键指标 + 次行核心逻辑
    直接从 ai_data（原始JSON）提取，不用文本解析
    """
    from datetime import datetime

    date_str = datetime.now().strftime("%Y-%m-%d")
    lines = [f"📊 基金追踪 | {date_str}（宏观局势已注入）\n"]

    for r in results:
        if not r.get("ok"):
            continue

        code = r.get("code", "")
        name = r.get("name", code)
        val  = r.get("valuation") or {}
        nav  = val.get("nav", 0)
        chg  = val.get("est_change", 0)
        sign = "+" if chg >= 0 else ""
        pos  = r.get("position")

        ai_data = r.get("ai_data") or {}
        score   = ai_data.get("综合评分", {})
        action  = ai_data.get("操作建议", {})
        levels  = ai_data.get("关键价位", {})
        ops     = ai_data.get("多时间维度操作建议", {})
        game    = ai_data.get("博弈论分析", {})

        total_score    = score.get("总分", "?")
        rating_emoji   = {"极强":"🟢🟢","强劲":"🟢","良好":"🟡","中性":"🟡","偏弱":"🔴","弱势":"🔴🔴"}.get(score.get("综合评级",""), "🟡")
        action_emoji  = {"强烈买入":"🟢🟢","买入":"🟢","持有":"🟡","观望":"⚪","减仓":"🔴","强烈减仓":"🔴🔴"}.get(action.get("行动",""), "🟡")
        action_text   = action.get("行动", "持有")
        stop_loss     = action.get("止损位", "—")
        take_profit   = action.get("止盈参考", "—")
        confidence    = action.get("置信度", "?")
        core_reason   = action.get("核心理由", "—")
        support       = levels.get("强支撑位1", "—")
        pressure      = levels.get("强压力位1", "—")

        short         = (ops.get("短线（1-4周）") or {}) if ops else {}
        short_action  = short.get("建议", "—")
        short_cond_add = short.get("触发加仓条件", "")
        short_cond_sub = short.get("触发减仓条件", "")

        game_conclusion = (game.get("博弈论结论","") or "") if game else ""
        game_key_price  = (game.get("关键博弈价位","") or "") if game else ""

        pos_info = ""
        if pos:
            qty    = pos.get("total_quantity", 0)
            cost   = pos.get("avg_cost", 0)
            profit = (nav - cost) * qty if nav and cost else 0
            pct    = (nav / cost - 1) * 100 if nav and cost else 0
            psign  = "+" if profit >= 0 else ""
            pos_info = f" | 持仓{qty}份 成本{cost:.4f} {psign}{profit:.2f}元({psign}{pct:.2f}%)"

        # 第一行
        line1 = (
            f"{rating_emoji} {name}（{code}）"
            f" {action_emoji}{action_text} {total_score}分"
            f" | 净值{nav:.4f} {sign}{chg:.2f}%"
            f" | 支撑{support} / 压力{pressure}"
        )

        # 第二行
        line2_parts = []
        if core_reason and core_reason != "—":
            line2_parts.append(core_reason[:70] + ("…" if len(core_reason) > 70 else ""))
        if short_action and short_action != "—" and (short_cond_add or short_cond_sub):
            add_str = f"加:{short_cond_add[:30]}" if short_cond_add else ""
            sub_str = f"减:{short_cond_sub[:30]}" if short_cond_sub else ""
            cond_str = " ".join(x for x in [add_str, sub_str] if x)
            line2_parts.append(f"短线{short_action} {cond_str}")
        if game_conclusion and game_conclusion != "—":
            line2_parts.append(f"🎯{game_conclusion[:55]}{'…' if len(game_conclusion) > 55 else ''}")
        if game_key_price and game_key_price != "—":
            line2_parts.append(f"博弈位:{game_key_price}")
        if pos_info:
            line2_parts.append(pos_info)

        line2 = ("  " + " | ".join(line2_parts)) if line2_parts else ""

        lines.append(line1)
        if line2:
            lines.append(line2)
        lines.append("")

    return "\n".join(lines)


def format_analysis_report(results: list) -> str:
    """格式化分析报告（纯文本）"""
    lines = ["📊 基金追踪分析报告\n"]

    for r in results:
        if not r.get("ok"):
            lines.append(f"❌ {r.get('code')}: {r.get('error')}\n")
            continue

        val = r.get("valuation", {}) or {}
        ana = r.get("analysis", {})
        pos = r.get("position")
        name = r.get("name", r["code"])
        nav = val.get("nav", 0)
        est_change = val.get("est_change", 0)
        sign = "+" if est_change >= 0 else ""
        nav_color = "🔴" if est_change >= 0 else "🟢"

        lines.append(f"─── {name}（{r['code']}）───")
        lines.append(f"净值: {nav:.4f}  {nav_color}{sign}{est_change:.2f}%")

        # 持仓信息
        if pos:
            profit = (nav - pos["avg_cost"]) * pos["total_quantity"] if nav else 0
            profit_pct = (nav / pos["avg_cost"] - 1) * 100 if nav and pos["avg_cost"] else 0
            profit_sign = "+" if profit >= 0 else ""
            lines.append(f"📦 持仓: {pos['total_quantity']}份  成本价: {pos['avg_cost']:.4f}  盈亏: {profit_sign}{profit:.2f}元 ({profit_sign}{profit_pct:.2f}%)")

        lines.append(f"趋势: {ana.get('trend', '—')}")
        lines.append(f"RSI: {ana.get('rsi14', '—')}")
        lines.append(f"MACD: DIF={ana.get('macd_dif','—')} DEA={ana.get('macd_dea','—')} Hist={ana.get('macd_hist','—')}")
        lines.append(f"布林带: {ana.get('boll_upper','—'):.4f} / {ana.get('boll_middle','—'):.4f} / {ana.get('boll_lower','—'):.4f}")
        lines.append(f"波动率: {ana.get('volatility','—')}%  回撤: {ana.get('max_drawdown','—')}%  夏普: {ana.get('sharpe_ratio','—')}")
        r1w = ana.get('return_1w')
        r1m = ana.get('return_1m')
        r3m = ana.get('return_3m')
        lines.append(f"近1月: {r1m}%" + (f"  近3月: {r3m}%" if r3m else "") + (f"  近6月: {ana.get('return_6m','—')}%" if ana.get('return_6m') is not None else ""))
        # AI 分析
        if r.get("ai_text"):
            lines.append("")
            lines.append("🤖 AI 量化分析:")
            lines.append(r["ai_text"])
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"

    if cmd == "list":
        funds = list_funds()
        if not funds:
            print("追踪列表为空，请使用 analyzer.py add <代码> 添加基金")
        else:
            print(f"共追踪 {len(funds)} 只基金:")
            for i, f in enumerate(funds, 1):
                print(f"  {i}. {f['code']} - {f.get('name', '未知')}")

    elif cmd == "add" and len(sys.argv) > 2:
        code = sys.argv[2].strip()
        result = add_fund(code)
        if result["ok"]:
            print(f"✅ 已添加: {result.get('name', result['fund'].get('name', ''))}（{code}）")
        else:
            print(f"❌ {result['error']}")

    elif cmd == "remove" and len(sys.argv) > 2:
        code = sys.argv[2].strip()
        result = remove_fund(code)
        if result["ok"]:
            print(f"✅ 已移除: {code}")
        else:
            print(f"❌ {result['error']}")

    elif cmd == "single" and len(sys.argv) > 2:
        code = sys.argv[2].strip()
        result = analyze_fund(code)
        if result["ok"]:
            report = format_analysis_report([result])
            print(report)
            if result.get("chart_img"):
                out = os.path.join(ASSETS_DIR, f"{code}_analysis.png")
                with open(out, "wb") as f:
                    f.write(result["chart_img"])
                print(f"📊 图表已保存: {out}")
            if result.get("ai_text"):
                print(f"\n🤖 AI 量化分析:\n{result['ai_text']}")
        else:
            print(f"❌ {result.get('error')}")

    elif cmd == "ai" and len(sys.argv) > 2:
        code = sys.argv[2].strip()
        result = analyze_fund(code)
        if result["ok"]:
            ai_text = result.get("ai_text")
            if ai_text:
                print(ai_text)
                # 保存 AI 分析文本
                out = os.path.join(ASSETS_DIR, f"{code}_ai.txt")
                with open(out, "w") as f:
                    f.write(ai_text)
                print(f"\n💾 AI 分析已保存: {out}")
            else:
                print("⚠️ AI 分析未返回结果")
        else:
            print(f"❌ {result.get('error')}")

    elif cmd == "analyze" or cmd == "all":
        results = analyze_all()
        report = format_analysis_report(results)
        print(report)
        # 保存各基金独立图表
        for r in results:
            if r.get("ok") and r.get("chart_img"):
                out = os.path.join(ASSETS_DIR, f"{r['code']}_analysis.png")
                with open(out, "wb") as f:
                    f.write(r["chart_img"])
                print(f"📊 {r['name']}（{r['code']}）图表: {out}")
        # 生成7只基金合并对比图表
        funds_data = []
        for r in results:
            if not r.get("ok"):
                continue
            val = r.get("valuation") or {}
            funds_data.append({
                "code": r["code"],
                "name": r.get("name", ""),
                "nav": val.get("nav", 0),
                "change": val.get("est_change", 0),
                "prices": r.get("prices", []),
                "dates": r.get("dates", []),
                "analysis": r.get("analysis", {}),
            })
        if funds_data:
            try:
                from chart_generator import generate_combined_chart
                combined = generate_combined_chart(funds_data)
                if combined:
                    out = os.path.join(ASSETS_DIR, "latest_analysis.png")
                    with open(out, "wb") as f:
                        f.write(combined)
                    print(f"📊 合并对比图表: {out}")
            except Exception as e:
                print(f"[图表] 合并图表生成失败: {e}")

    elif cmd == "compare" and len(sys.argv) > 3:
        codes = [sys.argv[2].strip(), sys.argv[3].strip()]
        from technical import calc_ma
        from fund_api import fetch_otc_fund_history, fetch_fund_info
        results = []
        for code in codes:
            info = fetch_fund_info(code)
            name = info.get("name", code) if info else code
            hist = fetch_otc_fund_history(code, days=90)
            if hist:
                prices = [d["nav"] for d in hist]
                ma5_d = [calc_ma(prices, 5)] * len(prices) if len(prices) >= 5 else None
                ma10_d = [calc_ma(prices, 10)] * len(prices) if len(prices) >= 10 else None
                ma20_d = [calc_ma(prices, 20)] * len(prices) if len(prices) >= 20 else None
                dates = [d["date"] for d in hist]
                try:
                    from chart_generator import draw_fund_chart
                    img_data = draw_fund_chart(prices, dates, ma5_d, ma10_d, ma20_d, width=420, height=200)
                    out = os.path.join(ASSETS_DIR, f"compare_{code}.png")
                    with open(out, "wb") as f:
                        f.write(img_data)
                    print(f"✅ {name}（{code}）图表: {out}")
                except Exception as e:
                    print(f"图表生成失败: {e}")
                results.append({"code": code, "name": name, "hist": hist})
            else:
                print(f"❌ 无法获取 {code} 数据")
        if len(results) == 2:
            def period_ret(hist, days):
                if len(hist) < days + 1:
                    return None
                try:
                    return round((hist[0]["nav"] - hist[days]["nav"]) / hist[days]["nav"] * 100, 2)
                except Exception:
                    return None
            r1, r2 = results
            print(f"\n📊 基金对比:")
            print(f"  {r1['name']}（{r1['code']}）近1月: {period_ret(r1['hist'], 22)}%  近3月: {period_ret(r1['hist'], 66)}%")
            print(f"  {r2['name']}（{r2['code']}）近1月: {period_ret(r2['hist'], 22)}%  近3月: {period_ret(r2['hist'], 66)}%")

    elif cmd == "search" and len(sys.argv) > 2:
        keyword = sys.argv[2].strip()
        from fund_api import search_fund
        results = search_fund(keyword)
        if not results:
            print(f"未找到包含 '{keyword}' 的基金")
        else:
            print(f"找到 {len(results)} 只基金:")
            for f in results[:10]:
                nav_str = f" 净值:{f.get('nav','-')}" if f.get('nav') else ""
                print(f"  {f['code']} - {f['name']} ({f.get('type','')}){nav_str}")

    elif cmd == "history" and len(sys.argv) > 3:
        code = sys.argv[2].strip()
        days = int(sys.argv[3].strip())
        from fund_api import fetch_otc_fund_history
        hist = fetch_otc_fund_history(code, days=days)
        if hist:
            print(f"{code} 近{days}天净值:")
            for r in hist[:30]:
                print(f"  {r['date']}  {r['nav']:.4f}  {r['change']:+.2f}%")
        else:
            print(f"❌ 无法获取 {code} 历史数据")

    elif cmd == "buy" and len(sys.argv) >= 6:
        # buy <code> <price> <quantity> <date> [note]
        code = sys.argv[2].strip()
        price = float(sys.argv[3].strip())
        quantity = float(sys.argv[4].strip())
        op_date = sys.argv[5].strip()
        note = sys.argv[6].strip() if len(sys.argv) > 6 else ""
        from positions import add_record
        rec = add_record(code, "buy", price, quantity, op_date, note)
        print(f"✅ 买入记录已添加: {code} {rec['price']:.4f} × {rec['quantity']}份 @ {rec['date']}")

    elif cmd == "sell" and len(sys.argv) >= 6:
        code = sys.argv[2].strip()
        price = float(sys.argv[3].strip())
        quantity = float(sys.argv[4].strip())
        op_date = sys.argv[5].strip()
        note = sys.argv[6].strip() if len(sys.argv) > 6 else ""
        from positions import add_record
        rec = add_record(code, "sell", price, quantity, op_date, note)
        print(f"✅ 卖出记录已添加: {code} {rec['price']:.4f} × {rec['quantity']}份 @ {rec['date']}")

    elif cmd == "positions" and len(sys.argv) > 2:
        code = sys.argv[2].strip()
        from positions import get_position_for_fund
        pos = get_position_for_fund(code)
        if not pos:
            print(f"❌ {code} 没有持仓记录")
        else:
            print(f"📦 {code} 当前持仓:")
            print(f"  剩余份额: {pos['total_quantity']}份")
            print(f"  成本价: {pos['avg_cost']:.4f}")
            print(f"  总成本: {pos['total_cost']:.2f}元")
            print(f"  持仓天数: {pos['hold_days']}天")
            print(f"  买入次数: {pos['buy_count']} | 卖出次数: {pos['sell_count']}")
            print(f"\n操作记录:")
            for r in pos["records"]:
                sign = "+" if r["type"] == "buy" else "-"
                emoji = "🟢买入" if r["type"] == "buy" else "🔴卖出"
                print(f"  {emoji} {r['date']}  价格:{r['price']:.4f}  份额:{sign}{r['quantity']}  ID:{r['id']}  {r.get('note','')}")

    elif cmd == "my_positions":
        from positions import get_all_positions
        from fund_api import fetch_otc_fund_valuation
        all_pos = get_all_positions()
        if not all_pos:
            print("暂无持仓记录")
        else:
            print(f"📦 我的持仓（共 {len(all_pos)} 只基金）:\n")
            for code, pos in all_pos.items():
                val = fetch_otc_fund_valuation(code)
                nav = val.get("nav", 0) if val else 0
                current_value = nav * pos["total_quantity"]
                profit = (nav - pos["avg_cost"]) * pos["total_quantity"]
                profit_pct = (nav / pos["avg_cost"] - 1) * 100 if pos["avg_cost"] > 0 else 0
                sign = "+" if profit >= 0 else ""
                name = val.get("name", code) if val else code
                print(f"  【{name}】{code}")
                print(f"    持仓: {pos['total_quantity']}份  成本价: {pos['avg_cost']:.4f}  当前: {nav:.4f}")
                print(f"    盈亏: {sign}{profit:.2f}元 ({sign}{profit_pct:.2f}%)  市值: {current_value:.2f}元")
                print(f"    持仓: {pos['hold_days']}天\n")

    elif cmd == "position_remove" and len(sys.argv) > 3:
        code = sys.argv[2].strip()
        record_id = sys.argv[3].strip()
        from positions import remove_record
        ok = remove_record(code, record_id)
        print(f"{'✅ 已删除' if ok else '❌ 删除失败'} 记录ID: {record_id}")

    elif cmd == "recommend":
        from recommend import format_recommendation_report
        print(format_recommendation_report())

    else:
        print("用法:")
        print("  analyzer.py list                          # 列出追踪基金")
        print("  analyzer.py add <代码>                   # 添加基金")
        print("  analyzer.py remove <代码>                 # 移除基金")
        print("  analyzer.py single <代码>                 # 分析单只基金")
        print("  analyzer.py analyze                       # 分析所有追踪基金")
        print("  analyzer.py compare <代码1> <代码2>       # 对比两只基金")
        print("  analyzer.py search <关键词>               # 搜索基金")
        print("  analyzer.py history <代码> <天数>          # 查看历史净值")
        print("  analyzer.py buy <代码> <价格> <份额> <日期> [备注]   # 记录买入")
        print("  analyzer.py sell <代码> <价格> <份额> <日期> [备注] # 记录卖出")
        print("  analyzer.py positions <代码>             # 查看某基金持仓记录")
        print("  analyzer.py my_positions                # 查看所有基金当前持仓汇总")
        print("  analyzer.py position_remove <代码> <ID>  # 删除持仓记录")
        print("  analyzer.py recommend                   # 建仓优化建议（核心功能）")
