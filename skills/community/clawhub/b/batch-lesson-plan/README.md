# batch-lesson-plan

> 把一份《授课计划 / 教学进度表》自动转成整学期、整本教材的中专教案（Word `.docx`）。
> 适用于某某A 老师《单片机原理与应用》XX电子1 等同类任务；其他课程 / 教师可替换字段复用。

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Python ≥ 3.10](https://img.shields.io/badge/python-≥3.10-blue.svg)]()

## 它做什么

1. 读授课计划（`.doc` / `.docx`） → 解析成"课次—课时—主题"清单
2. 读教材 **扫描版 PDF**（无文字层）→ 按章节页码逐页渲染成图、多模态取原文
3. 按用户规则写每课的内容 JSON
4. 用现成的中专教案模板（15 行表格）填充 → 生成 `.docx`
5. 自动结构校验（行数 / 单元格数 / vMerge）

已验证：单学期 **39 份 / 100 课时** 连续生成全部通过校验，平均单份生成 < 30 秒。

## 仓库内容

```
.
├── SKILL.md                  # WorkBuddy/Claude 技能说明（含完整工作流）
├── tools/
│   └── fill_lesson_plan.py   # JSON → docx 填充工具（保留 vMerge、含结构校验）
├── examples/
│   └── 01_sample_first_lesson.json   # 一份已写好的内容 JSON 示例
├── README.md                 # 本文件
├── LICENSE                   # Apache-2.0
└── .gitignore
```

## 快速开始

### 1. 准备环境

- Python ≥ 3.10
- 第三方库：
  ```bash
  pip install pymupdf lxml pillow
  ```
- 中专教案模板 `templates/中专教案模板.docx`（含 15 行表格，vMerge 已布置）
  - 模板可在 WorkBuddy 配套技能 `zhongshan-lesson-plan` 中找到
  - 或自行准备一只同结构的 `.docx` 模板

### 2. 解析授课计划

授课计划通常含「周次 | 章节名称及主要内容 | ... | 授课节数」四列。本技能已固化的提取规则（其他课程应先与作者确认）：

| 规则 | 说明 |
|---|---|
| 数字行才出教案 | 「授课节数」列有阿拉伯数字的行才生成教案 |
| 课时数取数字 | 2/4 等数字即为课时数 |
| 主题取原文 | 取「章节名称及主要内容」列原文 |
| 连续重复合并 | 同一主题（含"任务X-N 修改"）连续出现 → 合并为一份 |
| 期末不计入 | 期末考试 4 课时不计入总课时 |
| 复习只出一份 | "课程复习"只生成 1 份通用复习课教案 |
| 版本按计划 | 教材版本按授课计划表填，内容以资料库 PDF 为准 |

### 3. 写内容 JSON

每份教案一个 JSON，字段参考 `examples/01_sample_first_lesson.json`：

```json
{
  "teacher": "某某A",
  "course": "单片机原理与应用",
  "textbook": "《单片机应用技术》（C语言版）第4版",
  "class": "XX电子1",
  "topic": "1.1.1 认识单片机，1.1.2 单片机内部结构",
  "hours": 2,
  "knowledge": "...",
  "ability": "...",
  "quality": "...",
  "key_points": "...",
  "process": "..."
}
```

### 4. 填充为 docx

```bash
# 模式 A：传模板，自动分析结构（推荐）
python tools/fill_lesson_plan.py \
  examples/01_sample_first_lesson.json \
  output_lesson_01.docx \
  我的教案模板.docx

# 模式 B：先用 --analyze 导出结构描述（脚本分析模板的表格 + vMerge）
python tools/fill_lesson_plan.py --analyze 我的教案模板.docx > structure.json
python tools/fill_lesson_plan.py \
  examples/01_sample_first_lesson.json \
  output_lesson_01.docx \
  --structure structure.json 我的教案模板.docx

# 模式 C：不传模板 — 用内置默认结构（前提：环境变量 LESSON_TEMPLATE 或
#         ~/.workbuddy/skills/zhongshan-lesson-plan/templates/中专教案模板.docx 存在）
python tools/fill_lesson_plan.py \
  examples/01_sample_first_lesson.json \
  output_lesson_01.docx
```

工具会自动：
- 读入 JSON 内容
- 分析传入的模板（或使用 `--structure` 提供 / 内置默认）
- 在原模板的 15 行表格对应单元格写文字
- 校验生成文件结构与模板一致

退出码 0 即通过；非 0 表示结构破坏（如某单元格超出该行容量）。

### 5. 处理扫描版 PDF（关键）

教材 PDF 多为**纯扫描件**、无文字层。处理步骤：

1. 用 `pymupdf` 按 PDF 索引 = **书页码 + 偏移** 渲染页
2. 多页拼成 2×2 或 3×3 大图（dpi 118–130）
3. 用多模态 agent / 视觉模型直接读图取原文
4. 缩写进内容 JSON

偏移值因教材不同而异：本仓库使用的样本为 **+9**（用户视具体教材实测）。

## 推荐口径

| 单元 | 课时 | 内容组织 |
|---|---|---|
| 理论节 | 2 课时（90 min） | 6 大环节：情境导入→新授知识→拓展延伸→应用举例→小结→作业 |
| 任务节 | 2 课时（90 min） | 6 大环节：任务描述→知识准备→任务实施→任务调试→任务验收→拓展 |
| 合并节 | 4 课时（180 min） | 两份 2 课时合并，含完整 4 个子环节 |

## 校验脚本

`tools/fill_lesson_plan.py` 内置**模板自适应 + 结构校验**（退出码含义）：

| 退出码 | 含义 |
|---|---|
| 0 | 行数 / 单元格数 / vMerge 全部对齐模板结构 |
| 1 | 调用错误（缺参数 / 默认模板不可用） |
| 2 | 生成的文件结构与模板不符 |

`--analyze` 模式可单独使用，输出模板结构 JSON（行数、各行单元格数、vMerge 状态），便于排查模板与 JSON 不匹配的问题。

## 适用与限制

- ✅ Word 文档格式 `.docx`（含复杂 vMerge 单元格）
- ✅ 扫描版教材（无文字层）
- ⚠ 模板结构绑死 15 行表格；其他模板需重写单元格定位
- ⚠ 内容质量取决于资料库 / 原始 PDF 文本质检

## 复现 某某A 老师的 XX电子1 学期案例

配套了 `examples/01_sample_first_lesson.json` 作为参考。

完整 39 份案例（含配套学案、默写小测、任务工单）的对话复现见：
[WorkBuddy 对话存档（2026-09-10 / 2026-09-11）](https://workbuddy.cn)

## 贡献

欢迎 fork / PR，约定：
- 抽掉任何属于特定用户（学生姓名、班级、教材版本号等）的硬编码
- 在 `examples/` 下补一个跨课程的样本 JSON

## 协议

[Apache License 2.0](./LICENSE)

## 致谢

- 模板来自 `zhongshan-lesson-plan` 技能（某某X 教务处标准模板）
- 教材示例：《单片机应用技术》（C 语言版）第 5 版活页式，某某B 主编
