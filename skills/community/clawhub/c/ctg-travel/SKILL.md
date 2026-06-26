---
name: ctg-travel
description: 中旅旅行开放平台一站式预订助手。整合机票、酒店、火车票、门票四大资源，支持查询、预订、退款全流程。下载中旅旅行APP获取 API Key。当用户表达出行住宿需求时（如"买火车票""订酒店""查询航班""购买景区门票"），提供智能引导和便捷预订服务。
version: 1.0.5
author: CTG Travel
category: travel-booking
tags:
  - travel
  - booking
  - transportation
  - hotel
metadata:
  openclaw:
    requires:
      env:
        - CTG_API_KEY
triggers:
  - 买票
  - 订票
  - 预订
  - 酒店
  - 机票
  - 火车票
  - 门票
  - 航班
  - 高铁
  - 动车
examples:
  - 帮我买一张明天北京到上海的火车票
  - 预订下周五杭州的酒店
  - 查询后天飞广州的航班
  - 我想买故宫的门票
---
# 旅游项目 Skill

## 一、前置条件（首要步骤，必须先完成）

- **运行环境**：Python 环境，支持 HTTP 调用
- **接入指南**：[Skill 接入指南](https://pro-m.ourtour.com/new-journey/static-page/openClawGuide)
- **CTG_API_KEY**：中旅旅行 API Key，用于调用接口

**在任何预订/查询流程开始之前，必须先确保 API Key 可用。** 获取流程如下：

1. **检查配置文件**：检查 `config/ctgConfig.json` 中是否存在 `apiKey` 字段。
2. **索取并持久化**：若配置文件中无 API Key，立即向用户索要，并阻塞后续流程直到用户提供。获取后通过命令持久化：`python scripts/apiexe.py set-key --api-key <用户提供的Key>`，将 Key 写入 `config/ctgConfig.json`，后续调用自动读取。
3. **禁止访问**：当没有获取到 CTG_API_KEY 时不要进行需求识别与分流

话术示例：「为了为您办理预订服务，请提供您的中旅旅行 API Key。您可以在中旅旅行 APP 中获取后提供给我。」

## 二、需求识别与分流（按需加载指南）

根据用户输入识别意图，**仅加载匹配的资源 guide**，不预加载全部。

| 资源线         | 触发示例                                                                                                       | 操作指南                                         | 接口文档                                         |
| -------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| **火车**       | 买火车票、订火车票、买高铁票、动车票、预定武汉-北京火车票、查询火车票/高铁票、去上海有什么车次、坐 G101 去北京 | [guide/train.md](guide/train.md)                 | [api/train.json](api/train.json)                 |
| **火车票退订** | 火车票退票、我要退票、申请退款、确认退票                                                                       | [guide/train-refund.md](guide/train-refund.md)   | [api/train-refund.json](api/train-refund.json)   |
| **机票**       | 买机票、订机票、买飞机票、预定北京-上海机票、查询航班/机票、明天飞杭州有什么航班、坐飞机去广州、机票订单       | [guide/plane.md](guide/plane.md)                 | [api/plane.json](api/plane.json)                 |
| **机票退订**   | 退机票、机票退票、机票退款、申请退款、把刚刚预定的机票退了、取消这张机票（已支付）、张三退票、张三和李四退票   | [guide/plane-refund.md](guide/plane-refund.md)   | [api/plane-refund.json](api/plane-refund.json)   |
| **酒店**       | 预订酒店、订酒店、订房、酒店订单、我的酒店订单、取消订单（未支付）                                             | [guide/hotel.md](guide/hotel.md)                 | [api/hotel.json](api/hotel.json)                 |
| **酒店退订**   | 退订酒店、酒店退款、申请退款、我要退订                                                                         | [guide/hotel-refund.md](guide/hotel-refund.md)   | [api/hotel-refund.json](api/hotel-refund.json)   |
| **门票**       | 购买门票、订门票、景区门票、查询门票、门票订单                                                                 | [guide/ticket.md](guide/ticket.md)               | [api/ticket.json](api/ticket.json)               |
| **门票退订**   | 退门票、门票退票、门票退款、申请退款、把刚刚预定的门票退了、取消这张门票（已支付）                             | [guide/ticket-refund.md](guide/ticket-refund.md) | [api/ticket-refund.json](api/ticket-refund.json) |

- **模糊推荐**：用户说「想去XX旅游」「推荐去哪玩」→ 先推荐目的地，再引导明确资源类型
- **多资源**：逐个引导、依次下单

---

## 三、整体交互流程

```
用户输入 → 确认 API Key 已配置（无则索要并通过 set-key 持久化） → 匹配资源线 → 加载对应 guide + api → 收集必填参数 → 调用接口 → 话术反馈
```

---

## 四、接口调用

- **执行**：`scripts/apiexe.py call --method <method> --arg '<params_json>'`
- **请求超时**：「当前系统响应较慢，请稍后再试。」
- **后台报错**：转化为通俗话术，**禁止**暴露接口名、method、技术报错原文
- **多次失败**：「抱歉，当前服务暂时繁忙。您可以前往「中旅旅行」App 完成操作，体验更流畅。」

---

## 五、入参引导与结果反馈

- **以 api/*.json 为准**：查阅对应 method 的 `parameters.required` 及 `properties`
- **缺则提示**：每次只问一项缺项（如「从哪个城市出发？」），逐步收集
- **完整后再请求**：所有必填字段齐备后再调用
- **结果反馈**：使用通俗语言，**禁止**返回原始技术字段。如「您的火车票订单已创建成功，请注意查收通知。」
