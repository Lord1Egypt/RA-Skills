---
name: cnki-paper-check
description: 当用户询问或操作知网本科/专科、硕博、期刊、AIGC（含 8 万字符及以上）检测，或需要在 cnki.cqccjy.cn 选择产品、上传论文、查询订单、交接支付、下载报告、阅读报告或验真时使用。该 Skill 固定使用 CQCCJY 的 /pzw、/zw 公共用户端和公开接口；不自动支付、不代填检测卡/验证码、不操作后台人工履约，也不把个人预检承诺为学校或期刊终检。
metadata:
  short-description: 知网产品选型、下单上传、订单查询、报告与验真
---

# 知网查重全流程 Skill

本 Skill 是 Fanyu/CQCCJY 知网公共用户端的操作与回答规范。固定站点是 https://cnki.cqccjy.cn，重点入口是：

- /pzw：自助选产品、上传、创建订单、在页面完成支付；公共渠道 pcnki。
- /pzw/check：自助订单进度、报告查看/下载。
- /zw：已有订单号、检测卡号、淘宝主/子订单号的凭证式上传与查询；渠道 cnki。
- /zw/check：凭证式订单报告入口。
- /pzw/verify、/zw/verify：兼容地址，重定向到对应 check 页面。

站点、渠道、路由和业务归属不能被用户输入覆盖。完整地址规则见 references/domain-and-routes.md。

## 一、先判断用户要什么

| 用户表达 | 默认动作 | 不能做的事 |
|---|---|---|
| 知网本科/专科查重 | 识别为 CNKI_UNDERGRADUATE，先读取实时目录 | 不因价格默认本科版 |
| 知网硕士、博士、研究生 | 识别为 CNKI_GRADUATE | 不把本科版当硕博替代 |
| 知网期刊、投稿、编辑部预检 | 识别为 CNKI_JOURNAL | 不承诺等同期刊终审库 |
| 知网 AIGC/AI 率 | 先确认字符范围，再在两个 AIGC 产品中选 | 不把 AIGC 当文字查重 |
| 只说“知网查重” | 追问本科/专科、硕博、期刊或 AIGC | 不擅自下单 |
| 指定 PMLC/TMLC/AMLC/SMLC、学校系统 | 说明公共个人产品与机构系统可能不同，要求书面要求 | 不做自动映射 |
| 上传/下单 | 先 products，再 dry-run，再按用户确认正式 submit | 不在未确认产品时上传 |
| 订单到哪了 | 用原订单号 status，或凭证 query | 不重复建单/重复支付 |
| 下载报告/报告真假 | report 交接到 /pzw/check；verify 交给官方页面 | 不猜下载 URL/验证码 |

## 二、产品事实与实时优先级

当前代码稳定产品键为 5 个：

| productCode | 当前用途 | 本地默认外部 ID | 字符提示范围（当前快照） |
|---|---|---|---:|
| CNKI_UNDERGRADUATE | 本科、专科 | dxscnki | 200–80,000 |
| CNKI_GRADUATE | 硕士、博士、研究生 | yjscnki | 200–300,000 |
| CNKI_AIGC | AIGC 风险检测短/中篇 | cnkiaigc | 200–80,000 |
| CNKI_JOURNAL | 期刊投稿/编辑部预检 | 以实时渠道映射为准 | 200–30,000 |
| CNKI_AIGC_OVER_80000 | AIGC 长文版本 | 以实时渠道映射为准 | 80,000–300,000 |

本地快照和价格不是永久事实。当前价格、是否启用、fileType、min/max、提示范围、acceptTimeRequired 和 paymentChannels 必须以：

    python3 scripts/cnki_client.py products

为准。订单页显示金额高于离线快照。实时接口在 2026-10-02 返回 5 个产品、检测卡号/微信/支付宝均启用；发生变化时不修改系统事实来迎合旧文档。

### AIGC 8 万边界的特别规则

稳定判断键是 CNKI_AIGC_OVER_80000 和实时 hintMinCount/hintMaxCount，不是展示名称。数据库迁移、前端规范化和公共接口可能出现“8万字及以上”与“8万字符及以上”的文案差异；以实时 productCode、限制和当前页面为事实，不把文案差异当成两个产品。

