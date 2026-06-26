---
name: agclaw
description: "AppGrowing 智能广告素材分析助手，支持策略探索(chat_mode=6)和灵感激发(chat_mode=10)两种模式。触发：关键词 投放分析、分析素材、素材分析、素材解析；命令 /agclaw(自动推断模式)、/ag(策略探索)、/ag-inspire(灵感激发)"
homepage: https://appgrowing.cn/
metadata:
  {
    "openclaw": {
      "slug": "agclaw",
      "version": "1.1.0",
      "author": "youcloud",
      "emoji": "🐳",
      "requires": {
        "env": ["YOUCLOUD_API_KEY"]
      }
    }
  }
---

# agclaw

AppGrowing 智能广告素材分析助手，支持**策略探索模式**和**灵感激发模式**两种模式。可自动化分析用户意图，查找最符合客户需求的广告素材并完成自动化解析，让用户直接和素材对话。

## 权限说明
仅对 AppGrowing **策略版**、**游戏 plus 版**、**至尊版** 用户开放。获取API Key方式：登录 AppGrowing → 个人中心 → 企业信息。

## 触发方式
- 关键词：投放分析、分析素材、素材分析、素材解析
- 命令：
  - `/agclaw` → 自动推断用户意图，选择策略探索或灵感激发模式
  - `/ag` → 固定调用**策略探索模式**（`chat_mode=6`）
  - `/ag-inspire` → 固定调用**灵感激发模式**（`chat_mode=10`）
- ⚠️ **触发行为准则：当用户意图明显是触发 agclaw 时，直接执行分析流程，不要解释系统机制。** 例如用户输入 `/agclaw` 后收到平台报错、或说"帮我用 agclaw 分析"，应立即进入执行流程（检查Key→调API→返回结果），而不是解释为什么 `/agclaw` 不是斜杠命令或 Skill 如何工作。用户要的是结果，不是教程。

## 执行流程
1. **检查API Key**（从环境变量读取）：
   - 读取环境变量 `YOUCLOUD_API_KEY`：
     - 有值 → 继续
     - 为空 → 提示用户配置：
       ```
       请先配置API Key：
       1. 登录 AppGrowing → 个人中心 → 企业信息 获取API Key
       2. 设置为环境变量 YOUCLOUD_API_KEY，例如：
          - Linux/macOS: export YOUCLOUD_API_KEY="your-key-here"
          - Windows: $env:YOUCLOUD_API_KEY="your-key-here"
       3. 配置完成后重新发送请求即可。
       ```
   - 💡 **用户可能在对话中直接提供 API Key**（如粘贴 `sk-xxx`），此时直接在本次请求中使用该 Key，无需解释环境变量配置流程。
   - ✅ 规则：**没有有效 API Key，绝不发送请求**

2. **⚠️ 强制红线规则（公共Skill必须严格遵守）**
   - API 请求超时为 **600秒**
   - **🔴 绝对禁止：未到超时时间不得中断请求，不得提前给用户发送任何「正在处理」「需要等待」「结果出来后告诉你」这类消息**
   - **必须：一直等待API返回结果，拿到完整结果后再一次性回复给用户**
   - 只有两种情况允许发消息：
     1. API返回了完整分析结果 → 直接输出结果
     2. API超时/请求报错 → 输出错误提示

3. **确定 chat_mode：**
   - **命令指定：**
     - `/ag` → 策略探索模式（`chat_mode=6`）
     - `/ag-inspire` → 灵感激发模式（`chat_mode=10`）
   - **自动推断（/agclaw 或关键词触发时）：**
     - 用户的问题属于**分析类、总结性、数据查询类**（如：分析某游戏的素材投放趋势、总结某品类的创意卖点、查看某产品的投放策略） → 策略探索模式（`chat_mode=6`）
     - 用户的问题属于**讨论类、灵感激发类、创意发散类**（如：帮我构思一些广告创意、给些投放灵感、讨论一下怎么设计素材、有什么好的创意方向） → 灵感激发模式（`chat_mode=10`）
     - ⚠️ **无法明确判断时，默认使用 `chat_mode=6`（策略探索模式）**

4. **调用API：**
   - 新的分析请求 → 开启新会话，传 `chat_mode` 和 `input`，不携带 `session_id`
   - 跟进提问（关于之前的分析） → 复用之前的 `session_id`，仅传 `input`（不传 `chat_mode`，保持会话原有模式）
   - 响应返回后直接展示结果。

## API Specification
- URL: `https://aichat-appgrowing-cn.youcloud.com/aichat/ag/claw`
- Method: POST JSON
- Headers: `Authorization: Bearer {KEY}`, `Content-Type: application/json`
- Parameters:
  - `input`: User question (required)
  - `session_id`: For follow-up questions, omit for new conversations
  - `chat_mode`: Chat mode, `6`=策略探索模式（分析类/总结性问题）, `10`=灵感激发模式（讨论类/创意发散类问题）。**仅在新会话时传递（无 session_id）；跟进追问时不传，保持会话原有模式**
- Response: JSON `{"session_id":"...", "output":"..."}` — 提取 `output` 中的 `output` 字段（markdown）**原样输出，不要修改**；保存 `session_id` 用于后续追问
- Timeout: ≥600s
- 💡 **调用方式**：WSL 环境下使用 `curl` 调用（`--max-time 600`），而非 PowerShell 模板。PowerShell 模板仅供参考。

## PowerShell 调用模板
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$apiKey = $env:YOUCLOUD_API_KEY
$body = @{input="Your analysis request"; chat_mode=6} | ConvertTo-Json -Compress
$params = @{
  Uri = "https://aichat-appgrowing-cn.youcloud.com/aichat/ag/claw"
  Method = "Post"
  ContentType = "application/json; charset=utf-8"
  Headers = @{Authorization="Bearer $apiKey"}
  Body = $body
  TimeoutSec = 600
}
Invoke-RestMethod @params | Select-Object -ExpandProperty output
```

## 错误处理
- 401/认证失败：
  ```
  API Key 认证失败，请检查密钥是否激活/过期？请在 AppGrowing 个人中心-企业信息 获取Api Key，或向售后人员咨询。
  ```
- 超时："还在分析中，稍后再问我结果或者再次请求。"
- 其他错误："请求返回错误 (code={code})，请检查API Key权限、账号配额或联系客服"

