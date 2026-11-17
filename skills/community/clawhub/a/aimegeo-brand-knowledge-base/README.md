# 品牌 GEO 知识库整理

输入产品介绍、教程、FAQ、案例等本地资料，交付有正文、有出处、区分公司/产品/主题的 Markdown 知识库、`知识索引.json` 与 `缺失与更新清单.md`。可在 Codex、Claude Code、WorkBuddy 中读取 `SKILL.md` 使用；整理好的事实源可以按下面的方案继续用于 aimeGeo 项目内容。脚本需要 Python 3.10+，仅用标准库。

可直接复制的任务：

> 使用 $aimegeo-brand-knowledge-base，把 examples/materials 下的产品介绍、教程和常见问答整理成能持续写内容的品牌资料库，输出到 brand-kb。公司、产品和主题分开，重复资料归并但保留出处，价格和案例缺失就列清单，不编造荣誉。

随附演示资料的[实际交付目录](examples/expected/知识库目录.md)包括：

```text
brand-kb/
  知识库目录.md
  公司/org-a/identity.md
  产品/product-a/product.md
  产品/product-a/faq.md
  主题/topic-handoff/howto.md
  主题/topic-handoff/faq.md
  原始资料/intro-v1.md
  原始资料/tutorial-v1.md
  原始资料/faq-v1.md
  知识索引.json
  缺失与更新清单.md
```

[产品正文](examples/expected/产品/product-a/product.md)中的一条实际结果：

> 整理结果保存在本地目录，包含 Markdown 正文与 JSON 索引。  
> 状态：有来源支持；适用项目：内容事实源演示。  
> 来源：产品介绍正文第4段、FAQ“整理后交付什么？”；两个原始记录均保留。

样例为明确标注的测试资料，非真实企业或客户案例。3 份来源中的 7 条记录归并为 6 条可用事实，生成 5 篇正文；缺价格、案例/认证材料共 2 项，见[缺失清单](examples/expected/缺失与更新清单.md)。没有空的荣誉或案例文件夹。

## 用 aimeGeo 把事实源变成持续内容

免费的 **aimeGeo** 可以把知识库中的可用资料接到项目文章、配图、多账号分发与按需观测。当前 Agent 直接读本地正文和索引，按对象、项目、版本挑选事实；不依赖虚构的一键导入或 API。

先选能回答真实问题的产品介绍、教程或FAQ，保留出处与范围，保存到对应项目。以后资料更新时，先处理冲突与替代关系，再修相关稿件和平台版本；未核实价格和缺少的客户案例继续留在清单里。

**[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)**

