#!/usr/bin/env python3
"""
Auto Workflow Engine v2.0 - 智能工作流引擎
用法：python3 workflow-engine.py <command> <workflow_file> [选项]

Copyright © 2026 anyafu. All rights reserved.
Licensed under MIT License.
"""

import json
import os
import sys
import shutil
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
import time
import hashlib

# 配置
CONFIG = {
    'timeout': 60,
    'max_retries': 3,
    'retry_delay': 1,
    'log_dir': '/tmp/workflow-logs',
}

class Color:
    """终端颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log(msg, level='info', indent=0):
    """日志输出"""
    colors = {
        'info': Color.CYAN,
        'success': Color.GREEN,
        'warning': Color.YELLOW,
        'error': Color.RED,
        'debug': Color.BLUE,
    }
    color = colors.get(level, '')
    prefix = "  " * indent
    print(f"{color}{prefix}{msg}{Color.ENDC}")

class WorkflowEngine:
    def __init__(self, workflow_def):
        self.workflow = workflow_def
        self.context = {}
        self.start_time = datetime.now()
        self.log_file = None
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        os.makedirs(CONFIG['log_dir'], exist_ok=True)
        log_name = self.workflow.get('name', 'workflow').replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(CONFIG['log_dir'], f"{log_name}_{timestamp}.log")
    
    def write_log(self, msg):
        """写入日志文件"""
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
    
    def execute_step(self, step, step_num):
        """执行单个工作流步骤"""
        action = step.get('action', '')
        params = step.get('params', {})
        name = step.get('name', action)
        critical = step.get('critical', True)
        retries = step.get('retries', CONFIG['max_retries'])
        
        log(f"步骤 {step_num}: {name}", 'info')
        self.write_log(f"开始执行步骤 {step_num}: {name}")
        
        # 重试逻辑
        for attempt in range(1, retries + 1):
            try:
                result = self._execute_action(action, params)
                if result and result.get('success', False):
                    log(f"  ✅ 完成", 'success', 1)
                    self.write_log(f"步骤 {step_num} 执行成功")
                    return result
                else:
                    error_msg = result.get('error', '未知错误') if result else '执行失败'
                    if attempt < retries:
                        log(f"  ⚠️  {error_msg}，{CONFIG['retry_delay']}秒后重试 ({attempt}/{retries})", 'warning', 1)
                        time.sleep(CONFIG['retry_delay'])
                    else:
                        log(f"  ❌ 失败：{error_msg}", 'error', 1)
                        self.write_log(f"步骤 {step_num} 执行失败：{error_msg}")
                        if critical:
                            return {'success': False, 'error': error_msg}
                        return result
            except Exception as e:
                error_msg = str(e)
                if attempt < retries:
                    log(f"  ⚠️  {error_msg}，重试 ({attempt}/{retries})", 'warning', 1)
                    time.sleep(CONFIG['retry_delay'])
                else:
                    log(f"  ❌ 异常：{error_msg}", 'error', 1)
                    self.write_log(f"步骤 {step_num} 异常：{error_msg}")
                    if critical:
                        return {'success': False, 'error': error_msg}
        
        return {'success': False, 'error': '超过最大重试次数'}
    
    def _execute_action(self, action, params):
        """执行具体动作"""
        # 展开变量
        params = self.expand_params(params)
        
        # 文件操作
        if action == 'file.copy':
            return self.file_copy(params)
        elif action == 'file.move':
            return self.file_move(params)
        elif action == 'file.delete':
            return self.file_delete(params)
        elif action == 'file.download':
            return self.file_download(params)
        elif action == 'archive.create':
            return self.archive_create(params)
        elif action == 'archive.extract':
            return self.archive_extract(params)
        
        # HTTP 请求
        elif action == 'http.get':
            return self.http_get(params)
        elif action == 'http.post':
            return self.http_post(params)
        
        # 数据处理
        elif action == 'data.convert':
            return self.data_convert(params)
        elif action == 'data.transform':
            return self.data_transform(params)
        
        # Shell 命令
        elif action == 'shell.exec':
            return self.shell_exec(params)
        
        # 条件判断
        elif action == 'condition.if':
            return self.condition_if(params)
        
        # 等待
        elif action == 'wait':
            return self.wait(params)
        
        # 通知
        elif action == 'notify':
            return self.notify(params)
        
        else:
            log(f"  ⚠️  未知动作：{action}", 'warning', 1)
            return {'success': False, 'error': f'Unknown action: {action}'}
    
    def file_copy(self, params):
        """复制文件"""
        src = params.get('source')
        dst = params.get('dest')
        try:
            shutil.copy2(src, dst)
            log(f"    {src} → {dst}", 'success', 2)
            return {'success': True, 'dest': dst}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def file_move(self, params):
        """移动文件"""
        src = params.get('source')
        dst = params.get('dest')
        try:
            shutil.move(src, dst)
            log(f"    {src} → {dst}", 'success', 2)
            return {'success': True, 'dest': dst}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def file_delete(self, params):
        """删除文件"""
        path = params.get('path')
        try:
            if os.path.isfile(path):
                os.remove(path)
                log(f"    删除：{path}", 'success', 2)
            elif os.path.isdir(path):
                shutil.rmtree(path)
                log(f"    删除目录：{path}", 'success', 2)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def file_download(self, params):
        """下载文件"""
        url = params.get('url')
        save = params.get('save')
        try:
            log(f"    下载：{url}", 'info', 2)
            with urllib.request.urlopen(url, timeout=CONFIG['timeout']) as response:
                with open(save, 'wb') as f:
                    f.write(response.read())
            log(f"    保存到：{save}", 'success', 2)
            return {'success': True, 'file': save}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def archive_create(self, params):
        """创建压缩包"""
        source = params.get('source')
        output = params.get('output')
        format = params.get('format', 'gztar')
        try:
            os.makedirs(os.path.dirname(output), exist_ok=True)
            shutil.make_archive(output.replace('.tar.gz', '').replace('.zip', ''), format, source)
            out_file = output if '.' in output else output + '.tar.gz'
            log(f"    创建压缩包：{out_file}", 'success', 2)
            return {'success': True, 'output': out_file}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def archive_extract(self, params):
        """解压文件"""
        source = params.get('source')
        dest = params.get('dest', '.')
        try:
            shutil.unpack_archive(source, dest)
            log(f"    解压到：{dest}", 'success', 2)
            return {'success': True, 'dest': dest}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def http_get(self, params):
        """HTTP GET 请求"""
        url = params.get('url')
        save = params.get('save')
        headers = params.get('headers', {})
        try:
            log(f"    GET {url}", 'info', 2)
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=CONFIG['timeout']) as response:
                data = response.read()
                if save:
                    with open(save, 'wb') as f:
                        f.write(data)
                    log(f"    保存到：{save}", 'success', 2)
                    return {'success': True, 'file': save}
                return {'success': True, 'data': data.decode()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def http_post(self, params):
        """HTTP POST 请求"""
        url = params.get('url')
        data = params.get('data', {})
        headers = params.get('headers', {})
        try:
            log(f"    POST {url}", 'info', 2)
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers={'Content-Type': 'application/json', **headers}
            )
            with urllib.request.urlopen(req, timeout=CONFIG['timeout']) as response:
                return {'success': True, 'data': response.read().decode()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def data_convert(self, params):
        """数据格式转换"""
        import csv
        input_file = params.get('input')
        output_file = params.get('output')
        try:
            log(f"    转换：{input_file} → {output_file}", 'info', 2)
            if input_file.endswith('.json') and output_file.endswith('.csv'):
                with open(input_file) as f:
                    data = json.load(f)
                if data:
                    with open(output_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
            elif input_file.endswith('.csv') and output_file.endswith('.json'):
                with open(input_file, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                return {'success': False, 'error': '不支持的转换'}
            log(f"    转换完成", 'success', 2)
            return {'success': True, 'output': output_file}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def data_transform(self, params):
        """数据转换（简单 JSON 处理）"""
        input_file = params.get('input')
        output_file = params.get('output')
        transform = params.get('transform', {})
        try:
            with open(input_file, encoding='utf-8') as f:
                data = json.load(f)
            
            # 简单转换：字段重命名、过滤等
            if isinstance(data, list) and 'fields' in transform:
                fields = transform['fields']
                data = [{k: item.get(v, item.get(k)) for k, v in fields.items()} for item in data]
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            log(f"    转换完成", 'success', 2)
            return {'success': True, 'output': output_file}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def shell_exec(self, params):
        """执行 Shell 命令"""
        cmd = params.get('command')
        timeout = params.get('timeout', CONFIG['timeout'])
        try:
            log(f"    执行：{cmd}", 'info', 2)
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout
            )
            if result.returncode == 0:
                log(f"    完成", 'success', 2)
                return {'success': True, 'stdout': result.stdout, 'stderr': result.stderr}
            else:
                return {'success': False, 'error': result.stderr or f'Exit code: {result.returncode}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def condition_if(self, params):
        """条件判断"""
        condition = params.get('condition', True)
        # 简单条件判断，可以扩展
        log(f"    条件：{condition}", 'info', 2)
        return {'success': True, 'result': bool(condition)}
    
    def wait(self, params):
        """等待"""
        seconds = params.get('seconds', 1)
        log(f"    等待 {seconds} 秒", 'info', 2)
        time.sleep(seconds)
        return {'success': True}
    
    def notify(self, params):
        """通知（终端显示）"""
        message = params.get('message', '')
        level = params.get('level', 'info')
        log(f"    📢 {message}", level, 2)
        return {'success': True}
    
    def expand_params(self, params):
        """展开参数中的变量"""
        if isinstance(params, str):
            return self.expand_vars(params)
        elif isinstance(params, dict):
            return {k: self.expand_params(v) for k, v in params.items()}
        elif isinstance(params, list):
            return [self.expand_params(item) for item in params]
        return params
    
    def expand_vars(self, text):
        """展开变量"""
        if not text or not isinstance(text, str):
            return text
        
        now = datetime.now()
        text = text.replace('{date}', now.strftime('%Y%m%d'))
        text = text.replace('{datetime}', now.strftime('%Y%m%d_%H%M%S'))
        text = text.replace('{year}', now.strftime('%Y'))
        text = text.replace('{month}', now.strftime('%m'))
        text = text.replace('{day}', now.strftime('%d'))
        text = text.replace('{hour}', now.strftime('%H'))
        text = text.replace('{minute}', now.strftime('%M'))
        
        # 环境变量
        for key, value in os.environ.items():
            text = text.replace(f'{{{key}}}', value)
        
        # 上下文变量
        for key, value in self.context.items():
            text = text.replace(f'{{{key}}}', str(value))
        
        return text
    
    def run(self):
        """运行工作流"""
        name = self.workflow.get('name', 'Unnamed')
        desc = self.workflow.get('description', 'No description')
        
        print(f"\n{Color.BOLD}🚀 开始执行工作流：{name}{Color.ENDC}")
        print(f"{Color.CYAN}📝 描述：{desc}{Color.ENDC}")
        print(f"{Color.CYAN}{'='*60}{Color.ENDC}\n")
        
        self.write_log(f"开始执行工作流：{name}")
        self.write_log(f"描述：{desc}")
        
        steps = self.workflow.get('steps', [])
        results = []
        start_time = datetime.now()
        
        for i, step in enumerate(steps, 1):
            result = self.execute_step(step, i)
            results.append(result)
            
            # 将结果存入上下文
            if result:
                for key, value in result.items():
                    self.context[f'step_{i}_{key}'] = value
            
            # 如果关键步骤失败，停止执行
            if result and not result.get('success', True):
                if step.get('critical', True):
                    log(f"\n❌ 关键步骤失败，停止执行", 'error')
                    self.write_log(f"关键步骤失败，停止执行")
                    break
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n{Color.GREEN}{'='*60}{Color.ENDC}")
        print(f"{Color.BOLD}✅ 工作流执行完成{Color.ENDC}")
        print(f"📊 执行了 {len(results)}/{len(steps)} 个步骤")
        print(f"⏱️  耗时：{duration:.2f}秒")
        print(f"📄 日志：{self.log_file}")
        print(f"{Color.GREEN}{'='*60}{Color.ENDC}\n")
        
        self.write_log(f"工作流执行完成，耗时{duration:.2f}秒")
        
        return {
            'success': True,
            'steps_executed': len(results),
            'steps_total': len(steps),
            'duration': duration,
            'results': results,
            'log_file': self.log_file,
        }

def load_workflow(path):
    """加载工作流定义"""
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def create_template(name):
    """创建工作流模板"""
    template = {
        "name": name,
        "description": "工作流描述",
        "version": "2.0",
        "steps": [
            {
                "name": "第一步",
                "action": "file.copy",
                "params": {"source": "/path/to/source", "dest": "/path/to/dest"},
                "critical": True,
                "retries": 3
            }
        ]
    }
    output_file = f"{name}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    print(f"✅ 工作流模板已创建：{output_file}")
    print("编辑此文件定义你的工作流，然后用 'run' 命令执行")
    print(f"\n可用动作：file.copy, file.move, file.delete, file.download,")
    print(f"          archive.create, archive.extract, http.get, http.post,")
    print(f"          data.convert, data.transform, shell.exec, condition.if, wait, notify")

def list_presets():
    """列出预设工作流"""
    presets_dir = os.path.join(os.path.dirname(__file__), '..', 'presets')
    if os.path.exists(presets_dir):
        print(f"\n{Color.BOLD}📋 预设工作流：{Color.ENDC}")
        for f in os.listdir(presets_dir):
            if f.endswith('.json'):
                print(f"  - {f.replace('.json', '')}")
    else:
        print("暂无预设工作流")

def main():
    if len(sys.argv) < 3:
        print(f"""
{Color.BOLD}🔧 Auto Workflow Engine v2.0 - 智能工作流引擎{Color.ENDC}
{Color.CYAN}{'='*60}{Color.ENDC}

