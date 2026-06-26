---
name: forces-reanalyze-smart
version: 1.0.2
description: '完成智慧门店工单复盘全流程。触发词：工单复盘、复盘工单、拉取工单数据、创建复盘文档、工单分析、创建复盘。完整覆盖三个阶段：(1)拉取Furcas工单数据并导入多维表格 (2)创建/更新工单复盘总文档 (3)创建开发复盘文档并填充TOP5统计。当用户要求进行工单复盘时使用。'
---

# 智慧门店工单复盘全流程

## 流程概览

一次完整的工单复盘涉及 **3个文档**，按顺序执行：

```
Step 0：复盘跟踪表（前置检查）
  检查/创建 目标月份记录 → 落数据基线

阶段一：工单数据表（飞书多维表格）
  Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 5b
  解析月份 → 获取Cookie → 拉取Furcas数据 → 创建/复用月份bitable（模板：J4tawf06GijvEmkBTSCcdyNsnyd）→ 导入CSV → 更新mention-doc链接

阶段二：工单复盘总文档（知识库文档）
  Step 6 → Step 7
  创建文档（模板：GEqawooPYiDXLWkRKZHcJnLcnFc）→ 填充变量

阶段三：开发复盘文档（知识库文档）
  Step 8
  创建文档（模板：Secqwa7deiaRwTkUsG6cJ7xpnzj）→ 填充TOP5统计
```

## 关键链接

| 类型 | 链接/Token |
|------|-----------|
| 工单数据Bitable模板 | `J4tawf06GijvEmkBTSCcdyNsnyd` (table: `tblXtjn9QHTcB5oa`, view: `vew8A2EB9c`) |
| 复盘总文档模板 | `GEqawooPYiDXLWkRKZHcJnLcnFc` |
| 开发复盘文档模板 | `Secqwa7deiaRwTkUsG6cJ7xpnzj` |
| 复盘跟踪表（前置数据源） | `YMQjwQeWCipABCkl8y7ckZlunQe` (table: `tblpygt9n8dqZcsw`，参见 Step 0) |
| Bot App ID | `cli_a97b6a0ffc399cc0` |

---

# ⚙️ 环境要求与配置

## 运行时依赖

使用此 skill 需要以下运行时环境（OpenClaw 标准环境已预装 Node.js）：

| 依赖 | 用途 | 安装命令 |
|------|------|---------|
| Python 3 | 运行 fetch_furcas.py & generate_batches.py | 通常已预装 |
| requests (Python) | Furcas API 调用 | `pip3 install requests` |
| Node.js 18+ | 运行 import_to_bitable.mjs & fill_review_cells.cjs | 通常已预装 |

## 环境变量说明

> **这是此 skill 被其他人使用时最容易出错的部分。** 以下是所有脚本读取的环境变量：

### 必须设置的环境变量

| 环境变量 | 脚本 | 说明 |
|---------|------|------|
| `FURCAS_COOKIE` | `fetch_furcas.py` | Furcas 登录 Cookie。从 https://furcas.shouqianba.com 登录后 F12 → Network → 复制完整 Cookie 请求头 |
| `SENDER_OPEN_ID` | `fill_review_cells.cjs` | 当前用户的飞书 open_id（每人不同）。格式 `ou_xxxxxxxx`。可从飞书开发者后台获取 |

### 可选设置的环境变量

| 环境变量 | 脚本 | 默认值 | 说明 |
|---------|------|-------|------|
| `FEISHU_UAT_DIR` | `import_to_bitable.mjs`, `fill_review_cells.cjs` | `$XDG_DATA_HOME/openclaw-feishu-uat` | OAuth 加密令牌存储目录。标准部署无需修改，特殊部署需指定 |
| `APP_TOKEN` | `import_to_bitable.mjs` | （必填） | 工单数据多维表格的 app_token |
| `TABLE_ID` | `import_to_bitable.mjs` | （必填） | 工单数据表的 table_id |
| `CSV_PATH` | `import_to_bitable.mjs` | `/workspace/furcas.csv` | CSV 文件路径 |
| `BATCH_SIZE` | `import_to_bitable.mjs` | `15` | 每批导入条数 |
| `TABLE_NAME` | `import_to_bitable.mjs` | `工单数据` | 目标表名（用于校验） |
| `APP_ID` | `fill_review_cells.cjs` | `cli_a97b6a0ffc399cc0` | Bot App ID（团队共用，通常无需修改） |
| `DOC_ID` | `fill_review_cells.cjs` | （必填） | 要填充的复盘总文档 ID |
| `MONTH` | `fill_review_cells.cjs` | （必填） | 目标月份标签，如 `2026-05` |

## 首次使用前的准备

1. **安装 Python 依赖**：运行一次 `pip3 install requests`
2. **完成飞书 OAuth 授权**：执行 `clawhub install forces-reanalyze-smart` 后，按提示完成飞书授权
3. **获取 Furcas Cookie**：登录 Furcas 后拷贝 Cookie
4. **确认自己的 open_id**：在飞书开放平台获取或咨询管理员

---

# 前置步骤：复盘跟踪表

## Step 0: 检查/创建跟踪表记录

在创建任何文档之前，先检查复盘跟踪表是否已有目标月份的记录。

### 跟踪表链接

`https://sqb.feishu.cn/wiki/YMQjwQeWCipABCkl8y7ckZlunQe?table=tblpygt9n8dqZcsw&view=vewme7V2C9`

- Bitable App Token: `YMQjwQeWCipABCkl8y7ckZlunQe`
- Table ID: `tblpygt9n8dqZcsw`

### ⚠️ 核心规则：必须先查存在，绝不复件

> **这条规则是全局最高优先级。任何创建操作前必须先查，查到已存在则直接复用，绝不允许创建第二条同名记录。**

### 操作步骤

1. **查询已有记录（必须执行，不可跳过）**：

```
操作：feishu_bitable_app_table_record list
参数：
  app_token: "YMQjwQeWCipABCkl8y7ckZlunQe"
  table_id: "tblpygt9n8dqZcsw"
  filter: {
    conjunction: "and",
    conditions: [
      {field_name: "复盘范围", operator: "is", value: ["2026-05"]}
    ]
  }
```

> **注意 field_name 必须用中文名「复盘范围」（是文本类型的主字段），不要用 field_id。**

2. **判断是否已有目标月份**：
   - ✅ **找到记录** → **立即停止创建流程**，直接使用已有记录的 `record_id` 及其包含的所有数据（工单总数、复盘工单数、各分类统计等），进入阶段一
   - ❌ **没找到** → 执行第 3 步创建新记录

   > **绝对禁止**：查到已有记录后，再创建第二条同名或同周期的记录。

3. **新建记录**（仅在确认不存在时执行）：

```
操作：feishu_bitable_app_table_record create
参数：
  app_token: "YMQjwQeWCipABCkl8y7ckZlunQe"
  table_id: "tblpygt9n8dqZcsw"
  fields:
    复盘范围: "{月份标签}"     // 整月如 "2026-05"（不要加 "-整" 后缀）
    开始时间: {毫秒时间戳}     // 范围起始日期 00:00:00 UTC+8
    结束时间: {毫秒时间戳}     // 范围结束日期 23:59:59 UTC+8
    日期: {毫秒时间戳}         // 当前操作日期（执行复盘的当天）
```

### 字段说明

| 字段 | 类型 | 填写规则 |
|------|------|---------|
| `复盘范围` | 文本 (主字段) | 整月：`2026-05`（**不要写** `2026-05-整`）；上半月：`2026-05-上`；下半月：`2026-05-下` |
| `开始时间` | 日期（毫秒时间戳） | 范围起始日 `00:00:00 UTC+8`，如2026年5月整月 → `1777593600000`（对应 `2026-05-01T00:00:00+08:00`） |
| `结束时间` | 日期（毫秒时间戳） | 范围结束日 `23:59:59 UTC+8`，如2026年5月整月 → `1780271999000`（对应 `2026-05-31T23:59:59+08:00`） |
| `日期` | 日期（毫秒时间戳） | 当前操作日期，即执行复盘的当天，如2026年5月6日 → `1777910400000`（`2026-05-06T00:00:00+08:00`） |

> ⏰ **时间戳必须二次确认**：创建记录后立即读取该记录，检查时间戳对应的年份是否与目标年份一致（2026年）。一个常见的错误是毫秒时间戳算成了2025年的日期。如果时间戳不对，删除该记录，重新计算并创建。

> **注意**：其余字段（工单总数、复盘工单、超时工单数、各解决类别统计等）均为 Lookup/Formula 自动计算字段，无需手动填写，数据导入后会自行更新。

### 创建后操作

- ✅ 确认记录已成功创建
- ✅ **读取刚创建的记录，验证时间戳是否对应正确的日期（2026年不是2025年）**
- 记录下 `record_id`，后续阶段二填充文档第三节表格时需要
- 进入阶段一，开始拉取工单数据

---

# 阶段一：工单数据表

## Step 1: 解析用户意图

用户说"做X月工单复盘"或"复盘X月"时：
- 提取目标月份（如 `2026-04`）
- 计算开始/结束日期：`2026-04-01` ~ `2026-04-30`
- 记录月份标签：`2026-04`

如果用户提到"拉取X到X的工单数据"，直接使用指定的起止日期。

## Step 2: 获取 Cookie

本阶段需要有效的 Furcas Cookie。

