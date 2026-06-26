# Feishu Message Automation - 飞书消息自动化

## 技能描述

自动化发送飞书消息，支持文字、语音、文件、交互式卡片，以及消息回复、删除、反应等高级功能。

## 触发条件

- **自动触发**：各 Skill 需要发送通知时
- **手动触发**：用户说"发送飞书"、"通知 XX"、"发消息"

## 核心能力

1. **文字消息** - 发送 Markdown 格式文字
2. **语音消息** - TTS 转换 + 文件发送 + 自动播放
3. **文件发送** - Word/Excel/HTML/PDF 等
4. **交互卡片** - 带按钮的可点击卡片
5. **消息回复** - 引用回复指定消息
6. **消息删除** - 删除已发送消息
7. **消息反应** - 添加 emoji 反应
8. **批量发送** - 发送给多人/多群组

## 成功案例（2026-03-06）

### 优先级提醒消息

**类型：** 文字 + 语音
**频率：** 每小时
**内容：**
```markdown
## 🔴 优先：飞书 OAuth 配置（5 分钟）
## 🟡 次优：地理知识库 KML 导出（有空再弄）
## 💡 建议：先搞定 OAuth，再考虑其他
```

**发送流程：**
1. TTS 生成语音
2. message tool 发送（文字 + 语音）
3. Start-Process 本地播放

---

### 批注清单消息

**类型：** 结构化 Markdown
**场景：** 项目文档第 2 轮批注
**内容：**
```markdown
## 📝 第 2 轮批注清单（共 10 条）

**文档：** 感知与行动中心 v2.0
**批注时间：** 2026-03-06
**状态：** 待用户回复

---

### ❓ 疑问类（3 条）

**批注 001：** 项目经理人选未明确
- 位置：项目基本信息摘要
- 内容：建议确认项目经理姓名

### ⚠️ 风险提示（2 条）

**批注 002：** 产能达标率数据准确性
- 位置：1.2 当前现状和痛点

### 💡 建议类（3 条）

**批注 003：** 补充具体时间节点
- 位置：3.2 实施计划

### 📝 待补充（2 条）

**批注 004：** 实施费用明细
- 位置：3.4 实施费用
```

---

### 交互式卡片消息

**类型：** msg_type: interactive
**按钮：** 3 个可点击按钮
**内容：**
```json
{
  "msg_type": "interactive",
  "card": {
    "config": { "wide_screen_mode": true },
    "elements": [
      {
        "tag": "action",
        "actions": [
          { "tag": "button", "text": { "tag": "plain_text", "content": "✅ 确认" }, "type": "primary" },
          { "tag": "button", "text": { "tag": "plain_text", "content": "❓ 疑问" }, "type": "default" },
          { "tag": "button", "text": { "tag": "plain_text", "content": "💡 建议" }, "type": "default" }
        ]
      }
    ]
  }
}
```

---

### 晚安同步确认消息

**类型：** 文字 + 语音
**内容：**
```markdown
## 🌙 晚安记忆同步完成

**时间：** 2026-03-07 00:55
**状态：** ✅ 成功

**同步文件：**
- memory/2026-03-07.md (4.5 KB)
- MEMORY.md
- worklog.txt
- skills/ (4 个文件)

**总计：** 4 个文件，18 KB
**位置：** OneDrive/Documents/阿福记忆备份

晚安！好梦！🌙
```

---

## 消息类型

### 1. 文字消息（text）

**适用：** 通知、提醒、总结

**示例：**
```json
{
  "action": "send",
  "message": "## 📊 周报已生成\n\n请审阅内容...",
  "target": "ou_e3a0d4a64a9e0932ee919b97f17ec210"
}
```

### 2. 语音消息（audio）

**适用：** 语音提醒、故事讲述

**示例：**
```json
{
  "action": "send",
  "filePath": "C:\\Users\\Xiabi\\AppData\\Local\\Temp\\tts-*/voice-*.mp3",
  "message": "文字稿内容...",
  "target": "ou_e3a0d4a64a9e0932ee919b97f17ec210"
}
```

### 3. 文件消息（file）

**适用：** Word/Excel/HTML/PDF

**示例：**
```json
{
  "action": "send",
  "filePath": "C:\\Users\\Xiabi\\.openclaw\\workspace\\skills\\阿福 Skills 汇总文档 V2.0.docx",
  "message": "请查看附件文档",
  "target": "ou_e3a0d4a64a9e0932ee919b97f17ec210"
}
```

### 4. 交互卡片（interactive）

**适用：** 需要用户操作（确认/选择）

**示例：** 见成功案例

### 5. 图片消息（image）

**适用：** 截图、图表

**示例：**
```json
{
  "action": "send",
  "media": "C:\\Users\\Xiabi\\Pictures\\screenshot.png",
  "message": "请查看截图",
  "target": "ou_e3a0d4a64a9e0932ee919b97f17ec210"
}
```

---

## 工作流程

### 语音消息完整流程

```
1. 生成文字稿 - Markdown 格式
2. TTS 转换 - 生成 MP3
3. 发送消息 - message tool（filePath + message）
4. 本地播放 - Start-Process
5. 确认送达 - 检查 messageId
```

### 文件发送流程

```
1. 准备文件 - 确认文件存在
2. 编写说明 - Markdown 格式
3. 发送消息 - message tool（filePath + message）
4. 确认送达 - 检查 messageId
5. 可选：自动打开 - Start-Process
```

### 交互卡片流程

```
1. 设计卡片 - JSON 格式
2. 配置按钮 - 设置回调
3. 发送消息 - message tool（msg_type: interactive）
4. 等待回调 - HTTP callback
5. 处理响应 - 根据按钮执行
```

