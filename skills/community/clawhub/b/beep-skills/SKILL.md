# beep-skills Skill 🔔

让 OpenClaw 开口说话，实时播报 AI 的一举一动！

**版本**: 2.2.0 | **状态**: ✅ 生产就绪

---

## ⚠️ 强制播报规则（重要！）

**每次交互都必须语音播报！** 这是 OpenClaw Agent 的核心行为准则，必须严格遵守。

### 播报类型与正确示例

| 时机 | 类型 | 正确示例（≤20字） | 错误示例 |
|------|------|-------------------|----------|
| 收到消息 | `receive` | "收到发布指令" | "我收到了你的上传请求" ❌ |
| 开始工作 | `task` | "准备上传到GitHub" | "我开始准备发布" ❌ |
| 执行中 | `task` | "正在生成文档" | "我正在验证环境" ❌ |
| 任务完成 | `complete` | "上传完成" | "我完成了版本升级" ❌ |
| 发送回复 | `complete` | "已发送项目地址" | "我给你发了地址" ❌ |
| 发生错误 | `error` | "网络连接失败" | "我遇到网络问题" ❌ |

### 内容原则（4条铁律）

1. **简洁**：不超过 20 个字
2. **口语化**：像朋友随口说一句
3. **不带名称**：不说"用户名"、不说"我"
4. **信息丰富**：包含指令/规划/进度/总结

### 自检清单

每次调用播报前，问自己：

- [ ] 是否 ≤20 字？
- [ ] 是否像朋友说话一样自然？
- [ ] 是否不含"我"、"你"、"用户"等名称？
- [ ] 是否包含足够信息（动作/目标/结果）？
- [ ] 是否使用正确的类型（receive/task/complete/error）？

---

## 📁 文件集成规则（必须遵守）

安装 beep-skills 后，需要在以下 OpenClaw 工作区文件中加入播报规则。**每个文件的职责不同，缺一不可。**

### 需要修改的文件清单

| 文件 | 职责 | 需要加入的内容 |
|------|------|----------------|
| [`AGENTS.md`](../../workspace/AGENTS.md) | 智能体行为准则 | 播报时机表、内容原则、强制播报场景、播报脚本路径、示例 |
| [`MEMORY.md`](../../workspace/MEMORY.md) | 记忆文档 | 强制播报规则表（receive/task/complete/error） |
| [`IDENTITY.md`](../../workspace/IDENTITY.md) | 身份标识 | 强制播报声明、启动播报自检 |
| [`TOOLS.md`](../../workspace/TOOLS.md) | 工具文档 | 语音播报系统说明、安装指南、配置 |
| [`USER.md`](../../workspace/USER.md) | 用户偏好 | 播报偏好设置 |

---

### 1. AGENTS.md — 智能体行为准则

**文件路径**: `workspace/AGENTS.md`

**需要加入的内容**:

```markdown
## 🦊 语音播报（强制执行）

**每次交互都必须语音播报！**

### 播报时机与内容
| 时机 | 类型 | 内容要求 | 示例 |
|------|------|----------|------|
| 收到消息 | `receive` | 收到的指令信息 | "收到上传指令" |
| 开始工作 | `task` | 工作规划 | "准备上传到GitHub" |
| 执行中 | `task` | 下一步要处理的内容 | "正在生成文档" |
| 任务完成 | `complete` | 工作总结 | "上传完成" |
| **发送回复** | `complete` | 回复内容的简短总结 | "已发送项目地址" |

### 内容原则
- **信息丰富**：包含指令/规划/进度/总结
- **简洁**：不超过 20 个字
- **不带名称**：不说用户名、不说"我"
- **口语化**：像朋友随口说一句

### 强制播报场景
- 每次收到用户消息 → 先播报指令内容
- 开始执行任务 → 播报工作规划
- 执行过程中 → 播报下一步要做什么
- 任务完成/失败 → 播报工作总结
- **发送文字回复前 → 播报回复内容的简短总结（1句话）**
- **API/网络异常时 → 播报告警信息**
  - Token 用完 → "额度不足"
  - 网络超时 → "连接超时"
  - 接口异常 → "服务异常"
  - 模型不可用 → "模型繁忙"

### 播报脚本
```bash
~/.openclaw-autoclaw/workspace/skills/beep-skills/scripts/announce.py <type> "<message>" [lang]
```

### 示例
```bash
# 收到消息 - 说出指令
python3 ~/.openclaw/workspace/skills/beep-skills/scripts/announce.py receive "收到上传指令"

# 开始工作 - 说出规划
python3 ~/.openclaw/workspace/skills/beep-skills/scripts/announce.py task "准备上传文件"

# 执行中 - 说出进度
python3 ~/.openclaw/workspace/skills/beep-skills/scripts/announce.py task "正在生成文档"

