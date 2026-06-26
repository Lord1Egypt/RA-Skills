# Feishu Log - 飞书工作日志技能

自动将工作内容整理并记录到飞书文档的工具。

## 📁 文件夹结构

```
RS 工作日志/
├── 2026 年/
│   ├── 03 月/
│   │   ├── 12 日/
│   │   │   └── 工作日志 -2026-03-12.docx
```

## ✨ 功能特点

- ✅ 自动创建 `年/月/日` 文件夹结构
- ✅ 智能复用已有文件夹（不重复创建）
- ✅ 自动整理日志内容（分段落、分要点）
- ✅ 生成结构化文档（标题、时间、分段）
- ✅ 支持 Markdown 格式（标题、列表、代码块等）
- ✅ 命令行工具和 API 两种使用方式
- ✅ **写入前确认机制**（防止误写，可预览内容）

## 🚀 使用方法

### 方式 1：作为 OpenClaw 技能

```
使用 feishu-log 技能记录日志：

## 今日工作
- 完成了项目 A 的开发
- 修复了 3 个 bug
- 参加了需求评审会议

## 明日计划
- 继续完善项目 A
- 准备技术分享
```

### 方式 2：命令行工具

```bash
cd /Users/one/.openclaw/workspace/skills/feishu-log

# 记录今天
node log.js "今天完成了项目 A 的开发"

# 指定日期
node log.js --date 2026-03-10 "昨天的工作内容"

# 多行内容
node log.js "
## 今日完成
- 任务 1
- 任务 2

## 遇到的问题
- 问题描述
"
```

### 方式 3：直接调用 API

```javascript
import { logWork } from './log-work.mjs';

await logWork(`
## 工作内容
- 任务 1
- 任务 2
`, new Date(), 'RdVIffbJxl8HDCdJiULcIpdgnzf');
```

## 📝 文档格式

生成的文档格式：

```
# 工作日志 - 2026-03-12

记录时间：2026/3/12 18:31:56

---

## 工作内容
- 项目 1
- 项目 2

## 技术细节
- 细节 1
- 细节 2

---

*本日志由 AI 助手自动生成*
```

## 🛠️ 配置

### 方式 1：使用配置工具（推荐）

```bash
cd /Users/one/.openclaw/workspace/skills/feishu-log
node config-credentials.js
```

按提示输入飞书 App ID、App Secret 和 Folder Token。

### 方式 2：手动创建配置文件

创建 `~/.openclaw/feishu-credentials.json`：

```json
{
  "app_id": "cli_xxx",
  "app_secret": "xxx",
  "root_folder_token": "xxx"
}
```

### 方式 3：环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_LOG_ROOT_TOKEN="xxx"
```

### 方式 4：直接修改代码（不推荐）

在 `log-work.mjs` 或 `log.js` 中修改配置：

```javascript
const APP_ID = "cli_a93b936aa9391cc7";
const APP_SECRET = "aMRJMyi3KSXbSJhRgyx7ycvyT5D3rsrs";
const ROOT_FOLDER_TOKEN = "RdVIffbJxl8HDCdJiULcIpdgnzf"; // 根目录
```

## 📂 文件说明

```
skills/feishu-log/
├── SKILL.md        # 技能说明（OpenClaw 使用）
├── README.md       # 完整使用文档
├── log-work.mjs    # 完整功能实现（含测试数据）
└── log.js          # 命令行工具
```

## 🔧 技术实现

- 使用飞书开放 API
- `feishu_drive` - 管理文件夹结构
- `feishu_doc` - 创建和写入文档内容
- Markdown 转换 - 通过 `convert` API
- 批量插入 - 通过 `documentBlockDescendant` API

## ⚠️ 注意事项

1. **文件夹权限**：确保应用有根目录的访问权限
2. **API 限流**：大量写入时可能遇到 429，建议添加重试
3. **同名文档**：当前会创建新文档，不会覆盖（可扩展为覆盖模式）
4. **格式兼容**：避免使用复杂的 Markdown 格式（如粗体），使用简单文本

## 📈 后续优化

- [ ] 支持同名文档覆盖/追加模式
- [ ] 添加重试机制处理 API 限流
- [ ] 支持更多格式（表格、图片等）
- [ ] 添加日志检索功能
- [ ] 支持导出为其他格式

## 📊 测试记录

- ✅ 文件夹创建/复用
- ✅ 文档创建
- ✅ 内容写入（标题、列表、代码块）
- ✅ 时间戳格式修复
- ✅ 命令行工具测试

---

*最后更新：2026-03-12*
