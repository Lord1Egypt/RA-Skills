# CodeBuddy 配置结构参考文档

本文档记录了 CodeBuddy 各类配置的文件格式、存储路径和安装方式，供配置管理器（code-buddy-config-manager Skill）在执行自动化任务时参考。

---

## 1. MCP Server 配置

### 文件路径

| 作用域 | 路径 |
|--------|------|
| **全局** | `~/.codebuddy/mcp.json` |
| **项目** | `{project}/.codebuddy/mcp.json` |

### JSON 格式

```json
{
  "mcpServers": {
    "<server-name>": {
      "type": "stdio",
      "command": "<启动命令>",
      "args": ["<参数1>", "<参数2>"],
      "env": {
        "<环境变量名>": "<环境变量值>"
      },
      "description": "服务器描述（可选）",
      "version": "1.0.0（可选）"
    }
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 连接类型，通常为 `stdio`（标准输入输出） |
| `command` | string | 是 | 启动 MCP Server 的可执行命令 |
| `args` | string[] | 否 | 命令参数列表 |
| `env` | object | 否 | 环境变量键值对 |
| `description` | string | 否 | 服务器功能描述，用于 UI 展示 |
| `version` | string | 否 | 版本标识，用于版本比对 |

### 示例

```json
{
  "mcpServers": {
    "python-tools": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/tools"
      },
      "description": "Python 工具集"
    },
    "browser-automation": {
      "type": "stdio",
      "command": "npx",
      "args": ["@anthropic/mcp-server-playwright"]
    }
  }
}
```

### 安装方式

1. **从 MCP Market 一键安装**：CodeBuddy Settings → MCP 标签 → 选择 Server 点击安装
2. **手动配置**：CodeBuddy Settings → MCP 标签 → Add MCP → 编辑 JSON
3. **通过 config-manager 安装**：`install_mcp.sh <name> <scope> <command> [args...]`

### 状态检测

- 读取 `mcpServers` 对象下是否存在以 `{name}` 为键的配置块
- 若配置块存在且包含有效 `command`，则视为 `enabled`

---

## 2. Skill 配置

### 目录结构

| 作用域 | 路径 |
|--------|------|
| **全局（Marketplace）** | `~/.codebuddy/skills-marketplace/skills/{name}/` |
| **项目（自定义）** | `{project}/.codebuddy/skills/{name}/` |

### 标准目录结构

```
{name}/
├── SKILL.md              # 核心技能定义（必需）
├── scripts/              # 辅助脚本（可选）
│   ├── *.sh
│   └── *.py
└── references/           # 参考文档（可选）
    ├── *.md
    └── *.json
```

### SKILL.md 格式

```markdown
---
name: <技能名称>               # 必填，kebab-case 格式
description: <英文描述>        # 必填
description_zh: <中文描述>     # 推荐
description_en: <英文描述>     # 推荐
version: <语义版本号>          # 必填，如 2.0.2
allowed-tools: <工具权限>      # 可选，如 "Bash(browser-use:*)"
---

# 技能标题

## 前提条件 (Prerequisites)

...

## 核心工作流 (Core Workflow)

...

## 命令参考 (Commands)

...

## 配置说明 (Configuration)

...

## 常见问题排查 (Troubleshooting)

