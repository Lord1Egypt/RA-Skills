# 商品资料与文件约定

创建商品目录、恢复任务或写入新产物时读取。所有路径相对于宿主允许写入的本轮工作目录；不要使用固定示例路径替代真实文件。

## 目录与身份

本轮目录用不重复的短标识，每件商品使用稳定 `productId`，例如 `p001`。目录名可带简称；改名不改变身份。同名商品按货号、批次、用户归组区分；货号、SKU ID、参考商品 ID 均按字符串保留前导零。

```text
本轮目录/
  执行计划.md
  p001-商品简称/
    image/
      主图/白底主图/img-001.jpg
      标签图/水洗唛/img-002.jpg
      规格图表/img-003.png
      详情图/细节说明图/img-004.jpg
    text/
      source.json
      manifest.json
      facts.json
      category.json
      category-schema.json
      sku-input.json
      selection.json
      title.json
      catProp.json
      skuTable.json
      imageList.json
      detail.json
      tasks/title/…
      evidence/…
      draft/request.json
      draft/response.json
    说明.md
```

按需创建文件和子目录。原始 Office/PDF 附件可以保存在 `text/source/`；提取结果均写成 JSON。不要创建填有示例数据的空壳产物，也不要仅写出路径就声称文件已落地。

## 字段文件

可直接供草稿使用的五项文件，内部使用真实接口字段，元数据不混进业务值：

| 文件 | JSON 形态 | 写入时机 |
|---|---|---|
| `category.json` | `{"categoryId": 实际数字ID, "catNamePath": "实际路径"}` | 类目已采用 |
| `category-schema.json` | `{"catPropSchema": [...], "salePropNames": [...], "requiredSalePropNames": [...]}` | 真实 schema 回执解析后，推荐与必填分开保留 |
| `sku-input.json` | `{"skuTable": [...]}` | 第二层采用的可售组合、价格、库存 |
| `title.json` | `{"title": "实际标题"}` | 标题工具成功返回后原样保存 |
| `catProp.json` | `{"catProp": [...]}` | CPV 工具成功返回后原样保存 |
| `skuTable.json` | `{"skuTable": [...]}` | SKU 工具成功返回后原样保存 |
| `imageList.json` | `{"imageList": ["实际图片银行URL", ...]}` | 发布图序确定且转换完成 |
| `detail.json` | `{"detail": "实际详情HTML"}` | 现有图片组装完成 |

未齐全的输入信息用 `null` 和缺失原因表示，不补假值。`sku-input.json` 是已核对/按授权采用的输入，价格库存可缺省或为 null，无必填规格可为空行表。`skuTable.json` 是采用的工具输出；两者各自保留，不强制逐行一致，不反向覆盖原输入。三个素材工具默认原样写入上表产物，仅 [生产规则](03-00-production.md) 的明显冲突例外允许局部修正；原始回执不变，修正依据存台账，最终请求直接组装字段文件，不另维护一套发布值。

## 来源与台账

`source.json` 保存输入记录数组，每条至少有 `sourceId`、`kind`、`locator`、`content`、`productScope`。`locator` 可为消息轮次、文件/工作表/行列、PDF 页码、图片编号或网页 URL；内容保留原话与原始值。补充记录追加，不覆盖原记录。网页和参考款标为 `reference`，用户新品资料标为 `target`。

`facts.json` 记录当前整理结论：字段、值、来源 ID、适用商品/SKU、单位、时间、状态。状态区分 `observed`（提取到）、`candidate`（预测）、`adopted`（已采用）、`conflict`、`missing`。来源冲突不能按文件顺序或“最新一条”机械覆盖；按用户明确修正和适用范围处理。

`manifest.json` 是身份、素材和执行状态的机器索引。至少包含：

- `productId`、目标（整理/预览/保存草稿）、当前状态、是否在本次发布范围内；`store` 记录入口已确定的真实授权店铺及绑定依据，不记录凭证。
- `assets`：每张图的稳定 `assetId`、来源列表、本地路径、SHA-256、实际格式/尺寸、分类及多角色、用户顺序、是否选用、宿主 CDN URL/asset-id、图片银行 URL、入库回执位置、派生父图。不存在的 URL 用 `null`。
- `decisions`：类目、SKU、商品归组的采用方式、证据来源、采用值所在文件。类目保留接口原始候选顺序、采用的第一项有效候选及回执来源，不记成用户确认；SKU 记录必填缺口、有效澄清轮次、可选项跳过、AI 补充授权及推定依据。沉默/取消不能记成跳过或委托。
- `artifacts`：字段文件路径、状态（候选/有效/失效/阻塞）、内容校验值、所依赖文件及其校验值、验收理由。文件变化后重新比较依赖；未变化且依赖仍一致的产物可以复用。
- `tasks`：每个生成类型的工具名、真实 `taskId`、绑定店铺、任务状态、请求与回执路径；`draft`：待保存/结果待核实/已保存、真实 ID 和是否已交付。任务以商品、类型和本次输入快照共同定位，不跨商品或跨工具借用 ID。
- `blockers`：具体缺失字段、冲突、不可访问素材及下一步。业务终止另在 `stopReason` 记录 `CATEGORY_EMPTY`、`INDUSTRY_CATEGORY_NOT_SUPPORTED` 或 `DRAFT_CAPACITY_FULL`，关联回执与店铺；不因“继续”自动清除。恢复条件见 [00-02](00-02-recovery.md)。

`selection.json` 存放按顺序选中的图片编号：`main`、`detail`、`sku` 及各生成类型需要的证据图。编号指向 `manifest.json.assets`；URL 随转换更新，不用位置猜对应关系。

供本地组装脚本核验的图片字段名固定为 `assets[].assetId`、`localPath`，以及入库后填写的 `bank` 对象：`url`（图片银行 URL）、`file`（本次实际入库文件的包内相对路径）、`sha256`（该文件的实际校验值）、`receipt`（对应入库回执的包内相对路径）。未入库时 `bank` 为 `null`。若入库使用压缩副本，`bank.file` 指向副本，`localPath` 仍指向原图；外转内使用宿主转码图时，保留与所转 URL 对应的本地副本并准确注明。回执与内容对应关系还须人工/Agent 核对，脚本只能检查文件和校验值。

## 说明.md 必须同步

每次补充、移动图片、改分类、转图片银行、生成成功/失败或保存草稿后，从上述记录更新说明：

1. 商品身份、目标、当前状态与下一步。
2. 已采用事实、候选和缺口，以及用户确认/委托的原话来源。
3. 图片对应表：图片编号、本地文件、原始来源 URL、宿主 CDN URL、图片银行 URL、角色、发布顺序、转换状态。无 URL 如实写无/待转换。
4. 字段文件与状态：标题、类目、CPV、SKU、主展示图、详情，写明来源及依赖。
5. 未完成问题、生成任务及草稿结果入口。

JSON 为机器索引，说明是可读摘要；两者不一致时核对真实文件和回执后修正，不能挑方便的一份继续。JSON 用 UTF-8；数字保留精度，金额计算使用十进制；不得手工改写 URL 字符。

## 更新与保留

图片移动保留编号和校验值，原始与派生文件分别编号；同图多来源保留全部来源，不误算多张素材。原文件不被压缩/生成结果覆盖。字段变更前保留已采用值、依据和相关请求快照；只把受影响的产物标为失效。商品已保存时，后续补充不能自动触发第二次保存，按 [恢复规则](00-02-recovery.md) 处理。
