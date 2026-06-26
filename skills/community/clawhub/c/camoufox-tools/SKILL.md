---
name: camoufox-tools
description: Simplified CLI tools for camoufox anti-detection browser automation. Provides fox-open, fox-scrape, fox-eval, fox-close, and fox-bilibili-stats commands for easy web scraping and data extraction.
---

# camoufox-tools

🦊 封装 camoufox + agent-browser 的最佳实践，提供简化的命令行工具用于反检测浏览器自动化和数据抓取。

## 为什么需要这个 Skill？

- **反检测**: camoufox 是基于 Firefox 的防指纹浏览器，能绕过 Bilibili 等网站的风控
- **简化命令**: 隐藏复杂的 `--executable-path` 和 `--headed` 参数
- **最佳实践**: 自动处理 `close` 规范，避免资源泄漏
- **即装即用**: 一键安装，无需记忆长路径

## 安装

```bash
# 运行安装脚本，将工具添加到 PATH
cd ~/.openclaw/workspace/skills/camoufox-tools
./install.sh

# 或者手动添加到 PATH
export PATH="$HOME/.openclaw/workspace/skills/camoufox-tools/bin:$PATH"
```

## 环境变量

```bash
# 可选：自定义 camoufox 路径（默认: ~/.local/share/camoufox/camoufox）
export CAMOUFOX_PATH=/path/to/camoufox
```

## 工具列表

### 1. fox-open - 有头模式打开网页

使用 camoufox 有头模式打开指定网页。

```bash
fox-open "https://example.com"
fox-open "https://bilibili.com"
```

**特性:**
- 自动关闭之前的 browser 实例
- 自动使用 `--headed` 模式
- 自动填充 camoufox 路径

---

### 2. fox-scrape - 抓取页面内容

抓取网页内容，支持等待时间和 CSS 选择器。

```bash
# 基本用法
fox-scrape "https://example.com"

# 等待 5 秒后抓取
fox-scrape "https://example.com" --wait 5000

# 抓取特定元素
fox-scrape "https://example.com" --selector ".article-content"

# 短选项
fox-scrape "https://example.com" -w 5000 -s ".content"
```

**选项:**
- `-w, --wait <ms>` - 等待时间（毫秒，默认 3000）
- `-s, --selector <sel>` - CSS 选择器，提取特定元素

**特性:**
- 自动启动 browser（如未运行）
- 任务完成后自动关闭 browser

---

### 3. fox-eval - 执行 JavaScript

在当前页面执行 JavaScript 代码。

```bash
# 获取页面标题
fox-eval "document.title"

# 获取元素文本
fox-eval "document.querySelector('.like-btn').textContent"

# 获取多个元素
fox-eval "[...document.querySelectorAll('.stat')].map(e => e.textContent)"
```

**注意:** 需要先使用 `fox-open` 打开网页。

---

### 4. fox-close - 规范关闭

关闭所有 browser 实例，释放资源。

```bash
fox-close
```

**建议:** 在每个任务完成后执行，避免资源占用。

---

### 5. fox-bilibili-stats - 获取 B 站视频数据

获取 Bilibili 视频的统计数据。

```bash
fox-bilibili-stats "BV1NGZtBwELa"
fox-bilibili-stats "BV1xx411c7mD"
```

**输出:**
- 📺 视频标题
- ▶️  播放量
- 👍 点赞数
- 🪙 投币数
- ⭐ 收藏数
- 📤 分享数
- 💬 弹幕数

**特性:**
- 自动处理 BV 号格式
- 自动启动和关闭 browser

---

## 典型工作流

### 工作流 1: 快速查看网页
```bash
fox-open "https://example.com"
# 查看完成后
fox-close
```

### 工作流 2: 抓取动态内容
```bash
fox-scrape "https://example.com" --wait 5000 --selector ".dynamic-content"
```

### 工作流 3: 交互式数据提取
```bash
# 打开页面
fox-open "https://example.com"

# 执行一些操作后提取数据
fox-eval "document.querySelector('.data').textContent"

# 关闭
fox-close
```

### 工作流 4: B 站视频数据分析
```bash
fox-bilibili-stats "BV1NGZtBwELa"
```

---

## 故障排除

### Browser 无法启动
- 检查 camoufox 是否已安装: `ls ~/.local/share/camoufox/camoufox`
- 设置正确的路径: `export CAMOUFOX_PATH=/path/to/camoufox`

### 页面加载超时
- 增加等待时间: `fox-scrape --wait 10000`
- 检查网络连接

### 选择器找不到元素
- 使用 `fox-open` 打开页面后手动检查元素
- 使用 `fox-eval` 测试选择器: `fox-eval "document.querySelector('.your-selector')"`

---

## 依赖

- openclaw CLI
- camoufox (headless Firefox)
- agent-browser 扩展

---

## 许可证

MIT
