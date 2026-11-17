# 知网支付、卡结算与状态机

## 用户侧两条主流程

### A. /pzw 自助订单

1. 读取公共配置并选择一个产品。
2. 上传文件，服务端先返回预签名 OSS 地址，再由浏览器 PUT 文件，最后创建订单。
3. 新订单通常为 WAIT_PAY + UNPAID，页面显示应付金额和可用支付方式。
4. 页面可选择检测卡号、微信或支付宝。在线支付由页面生成二维码/支付单；skill 不点击、不代填、不轮询支付凭证。
5. 支付成功后服务端把订单推进到提交/检测；用户继续用同一订单号查询。

### B. /zw 凭证上传

1. 用户先提供订单号、检测卡号或淘宝主/子订单号。
2. 页面通过 GET /order/query?keyword= 解析凭证并回填产品；只有 canUpload=true 才允许上传。
3. 上传时产品必须与凭证产品一致；前端会阻止跨版本上传。
4. 用户提交后不再重复创建订单；后续仍按原 orderNo 查询。

## 支付方式事实

实时公共配置在 2026-10-02 快照中返回：

| channel | 页面标签 | 当前状态 | 说明 |
|---|---|---|---|
| DETECTION_CARD | 检测卡号支付 | enabled | 通过 settlement/card 核销一个未使用凭证 |
| WECHAT | 微信支付 | enabled | 页面二维码模式，mobilePayMode=SCAN |
| ALIPAY | 支付宝 | enabled | 页面二维码/直接支付模式，mobilePayMode=DIRECT |

以上是快照，不是永久承诺；正式下单和支付页的 paymentChannels、订单 canPay/canSelectCard、二维码返回状态优先。

## 订单状态

后端枚举为：

| code | label | 用户下一步 |
|---|---|---|
| PENDING_UPLOAD | 待上传 | 在原订单/凭证页面补传论文 |
| WAIT_PAY | 待支付 | 打开原订单支付页；不要重建订单 |
| PAYING | 支付中 | 查询二维码支付状态；必要时刷新原页面 |
| PAID | 已支付 | 等待系统提交检测 |
| MANUAL_PENDING | 待手动送检 | 只可能出现在内部人工流程或手动处理凭证；联系页面客服 |
| SUBMITTING | 提交中 | 等待供应商接收，不重复提交 |
| SUBMIT_BLOCKED | 余额不足待提交 | 用户侧显示为系统处理中；联系平台客服，不改渠道/余额 |
| SUBMIT_FAIL | 提交失败 | 保留订单号和 failReason，联系客服 |
| DETECTING | 检测中 | 按原订单轮询，前端默认约 6 秒刷新一次 |
| COMPLETED | 报告完成 | 下载/在线预览，尽快保存 |
| FAIL | 检测失败 | 停止轮询，联系客服，不重建订单 |
| DELETED | 报告已删除 | 不能当作报告可用；删除是破坏性操作 |
| INVALID | 已失效 | 不能继续使用，回到客服/新订单判断 |

支付状态另有独立枚举：UNPAID、PAYING、PAID、CLOSED、REFUNDED。不能仅看 status 判断付款；同时看 payStatus、canPay、canSelectCard。

## 公共字段如何解释

- orderNo：本站订单号；状态接口 /order/{orderNo} 只接受数字路径。
- cardOrderFlag、cardOrderNo：是否与检测卡凭证相关；不能把它们误叫成本站订单号。
- productCode/productName：订单冻结的产品身份；报告查询和上传必须与其匹配。
- wordCount：服务端/供应商解析出的字数，可能在提交或轮询时才出现。
- reportNum：报告单编号线索，用于验真时从报告首页确认，不要把它当订单号。
- reportUrl/reportPreviewUrl/reportMobilePreviewUrl/reportJsonUrl：报告数据字段；只有明确 COMPLETED 才说报告可用。
- rateInfo：页面或回调提供的结果摘要，不能自行改写成“合格/不合格”。
- canUpload/canPay/canSelectCard/canDeleteReport：服务端当前动作权限，优先于模型记忆。

## 何时停止

- 未拿到 orderNo：预签名/建单失败时不声称已下单。
- 已拿到 orderNo：任何超时、支付延迟、回调延迟都先查同一订单。
- FAIL/SUBMIT_FAIL：不自动重提、不自动转人工、不修改渠道。
- DELETED/INVALID：不把旧报告恢复成可用，不再次下载猜测地址。
