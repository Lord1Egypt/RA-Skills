---
slug: cn-web-screenshot
name: cn-web-screenshot
version: "1.0.0"
description: "网页截图工具。输入URL自动捕获网页截图，支持全页截图、视口截图、移动端视图、延迟加载等待。保存为PNG格式。"
scope: "web screenshot, page capture, visual testing"
install: |
  pip install playwright
  playwright install chromium
env: ""
entry:
  type: prompt
  prompt: |
    当用户需要截取网页、保存网页截图、捕获页面时，使用此skill。
    识别意图：
    - "截取这个网页"
    - "网页截图"
    - "保存页面截图"
    - "捕获网站画面"
    - "帮我截图"
    执行流程：
    1. 获取URL
    2. 调用 scripts/web_screenshot.py 截图
    3. 返回截图路径
handler: |
  调用 scripts/web_screenshot.py 截取网页
---

# CN Web Screenshot - 网页截图工具

基于 Playwright 的网页截图工具，支持全页截图、视口截图、移动端/平板视图、自定义尺寸和延迟等待。

## 功能

- **全页截图**：捕获整个网页（超出视口的滚动区域也包含）
- **视口截图**：仅截取当前视口可见区域
- **移动端视图**：模拟 iPhone 6/7/8 尺寸 (375×667)
- **平板视图**：模拟 iPad 尺寸 (768×1024)
- **自定义等待**：页面加载后等待指定毫秒再截图（适合 JS 渲染的页面）
- **自动协议**：URL 缺少协议时自动补全 `https://`

## 依赖安装

```bash
pip install playwright
playwright install chromium
```

## 使用方法

```bash
# 基本截图（全页，移动端视图）
python3 scripts/web_screenshot.py "https://example.com" --viewport mobile

# 视口截图
python3 scripts/web_screenshot.py "https://news.ycombinator.com" -p

# 平板视图截图
python3 scripts/web_screenshot.py "https://example.com" --viewport tablet

# 指定输出路径
python3 scripts/web_screenshot.py "https://example.com" -o /tmp/page.png

# 等待3秒后截图（适合 SPA/React/Vue 页面）
python3 scripts/web_screenshot.py "https://example.com" --wait 3000

# 完整示例
python3 scripts/web_screenshot.py "https://example.com" --viewport mobile --wait 2000 -o /tmp/mobile.png
```

## 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `<url>` | 目标网页 URL（必填） | 任意 http/https URL |
| `--viewport, -v` | 视口类型 | mobile / tablet（默认桌面1280×720） |
| `--partial, -p` | 仅截取视口可见区域，不全页滚动 | flag |
| `--output, -o` | 输出文件路径 | 任意 .png 路径（默认 /tmp/screenshot_时间戳.png） |
| `--wait, -w` | 截图前等待毫秒数 | 数字，默认 2000ms |

## 应用场景

- 存档网页快照（新闻、公告、证据留存）
- 监测网站 UI 变化（视觉回归测试）
- 社交媒体内容预览图
- SEO 诊断（查看页面渲染后内容）
- 移动端兼容性检查

## 注意事项

- Chromium 仅支持，依赖系统已安装 Chromium
- 登录态页面（如需要 Cookie/Token）无法直接截图（可结合 browser skill）
- 超长页面（>10000px）全页截图可能较慢
- 等待时间建议 1000-3000ms（太快 JS 未渲染，太慢浪费时间）

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
