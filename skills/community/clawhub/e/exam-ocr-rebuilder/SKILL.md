---
name: exam-ocr-rebuilder
version: 1.0.2
description: "Exam paper OCR rebuilder with LLM audit. Supports 11 question types, tencent-docs OCR integration, and interactive HTML report generation. Triggers: 试卷OCR, 试卷识别, 试卷重建, 试卷录入, PDF试卷, exam OCR, exam paper rebuild"
description_zh: "试卷OCR重建助手。上传试卷PDF或图片，自动OCR识别内容，AI分类题型、提取结构，LLM审核校正，重建为可编辑的新试卷。支持11种题型，输出HTML/JSON/Markdown格式。"
user-invocable: true
argument-hint: "上传试卷PDF文件或试卷图片，支持多页"
tags:
  - ocr
  - exam
  - education
  - ai
  - productivity
---

# 试卷OCR重建助手

你是一位专业的试卷数字化工程师。你的任务是将PDF或图片格式的试卷，通过OCR识别+AI结构化解析+**LLM审核校正**，重建为清晰、可编辑的新试卷。

## 处理流程总览

```
输入（PDF/图片）
  ↓
[第一步] PDF转图片（如需要）
  ↓
[第二步] OCR文字识别（tencent-docs OCR / 本地PaddleOCR）
  ↓
[第三步] AI结构化解析（题型分类、题干/选项/答案提取、LaTeX公式转换）
  ↓
[第四步] LLM大模型审核检查（校正OCR错误、补全截断内容、修正LaTeX公式）
  ↓
[第五步] 生成输出（HTML交互报告 + JSON + Markdown）
  ↓
[第六步] （可选）创建腾讯文档在线编辑版
```

## 输入识别

根据输入类型走不同路径：

### 路径A：PDF文件
1. 使用 `scripts/pdf_to_images.py` 将PDF逐页转换为高清图片
2. 对每页图片执行OCR识别
3. 合并所有页面文本后进入结构化解析

### 路径B：图片文件（jpg/png/bmp等）
1. 直接对图片执行OCR识别
2. 如果有多张图片，按顺序合并文本

### 路径C：图片URL
1. 使用 tencent-docs OCR `ocr.extract` 直接识别URL图片
2. 无需下载到本地

## 处理流程

### 第一步：PDF转图片（仅PDF输入时）

运行辅助脚本将PDF转为图片：

```bash
python "scripts/pdf_to_images.py" --input "试卷.pdf" --output_dir "temp_pages" --dpi 300
```

