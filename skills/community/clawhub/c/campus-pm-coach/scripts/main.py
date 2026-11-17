#!/usr/bin/env python3
"""
resume-jd-review 主入口：校招/实习 · 互联网产品经理简历诊断套件。

能力编排（全部基于腾讯云 AI Skills 技能矩阵 + 本地规则引擎，零大模型依赖）：
  1. 简历评分（review）      ：矩阵内 OCR 提取 + 本地规则多维评分（按你的维度与标准）
  2. 简历一键优化（review）   ：按用户优化指令生成优化后简历文档
  3. 模拟面试题（interview） ：基于 JD 拆解 + 简历项目深挖，生成面试官可能问的问题

用法：
  # 纯文本免费模式（推荐日常使用）
  python main.py --resume-text "$(cat ../sample/resume.txt)" --jd ../sample/jd.txt --stage all -o ../sample/output

  # 首轮诊断：直接输出三部分（①评分+细项原因 ②可能问到的问题 ③综合判断）
  python main.py --resume-text "..." --jd "..." --stage quick -o ./out

  # 图片/PDF 简历（矩阵内 OCR 模式）
  python main.py --resume-file ../sample/resume.png --jd ../sample/jd.txt --stage all -o ../sample/output

  # 只做评分 + 一键优化，且带优化指令（优化稿末尾附带三部分诊断）
  python main.py --resume-text "..." --jd "..." --stage review \
    --optimize-instruction "突出实习经历，补充量化表达，针对 JD 定制" -o ./out

  # 自定义评价维度（你的专业能力输出）
  python main.py --resume-text "..." --jd "..." --dimensions ./my_dimensions.json --stage all -o ./out
"""

import argparse
import json
import os
import sys

import resume_parser
import evaluator
import optimizer as optimizer_mod
import interviewer as interviewer_mod
import formatter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DIMENSIONS = os.path.join(BASE_DIR, "config", "default_dimensions.json")


# ---------------------------------------------------------------------------
# 输入处理
# ---------------------------------------------------------------------------

def load_text_or_file(value: str) -> str:
    """参数既可以是文本也可以是文件路径。"""
    if os.path.isfile(value):
        with open(value, "r", encoding="utf-8") as f:
            return f.read()
    return value


def load_dimensions(path: str = "") -> list:
    """加载评价维度配置：默认配置或用户自定义 JSON 文件。"""
    p = path or DEFAULT_DIMENSIONS
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    dims = data.get("dimensions") if isinstance(data, dict) else (data if isinstance(data, list) else [])
    if not dims:
        raise RuntimeError(f"维度配置为空：{p}")
    return dims


def acquire_resume_text(args) -> tuple:
    """获取简历文本与结构化结果。

    返回 (resume_text, structured, source_desc)
    """
    if args.resume_file:
        is_pdf = args.is_pdf or str(args.resume_file).lower().endswith(".pdf")
        # 能力来源：tencentcloud-ocr（矩阵内）
        import ocr_service
        print(f"[OCR] 使用矩阵内技能 tencentcloud-ocr（GeneralAccurateOCR）解析: {args.resume_file}")
        resume_text = ocr_service.extract_resume_text(args.resume_file, is_pdf=is_pdf, pdf_page=args.pdf_page)
        # 能力来源：tencentcloud-ocr-extractdocagent（矩阵内，字段抽取增强）
        fields = {}
        try:
            fields = ocr_service.extract_resume_fields(args.resume_file, pdf_page=args.pdf_page)
            if fields:
                print(f"[OCR] ExtractDocAgent 字段抽取成功：{list(fields.keys())}")
        except Exception as exc:
            print(f"[warn] ExtractDocAgent 跳过：{exc}")
        source_desc = f"OCR({os.path.basename(args.resume_file)})"
    elif args.resume_text:
        resume_text = args.resume_text
        fields = {}
        source_desc = "文本"
    else:
        raise RuntimeError("必须提供 --resume-text 或 --resume-file 之一")

    structured = resume_parser.parse_resume(resume_text)
    return resume_text, structured, source_desc


# ---------------------------------------------------------------------------
# 能力 0：首轮诊断（三部分一体化输出）
# ---------------------------------------------------------------------------

def stage_quick(resume_text, jd_text, dimensions, output_dir):
    """首轮沟通一体化诊断：一次性输出 ① 评分+细项原因 ② 可能问到的问题 ③ 综合判断。"""
    structured = resume_parser.parse_resume(resume_text)
    evaluation = evaluator.evaluate_resume(resume_text, structured, jd_text, dimensions)
    questions_md = interviewer_mod.generate_interview_questions(resume_text, jd_text, structured)
    report = formatter.format_quick_report(evaluation, jd_text, questions_md)
    path = formatter.save_report(report, output_dir, "00_首轮诊断报告.md")
    print(f"[输出] 首轮诊断报告: {path}")
    formatter.save_json(evaluation, output_dir, "03_评分结果.json")
    print(f"[结果] 综合评分: {evaluation['total_score']} / 100")
    return path


# ---------------------------------------------------------------------------
# 能力 1：评分 + 一键优化
# ---------------------------------------------------------------------------

