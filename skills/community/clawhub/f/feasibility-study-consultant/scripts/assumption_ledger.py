#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""假设验证台账（Assumption Ledger）

项目论证里最值钱的一句话是："**我们赌的是什么、什么时候能验出来**"。
本工具把项目里的关键假设排成一张台账，按「影响 × 不确定性」排序，
让你先验最要命的假设，而不是先做最容易做的事。

用法：
    python3 assumption_ledger.py 假设台账.csv
    python3 assumption_ledger.py 假设台账.json --plan      # 追加"验证计划"输出
    python3 assumption_ledger.py 假设台账.csv --json
    python3 assumption_ledger.py --demo

输入（CSV 表头可中英混用，或用 JSON 数组；只需列：假设/影响/不确定性）：
    假设,类别,影响,不确定性,验证方法,证据等级,状态,负责人,截止
    3家头部客户签入驻意向,市场,5,4,上门访谈+意向书,B,unverified,张经理,2026-10-01
    拿地成本≤45万/亩,成本,5,2,查当地成交公告,A,verified,李工,-

字段说明：
    影响(impact)         1-5，这条假设不成立，对项目结论的杀伤力
    不确定性(uncertainty) 1-5，目前对它有多不确定
    状态(status)         unverified 未验证 / in_progress 验证中 / verified 已验证 / falsified 已证伪
    证据等级(evidence)    A 官方一手 / B 权威二手 / C 一般二手 / D 推断

退出码：
    0 = 台账健康（没有"高影响且未验证"的阻塞假设）
    1 = 存在阻塞假设（高影响 [≥4] 且未验证）——不应带着它下结论
    2 = 用法或数据错误

