# AI 开发技术栈选型指南

## LLM API 对比

| 提供商 | 模型 | 输入价格 ($/1M tokens) | 输出价格 | 中文能力 | 适合场景 |
|-------|------|:------------------:|:------:|:------:|---------|
| OpenAI | GPT-4o | $2.50 | $10.00 | ★★★★ | 复杂推理、多模态 |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 | ★★★★ | 日常对话、分类 |
| DeepSeek | deepseek-chat | ¥1 | ¥2 | ★★★★★ | 中文场景首选 |
| DeepSeek | deepseek-reasoner | ¥4 | ¥16 | ★★★★★ | 复杂推理 |
| DashScope | qwen-max | ¥2.5 | ¥10 | ★★★★★ | 国内合规优先 |
| DashScope | qwen-turbo | ¥0.3 | ¥0.6 | ★★★★ | 高并发低价 |
| Anthropic | Claude 3.5 Sonnet | $3.00 | $15.00 | ★★★ | 代码生成、长文 |
| Google | Gemini 1.5 Pro | $1.25 | $5.00 | ★★★ | 多模态、长上下文 |

## Embedding 模型对比

| 模型 | 维度 | 价格 | 中文效果 | 推荐场景 |
|------|:---:|------|:------:|---------|
| text-embedding-3-small | 512 | $0.02/1M | ★★★★ | 通用 (性价比最高) |
| text-embedding-3-large | 3072 | $0.13/1M | ★★★★★ | 高精度需求 |
| bge-large-zh-v1.5 | 1024 | 免费(本地) | ★★★★★ | 中文私有化部署 |
| m3e-base | 768 | 免费(本地) | ★★★★ | 轻量中文私有化 |
| qwen-text-embedding | 1536 | ¥0.7/1M | ★★★★★ | 国内云服务 |

## 向量数据库对比

| 数据库 | 类型 | 开源 | 适合规模 | 推荐场景 |
|-------|------|:---:|:---:|---------|
| Milvus | 专用向量库 | ✓ | 亿级 | 生产环境首选 |
| pgvector | PG插件 | ✓ | 千万级 | 已有PostgreSQL |
| Chroma | 专用向量库 | ✓ | 百万级 | 快速原型 |
| Qdrant | 专用向量库 | ✓ | 亿级 | 高性能RAG |
| Weaviate | 专用向量库 | ✓ | 千万级 | 多模态RAG |
| Elasticsearch | 搜索引擎 | ✓ | 千万级 | 已有ES集群 |

## 框架选型

| 框架 | 定位 | 适合 | 不适合 |
|------|------|------|--------|
| LangChain | 全能SDK | 快速原型、学习 | 生产环境 (抽象层太重,调试困难) |
| LlamaIndex | RAG专用 | 数据索引、检索增强 | 通用Agent |
| DSPy | 声明式Prompt | Eval驱动开发 | UI交互 |
| AutoGen | Multi-Agent | 多智能体协作 | 简单单Agent |
| CrewAI | Multi-Agent | 角色扮演Agent | 高性能场景 |
| **自研+FastAPI** | **完全控制** | **生产环境** | 快速原型 |
| Vercel AI SDK | 前端AI | Next.js项目 | Python项目 |

> **推荐策略**: 原型阶段用 LangChain/LlamaIndex → 确认方案后逐步迁移到自研 FastAPI

## 监控与追踪

| 工具 | 类型 | 开源 | 核心功能 |
|------|------|:---:|---------|
| LangFuse | LLM观测 | ✓ | Trace、Eval、成本追踪 |
| LangSmith | LLM观测 | ✗ | Trace、Eval、Playground |
| Phoenix (Arize) | LLM观测 | ✓ | Embedding可视化、漂移检测 |
| Helicone | LLM网关 | ✗ | 日志、缓存、限流 |
| Weights & Biases | MLOps | 部分 | 实验追踪、Prompt管理 |
| Prometheus+Grafana | 通用监控 | ✓ | 基础设施监控 |

## 部署方案对比

| 方案 | 成本 | 运维复杂度 | 弹性 | 适合 |
|------|:--:|:--------:|:---:|------|
| 单机Docker | 低 | 低 | 无 | MVP、小流量 |
| Docker Swarm | 低 | 中 | 有限 | 中小团队 |
| K8s | 高 | 高 | 无限 | 大规模生产 |
| Serverless (云函数) | 中 | 低 | 高 | 事件驱动、低频 |
| Vercel/Railway | 中 | 极低 | 中 | 独立开发者 |

## 国内特殊考虑

- **网络**: 直连 OpenAI/GitHub 不稳定, 需代理或使用国产替代
- **合规**: 用户数据不出境, DashScope/百炼是首选
- **模型部署**: ModelScope + hf-mirror 解决模型下载慢
- **域名备案**: 国内服务需要ICP备案
- **内容审核**: 必须接入内容安全API (阿里云/腾讯云)
