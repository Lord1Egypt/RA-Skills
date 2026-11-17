---
name: easypost
description: 使用 EasyPost CLI 通过日常 Chrome 浏览器将图文笔记与短视频一键自动填充或发布到全网各大社交平台。Use when 用户需要将内容批量分发到小红书、抖音、微信视频号、B站、快手、微博、X、Instagram 等多个平台。
license: MIT-0
slug: easypost
displayName: EasyPost 多平台极速分发总入口
version: 1.0.0
summary: 基于真实 Chrome 浏览器 Native Messaging 桥的多平台零风控自动分发。
---

# EasyPost 跨平台极速分发总入口

EasyPost 通过 Chrome Native Messaging 机制直接复用用户日常真实浏览器中的登录状态，无需配置 Cookie、密码或 API 密钥，零 CDP 探针暴露，支持多平台并发一键填充。

## 平台与对应独立 Skill 入口

| 平台 | 专用 Skill | 平台标识 (platform id) | 支持内容形态 |
| :--- | :--- | :--- | :--- |
| **小红书** | `xiaohongshu-upload` | `xiaohongshu` | 图文笔记 (imageText) / 短视频 (shortVideo) |
| **抖音** | `douyin-upload` | `douyin` | 短视频 (shortVideo) / 图文笔记 (imageText) |
| **视频号** | `shipinhao-upload` | `shipinhao` | 短视频 (shortVideo) |
| **Bilibili** | `bilibili-upload` | `bilibili` | 视频 (shortVideo) / 动态 (dynamic) |
| **快手** | `kuaishou-upload` | `kuaishou` | 短视频 (shortVideo) / 图文 (imageText) |
| **微博** | `weibo-upload` | `weibo` | 动态图文 (dynamic) / 视频 (shortVideo) |
| **X (Twitter)**| `x-upload` | `x` | 动态图文 (dynamic) / 视频 (shortVideo) |
| **Instagram** | `instagram-upload` | `instagram` | 图文笔记 (imageText) / 视频 (shortVideo) |

---

## 核心工作流程与原则

1. **环境检查**：执行任何发布前，先运行 `easypost doctor` 确保 Chrome 扩展在线。若未在线，提示用户打开 Chrome 浏览器或安装扩展。
2. **多平台组合优先**：若用户要发布到多个平台，优先利用组合（如 `comboName: "通用（国内）"` 或 `platforms: ["xiaohongshu", "douyin", "shipinhao"]`）进行并发派发。
3. **安全模式原则**：
   - 默认推荐 `easypost fill`（自动打开平台页面、上传媒体、填入标题文案与标签，留待创作者在网页上亲自核验后点击发布）；
   - 只有当用户明确要求直接全自动发布时，才使用 `easypost publish --yes`。
4. **素材准备**：本地媒体路径必须为绝对路径，封面支持宽高比自动分流（竖版 9:16 为 `cover`，横版 16:9 为 `horizontalCover`）。

---

## 快速调用示例

### 1. 多平台并发填充任务（JSON 输入）
```bash
printf '%s\n' '{
  "type": "imageText",
  "platforms": ["xiaohongshu", "douyin"],
  "data": {
    "title": "今日高效创作技巧分享",
    "content": "分享一套极简多平台分发工作流... #创作工具 #生产力",
    "tags": ["创作工具", "生产力"]
  },
  "assets": [
    {
      "path": "/absolute/path/to/image1.png",
      "role": "media"
    }
  ]
}' | easypost fill
```

### 2. 查询任务执行结果
```bash
easypost status <requestId>
```

---

## 安装与 Skill 分发
从 `skills.sh` 安装本 Skill：
```bash
npx skills add gybin02/easypost --skill easypost
```
