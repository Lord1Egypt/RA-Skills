---
name: sjzl-ai-okc
description: >
  商机助理（一键上货）。当用户有以下任何需求时，**必须**使用此技能：
  - 提到"商机助理"且包含"上货"、"复制"、"发布"关键词时，进行商品一键上货
  - 一键上货到商机助理平台
  - 查看的商机助理账号
  - 保存或修改商机助理授权
  自动识别用户输入中的商品链接，调用商品链接识别MCP接口进行处理。
  如果用户输入中没有链接，则提示用户提供链接。
---

# 商机助理一键上货

识别用户输入中的商品链接，调用 MCP 工具进行一键上货。

## MCP 服务配置

本技能依赖以下 MCP 服务，运行时**必须**先读取 `skill-config.json` 获取鉴权 Token：

| 配置项 | 说明 |
|--------|------|
| 鉴权方式 | HTTP Header 携带 `sToken`，值取自 `skill-config.json` 的 `sToken` 字段 |

### 配置读取方式

**约束：调用方 agent 必须在执行任何 MCP 调用前，先读取 skill-config.json 文件获取 sToken**

若 `sToken` 为空（空字符串或字段不存在），则**停止后续流程**，**仅输出以下两行内容**给用户：**不要输出 `---` 分隔符**，**不要添加任何额外的解释、叙述或前言文字**（包括"授权 Token 为空"等说明），**不要输出多余空行或分割线**：