1. 如果已有可用的 `FURCAS_COOKIE` 环境变量，直接使用
2. 如果没有，引导用户：
   - 登录 `https://furcas.shouqianba.com`
   - F12 开发者工具 → Network → 复制完整的 Cookie 请求头
   - 设置环境变量：`export FURCAS_COOKIE="完整Cookie值"`

> ⚠️ **不要**将 Cookie 硬编码写入脚本文件。这是个人凭据，每个使用者必须用自己的 Cookie。
> 环境变量方式可在 session 级别临时设置，不会污染源代码，也便于他人使用。

## Step 3: 拉取工单数据

```bash
python scripts/fetch_furcas.py -s "2026-04-01" -n "2026-04-30" -o /workspace/furcas.csv
```

输出字段：问题描述、问题链接、工单状态\|修复情况、问题原因、责任人、解决类别、解决模块、超时时间、超时备注

## Step 4: 创建/复用月份工单数据 Bitable

⚠️ **必须检查**：先确认目标月份目录下是否已有同名 bitable。用 `feishu_wiki_space_node list` 列出目录内容，看是否已有工单数据表。如有则直接复用，跳过创建。

### 正确创建方式（仅需一步）

使用 `feishu_wiki_space_node copy` 将模板节点直接复制到目标月份目录：

```
操作：feishu_wiki_space_node copy
参数：
  node_token: "J4tawf06GijvEmkBTSCcdyNynsd"  // 工单数据表模板
  space_id: "7510046829784662017"
  target_parent_token: "{目标月份目录节点token}"
  target_space_id: "7510046829784662017"
```

**为什么必须用 wiki node copy？**
- ❌ `feishu_bitable_app copy` → 创建独立 bitable（不在 wiki 目录中）
- ❌ `feishu_wiki_space_node create` → 创建空白 bitable（表名 "Table"，字段全英文）
- ✅ `feishu_wiki_space_node copy` → 直接在 wiki 内创建模板副本，字段/视图全部正确

### 复制后的处理

1. **重命名**：bitable 名称 → `智慧门店-2026-5月工单数据`
2. **删除模板空记录**：模板自带 5 条空记录（`fields: {}`），用 `batch_delete` 清空
3. **验证字段结构**：应包含以下 9 个字段：
   - `文本`（Text, primary）、`问题链接`（Url）、`工单状态|修复情况`（Text）、`问题原因`（Text）
   - `责任人`（Text）、`解决类别`（SingleSelect）、`解决模块`（SingleSelect）
   - `超时时间`（Text）、`超时备注`（Text）

**关键约束**：
- `工单状态|修复情况` 含竖线 `|`（CSV中为 `/`，脚本会自动映射）
- `问题链接` 是 URL 类型，导入时用 `{"link": "URL", "text": "查看工单"}`
- `责任人` 是文本类型（type=1），不是人员类型

## Step 5: 导入数据到多维表格

**推荐：使用导入脚本**

```bash
APP_TOKEN={月份bitable的app_token} \
TABLE_ID={月份bitable的table_id} \
CSV_PATH=/workspace/furcas.csv \
BATCH_SIZE=15 \
node scripts/import_to_bitable.mjs --name "数据表"
```

> ⚠️ **`--name` 参数必须传**：模板复制出来的表名叫 `数据表`，但脚本默认校验名为 `工单数据`。必须用 `--name "数据表"` 或 `TABLE_NAME="数据表"` 让校验通过。不传的话校验会警告但不阻止导入。

脚本自动：校验表名 → 清空旧数据 → 分批创建记录 → 创建看板视图 → 验证条目数 → **校验超时备注** → **去重检查**。

> ⚠️ **`batch_delete` 参数名是 `record_ids`（不是 `records`）**：这是飞书 API 的规范。如果写错，清空静默失败，新数据追加到旧数据上，导致重复。

> ⚠️ **去重检查是最后一道防线**：即使清空步骤因意外失败（如网络超时、API 限流），去重步骤也会自动删除重复工单，保证每个工单 ID 唯一。

> ⚠️ **表名校验**：脚本在导入前会调用 API 读取目标表的实际名称，与 `TABLE_NAME` 环境变量比对。如果名称不匹配会给出警告，防止数据写入错误的表。

**手动替代方案**：使用 `feishu_bitable_app_table_record` 工具 `action=batch_create`，records 参数用 `string="false"`。

---

# 阶段二：工单复盘总文档

## Step 5b: 更新文档 Mention-Doc 链接

导入数据后，立即更新复盘总文档中的 mention-doc 链接，确保指向当前月份的正确表格和开发复盘文档。

**为什么必须做：** 复盘总文档从模板复制后，mention-doc 链接指向的是模板的占位对象（如旧月份的表格或模板文档）。不更新的话，点击链接会看到错误的数据。

### 更新步骤

1. **获取复盘总文档的文档 ID**（从 step 6/7 创建或之前创建的文档获取）
2. **找到 mention-doc 所在的 block**：
   - 遍历文档根级 children，找到包含「月具体工单请查看飞书表格」文本的 block
   - 该 block 是 type=2（text），其 elements[] 中包含 mention_doc 类型的 element
3. **PATCH 更新该 block 的 elements**：
   - `工单数据表 mention-doc`：token → 当前月份的 bitable token，obj_type → 8（bitable）
   - `开发复盘文档 mention-doc`：token → 当前月份的 wiki 节点 token，obj_type → 16（wiki）
   - **不写 text_run 的 content**（显示文本由文档标题决定）
   - **obj_type 必须传整数**（8=bitable, 16=wiki），传字符串会报 `99992402`

### 脚本参考

```javascript
// PATCH /docx/v1/documents/{docId}/blocks/{blockId}
// Body: { update_text_elements: { elements: [originalElements] } }
// 只改 mention_doc.token/obj_type/url，保持 text_run 不变
```

### 第 34 个经验（2026-05-07）：Mention-doc 更新后 token 被自动解析

发送 wiki 节点 token 后，飞书 API 会自动解析为实际文档的 obj_token，类型也会从 wiki(16) 变为具体类型（如 docx=22, bitable=8）。修改后 fetch-doc 验证即可。

## Step 6: 创建工单复盘总文档

### 前置检查

**在创建之前，先检查目标月度目录下是否已存在同名的文档。**

使用 `feishu_wiki_space_node list` 列出月度目录下的所有节点。如果已有同名文档，直接进入 Step 7 更新即可，**不要重复创建**。

### 创建步骤

1. **复制模板**：从模板 `GEqawooPYiDXLWkRKZHcJnLcnFc` 复制创建新文档
2. **重命名**：按月份命名，如 `智慧门店-2026-05月-工单复盘`
3. **放入对应目录**：确认文档在正确的年度/月度知识库目录下

复制文档的两种方式：
- 使用 `feishu_wiki_space_node` 的 `copy` 操作（如果模板是 wiki 节点），传入 `space_id` 和 `target_parent_token`
- 或用 `feishu_create_doc` 从模板创建（传入 wiki 节点 token）
- 或用 `feishu_drive_file` 的 `copy` 操作

## Step 7: 填充复盘总文档变量

模板中有大量 `x` 占位符（橙色高亮），需要按以下规则替换为实际数据。

### 模板结构要点（非常重要）

**不要破坏模板原有的换行和段落结构。** 模板中每个变量的位置和间距都有意义。以下从实际模板 `GEqawooPYiDXLWkRKZHcJnLcnFc` 获取的精确结构：

```
# 一、会议信息
会议主题：智慧门店-<text color="orange">2026-</text><text color="orange">10</text>月工单复盘
会议时间：<text color="orange">2026.05.07（周四） 16:00 - 16:30</text>

# 二、会议议程
**复盘时间：**<text color="orange">**2026.05.07**</text>
**复盘范围：**<text color="orange">**2026.04.01 00:00:00-2026.04.30 23:59:59**</text>
**参与人员：**
- **开发：朱栋泉、**<text color="orange">**李文茂(28)、付雷(12)、王佳明(10)、赵杭琪(9)**</text>
- **产品：**
- **测试：**
- **技术支持：崔文思**
- **运营：蒋达周**

# 三、工单总计<text color="orange">XX</text>个(按工单数统计)

[Table: 10行×11列，3个月数据（2026-02/03/04），每33格一组=110格]
⚠️ 2026-04 组（最近一个月）使用整体橙色格式，与 02/03 组的逐字橙色不同

<text color="orange">2026-04</text>月具体工单请查看飞书表格：<mention-doc token="J4tawf06GijvEmkBTSCcdyNynsd" type="wiki">2026-xx月-智慧门店工单数据</mention-doc>
开发复盘文档：<mention-doc token="Secqwa7deiaRwTkUsG6cJ7xpnzj" type="wiki">开发复盘文档模板</mention-doc>

# 四、工单总结
## 工单数量分析
- <text color="orange">2026-04</text>月共产生工单<text color="orange">646</text>个，本次复盘筛选出<text color="orange">154</text>个工单。同比<text color="orange">2026-03</text>月<text color="orange">增加25.19%</text>
- 从**解决类别**看，工单主要集中在：<text color="orange">外部原因-无需技术排查(208)、设计如此-无需优化(160)、外部原因-需技术排查(81)</text>
- 从**解决模块**看：工单主要集中在：<text color="orange">收银系统-餐饮(197)、打印机(150)、扫码点单(117)</text>

## 工单时效分析
<text color="orange">90</text>个超时工单（其中产研介入<text color="orange">59</text>个），时效内解决占比<text color="orange">84.67</text>%，较3月<text color="orange">82%</text>有所提高。
主要超时原因：

## 问题总结
立即更改内容跟进：
同步客服&技术支持：

# 五、历史跟进事项
<text color="orange">**2026-03**</text>**月跟进事项**：
...
<text color="orange">**2026-02**</text>**月跟进事项**：
...
```

