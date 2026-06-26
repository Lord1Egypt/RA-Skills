# 88 生意通产品概览

## 产品定位

**88 生意通**是 1688 面向线下买卖合作的交易服务工具，通过电子合约（采购单/合同）与银行资金专户等能力，帮助买卖双方安全、便捷地完成收付款。

## 核心概念

- **账号**：需使用 1688 账号登录。
- **主账号 / 子账号**：企业在 1688 注册认证的主账号拥有最高权限；子账号由主账号创建。**本技能仅支持主账号**操作，子账号引导网页端。
- **买家 / 卖家**：平台两种角色；**卖家即商家**。
- **用户服务协议**：操作前买卖双方需签署 88 生意通用户服务协议。
- **实名认证**：发起交易前，发起方需完成实名认证。
- **收款账户**：卖家在采购单确认或签署前需绑定银行卡收款账户。
- **交易方式**：采购单、合同两类。**本技能仅支持采购单**；合同类请去网页端。
- **支付方式**：引导网页端。

## 采购单主流程（概念）

1. 买家或卖家发起采购单（发起前需实名认证）；
2. 收集并确认采购单信息；
3. 邀请对方确认；
4. 确认完成后，买家通过**银行卡转账**支付；
5. 卖家发货；
6. 买家确认交易完成或申请退款（分支：完成则卖家收款；退款则按规则处理）。

## 能力亮点（简述）

- 银行资金专户：买家付款后资金进入专户管理，确认完成后再结算给卖家。
- 电子采购单/合同：支持在线生成与确认（电子合同签署由 e 签宝等能力支撑，合同签署以网页为准）。

## 网页入口（须带 tracelog）

- 卖家首页：`https://syt.1688.com/page/SYT/seller?__existtitle__=1&__removesafearea__=1&__immersive__=1&tracelog=88sytskill`
- 买家首页：`https://syt.1688.com/page/SYT/buyer?__existtitle__=1&__removesafearea__=1&__immersive__=1&tracelog=88sytskill`
- 买家采购单详情页：`https://syt.1688.com/page/SYT/buyer-contract-simple?draftNo=${draftNo}&__existtitle__=1&__removesafearea__=1&__immersive__=1&tracelog=88sytskill`
  - ${draftNo}: **需要根据上下文动态替换**。
- 卖家采购单详情页：`https://syt.1688.com/page/SYT/seller-contract-simple?draftNo=${draftNo}&__existtitle__=1&__removesafearea__=1&__immersive__=1&tracelog=88sytskill`
  - ${draftNo}: **需要根据上下文动态替换**。
- 用户服务协议：`https://syt.1688.com/n/openService/sign/preview?code=SYT_OPEN_SERVICE_AGREEMENT&tracelog=88sytskill`
- 帮助文档：`https://peixun.1688.com/space/WVJqzq3VdLKmYEKZ2AmonAjAbY4pDXdb?tracelog=88sytskill#4ever-bi-201`

## 常见问答（对客口径）

- **是否官方产品**：是 1688 官方线下交易服务工具。
- **支付是否安全**：资金专户管理，买家确认完成后卖家收款，过程可追溯。
- **卖家价值**：增强买家信任、促成交易；平台对交易额有相应权益说明以官方为准。
- **转账是否麻烦**：发起/确认采购单 → 买家付款 → 卖家发货 → 买家在 88 生意通确认完成，资金按规则结算。
- **账期支付**：本技能不支持，请前往 **88 生意通网页**办理。
- **法律效力**：经双方确认的采购单及电子合同具有与纸质合同同等法律效力；电子合同签章服务以平台公示为准。
