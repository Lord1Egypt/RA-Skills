# AI E2E Cases

## 目的

验证 AI 对本技能的理解和执行能力，包括：
- 意图路由正确性
- 命令选择准确性
- 模糊匹配能力
- 用户交互流程

---

## 标准流程测试

### Case 1: 高置信度 - 完全匹配直接激活

**用户输入**：切到企微

**预期 AI 行为**：
1. 执行 `find-window "企微" 5 --json`
2. 检查 `items[0]`，判定为完全匹配（别名映射）
3. 直接执行 `activate-window "企微" 1 --json`
4. 返回成功提示

**关键验证点**：AI 能识别别名"企微"→"企业微信"，无需询问用户

---

### Case 2: 中等置信度 - 部分匹配需确认

**用户输入**：切到文档

**预期 AI 行为**：
1. 执行 `find-window "文档" 5 --json`
2. 发现多个候选，不完全匹配
3. **询问用户**：列出候选列表
4. 用户回复序号后，执行 `activate-window "文档" <序号> --json`

**关键验证点**：AI 不盲目激活，有歧义时主动确认

---

### Case 3: 低置信度 - 无匹配重试

**用户输入**：切到不存在的窗口

**预期 AI 行为**：
1. 执行 `find-window "不存在的窗口" 3 --json`
2. 返回 `not_found`
3. 尝试简化关键词重试，或执行 `list-windows --json`
4. 告知用户未找到，并列出当前窗口

**关键验证点**：失败时优雅降级，提供有用信息

---

## 模糊匹配测试

### Case 4: 缩写匹配

**命令**：`find-window "企微" 3 --json`
**预期**：匹配到"企业微信"窗口
**状态期望**：`ok`，且企业微信在候选前列

---

### Case 5: 英文别名匹配

**命令**：`find-window "vscode" 3 --json`
**预期**：匹配到"Visual Studio Code"窗口
**状态期望**：`ok`

---

### Case 6: 跳跃字符匹配

**命令**：`find-window "qiyou" 3 --json`
**预期**：模糊匹配到"企业微信"
**状态期望**：`ok`

---

### Case 7: 连字符兼容

**命令**：`find-window "企业微信文档" 3 --json`
**目标窗口**："企业微信-文档"
**预期**：成功匹配
**状态期望**：`ok`

---

### Case 8: 大小写不敏感

**命令**：`find-window "CHROME" 3 --json`
**预期**：匹配到"chrome"或"Google Chrome"
**状态期望**：`ok`

---

## 具体命令测试

### Case 9: find-window 基础功能

**命令**：`scripts\d-switch.cmd find-window "微信" 3 --json`
**预期状态**：`ok`
**预期字段**：`mode="find"`, `count>0`, `items[0].title` 包含微信

---

### Case 10: activate-window 激活

**前提**：已通过 find-window 确认窗口存在
**命令**：`scripts\d-switch.cmd activate-window "微信" 1 --json`
**预期状态**：`activated`

---

### Case 11: activate-process 按进程激活

**命令**：`scripts\d-switch.cmd activate-process "Code" 1 --json`
**适用场景**：VS Code 等标题变化频繁的应用
**预期状态**：`activated`

---

### Case 12: activate-handle 精确激活

**前提**：通过 list-windows 获取有效句柄
**命令**：`scripts\d-switch.cmd activate-handle 0x2072C --json`
**预期状态**：`activated` 或 `not_found`

---

### Case 13: list-windows 列表

**命令**：`scripts\d-switch.cmd list-windows --json`
**预期状态**：`ok`
**预期字段**：`mode="list"`, `count>=0`

---

## 错误处理测试

### Case 14: 未找到目标

**命令**：`scripts\d-switch.cmd activate-window "xyz_not_exist" 1 --json`
**预期状态**：`not_found`
**退出码**：2

---

### Case 15: 候选序号越界

**命令**：`scripts\d-switch.cmd activate-window "微信" 99 --json`
**预期状态**：`choice_out_of_range`
**退出码**：4

---

### Case 16: 激活失败恢复

**命令**：`scripts\d-switch.cmd activate-window "some_protected_window" 1 --json`
**预期状态**：`activation_failed` 或 `not_found`
**AI 行为**：应重试1次，仍失败则降级到 `Dalt -1`

---

## 组合场景测试

### Case 17: 窗口 + 标签切换

**用户输入**：切到浏览器，再切到下一个标签

**预期 AI 行为**：
1. `activate-window "chrome" 1 --json`
2. 成功后 `Dctrl -1`

---

### Case 18: 多轮对话确认

**用户输入**：切到终端

**AI 行为**：
1. `find-window "终端" 3 --json`
2. 发现多个：Windows Terminal、CMD、Git Bash
3. **询问**："找到多个终端：1. Windows Terminal 2. CMD 3. Git Bash，请选择"
4. 用户：1
5. `activate-window "终端" 1 --json`

---

### Case 19: 进程名稳定激活

**用户输入**：切到 VS Code

**AI 判定**：VS Code 标题随文件变化，使用进程名更稳定

**预期行为**：
1. `find-window "vscode" 3 --json` 先确认
2. 或直接 `activate-process "Code" 1 --json`

---

## 防误触发测试

### Case 20: 纯知识询问（不触发）

**用户输入**：Alt+Tab 是什么快捷键？
**预期 AI 行为**：**不执行**任何脚本，仅解释快捷键功能

---

### Case 21: 纯概念讨论（不触发）

**用户输入**：Windows 怎么管理窗口？
**预期 AI 行为**：**不执行**任何脚本，仅讨论原理

---

### Case 22: 明确拒绝执行

**用户输入**：不要切窗口，我只想知道怎么切换
**预期 AI 行为**：**不执行**脚本，仅提供说明

---

## 执行速查表

| # | 场景 | 命令 | 预期状态 |
|---|------|------|----------|
| 1 | 完全匹配 | `activate-window "企微" 1 --json` | `activated` |
| 2 | 查找候选 | `find-window "文档" 5 --json` | `ok` |
| 3 | 别名匹配 | `find-window "vscode" 3 --json` | `ok` |
| 4 | 进程激活 | `activate-process "Code" 1 --json` | `activated` |
| 5 | 句柄激活 | `activate-handle 0x2072C --json` | `activated` |
| 6 | 列出窗口 | `list-windows --json` | `ok` |
| 7 | 未找到 | `activate-window "xyz" 1 --json` | `not_found` |
| 8 | 越界 | `activate-window "微信" 99 --json` | `choice_out_of_range` |
| 9 | 切标签 | `Dctrl -1` | 执行成功 |
| 10 | AltTab | `Dalt -1` | 执行成功 |

---

## 测试执行建议

1. **优先使用 `--json`**：便于验证返回状态
2. **准备测试窗口**：测试前确保相关窗口已打开
3. **检查退出码**：`$LASTEXITCODE` 或 `%ERRORLEVEL%`
4. **多轮验证**：模糊匹配需验证多种变体
