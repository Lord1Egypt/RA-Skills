# 飞书文件批量发送技能 (feishu-send-files)

飞书多维表格文件批量发送统一入口，支持机器人触发和命令行调用。

## ✨ 功能特性

- **两种方式触发**：机器人对话或命令行直接调用
- **自动配置**：首次使用自动创建本地配置文件
- **多 Agent 支持**：每个 workspace 独立配置，互不干扰
- **隐私保护**：不含任何硬编码的用户 ID 或敏感信息
- **灵活发送**：支持发送任意路径的文件到飞书聊天
- **批量发送**：支持一次发送多个文件（机器人和命令行都支持）

## 📦 安装

### 方式 1：通过 ClawHub 安装（推荐）

```bash
# 搜索技能
clawhub search "feishu-send-files"

# 安装技能
clawhub install feishu-send-files

# 重启 OpenClaw 会话，技能即可使用
```

### 方式 2：手动安装

```bash
# 将本目录复制到 OpenClaw workspace 的 skills 目录
cp -r feishu-send-files ~/.openclaw/workspace/skills/

# 或者克隆到任意位置，然后在 openclaw.json 中添加
```

### 方式 3：Git 克隆

```bash
git clone <repo-url> ~/.openclaw/workspace/skills/feishu-send-files
```

**安装后**：
- 重启 OpenClaw 会话（`/reset` 或重新连接）
- 技能会自动加载，无需额外配置
- 首次运行会自动创建配置文件

## 🔧 配置

### 方式 1：自动配置（推荐）

首次运行脚本时，会自动从全局配置读取并创建 `config.json`：

```bash
node index.js --file "/path/to/file"
```

### 方式 2：手动配置

在 `workspace/config.json` 中配置默认接收者：

```json
{
  "defaultRecipient": {
    "type": "open_id",
    "id": "ou_xxxxxxxxxxxxxxxxxxxxxxxx",
    "note": "可选备注"
  }
}
```

### 方式 3：命令行参数

临时指定接收者：

```bash
node index.js --file "/path/to/file" --to "ou_xxx"
```

## 📖 使用方法

### 机器人模式

在飞书中@机器人并发送文件路径或关键词：

```
@小助理 发送 /home/user/document.pdf 给我
@小助理 发送 PPT 文件
```

**批量发送（多文件选择）**：
```
@小助理 发送 PPT 文件
# 机器人找到多个文件后，回复：1,2,3 或 all
```

### 命令行模式

```bash
# 发送单个文件
node index.js --file "/path/to/file"

# 批量发送多个文件（多个 --file 参数）
node index.js --file "/path1" --file "/path2" --file "/path3"

# 批量发送（逗号分隔）
node index.js --files "/path1,/path2,/path3"

# 搜索文件（按关键词）
node index.js --search "PPT"

# 发送到指定用户
node index.js --file "/path/to/file" --to "ou_xxx"
```

## 🔒 隐私安全

- ✅ **无硬编码 ID**：所有用户 ID 从配置读取
- ✅ **自动创建配置**：首次使用自动生成本地配置
- ✅ **多 Agent 隔离**：每个 workspace 独立配置
- ✅ **配置文件可忽略**：`.gitignore` 已包含配置文件

## 📝 文件结构

```
feishu-send-files/
├── index.js          # 主脚本
├── config.json       # 本地配置（自动生成，需忽略）
├── config.example.json  # 配置示例
├── logs/             # 日志目录（运行时生成，需忽略）
│   └── send-YYYY-MM-DD.log
├── .gitignore        # Git 忽略规则
├── README.md         # 本文件
├── SKILL.md          # 技能说明
├── skill.json        # 技能触发配置
└── package.json      # 依赖配置（可选）
```

**⚠️ 重要**：
- `config.json` 和 `logs/` 目录已被 `.gitignore` 忽略，**不要提交到 Git**
- 使用 `config.example.json` 作为配置模板

## 🛠️ 依赖

**无外部依赖！** 只使用 Node.js 内置模块：
- `fs` - 文件系统
- `https` - HTTPS 请求
- `path` - 路径处理
- `os` - 操作系统信息

**不需要 `npm install`，直接运行即可！**

**要求**：
- Node.js 14+
- OpenClaw 环境（需配置飞书 App）

## 📄 许可证

MIT License
