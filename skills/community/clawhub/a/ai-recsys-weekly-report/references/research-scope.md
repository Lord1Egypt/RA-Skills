# 搜广推技术周报 - 研究范围与模板

## 核心研究方向

### 1. 统一 Backbone 架构

**背景**：传统推荐系统采用"序列建模 + 特征交互"两段式架构，存在信息孤岛和优化割裂问题。

**代表性工作**：
| 工作 | 机构 | 会议/时间 | 链接 |
|:---|:---|:---|:---|
| OneTrans | 字节跳动 | WWW 2026 | [arxiv.org/abs/2510.26104](https://arxiv.org/abs/2510.26104) |
| MixFormer | 抖音 | arXiv 2026.2 | [arxiv.org/abs/2602.14110](https://arxiv.org/abs/2602.14110) |
| RankMixer | 阿里 | - | [相关讨论](https://zhuanlan.zhihu.com/p/1917951263083038325) |

**搜索关键词**：`unified backbone recommender`, `one transformer recommendation`, `RankMixer`, `OneTrans`, `MixFormer`

### 2. Scaling Law in Recommendation

**背景**：验证推荐系统是否遵循类似 LLM 的 Scaling Law——模型越大、数据越多，性能是否持续提升？

**代表性工作**：
| 工作 | 机构 | 会议 | 关键数据 |
|:---|:---|:---|:---|
| 1B-Param Recommender Transformer | 音乐平台 | KDD 2026 | 收听+2.26%, 点赞+6.37% |
| MTGR (美团) | 美团 | 内部 | 生成式推荐 Scaling Law 落地 |

**搜索关键词**：`scaling law recommendation system`, `billion parameter recommender`, `large scale transformer recommender`

### 3. MoE (混合专家) 在推荐中的应用

**背景**：MoE 通过稀疏激活降低计算量，同时保持大模型的表达能力。DeepSeekMoE 是当前最先进的 MoE 变体。

**核心问题**：如何设计专家路由策略？不同品类/领域是否应该用不同专家？

**搜索关键词**：`mixture of experts recommendation system`, `DeepSeekMoE ranking`, `sparse expert routing recommender`

### 4. 稀疏注意力机制

**背景**：全量注意力的 O(n²) 复杂度限制了序列长度。稀疏注意力通过选择性计算降低成本。

**代表性工作**：
| 工作 | 来源 | 策略 | 链接 |
|:---|:---|:---|:---|
| BlossomRec | WWW 2026 | 块级双模式(长期+短期) | [arxiv.org/abs/2512.13368](https://arxiv.org/abs/2512.13368) |
| DeepSeek DSA | DeepSeek-V3.2 | Token级细粒度稀疏 | [解读](https://blog.csdn.net/v_JULY_v/article/details/155578958) |
| STRec | RecSys 2023 | 全局稀疏模式 | [ACM DL](https://dl.acm.org/doi/10.1145/3604915.3608779) |

**搜索关键词**：`sparse attention sequential recommendation`, `long sequence modeling recommender`, `efficient attention mechanism`

### 5. 注意力机制创新

| 技术 | 来源 | 核心思想 | 对搜广推的启发 |
|:---|:---|:---|:---|
| Kimi AttnRes | 月之暗面 2026.3 | 动态加权替代固定残差连接 | 即插即用，多目标优化场景适用 |
| Qwen Gated Attention | NeurIPS 2025 Best Paper | 门控注意力，消除Attention Sink | 特征重要性动态加权 |
| FlashMLA | DeepSeek 开源 | 高性能 Sparse Attention CUDA kernel | 工业部署算子基础 |

### 6. 优化器与激活函数迁移

| LLM 技术 | 原始用途 | 搜广推潜在应用 |
|:---|:---|:---|
| Muon 优化器 | LLM 快速训练 | 替代 AdamW, 2x 效率提升 |
| SwiGLU / GeGLU | LLM 表达能力增强 | 替代 ReLU/GELU |
| Adam-mini | 高效训练 | 降低显存占用 |

## 信息源优先级

### Tier 1（必搜）
- **ArXiv**: cs.IR (Information Retrieval), cs.LG (Machine Learning)
- **会议论文**: KDD, WWW, SIGIR, ICML, NeurIPS, RecSys, WSDM

### Tier 2（强烈建议）
- **微信公众号**: 搜索"大模型推荐"、"搜广推 Transformer"等
- **知乎专栏**: 深度技术分析文章
- **InfoQ / AICon**: 行业大会精华总结

### Tier 3（补充）
- **公司技术博客**: 腾讯云、阿里 DAMO、美团技术团队、字节跳动
- **GitHub Trending**: 关注 recommendation-system, llm-rec 相关项目
- **CSDN / 掘金**: 中文技术实践文章
