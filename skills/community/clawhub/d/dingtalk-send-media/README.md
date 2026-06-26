# 钉钉媒体文件发送技能 (dingtalk-send-media)

发送钉钉媒体文件（图片/语音/视频/文件）给用户。支持从环境变量或 OpenClaw 配置自动检测账号，跨平台支持。

> 背景：我在使用openclaw和钉钉的官方连接器，但是他们不支持这些功能（最新版本0.8.13）。
>
> 这是我的issue： https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/issues/456
>
> [于是有了这个玩具。](https://clawhub.ai/shyzhen/dingtalk-send-media)

---

## 🚀 快速开始

### 1. 配置钉钉凭证

**方式 1：编辑 `~/.openclaw/.env` 文件（推荐，优先级最高）**

OpenClaw 会在启动时自动加载此文件中的环境变量。

```bash
# ~/.openclaw/.env
DINGTALK_CLIENTID=dingxxxxxx
DINGTALK_CLIENTSECRET=your_secret
DINGTALK_ROBOTCODE=dingxxxxxx  # 可选，默认同 clientId
```

**方式 2：编辑 `~/.openclaw/openclaw.json` 配置文件**

```json5
{
  "channels": {
    "dingtalk-connector": {
      "accounts": {
        "prd_bot": {
          "clientId": "dingxxxxxx",
          "clientSecret": "your_secret",
          "robotCode": "dingxxxxxx"
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "dingtalk-connector",
        "accountId": "prd_bot"
      }
    }
  ]
}
```

**方式 3：配置文件 + 环境变量占位符**

```json5
{
  "channels": {
    "dingtalk": {
      "accounts": {
        "prd_bot": {
          "clientId": "${DINGTALK_CLIENTID}",
          "clientSecret": "${DINGTALK_CLIENTSECRET}"
        }
      }
    }
  }
}
```

**获取凭证：**
1. 登录 [钉钉开放平台](https://open.dingtalk.com/)
2. 进入「应用开发」→「企业内部开发」
3. 创建或选择已有应用
4. 在「应用详情」页面获取 `AppKey` (ClientId) 和 `AppSecret` (ClientSecret)

**注意：** 修改 `.env` 文件后需要重启 OpenClaw Gateway 才能生效。

---

### 2. 配置优先级

| 方式 | 优先级 | 适用场景 |
|------|--------|----------|
| 环境变量 `DINGTALK_*` | ⭐⭐⭐ 最高 | 临时切换、CI/CD、Docker |
| 配置文件 `${VAR}` 占位符 | ⭐⭐ 中 | 统一配置管理 |
| 配置文件显式值 | ⭐ 低 | 固定配置 |

**说明：** 环境变量优先级最高，设置后会覆盖配置文件中的值。

---

### 3. 申请应用权限

在钉钉开放平台「权限管理」中申请以下权限：

| 权限码 | 用途 | 必需 |
|--------|------|------|
| 机器人消息发送相关权限 | 发送消息给用户 | ✅ |
| 媒体文件上传相关权限 | 上传文件/图片/视频 | ✅ |

**申请步骤：**
1. 进入应用管理页面
2. 点击「权限管理」
3. 搜索上述权限码并申请
4. 等待管理员审批通过

---

### 4. 验证配置

重启 OpenClaw Gateway 后，可以通过以下方式验证配置是否生效：

```bash
# 检查环境变量是否加载
openclaw env | Select-String DINGTALK

# 或查看 Gateway 日志
openclaw logs --grep DINGTALK
```

---

## ✨ 核心特性

- ✅ **自动账号检测** - 从环境变量、`OPENCLAW_AGENT_ID`、bindings 或配置文件自动推导钉钉账号
- ✅ **零依赖** - 仅使用 Python 标准库，无需 `curl`/`jq`
- ✅ **跨平台** - Windows/Linux/macOS 通用
- ✅ **多媒体支持** - 自动检测 `image` / `voice` / `video` / `file`
- ✅ **正确的文件名** - 自动传递 `fileName` 参数，避免显示 `#fileName#`

---

## 📖 使用方法

### 方式 1：直接调用脚本（推荐）

```bash
# 进入技能目录
cd ~/.openclaw/skills/dingtalk-send-media

# 发送文件（自动检测账号）
python scripts/send_media.py <文件路径> <目标 ID>

# 发送文件（指定账号）
python scripts/send_media.py <文件路径> <目标 ID> [账号 ID] [媒体类型] [--group|--user] [--debug]
```

**参数说明：**
- `文件路径`: 本地文件的绝对路径
- `目标 ID`: 钉钉用户 ID（如 `300523656829570034`）或群 ID（以 `cid` 开头）
- `账号 ID`: OpenClaw 配置中的钉钉账号 ID（可选，默认自动检测）
- `媒体类型`: `image` / `voice` / `video` / `file`（可选，默认自动检测）
- `--group` / `--user`: 显式指定按群聊或单聊发送；默认会把 `cid...` 自动识别为群聊
- `--debug`: 输出账号检测和目标类型判断过程

### 方式 2：在对话中使用

告诉模型你要发送的文件，模型会自动调用脚本。

**示例：**
```bash
# 自动检测账号，发送文件
python scripts/send_media.py "C:/path/to/file.pdf" "300523656829570034"

# 指定账号发送
python scripts/send_media.py "C:/path/to/image.png" "300523656829570034" prd_bot

# 指定媒体类型
python scripts/send_media.py "C:/path/photo.jpg" "300523656829570034" prd_bot image

# 发送到群聊
python scripts/send_media.py "C:/path/to/meeting.mp4" "cidxxxxxxxx" dev_bot video

# 显式指定按群聊发送
python scripts/send_media.py "C:/path/to/meeting.mp4" "some_target_id" dev_bot video --group
```

---

## 🎯 典型场景

### 场景 1：发送报告文件

**用户**: "把昨天的销售报告发给我"

**模型**:
```bash
python scripts/send_media.py "C:/path/to/reports/sales_report_2026-04-06.pdf" "300523656829570034"
```

### 场景 2：发送截图

**用户**: "把这个错误的截图发给我看看"

**模型**:
```bash
python scripts/send_media.py "C:/path/to/screenshots/error_2026-04-07.png" "300523656829570034"
```

### 场景 3：发送到群聊

**用户**: "把会议纪要发到项目群"

**模型**:
```bash
python scripts/send_media.py "C:/path/to/meeting_notes.docx" "cidxxxxxxxx" prd_bot file
```

### 场景 4：发送语音/视频

**用户**: "把这个录音发给客户"

**模型**:
```bash
python scripts/send_media.py "C:/path/to/recording.mp3" "300523656829570034" prd_bot voice
```

---

## ⚠️ 注意事项

### 文件大小限制

| 类型 | 最大大小 |
|------|---------|
| 文件 | 20MB |
| 图片 | 10MB |
| 语音 | 2MB |
| 视频 | 20MB |

### 支持的文件格式

- **文件**：PDF, DOCX, XLSX, PPTX, TXT, ZIP 等
- **图片**：JPG, PNG, GIF, BMP, WEBP
- **语音**：MP3, WAV, AMR
- **视频**：MP4, AVI, MOV, WMV

### 目标 ID 格式

- **用户 ID**: 钉钉用户 ID（如 `300523656829570034`）
- **群 ID**: 以 `cid` 开头（如 `cidxxxxxxxx`）
- **自动检测规则**: 目标 ID 以 `cid` 开头时，脚本默认按群聊发送；否则默认按单聊发送

---

## 🐛 故障排除

### 问题 1: 找不到配置文件

```
错误：未找到 OpenClaw 配置文件 openclaw.json
```

**解决**: 
- 确认 `~/.openclaw/openclaw.json` 存在
- 或直接设置 `DINGTALK_CLIENTID` 和 `DINGTALK_CLIENTSECRET` 环境变量

### 问题 2: 获取 access token 失败

```
错误：获取 access token 失败：...
```

**解决**: 
- 检查 `clientId` 和 `clientSecret` 是否正确
- 确认钉钉应用已发布

### 问题 3: 上传文件失败

```
错误：上传媒体文件失败：...
```

**解决**: 
- 确认文件路径正确且文件存在
- 确认文件大小不超过限制
- 确认钉钉应用有媒体上传权限

### 问题 4: 发送消息失败

```
错误：发送消息失败：...
```

**解决**:
- 确认目标用户 ID 或群 ID 正确
- 确认机器人已添加到群聊（群聊场景）
- 确认 `robotCode` 配置正确

### 问题 5: 账号检测错误

```
错误：未找到钉钉账号配置：xxx
```

**解决**:
- 检查 `~/.openclaw/.env` 中是否设置了 `DINGTALK_CLIENTID` 和 `DINGTALK_CLIENTSECRET`
- 检查 `openclaw.json` 中的 `channels.dingtalk.accounts` 配置
- 检查 `openclaw.json` 中的 `channels.dingtalk-connector.accounts` 配置
- 检查 `bindings` 中的 `agentId → accountId` 映射
- 或在命令行显式指定账号 ID 参数

---

## 📊 与 dingtalk-file-send 对比

| 特性 | dingtalk-send-media | dingtalk-file-send |
|------|---------------------|-------------------|
| 实现语言 | Python | Bash |
| 外部依赖 | 无 | `curl`, `jq` |
| Windows 兼容 | ✅ 原生支持 | ❌ 需要 Git Bash/WSL |
| 自动账号检测 | ✅ 支持 | ✅ 支持 |
| 多媒体类型 | image/voice/video/file | 仅 file |
| OpenClaw 元数据 | ✅ 支持 | ✅ 支持 |

---

## 🔧 调试模式

使用 `--debug` 或 `-d` 参数查看账号检测过程：

```bash
python scripts/send_media.py "file.pdf" "user_id" --debug
```

输出示例：
```
[DEBUG] OPENCLAW_AGENT_ID=main
[DEBUG] OPENCLAW_ACCOUNT_ID=未设置
[DEBUG] 账号检测来源：binding:main→prd_bot
```

在 Linux 或 macOS 上，如果系统没有 `python` 命令，请改用：

```bash
python3 scripts/send_media.py "/path/to/file.pdf" "300523656829570034"
```

---

**最后更新：** 2026-04-10  
**版本：** 1.0  
**作者：** Ash
