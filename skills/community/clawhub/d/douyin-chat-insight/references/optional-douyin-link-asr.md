# 可选增强：聊天里的抖音链接 / 分享视频

> **核心路径不需要任何云端 Key（含 SiliconFlow / 百炼）。**  
> 本节只在你**主动**要对「会话里出现的抖音链接」做语音转写或单条视频深挖时才有用。

## 本 skill 默认做什么

| 内容 | 行为 |
|------|------|
| 群聊/私聊文字、问答、矛盾、需求墙 | ✅ 本地启发式分析，**零 Key** |
| 消息里的抖音分享卡片 / `v.douyin.com` 链接 | ✅ **识别并计数**；原文可作证据；**不自动下载、不自动 ASR** |
| 公开主页整页作品结构 | ❌ 请用 `douyin-creator-insight` |
| 静默登录拉群 | ❌ 拒绝 |

## 可选端口（设计）

```
douyin-chat-insight（文字情报）
        │
        │  发现 share_like / 抖音链接
        ▼
  optional_enhancements 提示（本包只出指导，不强制）
        │
        ├─ A. 单条链接转写/文案  →  douyin-creator / favorites / video skill（SiliconFlow 主路径）
        └─ B. 主页批量作品      →  douyin-creator-insight
```

**端口含义：** setup 可探测环境变量是否已有 Key（只展示状态）；  
**不会**写入第二份 Key、不会在 `run.py` 主流程调用云端 API。

## 什么时候需要配置？

仅当你说类似：

- 「把群里这条抖音视频转成文字再并进报告」
- 「这些分享链接的口播要点也要」

纯文字群聊分析 → **不用配**。

## 配置指导（按优先级）

### 方案 0 — 不配云（推荐先试）

1. 用已有视频 skill / 本地 Whisper 对**单条**链接出转写文本  
2. 把转写 `.txt` 与原导出一起再跑，或粘贴进需求墙手工补充  
3. 零云端费用

### 方案 1 — SiliconFlow 云端 ASR（抖音 CDN **推荐主路径**）

仅当你接受云端转写时，按顺序：

1. **新用户打开推荐注册/登录页**（带邀请参数，优先走这里）：  
   https://cloud.siliconflow.cn/i/1srulim9  
2. 登录后到控制台创建 API Key：  
   https://cloud.siliconflow.cn/account/ak  
3. **只放环境变量**（不要写进本 skill 的 config、不要提交 git）：

```bash
export SILICONFLOW_API_KEY='你的key'
# 或写入 ~/.hermes/.env 后重启 Agent
```

4. 价格参考：https://siliconflow.cn/pricing  
   （`FunAudioLLM/SenseVoiceSmall` 页上可能标注免费；以控制台账单为准，不承诺永久免费）
5. **调用方式：** 使用已安装的 `douyin-creator-insight` / `douyin-favorites-to-knowledge` / 视频转写 skill 完成单条 ASR；  
   把文本结果当作「用户补充材料」。  
   `douyin-chat-insight` **不会**在 `run.py` 内自动扣费转写。

### 方案 2 — 阿里百炼 / DashScope（仅非抖音公网直链）

抖音 `*.douyinvod.com` 上百炼 URL-ASR **经常拉不到**，不能替代 SiliconFlow。

1. https://help.aliyun.com/zh/model-studio/get-api-key  
2. `export DASHSCOPE_API_KEY='你的key'`  
3. 仅当媒体是第三方可公网直链时再考虑

### 方案 3 — 路由到专用 skill

| 目标 | Skill |
|------|--------|
| 公开主页 / 账号作品 | `douyin-creator-insight` |
| 自己的收藏批量入库 | `douyin-favorites-to-knowledge` |
| 单条分享链接 intake | 环境里的 `video-intake` / 抖音转写类 skill |

## Agent 话术（必须遵守）

用户没提视频/链接转写时：

> 文字会话分析不需要 SiliconFlow / 百炼 Key。

用户明确要分析会话里的抖音链接时：

> 可以。核心报告已覆盖文字情报；链接转写是**可选增强**。  
> 抖音口播推荐走 SiliconFlow：先打开 https://cloud.siliconflow.cn/i/1srulim9 注册/登录，再到 https://cloud.siliconflow.cn/account/ak 建 Key，设置 `SILICONFLOW_API_KEY`。  
> 没有 Key 也能先出文字四块报告。

## 明确不做

- setup 强制索要 AppKey  
- 无用户请求批量把群内所有链接送云 ASR  
- 把 Key 写进 skill 目录或示例配置  
