#!/usr/bin/env python3
"""
桌面监控悬浮球 - 简易版 (使用 web 浏览器)
无需 tkinter，使用浏览器显示监控界面
"""

import psutil
import time
import webbrowser
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import json

# 监控数据缓存
monitor_data = {
    'cpu': 0,
    'memory': 0,
    'disk': 0,
    'temp': 'N/A',
    'uptime': '',
    'processes': 0
}

def get_cpu_temp():
    """获取 CPU 温度"""
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    if 'cpu' in entry.label.lower() or 'core' in entry.label.lower():
                        return entry.current
            for name, entries in temps.items():
                for entry in entries:
                    return entry.current
    except:
        pass
    return 'N/A'

def update_monitor_data():
    """后台更新监控数据"""
    global monitor_data
    while True:
        try:
            # CPU
            monitor_data['cpu'] = psutil.cpu_percent(interval=1)
            
            # 内存
            mem = psutil.virtual_memory()
            monitor_data['memory'] = mem.percent
            
            # 磁盘
            disk = psutil.disk_usage('/')
            monitor_data['disk'] = disk.percent
            
            # 温度
            monitor_data['temp'] = get_cpu_temp()
            
            # 运行时间
            uptime = time.time() - psutil.boot_time()
            days = int(uptime // 86400)
            hours = int((uptime % 86400) // 3600)
            mins = int((uptime % 3600) // 60)
            if days > 0:
                monitor_data['uptime'] = f"{days}天{hours}小时"
            else:
                monitor_data['uptime'] = f"{hours}小时{mins}分"
            
            # 进程数
            monitor_data['processes'] = len(psutil.pids())
        except:
            pass
        
        time.sleep(2)

class MonitorHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(monitor_data).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>系统监控</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .widget {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            width: 320px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }
        h1 { font-size: 18px; margin-bottom: 20px; color: #fff; }
        .stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
        }
        .stat-label { font-size: 14px; color: #aaa; }
        .stat-value { font-size: 18px; font-weight: bold; }
        .cpu { color: #00ff00; }
        .memory { color: #00ffff; }
        .disk { color: #ff9900; }
        .temp { color: #ff6666; }
        .uptime { color: #6666ff; }
        .processes { color: #ff66ff; }
        .progress {
            width: 100px;
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #00ff00, #00ffff);
            transition: width 0.3s;
        }
        .status {
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #666;
        }
        .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #00ff00;
            border-radius: 50%;
            margin-right: 5px;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="widget">
        <h1>🖥️ 系统监控</h1>
        
        <div class="stat">
            <span class="stat-label">CPU</span>
            <div style="display:flex;align-items:center;gap:10px;">
                <div class="progress"><div class="progress-bar" id="cpu-bar"></div></div>
                <span class="stat-value cpu" id="cpu">--%</span>
            </div>
        </div>
        
        <div class="stat">
            <span class="stat-label">内存</span>
            <div style="display:flex;align-items:center;gap:10px;">
                <div class="progress"><div class="progress-bar" id="mem-bar"></div></div>
                <span class="stat-value memory" id="memory">--%</span>
            </div>
        </div>
        
        <div class="stat">
            <span class="stat-label">磁盘</span>
            <div style="display:flex;align-items:center;gap:10px;">
                <div class="progress"><div class="progress-bar" id="disk-bar"></div></div>
                <span class="stat-value disk" id="disk">--%</span>
            </div>
        </div>
        
        <div class="stat">
            <span class="stat-label">温度</span>
            <span class="stat-value temp" id="temp">--°C</span>
        </div>
        
        <div class="stat">
            <span class="stat-label">运行时间</span>
            <span class="stat-value uptime" id="uptime">--</span>
        </div>
        
        <div class="stat">
            <span class="stat-label">进程数</span>
            <span class="stat-value processes" id="processes">--</span>
        </div>
        
        <div class="status">
            <span class="dot"></span>实时监控中
        </div>
    </div>
    
    <script>
        function updateData() {
            fetch('/data')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('cpu').textContent = data.cpu + '%';
                    document.getElementById('cpu-bar').style.width = data.cpu + '%';
                    
                    document.getElementById('memory').textContent = data.memory + '%';
                    document.getElementById('mem-bar').style.width = data.memory + '%';
                    
                    document.getElementById('disk').textContent = data.disk + '%';
                    document.getElementById('disk-bar').style.width = data.disk + '%';
                    
                    document.getElementById('temp').textContent = (data.temp !== 'N/A' ? data.temp + '°C' : 'N/A');
                    document.getElementById('uptime').textContent = data.uptime;
                    document.getElementById('processes').textContent = data.processes;
                });
        }
        
        updateData();
        setInterval(updateData, 2000);
    </script>
</body>
</html>
'''
            self.wfile.write(html.encode())
        else:
            super().do_GET()

def start_server():
    server = HTTPServer(('127.0.0.1', 8765), MonitorHandler)
    print("🖥️ 系统监控悬浮球已启动")
    print("📍 访问地址：http://127.0.0.1:8765")
    print("按 Ctrl+C 停止")
    server.serve_forever()

if __name__ == '__main__':
    # 启动数据更新线程
    threading.Thread(target=update_monitor_data, daemon=True).start()
    
    # 启动服务器
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 打开浏览器
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:8765')
    
    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止监控...")
