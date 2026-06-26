---
name: feishu-doc-publisher
version: 1.1.2
description: >-
  将 Markdown 文件发布为飞书（Feishu/Lark）在线文档。
  支持完整的 Markdown 语法，独创表格列宽智能自适应算法，完美呈现复杂富文本，并支持互联网公开分享。
  配置说明：运行前请确保在环境变量或工作区 `.env` 文件中配置 `FEISHU_APP_ID` 
  和 `FEISHU_APP_SECRET`。还可配置 `FEISHU_ADMIN`（邮箱或 OpenID）
  以实现发布后全自动将文档所有权移交给您的个人账号。
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
        - FEISHU_ADMIN
    primaryEnv: FEISHU_APP_SECRET
---

# 飞书文档发布器 (Feishu Doc Publisher)

将 Markdown 文件发布为飞书在线文档，完整支持表格等富文本样式。

## 前置条件

1. 用户需要在飞书开放平台创建应用并获取 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`。
2. 应用需要具备以下权限：
   - `docx:document` — 读写新版文档
   - `drive:drive` — 查看、评论、编辑和管理云空间中所有文件 (必须：用于配置文档分享权限及移交 Owner)
   - `docx:document:readonly` — 只读新版文档（可选）
3. **安全建议**：
   - 建议创建专用的飞书应用，仅授予文档读写权限（最小权限原则）。
   - 妥善保管 App Secret，避免泄露；如疑似泄露请立即轮换凭证。
   - 仅发布你确实需要上传到飞书的 Markdown 文件，避免发布包含敏感信息的文件。

## 安装

本技能无需额外安装第三方依赖包，使用纯 Python 标准库编写。仅需确保您的环境中已安装 Python 3 即可。

如果需要配置全局凭证（可选），您可以手动创建 `~/.config/feishu-doc-publisher/.env` 文件并写入凭证信息。

## 使用方式

### 发布 Markdown 文件到飞书

当用户要求将一个 Markdown 文件发布到飞书时，执行以下命令：

```bash
python3 {baseDir}/scripts/publish.py "<markdown_file_path>"
```

**参数说明：**
- `<markdown_file_path>`：待发布的 Markdown 文件路径（必填）

**输出示例：**
```
✅ 文档发布完成
📄 文档标题: 五一家庭出游计划
📄 文档 ID: FiMLd0a9so1tgLxp3rncj2AEnob
🔗 文档链接: https://feishu.cn/docx/FiMLd0a9so1tgLxp3rncj2AEnob
📊 成功: 85, 失败: 0
```

### 发布并指定自定义标题

```bash
python3 {baseDir}/scripts/publish.py "<markdown_file_path>" --title "自定义文档标题"
```

### 发布到指定目录

```bash
python3 {baseDir}/scripts/publish.py "<markdown_file_path>" --folder "<folder_token>"
```

`folder_token` 可以从飞书文件夹 URL 中获取。

### 设置公共链接权限（外部公开与组织内分享）

```bash
# 赋予组织内获得链接的人可编辑权限
python3 {baseDir}/scripts/publish.py "<markdown_file_path>" --share tenant-edit
```
支持的权限选项：
- `tenant-read`: 组织内可阅读
- `tenant-edit`: 组织内可编辑
- `public-read`: 互联网可见可阅读
- `public-edit`: 互联网可见可编辑

> **注意**：设置互联网可见需要您的飞书应用拥有相应的权限，且飞书企业管理后台未禁止将文档分享到组织外。

### 移交文档所有权 (Transfer Owner)

由于文档由脚本(机器人)创建，机器人默认是最高权限的 Owner。为便于后续您在飞书中管理该文档，可以在发布时将其所有权“过户”给指定的人类账号。
支持使用企业邮箱（`email`）或 `openid`、`userid` 等标识：

```bash
python3 {baseDir}/scripts/publish.py "<markdown_file_path>" --owner "email:your_name@company.com"
```
成功过户后，机器人将被降级，该人类账号将成为文档在飞书系统中的最终 Owner，可在飞书中随意调整分享和人员权限。

> **自动化提示**: 如果不想每次都在命令行输入 `--owner`，您可以在任意生效的 `.env` 文件中配置统一的环境变量 **`FEISHU_ADMIN`**。
>
> 脚本会自动通过内容推断您的身份类型：
> - 包含 `@` 符号，自动按 `email` 邮箱移交。
> - 以 `ou_` 开头，自动按 `openid` 移交。
> - 其他情况，默认按内部 `userid` 工号移交。
> 
> ```env
> # 在 .env 中增加如下配置，即可实现发文后全自动过户！
> FEISHU_ADMIN=your_name@company.com
> ```

## 支持的 Markdown 元素

| 元素 | 支持状态 | 说明 |
|------|---------|------|
| 标题 (h1~h6) | ✅ | 自动映射为飞书标题层级 |
| 段落 | ✅ | 普通文本段落 |
| **加粗** | ✅ | `**text**` 格式 |
| *斜体* | ✅ | `*text*` 格式 |
| ~~删除线~~ | ✅ | `~~text~~` 格式 |
| `行内代码` | ✅ | 反引号格式 |
| 超链接 | ✅ | `[text](url)` 格式 |
| 表格 | ✅ | 完整表格样式，含表头 |
| 有序列表 | ✅ | `1. item` 格式 |
| 无序列表 | ✅ | `- item` 格式 |
| 待办事项 | ✅ | `- [ ] item` 格式 |
| 分隔线 | ✅ | `---` 格式 |
| 引用 | ✅ | `> text` 格式 |
| 代码块 | ✅ | 三反引号格式 |

## 技术实现

1. 先调用飞书 `blocks/convert` API 将 Markdown 转为飞书 Block 结构
2. 创建空白飞书文档
3. 非表格内容使用 `children` 接口批量插入
4. 表格使用 `descendant` 接口插入（需要重建临时 block ID）
5. 插入失败时自动回退为纯文本格式

## 错误处理

- 如果发布脚本报 token 获取失败，检查 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 是否正确
- 如果报权限不足，确认飞书应用已开启文档相关权限
- 表格插入失败会自动回退为纯文本段落，不影响整体文档发布

## 配置说明

环境变量加载优先级（由高到低，找到即生效）：

1. **系统环境变量**: 系统中已存在的 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
2. **OpenClaw 统一配置**: `~/.openclaw/.env`
3. **专属全局配置**: `~/.config/feishu-doc-publisher/.env`
4. **当前工作区配置**: 执行该工具的当前目录或上级工作区目录中的 `.env` 文件
5. **Skill 本地目录**: 项目根目录下的 `.env` 文件

`.env` 文件格式：
```
FEISHU_APP_ID=cli_xxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxx
```

## 规则

- 始终通过 `{baseDir}` 引用脚本路径
- 发布前确认环境变量 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 已配置
- 脚本会自动按照预设优先级加载相关的 `.env` 配置文件
