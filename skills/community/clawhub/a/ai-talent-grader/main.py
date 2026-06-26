#!/usr/bin/env python3
"""
AI人才定级专家 - 一站式自动化评估系统

用法:
    # 单次评估（仅简历）
    python main.py audit --resume 简历.pdf

    # 完整定级（简历 + 面试）
    python main.py evaluate --resume 简历.pdf --interview 面试记录.txt

    # 指定公司背景
    python main.py evaluate --resume 简历.pdf --interview 面试记录.txt \\
        --env medium --leverage high --growth high

    # 批量处理
    python main.py batch --input-dir candidates/ --output-dir reports/

    # 指定配置
    python main.py evaluate --resume 简历.pdf --config custom_config.yaml
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Optional

import yaml
from loguru import logger

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from modules.file_parser import FileParser, CandidateInfo, InterviewRecord
from modules.resume_audit import ResumeAuditor, ResumeAuditResult
from modules.interview_analyzer import InterviewAnalyzer, InterviewAnalysisResult
from modules.evaluation_engine import EvaluationEngine, EvaluationResult
from modules.report_generator import ReportGenerator


class AITalentGrader:
    """AI人才定级一站式评估器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化评估器

        Args:
            config_path: 配置文件路径，默认使用 config/evaluation_config.yaml
        """
        self.config = self._load_config(config_path)
        self.file_parser = FileParser(self.config.get('file_parser', {}))
        self.resume_auditor = ResumeAuditor()
        self.interview_analyzer = InterviewAnalyzer()
        self.evaluation_engine = EvaluationEngine(self.config)
        self.report_generator = ReportGenerator()

        logger.info("AI人才定级评估器初始化完成")

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent / 'config' / 'evaluation_config.yaml'

        config_path = Path(config_path)
        if not config_path.exists():
            logger.warning(f"配置文件不存在: {config_path}，使用默认配置")
            return self._default_config()

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        logger.info(f"已加载配置: {config_path}")
        return config

    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            'weights': {
                'ai_fluency': 1.0,
                'human_ai_judgment': 1.2,
                'architecture_design': 1.5,
                'hybrid_orchestration': 1.1,
                'cognitive_depth': 1.3,
                'problem_modeling': 1.4,
            },
            'level_thresholds': {'l1': 4.0, 'l2': 8.0, 'l3': 12.0, 'l4': 15.0},
            'environment_complexity': {
                'low': {'coefficient': 0.7},
                'medium': {'coefficient': 1.0},
                'high': {'coefficient': 1.2},
            },
            'personal_leverage': {
                'low': {'coefficient': 0.7},
                'medium': {'coefficient': 1.0},
                'high': {'coefficient': 1.3},
            },
            'growth_speed': {
                'low': {'adjustment': -0.5},
                'medium': {'adjustment': 0},
                'high': {'adjustment': 0.5},
            },
        }

    def audit_only(
        self,
        resume_path: str,
        candidate_id: str = "",
        output_path: Optional[str] = None,
    ) -> Dict:
        """
        模式A：仅简历审计 + 测谎题生成

        Args:
            resume_path: 简历文件路径
            candidate_id: 候选人编号
            output_path: 报告输出路径

        Returns:
            包含审计结果和报告路径的字典
        """
        logger.info(f"=== 模式A：简历审计 ===")
        logger.info(f"简历: {resume_path}")

        # 1. 解析简历
        candidate = self.file_parser.parse_resume(resume_path)
        candidate_id = candidate_id or candidate.candidate_id
        logger.info(f"候选人ID: {candidate_id}")

        # 2. 简历审计
        audit_result = self.resume_auditor.audit(
            candidate.raw_text,
            candidate_info={
                'candidate_id': candidate_id,
                'years_of_experience': candidate.years_of_experience,
                'skills': candidate.skills,
            },
        )

        # 3. 生成报告
        report = self.report_generator.generate_audit_report(
            audit_result,
            candidate_info={'candidate_id': candidate_id},
            candidate_id=candidate_id,
        )

        # 4. 保存报告
        if output_path is None:
            output_path = f"report_{candidate_id}_audit.md"

        self.report_generator.save_report(report, output_path)

        return {
            'candidate_id': candidate_id,
            'audit_result': audit_result,
            'report_path': output_path,
            'report': report,
        }

    def evaluate_full(
        self,
        resume_path: str,
        interview_path: str,
        candidate_id: str = "",
        env_complexity: str = "medium",
        personal_leverage: str = "medium",
        growth_speed: str = "medium",
        dimension_scores: Optional[Dict[str, float]] = None,
        evidence_map: Optional[Dict[str, str]] = None,
        cognitive_levels: Optional[Dict[str, str]] = None,
        output_path: Optional[str] = None,
        output_format: str = "md",
    ) -> Dict:
        """
        模式B：完整定级（简历 + 面试）

        Args:
            resume_path: 简历文件路径
            interview_path: 面试记录文件路径
            candidate_id: 候选人编号
            env_complexity: 环境复杂度 low/medium/high
            personal_leverage: 个人杠杆率 low/medium/high
            growth_speed: 成长速度 low/medium/high
            dimension_scores: 手动指定六维度得分（可选）
            evidence_map: 各维度依据说明
            cognitive_levels: 各维度认知层级
            output_path: 报告输出路径
            output_format: 输出格式 md/json

        Returns:
            包含完整评估结果的字典
        """
        logger.info(f"=== 模式B：完整定级 ===")
        logger.info(f"简历: {resume_path}")
        logger.info(f"面试: {interview_path}")

        # 1. 解析文件
        candidate = self.file_parser.parse_resume(resume_path)
        interview = self.file_parser.parse_interview(interview_path)
        candidate_id = candidate_id or candidate.candidate_id
        logger.info(f"候选人ID: {candidate_id}")

        # 2. 简历审计
        audit_result = self.resume_auditor.audit(
            candidate.raw_text,
            candidate_info={
                'candidate_id': candidate_id,
                'years_of_experience': candidate.years_of_experience,
                'skills': candidate.skills,
            },
        )

        # 3. 面试交叉验证
        cross_verification = self.interview_analyzer.cross_verify(
            audit_result.issues,
            interview.raw_text,
        )

        # 4. 评估面试质量
        interview_quality = self.interview_analyzer.evaluate_interview_quality(
            interview.raw_text
        )

        # 5. 提取面试关键观察
        key_observations = self.interview_analyzer.extract_key_observations(
            interview.raw_text,
            candidate_info={'candidate_id': candidate_id},
        )

        # 6. 六维度评估
        # 如果用户手动指定了分数，使用用户指定值
        # 否则基于审计和分析结果自动推断（此处提供默认值作为示例）
        if dimension_scores is None:
            dimension_scores = self._infer_dimension_scores(
                candidate, audit_result, cross_verification
            )

        evidence_map = evidence_map or {}
        cognitive_levels = cognitive_levels or {}

        # 7. 执行评估引擎
        eval_result = self.evaluation_engine.evaluate(
            dimension_scores=dimension_scores,
            env_complexity=env_complexity,
            personal_leverage=personal_leverage,
            growth_speed=growth_speed,
            evidence_map=evidence_map,
            cognitive_levels=cognitive_levels,
        )

        # 8. 生成报告
        source_files = [resume_path, interview_path]

        if output_format == 'json':
            report = self.report_generator.generate_json(
                eval_result, audit_result, candidate_id
            )
            ext = '.json'
        else:
            report = self.report_generator.generate_full_report(
                eval_result,
                audit_result,
                cross_verification=cross_verification,
                candidate_info={'candidate_id': candidate_id},
                candidate_id=candidate_id,
                source_files=source_files,
            )
            ext = '.md'

        # 9. 保存报告
        if output_path is None:
            output_path = f"report_{candidate_id}_full{ext}"

        self.report_generator.save_report(report, output_path)

        return {
            'candidate_id': candidate_id,
            'audit_result': audit_result,
            'cross_verification': cross_verification,
            'evaluation_result': eval_result,
            'interview_quality': interview_quality,
            'key_observations': key_observations,
            'report_path': output_path,
            'report': report,
        }

    def _infer_dimension_scores(
        self,
        candidate: CandidateInfo,
        audit_result: ResumeAuditResult,
        cross_verification: InterviewAnalysisResult,
    ) -> Dict[str, float]:
        """
        基础维度得分推断（v3.2 修正版）

        v3.2 关键修正：不再基于技能数量、经验年限等粗糙指标自动打分。
        这些规则违反 skill 铁律：工具数量≠能力、年限是参考不是铁律。

        此方法仅提供保守的兜底默认值（全 2.0），强烈建议用户通过 --scores 参数手动指定。
        真实的维度打分应基于行为锚点充要条件，由人类面试官或 LLM 根据完整上下文评定。

        参考：references/behavioral_anchors.md（v3.2 充要条件版）
        """
        scores = {
            'ai_fluency': 2.0,
            'human_ai_judgment': 2.0,
            'architecture_design': 2.0,
            'hybrid_orchestration': 2.0,
            'cognitive_depth': 2.0,
            'problem_modeling': 2.0,
        }

        logger.warning(
            "⚠️ 自动推断维度得分已使用保守默认值（全 2.0）。"
            "这些值不代表候选人真实水平，仅作为计算兜底。"
            "请通过 --scores 参数传入手动评估的维度得分。"
            "参考：references/behavioral_anchors.md（v3.2 充要条件版）"
        )
        logger.info(f"兜底维度得分: {scores}")
        return scores

    def batch_process(
        self,
        input_dir: str,
        resume_suffix: str = "_resume",
        interview_suffix: str = "_interview",
        output_dir: str = "reports/",
        env_complexity: str = "medium",
        personal_leverage: str = "medium",
        growth_speed: str = "medium",
    ) -> list:
        """
        批量处理候选人

        文件命名规则：
        - {name}{resume_suffix}.pdf/.docx → 简历
        - {name}{interview_suffix}.txt/.md → 面试记录

        Args:
            input_dir: 输入目录
            resume_suffix: 简历文件后缀标识
            interview_suffix: 面试文件后缀标识
            output_dir: 输出目录
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 查找简历文件
        resume_files = {}
        for ext in ['.pdf', '.docx', '.txt', '.md']:
            for f in input_path.glob(f'*{resume_suffix}{ext}'):
                name = f.stem.replace(resume_suffix, '')
                resume_files[name] = str(f)

        results = []
        for name, resume_path in resume_files.items():
            # 查找对应的面试文件
            interview_path = None
            for ext in ['.txt', '.md', '.json', '.yaml']:
                candidate = input_path / f'{name}{interview_suffix}{ext}'
                if candidate.exists():
                    interview_path = str(candidate)
                    break

            if interview_path:
                logger.info(f"处理: {name}")
                try:
                    result = self.evaluate_full(
                        resume_path=resume_path,
                        interview_path=interview_path,
                        candidate_id=name,
                        env_complexity=env_complexity,
                        personal_leverage=personal_leverage,
                        growth_speed=growth_speed,
                        output_path=str(output_path / f'report_{name}.md'),
                    )
                    results.append({'name': name, 'status': 'success', 'result': result})
                except Exception as e:
                    logger.error(f"处理失败 {name}: {e}")
                    results.append({'name': name, 'status': 'error', 'error': str(e)})
            else:
                logger.warning(f"未找到面试记录: {name}")
                try:
                    result = self.audit_only(
                        resume_path=resume_path,
                        candidate_id=name,
                        output_path=str(output_path / f'report_{name}_audit.md'),
                    )
                    results.append({'name': name, 'status': 'audit_only', 'result': result})
                except Exception as e:
                    logger.error(f"处理失败 {name}: {e}")
                    results.append({'name': name, 'status': 'error', 'error': str(e)})

        # 生成汇总
        summary = self._generate_batch_summary(results, output_path)
        logger.info(f"批量处理完成: {len(results)} 个候选人，汇总: {summary}")

        return results

    def _generate_batch_summary(self, results: list, output_path: Path) -> str:
        """生成批量处理汇总"""
        lines = [
            "# 批量评估汇总\n",
            f"处理时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"总候选人: {len(results)}\n",
            "| 候选人 | 状态 | 级别 | 备注 |",
            "|--------|------|------|------|",
        ]

        for r in results:
            name = r['name']
            status = r['status']
            if status == 'success':
                grade = r['result']['evaluation_result'].final_grade
                level = f"L{grade.level}"
                note = grade.level_name
            elif status == 'audit_only':
                level = '-'
                note = '仅审计'
            else:
                level = '-'
                note = r.get('error', '未知错误')

            lines.append(f"| {name} | {status} | {level} | {note} |")

        summary_path = output_path / 'batch_summary.md'
        summary_text = '\n'.join(lines)
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_text)

        return str(summary_path)


