# 搜索策略

## 1. 关键词生成规则

从目标工具提取两套关键词：

1. **中文关键词**：工具名 + 平替/免费/开源/自托管 + 品类词
2. **英文关键词**：工具名 + alternative/free/open source/self-hosted + 品类词

**示例**（目标 Notion）：
- 中文：`Notion 平替`、`Notion 免费替代`、`开源笔记软件`、`自托管知识库`
- 英文：`notion alternative`、`free notion alternative`、`open source wiki`、`self-hosted notion`

分层规则见 SKILL.md 第 4 节（L1-L5），搜索前必须出表并经用户回复「1」确认。

## 2. 渠道优先级（16 渠道四梯队）

### 2.1 第一梯队：结构化 API 搜索（覆盖面最广，有评分/下载量）
1. SkillHub — 8.7万 Skill，语义搜索
2. SkillsMP — 164万文件，全球最大索引
3. AlternativeTo — 最专业替代品库，license 字段可判免费属性

### 2.2 第二梯队：CLI 生态（安装最方便）
4. ClawHub — OpenClaw 生态，一键安装
5. Vercel Skills — 67万 Skill，前端/部署相关

### 2.3 第三梯队：GitHub 直接（全量开源，需人工筛选）
6. GitHub repos — 全量搜索，覆盖最广
7. awesome-selfhosted — 自托管免费软件金标准，license 标注全
8. awesome-agent-skills — 380+ 精选列表，技能向
9. Anthropic 官方 — 官方白名单，零审计风险

### 2.4 第四梯队：社区与全网（口碑佐证，辅助补充）
10. HackerNews（Algolia）— Show HN + 老鸟讨论
11. Reddit — 真实用户评价与避坑
12. Product Hunt — 新产品/免费竞品
13. WebSearch（DuckDuckGo）— 全网兜底
14. 虾评 — 中文社区（需 XIAPING_KEY）
15. 小红书 — 中文口碑，AI 手动辅助
16. Coze 技能商店 — 需登录，AI 手动辅助

## 3. 推荐优先级铁律（免费 > 付费，不可被渠道覆盖率覆盖）

1. **四级分类**：每个候选必须标注付费属性——
   - `免费开源`：GitHub / 自托管 / MIT、Apache、GPL 等可零成本自托管
   - `免费额度`：SaaS 免费档（有限次/有水印/功能阉割）
   - `未验证`：license 不明，需人工确认
   - `付费`：按次 / 订阅收费
2. **硬排序**：免费开源 > 免费额度 > 未验证 > 付费；同档内按 stars/downloads 降序，无数据标「未验证」排同档末尾。
3. **打分公式**（脚本内置）：`score = tier_weight + min(20*log10(stars+1), 100)`，tier_weight：免费开源 100 / 免费额度 60 / 未验证 30 / 付费 0。log10 刻度保证同档内 star 数严格保序，同时避免巨星级仓库压倒档位分层。
4. **分组展示**：先列免费开源组，再列免费额度组，最后其余候选。
5. **每条结果必带标签**：`[免费开源] ★2.3k` 格式。

## 4. 去重合并规则

1. 同名工具（GitHub 去掉 owner 前缀后名称相同）→ 保留得分最高的渠道结果，渠道字段合并标注。
2. 功能重叠（描述相似度 > 70%）→ 合并为一条，标注多个来源。
3. 最终展示按优先级铁律分组，注明来源渠道与付费属性标签。

## 5. 本地优先检查

展示结果前，先检查本地是否已有相关技能/工具沉淀：

```bash
ls ~/.workbuddy/skills/ | grep -i "{keyword}"
ls ~/.workbuddy/skills-marketplace/skills/ 2>/dev/null | grep -i "{keyword}"
```

本地已有 → 在报告「本地已有相关」节说明，避免重复推荐。

## 6. 渠道可用性自检

搜索前跑 `alt_search.py --check`，不可用的渠道跳过，在结果报告中注明。

## 7. 无结果处理

如果 16 个渠道都无结果：

1. 告知用户「十六渠道均未找到匹配平替」
2. 进入 AI 自研可行性评估（S/A 级则给最小可行自研方案）
3. 询问是否需要帮助直接开发

```
已扫完 16 渠道：均未找到「{目标工具}」的免费平替。

下一步两个选项：
1. 按 S/A 级标准评估自研，我出最小可行方案
2. 换更宽的关键词再扫一轮

你选哪个？
```
