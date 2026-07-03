---
name: fetch-zhihu-content
description: "Use when the user wants to download any Zhihu article/answer by URL — including '下载知乎文章', '抓取知乎回答', '帮我保存这篇知乎', '把这个知乎链接转成Markdown', or any request to extract content from a zhuanlan.zhihu.com or zhihu.com/question/.../answer URL. Accepts one or more Zhihu URLs and saves each as Markdown (with optional HTML). Uses Playwright to render pages and extract clean text content. Handles both zhuanlan.zhihu.com articles and zhihu.com answers."
compatibility:
  - python3
  - playwright
  - Windows: Microsoft Edge (playwright install msedge)
  - Linux: Firefox (playwright install firefox) 或 Chromium
---

# Fetch Zhihu Content

下载任意知乎文章或回答的完整正文，保存为 Markdown 文件。支持：
- **知乎专栏文章**: `https://zhuanlan.zhihu.com/p/{id}`
- **知乎回答**: `https://www.zhihu.com/question/{qid}/answer/{aid}` 或 `https://www.zhihu.com/answer/{aid}`
- **知乎问题页**: `https://www.zhihu.com/question/{qid}`

## 工作流程

### 1. 确认输入

用户提供知乎 URL 或告诉你要下载哪篇文章。

### 2. 运行抓取脚本

```bash
python <skill_dir>/scripts/fetch_zhihu_content.py [--browser auto|chromium|firefox] <一个或多个知乎URL> [输出目录]
```

示例：
```bash
# 下载一篇（Windows 默认 Edge，Linux 默认 Firefox）
python scripts/fetch_zhihu_content.py https://zhuanlan.zhihu.com/p/123456

# 指定用 Firefox
python scripts/fetch_zhihu_content.py --browser firefox https://zhuanlan.zhihu.com/p/123456

# 下载多篇
python scripts/fetch_zhihu_content.py https://zhuanlan.zhihu.com/p/123456 https://www.zhihu.com/question/789/answer/456

# 指定输出目录
python scripts/fetch_zhihu_content.py https://zhuanlan.zhihu.com/p/123456 ./output
```

### 3. 脚本行为

1. 启动 Playwright（有头模式，弹出真实浏览器窗口渲染页面）
2. 依次访问每个 URL，等待页面加载
3. 智能选择正文容器（优先 `.RichText`，依次降级尝试其他选择器）
4. 提取标题（页面标题或 document.title）
5. 保存为 `.md` 文件
6. 自动关闭浏览器

### 4. 输出格式

脚本输出到终端：
- 每个 URL 的处理结果
- 正文长度
- 保存的文件路径

保存的文件：
- **`zhihu_{类型}_{标题前40字}.md`** — 含元数据和完整正文的 Markdown

## 注意事项

1. **需要 GUI 环境**：Playwright 以 headed 模式启动真实浏览器。无 GUI 的服务器会自动使用 headless 模式。
2. **公开内容无需登录**：知乎公开文章/回答可直接抓取，无需 Cookie
3. **私密内容需要登录**：如需抓取付费内容或自己的草稿，需先准备 Cookie 文件
4. **依赖安装**：
   ```bash
   pip install playwright
   playwright install firefox    # Linux（推荐）
   playwright install msedge     # Windows
   playwright install chromium   # 备选
   ```
5. **动态加载**：知乎页面可能有懒加载内容，脚本会自动滚动页面触发加载
6. **指定浏览器**：支持 `--browser firefox` / `--browser chromium` 参数
