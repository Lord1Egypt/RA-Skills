# Formula-PDF 📄

**MathJax + Headless Edge → 完美公式PDF**

告别Word公式乱码，拥抱真正的数学排版。写HTML，加LaTeX公式，一键转PDF。

---

## 为什么选 Formula-PDF？

| 问题 | 解决方案 |
|------|----------|
| Word公式变图片/乱码 | ✅ 真正的矢量数学符号 |
| 截图公式模糊 | ✅ 高清可缩放 |
| LaTeX编译太复杂 | ✅ 只需要HTML+CDN |
| Markdown渲染公式有限 | ✅ 完整LaTeX命令支持 |

**公式渲染效果：** $e^{i\pi} + 1 = 0$ ✓ 真正渲染，不是图片

**科研必备场景：**
- 课程报告 / 实验报告
- 学术笔记 / 复习资料
- 试卷 / 习题解答
- 论文初稿排版
- 技术文档含公式

**可视化优势：**
- 所见即所得——HTML里长啥样，PDF里就长啥样
- 公式、表格、代码块、图片混排
- 支持所有标准LaTeX数学环境（cases、matrix、align等）

## 快速开始（60秒）

### 1. 写一个带公式的HTML

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
</head>
<body>
    <h1>二次方程求根公式</h1>
    <p>$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$</p>
</body>
</html>
```

### 2. 一键转换

```powershell
# 手动
& 'edge' --headless=new --virtual-time-budget=30000 --print-to-pdf="output.pdf" --no-margins "file:///C:/path/to/input.html"

# 或用脚本
python scripts/html_to_pdf.py input.html -o output.pdf --verify
```

### 3. 🎉 完成

打开 `output.pdf`——公式已是真正的数学符号，可复制、可搜索、高清打印。

## 目录

```
formula-pdf/
├── SKILL.md                    # AI技能配置
├── README.md
├── scripts/
│   ├── html_to_pdf.py          # 基础转换脚本
│   └── html_to_pdf_enhanced.py # 增强版（重试+验证）
├── assets/
│   └── template.html           # HTML模板
└── references/
    └── lessons_learned.md      # 踩坑记录
```

## 公式语法速查

使用标准 LaTeX 数学语法，MathJax 自动渲染：

| 效果 | 写法 |
|------|------|
| 行内 | `$E = mc^2$` |
| 块级 | `$$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$$` |
| 方程组 | `$$\begin{cases} x+y=1 \\ x-y=0 \end{cases}$$` |
| 矩阵 | `$$\begin{pmatrix} a & b \\ c & d \end{pmatrix}$$` |
| 求和 | `$$\sum_{i=1}^{n} i^2$$` |
| 积分 | `$$\int_{a}^{b} f(x)dx$$` |

## 技术原理

```
HTML (含LaTeX公式)
       ↓
  MathJax CDN (渲染为数学符号)
       ↓
Edge Headless (虚拟计时等待渲染完成)
       ↓
  PDF (矢量数学符号)
```

## 常见问题

**公式显示为代码？** → 加长等待时间：`--virtual-time-budget=60000`

**中文乱码？** → CSS加字体：`font-family: 'Microsoft YaHei', serif;`

**PDF没生成？** → 检查Edge路径和文件URL格式

**公式不可复制？** → 使用 `tex-svg.js` 替代 `tex-chtml.js`

## 依赖

- Windows + Microsoft Edge
- Python 3（脚本用）
- pymupdf（验证用，可选）

## 许可证

MIT