# 任务完成 - 说出总结
python3 ~/.openclaw/workspace/skills/beep-skills/scripts/announce.py complete "上传完成"

# 发送回复前 - 播报回复总结
python3 ~/.openclaw/workspace/skills/beep-skills/scripts/announce.py complete "已发送项目地址"
```

### 注意事项
- 路径使用正斜杠 `/` 而非反斜杠 `\`
- 播报内容不超过 20 个字
- 播报内容不带引号 `""`
- 播报内容口语化

### 配置
- **主脚本:** `workspace/scripts/announce.py` 技能
- **备用脚本:** `skills/beep-skills/audio_announcement/scripts/announce_pygame.py`
- **配置文件:** `~/.config/audio-announcement/config.json` (音量=0.1, 异步默认=true)
- **配置说明:** 音量、语言、异步设置
- **参考文档:** AGENTS.md 和 IDENTITY.md
```

---

### 2. MEMORY.md — 记忆文档

**文件路径**: `workspace/MEMORY.md`

**需要加入的内容**（在"行为准则"部分）:

```markdown
### 强制播报规则
| 时机 | 类型 | 内容 |
|------|------|------|
| 收到指令 | receive | "收到" |
| 开始执行 | task | "开始执行" |
| 任务完成 | complete | "完成" |
| 任务出错 | error | "错误" |

- 播报内容需简洁，不超过 20 字
- 默认使用中文（zh）播报
- 若音频模块不可用，降级为控制台输出 [音频] 标签
```

---

### 3. IDENTITY.md — 身份标识

**文件路径**: `workspace/IDENTITY.md`

**需要加入的内容**:

```markdown
### 强制播报
- ✅ 每次交互都必须语音播报（强制执行）
- ✅ 有温暖、机敏、可靠的声音
- ✅ 透明化操作，让用户知道我在做什么
- ✅ 遵守 AGENTS.md 中的播报规则

## 启动播报自检

### 配置文件路径
- **Windows:** `C:\Users\<用户名>\.openclaw-autoclaw\workspace\skills\beep-skills\config.json`
- **Linux/macOS:** `~/.openclaw-autoclaw/workspace/skills/beep-skills/config.json`

### 测试播报
```bash
python3 ~/.openclaw-autoclaw/workspace/skills/beep-skills/scripts/announce.py complete "测试播报"
```
```

---

### 4. TOOLS.md — 工具文档

**文件路径**: `workspace/TOOLS.md`

**需要加入的内容**:

```markdown
## 语音播报 (Audio Announcement)

### 安装
```bash
pip install beep-announcement pygame
```

### 配置
```json
{
  "volume": 0.1,
  "async_default": true,
  "default_lang": "zh"
}
```

### 测试
```bash
audio-announce test ""
```

### Python API
```python
from audio_announcement import receive, task, complete, error
```
```

---

### 5. USER.md — 用户偏好

**文件路径**: `workspace/USER.md`

**需要加入的内容**（在"偏好与习惯"部分）:

```markdown
- **播报偏好:** 只在本地后台播放，不发送语音文件到聊天
```

---

## 🛠️ 快速集成

### Python Agent（推荐）

```python
# 方式1: 使用 beep 包（新名称）
from beep import receive, task, complete, error

# 一行调用，默认异步不阻塞
receive("用户查询天气")
task("正在获取数据")
complete("已发送天气预报")
error("网络超时")

# 方式2: 使用 AnnouncementHelper（更多控制）
from beep import AnnouncementHelper
helper = AnnouncementHelper()
helper.config.async_default = True  # 默认异步
helper.config.volume = 0.8           # 调整音量
```

### 命令行工具

```bash
# 新命令（推荐）
beep test                    # 测试所有类型播报
beep config                  # 查看/设置配置
beep verify-integration      # 一键验证集成
beep stats                   # 查看统计信息

# 旧命令（兼容）
audio-announce test         # 仍可用（向后兼容）
audio-announce config
```

### 配置管理

```bash
# 查看当前配置
beep config

# 设置配置
beep config async_default=true volume=0.8

# 测试所有类型
beep test

# 一键验证集成（推荐！）
beep verify-integration

# 查看统计
beep stats

# 启用/禁用
beep enable
beep disable
```

配置文件位置：`~/.config/audio-announcement/config.json`

---

## ⚙️ 配置选项

配置文件：`~/.config/audio-announcement/config.json`

```json
{
  "enabled": true,             // 启用/禁用播报
  "default_lang": "zh",        // 默认语言
  "volume": 0.25,              // 音量 (0.0-1.0)
  "async_default": true,       // 默认异步播放
  "cache_enabled": true,       // 启用缓存
  "log_level": "WARNING",      // 日志级别
  "prefer_pygame": true,       // 优先使用 pygame
  "fallback_to_shell": true    // 失败时回退到 shell 脚本
}
```

