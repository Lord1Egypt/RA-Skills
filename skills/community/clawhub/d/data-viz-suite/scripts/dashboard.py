"""
Dashboard - 交互式仪表盘
"""

import json
from typing import Dict, List, Optional, Any
from plotly.graph_objects import Figure as PlotlyFigure


class Dashboard:
    """交互式仪表盘"""
    
    def __init__(self, title: str = '数据仪表盘', theme: str = 'light',
                 layout: str = 'grid'):
        self.title = title
        self.theme = theme
        self.layout = layout
        self.charts: Dict[str, Any] = {}
        self.kpis: List[Dict] = []
        self.tables: List[Dict] = []
    
    def add_chart(self, chart_id: str, fig: Any, title: str = ''):
        """添加图表"""
        self.charts[chart_id] = {
            'figure': fig,
            'title': title or chart_id
        }
    
    def add_kpi(self, title: str, value: Any, change: Optional[float] = None,
                prefix: str = '', suffix: str = ''):
        """添加KPI指标"""
        self.kpis.append({
            'title': title,
            'value': value,
            'change': change,
            'prefix': prefix,
            'suffix': suffix
        })
    
    def add_table(self, title: str, data: Any, columns: Optional[List[str]] = None):
        """添加数据表"""
        import pandas as pd
        
        if hasattr(data, 'to_dict'):  # DataFrame
            table_data = data.to_dict('records')
            table_columns = columns or list(data.columns)
        else:
            table_data = data
            table_columns = columns or list(data[0].keys()) if data else []
        
        self.tables.append({
            'title': title,
            'data': table_data,
            'columns': table_columns
        })
    
    def _generate_html(self) -> str:
        """生成HTML"""
        # 基础样式
        if self.theme == 'dark':
            bg_color = '#1a1a1a'
            text_color = '#ffffff'
            card_bg = '#2d2d2d'
        else:
            bg_color = '#f5f5f5'
            text_color = '#333333'
            card_bg = '#ffffff'
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: {bg_color};
            color: {text_color};
        }}
        .dashboard-title {{
            text-align: center;
            font-size: 28px;
            margin-bottom: 30px;
            color: {text_color};
        }}
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .kpi-card {{
            background: {card_bg};
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .kpi-title {{
            font-size: 14px;
            color: #888;
            margin-bottom: 8px;
        }}
        .kpi-value {{
            font-size: 32px;
            font-weight: bold;
            color: {text_color};
        }}
        .kpi-change {{
            font-size: 14px;
            margin-top: 8px;
        }}
        .kpi-change.positive {{ color: #4caf50; }}
        .kpi-change.negative {{ color: #f44336; }}
        .charts-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .chart-card {{
            background: {card_bg};
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 18px;
            margin-bottom: 15px;
            color: {text_color};
        }}
        .table-container {{
            background: {card_bg};
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
            color: {text_color};
        }}
        th {{
            background-color: rgba(128,128,128,0.1);
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <h1 class="dashboard-title">{self.title}</h1>
"""
        
        # 添加KPI区域
        if self.kpis:
            html += '    <div class="kpi-container">\n'
            for kpi in self.kpis:
                change_html = ''
                if kpi['change'] is not None:
                    change_class = 'positive' if kpi['change'] >= 0 else 'negative'
                    sign = '+' if kpi['change'] >= 0 else ''
                    change_html = f'<div class="kpi-change {change_class}">{sign}{kpi["change"]:.1f}%</div>'
                
                value_str = f"{kpi['prefix']}{kpi['value']}{kpi['suffix']}"
                html += f"""
        <div class="kpi-card">
            <div class="kpi-title">{kpi['title']}</div>
            <div class="kpi-value">{value_str}</div>
            {change_html}
        </div>
"""
            html += '    </div>\n'
        
        # 添加图表区域
        if self.charts:
            html += '    <div class="charts-container">\n'
            for chart_id, chart_info in self.charts.items():
                html += f"""
        <div class="chart-card">
            <div class="chart-title">{chart_info['title']}</div>
            <div id="chart-{chart_id}"></div>
        </div>
"""
            html += '    </div>\n'
        
        # 添加表格区域
        for table in self.tables:
            html += '    <div class="table-container">\n'
            html += f'        <h3>{table["title"]}</h3>\n'
            html += '        <table>\n            <tr>\n'
            for col in table['columns']:
                html += f'                <th>{col}</th>\n'
            html += '            </tr>\n'
            for row in table['data'][:50]:  # 最多显示50行
                html += '            <tr>\n'
                for col in table['columns']:
                    val = row.get(col, '')
                    html += f'                <td>{val}</td>\n'
                html += '            </tr>\n'
            html += '        </table>\n'
            html += '    </div>\n'
        
        # 添加图表渲染脚本
        html += '    <script>\n'
        for chart_id, chart_info in self.charts.items():
            fig = chart_info['figure']
            if hasattr(fig, 'to_json'):
                fig_json = fig.to_json()
                html += f"""
        Plotly.newPlot('chart-{chart_id}', {fig_json}.data, {fig_json}.layout, {{responsive: true}});
"""
        html += '    </script>\n'
        
        html += '</body>\n</html>'
        return html
    
    def save(self, path: str):
        """保存仪表盘为HTML"""
        html = self._generate_html()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"仪表盘已保存到: {path}")


if __name__ == '__main__':
    from chart_engine import ChartEngine
    
    dash = Dashboard(title='测试仪表盘', theme='dark')
    dash.add_kpi('销售额', 1250000, change=12.5, prefix='¥')
    dash.add_kpi('用户数', 54321, change=-2.3)
    
    engine = ChartEngine()
    data = {'月份': ['1月', '2月', '3月'], '销售额': [100, 150, 200]}
    fig = engine.line_chart(data, x='月份', y='销售额', title='趋势')
    dash.add_chart('trend', fig, '月度趋势')
    
    dash.save('test_dashboard.html')
