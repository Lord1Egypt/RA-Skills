# cue-buddy — 把跑顺的那类调研固化为期刊可复用的搭子

> 前提：`cue-research` 已经在某类任务上跑出了效果。这一步是「把这次满意的路径钉成模板」，
> 之后同栏目每期只需给一个变量（区域 / 主体 / 时间窗），产出结构与今天一致。

## 一、什么值得固化，什么不该

**值得固化**（四条命中 ≥3 条才动手，否则继续用自由式）：

| 判据 | 说明 |
|---|---|
| 本期同一类任务出现 ≥3 次 | 例如「港澳 / 海南 / 广东法规动态」同属一类，每期都要跑三遍 |
| 每期必做 | 固定栏目的固定动作——周期性本身就是固化的根本理由 |
| 输入可枚举成变量 | 能写成 `[目标_政策_区域]` `[统计_时间_区间]` 这种三段式变量 |
| 已有稳定的 UnitPattern | 产出要挂得进既有的单元模板；没有的话先别固化，先做人肉两期把 pattern 稳定下来 |

**不该固化**：

- 一次性选题（本期特稿做完就再不做）
- 依赖内部数据的任务（内部业绩、客户名单、未公开人事、未公开合同金额）——Cue 只覆盖公开数据源，硬做会退化成普通联网搜索
- 输入变量抽象不出来、每次问法差别很大的探索性话题

**成本账**：固化本身不花钱（`+author` / `+validate` / `+create` / `+frequent` 均免费），
只有跑一次真实验证（`+test`，约 3–8 积分）要花钱。判据命中就该固化，别舍不得——省下的是每期重复写调研指令的时间。

## 二、⚠️ 最关键的一条：`mimic` 与 `template-id` 互斥

自由式阶段我们靠 `--mimic-file <样刊>` 让研究报告天生带本刊腔调。
**一旦换成 `--template-id` 跑搭子，后端让 template_id 覆盖 mimic → mimic 静默失效**，runner 干脆直接拒绝二者同传。

所以固化时必须做一次「调性搬家」：把 mimic 交给 `report_format` 承担。

| 原来由 mimic 承担 | 固化后写在buddy 的哪里 |
|---|---|
| 句式、语气、专业程度 | `> **关键配置** · 基调设定` |
| 篇幅、每节长短 | `> **关键配置** · 篇幅约束`（直接写 UnitPattern 的字数区间） |
| 结构顺序 | `report_format` 的章节顺序 |
| 固定件（CTA、收尾句） | 各章执行蓝图的 `**输出形式**` |
| 事实密度、引用要求 | 各章执行蓝图的 `**信息需求**` |

搬家做不好，跑搭子的产出会比自由式更糟——因为自由式至少还能靠 mimic 兜一层。

## 三、report_format 怎么对齐 UnitPattern

这是两个技能真正咬合的地方：**让 Cue 产出的报告天然能按 UnitPattern 切片**，省掉一整轮改写。

对齐规则：

1. **章节数 ≈ UnitPattern 的 slot 分组数**（经验比约 1:1，最多不超过 15 章）。
   例如 U1 法规动态条目的 slots 是「标题 / 日期导语 / 要点 / 影响 / CTA」，就拆成：一览清单 / 逐条要旨与影响 / 待核实 / 边界说明 四章。
2. **强制保留一个「待核实」章节**。它直接对应 journal-draft 的 EvidenceCard 缺口，
   让不可靠内容被隔离到单独区域，而不是混进正文——这一步省掉的是后面整整一轮人工核对。
3. **主标题用本刊的维度变量**，不要硬码：`# [目标_政策_区域] 区域新规动态底稿`。
4. **每章必须有 `[执行蓝图]` 四件套**（研究目标 / 逻辑链条 / 信息需求 / 输出形式），
   其中「输出形式」只定形态不定列名（列名会让 reporter 陷入幻觉）。

参考实现：[`../assets/templates/buddy.region-policy-scan.json`](../assets/templates/buddy.region-policy-scan.json)
——「区域新规动态」搭子草案（对应样刊 01 法规动态栏目），已用 `+validate` 跑到 **0 error / 0 warning**。

