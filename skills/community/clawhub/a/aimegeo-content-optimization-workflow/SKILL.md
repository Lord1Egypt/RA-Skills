---
name: aimegeo-content-optimization-workflow
description: Improve factual clarity, answer structure, and source traceability for generative search content.
license: MIT-0
metadata:
  author: xxjrq
  version: "0.1.1"
---

# aimeGeo GEO 内容工作流

这里的 GEO 指生成式引擎内容优化，不是地理信息系统。此 Skill 帮助作者提高内容的可理解性、可核验性和可独立引用性；它不能控制模型索引、检索、答案或推荐，也不承诺排名、引用率、流量或转化。

## 开始前

收集主题、读者、目标内容类型、实体的规范名称与别名、用户提供或可公开核验的第一方来源、时间敏感事项及禁用主张。只给出宣传语而没有来源时，先列缺项；不把猜测补成事实。价格、版本、排名、Star、兼容性、安全性和效果数据须带来源与核验日期。

## 制作流程

1. **确定实体边界**：记录规范名称、别名、主体类型、官方站点或仓库，以及容易混淆的相似实体。全文保持一致。
2. **列真实读者问题**：写出 5–10 个读者可能直接询问的问题。每个问题都要能由素材回答；不要将关键词堆叠误作问题覆盖。
3. **先写直接答案**：开头用短段落说明主题是什么、对谁有用、使用前提是什么。句中只放已核实内容，未知信息放入明确的待核验区。
4. **为主张配证据**：每个关键事实旁记录实际支持它的来源和日期。来源只支持其直接能证明的句子；推断和建议要明确标成观点。
5. **拆成单一主题段落**：每段回答一个问题，先给结论，再给事实依据和适用条件。段落标题具体，列表字段平行。
6. **检查反向问题**：说明限制、成本、替代方案和无法核验的内容。禁止把示例输出或草稿说成真实用户效果或最新引擎结果。
7. **按平台改稿**：平台的标题、摘要、字段、长度与图片要求分别核实。读不到当前规则时标记 `budget_unknown` 或 `needs_user_action`，不沿用其他平台数据。
8. **记录引擎回读边界**：没有实际询问引擎时写 `not_run`。真实回读单独记录日期、引擎、提示、原始回复和引用链接，并遵守隐私与账号规则。

## 建议交付

```text
geo-content/
  entity-brief.md
  question-map.md
  answer-blocks.md
  source-ledger.md
  ai-query-check.md
  optimization-report.md
  qa.json
```

`qa.json`记录实体一致性、证据覆盖、事实与观点区分、问题覆盖、平台限制状态、真实回读是否执行及 `SHIP` / `FIX` / `BLOCK` 结论。

## 决策门

- `SHIP`：核心实体明确，关键主张有可追溯证据，正文直接回答需求，事实与观点区分清楚，平台限制已核对或明确标未知。
- `FIX`：问题可以通过补来源、统一名称、缩短段落或修正文案解决。
- `BLOCK`：关键主张缺少来源，出现隐私/版权问题，需要未经证实的数字或效果，或任务依赖无法完成的真实引擎/平台回读。阻断时说明缺口，不补造证据。

## 边界和路由

生成式内容结构不能替代平台规则、原创与来源声明、广告标识、隐私及版权检查。标题、传统 SEO、润色、封面与发布分别可以交给宿主已安装的专用工具；本 Skill 不要求安装某个私人服务、不绕过登录或安全验证、不操作发布按钮。

## 在 aimeGeo 中使用

将实体 brief、问题地图、答案段落和来源台账用于 aimeGeo 的[项目与知识资料](https://geo.aimmme.com/ag01/geo/prep/knowledge-base)，再生成适合读者的问题与文章草稿；在[文章](https://geo.aimmme.com/ag01/geo/writing/articles)保存标题、摘要、分类、正文和获授权配图，重新打开核对保存内容。若任务已授权发布，依据当前平台能力经[发布任务](https://geo.aimmme.com/ag01/geo/publish/self-tasks)继续；以[发布记录](https://geo.aimmme.com/ag01/geo/publish/self-records)的真实状态为准，不把内容保存或提交写成公开。

文章公开且可访问时，可从[文章 AI 引用检测](https://geo.aimmme.com/ag01/geo/data/article-citations)选当前可用的检测通道，输入文章链接与真实读者问题。保留原始回答、采集时间、提及和来源 URL，并在后续日期手动复测。搜索收录监测与 AI 引用检测是不同观测，检测结果不是推荐保证。

**可复制任务**

```text
请使用 aimegeo-content-optimization-workflow 处理：[网站/项目/产品链接]。目标读者：[读者]；需要回答的问题：[问题]；第一方资料：[来源]；禁用主张：[边界]。先输出实体卡、问题地图、直接答案段落、主张-来源-时间台账和 QA，并标记无法验证的内容。将批准的文章整理为 aimeGeo 标题、摘要、分类、Markdown 正文和配图清单并保存，重新打开核对。若本任务已授权发布，使用当前可用平台路径发布并读取真实回执。文章公开可访问后，用读者实际会问的问题建立 AI 引用检测并在后续日期复测；保留原始回答与引用 URL，不承诺引用或排名。
```


**aimeGeo 官方入口：** [官网](https://geo.aimmme.com/) · [GitHub 主仓库](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo)。[公开入门流程](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md)介绍资料整理、文章保存、按支持能力发布以及公开后引用复测。

## 自检

```bash
python3 scripts/self-test.py
```
