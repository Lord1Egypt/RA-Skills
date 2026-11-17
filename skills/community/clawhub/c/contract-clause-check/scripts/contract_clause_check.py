import argparse, json, re, sys

MUST = ["违约", "争议", "管辖"]
RISKY = [
    ("最终解释权", "单方保留最终解释权条款，多被认定无效且显失公平"),
    ("自动续期", "含自动续期/自动续约，注意退出窗口与通知期"),
    ("永久保密", "永久保密义务需评估对等性与期限合理性"),
    ("放弃诉讼", "放弃诉权类条款效力存疑，请律师复核"),
]

def main():
    ap = argparse.ArgumentParser(description="contract-clause-check · 合同高危条款扫描（零依赖）")
    ap.add_argument("--text", required=True, help="合同文本（可粘贴要点）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    t = a.text
    problems, risky = [], []
    for k in MUST:
        if k not in t:
            problems.append("缺少必备条款关键词：" + k)
    for k, why in RISKY:
        if k in t:
            risky.append({"term": k, "why": why})
    penalty = re.search(r"违约金[^\d]{0,6}(\d{1,2}(?:\.\d+)?)\s*%", t)
    if penalty and float(penalty.group(1)) > 30:
        risky.append({"term": "违约金" + penalty.group(1) + "%", "why": "违约金超损失30%部分可能被法院调减（民法典585条）"})
    if a.json:
        print(json.dumps({"pass": not problems, "missing_must": problems, "risky": risky},
                         ensure_ascii=False, indent=2))
    else:
        print("必备条款：")
        for k in MUST:
            print(("  [x] " if k in t else "  [ ] ") + k)
        if risky:
            print("风险提示：")
            for r in risky:
                print("    - " + r["term"] + "：" + r["why"])
        print("  判定：" + ("PASS" if not problems else "FAIL 缺必备条款"))
        print("  免责：本工具为初筛，不构成法律意见，重要合同请律师复核。")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
