---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_08b6b471731111f1b2f55254006c9bbf
    ReservedCode1: sNLHC2PT6qH08HoP/ExQkJo7O53VyQ6xSEXZWr9w83MdzJCIcu4GdGGE/Nk5fRaLyNe/aBja7GxT8bA96Snvbada6GPozBFVjN0xlLJy/ObS5zFzeUQYrMEhOfMiVqSxxOKV6LpKbarwI0ef980pzHn7SROqUXqPlegIYs8pYtXFlvacPfnf1U3t/T8=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_08b6b471731111f1b2f55254006c9bbf
    ReservedCode2: sNLHC2PT6qH08HoP/ExQkJo7O53VyQ6xSEXZWr9w83MdzJCIcu4GdGGE/Nk5fRaLyNe/aBja7GxT8bA96Snvbada6GPozBFVjN0xlLJy/ObS5zFzeUQYrMEhOfMiVqSxxOKV6LpKbarwI0ef980pzHn7SROqUXqPlegIYs8pYtXFlvacPfnf1U3t/T8=
---

# Gateway 配置思路

## 连接方式

Gateway 通过飞书开放平台的长连接接收群消息推送。核心思路：飞书群消息 → WebSocket 长连接 → Gateway → 路由到 Agent。

## 路由逻辑

Gateway 按群 ID 匹配路由，将不同群的消息分发给指定 Agent。多 Agent 在同一群协作时，需要通过消息前缀或关键词来区分目标 Agent（路由本身不解析 @ 语义）。

## 消息发送

Agent 回复群消息时，需注意消息格式选择——格式选错会导致回复在群里显示异常。

## Token 续期

飞书接入 Token 有时效限制，Gateway 需具备自动续期能力，否则运行一段时间后会中断。

## 部署顺序

先建群 → 获取群信息 → 配置路由 → 重启 Gateway → 测试。

> 各框架 Gateway 配置模板与验证方法见部署文档：https://www.jinengpu.chat/feishu-multi-agent-detail.html
*（内容由AI生成，仅供参考）*
