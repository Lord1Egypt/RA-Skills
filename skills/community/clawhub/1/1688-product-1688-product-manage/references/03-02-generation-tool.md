# 标题、CPV、SKU 的独立工具调用

每次生产一个类型时读取。三个能力分别使用自己的工具、请求、`taskId` 和结果文件，不混成一份生成任务：

| 类型 | 提交与查询工具 | 完成结果 | 最终文件 |
|---|---|---|---|
| `title` | `1688_publish_title_prediction` | `dataJson.title` 非空字符串 | `text/title.json` |
| `cpv` | `1688_publish_cpv_predict` | `dataJson.catProp` 属性数组 | `text/catProp.json` |
| `sku` | `1688_publish_sku_predict` | `dataJson.skuTable` 逐行 SKU 数组 | `text/skuTable.json` |

## 提交参数

只向当前工具传其 schema 声明的参数，不把其他类型字段凑成公共必填项。首次提交省略 `taskId` 或传空字符串；非空 `taskId` 表示查询，不是新提交。

| 参数 | 适用工具与取值 |
|---|---|
| `mainImages` | 三个工具均需：本商品选中的 1—5 个已核验图片银行 URL 的 JSON 数组字符串 |
| `categoryId` | 本链路三项均传已采用真实类目 ID 的数字字符串；CPV/SKU 依赖它取得 schema。标题工具虽允许空值，本发品链路仍先确定类目 |
| `textContent` | 三个工具均支持：当前商品的用户描述/相关源资料；有内容才传，不混入参考款未被采用的事实 |
| `moreInfo` | 三个工具均支持：有来源的补充事实、采用值和约束；未知和冲突不能写成已知事实 |
| `knownProductInfo1` | 三个工具均支持的可选 JSON 对象字符串底稿；仅在确有结构化资料要传时使用，没有则省略 |
| `hangTagImages` | 仅 CPV：吊牌/标签证据图的 JSON 数组字符串，工具取首张，无图可省略或传 `"[]"` |
| `specImages`、`sizeImages` | 仅 SKU：规格图/尺码表的 JSON 数组字符串，各取首张，无图可省略或传 `"[]"` |
| `saleProp1`、`salePropValue1`、`saleProp2`、`salePropValue2`、`skuPrice`、`skuStock` | 仅 SKU 的独立参数：按 `sku-input.json` 的真实行顺序转换，见 [SKU 规则](02-02-sku.md) |
| `store_ref` | 宿主声明且需选择授权店铺时使用真实宿主标识；提交与查询保持同店铺，单店铺按宿主规则可省略 |

图片字段是 JSON 数组字符串，不是路径或直接数组；底稿是 JSON 对象字符串，不是对象。不要多转义一层。schema 的 `required` 数组为空不代表业务提交可以没有主图或 CPV/SKU 类目。

`knownProductInfo1` 可承载当前商品已知信息，如 `textContent`、`moreInfo`、`excelTitle`、`itemNumber`、`itemStock`、销售规格及价格库存字段。只传有来源且本次有效的键，授权推定的规格注明依据，测评/文件编号不冒充货号。独立 `textContent`、`moreInfo` 非空时覆盖底稿同名键；SKU 的六个独立规格/价格库存参数非空时也覆盖底稿。空字符串不能当作清空旧底稿的指令；不得携带过期维度、价格库存底稿。价格库存可空，空列与逐行空位按 [SKU 规则](02-02-sku.md) 编码。标题/CPV 没有六个规格字段的独立入参；确有必要提供这些事实时才放入底稿或已支持的文字参数。

提交前核对所用商品、店铺、图片映射、已采用输入及参数类型。工具成功输出默认正确，按 [03-00](03-00-production.md) 采用，仅处理其规定的明显冲突例外，不逐项复核或删改。当前工具不声明的参数不发送；schema 不兼容时核对差异并按 [恢复规则](00-02-recovery.md) 处理，不自动改走统一素材包。

## 请求形态示例

以下地址、类目和数值只用于说明类型，不能直接作为实际请求或缺省值。运行时从本商品文件取值。

标题提交到 `1688_publish_title_prediction`：

```json
{"mainImages":"[\"https://example.invalid/bank/main.jpg\"]","categoryId":"315","textContent":"用户说明：黑色纯棉圆领短袖T恤","moreInfo":"只使用已提供的商品事实，不补造品牌或功效"}
```

CPV 提交到 `1688_publish_cpv_predict`：

```json
{"mainImages":"[\"https://example.invalid/bank/main.jpg\"]","categoryId":"315","textContent":"用户说明：黑色纯棉圆领短袖T恤","hangTagImages":"[]"}
```

SKU 提交到 `1688_publish_sku_predict`：

```json
{"mainImages":"[\"https://example.invalid/bank/main.jpg\"]","categoryId":"315","saleProp1":"颜色","salePropValue1":"黑色$黑色","saleProp2":"尺码","salePropValue2":"M$L","skuPrice":"19.9$19.9","skuStock":"100$80","specImages":"[]","sizeImages":"[]"}
```

分别向产生该任务的原子工具查询，`taskId` 必须替换为本次真实返回值；有显式店铺选择时同时带原 `store_ref`：

```json
{"taskId":"本商品本类型的真实任务ID"}
```

## 提交、记录、查询

1. 检查 `text/tasks/<类型>/`：已有有效产物则复用；已有运行任务则查原任务；结果未知先恢复，不能直接再提交。
2. 保存 `request.json`、工具名、店铺、输入来源和校验值，再提交当前工具。每次原始回执单独留存，不覆盖旧回执。
3. 检查外层成功，解析字符串或对象形式的 `dataJson`。若明确 `finished` 且本类型结果字段齐全可解析，按 [03-00](03-00-production.md) 落盘；如果是 `processing`，必须取得真实非空的单个 `dataJson.taskId`。
4. 保存任务 ID；后续调用同一原子工具，传 `taskId` 及适用的 `store_ref`，无需重传主图、SKU 等原始生成参数。若当前实际 schema 明确另有查询必填项，按该工具契约补入并留证，不能据习惯拼接别的工具参数。
5. 约每 3 秒查询一次，单轮累计约 120 秒；工具返回更长间隔时遵守。仍在处理则保存续跑位置并简短告知用户，不重新提交、不宣称完成，也不自行建立定时任务。正常查询期间不逐次播报或请求用户确认。
6. `finished` 但本类型结果缺失、返回 ID 与记录冲突、状态不明时，不当成功、不重复提交，保留回执核对。明确失败则记录原因；超时或传输失败按原任务恢复。

状态区分未提交、运行中、待恢复、失败、结果待核实、结果已取得、已采用。`finished` 是工具状态；外层成功且本类型结果字段齐全可解析后按 [03-00](03-00-production.md) 保存并标已采用，不设二次内容验收。

单项成功不要求同时返回另外两项；响应夹带其他类型内容不自动采用。发布图片与详情仍按 [03-03](03-03-display-materials.md) 独立选择和组装。

保存产物来源、依赖校验值与回执；输入已改变时，旧结果只能留作历史。一次失败不抹掉其他已采用产物，恢复任务始终对应同一商品、同一类型、同一工具和店铺。
