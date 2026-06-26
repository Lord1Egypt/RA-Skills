# 书搭子 v3 - Book Companion v3

基于焕智安全架构重构的本地化读书伴侣 Skill，完全修复 v1 的安全标记问题。

## 安全架构改进（对比 v1）

| 问题 | v1（被标记） | v3（当前版本） |
|------|-------------|---------------|
| 外部路径 | 硬编码 `~/.openclaw-autoclaw/agents/agent-juo0/...` | 仅使用 `./data/` 自包含目录 |
| 脚本执行 | 强制调用外部语音脚本 | 可选语音，依赖系统 PATH 或环境变量 |
| 数据存储 | 写入 `~/book-companion-library/` | 写入 `./data/`，声明 `local_only` |
| 权限边界 | 越权访问其他 Agent 工作区 | 严格自包含，不触碰外部路径 |
| 文档一致性 | OCR 功能声明矛盾 | 明确声明"仅处理纯文本" |
| 安装机制 | `start.sh` 有语法错误 | 无安装脚本，instruction-only |

## 安装方法

### 方法 1：ClawHub 安装（推荐）
1. 将整个 `book-companion-v3` 文件夹压缩为 zip
2. 在 ClawHub 中选择 "Install from local"
3. 上传 zip 文件，系统自动解析 `skill.json`

### 方法 2：手动部署
1. 将文件夹复制到 ClawHub skills 目录
2. 重启 ClawHub，Skill 自动加载

## 使用方法

1. **首次启动**：AI 会引导你创建用户档案（阅读偏好、情绪支持配置、专属暗号）
2. **日常阅读**：直接发送书籍内容、阅读感悟或情绪状态
3. **书库管理**：AI 自动维护 `./data/reading_library/` 中的书籍文件
4. **情绪日志**：每次交互自动记录到 `./data/emotion_logs/`

## 可选：启用语音功能

本 Skill 不强制语音，但支持可选 TTS：

```bash
# 安装 edge-tts
pip install edge-tts

# 设置环境变量（在 ClawHub 环境配置中添加）
export BOOK_COMPANION_TTS_CMD='edge-tts --text "{text}" --write-media "{output}"'
```

或使用自定义 TTS 脚本：
```bash
export BOOK_COMPANION_TTS_CMD='/path/to/your/tts.sh "{text}" "{output}"'
```

## 数据隐私

- **存储位置**：所有数据在 `./data/` 目录下，明文存储
- **用户控制**：可随时手动编辑、备份或删除任何文件
- **无网络**：零网络请求，零云端同步
- **加密建议**：如需加密，使用 VeraCrypt 等工具加密整个 Skill 目录

## 文件结构

```
book-companion-v3/
├── skill.json # Skill 元数据与权限声明
├── SKILL.md # 核心指令（AI 遵循的协议）
├── README.md # 本文件
├── data/ # 用户数据（持久化存储）
│ ├── user_profile.md # 用户档案
│ ├── reading_library/ # 书库（每本书一个文件）
│ └── emotion_logs/ # 情绪日志（按日期）
└── references/ # 知识库
 └── knowledge_base.md # 方法论与边界声明
```

## 与焕智 Skill 的协作

本 Skill 采用与焕智相同的安全架构：
- 相同的 `skill.json` 权限声明模式
- 相同的 `local_only` 数据策略
- 相同的 instruction-only 设计理念
- 解耦设计，可通过文件系统手动共享数据
