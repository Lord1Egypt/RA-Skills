"""Tier 1+2 校验生成内容。

Tier 1:
- 占位符全部填充（每个 placeholder_id 都有对应内容）
- 无占位符原文泄漏（生成内容不含 original_text 中的提示性文字）
- 字数在 [min_words, max_words] 区间内

Tier 2:
- required_keywords 全部存在
- 结构硬约束满足（表格 cell 内容不超长，避免破坏布局）
- 数据单元格值类型与 expected_value_type / header_text 语义匹配（防错列）
"""

import argparse
import json
import re
import sys
from pathlib import Path


def _count_words(text: str) -> int:
    """统计字数：中文按字符计，英文单词与数字串各按 1 计。"""
    if not text:
        return 0
    cn_chars = len(re.findall(r"[\u4e00-\u9fa5]", text))
    alnum_tokens = len(re.findall(r"[a-zA-Z0-9]+", text))
    return cn_chars + alnum_tokens


def _check_original_leak(text: str, original_text: str) -> bool:
    """检查生成内容是否泄漏了模板原文的提示性文字。"""
    if not original_text or not text:
        return False
    # 提取原文中的提示性短语
    markers = ["请填写", "本部分", "依据", "此处", "填写", "需要", "本节", "本部分需"]
    for marker in markers:
        if marker in original_text and marker in text:
            # 生成内容中如果直接出现"请填写"等指令词，视为泄漏
            if marker in ["请填写", "此处", "本部分需", "本节"]:
                return True
    return False


# === Tier 2: 数据单元格值类型语义校验 ===

def _check_value_type(text: str, expected_value_type: str, header_text: str = "") -> tuple:
    """校验短数据单元格内容是否与期望值类型语义匹配。

    返回: (ok: bool, hint: str|None)
    仅对短文本（<= 50 字符）做强校验，长文本（如简介）跳过避免误伤。
    """
    if not text or not text.strip():
        return True, None
    if len(text) > 50:
        # 长文本多为描述性内容，不适用类型校验
        return True, None

    vt = (expected_value_type or "").strip()
    header = (header_text or "").strip()

    # 优先按 expected_value_type 校验
    if vt:
        if vt.startswith("enum:"):
            allowed = [v.strip() for v in vt[5:].split(",") if v.strip()]
            if text.strip() not in allowed:
                return False, f"内容 '{text}' 不在允许枚举 {allowed} 内（依据 expected_value_type）"
            return True, None
        if vt.startswith("int:"):
            range_part = vt[4:]
            m = re.fullmatch(r"\s*(\d+)\s*-\s*(\d+)\s*", range_part)
            if m:
                lo, hi = int(m.group(1)), int(m.group(2))
                if not re.fullmatch(r"\d+", text.strip()):
                    return False, f"内容 '{text}' 不是整数（期望 int:{lo}-{hi}）"
                val = int(text.strip())
                if val < lo or val > hi:
                    return False, f"内容 '{text}' 超出范围 [{lo}, {hi}]"
                return True, None
            # 无范围的 int
            if not re.fullmatch(r"\d+", text.strip()):
                return False, f"内容 '{text}' 不是整数（期望 int）"
            return True, None
        if vt == "money":
            # 允许纯数字、带"万"、"元"、"," 等
            cleaned = re.sub(r"[,，]", "", text.strip())
            if not re.fullmatch(r"\d+(\.\d+)?(万元?|元)?", cleaned):
                return False, f"内容 '{text}' 不是合法金额格式（期望 money）"
            return True, None
        if vt == "date":
            # 常见日期格式：2024-03 / 2024年3月 / 2024/03/01 / 2024.03.01
            date_patterns = [
                r"\d{4}[-/.年]\d{1,2}[-/.月]?(\d{1,2}日?)?",
                r"\d{1,2}[-/.]\d{1,2}[-/.]\d{4}",
            ]
            if not any(re.fullmatch(p, text.strip()) for p in date_patterns):
                return False, f"内容 '{text}' 不是合法日期格式（期望 date）"
            return True, None
        if vt == "email":
            if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text.strip()):
                return False, f"内容 '{text}' 不是合法邮箱格式（期望 email）"
            return True, None
        if vt == "phone":
            if not re.fullmatch(r"\+?\d{3,4}[-\s]?\d{7,8}|\+?\d{11}", text.strip()):
                return False, f"内容 '{text}' 不是合法电话格式（期望 phone）"
            return True, None
        if vt == "id":
            if not re.fullmatch(r"[A-Za-z0-9\-_]+", text.strip()):
                return False, f"内容 '{text}' 不是合法编号格式（期望 id）"
            return True, None
        if vt == "text":
            return True, None

    # 兜底：若 expected_value_type 缺失但有 header_text，按表头关键词推断
    if header:
        # 性别
        if "性别" in header:
            if text.strip() not in {"男", "女", "M", "F", "male", "female", "Male", "Female"}:
                return False, f"表头 '{header}' 期望性别值（男/女），实际 '{text}'"
            return True, None
        # 年龄
        if "年龄" in header or "岁数" in header:
            if not re.fullmatch(r"\d{1,3}", text.strip()):
                return False, f"表头 '{header}' 期望年龄数字，实际 '{text}'"
            val = int(text.strip())
            if val < 0 or val > 150:
                return False, f"表头 '{header}' 年龄 {val} 超出合理范围 [0, 150]"
            return True, None
        # 金额
        if any(k in header for k in ["金额", "经费", "预算", "费用", "价格"]):
            cleaned = re.sub(r"[,，]", "", text.strip())
            if not re.fullmatch(r"\d+(\.\d+)?(万元?|元)?", cleaned):
                return False, f"表头 '{header}' 期望金额，实际 '{text}'"
            return True, None
        # 日期
        if any(k in header for k in ["日期", "时间", "出生", "开始", "结束"]):
            date_patterns = [
                r"\d{4}[-/.年]\d{1,2}[-/.月]?(\d{1,2}日?)?",
                r"\d{1,2}[-/.]\d{1,2}[-/.]\d{4}",
            ]
            if not any(re.fullmatch(p, text.strip()) for p in date_patterns):
                return False, f"表头 '{header}' 期望日期，实际 '{text}'"
            return True, None
        # 邮箱
        if any(k in header for k in ["邮箱", "电子邮件", "Email", "email"]):
            if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text.strip()):
                return False, f"表头 '{header}' 期望邮箱，实际 '{text}'"
            return True, None
        # 电话
        if any(k in header for k in ["电话", "手机", "联系方式"]):
            if not re.fullmatch(r"\+?\d{3,4}[-\s]?\d{7,8}|\+?\d{11}", text.strip()):
                return False, f"表头 '{header}' 期望电话，实际 '{text}'"
            return True, None

    return True, None


