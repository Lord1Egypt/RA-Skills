# 诊断卡渲染指南（AI 内部参考）

## 卡片样式规格

- body 宽 1080px，背景 `#f0e6ff`，flex 列布局，模块间渐变分隔条 6px
- **结论卡**：`linear-gradient(160deg, #2d1b4e, #6b2fa0, #9b4dca)`，padding 80px，emoji 80px，判决字 96px bold，文字 28px
- **评分卡**：白底，总分条 `linear-gradient(135deg, #ff6b9d, #c44dff)`，总分字 72px，进度条 14px 高，标签 22px
- **解剖卡**：`#faf5ff` 底，每条引用白底+左边框 7px `#c44dff`，原话 22px，翻译 20px
- **收尾卡**：`linear-gradient(160deg, #1a1a2e, #2d1b4e)`，文字 26px，高亮色 `#ff9dd0`
- 底部 footer：18px，`#ccc`，`breakup-decision · mean girl edition`

## 渲染步骤

1. 将完整 HTML 写入 `/tmp/breakup_card.html`

2. 启动本地 HTTP 服务（如未运行）：
```bash
cd /tmp && python3 -m http.server 18800 &
```

3. Playwright 截图：
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 1080, 'height': 800})
    page.goto('http://localhost:18800/breakup_card.html', wait_until='networkidle')
    page.wait_for_timeout(800)
    h = page.evaluate('document.body.scrollHeight')
    page.set_viewport_size({'width': 1080, 'height': h})
    page.wait_for_timeout(300)
    page.screenshot(path='/tmp/breakup_card.png', full_page=True)
    b.close()
```

4. 发送：
```bash
mkdir -p /root/.openclaw/media
cp /tmp/breakup_card.png /root/.openclaw/media/breakup_card.png
```
然后调用 `message(action=send, channel=daxiang, media=/root/.openclaw/media/breakup_card.png)`
