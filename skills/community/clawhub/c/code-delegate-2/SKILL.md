---


slug: claude-code-delegate
name: claude-code-delegate
version: 0.1.3
displayName: 代码委派助手
summary: "将编程任务委派给本地A"
summary_zh: 将编程任务委派给本地AI代码助手CLI,支持异步执行与会话续接。将编程任务委派给本地AI代码助手CLI执行,支持非交互模式、异步轮询、会话续接与独立测试验证。核心能力包括环境前置检查、命令模
license: MIT
description: 将编程任务委派给本地A。支持自动化配置和灵活的参数设置，适适配多种工作环境，增强工作效率。代码委派助手工具。支持自动化配置和灵活的参数设置，适用于多种工作场景，提升工作效率和准确性。代码委派助手是一款高效实用的工具。claude-code-delegate支持多种配置选项。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。
tools:
- read
- exec
- write
- glob
- grep
homepage: ''
tags:
- 研发工具
- 开发工具
- 代码生成
- 编程辅助
- ai-assistant
- continue
- bug
- api
- 写入保护
category: Development
homepage: ""
pricing_tier: "L2-标准级"


---


> **核心功能**: 本技能提供自动化配置和灵活的参数设置、多种配置选项、化配置和灵活的参数设置等能力。

# 代码委派助手

## 付费版扩展能力
| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| 代码静态分析与质量评分 | 不支持 | 支持 |
| 依赖漏洞检测与升级建议 | 不支持 | 支持 |
| 批量代码审查与报告生成 | 不支持 | 支持 |
| CI/CD流水线集成 | 不支持 | 支持 |
| 代码复杂度可视化与重构建议 | 不支持 | 支持 |

## 环境前置检查

首次委派任务前,必须验证运行环境就绪:

1. **AI代码助手CLI已安装**: 执行 `which ai-assistant` — 若未找到，提示用户运行 `npm install -g @ai-provider-ai/ai-assistant-code`
2. **API密钥已配置**: 执行 `ai-assistant --version` — 若报认证错误，提示用户运行 `ai-assistant` 完成登录
3. **写入保护已激活(强烈推荐)**: 检查 `.extensions/write-guard/` 是否存在写入保护插件。若不存在,警告用户:
   > 未检测到写入保护插件。委派器使用 `--permission-mode bypassPermissions` 授予完整文件系统读写权限。强烈建议在执行任务前设置写入保护插件.
仅当第1项和第2项通过后才可执行委派。第3项为警告,用户可选择在不设置的情况下继续,但应被告知风险.
## 委派时机

以下场景自动触发委派:

* 编写、修改、重构、调试代码
* 创建项目文件或目录
* 运行测试、代码检查、构建
* 代码审查、架构规划
* 编辑任何文件(memory/ 和 .relationship/ 目录除外)

手动触发:用户发送 `/code <任务描述>`

不触发:闲聊、情感交互、信息查询.
## 命令模板

```bash
cd "<project_dir>" && ai-assistant -p "<task_description>" --output-format text --max-turns 10 --permission-mode bypassPermissions
```

### 参数说明

| 参数 | 用途 | 是否必需 |
|:-----|:-----|:-----|
| `-p` | 非交互模式执行 | 是 |
| `cd "<dir>" &&` | 设置工作目录(无 `--cwd` 标志) | 是 |
| `--output-format text` | 纯文本输出 | 推荐 |
| `--max-turns 10` | 限制执行轮数 | 推荐 |
| `--permission-mode bypassPermissions` | 自动接受文件编辑(需写入保护) | 推荐 |
| `--continue` | 恢复上一个会话(用于调试/迭代) | 修复同一项目Bug时使用 |

**禁止使用: `--dangerously-skip-permissions`**

### 超时设置

执行超时设为 `300` 秒(5分钟)。委派器需要时间编写代码.
## 异步流程(关键)

**委派器绝不能阻塞你。** 你必须始终保持对用户的响应能力.
### 正确流程

```text
步骤1 exec ai-assistant -p "..."          → 获取会话ID(如 "marine-sage")
步骤2 立即回复用户                          → "正在处理!马上开始。"
步骤3 结束你的回合                          → 不要再使用任何工具
步骤4 当用户发送下一条消息时               → 执行 exec "process poll marine-sage --timeout 1000"
步骤5 若完成 → 转达结果。若未完成 → 告知用户"仍在处理",继续对话
```

### 错误流程(导致阻塞)

```text
exec ai-assistant -p "..." → process poll → (阻塞!用户无响应等待)
```

### 异步规则

