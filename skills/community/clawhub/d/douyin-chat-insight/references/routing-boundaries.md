# 路由边界

| 用户意图 | 去向 |
|----------|------|
| 公开抖音主页 / 博主作品结构 | `douyin-creator-insight` |
| 主页最新 N 条视频文案 | `douyin-video-analyst` / `douyin-workflow` |
| 群聊/私聊导出里有啥价值 | **`douyin-chat-insight`** |
| 分享视频单条 ASR | **可选端口**：见 `optional-douyin-link-asr.md`（指导/路由）；核心 `run.py` 不自动云 ASR |
| 群内抖音链接但只要文字情报 | 仍用本 skill；无需 Key |
| 「帮我静默导出任意抖音群」 | **拒绝主路径**；指向 how-to-get-exports |

## 为何不是附属 skill

- 公开安装不能绑 IM cookie / 浏览器 profile
- 与「公开创作者研究」是两类产品
- README 互链，零 required 依赖

## workflow 一行

聊天导出价值分析 → `douyin-chat-insight`：先 inventory，再 analyze。