## 四、固化流程与命令

**Step 0（免费，必做）：先查库里有没有**——用户的模板库默认不是空的，Cue 有上百个公有搭子可用，
一句话能省掉整个 `+author`。不要默认「我要新建一个」。

```bash
python3 ~/.workbuddy/skills/cue-buddy/scripts/cue_api.py list
```

实测：本机库里 20 个模板，期刊取料场景能直接用的只有「红筹拆除实证」「上市公司财报点评」等少数几个，
**没有任何法规动态 / 政策追踪类**——所以区域新规动态这个空白值得自己固化。
若查到近似的，优先 `get <id>` 取全文看能否改着用，而不是从零写。

```
1) 自由式跑通：cue-research 跑一次，确认产出满意（要用 --mimic-file 带上样刊调性）
2) 保存：cue-research +save <conversation_id>
        → 后端按这次会话历史生成模板草稿，交到 cue-buddy 的 +author 流程
        （模板生成本身免费）
3) 改：按 §二 做调性搬家、按 §三 对齐 report_format
4) 校验（免费，务必跑）：
   python3 ~/.workbuddy/skills/cue-buddy/scripts/validate_template.py <payload.json>
5) 入库（免费，须用户确认）：
   python3 ~/.workbuddy/skills/cue-buddy/scripts/cue_api.py create <payload.json>
   → 返回 template_id（形如 template_fnig0i，不是数字 id）
6) 钉常用（免费）：
   python3 ~/.workbuddy/skills/cue-buddy/scripts/cue_api.py frequent <template_id>
7) 验收（花钱，约 3–8 积分，先告知用户）：
   python3 ~/.workbuddy/skills/cue-buddy/scripts/test_template.py <template_id> <真实主体> --save run.md
   产出报告按 UnitPattern 切片 → 能直接进 content.json 才算通过
8) 不合格就用 +tune 附上问题清单再改，然后回到 4)
```

日常调用（后台跑，别同步等）：

```bash
python3 ~/.workbuddy/skills/cue-research/scripts/research_run.py \
  --template-id <template_id> \
  --query "<本期这条要查的问题>" \
  --output <本期素材目录>/<栏目>-<主体>.md
# run_in_background: true；单次 3–15 分钟，服务端硬上限 60 分钟
```

其它：`cue_api.py list`（看已有模板）/ `get <id>`（取全文）/ `update <id> payload.json`（改）。

## 五、期刊场景的搭子候选清单

按样刊结构推算，最可能被反复用到的几类（命中判据才做，不要一次全做）：

| 期刊环节 | 搭子 | 变量设计 | 对齐哪个 UnitPattern |
|---|---|---|---|
| 法规动态 | 区域新规动态（已备草案） | `[目标_政策_区域]` `[业务_关注_领域]` `[统计_时间_区间]` | U1 法规动态条目 |
| 合规案例 | 监管处罚与合规快照 | `[目标_受罚_主体]` `[关注_处罚_领域]` | U1 的变体 |
| 业绩快讯 | 公开发行 / 上市项目核查 | `[目标_项目_主体]` `[公告_时间_区间]` | U3 业绩快讯（必带承办角色） |
| 深度观察 | 行业风向与政策追踪 | `[目标_产业_主题]` `[统计_时间_区间]` | U2 深度文章 |
| 人事栏目 | 公开履历核验 | `[目标_入职_人员]` | U4 新闻人事 |
| 竞对栏目 | 同业动态扫描 | `[目标_同业_主体]` | U1 / U2 变体 |

## 六、沉淀进派生子技能

`+spec` 派生出 `journal-<企业>-<类型>` 时，把这个刊物验证过的 buddy 映射写进子技能（见 `instantiation.md`）：

```
## 已固化的调研搭子
| 场景 | template_id | 对齐 UnitPattern | 上期验收结果 |
|---|---|---|---|
| 区域新规动态 | template_xxxx | U1 | 2026-Q2 通过，逐条可直接入content.json |
```

第二期起直接按表调用，不必重新 `+author`。`template_id` 变了要记得同步这张表——它承接的是每期的调研路径，一旦断掉就退回自由式从头协商。
