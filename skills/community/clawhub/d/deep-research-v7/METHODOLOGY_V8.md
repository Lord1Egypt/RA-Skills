# 深度研究 v8.0 - 世界先进方法论

## 核心理念

```
┌─────────────────────────────────────────────────────────┐
│                    深度研究流程                            │
├─────────────────────────────────────────────────────────┤
│  1. 宽口径搜索  →  2. 筛选聚类  →  3. 深度解读         │
│       ↓                    ↓                    ↓       │
│  多数据源            相关性评分          原文分析+摘要      │
│  20+关键词          AI自动筛选          关键页提取       │
│                                                         │
│  4. 交叉验证  →  5. 观点综合  →  6. 报告生成           │
│       ↓                    ↓                    ↓       │
│  多源对比            争议点识别          三层输出       │
│  数据一致性          专家观点            决策/执行/审计 │
└─────────────────────────────────────────────────────────┘
```

---

## 数据源矩阵 (v8.0)

| 优先级 | 数据源 | 用途 | 格式 |
|--------|--------|------|------|
| P0 | arXiv | AI/ML最新 | PDF |
| P0 | PubMed | 医学研究 | 摘要 |
| P1 | Google Scholar | 广泛覆盖 | 混合 |
| P1 | IEEE/ACM | 会议论文 | PDF |
| P1 | SSRN | 预印本 | PDF |
| P2 | 咨询公司报告 | 行业趋势 | PDF |
| P2 | 公司年报 | 数据分析 | PDF |

---

## 执行工具

```python
class DeepResearchV8:
    """世界级深度研究引擎"""
    
    def __init__(self):
        self.sources = ['arxiv', 'pubmed', 'google_scholar', 'semantic']
    
    def full_flow(self, topic, domain='general'):
        """
        完整研究流程
        """
        # Phase 1: 宽口径搜索 (20+关键词)
        papers = self.broad_search(topic, max=50)
        
        # Phase 2: 智能筛选聚类
        clusters = self.cluster_and_rank(papers)
        
        # Phase 3: 深度解读 (PDF原文)
        analyses = self.deep_read(clusters[:10])
        
        # Phase 4: 交叉验证
        validation = self.cross_validate(analyses)
        
        # Phase 5: 观点综合
        synthesis = self.synthesize(validation)
        
        # Phase 6: 三层报告
        return self.generate_reports(synthesis)
    
    def broad_search(self, topic, max=50):
        """多数据源宽口径搜索"""
        # 1. 自动生成关键词变体
        keywords = self.expand_keywords(topic)
        
        # 2. 并行搜索所有数据源
        # 3. 去重 + 相关性排序
        # 4. 取top N
        pass
    
    def cluster_and_rank(self, papers):
        """聚类 + 相关性评分"""
        # 1. 主题聚类
        # 2. 时间排序
        # 3. 引用排序
        # 4. AI相关性打分
        pass
    
    def deep_read(self, papers):
        """深度解读"""
        # 1. 下载PDF
        # 2. 提取关键页 (摘要+方法+实验+结论)
        # 3. 结构化提取
        # 4. 生成摘要
        pass
    
    def cross_validate(self, analyses):
        """交叉验证"""
        # 1. 多源对比同一观点
        # 2. 识别争议点
        # 3. 标注证据强度
        pass
    
    def synthesize(self, validation):
        """观点综合"""
        # 1. 一致观点 → 强结论
        # 2. 争议观点 → 保留意见
        # 3. 证据不足 → 标注待验证
        pass
    
    def generate_reports(self, synthesis):
        """三层报告输出"""
        # 1. Executive Summary (≤1页)
        # 2. Validation Checklist (可执行)
        # 3. Full Report (完整溯源)
        pass
```

---

## 预期提升

| 指标 | v7.0 | v8.0目标 | 提升 |
|------|------|----------|------|
| 论文数量 | 9 | 50+ | 5x |
| 数据源 | 1 | 6+ | 6x |
| 内容深度 | 框架 | 原文解读 | 质变 |
| 报告页数 | 3 | 20+ | 7x |
| 得分 | 20 | 80+ | 4x |

---

## 技术需求

1. **并行搜索**: asyncio并发搜索多个数据源
2. **PDF解析**: pymupdf提取关键页
3. **LLM总结**: 调用LLM进行深度分析
4. **知识图谱**: 构建概念关联
5. **自动更新**: 监控新论文

---

*设计：2026-03-21*
