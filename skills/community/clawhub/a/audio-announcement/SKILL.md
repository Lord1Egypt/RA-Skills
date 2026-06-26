# Audio Announcement Skill 🦊

让 OpenClaw 开口说话，实时播报 AI 的一举一动！

## 概述

这是一个语音播报技能，可以让你的 AI 代理通过语音实时告诉你它在做什么。就像一只爱说话的龙虾，让你更清楚、更安心地知道 AI 的当前状态。

**版本**: 2.0.8  
**状态**: ✅ 生产就绪  
**安装**: `clawhub install audio-announcement` 或 `pip install audio-announcement`

### 🎯 最新更新 (v2.0.8 - 2026-04-05)
- ✅ **播报本地化** - 所有播报仅在本机后台播放，不发送语音文件到聊天界面
- ✅ **统一包装脚本** - 新增 `scripts/announce.py`，自动解析 skill 路径，避免硬编码
- ✅ **默认音量优化** - 配置文件默认 `volume: 0.1`（10%），保护听力避免打扰
- ✅ **CLI 工具修复** - 修复 pygame 导入问题，提升 Windows 稳定性
- ✅ **文档全面升级** - MEMORY.md / AGENTS.md / TOOLS.md 统一管理播报工作流
- ✅ **会话复盘机制** - 建立复盘流程，持续改进
- ✅ **安全边界强化** - 破坏性操作（关机）必须明确授权

### 🎯 最新更新 (v2.0.7 - 2026-04-05)
- ✅ **高优先级优化完成** - PyPI 打包支持、配置文件系统、异步默认化
- ✅ **PyPI 支持** - 可通过 `pip install audio-announcement` 安装
- ✅ **配置文件** - `~/.config/audio-announcement/config.json`（enabled/lang/volume/async_default）
- ✅ **异步默认** - 默认后台播放，减少对 Agent 响应时间的阻塞
- ✅ **CLI 工具** - `audio-announce` 命令支持测试、配置、统计
- ✅ **集成建议更新** - AGENTS.md 添加最佳实践和示例代码

### 🎯 最新更新 (v2.0.6 - 2026-04-05)
- ✅ **增强防遗忘机制** - 添加验证脚本、集成检查清单
- ✅ **快速集成指南** - 提供 announce_helper.py 简化集成
- ✅ **强制规则模板** - 可直接复制到 AGENTS.md 的完整规则
- ✅ **Windows 高可靠性** - 使用 python -m edge_tts 模块调用，不依赖 PATH

### 🎯 最新更新 (v2.0.5 - 2026-04-05)
- ✅ **修复 PATH 依赖问题** - announce_pygame.py 改用 `python -m edge_tts` 模块调用，不依赖 PATH 环境变量
- ✅ **Windows 高可靠性** - 即使 edge-tts 不在 PATH 也能正常工作
- ✅ **配置状态记录** - AGENTS.md 添加语音播报配置状态追踪

### 🎯 最新更新 (v2.0.4 - 2026-03-28)
- ✅ **强化播报规则** - 5 种播报时机，内容原则，检查清单
- ✅ **集成到核心配置** - AGENTS.md / SOUL.md / USER.md / MEMORY.md
- ✅ **强制执行机制** - 每次交互都必须播报，不能遗漏
- ✅ **内容规范** - ≤20 字，口语化，不带名称

### 🎯 历史更新 (v1.5.0-v1.7.4)
- ✅ **Windows 默认使用 pygame** - `announce.sh` 在 Windows 平台自动调用 `announce_pygame.py`
- ✅ **简化 Windows 使用** - 无需手动选择脚本，统一使用 `announce.sh`
- ✅ **清理无用测试脚本** - 移除 `test-integration.sh` 和备份文件

