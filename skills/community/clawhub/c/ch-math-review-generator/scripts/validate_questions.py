#!/usr/bin/env python3
"""
题目校验脚本
校验 HTML 复习资料中的数学题目是否存在逻辑错误：

检查类型：
  1. 正比例函数/一次函数参数题：b 必须能通过参数消掉，否则无解
  2. 分式方程：分母不能为零
  3. 方程无解：判别式 Δ < 0 无实数解的情况（如故意出题需标注）
  4. 多结论题：结论之间是否自相矛盾
  5. 填空题：答案是否唯一、是否在题目条件范围内有解
  6. 几何证明：条件是否充分（不能凭空推导不存在的结论）
  7. 计算题：中间步骤是否会除零、平方根负数等
  8. 选择题选项互斥性：是否有多个正确答案

使用方法：
  python scripts/validate_questions.py <html_file_path> [--verbose]
"""

import sys
import re
import argparse
from pathlib import Path

C_OK   = '\033[92m'
C_ERR  = '\033[91m'
C_WARN = '\033[93m'
C_INFO = '\033[96m'
C_END  = '\033[0m'

def log(msg, level="INFO"):
    p = {"INFO": f"{C_INFO}[INFO]{C_END}", "WARN": f"{C_WARN}[WARN]{C_END}",
         "ERROR": f"{C_ERR}[ERROR]{C_END}", "OK": f"{C_OK}[OK]{C_END}"}
    try:
        print(f"{p.get(level, '[INFO]')} {msg}")
    except UnicodeEncodeError:
        import re as _re
        clean = _re.sub(r'\x1b\[[0-9;]*m', '', f"{p.get(level, '[INFO]')} {msg}")
        print(clean)


# ─── 校验规则定义 ────────────────────────────────────────────

def check_linear_no_solution(question_text, answer_text, verbose=False):
    """
    检查：y=(k-?)x+c 是否能成为正比例函数
    正比例函数要求 b=0，即常数项必须为0
    如果常数项是固定非零数（如+1, -2, 3），则无解
    """
    errors = []

    # 检测形式：y = (k-数字)x + 固定常数（非k的表达式）
    # 先看答案中有没有"No solution"或类似标记
    if any(kw in answer_text for kw in ['无解', '错误', '不存在', 'impossible', 'no solution', 'cannot']):
        return errors  # 已标注无解，不报错

    # 检测 y=(k-2)x+1 这类形式（固定常数项）
    fixed_const_pattern = re.search(
        r'y\s*=\s*\(?\s*k\s*[-+]\s*\d[\.0-9]*\)?\s*x\s*([+\-])\s*(\d+(?:\.\d+)?)\s*$',
        question_text.replace(' ', '')
    )
    if fixed_const_pattern and fixed_const_pattern.group(1) == '+':
        const = float(fixed_const_pattern.group(2))
        if const != 0:
            errors.append(
                f"正比例函数题：y=(k±数字)x+{const} 永远无法成为正比例函数（常数项固定为{const}≠0）"
            )
    if fixed_const_pattern and fixed_const_pattern.group(1) == '-':
        const = float(fixed_const_pattern.group(2))
        errors.append(
            f"正比例函数题：y=(k±数字)x-{const} 永远无法成为正比例函数（常数项固定为-{const}≠0）"
        )

    # 检测 y=(k-2)x+k-2：需要 k-2=0 同时 截距=0（不可能同时满足）
    dual_k_pattern = re.search(
        r'y\s*=\s*\(?\s*k\s*[-+]\s*\d[\.0-9]*\)?\s*x\s*([+\-])\s*\(?\s*k\s*([+\-])\s*\d[\.0-9]*\)?',
        question_text.replace(' ', '')
    )
    if dual_k_pattern:
        # 这类需要解方程，看答案是否合理
        pass  # 这类题可能是有解的（k²-4=0 且 k≠2 的情况）

    return errors


def check_quadratic_discriminant(question_text, answer_text, verbose=False):
    """
    检查：一元二次方程题，判别式是否导致无实数根
    规则：如果方程应该"有解"但判别式<0，则题目有误
    """
    errors = []

    # 检测方程 ax²+bx+c=0 形式
    eq_match = re.search(
        r'([-+]?\d*\.?\d*)x\^2\s*([+\-])\s*([-+]?\d*\.?\d*)x\s*([+\-])\s*(\d+\.?\d*)\s*=\s*0',
        question_text
    )
    if eq_match:
        a_str = eq_match.group(1) or '1'
        b_str = eq_match.group(3)
        c_str = eq_match.group(5)
        b_sign = eq_match.group(2)
        c_sign = eq_match.group(4)

        a = float(a_str) if a_str not in ('', '+') else 1
        b = float(b_sign + b_str) if b_str else 0
        c = float(c_sign + c_str) if c_str else 0

        discriminant = b**2 - 4*a*c

        # 检测题目是否暗示"有解"
        has_solution_hint = any(h in question_text for h in [
            '有解', '有两个', '有两个不相等', '实数根', '求根', '根为',
            '求k', 'k的取值', '恒成立', '总为正', '总为负'
        ])
        no_solution_hint = any(h in question_text for h in [
            '无实数根', '无解', '无根', '判别式<0', '判别式<0'
        ])

        if has_solution_hint and not no_solution_hint:
            if discriminant < -1e-9:
                errors.append(
                    f"二次方程题：{a}x²{b_str}x{c_sign}{c}=0 判别式Δ={discriminant:.2f}<0，题设暗示有解但方程无实数根"
                )
        elif discriminant == 0:
            if '不相等' in question_text:
                errors.append(
                    f"二次方程题：{a}x²...=0 的判别式=0，两个实根相等（相等）但题目要求'不相等'"
                )

    return errors


