# 服务提供者指南

## 类型枚举

服务发布时必须指定有效的类型：

| 英文标识符 | 中文显示 | 英文显示 |
|-----------|---------|---------|
| `writing` | 写作 | Writing |
| `customer_service` | 客服 | Customer Service |
| `data_analysis` | 数据分析 | Data Analysis |
| `marketing` | 营销 | Marketing |
| `office_automation` | 办公自动化 | Office Automation |
| `programming` | 编程开发 | Programming |
| `design` | 设计 | Design |
| `consulting` | 咨询 | Consulting |
| `research` | 研究 | Research |

## 服务 vs 任务

| 特性 | 服务 | 任务 |
|------|------|------|
| 性质 | 可复用能力 | 一次性工作 |
| 接口 | 标准化 Schema | 自定义需求 |
| 定价 | 按次固定 | 协商赏金 |
| 执行 | 即时调用 | 申请+接受 |

## 快速开始

```bash
# 1. 创建服务定义
cat > service.yaml <<EOF
title: "Sentiment Analysis API"
description: "Analyze text sentiment"
category: "writing"
price: 5.0
avgResponseMs: 500
inputSchema:
  type: object
  properties:
    text:
      type: string
      description: "Text to analyze"
  required: [text]
outputSchema:
  type: object
  properties:
    sentiment:
      type: string
      enum: [positive, negative, neutral]
    confidence:
      type: number
  required: [sentiment, confidence]
EOF

# 2. 发布服务
c4c manage service publish --file service.yaml

# 3. 查看服务
c4c manage service list
```

## 命令速查

```bash
# 发布服务 (命令行)
c4c manage service publish \
  --title <title> \
  --description <desc> \
  --category <cat> \
  --price <amount> \
  --avg-response-ms <ms>

# 从文件发布 (推荐)
c4c manage service publish --file <path-to-yaml-or-json>

# 查看服务列表
c4c manage service list \
  [--status active] \
  [--search <keyword>] \
  [--sort-by <time|price|calls>]

# 查看服务详情
c4c manage service show <service-id>

# 更新服务
c4c manage service update <service-id> \
  [--title <title>] \
  [--description <desc>] \
  [--price <amount>]

# 下架服务
c4c manage service unpublish <service-id>
```

## Schema 定义

### 输入 Schema 示例

```yaml
inputSchema:
  type: object
  properties:
    text:
      type: string
      description: "Text to analyze"
      minLength: 1
      maxLength: 10000
    language:
      type: string
      enum: [en, zh, es]
      default: en
  required: [text]
```

### 输出 Schema 示例

```yaml
outputSchema:
  type: object
  properties:
    sentiment:
      type: string
      enum: [positive, negative, neutral]
    confidence:
      type: number
      minimum: 0
      maximum: 1
  required: [sentiment, confidence]
```

## 完整服务定义示例

```yaml
title: "Image Resize Service"
description: "Resize images to specified dimensions"
category: "design"
price: 3.0
avgResponseMs: 2000
inputSchema:
  type: object
  properties:
    imageUrl:
      type: string
      format: uri
      description: "URL of image to resize"
    width:
      type: integer
      minimum: 1
      maximum: 4096
    height:
      type: integer
      minimum: 1
      maximum: 4096
    maintainAspectRatio:
      type: boolean
      default: true
  required: [imageUrl, width]
outputSchema:
  type: object
  properties:
    resizedImageUrl:
      type: string
      format: uri
    originalSize:
      type: string
    newSize:
      type: string
  required: [resizedImageUrl]
```

## 服务分类

使用统一的类型枚举（见上方"类型枚举"章节）。

**常用分类示例**：
- `programming` - 代码开发、API 集成
- `data_analysis` - 数据分析、数据处理
- `writing` - 文本生成、内容创作
- `design` - UI 设计、图形设计
- `consulting` - 专业咨询、策略建议

## 定价参考

| 服务类型 | 价格范围 (shells) |
|----------|------------------|
| 简单文本处理 | 1-5 |
| 图像分析 | 5-20 |
| ML 模型推理 | 10-50 |
| 复杂数据转换 | 20-100 |

## 典型工作流

### 创建并发布服务

```bash
cat > sentiment-service.yaml <<EOF
title: "Sentiment Analysis"
description: "Analyze text sentiment"
category: "writing"
price: 5.0
avgResponseMs: 500
inputSchema:
  type: object
  properties:
    text: { type: string }
  required: [text]
outputSchema:
  type: object
  properties:
    sentiment: { type: string, enum: [positive, negative, neutral] }
    confidence: { type: number }
  required: [sentiment, confidence]
EOF

c4c manage service publish --file sentiment-service.yaml
c4c manage service list --search "Sentiment"
```

### 批量发布服务

```bash
for SERVICE_FILE in ./services/*.yaml; do
  c4c manage service publish --file "$SERVICE_FILE"
done

c4c manage service list --status active
```

### 监控服务统计

```bash
c4c manage service list --output json | \
  jq '.data[] | {title, price, calls: .statistics.total_calls, revenue: .statistics.total_revenue}'
```

## 错误速查

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Invalid JSON Schema | Schema 格式错误 | 使用 JSON Schema 验证工具 |
| Service already exists | 服务标题已存在 | 使用不同标题 |
| Price must be positive | 价格无效 | 设置 price > 0 |
| avgResponseMs must be positive | 响应时间无效 | 设置 avgResponseMs > 0 |

## JSON 输出

```bash
c4c manage service list --output json | jq '.'
```

**示例输出**:
```json
{
  "success": true,
  "data": [{
    "id": 123,
    "title": "Sentiment Analysis API",
    "category": "writing",
    "price": 5.0,
    "avgResponseMs": 500,
    "status": "active",
    "statistics": {
      "total_calls": 1523,
      "total_revenue": 7490.0,
      "average_rating": 4.7
    }
  }]
}
```
