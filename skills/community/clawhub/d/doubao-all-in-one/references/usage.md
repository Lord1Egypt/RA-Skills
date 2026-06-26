# 使用说明

## 适用范围

`doubao-all-in-one` 负责：

1. 调用豆包图片生成接口
2. 调用豆包图片编辑接口
3. 调用豆包视频生成接口
4. 将结果保存到本地

它不负责：

- 对象存储上传
- 返回公网 URL
- 工作流编排

## 运行方式

设 `DOUBAO_SKILL_DIR` 为 `.claude/skills/doubao-all-in-one` 的绝对路径，从项目根目录执行：

```shell
uv run --python python $DOUBAO_SKILL_DIR/scripts/text_to_image.py --prompt "..."
uv run --python python $DOUBAO_SKILL_DIR/scripts/image_to_image.py --image resources/images/climb1.jpeg --prompt "..."
uv run --python python $DOUBAO_SKILL_DIR/scripts/create_video_task.py --prompt "..." --poll
```

## 输出约定

- 文生图目录：`outputs/doubao/images/text_to_image/`
- 图生图目录：`outputs/doubao/images/image_to_image/`
- 视频目录：
  - 文生视频：`outputs/doubao/videos/text_to_video/`
  - 首帧图生视频：`outputs/doubao/videos/first_frame_to_video/`
  - 首尾帧图生视频：`outputs/doubao/videos/first_last_frame_to_video/`
- 输出字段：
  - `provider=doubao`
  - `scene`
  - `used_model`
  - `local_path`

## 环境变量

- `ARK_API_KEY`（必需）