#### 📌 模板关键位置标注
| 位置 | 说明 |
|------|------|
| Section 3 标题 | `# 三、工单总计<text color="orange">XX</text>个(按工单数统计)`，**无 callout 块** |
| Section 3 末尾 | **Mention-doc**（工单数据表 bitable + 开发复盘文档 wiki） |
| Section 4: 工单数量分析 | 含同比上月数据行 `<text color="orange">同比...增加xx%</text>` |
| Section 4: 工单时效分析 | `主要超时原因：`后为填空区域 |
| Section 5 | 月份为「目标月-1」和「目标月-2」，如05月复盘则显示04和03月 |
| 表格最后一组（最近月） | 使用整体橙色 `<text color="orange">已解决x（产研介x）</text>` 格式，与前面两组不同 |

#### 📌 Section 5 月份命名规则
- 表头显示「目标月-1」和「目标月-2」的跟进事项
- 例如：05月复盘 → 显示 `**2026-04**月跟进事项` 和 `**2026-03**月跟进事项`
- 月份部分用橙色标签包裹：`<text color="orange">**2026-03**</text>**月跟进事项**：`

---

### 🏷️ 命名规范（必须遵守）

创建文档时**禁止直接使用模板的名称**。每次创建必须按以下规范重命名：

| 文档类型 | 模板节点 | 创建后命名规范 | 示例（2026-05月） |
|---------|---------|--------------|------------------|
| 工单数据跟踪表（多维表格） | `J4tawf06GijvEmkBTSCcdyNynsd` | `智慧门店-2026-xx月-工单数据` | `智慧门店-2026-05月-工单数据` |
| 工单复盘文档（知识库文档） | `GEqawooPYiDXLWkRKZHcJnLcnFc` | `智慧门店-2026-xx月-工单复盘` | `智慧门店-2026-05月-工单复盘` |
| 开发复盘文档（知识库文档） | `Secqwa7deiaRwTkUsG6cJ7xpnzj` | `智慧门店-2026-xx月-开发复盘文档` | `智慧门店-2026-05月-开发复盘文档` |

**重命名方式**（API 不支持，必须手工）：
1. 复制模板创建文档后，在飞书页面打开
2. 右键左侧目录树中的节点 → 选择「重命名」
3. 按上表命名规范输入新名称
4. 标题改完后，mention-doc 的显示文字会自动更新（因为 mention 显示的是文档实际标题）

> ⚠️ Section 3 的表格是 `<lark-table>` 格式（带 rowspan/colspan 的复杂表格），**不能用 markdown 表格替代**。
> 使用 `overwrite` 模式重写文档时，表格结构会丢失。因此 Section 3 必须保留原始 `<lark-table>` 代码。

### ⚠️ ⚠️ ⚠️ 三大数据来源规则（必须遵守，不要再出错） ⚠️ ⚠️ ⚠️

> **以下3条规则已经被用户多次重复强调。每次出错都会导致文档数据混乱。阅读此文件时请逐条仔细核对！**

#### 规则1：参与人员 → 取开发复盘文档 TOP5

**复盘总文档**中 `# 二、会议议程` → `参与人员：` → `开发：` 后面的橙色部分，必须填入**开发复盘文档 Section 2 中前5名责任人** 的姓名和工单数量。

- 不要使用模板中的旧数据（如 `李文茂(28)、付雷(12)、王佳明(10)、赵杭琪(9)`）
- 不要自行编造
- 准确取本月的开发复盘文档中 Section 2 的5位开发人员及其工单数量
- 格式：`李文茂(5)、蒋达周(3)、赵杭琪(2)、金海轩(2)、王金楠(2)`

#### 规则2：工单总计 XX + 第三节表格 → 全部来自复盘跟踪表

**模板中所有带 `x` 的数字占位符**（包括 Section 3 标题 `XX`、表格中所有 `x`）的填充值，必须全部从 **复盘跟踪表** Bitable 获取：

```
复盘跟踪表: https://sqb.feishu.cn/wiki/YMQjwQeWCipABCkl8y7ckZlunQe?table=tblpygt9n8dqZcsw
```

- **Section 3 标题** `三、工单总计XX个` → X 填复盘跟踪表中当月记录的 `工单总数` 字段
- **表格数据** → 全部填复盘跟踪表中各月份的字段值
- **表格顺序**：必须按时间从上到下排列，**新数据在下方**。例如做 5 月复盘时：
  - 第一行（最上方）：2026-03（最旧）
  - 第二行（中间）：2026-04
  - 第三行（最下方）：2026-05（最新）
  - **不要**把最新行放在最上面

#### 规则3：Section 4 工单数量分析 + 工单时效分析 → 全部来自复盘跟踪表

`# 四、工单总结` 下所有带数字的橙色文本，数据来源均为**复盘跟踪表**（不是工单数据表）：

- `X月共产生工单X个` → 跟踪表 `工单总数`
- `本次复盘筛选出X个工单` → 跟踪表 `复盘工单`
- `同比上月增加/减少XX%` → 对比跟踪表中上月的 `工单总数`
- `解决类别TOP3` → 跟踪表中各解决类别字段（`外部原因-无需技术排查`、`无需优化`、`外部原因-需技术排查` 等）
- `解决模块TOP3` → 跟踪表中各模块字段（`收银系统-餐饮`、`扫码点单`、`打印机` 等）
- **超时工单数/产研介入** → 跟踪表 `超时工单数`、`超时工单数-产研介入`
- **时效内解决占比** → `1 - 超时工单数/工单总数 × 100%`

---

### 数据来源一览

| 数据 | 来源 |
|------|------|
| 会议信息、议程 | 用户提供或从上月文档沿用 |
| **参与人员（开发TOP5）** | **开发复盘文档 Section 2 的前5名责任人** |
| **第三节标题 XX** | **复盘跟踪表 `工单总数`** |
| **第三节表格（所有数字）** | **复盘跟踪表（全部字段）** |
| **工单数量分析（所有数字）** | **复盘跟踪表** |
| **工单时效分析（所有数字）** | **复盘跟踪表** |
| 历史跟进事项 | 从上月复盘文档复制 |

### 7.1 填充第三节表格

使用 `scripts/fill_review_cells.cjs` 填充嵌套表格单元格。详细操作见 `references/data_mapping.md`。

配置脚本顶部：
```javascript
const DOC_ID = '...';  // 新创建的复盘总文档 ID
const MONTH = '2026-04';  // 目标月份
const CELL_DATA = {
  total:    '644',
  noOpt:    '160（产研介入94）',
  prodOpt:  '42（20）',
  techWork: '0',
  techCheck:'79（48）',
  noTech:   '208（28）',
  internal: '138（产研介入87）',
  solved:   '已解决54（27）',
  deferred: '延期处理66（46）',
  noRepro:  '无法重现：18（14）',
  timeout:  '88（58）',
};
```

执行：`node scripts/fill_review_cells.cjs`

### 7.2 第三节表格：最近3个月数据

模板中 `# 三、工单总计XX个(按工单数统计)` 下方自带一个 `<lark-table>` 格式的嵌套表格。此表格**必须保留**，不能删除或替换为文本。

#### 表格内容规则

表格内应填充**最近3次工单复盘的数据**（包含目标月份+前2个月）。例如做 2026-05 月复盘时，表格应包含：

| 行 | 内容 |
|----|------|
| 第一行（表头） | 复盘范围、时间、工单总数等列名 |
| 第一数据行（最旧） | 2026-03 数据（跟踪表记录） |
| 第二数据行（中间） | 2026-04 数据（跟踪表记录） |
| 第三数据行（最新，在最下方） | 2026-05 数据（跟踪表记录） |

**⚠️ 顺序规则**：
- 模板默认把最近月放在第一行（上方），但**正确顺序是旧数据在上、新数据在下**
- 因此需要把模板的行标签和数据都修改过来。例如模板中的 `2026-02` 行应改为 `2026-03` 数据，`2026-03` 行改为 `2026-04` 数据，`2026-04` 行改为 `2026-05` 数据
- 是的，需要把所有行的标签和数据都改一遍，不能偷懒只改一行

#### 数据获取

1. 从复盘跟踪表 `list` 全部记录
2. 找到最近3个月的记录（按月份排序 `2026-05` / `2026-04` / `2026-03`）
3. 提取各字段值：工单总数、复盘工单、超时工单数、无需优化、待产品优化、内部原因等

#### 填充方式

使用 `scripts/fill_review_cells.cjs` 逐个填充表格单元格。详细操作见 `references/data_mapping.md`。

配置脚本顶部：
```javascript
const DOC_ID = '...';  // 新创建的复盘总文档 ID
const MONTH = '2026-05';  // 目标月份（用于查找表格中的对应单元格）
const CELL_DATA = {
  // 以下数据来自复盘跟踪表，key 见 data_mapping.md
  total:    '21',
  noOpt:    '11（产研介入7）',
  prodOpt:  '0',
  techWork: '0',
  techCheck: '0',
  noTech:   '0',
  internal: '10（产研介入3）',
  solved:   '已解决4（1）',
  deferred: '延期处理6（2）',
  noRepro:  '无法重现：0',
  timeout:  '11（3）',
};
```

如果目标月份在跟踪表中尚无数据（月未结束），表格中该行留空或填 "-"，用附注说明。

