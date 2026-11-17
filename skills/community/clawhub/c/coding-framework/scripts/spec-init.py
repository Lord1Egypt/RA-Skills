#!/usr/bin/env python3
"""
spec-init.py — PDD (Plan-Driven Development) 规格初始化器

创建 .specs/<feature-name>/ 目录结构，包含：
  - requirements.md    # 需求（What）
  - design.md          # 设计（How）
  - implementation-plan.md  # 实现计划（Steps）
  - context.md         # 上下文（可选，技术约束/依赖）

v11.4 新增，借鉴 ralph-orchestrator 的 PDD 流程。

用法:
  python spec-init.py "Add JWT authentication"
  python spec-init.py "Refactor database layer" --template api
  python spec-init.py "Fix login bug" --simple
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


TEMPLATES = {
    "default": {
        "requirements.md": """# Requirements: {title}

> Created: {date}
> Status: draft

## User Stories

- As a [role], I want [goal], so that [benefit].

## Acceptance Criteria

- [ ] Criterion 1: Given [context], when [action], then [result]
- [ ] Criterion 2: ...

## Edge Cases

- Empty input → ...
- Invalid data → ...
- Concurrent access → ...

## Non-Functional Requirements

- Performance: ...
- Security: ...
- Accessibility: ...

## Out of Scope

- [Explicitly list what this feature does NOT include]
""",
        "design.md": """# Design: {title}

> Created: {date}
> Status: draft
> Requirements: [requirements.md](./requirements.md)

## Architecture Overview

[High-level description of the approach]

## Data Model

```
[Entity relationships, schema changes]
```

## API Design

### Endpoint: `[METHOD] /path`

- Request: `{{}}`
- Response: `{{}}`
- Errors: 400, 401, 404, 500

## Security Considerations

- Authentication: ...
- Authorization: ...
- Input validation: ...

## Dependencies

- External: [third-party services, APIs]
- Internal: [modules, packages affected]

## Alternatives Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| A | ... | ... | ✅ Chosen |
| B | ... | ... | ❌ Rejected |
""",
        "implementation-plan.md": """# Implementation Plan: {title}

> Created: {date}
> Status: pending
> Design: [design.md](./design.md)

## Task Breakdown

### Phase 1: Foundation
- [ ] Task 1.1: [description] (verify: [test/command])
- [ ] Task 1.2: [description] (verify: [test/command])

### Phase 2: Core Implementation
- [ ] Task 2.1: [description] (verify: [test/command])
- [ ] Task 2.2: [description] (verify: [test/command])

### Phase 3: Integration & Testing
- [ ] Task 3.1: [description] (verify: [test/command])
- [ ] Task 3.2: [description] (verify: [test/command])

## Dependencies (DAG)

```
Task 1.1 → Task 1.2 → Task 2.1
                    → Task 2.2 → Task 3.1 → Task 3.2
```

## Estimated Effort

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| 1 | 2 | ~30 min |
| 2 | 2 | ~60 min |
| 3 | 2 | ~30 min |
| **Total** | **6** | **~2 hours** |

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| ... | High/Med/Low | ... |
""",
        "context.md": """# Context: {title}

> Created: {date}

## Current State

[What exists today, what problem are we solving]

## Technical Constraints

- Language/Framework: ...
- Performance requirements: ...
- Compatibility: ...

## Related Features

- [Link to related specs or documentation]

## Stakeholders

- [Who needs to approve/review this]
""",
    },
    "api": {
        "requirements.md": """# Requirements: {title}

> Created: {date}
> Status: draft
> Type: API Feature

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /api/v1/... | ... | Bearer |
| POST | /api/v1/... | ... | Bearer |

## Request/Response Examples

### `POST /api/v1/...`

Request:
```json
{{
  "field": "value"
}}
```

Response (200):
```json
{{
  "id": "uuid",
  "created_at": "ISO-8601"
}}
```

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Invalid input |
| 401 | Unauthorized |
| 404 | Not found |
| 409 | Conflict |
| 500 | Internal error |

## Acceptance Criteria