---

## 技术实现

### 发送语音消息（PowerShell）

```powershell
param(
    [string]$Text,
    [string]$Target
)

# TTS 生成
$ttsResult = Invoke-TTS -Text $Text
$voicePath = $ttsResult.mediaUrl

# 发送消息
$message = @"
## 📢 语音消息

$Text
"@

Invoke-MessageSend `
    -Action "send" `
    -FilePath $voicePath `
    -Message $message `
    -Target $Target

# 本地播放
Start-Process $voicePath

Write-Host "✅ 语音已发送并播放"
```

### 发送文件

```powershell
param(
    [string]$FilePath,
    [string]$Description,
    [string]$Target
)

if (Test-Path $FilePath) {
    $fileSize = (Get-Item $FilePath).Length
    $fileName = Split-Path $FilePath -Leaf
    
    $message = @"
## 📄 文件发送

**文件名：** $fileName
**大小：** $([math]::Round($fileSize/1KB, 2)) KB
**说明：** $Description

[打开文件](file://$FilePath)
"@

    Invoke-MessageSend `
        -Action "send" `
        -FilePath $FilePath `
        -Message $message `
        -Target $Target
    
    Write-Host "✅ 文件已发送：$fileName"
} else {
    Write-Host "❌ 文件不存在：$FilePath"
}
```

### 发送交互卡片

```powershell
$card = @{
    msg_type = "interactive"
    card = @{
        config = @{ wide_screen_mode = $true }
        elements = @(
            @{
                tag = "action"
                actions = @(
                    @{
                        tag = "button"
                        text = @{ tag = "plain_text"; content = "✅ 确认" }
                        type = "primary"
                        value = @{ action = "confirm" }
                    },
                    @{
                        tag = "button"
                        text = @{ tag = "plain_text"; content = "❓ 疑问" }
                        type = "default"
                        value = @{ action = "question" }
                    }
                )
            }
        )
    }
}

Invoke-MessageSend `
    -Action "send" `
    -Target $Target `
    -Card $card
```

---

## 输出格式

### 消息模板库

**优先级提醒：**
```markdown
## 🔴 优先：[任务名]（[耗时]）
## 🟡 次优：[任务名]（[说明]）
## 💡 建议：[建议内容]
```

**周报生成通知：**
```markdown
## 📊 周报已生成

**时间：** [时间]
**周期：** [周数]

**内容来源：**
- ✅ worklog.txt (X 条记录)
- ✅ 豆包会话 (X 条)

**下一步：**
1. 审阅周报内容
2. 手动完善措辞
3. 发送给领导

[查看周报](file://workreport.txt)
```

**批注清单：**
```markdown
## 📝 第 X 轮批注清单（共 X 条）

**文档：** [文档名]
**批注时间：** [日期]
**状态：** 待用户回复

---

### ❓ 疑问类（X 条）

**批注 001：** [标题]
- 位置：[章节]
- 内容：[说明]
- 需要回复：✅ 是

[更多批注...]
```

**晚安同步：**
```markdown
## 🌙 晚安记忆同步完成

**时间：** [时间]
**状态：** ✅ 成功

**同步文件：**
- [文件列表]

**总计：** X 个文件，X KB
**位置：** [OneDrive 路径]

晚安！好梦！🌙
```

---

## 用户偏好

- ✅ **文字 + 语音** - 同时发送文字稿和语音
- ✅ **自动播放** - TTS 后自动 Start-Process
- ✅ **filePath 参数** - message tool 用 filePath（不用 buffer）
- ✅ **Markdown 格式** - 结构化排版
- ✅ **图标点缀** - emoji 增强可读性
- ✅ **简洁清晰** - 重点突出，不冗长

---

## 示例用法

**场景 1：发送优先级提醒**
```
用户："每小时提醒优先级"
AI:
1. 生成文字稿
2. TTS 转换
3. 发送飞书（文字 + 语音）
4. 本地播放
```

**场景 2：发送文件**
```
用户："把 V2.0 文档发给我"
AI:
1. 确认文件存在
2. 编写说明
3. 发送飞书（文件 + 说明）
4. 可选：自动打开
```

**场景 3：发送批注清单**
```
AI: 
1. 生成批注清单（10 条）
2. 分类整理（疑问/风险/建议/待补充）
3. 发送飞书（结构化 Markdown）
4. 等待用户回复
```

**场景 4：发送交互卡片**
```
AI:
1. 设计卡片（3 个按钮）
2. 配置回调
3. 发送飞书
4. 等待用户点击
```

---

## 与其他 Skill 的协作

**周报 Skill：**
- 发送周报生成通知
- 发送审阅提醒

**项目进度同步 Skill：**
- 发送同步完成通知
- 发送项目状态更新

**晚安记忆同步 Skill：**
- 发送同步确认
- 发送晚安语音

**HTML 专家点评 Skill：**
- 发送 HTML 生成通知
- 发送核心内容摘要

---

## 注意事项

1. **filePath 参数** - 用 filePath（不用 buffer）
2. **文件大小** - 控制在 20MB 以内
3. **语音长度** - ≤1500 字符（避免自动摘要）
4. **发送频率** - 避免短时间大量发送
5. **用户确认** - 重要操作需用户确认

---

## 参考文档

- message tool 文档：`openclaw docs/message`
- 成功案例：2026-03-06 各消息记录
- 飞书开放平台：`https://open.feishu.cn/document`

---

_最后更新：2026-03-07 01:10 - 创建 Skill（参考 2026-03-06 成功案例）_