#### 重要：表格数据来自复盘跟踪表

复盘总文档第三节表格的数据**不直接来自工单数据表**，而是来自复盘跟踪表。跟踪表中各字段是 Lookup 公式，会自动根据 Step 0 创建的记录中的时间范围和已导入的工单数据计算汇总值。

因此复盘的正常顺序是：
1. **Step 0** → 创建跟踪表记录
2. **阶段一** → 导入工单数据
3. **之后** 跟踪表各 Lookup 字段会自动计算
4. **Step 7** → 从跟踪表读取计算结果，填入第三节表格

### 7.3 填充工单总结

**⚠️ 所有数字均来自复盘跟踪表，不是工单数据表**

模板中 Section 4 的每一条文本都有橙色标记的数字占位符。所有数值必须从**复盘跟踪表**获取，不能从刚导入的工单数据表（24条）统计。

**工单数量分析**需要以下统计数据（全部来自复盘跟踪表 filter `复盘范围`=当月）：

| 变量 | 跟踪表字段 | 取值方式 |
|------|-----------|---------|
| 当月工单总数 | `工单总数` | 直接取值 |
| 复盘工单数 | `复盘工单` | 直接取值 |
| 同比上月增减% | 对比上月 `工单总数` | `(本月-上月)/上月 × 100%` |
| 解决类别TOP3 | `外部原因-无需技术排查`、`无需优化`、`待产品优化`、`外部原因-需技术排查` 等 | 按字段值排序取TOP3 |
| 解决模块TOP3 | `收银系统-餐饮`、`扫码点单`、`打印机`、`收银系统-零售` 等 | 按字段值排序取TOP3 |

**工单时效分析**需要（全部来自跟踪表）：
| 变量 | 跟踪表字段 | 取值方式 |
|------|-----------|---------|
| 超时工单数 | `超时工单数` | 直接取值 |
| 超时产研介入 | `超时工单数-产研介入` | 直接取值 |
| 时效内解决占比% | `工单总数` + `超时工单数` | `(1 - 超时工单数/工单总数 × 100%)`，保留两位小数 |

**获取方式**：`feishu_bitable_app_table_record list` 查询 `复盘范围` = 当月，然后从返回的 fields 中提取所需字段。

**注意**：Section 4 的文本包含大量橙色标记（`<text color="orange">`），无法通过简单的 `replace_range` 或 `selection_with_ellipsis` 更新（因为标记打断了文本连续性）。
- 超时文本块（如 `25个超时工单`）可以通过 block PATCH 更新（type 2 块）
- 列表项（type 12）和标题块（type 3）无法通过 block API 更新
- 必须通过 `feishu_update_doc replace_all`（但会破坏 callout）或手动编辑

**问题总结**和**历史跟进事项**从上月文档复制，或由用户填写。

---

# 阶段三：开发复盘文档

## Step 8: 创建开发复盘文档

### 前置检查

**同样先检查目标月度目录下是否已有同名文档。** 使用 `feishu_wiki_space_node list` 确认后再操作。

### 创建步骤

1. **复制模板**：从 `Secqwa7deiaRwTkUsG6cJ7xpnzj` 复制创建
2. **重命名**：按月份命名，如 `智慧门店-2026-05月-开发复盘文档`
3. **放入对应目录**

### ⚠️ 开发复盘文档需要修改/填充的内容（共3项，缺一不可！）

**不要破坏模板原有的换行和段落结构。** 完整模板结构如下：

```
# 一、开发复盘文档
- 工单复盘文档：<mention-doc token="..." type="wiki">智慧门店工单复盘模版</mention-doc>   ← 需修改 ①
- 复盘表格内容：<mention-doc token="..." type="wiki">2026-xx月-智慧门店工单数据</mention-doc>   ← 需修改 ②

# 二、主要人员总结材料
<text color="orange">开发A(</text>工单总数<text color="orange">x</text>个)(超时工单<text color="orange">x</text>个)   ← 需修改 ③
[callout] ← 保持模板原样！不要改动！
```

---

#### 修改① 替换「工单复盘文档」mention-doc

**目标**：指向本次创建的复盘总文档 wiki 节点
```
{ mention_doc: { token: "{复盘总文档的wiki节点token}", obj_type: 16, // wiki
  title: "智慧门店-2026-05月-工单复盘",
  url: "https://sqb.feishu.cn/wiki/{wiki节点token}" } }
```

#### 修改② 替换「复盘表格内容」mention-doc

**目标**：指向当前月份的工单数据 bitable
```
{ mention_doc: { token: "{月份bitable的app_token}", obj_type: 8, // bitable
  title: "智慧门店-2026-5月工单数据",
  url: "https://sqb.feishu.cn/base/{app_token}?table={table_id}&view={view_id}" } }
```

#### 修改③ 替换橙色高亮区的占位符（开发A~E 和 x）

**这是最容易出错的地方！严格按照以下步骤：**

1. 找到文档根 children 中的 **type 2 块**（5个，对应开发A~E）
2. 对每个块的 elements，执行 3 个替换：

| 位置 | 原来 | 改为 | 示例（李文茂） |
|------|------|------|------|
| 第一个 text_run | `开发A(` | `责任人姓名+（` | `李文茂(` |
| 中间 text_run（内容为`x`） | `x` | 该人**工单总数** | `5` |
| 末尾 text_run（内容为`x`） | `x` | 该人**超时工单数** | `4` |

**元素结构参考**（以开发A为例，其余开发B~E结构相同但元素数可能不同）：
```javascript
// 开发A 的 elements（8个元素）：
[ {text_run: "开发A("},      // 改为人名
  {text_run: "工单总"},        // 不动
  {text_run: "数"},           // 不动
  {text_run: "x"},           // 改为工单总数
  {text_run: "个"},           // 不动
  {text_run: ")(超时工单"},    // 不动
  {text_run: "x"},           // 改为超时工单数
  {text_run: "个)"}           // 不动
]

// 开发B~E 的 elements（6个元素）：
[ {text_run: "开发X("},       // 改为人名
  {text_run: "工单总数"},       // 不动
  {text_run: "x"},            // 改为工单总数
  {text_run: "个)(超时工单"},   // 不动
  {text_run: "x"},            // 改为超时工单数
  {text_run: "个)"}            // 不动
]

// 替换后效果：
[ {text_run: "李文茂("},
  {text_run: "工单总"},
  {text_run: "数"},
  {text_run: "5"},           // 原来是 x
  {text_run: "个"},
  {text_run: ")(超时工单"},
  {text_run: "4"},           // 原来是 x
  {text_run: "个)"}
]
```

**✅ 最终橙色高亮区的效果**（模板 → 正确）：
```
<text color="orange">开发A(</text>工单总数<text color="orange">x</text>个)(超时工单<text color="orange">x</text>个)
   ↓ 替换为
<text color="orange">李文茂(</text>工单总数<text color="orange">5</text>个)(超时工单<text color="orange">4</text>个)
```

---

### ❗ 绝对不要做的事（踩坑记录）

| ❌ 错误 | 后果 |
|---------|------|
| 只替换数字 `x`，不把`开发A`改成责任人姓名 | 橙色区显示 "开发A(工单总数5个)" 而非 "李文茂(工单总数5个)" |
| 把分析总结填入 callout 内容 | callout 应该保持模板占位符状态，留给用户手动填写 |
| 写入多行文本到 callout 块（如 `工单原因分析：\n1. xxx`） | 后续无法一次性清空，需要逐元素删除残留行 |
| 用 `feishu_update_doc replace_all` 更新文档内容 | 会破坏 `<callout>` 块结构 |

---

### 责任人的选取规则
- 从工单数据表（阶段一导入的）统计 TOP5 责任人
- **排除** `崔文思` 和 `蒋达周`
- 统计每个责任人：
  - 工单总数：该责任人名下的工单数量
  - 超时工单数：该责任人名下 `超时时间` 不为空的工单数

**数据获取方式**：
1. 从工单数据表 `list` 全部记录
2. 按 `责任人` 字段分组计数
3. 排除崔文思、蒋达周
4. 取工单数最多的前5名
5. 对每个负责人统计超时工单数

**填充方式**：
- 使用 UAT 调飞书 Docx PATCH API 逐元素更新，不要用 `feishu_update_doc`（会破坏 `<callout>` 块）
- 通过 PATCH `update_text_elements` 替换橙色占位符的 `x`，保留 `<text color="orange">` 样式
- 模板已有5个开发者槽位（开发A-E），直接 PATCH 全部5个槽位的占位符，无需 POST 追加

### 分析总结占位符

每个责任人段落的 callout 区域包含需要用户填写的分析总结（无法自动生成）：
```
分析总结：
超时工单分析：
工单原因分析：
需更改需跟进事项：
需同步产品：
需同步开发：
需同步测试：
需同步客服：
需同步技术支持：
其他：
```

在填充数据后告知用户这些区域需要手动填写。

---

# 脚本说明

## `scripts/fetch_furcas.py`
从 Furcas API 拉取数据。参数：`-s` 开始日期、`-n` 结束日期、`-o` 输出路径。

## `scripts/import_to_bitable.mjs`
CSV → 多维表格导入一体化脚本。环境变量：`APP_TOKEN`, `TABLE_ID`, `CSV_PATH`, `BATCH_SIZE`, `TABLE_NAME`。

## `scripts/generate_batches.py`
CSV → JSON 批处理文件。参数：`--csv`, `--output-dir`, `--batch-size`。