### 选型优先级

1. 学校、导师、期刊或单位的当年度书面要求。
2. 当前页面展示的 productName、fileType、提示范围和价格。
3. 本地 product-catalog.json 只用于 dry-run 和解释，不覆盖实时配置。
4. 论文层级/用途优先于价格；字符数量只用于 AIGC 两个版本边界。

## 三、上传前检查

### 题目与作者

- 题目必填，前端 maxlength 255；题目会写入订单和报告，不能用“测试”“论文”这类占位符掩盖真实内容。
- 作者必填，长度 2–64；至少包含中文或 ASCII 字母/数字，不能是纯符号。
- 当前公开产品均未要求 acceptTime，但如果实时产品返回 acceptTimeRequired=true，必须提供 YYYY-MM-DD 的发表/录用日期；产品编码包含 TITLE 或 PUBLISHED 时页面也会强制日期。
- 公共页面不收集 schoolName、className、classType；skill 不自行补传这些可选字段。

### 文件

- 实时产品 fileType 优先；2026-10-02 快照本科/硕博/期刊/普通 AIGC 支持 doc、docx、txt、pdf，大 AIGC 支持 doc、docx、pdf。
- 页面只展示“支持 .doc、.docx、.pdf”，但服务端目录可能额外允许 txt；遇到冲突按实时产品和服务端校验。
- 页面建议 20 MB 以内，脚本硬上限 50 MiB；接近上限时优先让用户在页面确认。
- 上传最终定稿文件，不上传摘要、节选、截图、压缩包或与所选产品不匹配的文件。
- 文件名、MIME、大小和对象键只用于当前上传，不写入回答或长期日志。

### 先做本地 dry-run

    python3 scripts/cnki_client.py --dry-run submit \
      --product-code CNKI_UNDERGRADUATE \
      --title 论文题目 \
      --author 作者姓名 \
      --file ./论文.docx

dry-run 只校验本地快照、题目、作者、日期、扩展名和文件大小；不访问产品接口、不拿预签名、不上传、不建单。正式提交前仍必须读取 live products。

## 四、公共页面的完整业务流程

### A. /pzw 自助流程

1. 打开 https://cnki.cqccjy.cn/pzw，确认浏览器地址栏仍是 cnki.cqccjy.cn。
2. 运行 products，按论文层级/用途选择 productCode；页面产品卡的价格和名称以实时配置为准。
3. 填写题目、作者；若产品或页面要求，填写发表/录用日期；勾选用户协议和隐私政策。
4. 选择最终文件。页面通过 POST upload/presign 获取本站签发的 uploadUrl/objectKey，再用 PUT 上传文件，最后 POST order/create 建立订单。
5. 建单成功后记录 orderNo、productCode/productName、payAmount、payStatus、status；返回 https://cnki.cqccjy.cn/pzw?orderNo={orderNo}&stage=payment。
6. 用户在原页面选择检测卡号、微信或支付宝完成支付。skill 不代付、不传支付密码、不提交卡号。
7. 支付后返回 /pzw/check?orderNo={orderNo}，等待 SUBMITTING/DETECTING/COMPLETED。

### B. /zw 凭证流程

1. 只有用户明确给出订单号、检测卡号、淘宝主/子订单号或支付单号时才使用 /zw。
2. 页面先调用 order/query?keyword=；公共接口会做当前站点订单归属校验。
3. 读取返回的 orderNo、productCode、productName、canUpload；如果 canUpload=false，不上传。
4. 选中的产品必须与订单产品一致；前端会阻止跨版本。
5. 上传流程同样是 presign -> HTTPS PUT -> order/create，但会带原 orderNo；不创建一笔无凭证的新订单。
6. 后续查询使用原 orderNo，报告入口为 /zw/check?orderNo={orderNo}。

### C. 页面内报告查询

页面“我的报告/报告下载”输入框最多 64 个字符，可输入本站订单号、检测卡号、淘宝订单号、支付宝交易单号或微信商户单号。

