#!/usr/bin/env python3
"""G1-G8 硬门禁的机械校验器（harness 层强制，非 prompt 层声明）。

用途：对一份 destination-architect 的输出文本逐门禁扫描，输出 PASS/FAIL。
可在 CI 或本地调用，把"机械可校验"从承诺变为事实。

用法：
    python3 scripts/check_gates.py <output.md>
    python3 scripts/check_gates.py -              # 从 stdin 读取
    python3 scripts/check_gates.py <output.md> --json
    python3 scripts/check_gates.py --selftest     # 运行内置自测

退出码：0 = 全部 PASS；1 = 至少一门禁 FAIL。
"""
import json
import re
import sys

EVIDENCE_LABELS = ("实测", "引用", "假设", "未知")
# 裸数字：数字 + 常见量纲（无证据标签同行即为违规）
BARE_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?\s*(?:万|亿|%|％|元|人|年|晚|间|次)")

# 套话黑名单（与 core/information-discipline.md 保持一致）
BANNED = (
    "打造国际一流", "国内领先", "世界级",
    "赋能文旅融合", "赋能一切",
    "提升影响力", "扩大知名度",
    "推动高质量发展", "高质量发展",
    "打造 IP 矩阵", "矩阵式布局",
    "构建生态闭环", "生态化运营",
    "全面铺开", "全方位覆盖",
)

# 策划案四大落地要件：{要件名: (标题关键词,...)}
PROPOSAL_REQUISITES = {
    "实施路线图": ("实施",),
    "财务测算模型": ("财务",),
    "运营组织 / 合规": ("组织", "合规"),
    "空间 / 招商产品": ("招商", "空间"),
}


def _read(argv):
    if len(argv) < 2:
        return None
    path = argv[1]
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _sections(text):
    """返回 [(heading, body)]，按 markdown 标题切分。"""
    parts, cur, buf = [], None, []
    for line in text.splitlines():
        if line.startswith("#"):
            if cur is not None:
                parts.append((cur, "\n".join(buf)))
            cur, buf = line.lstrip("#").strip(), []
        else:
            buf.append(line)
    if cur is not None:
        parts.append((cur, "\n".join(buf)))
    return parts


def _table_rows(body):
    """提取表格数据行（排除表头与分隔行），保留单元格内容为列表。"""
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):  # 分隔行
            continue
        rows.append(cells)
    return rows[1:] if rows else []  # 去掉表头行


def _has_content_row(rows):
    return any(any(len(c) >= 2 for c in row) for row in rows)


def check_g1(text):
    ok = ("【一页结论】" in text) or ("一页结论" in text)
    return ok, "含『一页结论』前置区块" if ok else "缺少『一页结论』前置区块"


def check_g2(text):
    viol = []
    for i, line in enumerate(text.splitlines(), 1):
        if any(lb in line for lb in EVIDENCE_LABELS) or "无可比数据" in line:
            continue
        for m in BARE_NUMBER.finditer(line):
            viol.append(f"L{i}: {m.group(0)}")
    if viol:
        return False, f"{len(viol)} 处裸数字，例：{'; '.join(viol[:3])}"
    return True, "所有量化陈述均带证据标签"


def check_g3(text):
    for head, body in _sections(text):
        if "信息缺口" in head:
            if _has_content_row(_table_rows(body)):
                return True, "信息缺口清单非空"
            return False, "信息缺口清单为空（= 假装知道）"
    return False, "缺少『信息缺口清单』"


def check_g4(text):
    for head, body in _sections(text):
        if "预测登记" in head:
            rows = _table_rows(body)
            if _has_content_row(rows) and ("锁定时点" in body or "锁定" in body):
                return True, "预测已登记且标明锁定时点"
            return False, "预测登记表为空或缺『锁定时点』"
    return False, "缺少『预测登记』"


def check_g5(text):
    if "证伪" not in text:
        return False, "缺少最小成本证伪实验"
    has_threshold = ("阈值" in text) or ("锁定" in text)
    has_cost = ("成本" in text) and ("周期" in text)
    if has_threshold and has_cost:
        return True, "含最小成本证伪实验（阈值/成本/周期）"
    return False, "证伪实验缺少阈值或成本/周期"