def validate_content(content: dict, contract: dict) -> dict:
    failed_checks = []
    tier_failed = None

    contents_list = content.get("contents", [])
    content_map = {c["placeholder_id"]: c.get("text", "") for c in contents_list}

    placeholders = contract.get("placeholders", [])

    # === Tier 1: 结构完整性 ===
    for p in placeholders:
        pid = p.get("id")
        if pid not in content_map:
            failed_checks.append({
                "check": f"placeholder_{pid}_empty",
                "fix_hint": f"占位符 {pid} 未填充",
            })
            if tier_failed is None:
                tier_failed = 1
            continue

        text = content_map[pid]
        if not text.strip():
            failed_checks.append({
                "check": f"placeholder_{pid}_empty",
                "fix_hint": f"占位符 {pid} 内容为空",
            })
            if tier_failed is None:
                tier_failed = 1
            continue

        # 字数校验
        min_w = p.get("min_words")
        max_w = p.get("max_words")
        word_count = _count_words(text)
        if min_w is not None and word_count < min_w:
            failed_checks.append({
                "check": f"placeholder_{pid}_too_short",
                "fix_hint": f"占位符 {pid} 字数 {word_count} < 最小 {min_w}",
            })
            if tier_failed is None:
                tier_failed = 1
        if max_w is not None and word_count > max_w:
            failed_checks.append({
                "check": f"placeholder_{pid}_too_long",
                "fix_hint": f"占位符 {pid} 字数 {word_count} > 最大 {max_w}",
            })
            if tier_failed is None:
                tier_failed = 1

        # 原文泄漏检查
        original = p.get("original_text", "")
        if _check_original_leak(text, original):
            failed_checks.append({
                "check": f"placeholder_{pid}_original_leak",
                "fix_hint": f"占位符 {pid} 内容含模板原文提示性文字，需删除",
            })
            if tier_failed is None:
                tier_failed = 1

    # === Tier 2: 约束满足 ===
    if tier_failed is None:
        for p in placeholders:
            pid = p.get("id")
            text = content_map.get(pid, "")

            required_kws = p.get("required_keywords", [])
            missing_kws = [kw for kw in required_kws if kw not in text]
            if missing_kws:
                failed_checks.append({
                    "check": f"placeholder_{pid}_missing_keywords",
                    "fix_hint": f"占位符 {pid} 缺少关键词: {missing_kws}",
                })
                if tier_failed is None:
                    tier_failed = 2

            # 数据单元格值类型语义校验（防错列）
            if p.get("type") == "table_cell":
                evt = p.get("expected_value_type", "")
                header = p.get("header_text", "")
                if evt or header:
                    ok, hint = _check_value_type(text, evt, header)
                    if not ok:
                        failed_checks.append({
                            "check": f"placeholder_{pid}_value_type_mismatch",
                            "fix_hint": f"占位符 {pid}（表头 '{header}'）内容疑似错列：{hint}",
                        })
                        if tier_failed is None:
                            tier_failed = 2

    return {
        "passed": len(failed_checks) == 0,
        "tier_failed": tier_failed,
        "failed_checks": failed_checks,
    }


def main():
    parser = argparse.ArgumentParser(description="Tier 1+2 校验生成内容")
    parser.add_argument("--content", required=True, help="generated_content.json 路径")
    parser.add_argument("--contract", required=True, help="fill_contract.json 路径")
    args = parser.parse_args()

    content = json.loads(Path(args.content).read_text(encoding="utf-8"))
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))

    result = validate_content(content, contract)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
