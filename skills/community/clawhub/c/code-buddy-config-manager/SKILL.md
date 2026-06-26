---
name: code-buddy-config-manager
description: Auto-detect, install, update and verify all CodeBuddy configurations (MCP, Skill, Plugin, Model, CLI)
description_zh: code buddy配置管理 - 自动检测、安装、更新和验证 CodeBuddy 的各类配置（MCP Server、Skill、Plugin、Model、CLI 工具等）
version: 1.0.0
author: 小肚小肚
allowed-tools: "Bash(*) Python3(*) Perl(*) CodeBuddy(*) UserInput()"
---

# CodeBuddy 配置管理器

## 触发条件

当用户输入包含以下意图时触发本 Skill：

- 配置/安装/更新/检测某个 CodeBuddy 组件
- 需要安装或管理 MCP/Skill/Plugin/Model/CLI 工具
- 需要验证 CodeBuddy 配置状态

## 输入解析

### 输入参数

用户需提供以下信息（通过自然语言解析）：

| 参数 | 类型 | 必填 | 说明 | 默认行为 |
|------|------|------|------|----------|
| `config_type` | string | 是 | 配置类型：`model` / `mcp` / `skill` / `cli` / `plugin` / `other` | - |
| `config_name` | string | 是 | 要配置的内容名称 | - |
| `config_url` | string | 否 | 配置获取网址 | 若未提供，自动搜索互联网获取最新配置信息 |
| `config_scope` | string | 否 | `global` (全局) 或 `project` (项目) | 默认为 `project` |

### 输入解析示例

```
用户: "帮我安装一个名为 python-tools 的 MCP Server，从 https://example.com/mcp.json 获取配置，全局安装"
→ 解析结果: { type: "mcp", name: "python-tools", url: "https://example.com/mcp.json", scope: "global" }

用户: "检测一下有没有安装 browser-use 这个 Skill"
→ 解析结果: { type: "skill", name: "browser-use", url: null, scope: "project" }

用户: "安装 playwright 这个 CLI 工具"
→ 解析结果: { type: "cli", name: "playwright", url: null, scope: "project" }
```

---

## 工作流

### 阶段 1: 状态检测

**调用**: `bash scripts/check_status.sh {config_type} {config_name} {config_scope}`

> **集成提示**: 如需跨目录搜索（如搜索全局和项目的多个技能目录），可使用 **[subagent:code-explorer]** 辅助检测。

**检测目标**:

| 配置类型 | 检测路径 | 状态判定 |
|----------|----------|----------|
| MCP | `~/.codebuddy/mcp.json` 或 `{project}/.codebuddy/mcp.json` | `mcpServers.{name}` 配置块存在 |
| Skill | `~/.codebuddy/skills-marketplace/skills/{name}/` 或 `{project}/.codebuddy/skills/{name}/` | 目录存在且包含 SKILL.md |
| Plugin | `~/.codebuddy/settings.json` → `enabledPlugins` | 键存在且值为 `true` |
| Model | IDE 设置 / 环境变量 | 存在 API Key 或端点配置 |
| CLI | `command -v {name}` | PATH 中存在可执行文件 |

**输出格式**:

```json
{
  "exists": true/false,
  "status": "enabled" | "disabled" | "error" | "not_found",
  "version": "当前版本号或 null",
  "needs_update": true/false,
  "details": "详细状态描述"
}
```

**判定逻辑**:
- `exists=true` 且 `status=normal` → 返回"已存在无需操作"，终止流程
- `exists=true` 且 `needs_update=true` → 进入阶段 2（更新模式）
- `exists=false` → 进入阶段 2（安装模式）

---

### 阶段 2: 安装/更新

#### 2a: 获取配置信息

当 `config_type` 为 `skill` / `other` 或需要从外部获取配置信息时，按以下优先级获取：

##### 优先级 1: 直接使用 config_url

若用户已提供 `config_url`：

- 使用 `curl -sL` 或 `wget -qO-` 下载
- 对于 MCP 类型，尝试解析为 JSON 并写入 mcp.json
- 对于 Skill 类型，尝试下载为 zip 包或 SKILL.md