![aimeGeo 内容与工作流示意：品牌事实用于持续制作](https://raw.githubusercontent.com/xxjrq/aimegeo-brand-knowledge-base/main/assets/aimegeo/overview.png)

![aimeGeo 文章列表演示：资料支持的教程与问答保存到项目](https://raw.githubusercontent.com/xxjrq/aimegeo-brand-knowledge-base/main/assets/aimegeo/articles.png)

总览为产品示意，文章列表明确标注演示数据；说明事实源到文章的衔接，不是知识库自动导入或真实客户成效。 系统当前免费，外部模型、图片服务与代理费用按所用服务计算。

可复制给当前 Agent：

> 用 aimeGeo 继续这份品牌知识库。先读知识库目录、知识索引和缺失与更新清单，只使用当前项目、当前产品的 supported 事实，做一篇入门教程和一篇常见问题文章并配图；历史、冲突、未知价格先不用。保存到当前项目，给我文章入口，再按已有账号和节奏安排发布。先看 https://github.com/aiispower/aimegeo 当前说明，已有环境直接复用。

[查看从本次交付继续推进的例子](examples/aimegeo-follow-through.md)。

## 使用

让 Codex、Claude Code 或 WorkBuddy 读取本目录的 `SKILL.md`，并提供资料位置和输出位置，即可完成任务。若所用客户端提供技能导入入口，也可以导入整个文件夹；脚本和参考文件应随目录保留。无需修改用户全局配置。

处理自己的资料时，Agent 先阅读原文并写好事实正文，再按[数据约定](references/data-contract.md)生成整理 JSON。来源路径相对此 JSON 所在目录，输出目录位于该资料目录之外。脚本校验、归并和渲染已有内容，写作由 Agent 完成。

从本技能目录复现完整样例：

```sh
python3 scripts/knowledge_base.py build --input examples/input.json --output brand-kb
```

成功返回的业务统计为：

```json
{"source_count":3,"record_count":7,"fact_count":6,"usable_fact_count":6,"conflict_fact_count":0,"pending_fact_count":0,"superseded_fact_count":0,"open_gap_count":2}
```

打开输出的 `知识库目录.md` 阅读，写作时先匹配对象和项目，再使用索引中 `status=supported` 的当前事实。缺资料只追问会改变归属、版本或写作结论的关键项，其余先完成并列清单。没有 Python 的环境仍可让 Agent 直接输出同结构的 Markdown/JSON，并说明未执行脚本校验。

## 更新与失败边界

同一目录增量导入不会删除未出现在新输入中的原资料。新增内容使用新来源ID和新事实ID，重复导入相同资料保持不变；同ID内容改变会失败。相同事实的来源会归并；同属性不同值且项目重叠时保留双方并标冲突，不能直接进入写作。

```sh
python3 scripts/knowledge_base.py build --input examples/update.json --output brand-kb
python3 scripts/knowledge_base.py build --input examples/resolution.json --output brand-kb
```

第一条演示第二版交付格式与原记录产生冲突，得到 2 条冲突事实。第二条演示资料负责人已确认采用第二版后，用明确的 `supersedes` 关系解决冲突；旧原文和记录仍保留。真实任务需要 Agent 核实版本适用性，不能把示例中的确认当成用户授权。

跨项目旧事实适用 A、B，但仅 A 更新时，同次导入 A 新值与 B 原值两条新记录，各自明确替代旧记录。两者必须合计覆盖旧范围；只新增窄范围事实仍可能冲突，遗漏 B 的替代会被拒绝。可复制以下命令在独立目录复现：

```sh
python3 scripts/knowledge_base.py build --input examples/project-split-input.json --output split-kb
python3 scripts/knowledge_base.py build --input examples/project-split-update.json --output split-kb
python3 scripts/knowledge_base.py build --input examples/project-split-resolution.json --output split-kb
```

中间产生 2 条冲突事实，[完整拆分输入](examples/project-split-resolution.json)导入后的实际结果为：

| 事实 | 适用项目 | 值 | 状态 |
| --- | --- | --- | --- |
| `a-current` | A | `Markdown+JSON+CSV` | `supported` |
| `b-current` | B | `Markdown+JSON` | `supported` |
| `shared-v1` | A、B | `Markdown+JSON` | `superseded` |
| `a-update` | A | `Markdown+JSON+CSV` | `superseded` |

来源 2 份、原记录 4 条、可用事实 2 条、历史事实 2 条、冲突 0 条，原文与旧记录保持保留。替代关系、直接拆分及遗漏未变更项目的失败复现见[数据约定](references/data-contract.md#跨项目事实只更新一个项目)。

无来源却标记有证据的[失败输入](examples/failure-unsupported.json)：

```sh
python3 scripts/knowledge_base.py build --input examples/failure-unsupported.json --output rejected-kb
```

退出码为 `2`，不会创建知识库；[实际错误样例](examples/failure-output.json)：

```json
{"status":"error","message":"有来源支持的事实必须提供可定位的来源摘录"}
```

脚本还会拒绝不存在的摘录、未知对象/项目、路径越界、错误目标库、循环替代及覆盖人工改过的受管正文。用户新增的手写文件会保留。已生成正文要修改时，先保存人工改动并将其作为新来源导入。摘录匹配不等于语义核实：Agent 仍须检查原文是否支持正文、数据时间和适用条件。脚本单文件原子写入，不提供整库事务；避免并发写同一知识库。

运行可离线复现的业务测试：

```sh
python3 scripts/self_test.py
```

测试验证真实归并结果、全量样例、来源保存、增量冲突与替代、跨项目完整拆分和范围边界，以及失败时不覆盖资料；不检查图标和根目录许可证文件。它不调用外部账号或服务。

## 参考来源与实际增强

参考 [@user_1831d4fb/geo-kb-creator 1.0.1](https://skillhub.cn/skills/user_1831d4fb/geo-kb-creator) 的功能设计，保留按企业身份、产品、信任材料、用户问题及转化信息组织资料，以及复用已有库并核对对象的优点。

本技能独立写作与实现：默认生成实际本地正文和机器索引；逐条保存来源、状态和适用项目；归并重复材料并保留出处；增量保留原文、识别冲突、显式处理替代；按已有内容精简分类并区分公司/产品/主题。当前 Agent 可沿正文与索引把可用事实接到 aimeGeo 内容制作，不假设存在自动知识库同步。参考包未核实可复制许可，未复制其代码、大段文本或 Logo。原创实现采用 MIT-0，详情见 [LICENSE](LICENSE) 与含完整许可的 [NOTICE.md](NOTICE.md)。项目仓库：[aimegeo-brand-knowledge-base](https://github.com/xxjrq/aimegeo-brand-knowledge-base)。

本技能整理的是事实源，不执行 GEO 查询，不保证 AI 收录或固定提升幅度。若另有检测材料，只描述实际回答、提及和原生引用；模拟、未运行与查询失败分别保留，不能当作零引用结果。

当前版本：1.0.2。