def stage_review(resume_text, jd_text, dimensions, optimize_instruction, output_dir):
    structured = resume_parser.parse_resume(resume_text)
    evaluation = evaluator.evaluate_resume(resume_text, structured, jd_text, dimensions)

    report = formatter.format_evaluation_report(evaluation, jd_text)
    report_path = formatter.save_report(report, output_dir, "01_评分报告.md")
    print(f"[输出] 评分报告: {report_path}")

    # 一键优化：生成优化后简历文档（每轮优化后输出结构都包含三部分诊断）
    opt = optimizer_mod.build_optimized_resume(
        resume_text, structured, evaluation, jd_text, optimize_instruction
    )
    if opt.get("hallucination_warnings"):
        print("[防幻觉校验] 发现可能新增的内容，请人工核对：")
        for w in opt["hallucination_warnings"]:
            print(f"  - {w}")
    questions_md = interviewer_mod.generate_interview_questions(opt["resume"], jd_text, structured)
    opt_full = formatter.append_diagnosis_section(opt["resume"], evaluation, questions_md)
    opt_path = formatter.save_report(opt_full, output_dir, "02_优化后简历.md")
    print(f"[输出] 优化后简历（含三部分诊断）: {opt_path}")
    if opt["change_log"]:
        for log in opt["change_log"]:
            print(f"  - {log}")

    # 优化后自动复评闭环：用评分引擎对优化稿正文（剥离元信息后）重新评分，
    # 验证分数不低于原文，防止"优化后反而低分"。
    opt_body = evaluator.strip_meta_text(opt["resume"])
    s_opt = resume_parser.parse_resume(opt_body)
    e_opt = evaluator.evaluate_resume(opt_body, s_opt, jd_text, dimensions)
    delta = round(e_opt["total_score"] - evaluation["total_score"], 1)
    if delta >= 0:
        print(
            f"[闭环校验] 优化后自动复评: {evaluation['total_score']} → "
            f"{e_opt['total_score']}（+{delta}），优化有效，分数不降"
        )
    else:
        print(
            f"[闭环校验] ⚠ 优化后自动复评下降: {evaluation['total_score']} → "
            f"{e_opt['total_score']}（{delta}），以下维度需人工复核："
        )
        for d1, d2 in zip(evaluation["dimension_scores"], e_opt["dimension_scores"]):
            if d2["score"] < d1["score"]:
                print(f"    ↓ {d1['name']}: {d1['score']} → {d2['score']}")

    formatter.save_json(evaluation, output_dir, "03_评分结果.json")
    print(f"[输出] 评分 JSON: {os.path.join(output_dir, '03_评分结果.json')}")

    return opt["resume"], evaluation


# ---------------------------------------------------------------------------
# 能力 2：模拟面试题
# ---------------------------------------------------------------------------

def stage_interview(resume_text, jd_text, structured, optimized_resume, output_dir):
    questions_md = interviewer_mod.generate_interview_questions(
        optimized_resume or resume_text, jd_text, structured
    )
    report = formatter.format_interview_report(questions_md)
    path = formatter.save_report(report, output_dir, "04_模拟面试题.md")
    print(f"[输出] 模拟面试题: {path}")
    return path


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="校招/实习 · 互联网产品经理简历诊断套件（矩阵内技能 + 本地规则引擎，零大模型）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--resume-text", type=str, help="简历文本（免费模式，推荐）")
    input_group.add_argument("--resume-file", type=str, help="简历图片/PDF 文件路径（矩阵内 OCR 模式）")
    parser.add_argument("--jd", type=str, required=True, help="JD 文本或 JD 文件路径")
    parser.add_argument("--dimensions", type=str, default="", help="自定义评价维度 JSON 文件路径（默认使用内置产品经理维度）")
    parser.add_argument("--stage", type=str, choices=["quick", "review", "interview", "all"], default="all", help="quick=首轮诊断(三部分一体化), review=评分+优化, interview=面试题, all=全流程")
    parser.add_argument("--optimize-instruction", type=str, default="", help="一键优化指令，如：突出实习经历、补充量化表达、针对 JD 定制")
    parser.add_argument("--is-pdf", action="store_true", help="resume-file 为 PDF 时指定")
    parser.add_argument("--pdf-page", type=int, default=1, help="PDF 识别页码（默认 1）")
    parser.add_argument("-o", "--output", type=str, default="output", help="输出目录")
    args = parser.parse_args()

    try:
        jd_text = load_text_or_file(args.jd)
        dimensions = load_dimensions(args.dimensions)
        resume_text, structured, source_desc = acquire_resume_text(args)
    except Exception as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"[输入] 简历来源: {source_desc}，简历字数: {len(resume_text)}")
    print(f"[输入] 评价维度: {len(dimensions)} 个（场景：{dimensions[0].get('standard', '')[:20] if dimensions else ''}…）")
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    optimized_resume = ""
    evaluation = {}

    if args.stage == "quick":
        print("\n=== 能力0：首轮诊断（三部分一体化输出）===")
        stage_quick(resume_text, jd_text, dimensions, output_dir)
    elif args.stage in ("review", "all"):
        print("\n=== 能力1：简历评分 + 一键优化 ===")
        optimized_resume, evaluation = stage_review(
            resume_text, jd_text, dimensions, args.optimize_instruction, output_dir
        )
        print(f"[结果] 综合评分: {evaluation['total_score']} / 100")

    if args.stage in ("interview", "all"):
        print("\n=== 能力2：模拟面试题生成 ===")
        if not optimized_resume:
            # interview 单独执行：先内部跑 review 拿优化稿
            print("[提示] 未提供优化后简历，先执行 review 生成优化稿作为面试题输入")
            optimized_resume, evaluation = stage_review(
                resume_text, jd_text, dimensions, args.optimize_instruction, output_dir
            )
        stage_interview(resume_text, jd_text, structured, optimized_resume, output_dir)

    print("\n完成。报告已输出至:", os.path.abspath(output_dir))


if __name__ == "__main__":
    main()
