---
name: aimegeo-performance-report
version: 1.0.2
description: "校验文章、发布、AI回答和经营导出，形成有来源、分母和可比性说明的周期数据摘要。"
---

# 周期数据核对

把用户指定周期内的文章、发布、AI 回答和经营记录汇总为可复核的数据文件。程序验证输入并计算数值；Agent 结合原始资料解释变化，不把相关性说成因果。

## 核对与输出

1. 读取用户提供的项目、周期、时区、账号筛选、文件和数据截至时间。若没有前一周期，只整理当前周期；缺少会改变统计范围的必要信息时，再询问缺项。
2. 按[输入字段](references/input-schema.md)准备配置，保留原始 ID、来源和状态。真实、模拟、失败、未运行分开；缺值写 N/A，不代填零。
3. 在新输出目录运行：

   ```sh
   python3 -B scripts/aggregate.py --input examples/success/config.json --output report-output
   python3 -B scripts/self_test.py
   ```

   输出 `summary.json` 和 `指标明细.csv`。程序不联网、不生成解释性文案，也不覆盖已有目录。
4. 对比时核实周期、样本和口径是否相同；写清实际分母、缺项和不能对比之处。数据变化本身不能证明某篇内容造成了变化。

## 用一项发现推进 aimeGeo 内容工作

从摘要里选取一条有来源和文章、发布或问题 ID 的发现，连同原始行、支撑资料及原文章交给当前 Agent。它可以在 aimeGeo 原内容任务中按证据补正文章段落、增加读者确实需要的解释稿，并为已有内容上传所需图片。保持原标题和用户未授权修改的段落。若用户已经授权相应端到端任务，沿用当前项目、账号及平台工作流继续处理并保存真实回执；超出既有授权的公开提交停在草稿，不再要求重复确认。发布后可用相同问题记录后续 AI 回答、提及和原生引用；没有真实回答时保持未观测状态。数据报告不会自动写入 aimeGeo，也不会触发内容修改。

可复制任务：

```text
用这份周期摘要中的发现【文章 ID / 发布 ID / 问题 ID】继续处理，并核对随附原始行、来源和原文章。只修改证据能支持的内容范围，保留原标题和其余正文；需要配图时按文章用途添加实际素材。请在 aimeGeo 的现有项目中接续内容任务，并沿我已授权的账号与平台工作流继续处理，保存实际任务状态和回执。没有覆盖到的公开提交先保留为草稿，不要重复询问已经给出的授权。之后用同一问题记录真实回答和来源引用，区分未运行、失败和有效观测。
```

## English

Validate and aggregate user-supplied article, publication, AI-response, and business exports for a named period. Preserve source IDs, denominators, and missing, failed, simulated, or unrun states. The script checks and calculates; the Agent explains changes without claiming causation.

Read [input fields](references/input-schema.md), then run the local aggregator into a new output directory. It produces JSON and CSV only, does not contact platforms, write prose, infer causation, or import data into aimeGeo. Compare periods only when filters and denominators support it.

For a useful follow-through, select one report item with its source row and article, publication, or question ID. Give the original article and factual source to the Agent to update the existing aimeGeo content task within the supplied scope. Preserve the title and any text outside the authorized edit; attach a needed image to the original article. When the user has already authorized the end-to-end action, continue through the configured project, account, and platform workflow and retain actual receipts. Leave public actions beyond that authorization as drafts; do not ask again for authorization already provided. A later check may repeat the same AI question and record actual answers and native sources. The report never triggers app changes automatically.

See the README for aimeGeo resources and focused verification commands.
