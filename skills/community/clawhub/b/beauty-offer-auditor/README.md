# Beauty Offer Auditor

一个面向 ClawHub 的可复用 Skill，用证据分级方式审计化妆品大促购买方案。它比较现金到手价，区分单品、套装与多件装，在证据充分时保守计算赠品净值，并把历史 offer 和低等级线索排除出当前排名。

## 文件

- `SKILL.md`：触发条件、边界、审计流程与失败降级。
- `references/offer-snapshot-v2.md`：数据结构、字段与公式规范。
- `references/output-template.md`：面向用户的标准输出模板。
- `examples/generic-case.json`：不含私人数据的虚构通用案例。

## 核心口径

```text
cash_landed_price = display_price - confirmed_discount + mandatory_cost
gift_net_value = sum(reference_value * quantity * realization_rate)
net_effective_cost = cash_landed_price - gift_net_value
gap_amount = reference_cash_landed_price - candidate_cash_landed_price
gap_rate = gap_amount / reference_cash_landed_price
```

未知字段保持 `null`，不得用零替代。历史报价、规格不匹配及 C/D 级证据不得进入当前价格排名。没有 A 级完整证据时，不输出无条件购买推荐。

## 安全边界

本 Skill 不宣称全网最低，不自动下单，不获取或保存用户账号、订单、地址、支付信息等私人数据，也不把某次查询结果固化进 Skill。

## 本地校验

测试位于源码仓库的 `tests/`，依赖仓库根目录结构，**不随 ClawHub 分发的归档一起下发**。需要校验时先取得源码：

```bash
git clone https://github.com/bonniegeng-max/price-gap-map.git
cd price-gap-map
python3 -m unittest discover -s tests -v
```

测试会校验 Skill 结构、frontmatter、引用文件、示例数据、公式、证据资格、历史排除和禁止性边界。

## 状态

已发布到 ClawHub：`@bonniegeng-max/beauty-offer-auditor`

- 页面：https://clawhub.ai/bonniegeng-max/skills/beauty-offer-auditor
- 安装：`openclaw skills install @bonniegeng-max/beauty-offer-auditor`

发布注意：直链可访问不等于被收录。实测观察到，ClawHub 公开广场与搜索里的 96 个 skill 无一带 `beta` 标签，而本 Skill 带 `beta` 标签时确实搜不到；两者是否构成因果尚未单独验证。正式发布时建议使用非预发布版本标签，并在发布后按**精确 slug** 复查是否已进入公开列表。
