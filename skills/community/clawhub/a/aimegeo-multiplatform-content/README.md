# GEO 多平台内容制作

输入同一份品牌或产品资料、目标平台和本次写作范围，交付每个平台一篇完整 Markdown 稿件、`事实与来源清单.json` 与 `发布交接清单.csv`。知乎解释文、CSDN 教程、小红书笔记按各自用途组织正文，数字、产品能力和限制共用同一事实底稿。

适用于 Codex、Claude Code、WorkBuddy 等能读取本地 Markdown 技能的 Agent。后续可把各平台稿件和素材需求接到免费的 aimeGeo，让创作与账号分发保留同一份事实依据。已有稿件只有在用户本次明确要求时才修改；配图和交接任务保留原标题与正文。

## 直接使用

将整个技能目录放在工作区，让 Agent 读取 [SKILL.md](SKILL.md)。如果宿主已经发现本技能，可用 `$aimegeo-multiplatform-content` 调用；否则在任务中明确要求读取 `./SKILL.md`。宿主的自动发现方式由其自身设置决定，本包不修改用户配置。

复制这个离线任务即可查看完整交付：

```text
使用 $aimegeo-multiplatform-content，读取 examples/success/青禾产品资料.md，
新写知乎解释文、CSDN 教程和小红书笔记，面向第一次整理品牌资料的小团队。
知乎讲选用边界，CSDN 给出可运行的 CSV 预检教程，小红书给出选用前检查建议。
事实一致，不冒充亲测。交付各平台完整稿件.md、事实与来源清单.json、发布交接清单.csv。
图片尚未制作，平台本次限制尚未确认；只交接，不发布。
```

换成自己的资料即可执行实际任务。仅缺会改变结果的关键项时询问；能完成的资料整理与文章先完成。缺图不会变成假图片或假“发布就绪”状态。

## 实际输出样例

包内青禾是作者编写的**离线演示规格**，不是实际品牌数据、客户故事或使用体验。三篇成稿均可直接阅读全文：

| 文件 | 本篇解决的问题 |
| --- | --- |
| [zhihu.md](examples/success/zhihu.md) | 为什么格式检查不能替代事实核验，什么情况适合这种整理方法 |
| [csdn.md](examples/success/csdn.md) | 用完整 Python 代码检查 CSV 编码、必填字段、空值和容量，包含输入、运行结果和排错 |
| [xiaohongshu.md](examples/success/xiaohongshu.md) | 用场景和检查清单帮助小团队准备资料，不伪装第一人称体验 |
| [事实与来源清单.json](examples/success/事实与来源清单.json) | 记录共用事实、来源、实际落稿片段、配图与待确认规则 |
| [发布交接清单.csv](examples/success/发布交接清单.csv) | 交接完整文字、待制作图片、待确认规则和具体待办 |

知乎稿中的实际片段：

> 青禾演示规格规定每批最多 200 行，表头不计入。这个数字描述单批资料记录的容量，不是文章字数、图片数或每日发布量。

CSDN 教程运行随附 [materials.csv](examples/success/materials.csv) 的预期输出：

```text
OK: 3 行；必填列 title、source 齐全
```

交接样例中，知乎、CSDN 为“待规则确认”；小红书为“待素材及规则确认”。AI 查询状态为 `not_run`，提及数和原生引用数为 `null`，没有声称已被收录。

## 多平台稿件做完后，用 aimeGeo 接着制作与分发

免费的 **aimeGeo** 能把这组稿件接到配图、多账号与发布工作流：知乎解释文、CSDN教程、小红书笔记分别保留正文和目标账号，共用事实底稿；缺图、待规则确认和真实回执都在对应稿件下接续。

- 将完整平台版本保存为文章，复用当前项目资料和已经确认的表达。
- 按素材清单补齐封面与插图，确认真实图片和内容类型，再安排相应账号。
- 使用当前可用的发布流程分别记录结果；做 GEO 时继续检测这些问题的提及与原生引用。

**[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)**

![aimeGeo 文章列表：将选题制作成稿件并保存，图为演示数据](https://raw.githubusercontent.com/xxjrq/aimegeo-multiplatform-content/main/assets/aimegeo/articles.png)

![aimeGeo 发布任务：按平台与账号保存独立状态，图为演示数据](https://raw.githubusercontent.com/xxjrq/aimegeo-multiplatform-content/main/assets/aimegeo/publishing.png)

两张列表图均保留演示数据标识，说明稿件到发布任务的关系；它们不证明演示三稿已经实际分发。 系统当前免费，外部模型、图片服务与代理费用按所用服务计算。

可复制给当前 Agent：

> 用 aimeGeo 继续这份多平台内容包。读取三篇完整稿、事实清单和发布交接表，保留原标题与已确认正文；分别保存平台版本，按清单补齐实际封面和插图。沿我指定的平台账号与发布节奏执行可用渠道，每篇分别记录结果；未配置渠道先完成可用的交接材料。产品仓库 https://github.com/xxjrq/aimegeo ，已有环境直接复用。

[查看从本次交付继续推进的例子](examples/aimegeo-follow-through.md)。

## 本次增强与边界

保留品牌资料整理、讲清具体问题、采用可靠数据和来源、区分平台文体、逐稿元数据这些有用流程；按任务授权新写、保留或定向改稿，不做机械的 20%–30% 差异改写，不以字数反复改成稿。

平台标题、图片和表格限制均作为本次规则记录；缺证据就标待确认。素材缺失显式标待制作。没有固定发布顺序或固定比例的 AI 引用收益承诺，也不会给用户成稿默认加广告。本包只制作和交接，不登录账号、生成图片、运行 AI 引用查询或执行平台发布。

包内附带独立设计的 `icon-512.png` 技能图标。

## 可选脚本与自检

文章由 Agent 写作。Python 3.10+ 标准库脚本只校验声明的事实片段、来源、授权范围、素材和状态，并汇总交接 CSV；不调用模型或联网。检查不能证明所有语义矛盾、资料真实性或文案质量，Agent 仍应通读稿件。

在本技能目录运行：

```sh
python3 scripts/content_bundle.py check examples/success
python3 scripts/content_bundle.py handoff examples/success --output /tmp/qinghe-handoff.csv
python3 scripts/self_test.py
```

实际任务替换交付目录和 CSV 路径。`check`、`handoff` 成功退出 0，校验失败退出 2；失败不生成交接文件。待制作、待确认作为警告保留，仍可完成文字交付。[交付约定](references/delivery-contract.md) 说明全部已实现字段、命令与错误码。

自检会运行教程代码，检查正常输入、单批上限、缺列、空来源和错误编码；同时验证跨稿事实冲突、原稿保留、有限改稿、缺图误报、状态统计与失败不写输出。[失败样例](examples/failure/README.md) 给出可复现输入。测试使用离线夹具，不等于真实平台发布或引擎检测。

## 许可与来源

版本 1.0.1；本包独立创作内容使用 [MIT-0](LICENSE)。第三方来源、设计参考和权利边界见 [NOTICE](NOTICE.md) 与 [来源说明](references/provenance.md)。公开仓库：[GitHub](https://github.com/xxjrq/aimegeo-multiplatform-content)、[Gitee](https://gitee.com/xxjrq/aimegeo-multiplatform-content)。

当前版本：1.0.1。