### 📜 历史更新
- **v1.4.0**: Windows 11 完整支持，新增 `announce_pygame.py`，修复新会话语音、macOS 兼容性、跨平台哈希计算
- **v1.3.0**: 新增 workflow-helper.sh，支持自动包装命令
- **v1.2.0**: 新增离线模式支持
- **v1.1.0**: 支持多语言（9种语言）
- **v1.0.0**: 初始版本，支持 macOS/Linux

### 特性

- 🎯 **透明度**：清楚知道 AI 正在执行什么操作
- 🔒 **安全感**：实时听到操作，不用盯着日志看
- 💬 **人性化**：友好的声音，不是冷冰冰的文字
- ⚡ **效率**：专注你的工作，让 AI 用声音告诉你进度
- 🌍 **9种语言**：中文、英文、日文、韩文、西班牙语、法语、德语等
- 🔄 **队列机制**：消息永不丢失，自动重试
- 🛡️ **防遗忘**：启动自检 + 身份绑定，两重保障
- 🔌 **Session Hook**：自动在 /NEW 和 /RESET 后运行检查

---

## 🛡️ 防遗忘机制（最重要！）

为了防止播报功能在 `/RESET` 或 `/NEW` 后失效，本 skill 实现了**多层防护**：

### 1️⃣ 启动自检（Session Start）

每次 OpenClaw 新会话开始时，自动运行 `scripts/startup_check_announcement.py`：

- ✅ 检查 edge-tts、pygame、配置文件、包安装
- ✅ 自动播放"系统启动"测试语音
- ✅ 如有问题立即输出修复建议

**自动配置方法**（任选其一）：

**Windows PowerShell** (`$PROFILE`)：
```powershell
$checkAudio = "C:\Users\williammiao\.openclaw-autoclaw\skills\audio-announcement\scripts\startup_check_announcement.py"
if (Test-Path $checkAudio) {
    python $checkAudio | Out-Host
}
```

**macOS/Linux** (`~/.bashrc`)：
```bash
python ~/.openclaw-autoclaw/skills/audio-announcement/scripts/startup_check_announcement.py 2>/dev/null || true
```


### 3️⃣ 强制规则（AGENTS.md）

在 `AGENTS.md` 中添加：

```markdown
### 2️⃣ 语音播报强制执行（严禁遗漏）

- 所有 agent 必须显式调用播报脚本
- 禁止仅依赖记忆中的规则而不实际执行
- 每次发送回复前必须完成 `complete` 播报
- 任务开始前必须完成 `task` 播报

📋 自我检查清单：
- [ ] 收到消息时是否播报了 `receive`？
- [ ] 任务开始时是否播报了 `task`？
- [ ] 执行过程中是否播报了关键步骤？
- [ ] 完成任务后是否播报了 `complete`？
- [ ] 遇到异常时是否播报了 `error`？
```

### 4️⃣ 身份绑定（IDENTITY.md）

播报是你的**核心身份特质**，不是可选项。在 `IDENTITY.md` 中记录：

```markdown
## 核心特质
- 每次交互都必须语音播报（强制执行）
- 有温暖、机敏、可靠的声音
- 透明化操作，让用户知道我在做什么

## 启动播报自检
每次 /NEW 或 /RESET 后，自动检查：
- [ ] edge-tts 和 pygame 是否安装
- [ ] 配置文件是否存在
- [ ] 运行 audio-announce test 验证功能
- [ ] 如果失败，立即修复或提醒用户
```

### 5️⃣ 首次设置引导（BOOTSTRAP.md）

在首次对话时，BOOTSTRAP.md 提供完整的播报设置流程，确保从一开始就配置好。

---

## 🎤 语音播报（强制执行）

**每次交互都必须语音播报！**

