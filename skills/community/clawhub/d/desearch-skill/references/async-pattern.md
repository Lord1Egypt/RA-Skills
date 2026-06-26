# Zeelin Deep Research - 异步任务处理指南

## 问题背景

Deep Research任务是一个长时任务，可能需要数分钟到数十分钟。如果让Agent一直阻塞等待，会导致：
1. 会话超时
2. 资源浪费
3. 用户体验差

## 解决方案

采用**异步模式 + 定时检查**的方案：

### 方案1：后台任务 + 轮询

```python
# 在agent中执行
import subprocess
import time

# 1. 提交任务，后台运行
result = subprocess.run([
    "python3", "scripts/submit_research.py",
    "--query", "分析小米汽车市场",
    "--output", "/tmp/task_id.txt"
], capture_output=True)

# 2. 读取task_id
with open("/tmp/task_id.txt") as f:
    task_id = f.read().strip()

# 3. 启动后台监控（非阻塞）
subprocess.Popen([
    "python3", "scripts/check_status.py",
    "--task-id", task_id,
    "--watch",
    "--output", "/tmp/result.json",
    "--interval", "30",
    "--timeout", "3600"
])

# 4. 立即返回，告诉用户如何获取结果
return f"任务已提交，ID: {task_id}。结果将保存到 /tmp/result.json"
```

### 方案2：使用Webhook回调

```python
# 提交任务时指定webhook
result = submit_research(
    query="分析市场趋势",
    webhook="https://your-server.com/callback"
)
# 任务完成后自动推送结果到你的服务器
```

### 方案3：Cron定时检查

```bash
# 每5分钟检查一次
*/5 * * * * python3 /path/to/check_status.py --task-id YOUR_TASK_ID --output /path/to/result.json
```

## Agent使用流程

```
用户: 帮我研究一下新能源汽车市场

Agent:
1. 调用 submit_research.py 提交任务
2. 获取 task_id
3. 返回用户: "任务已提交 (ID: xxx)，预计需要5-10分钟。我会定期检查并在完成后通知你。"
4. (可选) 启动后台进程监控状态
5. (可选) 通过cron定期检查
```

## 状态码说明

| 状态 | 说明 |
|------|------|
| pending | 等待处理 |
| processing | 处理中 |
| completed | 完成 |
| failed | 失败 |

## 超时建议

| 研究模式 | 建议超时 |
|----------|----------|
| basic | 300秒 |
| deep | 1800秒 |
| industry | 3600秒 |
| expert | 7200秒 |