##### 优先级 2: 使用 [skill:agent-browser] 自动搜索

当未提供 `config_url` 时，调用 `[skill:agent-browser]` 进行互联网搜索：

```markdown
1. 调用 [skill:agent-browser] 搜索关键词:
   - "CodeBuddy {config_name} {config_type} 安装"
   - "{config_name} 文档 配置"
   
2. 目标页面类型:
   - 官方 GitHub 仓库: 查找 README、配置文件示例
   - npm 包页: 查找安装命令、依赖
   - 官方文档: 查找配置指南
   
3. 需要提取的信息:
   - 安装命令和方式
   - 配置文件模板（JSON/YAML）
   - 依赖要求（Python 包、npm 包等）
   - 版本信息和更新日志
   
4. 输出整理为结构化数据:
   - install_command: string
   - config_template: JSON object or null
   - dependencies: string[]
   - version: string
```

##### 优先级 3: 使用 [skill:playwright-cli] 精细化提取

当 `[skill:agent-browser]` 搜索结果不精确或需要与页面交互（如下载需要展开的文档页面）时：

```markdown
1. 调用 [skill:playwright-cli] 打开目标页面
2. 交互操作（如点击展开按钮、滚动加载等）
3. 提取精确的配置信息
4. 与 agent-browser 结果合并
```

##### 优先级 4: 综合推理

当上述搜索均无法获取足够信息时：

```markdown
1. 基于 {config_name} 和 {config_type} 做合理推断
2. 使用 [subagent:code-explorer] 在全局已安装配置中查找相似案例
3. 参考 references/config-structures.md 中的格式模板
4. 提供最佳猜测配置并标注"需人工确认"
```

---

#### 2b: 按类型执行安装/更新

##### MCP Server → 脚本 + agent-browser

执行 `bash scripts/install_mcp.sh {name} {scope} {command} [args...]`

**agent-browser 集成**:
当需要查找 MCP Server 的启动命令时：
1. `[skill:agent-browser]` 搜索 `"{name} mcp server github install"`
2. 从搜索结果提取 `command` 和 `args`
3. 调用 install_mcp.sh 安装

**示例**:
```
搜索 "python-tools mcp server" → 发现 python-tools 需要 "python -m mcp_server"
→ install_mcp.sh python-tools global python -m mcp_server
```

---

##### Skill → 脚本 + find-skills + skill-creator

**第一步: 搜索 Marketplace ← [skill:find-skills]**

调用方式：
```markdown
1. 调用 [skill:find-skills] 搜索 {config_name}
2. 从搜索结果获取:
   - 精确匹配的 Skill 名称
   - 模糊匹配的推荐列表（名称、描述、版本）
   - 安装方式（一键安装或手动）

3. 处理搜索结果:
   - 找到精确匹配 → 确认是否已存在，不存在则安装
   - 找到模糊匹配 → 按相似度排序，选择最佳匹配
   - 未找到 → 进入第二步（自定义创建）
```

搜索后处理示例：
```
搜索 "browser-use" → 找到精确匹配 Skill "browser-use"
→ 执行 install_skill.sh browser-use project

搜索 "custom-slack" → 未在 marketplace 找到
→ 进入第二步：使用 skill-creator 创建
```

**第二步: 自定义创建 ← [skill:skill-creator]**

当 marketplace 中未找到时：

```markdown
1. 调用 [skill:skill-creator] 创建自定义 Skill:
   - 输入: {config_name} 名称、描述
   - 输出: 完整的 Skill 目录结构

2. skill-creator 会生成:
   - SKILL.md 文件（含 YAML frontmatter、工作流模板）
   - scripts/ 目录（如需要）
   - references/ 目录（如需要）

3. 创建完成后:
   - 检查 SKILL.md 的 YAML frontmatter 是否完整
   - 确认版本号是否正确
   - 调用 check_status.sh 验证
```

---

##### Plugin → 脚本 + agent-browser

执行 `bash scripts/install_plugin.sh {name}`

**agent-browser 集成**:
当需要查找插件对应的 marketplace 源时：

```markdown
1. [skill:agent-browser] 搜索 "CodeBuddy {name} plugin"
2. 确定 marketplace 标识（如 codebuddy-plugins-official）
3. 执行 install_plugin.sh {name} --marketplace {marketplace}
```