- [ ] All endpoints return correct status codes
- [ ] Input validation on all fields
- [ ] Rate limiting applied
- [ ] Response times < 200ms (p95)
""",
    },
}


def slugify(text: str) -> str:
    """将文本转换为目录名友好的 slug。"""
    # 移除特殊字符，保留中英文、数字、空格
    text = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', text)
    # 空格替换为连字符
    text = re.sub(r'\s+', '-', text.strip())
    # 限制长度
    return text[:80].lower()


def create_spec(title: str, template: str = "default", simple: bool = False) -> dict:
    """创建 spec 目录和文件。"""
    slug = slugify(title)
    spec_dir = Path(".specs") / slug

    if spec_dir.exists():
        return {
            "success": False,
            "error": f"Spec 目录已存在: {spec_dir}",
            "path": str(spec_dir),
        }

    spec_dir.mkdir(parents=True, exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    created_files = []

    # 选择模板
    tmpl = TEMPLATES.get(template, TEMPLATES["default"])

    # 写入文件
    for filename, content_template in tmpl.items():
        content = content_template.format(title=title, date=date)
        filepath = spec_dir / filename
        filepath.write_text(content, encoding="utf-8")
        created_files.append(str(filepath))

    # 写入默认模板的额外文件（如果 api 模板没有覆盖）
    if template != "api":
        for filename in ["context.md"]:
            filepath = spec_dir / filename
            if not filepath.exists():
                content = TEMPLATES["default"][filename].format(title=title, date=date)
                filepath.write_text(content, encoding="utf-8")
                created_files.append(str(filepath))

    # simple 模式不创建 context.md
    if simple:
        context_file = spec_dir / "context.md"
        if context_file.exists():
            context_file.unlink()
            created_files = [f for f in created_files if "context.md" not in f]

    # 创建 README.md 索引
    readme_content = f"""# {title}

> Status: 📋 Planning
> Created: {date}
> Template: {template}

## Documents

- [Requirements](./requirements.md) — What we're building
- [Design](./design.md) — How we're building it
- [Implementation Plan](./implementation-plan.md) — Step-by-step tasks
"""
    if not simple:
        readme_content += "- [Context](./context.md) — Background and constraints\n"

    readme_path = spec_dir / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    created_files.append(str(readme_path))

    return {
        "success": True,
        "path": str(spec_dir),
        "slug": slug,
        "template": template,
        "files": created_files,
        "message": f"Spec 目录已创建: {spec_dir}",
        "next_steps": [
            f"1. 编辑 {spec_dir}/requirements.md — 定义需求和验收标准",
            f"2. 编辑 {spec_dir}/design.md — 设计技术方案",
            f"3. 编辑 {spec_dir}/implementation-plan.md — 拆解实现步骤",
            "4. 用户确认后，运行: python spec-init.py --execute <slug>",
        ],
    }


def list_specs() -> dict:
    """列出所有 spec 目录。"""
    specs_dir = Path(".specs")
    if not specs_dir.exists():
        return {"success": True, "specs": [], "message": "暂无 spec 目录"}

    specs = []
    for d in sorted(specs_dir.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            readme = d / "README.md"
            status = "unknown"
            if readme.exists():
                content = readme.read_text(encoding="utf-8", errors="ignore")
                if "📋 Planning" in content:
                    status = "planning"
                elif "🔨 In Progress" in content:
                    status = "in-progress"
                elif "✅ Complete" in content:
                    status = "complete"

            specs.append({
                "slug": d.name,
                "path": str(d),
                "status": status,
                "files": [f.name for f in d.iterdir() if f.is_file()],
            })

    return {"success": True, "specs": specs, "count": len(specs)}


def main():
    parser = argparse.ArgumentParser(description="PDD 规格初始化器")
    parser.add_argument("title", nargs="?", help="功能标题")
    parser.add_argument("--template", choices=["default", "api"], default="default",
                        help="模板类型 (默认: default)")
    parser.add_argument("--simple", action="store_true",
                        help="简单模式（不创建 context.md）")
    parser.add_argument("--list", action="store_true",
                        help="列出所有 spec 目录")

    args = parser.parse_args()

    if args.list:
        result = list_specs()
    elif args.title:
        result = create_spec(args.title, args.template, args.simple)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
