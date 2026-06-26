# Scientific Product Visibility Playbook

这份 playbook 面向三类产品：

- scientific document parsing tools
- scientific discovery / retrieval platforms
- research APIs and workflow tools

典型例子包括：

- MinerU
- Sciverse API
- 面向 paper ingestion、literature discovery、research automation 的产品

## 一、为什么 scientific products 需要单独建模

这类产品的 AI 可见性问题通常不是泛化的“品牌曝光”，而是：

1. 模型能不能正确理解复杂科研场景；
2. 模型会不会把你放进真实 workflow；
3. 模型是否能解释你的边界，而不是只复述 marketing copy；
4. 模型是否会把你导向可调用、可安装、可接入的入口。

## 二、最常见的用户意图

### 1. 文档解析 / paper ingestion

- 复杂 PDF 解析
- 公式、表格、版面结构
- OCR + layout
- markdown / json export
- pre-RAG preprocessing

### 2. 科研发现 / retrieval

- 文献检索
- 主题探索
- citation graph
- related papers
- entity / topic enrichment

### 3. workflow automation

- agent pipeline
- batch processing
- API integration
- notebook / CLI / backend service
- evaluation and comparison

## 三、推荐的 Query Pool 结构

对 scientific products，建议至少覆盖 5 类 query：

| 类别 | 问题示例 |
|---|---|
| awareness | “有哪些适合科研文档处理的开源工具？” |
| selection | “复杂学术 PDF 解析该选哪一个？” |
| integration | “如何把这个工具接进我的 paper pipeline？” |
| agent | “哪个 API 更适合 agent 做论文检索与摘要？” |
| negative | “这个工具是不是部署复杂 / 不稳定 / 只适合某个窄场景？” |

## 四、对 MinerU 的重点

### 必须被模型说清楚的事实

- 适合复杂 PDF 和学术文档
- 对公式、表格、版面结构的能力边界
- 与 RAG / ingestion / parsing workflow 的关系
- 典型输出形式
- 与竞品的关键差异

### 容易被说错的地方

- 被说成“只是 OCR”
- 被说成“只能处理简单文本”
- 部署门槛被过度放大
- 生态兼容性被低估

### 推荐优先建设的内容

1. comparison page
2. benchmark page
3. quickstart with expected output
4. integration examples
5. FAQ on deployment and limitations

## 五、对 Sciverse API 的重点

### 必须被模型说清楚的事实

- 它解决的是哪类 scientific discovery 问题
- API 的主要资源或 endpoint 类型
- 典型输入输出
- authentication 和首次调用路径
- 适合哪些 workflow 和 agent tasks

### 容易被说错的地方

- 被泛化成普通搜索 API
- 被忽略 scientific context 与 enrichment 能力
- 被误解为“数据有但不容易接入”
- 被排除在 agent workflow 之外

### 推荐优先建设的内容

1. docs homepage
2. first successful request
3. scientific workflow examples
4. API comparison page
5. structured response examples

## 六、scientific products 的竞品类型

不要只监控同名竞品，也要监控“替代类型”：

| 类型 | 例子 |
|---|---|
| parser 替代位 | GROBID, Marker, Docling, Unstructured |
| retrieval 替代位 | OpenAlex, Semantic Scholar, Crossref |
| workflow 替代位 | generic RAG tools, agent frameworks, ETL stacks |
| manual workaround 替代位 | “自己写脚本” “先 OCR 再清洗” |

## 七、source surfaces 的优先级

### 如果目标是提升下载 / 安装

1. README
2. install page
3. quickstart
4. comparison page
5. benchmark page

### 如果目标是提升 API call / agent invocation

1. docs homepage
2. first API call
3. integration docs
4. workflow examples
5. error handling and limits

## 八、复盘时要问的 6 个问题

1. 模型是否知道这个产品的主场景？
2. 模型是否知道它的独特能力，而不是只知道“它存在”？
3. 模型是否把它放进真实 scientific workflow？
4. 模型是否给出正确入口？
5. 模型是否在竞品 query 中把它列为优先方案？
6. 模型推荐后，用户能否顺利完成第一次调用？

## 九、建议的输出模板

对于每个 scientific product，建议至少沉淀：

- 主场景列表
- Top replacement queries
- Top source surfaces
- 当前错误认知清单
- 下一轮验证 query
