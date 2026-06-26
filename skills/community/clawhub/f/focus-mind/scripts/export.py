#!/usr/bin/env python3
"""
FocusMind 导出模块
支持导出分析结果为多种格式
"""

import json
import os
from typing import Any, Dict, Optional
from datetime import datetime


class Exporter:
    """
    导出器
    
    支持导出为 Markdown、JSON、HTML 格式
    """
    
    @staticmethod
    def to_markdown(health: Dict, summary: Dict, goals: Dict) -> str:
        """导出为 Markdown"""
        lines = [
            "# FocusMind 分析报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 上下文健康度",
            "",
            f"- **评分**: {health['score']}/100 {health['emoji']}",
            f"- **状态**: {health['label']}",
            f"- **Token 数**: {health['details']['token_count']}",
            f"- **重复率**: {health['details']['repetition_ratio']}%",
            "",
            "### 建议",
        ]
        
        for rec in health.get('recommendations', []):
            lines.append(f"- {rec}")
        
        lines.extend([
            "",
            "## 上下文摘要",
            "",
            summary.get('summary', '无'),
            "",
            "## 目标提取",
            "",
        ])
        
        if goals.get('main_goal'):
            lines.extend([
                f"### 核心目标",
                goals['main_goal'],
                "",
            ])
        
        if goals.get('sub_goals'):
            lines.append("### 子目标")
            for g in goals['sub_goals']:
                status = "✓" if g.get('completed') else "○"
                lines.append(f"- {status} {g['content']}")
            lines.append("")
        
        if goals.get('pending'):
            lines.append("### 待完成")
            for p in goals['pending']:
                lines.append(f"- {p}")
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def to_json(health: Dict, summary: Dict, goals: Dict, pretty: bool = True) -> str:
        """导出为 JSON"""
        data = {
            "generated_at": datetime.now().isoformat(),
            "health": health,
            "summary": summary,
            "goals": goals
        }
        
        if pretty:
            return json.dumps(data, ensure_ascii=False, indent=2)
        return json.dumps(data, ensure_ascii=False)
    
    @staticmethod
    def to_html(health: Dict, summary: Dict, goals: Dict) -> str:
        """导出为 HTML"""
        # 状态颜色
        level_colors = {
            "green": "#4caf50",
            "yellow": "#ff9800",
            "red": "#f44336"
        }
        color = level_colors.get(health['level'], "#666")
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>FocusMind 分析报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #555; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .health {{ background: {color}20; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .score {{ font-size: 2em; font-weight: bold; color: {color}; }}
        .meta {{ color: #888; font-size: 0.9em; }}
        .recommendations {{ background: #f5f5f5; padding: 15px; border-radius: 8px; }}
        .todo {{ margin: 10px 0; }}
        .done {{ text-decoration: line-through; color: #888; }}
    </style>
</head>
<body>
    <h1>🧠 FocusMind 分析报告</h1>
    <p class="meta">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="health">
        <h2>上下文健康度</h2>
        <div class="score">{health['score']}/100 {health['emoji']}</div>
        <p><strong>状态:</strong> {health['label']}</p>
        <p><strong>Token 数:</strong> {health['details']['token_count']}</p>
        <p><strong>重复率:</strong> {health['details']['repetition_ratio']}%</p>
    </div>
    
    <h2>建议</h2>
    <div class="recommendations">
        <ul>
"""
        
        for rec in health.get('recommendations', []):
            html += f"            <li>{rec}</li>\n"
        
        html += """        </ul>
    </div>
    
    <h2>上下文摘要</h2>
    <pre>"""
        html += summary.get('summary', '无').replace('<', '&lt;').replace('>', '&gt;')
        html += """</pre>
    
    <h2>目标提取</h2>
"""
        
        if goals.get('main_goal'):
            html += f"    <h3>核心目标</h3>\n    <p>{goals['main_goal']}</p>\n"
        
        if goals.get('sub_goals'):
            html += "    <h3>子目标</h3>\n    <ul>\n"
            for g in goals['sub_goals']:
                status = "✓" if g.get('completed') else "○"
                cls = "done" if g.get('completed') else ""
                html += f'        <li class="{cls}">{status} {g["content"]}</li>\n'
            html += "    </ul>\n"
        
        if goals.get('pending'):
            html += "    <h3>待完成</h3>\n    <ul>\n"
            for p in goals['pending']:
                html += f"        <li>{p}</li>\n"
            html += "    </ul>\n"
        
        html += """</body>
</html>"""
        
        return html
    
    @staticmethod
    def export(health: Dict, summary: Dict, goals: Dict, 
               filepath: str, format: Optional[str] = None) -> bool:
        """
        导出到文件
        
        Args:
            health: 健康度数据
            summary: 摘要数据
            goals: 目标数据
            filepath: 输出文件路径
            format: 格式 (markdown/json/html)，如果为 None 则根据文件扩展名自动判断
        
        Returns:
            是否成功
        """
        # 自动判断格式
        if format is None:
            ext = os.path.splitext(filepath)[1].lower()
            format = ext[1:] if ext else "markdown"
        
        format = format.lower()
        
        # 根据格式导出
        if format == "markdown" or format == "md":
            content = Exporter.to_markdown(health, summary, goals)
        elif format == "json":
            content = Exporter.to_json(health, summary, goals)
        elif format == "html":
            content = Exporter.to_html(health, summary, goals)
        else:
            print(f"❌ 不支持的格式: {format}")
            return False
        
        # 写入文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 已导出到: {filepath}")
            return True
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False


# 便捷函数
def export_report(health: Dict, summary: Dict, goals: Dict, 
                  filepath: str, format: Optional[str] = None) -> bool:
    """导出报告"""
    return Exporter.export(health, summary, goals, filepath, format)


# 导出
__all__ = ["Exporter", "export_report"]
