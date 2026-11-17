# 知网公共 API 契约

脚本 scripts/cnki_client.py 只访问 domains/cqccjy.json 中的 HTTPS 公共地址。所有 JSON 字段名以当前 Controller、前端 API 和实时响应为准。

## 统一前缀

    https://cnki.cqccjy.cn/api/paper/cnki/public

自助 /pzw 请求显式传 channel=pcnki；/zw 页面传 channel=cnki。不要传内部供应商渠道或路由字段。

## 1. config

    GET /config?channel=pcnki

返回 PaperCnkiPublicConfigVO：ownerEmployeeId、channelCode、enabled、customerServiceQrUrl、客服聊天配置、customerServiceFloatEnabled、reductionEntryEnabled、paymentChannels、products。

每个公开产品可能含 productCode、productName、externalProductId、unit、pricingMode、unitWordCount、fileType、minCount、maxCount、hintMinCount、hintMaxCount、defaultCheckDbs、acceptTimeRequired、salePrice、priceLabel。客服 token 和供应商配置只能在页面需要时由前端使用，脚本输出会主动过滤。

## 2. presign、上传和建单

### presign

    POST /upload/presign
    { fileName, productCode, channel }

返回 uploadUrl、objectKey、可选 headers。浏览器/脚本必须使用返回的 HTTPS uploadUrl 做 PUT，不能改 host、路径、query、header 或把票据发到其他站点。

### create

    POST /order/create
    {
      title, author, productCode, fileName, objectKey,
      storageService, contentType, fileSize, channel,
      orderNo?, acceptTime?, checkDbs?
    }

页面公共上传实际发送 title、author、fileName、objectKey、contentType、fileSize、channel；凭证式 /zw 额外带 orderNo；acceptTime/checkDbs 只有真实有值时发送。后端 DTO 允许 schoolName/className/classType，但当前公开页面不收集，skill 不编造。

成功返回 PaperCnkiPublicOrderVO：公共查询字段加 payAmount。若未返回 orderNo，不说“已下单”。

## 3. 订单查询

### 数字订单路径

    GET /order/{orderNo}

用于 status/report；Controller 路径参数是 Long，脚本应传本站数字订单号。

### 关键字查询

    GET /order/query?keyword=订单号或凭证

keyword 可是本站订单号、检测卡号、已核销卡号、淘宝主/子订单号、支付宝交易单号或微信商户单号；后端按多个索引尝试解析并做当前销售站点归属校验。

脚本命令：

    python3 scripts/cnki_client.py query --keyword 订单号或凭证

## 4. 支付和卡结算（只记录，不自动执行）

    POST /order/{orderNo}/pay
    POST /order/{orderNo}/pay/qr
    GET  /order/{orderNo}/pay/qr
    POST /order/{orderNo}/settlement/card

页面二维码请求体是 scene=PAGE、payChannel=ALIPAY 或 WECHAT；卡结算请求体是 cardOrderNo。Skill 不调用这些写入/扣款接口，避免重复支付或一次性卡号被核销。

## 5. 报告

    GET /order/{orderNo}/report-download-url
    GET /order/{orderNo}/report-download

前者返回报告地址字符串，后者返回二进制附件。公共页面当前使用前者并触发浏览器下载；后端可能把供应商 HTTP 临时报告镜像/缓存到本站 OSS。脚本只输出 HTTPS 地址，非 HTTPS 地址丢弃；用户优先使用 /pzw/check 或 /zw/check 的按钮。

## 6. 删除

    POST /order/{orderNo}/delete

接口存在且页面在 canDeleteReport=true 时会显示“删除报告”。删除后不能继续下载，属于破坏性操作，脚本不提供命令，除非用户明确要求且另行确认页面行为。

## 7. 统一脚本输出

输出 JSON 重点字段：

    action, order_no, product_code, product_name,
    status, status_label, pay_status, pay_status_label,
    pay_amount, word_count, fail_reason,
    browser_url, browser_urls, report_download_url,
    browser_action, next_action

上传票据、签名 URL、临时 header、objectKey 和文件正文不出现在输出中。没有服务端事实的字段使用 null，不猜测。