---

##### Model → 引导 + agent-browser

```markdown
1. [skill:agent-browser] 搜索 "{name} API 配置 教程"
2. 提取 API Key 获取方式、Endpoint URL
3. 引导用户在 IDE 设置中配置
4. 提示用户设置环境变量（如需要）
```

---

##### CLI 工具 → 脚本

执行 `bash scripts/install_cli.sh {name}`

脚本自动检测 brew/npm/pip3/cargo/go 中可用的包管理器。

---

##### 其他类型 (other) → agent-browser 优先

```markdown
1. 调用 [skill:agent-browser] 搜索 "{name} 安装 {config_type}"
2. 根据搜索结果确定具体安装方式
3. 若搜索结果不足，使用 [skill:playwright-cli] 精细化搜索
4. 按获取到的信息执行自定义安装流程
```

---

### 阶段 3: 验证配置

**调用**: `bash scripts/verify_config.sh {config_type} {config_name} {config_scope} {operation}`

**流程**:
1. 再次调用阶段 1 的检测逻辑
2. 比对预期状态与实际结果
3. 输出结构化的验证报告

**输出格式**:
```json
{
  "overall_status": "success" | "partial" | "failed",
  "config_type": "mcp",
  "config_name": "python-tools",
  "scope": "global",
  "operation": "install" | "update",
  "target_path": "/Users/dxc/.codebuddy/mcp.json",
  "previous_status": {"exists": false, "status": "not_found"},
  "final_status": {"exists": true, "status": "normal", "version": "1.0.0"},
  "steps": [
    {"step": "状态检测", "status": "passed", "detail": "检测到未安装"},
    {"step": "配置获取", "status": "passed", "detail": "从 URL 获取配置成功"},
    {"step": "依赖安装", "status": "passed", "detail": ""},
    {"step": "配置写入", "status": "passed", "detail": "已写入 mcp.json"},
    {"step": "验证确认", "status": "passed", "detail": "配置正常，版本 1.0.0"}
  ],
  "recommendations": ["重启 IDE 以应用配置更改"]
}
```

---

## 外部技能集成指南

本部分详细说明如何在各个工作流阶段调用和利用外部技能。

### 1. [skill:agent-browser] 集成

**调用时机**:
- 阶段 2a 获取配置信息时（未提供 `config_url`）
- 查找 MCP Server 的启动命令和参数
- 查找 Plugin 对应的 marketplace
- 查找 Model 的 API 配置信息
- 任意 `other` 类型的配置信息搜索

**调用方式**:
```markdown
[skill:agent-browser] 搜索关键词
        
关键词模板:
- "{config_name} codebuddy {config_type}"
- "{config_name} install config tutorial"
- "{config_name} github {project_type}"
```

**预期输出解析**:
```markdown
agent-browser 返回的页面内容需提取:
1. 安装命令（从 README 或文档中提取）
2. 配置文件示例（JSON/YAML 块）
3. 依赖列表（如需要 pip install xxx）
4. 版本号（从 release 页面或 package.json 提取）

提取后的信息格式化为:
- command: string        # 可执行命令
- args: string[]         # 命令参数
- env: {key: value}      # 环境变量
- dependencies: string[] # 需要额外安装的包
- version: string        # 最新版本号
```

**错误处理**:
```markdown
- 若 agent-browser 搜索失败（页面加载超时等）:
  1. 尝试 [skill:playwright-cli] 替代搜索
  2. 若仍失败，提示用户手动提供 config_url
  3. 使用 references/config-structures.md 中的模板生成默认配置

- 若搜索结果不包含所需信息:
  1. 尝试多个关键词组合搜索
  2. 搜索官方文档站而非 GitHub
  3. 提示用户部分信息缺失，建议补全
```

---

### 2. [skill:playwright-cli] 集成

**调用时机**:
- agent-browser 无法满足需求时（需要交互操作）
- 需要从动态加载的文档页面提取内容
- 需要下载文件或填写表单

