---
name: phone-detection-alert
description: 玩手机检测告警技能。通过摄像头抓图→AI 分析→TTS 语音→设备播放的完整流程。Use when: 需要监控玩手机行为并自动告警、课堂/考场/会议室纪律监控、通过萤石摄像头进行 AI 行为检测。
metadata:
  {
    "openclaw": {
      "emoji": "📱",
      "requires": {
        "env": ["EZVIZ_APP_KEY", "EZVIZ_APP_SECRET", "EZVIZ_DEVICE_SERIAL"],
        "pip": ["requests", "edge-tts"]
      },
      "primaryEnv": "EZVIZ_APP_KEY"
    }
  }
---

# Phone Detection Alert (玩手机检测告警)

萤石开放平台 AI 算法 + 语音告警，检测到玩手机自动播放提醒。

## 快速开始

### 安装依赖

```bash
pip install requests edge-tts
```

### 设置环境变量（必需）

**必需的环境变量**:
```bash
export EZVIZ_APP_KEY="your_app_key"
export EZVIZ_APP_SECRET="your_app_secret"
export EZVIZ_DEVICE_SERIAL="dev1,dev2,dev3"
```

**可选的环境变量**:
```bash
export EZVIZ_CHANNEL_NO="1"  # 通道号，默认 1
```

⚠️ **重要**: 
- `EZVIZ_APP_KEY`, `EZVIZ_APP_SECRET`, `EZVIZ_DEVICE_SERIAL` 是**必需**的环境变量
- 技能运行前必须设置这些环境变量
- 不需要设置 `EZVIZ_ACCESS_TOKEN`！技能会自动用 `appKey + appSecret` 获取 Token（有效期 7 天，内存缓存）

运行：
```bash
python3 {baseDir}/scripts/phone_detection_alert.py
```

命令行参数：
```bash
# 单个设备
python3 {baseDir}/scripts/phone_detection_alert.py appKey appSecret dev1 1

# 多个设备（逗号分隔）
python3 {baseDir}/scripts/phone_detection_alert.py appKey appSecret "dev1,dev2,dev3" 1

# 指定通道号
python3 {baseDir}/scripts/phone_detection_alert.py appKey appSecret "dev1:1,dev2:2" 1

# 测试模式（跳过检测，直接播放告警）
python3 {baseDir}/scripts/phone_detection_alert.py appKey appSecret "dev1,dev2" 1 --test
```

## 工作流程

```
1. 获取 Token (appKey + appSecret → accessToken, 有效期 7 天)
       ↓
2. 设备抓图 (accessToken + deviceSerial → picUrl, 有效期 2 小时)
       ↓
3. AI 分析 (accessToken + picUrl → 是否玩手机)
       ↓ [检测到]
4. TTS 语音 ("检测到有人玩手机" → audio.mp3)
       ↓
5. 上传语音 (accessToken + audio.mp3 → fileUrl)
       ↓
6. 下发播放 (accessToken + deviceSerial + fileUrl → 设备播放)
```

## Token 自动获取说明

**你不需要手动获取或配置 `EZVIZ_ACCESS_TOKEN`！**

技能会自动处理 Token 的获取和缓存：

```
首次运行:
  appKey + appSecret → 调用萤石 API → 获取 accessToken
  ↓
  缓存到内存（有效期 7 天）
  ↓
后续运行 (7 天内):
  使用缓存的 accessToken（无需重复获取）
  ↓
7 天后:
  自动重新获取新的 accessToken
```

**Token 管理特性**:
- ✅ **自动获取**: 首次运行时自动调用萤石 API 获取
- ✅ **自动缓存**: Token 保存在内存中，7 天内重复使用
- ✅ **自动刷新**: Token 过期后自动重新获取
- ✅ **无需配置**: 不需要手动设置 `EZVIZ_ACCESS_TOKEN` 环境变量
- ✅ **安全**: Token 不写入日志，不保存到磁盘

**为什么这样设计**:
- 萤石 Token 有效期为 7 天，无需每次获取
- 自动管理减少用户配置负担
- 避免 Token 泄露风险（不暴露在环境变量中）

## 输出示例

```
============================================================
Phone Detection Alert System
============================================================
[INFO] Detected 2 device(s): [('dev1', 1), ('dev2', 1)]
[SUCCESS] Token obtained, expires: 2026-03-20 15:00:00

[Device] dev1 (Channel: 1)
[SUCCESS] Image captured: https://opencapture.ys7.com/...
[ALERT] Phone usage detected! (confidence: 0.95)
[SUCCESS] Voice uploaded: http://custom-voice-reminder-hn...
[SUCCESS] Alert sent to device dev1!

[Device] dev2 (Channel: 1)
[SUCCESS] Image captured: https://opencapture.ys7.com/...
[INFO] No phone usage detected

============================================================
DETECTION SUMMARY
============================================================
  Total devices:     2
  Phone detected:    1
  Not detected:      1
  Failed:            0
  Alerts sent:       1
============================================================
```

