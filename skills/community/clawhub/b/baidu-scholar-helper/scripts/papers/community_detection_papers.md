# 社区检测论文推荐清单

## 📊 经典基础论文

### 1. 模块度优化方法

**Newman-Girvan算法**
- 标题：Finding and evaluating community structure in networks
- 作者：M. E. J. Newman, M. Girvan
- 年份：2004
- 期刊：Physical Review E
- 引用量：20,000+
- 核心贡献：提出模块度(Modularity)概念，成为社区检测的标准评价指标

**Louvain算法**
- 标题：Fast unfolding of communities in large networks
- 作者：V. D. Blondel, J.-L. Guillaume, R. Lambiotte, E. Lefebvre
- 年份：2008
- 期刊：Journal of Statistical Mechanics
- arXiv: 0803.0476
- 链接：https://arxiv.org/abs/0803.0476
- PDF：https://arxiv.org/pdf/0803.0476.pdf
- 核心贡献：快速模块度优化算法，可处理大规模网络

**Leiden算法（Louvain改进版）**
- 标题：From Louvain to Leiden: guaranteeing well-connected communities
- 作者：V. A. Traag, L. Waltman, N. J. van Eck
- 年份：2019
- 期刊：Scientific Reports
- arXiv: 1810.08473
- 链接：https://arxiv.org/abs/1810.08473
- PDF：https://arxiv.org/pdf/1810.08473.pdf
- 核心贡献：改进Louvain，保证社区内部连通性

### 2. 统计推断方法

**随机块模型(SBM)**
- 标题：Community detection in networks: Algorithms, complexity, and information limits
- 作者：Emmanuel Abbe
- 年份：2017
- arXiv: 1707.01489
- 链接：https://arxiv.org/abs/1707.01489
- PDF：https://arxiv.org/pdf/1707.01489.pdf
- 核心贡献：系统综述社区检测的理论基础和信息极限

**随机块模型推断**
- 标题：Stochastic block models and community structure in networks
- 作者：Brian Karrer, M. E. J. Newman
- 年份：2011
- 期刊：Physical Review E
- 核心贡献：提出degree-corrected SBM

### 3. 标签传播算法

- 标题：Near linear time algorithm to detect community structures in large-scale networks
- 作者：Usha Nandini Raghavan, Réka Albert, Soundar Kumara
- 年份：2007
- 期刊：Physical Review E
- 核心贡献：O(n)时间复杂度的社区检测算法

## 🔬 近期前沿研究

### 1. 深度学习方法

**图神经网络社区检测**
- 标题：Deep Learning for Community Detection: Progress, Challenges and Opportunities
- arXiv: 2105.12885
- 链接：https://arxiv.org/abs/2105.12885
- PDF：https://arxiv.org/pdf/2105.12885.pdf
- 核心内容：深度学习在社区检测中的应用综述

**GNN-based Community Detection**
- 标题：Community Detection in Graph Neural Networks: A Survey
- 年份：2022-2023
- 核心内容：图神经网络社区检测方法综述

### 2. 重叠社区检测

- 标题：Overlapping community detection in networks: The state-of-the-art and comparative study
- 作者：Jaewon Yang, Jure Leskovec
- 年份：2013
- ACM Computing Surveys
- 核心贡献：重叠社区检测方法综述

### 3. 动态社区检测

- 标题：Dynamic community detection in evolving networks
- 年份：2020-2024
- 核心内容：时序网络中的社区演化检测

### 4. 多层网络社区检测

- 标题：Community detection in multilayer networks
- 年份：2015-2024
- 核心内容：多层/多关系网络的社区检测

## 📚 综述论文

### 1. 经典综述

**Fortunato综述**
- 标题：Community detection in graphs
- 作者：Santo Fortunato
- 年份：2010
- 期刊：Physics Reports
- 引用量：10,000+
- 核心内容：社区检测领域的经典综述

**扩展综述**
- 标题：Community detection in networks: A user guide
- 作者：Santo Fortunato, Darko Hric
- 年份：2016
- 期刊：Physics Reports
- 核心内容：面向实践的社区检测指南

### 2. 现代综述

**深度学习综述**
- 标题：A Comprehensive Survey on Community Detection with Deep Learning
- 年份：2022
- arXiv: 2105.12537
- 链接：https://arxiv.org/abs/2105.12537
- 核心内容：深度学习社区检测方法全面综述

## 🎯 热门研究方向

### 1. 异常社区检测
- 检测网络中的异常社区结构

### 2. 高阶网络社区检测
- 基于超图、单纯复形等高阶结构的社区检测

### 3. 可解释性社区检测
- 提供社区结构可解释性的方法

### 4. 大规模社区检测
- 针对十亿节点网络的分布式算法

### 5. 社区搜索
- 查询驱动的社区发现

## 🔧 工具和库

### Python库
- **python-louvain**: Louvain算法实现
- **python-igraph**: 多种社区检测算法
- **networkx**: 基础社区检测算法
- **leidenalg**: Leiden算法实现
- **CDLib**: 社区检测算法库

### 使用示例
```python
import networkx as nx
import community as community_louvain

# Louvain算法
partition = community_louvain.best_partition(G)

# Leiden算法（需要leidenalg）
import leidenalg
partition = leidenalg.find_partition(ig_graph, leidenalg.ModularityVertexPartition)
```

## 📥 推荐下载

根据你的需求，我推荐优先阅读以下论文：

### 入门必读
1. Newman (2004) - 模块度概念
2. Blondel et al. (2008) - Louvain算法
3. Fortunato (2010) - 经典综述

### 进阶阅读
4. Abbe (2017) - 理论基础
5. Traag et al. (2019) - Leiden算法

### 前沿研究
6. 深度学习社区检测综述 (2022)

## 🔗 有用的链接

- **arXiv搜索**: https://arxiv.org/search/?searchtype=all&query=community+detection+networks
- **百度学术**: https://xueshu.baidu.com/s?wd=社区检测&sort=sc_cite
- **Google Scholar**: https://scholar.google.com/scholar?q=community+detection+networks
- **论文代码**: https://paperswithcode.com/task/community-detection

生成时间：2026-04-07
