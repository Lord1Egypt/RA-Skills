# 使用指南 — 认知力增强引擎

## 安装

### 方式一：一键安装（推荐）

```bash
# Linux / macOS / WSL
bash scripts/setup.sh

# Windows
双击 scripts/setup.bat
# 或在 cmd 中运行:
scripts\setup.bat
```

安装脚本自动检测 Python 并验证引擎。

### 方式二：直接使用
```bash
# 复制 engine.py 到项目目录
cp skills/cognitive-enhancement-engine/engine.py ./my_project/
```

### 方式三：ClawHub 安装
```bash
clawhub install cognitive-enhancement-engine
cd cognitive-enhancement-engine
bash scripts/setup.sh  # 补充安装
```

## 快速上手

### 基础用法

```python
from engine import CognitiveEnhancer

# 初始化
brain = CognitiveEnhancer(long_term_capacity=100)

# 1. 记忆知识
brain.memorize("The Earth orbits the Sun.", importance=0.8)
brain.memorize("Light travels at 299,792,458 m/s.", importance=0.7)

# 2. 检索
results = brain.recall("speed of light", top_k=2)
for r in results:
    print(f"[{r['importance']:.1f}] {r['content']}")

# 3. 规划
plan = brain.plan("Calculate the time for light to reach Earth")
for step in plan:
    print(f"Step {step['step_id']}: {step['action']}")

# 4. 直接执行
result = brain.execute_task("What is the distance from Earth to Sun?")
print(result['result'])
```

### 工作记忆

```python
# 感知信息自动进入工作记忆
brain.perceive("User is asking about astronomy")
brain.perceive("Current topic: solar system")

# 工作记忆是 FIFO 队列
status = brain.get_status()
print(status['working_memory'])  # 最近 10 条
```

### 反思

```python
# 触发反思（基于过去的失败记录）
suggestions = brain.reflect()
for s in suggestions:
    print(f"Suggestion: {s}")
```

## 最佳实践

1. **记忆容量管理** — 设置合适的 `long_term_capacity`，超出时最早的记忆会被淘汰
2. **重要性权重** — 关键知识设 `importance=1.5`，临时信息设 `importance=0.5`
3. **定期反思** — 在任务间隙调用 `reflect()`，挖掘失败模式
4. **工作记忆大小** — 根据上下文窗口调整，默认 10 适合大多数场景

## 运行测试

```bash
# Python 测试
python scripts/test-basic.py

# Node.js 测试
node scripts/test-client.js

# 内置演示
python engine.py
```
