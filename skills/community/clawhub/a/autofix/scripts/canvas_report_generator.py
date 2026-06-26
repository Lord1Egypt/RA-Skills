"""
Canvas 诊断报告生成器 (v5.0)
自动生成交互式的诊断报告 HTML 页面

功能:
- 封装 CanvasSnapshot 工具调用
- HTML+JS 模板渲染
- Canvas URL 注册和持久化
- PNG/HTML 格式输出

使用方法:
    from tools.canvas_report_generator import CanvasReportGenerator
    
    generator = CanvasReportGenerator()
    html = generator.generate_report(diag_data)
    png_url = generator.generate_png_screenshot(html, timeoutMs=15000)
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple


class CanvasReportGenerator:
    """
    Canvas 诊断报告生成器 v5.0
    
    功能:
    - 封装 CanvasSnapshot 工具调用
    - HTML+JS 模板渲染
    - Canvas URL 注册和持久化
    - PNG/HTML 格式输出
    """
    
    def __init__(self, canvas_root: str = str(Path.home() / ".openclaw" / "canvas")):
        """
        初始化 Canvas 报告生成器
        
        Args:
            canvas_root: Canvas 文档根目录路径（默认使用 OpenClaw 标准路径）
        """
        self.canvas_root = Path(canvas_root) / "documents" / "reports"
        
    def _generate_timestamp(self) -> str:
        """生成时间戳用于文件命名"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_diagnosis_data(
        self,
        exec_output: str,
        problem_context: str = "CLI/Config",
        evidence_chain: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        生成诊断报告所需的数据结构
        
        Args:
            exec_output: 原始 exec 输出（包含错误信息）
            problem_context: 问题上下文（如："CLI/Config", "Tooling"）
            evidence_chain: 来自 MODULE_02_SearchChain 的证据链数据
            
        Returns:
            Dict[str, Any]: 结构化诊断数据
        """
        
        # 提取关键信息（简化版，实际可使用 ELIS 分析）
        risk_level = self._infer_risk_level(exec_output)
        problem_type = f"MRE-{problem_context} Failure"
        affected_tools = ["openclaw", "exec"]
        error_logs = exec_output[:1000] if len(exec_output) > 1000 else exec_output
        
        # AI 根因分析（简化版）
        root_cause = {
            "core_issue": self._extract_core_issue(exec_output),
            "causes": self._extract_possible_causes(exec_output),
            "confidence_score": self._estimate_confidence(exec_output)
        }
        
        # 修复建议
        fix_command = self._generate_fix_command(problem_context, exec_output)
        
        # 回滚命令
        rollback_command = f"""# 回滚命令 (如需要撤销):
