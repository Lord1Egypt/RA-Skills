# 薪酬市场动态数据架构

更新时间：2026-05-19

这份文件回答 3 个问题：

1. 薪酬市场调研数据从哪里来
2. 哪些数据可以动态拿，哪些不能
3. skill 应该如何区分“市场信号”和“正式定薪依据”

## 一、核心原则

薪酬 skill 不能把所有数据都当成同一种证据。

至少要区分 4 层：

1. `official_policy`
   官方动态资料，例如国家统计局、税务局、公积金中心、地方人社口径
2. `public_market_signal`
   公网职位薪资、招聘平台公开区间、景气和招聘热度
3. `paid_survey_data`
   企业采购的薪酬调研结果，例如 Mercer、智联企业薪酬调研等
4. `internal_company_data`
   企业自己的 band、内部同岗参考、预算、历史 offer、接受率

## 二、每一层能做什么

### `official_policy`

能支持：

1. 合规边界
2. 城市年度口径
3. 社保、公积金、个税相关约束
4. 宏观工资趋势

不能直接支持：

1. 某一岗位的精准定薪
2. 某一级别的 P50/P75 报价

### `public_market_signal`

能支持：

1. 当前市场招聘热度
2. 公开薪资区间趋势
3. 城市、行业、岗位的招聘侧价格信号

不能直接支持：

1. 最终成交薪资
2. 企业内部公平
3. 可审计的正式定薪依据

所以它最多只能作为：

`market signal only`

### `paid_survey_data`

能支持：

1. 分城市、分岗位、分级别的市场分位点
2. 定薪、调薪、band 校准
3. 对业务或老板的正式解释材料

这是最接近真实薪酬 benchmark 的外部数据。

### `internal_company_data`

能支持：

1. band 判断
2. 内部公平判断
3. 预算约束
4. 历史 offer 一致性
5. 真正的审批建议

这是最终定薪最关键的一层。

## 三、skill 的判断权重

对于 `review_compensation_band_and_offer`，建议使用下面的判断优先级：

1. `internal_company_data`
2. `paid_survey_data`
3. `public_market_signal`
4. `official_policy`

## 四、什么时候允许 skill 给出强结论

### 可以给“正式建议”

至少满足：

1. 有 `band`
2. 有 `internal_company_data`
3. 有 `paid_survey_data` 或高质量市场分位点
4. 有候选人当前薪资或总包口径
5. 有预算范围

### 只能给“弱建议”或“仅市场信号判断”

如果出现这些情况：

1. 只有公网职位薪资，没有正式调研
2. 没有内部 band
3. 没有内部同岗同级参考
4. 没有预算
5. 候选人只有期望薪资，没有当前薪资或总包口径

这时 skill 必须主动说：

1. 当前只能给市场信号判断
2. 不能作为正式定薪依据
3. 还缺哪些数据

## 五、建议的输入结构

建议每次定薪判断输入都显式区分来源：

```text
policy_context
public_market_signal
paid_survey_data
internal_company_data
candidate_compensation_context
```

不要把所有东西都混在一个 `market_benchmark` 里。

## 六、最小可行动态方案

如果现在就要做一个“动态版薪酬 skill”，最实际的路线是：

1. 官方动态口径：由 skill 内置并定期更新
2. 公网市场信号：允许用户补充或人工抓取摘要
3. 正式调研数据：由用户上传最新报告或 Excel
4. 企业内部数据：由用户上传 band、预算、内部参考

也就是说：

`动态` 不等于 `全靠 skill 自己上网抓`

而是：

`skill 能持续消费会变化的数据，并且知道每种数据能撑起多强的判断`
