# 图标参考：语义图形 + 箭头体系 + 产品图标库

---

## A. 语义图形库

通用图形词汇表。每种形状对应固定含义，确保不同图表间的视觉一致性。
所有代码片段中 `{cx}`、`{cy}` 表示节点中心坐标，根据实际布局替换。

### 1. LLM / 模型（双边框圆角矩形 + 闪电）

标识 AI 大语言模型节点。双边框表示"智能"组件。

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"
      fill="{fill}" stroke="{stroke-outer}" stroke-width="2.5"/>
<rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h-6}" rx="8"
      fill="none" stroke="{stroke-inner}" stroke-width="0.8" opacity="0.5"/>
<text x="{cx}" y="{cy-6}" text-anchor="middle" font-size="14">⚡</text>
<text x="{cx}" y="{cy+10}" text-anchor="middle" fill="{text-color}"
      font-size="13" font-weight="600">{模型名称}</text>
```

### 2. Agent / 编排器（六边形）

标识自主代理或编排器组件。外接圆半径 `r` 推荐 36。

```xml
<polygon points="{cx},{cy-r} {cx+r*0.866},{cy-r*0.5} {cx+r*0.866},{cy+r*0.5} {cx},{cy+r} {cx-r*0.866},{cy+r*0.5} {cx-r*0.866},{cy-r*0.5}"
         fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<text x="{cx}" y="{cy+5}" text-anchor="middle" fill="{text}"
      font-size="12" font-weight="600">{Agent 名称}</text>
```

r=36 时关键坐标：`r*0.866 ≈ 31.2`, `r*0.5 = 18`

### 3. 向量数据库（圆柱体 + 内环）

标识向量存储。内环线条表示数据分区，可选（无内环则为普通数据库）。

```xml
<ellipse cx="{cx}" cy="{top}" rx="{w/2}" ry="{w/6}"
         fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<rect x="{cx-w/2}" y="{top}" width="{w}" height="{h}"
      fill="{fill}" stroke="none"/>
<line x1="{cx-w/2}" y1="{top}" x2="{cx-w/2}" y2="{top+h}"
      stroke="{stroke}" stroke-width="1.5"/>
<line x1="{cx+w/2}" y1="{top}" x2="{cx+w/2}" y2="{top+h}"
      stroke="{stroke}" stroke-width="1.5"/>
<!-- 内环（向量数据库专用） -->
<ellipse cx="{cx}" cy="{top+h*0.33}" rx="{w/2}" ry="{w/6}"
         fill="none" stroke="{stroke}" stroke-width="0.7" opacity="0.5"/>
<ellipse cx="{cx}" cy="{top+h*0.66}" rx="{w/2}" ry="{w/6}"
         fill="none" stroke="{stroke}" stroke-width="0.7" opacity="0.5"/>
<!-- 底部椭圆 -->
<ellipse cx="{cx}" cy="{top+h}" rx="{w/2}" ry="{w/6}"
         fill="{fill-dark}" stroke="{stroke}" stroke-width="1.5"/>
<text x="{cx}" y="{top+h*0.5+5}" text-anchor="middle" fill="{text}"
      font-size="11" font-weight="700">{名称}</text>
```

推荐尺寸：w=80, h=70

### 4. 工具 / 函数调用（矩形 + 齿轮）

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"
      fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="16">⚙</text>
<text x="{cx}" y="{cy+12}" text-anchor="middle" fill="{text}"
      font-size="12">{工具名称}</text>
```

### 5. 决策点（菱形）

```xml
<polygon points="{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}"
         fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<text x="{cx}" y="{cy+5}" text-anchor="middle" fill="{text}"
      font-size="12">{条件?}</text>
```

推荐 hw=50, hh=35

### 6. 用户 / 人类（圆形头 + 身体）

```xml
<circle cx="{cx}" cy="{cy-18}" r="10"
        fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>
<path d="M {cx-14},{cy+16} Q {cx-14},{cy-4} {cx},{cy-4} Q {cx+14},{cy-4} {cx+14},{cy+16}"
      fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>
<text x="{cx}" y="{cy+30}" text-anchor="middle" fill="{text}"
      font-size="12">{用户}</text>
```

### 7. 记忆节点（虚线边框矩形）

标识短期/长期记忆组件。

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
      fill="{fill}" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="6,3"/>
<text x="{cx}" y="{cy-6}" text-anchor="middle" fill="{text}"
      font-size="10" opacity="0.7">MEMORY</text>
<text x="{cx}" y="{cy+8}" text-anchor="middle" fill="{text}"
      font-size="13">{记忆类型}</text>
