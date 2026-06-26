# ACE-Step Agent 共享指南

## 概述

ACE-Step 1.5 已安装在主人机器上，其他本地 Agent 可以通过以下方式调用：

---

## 方式 1: HTTP API (推荐 ⭐)

### 启动 API 服务
```bash
python3 skills/ace-step/ace_step_agent_server.py
```

### 其他 Agent 调用示例

**检查状态:**
```bash
curl http://localhost:8765/status
```

**生成音乐:**
```bash
curl -X POST http://localhost:8765/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A peaceful piano melody with soft strings",
    "duration": 30
  }'
```

**Python 调用:**
```python
import requests

# 生成音乐
response = requests.post('http://localhost:8765/generate', json={
    'prompt': 'Upbeat electronic music',
    'duration': 60,
    'output_path': '/tmp/my_music.wav'
})

result = response.json()
if result['success']:
    print(f"Generated: {result['file']}")
```

---

## 方式 2: Shell 命令

### 使用方法
```bash
# 生成音乐
skills/ace-step/ace-step-agent.sh generate "prompt text" [duration] [output_file]

# 检查状态
skills/ace-step/ace-step-agent.sh status

# 安装
skills/ace-step/ace-step-agent.sh install
```

### 示例
```bash
# 生成 30 秒钢琴曲
skills/ace-step/ace-step-agent.sh generate "Peaceful piano melody" 30

# 生成到指定路径
skills/ace-step/ace-step-agent.sh generate "Electronic dance music" 60 /tmp/edm.wav
```

---

## 方式 3: Python 直接导入

如果 Agent 本身也是 Python，可以直接导入：

```python
import sys
sys.path.insert(0, '/Users/qinghetangzhu/workspace/ace-step')

# 激活虚拟环境 (需要在子进程中)
import subprocess
result = subprocess.run([
    '/Users/qinghetangzhu/ace-step-env/bin/python',
    '-c',
    '''
import sys
sys.path.insert(0, '/Users/qinghetangzhu/workspace/ace-step')
# 调用 ACE-Step 生成音乐
    '''
], capture_output=True, text=True)
```

---

## 文件位置

| 项目 | 路径 |
|------|------|
| 虚拟环境 | `~/ace-step-env` |
| 代码目录 | `~/workspace/ace-step` |
| 输出目录 | `~/Music/ACE-Step` |
| API 服务 | `skills/ace-step/ace_step_agent_server.py` |
| Shell 接口 | `skills/ace-step/ace-step-agent.sh` |

---

## 注意事项

1. **ACE-Step 安装状态**: 代码已下载，但 pip install -e . 因 Python 版本未完成
2. **需要 Python 3.12**: 当前系统是 3.14，需要隔离环境
3. **API 服务需手动启动**: 不会自动运行，需要时启动

---

## 快速测试

```bash
# 1. 启动 API 服务 (终端 1)
python3 skills/ace-step/ace_step_agent_server.py

# 2. 测试调用 (终端 2)
curl http://localhost:8765/status
curl -X POST http://localhost:8765/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "duration": 10}'
```
