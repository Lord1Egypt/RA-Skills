# instantiation — 样例技能 · 派生 · 改造

> 目标：把「做过一次」变成「下次十分钟」。
> 跑完一期刊（或做顺一次样式）后，`+spec` 生成一个专属子技能 `journal-<企业>-<类型>`。

## 〇、先看成品：随包样例技能

父技能的 `examples/` 目录里有**已经派生好的成品**，例如
`examples/journal-qiming-regional/`（源刊：启明《区域观察》第 21 期）。

在读下面的流程之前，建议先翻一遍那个目录——**看生成物比看方法论快**。它同时也是
你自己派生时的对照样本：别人的产出长什么样，你的就该长什么样。

样例的三种用法：

| 用法 | 怎么做 | 适合谁 |
|---|---|---|
| 直接安装 | 整个目录拷进 `~/.workbuddy/skills/` | 就想试试这套流水线 |
| 照着改造 | 按样例里的 `README.md` 逐项替换 | 有自己的刊物，想省去摸索 |
| 只作参考 | 只读 `assets/examples/qiming-regional-sample/unit-patterns.md` | 想搞清楚「单元模板」到底要写多细 |

**samples 和 examples 别混**：

- `assets/examples/<样例>/` —— 学习过程的**中间产物**（stylespec / semantic / unit-patterns），用于调试 `+learn`；
- `examples/<技能名>/` —— 学习完成后的**成品技能**，可直接安装、改造、分发。

## 一、为什么要派生

框架层每次都要重新：读样例 → 抽 StyleSpec → 合并网格 → 猜模板用途 → 重问一遍固定件。
这些**同一家公司的同一本刊物，第二期全都一样**。派生的本质就是把这些钉死。

代价对比：

| | 第 1 期（走框架） | 第 2 期起（走派生） |
|---|---|---|
| 用户要提供 | 样例 + 素材 + 3 轮确认 | 素材 + 1 轮确认 |
| +learn | 20–40 分钟 | **跳过**（已钉死） |
| +gather | 全量探索 | 照上次的数据源清单走 |

## 二、派生技能的目录

`scripts/derive_skill.py` 的实际产出（**不要手写**，手写十几份文件必然漏项）：

```
~/.workbuddy/skills/journal-<企业>-<类型>/
├── SKILL.md                    # 精简流程：Parent 兜底，日常不再跑样式学习
├── README.md                   # **改造指南**：哪些钉死别动、哪些每期必改、怎么换成自家
├── scripts/
│   └── build_draft.py          # 由父技能拷入 —— 派生技能必须自包含，不能依赖父技能路径
├── assets/
│   ├── stylespec.json          # 钉死的版式（已剥离 semantic，体积约减半）
│   ├── unit-patterns.md        # 钉死的 UnitPattern + 语料
│   ├── fixed-pieces.md         # 页眉 / CTA / 免责声明 / 名录
│   ├── glossary.md             # 术语与实体表（待填「统一写法」列）
│   └── last-issue.md           # 上期目录与篇幅基线 —— 给新一期定容量
├── sources.template.md         # 待填：官网 / 公众号 / 监管机构 / Cue 搭子
└── runbook.template.md         # 待填：额度经验、踩坑、用户偏好决策
```

带 `.template` 后缀的表示**派生时没有真值，必须人工填**，填完去掉后缀。

生成命令：

```bash
python3 ~/.workbuddy/skills/journal-draft/scripts/derive_skill.py \
    --spec ./qiming-regional-sample/stylespec.json \
    --unit-patterns ./qiming-regional-sample/unit-patterns.md \
    --out ~/.workbuddy/skills/journal-<企业>-<类型> \
    --name journal-<企业>-<类型> \
    --slug journal-<企业>-<类型> \
    --publisher "<发行方全称>" \
    --title "<刊名>" --kind "<双月刊 / 内刊 / 年报>" \
    --alias "<别名，多个用 / 分隔>"
```

`--spec` 里的 `semantic` 段会被剥掉：那是一次性的学习产物，派生后不再需要。

### 派生出的 SKILL.md 自带发布字段

`--slug` / `--name` / `--publisher` / `--title` 会被自动写成
`slug` + `displayName` + 顶层 `version` + `summary` + `tags`，
所以子技能**可以直接独立发布到技能市场**，不必事后手改 frontmatter。

