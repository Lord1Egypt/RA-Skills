# BiliYouTik2Brain 全量复查 · 2026-05-15

以慢学AI《skill》13集方法论为第一性原理参照，
对 BiliYouTik2Brain 技能自身的结构与工程质量进行全面审视。

## 参照标准

| 来源 | 核心原则 |
|:----|:---------|
| Anthropic P01-P03 | 渐进式披露、认知/执行分离、Eval-first、人机共创 |
| Google P04 | 5种设计模式：ToRapper/Generator/Reviewer/Inversion/Pipeline |
| Claude Code P05-P07 | 9类能力地图、Gotchas>教程、约束目标不约束路径、Hooks |
| OpenAI P08-P09 | Eval-first方法论、4类测试集、运行时轨迹 |
| Perplexity P11-P13 | 上下文税、逆向5原则、Eval-Gotcha飞轮、3类问题分类 |

## ✅ 做得好

### 1. Pipeline 设计模式（Google P04）
- `pipeline_graph.py`: 拓扑排序→分层并行→7节点DAG
- 30+真实视频验证（院长×21+熊猫+张聚贤+skill合集×13+抖音×4）
- 零数据丢失，生产级稳定性

### 2. 认知与执行分离（Anthropic P02）
- 认知节点（collect→assess→enhance）: LLM驱动
- 执行节点（transcribe→ocr→save→update_knowledge）: 代码驱动
- 只有需要思考的部分进 LLM 上下文

### 3. 三层缓存经济（Perplexity P11）
- Index层: SKILL.md（86行，~3KB，轻量）
- Load层: LLM缓存（~1.2MB，重复视频不走 API）
- Runtime层: raw缓存（~315KB，清LLM缓也不触发重新转录）
- **超越理论——P11只提出三层税概念，BiliYouTik2Brain实现了三层缓存**

### 4. 蜂群模式 ≈ Eval-Gotcha 飞轮雏形（Perplexity P13）
- 3000+字自动切块→并行LLM修复→JSON拼接
- 每块独立置信度评估→综合置信度
- 每次修复自带评估：修改→置信度→不通过→修→再评估

### 5. 纠错词典 = Gotchas知识积累（Claude Code P06）
- 说话人分类纠错 + 语境保护
- 示例："做→说"只在吴江说话语境执行，"孕线"永不改成"均线"
- 这正是 P06 说的 Gotchas > Tutorials——抽象方法论到处都是，踩坑才是稀缺资产

## ❌ 待改进（已按优先级执行）

| P | 项目 | 发现 | 已执行 |
|:-:|:----|:-----|:------:|
| P0 | 置信度写入bug | skill-batch.py line162: `result.get('confidence_score')` 但值在`result['analysis']`子结构 | ✅ |
| P0 | 历史备份积压 | v1.4.0/v1.5.0 两个旧 `.py` 备份在发布版目录 | ✅ |
| P1 | 无Eval测试集（最大短板） | 0个回归测试，修改后无法验证是否变好/变坏 | ✅ |
| P2 | Description缺路由信号 | 200字场景列表，无"不触发"信号 | ✅ |
| P2 | SKILL.md混搭开发者文档 | 包含`pip show faster-whisper`等依赖检查段落 | ✅ |
| P2 | 知识库偏瘦 | 30+视频处理→knowledge/只2文档655行 | ✅ `_node_auto_archive` |
| P2 | 合集自动分解 | 仅支持单链接，合集需手写batch脚本 | ✅ `list_collection()` |
| P3 | VAD自适应 | P15(124min)因curl E2BIG失败 | ✅ v1.7.0已实现（资源公式驱动） |

## Lessons 提炼

### [CODE] 输出字段路径一致性
**When:** batch脚本从pipeline函数读取嵌套返回结构
**Do:** 先检查返回结构（print或debug），再写字段路径
**Don't:** 假设结构是扁平的，直接从 `result.get('confidence_score')`
**Why:** 2026-05-15 skill-batch.py 13个视频置信度全部 N/A 因为 `confidence_score` 在 `result['analysis']` 子结构中，不在顶层。批处理运行正常但数据质量有漏洞。

### [ARCH] Perplexity 上下文税原则
**When:** 设计技能时（SKILL.md、参考文档、模板）
**Do:** 每段文本都问"这段需要每次加载吗？"——不需要则卸载到 `docs/` 或 `references/`
**Don't:** 把所有东西堆在 SKILL.md 里
**Why:** P11 指出每行字都是向所有用户收的税。BiliYouTik2Brain 的`## 依赖检查`（10行，占12%）和 BG 吴江的`九层打法`（120行，占32%）都是不需要每次加载的内容。
