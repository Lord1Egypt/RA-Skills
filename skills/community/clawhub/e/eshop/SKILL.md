---
name: eShop
description: 一个聚合购物与外卖服务的智能平台，帮助用户完成商品搜索、下单购买、外卖点餐、订单查询、优惠券领取等全流程购物体验。支持多平台、多商家、多品牌的统一接入与智能路由。
version: 1.0.4
author: xavizhou
metadata: {"openclaw": {"emoji": "🛒", "category":[ "shopping","delivery","e-commerce"], "tags": ["电商", "外卖", "聚合", "商品搜索", "购物助手", "餐饮点单"]}}
---

# eShop

## 概述

`eShop` 是电商和外卖的工具库，用于帮助用户购物或者点外卖。

顶层 `skill.md` 只负责：

- 识别用户意图
- 判断任务域
- 识别平台、商家、品牌等实体
- 将请求路由到对应子文档
- 在必要时才加载详细说明

---

## 任务域

### 外卖
适用于以下请求：

- 我要点餐
- 我要点外卖
- 帮我点麦当劳
- 看看有什么吃的

对应子目录：

```text
delivery/
```

### 电商
适用于以下请求：

- 我要买东西
- 帮我找商品
- 看看某个平台上的商品
- 我想买手机壳

对应子目录：

```text
ecommerce/
```

---

## 路由原则

处理流程：

```text
用户输入
-> 意图识别
-> 任务域判断
-> 实体抽取
-> 别名归一化
-> 文件映射
-> 按需加载子文档
```

规则：

1. 先判断是外卖还是电商
2. 再识别用户是否指定了平台、商家、品牌或店铺
3. 只有在目标明确平台，商家，品牌信息的时候，才加载对应子文档
4. 不要一次性加载所有子文档
5. 若信息不足，先澄清，再决定是否加载

---

## 实体映射

当用户提到已知平台、商家或品牌时，先做别名归一化，再映射到文件路径。

示例：

- 麦当劳 / McDonald's / mcd -> `delivery/merchants/mcd.md`
- 肯德基 / KFC -> `delivery/merchants/kfc.md`
- 必胜客 / Pizza Hut -> `delivery/merchants/pizzahut.md`
- 骆岗/ Luogang / inLG -> `ecommerce/platforms/luogang.md`
- 平台1 -> `delivery/platforms/platform1.md`

匹配优先级：

1. 精确别名
2. 常见缩写
3. 标准名称
4. 若有多个候选，先澄清
5. 若没有命中，留在顶层通用流程

---

## Routing Index

### 外卖商家
- aliases: `麦当劳`, `McDonald's`, `McDonald`, `mcd`, `mcdonalds`
  target: `delivery/merchants/mcd.md`

<!-- - aliases: `肯德基`, `KFC`, `kfc`
  target: `delivery/kfc.md`

- aliases: `必胜客`, `Pizza Hut`, `pizzahut`
  target: `delivery/pizzahut.md`

### 外卖平台
- aliases: `平台1`, `外卖平台1`
  target: `delivery/platform1.md`

- aliases: `平台2`, `外卖平台2`
  target: `delivery/platform2.md`

- aliases: `平台3`, `外卖平台3`
  target: `delivery/platform3.md` -->

### 电商平台
- aliases: `luogang`,`Luogang`,`inLG`,`骆岗`, `骆岗电商`, `骆岗门市部`
  target: `ecommerce/platforms/luogang.md`

---

## 澄清策略

以下情况先澄清，不直接加载子文档：

- 未说明是外卖还是电商
- 未指定平台或者品牌，但后续必须依赖平台规则
- 实体可能对应多个目标

示例提问：

- 你是想点外卖，还是买商品？
- 你有指定平台吗？

---

## 示例

### 我要点麦当劳
处理：

```text
外卖
-> 实体: 麦当劳
-> 归一化: mcd
-> 加载: delivery/mcd.md
```

### 我想买手机壳
处理：

```text
电商
-> 未指定平台，默认使用 luogang
-> 再决定是否加载子文档
```

### 去骆岗看看耳机
处理：

```text
电商
-> 实体: luogang
-> 加载: ecommerce/luogang.md
```
