# 通用岗位人才定级专家（General Talent Grader v1.0）

基于 ai-talent-grader v3.5 方法论构建。保留全部硬核审计能力（漏洞穿透、量化审计、光滑度检测、三层追问测谎），将评估维度从"AI 专用"升级为"角色自适应"。

## 核心变更

| 维度 | AI 版（v3.5） | 通用版（v1.0） |
|------|-------------|--------------|
| 维度1 | AI 流利度 | **专业流利度** — 在其专业领域的深度与广度 |
| 维度2 | 人机判断力 | **决策判断力** — 在不确定环境下的判断质量 |
| 维度3 | 架构设计力 | **系统设计力** — 将模糊需求转化为系统方案 |
| 维度4 | 混合编排力 | **资源编排力** — 协调多角色/多资源达成目标 |
| 维度5 | 认知深度 | **认知深度** — 知其然 vs 知其所以然 |
| 维度6 | 问题建模能力 | **问题重构能力** — 发现真问题、重新定义问题 |

## 新增能力

### 角色感知评估

自动识别候选人的职业角色（产品/技术/运营/销售/管理等），切换对应的评估锚点。

### 行业适配

根据候选人所在行业调整量化阈值的合理性判断（如互联网的增长率 vs 制造业的增长率）。

### 通用行为锚点

不再局限于"AI 能力"，而是评估任何岗位的核心竞争力。

---

## 使用方法

```bash
# 单次评估（仅简历）
python main.py audit --resume 简历.pdf

# 完整定级（简历 + 面试）
python main.py evaluate --resume 简历.pdf --interview 面试记录.txt

# 指定角色（可选，自动检测）
python main.py evaluate --resume 简历.pdf --role product

# 指定行业（可选，自动检测）
python main.py evaluate --resume 简历.pdf --industry tech
```

## 角色识别规则

| 关键词 | 自动识别角色 |
|--------|-------------|
| 产品/PM/产品经理/产品总监 | product |
| 技术/开发/工程师/架构师 | engineering |
| 运营/用户运营/内容运营 | operations |
| 销售/BD/商务 | sales |
| 管理/总监/VP/CEO/负责人 | management |
| 设计/UX/UI | design |
| 数据/分析师/数据科学 | data |
| HR/人力资源 | hr |
| 财务/会计 | finance |
| 市场/品牌/公关 | marketing |

## 参考文件

| 文件 | 说明 |
|------|------|
| `references/resume_audit.md` | 简历漏洞穿透审计（通用版，无AI专用） |
| `references/quantitative_thresholds.md` | 量化阈值表（通用版） |
| `references/behavioral_anchors.md` | L1-L4 通用行为锚点（角色自适应） |
| `references/signal_extraction.md` | 信号提取标准化（角色自适应） |
| `references/cognitive_depth.md` | 认知深度 4 项检查（通用版） |
| `references/output_templates.md` | 定级报告标准输出模板 |
| `references/pre-flight-check.md` | 执行前检查清单 |
| `scripts/validate_scores.py` | 评分一致性校验器 |
