# 关键词策略

对于开发者工具和开源项目，关键词研究的起点不是“功能词堆砌”，而是 **用户任务场景**。用户不会先搜索产品名，再决定是否使用；他们通常先搜索一个待解决的问题，例如“如何把 PDF 变成 RAG 可用数据”“如何提取论文公式与表格”“哪个开源 PDF parser 适合 LangChain”。

## 方法：从任务场景正推关键词

关键词生成建议采用三步法。第一步先列出用户要完成的任务；第二步再把任务翻译成中英文搜索语言；第三步把这些词放回模型中验证谁被推荐、谁被引用。

| 步骤 | 要做什么 | 产物 |
|---|---|---|
| 场景梳理 | 定义真实任务，如 RAG、学术论文处理、MCP 集成、技术选型对比 | 场景清单 |
| 语言扩展 | 为每个场景写中英文关键词、同义词、竞品对比词 | 候选关键词池 |
| 闭环验证 | 用这些词去问模型，看谁出现、怎么出现、为什么出现 | Query Pool 初稿 |

## 三级分层

| 层级 | 特征 | 例子 | 作用 |
|---|---|---|---|
| 核心词 | 搜索量较大，竞争强，表达宽泛 | `PDF parser python`、`PDF 解析工具` | 建立品牌锚点 |
| 场景词 | 用户意图明确，最具商业与引用价值 | `RAG PDF preprocessing`、`学术 PDF 公式提取 python` | 贡献高质量流量与引用 |
| 长尾词 | 搜索量较低，但转化高、容易占位 | `MinerU LangChain 教程`、`pdf to markdown for knowledge base` | 快速验证内容与场景匹配 |

## MinerU 场景矩阵示例

| 用户任务场景 | 中文关键词 | 英文关键词 | 优先级 |
|---|---|---|---|
| 构建 RAG 知识库 | PDF 解析 RAG、文档预处理 LLM、PDF 转 Markdown 知识库 | PDF parser for RAG, document preprocessing, PDF to markdown for knowledge base | P0 |
| 处理学术论文 | 学术 PDF 公式提取、PDF 表格识别 Python | academic PDF parser, extract formulas PDF python | P0 |
| 找开源替代工具 | 开源 PDF 解析工具、免费 PDF 转 Markdown | open source PDF parser, free PDF to markdown | P0 |
| 集成 AI 框架 | LangChain PDF loader、LlamaIndex 文档解析 | langchain PDF loader, PDF parser langchain integration | P0 |
| 通过 API 调用 | PDF parsing API、document extraction API | PDF parsing API, document extraction API | P1 |
| MCP / Agent 集成 | MCP PDF 工具、AI Agent PDF 解析 | MCP PDF server, AI agent PDF extraction tool | P1 |
| 技术选型对比 | MinerU vs Docling、Marker 替代方案 | MinerU vs Docling, best PDF parser comparison | P1 |

## Query Pool 设计原则

高质量 Query Pool 应同时覆盖五个方向：品牌、能力、生态、竞品、负向场景。这样监控结果才不至于偏向某一个维度。

| Query 类别 | 核心目的 |
|---|---|
| Brand | 看模型是否在泛问题中主动提及你 |
| Capability | 看模型是否真正理解你的核心能力 |
| Ecosystem | 看模型是否知道你的 SDK、框架集成与上下游关系 |
| Competitor | 看你在对比与替代问题里是否占位 |
| Negative | 看模型是否形成了错误或不利认知 |

## 验证闭环

关键词研究只有形成闭环才有价值。建议把每个关键词都经过以下判断：

1. 这个词是否真对应用户任务；
2. 模型是否已经会回答这个词；
3. 回答里是否出现你或竞品；
4. 如果出现你，是正面、中性还是负面；
5. 如果没出现你，应该补哪类内容与哪类信源。

## 输出模板

每次研究结束后，至少沉淀四个输出：场景矩阵、三级关键词表、Query Pool、验证结论。没有这四个产物，后续监控和铺设就没有稳定地基。