#### 播报时机与内容
| 时机 | 类型 | 内容要求 | 示例 |
|------|------|----------|------|
| 收到消息 | `receive` | 收到的指令信息 | "收到上传指令" |
| 开始工作 | `task` | 工作规划 | "准备上传到GitHub" |
| 执行中 | `task` | 下一步要处理的内容 | "正在生成文档" |
| 任务完成 | `complete` | 工作总结 | "上传完成" |
| **发送回复** | `complete` | 回复内容的简短总结 | "已发送项目地址" |
| 遇到异常 | `error` | 错误描述 | "网络连接失败" |

#### 内容原则
- **信息丰富**：包含指令/规划/进度/总结
- **简洁**：不超过 20 个字
- **不带名称**：不说用户名、不说"我"
- **口语化**：像朋友随口说一句

---

## 🛠️ 快速集成

### Python Agent（推荐）

```python
# 方式1: 使用 audio_announcement 包
from audio_announcement import receive, task, complete, error

# 一行调用，默认异步不阻塞
receive("用户查询天气")
task("正在获取数据")
complete("已发送天气预报")
error("网络超时")

# 方式2: 使用 AnnouncementHelper（更多控制）
from audio_announcement import AnnouncementHelper
helper = AnnouncementHelper()
helper.config.async_default = True  # 默认异步
helper.config.volume = 0.8           # 调整音量
```

### 配置管理

```bash
# 查看当前配置
audio-announce config

# 设置配置
audio-announce config async_default=true volume=0.8

# 测试所有类型
audio-announce test

# 查看统计
audio-announce stats

# 启用/禁用
audio-announce enable
audio-announce disable
```

配置文件位置：`~/.config/audio-announcement/config.json`

---

## 🔧 平台支持

| 平台 | 主方案 | 备选方案 | 安装命令 |
|------|--------|----------|----------|
| **Windows** | `announce_pygame.py` (pygame) | 无 | `pip install edge-tts pygame` |
| **macOS** | `announce_pygame.py` (pygame) | `announce.sh` (afplay) | `brew install edge-tts && pip install pygame` |
| **Linux** | `announce_pygame.py` (pygame) | `announce.sh` (mpg123) | `apt install edge-tts mpg123 && pip install pygame` |

**自动选择逻辑**：
- 如果 `pygame` 可用 → 所有平台统一使用 `announce_pygame.py`
- 如果 `pygame` 不可用 → macOS/Linux 使用 `announce.sh` + 系统播放器
- Windows 无 pygame 会报错（必须安装 pygame）

---

## 📦 安装方式

### 方式一：PyPI（推荐）
```bash
pip install audio-announcement
pip install pygame  # 确保 pygame 可用
```

### 方式二：ClawHub
```bash
clawhub install audio-announcement
```

### 方式三：GitHub 源码
```bash
git clone https://github.com/wililam/audio-announcement-skills.git
cd audio-announcement-skills
pip install -e .
```

---

## 🧪 测试与验证

### 完整验证脚本

```bash
# 项目自带的验证脚本
cd ~/.openclaw-autoclaw/workspace
py -3 scripts/verify_announcement.py
```

预期输出：
```
=== 语音播报功能验证 ===

1. 检查依赖
[OK] edge-tts 已安装: edge-tts 7.2.8
[OK] pygame 已安装: 2.6.1

2. 检查脚本文件
[OK] 脚本存在: ...\announce_pygame.py

3. 测试播报功能
[OK] receive 播报成功
[OK] task 播报成功
[OK] complete 播报成功
[OK] error 播报成功

==================================================
全部通过
通过率: 4/4

恭喜！语音播报功能工作正常！
```

### 启动自检脚本

```bash
cd ~/.openclaw-autoclaw/skills/audio-announcement
python scripts/startup_check_announcement.py
```

### CLI 测试

```bash
audio-announce test
```

---

## ⚙️ 配置选项

配置文件：`~/.config/audio-announcement/config.json`