脚本依赖 PyMuPDF（fitz），安装命令：
```bash
pip install PyMuPDF -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

输出：每页一个PNG文件，命名格式 `page_001.png`, `page_002.png`, ...

### 第二步：OCR文字识别

**优先方案：tencent-docs OCR（已连接）**

对每张图片调用 `mcp__tencent-docs__ocr.extract`：
- `extract_type`: "accurate"（高精度模式）
- `image_base64` 或 `image_url`：图片数据
- `with_positions`: true（保留位置信息，辅助结构分析）

将每页OCR结果按页码顺序合并为完整文本。

**备选方案1：tencent-docs `ocr.toword`**
- 一次性传入1-9张图片，直接生成在线Word文档
- 适合快速出文档，但结构化程度较低

**备选方案2：PDF直接导入腾讯文档**
- 使用 `manage.pre_import` → 上传文件 → `manage.async_import` → `manage.import_progress` 轮询
- 导入完成后使用 `get_content` 读取文本
- 适合扫描版PDF的快速文本提取

### 第三步：AI结构化解析

将OCR识别的完整文本，使用LLM进行结构化解析。解析时遵循以下规则：

#### 题型识别标准

按照 [题型分类标准](references/question-types.md) 识别以下题型：

| 题型代码 | 中文名称 | 识别特征 |
|---------|---------|---------|
| single_choice | 单项选择题 | A/B/C/D选项，单一答案 |
| multi_choice | 多项选择题 | A/B/C/D/E选项，多个答案 |
| true_false | 判断题 | 对/错、正确/错误、T/F |
| fill_blank | 填空题 | 下划线___、括号()留空 |
| short_answer | 简答题 | "简述""简要说明" |
| calculation | 计算题 | "计算""求解""求" |
| essay | 论述题 | "论述""分析""谈谈" |
| reading | 阅读理解 | 材料+多小题 |
| cloze | 完形填空 | 文章+编号空格 |
| proof | 证明题 | "证明""求证" |
| other | 其他题型 | 不属于以上类型 |

#### 解析JSON结构

每道题解析为以下JSON结构：

```json
{
  "exam_info": {
    "title": "试卷标题",
    "subject": "学科",
    "total_score": 100,
    "duration": "120分钟",
    "source": "来源信息"
  },
  "sections": [
    {
      "section_id": 1,
      "section_title": "一、单项选择题",
      "section_type": "single_choice",
      "section_score": 40,
      "questions": [
        {
          "question_id": 1,
          "type": "single_choice",
          "score": 2,
          "stem": "题干文本",
          "options": {
            "A": "选项A内容",
            "B": "选项B内容",
            "C": "选项C内容",
            "D": "选项D内容"
          },
          "answer": "B",
          "explanation": "解析说明（如有）",
          "image_refs": [],
          "latex_formulas": []
        }
      ]
    }
  ],
  "stats": {
    "total_questions": 0,
    "type_distribution": {},
    "total_score": 0
  }
}
```

#### 解析要点

1. **题号识别**：用正则 `^\d+[\.．、]` 识别题号，支持阿拉伯数字和中文数字
2. **选项识别**：匹配 `^[A-Z][\.．、)]` 识别选项
3. **分值提取**：匹配 `（\d+分）`、`(\d+分)`、`每小题\d+分`
4. **公式处理**：将OCR识别的数学公式转为LaTeX格式，用 `$...$` 包裹
5. **图片引用**：OCR中标注的图片区域，记录位置信息
6. **答案分离**：如果试卷含答案，将答案单独存入answer字段；如果不含答案，answer为null
7. **阅读理解/完形填空**：材料文本存入material字段，各小题存入questions数组

### 第四步：LLM大模型审核检查（OCR质量保障）

OCR识别存在错字、漏字、公式识别不准等问题。本步骤用LLM对结构化解析结果进行逐题审核校正。

#### 审核策略

将结构化JSON中的题目分批送入LLM，与原始OCR文本和原始图片（如有）进行比对校正。

**审核维度（共8项）**：

| 维度 | 检查内容 | 校正动作 |
|------|---------|---------|
| 题干完整性 | 题干是否截断、缺字 | 对照OCR原文补全 |
| 字符错误 | 错别字、同音字（如"设"识别为"没"） | 根据上下文纠正 |
| 数字错误 | 数字识别错误（如"0"识别为"O"） | 结合数学逻辑校正 |
| 公式LaTeX | LaTeX公式是否准确反映原题 | 重新生成正确LaTeX |
| 选项完整性 | 选项是否缺失、错位 | 对照OCR原文补全选项 |
| 题号连续性 | 题号是否跳号、重复 | 修正题号顺序 |
| 答案正确性 | 答案是否与题目匹配 | 如答案明显错误则标注warning |
| 题型一致性 | 题型分类是否正确 | 修正题型标签 |

#### 审核Prompt模板

使用 [LLM审核Prompt模板](references/llm-audit-prompt.md) 作为审核指令。

#### 审核流程

```
输入：
  - questions_batch: 一批题目（建议每批5-10题）
  - ocr_raw_text: 对应区域的OCR原始文本
  - original_image_base64（可选）: 对应区域的图片

处理：
  1. 将题目JSON + OCR原文 + 图片（可选）一起送入LLM
  2. LLM逐题对比，输出校正后的题目JSON
  3. 同时输出每题的 audit_note（审核说明），格式：
     {"question_id": 1, "status": "corrected", "issues": ["题干缺字已补全", "LaTeX公式修正"], "confidence": "high"}
     status 枚举：ok（无需修改）/ corrected（已修正）/ warning（存疑，需人工复核）/ error（无法处理）
  4. 置信度 confience 枚举：high / medium / low

输出：
  - audit_results: 审核后的题目JSON数组
  - audit_log: 每题的审核记录数组
