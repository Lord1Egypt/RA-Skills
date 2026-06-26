# 知识库管理 (knowledge_query / knowledge_answer)

## 概述

两个命令共同管理接待助手的知识缺口：
- `knowledge_query`：查询接待助手接待中无法回答或转人工的问题列表
- `knowledge_answer`：为指定问题补充标准答案，自动写入云端知识库

## knowledge_query

### 入参

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `--page` | int | 否 | 1 | 页码 |
| `--page-size` | int | 否 | 10 | 每页条数 |

### TPP 接口

`POST /api/cowboy_knowledge_query/1.0.0`

请求体（项目内部 page → 网关字段 pageNum）：
```json
{"pageNum": 1, "pageSize": 10}
```

返回字段（网关双层 Result 包装，外层 success + 内层 AiSellerCcPageResult）：
```json
{
  "success": true,
  "data": {
    "data": [
      {
        "id": "TQR001",
        "query": "这款手机支持5G网络吗？",
        "createTime": "2026-05-14 10:30:00",
        "relatedProducts": [
          {
            "productId": "PROD001",
            "productName": "iPhone 15 Pro Max",
            "productImage": "https://example.com/products/iphone15promax.jpg"
          }
        ]
      }
    ],
    "total": 15,
    "pageNum": 1,
    "totalPages": 2
  }
}
```

### 字段映射（网关 → 项目内部）

| 网关字段 | 项目内部字段 | 说明 |
|----------|-------------|------|
| `id` | `question_id` | 问题 ID |
| `query` | `question` | 问题内容 |
| `createTime` | `create_time` | 问题产生时间 |
| `relatedProducts` | `products` | 关联商品列表 |
| `relatedProducts[].productId` | `products[].id` | 商品 ID |
| `relatedProducts[].productName` | `products[].name` | 商品名称 |
| `relatedProducts[].productImage` | `products[].image` | 商品图片 |

### 输出格式

Markdown 列表展示，每条包含：问题内容、问题ID、关联商品名称、时间。
支持分页提示（当有下一页时提示 `--page N`）。

---

## knowledge_answer

### 入参

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--question` | str | 是 | 问题内容 |
| `--answer` | str | 是 | 答案内容 |
| `--question-id` | str | 否 | 问题 ID（可选；不传则自动生成 UUID） |

### TPP 接口

`POST /api/cowboy_knowledge_answer/1.0.0`

请求体（项目内部 question_id → 网关字段 recordId，question → query）：
```json
{
  "recordId": "TQR001",
  "query": "这款手机支持5G网络吗？",
  "answer": "是的，iPhone 15 Pro Max 支持全球主流5G频段"
}
```

返回字段（网关双层 Result 包装，外层 success + 内层 AiSellerCcResult\<Boolean\>）：
```json
{
  "success": true,
  "data": {
    "success": true,
    "data": true
  }
}
```

内层 `data` 为 Boolean：
- `true`：答案成功入库
- `false`：网关受理但入库未成功（检查 query 与 question_id 是否匹配）

### 写入规则

- 提交后该问题从待完善列表移除
- 答案自动写入云端知识库
- 接待助手下次遇到类似问题时将使用该答案回复

### 注意事项

1. **双层 Result 包装**：所有 1688 网关接口返回都是外层 Result + 内层业务壳，代码需剥两层
2. **字段名边界映射**：项目内部统一使用 question_id / question，仅在构造请求 body 时映射为网关字段名（recordId / query）
3. **UUID 自动生成**：当 `--question-id` 未传时，service 层本地生成 uuid 作为 recordId

### 关联页面

执行 `knowledge_query` 后，Agent 应同时引导商家打开培训中心 - 待完善知识页，供其在页面中直接操作。
