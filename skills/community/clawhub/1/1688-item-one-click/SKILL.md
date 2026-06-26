---
name: 1688-item-one-click
description: |
  1688 商品一键操作 —— 提供商品快速修改能力，支持一键修改标题、主图和发布会员号动态。
  工具能力：修改商品标题、修改商品主图、发布会员号动态，传入商品ID和新内容即可完成操作。
  触发词：修改标题、改标题、换标题、修改主图、换主图、一键修改、商品修改、发动态、会员号动态、私域营销、上新通知。
metadata: {"openclaw": {"emoji": "⚡", "requires": {"bins": ["python"]}}}
---

# 1688-item-one-click — 商品一键操作

## 技能概述

1688 商品一键操作助手。提供商品快速修改能力，支持一键修改商品标题、商品主图和发布会员号动态。采用两步操作流程：先调用 `before_check` 检查是否可执行（含协议签署），用户确认后再调用 `execute` 执行修改。

## 使用场景

- 商品标题确认后需要一键应用修改
- 商品主图优化后需要一键替换
- 商品需要私域营销、上新通知时发布会员号动态
- 批量修改商品标题或主图
- 配合 1688-item-title-optimizer（标题优化）或 1688-item-image-optimizer（图片优化）的结果，直接应用修改

## 支持的操作类型

| 操作 | spi_code | spi_params | 说明 |
|------|----------|------------|------|
| 修改标题 | `spi_hsf_automatic_title` | `{"newTitle": "新标题"}` | 修改商品标题 |
| 修改主图 | `spi_hsf_modify_main_img` | `{"newMainImg": "图片URL"}` | 修改商品主图 |
| 发布会员号动态 | `spi_hsf_offer_send_dynamics` | `{"title": "动态标题", "description": "动态内容"}` | 发布会员号动态，用于私域营销、商品上新通知。参数可选，未提供时使用 before_check 返回的推荐值 |

## CLI 命令

### configure — 配置 AK

```bash
# 查看 AK 状态
python {baseDir}/cli.py configure

# 设置 AK
python {baseDir}/cli.py configure YOUR_AK
```

配置网关鉴权所需的 AK。所有操作命令都依赖 AK，首次使用前需先配置。

### before_check — 执行前检查

```bash
# 检查修改标题
python {baseDir}/cli.py before_check --item_id <商品ID> --spi_code spi_hsf_automatic_title --spi_params '{"newTitle": "新标题内容"}'

# 检查修改主图
python {baseDir}/cli.py before_check --item_id <商品ID> --spi_code spi_hsf_modify_main_img --spi_params '{"newMainImg": "图片URL"}'

# 检查发布会员号动态（参数可选，不传时使用推荐值）
python {baseDir}/cli.py before_check --item_id <商品ID> --spi_code spi_hsf_offer_send_dynamics --spi_params '{}'

# 检查发布会员号动态（用户指定内容）
python {baseDir}/cli.py before_check --item_id <商品ID> --spi_code spi_hsf_offer_send_dynamics --spi_params '{"title": "动态标题", "description": "动态内容"}'
```

执行操作前的前置检查，判断是否可以执行、是否有协议需要签署。**每次操作前必须先调用此命令**。

### execute — 执行操作

```bash
# 执行修改标题
python {baseDir}/cli.py execute --item_id <商品ID> --spi_code spi_hsf_automatic_title --spi_params '{"newTitle": "新标题内容"}'

# 执行修改主图
python {baseDir}/cli.py execute --item_id <商品ID> --spi_code spi_hsf_modify_main_img --spi_params '{"newMainImg": "图片URL"}'

# 执行设置限时折扣
python {baseDir}/cli.py execute --item_id <商品ID> --spi_code spi_hsf_offer_promotion_dszk --spi_params '{"discountRate": "9.5", "activityDay": "15"}'

# 执行发布会员号动态
python {baseDir}/cli.py execute --item_id <商品ID> --spi_code spi_hsf_offer_send_dynamics --spi_params '{"title": "动态标题", "description": "动态内容"}'
```

执行实际的修改操作。**必须在 `before_check` 通过且用户确认后才能调用**。

## ⚠️ 重要：Agent 使用规范

### 规则1：严格两步操作流程

每一个修改操作**必须**按以下流程执行，不可跳过任何步骤：

**Step 1 — 前置检查**（调用 `before_check`）

```bash
python {baseDir}/cli.py before_check --item_id <商品ID> --spi_code <操作码> --spi_params '<参数JSON>'
```

根据返回结果判断：

| 返回情况 | 判断依据 | Agent 行为 |
|---------|---------|----------|
| **可以执行** | `markdown` 含"让用户确认后可以执行" | 向用户展示修改内容，请求确认 |
| **需签署协议** | `markdown` 含"协议名称"和"协议链接" | 向用户展示协议信息及链接，请用户阅读并确认协议后继续 |
| **不可执行** | `markdown` 含"不可执行"或其他拒绝原因 | 向用户展示不可执行的原因，**终止流程，不调用 execute** |

**Step 2 — 用户确认**