**调用方式**:
```markdown
[skill:playwright-cli] navigate {url}
→ 等待页面加载 → 提取内容

如需要交互:
[skill:playwright-cli] click {selector}
[skill:playwright-cli] fill {selector} {value}
[skill:playwright-cli] screenshot {path}
```

---

### 3. [skill:find-skills] 集成

**调用时机**:
- 阶段 2b 处理 `config_type=skill` 时
- 需要在 marketplace 中搜索匹配的 Skill

**调用方式**:
```markdown
[skill:find-skills] {config_name}
```

**输出处理**:
```markdown
find-skills 返回结果格式（预期）:
- 精确匹配: { name: "xxx", version: "x.x.x", description: "..." }
- 模糊匹配: [ { name: "xxx", score: 0.95 }, ... ]
- 无匹配: null

处理逻辑:
1. 精确匹配 → 直接安装
2. 模糊匹配且最高分 > 0.7 → 确认后安装
3. 否则 → 使用 skill-creator 创建
```

---

### 4. [skill:skill-creator] 集成

**调用时机**:
- `[skill:find-skills]` 未找到匹配时
- 用户主动要求创建自定义 Skill

**调用方式**:
```markdown
[skill:skill-creator] {config_name}
```

**生成后的工作**:
```markdown
1. 确认 skill-creator 生成的目录结构完整
2. 检查 SKILL.md 包含:
   - ✅ YAML frontmatter (name, description, version)
   - ✅ 清晰的触发条件
   - ✅ 完整的工作流定义  
   - ✅ 错误处理说明
3. 执行 check_status.sh 验证:
   - 目录存在
   - SKILL.md 非空
   - 版本号正确
4. 报告创建结果给用户
```

---

### 5. [subagent:code-explorer] 集成

**调用时机**:
- 阶段 1 状态检测时（跨目录搜索）
- 需要枚举全局/项目的技能、插件列表时
- 验证阶段需要检查配置目录结构时

**调用方式**:
```markdown
[subagent:code-explorer] 探索以下目录:
- ~/.codebuddy/skills-marketplace/skills/
- {project}/.codebuddy/skills/
- ~/.codebuddy/plugins/marketplaces/
- ~/.codebuddy/mcp.json
```

---

## 完整调用流程示例

### 示例 A: 安装 MCP Server（含 agent-browser 搜索）

```
用户输入: "安装 python-tools 这个 MCP Server"

1. check_status.sh mcp python-tools project
   → {"exists": false, "status": "not_found"}

2. [skill:agent-browser] 搜索 "python-tools mcp server github"
   → 找到 GitHub 仓库, 提取安装信息:
     command: "python"
     args: ["-m", "python_mcp_tools"]

3. install_mcp.sh python-tools project python -m python_mcp_tools
   → {"success": true, "message": "安装成功"}

4. check_status.sh mcp python-tools project
   → {"exists": true, "status": "enabled"}

5. verify_config.sh mcp python-tools project install
   → {"overall_status": "success", ...}
```

### 示例 B: 安装 Skill（含 find-skills + skill-creator 集成）

```
用户输入: "安装一个数据分析 Skill"

1. check_status.sh skill data-analyst project
   → {"exists": false, "status": "not_found"}

2. [skill:find-skills] data-analyst
   → 未找到精确匹配
   → 模糊匹配: "data-analysis-toolkit" (0.82), "data-viz-assistant" (0.65)

3. 用户选择: 创建自定义 Skill

4. [skill:skill-creator] data-analyst
   → 生成 .codebuddy/skills/data-analyst/SKILL.md

5. check_status.sh skill data-analyst project
   → {"exists": true, "status": "enabled", "version": "1.0.0"}
```

### 示例 C: 搜索并安装未知配置（other + agent-browser + playwright-cli）

```
用户输入: "配置一个 k8s-tools 组件，不知道它属于什么类型"

1. config_type = "other", 执行全面检测
   check_status.sh other k8s-tools project
   → {"exists": false, "status": "not_found"}

2. [skill:agent-browser] 搜索 "k8s-tools codebuddy"
   → 搜索不到相关信息

3. [skill:playwright-cli] 搜索更精确的页面
   → 发现 k8s-tools 是一个 CLI 工具

4. config_type 更新为 "cli"
   install_cli.sh k8s-tools
   → 通过 brew 安装成功

5. verify_config.sh cli k8s-tools project install
   → {"overall_status": "success", ...}
```

