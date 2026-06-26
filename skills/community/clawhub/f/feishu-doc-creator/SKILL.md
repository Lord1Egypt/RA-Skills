---
name: feishu-doc-creator
version: 1.0.0
description: 在飞书中创建各种类型的文档（多维表格、云文档、电子表格、幻灯片、思维笔记），自动命名并转移所有权，通过交互式卡片发送链接。支持特殊的周报管理模式。供 @larksuite/openclaw-lark 插件使用。
---

# Feishu Doc Creator - 飞书文档创建器

本skill提供在飞书中自动创建各种类型文档的能力，自动命名、转移所有权，并通过交互式卡片发送文档链接给用户。

## 核心优势

**绕过用户版本限制创建文档：**

- 飞书原生插件通常使用**用户身份**创建文档，非旗舰版用户会遇到创建数量限制
- 本skill使用**机器人应用身份**创建文档，不受用户个人版本限制，可以无限制创建
- 创建完成后自动将文档所有权转移给操作用户，用户直接使用
- **优先级：** 本skill优先级应高于飞书插件自带的文档创建功能

**独立使用，不依赖插件：**

- 可直接被Agent调用，不需要依赖其他飞书插件
- 自动从OpenClaw配置文件 `~/.openclaw/openclaw.json` 读取飞书凭证
- 参数传递灵活：命令行参数 > 环境变量 > OpenClaw配置

## 功能特性

- ✅ 支持创建 **4种类型** 的飞书文档：
  - 多维表格 (bitable)
  - 云文档 (docx)
  - 电子表格 (spreadsheet)
  - 幻灯片 (slide)
- ✅ 自动命名格式：`[时间]_[用户名]_[类型]`
- ✅ 创建后自动**转移所有权**给操作用户
- ✅ 通过**交互式卡片**发送文档链接
- ✅ 特殊 `wen_admin` 模式用于创建周报文档，转移给指定应用并添加协作者
- ✅ 遵循 OpenClaw 集成规范，从配置读取凭证，不硬编码

## 命令行使用

```bash
python scripts/create-document.py \
  --app-id <APP_ID> \
  --app-secret <APP_SECRET> \
  --type <DOC_TYPE> \
  --user-open-id <USER_OPEN_ID> \
  [--mode normal|wen_admin] \
  [--target-app-open-id <TARGET_APP_ID>] \
  [--admin-open-ids <ADMIN1>,<ADMIN2>]

> 支持的 `--type` 值：`bitable` / `docx` / `spreadsheet` / `slide`
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--app-id` | 否 | 飞书应用ID（也可从 `FEISHU_APP_ID` 环境变量读取，或从OpenClaw配置自动读取） |
| `--app-secret` | 否 | 飞书应用密钥（也可从 `FEISHU_APP_SECRET` 环境变量读取，或从OpenClaw配置自动读取） |
| `--type` | 是 | 文档类型：`bitable`\|`docx`\|`spreadsheet`\|`slide` |
| `--user-open-id` | 是 | 操作用户的 open_id |
| `--mode` | 否 | 创建模式：`normal`（默认）或 `wen_admin`（周报管理模式） |
| `--target-app-open-id` | 否 | `wen_admin` 模式下目标应用的 open_id |
| `--admin-open-ids` | 否 | `wen_admin` 模式下管理员 open_id 列表，逗号分隔 |
| `--output` | 否 | 输出格式：`json`（默认）或 `text` |

## 输出格式

### 成功（JSON）
```json
{
  "success": true,
  "document_url": "https://feishu.cn/docx/xxxxxxxx",
  "document_name": "2026-04-15 14:30:00_张三_云文档",
  "document_type": "云文档",
  "document_token": "xxxxxxxx",
  "message": "创建成功"
}
```

### 失败（JSON）
```json
{
  "success": false,
  "error": "错误信息描述"
}
```

## 文档类型映射

| CLI 类型 | event_key | 显示名称 | 链接格式 |
|----------|-----------|----------|----------|
| `bitable` | `duo` | 多维表格 | `https://feishu.cn/base/{token}` |
| `docx` | `wen` | 云文档 | `https://feishu.cn/docx/{token}` |
| `spreadsheet` | `biao` | 电子表格 | `https://feishu.cn/sheets/{token}` |
| `slide` | `hua` | 幻灯片 | `https://feishu.cn/slides/{token}` |

## 使用示例

### 示例 1：直接使用（自动读取配置）**推荐**

OpenClaw环境中已配置飞书凭证，无需手动提供：

```bash
python ./scripts/create-document.py \
  --type docx \
  --user-open-id "ou_xxxxxxxxxxxxxxxxxxxx"
```

### 示例 2：使用环境变量

```bash
export FEISHU_APP_ID="cli_xxxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

python ./scripts/create-document.py \
  --type bitable \
  --user-open-id "ou_xxxxxxxxxxxxxxxxxxxx"
```

