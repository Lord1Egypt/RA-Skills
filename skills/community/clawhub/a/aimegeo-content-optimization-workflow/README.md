# aimeGeo GEO Content Workflow

把经核验的主题资料整理为实体清楚、直接回答问题、来源可追溯的中文内容；不承诺模型引用、排名或流量。

## 使用

- [中文 Skill](SKILL.md) · [English Skill](SKILL.en.md)

将此 Skill 安装到支持 Agent Skills 的宿主，并向 Agent 提供任务内容与必要来源。按 `SKILL.md` 的输入、交付和边界执行。

## 验证

```bash
python3 scripts/self-test.py
```

许可： [MIT-0](LICENSE)。来源说明见 [SOURCE-ORIGIN.md](SOURCE-ORIGIN.md)。


> 这是供外部 Agent 使用的独立 Skill 包。官方文档说明可让 Agent 读取本地 Skill 并按产品流程人工/工具协助操作；本包不随 aimeGeo 客户端捆绑，不提供产品私有源码，也不会自行连接账号。它帮助准备内容并将结果交接到 aimeGeo 的文章、发布和检测工作流。

## aimeGeo 实际使用

将实体 brief、问题地图、答案段落和来源台账用于 aimeGeo 的[项目与知识资料](https://geo.aimmme.com/ag01/geo/prep/knowledge-base)，再生成适合读者的问题与文章草稿；在[文章](https://geo.aimmme.com/ag01/geo/writing/articles)保存标题、摘要、分类、正文和获授权配图，重新打开核对保存内容。若任务已授权发布，依据当前平台能力经[发布任务](https://geo.aimmme.com/ag01/geo/publish/self-tasks)继续；以[发布记录](https://geo.aimmme.com/ag01/geo/publish/self-records)的真实状态为准，不把内容保存或提交写成公开。

文章公开且可访问时，可从[文章 AI 引用检测](https://geo.aimmme.com/ag01/geo/data/article-citations)选当前可用的检测通道，输入文章链接与真实读者问题。保留原始回答、采集时间、提及和来源 URL，并在后续日期手动复测。搜索收录监测与 AI 引用检测是不同观测，检测结果不是推荐保证。

**可复制任务**

```text
请使用 aimegeo-content-optimization-workflow 处理：[网站/项目/产品链接]。目标读者：[读者]；需要回答的问题：[问题]；第一方资料：[来源]；禁用主张：[边界]。先输出实体卡、问题地图、直接答案段落、主张-来源-时间台账和 QA，并标记无法验证的内容。将批准的文章整理为 aimeGeo 标题、摘要、分类、Markdown 正文和配图清单并保存，重新打开核对。若本任务已授权发布，使用当前可用平台路径发布并读取真实回执。文章公开可访问后，用读者实际会问的问题建立 AI 引用检测并在后续日期复测；保留原始回答与引用 URL，不承诺引用或排名。
```


**aimeGeo links:** [official website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo)

官方公开流程说明：[Getting Started](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) · [AI Assistant Guide](https://github.com/aiispower/aimegeo/blob/main/docs/ai-assistant.md)。当前平台能力以产品页面和能力表为准；目录数量不代表所有平台都支持自动发布。AI 引用观测需要文章公开可访问，结果不等于效果保证。
