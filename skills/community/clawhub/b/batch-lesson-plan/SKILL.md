---
name: batch-lesson-plan
description: 把一份《授课计划》自动转成整套中专教案（.docx）。当用户提供"授课计划"/"教学进度表"并要求"按计划生成教案""批量生成教案""整学期的教案"时使用。流程：解析授课计划表 → 提取课次清单 → 读扫描版教材 PDF 原文 → 写内容 JSON → 批量生成 docx → 结构校验。中专电子/机械/计算机等专业的理论+任务一体化课程均适用。
agent_created: true
---

# 授课计划 → 批量教案生成

把一份「授课计划（教学进度表）」变成整本、可直接打印的中专教案（`.docx`）。

## 适用与前置

- **模板**：15 行中专教案模板（`vMerge` 已布置）。例：`templates/中专教案模板.docx`
- **填表工具**：本技能 `tools/fill_lesson_plan.py`（JSON → docx，含结构校验）
- **Python**：≥ 3.10，依赖 `pymupdf` `lxml` `pillow`
- **教材 PDF**：很多教材是**纯扫描件**（无文字层），需用 `pymupdf` 渲染成图后借助多模态读取

> 所有脚本都不假设绝对路径。模板 / 教材 PDF / 输出目录都通过命令行传入。

## 第一步：读授课计划

| 输入 | 推荐工具 |
|---|---|
| `.doc`（老格式） | WPS / LibreOffice 转成 `.docx`，或调用 WorkBuddy 的 `tencent-local-office-edit` |
| `.docx` | `zipfile` + `lxml` 直接读 `word/document.xml` |
| `.pdf` | `pymupdf` 渲染后多模态读 |

> 详细 `.docx` 解析方法见 `examples/` 或 README。

## 第二步：按用户规则提取清单（必须先确认）

典型授课计划列：`周次 | 章节名称及主要内容 | ... | 授课节数`。
下列规则已在某某A 老师《单片机原理与应用》XX电子1 案例中确认，其他课程/教师应**先与作者对齐**再批量：

1. 「授课节数」列**有阿拉伯数字的行**才出教案
2. 课时数 = 数字（通常 2 或 4）
3. 主题 = 「章节名称及主要内容」列**原文**
4. 连续重复主题（含"任务X-N 修改"与同一任务）→ **合并为一份**，课时相加
5. 期末考试 → **不出教案**；标称总课时与逐行加总不一致时按作者口径处理
6. "课程复习"多条 → **只出 1 份**通用复习课教案
7. 教材版本按授课计划/作者口述填（可能与资料库 PDF 版本不同，以作者为准）

> **永远不要直接批量出**：先用脚本统计并打印清单，让作者确认后再生成。

## 第三步：建内容 JSON

写 `examples/<两位序号>_<简写>.json`：

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

字段含义与示例见 `examples/01_sample_first_lesson.json`。

## 第四步：扫描版教材 PDF 处理

教材 PDF 无文字层时：

1. **实测页码偏移**：找一处可识别的章节标题页（如"目录"或"第 1 章"），对比 PDF 索引与书页码，确定 `偏移 = PDF索引 - 书页码`
2. 用 `pymupdf` 按 `dpi=118` 渲染多个书页（2×2 拼图效率最高）
3. 多模态读图整理原文
4. 按"任务描述→知识准备→任务实施→任务调试→任务验收→拓展"组织教学过程，体现实验室理实一体化

参考实现见 `tools/fill_lesson_plan.py` 内的辅助函数。

## 第五步：批量生成 docx

```bash
# 模式 A：传模板（脚本自动分析结构）
python tools/fill_lesson_plan.py examples/01_sample_first_lesson.json \
  output/lesson_01.docx 我的教案模板.docx

# 模式 B：先分析再用预生成结构
python tools/fill_lesson_plan.py --analyze 我的教案模板.docx > structure.json
python tools/fill_lesson_plan.py examples/01_sample_first_lesson.json \
  output/lesson_01.docx --structure structure.json 我的教案模板.docx

# 模式 C：不传模板 → 用内置默认结构
python tools/fill_lesson_plan.py examples/01_sample_first_lesson.json \
  output/lesson_01.docx
```

工具会打印 `filled=N rows=K validate: 结构完整`，退出码 0 即通过。

## 推荐课时分配

| 单元 | 课时 | 6 大环节 |
|---|---|---|
| 理论节 | 2 课时 | 情境导入→新授→拓展→应用→小结→作业 |
| 任务节 | 2 课时 | 任务描述→知识准备→任务实施→任务调试→任务验收→拓展 |
| 合并节 | 4 课时 | 两份 2 课时合并（覆盖该节全部小节） |

## 思政元素（建议融入）

- 国产芯片发展（宏晶 STC、兆易 GD32 等）
- 关键核心技术自主可控
- 工匠精神 / 严谨作风 / 标准化规范
- 信息安全 / 密码学原理（与课程章节相关时）

## 配套资料（可选）

批量完成后可一并生成：
- **学案**（学生用）：信息行→三维目标→重点难点→知识梳理(填空)→课堂练习→作业→反思
- **默写小测**：8 大部件、关键寄存器（PSW/TMOD/TCON/SCON/IE/IP 等）
- **任务工单**：硬件→电路→程序→调试→验收→拓展→评价

模板与示例见 `examples/` 配套文件（与 Skills Archive 保持同步）。

## 复现案例

某某A 老师《单片机原理与应用》XX电子1 学期案例：39 份 / 100 课时 + 39 份学案 + 16 份任务工单 + 2 份默写小测 + 1 份总目录 = **97 份 docx**，全部通过校验。

完整对话复现见 [WorkBuddy 对话存档](https://workbuddy.cn)（2026-09-10 / 2026-09-11）。

## 协议

Apache License 2.0.