依赖：仅 Python 3 标准库。
"""
import csv
import json
import sys

STATUS_ALIAS = {
    "unverified": "unverified", "未验证": "unverified", "未": "unverified", "": "unverified",
    "in_progress": "in_progress", "验证中": "in_progress", "进行中": "in_progress",
    "verified": "verified", "已验证": "verified", "已验": "verified", "是": "verified",
    "falsified": "falsified", "已证伪": "falsified", "证伪": "falsified", "否": "falsified",
}
STATUS_LABEL = {
    "unverified": "未验证", "in_progress": "验证中",
    "verified": "已验证", "falsified": "已证伪",
}
KEYS = {
    "assumption": ["假设", "assumption", "前提", "结论依赖"],
    "category": ["类别", "category", "类型"],
    "impact": ["影响", "impact", "影响力"],
    "uncertainty": ["不确定性", "uncertainty", "不确定度"],
    "method": ["验证方法", "method", "怎么验"],
    "evidence": ["证据等级", "evidence", "证据"],
    "status": ["状态", "status"],
    "owner": ["负责人", "owner", "谁负责"],
    "due": ["截止", "due", "时间", "deadline"],
}


def _pick(row, aliases, default=""):
    for k in aliases:
        if k in row and row[k] not in (None, ""):
            return row[k]
    return default


def _norm_status(v):
    return STATUS_ALIAS.get(str(v).strip().lower(), STATUS_ALIAS.get(str(v).strip(), "unverified"))


def _i(v, default=3):
    try:
        n = int(float(str(v).strip()))
        return min(5, max(1, n))
    except (TypeError, ValueError):
        return default


def load(path):
    if path.lower().endswith(".json"):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = data.get("assumptions", [])
    else:
        with open(path, encoding="utf-8-sig", newline="") as f:
            data = list(csv.DictReader(f))
    out = []
    for r in data:
        a = str(_pick(r, KEYS["assumption"])).strip()
        if not a:
            continue
        item = {
            "假设": a,
            "类别": str(_pick(r, KEYS["category"], "未分类")).strip(),
            "影响": _i(_pick(r, KEYS["impact"], 3)),
            "不确定性": _i(_pick(r, KEYS["uncertainty"], 3)),
            "验证方法": str(_pick(r, KEYS["method"], "")).strip(),
            "证据等级": str(_pick(r, KEYS["evidence"], "D")).strip().upper()[:1] or "D",
            "状态": _norm_status(_pick(r, KEYS["status"], "unverified")),
            "负责人": str(_pick(r, KEYS["owner"], "")).strip(),
            "截止": str(_pick(r, KEYS["due"], "")).strip(),
        }
        item["优先级"] = item["影响"] * item["不确定性"]
        item["阻塞"] = item["影响"] >= 4 and item["状态"] not in ("verified", "falsified")
        out.append(item)
    return out


def analyze(items):
    items = sorted(items, key=lambda x: (x["阻塞"], x["优先级"]), reverse=True)
    blocked = [i for i in items if i["阻塞"]]
    falsified = [i for i in items if i["状态"] == "falsified"]
    verified = [i for i in items if i["状态"] == "verified"]
    stat = {}
    for i in items:
        stat[STATUS_LABEL[i["状态"]]] = stat.get(STATUS_LABEL[i["状态"]], 0) + 1
    # 建议动作
    for i in items:
        if i["状态"] == "falsified":
            i["建议"] = "停下：该假设不成立，重估项目前提（价值主张/成本结构/范围）"
        elif i["阻塞"]:
            i["建议"] = i["验证方法"] or "立即设计最小成本验证（访谈/试点/小样/查一手数据）"
        elif i["状态"] == "unverified" and i["优先级"] >= 12:
            i["建议"] = i["验证方法"] or "排入本轮验证（中优先级）"
        elif i["状态"] == "verified":
            i["建议"] = "已闭环，归档为论证依据"
        else:
            i["建议"] = "低优先级，可先做后验"
    return {"items": items, "blocked": blocked, "falsified": falsified,
            "verified": verified, "stat": stat}


def render(res, plan=False):
    L = ["=" * 72, "假设验证台账", "=" * 72, ""]
    L.append("概览：" + "，".join(f"{k} {v}" for k, v in res["stat"].items()))
    L.append("")
    L.append(f"{'假设':<34}{'影响':>4}{'不确定':>6}{'优先级':>7}{'状态':>7}{'证据':>5}")
    for i in res["items"]:
        name = i["假设"][:32] + ("…" if len(i["假设"]) > 32 else "")
        flag = "❗" if i["阻塞"] else ("✔" if i["状态"] == "verified" else " ")
        L.append(f"{flag}{name:<33}{i['影响']:>4}{i['不确定性']:>6}{i['优先级']:>7}"
                 f"{STATUS_LABEL[i['状态']]:>7}{i['证据等级']:>5}")
    L.append("")
    if res["falsified"]:
        L.append("❌ 已证伪（一票否决，先处理）：")
        for i in res["falsified"]:
            L.append(f"   · {i['假设']} → {i['建议']}")
        L.append("")
    if res["blocked"]:
        L.append("🚧 阻塞项（高影响 + 未验证）：带着它下结论＝赌博")
        for i in res["blocked"]:
            L.append(f"   · {i['假设']}（优先级 {i['优先级']}，建议：{i['建议']}）")
    else:
        L.append("✅ 无阻塞项：高影响假设均已验证或已证伪")
    L.append("")
    L.append("规则：先验「影响最大 × 最不确定」的那条 —— 而不是最容易验的那条。")
    L.append("     项目论证结论里必须写明：哪几条假设一旦不成立，结论就反转。")
    if plan:
        L.append("")
        L.append("-" * 72)
        L.append("验证计划（按优先级）")
        L.append("-" * 72)
        for n, i in enumerate([x for x in res["items"] if x["状态"] != "verified"], 1):
            L.append(f"{n}. [{i['状态']}] {i['假设']}")
            L.append(f"   方法：{i['验证方法'] or '待定'}｜证据目标：≥B｜"
                     f"负责人：{i['负责人'] or '待定'}｜截止：{i['截止'] or '待定'}")
            L.append("   判据：验到什么程度才算过？（建议写死阈值，如“3家意向书”而不是“客户有意向”）")
    return "\n".join(L)


DEMO = [
    {"假设": "3 家区域头部客户签订入驻意向（锁定 60% 库容）", "类别": "市场", "影响": 5, "不确定性": 4,
     "验证方法": "上门访谈 + 意向书", "证据等级": "B", "状态": "unverified", "负责人": "张经理", "截止": "2026-10-01"},
    {"假设": "拿地成本 ≤ 45 万元/亩", "类别": "成本", "影响": 5, "不确定性": 2,
     "验证方法": "查当地近一年成交公告 + 园区口头报价", "证据等级": "A", "状态": "verified", "负责人": "李工", "截止": "—"},
    {"假设": "用电按工业电价执行（非商业电价）", "类别": "成本", "影响": 4, "不确定性": 4,
     "验证方法": "供电局书面确认", "证据等级": "A", "状态": "unverified", "负责人": "李工", "截止": "2026-09-30"},
    {"假设": "满库率第 3 年达到 75%", "类别": "运营", "影响": 5, "不确定性": 5,
     "验证方法": "对标同城同类型园区实际出租率 + 与运营方访谈", "证据等级": "B", "状态": "in_progress", "负责人": "王总", "截止": "2026-10-15"},
    {"假设": "融资成本不高于 5%", "类别": "财务", "影响": 4, "不确定性": 3,
     "验证方法": "两家银行授信意向函", "证据等级": "A", "状态": "unverified", "负责人": "财务部", "截止": "2026-10-20"},
    {"假设": "周边无新增同质园区（3 年内）", "类别": "竞争", "影响": 4, "不确定性": 3,
     "验证方法": "查国土空间规划 + 发改备案库", "证据等级": "A", "状态": "falsified", "负责人": "张经理", "截止": "—"},
]


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    if "--demo" in flags or not args:
        items = load_dicts(DEMO)
    else:
        try:
            items = load(args[0])
        except Exception as e:  # noqa: BLE001
            print(f"读取台账失败：{e}", file=sys.stderr)
            return 2
    if not items:
        print("台账为空：至少需要一条假设（列：假设,影响,不确定性,...）", file=sys.stderr)
        return 2
    res = analyze(items)
    if "--json" in flags:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res, plan="--plan" in flags))
    return 1 if res["blocked"] or res["falsified"] else 0


def load_dicts(data):
    """直接把 list[dict] 走同一条解析路径（供 --demo 用）"""
    import tempfile, os
    fd, p = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    try:
        return load(p)
    finally:
        os.unlink(p)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
