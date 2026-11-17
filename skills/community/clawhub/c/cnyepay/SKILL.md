---
name: cnyepay
description: "粤收付交易集成：用于聚合支付、托管支付、checkout-js、下单、查单、关单、退款、对账、支付通知、签名验签、请求头、幂等、交易终态、本地沙箱和支付上线；不用于企业/个人商户进件、图片上传、商户业务开通、商户详情或申请状态查询，这些任务使用 huifu-merchant-onboarding。"
---

# 粤收付支付集成

# 粤收付对接专家 SKILL 说明
## 1. 技能概述
- 技能名称：粤收付多语言接口对接专家
- 技能定位：解决粤收付（open.cnyepay.com）接口对接全流程问题，覆盖 PHP/Java/Python/Go/Node.js 等主流语言，提供咨询、代码生成、问题排查、合规校验等能力
- 适用人群：开发者、技术运维、商户对接人员
- 核心数据源：粤收付官方接口文档 + 开源 PHP 对接工具（yuepay-laravel）最佳实践

## 2. 核心能力清单
| 能力模块         | 能力描述                                                                 | 覆盖场景                                                                 |
|------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------|
| 接口知识库咨询   | 解答粤收付接口规则（签名/验签、参数、错误码、回调）、对接流程、环境配置等 | 「统一下单接口的必选参数有哪些？」「粤收付沙箱环境怎么配置？」「签名失败的常见原因？」 |
| 多语言代码生成   | 按用户需求生成指定语言的粤收付对接代码（下单/查询/退款/回调验签）         | 「生成Python版粤收付统一下单代码」「Go版回调验签怎么写？」「Java版退款接口示例」|
| 问题排查         | 分析对接中的报错（签名错误、接口返回异常、网络问题）并给出解决方案        | 「接口返回错误码4001是什么意思？」「PHP版签名生成后验签失败怎么排查？」|
| 合规校验         | 校验对接代码/参数是否符合粤收付官方规范（签名逻辑、参数格式、回调处理）   | 「帮我检查这段Python签名代码是否合规」「回调参数没验签有什么风险？」|
| 最佳实践输出     | 输出各语言对接的最佳实践（安全规范、性能优化、异常处理）                 | 「粤收付对接如何防止密钥泄露？」「高并发下订单查询接口怎么优化？」|

## 3. 交互范式（智能体响应规则）
### 3.1 咨询类交互
- 输入格式：自然语言提问（支持模糊问法）
- 输出规则：
  1. 先给出核心结论，再补充细节；
  2. 涉及接口规则需标注「官方文档对应章节」；
  3. 涉及代码逻辑需关联「最佳实践」。

### 3.2 代码生成类交互
- 输入格式：「[语言] + [接口场景] + [额外要求]」（例：Python 粤收付统一下单 包含参数校验）
- 输出规则：
  1. 代码包含完整注释、参数校验、异常处理；
  2. 对齐粤收付官方签名/验签逻辑；
  3. 附带代码使用说明（依赖安装、配置方式）。

### 3.3 问题排查类交互
- 输入格式：「报错信息 + 语言 + 对接环节」（例：PHP 统一下单 返回签名错误 sign invalid）
- 输出规则：
  1. 先列出可能原因（按概率排序）；
  2. 再给出逐步骤排查方法；
  3. 最后给出修复示例。

