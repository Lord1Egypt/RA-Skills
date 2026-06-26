# ================================
# fanzhi-provenance: fz:skill:4e1b5585:wsl_lobster:mpc2j3a6
# project: html-to-pdf v1.0.4
# content-hash: 4e1b5585
# license: MIT-0 (ClawHub)
# copyright: 泛智生态 / Ronie & 泛智小龙虾
# fanzhi-signature: (Phase 3)
# ================================

# HTML → PDF 技术原理参考

## 核心链路

```
HTML 页面
  ↓ puppeteer
渲染到 Chromium（headless）
  ↓ page.goto + waitForCanvas + 2s 等待
完整渲染状态
  ↓ Step1: 展开 tab / 淡入 / 折叠
展开后的页面
  ↓ Step2: 测量 + 2px filler
精确的页面高度
  ↓ Step3: overflow:hidden
防切割
  ↓ Step4: page.pdf()
PDF 输出
  ↓ pdf-lib 验证
确认页数
```

## 为什么 Chromium PDF 优于 jsPDF / pdfmake

| 特性 | Chromium PDF | jsPDF | pdfmake |
|------|-------------|-------|---------|
| 中文原生 | ✅ 安装字体即可 | ❌ 需 TTF 子集化 | ❌ 需 TTF |
| ECharts 支持 | ✅ 原生渲染 | ❌ 需 html2canvas | ❌ 不支持 |
| 交互页面 | ✅ 可展开 tab/动画 | ❌ 静态 PDF | ❌ 静态 PDF |
| 输出质量 | 截图级 | 低（矢量但排版简陋） | 中 |
| 文件大小 | ~300KB-2.6MB | ~500KB | ~500KB |

## Chromium PDF 渲染器的三层结构

```
层3: CSS 内容层 → 渲染 HTML/CSS/图表 ✅
层2: DOM 元素层 → 可编程注入 filler ✅
层1: 白色 PDF 画布 → Chromium 内部默认层 ❌
```

1px 白边 = 层2 比 层3 短 1px → 层1 的白色透出

**解决方案**：在层2 底部加 2px 的实体 DOM 元素（有背景色），使层2 完全覆盖层1。

## 隐藏内容模式大全

| 隐藏方式 | CSS | 激活方式 | 场景 |
|---------|-----|---------|------|
| `display: none` | 元素不占空间 | 加 class 或设 style | Tab 切换、折叠面板 |
| `opacity: 0` | 元素占空间但透明 | 加 `.sho` / `opacity: 1` | IntersectionObserver 淡入 |
| `visibility: hidden` | 元素占空间但不可见 | `visibility: visible` | 过渡动画 |
| `clip/clip-path` | 裁剪到 0 | 移除裁剪规则 | 滚动动画 |
| `max-height: 0` | 高度折叠 | 设 `max-height: n` | 手风琴菜单 |

headless 模式下，IntersectionObserver 不触发视口外元素，需手动激活所有 `opacity: 0` 内容。

## Chromium 分页机制

Chromium 对超过内部限制的页面会自动切割。表现为：
- 第一页正常（有内容）
- 后续页空白

**修复**：在生成 PDF 前注入 `overflow: hidden` CSS。

## 验证方案

生成 PDF 后，用 pdf-lib 打开并检查：

```javascript
import { PDFDocument } from 'pdf-lib';
const doc = await PDFDocument.load(pdfBuffer, { ignoreEncryption: true });
console.log('页数:', doc.getPageCount());
console.log('尺寸:', doc.getPage(0).getSize());
```
