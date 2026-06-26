# CNC报价系统-RAG版 物料清单

## 核心文件

| 文件 | 用途 | 行数 |
|------|------|------|
| quote_engine.py | 报价引擎核心 | ~1200 |
| hybrid_retriever.py | 混合检索器 | ~400 |
| case_retriever.py | 案例检索 | ~250 |
| embeddings.py | 向量嵌入 | ~150 |
| risk_control.py | 风险控制 | ~570 |

## 知识库文件

| 文件 | 内容 |
|------|------|
| al_6061.md | 铝合金6061参数 |
| sus_304.md | 不锈钢304参数 |
| steel_45.md | 45号钢参数 |
| abs.md | ABS塑料参数 |
| pa66.md | PA66尼龙参数 |

## 依赖项

| 包 | 版本 | 用途 |
|---|------|------|
| faiss-cpu | >=1.7.4 | 向量索引 |
| numpy | >=1.21.0 | 数值计算 |
| pandas | >=1.3.0 | 数据处理 |
| requests | >=2.26.0 | API调用 |

## 性能基准

| 指标 | 值 |
|------|-----|
| 检索延迟 | <200ms |
| 向量维度 | 768 |
| 索引大小 | ~50MB |

---

Author: timo.cao (miscdd@163.com)
License: MIT