...
```

### YAML Frontmatter 字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 技能唯一标识符，使用 kebab-case（如 `config-manager`） |
| `description` | 是 | 英文描述 |
| `description_zh` | 推荐 | 中文描述 |
| `description_en` | 推荐 | 英文描述 |
| `version` | 是 | 语义化版本号，如 `1.0.0`、`2.15.4` |
| `allowed-tools` | 否 | 指定技能可使用的工具权限 |

### 安装方式

1. **从 Skill Marketplace 安装**：通过 CodeBuddy 设置或 `[skill:find-skills]` 搜索安装
2. **创建自定义 Skill**：手动创建目录和 SKILL.md，或使用 `[skill:skill-creator]`
3. **通过 config-manager 安装**：`install_skill.sh <name> <scope> --create`

### 状态检测

- 检查 `{name}/SKILL.md` 是否存在且非空
- 从 YAML frontmatter 读取 `version` 字段

---

## 3. Plugin 配置

### 文件路径

| 作用域 | 路径 |
|--------|------|
| **全局** | `~/.codebuddy/settings.json` |

### JSON 格式

```json
{
  "enabledPlugins": {
    "<plugin-name>@<marketplace>": true
  }
}
```

### 插件键名约定

插件键名格式为 `{name}@{marketplace}`，其中：

| 部分 | 说明 | 示例 |
|------|------|------|
| `name` | 插件名称 | `pptx`, `pdf`, `find-skills` |
| `marketplace` | 插件市场标识 | `codebuddy-plugins-official`, `cb_teams_marketplace` |

### 当前已启用的插件（此系统）

```json
{
  "enabledPlugins": {
    "pptx@codebuddy-plugins-official": true,
    "pdf@codebuddy-plugins-official": true,
    "docx@codebuddy-plugins-official": true,
    "xlsx@codebuddy-plugins-official": true,
    "agent-browser@codebuddy-plugins-official": true,
    "playwright-cli@codebuddy-plugins-official": true,
    "skills-sec-audit@codebuddy-plugins-official": true,
    "find-skills@codebuddy-plugins-official": true
  }
}
```

### 安装方式

1. **从插件市场安装**：下载插件包到 `~/.codebuddy/plugins/marketplaces/{marketplace}/`
2. **手动启用**：在 `settings.json` 的 `enabledPlugins` 中添加键值
3. **通过 config-manager 安装**：`install_plugin.sh <name> [--marketplace <marketplace>]`

### 状态检测

- 读取 `enabledPlugins` 对象：
  - 精确匹配键名 `{name}` 或 `{name}@{marketplace}`
  - 模糊匹配键名前缀 `{name}@`
  - 值为 `true` 表示启用，`false` 表示禁用

---

## 4. Model 配置

### 配置方式

Model 配置主要通过 CodeBuddy IDE 的设置界面管理，不直接存储为标准配置文件。有两种方式：

#### 方式一：IDE 设置（推荐）

```
CodeBuddy → 设置 → AI Model → 添加自定义模型
```

#### 方式二：环境变量

部分模型 SDK 通过环境变量配置：

```bash
export OPENAI_API_KEY="sk-xxxxx"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export DEEPSEEK_API_KEY="sk-xxxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
```

### 状态检测

- 读取 `~/.codebuddy/settings.json` 中的模型相关键值
- 检查常见环境变量：`OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `ANTHROPIC_API_KEY`, `AZURE_OPENAI_API_KEY`

---

## 5. CLI 工具配置

### 安装方式

CLI 工具通过系统包管理器安装，检测优先级如下：

| 包管理器 | 检测命令 | 适用范围 |
|----------|----------|----------|
| **Homebrew** | `which brew` | macOS/Linux 通用包管理器 |
| **npm** | `which npm` | Node.js 生态工具 |
| **pip3** | `which pip3` | Python 生态工具 |
| **cargo** | `which cargo` | Rust 生态工具 |
| **go** | `which go` | Go 生态工具 |

### 状态检测

- 使用 `command -v {name}` 检测是否在 PATH 中
- 使用 `{name} --version` 或 `{name} -v` 获取版本信息

### 包管理器安装命令参考

| 管理器 | 安装命令 | 全局安装 |
|--------|----------|---------|
| brew | `brew install <pkg>` | 默认全局 |
| npm | `npm install -g <pkg>` | 加 `-g` |
| pip3 | `pip3 install <pkg>` | 默认全局 |
| cargo | `cargo install <pkg>` | 默认全局 |
| go | `go install <pkg>@latest` | 默认全局 |

### 本系统可用包管理器

系统 `darwin`（macOS），已检测到以下包管理器全部可用：

- `brew` — Homebrew
- `npm` — Node.js 包管理器
- `pip3` — Python 3 包管理器
- `cargo` — Rust 包管理器
- `go` — Go 包管理器

---

## 6. 全局 vs 项目配置对比

| 配置类型 | 全局路径 | 项目路径 |
|----------|----------|----------|
| **MCP** | `~/.codebuddy/mcp.json` | `{project}/.codebuddy/mcp.json` |
| **Skill** | `~/.codebuddy/skills-marketplace/skills/{name}/` | `{project}/.codebuddy/skills/{name}/` |
| **Plugin** | `~/.codebuddy/settings.json` | 暂仅支持全局 |
| **Model** | IDE 设置 / 环境变量 | IDE 设置 |
| **CLI** | PATH 中的可执行文件 | 同全局 |

