#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业AI应用诊断工具 - HTML报告生成器
"""

import os
from datetime import datetime
from typing import Dict, List, Any

class EnterpriseReportHTMLGenerator:
    """企业AI诊断报告HTML生成器"""
    
    def __init__(self):
        """初始化"""
        pass
    
    def generate_html_report(self,
                            enterprise_info: Dict,
                            process_analysis: Dict,
                            roi_analysis: Dict,
                            implementation_plan: Dict) -> str:
        """
        生成HTML格式的企业AI诊断报告
        
        Args:
            enterprise_info: 企业信息
            process_analysis: 流程分析
            roi_analysis: ROI分析
            implementation_plan: 实施计划
            
        Returns:
            HTML格式的报告
        """
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>企业AI应用诊断报告 - {enterprise_info['basic_info']['company_name']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .roi-card {{
            background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
            color: white;
            padding: 40px;
            text-align: center;
            margin: 30px 0;
            border-radius: 15px;
        }}
        .roi-card h2 {{
            font-size: 3em;
            margin-bottom: 20px;
        }}
        .roi-card .value {{
            font-size: 4em;
            font-weight: bold;
            margin: 20px 0;
        }}
        .content {{
            padding: 40px;
        }}
        .process-card {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border-left: 5px solid #667eea;
        }}
        .score-circle {{
            display: inline-block;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            line-height: 80px;
            font-size: 24px;
            font-weight: bold;
            margin-right: 20px;
        }}
        .scenario-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }}
        .phase-card {{
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        .footer {{
            background: #2d3436;
            color: white;
            padding: 30px;
            text-align: center;
            margin-top: 40px;
        }}
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 企业AI应用诊断报告</h1>
            <div class="subtitle">
                <div>企业名称：{enterprise_info['basic_info']['company_name']}</div>
                <div>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
        </div>
        
        <div class="content">
            <div class="roi-card">
                <h2>💰 ROI分析</h2>
                <div class="value">{roi_analysis['roi_percentage']}%</div>
                <p style="font-size: 1.3em;">投资回报率</p>
                <div style="margin-top: 30px; font-size: 1.1em;">
                    <p>总投入：{roi_analysis['total_investment']}元</p>
                    <p>年化收益：{roi_analysis['annual_savings']}元</p>
                    <p>回报周期：{roi_analysis['payback_months']}个月</p>
                </div>
            </div>
            
            <h2 style="text-align: center; margin: 40px 0; color: #2d3436;">📊 业务流程AI适用性分析</h2>
"""
        
        # 添加流程分析
        for name, data in process_analysis.items():
            score_color = '#00b894' if data['ai_score'] >= 80 else ('#fdcb6e' if data['ai_score'] >= 60 else '#e17055')
            
            html += f"""
            <div class="process-card">
                <div style="display: flex; align-items: center; margin-bottom: 20px;">
                    <div class="score-circle" style="background: {score_color};">{data['ai_score']}</div>
                    <div>
                        <h3 style="font-size: 1.5em; color: #2d3436;">{name}</h3>
                        <p style="color: #636e72;">AI适用性评分：{data['ai_score']}/100</p>
                    </div>
                </div>
                
                <div style="margin: 20px 0;">
                    <h4 style="color: #2d3436; margin-bottom: 10px;">当前成本</h4>
                    <p>⏱️ 时间成本：{data['time_cost']}小时/月</p>
                    <p>💵 人力成本：{data['labor_cost']}元/月</p>
                    <p>⚠️ 痛点级别：{data['pain_level']}</p>
                </div>
                
                <div style="margin: 20px 0;">
                    <h4 style="color: #2d3436; margin-bottom: 10px;">推荐的AI应用场景</h4>
"""
            
            for scenario in data['ai_scenarios']:
                html += f"""
                    <div class="scenario-card">
                        <strong>🎯 {scenario['name']}</strong><br>
                        <span style="color: #636e72;">预估节省：{scenario['savings']}</span><br>
                        <span style="color: #636e72;">实施难度：{scenario['difficulty']}</span>
                    </div>
"""
            
            html += f"""
                </div>
                
                <div style="background: #dfe6e9; padding: 15px; border-radius: 10px; margin-top: 20px;">
                    <h4 style="color: #2d3436; margin-bottom: 10px;">预估收益</h4>
                    <p>✅ 时间节省：{data['estimated_savings']['time_savings_hours']}小时/月</p>
                    <p>✅ 成本节省：{data['estimated_savings']['labor_savings_yuan']}元/月</p>
                    <p>✅ 节省比例：{data['estimated_savings']['savings_ratio']}</p>
                </div>
            </div>
"""
        
        # 添加实施计划
        html += """
            <h2 style="text-align: center; margin: 40px 0; color: #2d3436;">🚀 实施路径规划</h2>
"""
        
        for phase_key, phase_data in implementation_plan.items():
            phase_num = phase_key.split('phase')[1]
            html += f"""
            <div class="phase-card">
                <h3 style="font-size: 1.8em; margin-bottom: 15px;">阶段{phase_num}：{phase_data['timeline']}</h3>
                <p style="font-size: 1.2em; margin-bottom: 20px;">🎯 {phase_data['goal']}</p>
                
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <h4 style="margin-bottom: 10px;">优先实施流程：</h4>
                    <ul style="margin-left: 20px;">
"""
            
            for process in phase_data['processes']:
                html += f"                        <li>{process}</li>\n"
            
            html += """                    </ul>
                </div>
"""
            
            if phase_data.get('tools'):
                html += f"""
                <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <h4 style="margin-bottom: 10px;">推荐工具：</h4>
                    <ul style="margin-left: 20px;">
"""
                for tool in phase_data['tools']:
                    html += f"                        <li>{tool}</li>\n"
                html += """                    </ul>
                </div>
"""
            
            html += f"""
                <p style="font-size: 1.1em; margin-top: 15px;">✨ <strong>预期效果</strong>：{phase_data['expected_result']}</p>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="footer">
            <h3>📞 后续支持</h3>
            <p style="margin-top: 15px;">如需进一步咨询或定制方案，请联系：</p>
            <p style="margin-top: 10px;">📧 邮箱：87287416@qq.com</p>
            <p style="margin-top: 10px;">💬 飞书：@胡大大</p>
            <p style="margin-top: 30px; opacity: 0.7;">
                报告生成：企业AI应用诊断工具 v1.0<br>
                小龙虾协助制作 🦞
            </p>
        </div>
    </div>
</body>
</html>
"""
        
        return html


def generate_and_save_html_report(enterprise_info, process_analysis, roi_analysis, implementation_plan, output_dir):
    """
    生成并保存HTML报告
    
    Args:
        enterprise_info: 企业信息
        process_analysis: 流程分析
        roi_analysis: ROI分析
        implementation_plan: 实施计划
        output_dir: 输出目录
        
    Returns:
        HTML文件路径
    """
    generator = EnterpriseReportHTMLGenerator()
    html_content = generator.generate_html_report(
        enterprise_info, process_analysis, roi_analysis, implementation_plan
    )
    
    # 生成文件名
    company_name = enterprise_info['basic_info']['company_name'].replace(' ', '_').replace('/', '_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{company_name}_AI诊断报告_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)
    
    # 保存HTML
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath
