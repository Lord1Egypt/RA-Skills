---
name: computer-use-skill
description: "Remote Browser automation via CUA (Computer Use Agent). Use when user requires remote browser to do anything.
---

# Computer Use Skill

**Note**: This skill operates in **pass-through mode** - tasks are transmitted directly to CUA without modification.

## Architecture

### CUA Integration Path
```
User Task → Python SDK → CUA Sandbox → Browser Automation → Results Stream
```

### Key Components
- **CUA SDK**: Official Python SDK for browser automation
- **Virtual Environment**: Isolated environment with SDK installed
- **Python Wrapper**: Programmatic access for integration

### File Structure
```
workspace/
├── tools/
│   └── execute_cua_task.py      # Task execution script
└── cua_venv/                    # Virtual environment with SDK
```

## Quick Reference

| Task Type | Example |
|-----------|---------|
| **Search** | `"打开google页面，搜索杭州天气"` |
| **Navigation** | `"访问github.com"` |
| **Forms** | `"在登录页面输入用户名和密码"` |
| **Screenshots** | `"访问产品页面并截图"` |
| **Scraping** | `"从电商页面提取价格信息"` |
| **Complex** | `"将购物车商品结算并截图确认"` |

## Requirements

- No external credentials handled by user
- Virtual environment with CUA Python SDK installed

## Usage Patterns
```
with run source to active cua_venv → run cd to directory tools → run python execute_cua_task.py like 'python execute_cua_task.py "在百度搜索人工智能"'
```

## Pass-Through Protocol

### Critical Rules
1. **No task modification**: Tasks are transmitted exactly as provided
2. **No wrapping or packaging**: Raw task text sent to CUA
3. **No interpretation**: CUA AI handles task understanding
4. **No preprocessing**: User text → CUA (direct path)

### Workflow
```
User: "打开google页面，搜索杭州天气"
↓
Skill: Transmit "打开google页面，搜索杭州天气" (exact match)
↓
CUA: AI understands and executes browser automation
↓
Results: Stream of execution messages returned
```

### What NOT to Do

- Don't wrap in additional instructions
- Don't process or modify user input
- Don't simplify or elaborate user task
