---
name: axiom-url-canonicalizer
description: URL 规范化器 — 为 SEO 和比较规范化 URL:小写主机、排序参数、去除跟踪、规范化百分号编码。在需要规范 URL 形式时使用。纯标准库,无需 LLM。
version: 0.1.2
license: Apache-2.0
---

# axiom-url-canonicalizer

**Version:** 0.1.2
**Axioma Tools**

将 URL 规范化为适合 SEO 和比较的形式。

## What this skill does

- 主机小写 (保留路径大小写)
- 对查询参数排序
- 去除默认端口 (80, 443)
- 可选:去除跟踪参数 (utm_*, fbclid, gclid)
- 可选:规范化百分号编码
- 删除根路径上的尾部斜杠

## When to use this skill

- ✅ 为 SEO 生成规范 URL
- ✅ URL 列表去重
- ✅ 比较 URL 时忽略跟踪噪音
- ❌ 跟随重定向 (需要单独的库)
- ❌ 从 HTML 解析 URL (使用 BeautifulSoup)

## Usage

```bash
python3 axiom_url_canonicalizer.py "HTTPS://Example.com:443/Path/?b=2&a=1&utm_source=tw"
python3 axiom_url_canonicalizer.py urls.txt --strip-tracking
```

```python
from axiom_url_canonicalizer import canonicalize
canonicalize('HTTPS://Example.com/?b=2&a=1')
# 'https://example.com/?a=1&b=2'
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 20 cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
