# 图片生成模式详解

爱创AI平台支持18种图片生成模式，每种模式对应不同的 `sceneMode` 值和参数要求。

## 重要提示

### prompt 字段规则

大多数模式**必须有 prompt**，且不同模式有固定的默认 prompt。如果 prompt 为空或不符合模式要求，任务会发布失败（code: 999）。

- **Agent模式 / 自由创作**: prompt 由用户自定义描述，是核心参数
- **其他16种模式**: 有预设的默认 prompt（见各模式说明），通常不需要用户额外输入
- 部分模式的 prompt 中包含动态参数（如颜色、语言、表情等），需要根据实际情况填充

## 模式列表

### 1. Agent模式 (agent) ⭐ 首选推荐
- **sceneMode**: `agent_image`
- **说明**: AI智能体辅助图片生成，上传参考图后由AI自主分析意图、制定方案并生成优化后的图片。支持流式进度反馈（思考中→分析意图→制定方案→生成中）。**平台默认首屏模式**，当用户没有明确指定具体功能模式时，优先推荐使用此模式。
- **参考图**: 最多10张（建议至少上传1张让AI分析）
- **参数**: `prompt`（用户自定义需求描述）
- **积分**: 5积分/张
- **API 说明**: 前端使用 SSE 流式接口 `Task/GenerateAgentImageStream`，参数：`conversationId`、`imageUrls`（参考图URL数组）、`des`（prompt）、`ratio`（比例）、`taskJobId`。流式返回 `status_change`（状态更新）→ `task_intention`（意图分析）→ `task_plan`（方案制定）→ `task_info`（生成结果，含 `image_length`）→ `workflow_finish`（工作流完成）。出错时返回 `task_error`。如无需流式体验，也可用 `Task/Publish` + `sceneMode: free_creation` 获得类似的图片生成效果。

### 2. 自由创作 (freestyle)
- **sceneMode**: `free_creation`
- **说明**: 最通用的图片生成模式，上传参考图并描述需求即可生成
- **参考图**: 最多10张
- **参数**: `prompt`, `referenceImages`
- **默认 prompt**: 用户自定义（必填，描述想要什么图片）
- **积分**: 5积分/张

### 3. 商品图 (product-image)
- **sceneMode**: `product_image`
- **说明**: 专为电商商品展示设计，生成高质量商品图
- **参考图**: 需要上传商品照片
- **参数**: `prompt`, `referenceImages`
- **默认 prompt**: `生成专业商品图。`

### 4. 主图套图 (main-picture)
- **sceneMode**: `main_image_set`
- **说明**: 生成电商主图套图（通常包含5张不同角度/场景的图片）
- **积分**: 25积分/套（5张）
- **参考图**: 需要上传商品照片
- **默认 prompt**: `基于上传参考图，生成一套5张的主图套图`

### 5. AI试衣 (try-clothes)
- **sceneMode**: `ai_try_on_clothes`
- **说明**: 将衣服虚拟穿到模特身上
- **默认 prompt**: `将上传的服饰自然穿在模特身上。`
- **参考图**:
  - 第一组 (`images`): **衣服照片（必填）**，最多2张
  - 第二组 (`images2`): 模特照片（**可选**），最多1张。如不填，平台使用默认模特

### 6. AI试鞋 (try-shoes)
- **sceneMode**: `ai_try_on_shoes`
- **说明**: 将鞋子虚拟穿到模特脚上
- **默认 prompt**: `将鞋子自然穿在脚部姿势上。`
- **参考图**:
  - 第一组 (`images`): **鞋子照片（必填）**
  - 第二组 (`images2`): 试鞋姿势图（**可选**），最多1张

### 7. 商品换色 (product-recolor)
- **sceneMode**: `product_recolor`
- **说明**: 改变商品的颜色
- **默认 prompt**: `将商品主体颜色更改为【{目标颜色}】`
- **参考图**: 商品照片
- **额外参数**: 需要在 prompt 中指定目标颜色，如 `将商品主体颜色更改为【红色】`

### 8. 去除水印 (remove-watermark)
- **sceneMode**: `remove_watermark`
- **说明**: 去除图片中的水印
- **默认 prompt**: `去除图片中的水印。`
- **参考图**: 带水印的图片

