# 大模型能力等级与权限规则

每次唤醒时读取此文件，确定当前模型的能力等级和操作权限。

## 能力等级映射表

> 此表由创建者和老板一起维护。发现新模型时，查询其能力并更新此表。
> 判断依据：上下文窗口大小、推理能力、工具调用能力综合评估。

### 高等级模型（推理能力强，适合独立决策）

- claude-opus-4-6 (1M/200K)
- gpt-5.2 / gpt-5.1 / o3
- gemini-3.1-pro / gemini-3-pro / gemini-2.5-pro
- deepseek-v4 / deepseek-v3.2-speciale
- glm-5
- grok-4.1

### 中等级模型（推理能力中上，核心操作需老板确认）

- claude-sonnet-4-6 / claude-sonnet-4-5
- gpt-5-mini / gpt-4.1 / o1
- gemini-3-flash / gemini-2.5-flash
- deepseek-v3 / deepseek-r1
- kimi-k2.5 / kimi-k2
- glm-4.7 / glm-4.5
- qwen-3.5 / qwen-3-max-thinking

### 低等级模型（推理能力较弱，仅适合资料收集）

- claude-haiku-4-5
- gpt-4o-mini
- gemini-flash-lite
- deepseek-v2-lite
- glm-4-flash
- qwen-turbo
- 未在此表中的模型 → 上网查询后归类并更新此表

## 权限规则

### 高等级 — 无限制
- 可执行所有命令
- 可修改所有文件
- 可独立决策

### 中等级 — 受限修改
- 不可修改核心 memory 文件（learning-plan.md、agents-registry.md）
- 可修改 knowledge/ 目录下的知识库文件
- 核心决策前需提示老板确认

### 低等级 — 只读 + 收集
- 只能创建新文件、追加日志和报告
- 不可修改任何现有文件
- 适合做资料收集和学习素材整理
