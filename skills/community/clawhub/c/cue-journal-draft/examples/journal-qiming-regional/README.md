# 把这份样例技能改成你自己的

> **本样例已脱敏**：机构名、刊物名、自然人姓名、客户与项目名称、源文件名**全部为虚构合成实体**。
> 保留的是实测的版式参数与内容模板结构 —— 它演示的是**成套方法**，不是任何一家机构的真实刊物。
> 改造你自己的刊时，这些字段**本来就要全部换掉**（见下面第二节）。

> 这份技能是 journal-draft 的一个**成品样例**，可以三类用法：
> ① 直接拿去做《区域观察》的下一期；② 照着结构改成你公司的刊；
> ③ 只当参考——看一本真实刊物的版式与内容模板被抽成了什么样。
>
> 改造成自己之前，建议先完整跑一遍，知道每个文件在什么时候被用到。

## 一、先分清三类文件

| 类别 | 文件 | 改造时要不要动 |
|---|---|---|
| **已钉死** | `assets/stylespec.json`、`assets/unit-patterns.md` | **不要手改**。它们是这台机器的参数；要改请用父技能 `journal-draft` 重新 `+learn` 一遍样例 |
| **待填清单** | `sources.template.md`、`runbook.template.md` | **必须填**。填上后把 `.template` 后缀去掉 |
| **每期变** | `assets/last-issue.md`、`SKILL.md` 的期次信息 | 每期更新，尤其 `last-issue.md`——它是新一期的容量基线 |

## 二、换成自家的最小改动

1. **换名字**：改 `SKILL.md` 的 frontmatter（`name` / `description` / Triggers）。
   `description` 里必须带上你刊的真实叫法和别名，否则触发不到。
2. **换版式**：**不要手改 stylespec.json**。拿你家的一期刊物当样例，
   用父技能跑一遍 `+learn`，产出替换掉 `assets/stylespec.json`。手改几十个字段必然漏。
3. **换内容模板**：重写 `assets/unit-patterns.md`。这是最值得花时间的一份——
   版式可以错一点，**内容模板错了整本刊都是错的**。每条至少要包含：slot 清单、
   字数硬指标、固定件要求、3 条真实例句。
4. **换固定件**：`assets/fixed-pieces.md` 填免责声明全文与名录。
   免责声明漏掉是法律风险，不是排版问题。
5. **填数据源**：`sources.template.md` 列官网栏目、公众号、监管机构原文站点。
6. **术语表**：`assets/glossary.md` 的「统一写法」列手工填——同一份条例在
   不同文章里出现三种简称，是内刊最常见的硬伤。

## 三、判断改好了没有

拿一期的真实素材跑一遍，然后看两个数字：

- **被打断几次**：确认提问应当在一轮内完成（父技能规定 ≤5 个问题且必带默认值）。
  超过一轮说明 `+brief` 没问到位，回到 `sources.md` 和固定件清单找原因。
- **直接可用比例**：产出的底稿里，多少比例的内容可以不改就进设计。
  低于一半通常是 UnitPattern 写得不够具体——回去补例句和字数硬指标。

## 四、什么时候别派生

- 只做过一期、还没拿到内部反馈
- 刊物本身在改版中
- 只是想看看效果

派生是承诺：一旦钉死，后续就照它执行。**样式定了再派生。**

## 五、派生过程

由父技能 `journal-draft` 的 `scripts/derive_skill.py` 生成：

```bash
python ~/.workbuddy/skills/journal-draft/scripts/derive_skill.py \   # 需已安装主技能 journal-draft
    --spec ./stylespec.json --unit-patterns ./unit-patterns.md \
    --out ~/.workbuddy/skills/<你的技能名> \
    --name <你的技能名> --publisher "<发行方>" --title "<刊名>"
```

**机器粗加工 ≠ 定稿。** 生成的 `spec_confidence` 若为 `drafted` 或 `weak`，
`unit-patterns.md` 是由样例统计倒推的草稿，**投产前必须人工复核并定稿**。
