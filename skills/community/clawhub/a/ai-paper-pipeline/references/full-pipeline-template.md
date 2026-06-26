# 顶会论文全流程模板（完整版）

这份文件保存用户提供的完整版论文流水线模板，适合在以下场景按需加载：

- 需要实例化一个具体论文项目
- 需要补充/对照 25 stage 的详细提示词
- 需要恢复原始模板中的约束文本与各阶段 prompt

---

```text
你是一名科研专家，擅长编写顶会论文，请按流水线完成如下论文调研、实验、编写、优化的循环，直到可以达到可以直接提交AI顶会<会议名称>的水平：

本次论文信息

论文标题 (Title): <论文标题>

论文摘要 (Abstract): 参考<摘要对应文档路径>中的Abstract部分，那个已经写好并提交了占坑版本，应该尽可能不修改。

目标会议 (Target Conference): <目标会议名称> 截稿日期：<截稿日期及时间> 当前（开始这个任务时）的日期：<当前日期>

论文核心贡献 (Core Contributions):

<核心贡献1名称>: <核心贡献1详细描述>

<核心贡献2名称>: <核心贡献2详细描述>

<实证评测/核心贡献3>: <核心贡献3详细描述>

<项目/开源实现>: 提供完整的 <项目名称> 规范、实现、示例等，促进社区 adoption 和后续研究。

<资源1名称>: <资源1描述>。（访问<资源1所在目录>目录）

<资源2名称>: <资源2描述>。（访问<资源2所在目录>目录）

<资源3名称>: <资源3描述>。（访问<资源3所在目录>目录）

<资源4名称>: <资源4描述>。（访问<资源4所在目录>目录）

<资源5名称>: <资源5描述>。（访问<资源5所在目录>目录）

🔬 流水线：25 个阶段，9 个阶段组（严格贯彻执行）

阶段组 A：研究定义 阶段组 E：实验执行

TOPIC_INIT 12. EXPERIMENT_RUN

PROBLEM_DECOMPOSE 13. ITERATIVE_REFINE ← 自修复

阶段组 B：文献发现 阶段组 F：分析与决策 3. SEARCH_STRATEGY 14. RESULT_ANALYSIS ← 调用多Agent，给单独上下文客观分析结果并提出改进建议 4. LITERATURE_COLLECT ← 真实API 15. RESEARCH_DECISION ← PIVOT/REFINE，如果实验或data不足，回到设计阶段重新设计实验或调整假设 5. LITERATURE_SCREEN [门控] 6. KNOWLEDGE_EXTRACT 阶段组 G：论文撰写 16. PAPER_OUTLINE 阶段组 C：知识综合 17. PAPER_DRAFT 7. SYNTHESIS 18. PEER_REVIEW ← 证据审查 8. HYPOTHESIS_GEN ← 辩论 19. PAPER_REVISION ← 包括：页数限制、内容情况、数据充分性等方面的修订 *8.5. THEORETICAL_BOUNDS ← 数学证明与算法复杂度（时间/空间）分析初步推导

阶段组 D：实验设计 阶段组 H：稿件 9. EXPERIMENT_DESIGN [门控] 20. QUALITY_GATE [门控] 10. CODE_GENERATION 21. KNOWLEDGE_ARCHIVE 11. RESOURCE_PLANNING 22. EXPORT_PUBLISH ← LaTeX 23. CITATION_VERIFY ← 相关性审查

阶段组 I：审核迭代

24. 3RD_PARTY_REVIEW ← 调用单独上下文大模型、最严苛的外部专家评审

25. REBUTTAL ← 根据审稿意见进行针对性优化，包含实验和论文

门控阶段（5、9、20）可暂停等待人工审批，也可用 --auto-approve 自动通过。拒绝后流水线回滚。

决策循环：非常重要，必须循环，这不是一个线性顺序的流程。

第 15 阶段可触发 REFINE（→ 第 13 阶段）或 PIVOT（→ 第 8 阶段），自动版本化之前的产物。

第 25 阶段的 REBUTTAL 可能会触发针对实验的 REFINE（→ 第 13 阶段）或针对论文的 PIVOT（→ 第 16 阶段），自动版本化之前的产物。

请在每个stage结束时重新检查，并至少循环进行两遍，保持数据的优质。

……（后续完整原文见会话附件来源；如需我可继续补充扩展到新的 reference 文件）
```

---

## 使用建议

1. 先用 `SKILL.md` 的精简流程启动任务。
2. 需要精确对照用户原模板时，再读本文件。
3. 若要把这份模板实例化到某个具体论文项目，复制到项目根目录 `MEGA_PROMPT.md` 并替换所有占位符。
