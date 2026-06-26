# human_tryon 工作流参考

## API 信息

- **Path**: `/marketing/algorithm/human_tryon`
- **Method**: POST
- **appKey**: marketing-server
- **apiName**: marketing_algorithm_human_tryon
- **QPS**: 10
- **类型**: 异步接口，通过任务轮询获取结果

## 接口参数（skill 暴露的子集）

| 参数 | 类型 | 必须 | 默认值 | 说明 |
|------|------|------|--------|------|
| image_cloth | string | 是 | - | 服装图像 URL（可为真人穿着图） |
| list_images_human | string[] | 是 | - | 模特图像 URL 列表（目前只取第一个） |
| cloth_length | string | 是 | overall | 服装区域：upper/lower/overall |
| dpi | integer | 否 | 300 | 输出图像 DPI |
| output_format | string | 否 | jpg | 输出格式：jpg/png |

## 未暴露但接口支持的完整参数

以下参数在 API 中存在，但在当前 skill 中未暴露：

| 参数 | 说明 |
|------|------|
| mask_cloth | 服装 mask，决定取哪部分作为服饰输入；未传则自动分割 |
| list_masks_human | 模特 mask 列表；未传则自动分割 |
| restore_bg | 是否保持原背景（默认 true） |
| condition_mode | 模特辅助参考：mixed(骨骼+身材)/skeleton(骨骼)，默认 mixed |
| model_type | 出图策略：1=模型A, 2=模型B，空则按 batch_size 自动分配 |
| repaint_mode | 重绘区域：v2/v2_bbox/v3，默认 v2_bbox |
| material_enhancement | 材质增强（提升纹理细节），默认 false |
| batch_size | 生成数量 [1,8]，默认 1 |
| callBackUrl | 异步回调 URL |

## 返回格式

```json
{
  "requestId": "xxx",
  "code": 2000,
  "message": "success",
  "data": 12345  // task_id，用于轮询
}
```

## 图片要求

- 格式：JPG, PNG, JPEG, BMP, WEBP
- 大小：不超过 20MB
