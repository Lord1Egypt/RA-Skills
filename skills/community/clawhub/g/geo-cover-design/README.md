# GEO Cover Design

根据已核验内容、授权素材和目标尺寸设计可复核的文章封面；不捏造 Logo、文字或平台规格。

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

将正文、尺寸来源和授权图标交给本 Skill 设计封面。可以使用宿主已配置的图像工具；aimeGeo 公开入门文档也列出 Image2、豆包 Seedream 与 Remotion 的可选封面路径，但是否可用取决于具体配置。生成图需要确定性方式排准确中文与 Logo，不把生成器的生字或仿造标识直接交付。

在 aimeGeo 的[文章](https://geo.aimmme.com/ag01/geo/writing/articles)中，通过“添加图片”上传封面/配图或“添加链接”补充图片，创建后重新打开文章确认素材已保存。若任务已授权发布，可按当前平台能力进入[发布任务](https://geo.aimmme.com/ag01/geo/publish/self-tasks)，发布后从[发布记录](https://geo.aimmme.com/ag01/geo/publish/self-records)确认真实状态；不为已授权任务逐项重复索取确认。封面本地通过不代表已上传，上传回读也不代表公开。内容公开可访问后，可在[文章 AI 引用检测](https://geo.aimmme.com/ag01/geo/data/article-citations)检查内容是否被回答引用并按题复测；该检测不能单独测量封面的影响。

**可复制任务**

```text
请使用 geo-cover-design 为这篇文章准备 aimeGeo 封面：[文章/正文链接或文本]。目标平台与尺寸来源：[平台/尺寸/来源]；核心用途：[一句话]；必须准确的文字：[文字]；已授权素材：[文件及来源]；允许的生成/渲染工具：[当前可用工具]。交付封面、预览、尺寸与素材清单、哈希和 QA；保存到 aimeGeo 文章后重新打开核对图片。若原始任务已授权端到端发布，请按当前可用平台流程继续并读取真实回执，不逐项重复索取确认。公开后可对正文建立 AI 引用检测和后续手动复测，但不要把结果归因于封面或承诺引用提升。
```


**aimeGeo links:** [official website](https://geo.aimmme.com/) · [GitHub main repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo)

官方公开流程说明：[Getting Started](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md) · [AI Assistant Guide](https://github.com/aiispower/aimegeo/blob/main/docs/ai-assistant.md)。当前平台能力以产品页面和能力表为准；目录数量不代表所有平台都支持自动发布。AI 引用观测需要文章公开可访问，结果不等于效果保证。