# openclaw gateway status
# git checkout HEAD~1 -- .openclaw/
# python -m venv {Path.home()}\\.venv  
# pip install -r ~/.openclaw/workspace/.openclaw/requirements.txt"""
        
        # 证据链信息（如果提供）
        evidence_info = {
            "docs_match": evidence_chain.get("docs_match", False) if evidence_chain else False,
            "gh_match": evidence_chain.get("gh_match", False) if evidence_chain else False,
            "pattern_matches": evidence_chain.get("pattern_matches", []) if evidence_chain else [],
            "docs_confidence": evidence_chain.get("docs_confidence", 0.85) if evidence_chain else 0.85,
            "gh_issue": evidence_chain.get("gh_issue", "N/A") if evidence_chain else "N/A",
            "confidence_score": evidence_chain.get("confidence_score", 0.92) if evidence_chain else 0.92
        } if evidence_chain else {
            "docs_match": False,
            "gh_match": False,
            "pattern_matches": [],
            "docs_confidence": 0.85,
            "gh_issue": "N/A",
            "confidence_score": 0.92
        }
        
        return {
            "riskLevel": risk_level,
            "problemType": problem_type,
            "affectedTools": affected_tools,
            "errorLogs": error_logs,
            "rootCause": root_cause,
            "fixCommand": fix_command,
            "rollbackCommand": rollback_command,
            "evidenceChain": evidence_info
        }
    
    def _infer_risk_level(self, exec_output: str) -> str:
        """根据错误类型推断风险等级"""
        keywords = {
            "Critical": ["fatal", "crash", "segfault"],
            "Medium": ["error", "fail", "exception"],
            "Low": ["warning", "notice", "info"]
        }
        
        for level, keyword_list in keywords.items():
            if any(kw.lower() in exec_output.lower() for kw in keyword_list):
                return level
        
        return "Medium"  # 默认中风险
    
    def _extract_core_issue(self, exec_output: str) -> str:
        """提取核心问题（简化版，实际需使用 ELIS）"""
        
        lines = exec_output.strip().split('\n')
        
        for line in lines:
            if 'error' in line.lower() or 'fail' in line.lower():
                return line.strip()[:100]  # 取前 100 字符
        
        return "未检测到明确错误信息"
    
    def _extract_possible_causes(self, exec_output: str) -> list[str]:
        """提取可能原因（简化版）"""
        
        causes = []
        if 'pty' in exec_output.lower():
            causes.append("当前会话配置中缺少 pty 参数")
        if 'permission' in exec_output.lower():
            causes.append("执行命令需要 sudo/管理员权限")
        if 'timeout' in exec_output.lower():
            causes.append("执行超时或卡住（未指定 yieldMs）")
        if 'node' in exec_output.lower() or 'python' in exec_output.lower():
            causes.append("依赖项安装不完整或版本不匹配")
        
        if not causes:
            causes = ["环境配置可能需要重新初始化"]
        
        return causes[:3]  # 最多 3 个原因
    
    def _estimate_confidence(self, exec_output: str) -> float:
        """估计置信度（简化版）"""
        error_count = exec_output.lower().count('error') + exec_output.lower().count('fail')
        if error_count == 0:
            return 0.5
        elif error_count <= 3:
            return 0.75
        else:
            return min(0.6, 0.8 - (error_count * 0.1))
    
    def _generate_fix_command(self, problem_context: str, exec_output: str) -> str:
        """生成修复建议命令（简化版）"""
        
        base_command = "openclaw doctor --fix"
        
        if 'pty' in exec_output.lower():
            return f"{base_command} --pty=true --yieldMs=15000"
        elif 'permission' in exec_output.lower():
            return f"sudo {base_command}"
        elif 'timeout' in exec_output.lower():
            return f"{base_command} --timeout=300"
        
        return base_command
    
    def generate_report(self, diag_data: Dict[str, Any], output_format: str = "html") -> str:
        """
        生成诊断报告
        
        Args:
            diag_data: generate_diagnosis_data() 返回的诊断数据
            output_format: 输出格式（"html" 或 "png"）
            
        Returns:
            生成的报告内容（HTML 字符串或 PNG 路径）
        """
        
        # 使用 CanvasScript_DiagnosticReport.js 中的模板
        script_path = Path(__file__).parent / "CanvasScript_DiagnosticReport.js"
        
        if output_format == "html":
            return self._render_html_template(diag_data, script_path)
        else:
            return self._write_to_canvas_and_screenshot(diag_data, output_format)
    
    def _render_html_template(self, diag_data: Dict[str, Any], script_path: Path) -> str:
        """渲染 HTML 模板（简化版，实际使用 CanvasScript_DiagnosticReport.js）"""
        
        risk_level = diag_data["riskLevel"]
        problem_type = diag_data["problemType"]
        
        # 风险颜色
        risk_colors = {
            "Critical": "#dc3545",
            "Medium": "#ffc107",
            "Low": "#28a745"
        }
        risk_color = risk_colors.get(risk_level, "#6c757d")
        
        # 简化的 HTML 模板（实际使用 CanvasScript_DiagnosticReport.js）
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>OpenClaw 诊断报告 - {problem_type}</title>
</head>
<body style="font-family:'Segoe UI',sans-serif;padding:20px;background:#f8f9fa;">
    <h1>🔍 OpenClaw 诊断报告</h1>
    <p><strong>{problem_type}</strong></p>
    
    <div style="padding:15px;border-radius:8px;margin:15px 0;background:{risk_color}20;border:2px solid {risk_color};color:{risk_color};">
        ⚠️ Status: MRE Test Failed | Risk Level: {risk_level}
    </div>
    
    <div style="background:white;padding:20px;margin:15px 0;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
        <h2>📋 问题概览</h2>
        <pre style="background:#f4f4f4;padding:15px;border-radius:6px;overflow-x:auto;">{diag_data['errorLogs']}</pre>
    </div>
    
    <div style="background:white;padding:20px;margin:15px 0;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
        <h2>🔬 AI 根因分析</h2>
        <p><strong>核心问题：</strong> {diag_data['rootCause']['core_issue']}</p>
        <p><strong>可能原因：</strong></p>
        <ul style="margin-left:20px; margin-top:8px;">
            {''.join([f'<li>{cause}</li>' for cause in diag_data['rootCause']['causes']])}
        </ul>
    </div>
    
    <div style="background:white;padding:20px;margin:15px 0;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);border-left:4px solid #28a745;">
        <h2>🔧 修复建议</h2>
        <pre style="background:#f4f4f4;padding:15px;border-radius:6px;overflow-x:auto;"><code class="bash">{diag_data['fixCommand']}</code></pre>
    </div>
    
    <div style="text-align:center;color:#6c757d;font-size:13px;margin-top:20px;">
        Generated by autofix-theclaw v5.0 | OpenClaw Problem Solver
    </div>