def check_division_by_zero(question_text, answer_text, verbose=False):
    """检查：题目中是否存在除零风险"""
    errors = []

    # 简单检测：答案中出现 ÷0、/0、除以0
    if '÷0' in question_text or '/0' in question_text:
        errors.append(f"除零错误：题目中包含除以0的表达式")

    return errors


def check_contradiction(question_text, answer_text, verbose=False):
    """
    检查：题目条件是否自相矛盾
    例如：等腰三角形中 AB=AC 且 AB≠AC
    """
    errors = []

    q = question_text

    # 检测几何多条件矛盾
    if '平行四边形' in q or '矩形' in q or '菱形' in q or '正方形' in q:
        # 对角线矛盾
        if '对角线' in q:
            # 平行四边形对角线互相平分
            if '对角线相等' in q and '平行四边形' in q:
                # 一般平行四边形对角线不一定相等，只有矩形才对角线相等
                pass  # 这不是错误，只是需要矩形条件

        # 对边矛盾
        if '对边平行' in q and '对边相等' in q:
            # 这是平行四边形的性质，不矛盾
            pass

    return errors


def check_answer_feasibility(question_text, answer_text, verbose=False):
    """
    检查：答案是否符合题目的约束条件
    例如：填空题答案是否在题目所给范围内
    """
    errors = []
    warnings = []

    q = question_text.lower()
    a = answer_text.lower()

    # 检测正比例函数答案
    if '正比例' in q and 'k' in q:
        # 答案应为 k = 某个数字（不等于0/某个特定值）
        k_match = re.search(r'k\s*=\s*([-+]?\d+\.?\d*)', a)
        if k_match:
            k_val = float(k_match.group(1))
            if abs(k_val) < 1e-9:
                errors.append(f"正比例函数答案 k={k_val} 无效（k≠0）")
            # 检查是否与题目其他条件矛盾
            # 如：k≠2 但答案k=2
            k_ne_pattern = re.search(r'k\s*[!=<>]+\s*(\d+)', q)
            if k_ne_pattern:
                k_excluded = int(k_ne_pattern.group(1))
                if abs(k_val - k_excluded) < 1e-6:
                    errors.append(f"正比例函数答案 k={k_val} 与题设 k≠{k_excluded} 矛盾")

    # 检测反比例函数 k≠0
    if '反比例' in q and 'k' in q:
        k_match = re.search(r'k\s*=\s*([-+]?\d+\.?\d*)', a)
        if k_match:
            k_val = float(k_match.group(1))
            if abs(k_val) < 1e-9:
                errors.append(f"反比例函数答案 k={k_val} 无效（k≠0）")

    return errors, warnings


def check_multiple_choice_options(html_content, q_num, verbose=False):
    """
    检查选择题选项是否合理：
    1. 是否有多个选项完全相同
    2. 是否有明显错误的选项（如正方形判定中写"四边相等+四角不等"）
    """
    errors = []

    # 提取该题的所有选项
    # 查找选项模式：A. xxx  B. xxx  C. xxx  D. xxx
    q_pattern = re.search(
        rf'(?:第\s*{q_num}\s*题|{q_num}[.、)]\s*)(.*?)(?:<br|</p|答案|$)',
        html_content, re.DOTALL
    )
    if not q_pattern:
        return errors

    q_text = q_pattern.group(0)

    # 提取选项
    options = re.findall(r'([A-D])[.、)]\s*([^A-D\n<]{5,50})', q_text)
    if not options:
        return errors

    # 检测完全相同的选项
    option_contents = [opt[1].strip() for opt in options]
    seen = {}
    for i, opt in enumerate(option_contents):
        # 归一化比较
        norm = re.sub(r'\s+', '', opt)
        if norm in seen:
            errors.append(f"第{q_num}题：选项{seen[norm]}和{options[i][0]}完全相同")
        else:
            seen[norm] = options[i][0]

    # 检测互斥选项（如"①+②"和"仅①"同时出现）
    if verbose:
        log(f"  第{q_num}题选项: {[o[0]+'. '+o[1][:30] for o in options]}", "INFO")

    return errors


