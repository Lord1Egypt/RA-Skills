# tryon_shoes 工作流参考

## API 信息

- **Path**: `/marketing/algorithm/tryon_shoes`
- **Method**: POST
- **appKey**: marketing-server
- **apiName**: marketing_algorithm_tryon_shoes
- **QPS**: 10
- **类型**: 异步接口

## 接口参数（skill 暴露的子集）

| 参数 | 类型 | 必须 | 说明 |
|------|------|------|------|
| list_images_shoe | string[] | 是 | 鞋商品图列表（1~3 张，OSS Path） |
| list_images_human | string[] | 是 | 模特图列表（取第一个，OSS Path） |

固定参数（不暴露给 agent）：
- `tryon_type`: 固定为 5（专业模式）

## Executor 内部映射（对 agent 透明）

`list_images_shoe` 在 executor 内部自动映射为 API 参数：
- 1 张 -> `image_shoe` (单张鞋图字段)
- 2 张 -> `product_image: { both_feet_image, inner_side_image }`
- 3 张 -> `product_image: { both_feet_image, inner_side_image, outer_side_image }`

Agent 无需知道这些 API 字段名，只需传入鞋图列表即可。

## 未暴露但接口支持的完整参数

| 参数 | 说明 |
|------|------|
| product_image | 多角度鞋图对象（both_feet_image/inner_side_image/outer_side_image） |
| tryon_type | 1=高级/2=海报替换/3=标准/4=快速/5=专业（当前固定5） |
| aspect_ratio | 宽高比（仅 tryon_type=5 生效） |
| clarity | 清晰度 1k/2k/4k（仅 tryon_type=5 生效） |
| dpi | 输出 DPI（tryon_type=5 不生效） |
| output_format | 输出格式 jpg/png（tryon_type=5 不生效） |
| batch_size | 生成数量 [1,8] |
| callBackUrl | 异步回调 URL |

## 图片输入规范

所有图片参数统一处理为 OSS Path 后传入 API：
- 本地文件 -> 上传 OSS -> 提取 OSS Path
- URL -> 提取 OSS Path（去掉域名前缀）
- OSS Path -> 直接使用

## 图片要求

- 格式：JPG, PNG, JPEG
- 大小：不超过 20MB