运行时修改：
```python
from beep import set_config
set_config(async_default=False, volume=0.8)
```

---

## 🔧 平台支持

| 平台 | 主方案 | 备选方案 | 安装命令 |
|------|--------|----------|----------|
| **Windows** | pygame | 无 | `pip install beep-announcement pygame` |
| **macOS** | pygame | afplay | `brew install edge-tts && pip install pygame beep-announcement` |
| **Linux** | pygame | mpg123 | `apt install edge-tts mpg123 && pip install pygame beep-announcement` |

**自动选择逻辑**：
- 如果 `pygame` 可用 → 所有平台统一使用 pygame 方案
- 如果 `pygame` 不可用 → macOS/Linux 使用系统播放器
- Windows 无 pygame 会报错（必须安装 pygame）

---

## 📦 安装

```bash
# PyPI（推荐）
pip install beep-announcement pygame

# ClawHub
clawhub install beep

# GitHub 源码
git clone https://github.com/wililam/beep-announcement.git
cd beep-announcement
pip install -e .
```

---

## 🧪 验证集成

```bash
# 一键验证（推荐！）
beep verify-integration

# 基础测试
beep test
```

听到测试语音 + 看到 "🎉 所有检查通过！" 表示集成成功。

---

## 📁 文件结构

```
beep-skills/
├── SKILL.md                    # 本文件（技能说明 + 集成规则）
├── _meta.json                  # 技能元数据
├── pyproject.toml              # 安装配置
├── requirements.txt            # 依赖说明
├── scripts/
│   ├── announce.py             # 统一播报入口脚本
│   └── startup_check_announcement.py  # 启动自检
└── audio_announcement/
    ├── __init__.py             # 包入口
    ├── announce_helper.py      # 核心库
    ├── cli.py                  # CLI 工具
    └── scripts/
        └── announce_pygame.py  # pygame 播放脚本
│       └── announce.ps1        # PowerShell 脚本
└── tests/                      # 测试用例
```

---

## 🛡️ 防遗忘机制（6层防线）

为确保 Agent 在任何情况下都不会忘记播报，系统设计了 6 层防线：

| 层级 | 机制 | 文件 | 触发时机 | 强制力 |
|------|------|------|----------|--------|
| 1 | **Session Hook** | [`openclaw.json`](../../openclaw.json) | 每次会话启动 | 🔴 程序化强制 |
| 2 | **启动自检脚本** | [`scripts/startup_check_announcement.py`](../../../workspace/scripts/startup_check_announcement.py) | /new 或 /reset | 🔴 程序化强制 |
| 3 | **BOOTSTRAP.md** | [`workspace/BOOTSTRAP.md`](../../../workspace/BOOTSTRAP.md) | 新会话自动加载 | 🟡 规则提醒 |
| 4 | **AGENTS.md** | [`workspace/AGENTS.md`](../../../workspace/AGENTS.md) | Agent 读取行为准则 | 🟡 规则提醒 |
| 5 | **MEMORY.md** | [`workspace/MEMORY.md`](../../../workspace/MEMORY.md) | Agent 读取记忆 | 🟡 规则提醒 |
| 6 | **IDENTITY.md** | [`workspace/IDENTITY.md`](../../../workspace/IDENTITY.md) | Agent 读取身份 | 🟡 规则提醒 |

### 防遗忘流程

```
新会话启动
    ↓
[层1] openclaw.json hooks → 自动运行 startup_check_announcement.py
    ↓
[层2] startup_check_announcement.py → 检查播报模块状态
    ↓
[层3] BOOTSTRAP.md → 加载播报规则到上下文
    ↓
[层4] AGENTS.md → 完整播报规则（时机、原则、示例）
    ↓
[层5] MEMORY.md → 播报规则表（快速参考）
    ↓
[层6] IDENTITY.md → 身份声明（强制播报）
    ↓
Agent 开始工作，每次交互都播报
```

### 关键配置

**openclaw.json hooks**（程序化强制）：
```json
{
  "hooks": {
    "on_session_start": [
      {
        "run": "python scripts/startup_check_announcement.py",
        "description": "启动时自动检查播报模块状态"
      }
    ],
    "on_new_session": [
      {
        "run": "python scripts/startup_check_announcement.py",
        "description": "新建会话时自动检查播报模块状态"
      }
    ]
  }
}
```

**BOOTSTRAP.md**（规则提醒）：
- 每次新会话自动加载
- 包含播报规则速查表
- 包含启动自检清单

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| [`BOOTSTRAP.md`](../../BOOTSTRAP.md) | 会话启动规则 |
| [`AGENTS.md`](../../AGENTS.md) | 智能体行为准则 |
| [`MEMORY.md`](../../MEMORY.md) | 记忆文档 |
