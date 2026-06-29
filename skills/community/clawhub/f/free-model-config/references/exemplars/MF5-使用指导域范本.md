## MF5 使用指导域范本

### MF5-01 使用方法说明范本

**必选组件**：

1. **使用步骤**：

**步骤 1：配置模型**

1. 从平台后台网址生成 API Key
2. 将 API Key 添加到配置文件 `~/.workbuddy/models.json`
3. 验证配置是否正确

**步骤 2：调用模型**

1. 使用相应的 API 端点
2. 设置请求参数（model、prompt、max_tokens、temperature 等）
3. 发送请求

**步骤 3：处理结果**

1. 解析响应
2. 提取生成内容
3. 保存或展示结果

2. **使用示例**：

**文本生成示例**：

```bash
curl -X POST https://apihub.agnes-ai.com/v1/chat/completions \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-2.0-flash",
    "prompt": "请介绍一下人工智能的发展历史",
    "max_tokens": 500,
    "temperature": 0.7
  }'
```

**图像生成示例**：

```bash
curl -X POST https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.0-flash",
    "prompt": "A beautiful sunset over the ocean, vibrant colors, digital art",
    "size": "1024x1024",
    "extra_body": {
      "response_format": "url"
    }
  }'
```

**视频生成示例**：

视频生成通过脚本 `scripts/agnes_gen.py` 执行。本地图片会自动上传获取 URL。

**工作流总览**：

**单条生成**：

| 起点 | 流程 | 命令 |
|------|------|------|
| 文本 → 视频 | 文生视频 | `video --prompt` |
| 图片 → 视频 | 图生视频 | `video --image` |

**组合生成**（两步）：

| 起点 | 流程 | 命令 |
|------|------|------|
| 文本 → 图片 → 视频 | 文生图 → 图生视频 | `image` + `video` |
| 图片 → 图片 → 视频 | 图生图 → 图生视频 | `image --image` + `video` |

**批量生成 → 拼接**：

| 起点 | 流程 | 命令 |
|------|------|------|
| 同 prompt → 自动分段 → 拼接 | 长视频 | `long-video` |
| 已有视频文件 → 拼接 | 合并 | `concat` |
| 用户批量图 → 批量视频 → 拼接 | 图生视频 | `images-video` |
| 文本系列 → 系列视频 → 拼接 | 文生多段视频 | `story-video`（无 image） |
| 文本系列 → 系列图 → 系列视频 → 拼接 | 全流程 | `story-video` |

```bash
## --- 单条生成 ---
## 文生视频
python scripts/agnes_gen.py video --prompt "猫在草地上奔跑" --output cat.mp4

## 图生视频
python scripts/agnes_gen.py video --prompt "镜头推进" --image ./photo.png --output video.mp4

## --- 组合生成（两步）---
## 文生图 → 图生视频
python scripts/agnes_gen.py image --prompt "森林晨景" --output anchor.png
python scripts/agnes_gen.py video --prompt "镜头推进" --image anchor.png --output video.mp4

## --- 批量生成 → 拼接 ---
## 同 prompt 自动分段
python scripts/agnes_gen.py long-video --prompt "日出到日落" --segments 3 --output long.mp4

## 拼接已有视频
python scripts/agnes_gen.py concat --inputs part1.mp4 part2.mp4 --output merged.mp4

## 用户批量图 → 批量视频 → 拼接
python scripts/agnes_gen.py images-video --images s1.png s2.png s3.png --prompt "场景动起来" --output result.mp4

## 故事板文生系列视频（无 image，自动生成锚点图）
python scripts/agnes_gen.py story-video --storyboard text_only.json --output text_story.mp4

## 故事板全流程（含 image 的场景跳过生图）
python scripts/agnes_gen.py story-video --storyboard storyboard.json --output story.mp4
```

**故事板 JSON 格式**（`story-video` 使用）：

纯文本故事板（自动生成锚点图片）：

```json
{
  "base_prompt": "Studio Ghibli style, soft watercolor",
  "style": "cinematic, 4K",
  "seed": 42,
  "scenes": [
    {"prompt": "清晨森林，阳光透过树叶"},
    {"prompt": "小鹿溪边饮水，镜头推进"},
    {"prompt": "夕阳西下，金色光芒"}
  ]
}
```

混合故事板（部分场景用已有图片）：

```json
{
  "base_prompt": "photorealistic, 8K",
  "seed": 100,
  "scenes": [
    {"prompt": "城市天际线，日出"},
    {"prompt": "街道行人，慢动作", "image": "street.png"},
    {"prompt": "夜景霓虹灯"}
  ]
}
```

- `base_prompt` / `style`：共享描述，添加到每个 prompt 前面（保持风格一致）
- `seed`：固定随机种子（图片和视频一致性）
- `scenes[].image`：可选，有则跳过生图直接用，无则自动生成
- `scenes[].frames`：可选，该场景帧数

3. **使用注意事项**：

- API Key 必须从官方后台网址生成
- 请求参数必须在有效范围内
- 图像生成的 response_format 必须放在 extra_body 中
- 视频生成帧数按分辨率受限：1080p ≤169、720p ≤409、480p ≤961，需满足 8n+1
- 视频生成轮询使用 `task_id`，不要使用 `video_id`
- 图生视频的图片必须是公网 URL，本地文件需先上传（脚本自动处理）

**可选组件**：

**使用技巧**：

- **Prompt 优化**：使用清晰、具体的描述，避免模糊不清的表达
- **参数调整**：根据需求调整 max_tokens、temperature 等参数
- **错误处理**：检查 API Key 和接口地址是否正确
- **批量处理**：使用循环或脚本批量处理多个请求

