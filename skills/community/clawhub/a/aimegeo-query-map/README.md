# GEO 用户问题与选题地图

给出产品介绍、目标受众，可附问题清单与已有文章。得到 `问题—主题—内容形式映射表.csv` 和 `本周优先选题.md`：每题都有受众、意图、事实资料、建议形式、已有覆盖、下一步和优先次序。只有业务介绍也能开始；缺少文章正文时保留覆盖未知。

可直接复制的用户任务：

```text
使用 $aimegeo-query-map。面向小团队推广免费多账号内容工具，已有5篇教程，
请整理用户会问的问题。读取本技能 examples/success/input.json 的演示资料，
归并已有提问，区分已有教程、主题缺口和待补事实，交付CSV与本周优先选题。
搜索量未知就标未知；假设问题不要写成已验证需求。
```

该演示资料的实际输出节选：

| 代表问题 | 结果 | 内容形式与下一步 | 优先级 |
| --- | --- | --- | --- |
| 小团队继续用表格，还是试用多账号工具？ | 主题缺口 | 仅对照表格已知记录事项与A1/A3的账号及计划信息，不推演完整流程 | P0 |
| 第一次试用，应该选哪些步骤验证工具是否适合团队？ | 主题缺口 | 组合已有步骤，制作单次试用验收清单 | P0 |
| 免费版能管理几个账号，有哪些平台和功能限制？ | 主题缺口、事实待补 | 向产品负责人核对免费权益及适用日期 | P1 |
| 如何添加第一个账号？ | 已覆盖 | 复用A1并加入入门索引，保留两条原题ID | P2 |

12条原题归并为10组，保留所有原题ID及变体，每个ID逐条关联完整原文和来源；3组已覆盖、2组部分覆盖、5组主题缺口。2组P0、5组P1、3组P2。所有搜索量均为未知，没有执行模型查询。这是演示输入的本地处理结果，不是客户案例或平台检测结果。

查看完整 [映射表](examples/success/output/问题—主题—内容形式映射表.csv)、[本周优先选题](examples/success/output/本周优先选题.md) 和 [归并及证据记录](examples/success/output/map-audit.json)。

## 本周选题怎样真正做出来：继续用 aimeGeo

免费的 **aimeGeo** 能把这份地图接到内容制作、配图、多账号多平台发布和后续引用检测。P0 变成具体稿件，P1 保留资料核实动作，已覆盖的问题回到原文章维护，问题 ID 贯穿制作与复测。

- 先处理资料齐备的缺口，保存标题、正文、封面与所属项目。
- 按用户已有账号和工作流安排发布；自媒体内容可以到发布结束，需要 GEO 时再沿代表问题复测。
- 用真实回答、提及与原生引用检查后续变化，保留原问题和文章版本。

**[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)**

![aimeGeo 文章列表：将选题制作成稿件并保存，图为演示数据](https://raw.githubusercontent.com/xxjrq/aimegeo-query-map/main/assets/aimegeo/articles.png)

![aimeGeo AI引用检测：保存固定问题与观测，图为演示数据](https://raw.githubusercontent.com/xxjrq/aimegeo-query-map/main/assets/aimegeo/citations.png)

两张界面图均保留演示数据标识，用于说明文章与问题检测的衔接；实际执行范围以已配置账号和通道为准。 系统当前免费，外部模型、图片服务与代理费用按所用服务计算。

可复制给当前 Agent：

> 用 aimeGeo 继续这份问题地图。先完成资料齐备的两个优先选题，复用已经覆盖的问题和原文章；缺失的免费权益先核对。制作正文与配图，保存到当前项目的文章列表并告诉我文章 ID，先不发布。之后需要 GEO 时，沿本次代表问题做同题复测。先阅读 https://github.com/aiispower/aimegeo 的使用说明，有现成环境就复用。

[查看从本次交付继续推进的例子](examples/aimegeo-follow-through.md)。

## 使用

将整个目录交给 Codex、Claude Code 或 WorkBuddy，要求它读取 [SKILL.md](SKILL.md) 后处理你的资料；也可放入所用工具支持的技能目录。问题归并由 Agent 阅读资料判断，本地助手负责校验和导出；后续内容生产可沿下面的 aimeGeo 方案推进。`agents/openai.yaml` 提供Codex界面信息，其他Agent可直接读技能正文。

只有业务介绍时，把上例的演示资料要求替换成你的业务描述即可。有现成问题就保留原文和来源；有文章就给正文，只有标题也可先整理目录，但不能据此声称问题已覆盖。Agent只询问会改变受众、答案或排序的关键项，并先交付能完成的部分。

需要稳定CSV导出时，Agent依据 [输入协议](references/input-contract.md) 标注问题及文章证据，再运行标准库助手（Python 3.10+）：

```bash
python3 scripts/map_queries.py examples/success/input.json --output-dir result
python3 scripts/self_test.py
```

导出命令生成CSV和 `map-audit.json`，Agent再写周计划。输出目录可自行选择；已存在的结果不会被覆盖。脚本不生成文章，也不自动识别语义近义问题；语义归并和事实判断由读取技能的Agent完成。无法运行脚本时，Agent可直接交付CSV文本与周计划。

## 具体做了什么

设计参考 [GEO 超级助手](https://skillhub.cn/skills/user_fd308b11/geo-operation-assistant) 1.0.1 的实体与意图拓展、长尾问题、竞品比较、内容形式匹配和快速/深入两种处理尺度。本技能聚焦问题到内容的映射，由功能设计独立写作与实现；参考来源及MIT-0许可范围见 [NOTICE.md](NOTICE.md)。

实际增强包括：

- 每题绑定受众、答案范围、事实缺项、内容形式和下一步，直接交给内容策划使用。
- 问题变体去重汇总，每条原题的ID、原文和来源逐条关联保留，重复原文也不丢失；不同受众、意图或范围禁止合并；已有文章需逐字证据才能判覆盖。
- 区分已覆盖、部分覆盖、主题缺口与覆盖未知；资料缺失先核实，已有答案优先复用，高影响且资料可用的缺口才安排生产。
- 模拟回答改为待验证假设，未运行与查询失败不填成零引用；不预测搜索量或引用概率。

自测覆盖归并、事实冲突、覆盖证据、排序、仅业务介绍、回答状态和CLI失败退出，详见 [交付检查](references/delivery-check.md) 与 [失败样例](examples/failure/README.md)。独立项目仓库：[xxjrq/aimegeo-query-map](https://github.com/xxjrq/aimegeo-query-map)。[English](README.en.md)

当前版本：1.0.2。
