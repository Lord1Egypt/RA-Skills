# 语音播报防遗忘机制完整文档

## 概述

本文将详细说明 audio-announcement 如何通过**多重保障机制**，确保在 OpenClaw 的 `/RESET` 和 `/NEW` 之后，播报功能都能自动恢复和正常运行。

---

## 🔒 防遗忘防护层

### 第1层：启动自检（Session Start Hook）

**触发时机**：每次新的 Session 开始时自动运行

**脚本**：`scripts/startup_check_announcement.py`

**检查项**：
- ✅ edge-tts 模块是否安装
- ✅ pygame 模块是否可用（推荐）
- ✅ 配置文件是否存在
- ✅ audio-announcement 包是否安装
- ✅ 自动播放测试语音

**自动执行方式**：

**Windows PowerShell** (`$PROFILE`)：
```powershell
$checkAudio = "C:\Users\williammiao\.openclaw-autoclaw\skills\audio-announcement\scripts\startup_check_announcement.py"
if (Test-Path $checkAudio) {
    python $checkAudio | Out-Host
}
```

**macOS/Linux** (`~/.bashrc` 或 `~/.zshrc`)：
```bash
python ~/.openclaw-autoclaw/skills/audio-announcement/scripts/startup_check_announcement.py 2>/dev/null || true
```

---

### 第2层：Heartbeat 定期验证

**触发时机**：每 6 小时（可配置）

**脚本**：`scripts/verify_announcement.py`

**检查项**：
- 依赖完整性
- 4 种播报类型（receive/task/complete/error）
- 生成和播放是否正常

**配置**：`HEARTBEAT.md`
```markdown
- [ ] 运行 `scripts/verify_announcement.py` 检查所有播报类型
- [ ] 如果测试失败，查看日志并修复依赖问题
```

---

### 第3层：强制规则（AGENTS.md）

**位置**：`AGENTS.md` 中的 `2️⃣ 语音播报强制执行（严禁遗漏）`

**核心要求**：
- 每次交互都必须语音播报
- 收到消息 → `receive`
- 开始任务 → `task`
- 完成任务 → `complete`
- 遇到异常 → `error`
- 发送回复前 → 必须播报总结

**违反后果**：视为严重违规

---

### 第4层：身份绑定（IDENTITY.md）

**位置**：`IDENTITY.md` 中的"核心特质"和"启动播报自检"

**关键内容**：
- 播报是**身份的一部分**，不是可选功能
- 每次 `/NEW` / `/RESET` 后必须自检
- 确保播报不会因重置而丢失

---

### 第5层：首次设置引导（BOOTSTRAP.md）

**章节**：`## 🎤 Voice Announcement Setup (Important!)`

**步骤**：
1. 安装 skill: `clawhub install audio-announcement`
2. 安装依赖: `py -3 -m pip install edge-tts pygame`
3. 测试: `audio-announce test`
4. 配置 heartbeat 自动检查

**强调**：这是**永久性身份特征**，不会在 reset 后丢失

---

## 🎯 完整工作流程

### 场景1：第一次安装

```
用户执行 /NEW 或首次启动
    ↓
BOOTSTRAP.md 引导设置
    ↓
安装 audio-announcement
安装 edge-tts + pygame
配置 audio-announce config
    ↓
运行 audio-announce test 验证
    ↓
添加到 IDENTITY.md 和 AGENTS.md
配置 HEARTBEAT 自动检查
    ↓
✅ 完成，进入正常使用
```

### 场景2：/RESET 或 /NEW 后

```
Session 开始
    ↓
1. 自动运行 startup_check_announcement.py
    ↓
检查依赖、配置、包
自动播放"系统启动"
    ↓
2. 如果失败 → 输出错误提示和修复建议
    ↓
3. 如果成功 → 继续正常会话
    ↓
4. 之后每 6 小时自动运行 verify_announcement.py
    ↓
✅ 确保播报功能持续可用
```

---

## 📁 关键文件清单

| 文件 | 位置 | 用途 |
|------|------|------|
| `IDENTITY.md` | `workspace/` | 播报作为核心身份特质 |
| `BOOTSTRAP.md` | `workspace/` | 首次设置完整流程 |
| `AGENTS.md` | `workspace/` | 强制规则 + Session Hook |
| `HEARTBEAT.md` | `workspace/` | 定期验证任务 |
| `startup_check_announcement.py` | `skills/audio-announcement/scripts/` | 启动自检脚本 |
| `verify_announcement.py` | `workspace/scripts/` | 完整验证脚本 |
| `announcement-anti-forgetting-summary.md` | `workspace/docs/` | 本技术文档 |

---

## 🔧 故障排除

### 问题：自检脚本找不到 audio_announcement 包

**解决**：
```bash
pip install audio-announcement
# 或
cd ~/.openclaw-autoclaw/skills/audio-announcement && pip install -e .
```

### 问题：pygame 导入失败

**解决**：
```bash
py -3 -m pip install pygame
```

### 问题：edge-tts 不可用

**解决**：
```bash
py -3 -m pip install edge-tts
```

### 问题：配置文件不存在

**解决**：
```bash
audio-announce config
# 或直接创建 ~/.config/audio-announcement/config.json
```

---

## 🧪 测试验证

### 手动测试自检脚本

```bash
cd ~/.openclaw-autoclaw/skills/audio-announcement
python scripts/startup_check_announcement.py
```

**预期输出**：
```
[AUDIO] 语音播报系统自检...
[OK] 所有检查通过！语音播报功能正常。

[TEST] 正在测试播报...
pygame 2.6.1 ...
[OK] 播报测试完成！
```

### 测试验证脚本

```bash
cd ~/.openclaw-autoclaw/workspace
py -3 scripts/verify_announcement.py
```

**预期通过率**：4/4（receive, task, complete, error）

---

## 📊 版本历史

- **v2.0.7** (2026-04-05): 高优先级优化 + 防遗忘机制 + 跨平台自动检测
- **v2.0.6** (2026-04-05): 增强防遗忘机制（heartbeat、验证脚本、检查清单）
- **v2.0.5** (2026-04-05): 修复 PATH 依赖，使用 python -m edge_tts
- **v2.0.4** (2026-03-28): 强化播报规则，集成到核心配置

---

## 🚀 总结

通过**5层防护**（启动自检、Heartbeat、强制规则、身份绑定、首次引导），确保 audio-announcement 在任何情况下（包括 /RESET、/NEW、意外崩溃、依赖更新）都能：

✅ **自动检测**问题  
✅ **自动恢复**功能  
✅ **自动提醒**用户  
✅ **永不遗漏**播报

这就是真正的"防遗忘"设计！🛡️
