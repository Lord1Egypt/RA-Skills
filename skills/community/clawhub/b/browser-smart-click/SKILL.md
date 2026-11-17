---
name: browser-smart-click
description: "Retry browser clicks with automatic obstacle detection and dismissal. Use when browser tool clicks fail due to cookie banners, modals, or fixed headers blocking the target element."
tags: [browser, automation, playwright, click, overlay]
dependencies:
  - playwright
---

# browser-smart-click

解决 Playwright/OpenClaw browser 工具点击元素时被其他元素遮挡导致失败的问题�?
## 何时使用

- `browser click` 报错 `element is obscured` / `intercepted`
- 页面�?cookie banner、modal overlay、fixed header 遮挡目标元素
- 需要智能等待元素变为可交互状�?- 需要自动关闭弹窗后重试点击

## 核心 API

### Python 导入

```python
from smart_click import SmartClick, smart_click, wait_for_clickable
```

### smart_click(page, selector, **options) �?ClickResult

一行调用智能点击：

```python
result = await smart_click(page, '#submit-btn')
if result.success:
    print("Clicked!")
else:
    print(f"Failed: {result.message}")
    if result.blocked:
        print(f"Blocked by: {result.blocker}")
```

### wait_for_clickable(page, selector, timeout=10000) �?bool

等待元素可见且不被遮挡：

```python
clickable = await wait_for_clickable(page, '#btn', timeout=5000)
if clickable:
    await page.click('#btn')
```

### SmartClick 类（高级用法�?
```python
sc = SmartClick(auto_dismiss=True, max_retries=3)

# 基础点击
result = await sc.click(page, '#btn')

# 带重试的点击（滚�?�?JS click 回退�?result = await sc.click_with_retry(page, '#btn', max_retries=3)

# 等待可点�?ok = await sc.wait_for_clickable(page, '#btn', timeout=10000)
```

## ClickResult 格式

```json
{
  "success": true,
  "target": {"selector": "#submit-btn", "text": "Submit"},
  "blocked": false,
  "blocker": null,
  "retry_count": 0,
  "message": "Clicked successfully"
}
```

被遮挡时�?
```json
{
  "success": false,
  "target": {"selector": "#submit-btn", "text": "Submit"},
  "blocked": true,
  "blocker": {
    "tag": "div",
    "class_name": "cookie-banner",
    "text": "We use cookies",
    "bounding_box": {"x": 0, "y": 0, "width": 800, "height": 100},
    "attributes": {}
  },
  "retry_count": 1,
  "message": "Element blocked by: <div class=\"cookie-banner\"> text=\"We use cookies\""
}
```

## 自动处理策略

| 遮挡类型 | 检测方�?| 处理策略 |
|---------|---------|---------|
| Cookie Banner | class/id 包含 cookie/consent/gdpr | 点击 Accept/同意/允许 按钮 |
| Modal/Dialog | role=dialog �?class 包含 modal/popup | 点击 × 关闭按钮，或�?Escape |
| Fixed Header | style 包含 position:fixed/sticky | 滚动页面后重�?|
| 未知遮挡 | elementFromPoint 检�?| �?Escape 后重�?|

## 文件结构

```
skills/browser-smart-click/
├── SKILL.md                    # 本文�?├── scripts/
�?  ├── smart_click.py          # 核心实现
�?  └── test_smart_click.py     # 测试用例
└── references/
    └── usage.md                # 详细使用文档
```

## 测试

```bash
cd skills/browser-smart-click/scripts
pytest test_smart_click.py -v
```

## �?OpenClaw browser 工具配合

�?skill 不替�?OpenClaw browser 工具，而是作为补充�?
1. 先用 `browser snapshot` 获取页面状�?2. �?`browser act kind=click` 尝试点击
3. 如果失败（遮挡），导�?smart_click 处理�?   ```python
   from smart_click import smart_click
   result = await smart_click(page, '#target')
   ```
4. 或者在 OpenClaw �?`browser act evaluate` 中直接使用遮挡检�?JS
