"""
测试报告服务

生成HTML测试报告、AI失败分析和报告导出
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict
import logging

from sqlalchemy.orm import Session
from app.models.test_report import TestReport
from app.models.execute_record import ExecuteRecord
from app.models.script import AutoScript
from app.schemas.report import ReportGenerateRequest, ReportExportRequest
from app.services.ai_generator import AIGeneratorService
from app.core.config import settings

logger = logging.getLogger(__name__)


class ReportService:
    """测试报告服务类"""

    def __init__(self, db: Session):
        self.db = db

    def generate_report(self, request: ReportGenerateRequest, auth_code: str = None) -> TestReport:
        """
        生成测试报告

        Args:
            request: 报告生成请求
            auth_code: 授权码

        Returns:
            生成的测试报告
        """
        # 查询执行记录
        record = self.db.query(ExecuteRecord).filter(ExecuteRecord.id == request.record_id).first()
        if not record:
            raise ValueError(f"执行记录不存在: {request.record_id}")

        # 查询脚本信息
        script = self.db.query(AutoScript).filter(AutoScript.id == record.script_id).first()
        if not script:
            raise ValueError(f"脚本不存在: {record.script_id}")

        # 解析日志，提取测试统计
        test_stats = self._parse_test_statistics(record.log)

        # 生成HTML报告
        report_content = self._generate_html_report(
            script_name=script.name,
            script_type=script.type,
            result=record.result,
            log=record.log,
            duration=record.duration,
            test_stats=test_stats
        )

        # 保存报告到文件
        report_path = self._save_report_file(script.name, report_content)

        # AI分析（如果启用且测试失败）
        ai_analysis = None
        if request.include_ai_analysis and record.result == "fail":
            try:
                ai_analysis = self._generate_ai_analysis(record.log)
            except Exception as e:
                logger.error(f"AI分析失败: {str(e)}")
                ai_analysis = f"AI分析失败: {str(e)}"

        # 创建报告记录
        report = TestReport(
            record_id=record.id,
            script_id=script.id,
            script_name=script.name,
            script_type=script.type,
            result=record.result,
            total_tests=test_stats.get("total", 0),
            passed_tests=test_stats.get("passed", 0),
            failed_tests=test_stats.get("failed", 0),
            duration=record.duration,
            report_content=report_content,
            report_path=report_path,
            log_content=record.log,
            ai_analysis=ai_analysis
        )

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)

        logger.info(f"生成测试报告: ID={report.id}, script={script.name}, result={record.result}")
        return report

    def get_report(self, report_id: int) -> Optional[TestReport]:
        """获取报告"""
        return self.db.query(TestReport).filter(TestReport.id == report_id).first()

    def get_report_by_record(self, record_id: int) -> Optional[TestReport]:
        """根据执行记录ID获取报告"""
        return self.db.query(TestReport).filter(TestReport.record_id == record_id).first()

    def list_reports(self, script_id: Optional[int] = None, limit: int = 100) -> List[TestReport]:
        """列出报告"""
        query = self.db.query(TestReport)

        if script_id:
            query = query.filter(TestReport.script_id == script_id)

        return query.order_by(TestReport.create_time.desc()).limit(limit).all()

    def export_report(self, request: ReportExportRequest) -> str:
        """
        导出报告

        Args:
            request: 导出请求

        Returns:
            导出文件路径
        """
        report = self.get_report(request.report_id)
        if not report:
            raise ValueError(f"报告不存在: {request.report_id}")

        if request.format == "html":
            # 导出HTML（已经是HTML格式，直接返回路径）
            return report.report_path

        elif request.format == "pdf":
            # 导出PDF
            pdf_path = self._export_to_pdf(report, request.include_screenshots)
            return pdf_path

        else:
            raise ValueError(f"不支持的导出格式: {request.format}")

    def generate_ai_analysis(self, report_id: int) -> str:
        """
        生成AI分析

        Args:
            report_id: 报告ID

        Returns:
            AI分析结果
        """
        report = self.get_report(report_id)
        if not report:
            raise ValueError(f"报告不存在: {report_id}")

        if not report.log_content:
            return "无执行日志，无法进行分析"

        try:
            ai_analysis = self._generate_ai_analysis(report.log_content)

            # 更新报告
            report.ai_analysis = ai_analysis
            self.db.commit()

            return ai_analysis
        except Exception as e:
            logger.error(f"生成AI分析失败: {str(e)}")
            raise

    def _parse_test_statistics(self, log: str) -> Dict:
        """
        解析日志，提取测试统计

        Args:
            log: 执行日志

        Returns:
            测试统计字典
        """
        stats = {
            "total": 0,
            "passed": 0,
            "failed": 0
        }

        try:
            # 解析pytest输出
            lines = log.split('\n')
            for line in lines:
                # 匹配 "X passed" 或 "X failed"
                if "passed" in line.lower():
                    import re
                    match = re.search(r'(\d+)\s+passed', line)
                    if match:
                        stats["passed"] = int(match.group(1))

                if "failed" in line.lower():
                    import re
                    match = re.search(r'(\d+)\s+failed', line)
                    if match:
                        stats["failed"] = int(match.group(1))

                # 匹配 "X tests ran"
                if "test" in line.lower() and "ran" in line.lower():
                    import re
                    match = re.search(r'(\d+)\s+test', line)
                    if match:
                        stats["total"] = int(match.group(1))

            # 如果总数为0，估算总数
            if stats["total"] == 0:
                stats["total"] = stats["passed"] + stats["failed"]

        except Exception as e:
            logger.error(f"解析测试统计失败: {str(e)}")

        return stats

    def _generate_html_report(self, script_name: str, script_type: str, result: str,
                              log: str, duration: int, test_stats: Dict) -> str:
        """
        生成HTML报告内容

        Args:
            script_name: 脚本名称
            script_type: 脚本类型
            result: 测试结果
            log: 执行日志
            duration: 执行耗时
            test_stats: 测试统计

        Returns:
            HTML报告内容
        """
        # 根据结果显示不同的颜色
        result_color = "#28a745" if result == "success" else "#dc3545"
        result_text = "✓ 通过" if result == "success" else "✗ 失败"

        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试报告 - {script_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .summary-card h3 {{
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }}
        .summary-card .value {{
            font-size: 32px;
            font-weight: bold;
        }}
        .success {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .neutral {{ color: #007bff; }}
        .result-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 18px;
            background: {result_color};
            color: white;
        }}
        .log-section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }}
        .log-section h2 {{
            margin-bottom: 15px;
            color: #333;
        }}
        .log-content {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 500px;
            overflow-y: auto;
        }}
        .timestamp {{
            color: #999;
            font-size: 12px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 测试报告</h1>
            <p><strong>{script_name}</strong> ({script_type.upper()})</p>
            <p class="timestamp">生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>

        <div class="summary">
            <div class="summary-card">
                <h3>测试结果</h3>
                <div class="result-badge">{result_text}</div>
            </div>
            <div class="summary-card">
                <h3>总测试数</h3>
                <div class="value neutral">{test_stats.get('total', 0)}</div>
            </div>
            <div class="summary-card">
                <h3>通过数量</h3>
                <div class="value success">{test_stats.get('passed', 0)}</div>
            </div>
            <div class="summary-card">
                <h3>失败数量</h3>
                <div class="value fail">{test_stats.get('failed', 0)}</div>
            </div>
            <div class="summary-card">
                <h3>执行耗时</h3>
                <div class="value neutral">{duration}秒</div>
            </div>
        </div>

        <div class="log-section">
            <h2>📋 执行日志</h2>
            <div class="log-content">{log}</div>
        </div>

        <div class="footer">
            <p>AI自动化测试平台 © 2026</p>
            <p>Powered by FastAPI + Pytest + Playwright</p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def _save_report_file(self, script_name: str, report_content: str) -> str:
        """
        保存报告到文件

        Args:
            script_name: 脚本名称
            report_content: 报告内容

        Returns:
            报告文件路径
        """
        try:
            # 创建报告目录
            report_dir = f"data/reports"
            os.makedirs(report_dir, exist_ok=True)

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"{report_dir}/{script_name}_{timestamp}.html"

            # 保存文件
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_content)

            logger.info(f"保存报告到文件: {report_path}")
            return report_path

        except Exception as e:
            logger.error(f"保存报告文件失败: {str(e)}")
            raise

    def _export_to_pdf(self, report: TestReport, include_screenshots: bool) -> str:
        """
        导出报告为PDF

        Args:
            report: 测试报告
            include_screenshots: 是否包含截图

        Returns:
            PDF文件路径
        """
        try:
            # 使用weasyprint将HTML转换为PDF
            # 注意：需要安装 weasyprint: pip install weasyprint
            from weasyprint import HTML

            pdf_dir = "data/reports/pdf"
            os.makedirs(pdf_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = f"{pdf_dir}/{report.script_name}_{timestamp}.pdf"

            # 转换HTML到PDF
            HTML(string=report.report_content).write_pdf(pdf_path)

            logger.info(f"导出PDF报告: {pdf_path}")
            return pdf_path

        except ImportError:
            logger.error("weasyprint未安装，无法导出PDF")
            raise ImportError("请安装weasyprint: pip install weasyprint")
        except Exception as e:
            logger.error(f"导出PDF失败: {str(e)}")
            raise

    def _generate_ai_analysis(self, log_content: str) -> str:
        """
        生成AI分析

        Args:
            log_content: 执行日志

        Returns:
            AI分析结果
        """
        try:
            # 使用AI服务生成分析
            ai_service = AIGeneratorService(settings.DEEPSEEK_API_KEY)

            # 构建分析提示词
            prompt = f"""
