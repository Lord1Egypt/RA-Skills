---
name: fetch-wechat-article
description: >
  使用 Playwright headed 模式 + 真实系统浏览器抓取微信公众号文章。
  当用户给出 mp.weixin.qq.com 链接、说要抓取/下载公众号文章、
  或遇到"环境异常"验证页时，必须使用本技能。
  本技能会弹出真实浏览器窗口绕过微信反爬，提取文章标题、作者、正文，
  并同时保存 .md 和 .html 两种格式。
  不依赖微信登录态，所有公众号公开文章都可抓取。
compatibility:
  - python3
  - playwright (pip install playwright)
  - Windows: Edge (playwright install msedge)
  - Linux: Firefox (playwright install firefox) 或 Chromium
---

# Fetch WeChat Article

抓取微信公众号文章的专用技能。在 headed 模式下使用系统安装的 Edge 浏览器，真实渲染页面来绕过微信的反爬检测（headless 模式会被"环境异常"页面拦截）。

## 工作流程

### 1. 确认输入

用户提供微信公众号文章链接，格式通常为：
- `https://mp.weixin.qq.com/s/xxx`（短链接）
- `https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx&...`（长链接，带追踪参数）

两种都可以直接使用，但优先使用短链接（长链接中的 `sharer_shareinfo` 等追踪参数不影响抓取）。

### 2. 运行抓取脚本

```bash
python <skill_dir>/scripts/fetch_wechat_article.py [--browser auto|chromium|firefox] <文章URL> [输出目录]
```

脚本会：
1. 自动检测平台（Windows → Edge / Linux → Firefox），弹出真实浏览器窗口
2. 注入反检测脚本（覆盖 `navigator.webdriver`）
3. 加载文章 URL，等待内容渲染
4. 监控是否被拦截（"环境异常"关键词），每 2 秒检查一次，最多等 30 秒
5. 提取标题、作者、正文
6. 保存 `.md` 和 `.html` 到输出目录
7. 关闭浏览器

> **Linux 用户提示**：默认使用 Firefox，如想用 Chromium 可加 `--browser chromium` 参数。
> 无图形界面的服务器会自动启用 headless 模式。

### 3. 输出格式

脚本输出到终端：
- 加载过程中的 URL 状态
- 最终保存的文件路径

保存的文件：
- **`wechat_标题_时间戳.md`** — 结构清晰的 Markdown 文件，含标题、作者、时间、正文
- **`wechat_标题_时间戳.html`** — 带干净排版的 HTML 页面，可直接浏览器打开查看

### 4. 向用户汇报

抓取完成后，告知用户保存的文件路径和基本信息：
- 文章标题
- 作者
- 正文长度

## 注意事项

1. **需要 GUI 环境**：本技能依赖图形桌面，Playwright 以 headed 模式启动真实浏览器。无 GUI 的服务器环境无法使用。
2. **Edge/Chromium 需要安装**：首次使用需确保安装了 Playwright 浏览器：`playwright install msedge` 或 `playwright install chromium`
3. **浏览器窗口会弹出**：用户会看到 Edge 浏览器窗口短暂打开并自动关闭，这是正常现象。
4. **文章必须公开**：只能抓取公众号公开发布的文章，付费/限制访问的文章无法获取。
5. **依赖安装**：首次使用需要确保 Python 依赖齐全：
   ```bash
   pip install playwright
   playwright install msedge
   ```
