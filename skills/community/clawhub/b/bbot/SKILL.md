---
name: BBOT安全扫描服务
description: BBOT MCP服务器是一个用于管理和执行BBOT安全扫描的工具，提供模块管理、预设配置、实时监控等功能。
version: 1.0.0
---

# BBOT安全扫描服务

BBOT MCP服务器是一个用于管理和执行BBOT安全扫描的工具，提供模块管理、预设配置、实时监控等功能。

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
| List all available bbot modules | `scripts.tools.list_bbot_modules` |
| List all available bbot presets | `scripts.tools.list_bbot_presets` |
| 
Start a new bbot scan

Args:
    targets: Comma-separated list of targets (domains, IPs, URLs)
    modules: Comma-separated list of modules to use (optional)
    presets: Comma-separated list of presets to use (optional)
    flags: Comma-separated list of flags to use (optional)
    no_deps: Disable dependency installation to prevent sudo prompts (default: True)
 | `scripts.tools.start_bbot_scan` |
| Get the status of a specific scan | `scripts.tools.get_scan_status` |
| 
Get results from a specific scan

Args:
    scan_id: The ID of the scan
    limit: Maximum number of results to return (default: 100)
 | `scripts.tools.get_scan_results` |
| List all active scans | `scripts.tools.list_active_scans` |
| 
Wait for a scan to complete with timeout and progress reporting

Args:
    scan_id: The ID of the scan to wait for
    timeout: Maximum time to wait in seconds (default: 300 = 5 minutes)
    poll_interval: How often to check scan status in seconds (default: 5)
    include_progress: Whether to include progress updates in the response (default: True)
 | `scripts.tools.wait_for_scan_completion` |
| Get information about dependency management in bbot scans | `scripts.tools.get_dependency_info` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.list_bbot_modules
工具描述：List all available bbot modules
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.list_bbot_presets
工具描述：List all available bbot presets
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.start_bbot_scan
工具描述：
Start a new bbot scan

Args:
    targets: Comma-separated list of targets (domains, IPs, URLs)
    modules: Comma-separated list of modules to use (optional)
    presets: Comma-separated list of presets to use (optional)
    flags: Comma-separated list of flags to use (optional)
    no_deps: Disable dependency installation to prevent sudo prompts (default: True)

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|targets|string|true| |null|
|modules|string|false|""|null|
|presets|string|false|""|null|
|flags|string|false|""|null|
|no_deps|boolean|false|true|null|

---

## scripts.tools.get_scan_status
工具描述：Get the status of a specific scan
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|scan_id|string|true| |null|

---

## scripts.tools.get_scan_results
工具描述：
Get results from a specific scan

Args:
    scan_id: The ID of the scan
    limit: Maximum number of results to return (default: 100)

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|scan_id|string|true| |null|
|limit|integer|false|100.0|null|

---

## scripts.tools.list_active_scans
工具描述：List all active scans
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.wait_for_scan_completion
工具描述：
Wait for a scan to complete with timeout and progress reporting

Args:
    scan_id: The ID of the scan to wait for
    timeout: Maximum time to wait in seconds (default: 300 = 5 minutes)
    poll_interval: How often to check scan status in seconds (default: 5)
    include_progress: Whether to include progress updates in the response (default: True)

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|scan_id|string|true| |null|
|timeout|integer|false|300.0|null|
|poll_interval|integer|false|5.0|null|
|include_progress|boolean|false|true|null|

---

## scripts.tools.get_dependency_info
工具描述：Get information about dependency management in bbot scans
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