---

## 依赖扩展清单

### 必须集成的外部技能

| 技能 | 调用阶段 | 用途 | 失败回退 |
|------|----------|------|----------|
| `[skill:agent-browser]` | 2a | 自动搜索互联网配置信息 | 尝试 `[skill:playwright-cli]` |
| `[skill:playwright-cli]` | 2a | 精细化页面交互和内容提取 | 提示用户提供 URL |
| `[skill:find-skills]` | 2b (skill) | 在 marketplace 搜索 Skill | 使用 `[skill:skill-creator]` |
| `[skill:skill-creator]` | 2b (skill) | 自定义创建 Skill | 生成基本模板 |

### 辅助 SubAgent

| SubAgent | 调用阶段 | 用途 |
|----------|----------|------|
| `[subagent:code-explorer]` | 1, 3 | 跨目录搜索配置状态 |

---

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 配置类型不支持 | 返回提示，说明支持的配置类型列表 |
| 网络连接失败 | 提示网络异常，建议重试或使用本地配置 |
| agent-browser 搜索无结果 | 尝试 playwright-cli，若仍失败则提示用户提供 URL |
| find-skills 无匹配 | 提示用户使用 skill-creator 创建 |
| 依赖安装失败 | 列出失败原因和建议解决方案 |
| 配置文件格式错误 | 尝试修复或提示手动编辑 |
| 版本不兼容 | 提示兼容性问题，推荐兼容版本 |
| 权限不足 | 提示需要管理员权限的命令 |

## 边界情况

- **配置已存在且正常**: 直接返回"已配置，无需操作"，不执行任何变更
- **配置已存在但需要更新**: 执行更新操作，保留原有配置中的自定义部分
- **配置不存在但配置目录也不存在**: 先创建配置目录结构，再安装
- **多种配置类型同名**: 依次检查所有类型
- **URL 无法访问**: 回退到互联网搜索
- **项目级配置但项目下无 .codebuddy/**: 自动创建 .codebuddy/ 目录
- **agent-browser 返回空结果**: 尝试 playwright-cli 替代搜索
- **搜索结果模糊**: 列出多个候选，由用户选择或根据相关度排序

## 使用示例

### 示例 1: 安装 MCP Server（从指定 URL）
```
用户: "帮我安装一个名为 python-tools 的 MCP Server，从 https://example.com/mcp/config.json 获取，全局安装"
流程:
1. 检测 → MCP python-tools 不存在
2. 从 URL 获取配置信息
3. 写入 /Users/dxc/.codebuddy/mcp.json
4. 安装依赖（如果命令需要 Python 包）
5. 验证 → 配置正常
```

### 示例 2: 安装 Skill（自动搜索 + find-skills + skill-creator）
```
用户: "安装一个数据分析 Skill"
流程:
1. 检测 → Skill data-analyst 不存在
2. [skill:agent-browser] 搜索 Data Analysis Skill 相关信息  
3. [skill:find-skills] data-analyst → 搜索 marketplace
4. 若未找到 → [skill:skill-creator] data-analyst → 生成自定义 Skill
5. 验证 → 配置完成
```

### 示例 3: 检测并更新已有配置
```
用户: "检查一下 MCP python-tools 是否需要更新"
流程:
1. 检测 → MCP python-tools 存在，版本 1.0.0
2. [skill:agent-browser] 搜索最新版本 → 最新为 2.0.0
3. 执行更新
4. 验证 → 已更新到 2.0.0
```

### 示例 4: 搜索并安装未知类型的配置
```
用户: "帮我配置一个 k8s-debug 工具"
流程:
1. 尝试检测所有类型 → 均未找到
2. [skill:agent-browser] 搜索 "k8s-debug codebuddy"
3. 发现是 CLI 工具 → 更新 config_type 为 cli
4. [skill:agent-browser] 搜索安装方式 → 使用 brew install k8s-debug
5. install_cli.sh k8s-debug → 安装成功
6. 验证 → 配置完成
```