```json
{
  "enabled": true,             // 启用/禁用播报
  "default_lang": "zh",        // 默认语言
  "volume": 1.0,               // 音量 (0.0-1.0)
  "async_default": true,       // 默认异步播放
  "cache_enabled": true,       // 启用缓存
  "log_level": "WARNING",      // 日志级别
  "prefer_pygame": true,       // 优先使用 pygame
  "fallback_to_shell": true    // 失败时回退到 shell 脚本
}
```

运行时修改：
```python
from audio_announcement import set_config
set_config(async_default=False, volume=0.8)
```

---

## 📊 监控与维护


### 日志查看

```bash
# 播放日志
tail -f ~/.openclaw-autoclaw/skills/audio-announcement/logs/*.log

# 缓存统计
du -sh ~/.cache/audio-announcement/
```

### 清理缓存

```bash
# 清理所有缓存（会重新生成）
rm -rf ~/.cache/audio-announcement/*.mp3
```

---

## 🧩 高级用法

### 自定义语音

修改 `audio_announcement/announce_helper.py` 中的 `voices` 字典：

```python
voices = {
    "zh": "zh-CN-XiaoxiaoNeural",     # 晓晓
    "en": "en-US-JennyNeural",        # Jenny
    "ja": "ja-JP-NanamiNeural",       # 七海
    # 更多参考: https://learn.microsoft.com/azure/ai-services/speech-service/language-support#text-to-speech
}
```

### 批量播报

```python
from audio_announcement import announce

steps = ["开始处理", "步骤一完成", "步骤二完成", "任务结束"]
for step in steps:
    announce("task", step)
```

### 错误处理

```python
try:
    result = do_something()
    complete("操作成功")
except Exception as e:
    error(f"操作失败: {e}")
    raise
```

---

## 🔍 故障排除

### 问题：没有声音

1. 检查系统音量
2. 确认 pygame 已安装：`python -c "import pygame; print(pygame.version.ver)"`
3. 测试 edge-tts：`edge-tts --text "测试" --voice zh-CN-XiaoxiaoNeural --write-media test.mp3`
4. 手动播放 test.mp3 确认音频输出正常

### 问题：播报延迟

- 首次使用会有缓存延迟（下载语音包）
- 考虑使用 `async_default=true` 异步播放
- 检查网络连接（edge-tts 需要联网）

### 问题：/RESET 后播报失效

- 确认 `startup_check_announcement.py` 已配置自动运行
- 手动运行自检：`python scripts/startup_check_announcement.py`
- 检查 IDENTITY.md 和 AGENTS.md 是否保留

### 问题：ClawHub 发布失败

ClawHub CLI 可能存在环境兼容问题，建议：
- 使用 GitHub 版本：`pip install git+https://github.com/wililam/audio-announcement-skills.git`
- 或换用 Python 3.12 环境重试

---

## 📈 性能与优化

- **缓存机制**：首次生成 MP3 后缓存，后续播放直接复用（无需重复生成）
- **异步播放**：默认后台播放，不阻塞 Agent 响应（可配置为同步）
- **批量操作**：多文件处理时自动队列化
- **资源清理**：临时文件 24 小时自动清理

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

如果你发现任何遗漏播报的场景，或需要更多集成示例，请告诉我们。

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🎉 总结

audio-announcement v2.0.8 提供了：

- ✅ **跨平台支持**（Windows/macOS/Linux）
- ✅ **PyPI 一键安装**
- ✅ **配置文件管理**
- ✅ **防遗忘两重保障**（启动自检 + 强制规则）
- ✅ **Session Hook 自动恢复**
- ✅ **异步非阻塞播放**
- ✅ **9种语言支持**

**你的 OpenClaw Agent 现在可以"开口说话"了，而且永远不会忘记！** 🦀🗣️

---

**🚀 快速开始：**

```bash
# 1. 安装
pip install audio-announcement pygame

# 2. 配置
audio-announce config async_default=true

# 3. 测试
audio-announce test

# 4. 集成到你的 Agent
from audio_announcement import receive, task, complete, error
```

开始享受透明、有温度的声音体验吧！