- 平台（skillhub.cn）的**硬校验只有三个字段**：`slug`（kebab-case，2–128，全网唯一）、
  `version`（合法 SemVer）、`displayName`。`summary` / `description` / `tags` / `license` /
  `homepage` 官方明确写「建议检查但**不作为发布阻断**」。
- `--slug` 不传则取 `--name`；含大写、下划线、空格时会被规范化成 kebab-case 并打印 `[NOTE]`。
  **被平台占用了（`409`）就在 `--slug` 里加 handle 前后缀重跑**，不要去手改目录名。
- `--title` 不用带书名号；带了也会被去掉（曾渲染成 `《《刊名》》`）。
- 派生出来的子技能是**自包含**的：`scripts/`（11 个，排除 `derive_skill.py` 自身）与
  `assets/templates/`、`assets/diagram-templates/` 都随包拷贝，换台机器直接能跑；
  只有 `references/` 留在父技能里（会随框架演进，拷一份会立刻过期）。

## 三、SKILL.md 怎么写

子技能的 description 必须**能被自然触发**，并且明确指向 parent 做兜底：

```yaml
---
name: journal-<企业>-<期刊类型>
description: "<企业全称><刊名>的期刊底稿技能。Triggers: <刊名> 新一期 / 做<N>期 / <企业>内刊 / <别名>。已固化 StyleSpec 与 UnitPattern，直接跳到需求对齐；需要通用排版能力时回落到 journal-draft。"
license: MIT
agent_created: true
metadata:
  version: "0.1.0"
  parent: "journal-draft"
  pinned_spec: "stylespec.json"
---
```

正文只要三段：

1. **身份**：哪本刊、给谁看、多少页、几期一轮。
2. **固定动作**：每期必做什么（哪些固定件照抄、哪些必须核对、哪些每期重取）
3. **入口**：本期直接进 `+brief` 开工，不必重跑样式学习；若用户带了新样例或要求改版，再回落到父技能的样式提取。

`spec_confidence` 三档由脚本自动判定，直接写进 frontmatter：

| 档位 | 判据 | 能不能投产 |
|---|---|---|
| `pinned` | 结构识别 high **且**有人工定稿的 unit-patterns.md | 能 |
| `drafted` | 结构识别 high，但 UnitPattern 只有机器草稿 | **不能**，须先人工定稿 |
| `weak` | 结构识别置信度不足 | **不能**，须重跑 `+learn` |

脚本在这一档不是 pinned 时会在 stdout 打 `[WARN]`，并在生成的 `unit-patterns.md`
顶部加显眼警示。**不把未验证的推断伪装成定稿**——这条是所有自动化产出的底线。

## 四、钉死什么、不钉死什么

**钉死**（跨期几乎不变）：
- StyleSpec 全文、网格、色板、字号表
- UnitPattern 与语料、固定件全文
- 编辑部名单模板、联系方式模板、免责声明全文
- 该企业的官网栏目 / 公众号 / 年报路径
- 常用 Cue 搭子清单 + 每篇的额度经验值
- 术语表与禁用词

**不要钉死**（每期必变）：
- 期号、年月、封面图、当期话题
- 新的第三方评价 / 榜单引用
- 人员增减、联系方式变动
- 当期热点与 deadline

## 五、沉淀动线

```
跑完一期
  ├─ stylespec.json + unit-patterns.md（定稿版）→ 拷进子技能 assets/
  ├─ content.json + copy/                      → 拷进 last-issue/ （下期最好的语料）
  ├─ evidence/index.csv                        → 提炼出 sources.md 里好用的入口
  ├─ review.md 里的「阻塞项」                   → 写进 runbook.md 的踩坑与必查清单
  └─ 用户的偏好决策（哪类问题他总回答默认值）   → 写进 SKILL.md 的默认建议
```

## 六、什么时候别急着派生

- 只做过一期、还没拿到企业正式反馈 → 先跑第二期，用户说「就按这个来」再派生
- 刊物本身在改版中 → 样式未定，派生会马上过期
- 用户只是想看看效果 → 派生会把尚未验证的偏好过早固化

派生是承诺：一旦钉死，后续就会照它执行。**样式定了再派生。**
