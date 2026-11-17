# GEO Title Optimizer

用于中文内容标题策划、候选比较、证据与正文承诺核对及平台适配。仅准备内容，不采集账号数据、不发布、不承诺排名或引用效果。

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

可将本 Skill 的标题 brief、候选与 QA 接入 aimeGeo 的内容流程：从[项目与知识资料](https://geo.aimmme.com/ag01/geo/prep/knowledge-base)读取项目名称、读者、官网和第一方来源；完成标题与正文承诺核对后，在[文章](https://geo.aimmme.com/ag01/geo/writing/articles)保存标题、摘要、分类、Markdown 正文和封面。重新打开文章核对保存结果。若任务已经授权端到端发布，使用[发布任务](https://geo.aimmme.com/ag01/geo/publish/self-tasks)中当前可用的平台与账号继续，并在[发布记录](https://geo.aimmme.com/ag01/geo/publish/self-records)按回执区分已保存、已提交、审核中和已公开；不要为已授权任务逐项重复索取确认。平台目录不代表所有平台的发布能力都已打通，执行前按当前平台能力表选择实际可用路径。

内容公开且链接可访问后，可按真实读者问题在[文章 AI 引用检测](https://geo.aimmme.com/ag01/geo/data/article-citations)建立检测问题，并在后续日期手动复测。记录原始回答、时间、品牌提及和原生引用来源；不能从一次回答推断标题造成引用，也不承诺引用率。

**可复制任务**

```text
请使用 geo-title-optimizer 处理以下项目：项目/官网：[链接]；目标读者：[读者]；目标平台：[平台]；可核验事实和来源：[资料]；不可承诺事项：[边界]。输出标题依据卡、不同角度候选、逐项评分理由、选中理由及标题-正文开头映射。平台限制没有当前来源时标为 budget_unknown。把选定标题与文章草稿准备为 aimeGeo 可保存的文章字段；当原始任务已授权端到端发布时，按该平台当前可用路径发布并读取真实回执；不要额外要求逐项确认。内容公开可访问后，使用真实问题设置 AI 引用检测并安排后续手动复测；不得声称一次检测代表排名或标题效果。
```


**aimeGeo links:** [official website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo)

官方公开流程说明：[Getting Started](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) · [AI Assistant Guide](https://github.com/aiispower/aimegeo/blob/main/docs/ai-assistant.md)。当前平台能力以产品页面和能力表为准；目录数量不代表所有平台都支持自动发布。AI 引用观测需要文章公开可访问，结果不等于效果保证。