## API 接口

| 接口 | URL | 文档 |
|------|-----|------|
| 获取 Token | `POST /api/lapp/token/get` | https://open.ys7.com/help/81 |
| 设备抓图 | `POST /api/lapp/device/capture` | https://open.ys7.com/help/687 |
| 玩手机检测 | `POST /api/service/intelligence/algo/analysis/play_phone_detection` | https://open.ys7.com/help/3956 |
| 语音上传 | `POST /api/lapp/voice/upload` | https://open.ys7.com/help/1241 |
| 语音下发 | `POST /api/lapp/voice/send` | https://open.ys7.com/help/1253 |

## 网络端点

| 域名 | 用途 |
|------|------|
| `open.ys7.com` | 萤石开放平台 API |
| `aidialoggw.ys7.com` | 萤石 AI 智能体 |
| `aliyuncs.com` | 萤石语音存储（阿里云 OSS） |

## 格式代码

**检测返回**:
- `images: null` - 图片中没有人
- `label: "play_phone"` - 检测到玩手机行为
- `labelWeight: 0.95` - 置信度 95%

**错误码**:
- `200` - 操作成功
- `10002` - accessToken 过期
- `10028` - 抓图次数超限
- `20007` - 设备不在线
- `20008` - 设备响应超时

## Tips

- **多设备**: 逗号分隔 `dev1,dev2,dev3`
- **指定通道**: 冒号分隔 `dev1:1,dev2:2`
- **Token 有效期**: 7 天，自动缓存
- **图片有效期**: 2 小时
- **频率限制**: 建议间隔 ≥4 秒
- **定时任务**: 建议 ≥5 分钟

## 注意事项

⚠️ **频率限制**: 萤石抓图接口建议间隔 4 秒以上，频繁调用可能触发限流（错误码 10028）

⚠️ **隐私合规**: 使用摄像头监控可能涉及隐私问题，确保符合当地法律法规

⚠️ **设备要求**: 设备必须在线且支持语音对讲功能（`support_talk=1` 或 `3`）

⚠️ **Token 安全**: Token 仅在内存中使用，不写入日志，不发送到非萤石端点

## 数据流出说明

**⚠️ 重要：本技能会向以下第三方服务发送数据**

| 数据类型 | 发送到 | 用途 | 是否必需 | 隐私影响 |
|----------|--------|------|----------|----------|
| 摄像头抓拍图片 | `open.ys7.com` (萤石) | AI 玩手机行为分析 | ✅ 必需 | 🔴 包含监控画面 |
| TTS 文本 | `edge-tts.microsoft.com` (Microsoft Azure) | 生成语音文件 | ✅ 必需 | 🟢 仅文本 |
| 语音文件 | `aliyuncs.com` (阿里云 OSS) | 临时存储，供设备下载 | ✅ 必需 | 🟡 临时存储 2 小时 |
| appKey/appSecret | `open.ys7.com` (萤石) | 获取访问 Token | ✅ 必需 | 🔴 凭据 |
| 设备序列号 | `open.ys7.com` (萤石) | 设备控制 | ✅ 必需 | 🟡 设备标识 |

**数据流出详细说明**:

1. **萤石开放平台** (`open.ys7.com`, `aidialoggw.ys7.com`):
   - 发送：摄像头抓拍图片、appKey/appSecret、设备序列号
   - 用途：Token 获取、AI 玩手机行为分析、设备控制
   - 隐私：🔴 包含监控画面和凭据

2. **Microsoft Azure TTS** (`edge-tts.microsoft.com`):
   - 发送：TTS 文本（"检测到有人玩手机，请立即停止使用手机！"）
   - 用途：生成语音文件
   - 隐私：🟢 仅固定文本，不包含个人信息

3. **阿里云 OSS** (`aliyuncs.com`):
   - 发送：生成的语音文件（.mp3）
   - 用途：临时存储，供萤石设备下载播放
   - 隐私：🟡 临时存储 2 小时，自动过期
   - 存储位置：萤石合作的阿里云 OSS 存储桶

**数据不流出**:
- ❌ 不会发送数据到技能作者或任何个人
- ❌ 不会发送到 ClawHub 或 OpenClaw
- ❌ 不会永久存储任何数据

**凭证安全建议**:
- 使用**最小权限**的 appKey/appSecret（仅需设备控制和 AI 分析权限）
- 定期轮换凭据
- 不要使用主账号凭据
- 限制凭据的 IP 访问范围（如果萤石支持）

**凭证权限建议**:
- 使用**最小权限**的 appKey/appSecret
- 仅开通必要的 API 权限（设备抓图、AI 分析、语音）
- 定期轮换凭证
- 不要使用主账号凭证

**本地处理**:
- ✅ Token 缓存于内存，不写入磁盘
- ✅ 不记录完整 API 响应
- ✅ 不保存抓拍图片到本地（除非手动指定下载路径）
