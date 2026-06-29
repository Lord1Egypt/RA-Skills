#!/usr/bin/env python3
"""
harness.py — 智能批改安全护栏 v1.0

核心功能：
  L1: 结构化输出格式校验 — evidence 字段不得为空
  L2: 证据回溯校验 — grep 原文确认问题真实存在
  L3: 文件版本校验 — doc/docx 并存时自动选正确版本

设计原则：宁可漏报，不可误报。
"""

import json, os, sys, re, argparse
from pathlib import Path
from datetime import datetime

# ============================================================
# L1: 结构化输出校验
# ============================================================

REQUIRED_FIELDS = ["file", "issue", "evidence", "confidence"]
VALID_CONFIDENCE = {"高", "中", "低", "⚠️待验证"}

def validate_issue(issue: dict, idx: int) -> list:
    """校验单条问题的格式完整性"""
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in issue:
            errors.append(f"#{idx}: 缺少字段 '{field}'")
        elif field == "confidence" and issue[field] not in VALID_CONFIDENCE:
            errors.append(f"#{idx}: 置信度 '{issue[field]}' 无效，应为 {VALID_CONFIDENCE}")
        elif field == "evidence" and (not issue[field] or len(str(issue[field]).strip()) < 5):
            errors.append(f"#{idx}: evidence 为空或过短（<5字符），拒绝")
        elif field == "file" and not issue[field]:
            errors.append(f"#{idx}: file 字段为空")
    return errors

# ============================================================
# L2: 证据回溯校验
# ============================================================

def verify_evidence(issue: dict, txt_dir: str) -> dict:
    """
    在提取的文本文件中搜索 evidence 字符串
    返回: {"verified": bool, "found_in": str, "match_preview": str}
    """
    evidence = issue.get("evidence", "")
    filename = issue.get("file", "")

    if not evidence or len(evidence.strip()) < 5:
        return {"verified": False, "found_in": "", "match_preview": "evidence过短"}

    # 在 /tmp/auto_grading/ 目录下搜索
    search_dir = txt_dir or "/tmp/auto_grading"
    if not os.path.isdir(search_dir):
        return {"verified": False, "found_in": "", "match_preview": f"目录不存在: {search_dir}"}

    # 精确匹配或模糊匹配（取证据的前30字符）
    query = evidence.strip()[:30]
    for txt_file in sorted(os.listdir(search_dir)):
        if not txt_file.endswith(".txt"):
            continue
        txt_path = os.path.join(search_dir, txt_file)
        try:
            with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # 先精确匹配
            idx = content.find(evidence.strip())
            if idx >= 0:
                preview = content[max(0, idx - 10):idx + len(evidence) + 30]
                return {"verified": True, "found_in": txt_file,
                        "match_preview": preview.replace('\n', ' ')[:80]}
            # 降级：模糊匹配前30字符
            idx = content.find(query)
            if idx >= 0:
                preview = content[max(0, idx - 10):idx + len(query) + 50]
                return {"verified": True, "found_in": txt_file,
                        "match_preview": preview.replace('\n', ' ')[:80] + " (模糊匹配)"}
        except Exception:
            continue

    return {"verified": False, "found_in": "未找到",
            "match_preview": f"在 {len(os.listdir(search_dir))} 个文件中均未匹配"}

# ============================================================
# L3: 文件版本校验
# ============================================================

def check_doc_versions(directory: str) -> dict:
    """
    检查同一文档是否存在 .doc 和 .docx 两个版本
    返回推荐使用的版本及理由
    """
    versions = {}
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.startswith("~$"):
                continue  # 跳过临时文件
            ext = Path(f).suffix.lower()
            if ext not in (".doc", ".docx"):
                continue
            stem = Path(f).stem  # 不含扩展名的文件名
            path = os.path.join(root, f)
            mtime = os.path.getmtime(path)
            size = os.path.getsize(path)

            if stem not in versions:
                versions[stem] = []
            versions[stem].append({"ext": ext, "path": path,
                                   "mtime": mtime, "size": size})

    conflicts = {}
    for stem, vlist in versions.items():
        if len(vlist) >= 2:
            # 有冲突，选择推荐版本
            docx = [v for v in vlist if v["ext"] == ".docx"]
            doc = [v for v in vlist if v["ext"] == ".doc"]

            if docx and doc:
                docx_newer = docx[0]["mtime"] > doc[0]["mtime"]
                docx_bigger = docx[0]["size"] > doc[0]["size"] * 1.5  # docx 比 doc 大 50% 以上 = 含多图/模板

                # 读取 docx 开头检测是否为模板
                is_template = False
                if docx:
                    try:
                        from docx import Document
                        d = Document(docx[0]["path"])
                        first_text = '\n'.join([p.text for p in list(d.paragraphs)[:20]])
                        template_signals = ["请更换", "此处写", "这里的格式", "请直接输入",
                                           "删除此句", "作品名字", "全小写"]
                        if any(s in first_text for s in template_signals):
                            is_template = True
                    except Exception:
                        pass

                if is_template:
                    recommended = doc[0]["path"]
                    reason = "docx为模板半成品(含占位符)，使用doc"
                elif docx_bigger and not docx_newer:
                    recommended = doc[0]["path"]
                    reason = "docx虽大但更旧，疑似未完成版本，使用doc"
                elif docx_newer:
                    recommended = docx[0]["path"]
                    reason = "docx更新且无模板嫌疑，使用docx"
                else:
                    recommended = docx[0]["path"]
                    reason = "默认使用docx"

                conflicts[stem] = {
                    "versions": vlist,
                    "recommended": recommended,
                    "reason": reason,
                    "is_template": is_template,
                }

    return conflicts

