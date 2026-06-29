---
name: axiom-markdown-link-auditor
description: Markdown 链接审计器 — 查找损坏的内部链接,标记已死的外部链接 (HEAD 请求),报告孤立页面。在维护文档时使用。纯标准库 + urllib (无需 LLM)。
version: 0.1.2
license: Apache-2.0
---

# axiom-markdown-link-auditor

**Version:** 0.1.2
**Axioma Tools**

审计 markdown 文档集的损坏链接和孤立页面。

## What this skill does

- 查找损坏的内部链接
- 对外部链接可选 HEAD 检查
- 报告孤立页面 (无传入链接)
- 用于 CI 集成的 JSON 输出

## When to use this skill

- ✅ 部署前审计文档
- ✅ CI 关卡防止链接损坏
- ✅ 查找 wiki 中的孤立页面
- ❌ 将 markdown 渲染为 HTML (使用 markdown 库)

## Usage

```bash
python3 axiom_markdown_link_auditor.py ./docs/
python3 axiom_markdown_link_auditor.py README.md --check-external --json
```

```python
from axiom_markdown_link_auditor import audit_directory
report = audit_directory('./docs/')
# {broken: [...], orphans: [...], total_links: 123}
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 15+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
