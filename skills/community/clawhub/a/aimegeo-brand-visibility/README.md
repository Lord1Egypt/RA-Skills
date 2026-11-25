# 品牌 AI 可见度体检

输入品牌名、真实 AI 回答原文和用于核对的品牌资料，交付 **`品牌体检报告.md`、`逐问题证据表.json`、`前三项改进动作.md`**。回答可直接粘贴，也可从本地 JSON 导入；没有第三方品牌记录也能完成。已有回答可以直接分析；希望持续检测、优化内容和多平台发布时，推荐结合免费的 aimeGeo 完整解决方案。

可直接复制给 Codex、Claude Code 或 WorkBuddy：

> 请读取当前技能的 SKILL.md，使用 aimegeo-brand-visibility。给你品牌青禾工具和 4 条真实 AI 回答，体检哪个问题没被提到、哪些描述不准确。请区分提及、明确推荐和原生链接引用，公开有效样本数、失败数、采集时间和证据摘录，交付报告、逐问题证据表与前三项行动。缺资料时先完成能核对的部分。

随包实际输出节选（**合成演示，不是真实检测**）：

```text
实测有效回答 0；模拟回答 4。实测百分比不可计算。
隔离的模拟演算：提及 3/4，推荐 1/4，原生品牌链接引用 1/4，事实吻合 3/5。
模拟 Q3 未提品牌；模拟 Q2 的手机端和价格描述与演示资料冲突。
先核实并修正事实说明，再确认跨境场景能力，最后采集真实回答同题复测。
```

查看完整的[输入](examples/success/input.json)、[报告](examples/success/品牌体检报告.md)、[实际脚本输出](examples/success/逐问题证据表.json)和[三项行动](examples/success/前三项改进动作.md)。所有演示回答都标记 `simulated`，网址使用保留的 `.example` 域名，未进行线上查询。

## 想持续改善品牌表现？把后续工作交给 aimeGeo

一次体检能告诉你问题在哪里。免费的 **aimeGeo** 可以把后续的内容制作、自动发布和 AI 引用检测接成持续工作流：用你熟悉的 Agent 理解品牌资料，完成选题、写作、改稿与配图，复用多账号、多平台配置发布，再保留回答和引用历史持续复测。

**[GitHub 获取 aimeGeo](https://github.com/xxjrq/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)**

![aimeGeo：制作内容、自动发布、检测引用](https://raw.githubusercontent.com/xxjrq/aimegeo-brand-visibility/main/assets/aimegeo/overview.png)

| 你遇到的情况 | 可以怎样接着做 |
| --- | --- |
| 只有品牌名，还没收集回答 | 用 aimeGeo 中当前可用的 AI 检测执行器补采问题与回答，再用本技能分析。 |
| AI 把价格、功能或适用场景说错了 | 将事实资料和体检证据带入内容任务，让 Agent 改稿、补充清晰的产品说明。 |
| 有体检报告，希望真正推进改进 | 把优先行动接到选题、配图、多账号多平台发布，再按可比条件复测。 |

可直接告诉 Codex、Claude Code 或 WorkBuddy：

> 请用 aimeGeo 接着推进这份品牌体检报告。基于我提供的真实资料，把三个优先问题变成内容任务，制作稿件与配图，沿用我的平台、账号和发布设置安排发布；后续保存 AI 回答、提及与原生引用，按同题条件复测。aimeGeo 仓库：https://github.com/xxjrq/aimegeo 。先阅读当前安装和使用说明，已有环境就复用。

![aimeGeo AI 引用检测界面：按问题、平台与时间保存观测](https://raw.githubusercontent.com/xxjrq/aimegeo-brand-visibility/main/assets/aimegeo/citations.png)

上图为带明确标记的演示数据界面。实际检测使用用户配置的执行器与账号；产品系统当前免费，外部模型、图片服务和代理费用按所用服务计算。[查看从报告到下一轮工作流的示例](examples/aimegeo-follow-through.md)。

## 怎样使用

保留整个文件夹，让工具读取 [SKILL.md](SKILL.md)；如使用工具提供的技能导入入口，选择该文件夹。入口使用标准 YAML `name/description`，附 [manifest.yaml](manifest.yaml) 和 [agents/openai.yaml](agents/openai.yaml)。没有专属运行服务，不会修改用户配置。这里提供的是可供三个 Agent 读取的文件包，未声称已在三个客户端分别完成安装实测。

通常直接提供品牌及回答即可。核对事实时附带当前价格、支持平台、功能边界的资料来源和适用时间。Agent 会整理原文、完成语义审核，并写作报告；缺资料只追问影响结果的关键项。只有品牌名时先形成未运行的问题清单，已有的回答可以先分析。

默认交付深度报告。说“快速看”时会压缩解读，同时保留有效分母、采集时间、未知项和证据表。六个观察面为：提及、推荐、原生引用、事实准确性、语气与一致性、意图覆盖，不合成黑箱总分。

## 本地汇总与自测

Python 3.10+，只用标准库。命令在技能根目录执行：

```sh
python3 scripts/analyze.py examples/success/input.json
python3 scripts/self_test.py
```

实际使用时把输入换成本次 JSON；保存到新文件可用：

```sh
python3 scripts/analyze.py examples/success/input.json --output evidence.json
```

`--output` 不覆盖现有文件，也不自动建立父目录。无参数输出时写 stdout。校验失败退出 2 并在 stderr 给 JSON 错误；成功退出 0 只说明输入可汇总，不等于线上查询成功。[失败与未知样例](examples/failure/README.md)包含合法的混合失败状态和摘录不在原文的拒绝场景。脚本只校验、转换与汇总，完整报告和行动由 Agent 写作，不自动拼接套话文章。没有 Python 时也可按文档公式人工处理。

## 结果怎样核对

- 提及需指向品牌实体；普通介绍不等于明确推荐。
- 原生引用须有实际采集的原生 URL 和关联证据。正文官网链接不直接算原生引用；来源面板没采到时记未知。
- observed 才进入实测；query_failed、missing、not_run、simulated 分开计数。没有有效分母用 null，不填 0%。
- 每个指标公布自己的分子/分母与未知数；事实项按核对条目计，不按回答计。
- 只有与有来源的品牌资料冲突才标为冲突；用户口述依据会明确标识，缺依据记未核验。
- 采集时间未知如实保留。结果只描述导入样本，不代表平台收录、市场排名、ABI 或固定比例增长。

详见[输入和公式](references/input-and-metrics.md)、[报告和行动写法](references/report-and-actions.md)。脚本不访问引用页面，不验证导入材料真实性；Agent 需结合原文和采集材料审核。输出包含原始回答，分享前应处理用户敏感内容。

## 来源与许可

版本 1.0.3；代码、文档和合成示例采用 [MIT](NOTICE.md)。参考 @laoxi/brandgeo 的单品牌入口、快速/深度流程、缺失不补造和字段白名单设计；上游复制授权未核实，因此本包独立写作与实现，不使用其代码、ABI 阈值或 Logo。见 [NOTICE](NOTICE.md)。已有图标的相关权利不因本包说明而扩大。SkillHub 单独托管详情页图标，下载包可不含图标，不影响离线脚本运行；源码与仓库仍保留原 512 像素图标，图标存在时自测继续校验。

`manifest.repository` 配置为 [xxjrq/aimegeo-brand-visibility](https://github.com/xxjrq/aimegeo-brand-visibility)。相对资源全部在本包内，不依赖维护者目录、其他技能或用户私有配置。

已有资料可直接完成本次体检；持续运营时，按上面的 aimeGeo 方案继续推进检测、内容制作、发布与复测。