# ============================================================
# 综合校验入口
# ============================================================

def run_harness(issues_json_path: str, txt_dir: str = "/tmp/auto_grading",
                archive_dir: str = None) -> dict:
    """
    对审查输出的问题列表执行完整安全护栏校验

    Args:
        issues_json_path: 审查输出的JSON文件路径，格式：{"issues": [...]}
        txt_dir: 提取文本所在目录
        archive_dir: 原始存档目录（用于L3文件版本校验）

    Returns:
        {
            "total": int,           # 总问题数
            "passed": int,          # 通过数
            "failed": int,          # 未通过数
            "format_errors": [],    # L1格式错误
            "unverified": [],       # L2证据未验证
            "version_conflicts": {}, # L3文件版本冲突
            "clean_issues": [],     # 清洗后的问题列表（通过校验的）
        }
    """
    with open(issues_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    issues = data.get("issues", [])
    if not issues:
        # 尝试直接从数组中读取
        if isinstance(data, list):
            issues = data
        else:
            return {"total": 0, "passed": 0, "failed": 0, "error": "未找到issues字段"}

    result = {
        "total": len(issues),
        "passed": 0,
        "failed": 0,
        "format_errors": [],
        "unverified": [],
        "version_conflicts": {},
        "clean_issues": [],
        "harness_run_at": datetime.now().isoformat(),
    }

    # L3: 文件版本校验
    if archive_dir and os.path.isdir(archive_dir):
        result["version_conflicts"] = check_doc_versions(archive_dir)

    for i, issue in enumerate(issues):
        passed = True

        # L1: 格式校验
        fmt_errors = validate_issue(issue, i + 1)
        if fmt_errors:
            result["format_errors"].extend(fmt_errors)
            passed = False

        # L2: 证据回溯（仅对 confidence != "⚠️待验证" 的执行）
        if issue.get("confidence") != "⚠️待验证" and issue.get("evidence"):
            verify = verify_evidence(issue, txt_dir)
            issue["_harness_verify"] = verify
            if not verify["verified"] and issue.get("confidence") in ("高", "中"):
                # 高/中置信度的问题证据未找到 → 降级
                issue["confidence"] = "⚠️待验证"
                issue["_harness_note"] = f"证据未在文本中找到，自动降级"
                result["unverified"].append({
                    "index": i + 1,
                    "issue": issue["issue"],
                    "file": issue["file"],
                    "evidence_search": query(issue.get("evidence", ""), 30)
                })

        if passed:
            result["passed"] += 1
            result["clean_issues"].append(issue)
        else:
            result["failed"] += 1

    return result


def query(s, n): return s[:n] if s else ""

def main():
    parser = argparse.ArgumentParser(description="智能批改安全护栏")
    parser.add_argument("--input", required=True, help="审查输出JSON文件路径")
    parser.add_argument("--txt-dir", default="/tmp/auto_grading", help="提取文本目录")
    parser.add_argument("--archive-dir", help="原始存档目录（可选，用于L3）")
    parser.add_argument("--output", help="清洗后输出JSON路径")
    args = parser.parse_args()

    result = run_harness(args.input, args.txt_dir, args.archive_dir)

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result["clean_issues"], f, ensure_ascii=False, indent=2)
        print(f"\n清洗后输出: {args.output} ({len(result['clean_issues'])}/{result['total']} 条通过)")

    # 统计
    print(f"\n护栏报告: {result['total']}条问题 → {result['passed']}条通过, {result['failed']}条拒绝")
    if result["format_errors"]:
        print(f"  L1格式错误: {len(result['format_errors'])}条")
    if result["unverified"]:
        print(f"  L2证据未验证(已降级): {len(result['unverified'])}条")
    if result["version_conflicts"]:
        print(f"  L3文件版本冲突: {len(result['version_conflicts'])}处")

if __name__ == "__main__":
    main()
