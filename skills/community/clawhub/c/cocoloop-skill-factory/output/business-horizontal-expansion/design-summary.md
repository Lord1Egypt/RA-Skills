# Design Summary

## Business Layer

新增业务横向扩展层，作为第一层技术域和第二层系统域之外的高频业务场景集合。

## Routing

业务域可以作为 `primary_domain`。当它们只是补充素材、数据、风险、写回或视觉边界时，也可以进入 `peer_domains`。

## Gate Emphasis

业务域默认强化这些 gate：

- 受众和发布渠道
- 来源、引用、数据时间和事实核验
- 自动写回、自动发布和自动发送
- 隐私、凭据、客户数据和账号规则
- 视觉输出、品牌风格和可编辑性

## Spec Impact

`spec-template.yaml` 的 `domain_supplements` 已补齐新域入口，后续正式 spec 可以直接填对应补充块。