```

### 8. 队列 / 消息流（水平管道）

```xml
<ellipse cx="{x1}" cy="{cy}" rx="{ry*0.6}" ry="{ry}"
         fill="{fill-dark}" stroke="{stroke}" stroke-width="1.5"/>
<rect x="{x1}" y="{cy-ry}" width="{x2-x1}" height="{ry*2}"
      fill="{fill}" stroke="none"/>
<line x1="{x1}" y1="{cy-ry}" x2="{x2}" y2="{cy-ry}"
      stroke="{stroke}" stroke-width="1.5"/>
<line x1="{x1}" y1="{cy+ry}" x2="{x2}" y2="{cy+ry}"
      stroke="{stroke}" stroke-width="1.5"/>
<ellipse cx="{x2}" cy="{cy}" rx="{ry*0.6}" ry="{ry}"
         fill="{fill-light}" stroke="{stroke}" stroke-width="1.5"/>
<text x="{(x1+x2)/2}" y="{cy+5}" text-anchor="middle" fill="{text}"
      font-size="12">{队列名}</text>
```

### 9. API 网关（小六边形）

与 Agent 六边形类似，但更小（r=28）、不同配色。

```xml
<polygon points="{cx},{cy-28} {cx+24},{cy-14} {cx+24},{cy+14} {cx},{cy+28} {cx-24},{cy+14} {cx-24},{cy-14}"
         fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<text x="{cx}" y="{cy+5}" text-anchor="middle" fill="{text}"
      font-size="11">API</text>
```

### 10. 浏览器 / Web 客户端（带红绿灯圆点的矩形）

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"
      fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<!-- 标题栏 -->
<rect x="{x}" y="{y}" width="{w}" height="20" rx="6"
      fill="{fill-dark}" stroke="none"/>
<rect x="{x}" y="{y+14}" width="{w}" height="6" fill="{fill-dark}"/>
<!-- 红绿灯 -->
<circle cx="{x+12}" cy="{y+10}" r="4" fill="#ef4444" opacity="0.8"/>
<circle cx="{x+24}" cy="{y+10}" r="4" fill="#f59e0b" opacity="0.8"/>
<circle cx="{x+36}" cy="{y+10}" r="4" fill="#10b981" opacity="0.8"/>
<text x="{cx}" y="{cy+10}" text-anchor="middle" fill="{text}"
      font-size="12">{名称}</text>
```

### 11. 文档 / 文件（折角矩形）

```xml
<path d="M {x},{y} L {x+w-12},{y} L {x+w},{y+12} L {x+w},{y+h} L {x},{y+h} Z"
      fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
<path d="M {x+w-12},{y} L {x+w-12},{y+12} L {x+w},{y+12}"
      fill="{fill-dark}" stroke="{stroke}" stroke-width="1"/>
<!-- 内容线条 -->
<line x1="{x+8}" y1="{y+h*0.45}" x2="{x+w-8}" y2="{y+h*0.45}"
      stroke="{stroke}" stroke-width="1" opacity="0.5"/>
<line x1="{x+8}" y1="{y+h*0.6}" x2="{x+w-8}" y2="{y+h*0.6}"
      stroke="{stroke}" stroke-width="1" opacity="0.5"/>
<line x1="{x+8}" y1="{y+h*0.75}" x2="{x+w-16}" y2="{y+h*0.75}"
      stroke="{stroke}" stroke-width="1" opacity="0.5"/>
```

### 12. 泳道容器（虚线背景带）

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"
      fill="{fill}" fill-opacity="0.04" stroke="{stroke}"
      stroke-width="1" stroke-dasharray="6,4"/>
<text x="{x+12}" y="{y+16}" fill="{label-color}" font-size="10"
      font-weight="600" letter-spacing="0.06em">{层名称}</text>
