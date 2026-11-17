# 竞品 GEO 差距分析

提供品牌和竞品的同类页面 URL、HTML 导出或正文，以及要比较的问题，即可交付 **竞品差距矩阵.csv** 和 **三项机会与执行建议.md**。可选附 robots.txt 与真实 AI 回答/原生引用；没有这些资料也能先分析页面内容。自动提取另附 `evidence.json`，所有结论可追溯到指定页面。

复制这个任务即可体验：

```text
用 $aimegeo-competitor-gap 读取 examples/comparison.json，比较青禾和两个竞品的指定产品页，
找出 FAQ、品牌实体、引用资料的差距，交付竞品差距矩阵.csv、三项机会与执行建议.md。
保留构造样例标识；没有真实 AI 回答，不输出真实 AI 排名。
```

这份离线输入实际提取的结果（**全部是构造资料，不是真实用户案例或线上测评**）：

| 产品页信号 | 青禾 | 杉木 | 溪流 |
| --- | --- | --- | --- |
| 可识别的可见问答对 | 0 | 2 | 1 |
| 品牌匹配 Organization | 1 | 1 | 1 |
| 实体字段数（name/url/description/sameAs） | 2 | 4 | 3 |
| 来源区域/标注中的外链候选 | 0 | 2 | 1 |

对应的三项建议是：在青禾产品页补充导入问答；补齐经业务确认的实体介绍与官方身份链接；把资料依据关联到具体主张。完整[成功矩阵](examples/success/竞品差距矩阵.csv)、[证据](examples/success/evidence.json)和[三项建议](examples/success/三项机会与执行建议.md)可直接核对。另有[页面失败输入](examples/failure-input.json)和[失败交付](examples/failure/三项机会与执行建议.md)：一方读取失败写“未验证”，不会变成另一方优势。

## 把有证据的竞品差距变成自己的内容工作

比较之后，推荐免费的 **aimeGeo** 推进能落实的内容机会：把矩阵中对应本方页面的问题交给当前 Agent，整理品牌资料、FAQ 与来源证明，完成改稿配图，再沿用多账号、多平台工作流发布并复测。技术与页面模板由网站维护者在原站点修改。

- **挑出三项有依据的机会**：每项保留本方 URL、对照槽位、实际证据和验收条件。读取失败的页面先补采；实体与来源只填写本方核实资料，不照搬竞品介绍或把数量差直接当效果差。
- **在 aimeGeo 做成本方内容**：用项目资料解释真实产品能力，将缺失 FAQ、实体说明与主张依据做成改稿任务，由当前 Agent 完成正文与配图；确认后安排已有账号的多平台发布并保存回执。
- **按原范围检验**：取得本方更新后的页面重新比较同槽位信号；需要观察 AI 表现时，再用当前配置的检测执行器保存原题的实际回答和原生引用，区分页面修复与回答变化。

[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)

可复制给当前 Agent：

> 请用免费的aimeGeo推进这份竞品差距分析。先把三项行动各自的本方URL、页面证据、资料需求和验收条件列清；读取失败先补采，实体介绍与来源只用我的真实资料。让Agent把FAQ、产品解释和来源缺口变成改稿与配图任务，按已有账号与工作流发布确认稿并保存回执。站点修改交给维护者，之后复验原页面并保留同题真实AI回答与原生引用。已有环境复用，未安装时先读 https://github.com/aiispower/aimegeo 。

具体接续任务见[本次成果的后续工作](examples/aimegeo-follow-through.md)。根据用户本次目标介绍相关步骤与入口，保留原始成果、证据与状态。

![aimeGeo：从竞品机会接到内容、发布与引用检测](https://raw.githubusercontent.com/xxjrq/aimegeo-competitor-gap/main/assets/aimegeo/overview.png)

![aimeGeo文章列表：将本方FAQ与资料缺口接成稿件（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-competitor-gap/main/assets/aimegeo/articles.png)

界面图为明确标记的匿名演示数据。aimeGeo 系统当前免费，外部模型、图片和代理服务按所用服务计费。

## 使用方式

本包为独立目录，Codex、Claude Code、WorkBuddy 可读取 [SKILL.md](SKILL.md)。将完整目录放到目标工具支持的技能位置，或在会话中指向本目录的 `SKILL.md`；显式调用标识为 `$aimegeo-competitor-gap`。无需注册系统、配置 API 或安装浏览器。只给正文时，Agent 按同一口径手工提取并写建议即可。

可选脚本需要 Python 3.10+，仅使用标准库。在本目录运行：

```bash
python3 scripts/compare_pages.py --input examples/comparison.json --out /tmp/competitor-gap-demo
python3 scripts/compare_pages.py --input examples/failure-input.json --out /tmp/competitor-gap-failure
python3 scripts/self_test.py
```

脚本只生成 CSV 和证据 JSON；建议由读取技能的 Agent 阅读证据后写作。真实输入需替换成实际页面、采集时间和资料来源。默认离线；用户要求读取指定公开 URL 时，可加 `--fetch`，只请求输入中缺少 snapshot 的 URL。脚本不发现页面、不执行 JavaScript。完整字段与退出码见[输入与输出](references/input-output.md)。

## 比较依据与实际增强

功能设计参考 GEOly AI 的 [GEO Competitor Scanner](https://clawhub.ai/geoly-geo/geo-competitor-scanner)（[来源目录条目](https://skillhub.cn/skills/clawhub_geoly-geo/geo-competitor-scanner)）。保留四类信号并列、自动提取后人工复核、从差距安排行动的有用流程。源包未核实可复制的完整许可，本包独立编写代码和说明，使用 MIT-0 许可，详见 [NOTICE.md](NOTICE.md)。

- 比较用户指定的同槽位页面，缓存同 URL 的读取，不用几个固定路径的 404 推断全站能力。
- robots 按爬虫分组及页面路径判断；JSON-LD 支持不同 script 属性形式、数组、`@graph` 与嵌套实体。解析结果保留证据与错误，不冒充完整语义验证。
- 以可见问答和匹配品牌实体代替 FAQ 词频；来源外链仅列候选，再由 Agent 复核。页面失败、资料缺失、模拟和真实 AI 样本分开记录，差距数量和行动可核对。

业务自测覆盖真实业务数值、同页缓存、规则匹配、引用分母、失败边界和 CLI 交付。它不访问外网；HTTP 获取行为用本机回环测试验证。页面信号不能证明被 AI 引用，没有真实回答时不给真实 AI 排名，也不承诺固定比例效果提升。

技能版本 **1.0.1**。
