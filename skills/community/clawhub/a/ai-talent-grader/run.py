#!/usr/bin/env python3
"""
快速运行脚本 - 提供示例和测试功能
"""

import sys
import json
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from main import AITalentGrader


def create_example_files():
    """创建示例文件"""
    example_dir = Path("examples")
    example_dir.mkdir(exist_ok=True)

    # 示例简历
    resume_content = """张三 - AI工程师

工作经历
2022.01 - 至今  AI科技公司 高级AI工程师
- 负责公司AI产品研发，使用GPT-4、LangChain等技术构建智能问答系统
- 通过优化RAG架构，将问答准确率从75%提升到92%
- 设计并实现了一套AI工作流，将运营团队的工作效率提升了300%
- 主导了公司AI技术选型，推动从传统NLP向大语言模型转型

2020.07 - 2021.12  创业公司 全栈工程师
- 使用React + Django开发电商平台
- 引入机器学习算法优化推荐系统，提升转化率15%

技能
- 编程语言: Python, JavaScript, Java
- AI框架: TensorFlow, PyTorch, LangChain, OpenAI API
- 数据库: MySQL, MongoDB, Redis
- 云平台: AWS, Azure

教育背景
2016.09 - 2020.06  清华大学 计算机科学与技术 本科
"""

    # 示例面试记录
    interview_content = """面试记录 - 张三

面试时间: 2024-01-15
面试官: 李四

Q: 请介绍一下你在AI产品中的具体贡献
A: 我主要负责智能问答系统的架构设计。我们最初用的是传统的NLP方案，准确率只有75%左右。后来我推动团队转向大语言模型，使用GPT-4 + LangChain + RAG架构，经过几个月的优化，准确率提升到了92%。

Q: 这个提升过程中遇到的最大挑战是什么？
A: 最大的挑战是幻觉问题。GPT-4有时候会编造答案，我们通过设计多轮验证机制和人工审核节点来解决。另外，RAG的检索质量也很关键，我们优化了embedding模型和检索算法。

Q: 你提到将运营效率提升了300%，这个数据是怎么来的？
A: 我们统计了运营团队处理相同数量工单的时间。原来需要3个人每天工作8小时，现在只需要1个人工作4小时，而且有AI辅助审核。这个数据是经过A/B测试验证的。

Q: 在技术选型时，为什么选择GPT-4而不是其他模型？
A: 我们对比了GPT-4、Claude和国内的一些大模型。GPT-4在复杂推理和代码生成上表现最好，而且API稳定。虽然成本高一些，但考虑到准确率对业务的影响，我们选择了GPT-4。

面试官评价:
- 技术基础扎实，对AI技术有深入理解
- 项目经验丰富，有实际成果数据支撑
- 沟通表达清晰，能讲清楚技术决策的原因
- 建议评级: L3 (AI架构者)
"""

    # 保存示例文件
    resume_path = example_dir / "zhangsan_resume.txt"
    interview_path = example_dir / "zhangsan_interview.txt"

    resume_path.write_text(resume_content, encoding='utf-8')
    interview_path.write_text(interview_content, encoding='utf-8')

    print(f"示例文件已创建:")
    print(f"  简历: {resume_path}")
    print(f"  面试: {interview_path}")
    return resume_path, interview_path


def run_audit_example():
    """运行审计示例"""
    print("=== 运行模式A：简历审计示例 ===")
    grader = AITalentGrader()

    resume_path, _ = create_example_files()

    result = grader.audit_only(
        resume_path=str(resume_path),
        candidate_id="EXAMPLE_001",
        output_path="example_audit_report.md",
    )

    print(f"审计完成:")
    print(f"  候选人ID: {result['candidate_id']}")
    print(f"  审计结论: {result['audit_result'].overall_conclusion.value}")
    print(f"  报告文件: {result['report_path']}")
    print(f"  测谎题数量: {len(result['audit_result'].lie_detection_questions)}")

    # 显示部分报告
    print("\n--- 报告预览 (前10行) ---")
    lines = result['report'].split('\n')[:10]
    for line in lines:
        print(line)