您尚未授权，请前往 [商机助理](https://sjzl.fjdaze.com/v2/#/) 复制授权。

MEDIA:<SKILL目录>/images/auth.png

> **⚠️ 图片路径自动解析**：在输出授权提示前，agent 需读取本 SKILL.md 文件的实际路径，提取其父目录（即技能目录），然后拼接 `images/auth.png` 得到**绝对路径**，并将该绝对路径用于下方的 `MEDIA:` 标签。例如若 SKILL.md 位于 `C:\Users\Administrator\.openclaw\workspace\skills\sjzl-ai-okc\SKILL.md`，则 `MEDIA:` 应使用 `C:\Users\Administrator\.openclaw\workspace\skills\sjzl-ai-okc\images\auth.png`。

**等待用户输入授权 Token**，用户输入后进入 sToken 保存流程。

---

### sToken 保存流程

当满足以下任一条件时，触发 sToken 保存流程：

- 用户在授权提示后直接输入了 Token
- 用户输入中包含关键词**「保存授权」**或**「修改授权」**，并提供了 Token

#### sToken 格式校验

| 规则 | 说明 |
|------|------|
| 前缀 | 必须以 `st` 开头 |
| 后续字符 | `st` 后跟恰好 32 位字母数字字符（a-z、A-Z、0-9） |
| 总长度 | 34 位 |
| 正则校验 | `^st[a-zA-Z0-9]{32}$` |

示例：`st66666666666666666666666666666666`

#### 处理步骤

1. 从用户输入中提取符合正则 `^st[a-zA-Z0-9]{32}$` 格式的字符串
2. 校验结果处理：

| 情况 | 处理方式 |
|------|----------|
| 格式正确 | 将 `skill-config.json` 的 `sToken` 字段更新为提取到的值，提示用户："授权成功！" |
| 未提取到符合格式的 Token | 提示用户："授权 Token 格式不正确，请重新输入（格式：st + 32 位字母数字字符）" |

> 写入 `skill-config.json` 时，仅更新 `sToken` 字段，其他字段（如 `mcpServerUrl`）保持不变。

---

### 跨平台调用说明

**⚠️ 重要：call_mcp.py 脚本的 Python 路径**

在 Windows 系统上，`python3` 命令可能不存在。请使用以下方式之一执行脚本：

```bash
# 方式 1：使用 python（Windows 推荐）
python scripts/call_mcp.py ...

# 方式 2：使用完整路径（如果 python 也不在 PATH 中）
C:\ProgramData\anaconda3\python.exe scripts/call_mcp.py ...

# 方式 3：在 exec 中先 cd 再用 & 符号调用（PowerShell）
Set-Location "技能目录" ; & "python" scripts/call_mcp.py ...
```

**⚠️ 重要：PowerShell 下 JSON 参数传递问题**

PowerShell 对引号和花括号有特殊处理，导致 `--params` 传入的 JSON 字符串被破坏。**在 PowerShell 环境下，必须使用以下方式传递 JSON 参数**：

```bash
# ✅ 推荐方式 1：使用 --params-file 从文件读取参数
# 先将参数写入 JSON 文件，再通过 --params-file 指定
python scripts/call_mcp.py call get_copy_rule_config --params-file params.json

# ✅ 推荐方式 2：使用 --params @file.json 语法
python scripts/call_mcp.py call get_copy_rule_config --params @params.json

# ❌ 避免方式：直接在 PowerShell 中传递 JSON 字符串（引号会被破坏）
python scripts/call_mcp.py call get_copy_rule_config --params '{"rule":{...}}'  # 不可靠
```

参数文件的写入方式：agent 应先将 JSON 参数写入一个临时文件（如 `_mcp_params.json`），再通过 `--params-file` 或 `--params @文件路径` 引用。

**⚠️ 重要：MCP 接口参数格式**

所有 MCP 工具调用的参数必须通过 `--params` 传入，格式为 JSON 字符串。注意以下工具的参数结构：

- `get_copy_rule_config` 需要传入 `{"rule":{"mergeDefaultConfig":true,"copyConfigType":2}}`
- `save_copy_rule_config` 需要传入 `{"rule":{"copyConfigType":2,"copyWay":...,"status":...,"sendGoodsAddressId":...,"freightTemplateId":...,"productSingerPriceType":...}}`
- `copy_by_agent` 需要传入 `{"rule":{"copyConfigType":2,"copyProductInfos":[...]}}`
- `url_identify` 需要传入 `{"rule":{"productUrls":["..."]}}`
- `get_send_goods_addresses`、`get_skill_login_info` 无需参数
- `get_freight_templates` 需要传入 `{"rule":{"addressId":"<发货地址id>"}}`

---

## 触发条件

### 场景一：一键上货

用户输入文本**同时满足**以下两个条件时触发一键上货流程：

1. 包含关键词之一：`复制`、`上货`、`发布`
2. 包含关键词：`商机助理`

**示例触发语句**：
- "用商机助理上货这个链接"
- "商机助理复制这些商品"
- "用商机助理发布一下"

### 场景二：查看商机助理账号

用户输入文本包含关键词**「查看商机助理账号」**时，触发查看登录信息流程。

### 场景三：授权 / 修改授权

用户输入文本满足以下**任一**条件时，触发「sToken 保存流程」：

1. 包含关键词：`修改授权`
2. 包含关键词：`修改账号`

---

## 工作流程

### 场景：查看商机助理账号

将参数写入临时文件（如 `_mcp_params.json`），然后调用 MCP 工具 `get_skill_login_info`（无需参数）：

```bash
python scripts/call_mcp.py call get_skill_login_info
```

#### MCP 接口返回结果格式

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "userId": "",
    "userName": ""
  }
}
```

| 情况 | 处理方式 |
|------|----------|
| `code == 200` | 展示：`商机助理账号：<result.userName>` |
| `code != 200` | 将 `msg` 作为错误信息提示用户，**终止流程** |

---

### 第一步：识别用户输入中的链接

收到用户消息后：

1. 使用正则表达式从用户输入文本中提取所有 URL 链接
2. 判断是否提取到链接：

| 情况 | 处理方式 |
|------|----------|
| 提取到一个或多个链接 | 进入第二步，调用 MCP 接口 |
| 未提取到任何链接 | 提示用户："请提供需要上货的商品链接，支持同时输入多个链接。" |

**链接匹配规则**：匹配 `http://` 或 `https://` 开头的完整 URL。

### 第二步：调用商品链接识别 MCP 接口

将参数写入临时文件 `_mcp_params.json`：
```json
{"rule":{"productUrls":["<URL1>","<URL2>"]}}
```

然后调用 MCP 工具 `url_identify`：

```bash
python scripts/call_mcp.py call url_identify --params-file _mcp_params.json
```

#### MCP 接口返回结果格式

```json
{
  "Code": 200,
  "Msg": "",
  "Result": {
    "SuccessProductInfos": [
      {
        "Url": "",
        "ProductId": "",
        "OfferSource": 0,
        "CopyProductParam": null
      }
    ],
    "FailProductUrls": [
      ""
    ]
  }
}
```

#### 接口调用状态判断

首先根据返回的 `Code` 字段判断接口是否调用成功：

| 情况 | 处理方式 |
|------|----------|
| `Code == 200` | 调用成功，进入下方「结果展示与分支处理」 |
| `Code != 200` | 调用失败，直接将 `Msg` 字段作为错误信息提示用户，**终止流程** |

#### 结果展示与分支处理

