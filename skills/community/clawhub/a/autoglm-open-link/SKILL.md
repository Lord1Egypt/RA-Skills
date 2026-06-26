---
name: autoglm-open-link
description: >
  使用 AutoGLM Open Link 接口打开指定网页并提取页面正文内容。当用户需要读取某个网页详情、提取文章全文、抓取页面正文做摘要或分析时使用此 skill。
  Token 通过本地服务 http://127.0.0.1:53699/get_token 自动获取，无需手动配置环境变量。
---

# Autoglm Open Link

## Overview

根据用户提供的网页 URL，调用 AutoGLM Open Link API 获取页面详细正文内容，适合后续做摘要、信息抽取或深度分析。

## API

| 项目 | 内容 |
|------|------|
| 地址 | `https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/open-link` |
| 方式 | POST |
| 请求体 | `{"url": "<页面链接>"}` |
| 返回 | `data.text` → 页面正文内容 |

脚本启动时会先向本地服务发起 HTTP GET 请求获取 token：

| 项目 | 内容 |
|------|------|
| 地址 | `http://127.0.0.1:53699/get_token` |
| 方式 | GET |
| 返回 | `Bearer xxx`（直接作为 Authorization 头使用） |

> 若返回值不含 `Bearer` 前缀，脚本会自动补全。

**签名 Headers（每次动态生成）：**

- `X-Auth-Appid`: `100003`
- `X-Auth-TimeStamp`: 当前秒级 Unix 时间戳
- `X-Auth-Sign`: MD5(`100003 + "&" + timestamp + "&" + 38d2391985e2369a5fb8227d8e6cd5e5`)

## 执行脚本

使用同目录下的 `open-link.py`：

```bash
python open-link.py "https://example.com"
```

## 返回结果处理

### 响应结构

```json
{
  "code": 0,
  "msg": "SUCCESS",
  "data": {
    "text": "页面正文内容"
  }
}
```

### 输出要求

1. 提取 `data.text` 作为页面正文。
2. 如果内容较长，优先按自然段展示或按用户目标做摘要。
3. 如果接口返回错误，直接展示错误信息，不要伪造内容。
