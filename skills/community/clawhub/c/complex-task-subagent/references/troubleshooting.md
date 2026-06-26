# 故障排查

> 复杂任务指挥子代理的常见问题和解决方案

---

## 📚 目录

- [子代理问题](#子代理问题)
- [检查点问题](#检查点问题)
- [Heartbeat 问题](#heartbeat-问题)
- [状态文件问题](#状态文件问题)
- [Gitee 同步问题](#gitee-同步问题)
- [性能问题](#性能问题)
- [调试技巧](#调试技巧)

---

## 子代理问题

### 问题 1：子代理无法启动

**症状**：
```
Error: Failed to spawn subagent
```

**可能原因**：
1. OpenClaw Gateway 未运行
2. 子代理服务未配置
3. 网络问题
4. 资源不足

**排查步骤**：

1. 检查 Gateway 状态：
   ```bash
   openclaw gateway status
   ```

2. 检查子代理列表：
   ```bash
   subagents list
   ```

3. 检查日志：
   ```bash
   openclaw gateway logs --tail 100
   ```

4. 检查系统资源：
   ```bash
   free -h
   df -h
   ```

**解决方案**：

1. 启动 Gateway：
   ```bash
   openclaw gateway start
   ```

2. 检查网络连接：
   ```bash
   ping google.com
   ```

3. 增加超时时间：
   ```json
   {
     "timeout": 3600000  // 1 小时
   }
   ```

---

### 问题 2：子代理超时

**症状**：
- 阶段状态一直是 "running"
- 超时时间已过
- 日志显示超时错误

**可能原因**：
1. 任务过于复杂
2. 子代理卡死
3. 网络问题
4. API 限流

**排查步骤**：

1. 检查阶段状态：
   ```bash
   cat /root/.openclaw/workspace/task-progress.json | grep -A 10 "phase3"
   ```

2. 检查子代理日志：
   ```bash
   subagents list
   # 找到对应的 subagent ID
   # 查看详细日志
   ```

3. 检查网络连接：
   ```bash
   curl -I https://api.example.com
   ```

**解决方案**：

1. 增加超时时间：
   ```json
   {
     "timeout": 7200000  // 2 小时
   }
   ```

2. 重新启动子代理：
   ```bash
   # 手动重试
   sessions_spawn --task "..." --label "subagent-name" ...
   ```

3. 分解任务：
   - 将大任务拆分为多个小任务
   - 每个小任务独立执行

---

### 问题 3：子代理崩溃

**症状**：
- 子代理状态变为 "failed"
- 日志显示异常错误
- 检查点文件未创建

**可能原因**：
1. 代码错误
2. 资源不足
3. 依赖问题
4. 权限问题

**排查步骤**：

1. 查看崩溃日志：
   ```bash
   openclaw gateway logs --tail 200 | grep -i error
   ```

2. 检查检查点目录：
   ```bash
   ls -la /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints/
   ```

3. 检查权限：
   ```bash
   ls -la /root/.openclaw/workspace/
   ```

**解决方案**：

1. 修复代码错误：
   - 查看详细错误信息
   - 修复代码后重试

2. 增加资源限制：
   ```bash
   # 增加 Node.js 内存限制
   export NODE_OPTIONS="--max-old-space-size=4096"
   ```

3. 修复权限：
   ```bash
   chmod -R 755 /root/.openclaw/workspace/
   ```

---

### 问题 4：子代理结果错误

**症状**：
- 子代理完成但结果不正确
- 输出文件格式错误
- 数据不完整

**可能原因**：
1. 任务描述不清晰
2. 子代理理解错误
3. 数据质量问题

**排查步骤**：

1. 检查输出文件：
   ```bash
   cat /root/.openclaw/workspace/output/result.md
   ```

2. 检查检查点：
   ```bash
   cat /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints/phaseX.json
   ```

3. 验证任务描述：
   - 是否足够具体？
   - 是否有歧义？

**解决方案**：

1. 改进任务描述：
   - 更具体，避免模糊表述
   - 提供示例
   - 明确输出格式

2. 增加验证步骤：
   - 子代理完成前自我验证
   - 主会话验证结果

3. 使用参考文档：
   - 提供 examples/
   - 提供模板

---

## 检查点问题

### 问题 1：检查点文件未创建

**症状**：
- 子代理显示完成
- 但 checkpoints/ 目录为空
- Heartbeat 无法推进下一阶段

**可能原因**：
1. 子代理忘记写入检查点
2. 检查点路径错误
3. 权限问题

**排查步骤**：

1. 检查 checkpoints 目录：
   ```bash
   ls -la /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints/
   ```

2. 检查权限：
   ```bash
   ls -ld /root/.openclaw/workspace/complex-task-subagent-experience/
   ```

3. 检查子代理日志：
   ```bash
   openclaw gateway logs --tail 100
   ```

**解决方案**：

1. 在任务描述中明确要求写入检查点：
   ```
   "完成后必须写入检查点文件到
    /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints/phase1.json"
   ```

2. 修复权限：
   ```bash
   mkdir -p /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints
   chmod 755 /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints
   ```

3. 使用检查点写入脚本：
   ```python
   # 在子代理中
   from scripts.checkpoint_writer import write_checkpoint
   write_checkpoint("phase1.json", {...})
   ```

---

### 问题 2：检查点文件格式错误

**症状**：
- 检查点文件存在但 JSON 无效
- Heartbeat 无法读取检查点
- 推进失败

**可能原因**：
1. JSON 格式错误
2. 编码问题
3. 文件损坏

**排查步骤**：

1. 验证 JSON 格式：
   ```bash
   python3 -m json.tool phase1.json
   ```

2. 检查编码：
   ```bash
   file phase1.json
   ```

**解决方案**：

1. 修复 JSON：
   ```bash
   python3 -m json.tool phase1.json > phase1-fixed.json
   mv phase1-fixed.json phase1.json
   ```

2. 使用 JSON 写入函数：
   ```python
   import json

   with open(checkpoint_file, 'w', encoding='utf-8') as f:
       json.dump(data, f, indent=2, ensure_ascii=False)
   ```

---

### 问题 3：检查点文件过时

**症状**：
- 检查点文件存在但内容不匹配
- 状态文件显示不同状态
- 推进逻辑混乱

**可能原因**：
1. 手动修改了状态文件
2. 检查点文件未更新
3. 时间戳不同步

**排查步骤**：

1. 检查文件时间戳：
   ```bash
   stat task-progress.json
   stat checkpoints/phase1.json
   ```

2. 比对状态：
   ```bash
   cat task-progress.json | grep phase1
   cat checkpoints/phase1.json
   ```

**解决方案**：

1. 以 task-progress.json 为准（SSOT）：
   - 重新生成检查点
   - 更新状态文件

2. 添加时间戳验证：
   ```python
   checkpoint_time = os.path.getmtime(checkpoint_file)
   if checkpoint_time < expected_time:
       raise Exception("检查点文件过时")
   ```

---

## Heartbeat 问题

### 问题 1：Heartbeat 未触发

**症状**：
- 任务已完成但未同步到 Gitee
- 日志中没有 Heartbeat 记录
- 任务状态一直是 "in_progress"

**可能原因**：
1. HEARTBEAT.md 未配置
2. 心跳频率设置过大
3. Gateway 未运行

**排查步骤**：

1. 检查 HEARTBEAT.md：
   ```bash
   cat /root/.openclaw/workspace/HEARTBEAT.md
   ```

2. 检查 Gateway 状态：
   ```bash
   openclaw gateway status
   ```

3. 检查心跳配置：
   ```bash
   cat /root/.openclaw/openclaw.json | grep -A 10 heartbeat
   ```

**解决方案**：

1. 配置 HEARTBEAT.md：
   ```markdown
   # 任务检查清单

   1. 读取 task-progress.json
   2. 检查 checkpoints/ 目录
   3. 比对检查点和任务进度，更新状态
   4. 如果阶段完成但下一阶段未启动，自动推进
   5. 如果所有阶段完成，同步到 Gitee
   6. 记录操作日志
   7. 如果没有需要推进的内容，回复 HEARTBEAT_OK
   ```

2. 配置心跳频率：
   ```json
   {
     "agents": {
       "defaults": {
         "heartbeat": {
           "every": "10m"
         }
       }
     }
   }
   ```

3. 启动 Gateway：
   ```bash
   openclaw gateway start
   ```

---

### 问题 2：Heartbeat 频率过高

**症状**：
- Token 消耗过快
- 日志中大量重复的 HEARTBEAT_OK
- 成本增加

**可能原因**：
1. 心跳频率设置过小
2. 任务已完成但心跳仍在运行

**排查步骤**：

1. 检查心跳频率：
   ```bash
   cat /root/.openclaw/openclaw.json | grep "every"
   ```

2. 检查任务状态：
   ```bash
   cat /root/.openclaw/workspace/task-progress.json | grep status
   ```

**解决方案**：

1. 调整心跳频率：
   ```json
   {
     "every": "30m"  // 改为 30 分钟
   }
   ```

2. 任务完成后停止心跳：
   ```markdown
   # HEARTBEAT.md

   如果 task-progress.json 显示 status="completed"：
   - 回复 HEARTBEAT_OK
   - 不执行任何检查
   ```

---

### 问题 3：Heartbeat 推进失败

**症状**：
- Heartbeat 检测到检查点但无法推进
- 日志显示错误
- 下一阶段未启动

**可能原因**：
1. 依赖条件不满足
2. 子代理启动失败
3. 状态更新失败

**排查步骤**：

1. 检查 Heartbeat 日志：
   ```bash
   tail -100 /root/.openclaw/workspace/task-monitor.log
   ```

2. 检查依赖条件：
   ```bash
   cat task-progress.json | grep dependencies
   ```

3. 尝试手动推进：
   ```bash
   # 手动启动下一阶段
   sessions_spawn --task "..." --label "..."
   ```

**解决方案**：

1. 检查依赖逻辑：
   - 确保所有依赖阶段已完成
   - 检查依赖名称是否正确

2. 增加错误处理：
   ```python
   try:
       start_next_phase()
   except Exception as e:
       logger.error(f"推进阶段失败: {e}")
       notify_user(f"推进失败: {e}")
   ```

---

## 状态文件问题

### 问题 1：task-progress.json 损坏

**症状**：
- 无法读取状态文件
- JSON 解析错误
- 任务中断

**可能原因**：
1. 写入过程中崩溃
2. 磁盘空间不足
3. 手动编辑错误

**排查步骤**：

1. 验证 JSON 格式：
   ```bash
   python3 -m json.tool task-progress.json
   ```

2. 检查磁盘空间：
   ```bash
   df -h
   ```

**解决方案**：

1. 修复 JSON：
   ```bash
   # 备份
   cp task-progress.json task-progress.json.backup

   # 尝试修复
   python3 -m json.tool task-progress.json > task-progress-fixed.json
   mv task-progress-fixed.json task-progress.json
   ```

2. 从备份恢复：
   ```bash
   cp task-progress.json.backup task-progress.json
   ```

3. 使用原子写入：
   ```python
   import tempfile
   import os

   # 先写入临时文件
   with tempfile.NamedTemporaryFile(
       mode='w',
       dir=os.path.dirname(filepath),
       delete=False
   ) as f:
       json.dump(data, f, indent=2)
       temp_path = f.name

   # 原子性重命名
   os.rename(temp_path, filepath)
   ```

---

### 问题 2：状态不一致

**症状**：
- task-progress.json 和 checkpoints 不一致
- 已完成的阶段显示为 "running"
- 推进逻辑混乱

**可能原因**：
1. 多个进程同时修改
2. 手动修改了状态文件
3. 检查点文件更新延迟

**排查步骤**：

1. 比对状态：
   ```bash
   # task-progress.json
   cat task-progress.json | grep -A 5 "phase3"

   # checkpoint
   cat checkpoints/phase3.json | grep status
   ```

2. 检查修改历史：
   ```bash
   git log --oneline task-progress.json
   ```

**解决方案**：

1. 以 task-progress.json 为准：
   - 重新生成检查点
   - 忽略不一致的检查点

2. 实现状态同步：
   ```python
   def sync_status_with_checkpoint(task_progress, phase_id, checkpoint_file):
       """根据检查点同步状态"""

       # 读取检查点
       with open(checkpoint_file, 'r') as f:
           checkpoint = json.load(f)

       # 更新状态
       if checkpoint["status"] == "completed":
           task_progress["phases"][phase_id]["status"] = "completed"
           task_progress["phases"][phase_id]["completedAt"] = checkpoint["completedAt"]

       # 保存
       save_task_progress(task_progress)
   ```

3. 避免并发修改：
   - 使用文件锁
   - 单一控制源

---

## Gitee 同步问题

### 问题 1：Git push 失败

**症状**：
- 任务完成但无法推送到 Gitee
- 日志显示 push 错误
- 远程仓库未更新

**可能原因**：
1. 网络问题
2. 认证问题
3. 冲突

**排查步骤**：

1. 测试网络连接：
   ```bash
   ping gitee.com
   ```

2. 测试 SSH 连接：
   ```bash
   ssh -T git@gitee.com
   ```

3. 查看 Git 状态：
   ```bash
   cd /root/.openclaw
   git status
   ```

4. 尝试手动推送：
   ```bash
   git push
   ```

**解决方案**：

1. 修复网络连接：
   ```bash
   # 检查代理设置
   git config --get http.proxy
   git config --get https.proxy

   # 如果需要，设置代理
   git config --global http.proxy http://proxy.example.com:8080
   ```

2. 修复 SSH 密钥：
   ```bash
   # 生成新密钥
   ssh-keygen -t ed25519 -C "your_email@example.com"

   # 添加到 SSH agent
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519

   # 复制公钥到 Gitee
   cat ~/.ssh/id_ed25519.pub
   ```

3. 解决冲突：
   ```bash
   git pull --rebase
   git push
   ```

---

### 问题 2：Commit 信息错误

**症状**：
- Commit 信息不符合要求
- 推送成功但无法追踪

**可能原因**：
1. 脚本中 commit 格式错误
2. 缺少必要的元数据

**解决方案**：

使用标准化的 commit 格式：
```bash
COMMIT_MSG="任务完成：$(date '+%Y-%m-%d %H:%M')
Task: ${TASK_NAME}
Phases: ${COMPLETED_PHASES}/${TOTAL_PHASES}
Duration: ${ELAPSED_TIME}"

git commit -m "$COMMIT_MSG"
```

---

## 性能问题

### 问题 1：子代理启动慢

**症状**：
- 每个子代理启动需要很长时间
- 任务执行缓慢

**可能原因**：
1. 系统资源不足
2. 网络延迟
3. 大量依赖加载

**排查步骤**：

1. 检查系统资源：
   ```bash
   free -h
   top
   ```

2. 测试网络：
   ```bash
   curl -o /dev/null -s -w "%{time_total}\n" https://api.example.com
   ```

**解决方案**：

1. 增加系统资源：
   - 增加 Node.js 内存限制
   - 释放不必要的进程

2. 使用缓存：
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def load_reference(ref_file):
       # 缓存引用文档
       ...
   ```

3. 预加载依赖：
   ```bash
   # 在任务开始前预加载
   npm cache verify
   ```

---

### 问题 2：Token 消耗过多

**症状**：
- API 调用成本过高
- 日志显示大量重复内容

**可能原因**：
1. 子代理传递过多上下文
2. 重复执行相同操作
3. Heartbeat 频率过高

**解决方案**：

1. 优化上下文传递：
   ```bash
   # 只传递必要的上下文
   sessions_spawn \
     --task "任务描述" \
     --cwd "/root/.openclaw/workspace" \
     --context "minimal"
   ```

2. 使用引用文档：
   ```markdown
   # SKILL.md

   详见: [references/advanced-patterns.md](references/advanced-patterns.md)
   ```

3. 调整 Heartbeat 频率：
   ```json
   {
     "every": "30m"
   }
   ```

---

## 调试技巧

### 1. 启用详细日志

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/.openclaw/workspace/debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.debug("调试信息")
```

### 2. 使用断点调试

```python
import pdb

def start_subagent(phase_id, phase):
    logger.debug(f"启动阶段: {phase_id}")

    # 设置断点
    pdb.set_trace()

    # 继续执行...
```

### 3. 记录执行时间

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.time()
    yield
    end = time.time()
    logger.debug(f"{label} 耗时: {end - start:.2f} 秒")

# 使用
with timer("阶段1执行"):
    execute_phase1()
```

### 4. 单元测试

```python
import unittest

class TestTaskProgress(unittest.TestCase):
    def test_update_phase_status(self):
        task_progress = create_test_task_progress()
        update_phase_status(task_progress, "phase1", "completed")
        self.assertEqual(
            task_progress["phases"]["phase1"]["status"],
            "completed"
        )

if __name__ == "__main__":
    unittest.main()
```

### 5. 模拟子代理

```python
def mock_subagent(task, label, runtime="subagent"):
    """模拟子代理，用于测试"""
    logger.info(f"模拟子代理: {label}")

    # 模拟执行
    time.sleep(1)

    # 模拟检查点
    checkpoint = {
        "phase": label,
        "status": "completed",
        "completedAt": time.time()
    }

    write_checkpoint(f"{label}.json", checkpoint)
    return checkpoint

# 在测试中使用
if __name__ == "__main__":
    mock_subagent("测试任务", "test-phase")
```

---

## 总结

1. **保持日志清晰** - 记录足够的信息，但不要过多
2. **使用错误分类** - 区分临时性错误、可恢复错误和致命错误
3. **实现重试机制** - 对于临时性错误自动重试
4. **提供监控** - 实时监控任务进度
5. **文档化流程** - 记录已知问题和解决方案
6. **定期备份** - 备份状态文件和检查点
7. **优雅降级** - 失败时提供清晰的错误信息

---

**相关文档**：
- [quick-start.md](quick-start.md) - 快速开始
- [advanced-patterns.md](advanced-patterns.md) - 高级模式