解析 `Result` 后，按以下规则展示并决定后续流程：

1. 提取 `Result.SuccessProductInfos[*].Url` 作为**正确链接**列表
2. 提取 `Result.FailProductUrls` 作为**错误链接**列表
3. 按以下格式展示给用户（任一列表为空时仍需展示对应标题，下方留空或注明无）：

```
正确链接：
<SuccessProductInfos[0].Url>
<SuccessProductInfos[1].Url>
...

错误链接：
<FailProductUrls[0]>
<FailProductUrls[1]>
...
```

4. 分支判断：

| 情况 | 处理方式 |
|------|----------|
| `SuccessProductInfos` 为空（无任何成功链接） | 在展示结果后，提示用户："未识别到有效的商品链接，请重新输入正确的商品链接。"。**等待用户重新输入后，从「第一步：识别用户输入中的链接」开始重新执行整个流程** |
| `SuccessProductInfos` 不为空（存在至少一个成功链接） | 展示结果后，进入「第三步：获取上货设置」 |

### 第三步：获取上货设置

仅当第二步中 `SuccessProductInfos` 不为空时才执行本步。将参数写入临时文件 `_mcp_params.json`：
```json
{"rule":{"mergeDefaultConfig":true,"copyConfigType":2}}
```

然后调用 MCP 工具 `get_copy_rule_config`：

```bash
python scripts/call_mcp.py call get_copy_rule_config --params-file _mcp_params.json
```

#### MCP 接口返回结果格式

```json
{
    "code": 200,
    "msg": "",
    "result": {
        "产品类型": {
            "name": ""
        },
        "上架设置": {
            "name": ""
        },
        "发货地址": {
            "id": "",
            "name": ""
        },
        "运费设置": {
            "id": "",
            "name": "",
            "Type": ""
        },
        "价格类型": {
            "name": ""
        }
    }
}
```

> 各设置项均为对象格式，展示时仅展示 `name` 字段的值，`id` 和 `Type` 等字段用于内部逻辑判断。

#### 接口调用状态判断

| 情况 | 处理方式 |
|------|----------|
| `code == 200` | 调用成功，进入下方「设置展示与空值检测」 |
| `code != 200` | 调用失败，直接将 `msg` 字段作为错误信息提示用户，**终止流程** |

#### 设置展示与空值检测

`result` 包含 5 个固定设置项：`产品类型`、`上架设置`、`发货地址`、`运费设置`、`价格类型`，每项均为对象格式。

展示当前设置给用户（仅展示 `name` 字段）：

```
当前上货模板设置：
- 产品类型：<result.产品类型.name 或"未设置">
- 上架设置：<result.上架设置.name 或"未设置">
- 发货地址：<result.发货地址.name 或"未设置">
- 运费设置：<result.运费设置.name 或"未设置">
- 价格类型：<result.价格类型.name 或"未设置">
```

检测各项是否为空（对象的 `name` 字段为空字符串、`null` 或对象本身为 `null` / 不存在视为空值）：

| 情况 | 处理方式 |
|------|----------|
| 所有 5 项均不为空 | 展示设置后，向用户询问："以上为当前上货模板设置，是否使用以上设置进行一键上货？（是 / 否）"，等待用户确认。用户回复**「是」/「确认」/「确定」/「yes」**等肯定语义时，进入「第六步：执行一键上货」；用户回复**「否」/「取消」/「no」**等否定语义时，提示："已取消一键上货，您可前往 [商机助理](https://sjzl.fjdaze.com/) 修改上货模板设置后重试。"，**终止流程** |
| 存在至少一项为空 | 进入「第四步：补充空值设置」，逐项引导用户填写 |

---

### 第四步：补充空值设置

仅对 `result` 中**值为空**的设置项依次提示用户选择，顺序固定为：产品类型 → 上架设置 → 发货地址 → 运费设置 → 价格类型。

记录用户每一步的选择，等待用户**全部空值项**都填写完毕后，进入「第五步：保存上货设置」。

#### 产品类型（仅当值为空时提示）

提示用户选择：

```
请选择产品类型：
1. 发布为现货品
2. 发布为工厂品
```

| 选择 | 保存参数 |
|------|----------|
| 发布为现货品 | `copyWay = 0` |
| 发布为工厂品 | `copyWay = 1` |

#### 上架设置（仅当值为空时提示）

提示用户选择：

```
请选择上架设置：
1. 销售中
2. 草稿箱
3. 待上架
```

