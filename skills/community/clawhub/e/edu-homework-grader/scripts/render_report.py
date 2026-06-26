"""Render grading result as a student/teacher report."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def render(result: dict, flavor: str) -> str:
    lines = []
    if flavor == "student":
        lines.append(f"# 你的批改报告 / Your grading report")
        lines.append(f"**总分**: {result['score']} / {result['max_score']} ({result['percentage']}%)")
        lines.append("")
        for it in result["items"]:
            mark = "✅" if it.get("correct") else "✏️"
            lines.append(f"## {mark} {it['item_id']}  得分 {it['earned']}/{it['max']}")
            lines.append(f"> {it.get('feedback','')}")
            lines.append("")
    elif flavor == "teacher":
        lines.append(f"# 教师批阅汇总")
        lines.append(f"- 学生: {result.get('student','?')}")
        lines.append(f"- 总分: {result['score']}/{result['max_score']}")
        wrong = [i for i in result["items"] if i.get("earned",0) < i.get("max",0)]
        lines.append(f"- 失分题目数: {len(wrong)}")
        for it in wrong:
            lines.append(f"  - {it['item_id']}: {it.get('feedback','')}")
    return "\n".join(lines)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--grading-result", required=True)
    ap.add_argument("--format", choices=["student","teacher","class"], default="student")
    args = ap.parse_args()
    r = json.loads(Path(args.grading_result).read_text(encoding="utf-8"))
    print(render(r, args.format))