## `scripts/fill_review_cells.cjs`
填充复盘总文档第三节嵌套表格单元格。直接调飞书 Docx PATCH API，用用户 OAuth UAT。顶部配置区设置月份和数据。

---

# 注意事项

## 通用

1. **Cookie 时效性**：Furcas Cookie 可能过期，过期后需用户重新拷贝
2. **导入长度限制**：batch_create 每批 ≤ 15 条
3. **看板视图分组**：创建后需显式设置 `kanban_field_id`
4. **表格嵌套单元格**：不能用 markdown flat table 替代，必须用 `fill_review_cells.cjs` 逐个填充
5. **替换 `x` 变量**：开发复盘文档的 `<text color="orange">x</text>` 占位符必须用 UAT PATCH API 逐元素更新（保留橙色样式），**禁止用 `feishu_update_doc replace_all`**（会破坏 `<callout>` 块）。复盘总文档的 `x` 同样用 PATCH API 更新。
6. **责任人排除**：开发复盘 TOP5 统计需排除崔文思、蒋达周
7. **文档排版**：从模板复制后，确认文档结构完整。当前模板（2026-05起）已无 callout 提示块，无需手动删除

### 模板结构守则

8. **永远不要合并或删除模板中的换行**。模板的每个段落、列表都是精心设计的结构。特别是：
   - 会议信息的 `会议主题` / `会议时间` 各占一行
   - 会议议程的 `**复盘时间：**` / `**复盘范围：**` / `**参与人员：**` 各自独立成段
   - 参与人员列表用 `-` 无序列表格式
   - 开发复盘文档的 callout 中每个冒号标题独占一行，`>` 前缀必须保留
   - ⚠️ 复盘总文档模板（2026-05 版本）**已无 callout 块**，Section 3 标题后直接是 `<lark-table>`

9. **`feishu_update_doc` 禁止用于含表格的文档**：复盘总文档的 Section 3 包含 `<lark-table>`，**任何模式（overwrite/replace_all/append/insert_after/replace_range/delete_range）都会摧毁表格属性**（rowspan、colspan 丢失，cols 数变化）。
   - ❌ `feishu_update_doc` 会先序列化文档为 markdown 再反序列化，过程中 lark-table 的 HTML 属性丢失
   - ✅ **所有更新必须使用 UAT Token 直接调飞书 PATCH blocks API，逐元素更新**
   - ✅ 表格单元格：`PATCH /blocks/{cell_child_text_id}` 用 `update_text_elements`
   - ✅ 文本段落：`PATCH /blocks/{block_id}` 用 `update_text_elements`

10. **`feishu_update_doc` 禁止用于含 callout 块的文档**：开发复盘文档不含 lark-table，但含有 `<callout>` 块（type=19），feishu_update_doc 的 markdown 序列化/反序列化会：
    - ❌ `<callout>` → `>` blockquote（结构被破坏，callout 框消失）
    - ❌ `<text color="orange">` → 普通文本（颜色标记丢失）
    - ❌ 可能引入额外段落（如 `# 三、总结`）
    - ✅ **正确做法：所有更新必须使用 UAT Token 直接调飞书 PATCH blocks API，逐元素更新**

## 开发复盘文档填充经验

11. **替换开发 A/B/C/D/E 标记**（模板现含5个槽位）：
    - 模板使用 `<text color="orange">开发A(</text>工单总数<text color="orange">x</text>个)(超时工单<text color="orange">x</text>个)`（B/C/D/E同理）
    - 替换时搜索整个带标记的字符串，替换为 `**张姝（工单总数12个）（超时工单5个）**`
    - 橙色标记在替换时自动去除，改用加粗（** **）

12. **模板已有 5 个开发者槽位（开发A-E）**：最新模板 `Secqwa7deiaRwTkUsG6cJ7xpnzj` 已直接包含 5 组（开发A/B/C/D/E），每组含 `<text color="orange">开发X(工单总数x个)(超时工单x个)</text>` + `<callout>` 块。
    - 直接 PATCH 填满全部 5 个槽位即可（无需 POST 追加）
    - TOP5 开发者按工单数从多到少填入开发A→E
    - ❌ 模板只有3个槽位时（旧版），才需要 POST `/children` 追加开发D和E

## 含表格文档的 PATCH API 更新（关键）

### ⚠️ 核心规则：feishu_update_doc 不可用于含复杂表格的文档

复盘总文档的 Section 3 包含 `<lark-table>`（带 rowspan/colspan），**feishu_update_doc 的任何模式（replace_all、insert_after、delete_range、replace_range、overwrite）都会摧毁表格属性**。

原因：这些模式先将文档序列化为 markdown 再反序列化，反序列化时 lark-table 的 HTML 属性丢失。

后果示例：
- `cols="11"` → `cols="10"`（colspan=2 的合列丢失）
- `rowspan="3"` → 消失（每月 3 行不再合并）
- 表格从 10 行 11 列 → 7 行 10 列

### ✅ 正确做法：直接调飞书 Docx PATCH API

```
PATCH /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}
Authorization: Bearer {user_access_token}
Body: {
  "update_text_elements": {
    "elements": [{
      "text_run": {
        "content": "新文本内容",
        "text_element_style": {}
      }
    }]
  }
}
```

⚠️ `update_text_elements` 会**丢失格式**（bold/orange）：新的 text_run 使用空的 `text_element_style: {}`，所以加粗、橙色标记等格式会丢失。如需保留格式，需在 `text_element_style` 中显式设置 `bold: {}` 或 `inline_code: {color: 25, background_color: 2}`（橙色）。

### 更新顺序不可逆

```
模板拷贝 → 填表（fill_review_cells.cjs）→ 更新文本（PATCH API）
                 ↑                 ↑
           必须先做             后做
```

填表（表格单元格级别的 block 操作）必须在任何文本替换之前完成。如果先做文本替换再填表，feishu_update_doc 已经破坏了表格结构。

### Block-type-specific 文本属性

通过 PATCH API 读取/更新文本时，不同 block type 的文本存在不同属性中，不是都在 `block.text` 下：

| Block Type | 描述 | 文本所在属性 |
|-----------|------|------------|
| 2 | 文本段落 | `block.text.elements` |
| 3 | 标题1（#） | `block.heading1.elements` |
| 4 | 标题2（##） | `block.heading2.elements` |
| 5 | 标题3（###） | `block.heading3.elements` |
| 12 | 无序列表项（-） | `block.bullet.elements` |
| 14 | 有序列表项（1.） | `block.ordered.elements` |

**PATCH API 写入统一使用 `update_text_elements`**，不分类型。

### Heading 块可以有子节点

飞书文档中，标题块（block_type=3/4/5）**可以有** 子 children（如 Section 4 的 `## 工单数量分析` 就包含 bullet 子节点）。Section 4 的文本不是根级节点，而是 heading 的 children：

```javascript
// Section 4 的数据需要遍历 heading 的 children 获取：
const rootBlocks = getChildren(document_block_id);
for (const b of rootBlocks) {
  // b.block_type === 4 （heading2）
  // b.txt === '工单数量分析'
  const sectionKids = getChildren(b.block_id);  // ← ✅ 能拿到子节点
  // sectionKids[0].block_type === 12 （bullet）
  // sectionKids[0].txt === '2026-05月共产生工单81个...'
}
```

**但是**：表格（type=31）和 callout（type=19）**不是**任何块的 children，它们始终是文档根层的同级节点。即使它们在视觉上位于某个 heading 下方，API 读取时它们和 heading 是平级关系。

### 权限与加密

PATCH API 需要 User Access Token（UAT），用 OAuth 方式获取。UAT 加密存储，解密方式：

```javascript
const d = path.join(process.env.XDG_DATA_HOME || path.join(os.homedir(), '.local', 'share'), 'openclaw-feishu-uat');
const enc = fs.readFileSync(path.join(d, '{appId}_{userOpenId}.enc'));
const masterKey = fs.readFileSync(path.join(d, 'master.key'));
// AES-256-GCM: IV 12 bytes + tag 16 bytes + ciphertext
const iv = enc.subarray(0, 12), tag = enc.subarray(12, 28), cipher = enc.subarray(28);
const decipher = crypto.createDecipheriv('aes-256-gcm', masterKey, iv);
decipher.setAuthTag(tag);
const uat = JSON.parse(Buffer.concat([decipher.update(cipher), decipher.final()]).toString('utf8')).accessToken;
```

### fill_review_cells.cjs 的使用

位置：`scripts/fill_review_cells.cjs`

配置方式（通过环境变量传入，不需要修改脚本）：
```bash
# 设置必要的环境变量
export DOC_ID="新文档的obj_token"
export SENDER_OPEN_ID="ou_你的飞书open_id"
export MONTH="2026-05"
export APP_ID="cli_a97b6a0ffc399cc0"  # 团队共用，通常已设为默认值

# 运行脚本
node scripts/fill_review_cells.cjs
```

脚本中的 `CELL_DATA` 由 AI 根据复盘跟踪表数据自动生成并作为环境变量传入，请勿手动修改。

脚本会自动填充**最近 3 个月**（本月 + 前 2 个月）的数据到表格中的对应位置。填写规则见 `references/data_mapping.md`。

### 文本更新脚本参考

