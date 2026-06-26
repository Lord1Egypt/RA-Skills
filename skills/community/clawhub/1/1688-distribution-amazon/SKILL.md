---
name: 1688-distribution-amazon
description: 将1688商品铺货到Amazon店铺并保存为店小宝待发布草稿的工具链。当用户提到「铺货Amazon」「上架Amazon」「Amazon发品」「把1688商品发到Amazon」「亚马逊铺货」「生成Amazon草稿」「直接发布到Amazon」等场景时必须使用此技能。当前版本只创建店小宝 Amazon 待发布草稿；即便用户要求直接发布，也应告知仅支持保存草稿并引导用户去店小宝完成后续发布。覆盖：环境检查、店铺确认、session 初始化、1688商品查询、Amazon类目映射、主图白底/裁剪/翻译、Amazon schema解析、CPV映射、店小宝Amazon payload构造、本地草稿保存。
metadata:
  version: 1.0.2
  category: official-1688
  created: 2026-05-20
  label: 1688铺货Amazon
  author: 1688-open-skills
  variables:
    - key: DXB_USER_ID
      desc: 店小宝用户 ID，用于查询已绑定 Amazon 店铺
      required: "true"
    - key: ALPHASHOP_ACCESS_KEY
      desc: 遨虾网关 AK，用于1688商品、类目和CPV映射接口
      required: "true"
    - key: ALPHASHOP_SECRET_KEY
      desc: 遨虾网关 SK，与 AK 配合生成 JWT
      required: "true"
    - key: ALI_1688_AK
      desc: 源舟网关 AK，用于图片白底、裁剪和翻译处理
      required: "true"
---

# 1688 -> Amazon 商品铺货

## 前置环境变量检查

收到任何 Amazon 铺货请求后，必须最先执行：

```bash
bash scripts/run_python.sh scripts/check_env.py
```

缺少任意环境变量时立即停止，把缺失项展示给用户，并要求用户在本机 shell 或仓库 `.env` 中设置；不要在聊天中粘贴 AK/SK/`ALI_1688_AK` 明文。用户补齐后重新执行 `check_env.py`，通过后才能继续。

所有脚本都必须用 `bash scripts/run_python.sh ...` 执行，不要使用外部包管理器包装命令。`run_python.sh` 会优先选择牛顿客户端内置 Python runtime，找不到时才回退系统 `python3`。

## 核心发布边界

- 当前版本唯一发布动作是 `localSave`，只保存为店小宝 Amazon 待发布草稿，返回 `localId`，不创建 Amazon 在线商品。
- 用户要求“直接发布”“直接上架”“立即上架”“正式发布”时，也必须走 `localSave` 草稿链路；不要询问库存数量，不要执行在线发布命令。
- 对这类直接发布请求，回复时明确说明：当前 skill 仅支持创建店小宝 Amazon 待发布草稿，草稿保存成功后请前往店小宝亚马逊商品管理页-待发布商品完成后续发布。
- 店小宝亚马逊商品管理页-待发布商品 URL：`https://page.1688.com/html/isv-bridge.html?version=0.0.26&appKey=5050627&role=buyer`
- 草稿 payload 默认写入库存 `1`；用户指定库存时必须写入用户指定的正整数，但不能因此执行在线发布。
- 任一步骤失败必须停止并展示错误，不要想象结果，不要跳步。
- 铺货执行期间只允许运行本文档列出的脚本命令；禁止读取、搜索、编辑或修复 skill 源代码。脚本失败时停止，向用户报告失败步骤、错误摘要和 session 目录。
- `encryptedCode` 是内部凭证，只能作为脚本内部参数和 session 文件使用，禁止在用户可见回复、表格、报告或日志摘要中展示原文。需要提及时写 `<DXB_ENCRYPTED_CODE>`。
- “保存本地草稿”必须调用店小宝 `releaseProductToOut`。不要把 `build_product.json` 复制成 `draft.json`，不要把本机 JSON 文件当作草稿成功。唯一验收文件是 `<session_dir>/release_product.json`，成功响应必须包含 `localId` 或 `isSuccess=1`。

## 推荐一键入口

用户已经提供 `offerId` 和 `storeName` 时，优先只执行这一条命令。即便用户要求直接发布，也执行本命令保存店小宝草稿：

```bash
bash scripts/run_python.sh scripts/run_local_save.py <offerId> --store-name "<storeName>" --marketplace-id ATVPDKIKX0DER
```