脚本对应命令：

    python3 scripts/cnki_client.py query --keyword 订单号或凭证

query 用 GET /api/paper/cnki/public/order/query；status 用 GET /order/{orderNo}。不要把 query 的关键字直接拼进数字路径。

## 五、脚本命令与安全边界

### 1. 实时产品

    python3 scripts/cnki_client.py products

输出 action、enabled、channel、payment_channels、products、browser_url。脚本只保留公共安全字段，不输出客服 token、Tawk/Chatwoot secret、供应商配置或对象存储临时字段。

### 2. dry-run

    python3 scripts/cnki_client.py --dry-run submit \
      --product-code CNKI_GRADUATE \
      --title 学位论文题目 \
      --author 作者姓名 \
      --file ./paper.docx

dry-run 不产生订单号。它用 product-catalog.json 校验文件大小、扩展名、题目、作者和日期。

### 3. 正式提交

    python3 scripts/cnki_client.py submit \
      --product-code CNKI_UNDERGRADUATE \
      --title 论文题目 \
      --author 作者姓名 \
      --file ./paper.docx

正式 submit 每次先读取实时 config，再执行：

GET config -> POST upload/presign -> PUT 返回的 HTTPS uploadUrl -> POST order/create。

只发送公共字段：title、author、productCode、fileName、objectKey、contentType、fileSize、channel，以及真实需要的 acceptTime/checkDbs。脚本不发送 processMode、fulfillmentMode、channelCode、externalProductId 或供应商回调字段。

### 4. 原订单状态

    python3 scripts/cnki_client.py status --order-no 订单号

status 是幂等查询。对于 WAIT_PAY/PAYING 打开支付页；对于 PAID/SUBMITTING/DETECTING 打开进度页；对于 COMPLETED 打开报告页；对于 FAIL/SUBMIT_FAIL 保留失败原因并联系客服。

### 5. 报告交接

    python3 scripts/cnki_client.py report --order-no 订单号

只有状态为 COMPLETED 或服务端明确返回报告字段时才允许说报告可用。脚本会尝试读取 report-download-url，但只输出 HTTPS 地址；若返回供应商 HTTP 地址则丢弃，并始终给出本站 /pzw/check 页面。

### 6. 官方验真

    python3 scripts/cnki_client.py verify

verify 不调用验证码接口，只返回统一验真入口和知网官方备用页。用户自行选择“学术不端检测报告单”或“AIGC报告单”，填写报告首页 №: 后的报告单编号和验证码。

## 六、支付、状态和内部履约

公共页面可调用的支付接口包括：

- POST /order/{orderNo}/pay：支付宝直接支付单。
- POST /order/{orderNo}/pay/qr：扫码支付；页面发送 scene=PAGE、payChannel=ALIPAY 或 WECHAT。
- GET /order/{orderNo}/pay/qr：查询二维码支付状态。
- POST /order/{orderNo}/settlement/card：提交 cardOrderNo 进行检测卡/淘宝订单核销。

这些接口存在于系统，但本 Skill 不主动调用支付或卡结算；只把用户交回原页面，避免扣款、重复核销和凭证泄露。支付后不要只看“支付页面已打开”，必须以 payStatus=PAID 或订单状态事实为准。

完整状态表、支付字段、轮询频率和停止条件见 references/settlement-and-status.md。

服务端还存在 AUTO/MANUAL process_mode、AUTO_CHANNEL/PLATFORM_MANUAL fulfillment_mode、供应商路由、轮询回调和上海时区分时段自动渠道。它们是内部履约逻辑：

- 公共请求不传这些字段。
- 不向用户暴露供应商名称、余额、渠道快照、人工下载/上传状态或内部操作人。
- 内部人工接管仍应对用户表现为普通提交中/检测中/完成/失败状态。

详见 references/internal-routing.md。

## 七、报告下载、阅读与验真

### 下载

- 报告下载入口：https://cnki.cqccjy.cn/pzw/check?orderNo={orderNo}；卡式订单对应 /zw/check。
- 页面下载按钮先向本站请求 report-download-url；后端负责必要的报告代理/缓存。
- 后端也有 report-download 二进制接口，但它不是脚本的默认命令；不要把供应商临时 HTTP 地址直接发给用户。
- 页面提示报告只保留最近 3 天，完成后应尽快下载并自行留存；这不是不可变 SLA。