```javascript
// readText 必须检查所有 block-type 属性
function readText(block) {
  const src = block?.text || block?.heading1 || block?.heading2 || 
              block?.heading3 || block?.bullet || block?.ordered || block?.todo;
  return src?.elements?.map(e => e.text_run?.content || '').join('') || '';
}

// 写入统一用 update_text_elements
async function patchBlock(uat, blockId, newText) {
  const body = {
    update_text_elements: {
      elements: [{ text_run: { content: newText, text_element_style: {} } }]
    }
  };
  const url = `${DOCX_BASE}/${DOC_ID}/blocks/${blockId}`;
  return apiRetry('PATCH', url, { Authorization: `Bearer ${uat}` }, JSON.stringify(body));
}
```

## UAT 与 API 调用

13. **UAT 解密方式**：
    - 加密目录路径（动态解析）：`$FEISHU_UAT_DIR` → `$XDG_DATA_HOME/openclaw-feishu-uat` → `~/.local/share/openclaw-feishu-uat`
    - 加密文件：`{uatDir}/{appId}_{userOpenId}.enc`
    - Master key：`{uatDir}/master.key`（**32 字节原始密钥，不需要 SHA256 哈希**）
    - 解密算法：AES-256-GCM，IV 12 字节 + tag 16 字节 + ciphertext
    - 解密后的 JSON 字段：`accessToken`（驼峰，不是 `access_token`）
    - `import_to_bitable.mjs` 和 `fill_review_cells.cjs` 均已正确实现动态路径解析

14. **mention-doc 的 token 解析**：
    - 当用 `<mention-doc token="wiki节点token" type="wiki">` 时，飞书 API 会自动解析为实际文档的 obj_token
    - type 也会自动更新（如 wiki → docx 或 bitable）
    - 因此如果后续的 replace_all 索引用的原始 wiki token 找不到内容，很可能已被 API 自动替换
    - 应在每次更新后重新 fetch-doc 确认实际内容

## Import 脚本已知 bug

15. **`import_to_bitable.mjs` 看板创建 bug**：
    - `createKanbanView("按责任人分组")` 创建的看板视图没有返回正确的 view_id（返回 undefined）
    - 后续设置 `kanban_field_id` 时会因 `view_id=undefined` 而失败
    - 变通方案：脚本跑完后，手动创建看板视图或用 UAT 调飞书 API PATCH `/views/{viewId}` 设置 `kanban_field_id`
    - 正确字段 ID：`责任人` 的 field_id（可通过 list_fields 获取）

16. **FIELD_MAP 硬编码**：CSV 列名 "工单状态/修复情况" → bitable 字段名 "工单状态|修复情况"（竖线）。如果 bitable 字段名用了斜杠，需要修改 FIELD_MAP 或重命名字段。

17. **超时备注字段可能导入后为空（2026-05-15 发现）**：
    - FIELD_MAP 包含 `"超时备注": "超时备注"` 映射
    - `batch_create` 传入纯字符串 `"崔文思->某人: 05-15 10:00；"` 可以正确写入（已验证）
    - `PUT` 传入纯字符串也可以正确写入（已用此方法补了19条）
    - **但某些情况下数据会丢失**：猜测与 Cookie 切换后 CSV 列顺序或旧数据残留有关
    - **修复**：已加 [5b/6] 校验步骤，导入后自动对比 CSV 与 Bitable 中超时备注数据量，发现不一致则警告

## 2026-05-06 完整复盘经验总结

以下为 2026-05 月工单复盘全流程中遇到并解决的问题汇总，下次工单复盘前请先通读，避免重复踩坑。

---

### 一、Furcas 数据拉取

#### ❗ Cookie 过期处理
Furcas API 登录态不可持久化。每次执行 `fetch_furcas.py` 前：
1. 打开浏览器 → F12 → Network → 随便请求 Furcas 页面
2. 从请求头复制 cookie 请求头完整值（含 `acw_tc` 和 `furcas` 字段）
3. 更新脚本中的 `HEADERS["Cookie"]` 变量
4. 不要只更新部分字段，`acw_tc` 每次都会变

#### ❗ 解决类别 ID 映射
拉取数据后 `fetch_furcas.py` 会按解决类别分类写入 CSV，ID 映射如下：
| ID | 类别 |
|----|------|
| 1 | 设计如此-无需优化 |
| 2 | 外部原因-无需优化 |
| 3 | 内部原因-已解决 |
| 4 | 内部原因-延期处理 |
| 5 | 内部原因-无法重现 |

---

### 二、复盘跟踪表（bitable 操作）

#### ❗ 跟踪表记录创建规范
创建复盘跟踪表记录时：
- `app_token = YMQjwQeWCipABCkl8y7ckZlunQe`
- `table_id = tblpygt9n8dqZcsw`
- 年份字段填 2026（单选）
- 月份字段填 05（单选）
- `工单总数` = 该月 Furcas 所有工单的总数（从查询结果 count 获取）
- `复盘工单` = 筛选后需要复盘的工单数（排除设计如此、外部原因-无需优化后）
- 创建后等待 1-2 秒再 PATCH 其他字段

#### ❗ 字段 ID 映射（跟蹤表）
| 字段名 | field_id |
|--------|----------|
| 工单总数 | fldg7k4Zb |
| 复盘工单 | fldBxBSm3x |
| 无需优化 | fld2Fi7oVD |
| 待产品优化 | fldQ45Kqj8 |
| 外部原因-技术派工 | fldW8sKSSx |
| 外部原因-需技术排查 | fldRerqDIp |
| 外部原因-无需技术排查 | fldVefvMG2 |
| 内部原因 | fldIor3W9R |
| 已解决 | flde2eaOu |
| 延期处理 | fldZqWk3G |
| 无法复现 | fldYplayCE |
| 超时工单数 | fldTQkMXsW |

#### ✅ 工单总数来源
`工单总数` 字段值来自 **Furcas API 返回的总数**，不是从导入 bitable 的记录数获取，不是从 CSV 行数获取。导入脚本只导入需要复盘的工单（筛选后的子集），不能当作总数。

---

### 三、复盘总文档操作（含表格的文档）

#### ❗ 含 lark-table 的文档禁止用 feishu_update_doc 的任何模式
`feishu_update_doc` 的 `overwrite`、`replace_all`、`append` 模式**都会损坏 lark-table**（返回 3000/4000515 等错误）。
- ✅ 正确做法：使用 UAT Token 直接调用 PATCH blocks API，逐格更新单元格文本
- ✅ 使用 PATCH 更新文本块（heading、text、bullet 等）
- ❌ 禁止 `feishu_update_doc` 的任何模式

#### ❗ 表格单元格偏移（110格布局）
每个复盘表格有 110 个单元格：
- 前 11 格 = 表头行
- 之后每 33 格 = 一个月的数据
- Group 0（03月）= cells[11..43]
- Group 1（04月）= cells[44..76]
- Group 2（05月）= cells[77..109]

**每个月份组 33 格，单元格偏移**：
| 偏移（组内） | 字段 | 行 |
|-------------|------|----|
| 0 | 月份标签 | row1 |
| 1 | 工单总数 | row1 |
| 2-3 | 无需优化（colspan=2） | row1 |
| 4 | 待产品优化 | row1 |
| 5 | 外部原因-技术派工 | row1 |
| 6 | 外部原因-需技术排查 | row1 |
| 7 | 外部原因-无需技术排查 | row1 |
| 8 | 内部原因 | row1 |
| 9 | 已解决 | row1 |
| 10 | 超时（rowspan=3） | row1 |
| 20 | 延期处理 | row2 |
| 31 | 无法复现 | row3 |

**数据数组顺序必须匹配 offset 顺序**：
```javascript
// 正确顺序：total(1), noOpt(2), prodOpt(4), techWork(5), techCheck(6), noTech(7), internal(8), solved(9), timeout(10), deferred(20), noRepro(31)
const data = ['516', '147（产研介入55）', '48（产研介入17）', '3（产研介入3）', '72（产研介入53）', '147（产研介入25）', '96（产研介入56）', '已解决38（产研介入16）', '49（产研介入28）', '延期处理47（产研介入31）', '无法复现：11（产研介入9）'];
```

#### ❗ 月份标签重命名级联 bug（关键！）
**不能按顺序逐个改多个月份标签**！
- ❌ 错误做法：依次执行 02→03, 03→04, 04→05
  - 改名 02→03 后，原 03 组的标签仍然是 03
  - 第二次操作 03→04 会匹配到 **刚改好的那组**，而不是原 03 组
  - 导致一个月份被跳过
- ✅ 正确方案 A：从后往前改（04→05, 03→04, 02→03）
- ✅ **推荐方案 B**：一次性全部覆盖写入，无视当前值
  - 用已知正确数据直接覆盖所有三组，每次重新写全部数据
  - 这是最安全的做法

#### ❗ 表头标题行丢前缀
更新 heading1 的 `工单总计XX个(按工单数统计)` 后，前缀 `三、` 会丢失。
- **原因**：`update_text_elements` 完全替换了所有元素，前缀在另一个 element 中
- **修复**：更新时要保留完整标题，用 `# 三、工单总计x个(按工单数统计)`

#### ❗ heading 块用 update_text_elements
- ❌ `update_heading1` / `update_heading2` / `update_heading3` → 返回 `1770001 invalid param`
- ✅ `update_text_elements` → 对 heading1/2/3/text/bullet/ordered 都有效
- **通用原则**：所有文本元素的更新一律用 `update_text_elements: { elements: [...] }`

#### ❗ Section 4 子块遍历
Section 4（工单数量分析等）的 bullet 文本是 **heading 的 children**，不是根级块。
需要：
1. 遍历根级块找到 heading（type=4, txt='工单数量分析'）
2. 获取该 heading 的 children（`gC(docId, heading.block_id)`）
3. 逐个更新这些 bullet 块的文本

