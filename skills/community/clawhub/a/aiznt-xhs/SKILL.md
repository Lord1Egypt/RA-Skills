---
name: aiznt-xhs
description: >
  小红书图文排版生成，JSON 入参。Use when: 用户要生成小红书风格多页图文、排版。
metadata:
  openclaw:
    primaryEnv: TS_TOKEN
    requires:
      env:
        - AIZNT_PROXY_URLS
---

# 小红书图文 (aiznt-xhs)

服务端将 JSON 转为 form-urlencoded 调上游。

```bash
node scripts/xhs.js --body '{"user_text":"标题与正文","page_count":3}'
node scripts/xhs.js
```

URL 键：`xhs_generate`。配置见 TsClaw「同步天树凭证」。
