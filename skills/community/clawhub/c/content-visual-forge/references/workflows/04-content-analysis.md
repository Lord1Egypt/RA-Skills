# Workflow 04 · Content Analysis

在 Source Lock 和 Output Mode Router 完成后，对当前内容做进一步研究。

## 目标

提炼出适合卡片表达的内容骨架，而不是机械复述原文。

## 分析维度

- 用户会关心什么？
- 最值得被图解的是什么？
- 哪些信息适合做对比、步骤、框架、清单？
- 哪些部分必须忠于原文，不宜过度改写？
- 哪些内容适合强调、哪些适合删减？

## 输出

- 内容研究摘要
- 传播角度
- 可视化机会点
- 风险点
- 推荐页数或推荐卡片结构

## Content Compression Ladder 触发

当输出模式为 `social-card` 或长文需要拆页时，必须在此阶段之后、进入分页脚本之前执行 Content Compression Ladder（`references/config/content-compression-ladder.md`）。

触发条件（满足任一）：

- 输出模式为 `social-card`
- 输入源为长文 / 网页 / PDF，且需要拆成 4 页以上
- 用户要求内容压缩或摘要式卡片

Content Compression Ladder 的输出（`core_claim`、`viewer_promise`、`section_map`、`page_hooks`、`body_fragments`、`visual_evidence`）将作为后续分页脚本的输入。