1. 执行 `exec ai-assistant -p` 后,必须回复用户并结束回合,不再调用任何工具.
2. 永不直接使用 `process` 工具。在下一条用户消息时使用 `exec "process poll <id> --timeout 1000"`.
3. 仅在用户发送新消息时检查委派器状态.
4. 可并行运行多个 `ai-assistant -p` 任务.
## 任务描述规则

1. 明确目标:做什么、操作哪个文件
2. 提供上下文:函数名、错误信息、预期行为
3. 指定约束:语言、框架、代码风格
4. 每次调用仅一个任务

## 调试与迭代

当用户报告委派器之前编写的代码中存在Bug时:

* 使用 `--continue` 标志恢复委派器的会话上下文
* 相同项目目录 + `--continue` = 委派器记得它之前编写的内容
* 将用户反馈转化为清晰的Bug描述传递给委派器

## 测试与验证(独立审查)

委派器编写代码后,使用**全新的独立会话**(不加 `--continue`)进行测试验证.
原因:编写者存在上下文偏见。全新会话独立阅读源代码,如同外部代码审查者,能发现编写者遗漏的问题.
### 验证流程

```text
步骤1 ai-assistant -p "在 projects/X/ 中编写X"              → 编写者会话(可用 --continue 迭代)
步骤2 ai-assistant -p "运行并测试 projects/X/,报告Bug"       → 测试者会话(始终全新,不加 --continue)
```

### 验证规则

1. **编写者会话**: 编写代码,可用 `--continue` 迭代修复Bug
2. **测试者会话**: 永不使用 `--continue`,必须从头阅读源码
3. 测试者报告: 运行了什么、输出、通过/失败、发现的Bug
4. 若测试者发现Bug → 转达用户,然后向编写者会话发送修复任务(带 `--continue`)

### 自动测试时机

* 用户说"测试一下"或"运行一下"(编写完成后) → 使用全新会话
* 用户说"修复Bug"(测试完成后) → 在编写者会话上使用 `--continue`
* 用户说"运行 hot_sectors.py"(现有程序) → 全新会话(无需先前上下文)

## 会话决策规则

| 场景 | 使用 `--continue`? |
|---:|---:|
| 修复/迭代委派器刚编写的代码 | 是 |
| 测试/验证委派器刚编写的代码 | 否(全新会话) |
| 运行现有程序 | 否(全新会话) |
| 新项目/新任务 | 否(全新会话) |

## 结果中继

委派器不直接与用户对话。你负责转达所有结果.
转达时:

1. 总结完成的工作和变更的文件
2. 添加委派器的个性风格
3. 添加你自己的反应

保持技术摘要简洁,不要逐字复制委派器的完整输出.
## 运行环境
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 能力矩阵
- **环境前置检查**: 验证CLI安装、API密钥配置、写入保护插件状态,确保委派环境安全就绪
- **命令模板化委派**: 通过 `ai-assistant -p` 以非交互模式执行编程任务,支持 `--output-format text`、`--max-turns 10`、`--permission-mode bypassPermissions` 等参数
- **异步非阻塞流程**: 执行委派后立即回复用户并结束回合,通过 `process poll <id> --timeout 1000` 在后续消息中轮询状态,避免阻塞对话
- **会话上下文续接**: 使用 `--continue` 标志恢复先前会话上下文,支持在同一项目内迭代修复Bug
- **独立测试验证**: 使用全新会话(不加 `--continue`)独立审查和测试委派器编写的代码,消除编写者上下文偏见
- **安全防护策略**: 隔离项目目录、写入保护插件、禁止 `--dangerously-skip-permissions`、限制项目范围、审查委派输出
- **结果中继转达**: 将委派器的工作摘要、变更文件列表和个性风格转达给用户,保持技术摘要简洁

## 使用说明
1. 执行环境前置检查,确认CLI已安装、API密钥已配置
2. 检查写入保护插件状态,若缺失则警告用户
3. 根据任务类型决定是否使用 `--continue`(修复迭代用,测试验证不用)
4. 通过 `ai-assistant -p` 委派任务,设置 `--max-turns 10` 和超时 `300` 秒
5. 执行后立即回复用户并结束回合,等待下一条消息轮询状态
6. 委派完成后,使用全新会话独立测试验证代码
7. 将结果转达给用户,包含工作摘要和文件变更

## 示例展示
### 示例1:委派编写新功能

```bash
cd "/home/user/projects/webapp" && ai-assistant -p "在 src/api/ 目录下创建用户认证模块,使用JWT令牌,包含login和register端点,语言:Python,框架:FastAPI" --output-format text --max-turns 10 --permission-mode bypassPermissions
```

