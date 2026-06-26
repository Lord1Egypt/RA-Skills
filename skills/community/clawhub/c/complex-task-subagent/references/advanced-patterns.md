# 高级模式

> 复杂任务指挥子代理的高级使用模式和最佳实践

---

## 📚 目录

- [并行任务执行](#并行任务执行)
- [条件分支](#条件分支)
- [动态阶段生成](#动态阶段生成)
- [任务链和依赖](#任务链和依赖)
- [错误恢复策略](#错误恢复策略)
- [监控和可视化](#监控和可视化)
- [性能优化](#性能优化)

---

## 并行任务执行

### 场景

当多个任务可以同时执行且无依赖关系时，使用并行模式。

### 实现方式

```json
{
  "taskId": "parallel-task-20260312",
  "executionMode": "parallel",
  "phases": {
    "phase1": {
      "name": "审核文档 A",
      "status": "pending",
      "dependencies": [],
      "parallelGroup": 1
    },
    "phase2": {
      "name": "审核文档 B",
      "status": "pending",
      "dependencies": [],
      "parallelGroup": 1
    },
    "phase3": {
      "name": "审核文档 C",
      "status": "pending",
      "dependencies": [],
      "parallelGroup": 1
    },
    "phase4": {
      "name": "合并审核结果",
      "status": "pending",
      "dependencies": ["phase1", "phase2", "phase3"],
      "parallelGroup": 2
    }
  }
}
```

### 启动逻辑

```python
def start_parallel_phases(task_progress):
    """启动并行阶段的子代理"""

    # 找到所有可以启动的阶段
    ready_phases = []
    for phase_id, phase in task_progress["phases"].items():
        if phase["status"] == "pending":
            # 检查依赖
            deps_satisfied = True
            for dep in phase.get("dependencies", []):
                if task_progress["phases"][dep]["status"] != "completed":
                    deps_satisfied = False
                    break

            if deps_satisfied:
                ready_phases.append(phase_id)

    # 按并行分组
    groups = {}
    for phase_id in ready_phases:
        group = task_progress["phases"][phase_id].get("parallelGroup", 1)
        if group not in groups:
            groups[group] = []
        groups[group].append(phase_id)

    # 启动每个组
    for group_id, phase_ids in groups.items():
        print(f"启动并行组 {group_id}: {phase_ids}")
        for phase_id in phase_ids:
            phase = task_progress["phases"][phase_id]
            start_subagent(phase_id, phase)
```

### 注意事项

- ⚠️ 确保并行任务之间没有资源冲突
- ⚠️ 监控子代理数量，避免过多并发
- ✅ 合理设置超时时间
- ✅ 记录并行任务的启动和完成顺序

---

## 条件分支

### 场景

根据前一个阶段的结果，决定执行哪个后续阶段。

### 实现方式

```json
{
  "taskId": "conditional-task-20260312",
  "phases": {
    "phase1": {
      "name": "审核代码",
      "status": "pending",
      "branches": {
        "no_issues": {
          "nextPhase": "phase2",
          "condition": "result.issues.length == 0"
        },
        "has_issues": {
          "nextPhase": "phase3",
          "condition": "result.issues.length > 0"
        }
      }
    },
    "phase2": {
      "name": "直接部署",
      "status": "pending",
      "dependencies": ["phase1"]
    },
    "phase3": {
      "name": "修复问题",
      "status": "pending",
      "dependencies": ["phase1"]
    }
  }
}
```

### 条件评估逻辑

```python
def evaluate_conditional_branch(task_progress, phase_id, checkpoint):
    """评估条件分支"""

    phase = task_progress["phases"][phase_id]
    branches = phase.get("branches", {})

    # 读取检查点
    import json
    with open(checkpoint, 'r') as f:
        checkpoint_data = json.load(f)

    # 评估每个分支
    for branch_name, branch_config in branches.items():
        condition = branch_config.get("condition", "")

        # 简单的条件评估
        # 实际应用中可能需要更复杂的表达式解析
        try:
            # 示例：eval("result.issues.length == 0")
            # 安全起见，应该使用表达式解析器
            if eval(condition, {"result": checkpoint_data.get("result", {})}):
                return branch_config["nextPhase"]
        except Exception as e:
            print(f"条件评估失败: {e}")

    # 默认分支
    return phase.get("defaultNextPhase", None)
```

### 最佳实践

- ✅ 为每个分支定义清晰的退出条件
- ✅ 提供默认分支以防所有条件都不匹配
- ⚠️ 避免过于复杂的条件逻辑
- ✅ 在检查点中记录决策依据

---

## 动态阶段生成

### 场景

在运行时根据数据动态生成任务阶段。

### 示例：批量处理文件

```python
def generate_dynamic_phases(input_files):
    """根据输入文件动态生成阶段"""

    phases = {}
    base_phase_id = 0

    for file_path in input_files:
        phase_id = f"phase{base_phase_id}"
        base_phase_id += 1

        phases[phase_id] = {
            "name": f"处理文件: {file_path}",
            "status": "pending",
            "timeout": 600000,  # 10 分钟
            "maxRetries": 2,
            "checkpoint": f"checkpoint-{base_phase_id}.json",
            "output": f"output-{base_phase_id}.json",
            "input": file_path
        }

    # 添加汇总阶段
    phases["final"] = {
        "name": "汇总所有结果",
        "status": "pending",
        "dependencies": list(phases.keys())[:-1],
        "timeout": 300000,
        "maxRetries": 1
    }

    return phases
```

### 使用示例

```python
# 获取输入文件
import glob
input_files = glob.glob("/root/.openclaw/workspace/input/*.md")

# 动态生成阶段
phases = generate_dynamic_phases(input_files)

# 创建任务进度
task_progress = {
    "taskId": "dynamic-task-20260312",
    "taskName": "批量处理文件",
    "status": "in_progress",
    "phases": phases,
    "totalPhases": len(phases),
    "completedPhases": 0,
    "currentPhase": 0
}

# 保存到文件
import json
with open("/root/.openclaw/workspace/task-progress.json", 'w') as f:
    json.dump(task_progress, f, indent=2)
```

### 优点

- ✅ 灵活适应不同的输入
- ✅ 避免硬编码任务结构
- ✅ 易于扩展和维护

---

## 任务链和依赖

### 场景

复杂任务通常需要多个任务链，每个链内部有序，链之间可以并行。

### 依赖图示例

```
任务链 A：
  phase1 → phase2 → phase3
         ↓
任务链 B：
  phase4 → phase5

任务链 C：
  phase6 → phase7

最终汇总：
  phase8 (依赖 phase3, phase5, phase7)
```

### 配置示例

```json
{
  "taskId": "task-chains-20260312",
  "chains": {
    "chain-a": ["phase1", "phase2", "phase3"],
    "chain-b": ["phase4", "phase5"],
    "chain-c": ["phase6", "phase7"]
  },
  "phases": {
    "phase1": {
      "name": "数据采集",
      "status": "pending",
      "chain": "chain-a",
      "dependencies": []
    },
    "phase2": {
      "name": "数据清洗",
      "status": "pending",
      "chain": "chain-a",
      "dependencies": ["phase1"]
    },
    "phase3": {
      "name": "数据分析",
      "status": "pending",
      "chain": "chain-a",
      "dependencies": ["phase2"]
    },
    "phase4": {
      "name": "模型训练",
      "status": "pending",
      "chain": "chain-b",
      "dependencies": ["phase1"]
    },
    "phase5": {
      "name": "模型评估",
      "status": "pending",
      "chain": "chain-b",
      "dependencies": ["phase4"]
    },
    "phase6": {
      "name": "报告生成",
      "status": "pending",
      "chain": "chain-c",
      "dependencies": ["phase2"]
    },
    "phase7": {
      "name": "报告润色",
      "status": "pending",
      "chain": "chain-c",
      "dependencies": ["phase6"]
    },
    "phase8": {
      "name": "最终汇总",
      "status": "pending",
      "dependencies": ["phase3", "phase5", "phase7"]
    }
  }
}
```

### 依赖解析算法

```python
def resolve_dependencies(task_progress):
    """解析依赖关系，返回可以启动的阶段"""

    ready_phases = []

    for phase_id, phase in task_progress["phases"].items():
        if phase["status"] != "pending":
            continue

        # 检查所有依赖是否完成
        all_deps_completed = True
        for dep in phase.get("dependencies", []):
            dep_phase = task_progress["phases"].get(dep)
            if not dep_phase or dep_phase["status"] != "completed":
                all_deps_completed = False
                break

        if all_deps_completed:
            ready_phases.append(phase_id)

    return ready_phases
```

### 最佳实践

- ✅ 使用 DAG（有向无环图）表示依赖
- ✅ 避免循环依赖
- ✅ 提供依赖关系的可视化工具
- ⚠️ 限制依赖深度，避免过于复杂的依赖链

---

## 错误恢复策略

### 场景

子代理失败后，根据错误类型采取不同的恢复策略。

### 错误分类

```python
class ErrorType:
    TRANSIENT = "transient"      # 临时性错误（网络、超时）
    RECOVERABLE = "recoverable"  # 可恢复错误（数据问题）
    FATAL = "fatal"              # 致命错误（配置错误）
```

### 恢复策略配置

```json
{
  "errorHandling": {
    "defaultStrategy": "retry",
    "strategies": {
      "transient": {
        "action": "retry",
        "maxRetries": 5,
        "backoff": "exponential",
        "backoffMultiplier": 2
      },
      "recoverable": {
        "action": "rollback_and_retry",
        "maxRetries": 3,
        "rollbackPhase": "previous"
      },
      "fatal": {
        "action": "fail_and_notify",
        "notifyUser": true,
        "skipPhase": false
      }
    }
  }
}
```

### 错误检测和恢复逻辑

```python
def handle_error(task_progress, phase_id, error):
    """处理子代理错误"""

    phase = task_progress["phases"][phase_id]

    # 判断错误类型
    error_type = classify_error(error)

    # 获取恢复策略
    strategy_config = task_progress["errorHandling"]["strategies"].get(error_type)
    action = strategy_config.get("action", "retry")

    if action == "retry":
        # 重试
        if phase["retries"] < strategy_config["maxRetries"]:
            phase["retries"] += 1
            print(f"重试阶段 {phase_id} (第 {phase['retries']} 次)")

            # 指数退避
            if strategy_config.get("backoff") == "exponential":
                wait_time = 30 * (strategy_config["backoffMultiplier"] ** phase["retries"])
                time.sleep(wait_time)

            restart_subagent(phase_id, phase)
        else:
            mark_phase_failed(phase_id, "超过最大重试次数")

    elif action == "rollback_and_retry":
        # 回滚并重试
        rollback_to_checkpoint(phase_id)
        phase["retries"] += 1
        restart_subagent(phase_id, phase)

    elif action == "fail_and_notify":
        # 失败并通知
        mark_phase_failed(phase_id, str(error))
        if strategy_config.get("notifyUser"):
            notify_user(f"阶段 {phase_id} 失败: {error}")

def classify_error(error):
    """分类错误"""

    error_message = str(error).lower()

    if "timeout" in error_message or "network" in error_message:
        return ErrorType.TRANSIENT
    elif "data" in error_message or "format" in error_message:
        return ErrorType.RECOVERABLE
    else:
        return ErrorType.FATAL
```

### 最佳实践

- ✅ 提供详细的错误日志
- ✅ 实现自动重试机制
- ✅ 设置合理的超时时间
- ✅ 关键失败时及时通知用户
- ⚠️ 避免无限重试导致资源浪费

---

## 监控和可视化

### 场景

实时监控任务进度和子代理状态。

### 监控指标

```python
class TaskMetrics:
    def __init__(self, task_progress):
        self.task_progress = task_progress

    def get_progress_percentage(self):
        """获取任务完成百分比"""
        return (self.task_progress["completedPhases"] /
                self.task_progress["totalPhases"]) * 100

    def get_running_phases(self):
        """获取正在运行的阶段"""
        return [
            (phase_id, phase)
            for phase_id, phase in self.task_progress["phases"].items()
            if phase["status"] == "running"
        ]

    def get_failed_phases(self):
        """获取失败的阶段"""
        return [
            (phase_id, phase)
            for phase_id, phase in self.task_progress["phases"].items()
            if phase["status"] == "failed"
        ]

    def get_elapsed_time(self):
        """获取任务已运行时间"""
        import time
        last_updated = self.task_progress["lastUpdated"]
        elapsed = time.time() - last_updated
        return elapsed

    def estimate_remaining_time(self):
        """估计剩余时间"""
        completed_phases = self.task_progress["completedPhases"]
        total_phases = self.task_progress["totalPhases"]
        elapsed = self.get_elapsed_time()

        if completed_phases == 0:
            return None

        avg_time_per_phase = elapsed / completed_phases
        remaining_phases = total_phases - completed_phases
        estimated_remaining = avg_time_per_phase * remaining_phases

        return estimated_remaining
```

### 生成进度报告

```python
def generate_progress_report(task_progress):
    """生成进度报告"""

    metrics = TaskMetrics(task_progress)

    report = {
        "taskId": task_progress["taskId"],
        "taskName": task_progress["taskName"],
        "progress": f"{metrics.get_progress_percentage():.1f}%",
        "completedPhases": task_progress["completedPhases"],
        "totalPhases": task_progress["totalPhases"],
        "runningPhases": len(metrics.get_running_phases()),
        "failedPhases": len(metrics.get_failed_phases()),
        "elapsedTime": f"{metrics.get_elapsed_time() / 60:.1f} 分钟",
        "estimatedRemaining": f"{metrics.estimate_remaining_time() / 60:.1f} 分钟" if metrics.estimate_remaining_time() else "未知",
        "phases": {}
    }

    for phase_id, phase in task_progress["phases"].items():
        report["phases"][phase_id] = {
            "name": phase["name"],
            "status": phase["status"],
            "retries": phase.get("retries", 0)
        }

    return report
```

### 可视化展示

```python
def print_progress_report(report):
    """打印进度报告"""

    print("=" * 60)
    print(f"任务: {report['taskName']}")
    print(f"进度: {report['progress']}")
    print(f"已完成: {report['completedPhases']}/{report['totalPhases']}")
    print(f"运行中: {report['runningPhases']}")
    print(f"失败: {report['failedPhases']}")
    print(f"已用时间: {report['elapsedTime']}")
    print(f"预计剩余: {report['estimatedRemaining']}")
    print("=" * 60)
    print("\n阶段详情:")
    for phase_id, phase_info in report["phases"].items():
        status_icon = {
            "pending": "⏳",
            "running": "🔄",
            "completed": "✅",
            "failed": "❌"
        }.get(phase_info["status"], "❓")

        retries_str = f" (重试 {phase_info['retries']} 次)" if phase_info["retries"] > 0 else ""
        print(f"  {status_icon} {phase_id}: {phase_info['name']}{retries_str}")
```

### Web Dashboard（可选）

使用 Flask 或 FastAPI 创建简单的 Web 界面：

```python
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

@app.route('/')
def dashboard():
    """任务监控 Dashboard"""
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/task/<task_id>')
def get_task_status(task_id):
    """获取任务状态 API"""
    task_progress = load_task_progress(task_id)
    report = generate_progress_report(task_progress)
    return jsonify(report)

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>任务监控</title>
</head>
<body>
    <h1>任务监控 Dashboard</h1>
    <div id="task-info"></div>
    <script>
        // 定期刷新
        setInterval(() => {
            fetch('/api/task/{{ task_id }}')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('task-info').innerHTML =
                        `<h2>${data.taskName}</h2>
                         <p>进度: ${data.progress}</p>
                         <p>已完成: ${data.completedPhases}/${data.totalPhases}</p>
                         ...`;
                });
        }, 5000);
    </script>
</body>
</html>
"""
```

---

## 性能优化

### 1. 子代理资源管理

```python
class SubagentPool:
    """子代理池，限制并发数量"""

    def __init__(self, max_concurrent=3):
        self.max_concurrent = max_concurrent
        self.running_subagents = []

    def can_start(self):
        """是否可以启动新的子代理"""
        return len(self.running_subagents) < self.max_concurrent

    def add(self, subagent_id):
        """添加子代理"""
        self.running_subagents.append(subagent_id)

    def remove(self, subagent_id):
        """移除子代理"""
        if subagent_id in self.running_subagents:
            self.running_subagents.remove(subagent_id)

# 使用示例
pool = SubagentPool(max_concurrent=3)

# 启动子代理前检查
if pool.can_start():
    subagent_id = start_subagent(...)
    pool.add(subagent_id)
else:
    print("子代理池已满，等待...")
```

### 2. 检查点批量写入

```python
class CheckpointBuffer:
    """检查点缓冲区，批量写入"""

    def __init__(self, buffer_size=5, flush_interval=30):
        self.buffer = []
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.last_flush = time.time()

    def add(self, checkpoint_data):
        """添加检查点到缓冲区"""
        self.buffer.append(checkpoint_data)

        # 缓冲区满或时间间隔到，写入文件
        if len(self.buffer) >= self.buffer_size or \
           time.time() - self.last_flush > self.flush_interval:
            self.flush()

    def flush(self):
        """刷新缓冲区，写入文件"""
        for checkpoint in self.buffer:
            write_checkpoint_to_file(checkpoint)
        self.buffer.clear()
        self.last_flush = time.time()
```

### 3. 增量状态更新

```python
def update_task_progress_incremental(task_progress, phase_id, updates):
    """增量更新任务状态"""

    # 只更新变化的字段
    if phase_id in task_progress["phases"]:
        for key, value in updates.items():
            task_progress["phases"][phase_id][key] = value

    # 更新最后修改时间
    task_progress["lastUpdated"] = time.time()

    # 保存到文件
    import json
    with open("/root/.openclaw/workspace/task-progress.json", 'w') as f:
        json.dump(task_progress, f, indent=2)
```

### 4. 日志轮转

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logger = logging.getLogger("task-monitor")
logger.setLevel(logging.INFO)

# 日志轮转：每个日志文件最大 10MB，保留 5 个备份
handler = RotatingFileHandler(
    "/root/.openclaw/workspace/task-monitor.log",
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
logger.addHandler(handler)

# 使用
logger.info("任务开始")
logger.info("阶段 1 完成")
```

---

## 最佳实践总结

1. **保持简单** - 从简单的串行任务开始，逐步增加复杂性
2. **单一职责** - 每个阶段只做一件事
3. **明确边界** - 明确定义阶段的输入和输出
4. **可测试** - 每个阶段都应该可以独立测试
5. **可恢复** - 使用检查点确保任务可以恢复
6. **可监控** - 提供足够的日志和监控指标
7. **合理超时** - 根据任务复杂度设置合理的超时时间
8. **优雅降级** - 失败时提供清晰的错误信息

---

**相关文档**：
- [quick-start.md](quick-start.md) - 快速开始
- [troubleshooting.md](troubleshooting.md) - 故障排查
