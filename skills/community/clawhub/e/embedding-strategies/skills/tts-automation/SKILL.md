# TTS 自动化 Skill - 文本转语音 + 自动播放

> 版本：V2.0  
> 状态：✅ 已精简  
> 最后更新：**2026-03-07 17:48**（TTS 使用规范调整）  
> 触发词：**仅限「每小时优先级提醒」Cron 任务调用**

---

## 📋 Skill 定义

**名称：** TTS 自动化 Skill  
**编号：** SKILL-TTS-001  
**触发：** 仅限「每小时优先级提醒」Cron 任务调用

**一句话描述：** 调用阿里云 TTS 生成语音 → 保存到 workspace/tts → 自动播放

**⚠️ 重要调整（2026-03-07 17:48）：**
- ❌ **不再被其他 Skill 调用**（豆包点评/HTML 报告/项目构建等）
- ✅ **唯一使用场景：** 每小时优先级提醒（Cron 任务）

---

## 🎯 目标

**解决什么问题：**
- ✅ 文本→语音自动转换
- ✅ 语音文件统一归档（workspace/tts）
- ✅ 生成后自动播放（0 步操作）
- ✅ 锁屏时不播放（智能检测）

**核心价值：**
- 一键生成语音
- 自动播放，无需手动操作
- 文件统一管理

**使用规范（2026-03-07 17:48）：**
- ✅ 每小时优先级提醒（Cron 任务）- **唯一使用场景**
- ❌ 豆包会话专家点评 - 已取消
- ❌ HTML 报告生成 - 已取消
- ❌ 项目知识库构建 - 已取消
- ❌ 其他所有场景 - 已取消

---

## 🔄 工作流程

```
用户提供文本
  ↓
🆕 ATOM-VISUAL-030 过滤 Emoji 和特殊符号
  ↓
调用阿里云 TTS API（使用纯文本）
  ↓
生成 MP3 文件（workspace/tts/voice-时间戳.mp3）
  ↓
调用 ATOM-DELIVERY-013（本地播放语音）
  ↓
✅ 语音自动播放（屏幕活跃时）
```

---

## 📝 详细步骤

### 步骤 1：准备文本

```powershell
# 用户提供的文本
$text = "你好，这是优先级提醒。当前最优先任务是飞书 OAuth 配置。"

# 检查长度（≤1500 字符）
if ($text.Length -gt 1500) {
    Write-Host "文本超长，分段处理..." -ForegroundColor Yellow
    # 分段逻辑
}
```

### 🆕 步骤 2：过滤 Emoji 和特殊符号

```powershell
# 调用 ATOM-VISUAL-030 过滤 emoji
$cleanText = ATOM-VISUAL-030 -text $text

# 示例：
# 过滤前："✅ 完成：TTS 精简\n📊 统计：13 项完成"
# 过滤后："完成：TTS 精简 统计：13 项完成"

Write-Host "✅ Emoji 已过滤，纯文本：" $cleanText -ForegroundColor Green
```

### 步骤 3：调用阿里云 TTS API

```powershell
# 阿里云 TTS 配置
$apiKey = "sk-1f3847debc3e492e81f64115b20c6d82"
$voice = "zh-CN-yunxi"
$lang = "zh-CN"
$outputFormat = "mp3"

# 生成文件名
$timestamp = [DateTimeOffset]::Now.ToUnixTimeMilliseconds()
$ttsFolder = "C:\Users\Xiabi\.openclaw\workspace\tts"
$outputFile = Join-Path $ttsFolder "voice-$timestamp.mp3"

# 确保文件夹存在
if (!(Test-Path $ttsFolder)) {
    New-Item -ItemType Directory -Path $ttsFolder -Force | Out-Null
}

# 调用阿里云 TTS API
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

$body = @{
    "model" = "cosyvoice-v1"
    "input" = @{
        "text" = $text
    }
    "parameters" = @{
        "voice" = $voice
        "format" = $outputFormat
        "sample_rate" = 24000
    }
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "https://dashscope.aliyuncs.com/compatible-mode/v1/audio/speech" `
    -Method POST `
    -Headers $headers `
    -Body $body `
    -OutFile $outputFile

Write-Host "✅ TTS 生成成功：$outputFile" -ForegroundColor Green
```

### 步骤 3：自动播放（调用 ATOM-DELIVERY-013）

```powershell
# 检测锁屏状态
$lockProcess = Get-Process "LockApp" -ErrorAction SilentlyContinue

if ($lockProcess) {
    Write-Host "🔒 屏幕已锁定，跳过播放" -ForegroundColor Yellow
    # 记录日志
    Add-Content -Path "$env:TEMP\voice-playback-log.txt" -Value "$(Get-Date) - 跳过播放（屏幕锁定）"
} else {
    Write-Host "▶️  开始播放..." -ForegroundColor Cyan
    Start-Process $outputFile
    Write-Host "✅ 语音正在播放..." -ForegroundColor Green
    # 记录日志
    Add-Content -Path "$env:TEMP\voice-playback-log.txt" -Value "$(Get-Date) - 播放成功：voice-$timestamp.mp3"
}
```

