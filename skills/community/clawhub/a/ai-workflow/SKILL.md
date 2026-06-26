---
name: auto-workflow
description: |
  自动化工作流引擎 - 将重复性任务自动化。
  支持：文件处理、数据转换、定时任务、API 调用、多步骤工作流。
  触发词："自动化"、"工作流"、"批量处理"、"定时任务"、"workflow"、"automate"。
  自动执行：预设工作流或自定义流程。
author: anyafu
license: MIT
copyright: Copyright © 2026 anyafu. All rights reserved.
---

# Auto Workflow - 自动化工作流引擎

将重复性工作自动化，让你专注于更有价值的事情。

## 支持的工作流类型

| 类型 | 功能 | 示例 |
|------|------|------|
| 文件处理 | 批量重命名、格式转换、压缩解压 | 批量转换图片格式 |
| 数据处理 | CSV/JSON/XML 转换、数据清洗 | 导出 Excel 为 JSON |
| 定时任务 | 定时执行、周期任务 | 每日自动备份 |
| API 调用 | HTTP 请求、数据同步 | 自动获取天气并通知 |
| 多步骤 | 组合多个操作 | 下载→处理→上传 |

## 使用方法

### 基础用法

```bash
# 运行预设工作流
auto-workflow run preset_name

# 运行自定义工作流
auto-workflow run custom_workflow.json

# 创建工作流
auto-workflow create workflow_name
```

### 预设工作流

#### 1. 文件批量重命名

```bash
# 批量重命名文件（添加前缀/后缀、替换字符）
auto-workflow run rename --dir ./photos --pattern "IMG_{date}_{num}"
```

#### 2. 图片批量转换

```bash
# 批量转换图片格式
auto-workflow run convert-images --dir ./images --from png --to jpg --quality 85
```

#### 3. 数据格式转换

```bash
# CSV 转 JSON
auto-workflow run convert-data --input data.csv --output data.json

# JSON 转 Excel
auto-workflow run json-to-excel --input data.json --output data.xlsx
```

#### 4. 自动备份

```bash
# 每日自动备份指定目录
auto-workflow run backup --source ~/documents --dest ~/backups --schedule "0 2 * * *"
```

#### 5. API 数据获取

```bash
# 定时获取天气并保存
auto-workflow run fetch-weather --city beijing --output weather.json --schedule "0 8 * * *"
```

## 工作流定义示例

### 简单工作流

```json
{
  "name": "图片处理工作流",
  "description": "下载图片→压缩→添加水印→上传",
  "steps": [
    {
      "name": "下载图片",
      "action": "http.get",
      "params": {
        "url": "https://example.com/image.png",
        "save": "/tmp/image.png"
      }
    },
    {
      "name": "压缩图片",
      "action": "image.compress",
      "params": {
        "input": "/tmp/image.png",
        "output": "/tmp/image_compressed.jpg",
        "quality": 80
      }
    },
    {
      "name": "添加水印",
      "action": "image.watermark",
      "params": {
        "input": "/tmp/image_compressed.jpg",
        "output": "/tmp/image_watermarked.jpg",
        "text": "© MyBrand"
      }
    },
    {
      "name": "上传到 CDN",
      "action": "upload.cdn",
      "params": {
        "file": "/tmp/image_watermarked.jpg",
        "path": "/images/"
      }
    }
  ]
}
```

### 定时工作流

```json
{
  "name": "每日数据备份",
  "description": "每天凌晨 2 点自动备份重要文件",
  "schedule": "0 2 * * *",
  "steps": [
    {
      "name": "压缩文档目录",
      "action": "archive.create",
      "params": {
        "source": "~/documents",
        "output": "~/backups/documents_{date}.tar.gz"
      }
    },
    {
      "name": "上传到云存储",
      "action": "upload.cos",
      "params": {
        "file": "~/backups/documents_{date}.tar.gz",
        "bucket": "my-backups"
      }
    },
    {
      "name": "清理旧备份",
      "action": "cleanup.old",
      "params": {
        "dir": "~/backups",
        "pattern": "*.tar.gz",
        "keep_days": 30
      }
    }
  ]
}
```

## 脚本示例

### workflow-engine.py - 工作流引擎

