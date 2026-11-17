#!/usr/bin/env python3
"""
validate_report.py v3.1 — 薄入口

检查生成的 AI 新闻网站 HTML 是否完整合规。
适配 v3.0 新闻网站格式（news_site_template.html），兼容旧版 v2.0 周报格式。

本文件只保留「编排(validate) + 报告打印(print_report) + CLI(main)」；
所有检查函数已拆分到 validate_checks/ 子包（按职责：common / news_v3 / v2 /
market / keywords / source），便于维护与单测，且不直接膨胀主生成引擎
（受 P0#4 模块体量守护豁免）。

用法：
  python scripts/validate_report.py --html AI_News_2026-07-09.html
  python scripts/validate_report.py --html AI_Weekly_Report_2026_W27.html  # 兼容旧版

检查项：
  1. 文件完整性（存在 + 非空）
  2. 新闻条目 >= 20 条 + 来源链接 >= 80%
  3. 搜索栏功能（v3.0 新闻站）或 图表完整（v2.0 周报）
  4. 分类标签 / KPI 数据
  5. 数据来源说明
"""

import argparse
import json
import sys
from pathlib import Path

from validate_checks import (
    _detect_format, check_file_exists, check_data_sources,
    check_news_v3, check_search_v3, check_charts_v3, check_ranking_v3,
    check_leaderboard_quality, check_editorial_c0, check_editorial_c1,
    check_news_v2, check_kpi_v2, check_charts_v2,
    check_market_disclaimer, check_market_signals, check_market_structure,
    check_trend_evidence, check_market_data, check_en_cn_summary,
    check_market_signals_cn, check_empty_category_tabs, check_keyword_filter,
    check_keyword_clustering, check_weekly_dashboard, check_xss_safe,
    check_no_bare_except, check_iso8601, check_module_size,
    check_constraints,
)


