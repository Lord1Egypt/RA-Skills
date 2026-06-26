---
name: brand-analyzer-zeelin
slug: brand-analyzer-zeelin
version: 1.1.0
description: 品牌分析 Skill（零配置版）。用户仅需提供 Zeelin App-Key 和品牌名，调用服务端封装接口生成品牌底座；计费在服务端完成（成功扣50额度，失败不扣费）。
author: brand-analyzer team
license: MIT
tags: [brand, analysis, marketing, zeelin]
requires:
  - capability: http
---

## 隐私与透明度

- 服务提供方：Brand Analyzer API
- 计费平台：智灵 Skill 平台（https://skills.zeelin.cn）
- 数据处理：用户输入的品牌名/查询文本（可选附件）会发送到服务端生成品牌底座
- 敏感信息：网关密钥、计费逻辑、skill_id 均在服务端，不在本 Skill 包中分发

---

## 使用时机

当用户需要：
- 品牌底座、品牌分析、品牌定位梳理
- 竞品格局、用户画像、品牌调性总结
- 从品牌名快速产出结构化品牌报告

不适合：图片生成、代码生成、视频制作、纯数据爬虫任务。

---

## 计费规则

- 每次成功生成品牌底座扣 **50 额度**
- 失败不扣费
- 用户需在智灵平台创建并充值 App-Key

---

## 第一步（强制）：索取用户 App-Key

在任何生成动作前，先向用户索取 App-Key：

> 开始前需要先验证你的智灵账户额度。请提供你的 App-Key。

如果用户未提供 App-Key，停止后续流程。

---

## 第二步：调用品牌分析接口（服务端封装）

**固定接口地址（发布前必须替换为你的稳定正式域名）**：

`https://following-hull-easy-interactions.trycloudflare.com`

### 2-A. 常规请求（品牌名必填）

`POST https://following-hull-easy-interactions.trycloudflare.com/v1/brand-analyzer/generate`

Headers:
- `App-Key: <用户App-Key>`

Body (multipart/form-data):
- `brand_name` (必填)
- `query` (选填)

### 2-B. 附件策略（可用则传，失败降级）

- 若客户端支持附件上传：额外传 `file`
- 若上传失败或客户端不支持：自动降级为仅 `brand_name + query` 并告知用户“已降级执行”

---

## 第三步：处理返回

### 成功

当返回 `code=200`：
- 输出 `data.markdown` 作为主结果
- 补充提示：本次生成成功，消耗 50 额度，剩余额度 `data.remain_calls`

### 失败

当 `code!=200`：
- 直接使用 `message` 给用户可执行提示
- 常见场景：
  - 402：余额不足，提示前往智灵充值
  - 404：App-Key 无效，提示检查 Key
  - 500：服务异常，提示稍后重试

---

## 安全边界

- 本 Skill 不包含核心业务逻辑与计费实现。
- 所有扣费链路均在服务端执行：`detail -> business -> cost(50)`。
- 不在 Skill 包内暴露网关 key、内部提示词、skill_id。
