---
name: async-free-creation
description: >-
  通过 Flyelep 异步自由创作接口调用 Image-2 模型生成产品图或创意图。
  当用户要求异步自由创作、自由创作、Image-2 自由创作、根据提示词和参考图生成多张图片时使用此技能。
---
# Flyelep 异步自由创作

通过 Flyelep Image-2 自由创作 API 异步生成图片。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息

### 创建任务

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/allAroundCreationAsync`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`
- **超时时间**: 建议 120-300 秒

### 查询结果

- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult`
- **Content-Type**: `application/json`
- **认证方式**: 在请求头中传入 `secretKey`
- **说明**: 该接口是新版任务查询接口，优先使用；旧接口 `queryResult` 仍可作为兼容备选。

## 认证方式

在请求头中传入 `secretKey`。该密钥需由用户在 Flyelep 开放平台申请获得：https://www.flyelep.cn/controlboard 。

请求头示例：

```http
Content-Type: application/json
secretKey: 用户提供的API密钥
```

> **安全说明**：`secretKey` 必须放在请求头中，不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

## 创建任务请求 Body

```json
{
  "query": "生成钢笔的产品图",
  "apiImgUrlList": [
    "https://example.com/product.png"
  ],
  "detailPictureNumber": 4,
  "aspectRatio": "1:1"
}
```

## 创建任务响应格式

成功：

```json
{
  "code": 200,
  "data": {
    "agentGenerateTaskId": "2054467932287070209"
  }
}
```

- `code=200` 表示创建任务成功
- `data.agentGenerateTaskId` 为异步任务 ID
- 创建任务后必须继续调用查询结果接口获取最终图片 URL

## 查询结果请求 Body

```json
{
  "agentGenerateTaskId": "2054467932287070209"
}
```

## 查询结果响应格式

```json
{
  "code": 200,
  "data": {
    "taskList": [
      {
        "taskStatus": 2,
        "executeResult": "https://example.com/result1.png"
      },
      {
        "taskStatus": 1
      }
    ]
  }
}
```

### taskStatus 状态

| 值 | 含义 |
|----|------|
| `0` | 待生成 |
| `1` | 生成中 |
| `2` | 生成成功 |
| `3` | 生成失败 |

当 `taskStatus=2` 时，读取对应项的 `executeResult` 图片 URL 并展示给用户。若仍有 `0` 或 `1`，等待后继续轮询；若出现 `3`，告知用户该任务项生成失败。

## 参数说明

### 必传参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| query | - | 用户生成图片的具体需求描述，最多 1000 个字符 |
| detailPictureNumber | - | 需要生成的图片数量，支持 `1` 到 `4` |
| aspectRatio | 随机 | 图片比例；文档标注为必需，但为空时默认随机比例 |

### 可选参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| apiImgUrlList | - | 参考图片 URL 数组，最多 6 张，建议单张图片小于 10MB |

## 参数映射规则

### query

- 直接传入用户对图片的生成需求
- 保留用户原始创意意图，不要无故扩写成另一种产品或场景
- 如果用户只给产品名，可补充为简洁的产品图生成需求，例如：`生成钢笔的产品图`
- 最多 1000 个字符，超出时需要压缩描述

### apiImgUrlList

- 传入公网可访问的图片直链数组
- 最多 6 张
- 字段名是 `apiImgUrlList`，不是 `fileUrlList` 或 `imgUrlList`
- 用户未提供参考图时，不传此字段

### detailPictureNumber

- 支持 `1`、`2`、`3`、`4`
- 用户未指定数量时，默认传 `4`
- 用户要求超过 4 张时，告知该接口单次最多生成 4 张，可分多次调用

### aspectRatio

支持以下比例：

- `1:1`
- `3:2`
- `2:3`
- `3:4`
- `4:3`
- `4:5`
- `5:4`
- `9:16`
- `16:9`
- `21:9`

默认规则：

- 用户明确指定比例时，原样传入
- 用户未指定比例时，可传空字符串或不传，让接口随机选择
- 横版优先推断为 `16:9`
- 方图优先推断为 `1:1`
- 竖版优先推断为 `9:16`

## 调用示例

**创建异步自由创作任务：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/allAroundCreationAsync" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "aspectRatio": "1:1",
    "query": "生成钢笔的产品图",
    "detailPictureNumber": 4,
    "apiImgUrlList": [
      "https://example.com/product.png"
    ]
  }'
```

**查询任务结果：**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/queryTaskResult" \
  -H "Content-Type: application/json" \
  -H "secretKey: 你的密钥" \
  --max-time 300 \
  -d '{
    "agentGenerateTaskId": "2054467932287070209"
  }'
```

## 执行流程

1. 收集用户的生成需求并写入 `query`
2. 收集可选参考图并写入 `apiImgUrlList`
3. 确定 `detailPictureNumber`，未指定时默认 `4`
4. 确定 `aspectRatio`，未指定时可为空或不传
5. 在请求头中传入 `secretKey`
6. 调用 `allAroundCreationAsync` 创建任务
7. 从响应中读取 `data.agentGenerateTaskId`
8. 调用 `queryTaskResult` 轮询任务结果
9. 将 `taskStatus=2` 的 `executeResult` 图片 URL 逐个展示给用户

## 常见错误及解决方案

| 错误 | 原因与解决 |
|------|-----------|
| HTTP 401 / `code` 非 200 | `secretKey` 无效、缺失或已过期，确认请求头是否正确传入 |
| HTTP 405 Not Allowed | 请求方法错误，必须使用 `POST` |
| `agentGenerateTaskId` 为空 | 创建任务失败或响应结构异常，检查创建任务接口返回 |
| 查询结果一直是 `0` 或 `1` | 图片仍在排队或生成中，等待后继续轮询 |
| `taskStatus=3` | 对应图片生成失败，可简化提示词、减少参考图或重试 |
| `detailPictureNumber` 超出范围 | 该接口仅支持单次生成 `1-4` 张 |
| `apiImgUrlList` 无法访问 | 参考图 URL 不是公网直链、已过期，或源站限制访问 |
| 比例不支持 | `aspectRatio` 必须使用文档规定的比例枚举 |

## 提示词处理

该接口适合宽泛的创意图片生成，但仍应把提示词写得明确、短而有约束。

推荐提示词包含：

- 产品或主体
- 使用场景
- 风格与氛围
- 构图或比例要求
- 需要保留的参考图特征

不要在提示词中承诺接口不支持的细粒度编辑能力。若用户明确要求局部重绘、商品换色、商品替换、场景替换、图片翻译、抠图、放大或超清增强，应优先使用对应的专用 skill。