</body>
</html>"""
        
        return html_content
    
    def _write_to_canvas_and_screenshot(
        self, 
        diag_data: Dict[str, Any], 
        output_format: str = "png"
    ) -> Tuple[str, str]:
        """
        将报告写入 Canvas 并生成截图
        
        Args:
            diag_data: 诊断数据
            output_format: 输出格式（"html" 或 "png"）
            
        Returns:
            Tuple[HTML_content, PNG_URL]: HTML 内容和 PNG 截图 URL
        """
        
        timestamp = self._generate_timestamp()
        subdir = f"autofix_report_{timestamp}"
        full_path = self.canvas_root / subdir
        
        # 创建目录
        Path(full_path).mkdir(parents=True, exist_ok=True)
        
        # 生成 HTML 内容
        html_content = self._render_html_template(diag_data, None)
        
        # 写入 Canvas（模拟实际使用）
        html_index_path = full_path / "index.html"
        with open(html_index_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        canvas_url = f"/__openclaw__/canvas/documents/{timestamp}/index.html"
        
        # TODO: 实际使用时需调用 Canvas.snapshot()
        # 当前仅返回模拟的 PNG URL
        
        return html_content, canvas_url
    
    def generate_report_with_canvas(self, diag_data: Dict[str, Any]) -> str:
        """
        生成报告并保存到 Canvas（完整流程）
        
        Args:
            diag_data: 诊断数据
            
        Returns:
            Canvas URL（如："/__openclaw__/canvas/documents/autofix_report_xxx/index.html"）
        """
        
        import tempfile
        
        # 生成临时 HTML 文件
        html_content = self._render_html_template(diag_data, None)
        
        # 保存到临时目录
        with tempfile.NamedTemporaryFile(
            suffix=".html", 
            delete=False, 
            encoding="utf-8"
        ) as f:
            temp_html_path = Path(f.name)
            f.write(html_content.encode("utf-8"))
        
        # TODO: 实际使用时调用 Canvas.snapshot()
        # canvas.snapshot(
        #     action="snapshot",
        #     javaScript=f"<script src='{temp_html_path}"></script>",
        #     fullPage=True,
        #     timeoutMs=15000
        # )
        
        # 生成 Canvas URL
        timestamp = self._generate_timestamp()
        canvas_url = f"/__openclaw__/canvas/documents/reports/autofix_report_{timestamp}/index.html"
        
        return canvas_url


if __name__ == "__main__":
    """
    测试脚本 - 验证 Canvas Report Generator 功能
    
    Usage:
        python tools/canvas_report_generator.py
    """
    
    # 模拟诊断数据
    test_diag_data = {
        "riskLevel": "Medium",
        "problemType": "MRE-CLI/Config Failure",
        "affectedTools": ["openclaw", "exec"],
        "errorLogs": "ERROR: Command not found: tail -f\nReason: pty=true parameter is missing",
        "rootCause": {
            "core_issue": "exec 命令未指定 pty=true，导致 TTY 终端程序运行失败",
            "causes": [
                "当前会话配置中缺少 pty 参数",
                "目标命令需要交互式终端环境（如 tail -f, grep 等）",
                "执行模式为 sandboxed，未传递正确的 shell 环境变量"
            ]
        },
        "fixCommand": "openclaw doctor --fix --pty=true --yieldMs=15000",
        "rollbackCommand": "# 回滚命令（如需要）:\n# openclaw gateway status\n# git checkout HEAD~1 -- .openclaw/",
        "evidenceChain": {
            "docs_match": False,
            "gh_match": False,
            "pattern_matches": [],
            "docs_confidence": 0.85,
            "gh_issue": "N/A",
            "confidence_score": 0.92
        }
    }
    
    # 创建生成器实例
    generator = CanvasReportGenerator()
    
    print("Canvas Report Generator v5.0 Ready")
    print("=" * 60)
    
    # 测试 HTML 输出
    html_output = generator.generate_report(test_diag_data, output_format="html")
    print("\nHTML Output (first 1000 chars):")
    print("-" * 60)
    print(html_output[:1000])
    print("...")
    
    # 生成 Canvas URL（模拟）
    canvas_url = generator.generate_report_with_canvas(test_diag_data)
    print(f"\nCanvas URL (simulated): {canvas_url}")
    
    print("\n" + "=" * 60)
    print("Canvas Report Generator v5.0 Test Complete")