### 9. 手持商品 (handheld-product)
- **sceneMode**: `handheld_product`
- **说明**: 生成模特手持商品的图片
- **默认 prompt**: `生成自然的手持商品图。`
- **参考图**: 商品照片 + 可选的手部姿势参考

### 10. AI试戴 (ai-try-on-accessories)
- **sceneMode**: `ai_try_on_accessories`
- **说明**: 虚拟试戴配饰（项链、耳环、眼镜等）
- **默认 prompt**: `一键试戴。`
- **参考图**: 模特照片 + 配饰照片

### 11. 服装去皱 (clothes-dewrinkle)
- **sceneMode**: `clothes_dewrinkle`
- **说明**: 自动去除服装照片中的褶皱
- **默认 prompt**: `抚平服装表面褶皱，去皱强度：【{强度}】`
- **参考图**: 有褶皱的服装照片
- **额外参数**: prompt 中需要指定去皱强度，如 `抚平服装表面褶皱，去皱强度：【强】`

### 12. 去牛皮癣/去除杂物 (remove-noise)
- **sceneMode**: `remove_psoriasis`
- **说明**: 去除图片中的杂物、牛皮癣广告等
- **默认 prompt**: `一键清除牛皮癣，还原干净画面。`
- **参考图**: 需要清理的照片

### 13. 图片翻译 (image-translate)
- **sceneMode**: `image_translate`
- **说明**: 翻译图片中的文字内容
- **默认 prompt**: `识别图中文字并翻译成【{目标语言}】。`
- **参考图**: 包含文字的图片
- **额外参数**: prompt 中需要指定目标语言，如 `识别图中文字并翻译成【英语】。`

### 14. 商品替换 (product-replace)
- **sceneMode**: `product_replace`
- **说明**: 将商品放入新的背景/场景中
- **默认 prompt**: `用目标商品替换原图商品。`
- **参考图**: 商品照片 + 可选的场景参考

### 15. 商品平铺图 (product-flat-lay)
- **sceneMode**: `product_flat_lay`
- **说明**: 生成商品的平铺展示图
- **默认 prompt**: `提取图中商品生成平铺图。`
- **参考图**: 商品照片

### 16. 换姿势 (pose-change)
- **sceneMode**: `pose_change`
- **说明**: 改变人物照片中的姿势
- **默认 prompt**: `将人物从原姿势改为新姿势。`
- **参考图**: 人物照片 + 目标姿势参考

### 17. 换表情 (expression-change)
- **sceneMode**: `expression_change`
- **说明**: 改变人物照片中的表情
- **默认 prompt**: `将人物表情自然替换为【{目标表情}】`
- **参考图**: 人物照片
- **额外参数**: prompt 中需要指定目标表情，如 `将人物表情自然替换为【微笑】`

### 18. 商品精修 (product-retouch)
- **sceneMode**: `product_retouch`
- **说明**: 自动精修商品照片（调光、调色、锐化等）
- **默认 prompt**: `精修图片。`
- **参考图**: 商品照片
- **⚠️ 注意**: 当前后端枚举值未完全对接，调用可能报错。建议优先使用其他模式。

## 图片比例选项

所有图片模式支持以下比例：

| 比例 | 说明 |
|------|------|
| `auto` | 智能比例（默认） |
| `1:1` | 正方形 |
| `2:3` | 竖向 portrait |
| `3:2` | 横向 landscape |
| `3:4` | 竖向 portrait |
| `9:16` | 竖向（短视频封面） |
| `16:9` | 横向（横幅） |

## 生成数量

- Agent模式：不支持数量选择（固定1张）
- 自由创作等大多数模式：1-4张
- 主图套图：固定5张

## 参考图数据结构

```json
{
  "referenceImages": [
    {
      "key": "images",
      "index": 0,
      "url": "https://oss.fzputi.com/...",
      "description": ""
    }
  ]
}
```

对于需要两组图片的模式（如AI试衣），使用：
```json
{
  "referenceImages": [
    { "key": "images", "index": 0, "url": "模特照片URL", "description": "" },
    { "key": "images2", "index": 0, "url": "衣服照片URL", "description": "" }
  ]
}
```
