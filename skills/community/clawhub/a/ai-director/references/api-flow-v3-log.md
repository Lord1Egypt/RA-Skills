# API 完整流程测试日志 - v3

> 2026-02-06 21:49 ~ 22:04 UTC（约 15 分钟）

## 项目信息

- **Project ID**: `be13b128-197e-46aa-893e-3dcf36d54364`
- **Project Name**: api-flow-test-v3
- **故事**: 咖啡师与神秘顾客
- **镜头数**: 12
- **角色数**: 2（咖啡师、神秘顾客）

## 完整执行步骤

| #   | 步骤                   | API                                          | 状态 | 耗时   |
| --- | ---------------------- | -------------------------------------------- | ---- | ------ |
| 1   | 创建项目               | `POST /project/create`                       | ✅   | <1s    |
| 2   | script/update (第一次) | `POST /script/update`                        | ✅   | <1s    |
| 3   | 生成剧本               | `POST /script/storyExpansion`                | ✅   |        |
| 4   | 轮询剧本               | `GET /script/getExpandedStory`               | ✅   | ~27s   |
| 5   | 查询状态               | `GET /project/detail`                        | ✅   | <1s    |
| 6   | script/update (第二次) | `POST /script/update`                        | ✅   | <1s    |
| 7   | 生成角色               | `POST /character/generate`                   | ✅   |        |
| 8   | **project/update**     | `POST /project/update`                       | ✅   | <1s    |
| 9   | 轮询角色               | `GET /character/list`                        | ✅   | ~2min  |
| 10  | 生成分镜               | `POST /storyboard-shots/auto-generate`       | ✅   | <1s    |
| 11  | **project/update**     | `POST /project/update`                       | ✅   | <1s    |
| 12  | 查询图片价格           | `POST /payment/model-price`                  | ✅   | <1s    |
| 13  | 生成图片               | `POST /storyboard-shots/auto-generate-image` | ✅   |        |
| 14  | **project/update**     | `POST /project/update`                       | ✅   | <1s    |
| 15  | 轮询图片               | `GET /storyboard-shots/list`                 | ✅   | ~15s   |
| 16  | optimize-prompt        | `POST /storyboard-shots/optimize-prompt`     | ✅   | <1s    |
| 17  | **project/update**     | `POST /project/update`                       | ✅   | <1s    |
| 18  | 查询视频价格           | `POST /payment/model-price`                  | ✅   | <1s    |
| 19  | 逐个生成视频           | `POST /storyboard-shots/generate-video` x12  | ✅   | <1s/个 |
| 20  | 轮询视频               | `GET /storyboard-shots/list`                 | ✅   | ~3min  |
| 21  | **project/update**     | `POST /project/update`                       | ✅   | <1s    |

## 关键 API 请求详情

### 1. project/create

```bash
curl -X POST "https://giggle.pro/api/v1/project/create" \
  -H "x-auth: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "api-flow-test-v3", "type": "director", "aspect": "16:9"}'
```

### 2 & 6. script/update

```bash
# 第一次 - 只写 diy_script
curl -X POST "https://giggle.pro/api/v1/script/update" \
  -d '{"project_id": "xxx", "diy_script": "原创意"}'

# 第二次 - 写入 ai_script
curl -X POST "https://giggle.pro/api/v1/script/update" \
  -d '{"project_id": "xxx", "diy_script": "原创意", "ai_script": "完整剧本"}'
```

### 8/11/14/17/21. project/update（所有调用参数相同）

```bash
curl -X POST "https://giggle.pro/api/v1/project/update" \
  -H "x-auth: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "be13b128-197e-46aa-893e-3dcf36d54364"}'
```

**注意**: 只需要传 project_id，没有其他参数！

### 12. model-price (图片)

```bash
curl -X POST "https://giggle.pro/api/v1/payment/model-price" \
  -d '{"model": "seedream45", "generate_type": "ImageService.Txt2Img", "duration": 0}'
# Response: price: 5
```

### 18. model-price (视频)

```bash
curl -X POST "https://giggle.pro/api/v1/payment/model-price" \
  -d '{"model": "wan25", "generate_type": "VideoService.Img2Video", "duration": 5}'
# Response: price: 88
```

### 19. generate-video（逐个 shot 调用）

```bash
curl -X POST "https://giggle.pro/api/v1/storyboard-shots/generate-video" \
  -d '{
    "project_id": "xxx",
    "shot_id": 155687,          # 数字 ID，不是 "01"
    "model": "wan25",
    "prompt": "视频描述...",
    "start_frame": "image_asset_id",
    "end_frame": "",
    "duration": 5,
    "used": true,
    "generating_count": 1,
    "generate_audio": true,
    "optimize_prompt": false
  }'
```

## 价格统计

| 类型     | 模型       | 单价 | 数量 | 小计     |
| -------- | ---------- | ---- | ---- | -------- |
| 图片     | seedream45 | 5    | 12   | 60       |
| 视频     | wan25      | 88   | 12   | 1056     |
| **总计** |            |      |      | **1116** |

## 关键发现

1. **project/update 只需要 project_id** - 不需要传其他参数
2. **character/list 图片字段**: 是 `image_signed_url` 不是 `signed_url`
3. **generate-video 的 shot_id**: 使用数字 ID（如 155687），不是 shot_id 字符串（如 "01"）
4. **generate-video vs auto-generate-video**: auto-generate-video 已 deprecated，必须用 generate-video 逐个调用
5. **视频生成有排队**: 提交任务后可能需要等待 1-2 分钟才开始生成

## 时间线

- 21:49:55 - 创建项目
- 21:50:22 - 剧本生成完成
- 21:51:41 - 角色开始生成
- 21:53:xx - 角色图片生成完成
- 21:53:xx - 分镜生成完成
- 21:55:57 - 所有图片生成完成 (12/12)
- 21:56:xx - 视频生成任务提交
- 21:59:25 - 所有视频生成完成 (12/12)
- 22:04:xx - 流程完成

**总耗时**: ~15 分钟
