---
name: ctg-travel-booking
description: 【已过期】中旅旅行开放平台一站式预订助手。请前往 https://clawhub.ai/ctg-travel/ctg-travel 下载最新版本。整合机票、酒店、火车票、门票四大资源，支持查询、预订、退款全流程。下载中旅旅行APP获取 API Key。当用户表达出行住宿需求时（如"买火车票""订酒店""查询航班""购买景区门票"），提供智能引导和便捷预订服务。
version: 0.2.5
author: CTG Travel
category: travel-booking
tags:
  - travel
  - booking
  - transportation
  - hotel
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

## ⚠️ 重要提示

**此 Skill 已过期，不再维护。**

请前往官方地址下载最新版本：**https://clawhub.ai/ctg-travel/ctg-travel**

---

## 接入须知

- **配置要求**：下载中旅旅行APP，获取 API Key，配置到 `config/ctgConfig.json` 的 `apiKey` 字段
- **运行环境**：Python 环境，支持 HTTP 调用能力
- **接入指南**：[Skill 接入指南](https://pro-m.ourtour.com/new-journey/static-page/openClawGuide)

## 一、需求识别与分流（按需加载指南）

**重要**：先根据用户输入识别是「预定/查询某类具体资源」还是「模糊旅游推荐」，再决定是否加载操作指南。**仅当识别到用户要预定、查询某个具体资源时，才加载该资源对应的 guide 操作指南**，无需预先加载全部指南。

### 1. 触发条件（用于识别资源线）

根据下列关键词/意图匹配用户输入，命中哪一类则加载对应 guide：


| 资源线         | 触发示例（命中则加载对应 guide）                                                                               | 操作指南                                         | 接口文档                                         |
| -------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| **火车**       | 买火车票、订火车票、买高铁票、动车票、预定武汉-北京火车票、查询火车票/高铁票、去上海有什么车次、坐 G101 去北京 | [guide/train.md](guide/train.md)                 | [api/train.json](api/train.json)                 |
| **火车票退订** | 火车票退票、我要退票、申请退款、确认退票                                                                       | [guide/train-refund.md](guide/train-refund.md)   | [api/train-refund.json](api/train-refund.json)   |
| **机票**       | 买机票、订机票、买飞机票、预定北京-上海机票、查询航班/机票、明天飞杭州有什么航班、坐飞机去广州、机票订单       | [guide/plane.md](guide/plane.md)                 | [api/plane.json](api/plane.json)                 |
| **机票退订**   | 退机票、机票退票、机票退款、申请退款、把刚刚预定的机票退了、取消这张机票（已支付）、张三退票、张三和李四退票   | [guide/plane-refund.md](guide/plane-refund.md)   | [api/plane-refund.json](api/plane-refund.json)   |
| **酒店**       | 预订酒店、订酒店、订房、酒店订单、我的酒店订单、取消订单（未支付）                                             | [guide/hotel.md](guide/hotel.md)                 | [api/hotel.json](api/hotel.json)                 |
| **酒店退订**   | 退订酒店、酒店退款、申请退款、我要退订                                                                         | [guide/hotel-refund.md](guide/hotel-refund.md)   | [api/hotel-refund.json](api/hotel-refund.json)   |
| **门票**       | 购买门票、订门票、景区门票、查询门票、门票订单                                                                 | [guide/ticket.md](guide/ticket.md)               | [api/ticket.json](api/ticket.json)               |
| **门票退订**   | 退门票、门票退票、门票退款、申请退款、把刚刚预定的门票退了、取消这张门票（已支付）                             | [guide/ticket-refund.md](guide/ticket-refund.md) | [api/ticket-refund.json](api/ticket-refund.json) |

**按需加载**：若用户说「我要买火车票」→ 仅加载 `guide/train.md` 和 `api/train.json`，按该指南执行。若用户说「查一下明天北京到上海的航班」→ 仅加载 `guide/plane.md` 和 `api/plane.json`。未涉及到的资源线不加载其 guide。

### 2. 模糊旅游推荐（不加载具体资源 guide）

用户表达模糊旅游意愿时（如「我想去XX地方旅游」「推荐一下去哪玩」）：

1. 先进行旅游地合理推荐
2. 再引导用户明确资源订购意愿（火车/机票/酒店/门票）
3. 用户明确后，按上表触发条件加载对应 guide，进入该资源线流程

### 3. 多资源订购

用户同时订购多种资源（如「同时买火车票和酒店」）：

- **逐个引导、依次下单**：先按触发条件加载第一个资源的 guide 并完成流程，再加载下一个资源的 guide
- 避免多资源操作冲突

---

## 二、整体交互流程

```
用户输入 → 匹配触发条件 → 按需加载 guide + api → 收集必填参数 → 话术反馈
- 未命中触发条件 → 判断是否模糊旅游推荐 → 引导明确资源
- 禁止出现技术用语（接口名、API、method 等）
```

---

## 三、接口调用规范

### 统一接口

- **URL**：`callUrl`（config 中配置）
- **方法**：POST
- **请求体字段**：
  - `method`：从 api/*.json 获取（category、subCategory、action）
  - `params`：业务参数，对应接口文档中的 `parameters`
  - `auth`：脚本自动生成（key、timestamp、nonce、signature）

### 调用方式

- 执行：`scripts/apiexe.py call --method <method> --arg '<params_json>'`

### 异常处理

- **请求超时**：向用户说「当前系统响应较慢，请稍后再试。」
- **后台报错**：将错误转化为通俗话术（如「暂时无法获取结果，请稍后再试」），引导用户重试，**切勿**直接说「接口错误」「API 报错」等
- **流程卡住时的统一引导**：当多次重试仍失败或流程无法继续时，提示用户：「抱歉，当前服务暂时繁忙。您可以前往「中旅旅行」App 完成操作，体验更流畅。」

---

## 四、入参引导与结果反馈

### 面向用户的文案（重要）

**所有对用户说出的内容均为业务话术**，禁止出现：

- 「调用 xxx 接口」「请求 xxx API」「调用 cityList / getPassengerList」等
- 任何 method 名、接口名、技术报错原文

应使用用户能理解的说法，例如：

- 「正在为您查询航班」「正在为您占位，请稍候」「系统暂时繁忙，请稍后再试」

### 入参引导（不写死必填项）

- **以 api/*.json 为准**：需要发起请求时，查阅对应 method 的 `parameters.required` 及 `properties`
- **缺则提示**：若用户未给出某必填字段，则用自然语言提示用户填写（如「从哪个城市出发？」）
- **逐步收集**：每次只问一项缺项，待用户回复后再继续
- **完整后再请求**：所有必填字段收集完整后再发起请求

### 结果反馈

**成功示例**：「您的火车票订单已创建成功，请注意查收通知。」

**错误示例**：「抱歉，预定人数输入有误，请输入正确的正整数人数后重新尝试。」

- 不要直接返回后台原始响应或技术字段
- 始终用通俗、日常的语言与用户沟通
