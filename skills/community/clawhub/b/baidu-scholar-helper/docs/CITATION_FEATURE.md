# 引用量功能说明

## 功能概述

本技能已添加引用量查询功能，支持以下方式：

### 1. 本地引用量数据库

已内置经典论文的引用量数据，包括：

**社区检测领域：**
- Newman (2004) - Finding and evaluating community structure: 28,000+ 引用
- Blondel et al. (2008) - Fast unfolding (Louvain): 18,500+ 引用
- Fortunato (2010) - Community detection in graphs: 12,000+ 引用
- Traag et al. (2019) - Leiden algorithm: 4,200+ 引用

**其他领域：**
- Transformer (2017) - Attention is all you need: 95,000+ 引用
- BERT (2018) - Pre-training of deep bidirectional transformers: 75,000+ 引用

### 2. 手动查询链接

对于未匹配的论文，自动提供以下查询链接：
- Google Scholar
- Semantic Scholar
- 百度学术

## 使用方法

### 方式一：使用增强版脚本（推荐）

```bash
# 搜索社区检测论文，带引用量
python3 scripts/enhanced_search.py "community detection" 10

# 搜索特定主题
python3 scripts/enhanced_search.py "deep learning" 8
```

### 方式二：使用本地数据库版

```bash
# 使用本地引用量数据库
python3 scripts/citations_db.py "network analysis" 10
```

### 方式三：手动查询引用量

1. **Google Scholar**
   - 访问：https://scholar.google.com
   - 搜索论文标题
   - 查看引用次数

2. **Semantic Scholar**
   - 访问：https://www.semanticscholar.org
   - 提供API查询（免费）
   - 显示引用量、相关论文

3. **百度学术**
   - 访问：https://xueshu.baidu.com
   - 支持中文论文搜索
   - 显示引用量

## 引用量排序

所有搜索结果默认按引用量从高到低排序，方便快速找到领域内的重要论文。

## 输出示例

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 【论文 1】引用量：⭐18500
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 标题：Fast unfolding of communities in large networks
👥 作者：V. D. Blondel, J.-L. Guillaume, R. Lambiotte, E. Lefebvre
📅 发布：2008-10-09
🏷️ 分类：physics.soc-ph
🔗 链接：https://arxiv.org/abs/0803.0476

🧠 【核心工作】
   本文提出了一种快速算法，用于在大型网络中检测社区结构...

💡 【创新点】
   该算法通过局部优化模块度，实现了在大规模网络上的高效社区检测...

⬇️  PDF下载...
    ✅ 已下载: Fast_unfolding_communities_2008_arXiv.pdf
```

## 引用量数据来源

- **本地数据库**：手动维护经典论文引用量
- **Semantic Scholar API**：实时查询（注意速率限制）
- **Google Scholar**：手动查询
- **百度学术**：手动查询

## 注意事项

1. **API速率限制**
   - Semantic Scholar API有速率限制（100次/5分钟）
   - arXiv API也有访问限制
   - 建议使用本地数据库版本

2. **引用量准确性**
   - 本地数据库数据来自Google Scholar（2024年数据）
   - 实际引用量会随时间增长
   - 建议定期手动查询最新数据

3. **匹配算法**
   - 使用标题关键词匹配
   - 相似度阈值：至少3个关键词匹配
   - 如有误匹配，请手动查询确认

## 扩展本地数据库

可以在 `citations_db.py` 文件中的 `KNOWN_CITATIONS` 字典添加更多论文：

```python
KNOWN_CITATIONS = {
    "论文标题关键词": 引用量,
    "example paper title": 1000,
}
```

## 技术实现

### 已实现的脚本

1. **enhanced_search.py**
   - 集成Semantic Scholar API
   - 实时查询引用量
   - 自动排序

2. **citations_db.py**
   - 本地数据库匹配
   - 提供查询链接
   - 避免API限制

3. **smart_search.py**
   - 基础搜索功能
   - 创新点提取

### 待实现功能

- [ ] 批量查询Semantic Scholar（带缓存）
- [ ] 引用量趋势图
- [ ] 导出BibTeX格式
- [ ] 引用量数据持久化存储

## 更新日志

### V8.0.0 (2026-04-07)
- ✅ 添加本地引用量数据库
- ✅ 集成Semantic Scholar API
- ✅ 实现按引用量排序
- ✅ 提供手动查询链接
- ✅ 优化创新点提取算法

## 反馈与改进

如有问题或建议，请：
1. 提交Issue
2. 更新本地数据库
3. 改进匹配算法

---

**维护者：** 史婉媱
**更新时间：** 2026-04-07
**版本：** V1.1.0