**使用最佳实践**：

- **API Key 安全**：不要将 API Key 分享给他人，不要提交到代码仓库
- **请求频率**：避免频繁调用，遵守平台使用条款
- **错误处理**：记录错误日志，及时处理异常情况
- **性能优化**：合理设置参数，平衡质量和速度

**组装顺序**：使用准备 → 使用步骤 → 使用示例 → 使用确认

**约束**：使用说明必须清晰易懂

**格式**：使用说明（Markdown）

**输出示例**：

```markdown
## 模型使用说明

## 使用步骤

### 步骤 1：配置模型
1. 从平台后台网址生成 API Key
2. 将 API Key 添加到配置文件 ~/.workbuddy/models.json
3. 验证配置是否正确

### 步骤 2：调用模型
1. 使用相应的 API 端点
2. 设置请求参数
3. 发送请求

### 步骤 3：处理结果
1. 解析响应
2. 提取生成内容
3. 保存或展示结果

## 使用示例

### 文本生成
```bash
curl -X POST https://apihub.agnes-ai.com/v1/chat/completions \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-2.0-flash",
    "prompt": "请介绍一下人工智能的发展历史",
    "max_tokens": 500,
    "temperature": 0.7
  }'
```

### 图像生成
```bash
curl -X POST https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.0-flash",
    "prompt": "A beautiful sunset over the ocean",
    "size": "1024x1024",
    "extra_body": {
      "response_format": "url"
    }
  }'
```

## 使用注意事项
1. API Key 必须从官方后台网址生成
2. 请求参数必须在有效范围内
3. 图像生成的 response_format 必须放在 extra_body 中
4. 视频生成帧数按分辨率受限：1080p ≤169、720p ≤409、480p ≤961
5. 视频生成轮询使用 task_id，不要使用 video_id
6. 图生视频的图片必须是公网 URL，本地文件需先上传

## 使用技巧
1. Prompt 优化：使用清晰、具体的描述
2. 参数调整：根据需求调整 max_tokens、temperature 等参数
3. 错误处理：检查 API Key 和接口地址是否正确

## 使用最佳实践
1. API Key 安全：不要将 API Key 分享给他人
2. 请求频率：避免频繁调用，遵守平台使用条款
3. 错误处理：记录错误日志，及时处理异常情况
```

---

### MF5-02 注意事项提醒范本

**必选组件**：

1. **注意事项列表**：

**API Key 安全**：

- 不要将 API Key 分享给他人
- 不要将 API Key 提交到代码仓库
- 定期更换 API Key

**使用限制**：

- 注意免费额度限制
- 避免频繁调用
- 遵守平台使用条款

**错误处理**：

- 检查网络连接
- 验证 API Key 是否有效
- 确认接口地址是否正确

2. **风险提示**：

- 免费模型可能随时调整政策
- 生成内容可能受平台审核
- 建议定期备份重要配置

3. **解决建议**：

- 如果遇到 401 错误，检查 API Key 是否有效
- 如果遇到 404 错误，检查接口地址是否正确
- 如果遇到超时错误，检查网络连接
- 如果遇到频率限制，降低调用频率

**可选组件**：

**常见问题**：

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 401 错误 | API Key 无效 | 重新生成 API Key |
| 404 错误 | 接口地址错误 | 检查接口地址 |
| 超时错误 | 网络问题 | 检查网络连接 |
| 频率限制 | 调用过于频繁 | 降低调用频率 |
| 参数错误 | 参数格式不正确 | 检查参数格式 |
| 配额不足 | 免费额度用完 | 等待额度恢复或升级套餐 |
| task_not_exist | 用 video_id 轮询 | 改用 task_id 轮询 |
| num_frames exceeds maximum | 帧数超出分辨率限制 | 降低帧数或降低分辨率 |
| Invalid base64 | 图片用 data URI 传递 | 改为先上传图片获取 URL |

**故障排除**：

1. **检查配置**：确认 API Key 和接口地址正确
2. **测试连接**：使用 curl 测试接口是否可访问
3. **查看日志**：检查错误日志，了解具体问题
4. **联系支持**：如无法解决，联系平台技术支持

**组装顺序**：风险识别 → 注意事项 → 风险提示 → 解决建议

**约束**：必须提醒用户重要注意事项

**格式**：注意事项（Markdown）

**输出示例**：

```markdown
## 使用注意事项

## 注意事项列表

### API Key 安全
1. 不要将 API Key 分享给他人
2. 不要将 API Key 提交到代码仓库
3. 定期更换 API Key

### 使用限制
1. 注意免费额度限制
2. 避免频繁调用
3. 遵守平台使用条款

### 错误处理
1. 检查网络连接
2. 验证 API Key 是否有效
3. 确认接口地址是否正确

## 风险提示
1. 免费模型可能随时调整政策
2. 生成内容可能受平台审核
3. 建议定期备份重要配置

## 解决建议
1. 如果遇到 401 错误，检查 API Key 是否有效
2. 如果遇到 404 错误，检查接口地址是否正确
3. 如果遇到超时错误，检查网络连接
4. 如果遇到频率限制，降低调用频率

## 常见问题
| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 401 错误 | API Key 无效 | 重新生成 API Key |
| 404 错误 | 接口地址错误 | 检查接口地址 |
| 超时错误 | 网络问题 | 检查网络连接 |
| 频率限制 | 调用过于频繁 | 降低调用频率 |

## 故障排除
1. 检查配置：确认 API Key 和接口地址正确
2. 测试连接：使用 curl 测试接口是否可访问
3. 查看日志：检查错误日志，了解具体问题
4. 联系支持：如无法解决，联系平台技术支持
```
