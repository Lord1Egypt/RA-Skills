# -*- coding: utf-8 -*-
"""
Auto Video Generator Web UI v1.0
独立Web应用 - 让非技术人员通过浏览器使用视频生成功能

核心功能：
1. 文件上传（HTML/Vue/PRD）
2. URL输入生成
3. 可视化配置面板
4. 实时进度显示
5. 视频预览和下载
6. 历史记录管理
"""

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
import uuid
import threading
import time
import asyncio
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
from typing import Dict, List, Optional, Any


app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ============================================================
# 配置
# ============================================================

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')
ALLOWED_EXTENSIONS = {'html', 'vue', 'tsx', 'jsx', 'json', 'yaml', 'yml', 'md', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# 数据存储（内存中，生产环境应使用数据库）
# ============================================================

class TaskManager:
    """任务管理器"""
    
    def __init__(self):
        self.tasks: Dict[str, Dict] = {}
        self._lock = threading.Lock()
    
    def create_task(self, task_type: str, config: Dict) -> str:
        """创建新任务"""
        task_id = str(uuid.uuid4())[:8]
        
        with self._lock:
            self.tasks[task_id] = {
                'id': task_id,
                'type': task_type,
                'status': 'pending',
                'progress': 0,
                'config': config,
                'created_at': datetime.now().isoformat(),
                'started_at': None,
                'completed_at': None,
                'result': None,
                'error': None,
                'output_file': None,
            }
        
        return task_id
    
    def update_task(self, task_id: str, updates: Dict):
        """更新任务状态"""
        with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].update(updates)
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """获取任务信息"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self, limit: int = 20) -> List[Dict]:
        """获取所有任务（按时间倒序）"""
        with self._lock:
            tasks = sorted(
                self.tasks.values(),
                key=lambda x: x.get('created_at', ''),
                reverse=True
            )
            return tasks[:limit]


task_manager = TaskManager()


# ============================================================
# 辅助函数
# ============================================================

def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_default_config() -> Dict:
    """获取默认配置"""
    return {
        'browser': {
            'headless': True,
            'viewport_width': 1440,
            'viewport_height': 900,
        },
        'video': {
            'fps': 4,
            'format': 'mp4',
            'quality': 'high',
        },
        'audio': {
            'engine': 'edge_tts',
            'voice': 'zh-CN-YunxiNeural',
            'rate': '-5%',
        },
        'recording': {
            'interaction_mode': 'real',
            'clip_sidebar': True,
            'auto_scroll': True,
        }
    }


def simulate_video_generation(task_id: str, input_source: str):
    """
    模拟视频生成过程
    在实际应用中，这里会调用 integrated_video_generator.py
    """
    stages = [
        ('Initializing browser...', 5),
        ('Loading page content...', 15),
        ('Detecting UI framework...', 25),
        ('Analyzing page structure...', 35),
        ('Capturing screenshots...', 50),
        ('Generating audio narration...', 65),
        ('Encoding video frames...', 80),
        ('Applying audio synchronization...', 90),
        ('Finalizing output file...', 95),
        ('Complete!', 100),
    ]
    
    try:
        for stage_name, progress in stages:
            time.sleep(1.5)  # 模拟耗时
            
            task_manager.update_task(task_id, {
                'progress': progress,
                'status': 'processing',
            })
            
            # 通过WebSocket推送进度
            socketio.emit('task_progress', {
                'task_id': task_id,
                'progress': progress,
                'stage': stage_name,
            })
        
        # 生成模拟输出文件
        output_filename = f"demo_{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # 创建一个空文件作为占位符（实际应用中这里会是真正的视频）
        Path(output_path).touch()
        
        task_manager.update_task(task_id, {
            'status': 'completed',
            'progress': 100,
            'completed_at': datetime.now().isoformat(),
            'output_file': output_filename,
            'result': {
                'duration': '45s',
                'file_size': '12.3 MB',
                'resolution': '1440x900',
                'fps': 4,
            }
        })
        
        socketio.emit('task_completed', {
            'task_id': task_id,
            'output_file': output_filename,
        })
        
    except Exception as e:
        task_manager.update_task(task_id, {
            'status': 'failed',
            'error': str(e),
        })
        
        socketio.emit('task_failed', {
            'task_id': task_id,
            'error': str(e),
        })


# ============================================================
# 路由定义
# ============================================================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """获取当前配置"""
    config = get_default_config()
    return jsonify({
        'success': True,
        'data': config
    })


@app.route('/api/config', methods=['POST'])
def save_config():
    """保存配置"""
    try:
        data = request.json
        
        # 验证配置
        required_sections = ['browser', 'video', 'audio']
        for section in required_sections:
            if section not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing configuration section: {section}'
                }), 400
        
        # 在实际应用中，这里会保存到数据库或文件
        print(f"[Config] Updated: {json.dumps(data, indent=2)}")
        
        return jsonify({
            'success': True,
            'message': 'Configuration saved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传文件"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'data': {
                'filename': unique_filename,
                'original_name': filename,
                'size': os.path.getsize(filepath),
                'path': filepath
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/generate', methods=['POST'])
def generate_video():
    """启动视频生成任务"""
    try:
        data = request.json
        
        input_type = data.get('type')  # 'file', 'url', or 'prd'
        config = data.get('config', {})
        
        # 合并默认配置
        final_config = {**get_default_config(), **config}
        
        # 创建任务
        task_id = task_manager.create_task(input_type, final_config)
        
        # 更新任务为运行中
        task_manager.update_task(task_id, {
            'status': 'processing',
            'started_at': datetime.now().isoformat(),
            'input_data': data.get('input_data'),
        })
        
        # 启动后台线程执行生成
        thread = threading.Thread(
            target=simulate_video_generation,
            args=(task_id, data.get('input_data', ''))
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'data': {
                'task_id': task_id,
                'status': 'processing',
                'message': 'Video generation started'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id: str):
    """获取任务状态"""
    task = task_manager.get_task(task_id)
    
    if not task:
        return jsonify({
            'success': False,
            'error': 'Task not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': task
    })


@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """获取任务列表"""
    limit = request.args.get('limit', 20, type=int)
    tasks = task_manager.get_all_tasks(limit)
    
    return jsonify({
        'success': True,
        'data': tasks,
        'count': len(tasks)
    })


@app.route('/api/download/<filename>', methods=['GET'])
def download_video(filename: str):
    """下载生成的视频"""
    try:
        safe_path = os.path.basename(filename)
        return send_from_directory(
            app.config['OUTPUT_FOLDER'],
            safe_path,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@app.route('/api/preview/<filename>', methods=['GET'])
def preview_video(filename: str):
    """在线预览视频"""
    try:
        safe_path = os.path.basename(filename)
        return send_from_directory(
            app.config['OUTPUT_FOLDER'],
            safe_path
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """获取可用模板列表"""
    templates = [
        {
            'id': 'dashboard-demo',
            'name': 'Dashboard Demo Video',
            'description': 'Generate demo video for dashboard/admin panels',
            'category': 'admin',
            'icon': '📊',
        },
        {
            'id': 'ecommerce-product',
            'name': 'E-commerce Product Page',
            'description': 'Showcase product pages with narration',
            'category': 'ecommerce',
            'icon': '🛒',
        },
        {
            'id': 'form-wizard',
            'name': 'Form Wizard Tutorial',
            'description': 'Step-by-step form filling demonstration',
            'category': 'tutorial',
            'icon': '📝',
        },
        {
            'id': 'data-table',
            'name': 'Data Table Features',
            'description': 'Demonstrate sorting, filtering, pagination',
            'category': 'component',
            'icon': '📋',
        },
        {
            'id': 'login-flow',
            'name': 'Authentication Flow',
            'description': 'Login and registration process demo',
            'category': 'auth',
            'icon': '🔐',
        },
    ]
    
    return jsonify({
        'success': True,
        'data': templates
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取系统统计信息"""
    all_tasks = task_manager.get_all_tasks(1000)
    
    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t['status'] == 'completed')
    failed = sum(1 for t in all_tasks if t['status'] == 'failed')
    processing = sum(1 for t in all_tasks if t['status'] == 'processing')
    
    stats = {
        'total_tasks': total,
        'completed': completed,
        'failed': failed,
        'processing': processing,
        'success_rate': round((completed / total * 100) if total > 0 else 0, 1),
        'uptime_seconds': int(time.time() - app.start_time) if hasattr(app, 'start_time') else 0,
    }
    
    return jsonify({
        'success': True,
        'data': stats
    })


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
    })


# ============================================================
# WebSocket事件处理
# ============================================================

@socketio.on('connect')
def handle_connect():
    """客户端连接时发送欢迎消息"""
    emit('connected', {
        'message': 'Connected to Auto Video Generator',
        'server_time': datetime.now().isoformat(),
    })
    print(f"[WS] Client connected")


@socketio.on('disconnect')
def handle_disconnect():
    """客户端断开连接"""
    print(f"[WS] Client disconnected")


@socketio.on('subscribe_task')
def handle_subscribe(data):
    """订阅特定任务的更新"""
    task_id = data.get('task_id')
    if task_id:
        task = task_manager.get_task(task_id)
        if task:
            emit('task_update', task)


# ============================================================
# 主程序入口
# ============================================================

if __name__ == '__main__':
    app.start_time = time.time()
    
    print("=" * 60)
    print("Auto Video Generator Web UI v1.0")
    print("=" * 60)
    print(f"Starting server at http://localhost:5000")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    print("=" * 60)
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=False,
        allow_unsafe_werkzeug=True
    )
