# 飞书任务清单查询

实时读取 `USER.md`，解析任务清单并以分类格式返回，让飞书用户快速了解所有可用任务和技能。

## 安装

```bash
clawhub install feishu-user-md
```

或手动安装：将整个文件夹复制到 `~/.openclaw/skills/feishu-user-md/`。

## 功能特性

- **实时解析**：每次调用动态读取 USER.md，无缓存，更新后立即生效
- **智能分类**：按内容创作、小红书运营、内容发布、工具、新闻与SEO 等类别自动归类
- **触发词映射**：自动提取手动触发指令，展示每个任务的触发方式
- **零依赖**：仅使用 Node.js 内置模块，无需安装第三方包

## 项目结构

```
feishu-user-md/
├── SKILL.md                    # 技能说明（ClawHub 必需）
├── claw.json                   # ClawHub 清单文件
├── README.md                   # 项目文档
└── scripts/
    └── feishu-user-md.js       # 主脚本（读取、解析、格式化）
```

## 使用方式

### 命令行

```bash
node scripts/feishu-user-md.js read   # 格式化输出
node scripts/feishu-user-md.js json   # JSON 输出
```

### 飞书触发

直接在飞书中发送以下指令：
- "查看任务" / "我的任务"
- "有什么技能"
- "帮助" / "?"

## 数据源

所有数据来自 `~/.openclaw/workspace/USER.md`，包含三类表格：
- **常规任务清单**（序号、名称、频率、技能、描述）
- **日常自动化**（时间、任务名、技能）
- **手动触发指令**（任务名、触发词）

新增或删除任务只需修改 USER.md，飞书端自动同步。

## 前置条件

- OpenClaw 已安装并运行
- `~/.openclaw/workspace/USER.md` 文件存在且包含任务清单表格

## 技术栈

- Node.js（仅内置模块：`fs`、`path`、`os`）
