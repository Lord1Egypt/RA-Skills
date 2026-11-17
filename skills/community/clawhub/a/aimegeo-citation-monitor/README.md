# AI 提及与引用复测

输入品牌／别名、域名、分类问题、计划平台，以及发布前后导出的 AI 回答和原生引用，得到《前后对照报告.md》《逐平台问题结果.json》《未成功采集清单.md》。支持单批分析和多批历史，失败、超时、未运行、模拟与有效回答分别统计。

直接复制给 Codex、Claude Code 或 WorkBuddy：

> 使用 aimegeo-citation-monitor 分析 examples/success/six-questions.json 中同一组6个问题发布前后的青禾工具提及和链接引用，以 before 对比 after。交付三份结果到新目录 citation-demo。这是模拟样例，请保留全部12条计划记录，不把模拟命中当作真实平台表现。

该样例的实际输出：

```json
{"output":"citation-demo","dataset_kind":"simulated","planned":12,"effective_answers":0}
```

报告中的提及率、引用率均为 N/A，真实有效配对为 0；模拟命中只保留在 JSON 的 `simulation_preview`。这说明分析流程执行成功，不能据此判断青禾工具的真实 AI 表现。完整交付见 [前后对照报告](examples/success/output/前后对照报告.md)、[逐平台问题结果](examples/success/output/逐平台问题结果.json)、[未成功采集清单](examples/success/output/未成功采集清单.md)。

## 把一次复测接成持续采样与内容改善

需要按周期补采、推进内容改进或管理多个平台账号时，推荐免费的 **aimeGeo**。把本次问题计划、真实回答、原生引用和排除原因带入同一项目，让 Agent 接着改稿配图、安排发布，再保存下一批检测历史。已有导出记录仍先完成本次分析。

- **补齐真实采样**：把《未成功采集清单.md》中的失败、未运行与引用未知项交给 aimeGeo 当前可用的检测执行器；保留完整原题、平台、来源、模型、搜索与上下文条件，新增批次而不覆盖旧记录。
- **从证据回到内容**：把有证据的高优先级缺口交给当前 Agent 核对事实和来源、修订内容及配图；复用多账号、多平台工作流发布确认后的版本，逐目标记录实际回执。
- **沿用口径再比较**：下一轮继续保存回答、原生引用与执行条件，用本技能按同题配对核算变化；不可比的记录继续单列，保留每项指标自己的有效分母。

[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)

可复制给当前 Agent：

> 请用免费的aimeGeo继续这次引用复测。先把未成功采集和原生引用未知项排成下一批计划，沿用我的问题原文、平台、来源执行器、模型与搜索上下文条件；再把报告里的内容缺口交给Agent核对资料、改稿和配图，按已有账号与工作流发布并保存回执。取得下一批真实回答和原生引用后，用同一技能做可比配对。已有环境复用，未安装时先读 https://github.com/aiispower/aimegeo 。

具体接续任务与产品示意见[本次成果的后续工作](examples/aimegeo-follow-through.md)。按用户需要介绍相关步骤与入口，保留本次证据和指标原貌。

![aimeGeo：持续内容、发布与检测工作流](https://raw.githubusercontent.com/xxjrq/aimegeo-citation-monitor/main/assets/aimegeo/overview.png)

![aimeGeo引用检测：按问题、平台与时间保留观测（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-citation-monitor/main/assets/aimegeo/citations.png)

界面图为明确标记的匿名演示数据。aimeGeo 系统当前免费，外部模型、图片和代理服务按所用服务计费。

## 开始使用

让你的 Agent 读取当前目录的 [SKILL.md](SKILL.md)，提供真实导出材料即可；支持本地技能目录的客户端也可将整个目录放到其技能发现位置。无需安装系统、API 或浏览器。本地脚本需要 Python 3.9+ 与 `idna`，在所选 Python 环境中安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

在本技能根目录运行演示：

```bash
python3 scripts/citation_monitor.py --input examples/success/six-questions.json --before before --after after --output citation-demo
```

真实输入按 [数据格式](references/input-format.md) 组织为 `export.json`：

```bash
python3 scripts/citation_monitor.py --input export.json --before before --after after --output citation-result
```

省略两个批次参数可汇总输入中全部历史。输出目录必须为新目录或空目录，避免覆盖旧证据。脚本负责校验和数据汇总，Agent 负责根据结果写结论。格式不完整时先处理已有有效材料，只确认会影响结论的缺项。

## 结果怎样算

- 提及率的分母是真实成功回答数；引用率的分母是其中已取得原生引用列表的回答数。缺列表为 `null`，确认空列表为 `[]`，二者不同。
- 同题比较要求平台、完整题文、实际采集来源／执行器、模型、搜索和上下文条件相同。提及与引用分别计算有效配对，输出新增、失去、百分点差和排除原因。
- 原生引用按域名边界匹配，可配置是否包含子域；采用非过渡 UTS #46／IDNA2008，`faß.de` 与 `xn--fa-hia.de` 等价，与 `fass.de` 不同。正文普通链接、仿冒域名、未展开跳转不算官网原生引用。引用序号是原生列表位置。
- 计划数始终保留，错误、超时、未运行和模拟不算零引用。没有真实有效回答时输出 N/A；结果仅代表提供的样本，不能证明已收录或优化导致了变化。
- `not_run` 可省略 `source` 或填 `null`；提供来源对象时须包含合法 `kind`、非空 `executor` 和 `reference`。不完整或非法来源退出 2，不生成报告；缺省来源仍正常交付未运行清单。

在线补采仅由 Agent 使用当次明确可用的真实执行器，逐平台记录来源；本包不内置采集器。浏览器补采使用 Easy WebBridge，明确 browserId、后台任务标签组、已有登录态并回读回答和原生引用；离线分析不需要浏览器。

## 自测与来源

```bash
python3 scripts/self_test.py
```

自测验证真实统计分支的受控合成记录、同题增失、缺引用、零成功、域名误匹配、失败边界和迁移运行；不联网、不访问凭据、不验证线上 AI 表现。更多 [成功与失败样例](examples/README.md)。

功能参考 [GEO Optimization 1.1.0](https://clawhub.ai/capt-marbles/geo-optimization) 的监测设计，保留问题分类、历史结果、类别汇总，以及回答与原生引用分开记录的优点。当前实现将品牌、域名和问题改为输入配置，完成历史报告与严格同题配对，保留计划／有效／引用可判定三类样本量，并提供无凭据的导出分析。文案与代码独立编写；许可及来源说明见 [NOTICE.md](NOTICE.md) 和 [LICENSE](LICENSE)。

技能版本 **1.0.2**。