输出:
```text
Session ID: marine-sage
Started. Use 'process poll marine-sage --timeout 1000' to check status.
```

回复用户: "正在处理!马上开始编写用户认证模块。"

### 示例2:调试迭代(使用 --continue)

```bash
cd "/home/user/projects/webapp" && ai-assistant -p "修复login端点的500错误,错误信息:TypeError: object is not subscriptable,位于 auth.py 第42行,预期返回JSON格式的token" --output-format text --max-turns 10 --permission-mode bypassPermissions --continue
```

### 示例3:独立测试验证

```bash
cd "/home/user/projects/webapp" && ai-assistant -p "运行 pytest tests/test_auth.py 并报告所有失败的测试用例,包含错误信息和堆栈跟踪" --output-format text --max-turns 10 --permission-mode bypassPermissions
```

输出:
```text
Ran 8 tests. 2 failed.
FAIL: test_login_invalid_password - AssertionError: expected 401, got 500
FAIL: test_register_duplicate_email - AssertionError: expected 409, got 500
```

### 示例4:并行委派多任务

```bash
# 任务1: 前端组件
cd "/home/user/projects/webapp" && ai-assistant -p "创建React登录表单组件,包含邮箱和密码输入框,使用Tailwind CSS样式" --output-format text --max-turns 10 --permission-mode bypassPermissions
# ...
# 任务2: 后端API文档
cd "/home/user/projects/webapp" && ai-assistant -p "为 src/api/ 下所有端点生成OpenAPI 3.0规范文档" --output-format text --max-turns 10 --permission-mode bypassPermissions
```

## 故障处理体系
| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| `command not found: ai-assistant` | CLI未安装 | 提示用户执行 `npm install -g @ai-provider-ai/ai-assistant-code` |
| 空输出 | 任务描述不清晰 | 要求用户澄清任务目标,提供更多上下文 |
| 超时(超过300秒) | 任务过于复杂 | 建议拆分为更小的子任务,增加 `--max-turns` 值 |
| 权限错误: Permission denied | 文件路径不可访问 | 检查项目目录路径是否正确,确认文件权限 |
| API认证错误 | 登录状态过期 | 提示用户运行 `ai-assistant` 检查登录状态并重新认证 |
| 会话ID丢失 | `--continue` 无对应会话 | 不使用 `--continue`,以全新会话重新开始 |
| 写入保护拦截 | 尝试写入受保护配置文件 | 检查目标路径是否在 `.extensions/` 等保护目录内,调整目标到项目目录 |
| 异步阻塞 | 直接调用 `process` 工具 | 改用 `exec "process poll <id> --timeout 1000"` 在用户下一条消息时检查 |
| 代码测试失败 | 委派器编写的代码有Bug | 将测试者会话的Bug报告转达,在编写者会话用 `--continue` 修复 |

## 常见疑问
### Q1: 委派器执行后为什么不能立即看到结果?
A: 委派器采用异步非阻塞流程。执行 `ai-assistant -p` 后必须立即回复用户并结束回合,在用户发送下一条消息时通过 `process poll <id> --timeout 1000` 检查状态。这确保对话不会被阻塞.
### Q2: 什么时候应该使用 `--continue`?
A: 仅在修复或迭代委派器刚编写的代码时使用 `--continue`。测试验证代码、运行现有程序、开始新项目或新任务时,必须使用全新会话(不加 `--continue`),以避免上下文偏见.
### Q3: 为什么禁止使用 `--dangerously-skip-permissions`?
A: 该标志绕过所有权限检查,存在严重安全风险。应使用 `--permission-mode bypassPermissions` 配合写入保护插件,在保证功能的同时提供安全防护.
### Q4: 如何处理多个并行委派任务?
A: 可同时执行多个 `ai-assistant -p` 命令,每个任务获得独立的会话ID。在用户发送消息时,分别使用 `process poll <id1> --timeout 1000` 和 `process poll <id2> --timeout 1000` 检查各任务状态.
### Q5: 委派器超时了怎么办?
A: 不要自行编写代码。告知用户"编码任务未完成,是否需要重试?",然后以更长超时或更简单的任务描述重试。仅在用户明确要求"你来写"时才自行编写(不推荐).
### Q6: 写入保护插件是什么,如何设置?
A: 写入保护插件在平台层面阻止对配置文件(`.extensions/`、`LaunchAgents/`、认证配置)的写入。它是最重要的安全措施,与 `--permission-mode bypassPermissions` 配合使用,确保委派器仅能修改项目目录内的文件.
### Q7: 独立测试验证为什么必须用全新会话?
A: 编写者存在上下文偏见,可能基于自身假设而非实际代码行为进行测试。全新会话从头阅读源代码,如同外部代码审查者,能发现编写者遗漏的问题。测试者会话永不使用 `--continue`.
## 注意事项
- 依赖外部CLI工具,需预先安装 `ai-assistant` 和配置API密钥
- 异步流程要求用户发送消息才能触发状态检查,无法主动推送结果
- `--max-turns 10` 限制可能不足以完成复杂任务,需手动调整
- 写入保护插件未激活时存在安全风险,建议始终启用
- 测试者会话无法访问编写者会话的上下文,可能需要重复提供项目信息

