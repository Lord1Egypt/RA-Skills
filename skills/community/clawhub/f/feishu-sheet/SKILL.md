---
name: feishu-sheet
description: |
  飞书电子表格（Sheets）完整操作。当需要创建、读取或编辑飞书电子表格时激活此 skill。
  支持：创建表格、读写单元格、追加数据、图片插入、样式设置、合并单元格、行列操作、查找替换。
  需要飞书应用凭证：channels.feishu.appId 和 channels.feishu.appSecret（配置在 ~/.openclaw/openclaw.json 中）。
  飞书应用需开通 sheets:spreadsheet 权限。建议使用仅含表格权限的最小化飞书应用。
metadata:
  version: 1.2.0
  author: siyiding
  homepage: "https://clawhub.ai/skills/feishu-sheet"
  tags:
    - feishu
    - spreadsheet
    - sheets
  requires:
    - curl
    - python3
    - bash
  credentials:
    - name: channels.feishu.appId
      description: "Feishu app ID (from Feishu Open Platform). Configured in ~/.openclaw/openclaw.json at channels.feishu.appId"
      required: true
    - name: channels.feishu.appSecret
      description: "Feishu app secret (from Feishu Open Platform). Configured in ~/.openclaw/openclaw.json at channels.feishu.appSecret"
      required: true
  security:
    configFile: "~/.openclaw/openclaw.json (override with OPENCLAW_CONFIG env var)"
    credentialPath: "channels.feishu"
    networkAccess: "open.feishu.cn (Feishu Open API only)"
    fileAccess: "Reads local image files only when explicitly passed to insert_image/float_image commands"
    tokenCache: "Tenant access token cached in $TMPDIR with per-user isolation (uid suffix)"
    note: "Credentials are validated against ^[A-Za-z0-9_-]+$ before use. Python inline script uses single-quoted strings to prevent shell injection. Recommend using a minimal-permission Feishu app."
---

# 飞书电子表格 Skill

通过 `exec` 调用 `~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh` 脚本操作飞书电子表格。

## 前提条件

1. **飞书应用凭证**：`~/.openclaw/openclaw.json` 中必须配置 `channels.feishu`，包含 `appId` 和 `appSecret`
2. **飞书应用权限**：应用需要开通「电子表格」相关权限（`sheets:spreadsheet`）
3. **系统依赖**：`curl`、`python3`、`bash`

凭证自动从 `openclaw.json` 读取，无需手动配置。可通过 `OPENCLAW_CONFIG` 环境变量指定配置文件路径。

## Token 提取

从 URL `https://feishu.cn/sheets/shtcnABC123` → `spreadsheet_token` = `shtcnABC123`

---

## 📊 表格操作

### 创建电子表格
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh create '表格标题'"
```
返回 `spreadsheet_token` 和 URL。可选第二参数 `folder_token`。

### 获取元数据（必须先调这个拿 sheet_id）
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh meta shtcnABC123"
```

---

## 📖 数据读写

### 读取数据
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh read TOKEN 'sheetId!A1:C10'"
```

### 读取多个范围
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh read_multi TOKEN 'sheetId!A1:C10' 'sheetId!E1:F5'"
```

### 写入数据（覆盖指定范围）
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh write TOKEN 'sheetId!A1:C2' '[[\"表头1\",\"表头2\",\"表头3\"],[\"数据1\",100,true]]'"
```
values 是 JSON 二维数组。字符串用引号，数字和布尔值不用。

### 追加数据（在已有数据后面添加行）
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh append TOKEN 'sheetId!A1:C1' '[[\"新行1\",\"新行2\",\"新行3\"]]'"
```

### 前插数据
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh prepend TOKEN 'sheetId!A1:C1' '[[\"插入行1\",\"插入行2\",\"插入行3\"]]'"
```

---

## 🖼️ 图片操作

### 插入图片到单元格（本地文件）
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh insert_image TOKEN 'sheetId!E1:E1' /path/to/image.png"
```
图片会填充到指定单元格内。Range 必须是单个单元格。

### 插入浮动图片（本地文件）
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh float_image TOKEN sheetId /path/to/image.png 'sheetId!F1:F1' 400 300"
```
参数：token, sheet_id, 文件路径, 锚点单元格(可选), 宽度(可选), 高度(可选)

### 插入浮动图片（URL）
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh float_image_url TOKEN sheetId 'https://example.com/image.png' 'sheetId!F1:F1' 400 300"
```