| 选择 | 保存参数 |
|------|----------|
| 销售中 | `status = 2` |
| 草稿箱 | `status = 13` |
| 待上架 | `status = 7` |

#### 发货地址（仅当值为空时提示）

调用 MCP 工具 `get_send_goods_addresses` 获取发货地址列表（无需参数）：

```bash
python scripts/call_mcp.py call get_send_goods_addresses
```

返回结果格式：

```json
{
    "code": 200,
    "msg": "",
    "result": [
        {
            "id": 0,
            "fullAddress": ""
        }
    ]
}
```

| 情况 | 处理方式 |
|------|----------|
| `code == 200` | 展示所有 `fullAddress` 供用户选择 |
| `code != 200` | 将 `msg` 作为错误信息提示用户，**终止流程** |

展示格式：

```
请选择发货地址：
1. <fullAddress[0]>
2. <fullAddress[1]>
...
```

保存参数：`sendGoodsAddressId` = 用户所选 `fullAddress` 对应的 `id`

> **⚠️ 发货地址变更与运费指导模板联动**：当用户变更了发货地址（即新选择的地址 `id` 与 `get_copy_rule_config` 返回的 `result.发货地址.id` 不同），且当前运费设置为指导模板类型（`result.运费设置.Type == "3"`），则提示用户："发货地址已变更，当前运费指导模板可能不再适用，请重新选择运费模板。"，然后重新进入运费设置流程（需使用新的发货地址 `id` 调用 `get_freight_templates`）。

#### 运费设置（仅当值为空时提示）

> ⚠️ **前置条件**：选择运费模板类选项前，必须已有发货地址（`result.发货地址.id` 不为空）。若发货地址 `id` 为空，提示用户："请先选择发货地址后再设置运费。"，跳过运费设置，等待用户完成发货地址选择后再回到运费设置。

将参数写入临时文件 `_mcp_params.json`：
```json
{"rule":{"addressId":"<发货地址id>"}}
```

然后调用 MCP 工具 `get_freight_templates`：

```bash
python scripts/call_mcp.py call get_freight_templates --params-file _mcp_params.json
```

返回结果格式：

```json
{
    "code": 200,
    "msg": "",
    "result": {
        "freightTemplates": [
            {
                "id": 0,
                "name": "",
                "type": ""
            }
        ],
        "isGuideFreightTemplates": true
    }
}
```

| 情况 | 处理方式 |
|------|----------|
| `code == 200` | 根据 `isGuideFreightTemplates` 决定运费设置选项（见下方） |
| `code != 200` | 将 `msg` 作为错误信息提示用户，**终止流程** |

根据 `result.isGuideFreightTemplates` 的值决定运费设置选项：

**当 `isGuideFreightTemplates == true` 时**，提示用户选择：

```
请选择运费设置：
1. 运费指导模板
2. 使用运费模板
3. 使用运费说明
4. 卖家承担运费
```

| 选择 | 处理方式 |
|------|----------|
| 运费指导模板 | 从 `freightTemplates` 中筛选 `type == "3"` 的数据展示供用户选择（见下方「运费模板选择流程」） |
| 使用运费模板 | 从 `freightTemplates` 中筛选 `type == "2"` 的数据展示供用户选择（见下方「运费模板选择流程」） |
| 使用运费说明 | `freightTemplateId = -1001` |
| 卖家承担运费 | `freightTemplateId = 1` |

**当 `isGuideFreightTemplates == false` 时**，提示用户选择：

```
请选择运费设置：
1. 使用运费模板
2. 使用运费说明
3. 卖家承担运费
```

| 选择 | 处理方式 |
|------|----------|
| 使用运费模板 | 从 `freightTemplates` 中筛选 `type == "2"` 的数据展示供用户选择（见下方「运费模板选择流程」） |
| 使用运费说明 | `freightTemplateId = -1001` |
| 卖家承担运费 | `freightTemplateId = 1` |

##### 运费模板选择流程

当用户选择「运费指导模板」或「使用运费模板」时，根据选择类型从 `freightTemplates` 中筛选对应 `type` 的数据：

| 用户选择 | 筛选条件 |
|----------|----------|
| 运费指导模板 | `freightTemplates` 中 `type == "3"` 的项 |
| 使用运费模板 | `freightTemplates` 中 `type == "2"` 的项 |

若筛选后无数据，提示用户："当前没有可用的运费模板，请选择其他运费设置方式。"，重新展示运费设置选项。

若筛选后有数据，展示格式：

```
请选择运费模板：
1. <筛选后freightTemplates[0].name>
2. <筛选后freightTemplates[1].name>
...
```