#### ✅ 文本更新用 element-level 操作
当 template 有 `<text color="orange">x</text>` 样式时，不能简单替换整个文本字符串——会丢失颜色样式。
- ✅ 遍历 `elements[]`，只改 content 不变 style
- ✅ 如在会议主题中改 `10`→`05`，保留其余所有 element 的 style 属性

---

### 四、Callout 块处理

#### ❗ Callout 块不可通过 API 删除
- Feishu Docx API 的 DELETE 端点对 type=19（callout/quote）块返回 404
- ❌ `DELETE /blocks/{block_id}` 对 callout 无效
- ✅ 变通方案：只清空子节点的文本内容（将其 text element content 设为空字符串）
- ⚠️ Callout 框本身只能**手动在飞书页面删除**（选中后按 Delete/Backspace）

---

### 五、mention-doc 处理

#### ❗ mention-doc 是内联元素
- mention-doc **不是**独立的 type=33 块（那是独立 mention doc block）
- 在文本段落中，mention-doc 是 `elements[]` 数组中的一个 element
- 同一 element 可能同时有 `text_run` 和 `mention_doc` 两个属性

#### ❗ 更新 mention-doc token 的正确方式
PATCH 时需传入完整 element，**必须带的字段**：
```json
{
  "text_run": { "content": "显示文字", "text_element_style": {} },
  "mention_doc": {
    "obj_type": 16,  // 整數！不能传字符串 "wiki"
    "text_element_style": {},
    "token": "UJdQwNdkPidcvKkXZzbcL1tDnaf",  // wiki 节点 token
    "title": "显示标题",
    "url": "https://sqb.feishu.cn/wiki/UJdQwNdk..."
  }
}
```
- `obj_type` 是**整数**（16=wiki节点），传字符串会报 `99992402 field validation failed`

#### ❗ token 会被自动解析
发送 wiki 节点 token 后，飞书 API 会自动解析为实际文档的 obj_token：
- ⚡ token: `UJdQwNdk...` (wiki) → `UtJCdfO5Iotw...` (docx obj_token)
- ⚡ type: 16 (wiki) → 22 (docx)
- ⚡ url 保持不变（wiki URL）
- ⚡ title 会自动从**文档实际标题**获取，发送的 title 字段被忽略

#### ❗ 显示文本无法通过 API 修改
mention 在文档中显示的文字由**文档标题**决定，不是由你写入的 text_run.content 或 title 字段决定。
- ✅ 要改显示文字，必须**改文档标题**（手工右键重命名）
- ❌ 通过 PATCH 修改 element 中的 text_run.content 或 mention_doc.title 均无效

---

### 六、开发复盘文档操作

#### ❗ 旧版模板只有3个开发槽位（已更新为5个）
模板 `Secqwa7deiaRwTkUsG6cJ7xpnzj` 已在 2026-05-07 更新，直接包含开发A-E 五个槽位。旧版只有3个时：
1. 先 PATCH 填满 3 个槽位
2. 再通过 `POST /blocks/{root_doc_id}/children` 添加第 4、5 个
1. 用 UAT PATCH API 更新 3 个槽位的开发者名称和数量（逐元素更新，保留橙色样式）
2. 再通过 `POST /blocks/{root_doc_id}/children` 添加第 4、5 个

#### ❗ insert_after 的正确方式（插入兄弟块）
要插入兄弟块**不是** POST 到目标块，而是 POST 到**父块**（根文档 block_id = doc_id）：
```javascript
// ✅ 正确：POST 到父块（文档本身），指定 index
POST /documents/{docId}/blocks/{docId}/children
{ index: 金海轩的索引+1, children: [{ block_type: 2, text: { elements: [...] } }] }

// ❌ 错误：POST 到目标块自己（会把新内容作为金海轩的子块）
POST /documents/{docId}/blocks/{金海轩的block_id}/children
```

#### ❗ x 是单字母不是 xxx
模板中的占位符是 `x`（如 `工单总数x个`），不是 `xxx`。替换时注意匹配模式。

#### ❗ 排除特定人员
开发复盘 TOP5 必须排除崔文思（技术支持）和蒋达周（运营）。统计开发者时：
- 先统计每个开发者的工单数
- 去掉崔文思和蒋达周
- 取前 5 个填入

---

### 七、文档创建与复制

#### ❗ 模板复制后需验证 obj_token
`wiki_space_node action=copy` 返回的 `obj_token` 可能字符错位（如 `UtJCdfO5Iotw` 与 `UtJCdfO5Iotw` 中的 `5` 和 `O` 互换）。复制后：
1. ✅ 立即用 `wiki_space_node action=get` 验证新节点的实际 `obj_token`
2. ✅ 或用 `feishu_fetch_doc` 直接读节点 token 验证文档是否可访问

#### ❗ 文档创建后有一定延迟
复制创建的文档不会立即就绪。如果立即调用 PATCH 操作，可能返回 `4000515 resource not found`。
✅ 建议做法：创建后等待 2-3 秒再操作。

#### ❗ 标题改不了（API 限制）
- ❌ `PATCH /docx/v1/documents/{docId}` → `1770001 invalid param`（不支持改标题）
- ❌ `PATCH /wiki/v2/spaces/{spaceId}/nodes/{nodeToken}` → 404（没有 rename 端点）
- ✅ **必须手工操作**：在飞书页面右键节点 → 重命名

---

### 八、UAT 工具链

#### ❗ 标准 UAT 文件路径
```javascript
const LINUX_UAT_DIR = path.join(
  process.env.XDG_DATA_HOME || path.join(os.homedir(), '.local', 'share'),
  'openclaw-feishu-uat'
);
const encFile = path.join(LINUX_UAT_DIR, `${APP_ID}_${OPEN_ID}.enc`);
const masterKey = fs.readFileSync(path.join(LINUX_UAT_DIR, 'master.key'));
const uatToken = JSON.parse(
  decrypt(fs.readFileSync(encFile), masterKey)
).accessToken;  // 驼峰！不是 access_token
```
- 不要硬编码 `/root/.local/share/`，用 `XDG_DATA_HOME` 环境变量
- 加密文件命名规则：`{appId}_{userOpenId}.enc`（冒号替换为下划线）
- `accessToken` 是驼峰，不是下划线格式
- 解密算法：AES-256-GCM，IV=12字节 + tag=16字节 + ciphertext
- Master key 是 32 字节原始密钥，**不需要 SHA256 哈希**

---

### 九、复盘范围规范

#### ✅ 复盘范围时间格式
| 复盘类型 | 时间范围 |
|---------|---------|
| 整月复盘 | 当月1日 00:00:00 - 当月最后一日 23:59:59 |
| 上半月复盘 | — 当月15日 23:59:59 |
| 下半月复盘 | 当月16日 00:00:00 — |

文档中 color="orange" 的复盘范围文本要保持橙底样式，仅改日期文字。

---

### ⚠️ 文档命名规范（严格执行，否则重做）

#### 三个文档必须从模板创建，命名必须为：

| 文档类型 | 模板 | 命名规范（5月示例） |
|---------|------|------------------|
| 工单数据跟踪表（Bitable） | `J4tawf06GijvEmkBTSCcdyNynsd` | `智慧门店-2026-05月-工单数据` |
| 工单复盘总文档 | GEqawooPYiDXLWkRKZHcJnLcnFc (wiki节点) | `智慧门店-2026-05月-工单复盘` |
| 开发复盘文档 | Secqwa7deiaRwTkUsG6cJ7xpnzj (wiki节点) | `智慧门店-2026-05月-开发复盘文档` |

#### 顺序：先建数据表 → 拉数据 → 建复盘文档

#### 常见错误：命名带"模版"后缀、用"05-整"格式、忘记创建在对应月份目录下

### 十一、文档填充规则

#### 表格更新（重要）
- lark-table文档禁止feishu_update_doc（破坏结构）
- 使用docx PATCH API更新text block的`update_text_elements`
- 结构：table_cell(31) → 110个type32子节点 → 每个含type2 text block

#### 文本更新
- Feishu文本可能拆成多个text_run元素（每个有独立样式）
- 判断用`elements.map(e=>e.text_run?.content).join('')`（完整文本），修改用单个element的content
- `update_text_elements`对所有block_type通用
- type 12是bullet块，元素在`.bullet.elements`中
- mention_doc不可通过API修改
- **`feishu_update_doc` 禁止用于含 callout(type=19) 的文档**（序列化会破坏callout结构）
- callout块的内容需通过PATCH其子block的`update_text_elements`更新，不要替换整个文档

#### 文档标题/命名
- 创建时在copy request的`title`参数设置
- 不能通过API修改已有wiki节点标题
- 需重命名时：copy新文档+删除旧节点

### 十二、关键常量表

| 项目 | 值 |
|------|-----|
| 工单数据(含Furcas) app_token | `YMQjwQeWCipABCkl8y7ckZlunQe` |
| 工单汇总表 table_id | `tblpygt9n8dqZcsw` |
| Furcas工单表 table_id | `tbln4MvksjBRkGGn` |
| 工单数据跟踪表模板(Bitable) | `J4tawf06GijvEmkBTSCcdyNynsd` |
| 2026目录节点（space 7510046829784662017 下） | `MDK5w5CcGi8RK6kRFMKcuBKLnNg` |
| 复盘总文档模板 | wiki 节点 `GEqawooPYiDXLWkRKZHcJnLcnFc` |
| 开发复盘文档模板 | wiki 节点 `Secqwa7deiaRwTkUsG6cJ7xpnzj` |
| 用户 open_id（需替换为自己的） | `ou_xxx...` |
| App ID | `cli_a97b6a0ffc399cc0` |
| Space ID | `7510046829784662017` |
| 05月目录节点 | `KAXEwRivKinTfTkshDucvSiGn4g` |