```

---

## 图形速查表

| 图形 | 含义 | 使用时机 |
|------|------|----------|
| 双边框圆角矩形 + ⚡ | LLM / 模型 | 任何大语言模型调用节点 |
| 六边形 | Agent / 编排器 | 自主代理、工作流编排 |
| 圆柱体 + 内环 | 向量数据库 | Pinecone、Weaviate、Chroma 等 |
| 圆柱体（无内环） | 传统数据库 | PostgreSQL、MySQL、Redis 等 |
| 矩形 + ⚙ | 工具 / 函数 | API 调用、工具执行 |
| 菱形 | 决策点 | 条件判断、分支 |
| 圆形 + 身体 | 用户 / 人类 | 用户交互入口 |
| 虚线矩形 | 记忆节点 | 短期/长期记忆 |
| 水平管道 | 队列 / 消息流 | Kafka、RabbitMQ 等 |
| 小六边形 | API 网关 | 请求路由、网关 |
| 红绿灯矩形 | 浏览器 | Web 客户端 |
| 折角矩形 | 文档 / 文件 | 配置文件、日志 |
| 虚线背景带 | 泳道容器 | 分层、分组 |

---

## B. 箭头语义体系

### 箭头类型

| 类型 | 线宽 | 线型 | 用途 |
|------|------|------|------|
| 主数据流 | 2px | 实线 | 核心请求/响应路径 |
| 记忆写入 | 1.5px | 虚线 `stroke-dasharray="5,3"` | 写入向量库/缓存 |
| 异步/事件 | 1.5px | 点线 `stroke-dasharray="4,2"` | 事件驱动、回调 |
| 反馈/循环 | 1.5px | 曲线（贝塞尔） | 迭代、重试 |

### 颜色编码

| 颜色 | 含义 | 色值（随风格调整） |
|------|------|-------------------|
| 蓝色 | 主数据流 | 见各风格参考 |
| 红色 | 错误/备选路径 | 见各风格参考 |
| 绿色 | 数据写入/成功 | 见各风格参考 |
| 紫色 | 异步/事件 | 见各风格参考 |

### 箭头标记模板

```xml
<defs>
  <!-- 标准填充箭头 -->
  <marker id="arrow-{color}" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="{hex}"/>
  </marker>

  <!-- 空心箭头（关联线） -->
  <marker id="arrow-open" markerWidth="10" markerHeight="8"
          refX="9" refY="4" orient="auto">
    <path d="M 0 0 L 10 4 L 0 8" fill="none" stroke="{color}" stroke-width="1.5"/>
  </marker>

  <!-- 圆点（弱关联） -->
  <marker id="dot" markerWidth="8" markerHeight="8"
          refX="4" refY="4" orient="auto">
    <circle cx="4" cy="4" r="3" fill="{color}"/>
  </marker>
</defs>
```

### 连线示例

```xml
<!-- 主数据流：实线 -->
<line x1="100" y1="50" x2="300" y2="50"
      stroke="{blue}" stroke-width="2" marker-end="url(#arrow-blue)"/>

<!-- 记忆写入：虚线 -->
<line x1="100" y1="100" x2="300" y2="100"
      stroke="{green}" stroke-width="1.5" stroke-dasharray="5,3"
      marker-end="url(#arrow-green)"/>

<!-- 异步事件：点线 -->
<line x1="100" y1="150" x2="300" y2="150"
      stroke="{purple}" stroke-width="1.5" stroke-dasharray="4,2"
      marker-end="url(#arrow-purple)"/>

<!-- 反馈循环：贝塞尔曲线 -->
<path d="M 300,200 Q 350,250 300,300"
      fill="none" stroke="{red}" stroke-width="1.5"
      marker-end="url(#arrow-red)"/>
```

### 图例规则

**当图表中使用了 2 种以上箭头类型时，必须在左下角添加图例。**

图例模板（适配各风格的文字颜色）：

```xml
<g transform="translate(20, {canvas-height - 80})">
  <text x="0" y="0" font-size="12" font-weight="600">{图例}</text>
  <!-- 每种箭头类型一行 -->
  <line x1="0" y1="16" x2="30" y2="16" stroke="{blue}" stroke-width="2"
        marker-end="url(#arrow-blue)"/>
  <text x="36" y="20" font-size="11">{主数据流}</text>

  <line x1="0" y1="32" x2="30" y2="32" stroke="{green}" stroke-width="1.5"
        stroke-dasharray="5,3" marker-end="url(#arrow-green)"/>
  <text x="36" y="36" font-size="11">{记忆写入}</text>

  <line x1="0" y1="48" x2="30" y2="48" stroke="{purple}" stroke-width="1.5"
        stroke-dasharray="4,2" marker-end="url(#arrow-purple)"/>
  <text x="36" y="52" font-size="11">{异步事件}</text>
</g>
```

---

## C. 产品图标库

所有产品图标使用统一的圆形徽章 + 文字缩写模式。

### 圆形徽章模板

```xml
<circle cx="{cx}" cy="{cy}" r="22" fill="{BRAND_COLOR}"/>
<text x="{cx}" y="{cy+5}" text-anchor="middle" fill="white"
      font-size="10" font-weight="700" font-family="Helvetica">{BADGE}</text>
<!-- 可选：外层光环（AI 产品标记） -->
<circle cx="{cx}" cy="{cy}" r="24" fill="none"
        stroke="{BRAND_COLOR}" stroke-width="1" opacity="0.4"/>
```

### 向量数据库徽章模板（圆柱体 + 品牌色）

```xml
<ellipse cx="{cx}" cy="{top}" rx="40" ry="12"
         fill="{FILL}" stroke="{STROKE}" stroke-width="1.5"/>
