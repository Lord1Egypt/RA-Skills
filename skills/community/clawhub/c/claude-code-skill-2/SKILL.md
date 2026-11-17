---
name: Claude Code (小c)
slug: claude-code
version: 1.0.0
description: "调度 Claude Code（小c）执行重度编码任务：代码审查、完整模块生成、复杂 Debug 诊断、架构设计。笨笨统筹，小c干重活。"
metadata:
  clawdbot:
    emoji: "🔧"
    requires:
      bins:
        - claude
    os:
      - win32
    configPaths:
      - "~/claude-code/"
---

## 定位

小c 是 Claude Code CLI，笨笨的代码副手。**笨笨统筹调度，小c 干重活。**

- 小c 位置: `C:\Users\Renhai Huang\.local\bin\claude.exe`
- 笨笨通过 shell 命令调用小c，读取输出作为结果

## 何时调用小c

| 任务类型 | 谁做 | 原因 |
|---------|------|------|
| **读代码、做小改动、编译、git** | 笨笨自己 | 有直接 shell/read/write，零开销 |
| **代码审查、分析 Bug** | 小c 审查 → 笨笨修复 | 小c 快速读大文件分析，笨笨针对性改 |
| **生成完整代码/算法/模块** | 小c 写 → 笨笨整合编译 | 小c 生成能力强，笨笨负责上下文和验证 |
| **复杂 Debug（给报错+代码）** | 小c 诊断 → 笨笨实施 | 小c 分析到位，笨笨写最终代码和测试 |
| **架构/设计决策** | 小c 深度思考（pro）→ 笨笨拍板 | 深度任务值多用点 token |
| **一口气干到底的任务** | 小c 带工具权限直接干 | 比如重构整个文件，小c 改完笨笨验收 |

### 不调用小c 的情况

- 单文件简单修改（<20行）
- 纯信息查询
- 编译运行测试
- Git 操作
- 小任务调小c 是浪费（进程启动 + API 往返有开销），能自己干的就自己干

## 命令模板

### 1. 纯文本生成（最省 token）

```bash
claude -p "写一个xxx函数，要求..." --print --tools "" --model deepseek-v4-flash
```

- `--tools ""` 禁止工具调用，最省 token
- 适合：生成代码片段、算法实现、纯文本输出
- 模型：flash（便宜够用）

### 2. 代码审查

```bash
claude -p "审查这个文件，找出 bug、安全问题、性能问题" --print --model deepseek-v4-flash --permission-mode bypassPermissions
```

- 适合：代码审查、bug 分析、安全审计
- 模型：flash（审查不需要深度思考）

### 3. 操作项目文件

```bash
claude -p "在项目中修改xxx，要求..." --print --add-dir "D:\Qt program\MST-Visualizer" --permission-mode bypassPermissions
```

- `--add-dir` 给小c 项目上下文
- `--permission-mode bypassPermissions` 允许小c 直接读写
- 适合：重构、跨文件修改、项目级任务

### 4. 复杂任务（深度思考）

```bash
claude -p "设计xxx的架构方案，考虑..." --print --model deepseek-v4-pro
```

- 模型：pro（值得为架构决策多花 token）
- 适合：架构设计、复杂问题分析、技术方案对比

### 5. 带工作目录（当前项目）

```bash
claude -p "修改xxx" --print --add-dir "$(pwd)" --permission-mode bypassPermissions --model deepseek-v4-flash
```

- 适合：在当前工作目录的项目中做修改

## 调用流程

1. **判断任务复杂度** — 值得调小c 吗？（参考上表）
2. **选择合适的模板** — 根据任务类型选命令模板
3. **构造 prompt** — 清晰描述任务，给小c 足够上下文
4. **执行** — `bash("claude -p ...")` 
5. **解析结果** — 读小c 的输出
6. **行动** — 笨笨根据小c 的建议/代码进行后续操作

## Prompt 编写指南

给小c 的 prompt 要清晰具体：

```
好的 prompt：
"审查 D:\Qt program\MST-Visualizer\src\prim.cpp，重点关注：
1. 算法正确性（Prim 算法是否实现正确）
2. 内存管理（是否有泄漏风险）
3. 边界条件（空图、单节点图处理）
4. 性能瓶颈"

不好的 prompt：
"帮我看下代码"
```

## 与其他 Skill 的配合

- **coding-agent skill** — 已有。claude-code skill 是它的补充：coding-agent 适合轻量编码协助，claude-code 适合需要独立进程的重度任务
- **self-improving skill** — 小c 审查结果中发现的模式，记录到 `~/self-improving/`
- **proactivity skill** — 笨笨主动判断：当前对话是否适合交给小c？主动提议

## 注意事项

- 小c 是独立进程，不共享笨笨的上下文。prompt 要自包含
- 小c 的输出可能很长，注意截断关键部分
- `--tools ""` 模式下小c 不能读文件，只能基于 prompt 中的内容工作
- 带 `--add-dir` 时小c 可以用 Read/Edit/Bash 直接操作文件
- 调用前先判断：这活值得让它跑一次吗？
- 同一轮对话避免重复调小c 超过 3 次

## 相关文件

- 小c 的记忆: `C:\Users\Renhai Huang\.claude\projects\D--my-claudecode-workspace\memory\`
- 笨笨与小c 的分工: `MEMORY.md` → "我与 Claude Code 的分工" 章节