### 步骤 4：确认完成

```powershell
Write-Host "`n🎉 TTS 自动化完成！" -ForegroundColor Green
Write-Host "  文件：$outputFile" -ForegroundColor Cyan
Write-Host "  大小：$((Get-Item $outputFile).Length) 字节" -ForegroundColor Gray
Write-Host "  播放状态：$if ($lockProcess) { "已跳过（锁屏）" } else { "播放中" }" -ForegroundColor Gray
```

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** 需要转换的文字稿（≤1500 字符）
- **必填：** 是

### 输出
- **类型：** MP3 文件 + 自动播放
- **路径：** `workspace/tts/voice-时间戳.mp3`
- **附加：** 播放状态

---

## ⚙️ 偏好设置

### TTS 配置
- **提供商：** 阿里云（Aliyun）
- **声音：** zh-CN-yunxi
- **语言：** zh-CN（中文）
- **格式：** MP3
- **采样率：** 24000 Hz
- **码率：** 48 kbitrate

### 文件管理
- **存储位置：** `workspace/tts/`
- **命名规则：** `voice-时间戳.mp3`
- **统一归档：** 所有 TTS 文件集中管理

### 播放策略
- **自动播放：** ✅ 是（生成后立即播放）
- **锁屏检测：** ✅ 是（锁屏时跳过）
- **日志记录：** ✅ 是（记录到 Temp/voice-playback-log.txt）

---

## 🔄 使用示例

### 示例 1：生成优先级提醒语音

```
用户提供："当前最优先任务是飞书 OAuth 配置，5 分钟就能搞定。"
  ↓
调用：SKILL-TTS-001
  ↓
处理：
  - 调用阿里云 TTS
  - 生成：workspace/tts/voice-1772869000000.mp3
  - 检测：屏幕活跃
  - 播放：自动播放
  ↓
输出：MP3 文件 + 自动播放
```

### 示例 2：生成豆包点评语音

```
用户提供："豆包会话已处理，专家点评 HTML 已生成，请查看 Chrome。"
  ↓
调用：SKILL-TTS-001
  ↓
处理：同上
  ↓
输出：MP3 文件 + 自动播放
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- ATOM-DELIVERY-013：本地播放语音（自动调用）

### 复用原子动作
- 🆕 **ATOM-VISUAL-030**：过滤 Emoji 和特殊符号（步骤 2）
- ATOM-VISUAL-008：生成 TTS 语音（步骤 3）
- ATOM-DELIVERY-013：本地播放语音（步骤 5）

---

## ✅ 检查清单

执行前确认：
- [ ] 文本≤1500 字符
- [ ] 文本内容合适（无敏感信息）
- [ ] **已调用 ATOM-VISUAL-030 过滤 emoji**
- [ ] 阿里云 API Key 有效
- [ ] workspace/tts 文件夹可写
- [ ] 网络正常

执行后确认：
- [ ] MP3 文件已生成
- [ ] 文件大小正常（>0 字节）
- [ ] 自动播放已触发（或锁屏跳过）
- [ ] 日志已记录

---

## ⚠️ 常见错误

### 错误 1：文本超长

```
❌ 错误：>1500 字符（会被 TTS 截断）
✅ 正确：分段生成，每段≤1500 字符
```

### 错误 2：API Key 无效

```
❌ 错误：401 Unauthorized
✅ 正确：检查阿里云 API Key 配置
```

### 错误 3：文件夹不可写

```
❌ 错误：权限不足
✅ 正确：检查 workspace/tts 文件夹权限
```

### 错误 4：锁屏时播放

```
❌ 错误：锁屏时播放（浪费资源）
✅ 正确：检测 LockApp 进程，锁屏时跳过
```

---

## 💡 核心原则

> **文本转语音 → 自动播放，0 步操作！**

**关键点：**
1. ✅ 阿里云 TTS（高质量中文语音）
2. ✅ 统一归档（workspace/tts/）
3. ✅ 自动播放（屏幕活跃时）
4. ✅ 锁屏跳过（智能检测）

**触发词：**
- "生成语音"
- "转语音"
- "朗读这段"

---

## 📚 参考文档

- 原子动作：`ATOM-VISUAL-008 - 生成 TTS 语音`
- 原子动作：`ATOM-DELIVERY-013 - 本地播放语音`
- 配置：`openclaw.json`（TTS 配置）
- 阿里云文档：https://help.aliyun.com/zh/dashscope/

---

_TTS 自动化 | 一键生成 | 自动播放 | 2026-03-07_
_版本更新：V2.0（2026-03-07 17:48）- 精简 TTS 使用，仅每小时提醒调用_