保存参数：`freightTemplateId` = 用户所选 `name` 对应的 `id`

> **记录用户选择的运费模板类型**：当用户选择「运费指导模板」时，标记当前运费设置为指导模板类型（`type == "3"`），用于后续发货地址变更时的判断。

#### 价格类型（仅当值为空时提示）

提示用户选择：

```
请选择价格类型：
1. 原价
2. 促销价
```

| 选择 | 保存参数 |
|------|----------|
| 原价 | `productSingerPriceType = 1` |
| 促销价 | `productSingerPriceType = 2` |

---

### 第五步：保存上货设置

等用户完成所有空值项的选择后，将参数写入临时文件 `_mcp_params.json`：
```json
{"rule":{"copyConfigType":2,"copyWay":0,"status":2,"sendGoodsAddressId":123,"freightTemplateId":456,"productSingerPriceType":1}}
```

然后调用 MCP 工具 `save_copy_rule_config`：

```bash
python scripts/call_mcp.py call save_copy_rule_config --params-file _mcp_params.json
```

| 参数 | 说明 | 传入条件 |
|------|------|----------|
| `copyConfigType` | 配置类型，固定值 `2` | 始终传入 |
| `copyWay` | 产品类型 | 用户在第四步选择了产品类型时传入 |
| `status` | 上架设置 | 用户在第四步选择了上架设置时传入 |
| `sendGoodsAddressId` | 发货地址 ID | 用户在第四步选择了发货地址时传入 |
| `freightTemplateId` | 运费模板 ID | 用户在第四步选择了运费设置时传入 |
| `productSingerPriceType` | 价格类型 | 用户在第四步选择了价格类型时传入 |

返回结果格式：

```json
{
    "code": 200,
    "msg": "",
    "result": null
}
```

| 情况 | 处理方式 |
|------|----------|
| `code == 200` | 保存成功，**重新执行「第三步：获取上货设置」** |
| `code != 200` | 保存失败，将 `msg` 作为错误信息提示用户，**终止流程** |

---

### 第六步：执行一键上货

仅当第三步中所有 5 项设置均不为空，且用户在第三步确认环节回复**「是」**之后才执行本步。将参数写入临时文件 `_mcp_params.json`：
```json
{"rule":{"copyConfigType":2,"copyProductInfos":[{"productId":"<ProductId>","offerSource":<OfferSource>,"copyProductParam":<CopyProductParam>}]}}
```

然后调用 MCP 工具 `copy_by_agent`：

```bash
python scripts/call_mcp.py call copy_by_agent --params-file _mcp_params.json
```

参数从第二步返回的 `Result.SuccessProductInfos` 中逐项取値，构建 `copyProductInfos` 数组：

| 参数 | 来源字段 |
|------|----------|
| `copyConfigType` | 配置类型，固定值 `2` |
| `productId` | `SuccessProductInfos[*].ProductId` |
| `offerSource` | `SuccessProductInfos[*].OfferSource` |
| `copyProductParam` | `SuccessProductInfos[*].CopyProductParam`（为 `null` 时传 `{}`） |

#### 接口返回结果格式

```json
{
    "code": 200,
    "msg": "",
    "result": ""
}
```

`result` 为任务 ID。

| 情况 | 处理方式 |
|------|-----------|
| `code == 200` | 调用 MCP 工具 `get_skill_login_info` 获取 `result.copyRecordUrl`，提示用户："一键上货任务已提交，可打开 [上货记录](copyRecordUrl) 进行查看进度"；若 `get_skill_login_info` 调用失败或 `copyRecordUrl` 为空，则仅提示："一键上货任务已提交。" |
| `code != 200` | 将 `msg` 作为错误信息提示用户，**终止流程** |

---

## 输出格式

### 未检测到链接时

```
未检测到商品链接，请提供上货的商品链接，支持同时输入多个链接。
```

### 检测到链接并调用成功时

```
## 商机助理一键上货

**识别到 X 个商品链接：**
1. <URL1>
2. <URL2>
...

**处理结果：**

正确链接：
<SuccessProductInfos[*].Url>

错误链接：
<FailProductUrls[*]>
```

### 全部链接识别失败时

```
错误链接：
<FailProductUrls[*]>

未识别到有效的商品链接，请重新输入正确的商品链接。
```

### 设置含空值时（第四步逐项提示示例）