---

## 🎨 样式操作

### 设置单元格样式
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh style TOKEN 'sheetId!A1:D1' '{\"bold\":true,\"foreColor\":\"#FFFFFF\",\"backColor\":\"#4472C4\",\"fontSize\":14}'"
```

**支持的样式属性：**
- `bold` (bool) — 加粗
- `italic` (bool) — 斜体
- `foreColor` (string) — 字体颜色，如 `#FF0000`
- `backColor` (string) — 背景颜色，如 `#FFFF00`
- `fontSize` (int) — 字号，如 `14`
- `horizontalAlign` (int) — 水平对齐：0=左, 1=中, 2=右
- `verticalAlign` (int) — 垂直对齐：0=上, 1=中, 2=下
- `textDecoration` (int) — 0=无, 1=下划线, 2=删除线, 3=两者都有

### 批量设置样式
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh style_batch TOKEN '{\"data\":[{\"ranges\":\"sheetId!A1:D1\",\"style\":{\"bold\":true}},{\"ranges\":\"sheetId!A2:D10\",\"style\":{\"fontSize\":12}}]}'"
```

---

## 🔗 合并单元格

### 合并
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh merge TOKEN 'sheetId!A1:D1' MERGE_ALL"
```
合并类型：`MERGE_ALL`（全部合并）、`MERGE_ROWS`（按行合并）、`MERGE_COLUMNS`（按列合并）

### 拆分
```bash
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh unmerge TOKEN 'sheetId!A1:D1'"
```

---

## 📄 工作表操作

```bash
# 添加工作表
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh add_sheet TOKEN '工作表名称'"

# 删除工作表
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh delete_sheet TOKEN sheetId"

# 复制工作表
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh copy_sheet TOKEN sourceSheetId '副本名称'"
```

---

## ↕️ 行列操作

```bash
# 末尾加 10 行
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh add_rows TOKEN sheetId 10"

# 末尾加 5 列
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh add_cols TOKEN sheetId 5"

# 在第3行前插入到第5行（0-indexed）
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh insert_rows TOKEN sheetId 3 5"

# 删除第3到第5行
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh delete_rows TOKEN sheetId 3 5"

# 删除第2到第4列
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh delete_cols TOKEN sheetId 2 4"
```

---

## 🔍 查找替换

```bash
# 查找
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh find TOKEN sheetId '关键词'"

# 替换
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh replace TOKEN sheetId '旧文本' '新文本'"
```

---

## 常见流程示例

### 创建带格式的报表
```bash
# 1. 创建表格
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh create '月度报表'"
# → 得到 spreadsheet_token

# 2. 获取 sheet_id
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh meta TOKEN"
# → 得到 sheet_id

# 3. 写入表头
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh write TOKEN 'sheetId!A1:D1' '[[\"项目\",\"负责人\",\"进度\",\"备注\"]]'"

# 4. 设置表头样式（加粗+蓝底白字）
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh style TOKEN 'sheetId!A1:D1' '{\"bold\":true,\"backColor\":\"#4472C4\",\"foreColor\":\"#FFFFFF\",\"fontSize\":13}'"

# 5. 写入数据
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh write TOKEN 'sheetId!A2:D4' '[[\"功能A\",\"张三\",\"80%\",\"进行中\"],[\"功能B\",\"李四\",\"100%\",\"已完成\"],[\"功能C\",\"王五\",\"30%\",\"延期\"]]'"

# 6. 插入图片
exec command="~/.openclaw/skills/feishu-sheet/scripts/feishu-sheet.sh float_image_url TOKEN sheetId 'https://example.com/chart.png' 'sheetId!F1:F1' 500 300"
```

## 注意事项

- **Range 格式**：必须带 `sheetId` 前缀，用 `meta` 命令获取
- **单元格图片**：`insert_image` 的 range 必须是单个单元格（如 `A1:A1`）
- **浮动图片**：支持本地文件和 URL，会自动上传到飞书
- **values 格式**：JSON 二维数组，注意 shell 中引号转义
- **权限**：表格需要对机器人开放编辑权限，或由机器人创建
- **凭证**：自动从 `~/.openclaw/openclaw.json` 的 `channels.feishu` 读取，无需手动配置
