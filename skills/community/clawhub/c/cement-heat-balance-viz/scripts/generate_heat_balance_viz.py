#!/usr/bin/env python3
"""
Cement Heat Balance Visualization Generator
Generates HTML visualizations for cement production heat balance data
"""

import json
import os
from typing import Dict, List, Any


def generate_heat_balance_html(data: Dict[str, Any]) -> str:
    """
    Generate HTML visualization for cement heat balance data
    
    Args:
        data: Dictionary containing heat balance information
        
    Returns:
        HTML string with visualization
    """
    
    # Extract data with defaults
    process_stages = data.get('process_stages', [
        {"name": "生料喂入", "temp": 25, "type": "cold", "label": "环境温度"},
        {"name": "第1、2级预热器", "temp": 400, "type": "normal", "label": "煤粉干燥"},
        {"name": "3、4级预热器", "temp": 700, "type": "normal", "label": "石灰石分解"},
        {"name": "窑头尾气", "temp": 900, "type": "hot", "label": "热回收"},
        {"name": "窑腔", "temp": 1450, "type": "hot", "label": "熟料形成"}
    ])
    
    energy_distribution = data.get('energy_distribution', [
        {"item": "成品熟料 (Cl)", "percentage": 45, "description": "有效产热"},
        {"item": "窑筒散热", "percentage": 15, "description": "窑外壳散热"},
        {"item": "排烟损失", "percentage": 12, "description": "排出的热量"},
        {"item": "机械搅拌", "percentage": 8, "description": "物料搅拌"},
        {"item": "生料干燥", "percentage": 10, "description": "水分去除"},
        {"item": "预热器损失", "percentage": 5, "description": "预热不完全"},
        {"item": "其他损失", "percentage": 5, "description": "各种未计损失"}
    ])
    
    kpis = data.get('kpis', [
        {"value": "45%", "label": "有效利用率"},
        {"value": "850 kcal/kg", "label": "标准产热量"},
        {"value": "65%", "label": "热回收率"},
        {"value": "2.5", "label": "理论煤耗指数"}
    ])
    
    # Generate process flow HTML
    process_flow_items = ""
    for stage in process_stages:
        process_flow_items += f'''
                <div class="process-unit {stage['type']}">
                    <div>{stage['name']}</div>
                    <div class="temp-display">{stage['temp']}°C</div>
                    <div class="temp-label">{stage['label']}</div>
                </div>'''
    
    # Generate energy distribution table
    energy_table_rows = ""
    for item in energy_distribution:
        energy_table_rows += f'''
                    <tr>
                        <td>{item['item']}</td>
                        <td>{item['percentage']}%</td>
                        <td>{item['description']}</td>
                    </tr>'''
    
    # Generate KPI cards
    kpi_cards = ""
    for kpi in kpis:
        kpi_cards += f'''
                <div class="kpi-card">
                    <div class="kpi-value">{kpi['value']}</div>
                    <div class="kpi-label">{kpi['label']}</div>
                </div>'''
    
    html_template = f'''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>水泥生产热平衡分析</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #00d9ff; margin-bottom: 30px; font-size: 2.5em; }}
        h2 {{ color: #ff6b6b; border-bottom: 2px solid #ff6b6b; padding-bottom: 10px; margin: 20px 0; }}
        
        .section {{
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
        }}
        
        .process-flow {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }}
        
        .process-unit {{
            background: linear-gradient(145deg, #2a2a4a, #1e1e3f);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            min-width: 150px;
            border: 2px solid #00d9ff;
            transition: transform 0.3s;
        }}
        
        .process-unit:hover {{ transform: scale(1.05); }}
        .process-unit.hot {{ border-color: #ff6b6b; }}
        .process-unit.cold {{ border-color: #4dabf7; }}
        
        .temp-display {{
            font-size: 2em;
            font-weight: bold;
            color: #ffd43b;
            margin: 10px 0;
        }}
        
        .temp-label {{ color: #aaa; font-size: 0.9em; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }}
        
        th {{ background: rgba(0,217,255,0.2); color: #00d9ff; }}
        tr:hover {{ background: rgba(255,255,255,0.05); }}
        
        .energy-bar {{
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            height: 30px;
            margin: 10px 0;
            overflow: hidden;
        }}
        
        .energy-fill {{
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            transition: width 1s;
        }}
        
        .coal {{ background: linear-gradient(90deg, #868e96, #495057); }}
        .coal-fill {{ background: linear-gradient(90deg, #ffd43b, #fab005); }}
        
        .heat-input {{ background: linear-gradient(90deg, #4dabf7, #2a9df4); }}
        .heat-output {{ background: linear-gradient(90deg, #ff6b6b, #ff5252); }}
        
        .formula {{
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            overflow-x: auto;
        }}
        
        .highlight {{ color: #ffd43b; font-weight: bold; }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .kpi-card {{
            background: linear-gradient(145deg, #2a2a4a, #1e1e3f);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}
        
        .kpi-value {{ font-size: 2em; color: #00d9ff; font-weight: bold; }}
        .kpi-label {{ color: #aaa; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 水泥生产热平衡分析</h1>
        
        <div class="section">
            <h2>📊 热平衡概述</h2>
            <p>水泥生产过程中的热平衡是指能量输入与输出的分析，包括燃料燃烧产生的热量、各种热损失及有效利用的热量比例。</p>
        </div>
        
        <div class="section">
            <h2>🏭 生产流程温度分布</h2>
            <div class="process-flow">
{process_flow_items}
            </div>
        </div>
        
        <div class="section">
            <h2>⚡ 能量流分析</h2>
            <h3>热量输入 (100%)</h3>
            <div class="energy-bar">
                <div class="energy-fill coal-fill" style="width: 100%">煤 powder: 100%</div>
            </div>
            
            <h3>热量输出分布</h3>
            <table>
                <thead>
                    <tr>
                        <th>项目</th>
                        <th>热量占比</th>
                        <th>说明</th>
                    </tr>
                </thead>
                <tbody>
{energy_table_rows}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>📈 关键指标</h2>
            <div class="kpi-grid">
{kpi_cards}
            </div>
        </div>
        
        <div class="section">
            <h2>🔢 热平衡公式</h2>
            <div class="formula">
                <p>热平衡方程:</p>
                <p>Q<sub>煤</sub> = Q<sub>产物</sub> + Q<sub>散热</sub> + Q<sub>排烟</sub> + Q<sub>其他</sub></p>
                <br>
                <p>煤耗计算:</p>
                <p>k = (Q<sub>产物</sub> + Q<sub>散热</sub> + Q<sub>排烟</sub>) / m<sub>熟料</sub> × 100%</p>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html_template


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate cement heat balance visualization')
    parser.add_argument('--input', '-i', help='Input JSON file with heat balance data')
    parser.add_argument('--output', '-o', default='heat_balance_viz.html', help='Output HTML file')
    parser.add('--data', '-d', help='JSON string with heat balance data')
    
    args = parser.parse_args()
    
    # Load data
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif args.data:
        data = json.loads(args.data)
    else:
        # Use default data
        data = {}
    
    # Generate HTML
    html_content = generate_heat_balance_html(data)
    
    # Write output
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Visualization generated: {args.output}")


if __name__ == "__main__":
    main()