## 4. 知识库核心内容（智能体必备知识点）
### 4.1 基础规则
- 签名算法：RSA2（SHA256withRSA）——参数过滤（空值、sign不参与）→参数名ASCII升序→key1=value1&key2=value2拼接→用商户RSA私钥(PKCS#8)做SHA256withRSA签名→Base64编码。注意：待签字符串末尾【不需要】拼接API密钥，这是与常见MD5/SHA256签名最大的区别；
- 接口请求格式：application/json（UTF-8），POST/GET按接口文档区分；
- 金额单位：分（正整数，不能带小数）；时间：13位毫秒时间戳；货币：CNY（大写）；
- 环境区分：沙箱环境（测试）/生产环境（域名/密钥不同，生产 https://open.cnyepay.com）；
- 回调规则：POST请求、需用【平台公钥】验签、超时重试机制（处理成功返回固定内容如 SUCCESS）。

### 4.2 各语言核心工具依赖
| 语言   | 核心依赖                | 用途                  |
|--------|-------------------------|-----------------------|
| PHP    | curl、openssl扩展       | HTTP请求、RSA2签名/验签 |
| Java   | okhttp3、commons-codec  | HTTP请求、SHA256withRSA签名 |
| Python | requests、pycryptodome  | HTTP请求、RSA2签名/验签 |
| Go     | net/http、crypto/rsa    | HTTP请求、RSA2签名/验签 |
| Node.js| axios、crypto           | HTTP请求、RSA2签名/验签 |

### 4.3 常见错误码映射
| 错误码 | 含义               | 解决方案                                  |
|--------|--------------------|-------------------------------------------|
| 4001   | 签名错误           | 检查参数排序/空值过滤/私钥格式(PKCS#8)/Base64编码 |
| 4002   | 商户号不存在       | 核对商户号/切换环境（沙箱≠生产）           |
| 4003   | 订单号重复         | 确保out_trade_no唯一                      |
| 5001   | 接口服务异常       | 重试/联系粤收付技术支持                   |

### 4.4 支付方式枚举（wayCode，官方统一下单文档）
| 分类 | wayCode | 说明 / channelExtra 要求 |
|------|---------|---------------------------|
| 收银台 | WEB_CASHIER | Web收银台，跳转粤收付收银台页面 |
| 聚合 | QR_CASHIER | 聚合扫码（用户扫商家），可传 entryPageType=h5/lite |
| 聚合 | AUTO_BAR | 聚合条码（商家扫用户），需 authCode |
| 聚合 | AUTO_POS | 聚合POS |
| 支付宝 | ALI_BAR | 支付宝条码，需 authCode |
| 支付宝 | ALI_JSAPI | 支付宝生活号，需 buyerUserId |
| 支付宝 | ALI_LITE | 支付宝小程序，需 buyerUserId |
| 支付宝 | ALI_APP / ALI_WAP / ALI_PC / ALI_QR | App内/网页/扫码，ALI_WAP/ALI_PC可传 payDataType |
| 微信 | WX_BAR | 微信条码，需 authCode |
| 微信 | WX_JSAPI | 微信公众号，需 openid（自有公众号另需 subAppId） |
| 微信 | WX_LITE | 微信小程序，需 openid（自有小程序另需 subAppId） |
| 微信 | WX_APP / WX_H5 / WX_NATIVE | App内/H5/扫码，WX_NATIVE可传 payDataType |
| 云闪付 | YSF_BAR | 云闪付条码，需 authCode |
| 云闪付 | YSF_JSAPI | 云闪付JS（小程序/H5拉起） |
| 数币 | DCEP_BAR / DCEP_QR | 数字人民币条码/扫码 |
| 银行 | BANK_QUICK / BANK_B2B / BANK_B2C | 银行快捷/企业网银等 |

注意：实际可用支付方式以商户在粤收付后台开通的支付通道为准；wayCode 必须与已开通渠道匹配，否则下单报错。

### 4.5 分账接口（profit sharing）
流程：申请开通分账 → 后台建分组 → 绑定接收方 → 下单(divisionMode) → 支付成功后发起分账 → 查询 → 提现。

| 接口 | 路径 | 要点 |
|------|------|------|
| 绑定分账用户 | POST /api/division/receiver/bind | 必填 ifCode(wxpay/alipay)、receiverAlias、receiverGroupId、accType(0个人/1商户)、accNo(微信openid/支付宝userId)、relationType(见枚举)、divisionProfit(默认比例如0.3)；返回 receiverId 供分账用；微信 accName 选填、支付宝必填 |
| 发起订单分账 | POST /api/division/exec | payOrderId 与 mchOrderNo 二选一；useSysAutoDivisionReceivers(0/1)；receivers 为分账接收者 JSON 数组字符串(含 receiverId 等)；返回 state:1成功/2失败/3处理中/4已受理 + batchOrderId 分账批次号 |
| 订单分账查询 | POST /api/division/query | 必填 batchOrderId；可传 payOrderId/mchOrderNo、receiverId 过滤；返回 records(JSON数组字符串) |
| 查询分账用户可用余额 | POST /api/division/receiver/channelBalanceQuery | 必填 receiverId；返回 balanceAmount(分) |
| 分账用户余额提现 | POST /api/division/receiver/channelBalanceCashout | 必填 receiverId、cashoutAmount(分)；state:1成功/0失败；建议先查余额再提现 |

- 下单分账模式 divisionMode：官方明确 =2 商户手动分账（支付成功后手动调用发起分账）；=1 系统自动分账（按后台分组自动执行，其余取值以最新文档为准）；
- 分账关系类型 relationType 枚举：SERVICE_PROVIDER/STORE/STAFF/STORE_OWNER/PARTNER/HEADQUARTER/BRAND/DISTRIBUTOR/USER/SUPPLIER/CUSTOM（CUSTOM 时需传 relationTypeName）；
- 所有分账接口共用 BaseRequest（mchNo/appId/reqTime/version/sign/signType）+ RSA2 签名，返回统一 BaseResponse（code=0 成功，data 有独立 sign 需验签）。

### 4.6 转账/提现接口（transfer & cashout）
流程：开通转账通道 → 确认渠道余额 → 发起转账 → 回调+查询确认终态 → 对账；商户余额提现走提现接口。

| 接口 | 路径 | 要点 |
|------|------|------|
| 发起转账 | POST /api/transferOrder | 必填 mchOrderNo(≤64,幂等键)、ifCode(wxpay/alipay/aliaqfpay)、entryType(WX_CASH/ALIPAY_CASH/BANK_CARD/BANK_CARD_CORPORATE/DG_BALANCE)、amount(分)、currency=CNY、accountNo(微信openid/支付宝登录账号)；选填 accountName(填则上游核名)、bankName、clientIp、transferDesc、notifyUrl、channelExtra、extParam(回调原样返回)；返回 transferId+state |
| 查询转账订单 | POST /api/transfer/query | transferId 与 mchOrderNo 二选一；返回 state、amount、channelOrderNo、errCode/errMsg、createdAt/successTime(13位) 等全字段 |
| 查询转账可用余额 | POST /api/transfer/balance/query | 必填 ifCode(如 aliaqfpay)；返回 balanceAmount(分) |
| 手动提现 | POST /api/cashout/order/create | 必填 mchOrderNo(≤30)、amount(分)、ifCode(如 dgpay)、notifyUrl、remark；返回 cashoutOrderId+state |
| 查询提现详情 | POST /api/cashout/order/query | cashoutOrderId 与 mchOrderNo 二选一；返回 state、amount、balance(提现前余额)、bankName/accountNo/accountName(成功时返回)、successTime |

- 转账状态 state 枚举：0-订单生成、1-转账中、2-转账成功、3-转账失败、4-转账关闭（仅 2/3/4 为终态）；
- 提现状态 state 枚举：0-提现单初始化、1-提现中、2-提现成功、3-提现失败（无关闭态；失败时冻结余额会释放，勿重复提现）；
- 转账/提现均为异步，发起返回的 state=0/1 只是受理状态，业务必须以终态+回调(平台公钥验签)/查询双确认为准，且回调需幂等（返回 SUCCESS）；
- 共用 BaseRequest + RSA2 签名，返回统一 BaseResponse（code=0 成功，data 有独立 sign 需验签）。

### 4.7 退款/回调接口（refund & webhook）
流程：校验原单可退 → 发起退款(mchRefundNo 幂等) → 退款回调+查询双确认终态 → 原支付单变"已退款"。

| 接口 | 路径 | 要点 |
|------|------|------|
| 统一退款 | POST /api/refund/refundOrder | 原单 payOrderId 与 mchOrderNo 二选一；必填 mchRefundNo(≤64,幂等键)、refundAmount(分)、currency=CNY、refundReason；选填 notifyUrl(退款回调)、clientIp、channelExtra、extParam(回调原样返回)；返回 refundOrderId+state |
| 查询退款订单 | POST /api/refund/query | refundOrderId 与 mchRefundNo 二选一；返回 payOrderId、payAmount、refundAmount、state、channelOrderNo、successTime(13位) |

- 退款状态 state 枚举：0-订单生成、1-退款中、2-退款成功、3-退款失败、4-退款关闭（仅 2/3/4 终态；支持部分/多次退款，累计 ≤ 原支付金额）；
- 支付通知回调（Webhook）POST /webhooks/payment/notification：**form-urlencoded 表单（非 JSON）**，14 必填字段（payOrderId/mchNo/appId/mchOrderNo/ifCode/wayCode/amount/currency/state/subject/body/createdAt/reqTime/sign）；支付单 state：0生成/1支付中/2成功/3失败/4已撤销/**5已退款**/6关闭；
- 回调处理：平台公钥验签 → 幂等去重 → 金额/订单号核对 → 落库 → 返回纯文本 success/SUCCESS；非 success 按 0/30/60/90/120/150 秒重试；支付回调与退款回调各用各的 notifyUrl（统一下单/退款接口分别传）。

### 4.8 费率/汇率（商务条款，接口能力之外）
- 官方 API 文档【不包含】任何费率/手续费/汇率接口或字段（已核实 llms.txt 索引与统一下单响应，无 fee/rate/charge 相关字段）；官网(tlepay.com)同样不公开费率表，原文声明"涉及费率、结算周期、跨境与资金类产品，以正式协议与持牌合作方规则为准"、"费率与规则以协议为准"；费率是商务合同约定，按商户行业/交易量/风险等级差异化，需找粤收付商务确认或查合同；
- 境内所有通道（微信/支付宝/云闪付/银联/数字人民币/银行网关）均以 CNY 计价结算，通道之间不存在"汇率"；数字人民币(DCEP)与人民币 1:1 等值兑换；跨境/外币结算不在开放 API 范围，需单独商务沟通；
- 接口层面无法查询费率；实际费率以结算账单为准（结算单/账单每笔列出手续费，可按账单倒推实际费率）；
- 市场公开参考区间（非官方承诺，仅供参考）：微信/支付宝扫码类 0.38% 起（0.38%~0.6%），云闪付/银联收单 0.5% 起，银行快捷/网银 0.4%~1%，基础收单费率低至 0.25% 需高流水谈判；转账/提现/分账类按笔或按比例，均以商务约定为准。

## 5. 能力边界（明确不支持的场景）
- 不支持非粤收付官方接口的定制开发；
- 不支持代商户申请粤收付账号/密钥；
- 不支持跨语言的业务逻辑定制（仅聚焦接口对接层）；
- 不支持违规操作指导（如跳过验签、伪造参数）。

## 6. 版本更新日志
| 版本 | 更新时间 | 更新内容                  |
|------|----------|---------------------------|
| v1.0 | 2024-XX-XX | 初始版本，覆盖核心接口对接 |
| v1.1 | 2026-08-13 | 修正签名算法为 RSA2（SHA256withRSA+Base64，末尾不加密钥）；补充金额/时间/货币规范；依赖表更新（openssl/pycryptodome/crypto.rsa） |
| v1.2 | 2026-08-13 | 新增 4.4 支付方式枚举（24 种 wayCode 全量 + channelExtra 要求） |
| v1.3 | 2026-08-13 | 新增 4.5 分账接口（绑定/发起/查询/余额/提现 5 接口 + divisionMode + relationType 枚举） |
| v1.4 | 2026-08-13 | 新增 4.6 转账/提现接口（发起转账/查询转账/余额查询/手动提现/提现详情 5 接口 + state 状态机 + 幂等/双确认要点） |
| v1.5 | 2026-08-13 | 新增 4.7 退款/回调接口（统一退款/查询退款 + 退款状态机 + 支付回调 Webhook：form-urlencoded 格式、14 必填字段、state 含5已退款、重试 0/30/60/90/120/150s） |
| v1.6 | 2026-08-13 | 新增 4.8 费率/汇率说明（官方接口无费率字段、境内全 CNY 无汇率、数币 1:1、市场参考区间 0.25%~1%） |