### 优先级规则

1. **项目级配置优先于全局配置**（同一配置项两者都存在时，项目级生效）
2. **Plugin 暂仅支持全局配置**
3. **CLI 工具为系统级**，不区分作用域

---

## 7. Marketplace 结构

### Skill Marketplace

```
~/.codebuddy/skills-marketplace/
├── .codebuddy-skill/
│   └── marketplace.json       # 技能清单索引（~372KB, 含347+个技能）
├── skills/                    # 已安装的技能库
│   ├── {name}/                # 每个技能一个目录
│   │   ├── SKILL.md
│   │   └── references/
├── icons/                     # 技能图标
├── README.md
└── version.txt                # 市场版本标记
```

### Plugin Marketplace

```
~/.codebuddy/plugins/
├── known_marketplaces.json    # 已知插件市场源
├── marketplaces/
│   ├── codebuddy-plugins-official/
│   │   ├── plugins/           # 插件包
│   │   └── dist/              # 编译产物
│   └── cb_teams_marketplace/
└── settings.json              # 插件启用配置
```

---

## 8. 配置文件操作注意事项

### macOS 兼容性

- `sed` 在 macOS 上对中文/多字节字符处理不佳，优先使用 `perl -CS` 或 `python3` 进行文本处理
- 使用 `mktemp` 创建临时文件时，macOS 版本需要 `-t` 参数
- macOS 默认使用 bash 3.2，`local` 与 `set -u` 配合时可能行为异常

### JSON 处理

- 所有配置文件的读写推荐使用 `python3 -c "import json; ..."` 确保编码正确
- 写入时使用 `ensure_ascii=False` 保留中文字符
- 读取时做好错误处理（文件不存在、JSON 解析错误）

### 权限

- 全局配置文件位于 `~/.codebuddy/`，通常无需额外权限
- 项目级配置需确保对项目目录有写入权限
- CLI 工具安装（brew/npm/pip3）可能需要管理员权限

## 9. 隐私安全指南

### 敏感信息保护原则

| 原则 | 说明 |
|------|------|
| **不在日志输出敏感值** | 所有验证和状态报告仅输出配置的存在性信息，不输出 API Key、Token、Password 等敏感字段的明文值 |
| **不在参数中传密钥** | MCP Server 的 `args` 参数可能包含密钥，脚本输出时自动对敏感参数做 `****` 遮盖 |
| **环境变量只检不泄** | 检测 API Key 环境变量时，仅确认"存在"或"不存在"，不输出具体变量名和值 |
| **使用临时文件传递敏感数据** | 安装脚本通过临时文件将含敏感信息的参数传递给处理引擎，避免嵌入 heredoc 或命令行 |
| **URL 脱敏** | 输出 URL 时自动遮盖查询参数中的 `token`、`key`、`api_key`、`secret` 等值 |
| **错误信息脱敏** | 异常处理和错误输出中对疑似密钥的字符串做遮盖处理 |

### 代码实现规范

```bash
# ❌ 错误：直接输出变量值，可能泄露密钥
echo "Command: $cmd"
echo "Args: ${args[@]}"

# ✅ 正确：只输出数量或脱敏后的摘要
echo "Command: $(echo $cmd | cut -d' ' -f1)"
echo "参数数量: ${#args[@]}"

# ❌ 错误：在 heredoc 中嵌入含敏感信息的变量
python3 << PYEOF
payload = "$json_payload_with_keys"
PYEOF

# ✅ 正确：通过 stdin 或临时文件传递
printf '%s' "$payload" | python3 << PYEOF
payload = sys.stdin.read()
PYEOF
```

### 环境变量安全

```bash
# ❌ 错误：在输出中包含环境变量名
echo "检测到 $VAR 环境变量已设置"

# ✅ 正确：只报告是否存在
echo "环境变量中检测到 API Key 配置"
```

### 配置读写安全

- 写入 `mcp.json` 时可能包含敏感字段（如 `env` 中的 API Key），确保文件权限为 `600`
- 读取配置用于输出时，不输出 `env` 字段的值，仅输出变量名
- 对输出中的 `args` 参数做智能脱敏（对 `--key=xxx`、`--token xxx` 等模式遮盖值）
- 验证报告中的 `target_path` 如果包含 home 目录，考虑替换为 `~`
