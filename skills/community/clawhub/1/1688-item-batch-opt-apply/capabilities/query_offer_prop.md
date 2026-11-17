# query_offer_prop — 定向查询实际商品属性

用户已看到完整优化结果并点击「应用」后调用；仅查询，不写商品、不自动判定无差异。
调用方式沿用插件内已有技能：`accio-mcp-cli call query_offer_prop --json-file ... --raw`，
宿主注入身份，不配置 AK/Token。此处是只读工具，可由 Python 包装；弹写入卡仍必须直接调用。

```bash
python3 "{baseDir}/cli.py" query_offer_prop --items '[{"offerId":"1234567890","propertyNames":["主图","轮播图","首图","商品图","图片"]}]'
python3 "{baseDir}/cli.py" query_offer_prop --items_file "<UTF-8 JSON数组文件绝对路径>"
```

两个参数互斥且必选其一。Windows 优先文件方式，避免 JSON/正则符号被 shell 解析。

## 入参约定

- `items`：1–20 个商品对象，商品 ID 不重复。超过 20 个由主 Agent 分批。
- `offerId`：商品 ID，建议用字符串传入以保留精度。
- `propertyNames`：主 Agent 根据用户要求和最终方案中拟修改的商品字段提炼匹配词，任务 op 仅作参考。
  tool 内部用这些词生成正则匹配真实 CPV；不是用户输入的逐字复制，也不是属性值。
  例如“颜色”可扩展为 `["颜色","色彩","色系","花色"]`。
  同一商品多个任务合并词后去重；不同商品可以使用不同词。
- 只扩展语义相关词，不使用 `.*` 等全匹配表达式。本 CLI 强制非空数组，防止后端将
  空数组/缺省解释为全量查询（每个商品可能有上百个属性）。不擅自回退全量查询。

### 按应用目标选词（参考示例）

| 最终应用目标 | propertyNames 示例 |
|---|---|
| 商品标题 | `["标题","商品标题"]` |
| 主图 | `["主图","首图","商品图","轮播图"]` |
| 详情图 | `["详情图","商品详情","图文详情"]` |

这些词仅用于查询，不代表真实 key 或字段之间可相互替代；实际 key 仍按返回的 name/label 核对。
换背景、多图合成等操作按结果最终应用的位置选词，不固定绑定主图，也不因素材包含模特就查询“模特图”。
用户还要求修改其他属性时补充对应匹配词；同商品多个修改目标合并词后去重。
无商品 ID 的素材任务只交付产物，不进入商品应用或 CPV 查询。

## 返回与主 Agent 判断

返回 `data.items`（实际查询条件）和 `data.properties`（工具原始业务响应）。
仅解开 CLI/MCP 包装，保留业务响应中的 data、success、错误信息和所有商品属性字段，
不裁剪或改写 CPV，不执行 key/value 比较，不产生通过/不通过结论或澄清文案。
CLI 外层 success 表示调用完成；具体商品查询是否成功由主 Agent 查看工具原始返回。

当前样例中，ResultModel.data 是商品数组，商品项含 offerId/success/properties；
属性项含 name（实际属性标识）、label（名称）、inputType（控件类型）、values（当前值）
和 candidates（候选值）。返回结构可能调整，以实际数据为准。

主 Agent 按“先 key，后 value”与真实 CPV 对比：

先根据 name/label 核对模型生成的 key 是否存在、能否明确对应目标属性；未找到或存在歧义时
不能放行，由主 Agent 组织澄清。查询已按匹配词过滤，未返回不代表商品一定没有该属性，
必要时补充相关词查询。不得只因目标 value 在其他属性的候选内，就自动把 key 换成那个属性。

key 明确后，再按该属性的 inputType 判断用户输入的 value：

- SINGLE_SELECT：单个值是否在候选内。
- MULTI_SELECT：所选值是否在候选内。
- TEXT_INPUT：允许自由输入，不校验 value，但仍核对 key。

无须澄清则继续更新商品；需要澄清则由主 Agent 结合上下文生成问题。
用户回答后按澄清内容重新处理，展示完整最终方案，再弹出确认应用卡片，
用户二次确认后更新，流程见 SKILL.md 规则6。
CPV 查询结果和对比判断只用于会话上下文，不通过 save_result 落账。

## 来源

工具：[query_offer_prop](https://1688bot.alibaba-inc.com/#/tool/detail?code=query_offer_prop)。
`propertyNames` 的匹配词语义以本次工具开发者确认的契约为准；详情页曾描述为精确匹配，
该旧描述不能覆盖本约定。响应语义以本次用户提供的 ResultModel/OfferPropertyDTO 样例
为依据；尚未进行真实商家查询联调，新增 inputType 和约束字段须按实际契约补充。
