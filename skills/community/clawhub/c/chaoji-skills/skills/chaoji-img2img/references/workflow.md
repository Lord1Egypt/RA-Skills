# image2image 工作流参考

## API 信息

- **Path**: `/marketing/algorithm/material_generation_image_to_image`
- **Method**: POST
- **appKey**: marketing-server
- **apiName**: marketing_algorithm_image2image
- **QPS**: 10
- **类型**: 异步接口，通过任务轮询获取结果

## 接口参数（skill 暴露的子集）

| 参数 | 类型 | 必须 | 默认值 | 说明 |
|------|------|------|--------|------|
| img | string[] | 是 | - | 参考图列表（OSS Path，最多 14 张） |
| prompt | string | 是 | - | 文字描述（不超过 4000 字符） |
| ratio | string | 否 | auto | 生图比例 |
| resolution | string | 否 | 1k | 生成分辨率：1k, 2k |

## Executor 内部固定参数（不暴露给 agent）

| 参数 | 固定值 | 说明 |
|------|--------|------|
| model_type | chao_paint_3.0pro | 最新模型，支持多图(最多14张)、auto比例、1k/2k分辨率 |

## 未暴露但接口支持的完整参数

| 参数 | 说明 |
|------|------|
| batch_size | 生成数量 [1,8]，默认 1 |
| callBackUrl | 异步回调 URL |
| model_type | 其他可选模型：chao_paint_3.0, chao_paint_2.0pro, chao_paint_2.0, chao_paint_1.0 |

## 各模型能力对比（备忘）

| 模型 | 最多参考图 | ratio | resolution |
|------|-----------|-------|------------|
| chao_paint_3.0pro | 14 张 | auto,1:1,3:4,4:3,9:16,16:9,2:3,3:2,21:9 | 1k, 2k |
| chao_paint_3.0 | 14 张 | auto,1:1,3:4,4:3,9:16,16:9,2:3,3:2,21:9 | 1k |
| chao_paint_2.0pro | 10 张 | 1:1,3:4,4:3,9:16,16:9,2:3,3:2,21:9 | 1k, 2k, 4k |
| chao_paint_2.0 | 1 张 | auto | 1k |
| chao_paint_1.0 | 1 张 | 1:1,3:4,4:3,9:16,16:9,2:3,3:2,21:9 | 1k |

## 返回格式

```json
{
  "requestId": "xxx",
  "code": 2000,
  "message": "success",
  "data": 12345  // task_id
}
```

## 图片要求

- 格式：JPG, PNG, JPEG
- 大小：不超过 20MB