---

### 十三、2026-05-07 追加经验

以下为 2026-05-07 修复 4 月工单数据时发现并解决的问题。

#### ❗ `import_to_bitable.mjs` 清空步骤有静默失败 bug（致命！）

**bug 描述**：清空旧数据的 `batch_delete` API 参数名写错，用的 `records` 但正确参数是 `record_ids`。且 try-catch 吞掉了错误，导致清空失败时不停机：
```javascript
// ❌ 错误（旧代码）
await api("POST", `.../records/batch_delete`, { records: ids });
// 清空失败，错误被 catch 吃掉
// 旧数据继续留在表中，新数据追加写入
// → 每条工单出现 2 遍（304条 = 152 × 2）
```

**修复**：
1. 参数名改为 `record_ids` ✅
2. 去掉 try-catch，让清空失败直接报错停机 ✅
3. 导入完成后新增去重步骤（最后一道防线）✅
4. 去重逻辑：按工单 ID 分组，每个工单只保留 1 条记录 ✅

#### ❗ 多条同名空表被创建（`智慧门店-2026-05月-工单数据` × 4）

**原因**：首次创建 bitable 时没有检查知识库目录下是否已有同名表格。

**修复方式**：后续复盘时，在创建新 bitable 前必须：
1. 先搜索「工单数据表」目录下是否有同月名称的表格
2. 如果有，直接复用，不创建新的
3. 搜索方式：`feishu_wiki_space_node list` 列出目录下所有节点，检查名称是否包含目标月份

#### ❗ Mention-doc 指向错误的表格

**原因**：从模板复制复盘总文档后，文档内的 mention-doc 指向的是模板的占位对象（4月表或模板），不是当前月份的表。

**修复方式**（已添加 Step 5b 到流程中）：
1. 导入数据后立即更新 mention-doc 链接
2. 将指向前月份的 bitable mention-doc 改为当前月份的
3. 将指向模板的 wiki mention-doc 改为实际开发复盘文档节点

#### ❗ UAT 没有 bitable 读取权限

Raw API 调用 `/bitable/v1/apps/{token}/tables/{table_id}/records` 返回 `99991679 Unauthorized`：
- UAT 用户授权不包含 `bitable:app:readonly` 或 `base:record:read`
- ✅ **feishu_bitable_app_table_record 工具可以正常读取**（使用 bot 身份或不同授权路径）
- ✅ 如果脚本需要用 UAT 读 bitable，需要先 check 权限，否则使用 `feishu_bitable_app_table_record` 工具

#### ❗ 单个 DELETE 大量记录会超时

去重脚本一次删 152 条记录（逐条 DELETE）因超时被 SIGTERM：
- 超时阈值约 2 分钟
- ✅ 分批删除 20 条为一个 checkpoint，每次加 `await new Promise(r => setTimeout(r, 50))` 限速
- ✅ 如果超时，再次运行脚本即可继续删剩余的

#### ❗ feishu_update_doc replace_all 破坏 callout 块（生成 "三、总结"）

**现象**：使用 `feishu_update_doc replace_all` 更新开发复盘文档后：
- `<callout>` 块 → `>` markdown blockquote（callout 框消失）
- `<text color="orange">` → 普通文本（橙色丢失）
- 多出 `# 三、总结` 等异常段落

**根因**：`feishu_update_doc` 先将文档序列化为 markdown，再反序列化回飞书文档格式。反序列化时：
- `<callout>` 被当作 `>` blockquote 处理
- 如果 markdown 末尾包含 `# 三、总结` 等标题，会被当作新段落加入
- **SKILL.md 第10条之前错误地允许了在含 callout 的文档中使用 feishu_update_doc**

**修复**：
1. 从模板重新创建文档 ✅（必须用 copy，不能用 feishu_create_doc 写 markdown）
2. 所有更新用 UAT PATCH API 逐元素操作，不用 feishu_update_doc ✅
3. SKILL.md 第10条已更正，明确禁止 feishu_update_doc 用于含 callout 的文档 ✅

#### ❗ 开发复盘文档模板更新为5个开发者槽位（2026-05-07）

模板 `Secqwa7deiaRwTkUsG6cJ7xpnzj` 在 2026-05-07 更新，"主要人员总结材料"下从3个槽位（开发A/B/C）扩展到5个（开发A/B/C/D/E）。

**影响**：
- ✅ 复盘流程不再需要 POST `/children` 追加开发D/E
- ✅ 直接 PATCH 填充5个槽位即可
- ⚠️ 旧版3槽位模板已废弃，但SKILL.md保留了旧方法作为参考
- SKILL.md 第11条已改为"替换开发 A/B/C/D/E 标记"
- SKILL.md 第12条已更新

#### ❗ 开发复盘文档 Section 1 的 mention-doc 链接需替换（2026-05-07）

复制模板后，开发复盘文档的 Section 1 包含两个指向模板/占位对象的 mention-doc：

```
# 一、开发复盘文档
- 工单复盘文档：<mention-doc token="GEqawooPYiDXLWkRKZHcJnLcnFc" type="wiki">智慧门店工单复盘模版</mention-doc>
- 复盘表格内容：<mention-doc token="J4tawf06GijvEmkBTSCcdyNynsd" type="wiki">2026-xx月-智慧门店工单数据</mention-doc>
```

**必须替换为：**
1. `工单复盘文档` mention-doc: token → 本次创建的 **复盘总文档** wiki 节点 token
2. `复盘表格内容` mention-doc: token → 当前月份工单数据 **bitable** token（含 table_id 和 view_id）

**变更方式**：PATCH 对应 block 的 `update_text_elements`，修改 mention_doc 的 `token`、`obj_type`、`url`。

#### ❗ 创建月份工单数据 bitable 的正确方式（2026-05-07）

**错误做法**（之前踩过的坑）：
1. ❌ `feishu_bitable_app copy` 从模板复制 → 创建独立 bitable（不在 wiki 目录中）
2. ❌ `feishu_wiki_space_node create` 传 obj_token → 又新建一个**空白 bitable**（表名 "Table"，字段全英文）
→ 导致 wiki 链接指向空表，数据在独立表里

**正确做法**（仅需一步）：
1. ✅ `feishu_wiki_space_node copy` 直接将模板节点复制到目标月份目录
   - `node_token: "J4tawf06GijvEmkBTSCcdyNynsd"`（工单数据表模板）
   - `target_parent_token: "{目标月份目录节点token}"`
   - `space_id: "7510046829784662017"`
   → 直接在 wiki 内创建副本，bitable 结构、字段、视图全部正确

**复制后的处理**：
1. 重命名 bitable（如 "智慧门店-2026-5月工单数据"）
2. 删除模板自带的 5 条空记录（`batch_delete` 空记录的 `record_ids`）
3. 导入 CSV 数据

**导入脚本注意事项**：
- 表名默认校验为 "工单数据"，但模板复制出来的表名是 "数据表"
  → 用 `--name "数据表"` 参数
- 看板视图创建后的 `view_id` 可能返回 undefined（脚本返回值解析 bug）
  → 视图实际已创建，可通过 `feishu_bitable_app_table_view list` 获取 `view_id`
  → 手工设置 `property: { kanban_field_id: "责任人字段ID" }`

**开发复盘文档人名占位符规则（2026-05-07）**：
- 模板中 `开发A(` `开发B(` 等是**人名占位符**，不是固定标签
- 必须替换为责任人实际姓名（如 `李文茂(`），不是仅替换数字
- 替换后第一个元素内容从 "开发A(" → "李文茂("，保持橙色样式不变

**开发复盘文档 callout 内容规则（2026-05-07）**：
- callout 内（分析总结：、超时工单分析：等10个字段）**不要填充任何内容**
- callout 应保持模板的占位符状态，留给用户手动填写
- 如果误填了多行文本，清理时需要：1) 把多余元素全删除 2) 只剩单元素 "分析总结："

---

### 2026-05-15 新增经验

#### ❗ 超时备注导入后校验
FIELD_MAP 已有映射，但首次导入后超时备注字段为空。已在脚本 [5/6] 验证后追加 [5b/6] 校验步骤，自动检测 CSV 中超时备注数据是否成功写入 bitable。

**补救方法**（当超时备注导入失败时）：
```bash
# 从 CSV 读取超时备注数据，逐条写入 bitable（通过 UAT PUT API）
# 脚本逻辑：遍历 bitable 记录 → 按问题链接匹配 CSV → 对有超时时间的记录填写超时备注
```
UAT API 的 `batch_create` 和 `PUT` 操作均正常，传入纯字符串即可。

#### ❗ 视图可能隐藏关键字段
4月数据表的视图 `vewadQIK4f` 的 `hidden_fields` 中包含了 `解决类别`、`解决模块`、`责任人` 三个字段，导致用户看不到数据。

**排查方法**：用 `feishu_bitable_app_table_view action=get` 获取视图配置，检查 `property.hidden_fields` 列表

**修复方法**：调用 UAT API PATCH 视图，设置 `property: { }`（空对象或省略 hidden_fields 即可清除）

---