### 示例 3：显式指定凭证

```bash
python ./scripts/create-document.py \
  --app-id "cli_xxxxxxxxxxxxxx" \
  --app-secret "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  --type bitable \
  --user-open-id "ou_xxxxxxxxxxxxxxxxxxxx"
```

### 示例 4：使用 wen_admin 模式创建周报

```bash
python ./scripts/create-document.py \
  --type docx \
  --user-open-id "ou_7f08870cea0f449d23f9fc25dd9e5046" \
  --mode wen_admin \
  --target-app-open-id "ou_21a60ec03625f90c951ce190d2d61467" \
  --admin-open-ids "ou_7f08870cea0f449d23f9fc25dd9e5046,ou_xxxxxxxxxxxxxx"
```

## wen_admin 模式（周报管理）

当使用 `--mode wen_admin` 时，会启用特殊逻辑：

1. **自动命名**：`{year}-第{week}周-周报-{user_name}`
2. **转移所有权**：将文档所有权转移给指定的目标应用（如行政虾机器人）
3. **添加管理者**：添加指定用户为文档管理者
4. **添加当前用户**：如果当前用户不在管理者列表中，也添加为管理者
5. **企业可见**：设置文档为企业内成员可见

这用于每周周报自动创建场景。

## 在 Agent 中直接调用

因为本skill会**自动从OpenClaw配置读取飞书凭证**，Agent可以直接调用，不需要手动传入凭证：

```javascript
// 在OpenClaw Agent中直接调用skill
const result = await exec({
  command: `python /Users/macstudio/.agents/skills/feishu-doc-creator/scripts/create-document.py ` +
           `--type ${docType} ` +
           `--user-open-id ${userOpenId}`
});

// 解析JSON输出
const output = JSON.parse(result);
if (output.success) {
  // output.document_url - 文档链接
  // output.document_name - 文档名称
  // output.document_type - 文档类型中文
  // output.document_token - 文档token
  console.log(`文档创建成功: ${output.document_url}`);
} else {
  // output.error - 错误信息
  console.error(`创建失败: ${output.error}`);
}
```

如果需要指定自定义凭证：

```javascript
const result = await exec({
  command: `python /Users/macstudio/.agents/skills/feishu-doc-creator/scripts/create-document.py ` +
           `--app-id ${yourAppId} ` +
           `--app-secret ${yourAppSecret} ` +
           `--type ${docType} ` +
           `--user-open-id ${yourOpenId}`
});
```

## 飞书权限要求

此skill需要飞书应用配置以下权限范围：

| 权限 | 说明 |
|------|------|
| `im:message` | 发送消息 |
| `docx:document:create` | 创建云文档 |
| `base:app:create` | 创建多维表格 |
| `bitable:app` | 访问多维表格 |
| `drive:drive` | 云盘访问 |
| `drive:file` | 文件操作 |
| `docs:permission.member:transfer` | 转移所有权 |
| `sheets:spreadsheet` | 电子表格 |
| `slides:presentation` | 创建幻灯片 |
| `contact:contact.base:readonly` | 获取用户信息 |
| `contact:user.employee_id:readonly` | 获取用户详情 |

## ⚠️ 集成注意事项

**优先级说明：**

在 `@larksuite/openclaw-lark` 插件中使用本skill时，应将本skill的文档创建优先级设置**高于**插件自带的用户身份创建方式。

**原因：**
- 插件自带方式：使用**用户身份**创建文档 → 受飞书版本限制（非旗舰版用户创建数量有限制）
- 本skill方式：使用**机器人应用身份**创建文档 → 不受用户个人版本限制，可以无限制创建
- 创建完成后本skill自动将文档所有权从机器人转移给操作用户

因此，启用本skill后，默认应该走本skill的创建流程。

## 机器人菜单配置

在飞书开发者后台为机器人配置自定义菜单：

| 菜单项名称 | event_key | 文档类型 |
|-----------|-----------|---------|
| 创建多维表格 | `duo` | bitable |
| 创建云文档 | `wen` | docx |
| 创建电子表格 | `biao` | spreadsheet |
| 创建幻灯片 | `hua` | slide |
| 创建周报 | `wen_admin` | docx (wen_admin模式) |

事件 `application.bot.menu_v6` 需要在飞书开发者后台订阅。

## 依赖安装

```bash
cd scripts
pip install -r requirements.txt
```

## 依赖包

- `requests` - HTTP 请求
- `lark-oapi` - 飞书开放平台 SDK

## 参考资料

- [飞书开放平台 - 创建多维表格](https://open.feishu.cn/document/zh-cn/bitable-v1/app/create)
- [飞书开放平台 - 创建云文档](https://open.feishu.cn/document/zh-cn/docx-v1/document/create)
- [飞书开放平台 - 转移文档所有者](https://open.feishu.cn/document/zh-cn/drive-v1/permission/transfer_owner)