- 如果 Step 1 返回"可以执行"：向用户展示待修改内容，等待用户确认
- 如果 Step 1 返回"需签署协议"：向用户展示协议名称和链接，等待用户确认已阅读协议

**Step 3 — 执行修改**（调用 `execute`）

仅当 Step 1 判断可执行/协议已确认 **且** 用户明确确认后，才调用：

```bash
python {baseDir}/cli.py execute --item_id <商品ID> --spi_code <操作码> --spi_params '<参数JSON>'
```

### 规则2：结果展示规范

**before_check 结果展示**：

```
🔍 执行前检查结果：

【商品ID】{item_id}
【操作类型】修改标题 / 修改主图 / 设置限时折扣 / 发布会员号动态
【检查结果】可以执行 / 需签署协议 / 不可执行
【详细信息】{具体说明}

是否确认执行？
```

**execute 成功展示**：

```
✅ 操作成功！

【商品ID】{item_id}
【操作类型】修改标题 / 修改主图 / 设置限时折扣 / 发布会员号动态
【执行结果】{成功信息}
```

**execute 失败展示**：

```
❌ 操作失败

【商品ID】{item_id}
【失败原因】{失败原因}
```

### 规则3：设置限时折扣完整示例

```
用户："给商品944549591224设置限时折扣，打9.5折，持续15天"

Step 1: Agent 调用 before_check
  → python cli.py before_check --item_id 944549591224 --spi_code spi_hsf_offer_promotion_dszk --spi_params '{"discountRate": "9.5", "activityDay": "15"}'

Step 2: 检查通过，Agent 向用户确认
  → "检查通过，即将为商品设置限时折扣：打9.5折，持续15天，是否确认？"

Step 3: 用户确认后，Agent 调用 execute
  → python cli.py execute --item_id 944549591224 --spi_code spi_hsf_offer_promotion_dszk --spi_params '{"discountRate": "9.5", "activityDay": "15"}'

Step 4: 展示结果
  → "✅ 限时折扣设置成功！折扣：9.5折，活动时长：15天"
```

### 规则4：发布会员号动态完整示例

```
用户："给商品944549591224发一条会员号动态"

Step 1: Agent 调用 before_check（用户未指定 title/description，传空对象获取推荐值）
  → python cli.py before_check --item_id 944549591224 --spi_code spi_hsf_offer_send_dynamics --spi_params '{}'

Step 2: before_check 返回推荐的 title 和 description，Agent 向用户展示推荐内容并确认
  → "检查通过，推荐动态标题：'xx商品上新'，推荐内容：'商品卖点描述...'，是否确认发布？"

Step 3: 用户确认后，Agent 使用推荐值调用 execute
  → python cli.py execute --item_id 944549591224 --spi_code spi_hsf_offer_send_dynamics --spi_params '{"title": "xx商品上新", "description": "商品卖点描述..."}'

Step 4: 展示结果
  → "✅ 会员号动态发布成功！"
```

**用户指定内容的场景**：

```
用户："给商品944549591224发一条动态，标题是'夏季新品上架'，内容是'清凉透气面料，限时优惠中'"

Step 1: Agent 调用 before_check
  → python cli.py before_check --item_id 944549591224 --spi_code spi_hsf_offer_send_dynamics --spi_params '{"title": "夏季新品上架", "description": "清凉透气面料，限时优惠中"}'

Step 2: 检查通过，Agent 向用户确认
  → "检查通过，即将发布动态：标题'夏季新品上架'，内容'清凉透气面料，限时优惠中'，是否确认？"

Step 3: 用户确认后，Agent 调用 execute
  → python cli.py execute --item_id 944549591224 --spi_code spi_hsf_offer_send_dynamics --spi_params '{"title": "夏季新品上架", "description": "清凉透气面料，限时优惠中"}'

Step 4: 展示结果
  → "✅ 会员号动态发布成功！标题：夏季新品上架"
```

### 规则5：与优化技能配合

当用户先使用标题优化或图片优化技能后，要求应用优化结果时：

1. 从优化结果中提取新标题/新图片 URL
2. 调用 `before_check` 检查是否可执行
3. 根据检查结果向用户确认
4. 用户确认后调用 `execute` 执行修改

### 规则6：修改标题完整示例

```
用户："把商品944549591224的标题改成'轻奢沙发岩板茶几客厅设计师款2025新款茶桌'"

Step 1: Agent 调用 before_check
  → python cli.py before_check --item_id 944549591224 --spi_code spi_hsf_automatic_title --spi_params '{"newTitle": "轻奢沙发岩板茶几客厅设计师款2025新款茶桌"}'

Step 2: 检查通过，Agent 向用户确认
  → "检查通过，即将修改标题为'轻奢沙发岩板茶几客厅设计师款2025新款茶桌'，是否确认？"

Step 3: 用户确认后，Agent 调用 execute
  → python cli.py execute --item_id 944549591224 --spi_code spi_hsf_automatic_title --spi_params '{"newTitle": "轻奢沙发岩板茶几客厅设计师款2025新款茶桌"}'

Step 4: 展示结果
  → "✅ 标题修改成功！新标题：轻奢沙发岩板茶几客厅设计师款2025新款茶桌"
```

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|----------|
| 只读 | configure | 可直接执行，无需确认 |
| 只读 | before_check | 可直接执行，无需确认 |
| **写入** | execute | **必须** before_check 通过且用户确认后才能执行 |