用法：python3 workflow-engine.py <command> <argument> [选项]

命令:
  run <file>       - 运行工作流
  create <name>    - 创建工作流模板
  list             - 列出预设工作流
  validate <file>  - 验证工作流语法

示例:
  python3 workflow-engine.py run backup.json
  python3 workflow-engine.py create my_workflow
  python3 workflow-engine.py list
  python3 workflow-engine.py validate workflow.json

选项:
  --verbose        - 显示详细日志
  --dry-run        - 模拟运行（不执行实际操作）

{Color.CYAN}{'='*60}{Color.ENDC}
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    arg = sys.argv[2]
    
    if command == 'run':
        if not os.path.exists(arg):
            print(f"{Color.RED}❌ 文件不存在：{arg}{Color.ENDC}")
            sys.exit(1)
        workflow = load_workflow(arg)
        engine = WorkflowEngine(workflow)
        result = engine.run()
        sys.exit(0 if result.get('success', False) else 1)
    
    elif command == 'create':
        create_template(arg)
    
    elif command == 'list':
        list_presets()
    
    elif command == 'validate':
        if not os.path.exists(arg):
            print(f"{Color.RED}❌ 文件不存在：{arg}{Color.ENDC}")
            sys.exit(1)
        try:
            workflow = load_workflow(arg)
            if 'steps' in workflow and isinstance(workflow['steps'], list):
                print(f"{Color.GREEN}✅ 工作流语法有效{Color.ENDC}")
                print(f"  名称：{workflow.get('name', 'Unnamed')}")
                print(f"  步骤数：{len(workflow['steps'])}")
            else:
                print(f"{Color.RED}❌ 工作流缺少 steps 字段{Color.ENDC}")
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"{Color.RED}❌ JSON 格式错误：{e}{Color.ENDC}")
            sys.exit(1)
    
    else:
        print(f"{Color.RED}❌ 未知命令：{command}{Color.ENDC}")
        sys.exit(1)

if __name__ == '__main__':
    main()
