# 迭代模式参考

> coding-framework 的迭代循环机制详细说明。

## 概述

借鉴 Claude Code Ralph Wiggum 的 Stop Hook 自引用循环模式，通过状态文件 + 循环控制器实现可控的迭代执行。

## 迭代模式

### fixed（固定次数）

执行指定次数后停止，不做完成条件判断。

```bash
python scripts/loop-controller.py init --mode fixed --max 5
```

适用场景：已知需要 N 轮迭代的任务。

### max（最大次数 + 完成条件）

最多执行 N 次，满足完成条件时提前退出。

```bash
python scripts/loop-controller.py init --mode max --max 10 --condition "regex:BUILD SUCCESS"
```

适用场景：有明确完成标准但不确定需要多少轮。

### adaptive（自适应）

根据每轮改进幅度动态决定是否继续。连续 N 轮无改进则停止。

```bash
python scripts/loop-controller.py init --mode adaptive --max 20 --patience 3
```

适用场景：不确定需要多少轮，希望自动收敛。

## 完成条件类型

| 类型 | 说明 | 示例 |
|------|------|------|
| regex | 在最后一轮 summary 中匹配正则 | `regex:All tests passed` |
| file | 检查文件是否存在 | `file:output/result.txt` |
| file-changed | 检查文件是否在最近一轮被修改 | `file-changed:src/main.py` |
| llm | 由 LLM 评估（需外部处理） | `llm:代码质量达到可发布标准` |

## 工作流

### 1. 初始化循环

```bash
python scripts/loop-controller.py init \
  --name "refactor-module" \
  --mode max \
  --max 10 \
  --condition "regex:All tests passed"
```

### 2. 执行迭代

每轮迭代的标准流程：

```
1. 检查状态 → loop-controller.py check
2. 执行任务 → 运行实际工作
3. 评估结果 → 检查完成条件
4. 更新状态 → loop-controller.py update --result ...
5. 如果完成 → loop-controller.py complete
```

### 3. 与 sessions_spawn 集成

```
主代理：初始化循环 → loop-controller.py init
  ↓
循环开始：
  → sessions_spawn（子代理执行一轮迭代）
  → 子代理完成后报告结果
  → loop-controller.py update --result <结果>
  → loop-controller.py check（是否继续）
  ↓
循环结束：loop-controller.py complete
```

## 状态文件格式

```json
{
  "name": "任务名称",
  "mode": "fixed|max|adaptive",
  "max_iterations": 10,
  "current_iteration": 3,
  "completion_check": {
    "type": "regex|file|file-changed|llm",
    "pattern": "检测模式"
  },
  "patience": 3,
  "no_improvement_count": 0,
  "history": [
    {
      "iteration": 1,
      "timestamp": "2026-06-26T22:00:00",
      "result": "pass|fail|partial",
      "summary": "本轮做了什么",
      "metrics": {}
    }
  ],
  "artifacts": ["产出文件列表"],
  "status": "running|completed|failed|cancelled",
  "metadata": {}
}
```

## 命令参考

| 命令 | 说明 | 关键参数 |
|------|------|----------|
| init | 初始化循环 | `--name --mode --max --condition --patience --state` |
| check | 检查是否应继续 | `--state` |
| update | 更新迭代结果 | `--state --result --summary --metrics --artifact` |
| complete | 标记循环完成 | `--state --reason --status` |

## Stop Hook 集成

`hooks/stop-iteration.sh` 在会话结束前检查：
- 是否有活跃的迭代循环（loop-state.json status=running）
- 是否有待完成的承诺（.pending-promises）
- 未完成则阻止停止，返回提示信息

## 使用示例

### 代码重构迭代

```bash
python scripts/loop-controller.py init --name "refactor" --mode max --max 5 --condition "regex:coverage.*90%"
python scripts/loop-controller.py check --state loop-state.json
# → 执行重构...
python scripts/loop-controller.py update --state loop-state.json --result pass --summary "提取了3个函数"
python scripts/loop-controller.py complete --state loop-state.json --reason "覆盖率达到92%"
```

### 测试修复迭代

```bash
python scripts/loop-controller.py init --name "fix-tests" --mode adaptive --max 15 --patience 3
# 每轮：运行测试 → 修复失败 → 记录结果
# 连续3轮无进展时自动停止
```