```

#### 审核后处理

- **status=ok**：直接使用
- **status=corrected**：使用校正后内容，在HTML报告中标注"已校正"标记
- **status=warning**：在HTML报告中标注"需复核"警告，高亮显示
- **status=error**：保留原始OCR结果，标注"识别失败"

#### 审核报告

在最终HTML报告中新增"审核报告"面板，显示：
- 总题目数 / 无需修改 / 已校正 / 需复核 / 识别失败 的统计
- 逐题审核说明（可展开查看）
- 置信度分布图

### 第五步：生成输出

按照 [输出模板](references/output-template.md) 生成以下文件：

#### 1. HTML交互式报告（主要输出）

生成包含以下功能的HTML报告：
- **试卷预览**：按原试卷结构展示所有题目
- **题型筛选**：点击题型标签筛选显示
- **答案切换**：显示/隐藏答案开关
- **统计面板**：题型分布、分值统计、题目数量
- **导出功能**：一键复制为Markdown、导出JSON
- **搜索功能**：按关键词搜索题目

HTML模板要点：
- 使用内联CSS，无外部依赖
- 响应式布局，支持手机查看
- 答案默认隐藏，点击切换
- 题型标签可点击筛选
- 数学公式使用 KaTeX 渲染（CDN加载）

#### 2. JSON结构数据

将第三步的解析结果保存为 `exam_data.json`，可直接导入题库系统。

#### 3. Markdown试卷

生成Markdown格式的试卷文本，格式参考：

```markdown
# {试卷标题}

**学科**：{学科}  **总分**：{总分}  **时间**：{考试时间}

---

## 一、单项选择题（共{N}题，每题{M}分）

**1.** {题干文本}

A. {选项A}
B. {选项B}
C. {选项C}
D. {选项D}

<details>
<summary>答案</summary>
{答案}
</details>

---
```

### 第六步（可选）：创建腾讯文档

如果用户需要在线可编辑的Word文档：

1. 使用 `mcp__tencent-docs__manage.create_file` 创建新文档
2. 使用 `mcp__tencent-docs__doc.insert_markdown` 逐段插入试卷内容
3. 或使用 `mcp__tencent-docs__doc.insert_html_content` 插入富文本

## 质量检查

完成后对照以下检查清单验证：

### OCR识别质量
- [ ] 所有页面OCR识别完成，无遗漏
- [ ] 文字识别准确率检查（抽样对比原图）

### LLM审核质量
- [ ] LLM审核步骤已执行，无跳过
- [ ] 审核日志（audit_log）已生成
- [ ] status=warning 的题目已人工复核（或标注待复核）
- [ ] status=error 的题目已检查原因

### 结构化解析质量
- [ ] 题型分类正确，无误分类
- [ ] 题号连续，无跳号
- [ ] 选项完整，无截断
- [ ] 数学公式正确转为LaTeX（经LLM审核校正）
- [ ] 答案与题目正确对应（如有答案）
- [ ] 分值统计正确

### 输出质量
- [ ] HTML报告交互功能正常（题型筛选、答案切换、审核报告面板）
- [ ] JSON格式合法，可被解析
- [ ] Markdown格式可读
- [ ] 审核报告面板数据准确

## 常见问题处理

### OCR识别不清晰
- 提高PDF转图片的DPI（300→400）
- 使用 `extract_type: "accurate"` 高精度模式
- 对模糊区域单独放大处理

### 题型混淆
- 多选题与单选题：检查题干是否有"多选""至少两个"等关键词
- 填空题与简答题：根据空格数量和位置判断
- 计算题与证明题：题干动词"计算"vs"证明"

### 跨页题目
- 合并相邻页面末尾和开头的文本
- 检查题号连续性

### 表格题
- 使用 `ocr.toexcel` 单独识别表格区域
- 表格内容转为HTML table格式

## If Connectors Available

### tencent-docs（已连接）
- `ocr.extract`: 单图OCR识别（高精度模式）
- `ocr.toword`: 多图直接生成Word文档
- `ocr.toexcel`: 表格识别为在线表格
- `manage.pre_import` + `manage.async_import`: PDF直接导入
- `doc.create_with_markdown`: 从Markdown创建Word文档
- `doc.insert_html_content`: 插入富文本内容

### LLM审核模型选择
审核步骤使用当前会话的LLM（即你自身）。如需更高精度，可在Prompt中要求：
- "请特别注意数学公式的准确性"
- "请对照OCR原文逐字校对"
- 对公式密集的试卷，建议分批审核（每批3-5题）

### 如果没有连接器
- 使用 Python PaddleOCR 进行本地OCR识别
- 使用 PyMuPDF 直接提取PDF文本（仅限文本PDF）
- LLM审核步骤仍可使用（本地OCR结果 + LLM推理能力）
- 生成HTML/JSON/Markdown到本地文件
