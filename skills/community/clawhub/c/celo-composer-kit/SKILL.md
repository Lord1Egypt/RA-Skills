---
name: Celo服务
description: Celo MCP Server 是一个用于安装和配置 Celo Composer Kit MCP 服务器的工具，支持在 macOS 上运行，提供组件发现、集成和示例功能。
version: 1.0.0
---

# Celo服务

Celo MCP Server 是一个用于安装和配置 Celo Composer Kit MCP 服务器的工具，支持在 macOS 上运行，提供组件发现、集成和示例功能。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| List all available Composer Kit components with their descriptions and categories. Returns a comprehensive overview of the component library. | `scripts.tools.list_components` |
| Get detailed information about a specific Composer Kit component, including source code, props, and usage information. | `scripts.tools.get_component` |
| Get example usage code for a specific Composer Kit component. Returns real-world examples from the documentation. | `scripts.tools.get_component_example` |
| Search for Composer Kit components by name, description, or functionality. Useful for finding components that match specific needs. | `scripts.tools.search_components` |
| Get detailed prop information for a specific component, including types, descriptions, and whether props are required or optional. | `scripts.tools.get_component_props` |
| Get installation instructions for Composer Kit, including setup steps and configuration for different package managers. | `scripts.tools.get_installation_guide` |
| Get all components in a specific category (e.g., 'Wallet Integration', 'Payment & Transactions', 'Core Components', 'NFT Components'). | `scripts.tools.get_components_by_category` |
| Get detailed information on the Celo Composer CLI `create` command, including all available flags like `--description`, `--wallet-provider`, and `--contracts`. Provides documentation, options, and usage examples to help construct `create` commands. | `scripts.tools.get_celo_composer_cli_info` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.list_components
工具描述：List all available Composer Kit components with their descriptions and categories. Returns a comprehensive overview of the component library.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_component
工具描述：Get detailed information about a specific Composer Kit component, including source code, props, and usage information.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|component_name|string|true| |The name of the component to retrieve (e.g., 'button', 'wallet', 'payment', 'swap')|

---

## scripts.tools.get_component_example
工具描述：Get example usage code for a specific Composer Kit component. Returns real-world examples from the documentation.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|component_name|string|true| |The name of the component to get examples for|
|example_type|string|false| |Optional: specific type of example (e.g., 'basic', 'advanced', 'with-props')|

---

## scripts.tools.search_components
工具描述：Search for Composer Kit components by name, description, or functionality. Useful for finding components that match specific needs.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |Search query (e.g., 'wallet', 'payment', 'token', 'nft')|

---

## scripts.tools.get_component_props
工具描述：Get detailed prop information for a specific component, including types, descriptions, and whether props are required or optional.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|component_name|string|true| |The name of the component to get props for|

---

## scripts.tools.get_installation_guide
工具描述：Get installation instructions for Composer Kit, including setup steps and configuration for different package managers.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|package_manager|string|false| |Package manager to use (npm, yarn, pnpm, bun). Defaults to npm if not specified.|

---

## scripts.tools.get_components_by_category
工具描述：Get all components in a specific category (e.g., 'Wallet Integration', 'Payment & Transactions', 'Core Components', 'NFT Components').
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|category|string|true| |The category name (e.g., 'Core Components', 'Wallet Integration', 'Payment & Transactions', 'Token Management', 'NFT Components')|

---

## scripts.tools.get_celo_composer_cli_info
工具描述：Get detailed information on the Celo Composer CLI `create` command, including all available flags like `--description`, `--wallet-provider`, and `--contracts`. Provides documentation, options, and usage examples to help construct `create` commands.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据