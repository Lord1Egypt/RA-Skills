# Skill: Deep Research Pro
> 版本：2.0.0
> 描述：世界领先的深度研究技能，支持多阶段迭代、交叉验证、批判分析

## 触发条件
当用户要求进行深度研究、市场调研、学术论文检索、竞品分析时自动激活。

## 支持的命令格式
- `/research <主题> [--depth shallow|medium|deep]`
- `深度调研 <主题>`
- `研究 <主题> 的市场/技术/竞品`
- `帮我查一下 <主题> 的学术论文`

## 研究阶段（强制顺序执行）

### Phase 1: 研究规划 (Research Planning)
**目标**：明确研究问题、定义边界、设计检索策略
**输出**：`research-plan.md`
**必须包含**：
- 核心研究问题（3-5 个）
- 检索关键词矩阵（主关键词 + 同义词 + 相关概念）
- 数据源清单（学术/行业/政策/专利）
- 质量评估标准（纳入/排除标准）
- 预期产出结构

### Phase 2: 多源检索 (Multi-Source Retrieval)
**目标**：从多源获取信息，避免单一来源偏见
**输出**：`sources/raw-sources.json`
**必须包含**：
- 学术：OpenAlex/PubMed/Google Scholar（至少 15 篇核心论文）
- 行业：公司官网/行业报告/竞品文档（至少 5 个竞品）
- 政策：政府文件/监管机构/标准组织（如适用）
- 专利：Google Patents/WIPO（如适用）
- 每个来源必须有：URL、发布时间、作者/机构、摘要

### Phase 3: 质量筛选 (Quality Screening)
**目标**：过滤低质量信息，保留高可信度来源
**输出**：`sources/filtered-sources.json` + `sources/excluded-sources.json`
**评估维度**：
| 维度 | 权重 | 评估标准 |
|------|------|----------|
| 来源权威性 | 30% | 顶刊/知名机构/官方来源 |
| 时效性 | 25% | 近 3 年优先，经典文献可放宽 |
| 方法论严谨性 | 25% | 样本量、对照组、统计方法 |
| 可复现性 | 10% | 数据/代码是否公开 |
| 利益冲突披露 | 10% | 是否声明资助方/利益关系 |

### Phase 4: 深度分析 (Deep Analysis)
**目标**：提取关键洞察，而非简单摘要
**输出**：`analysis/insights.md`
**必须包含**：
- 每个核心发现的证据等级（A/B/C/D）
- 相互矛盾的研究发现及可能原因
- 研究局限性分析（样本、方法、地域等）
- 未解决的问题/研究空白

### Phase 5: 交叉验证 (Cross-Validation)
**目标**：多源信息相互印证，识别偏见
**输出**：`analysis/validation-matrix.md`
**必须包含**：
- 学术 vs 行业数据对比
- 不同研究机构结论对比
- 时间维度趋势分析（早期 vs 最新研究）
- 地域差异分析（如适用）

### Phase 6: 综合报告 (Synthesis Report)
**目标**：生成结构化、可追溯的深度报告
**输出**：`reports/final-report.md`
**必须包含**：
- 执行摘要（300 字内）
- 方法论透明说明（检索策略、筛选标准）
- 核心发现（带证据等级）
- 批判性分析（局限性、偏见、未解问题）
- 可操作建议（优先级排序）
- 完整参考文献（带可点击链接）
- 附录（原始数据、检索查询、排除来源说明）

### Phase 7: 用户反馈迭代 (Feedback Loop)
**目标**：支持用户质疑后重新检索/分析
**输出**：`reports/revised-report.md`
**触发条件**：用户对某结论提出质疑或要求深化
**必须包含**：
- 用户质疑点记录
- 补充检索策略
- 修订说明（什么变了、为什么）

## 执行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| depth | deep | shallow=快速概览，medium=标准深度，deep=完整7阶段 |
| sources | all | academic=仅学术，industry=仅行业，all=全源 |
| min_sources | 20 | 最低来源数量要求 |
| quality_threshold | 0.7 | 质量评分阈值（0-1） |

## 质量门禁（Quality Gates）

**报告生成前必须通过以下检查**：
- [ ] 核心结论至少有 2 个独立来源支持
- [ ] 所有数据都有明确来源和日期
- [ ] 相互矛盾的发现已标注并分析原因
- [ ] 研究局限性已明确说明
- [ ] 参考文献包含可访问链接

## 研究输出目录结构

```
research/domains/[领域]/[主题]/
├── research-plan.md          # Phase 1: 研究规划
├── sources/
│   ├── raw-sources.json      # Phase 2: 原始来源
│   ├── filtered-sources.json # Phase 3: 筛选后来源
│   └── excluded-sources.json # 排除的来源及原因
├── analysis/
│   ├── insights.md           # Phase 4: 深度分析
│   └── validation-matrix.md   # Phase 5: 交叉验证
└── reports/
    ├── final-report.md        # Phase 6: 最终报告
    └── revised-report.md      # Phase 7: 修订报告（如有）
```

## 工具依赖

| 工具 | 用途 | 备选方案 |
|------|------|----------|
| OpenAlex API | 学术论文检索 | PubMed/Google Scholar |
| jq | JSON处理 | Python json模块 |
| bc | 数学计算 | Python计算 |

## 质量评估标准

### 学术论文评分卡（0-10分）

| 维度 | 评分项 | 分值 |
|------|--------|------|
| 时效性 | 近3年 | 2.5 |
| 时效性 | 3-5年 | 2 |
| 时效性 | 5年+ | 1 |
| 权威性 | Nature/Science/Lancet | 3 |
| 权威性 | 其他顶刊 | 2.5 |
| 权威性 | PubMed索引 | 2 |
| 方法论 | 样本量>1000 | 1 |
| 方法论 | 有对照组 | 1 |
| 方法论 | 多中心 | 1 |
| 可复现 | 数据/代码公开 | 1 |
| 透明度 | 利益冲突声明 | 0.5 |

**证据等级**：A(9-10) / B(7-8) / C(5-6) / D(<5)

---

## 报告模板引用

详细报告模板请参考：`templates/report-template.md`
来源卡片模板请参考：`templates/source-card.md`

---

*Skill版本：2.0 | 最后更新：2026-03-19*