**全局写入规则（适用于所有写操作）**：
1. 修改标题、主图、设置限时折扣和发布会员号动态属于写入操作，会直接变更商品数据。
2. **必须先调用 before_check**，不可跳过前置检查。
3. 当信息缺失时，先向用户追问补齐后再执行。
4. 不擅自修改用户提供的标题、图片 URL、折扣参数或动态内容。
5. 如果 before_check 返回需要签署协议，必须展示协议信息并等待用户确认。
6. 如果 before_check 返回不可执行，**禁止**调用 execute，直接终止并告知用户原因。

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" 或 "签名无效" 或 "401" | 提示用户当前操作能力所需鉴权未就绪，请补充有效 AK 或检查鉴权配置后重试 |
| "参数缺失" 或 "item_id 不能为空" | 提示用户补充缺失参数后重试 |
| "不可执行" | 向用户展示不可执行的具体原因，终止流程 |
| "限流" 或 "429" | 建议用户等待 1-2 分钟后重试 |
| 其他 | 仅输出 markdown 即可 |

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。发布到不同环境时可直接替换该文件中的变量值。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_NAME` | `1688-item-one-click` | skill 名称 |
| `SKILL_VERSION` | `1.0.0` | skill 版本号 |
| `SKILL_CHANNEL` | `clawhub` | 发布渠道 |

> 已存在的系统环境变量优先级高于 `.env`，CI/CD 注入的变量不会被覆盖。

## 埋点上报

每次 CLI 命令执行时，自动向 skill 网关上报一次调用记录，用于统计 skill 调用次数。

- **实现位置**：`scripts/_tracker.py` → `report_skill_usage()`，在 `cli.py` 的 `main()` 中每次命令执行后自动调用
- **上报接口**：`POST /api/reportSkillsUsage/1.0.0`
- **上报参数**：

  | 参数 | 值来源 | 说明 |
  |------|--------|------|
  | `apiName` | 固定 `null` | 固定传 null |
  | `skillsName` | `.env` `SKILL_NAME` | skill 名称 |
  | `version` | `.env` `SKILL_VERSION` | skill 版本号 |
  | `scene` | 固定 `CLI` | 固定值 |
  | `channel` | `.env` `SKILL_CHANNEL` | 发布渠道 |

- **失败处理**：上报失败静默忽略，不影响主流程

## 输出格式

采用标准 JSON 输出：

### before_check 输出

**可以执行**：
```json
{
  "success": true,
  "markdown": "✅ 检查通过，让用户确认后可以执行",
  "data": {
    "__msgInfo__": "让用户确认后可以执行",
    "__success__": true
  }
}
```

**需签署协议**：
```json
{
  "success": true,
  "markdown": "📋 需要签署协议\n\n协议名称：《XX协议》，协议链接：https://terms.alicdn.com/...\n\n让用户确认协议后可以继续执行",
  "data": {
    "data": "协议名称：《XX协议》，协议链接：https://terms.alicdn.com/...",
    "success": true,
    "message": "让用户确认协议后可以继续执行"
  }
}
```

**不可执行**：
```json
{
  "success": false,
  "markdown": "❌ 不可执行，最近已经操作过",
  "data": {
    "__msgInfo__": "不可执行，最近已经操作过",
    "__success__": true
  }
}
```

### execute 输出

**执行成功**：
```json
{
  "success": true,
  "markdown": "✅ 执行成功，成功信息是：标题一键优化成功",
  "data": {
    "__msgInfo__": "执行成功，成功信息是：标题一键优化成功",
    "data": "沙发岩板茶几客厅设计师款2025新款茶桌",
    "__success__": true
  }
}
```

**执行失败**：
```json
{
  "success": false,
  "markdown": "❌ 执行失败，原因是：新标题和原标题一致",
  "data": {
    "__msgInfo__": "执行失败，原因是：新标题和原标题一致",
    "__success__": false
  }
}
```

## 执行前置（首次命中能力时必须）

- 首次执行 `configure` 前：先完整阅读 `capabilities/configure.md`
- 首次执行 `before_check` 前：先完整阅读 `capabilities/before_check.md`
- 首次执行 `execute` 前：先完整阅读 `capabilities/execute.md`

## Agent 执行检查清单

在执行修改时，请确认：

- [ ] 已提取商品ID
- [ ] 已提取新标题/新图片URL/折扣参数/动态内容（或使用推荐值）
- [ ] 已确定正确的 spi_code 和 spi_params
- [ ] 已调用 `before_check` 完成前置检查
- [ ] 检查结果为"可执行"或"协议已确认"
- [ ] 已向用户展示变更内容/协议信息并获得确认
- [ ] 调用 `execute` 执行修改
- [ ] 使用标准模板展示操作结果
