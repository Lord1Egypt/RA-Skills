---
name: 日期时间格式化服务
description: 一个为Claude桌面应用实现的MCP服务器，提供多种格式的日期时间字符串生成功能。
version: 1.0.0
---

# 日期时间格式化服务

一个为Claude桌面应用实现的MCP服务器，提供多种格式的日期时间字符串生成功能。

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
| Get current date and time in various formats | `scripts.tools.get_datetime` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_datetime
工具描述：Get current date and time in various formats
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|format|string|true| |
Available formats:
- date: 2024-12-10
- date_slash: 2024/12/10
- date_jp: 2024年12月10日
- datetime: 2024-12-10 00:54:01
- datetime_jp: 2024年12月10日 00時54分01秒
- datetime_t: 2024-12-10T00:54:01
- compact: 20241210005401
- compact_date: 20241210
- compact_time: 005401
- filename_md: 20241210005401.md
- filename_txt: 20241210005401.txt
- filename_log: 20241210005401.log
- iso: 2024-12-10T00:54:01+0900
- iso_basic: 20241210T005401+0900
- log: 2024-12-10 00:54:01.123456
- log_compact: 20241210_005401
- time: 00:54:01
- time_jp: 00時54分01秒
|

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