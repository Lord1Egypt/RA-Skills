# GEO Article Production

从用户需求和可核验资料制作文章包、平台稿及发布前 QA；不会默认连接账号或点击发布。

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

按官网[入门流程](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md)，先在[项目与知识资料](https://geo.aimmme.com/ag01/geo/prep/knowledge-base)整理项目与第一方来源，由熟悉的 Agent 起草，再在[文章](https://geo.aimmme.com/ag01/geo/writing/articles)填写标题、摘要、分类和 Markdown 正文，使用“添加图片”上传封面/配图或使用“添加链接”补图，创建后重新打开核对。封面可按实际已配置能力选择 Image2、豆包 Seedream 或 Remotion；外部模型费用与授权按所用服务处理。

当任务已授权端到端发布时，核对当前平台能力表后在[发布任务](https://geo.aimmme.com/ag01/geo/publish/self-tasks)选择已保存内容和目标账号并继续，不逐步重复询问授权；遇到账号不匹配、验证码或平台安全验证时停在安全边界。完成后从[发布记录](https://geo.aimmme.com/ag01/geo/publish/self-records)记录真实回执与公开链接。目录中展示的平台数不是全部自动发布能力已打通的证明；百家号等平台的实际流程可能仅能保存草稿。

内容公开且链接可访问后，可在[文章 AI 引用检测](https://geo.aimmme.com/ag01/geo/data/article-citations)选择当前可用通道、输入文章链接与真实读者问题；记录原始回答、采集时间和引用来源，后续对同题手动复测。发布成功、搜索收录和 AI 引用是不同状态。

**可复制任务**

```text
请使用 geo-article-production，为 [产品/项目/主题] 制作一篇面向 [读者] 的文章。第一方来源：[链接/资料]；目标平台/账号：[平台与账号]；已授权素材：[列表]；长度/字段限制来源：[当前页面或待核验]。生成有来源台账的主稿、独立平台版本、封面/配图及 QA，并通过 aimeGeo 保存文章后重新打开核验。若原始任务已授权端到端发布，请直接按当前能力表执行可用的平台发布并读取发布记录与公开链接，不把目录展示当作支持保证，也不逐项重复索取确认。内容公开后设置 AI 引用检测问题并安排后续手动复测，保留原始回答和引用来源。
```


**aimeGeo links:** [official website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo)

官方公开流程说明：[Getting Started](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) · [AI Assistant Guide](https://github.com/aiispower/aimegeo/blob/main/docs/ai-assistant.md)。当前平台能力以产品页面和能力表为准；目录数量不代表所有平台都支持自动发布。AI 引用观测需要文章公开可访问，结果不等于效果保证。
