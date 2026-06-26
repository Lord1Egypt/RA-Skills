# 电商增长运营预设

## domain_id

`ecommerce_growth_ops`

## common_jobs

- 商品标题、卖点、详情页、图片脚本和活动文案生成
- 店铺、商品、评价、问答和竞品资料分析
- 促销活动、直播脚本、短视频脚本和投放素材规划
- 订单、库存、转化、客单价和复购数据分析
- 多平台商品信息同步和运营日报生成

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 目标平台是什么，是否有主平台和分发平台
- 目标品类、商品、价格带和目标用户是什么
- 当前任务是商品内容、活动策划、竞品分析，还是经营报告
- 是否有品牌规范、平台规则、禁用词和素材限制
- 是否需要读取后台、评论、订单、库存或投放数据
- 是否涉及自动发布、批量上架、改价或库存变更
- 成功标准是点击、转化、复购、评价改善，还是运营效率

## recommended_execution_planes

- `Skill-only`
  适合商品文案、活动脚本、卖点提炼和人工审核素材
- `Skill + CLI`
  适合批量整理商品资料、图片清单和报表文件
- `Skill + API/MCP`
  适合店铺后台、ERP、CRM、广告平台和数据看板接入
- `Skill + CLI + API/MCP`
  适合经营数据拉取、内容生成、审核和系统写回

## risk_and_gates

- 自动上架、改价、库存和广告投放必须单独确认
- 平台规则、禁用词、资质和夸大宣传需要前置检查
- 价格、库存、促销和优惠信息必须核实
- 涉及评论、用户数据和订单数据时需要脱敏
- 竞品分析要记录来源和采集时间

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.ecommerce_growth_ops`
- 如果涉及图文或详情页视觉，必须补 `output_profile` 和 `design_md`
