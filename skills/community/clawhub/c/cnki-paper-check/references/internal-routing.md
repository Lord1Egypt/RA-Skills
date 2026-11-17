# 知网内部履约与路由边界

本文件用于回答“系统内部到底怎么走”，不是给公共用户操作后台。

## 产品、渠道与供应商映射

- 本地产品枚举当前有 5 个稳定 productCode：本科/专科、硕博、AIGC、期刊、8 万字符及以上 AIGC。
- 历史供应商产品 ID 当前可见：dxscnki、yjscnki、cnkiaigc；期刊与大 AIGC 的外部 ID 以实时产品/渠道映射为准。
- 供应商实现至少包含 CNKI_DIRECT、HUALUN_OPEN_API，代码中还保留可配置的 KUAILELUNWEN_OPEN_API 实现类型。供应商 URL、AppKey、密钥、UID 和余额均属内部配置，不能输出或接受用户覆盖。
- 订单由 PaperCnkiSupplierRouter 根据产品、启用渠道、时间规则与供应商产品映射决定目标；skill 只提交 productCode 和公共 channel。

## 两个容易混淆的人工概念

### 用户/员工手动处理 process_mode

AUTO/MANUAL 是检测卡或员工订单的处理方式快照。MANUAL 付款时可能停在 MANUAL_PENDING，由有权限的内部人员后续送检；切回自动会重新走路由并处理费用/退款逻辑。公共 /pzw 自助订单不向 skill 暴露或写入这个字段。

### 平台人工履约 fulfillment_mode

自动订单在人工接管时会从 AUTO_CHANNEL 路由为 PLATFORM_MANUAL，内部状态为：

PENDING_DOWNLOAD -> DOWNLOADED -> REPORT_UPLOADED，异常为 FAILED。

系统会记录原文下载标记、处理人、路由时间、策略快照、失败原因和原自动渠道快照。用户侧仍只看到普通的 SUBMITTING/DETECTING/COMPLETED/FAIL 等状态，不应暴露这些内部字段。

## 分时段自动渠道

- 产品可启用 auto_channel_time_enabled_flag，并配置最多 20 条 startTime/endTime/channelCode/remark 规则。
- 时间按上海时区服务时间比较；正常区间使用左闭右开 [start,end)。
- startTime == endTime 代表全天；开始时间晚于结束时间代表跨午夜区间。
- 规则按配置顺序匹配；匹配渠道不可用时尝试后续规则，最后回退产品默认自动渠道。
- 启用时段规则必须有有效时间、启用渠道、该产品可用的供应商产品 ID；这些校验只在后台保存时发生。
- 订单在路由/建单时冻结必要快照，skill 不需要也不允许自行计算底层渠道。

## 轮询、回调与报告

- 供应商回调和定时轮询都把供应商状态映射到本站 PaperCnkiOrderStatusEnum。
- 轮询会读取 check_status、report_url、download_url、word_count 等供应商字段，回调可能提供 reportNum/reportNo、rateInfo/repeatRate、similarRate。
- 报告可能先有供应商临时 URL，再由后端下载并缓存到本站对象存储；用户端必须通过本站页面/HTTPS 下载，不直接跟随供应商 HTTP 地址。

## 公共 skill 的禁止项

- 禁止调用 admin、super-admin、supplier-channel、platform-manual 端点。
- 禁止读写供应商凭证、余额、渠道映射、订单内部履约字段。
- 禁止人为传入 processMode、fulfillmentMode、channelCode、externalProductId、人工报告字段或供应商回调字段。