如果用户明确指定库存数量，必须使用一键入口的参数传入库存，禁止臆造 `INVENTORY=<n>` 这类未定义环境变量：

```bash
bash scripts/run_python.sh scripts/run_local_save.py <offerId> --store-name "<storeName>" --marketplace-id ATVPDKIKX0DER --inventory-quantity <n>
```

`run_local_save.py` 会内部完成环境检查、店铺校验、session 初始化、商品查询、类目映射、图片处理、Amazon schema、CPV 映射、payload 组装和 `releaseProductToOut type=localSave`。执行完成后，只根据脚本最后输出的 JSON 摘要回复用户。

成功回复必须包含：

- 已保存为店小宝 Amazon 待发布草稿。
- `localId`。
- 如果用户指定库存，只能根据脚本输出的 `inventoryQuantity` 回复实际写入草稿的库存值。
- 店铺、marketplace 和 session 目录。
- 引导用户前往店小宝亚马逊商品管理页-待发布商品，必须展示完整 URL 且包含 `https://`：`https://page.1688.com/html/isv-bridge.html?version=0.0.26&appKey=5050627&role=buyer`

如果一键入口失败，必须停止并展示失败步骤、错误摘要和 session 目录；不要继续手动补步骤，不要切到 Ozon/TikTok/其他平台，不要生成泛化运营建议。

## 信息收集

收到用户发品请求后，需要确认两件事：

| 信息 | 说明 | 必填 |
| --- | --- | --- |
| `offerId` | 1688 商品 ID | 是 |
| `storeName` | 目标 Amazon 店铺名称 | 是，必须先让用户确认 |

## Step1 查询 Amazon 店铺

```bash
bash scripts/run_python.sh scripts/query_user_info.py
```

向用户展示返回的 Amazon 店铺列表和 marketplace 信息，只展示 `storeName`，不要展示或复述 `encryptedCode`。

若没有 Amazon 店铺，停止流程并提示用户先完成店铺绑定。

## Step2 初始化 session

```bash
bash scripts/run_python.sh scripts/init_session.py <offerId> \
  --store-name "<storeName>" \
  --marketplace-id ATVPDKIKX0DER
```

`init_session.py` 会在内部根据 `storeName` 解析 `encryptedCode` 并写入 session 文件，不要把 `encryptedCode` 展示给用户。

脚本输出 session 目录，例如：

```text
/tmp/123456789-amazon-amazon-store-ATVPDKIKX0DER-20260520_120000000
```

后续所有步骤第一个参数统一传 `<session_dir>`。

## Step3 查询 1688 商品详情

```bash
bash scripts/run_python.sh scripts/query_offer.py <session_dir>
```

写入：

- `<session_dir>/query_offer.json`

## Step4 Amazon 类目映射

```bash
bash scripts/run_python.sh scripts/map_category.py <session_dir>
```

写入：

- `<session_dir>/map_category.json`

## Step5 图片处理

```bash
bash scripts/run_python.sh scripts/process_images.py <session_dir>
```

默认按 Amazon `productType` 执行图片 pipeline：

- `SCREEN_PROTECTOR`: `white_background,crop_4_3`
- `HANDBAG`: `white_background`
- `DRINKING_CUP`: `white_background`
- 其他类目：`white_background`

也可通过环境变量覆盖：

```bash
AMAZON_IMAGE_PIPELINE=white_background,crop_4_3,translate_to_en \
  bash scripts/run_python.sh scripts/process_images.py <session_dir>
```

写入：

- `<session_dir>/image_processing.json`

注意：该步骤不覆盖 `query_offer.json`。后续 `build_product.py` 会在内存中合并处理后的主图。

## Step6 查询并解析 Amazon 属性 schema

```bash
bash scripts/run_python.sh scripts/map_amazon_attrs.py <session_dir>
```

默认 `requiredMode=evaluated`，按当前 listing 上下文评估 Amazon 条件必填字段。

写入：

- `<session_dir>/map_amazon_attrs.json`

## Step7 CPV 映射

```bash
bash scripts/run_python.sh scripts/map_pv_attrs.py <session_dir>
```

该步骤必须带 `platform=amazon` 调用 CPV 映射接口。

写入：

- `<session_dir>/map_pv_attrs.json`

## Step8 组装 Amazon 发品 JSON

