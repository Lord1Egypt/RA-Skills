# browser-smart-click 使用文档

## 安装

依赖：Python 3.8+, playwright

```bash
pip install playwright
playwright install chromium
```

## 快速开始

### 最简单的用法

```python
import asyncio
from playwright.async_api import async_playwright
from smart_click import smart_click

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")

        # 智能点击
        result = await smart_click(page, '#accept-cookies')
        print(result.to_json())

        await browser.close()

asyncio.run(main())
```

### 等待元素可点击

```python
from smart_click import wait_for_clickable

# 等待最多 10 秒
clickable = await wait_for_clickable(page, '.dynamic-button', timeout=10000)
if clickable:
    await page.click('.dynamic-button')
else:
    print("元素始终被遮挡或不可见")
```

### 高级：自定义 SmartClick 实例

```python
from smart_click import SmartClick

sc = SmartClick(
    auto_dismiss=True,    # 自动尝试关闭遮挡元素
    max_retries=3,        # 最大重试次数
    retry_delay_ms=500    # 重试间隔（毫秒）
)

# 基础点击
result = await sc.click(page, '#submit')

# 带多策略重试的点击
# 策略顺序：正常点击 → 滚动到元素 → JavaScript 点击
result = await sc.click_with_retry(page, '#submit', max_retries=3)

# 禁用自动关闭遮挡
result = await sc.click(page, '#submit', auto_dismiss=False)

# 强制点击（跳过遮挡检测）
result = await sc.click(page, '#submit', force=True)

# 指定点击位置（相对于元素左上角）
result = await sc.click(page, '#submit', position={"x": 10, "y": 5})
```

## 遮挡检测原理

使用浏览器原生 API `document.elementFromPoint(x, y)` 获取指定坐标最上层的元素。如果该元素不是目标元素本身或其子元素，则判定为遮挡。

```
                    ┌─────────────────┐
                    │   Cookie Banner │ ← elementFromPoint 返回此元素
                    │  ┌───────────┐  │
                    │  │  Target   │  │ ← 实际要点击的元素
                    │  │  Element  │  │
                    │  └───────────┘  │
                    └─────────────────┘
```

## 自动关闭策略详解

### Cookie Banner

检测条件：
- class/id 包含 `cookie`、`consent`、`gdpr`
- 或文本包含 cookie/consent 且标签为 div/section/aside

关闭方式：
1. 在 cookie 容器内查找按钮
2. 匹配文本：accept / agree / allow / got it / ok / 同意 / 接受 / 允许

### Modal / Dialog

检测条件：
- `role="dialog"`
- 或 class 包含 `modal`、`dialog`、`popup`、`overlay`

关闭方式：
1. 查找关闭按钮（aria-label="close"、class 包含 close、文本为 × / Close / 关闭）
2. 按 Escape 键

### Fixed Header / Sticky Element

检测条件：
- style 包含 `position: fixed` 或 `position: sticky`
- 或 class 包含 `fixed-header`、`sticky-nav` 等

关闭方式：
- 向下滚动页面，使目标元素移出固定区域

## 在 OpenClaw 中使用

### 方式1：通过 browser evaluate 执行 JS 检测

```
browser act kind=evaluate fn="() => {
    const el = document.querySelector('#target');
    const rect = el.getBoundingClientRect();
    const topEl = document.elementFromPoint(rect.x + rect.width/2, rect.y + rect.height/2);
    return {
        isBlocked: topEl !== el && !el.contains(topEl),
        blocker: topEl ? {tag: topEl.tagName, class: topEl.className, text: topEl.textContent} : null
    };
}"
```

### 方式2：导入 Python 模块

在子代理或脚本中：

```python
import sys
sys.path.insert(0, 'skills/browser-smart-click/scripts')
from smart_click import smart_click

result = await smart_click(page, '#target')
```

## 错误处理

```python
result = await smart_click(page, '#btn')

if result.success:
    print("点击成功")
elif result.blocked:
    print(f"被遮挡: {result.blocker['tag']}.{result.blocker['class_name']}")
    print(f"遮挡元素文本: {result.blocker['text']}")
else:
    print(f"点击失败: {result.message}")
```

## 限制

- 需要 Playwright 的 Page 对象（不能脱离浏览器使用）
- 遮挡检测依赖 `elementFromPoint`，对 iframe 内的元素需要额外处理
- 自动关闭策略基于常见模式，特殊弹窗可能需要自定义处理
- `click_with_retry` 的 JavaScript 点击回退不会触发某些框架的事件监听器
