---
name: feishu-bgm
description: >
  飞书场景化背景音乐生成器。通过 MiniMax Music API 生成纯音乐 BGM，以音频消息发送到飞书群。
  触发词："来点BGM"、"开会背景音"、"加班音乐"、"头脑风暴BGM"、"会议音乐"、"工作BGM"、
  "放点音乐"、"背景音乐"、"需要BGM"。当用户在飞书群中描述场景并希望获得背景音乐时激活。
---

# 飞书 BGM — 场景化背景音乐生成器

根据工作场景生成纯音乐 BGM，通过飞书音频消息即时送达群聊。

**依赖**：MiniMax CLI（`mmx-cli`）+ Token Plan

---

## 快速配置（首次使用）

### 1. 安装 MiniMax CLI

```bash
npm install -g mmx-cli
```

> 需要 Node.js 18+。完整文档：https://github.com/MiniMax-AI/cli

### 2. 订阅 Token Plan

前往 MiniMax 平台订阅 Token Plan（音乐生成需要额度）：
- 🇨🇳 国内：https://platform.minimaxi.com/subscribe/token-plan
- 🌍 海外：https://platform.minimax.io/subscribe/token-plan

### 3. 登录认证

```bash
# 方式一：API Key 登录（推荐，从平台「接口密钥」页获取）
mmx auth login --api-key sk-xxxxx

# 方式二：浏览器 OAuth 登录
mmx auth login
```

### 4. 验证

```bash
# 检查登录状态
mmx auth status

# 检查剩余额度
mmx quota

# 测试生成一首 BGM
mmx music generate --prompt "calm piano, ambient" --instrumental --out /tmp/test_bgm.mp3
```

全部通过即可使用本 Skill。

---

## 场景预设表

用户描述模糊时，从预设匹配最近场景；描述具体时，直接用用户描述构建 prompt。

| 场景关键词 | 风格 | BPM | 情绪关键词 |
|-----------|------|-----|-----------|
| 开会/会议/讨论 | Ambient, Minimal | 70-90 | calm, professional, subtle |
| 头脑风暴/创意 | Electronic, IDM | 100-120 | creative, energetic, playful |
| 加班/赶工/冲刺 | Lo-fi, Chillhop | 85-95 | focused, determined, warm |
| 放松/休息/午休 | Bossa Nova, Jazz | 90-110 | relaxed, smooth, cozy café |
| 庆祝/发布/上线 | Funk, Disco | 115-125 | celebratory, groovy, uplifting |
| 复盘/总结/回顾 | Piano, Classical | 60-80 | reflective, thoughtful, gentle |
| 面试/1on1 | Acoustic, Folk | 80-100 | warm, comfortable, welcoming |
| 站会/日会 | Pop, Indie | 110-120 | light, breezy, efficient |

---

## 工作流

### Step 1: 解析用户意图

从用户消息中提取：
- **场景**：匹配上表或自由描述
- **时长偏好**：默认不指定（API 生成约 2 分钟）
- **特殊要求**：如"不要鼓点"、"要有钢琴"

### Step 2: 构建 Prompt 并生成

优先使用 CLI（无需管理 API Key），回退到 Python 脚本：

```bash
# 方式一：MiniMax CLI（推荐）
mmx music generate \
  --prompt "<constructed prompt>" \
  --instrumental \
  --out /tmp/openclaw/bgm_<scene>.mp3

# 方式二：Python 脚本（需要 MINIMAX_API_KEY 环境变量）
python3 scripts/generate_bgm.py \
  --prompt "<constructed prompt>" \
  --output /tmp/openclaw/bgm_<scene>.mp3
```

**Prompt 构建规则**：
```
<style>, instrumental, <mood keywords>, <instrument hints>, <BPM> BPM, 
background music for <scene description>, no vocals, professional and clean mix
```

示例：
```
Ambient, Minimal, instrumental, calm, professional, subtle, 
soft piano, warm pads, gentle strings, 80 BPM, 
background music for a team meeting, no vocals, professional and clean mix
```

### Step 3: 发送到飞书

生成完成后，使用 `message` 工具发送音频文件到当前群聊：

```
message(action="send", filePath="/tmp/openclaw/bgm_<scene>.mp3", 
        message="🎵 <场景名> BGM 已就绪")
```

### Step 4: 响应格式

发送后回复：
```
🎵 BGM 已送达！
场景：<场景描述>
风格：<风格>
适合：<使用建议>

💡 不满意可以说「换一首」或描述你想要的风格
```

---

## 快捷指令

| 用户说 | 动作 |
|--------|------|
| "换一首" / "再来一首" | 同场景重新生成 |
| "要欢快一点的" | 调整情绪关键词重新生成 |
| "不要鼓" / "加点吉他" | 修改乐器提示重新生成 |
| "停" / "够了" | 结束，不再生成 |

---

## 生成方式

### 方式一：MiniMax CLI（推荐，零代码）

CLI 自动管理认证和 region，无需手动传 API Key：

```bash
mmx music generate \
  --prompt "<prompt>" \
  --instrumental \
  --out /tmp/openclaw/bgm_<scene>.mp3
```

### 方式二：Python 脚本（需要 API Key）

`scripts/generate_bgm.py` 直接调用 MiniMax Music API：

- 读取 API Key：从环境变量 `MINIMAX_API_KEY` 获取
- 模型：`music-2.5+`
- 固定参数：`is_instrumental: true`，`output_format: url`
- 音频设置：44100 Hz，256kbps，MP3
- 超时：300 秒

---

## 错误处理

| 错误 | 处理 |
|------|------|
| API 超时 | 告知用户生成较慢，自动重试一次 |
| 生成失败 | 提示用户换个描述试试 |
| 余额不足 | 告知用户 API 额度用完 |

---

## 注意事项

- 只生成**纯音乐**（instrumental），避免人声歌曲作为 BGM
- 默认不加水印（`aigc_watermark: false`）
- 单次生成约 2 分钟音频，适合单曲循环
- 生成耗时约 60-120 秒，需提前告知用户等待