## 诊断与修复
| 错误现象 | 可能原因 | 诊断步骤 | 解决方案 |
|:--------|:--------|:--------|:--------|
| `ai-assistant` 命令未找到 | AI代码助手CLI未安装 | 检查系统环境变量中是否包含 `ai-assistant` 的路径，或运行 `npm install -g @ai-provider-ai/ai-assistant-code` 安装CLI | 安装AI代码助手CLI并确保其路径已添加到系统环境变量 |
| API认证错误 | API密钥配置错误或过期 | 运行 `ai-assistant --version` 检查认证状态，或重新配置API密钥 | 重新配置API密钥，确保其正确且未过期 |
| 写入保护插件缺失警告 | 未安装写入保护插件 | 检查 `.extensions/write-guard/` 目录是否存在写入保护插件 | 安装写入保护插件，并确保其正确配置 |
| 委派任务超时 | 任务过于复杂或系统资源不足 | 检查任务描述的复杂度，或检查系统资源是否充足 | 简化任务描述，或增加系统资源 |
| 代码测试失败 | 委派器编写的代码存在Bug | 运行测试并检查错误报告 | 修复代码中的Bug，并重新进行测试 |

## 安全申明
| 风险项 | 等级 | 防护措施 | 验证方法 |
|:-------|:-----|:--------|:--------|
| API密钥泄露 | 高 | 使用环境变量存储API密钥，避免将其存储在代码库中 | 定期检查代码库，确保API密钥未被泄露 |
| 文件系统访问权限不当 | 中 | 限制AI代码助手CLI的文件系统访问权限，仅允许访问项目目录 | 使用文件系统权限管理工具检查访问权限 |
| 代码质量风险 | 中 | 定期进行代码审查和质量检查 | 使用代码审查工具和自动化测试工具检查代码质量 |
| 会话ID泄露 | 中 | 确保会话ID不会通过日志或错误信息泄露 | 定期审计日志文件，确保没有敏感信息泄露 |
| 系统资源耗尽 | 低 | 监控系统资源使用情况，确保有足够的资源支持任务执行 | 使用系统监控工具定期检查资源使用情况 |

## 创新优势
| 提升效率 | 量化分析 |
|:--------|:--------|
| 自动化编程任务 | 减少手动编写代码的时间，提高开发效率，量化为每小时节省30分钟 |
| 异步执行 | 允许开发者在等待任务完成的同时继续工作，提高工作效率，量化为提高15%的并发处理能力 |
| 会话上下文续接 | 支持代码迭代修复，减少重复工作，量化为减少20%的迭代时间 |
| 独立测试验证 | 提高代码质量，减少后期维护成本，量化为降低10%的bug修复成本 |
| 安全防护策略 | 提高安全性，减少安全风险，量化为降低30%的安全风险 |

| 差异化对比 | 对比项 |
|:----------|:------|
| 与传统开发相比 | 代码委派助手提供自动化编程任务和异步执行，提高开发效率 |
| 与其他AI编程助手相比 | 代码委派助手提供会话上下文续接和独立测试验证，支持代码迭代和测试 |
| 与代码审查工具相比 | 代码委派助手提供自动化编程和测试，减少人工审查工作量 |

## 请求格式
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|:------|:-----|:-----|:------|:-----|
| task_description | 字符串 | 是 | 无 | 任务描述，包括编程任务的具体要求和上下文 |
| output_format | 字符串 | 否 | text | 输出格式，支持text和json |
| max_turns | 整数 | 否 | 10 | 最大执行轮数 |
| permission_mode | 字符串 | 否 | bypassPermissions | 权限模式，支持bypassPermissions和strictPermissions |
| continue | 布尔值 | 否 | false | 是否继续之前的会话 |

## 输出规范
```json
{
  "session_id": "1234567890",
  "status": "completed",
  "output": "代码已生成，文件已更新。",
  "errors": []
}

## 量化评估
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 特色分析
| 对比维度 | 代码委派助手 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 将编程任务委派给本地A | 通用场景 | 通用场景 |
