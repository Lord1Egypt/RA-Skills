#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 临床评价路径选择器（零依赖 / 确定性判定树 / JSON IR / 修复回执）
# 规则依据：NMPA 2021年第73号通告体系 + EU MDCG 2020-6 / MDR Art.61。输出为导航建议，以官方最新为准。
import argparse, json, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def route_nmpa(a, warns):
    cls = a.nmpa_class
    if cls == "I":
        route = "无需临床评价（临床评价资料豁免路径）"
        basis = ["《医疗器械注册与备案管理办法》（国家市场监督管理总局令第47号）",
                 "国家药监局 2021 年第 73 号通告及其配套指南"]
        evidence = ["证明产品安全性、有效性的其他研究资料",
                    "与免临床评价情形的符合性说明"]
        if a.implant == "yes":
            warns.append("输入为 I 类+植入：常见植入器械多为 II/III 类，请复核分类判定依据。")
        return {"market": "NMPA", "route": route, "basis": basis, "evidence": evidence, "notes": warns}
    if a.in_catalog == "yes":
        route = "免临床评价路径（列入《免于临床评价医疗器械目录》）"
        evidence = ["与目录条文的对比说明（适用范围/结构组成/性能指标逐项）",
                    "与同品种医疗器械的对比资料",
                    "目录对比不符项的评价资料"]
        basis = ["国家药监局 2021 年第 73 号通告",
                 "《免于临床评价医疗器械目录》（最新版）"]
        if a.eq_data == "yes":
            warns.append("同时具备同品种临床数据：目录路径优先，等同路径可作备选。")
        return {"market": "NMPA", "route": route, "basis": basis, "evidence": evidence, "notes": warns}
    if a.eq_data == "yes":
        route = "同品种临床评价路径"
        evidence = ["同品种器械的临床数据（文献/数据库/上市后数据）",
                    "差异部分的科学证据与验证资料",
                    "等同性论证对比表（适用范围/技术特征/生物学特性）"]
        basis = ["国家药监局 2021 年第 73 号通告",
                 "《医疗器械临床评价等同性论证技术指导原则》",
                 "《医疗器械同品种临床评价注册审查指导原则》"]
        return {"market": "NMPA", "route": route, "basis": basis, "evidence": evidence, "notes": warns}
    route = "临床试验路径（或先评估能否补充证据转入同品种路径）"
    evidence = ["临床试验方案与伦理审查文件",
                "临床试验机构备案（械临备）",
                "若为创新器械：考虑创新审查通道（绿色通道）"]
    basis = ["国家药监局 2021 年第 73 号通告",
             "《医疗器械临床试验质量管理规范》（GCP）"]
    if a.novel == "yes":
        route = "临床试验路径（新型器械，通常无同品种可用）"
    return {"market": "NMPA", "route": route, "basis": basis, "evidence": evidence, "notes": warns}


def route_eu(a, warns):
    cls = a.eu_class
    if a.wet == "yes":
        if cls == "III" or a.implant == "yes":
            warns.append("WET 名单路径一般不适用于 III 类/植入器械，请复核 MDCG 2020-6 适用条件。")
        route = "文献路径（Well-Established Technology, WET）"
        basis = ["MDCG 2020-6（Regulation (EU) 2017/745 项下充分成熟技术的临床证据要求）",
                 "MDR Annex XIV Part A"]
        evidence = ["WET 名单符合性说明",
                    "文献检索方案与报告（PRISMA 建议引用）",
                    "等同器械证据（如使用）"]
        return {"market": "EU MDR", "route": route, "basis": basis, "evidence": evidence, "notes": warns}
    if cls == "III" or a.implant == "yes":
        route = "临床调查为主路径（MDR Art.61(1)）"
        basis = ["MDR Art.61 / Annex XV", "MDCG 2020-6", "MEDDEV 2.7/1 rev 4（方法学参考）"]
        evidence = ["临床调查方案与伦理批件", "安全性随访计划", "等同器械路径仅在严格等同条件下可替代"]
        return {"market": "EU MDR", "route": route, "basis": basis, "evidence": evidence, "notes": warns}
    if cls == "I":
        route = "临床评价仍需开展，通常无需临床调查（Class I）"
        basis = ["MDR Art.61(10)", "MDCG 2020-6", "MDCG 2020-7 PMCF 计划模板"]
        evidence = ["文献综述与状态评价（SOTA）", "上市后监督（PMS）计划", "性能与安全参数符合性证据"]
        return {"market": "EU MDR", "route": route, "basis": basis, "evidence": evidence, "notes": warns}
    route = "文献/同品种证据组合路径（视证据充分性，必要时补充临床调查）"
    basis = ["MDCG 2020-6", "MEDDEV 2.7/1 rev 4（方法学参考）", "MDR Annex XIV"]
    evidence = ["等同器械 Technical File 可及性确认", "文献检索与评价报告", "差距分析（gap analysis）"]
    if a.ai_samd == "yes":
        warns.append("MDCG 2019-11：诊断类 SaMD 按 Rule 11 常落入 III 类，请先完成分类确认。")
    return {"market": "EU MDR", "route": route, "basis": basis, "evidence": evidence, "notes": warns}