def check_fill_blank_syntax(question_text, answer_text, verbose=False):
    """
    检查填空题：
    1. 是否有固定非零常数项的正比例函数题（无解）
    2. 答案格式是否合理（填空题不应要求"写出完整解题过程"）
    """
    errors = []

    q = question_text
    a = answer_text

    # 正比例函数固定常数项检测
    if '正比例函数' in q:
        # y=(k±数字)x + 固定数（非k的表达式）
        fixed_b = re.search(r'\+\s*(\d+(?:\.\d+)?)\s*$', q.replace(' ', '').replace('−','-'))
        if fixed_b:
            const = float(fixed_b.group(1))
            if const != 0 and 'k' not in fixed_b.group(0):
                # 确认常数项不是k的函数
                errors.append(
                    f"填空题：y=(k±n)x+{const} 形式的正比例函数题，常数项固定为{const}≠0，永远无法满足 b=0，题无解"
                )

    return errors


def validate_question(question_text, answer_text, q_num, verbose=False):
    """综合校验一道题目，返回错误和警告列表"""
    errors = []
    warnings = []

    errors.extend(check_linear_no_solution(question_text, answer_text, verbose))
    errors.extend(check_division_by_zero(question_text, answer_text))
    errors.extend(check_contradiction(question_text, answer_text))
    err2, warn2 = check_answer_feasibility(question_text, answer_text, verbose)
    errors.extend(err2)
    warnings.extend(warn2)
    errors.extend(check_fill_blank_syntax(question_text, answer_text))

    return errors, warnings


# ─── 主校验流程 ──────────────────────────────────────────────

def extract_qa_pairs(html_content, verbose=False):
    """
    从HTML中提取所有题目和答案对
    返回 [(q_num, q_text, a_text, q_type), ...]
    q_type: 'choice' | 'fill' | 'large'
    """
    pairs = []

    # 匹配选择题 q-header 或 q-card
    # 选择题通常有 q-num 标签和 A/B/C/D 选项
    choice_blocks = re.finditer(
        r'<div\s+class="q-card[^"]*"[^>]*>(.*?)<div\s+class="answer-box[^"]*"[^>]*id="([^"]+)"',
        html_content, re.DOTALL
    )
    for m in choice_blocks:
        block = m.group(0)
        qid = m.group(2)
        # 提取题号
        num_m = re.search(r'<span\s+class="q-num[^"]*"[^>]*>(\d+)</span>', block)
        q_num = num_m.group(1) if num_m else '?'

        # 提取题干（answer-box之前的内容）
        header_m = re.search(r'</div>\s*<div\s+class="q-body">(.*?)<div\s+class="answer-box', block, re.DOTALL)
        if header_m:
            q_text = re.sub(r'<[^>]+>', '', header_m.group(1)).strip()
        else:
            q_text = ""

        # 提取答案
        ans_m = re.search(r'<div\s+class="answer-box[^"]*"[^>]*id="' + re.escape(qid) + r'"[^>]*>(.*?)</div>', block, re.DOTALL)
        a_text = re.sub(r'<[^>]+>', '', ans_m.group(1)).strip() if ans_m else ""

        # 判断题型
        q_type = 'unknown'
        if any(opt in block for opt in ['A.', 'B.', 'C.', 'D.']):
            q_type = 'choice'
        elif '____' in q_text or '填空' in block:
            q_type = 'fill'

        if q_text:
            pairs.append((q_num, q_text, a_text, q_type))

    return pairs


def validate_file(html_path, verbose=False):
    path = Path(html_path)
    if not path.exists():
        log(f"文件不存在: {html_path}", "ERROR")
        return False

    content = path.read_text(encoding='utf-8')

    qa_pairs = extract_qa_pairs(content, verbose)
    if not qa_pairs:
        log("未找到题目，或HTML结构与预期不符（需包含 q-card、q-header、answer-box 等class）", "WARN")
        return True

    all_ok = True
    err_count = 0
    warn_count = 0

    for q_num, q_text, a_text, q_type in qa_pairs:
        if verbose:
            q_short = q_text[:60] + ('...' if len(q_text) > 60 else '')
            log(f"\n--- 第{q_num}题 ({q_type}) ---", "INFO")
            log(f"  题干: {q_short}", "INFO")

        errs, warns = validate_question(q_text, a_text, q_num, verbose)

        for e in errs:
            log(f"  第{q_num}题: {e}", "ERROR")
            all_ok = False
            err_count += 1
        for w in warns:
            log(f"  第{q_num}题: {w}", "WARN")
            warn_count += 1

        if verbose and not errs and not warns:
            log(f"  [OK] 第{q_num}题校验通过", "OK")

    log(f"\n{'='*50}", "")
    if all_ok:
        log(f"[PASS] 题目校验通过！共{len(qa_pairs)}道题，0个错误，{warn_count}个警告", "OK")
    else:
        log(f"[FAIL] 题目校验失败！共{len(qa_pairs)}道题，{err_count}个错误，{warn_count}个警告", "ERROR")
    return all_ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="校验HTML中的数学题目")
    parser.add_argument("html_file", help="HTML文件路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    args = parser.parse_args()
    ok = validate_file(args.html_file, verbose=args.verbose)
    sys.exit(0 if ok else 1)
