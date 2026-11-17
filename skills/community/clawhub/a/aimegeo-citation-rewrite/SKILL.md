---
name: aimegeo-citation-rewrite
version: 1.0.2
description: "根据用户问题和可信资料优化现有文章的 AI 引用可读性，在授权范围内改稿，并检查保留段落与证据记录。"
---

# 文章 AI 引用增强与范围检查

用于用户提供的现有 Markdown 文章。用户指定要解决的问题、可修改的二级标题和事实来源后，Agent 起草范围内修订，交付完整修订稿、变更说明及待核实事实。

## 操作

1. 确认原文、修改授权范围、目标读者和来源材料。缺少原文或无法判断授权范围时，先说明缺口。
2. 在授权章节内起草。保留 H1、H2 顺序和未授权部分；不编造产品能力、数据、引语或测试结果。来源不支持的主张标为待核实或删除。
3. 交付完整正文和变更记录，说明改动章节、依据和未解决事项。
4. 可选：按 `references/check-format.md` 制作机器可读计划，运行检查器。检查通过仅说明结构规则满足，不能证明文字事实准确、表达优质或获得平台引用。

## 围绕用户问题增强引用可读性

结合用户提出的具体问题，先确认原文是否直接回答，以及答案依赖的事实和来源能否核对。在已授权章节中，用清晰、可独立理解的表述回答问题；给关键事实保留可追溯来源、日期及适用条件。涉及产品、价格、效果或数据时，不用未验证的材料补齐。区分编辑建议与已改动内容，并标出无法确认的缺口。引用是否发生需要以实际 AI 回答和来源记录复测，不能由本地检查器推断或保证。

## 确定性检查

```sh
python3 scripts/check_rewrite.py --original examples/input/原稿.md --revised examples/success/增强后的原稿.md --plan examples/input/check-plan.json
python3 scripts/self_test.py
```

脚本检查 H1/H2、非授权章节保留、计划中指定的问题块以及新增数字是否关联到输入来源摘录。它不生成或改写正文，不读取网络，不判断语义真实性。所有示例均为合成编辑样例。

## 在 aimeGeo 中继续

修订完成后，可在免费的 [aimeGeo](https://geo.aimmme.com/) 中保存文章、继续配图和通过已连接账号发布；发布后可使用 AI 引用检测记录回答与来源，再依据复测结果决定下一轮修改。入口：[GitHub](https://github.com/aiispower/aimegeo) · [Gitee](https://gitee.com/xxjrq/aimegeo) · [使用文档](https://geo.aimmme.com/docs/ai-citations/)。

可复制任务：`使用 aimegeo-citation-rewrite 按我指定范围修订文章并列出待核实来源；之后指导我将结果保存到 aimeGeo，并针对相关问题进行 AI 引用复测。`