def main():
    ap = argparse.ArgumentParser(prog="clin_eval_route_picker", description="临床评价路径确定性选择器（NMPA/EU MDR）")
    ap.add_argument("--market", choices=["nmpa", "eu", "both"], default="nmpa")
    ap.add_argument("--nmpa-class", choices=["I", "II", "III", "unknown"], default="unknown")
    ap.add_argument("--eu-class", choices=["I", "IIa", "IIb", "III", "unknown"], default="unknown")
    ap.add_argument("--in-catalog", choices=["yes", "no", "unknown"], default="unknown", help="是否列入免临床目录")
    ap.add_argument("--eq-data", choices=["yes", "no", "unknown"], default="unknown", help="有无同品种临床数据")
    ap.add_argument("--novel", choices=["yes", "no"], default="no", help="是否新型器械")
    ap.add_argument("--implant", choices=["yes", "no"], default="no")
    ap.add_argument("--ai-samd", choices=["yes", "no"], default="no")
    ap.add_argument("--wet", choices=["yes", "no", "unknown"], default="unknown", help="EU：是否属成熟技术 WET")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    errors = []
    need_nmpa = a.market in ("nmpa", "both")
    need_eu = a.market in ("eu", "both")
    if need_nmpa and a.nmpa_class == "unknown":
        errors.append(("CE_E_MISSING", "--nmpa-class", "market 含 nmpa 但未给分类", "补 --nmpa-class I/II/III"))
    if need_nmpa and a.nmpa_class != "I" and a.in_catalog == "unknown":
        errors.append(("CE_E_MISSING", "--in-catalog", "未给免临床目录状态", "补 yes/no"))
    if need_nmpa and a.nmpa_class != "I" and a.in_catalog == "no" and a.eq_data == "unknown":
        errors.append(("CE_E_MISSING", "--eq-data", "目录外产品需同品种数据状态", "补 yes/no"))
    if need_eu and a.eu_class == "unknown":
        errors.append(("CE_E_MISSING", "--eu-class", "market 含 eu 但未给分类", "补 --eu-class"))
    if a.novel == "yes" and a.eq_data == "yes":
        errors.append(("CE_E_CONFLICT", "--novel/--eq-data", "新型器械通常无同品种数据，两者同 yes 自相矛盾", "核对证据现状"))
    if a.wet == "yes" and (a.eu_class == "III" or a.implant == "yes"):
        errors.append(("CE_E_CONFLICT", "--wet", "WET 与 III 类/植入通常互斥", "复核 MDCG 2020-6"))
    if errors:
        if a.json:
            print(json.dumps({"routes": None, "errors": [
                {"code": c, "subject": s, "evidence": e, "fixes": [f]} for c, s, e, f in errors]},
                ensure_ascii=False, indent=2))
        else:
            for c, s, e, f in errors:
                print("[%s] %s: %s -> %s" % (c, s, e, f))
        sys.exit(1)
    warns = []
    routes = []
    if need_nmpa:
        r = route_nmpa(a, warns)
        r.setdefault("notes", [])
        r["notes"].append("AI 辅助诊断软件：参照《人工智能医用软件产品分类界定指导原则》，常按第三类管理，路径选择趋严。")
        r["notes"].append("以上为按现行规则文本的确定性推荐，目录与通告会更新，以官方最新为准；注册策略请由注册人员确认。")
        routes.append(r)
    if need_eu:
        r = route_eu(a, warns)
        r.setdefault("notes", [])
        r["notes"].append("MDCG 文件会持续更新，以欧盟委员会最新版本为准；本输出不构成法规意见。")
        routes.append(r)
    if a.json:
        print(json.dumps({"routes": routes}, ensure_ascii=False, indent=2))
    else:
        for r in routes:
            print("== %s ==" % r["market"])
            print("推荐路径：%s" % r["route"])
            for b in r["basis"]:
                print("  依据：%s" % b)
            for e in r["evidence"]:
                print("  需提交：%s" % e)
            for n in r["notes"]:
                print("  提示：%s" % n)
    sys.exit(0)


if __name__ == "__main__":
    main()
