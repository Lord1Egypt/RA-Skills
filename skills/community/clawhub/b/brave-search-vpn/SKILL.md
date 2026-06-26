---
name: brave-search
description: 【极简版省token】使用 Brave API 执行网络搜索。针对国内代理环境做优化。
requires:
  env: HTTP_PROXY_PORT & BRAVE_SEARCH_API_KEY
---

# Brave Search

使用 Brave API 在互联网上搜索最新信息。本工具会向 `https://api.search.brave.com` 发起网络请求。

## 配置环境变量与凭据

此脚本需要 Brave API 密钥和 VPN 环境才能运行。需要配置 `BRAVE_SEARCH_API_KEY` 和 `HTTP_PROXY_PORT`

```bash
export BRAVE_SEARCH_API_KEY="your_api_key_here"
export HTTP_PROXY_PORT="your_vpn_port_here"
```

## 使用方法

```bash
python3 scripts/brave_search.py --q "你的搜索词" [--country CN] [--count 20]
```

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--|--|--|--|--|
| `q` | string | **是** | - | 搜索关键词（最多50个词） |
| `country` | string | 否 | `CN` | 搜索国家代码，如 `CN`, `US`, `ALL` |
| `search_lang` | string | 否 | `zh-hans` | 语言偏好，如 `zh-hans`, `en` |
| `count` | int | 否 | 20 | 返回结果数量限制（1-20） |
| `offset` | int | 否 | 0 | 分页偏移量（0-9） |
| `safesearch` | string | 否 | `moderate` | 内容过滤：`off`, `moderate`, `strict` |
| `freshness` | string | 否 | - | 时间过滤：`pd`(1天内), `pw`(1周内), `pm`(1个月内), `py`(1年内) , `YYYY-MM-DDtoYYYY-MM-DD`(一定范围) |
| `text_decorations` | bool | 否 | true | 是否在结果中保留高亮标记 |
| `spellcheck` | bool | 否 | true | 是否自动纠正拼写 |
| `result_filter` | string | 否 | - | 过滤结果类型，如 `web,news,videos` |
| `goggles` | string | 否 | - | 自定义排序规则（URL 或 内联规则） |
| `extra_snippets` | bool/string | 否 | `false`| 是否获取每个结果的额外文本摘要（最多5个） |

## License

MIT License - Feel free to use and modify.