def run_evaluate_example():
    """运行完整评估示例"""
    print("=== 运行模式B：完整评估示例 ===")
    grader = AITalentGrader()

    resume_path, interview_path = create_example_files()

    # 手动指定维度得分（实际使用中应由LLM分析后提供）
    dimension_scores = {
        'ai_fluency': 3.0,  # 熟练使用GPT-4、LangChain等
        'human_ai_judgment': 3.0,  # 有幻觉问题解决方案
        'architecture_design': 3.0,  # 设计RAG架构
        'hybrid_orchestration': 2.5,  # 推动团队转型
        'cognitive_depth': 3.0,  # 理解trade-off
        'problem_modeling': 3.0,  # 从传统NLP转向LLM
    }

    evidence_map = {
        'ai_fluency': '熟练使用GPT-4、LangChain、RAG等技术构建智能问答系统',
        'human_ai_judgment': '设计多轮验证机制和人工审核节点解决幻觉问题',
        'architecture_design': '设计GPT-4 + LangChain + RAG架构，将准确率从75%提升到92%',
        'hybrid_orchestration': '推动团队从传统NLP向大语言模型转型',
        'cognitive_depth': '理解GPT-4 vs Claude vs 国内模型的trade-off，选择GPT-4',
        'problem_modeling': '识别传统NLP方案瓶颈，重新设计为LLM方案',
    }

    result = grader.evaluate_full(
        resume_path=str(resume_path),
        interview_path=str(interview_path),
        candidate_id="EXAMPLE_002",
        env_complexity="high",  # AI科技公司
        personal_leverage="high",  # 主导技术选型
        growth_speed="high",  # 快速成长
        dimension_scores=dimension_scores,
        evidence_map=evidence_map,
        output_path="example_full_report.md",
    )

    grade = result['evaluation_result'].final_grade
    weighted = result['evaluation_result'].weighted_result

    print(f"评估完成:")
    print(f"  候选人ID: {result['candidate_id']}")
    print(f"  最终级别: L{grade.level} ({grade.level_name})")
    print(f"  加权得分: {weighted.final_score:.1f}")
    print(f"  报告文件: {result['report_path']}")

    # 显示维度得分
    print("\n--- 六维度得分 ---")
    for score in result['evaluation_result'].dimension_scores:
        print(f"  {score.dimension}: {score.score:.1f}/4")


def run_batch_example():
    """运行批量处理示例"""
    print("=== 运行批量处理示例 ===")
    grader = AITalentGrader()

    # 先创建示例文件
    create_example_files()

    # 运行批量处理
    results = grader.batch_process(
        input_dir="examples",
        output_dir="batch_reports",
        env_complexity="medium",
        personal_leverage="medium",
        growth_speed="medium",
    )

    print(f"批量处理完成:")
    print(f"  总处理: {len(results)} 个候选人")
    for r in results:
        if r['status'] == 'success':
            grade = r['result']['evaluation_result'].final_grade
            print(f"  {r['name']}: L{grade.level} ({grade.level_name})")
        else:
            print(f"  {r['name']}: {r['status']}")


def test_modules():
    """测试各个模块"""
    print("=== 测试模块功能 ===")
    grader = AITalentGrader()

    # 测试文件解析
    print("1. 测试文件解析...")
    resume_path, interview_path = create_example_files()
    candidate = grader.file_parser.parse_resume(str(resume_path))
    interview = grader.file_parser.parse_interview(str(interview_path))
    print(f"  解析成功: {candidate.candidate_id}, 技能: {len(candidate.skills)}项")

    # 测试简历审计
    print("2. 测试简历审计...")
    audit_result = grader.resume_auditor.audit(candidate.raw_text)
    print(f"  审计完成: {audit_result.overall_conclusion.value}, 问题: {len(audit_result.issues)}个")

    # 测试面试分析
    print("3. 测试面试分析...")
    cross_verification = grader.interview_analyzer.cross_verify(
        audit_result.issues,
        interview.raw_text,
    )
    print(f"  交叉验证: 覆盖{cross_verification.covered}/{cross_verification.total_issues}")

    # 测试评估引擎
    print("4. 测试评估引擎...")
    dimension_scores = {
        'ai_fluency': 3.0,
        'human_ai_judgment': 3.0,
        'architecture_design': 3.0,
        'hybrid_orchestration': 2.5,
        'cognitive_depth': 3.0,
        'problem_modeling': 3.0,
    }
    eval_result = grader.evaluation_engine.evaluate(
        dimension_scores=dimension_scores,
        env_complexity="high",
        personal_leverage="high",
        growth_speed="high",
    )
    print(f"  评估完成: L{eval_result.final_grade.level}")

    print("所有模块测试通过 ✓")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='AI人才定级 - 示例和测试')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # 创建示例文件
    create_parser = subparsers.add_parser('create', help='创建示例文件')
    create_parser.set_defaults(func=lambda: create_example_files())

    # 运行审计示例
    audit_parser = subparsers.add_parser('audit', help='运行审计示例')
    audit_parser.set_defaults(func=run_audit_example)

    # 运行评估示例
    eval_parser = subparsers.add_parser('evaluate', help='运行完整评估示例')
    eval_parser.set_defaults(func=run_evaluate_example)

    # 运行批量示例
    batch_parser = subparsers.add_parser('batch', help='运行批量处理示例')
    batch_parser.set_defaults(func=run_batch_example)

    # 测试模块
    test_parser = subparsers.add_parser('test', help='测试所有模块')
    test_parser.set_defaults(func=test_modules)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()