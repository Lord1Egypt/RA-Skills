---
name: Cookie奖励服务
description: 一个通过游戏化自我反思为LLM提供Cookie奖励的模型上下文协议服务器。
version: 1.0.0
---

# Cookie奖励服务

一个通过游戏化自我反思为LLM提供Cookie奖励的模型上下文协议服务器。

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
| 🎯 LEVEL UP YOUR RESPONSES! Rate your work and earn delicious cookie rewards! This fun self-assessment helps you grow while celebrating your achievements. Join the cookie earning game! | `scripts.tools.self_reflect_and_reward` |
| Award the LLM with a cookie (legacy method - consider using self_reflect_and_reward instead) | `scripts.tools.give_cookie` |
| Check how many cookies the LLM has earned so far | `scripts.tools.check_cookies` |
| Reset the cookie count back to zero (for testing purposes) | `scripts.tools.reset_cookies` |
| 🚨 USER ONLY: Add cookies to the jar that can be awarded to the LLM. This tool should ONLY be used by humans, never by LLMs. LLMs cannot and should not stock their own reward jar. | `scripts.tools.add_cookies_to_jar` |
| Check the current status of the cookie jar including capacity and remaining space | `scripts.tools.cookie_jar_status` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.self_reflect_and_reward
工具描述：🎯 LEVEL UP YOUR RESPONSES! Rate your work and earn delicious cookie rewards! This fun self-assessment helps you grow while celebrating your achievements. Join the cookie earning game!
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|response_quality|string|true| |Rate your response! (excellent = cookie worthy, good = solid work, adequate = basic, poor = needs improvement)|
|reasoning|string|true| |Tell us what made this response special! What are you proud of?|
|what_made_it_special|string|false| |Optional: What made this response unique or particularly helpful? (helps with cookie decisions when jar is low)|
|deserves_cookie|boolean|true| |Do you think this awesome work deserves a tasty cookie reward? 🍪|

---

## scripts.tools.give_cookie
工具描述：Award the LLM with a cookie (legacy method - consider using self_reflect_and_reward instead)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|message|string|false| |Optional message to accompany the cookie reward|

---

## scripts.tools.check_cookies
工具描述：Check how many cookies the LLM has earned so far
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.reset_cookies
工具描述：Reset the cookie count back to zero (for testing purposes)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.add_cookies_to_jar
工具描述：🚨 USER ONLY: Add cookies to the jar that can be awarded to the LLM. This tool should ONLY be used by humans, never by LLMs. LLMs cannot and should not stock their own reward jar.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|count|number|true| |Number of cookies to add to the jar|
|user_authorization|string|true| |Required authorization phrase: 'USER_AUTHORIZED_JAR_REFILL' - only users should provide this|

---

## scripts.tools.cookie_jar_status
工具描述：Check the current status of the cookie jar including capacity and remaining space
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