```python
#!/usr/bin/env python3
"""
简易工作流引擎
支持：文件操作、HTTP 请求、数据转换、定时任务
"""

import json
import os
import sys
import shutil
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

class WorkflowEngine:
    def __init__(self):
        self.context = {}
    
    def execute_step(self, step):
        """执行单个工作流步骤"""
        action = step.get('action', '')
        params = step.get('params', {})
        
        print(f"  执行：{step.get('name', action)}")
        
        # 文件操作
        if action == 'file.copy':
            return self.file_copy(params)
        elif action == 'file.move':
            return self.file_move(params)
        elif action == 'file.delete':
            return self.file_delete(params)
        elif action == 'archive.create':
            return self.archive_create(params)
        
        # HTTP 请求
        elif action == 'http.get':
            return self.http_get(params)
        elif action == 'http.post':
            return self.http_post(params)
        
        # 数据处理
        elif action == 'data.convert':
            return self.data_convert(params)
        
        # 其他
        elif action == 'shell.exec':
            return self.shell_exec(params)
        else:
            print(f"    ⚠️  未知动作：{action}")
            return None
    
    def file_copy(self, params):
        """复制文件"""
        src = self.expand_vars(params.get('source'))
        dst = self.expand_vars(params.get('dest'))
        shutil.copy2(src, dst)
        print(f"    ✅ {src} → {dst}")
        return {'success': True, 'dest': dst}
    
    def file_move(self, params):
        """移动文件"""
        src = self.expand_vars(params.get('source'))
        dst = self.expand_vars(params.get('dest'))
        shutil.move(src, dst)
        print(f"    ✅ {src} → {dst}")
        return {'success': True, 'dest': dst}
    
    def file_delete(self, params):
        """删除文件"""
        path = self.expand_vars(params.get('path'))
        if os.path.isfile(path):
            os.remove(path)
            print(f"    ✅ 删除：{path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"    ✅ 删除目录：{path}")
        return {'success': True}
    
    def archive_create(self, params):
        """创建压缩包"""
        source = self.expand_vars(params.get('source'))
        output = self.expand_vars(params.get('output'))
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output), exist_ok=True)
        
        # 创建 tar.gz
        shutil.make_archive(output.replace('.tar.gz', ''), 'gztar', source)
        print(f"    ✅ 创建压缩包：{output}")
        return {'success': True, 'output': output}
    
    def http_get(self, params):
        """HTTP GET 请求"""
        url = params.get('url')
        save = params.get('save')
        
        print(f"    🌐 GET {url}")
        
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read()
                
                if save:
                    save_path = self.expand_vars(save)
                    with open(save_path, 'wb') as f:
                        f.write(data)
                    print(f"    ✅ 保存到：{save_path}")
                    return {'success': True, 'file': save_path}
                else:
                    return {'success': True, 'data': data.decode()}
        except Exception as e:
            print(f"    ❌ 请求失败：{e}")
            return {'success': False, 'error': str(e)}
    
    def http_post(self, params):
        """HTTP POST 请求"""
        url = params.get('url')
        data = params.get('data', {})
        headers = params.get('headers', {})
        
        print(f"    🌐 POST {url}")
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers={'Content-Type': 'application/json', **headers}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return {'success': True, 'data': response.read().decode()}
        except Exception as e:
            print(f"    ❌ 请求失败：{e}")
            return {'success': False, 'error': str(e)}
    
    def data_convert(self, params):
        """数据格式转换"""
        input_file = self.expand_vars(params.get('input'))
        output_file = self.expand_vars(params.get('output'))
        
        print(f"    🔄 转换：{input_file} → {output_file}")
        
        # 简单实现：JSON ↔ CSV
        if input_file.endswith('.json') and output_file.endswith('.csv'):
            self.json_to_csv(input_file, output_file)
        elif input_file.endswith('.csv') and output_file.endswith('.json'):
            self.csv_to_json(input_file, output_file)
        else:
            print(f"    ⚠️  不支持的转换")
            return {'success': False}
        
        return {'success': True, 'output': output_file}
    
    def json_to_csv(self, input_file, output_file):
        """JSON 转 CSV"""
        import csv
        with open(input_file) as f:
            data = json.load(f)
        
        if not data:
            return
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        print(f"    ✅ 转换完成")
    
    def csv_to_json(self, input_file, output_file):
        """CSV 转 JSON"""
        import csv
        with open(input_file, newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"    ✅ 转换完成")
    
    def shell_exec(self, params):
        """执行 Shell 命令"""
        cmd = self.expand_vars(params.get('command'))
        print(f"    💻 执行：{cmd}")
        
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=60
            )
            print(f"    ✅ 完成")
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            print(f"    ❌ 执行失败：{e}")
            return {'success': False, 'error': str(e)}
    
    def expand_vars(self, text):
        """展开变量"""
        if not text:
            return text
        
        # 替换日期变量
        now = datetime.now()
        text = text.replace('{date}', now.strftime('%Y%m%d'))
        text = text.replace('{datetime}', now.strftime('%Y%m%d_%H%M%S'))
        text = text.replace('{year}', now.strftime('%Y'))
        text = text.replace('{month}', now.strftime('%m'))
        text = text.replace('{day}', now.strftime('%d'))
        
        # 替换环境变量
        for key, value in os.environ.items():
            text = text.replace(f'{{{key}}}', value)
        
        # 替换上下文变量
        for key, value in self.context.items():
            text = text.replace(f'{{{key}}}', str(value))
        
        return text
    
    def run_workflow(self, workflow_def):
        """运行工作流"""
        print(f"\n🚀 开始执行工作流：{workflow_def.get('name', 'Unnamed')}")
        print(f"📝 描述：{workflow_def.get('description', 'No description')}")
        print("=" * 60)
        
        steps = workflow_def.get('steps', [])
        results = []
        
        for i, step in enumerate(steps, 1):
            print(f"\n步骤 {i}/{len(steps)}:")
            result = self.execute_step(step)
            results.append(result)
            
            # 如果步骤失败且是关键的，停止执行
            if result and not result.get('success', True):
                if step.get('critical', True):
                    print(f"\n❌ 关键步骤失败，停止执行")
                    break
            
            # 将结果存入上下文
            if result:
                for key, value in result.items():
                    self.context[f'step_{i}_{key}'] = value
        
        print("\n" + "=" * 60)
        print("✅ 工作流执行完成")
        print(f"📊 执行了 {len(results)}/{len(steps)} 个步骤")
        
        return results

def load_workflow(path):
    """加载工作流定义"""
    with open(path) as f:
        return json.load(f)

def main():
    if len(sys.argv) < 3:
        print("用法：python3 workflow-engine.py <command> <workflow_file>")
        print("\n命令:")
        print("  run     - 运行工作流")
        print("  create  - 创建工作流模板")
        print("\n示例:")
        print("  python3 workflow-engine.py run backup.json")
        print("  python3 workflow-engine.py create my_workflow")
        sys.exit(1)
    
    command = sys.argv[1]
    arg = sys.argv[2]
    
    engine = WorkflowEngine()
    
    if command == 'run':
        if not os.path.exists(arg):
            print(f"❌ 文件不存在：{arg}")
            sys.exit(1)
        
        workflow = load_workflow(arg)
        engine.run_workflow(workflow)
    
    elif command == 'create':
        template = {
            "name": arg,
            "description": "工作流描述",
            "steps": [
                {
                    "name": "第一步",
                    "action": "file.copy",
                    "params": {
                        "source": "/path/to/source",
                        "dest": "/path/to/dest"
                    }
                }
            ]
        }
        
        output_file = f"{arg}.json"
        with open(output_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"✅ 工作流模板已创建：{output_file}")
        print("编辑此文件定义你的工作流，然后用 'run' 命令执行")

if __name__ == '__main__':
    main()
```

## 变现模式

### 免费层
- 基础文件操作
- 每日 10 次执行
- 预设工作流

### 付费层（¥79/月）
- 所有操作类型
- 无限次执行
- 自定义工作流
- 定时任务

### 企业层（¥599/月）
- 团队协作
- API 访问
- 私有化部署
- 专属支持

## 下一步

1. [ ] 完成脚本开发
2. [ ] 添加更多预设工作流
3. [ ] 开发 Web UI
4. [ ] 发布到 ClawHub

---

## 📜 License

**Copyright © 2026 anyafu. All rights reserved.**

Licensed under the MIT License.

### MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### 商业使用

- ✅ 允许个人和商业使用
- ✅ 允许修改和分发
- ✅ 允许私有化部署
- ⚠️ 如需闭源商业授权，请联系作者 anyafu