def main():
    parser = argparse.ArgumentParser(
        description='AI人才定级专家 - 一站式自动化评估系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest='command', help='命令')

    # ===== audit =====
    audit_parser = subparsers.add_parser('audit', help='仅简历审计（模式A）')
    audit_parser.add_argument('--resume', required=True, help='简历文件路径')
    audit_parser.add_argument('--id', default='', help='候选人编号')
    audit_parser.add_argument('--output', help='报告输出路径')
    audit_parser.add_argument('--config', help='配置文件路径')

    # ===== evaluate =====
    eval_parser = subparsers.add_parser('evaluate', help='完整定级（模式B）')
    eval_parser.add_argument('--resume', required=True, help='简历文件路径')
    eval_parser.add_argument('--interview', required=True, help='面试记录文件路径')
    eval_parser.add_argument('--id', default='', help='候选人编号')
    eval_parser.add_argument('--env', default='medium', choices=['low', 'medium', 'high'],
                             help='环境复杂度')
    eval_parser.add_argument('--leverage', default='medium', choices=['low', 'medium', 'high'],
                             help='个人杠杆率')
    eval_parser.add_argument('--growth', default='medium', choices=['low', 'medium', 'high'],
                             help='成长速度')
    eval_parser.add_argument('--scores', help='六维度得分JSON文件路径')
    eval_parser.add_argument('--output', help='报告输出路径')
    eval_parser.add_argument('--format', default='md', choices=['md', 'json'],
                             help='输出格式')
    eval_parser.add_argument('--config', help='配置文件路径')

    # ===== batch =====
    batch_parser = subparsers.add_parser('batch', help='批量处理')
    batch_parser.add_argument('--input-dir', required=True, help='输入目录')
    batch_parser.add_argument('--output-dir', default='reports/', help='输出目录')
    batch_parser.add_argument('--env', default='medium', choices=['low', 'medium', 'high'])
    batch_parser.add_argument('--leverage', default='medium', choices=['low', 'medium', 'high'])
    batch_parser.add_argument('--growth', default='medium', choices=['low', 'medium', 'high'])
    batch_parser.add_argument('--config', help='配置文件路径')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 初始化评估器
    grader = AITalentGrader(config_path=getattr(args, 'config', None))

    if args.command == 'audit':
        result = grader.audit_only(
            resume_path=args.resume,
            candidate_id=args.id,
            output_path=args.output,
        )
        print(f"\n报告已生成: {result['report_path']}")
        print(f"审计结论: {result['audit_result'].overall_conclusion.value}")

    elif args.command == 'evaluate':
        dimension_scores = None
        if args.scores:
            with open(args.scores, 'r', encoding='utf-8') as f:
                dimension_scores = json.load(f)

        result = grader.evaluate_full(
            resume_path=args.resume,
            interview_path=args.interview,
            candidate_id=args.id,
            env_complexity=args.env,
            personal_leverage=args.leverage,
            growth_speed=args.growth,
            dimension_scores=dimension_scores,
            output_path=args.output,
            output_format=args.format,
        )

        grade = result['evaluation_result'].final_grade
        print(f"\n报告已生成: {result['report_path']}")
        print(f"定级结果: L{grade.level} ({grade.level_name})")

    elif args.command == 'batch':
        results = grader.batch_process(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            env_complexity=args.env,
            personal_leverage=args.leverage,
            growth_speed=args.growth,
        )
        success = sum(1 for r in results if r['status'] == 'success')
        print(f"\n批量处理完成: {success}/{len(results)} 成功")


if __name__ == '__main__':
    main()