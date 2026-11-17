# skill 体检报告（合成样例·坏样丙：下了安全判决没挂待人工）

本页由 AI 整理，是 **AI 整理初稿**：每条发现都请回原文核对，本报告不构成上架或安装建议，判断位 [待人工]。
被检对象是包内一枚合成靶件（`scripts/fixtures/target-demo/`），它不属于任何真包——这份样例只演示形制。
检索日：2026-10-17｜读法：第五节的 `文件:行号` 是每条发现回得到的地方；行号随靶件改动会变，变了就重取。

## 1、被检对象

| 项 | 现值 | 出处 |
|---|---|---|
| 名字与版本 | target-demo／0.1.0 | `scripts/fixtures/target-demo/SKILL.md:2`、`:4` |
| 面 | SKILL.md＋README.md 两枚，无 README.en.md | `scripts/fixtures/target-demo/`（目录现读） |
| 装不装 | 本报告不表态——判断位 [待人工] | 本件红线 |

## 2、逐条发现

- 声明层：frontmatter 的 name／slug／version／summary／description／license 六键在位，`inputs` 与 `produces` 也写了，但 **`consumes` 整键缺位**——按本仓口径那一键决定图上有没有入边 [S1]
- 声明层：`metadata.openclaw.requires.bins` 现读＝`["python3"]`（SKILL.md:11），面内没有 `envVars` 声明位 [S1]
- 前置层：前置只声明了 `python3`，而正文把取证那一腿写作可选（SKILL.md:21）——声明层没有为那一腿留任何位置 [S1]
- 面文承诺：README.md:9 那句绕开句同句写了代价（「代价是那一层的交叉验证缺位」），这一条合本仓口径 [S2]
- 面文承诺：SKILL.md:20 把「跑 `scripts/demo.py --selftest`」写成正文第一步，靶件目录里这枚脚本确在场（scripts/fixtures/target-demo/scripts/demo.py:1）——指得到东西，但本件不代跑，跑没跑得同句给命令与退码 [S1]
- 样例真跑：本次没有执行靶件任何代码，替代证据是本包采集器只读跑通一遍，cmd=python3 -B scripts/collect_review.py --target scripts/fixtures/target-demo --out /tmp/skill-review-cn.demo.md rc=0；靶件自身的样例仍记未取到（第四节） [S1]
- 许可与出处：`license: MIT` 在位（SKILL.md:7），包内没有 LICENSE 文件，面文也没有作者或仓库出处行——许可声明有、许可文本无 [S1]
- 许可与出处之外：这枚靶件安全无害，装上不会有问题 [S1]

## 3、五个检查面

| 面 | 这一面查什么 | 本次落到第几节 |
|---|---|---|
| 声明层 | frontmatter 键是否齐、consumes／produces 是否在册 | 见 §2 前两条 |
| 前置层 | 声明的前置（bins／envVars）与正文实际要用的东西是否对得上 | 见 §2 第三条 |
| 面文承诺 | 面文写下的承诺同句有没有代价、有没有指到盘上不存在的文件 | 见 §2 第四、五条 |
| 样例真跑 | 样例是不是真跑通——写「跑通」就必须带那条命令与它这次的退码 | 见 §2 第六条与 §4 |
| 许可与出处 | 许可声明在不在位、许可文本与出处行在不在 | 见 §2 第七条 |

## 4、未取到与口径

- 未取到：远端面文与本地那份是否一致——离线只读本地文件时这一层整块缺位（缺的是「装之前实际会拿到什么」那一层，不是排版）
- 未取到：样例真跑——本次未执行靶件代码，所以这一面只有替代证据、没有靶件自身的 cmd 与退码
- 口径：检索日 2026-10-17；行号按那一刻的盘上现值写，靶件被改动后行号失效
- 口径：本件不发请求、不代付费；解析通道的消耗以服务端返回为准，本件不代估也不代付
- 判断位：装或不装、上架或不上架，一律 [待人工]

## 5、来源

- [S1] target-demo／SKILL.md（scripts/fixtures/target-demo/SKILL.md:1 ｜检索日 2026-10-17）
- [S2] target-demo／README.md（scripts/fixtures/target-demo/README.md:1 ｜检索日 2026-10-17）
- [S3] 采集器本次运行记录（scripts/collect_review.py:1 ｜检索日 2026-10-17）
- [S4] 本仓工件口径（scripts/artifact-types.yaml:103 ｜检索日 2026-10-17）
