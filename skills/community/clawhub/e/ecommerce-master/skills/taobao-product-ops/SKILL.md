---
name: taobao-product-ops
description: 淘宝商品发布与管理：TOP API 与 browser-ops 双通道、商品内容包结构、类目属性映射、资质门槛与合规红线
source:
  type: original
  repo: skills-repo/ecommerce-master
  path: skills/taobao-product-ops/SKILL.md
  version: 1.0.0
  updated: 2026-10-29
metadata:
  category: 淘宝运营
  platform: Web
  difficulty: 进阶
---

# 淘宝商品发布与管理（Taobao Product Ops）

> 发布/改价/上下架一条链：**API 优先、浏览器半自动兜底**的双通道设计。核心复用资产是
> 「商品内容包」——结构化 JSON 逐字段对应表单项，无论走 API 还是人工都能直接消费。

## 能力

- 商品内容包（Content Pack）标准结构：标题/类目/属性/图集/详情/定价
- TOP API 发布链路：`taobao.item.add` → `picture.upload` → 类目属性映射
- 无资质/闲鱼场景：内容包 + 浏览器半自动（发布按钮人工点）
- 资质门槛判断：个体工商户 + 企业支付宝 → 企业店铺 → 交易类 API 权限

## 使用方式

```
/taobao-product-ops 生成 Switch 卡带商品的内容包并发布到淘宝
/taobao-product-ops 这批旧货要上闲鱼，帮我出内容包和人工发布清单
/taobao-product-ops 我的店铺资质够不够走 API 发布？
```

## 双通道决策（先判资质，再判渠道）

| 条件 | 通道 |
|------|------|
| 有企业店铺 + TOP 应用已获 `taobao.item.add` 权限 | **A：API 发布**（`item.add` + `itemprops.get` 映射属性，限速重试） |
| 有个体户资质但 API 权限未批（人工审核 3–5 工作日） | 等审批，期间走 B |
| 无资质 / 渠道是闲鱼（无官方商家 API） | **B：内容包 + 浏览器半自动**（执行层用 `ai-fullstack-engineer` 的 `browser-ops`：视觉驱动填表、滑块人工过、发布按钮人点） |

## 商品内容包（核心资产）

```json
{
  "title": "<类目词+品牌+型号+成色+规格，30 汉字内，堆满不堆砌>",
  "category_path": "<一级/二级/叶子类目>",
  "props": {"成色": "95新", "region": "国行"},
  "images": ["主图1", "细节图xN（8 图制）"],
  "detail": "<成色描述+问题 disclosed+配件清单+售后口径>",
  "price": {"anchor": "<市场价>", "ours": "<定价>", "floor": "<底价>"},
  "channel": ["taobao", "xianyu"]
}
```

内容包一次生成、三处消费：API 请求体、browser-ops 填表、人工照抄清单。

## 红线（违反即停）

- **游戏账号/代练/账号租赁类目不得发淘宝**（平台禁售，下架处罚风险）——账号租赁只走闲鱼个人闲置形态
- 不写风控对抗代码；滑块/验证码一律人工兜底（见 `browser-ops` playbook）
- 类目/属性如实填写；批量上架走 API 限速，不做铺货式群控

## 限制

- API 通道需个体工商户资质、企业支付宝、自用型应用 + 交易类 API 权限（高级权限 3–5 工作日人工审核），交易类 API 可能需保证金
- TOP 有 App 级与 API 级限流；批量上架必须限速 + 重试退避
- 闲鱼无官方商家 API，自动化只能到「填到预览为止」