<rect x="{cx-40}" y="{top}" width="80" height="50"
      fill="{FILL}" stroke="none"/>
<line x1="{cx-40}" y1="{top}" x2="{cx-40}" y2="{top+50}"
      stroke="{STROKE}" stroke-width="1.5"/>
<line x1="{cx+40}" y1="{top}" x2="{cx+40}" y2="{top+50}"
      stroke="{STROKE}" stroke-width="1.5"/>
<ellipse cx="{cx}" cy="{top+50}" rx="40" ry="12"
         fill="{FILL_DARK}" stroke="{STROKE}" stroke-width="1.5"/>
<text x="{cx}" y="{top+30}" text-anchor="middle" fill="white"
      font-size="11" font-weight="700">{名称}</text>
```

### 图标尺寸规范

| 场景 | 尺寸 | 内边距 |
|------|------|--------|
| 节点内徽章 | 28×28 圆形 | 10px |
| 独立图标节点 | 40×40 | 16px |
| 英雄/中心节点 | 56×56 | 20px |
| 小内联指示器 | 16×16 | 6px |

---

### AI / ML 产品

| 产品 | 品牌色 | 徽章文字 |
|------|--------|----------|
| OpenAI / ChatGPT | `#10A37F` | OAI |
| Anthropic / Claude | `#D97757` | CL |
| Google Gemini | `#4285F4` | GEM |
| Meta LLaMA | `#0467DF` | LL |
| Mistral | `#FF7000` | MIS |
| Cohere | `#39594D` | CO |
| Groq | `#F55036` | GRQ |
| Together AI | `#6366F1` | TGR |
| Replicate | `#191919` | REP |
| Hugging Face | `#FFD21E` | HF |

> Hugging Face 使用深色文字 `fill="#191919"` 而非白色。

### AI 记忆与 RAG 产品

| 产品 | 品牌色 | 徽章文字 |
|------|--------|----------|
| Mem0 | `#6366F1` | M0 |
| LangChain | `#1C3C3C` | LC |
| LlamaIndex | `#8B5CF6` | LI |
| LangGraph | `#1C3C3C` | LG |
| CrewAI | `#EF4444` | CRW |
| AutoGen | `#0078D4` | AG |
| Haystack | `#FF6D00` | HS |
| DSPy | `#7C3AED` | DSP |

### 向量数据库

| 产品 | 品牌色 | 徽章文字 |
|------|--------|----------|
| Pinecone | `#1C1C2E` | PC |
| Weaviate | `#FA0050` | WV |
| Qdrant | `#DC244C` | QD |
| Chroma | `#FF6B35` | CH |
| Milvus | `#00A1EA` | MLV |
| pgvector | `#336791` | PGV |
| Faiss | `#0467DF` | FAI |

### 传统数据库

| 产品 | 品牌色 | 徽章文字 |
|------|--------|----------|
| PostgreSQL | `#336791` | PG |
| MySQL | `#4479A1` | MY |
| MongoDB | `#47A248` | MG |
| Redis | `#DC382D` | RD |
| Elasticsearch | `#005571` | ES |
| Cassandra | `#1287B1` | CAS |
| Neo4j | `#008CC1` | N4J |
| SQLite | `#003B57` | SQL |

### 消息队列与流处理

| 产品 | 品牌色 | 徽章文字 |
|------|--------|----------|
| Apache Kafka | `#231F20` | KFK |
| RabbitMQ | `#FF6600` | RMQ |
| AWS SQS | `#FF9900` | SQS |
| NATS | `#27AAE1` | NATS |
| Pulsar | `#188FFF` | PLS |

### 云平台与基础设施

| 产品 | 品牌色 | 徽章文字 |
|------|--------|----------|
| AWS | `#FF9900` | AWS |
| GCP | `#4285F4` | GCP |
| Azure | `#0089D6` | AZ |
| Cloudflare | `#F48120` | CF |
| Vercel | `#000000` | VCL |
| Docker | `#2496ED` | DKR |
| Kubernetes | `#326CE5` | K8S |
| Terraform | `#7B42BC` | TF |
| Nginx | `#009639` | NGX |
| FastAPI | `#009688` | FAPI |

### 可观测性

| 产品 | 品牌色 | 徽章文字 |
|------|--------|----------|
| Grafana | `#F46800` | GRF |
| Prometheus | `#E6522C` | PRM |
| Datadog | `#632CA6` | DD |
| LangSmith | `#1C3C3C` | LS |
| Langfuse | `#6366F1` | LF |
| Arize | `#6B48FF` | ARZ |
