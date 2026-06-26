# export_pdf.js 使用指南

## 工作原理

```
HTML → Puppeteer 按 selector 截图 → 等比缩放 → 合成 PDF
```

脚本流程：
1. 启动 headless Chrome，加载 HTML（`deviceScaleFactor: 2` 高清）
2. 遍历 SELECTORS，用 `getBoundingClientRect` 获取真实尺寸
3. 截图 → 生成临时 slide HTML（黑底居中）→ 截图为 1440×900 PNG
4. 所有 PNG 合成为横向 PDF

## 关键参数

```js
const W = 1440, H = 900;  // 幻灯片尺寸（px），可调整

const SELECTORS = [
  '.cover',
  '.section-2',
  ['.chart', '.stats'],  // 数组 = 合并为一页
];
```

## 运行方式

```bash
# 默认读取 slides.html，输出 slides.pdf
node export_pdf.js

# 指定 HTML 文件（输出自动同名）
node export_pdf.js my-deck.html
```

## 调试技巧

**查看每页实际尺寸**：脚本会打印 `(宽x高 → scale=X.XX)`，scale < 1 说明内容超高，考虑拆分

**跳过某页**：注释掉对应 selector

**只生成某几页**：临时只保留需要的 selector 测试

## 依赖

- Node.js 18+
- puppeteer（`npm install puppeteer`）

## ⚠️ 重要：Detached Frame 陷阱

脚本使用 **复用 overlayPage** 方案（全程只有一个辅助页面）。

**不要**改为 `browser.newPage()` / `p2.close()` 循环——新版 Puppeteer 会报 `Attempted to use detached Frame` 错误。

## 输出

- 输出文件：与输入 HTML 同名（扩展名改为 `.pdf`）
- 临时文件 `_pdf_pages/` 自动清理
