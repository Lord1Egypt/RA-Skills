# 语音命令识别 - 原子动作模块

> 编号：ATOM-VOICE-001  
> 分类：04-analysis（分析层）  
> 状态：🟡 待规范  
> 创建时间：2026-03-08 09:10

---

## 📋 动作定义

**名称：** 语音命令识别  
**输入：** 音频文件（WAV/MP3）或 语音转文字结果  
**输出：** 识别的命令名称 + 参数  
**耗时：** ≤3 秒

**一句话描述：** 将语音输入转换为可执行的命令对象

---

## 🎯 输入输出

### 输入
- **类型：** 音频文件 或 文字
- **格式：** WAV/MP3 或 纯文本
- **时长：** ≤60 秒
- **语言：** 中文普通话

### 输出
```json
{
  "command": "生成周报",
  "action": "weekly-report",
  "parameters": {},
  "confidence": 0.95,
  "timestamp": 1772930000000
}
```

---

## ⚙️ 偏好设置

### 识别引擎
- **首选：** 阿里云智能语音交互（在线，高精度）
- **备用：** Whisper.cpp（离线，隐私保护）
- **本地：** Windows 内置识别（快速，低精度）

### 命令词库
- **位置：** `voice-commands.json`
- **格式：** JSON
- **更新：** 支持热加载

---

## 📝 操作步骤

### 步骤 1：加载语音文件

```powershell
param(
    [string]$AudioPath
)

if (!(Test-Path $AudioPath)) {
    Write-Host "❌ 音频文件不存在：$AudioPath" -ForegroundColor Red
    return
}

$audioSize = (Get-Item $AudioPath).Length
Write-Host "📂 加载音频：$AudioPath ($([math]::Round($audioSize/1KB, 2)) KB)" -ForegroundColor Cyan
```

### 步骤 2：语音转文字（阿里云）

```powershell
# 阿里云配置
$apiKey = "sk-xxx"
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/octet-stream"
    "X-NLS-Token" = "your-token"
}

# 上传音频
$response = Invoke-RestMethod `
    -Uri "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr" `
    -Method POST `
    -Headers $headers `
    -InFile $AudioPath `
    -ContentType "audio/wav"

# 解析结果
$text = $response.text
$confidence = $response.confidence

Write-Host "🎤 识别结果：$text (置信度：$confidence)" -ForegroundColor Green
```

### 步骤 3：加载命令词库

```powershell
$commandsPath = "voice-commands.json"
if (Test-Path $commandsPath) {
    $global:VoiceCommands = Get-Content $commandsPath -Raw | ConvertFrom-Json
    Write-Host "📚 加载命令词库：$($global:VoiceCommands.Count) 条命令" -ForegroundColor Cyan
} else {
    Write-Host "❌ 命令词库不存在：$commandsPath" -ForegroundColor Red
    return
}
```

### 步骤 4：关键词匹配

```powershell
function Find-MatchingCommand {
    param(
        [string]$InputText
    )
    
    $bestMatch = $null
    $bestScore = 0
    
    foreach ($cmd in $global:VoiceCommands) {
        # 精确匹配
        if ($InputText -eq $cmd.name) {
            return $cmd
        }
        
        # 包含匹配
        if ($InputText -like "*$($cmd.name)*") {
            $score = $cmd.name.Length / $InputText.Length
            if ($score -gt $bestScore) {
                $bestScore = $score
                $bestMatch = $cmd
            }
        }
        
        # 同义词匹配
        if ($cmd.synonyms -and $cmd.synonyms -contains $InputText) {
            return $cmd
        }
    }
    
    if ($bestScore -gt 0.5) {
        return $bestMatch
    }
    
    return $null
}

$matchedCommand = Find-MatchingCommand -InputText $text

if ($matchedCommand) {
    Write-Host "✅ 匹配命令：$($matchedCommand.name) → $($matchedCommand.action)" -ForegroundColor Green
} else {
    Write-Host "❌ 未匹配命令：$text" -ForegroundColor Red
}
```

### 步骤 5：返回命令对象

```powershell
$result = @{
    command = $text
    action = $matchedCommand.action
    parameters = @{}
    confidence = $confidence
    timestamp = [DateTimeOffset]::Now.ToUnixTimeMilliseconds()
}

return $result
```

---

## 🔄 使用场景

### 场景 1：语音生成周报

```
输入：音频文件（用户说"生成周报"）
  ↓
识别：阿里云 ASR → "生成周报"
  ↓
匹配：命令词库 → weekly-report
  ↓
输出：@{ command="生成周报"; action="weekly-report" }
```

### 场景 2：语音查询优先级

```
输入：音频文件（用户说"当前优先级"）
  ↓
识别：阿里云 ASR → "当前优先级"
  ↓
匹配：命令词库 → priority-reminder
  ↓
输出：@{ command="当前优先级"; action="priority-reminder" }
```

### 场景 3：模糊匹配

```
输入：音频文件（用户说"帮我弄周报"）
  ↓
识别：阿里云 ASR → "帮我弄周报"
  ↓
匹配：包含"周报" → weekly-report
  ↓
输出：@{ command="帮我弄周报"; action="weekly-report" }
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- ATOM-VOICE-002：命令执行引擎
- ATOM-VISUAL-008：TTS 反馈生成
- ATOM-DELIVERY-010：飞书消息发送

### 复用原子动作
- 无（独立动作）

---

## ✅ 检查清单

执行前确认：
- [ ] 音频文件存在且可读
- [ ] 阿里云 API Key 有效
- [ ] 命令词库已加载
- [ ] 网络连接正常

执行后确认：
- [ ] 识别结果准确
- [ ] 命令匹配成功
- [ ] 返回对象格式正确
- [ ] 置信度 > 0.5

---

## ⚠️ 常见错误

### 错误 1：音频格式不支持

```
❌ 错误：只支持 WAV/MP3
✅ 正确：转换格式后重试
```

### 错误 2：环境噪音大

```
❌ 错误：识别准确率低（<0.5）
✅ 正确：安静环境重新录制
```

### 错误 3：命令未匹配

```
❌ 错误：不在词库中
✅ 正确：添加自定义命令
```

---

_语音命令识别 | 音频→文字→命令 | 2026-03-08_