def check_model_profiles_accuracy(skill_dir: Path | None = None) -> dict:
    """P0-2 模型档案准确性守护：扫描 model_profiles.json，禁止「无真实来源锚点」条目。

    判定：source 以「榜单自动抓取」开头（项目内部约定：自动抓取、未联网核实）
    或 source 为空 / 缺失 → 视为未核实，应移入 model_profiles_unverified.json。

    这是一个数据治理硬守护，独立于 HTML 内容；找不到文件时降级为 warn（不阻断）。
    """
    if skill_dir is None:
        skill_dir = Path(__file__).resolve().parent.parent
    prof_path = skill_dir / "model_profiles.json"
    if not prof_path.exists():
        return {"ok": True, "warn": True,
                "msg": f"未找到 model_profiles.json（{prof_path}），跳过档案准确性校验"}
    try:
        data = json.loads(prof_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return {"ok": False, "warn": False, "msg": f"model_profiles.json 解析失败：{e}"}

    bad = []
    for name, v in data.items():
        src = (v or {}).get("source")
        if not src or not str(src).strip():
            bad.append((name, "source 缺失"))
        elif str(src).strip().startswith("榜单自动抓取"):
            bad.append((name, "source 未联网核实"))
    if bad:
        detail = "；".join(f"{n}（{r}）" for n, r in bad[:8])
        more = f" 等共 {len(bad)} 条" if len(bad) > 8 else ""
        return {"ok": False, "warn": False,
                "msg": f"存在 {len(bad)} 条无来源锚点的未核实模型档案：{detail}{more}"
                        f"——请运行 validate_models.py --fix 移入 unverified 文件"}
    return {"ok": True, "warn": False,
            "msg": f"模型档案全部已核实（{len(data)} 条，均带真实来源锚点）"}


def validate(html_path: Path, opts: dict = None) -> dict:
    opts = opts or {}
    min_news = opts.get("min_news", 20)
    min_cov = opts.get("min_cov", 80)
    min_ranking = opts.get("min_ranking", 5)
    strict = opts.get("strict", False)

    # P0#19 源码静态守护：独立于 HTML，先执行（即使 HTML 缺失也能跑）
    src_res = {}
    src_dir = opts.get("source_dir")
    if src_dir:
        src_res["source_no_bare_except"] = check_no_bare_except(src_dir)
        src_res["source_iso8601"] = check_iso8601(src_dir)
        src_res["source_module_size"] = check_module_size(src_dir)

    try:
        content = html_path.read_text(encoding="utf-8")
    except OSError as e:
        return {
            "format": "未知（HTML 缺失）",
            "file": {"ok": False, "warn": False, "msg": f"文件读取失败：{e}"},
            "sources": {"ok": False, "warn": False, "msg": "未读取 HTML，跳过来源校验"},
            **src_res,
            "summary": {"passed": 0, "total": 0, "warned": 0,
                        "score": "0/0", "ok": False},
        }

    fmt = _detect_format(content)

    file_check = check_file_exists(html_path)
    sources_check = check_data_sources(content)

    if fmt == 'v3':
        news_check = check_news_v3(content, min_news, min_cov)
        search_check = check_search_v3(content)
        charts_check = check_charts_v3(content)
        ranking_check = check_ranking_v3(content, min_ranking)
        lb_quality_check = check_leaderboard_quality(content)  # L0#4/L0#5
        editorial_check = check_editorial_c0(content)
        editorial_c1_check = check_editorial_c1(content)
        market_check = check_market_disclaimer(content)
        signals_check = check_market_signals(content)
        structure_check = check_market_structure(content)
        trend_evidence_check = check_trend_evidence(content)
        market_data_check = check_market_data(content)
        en_cn_check = check_en_cn_summary(content)
        signals_cn_check = check_market_signals_cn(content)
        empty_cat_check = check_empty_category_tabs(content)
        kw_filter_check = check_keyword_filter(content)
        kw_cluster_check = check_keyword_clustering(content)
        dashboard_check = check_weekly_dashboard(content)

        results = {
            "format": "v3.0 新闻网站",
            "file": file_check,
            "news": news_check,
            "search": search_check,
            "charts": charts_check,
            "ranking": ranking_check,
            "editorial": editorial_check,
            "editorial_c1": editorial_c1_check,
            "market": market_check,
            "signals": signals_check,
            "structure": structure_check,
            "trend_evidence": trend_evidence_check,
            "market_data": market_data_check,
            "en_cn_summary": en_cn_check,
            "signals_cn": signals_cn_check,
            "empty_category_tabs": empty_cat_check,
            "keyword_filter": kw_filter_check,
            "keyword_clustering": kw_cluster_check,
            "weekly_dashboard": dashboard_check,
            "lb_quality": lb_quality_check,
            "sources": sources_check,
        }
    else:
        news_check = check_news_v2(content)
        kpi_check = check_kpi_v2(content)
        charts_check = check_charts_v2(content)

        results = {
            "format": "v2.0 周报",
            "file": file_check,
            "news": news_check,
            "kpi": kpi_check,
            "charts": charts_check,
            "sources": sources_check,
        }

    # P0-2：模型档案准确性守护（数据治理硬门槛，独立于 HTML）
    results["model_profiles_accuracy"] = check_model_profiles_accuracy(
        Path(__file__).resolve().parent.parent)

    # P2-XSS：HTML 内容级 XSS 守护（H1/H2 防回归），独立于源码静态扫描
    results["xss_safe"] = check_xss_safe(content)

    # P0#19 源码静态守护结果并入（已在函数开头计算，独立于 HTML）
    results.update(src_res)

    # 计分：ok=硬门槛达标；warn=软警告(降级但可用)；strict 下 warn 也算不过
    check_items = [r for r in results.values()
                   if isinstance(r, dict) and isinstance(r.get("ok"), bool)]
    passed = sum(1 for r in check_items if r.get("ok") is True)
    warned = sum(1 for r in check_items if r.get("warn") is True)
    total = len(check_items)
    all_ok = (passed == total) and (not strict or warned == 0)
    results["summary"] = {
        "passed": passed, "total": total, "warned": warned,
        "score": f"{passed}/{total}",
        "ok": all_ok,
    }
    return results


def print_report(results: dict) -> None:
    print("=" * 55)
    print(f"📋 AI 新闻网站验证报告（{results['format']}）")
    print("=" * 55)

    fmt = results["format"]

    if "v3" in fmt:
        checks = [
            ("文件完整性", results.get("file", {})),
            ("新闻条目 + 来源链接", results.get("news", {})),
            ("搜索/筛选功能", results["search"]),
            ("市场图表", None),
            ("模型排行榜", results["ranking"]),
            ("排行榜质量+schema(L0#4/5)", results.get("lb_quality", {})),
            ("内容质量 C0", results.get("editorial", {})),
            ("内容质量 C1", results.get("editorial_c1", {})),
            ("市场数据署名(M0)", results.get("market", {})),
            ("本周市场信号(M1)", results.get("signals", {})),
            ("市场结构图(M2)", results.get("structure", {})),
            ("趋势洞察×本周(M2)", results.get("trend_evidence", {})),
            ("市场图表厚度(M3)", results.get("market_data", {})),
            ("英文报道中文总结", results.get("en_cn_summary", {})),
            ("市场信号中文注解(Fix2)", results.get("signals_cn", {})),
            ("空分类动态隐藏(C2)", results.get("empty_category_tabs", {})),
            ("关键词可筛选(C2)", results.get("keyword_filter", {})),
            ("关键词自动聚类(C2#7)", results.get("keyword_clustering", {})),
            ("本周数字看板(C2#8)", results.get("weekly_dashboard", {})),
            ("XSS 安全守护(P2)", results.get("xss_safe", {})),
            ("无裸except(P0#19)", results.get("source_no_bare_except", {})),
            ("ISO8601日期(P0#19)", results.get("source_iso8601", {})),
            ("模块体量(P0#4)", results.get("source_module_size", {})),
            ("模型档案准确性(P0-2)", results.get("model_profiles_accuracy", {})),
            ("硬约束审计(P2-1)", results.get("constraints", {})),
            ("数据来源", results.get("sources", {})),
        ]
    else:
        checks = [
            ("文件完整性", results.get("file", {})),
            ("KPI 数据", results.get("kpi", {})),
            ("新闻条目", results.get("news", {})),
            ("数据来源", results.get("sources", {})),
            ("图表数据", None),
        ]

    for name, r in checks:
        if name == "市场图表" or name == "图表数据":
            print(f"\n📊 {name}：")
            for d in results["charts"]["details"]:
                status = "✅" if d["ok"] else "❌"
                print(f"  {status} {d['id']}：{d['msg']}")
        elif r:
            if r.get("ok"):
                status = "✅"
            elif r.get("warn"):
                status = "⚠️"
            else:
                status = "❌"
            print(f"{status} {name}：{r.get('msg', '')}")

    print("\n" + "=" * 55)
    s = results["summary"]
    if s.get("warned"):
        print(f"⚠️ 警告项：{s['warned']} 项（非致命；加 --strict 可将其视为不通过）")
    print(f"总分：{s['score']}  {'✅ 全部通过' if s['ok'] else '❌ 需修复'}")
    print("=" * 55)


def main():
    parser = argparse.ArgumentParser(description="验证 AI 新闻网站 / 周报完整性")
    parser.add_argument("--html", required=True, help="HTML 文件路径")
    parser.add_argument("--output", default=None, help="JSON 输出路径")
    parser.add_argument("--min-news", type=int, default=20, help="新闻最少条数(默认 20)")
    parser.add_argument("--min-coverage", type=float, default=80, help="来源链接覆盖率下限(默认 80)")
    parser.add_argument("--min-ranking", type=int, default=5, help="每榜最少模型数(默认 5)")
    parser.add_argument("--strict", action="store_true", help="警告项也视为不通过")
    parser.add_argument("--source-dir", default=str(Path(__file__).resolve().parent),
                        help="源码目录（P0#19 静态守护扫描，默认本脚本所在 scripts/）")
    args = parser.parse_args()

    opts = {
        "min_news": args.min_news,
        "min_cov": args.min_coverage,
        "min_ranking": args.min_ranking,
        "strict": args.strict,
        "source_dir": args.source_dir,
    }
    html_path = Path(args.html)
    results = validate(html_path, opts)
    print_report(results)

    out_path = Path(args.output) if args.output else html_path.with_suffix(".validation.json")
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📝 验证报告已保存：{out_path}")

    sys.exit(0 if results["summary"]["ok"] else 1)


if __name__ == "__main__":
    main()
