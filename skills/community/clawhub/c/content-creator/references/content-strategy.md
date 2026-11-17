# 内容策略与平台适配 playbook

> 在写第一条脚本之前，先回答三个问题：为谁做、在哪发、解决什么。本 playbook 给一套决策树 + 平台矩阵 + 常见坑。

## 1. 决策树：从 0 定内容方向

```
Q1 你的核心媒介是什么？
├─ 短视频/动态 → 抖音/快手/Reels/Shorts/TikTok → 走「短视频脚本」子技能
├─ 长视频/教程 → B站/YouTube → 走「视频编辑」+「YouTube 运营」
├─ 音频/访谈 → 播客 → 走「播客制作」
└─ 文字深度 → 博客/公众号 → （不在本库，转 writer-studio）

Q2 你的目标是什么？
├─ 涨粉/曝光 → 选题追趋势 + Hook 前置 + 高频更新
├─ 转化/带货 → 痛点开场 + 信任背书 + 明确 CTA
└─ 建立权威 → 系列化深度 + 信息增益 + 人设一致

Q3 你一周能稳定产出几条？
├─ <1 条 → 做精不做多，长视频/播客建立壁垒
└─ ≥3 条 → 短视频走量，用模板化脚本提效
```

**经验法则**：先在一个平台打透，再跨平台改编，不要一开始就全平台铺开。

## 2. 平台矩阵（速查）

| 平台 | 内容形态 | 关键指标 | 适配子技能 |
|------|----------|----------|------------|
| 抖音/快手 | 15-60s 短视频 | 完播率、互动 | short-video-script |
| YouTube | 长视频/短视频 | 观看时长、CTR | video-editing + youtube-automation |
| B站 | 中长视频 | 三连、弹幕 | video-editing |
| 小红书 | 图文+短视频 | 收藏、笔记 | short-video-script |
| 播客 | 音频 | 订阅、完播 | podcast-generation |

## 3. 选题方法论（避免自嗨）

1. **痛点优先**：从评论区、搜索词、竞品高赞里挖真实问题。
2. **信息增益**：你比现有内容多给什么？少做 AI 共识搬运。
3. **系列化**：一个爆款拆成 3-5 期，降低持续选题压力。
4. **可验证**：每条内容定一个假设（如"教程类完播更高"），发布后回看数据。

## 4. 发布前检查清单

- [ ] 受众与平台已明确（不是"全平台都发"）
- [ ] 开头 3 秒有 Hook（短视频）/ 标题与缩略图已优化（长视频）
- [ ] 一条内容只承载一个核心信息
- [ ] CTA 明确（关注/收藏/购买）
- [ ] 标题/标签覆盖目标搜索词

## 5. 常见坑

- **盲目追热点**：热点不对受众，流量来了也留不住。
- **重制作轻策略**：画面精美但没人看，因为没想清楚给谁看。
- **更新断更**：算法认持续更新， sporadic 发布难以起量。
- **忽略数据**：凭喜好做内容，不看留存曲线，永远不知道哪里流失。

## 6. 相关子技能与层次边界

本 playbook 是「策略层」方法论（L2），负责选题与平台定调；具体环节的产出落地下沉到 L3 子技能：

- 选题落到短视频脚本 → [skills/short-video-script/SKILL.md](../skills/short-video-script/SKILL.md)
- 长视频 / 教程制作与剪辑 → [skills/video-editing/SKILL.md](../skills/video-editing/SKILL.md)
- 缩略图 / SEO / 发布排期 / 数据分析 → [skills/youtube-automation/SKILL.md](../skills/youtube-automation/SKILL.md)
- 音频 / 访谈制作 → [skills/podcast-generation/SKILL.md](../skills/podcast-generation/SKILL.md)
- 邮件通讯 / 简报编排（编辑类，非本策略 playbook 范围）→ [skills/newsletter/SKILL.md](../skills/newsletter/SKILL.md) 与其 [references/newsletter-playbook.md](newsletter-playbook.md)
- 文字深度内容（博客 / 公众号）→ 不在本库，跨仓库调 `writer-studio`

边界：本 playbook 只给"为谁 / 在哪 / 做什么"的决策树与矩阵，不写具体脚本或剪辑操作；这些交给对应子技能。
