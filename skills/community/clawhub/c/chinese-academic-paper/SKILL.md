---
name: chinese-academic-paper
description: 中文课程论文综述写作与排版导出。触发词：算法综述 / 课程论文 / 作业综述 with 小四 + 宋体 + 双倍行距 + docx+pdf 输出要求；GB/T 7714 参考文献排版；学术作业类长文（约 20 页）。流程覆盖参考文献真实性核查、章节大纲、正文写作、docx+pdf 双格式导出。
version: 1.0.1
---

# 中文课程论文综述写作与排版导出

## 适用任务

高校课程作业中的「算法/技术综述」类长文，典型排版要求：
- 正文 **小四号（12pt）+ 双倍行距**
- **中文宋体**，**英文/数字 Times New Roman**
- 标题层级 **黑体**（二号 / 三号 / 小三）
- 参考文献 ≥ 20 篇（英文 ≥ 10 篇），**GB/T 7714-2015** 格式
- 长度 ≥ 20 页
- 输出 **docx + pdf** 双文件
- 文件名格式：`作业名+学号+姓名+综述名称`

## 工作流（4 步）

### Step 1：选题确认 + 参考文献真实性核查

**用户必填**：
- 选题（具体算法 / 技术方向）
- 学号 + 姓名
- 文件名（一般遵循作业模板）

**参考文献核查（学术诚信红线）**：
- 用 `web_search` 逐篇到原期刊/会议页面核验：作者、年份、期刊/会议名、卷期、页码、DOI
- 宁可少而真，不可多而假。AI 在学术写作中最常见的失败模式就是编造看起来合理的参考文献
- 建议留 5 篇以上缓冲（≥ 25 篇），覆盖：奠基论文、理论分析、改进算法、应用案例、近期综述
- 跟踪表（建议放在 `references/verification-log.md`）：

| # | 引用键 | 作者/年份 | 来源（IEEE Xplore / DOI / 期刊官网） | 状态 |

### Step 2：出大纲等用户审核

- 9 章左右标准结构（中英摘要 + 9 章正文 + 参考文献）：
  - 第 1 章 绪论（背景、综述脉络、选题意义、组织结构）
  - 第 2 章 起源 / 思想萌芽
  - 第 3 章 标准算法流程与结构
  - 第 4 章 改进研究（最长，约占 30%）
  - 第 5 章 理论分析（收敛性 / 稳定性 / 参数选择）
  - 第 6 章 应用研究
  - 第 7 章 与同类算法对比（可含对比表）
  - 第 8 章 未来发展趋势
  - 第 9 章 结论
- 字数预估 12,000-14,000 中文字符 → 20-24 页（小四双倍行距）
- **大纲必须用户确认后再写正文**

### Step 3：批量出正文

- 按大纲比例分配字数，引用 `[n]` 上标对应参考文献列表
- 数学公式：纯文本下标（`v_id`, `x_id`）足够 docx 渲染；如需 LaTeX 风格，可在 docx 中用 OOXML 嵌入 OMML（详见 references/formatting-spec.md）
- 一气呵成输出全文后再统一排版（避免来回切换格式）

### Step 4：排版导出

- 工具链：**python-docx** 生成 docx + **libreoffice (soffice --headless)** 转 pdf
- 详细字体/行距/段落规范见 `references/formatting-spec.md`
- 验证：`pdfinfo output.pdf | grep Pages` 确认页数 ≥ 20

## 关键避坑（必读）

1. **永远 web-verify 参考文献**——见 Step 1。这是 AI 学术写作的 #1 失败模式
2. **python-docx 字体必须设 OOXML `w:eastAsia`**——单纯 `run.font.name = "宋体"` 不会让中文渲染为宋体；要写到 `rFonts` 的 `eastAsia` 属性
3. **Linux 下没有宋体/SimSun**——脚本写 `宋体`，Word/WPS 打开时回退到本地可用中文字体（Linux 常用 Noto Serif CJK SC）；PDF 由 libreoffice 渲染时会用 Noto Serif CJK，效果接近
4. **页数预估**：A4 双倍行距小四约 600-700 中文字/页；20 页 ≈ 13,000 字
5. **pip 装 python-docx 用 `--break-system-packages`**——Ubuntu 24+ PEP 668 默认禁止系统级 pip，装本地：`pip install --break-system-packages --user`
6. **插图时 matplotlib 装不上就 Pillow**——matplotlib 依赖重、可能装到一半长时间无输出；Pillow (`from PIL import Image, ImageDraw, ImageFont`) 一般已装在系统，可以现成画流程图、分类树、收敛曲线等学术插图。中文字体走 `/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc`（ImageFont.truetype 直接读 .ttc 即可）。图嵌入 docx 的辅助函数见 `references/formatting-spec.md` §5.6

## 完成标准

- [ ] 用户确认选题 + 学号姓名 + 文件名
- [ ] ≥ 20 篇参考文献，每篇都有 web 核验记录（DOI 或期刊页码）
- [ ] 大纲经用户审核通过
- [ ] 正文 ≥ 12,000 中文字符
- [ ] docx + pdf 双文件
- [ ] PDF ≥ 20 页（A4）
- [ ] 字体符合（小四 + 宋体/TNR + 双倍行距）

## 参考文件

- `references/formatting-spec.md` —— 字体、行距、段落、GB/T 7714 格式、python-docx 关键代码片段、soffice 转 PDF 命令