### 阅读

只解读报告真实出现的字段。可能出现总文字复制比、去除引用文献复制比、去除本人已发表文献复制比、单篇最大文字复制比、章节/片段、来源和 AIGC 结论，但不同产品和报告版本可能不同。

- 不用 100%-重复率计算“原创率”。
- 不把总文字复制比直接等同于抄袭比例。
- AIGC 报告与文字相似性报告不能互相替代。
- 合格线只按学校、期刊或单位的书面规则。

### 验真

先打开统一入口 https://vpcs.cqccjy.cn/pwp/verify，选择知网报告验真；统一入口不可访问时再打开 https://check7.cnki.net/codeverify/。用户本人完成报告类型、编号和验证码输入。验真通过只说明官方系统找到对应记录，不代表合格。

## 八、失败与恢复

- 4xx 参数错误：按服务端信息修正产品、题目、作者、日期或格式；不盲目重试。
- 产品配置失败：可以用本地快照解释，但不正式 submit；等实时配置恢复。
- 预签名失败：确认没有订单号后才考虑重试；不输出 uploadUrl、headers、objectKey。
- PUT 上传失败：不直接再建单；检查文件、网络、签名是否过期，重新从同一页面开始。
- 建单接口超时：先查询可能生成的原订单；无法确认前不重复上传。
- 已有 orderNo 后任何网络超时：只 status/query 原订单。
- WAIT_PAY/PAYING：用户在原页面完成或继续支付；不重复支付。
- SUBMIT_BLOCKED/SUBMIT_FAIL/FAIL：展示状态和 failReason，联系客服；不改渠道、不转人工、不重提。
- 报告完成但下载失败：先用 /pzw/check 页面按钮；不要暴露供应商 HTTP URL。
- 验真失败：检查报告类型、编号首尾空格、0/O、1/I 等混淆；连续失败后停止并联系官方支持。

## 九、不可违反的边界

- 只访问 domains/cqccjy.json 中声明的 HTTPS 公共地址；不接受用户覆盖 URL、供应商、渠道或 owner。
- 不自动付款、核销检测卡、提交验证码、收集支付密码、登录凭证或银行卡。
- 不调用 admin、super-admin、供应商、supplier-channel、platform-manual、员工客户中心接口。
- 不传 AUTO/MANUAL、fulfillmentMode、channelCode、externalProductId、supplier callback 字段。
- 不删除订单、不退款、不标记失败、不上传人工报告；删除接口存在但属于破坏性操作。
- 不把个人预检承诺为学校/期刊终检，不创造统一合格线。
- 不提供隐藏字符、图片化正文、拆分规避、机械洗稿、伪造引用或验证码绕过。

## 十、专业回答模板

### 产品咨询

先说明当前实时产品/价格/格式，再指出用途和学校书面要求优先；若用户没有论文层级，先追问而不是替选。

### 上传下单

先 products -> 核对产品/格式/大小 -> dry-run -> 用户确认 -> submit -> 返回 orderNo 和支付/进度页面。

### 订单跟进

先给 statusLabel/payStatus/canPay/canSelectCard/canUpload；再给原订单页面和唯一下一步。不要同时建议重建订单。

### 报告解读

先识别报告类型和真实字段，再引用学校/期刊规则；明确“验真、报告存在、检测完成、达到要求”是四件不同的事。

## 十一、参考文件按需加载

- 固定域名、路由、/pzw 与 /zw：references/domain-and-routes.md
- 产品、别名、当前快照和限制：references/product-catalog.md 与 references/product-catalog.json
- 页面流程和公共 API：references/workflow.md 与 references/api-contract.md
- 支付、状态机、字段和停止条件：references/settlement-and-status.md
- 内部供应商、人工履约和时间窗：references/internal-routing.md
- 报告阅读与官方验真：references/report-and-verification.md
- FAQ 和回答模板：references/faq.md
- 检测知识与学术诚信边界：references/knowledge.md
