# 知网公共用户端完整流程

## 入口和角色

- /pzw 是面向公开用户的自助流程：选产品、上传、建单、支付、查报告。
- /zw 是凭证流程：用户已有订单号/检测卡号/淘宝主或子订单号，先查询凭证，再上传对应产品。
- 用户只需要看到本站订单号、产品、支付/检测状态和报告页面；供应商、人工履约、余额和路由是后台职责。

## /pzw 自助流程

1. 打开 https://cnki.cqccjy.cn/pzw，确认 HTTPS 和主机名。
2. 获取 GET /api/paper/cnki/public/config?channel=pcnki；enabled=false 或 products 为空时停止正式提交。
3. 根据论文层级/用途选择产品；价格、格式、提示字符范围以实时响应为准。
4. 填题目和作者；需要时填 acceptTime；勾选用户协议和隐私政策。
5. 获取 presign，使用返回的 HTTPS uploadUrl 做 PUT，再创建 order/create。
6. 保存 orderNo，不保存签名 URL、header 或 objectKey。
7. 如果返回 canPay/canSelectCard，用户在原页面选择检测卡号、微信或支付宝。
8. 支付后进入 /pzw/check?orderNo=订单号，等待检测状态变化。

## /zw 凭证流程

1. 打开 https://cnki.cqccjy.cn/zw。
2. 输入订单号、检测卡号、淘宝主/子订单号或第三方支付单号。
3. 调用 order/query?keyword=，读取 productCode、productName、orderNo、canUpload。
4. canUpload=false 时不要上传；可能是已上传、已消费、已失效或已进入报告流程。
5. 选择与凭证一致的产品，上传后建单请求带 orderNo；不创建无凭证新单。
6. 继续用实际 orderNo 查询，不用第三方凭证拼路径。

## 文件与元数据校验

- 题目：必填，最大 255。
- 作者：必填，2–64，至少有中文或 ASCII 字母/数字。
- 日期：只有产品或页面要求时填写 YYYY-MM-DD。
- 文件：按实时 fileType；页面建议 20 MB 内，脚本硬上限 50 MiB。
- 当前公开页面不让用户填写学校、班级、类型；不要手动造字段。

## 支付阶段

- 订单新建后常见状态是 WAIT_PAY + UNPAID。
- 页面可能显示检测卡号、微信、支付宝；配置关闭某一方式时不建议用户强行调用接口。
- 二维码支付请求可返回二维码、payAmount、outTradeNo、status；用户点击“我已完成支付”后页面再查询。
- 在线支付弹窗关闭不等于订单关闭；若 payStatus=PAYING 或 canPay=true，仍应在原订单页恢复支付。
- 检测卡/淘宝订单核销是一次性业务，skill 不代核销。

## 检测等待

前端约每 6 秒查询一次同一订单，状态为 PAYING、PAID、DETECTING、SUBMIT_BLOCKED、SUBMIT_FAIL 时会继续轮询；查询失败会停止轮询。脚本不做无限轮询，返回唯一下一步即可。

## 报告阶段

- COMPLETED 才是页面下载/预览条件。
- 下载入口是本站 /pzw/check 或 /zw/check；页面会调用 report-download-url。
- reportNum、rateInfo 和报告 URL 只在服务端返回时使用；不根据订单号猜报告地址。
- 报告完成后尽快保存；页面提示最近 3 天保留。
- 删除报告是破坏性动作，脚本不提供。
