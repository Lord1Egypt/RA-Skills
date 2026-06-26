---
name: html-to-pdf
description: 用 Puppeteer + 已安装的 Chrome/Chromium 将 HTML 渲染为纯中文 PDF。自动处理 ECharts 等待、Tab 展开、淡入动画、内容测高、白边消除、防分页。适用：看板/报表/网页转 PDF、中文 PDF、交互图表转 PDF。
metadata:
  version: "1.0.4"
  updated: "2026-05-20"
  owner: "Ronie"
---

<!-- 🦞 fanzhi-provenance -->
> **ContentID**: `fz:skill:2f8e9a7c:wsl_lobster:mpc2j3a6`
> **Version**: 1.0.3 | **License**: MIT-0 (ClawHub)
> **Owner**: 泛智生态 / Ronie & 泛智小龙虾
> **Provenance**: wsl_lobster 初次生成，v1.0.4 ClawHub 发布前优化
> **Note**: 本 Skill 依赖本机已安装的 Chromium，不含浏览器包

# html-to-pdf — HTML 页面转 PDF

## 用法

```bash
# 基本（PDF 输出到 HTML 同目录）
node scripts/html-to-pdf.mjs report.html

# 指定输出路径
node scripts/html-to-pdf.mjs input.html /tmp/output.pdf

# 指定 Chromium 路径
CHROME_PATH=/usr/bin/chromium node scripts/html-to-pdf.mjs input.html
```

## 不适合此技能的场景

- ❌ 需要 PDF 文本可选中/可搜索（PDF 内容是图片级的）
- ❌ HTML 依赖跨域 CDN 资源且网络不通
- ❌ 页面需要用户交互才能展示内容（如点击"加载更多"）
- ❌ 需要 A4 标准分页布局（如打印排版文档）

## 步骤

```
Step0: 渲染页面 + 等 JS 图表完成
Step1: 展开隐藏内容（.tc tab / .fi 淡入 / 折叠面板）
Step2: 测高度 + 底部 2px 实体 DOM（底色自动检测）
Step3: overflow:hidden 防 Chromium 额外分页 → PDF 生成
Step4: pdf-lib 验证页数
```

### Step0 — 渲染

等待 `networkidle0`，检测 canvas（ECharts）全部完成后再等 2 秒确保动画。

### Step1 — 展开

Headless 模式下 `IntersectionObserver` 不触发视口外元素。手动展开所有隐藏内容：

| 隐藏模式 | CSS | 修复手段 |
|---------|-----|---------|
| Tab 内容 | `.tc { display: none }` | 加 `.act` class |
| 淡入动画 | `.fi { opacity: 0; transform: translateY(...) }` | 加 `.sho` class |
| 折叠面板 | `display: none` | `style.display = ''` |

### Step2 — 白边消除

Chromium PDF 渲染器底层有白色画布。DOM 内容与页面高度有 1px 缝隙时画布透出。

**修复**：底部加 2px 实体 `<div>`，背景色自动检测（`--bg` CSS 变量 → computedStyle → 白色）。

### Step3 — 防分页 + 生成

Chromium 对超长页面会切割出空白第二页。**修复**：生成前注入 `overflow: hidden`。

### Step4 — 验证

输出示例：

```
✅ report.pdf (1288.7 KB)
   PDF 页数: 1
   页1: 1050 x 3001 pt
```

> 预期 1 页，>1 页表示有内容未展开或分页策略需调整。

## 依赖

```bash
npm install puppeteer-core pdf-lib
```

| 依赖 | 用途 |
|------|------|
| `puppeteer-core` | 浏览器控制（不含 Chromium 下载） |
| `pdf-lib` | PDF 页数验证 |

## Chromium

脚本自动检测当前平台，也可通过环境变量覆盖：

```bash
# macOS：自动定位 /Applications/Google Chrome.app/...
# Linux/WSL：自动定位 /opt/chrome-linux/chrome
# 手动指定
CHROME_PATH=/usr/bin/chromium node scripts/html-to-pdf.mjs input.html
```

各平台路径备忘 → [references/platforms.md](references/platforms.md)

> snap 版 Chromium 因沙箱隔离不可直接使用。

## 中文字体

本机需安装中文字体，否则 PDF 中文显示为方块。

**方法 A：从 Windows 复制（WSL 环境）**

```bash
mkdir -p ~/.fonts
cp "/mnt/c/Windows/Fonts/Noto Sans SC (TrueType).otf" ~/.fonts/
cp "/mnt/c/Windows/Fonts/msyh.ttc" ~/.fonts/
cp "/mnt/c/Windows/Fonts/seguiemj.ttf" ~/.fonts/
fc-cache -f -v ~/.fonts/
```

**方法 B：直接下载 Noto Sans CJK**

```bash
mkdir -p ~/.fonts && cd ~/.fonts
wget -O NotoSansSC.ttf "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf"
wget -O NotoEmoji.ttf "https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoEmoji-Regular.ttf"
fc-cache -f -v ~/.fonts/
```

## 故障排查

| 现象 | 可能原因 | 修复 |
|------|---------|------|
| `net::ERR_INVALID_URL` | 相对路径 | 传完整路径或用 `$(pwd)/` 前缀 |
| 第二页空白 | Chromium 内部分页 | 检查 `overflow:hidden` 注入  |
| 中文方块 | 缺少中文字体 | 执行"中文字体"节操作 |
| emoji 方块 | 缺少 emoji 字体 | 安装 Noto Emoji / Segoe UI Emoji |
| 底部 1px 白边 | 白色画布透出 | 确认 filler div 已注入且底色匹配 |
| ECharts 空框架 | 渲染中改动了 body 样式 | 用 `addStyleTag` 而非直接改 DOM |

## 首次验证

```bash
# 用任意本地 HTML 测试
node scripts/html-to-pdf.mjs path/to/your.html
# 或者生成一个简单测试文件
echo '<h1>你好世界 🦞</h1>' > /tmp/test.html
node scripts/html-to-pdf.mjs /tmp/test.html
```

## 安全性

- ✅ **输入校验**：路径含 `<>"|?*` 等特殊字符 × 拒绝；仅允许 `.html` / `.htm` 文件
- ✅ **输出安全**：指定输出路径时，仅在 HOME / /tmp / 当前目录下允许写入
- ✅ **异常安全**：try/catch/finally 确保浏览器正确关闭，不泄露进程
- ⚠️ **`--no-sandbox`**：单用户环境安全；多租户部署需移除

## 许可与来源

**直接引用**：puppeteer-core（Apache-2.0）+ pdf-lib（MIT），通过 npm import 调用 API，不修改上游代码。

**方案参考**：jsPDF / pdfmake / HTMX / Pico.css / mini.css（仅调研，未引用代码）。

完整许可声明 → [references/sources.md](references/sources.md)

## 已知问题

- CDN 资源（cdn.jsdelivr.net 等）需网络连通，可替换为本地
- 无限滚动/懒加载不会自动触发，需在 Step1 中手动处理