```bash
bash scripts/run_python.sh scripts/build_product.py <session_dir>
```

写入：

- `<session_dir>/build_product.json`

关键规则：

- 单 SKU no-SKU 商品使用 `baseInfo.parentSku` 承载唯一 seller SKU。
- 单 SKU no-SKU 的 `tradeInfo.skuAndPrice[0].skuCode` 必须置空。
- 库存默认值为 `1`，并同时写入 `tradeInfo.skuAndPrice[].inventory` 和 `fulfillment_availability.quantity`。
- 如果用户指定库存，使用 `run_local_save.py --inventory-quantity <n>` 或分步执行 `build_product.py <session_dir> --inventory-quantity <n>`；不要使用 `INVENTORY=<n>`。
- `image_processing.json` 中的处理后主图优先进入 `baseInfo.scImages`。

## Step9 保存店小宝 Amazon 待发布草稿

本步骤必须调用店小宝接口。优先使用 `release_product.py`，不要手动复制 JSON 文件作为替代结果。

默认执行：

```bash
bash scripts/run_python.sh scripts/release_product.py <session_dir>
```

等价于：

```bash
bash scripts/run_python.sh scripts/release_product.py <session_dir> --release-type localSave
```

写入：

- `<session_dir>/release_product.json`

成功点：店小宝返回成功响应和 `localId`。
失败时立即停止并报告错误，不要改成“保存本地文件”。

## 用户要求直接发布时的处理

不要执行在线发布。不要询问库存。不要调用未列入本文档的脚本。

处理方式：

1. 说明当前 skill 仅支持创建店小宝 Amazon 待发布草稿。
2. 继续执行 `run_local_save.py` 或默认分步 `localSave` 链路。
3. 草稿成功后返回 `localId`，并引导用户前往店小宝亚马逊商品管理页-待发布商品完成后续发布。

## 完整默认流程

```text
用户提供 offerId
  -> bash scripts/run_python.sh scripts/check_env.py
  -> bash scripts/run_python.sh scripts/query_user_info.py
     AI 展示 Amazon 店铺列表，等待用户确认 storeName；不要展示 encryptedCode
  -> bash scripts/run_python.sh scripts/init_session.py <offerId> --store-name "<storeName>"
  -> bash scripts/run_python.sh scripts/query_offer.py <session_dir>
  -> bash scripts/run_python.sh scripts/map_category.py <session_dir>
  -> bash scripts/run_python.sh scripts/process_images.py <session_dir>
  -> bash scripts/run_python.sh scripts/map_amazon_attrs.py <session_dir>
  -> bash scripts/run_python.sh scripts/map_pv_attrs.py <session_dir>
  -> bash scripts/run_python.sh scripts/build_product.py <session_dir>
  -> bash scripts/run_python.sh scripts/release_product.py <session_dir>
     默认 localSave，返回 localId 后完成
```

## 脚本索引

| 脚本 | 功能 |
| --- | --- |
| `scripts/check_env.py` | 检查 `DXB_USER_ID` / `ALPHASHOP_ACCESS_KEY` / `ALPHASHOP_SECRET_KEY` / `ALI_1688_AK` |
| `scripts/query_user_info.py` | 查询店小宝用户信息和 Amazon 店铺列表 |
| `scripts/init_session.py` | 创建 Amazon 铺货 session 目录 |
| `scripts/query_offer.py` | 查询并标准化 1688 商品详情 |
| `scripts/map_category.py` | 1688 类目映射到 Amazon 类目和 `productType` |
| `scripts/process_images.py` | Amazon 主图白底、裁剪、翻译处理 |
| `scripts/map_amazon_attrs.py` | 查询并解析 Amazon schema 必填属性 |
| `scripts/map_pv_attrs.py` | CPV 映射，固定 `platform=amazon` |
| `scripts/build_product.py` | 组装店小宝 Amazon 发品 JSON |
| `scripts/release_product.py` | 调用 `releaseProductToOut`，仅支持 `localSave` |
| `scripts/save_draft.py` | 兼容别名，内部等价调用 `release_product.py <session_dir> --release-type localSave`；优先使用 `release_product.py` |
| `scripts/run_local_save.py` | 推荐入口，一条命令完成默认本地草稿链路 |

## 参考文档

- `references/amazon-listing-chain.md`：Amazon 链路和接口字段说明
- `references/troubleshooting.md`：常见问题和处理方式