```
当前上货模板设置：
- 产品类型：未设置
- 上架设置：销售中
- 发货地址：未设置
- 运费设置：未设置
- 价格类型：未设置

检测到以下设置项未设置，请依次完成填写：

请选择产品类型：
1. 发布为现货品
2. 发布为工厂品
```

### 一键上货任务下发成功时

```
一键上货任务已提交，可打开 [上货记录](copyRecordUrl) 进行查看进度
```

### 查看商机助理账号成功时

```
商机助理账号：<result.userName>
```

### MCP 接口调用失败时（`Code != 200` 或 `code != 200`）

```
<返回的 Msg / msg 内容>
```

---

## 注意事项

- 查看商机助理账号场景：用户输入包含「查看商机助理账号」时，调用 `get_skill_login_info` 获取登录信息，`code == 200` 时展示 `商机助理账号：userName`，否则展示 `msg` 错误信息
- 一键上货场景：必须同时满足两个关键词条件（包含"复制/上货/发布"且包含"商机助理"）才触发
- 授权场景：用户输入包含「保存授权」或「修改授权」时，触发 sToken 保存流程
- sToken 格式校验：必须符合正则 `^st[a-zA-Z0-9]{32}$`（st 开头 + 32 位字母数字），格式错误时提示用户重新输入
- 保存 sToken 时仅更新 `skill-config.json` 的 `sToken` 字段，其他字段保持不变
- 用户输入中可能包含多个链接，需全部提取
- 调用 MCP 接口前必须从 `skill-config.json` 读取 `sToken`
- 所有 MCP 接口均需先校验 `Code` / `code` 字段：等于 `200` 才继续后续流程，否则将 `Msg` / `msg` 作为错误信息提示用户并终止
- 仅当 `SuccessProductInfos` 中存在至少一个成功链接时，才进入第三步；否则提示用户重新输入，并在用户重新输入后**从第一步重新执行**
- `get_copy_rule_config` 返回的 `result` 为包含 5 个固定键的字典：`产品类型`、`上架设置`、`发货地址`、`运费设置`、`价格类型`，每项均为对象格式，展示时仅展示 `name` 字段
- `get_copy_rule_config` 返回的 `运费设置` 对象包含 `Type` 字段，`Type == "3"` 表示运费指导模板，`Type == "2"` 表示普通运费模板
- `get_copy_rule_config` 返回的 `发货地址` 对象包含 `id` 字段，用于调用 `get_freight_templates` 时传入 `addressId` 参数
- 空值检测后，仅对值为空的设置项依次提示用户选择，非空项保持原值不变
- `save_copy_rule_config` 参数为增量传入，仅传入用户实际选择的项；保存成功后重新执行第三步（获取上货设置）
- 第三步所有设置项均不为空时，必须向用户展示当前上货模板设置并询问"是否使用以上设置进行一键上货？（是 / 否）"，仅在用户回复"是"等肯定语义后才进入第六步执行一键上货；用户回复"否"等否定语义时，提示已取消并引导前往商机助理修改设置，终止流程
- `copy_by_agent` 的 `copyProductInfos` 数组由第二步 `SuccessProductInfos` 逐项映射，`CopyProductParam` 为 `null` 时传 `{}`
- 一键上货成功后（`code == 200`），调用 `get_skill_login_info` 获取 `result.copyRecordUrl`，展示提示"一键上货任务已提交，可打开 [上货记录](copyRecordUrl) 进行查看进度"；若获取失败或字段为空则仅提示"一键上货任务已提交。"；失败则展示 `msg` 错误信息
- 发货地址通过 `get_send_goods_addresses` 获取，展示 `fullAddress`，保存对应 `id`
- 选择「运费指导模板」或「使用运费模板」时需调用 `get_freight_templates`，根据 `isGuideFreightTemplates` 决定是否展示「运费指导模板」选项
- `get_freight_templates` 返回的 `freightTemplates` 中每项包含 `type` 字段：`type == "3"` 为运费指导模板，`type == "2"` 为普通运费模板；选择「运费指导模板」时仅展示 `type == "3"` 的数据，选择「使用运费模板」时仅展示 `type == "2"` 的数据
- 选择运费模板类选项前，发货地址 `id` 不能为空，否则提示用户先选择发货地址
- 选择「使用运费说明」时 `freightTemplateId = -1001`，「卖家承担运费」时 `freightTemplateId = 1`
- **发货地址变更联动**：当发货地址变更（新 `id` 与原 `id` 不同）且当前运费设置为指导模板类型（`result.运费设置.Type == "3"`）时，提示用户重新选择运费模板