def check_g6(text):
    verdicts = ("值得做", "谨慎做", "不建议做", "值得投", "谨慎投", "不建议投")
    hit = [v for v in verdicts if v in text]
    if hit:
        return True, f"综合判断明确：{hit[0]}"
    return False, "综合判断缺失或模棱两可"


def check_g7(text):
    if "策划案" not in text:
        return True, "非策划案输出，G7 不适用"
    heads = [h for h, _ in _sections(text)]
    missing = []
    for name, keys in PROPOSAL_REQUISITES.items():
        if not any(any(k in h for k in keys) for h in heads):
            missing.append(name)
    if missing:
        return False, "策划案缺少落地要件：" + "、".join(missing)
    return True, "落地四大要件齐备（实施 / 财务 / 组织合规 / 空间招商）"


def check_g8(text):
    hit = [b for b in BANNED if b in text]
    if hit:
        return False, f"命中套话黑名单：{hit[0]}"
    return True, "未命中套话黑名单"


GATES = [
    ("G1", "一页结论前置", check_g1),
    ("G2", "量化陈述带证据标签", check_g2),
    ("G3", "信息缺口清单非空", check_g3),
    ("G4", "预测登记（含锁定时点）", check_g4),
    ("G5", "至少一个最小成本证伪实验", check_g5),
    ("G6", "综合判断明确", check_g6),
    ("G7", "策划案落地要件齐备", check_g7),
    ("G8", "反套话（黑名单未命中）", check_g8),
]


def run(text):
    results = []
    for gid, name, fn in GATES:
        ok, detail = fn(text)
        results.append({"id": gid, "name": name, "status": "pass" if ok else "fail", "detail": detail})
    return results


SELFTEST_PASS = """
## 【一页结论】
### 结论
**谨慎做**
### 必须先验证的假设
| 假设 | 证伪方式 | 成本 | 周期 | 阈值（事前锁定） |
|------|---------|------|------|----------------|
| 愿付 ≥800 元 | 定金测试 | 0.5 万 `[假设]` | 2 周 | 20% |
## 【信息缺口清单】
| 缺失信息 | 影响判断 | 获取方式 |
|---------|---------|---------|
| 真实客流 | 商业假设 | 试运营 |
## 【预测登记】
| 预测 | 置信度 | 锁定时点 |
|------|--------|---------|
| 复购率 > 20% `[假设]` | 中 | 2026-12-31 |
"""

SELFTEST_FAIL = """
预计年客流 3 万人，客单价 1000 元。本项目将打造国际一流文旅目的地。
"""

SELFTEST_PROPOSAL = """
# 某项目策划案
## 一页结论
**谨慎做**
## 项目理解
只有实施路线图，缺财务、组织合规、空间招商要件。
"""


def main(argv):
    if "--selftest" in argv:
        p = run(SELFTEST_PASS)
        f = run(SELFTEST_FAIL)
        pp = run(SELFTEST_PROPOSAL)
        ok = (all(r["status"] == "pass" for r in p)
              and any(r["status"] == "fail" for r in f)
              and any(r["status"] == "fail" for r in pp))
        print("[selftest]", "OK" if ok else "BROKEN")
        for r in p + f + pp:
            print(f"  {r['id']} {r['status']:4} {r['detail']}")
        return 0 if ok else 1

    text = _read(argv)
    if text is None:
        print(__doc__)
        return 2
    results = run(text)
    failed = [r for r in results if r["status"] == "fail"]

    if "--json" in argv:
        print(json.dumps({"gates": results, "failed": len(failed),
                          "verdict": "pass" if not failed else "fail"},
                         ensure_ascii=False, indent=2))
    else:
        print("=== G1-G8 硬门禁校验 ===")
        for r in results:
            mark = "PASS" if r["status"] == "pass" else "FAIL"
            print(f"[{mark}] {r['id']} {r['name']} — {r['detail']}")
        print(f"结论：{'全部通过' if not failed else str(len(failed)) + ' 项未通过'}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))