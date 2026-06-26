# cutout 工作流参考

## API 信息

- **Path**: `/marketing/algorithm/universal_cutout`
- **Method**: POST
- **appKey**: marketing-server
- **apiName**: marketing_algorithm_integrated_auto_segmentation
- **QPS**: 10
- **类型**: 同步接口，即时返回结果

## 接口参数（skill 暴露的子集）

| 参数 | 类型 | 必须 | 默认值 | 说明 |
|------|------|------|--------|------|
| image | string | 是 | - | 待抠图图片（OSS Path） |
| method | string | 否 | auto | 抠图模式 |
| cate_token | string | 否 | overall | 仅 clothseg 模式生效，服装类别 |

## Executor 内部固定参数

| 参数 | 固定值 | 说明 |
|------|--------|------|
| return_view_image | true | 始终返回透明底图 + mask |

## method 可选值

| 值 | 说明 |
|---|---|
| auto | 智能抠图（自动识别，推荐） |
| seg | 人像抠图 |
| clothseg | 服装分割（可配合 cate_token 指定上装/下装/全身） |
| patternseg | 图案抠图 |
| generalseg | 通用抠图 |

## 返回格式（同步）

```json
{
  "requestId": "xxx",
  "code": 2000,
  "message": "success",
  "data": {
    "image_mask": "https://...mask灰度图URL",
    "view_image": "https://...透明底图URL"
  }
}
```

## 图片要求

- 格式：JPG, PNG, JPEG
- 大小：不超过 20MB
