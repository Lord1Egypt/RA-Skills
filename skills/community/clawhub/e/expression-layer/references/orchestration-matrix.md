# 路由编排矩阵（完整版）

本文件维护 expression-layer 的完整路由映射，新增 skill 需同步更新。

---

## 核心路由表

| 意图标识 | 输入类型 | 编排路径 | 输出形式 | 依赖 Skill | 状态 |
|---------|---------|---------|---------|-----------|------|
| `plain` | 概念/问题/术语 | `ljg-plain` | 大白话文本（≤200字） | ljg-plain | ✅ |
| `writes` | 素材/草稿/观点 | `ljg-writes` → `humanizer-zh` | 深度文章（1000-1500字） | ljg-writes, humanizer-zh | ✅ |
| `card` | 文本/数据/图表 | `ljg-card`（-l/-i/-c/-w/-b） | PNG 卡片 | ljg-card | ✅ |
| `present` | 文本/大纲 | `ljg-present` | HTML 高桥流 | ljg-present | ✅ |
| `paper_flow` | 论文链接/PDF | `ljg-paper` → `ljg-card` | 解读Markdown + PNG | ljg-paper, ljg-card | ✅ |
| `word_flow` | 英文单词 | `ljg-word` → `ljg-card` | 解析Markdown + PNG | ljg-word, ljg-card | ✅ |
| `travel` | 城市/主题 | `ljg-travel` | 研究报告 + PNG卡片 | ljg-travel | ✅ |
| `wechat` | 完整文章/解读 | `wechat-publisher` | 公众号推文（HTML+封面） | wechat-publisher | ✅ |

---

## 扩展路由（待集成）

| 意图标识 | 输入类型 | 编排路径 | 输出形式 | 依赖 Skill | 状态 |
|---------|---------|---------|---------|-----------|------|
| `video` | 脚本/大纲 | `ljg-card(-v)` → 视频生成 | MP4 短视频 | ljg-card, 视频API | 🟡 规划中 |
| `audio` | 文本 | TTS 引擎 | MP3 语音条 | TTS API | 🟡 规划中 |
| `interactive` | 题库/知识点 | 互动测验生成 | HTML 互动页 | 测验引擎 | 🟡 规划中 |
| `report` | 数据/指标 | 数据可视化 | PDF/HTML 报告 | 报表引擎 | 🟡 规划中 |

---

## 新增 Skill 集成规范

1. **准备阶段**
   - 确保 skill 有 `SKILL.md` 和明确输入输出
   - 测试 skill 独立运行正常

2. **路由配置**
   - 在上方表格新增一行
   - 定义意图标识（小写+下划线）
   - 明确编排路径（单步/串联/并行）
   - 标注依赖 skill 和状态

3. **SKILL.md 同步**
   - 更新 `路由编排矩阵` 表格
   - 更新 `allowed-tools`（如需新工具）
   - 更新 `related_skills`

4. **版本管理**
   - 新增路由 → `patch` 版本（1.0.0 → 1.0.1）
   - 修改路由逻辑 → `minor` 版本（1.0.0 → 1.1.0）
   - 破坏性变更 → `major` 版本（1.0.0 → 2.0.0）

---

*最后更新：2026-04-24*
