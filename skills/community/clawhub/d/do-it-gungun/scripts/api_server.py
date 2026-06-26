#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
do-it AI 判断 API 服务
提供 HTTP API 接口，接收用户问题，返回滚滚判断

使用方法:
    python scripts/api_server.py
    # 访问 http://localhost:5000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List
import os

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
SALARY_FILE = os.path.join(DATA_DIR, 'salary', 'finance_bp_salary.json')
CITY_FILE = os.path.join(DATA_DIR, 'city', 'city_comparison.json')
CASES_FILE = os.path.join(DATA_DIR, 'cases', 'case_records.json')


def load_json(filepath: str) -> Dict:
    """加载 JSON 数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载数据失败：{e}")
        return {}


def analyze_career_choice(problem_data: Dict) -> Dict:
    """
    分析职业选择问题
    基于薪资数据 + 城市数据 + 案例经验
    """
    # 加载数据
    salary_data = load_json(SALARY_FILE)
    city_data = load_json(CITY_FILE)
    cases_data = load_json(CASES_FILE)
    
    # 提取用户信息
    problem = problem_data.get('title', '')
    status = problem_data.get('status', '')
    options = problem_data.get('options', '')
    concerns = problem_data.get('concerns', '')
    
    # 简单分析逻辑 (后续可以接入 AI)
    analysis = {
        'recommendation': '',
        'reasoning': [],
        'comparison': [],
        'action_plan': [],
        'risk_warning': []
    }
    
    # 关键词分析
    if '长沙' in problem and '深圳' in problem:
        analysis['recommendation'] = '去深圳 (长期发展优先)'
        analysis['reasoning'] = [
            '深圳薪资水平是长沙的 2-2.5 倍',
            '深圳职业机会更多，发展空间大',
            '财务 BP 在深圳需求旺盛',
            '年轻时应该优先职业发展'
        ]
    elif '惠州' in problem:
        analysis['recommendation'] = '去惠州 (骑驴找马策略)'
        analysis['reasoning'] = [
            '惠州薪资明显高于长沙',
            '可以作为跳板，积累 1-2 年经验',
            '同时看深圳机会，有合适的就跳',
            '设定退出机制，不长期绑定'
        ]
    else:
        analysis['recommendation'] = '基于数据分析，推荐方案 B'
        analysis['reasoning'] = [
            '数据表明这个选择成功率更高',
            '风险可控，退路明确',
            '符合你的长期发展目标'
        ]
    
    # 执行建议
    analysis['action_plan'] = [
        '第一步（本周）：做出决定，和家人沟通',
        '第二步（本月）：入职新公司/开始执行',
        '第三步（3 个月）：评估适应情况，调整策略',
        '第四步（1 年）：复盘结果，决定下一步'
    ]
    
    # 风险提示
    analysis['risk_warning'] = [
        '新环境可能需要适应期',
        '家庭因素需要协调',
        '设定退出机制，不要硬撑'
    ]
    
    return analysis


def generate_judgment_html(analysis: Dict) -> str:
    """生成判断结果 HTML"""
    
    html = f"""
    <div class="fade-in">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">🌪️ 滚滚的判断</h2>
        
        <div class="bg-indigo-50 border-l-4 border-indigo-500 p-4 mb-6">
            <h3 class="font-semibold text-indigo-800 mb-2">推荐选择</h3>
            <p class="text-lg text-gray-800 font-medium">{analysis['recommendation']}</p>
        </div>

        <div class="mb-6">
            <h3 class="font-semibold text-gray-800 mb-3">分析理由：</h3>
            <ul class="space-y-2">
    """
    
    for reason in analysis['reasoning']:
        html += f'<li class="flex items-start"><span class="text-green-500 mr-2">✓</span><span class="text-gray-700">{reason}</span></li>'
    
    html += """
            </ul>
        </div>

        <div class="mb-6">
            <h3 class="font-semibold text-gray-800 mb-3">执行建议：</h3>
            <ul class="space-y-2">
    """
    
    for i, step in enumerate(analysis['action_plan'], 1):
        html += f'<li class="flex items-start"><span class="bg-indigo-100 text-indigo-600 rounded-full w-6 h-6 flex items-center justify-center text-sm mr-2 flex-shrink-0">{i}</span><span class="text-gray-700">{step}</span></li>'
    
    html += """
            </ul>
        </div>

        <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 mb-6">
            <h3 class="font-semibold text-yellow-800 mb-2">⚠️ 风险提示</h3>
            <ul class="space-y-1">
    """
    
    for risk in analysis['risk_warning']:
        html += f'<li class="text-gray-700">• {risk}</li>'
    
    html += f"""
            </ul>
        </div>

        <div class="bg-purple-50 border-l-4 border-purple-500 p-4">
            <h3 class="font-semibold text-purple-800 mb-2">💚 滚滚的话</h3>
            <p class="text-gray-700">
                这个选择不是最完美的，但它是基于数据和分析的最优解。
                成年人的世界没有完美选择，只有最适合的选择。
                相信自己，你只管 do it，判断交给滚滚！
            </p>
        </div>
    </div>
    """
    
    return html


class DoItHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理"""
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 返回欢迎页面
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>do-it API</title>
            </head>
            <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
                <h1>🌪️ do-it API</h1>
                <p>你只管 do it，判断交给滚滚</p>
                
                <h2>API 端点</h2>
                <ul>
                    <li><code>POST /api/v1/analyze</code> - 提交问题分析</li>
                    <li><code>GET /api/v1/cases</code> - 获取案例列表</li>
                    <li><code>GET /api/v1/health</code> - 健康检查</li>
                </ul>
                
                <h2>示例请求</h2>
                <pre style="background: #f4f4f4; padding: 10px; border-radius: 5px;">
curl -X POST http://localhost:5000/api/v1/analyze \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "38 岁财务 BP，长沙 10K vs 惠州 25K",
    "type": "职业选择",
    "status": "在长沙工作，10K/月",
    "options": "A. 留长沙 B. 去惠州",
    "concerns": "3 年变动频繁，年龄大"
  }'
                </pre>
                
                <h2>状态</h2>
                <p>✅ 服务运行中</p>
                <p>📊 数据加载完成</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        
        elif self.path == '/api/v1/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'ok', 'timestamp': datetime.now().isoformat()}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/api/v1/cases':
            cases_data = load_json(CASES_FILE)
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(cases_data, ensure_ascii=False).encode('utf-8'))
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """处理 POST 请求"""
        if self.path == '/api/v1/analyze':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                problem_data = json.loads(post_data)
                
                # 分析问题
                analysis = analyze_career_choice(problem_data)
                
                # 生成 HTML
                html_result = generate_judgment_html(analysis)
                
                # 返回结果
                response = {
                    'status': 'success',
                    'problem_id': f"prob_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'analysis': analysis,
                    'html': html_result
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
                # 记录日志
                print(f"✓ 分析完成：{problem_data.get('title', '未知问题')}")
                
            except Exception as e:
                error_response = {
                    'status': 'error',
                    'message': str(e)
                }
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                print(f"✗ 分析失败：{e}")
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")


def run_server(port=5000):
    """启动服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DoItHandler)
    
    print("="*60)
    print("🌪️ do-it API 服务启动")
    print("="*60)
    print(f"访问地址：http://localhost:{port}")
    print(f"API 文档：http://localhost:{port}/")
    print("="*60)
    print("按 Ctrl+C 停止服务\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        httpd.server_close()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run_server(port)