请分析以下测试执行日志，找出失败原因并给出建议：

执行日志：
{log_content}

请提供：
1. **失败原因分析**：简要说明测试失败的主要原因
2. **问题定位**：指出可能的问题位置（文件名、行号等）
3. **解决建议**：给出具体的解决方案

分析要求：
- 语言简洁明了
- 突出关键信息
- 提供可操作的建议
"""

            # 调用AI生成分析
            from langchain.chains import LLMChain
            from langchain.prompts import PromptTemplate
            from langchain_openai import ChatOpenAI

            if not ai_service.llm:
                return "AI服务未初始化，无法进行分析"

            prompt_template = PromptTemplate(
                template=prompt,
                input_variables=[]
            )

            chain = LLMChain(llm=ai_service.llm, prompt=prompt_template)
            analysis = chain.run()

            return analysis

        except Exception as e:
            logger.error(f"生成AI分析失败: {str(e)}")
            return f"AI分析失败: {str(e)}"

    def delete_report(self, report_id: int) -> bool:
        """删除报告"""
        report = self.get_report(report_id)
        if not report:
            return False

        # 删除报告文件
        try:
            if report.report_path and os.path.exists(report.report_path):
                os.remove(report.report_path)
        except Exception as e:
            logger.error(f"删除报告文件失败: {str(e)}")

        # 删除数据库记录
        self.db.delete(report)
        self.db.commit()

        logger.info(f"删除测试报告: ID={report_id}")
        return True
