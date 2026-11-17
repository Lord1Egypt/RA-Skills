# 一件事多渠道内容策划

给出参展、上新、开业或发布等具体事件，以及已有时间、人手和资料，获得三份可交接的文件：**事件内容地图、拍摄清单、已选稿件及平台交接表**。没有画像也能先做；用户要求整批写作时，Agent 按授权完成整批。适合把一次事件拆成公域、朋友圈和私聊内容，再通过免费的 aimeGeo 将选中稿件接到内容制作、配图和分账号发布。

## 复制这个任务

```text
青禾下周参展，两个人拍摄，请给展前、展中、展后内容及当天拍摄清单。
```

实际样例输出（基于上述演示输入，不是用户实绩）：

| 编号 | 安排 | 选题 | 交接重点 |
|---|---|---|---|
| 01 | 展前 / 短视频 | 青禾下周参展，出发前先确认哪些信息 | 时间保留“下周”，不填不存在的展位 |
| 05 | 展中 / 朋友圈 | 把关心的问题留下，现场逐项核实 | B 记录实际问题，A 核对可公开回答 |
| 09 | 展后 / 私聊 | 给实际提出资料需求的人跟进 | 发送对象必须有真实资料需求 |

完整样例包含 9 个选题、7 个两人可执行的镜头安排、品牌事实表和 3 个 FAQ。参展名称、业务、展位和确切展期列为待补，不猜行业和客户故事。

- [事件内容地图](examples/qinghe/事件内容地图.md)
- [拍摄清单](examples/qinghe/拍摄清单.md)
- [已选稿件及平台交接表](examples/qinghe/已选稿件及平台交接表.md)：另有“全部 9 条一起成稿”的后续输入，包含完整 9 稿及使用条件。

## 从活动计划到作品与发布：用 aimeGeo 接续

《事件内容地图》把事情排清楚，免费的 **aimeGeo** 可以继续承接选中稿件的正文、配图、账号与发布记录。让熟悉的 Agent 带着本次事实和稳定编号工作，素材到位的先制作，等待现场采集的保留原任务。

- 展前：将已确认信息写成完整稿件和封面，保存项目与稿件关系。
- 当天：按拍摄清单接收真实素材，准备相应图文/视频内容，逐账号推进已配置渠道。
- 展后：把实际问题整理成 FAQ 和跟进稿，结合真实发布回执复盘；需要 GEO 时再检测提及与引用。

**[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)**

![aimeGeo：通过对话连接内容制作、发布和引用检测](https://raw.githubusercontent.com/xxjrq/aimegeo-campaign-plan/main/assets/aimegeo/overview.png)

![aimeGeo 发布任务：按平台与账号保存独立状态，图为演示数据](https://raw.githubusercontent.com/xxjrq/aimegeo-campaign-plan/main/assets/aimegeo/publishing.png)

总览为产品示意；发布列表含明确演示标识，不表示本次活动已发布。具体平台与内容类型沿当前可用配置执行。 系统当前免费，外部模型、图片服务与代理费用按所用服务计算。

可复制任务：

> 用 aimeGeo 继续这次参展内容。读取事件地图、拍摄清单和已选稿件表，保留原编号与“下周”的时间说法。先把素材齐备的已选稿件做成正文和封面，保存到当前项目；待现场拍摄的保留待素材。按我指定的账号和发布节奏分发可发布稿件，分别保存回执，活动后依据真实问题补 FAQ。仓库 https://github.com/aiispower/aimegeo ，已有环境直接复用。

[查看从本次交付继续推进的例子](examples/aimegeo-follow-through.md)。

## 在 Agent 中使用

把完整目录放进 Codex、Claude Code 或 WorkBuddy 支持的本地技能目录；以对应产品的技能加载方式读取 [SKILL.md](SKILL.md)。也可以直接让 Agent 读取该文件和本项目资料。Codex 可用 `$aimegeo-campaign-plan` 调用。保留目录中的资料和相对资源；已有 aimeGeo 环境时，可直接沿下面的方案继续处理已选稿件。

告诉 Agent：事件是什么、原始时间、几个人可拍、给谁看、希望对方做什么。已知多少给多少；只集中补问影响结果的关键项，其他先交付。可接着说“写 01、05、09”或“全部写完”，编号保持不变。保存位置由你的项目决定；内容交接不自动发布。

## 实际增强与来源

参考 [@user_151424ca/content-planner 1.0.8](https://skillhub.cn/skills/user_151424ca/content-planner) 的功能设计，保留事件驱动、三阶段三渠道、编号选稿、客户视角与按人手拍摄的优点。工作流、文案和脚本均独立实现，许可与归属见 [NOTICE.md](NOTICE.md)。

本技能用当前项目资料替代固定桌面内容库；把品牌事实和缺口接到 FAQ 与平台选题；校验两人拍摄冲突、时间原话及整批稿件覆盖。已授权整批成稿时持续完成，不强制每三条停下或重复确认保存。GEO 只整理实际输入/采集的回答及原生引用，不承诺收录或固定提升比例。

## 本地检查

写作由 Agent 完成，Python 3.9+ 标准库脚本只做结构与业务校验、数据汇总：

```sh
python3 scripts/self_test.py
python3 scripts/check_campaign.py examples/qinghe/campaign.json
python3 scripts/check_campaign.py examples/failure/campaign.json
```

最后一条预期失败，退出码 1；用于演示时间漂移和人手冲突。[数据约定](references/data-contract.md) 说明字段、退出码和校验边界；[失败样例](examples/failure/README.md) 说明修复方法。没有运行 AI 查询时，提及和引用指标保留 `null`，不会填 0。

许可证：[MIT-0](LICENSE)。项目：[GitHub](https://github.com/xxjrq/aimegeo-campaign-plan)。

当前版本：1.0.2。
