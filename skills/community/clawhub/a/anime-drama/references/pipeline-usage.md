# 动漫短剧生成 - Pipeline 使用说明

## 快速开始

### 方式一：直接运行 Pipeline（推荐用于测试）

```bash
python3 ~/.openclaw/workspace/skills/anime-drama/scripts/anime_drama_pipeline.py <小说原文文件> [输出目录]
```

示例：
```bash
python3 ~/.openclaw/workspace/skills/anime-drama/scripts/anime_drama_pipeline.py ~/story.txt ~/output
```

### 方式二：通过 ClawTeam Swarm 协作（多 Agent 并行）

```bash
# 创建团队
clawteam team spawn-team anime-swarm -d "动漫短剧生成" -n leader

# 启动多个图片生成 Worker（并行）
clawteam spawn --team anime-swarm --agent-name img-worker-1 --task "生成图片"
clawteam spawn --team anime-swarm --agent-name img-worker-2 --task "生成图片"

# 启动视频生成 Worker
clawteam spawn --team anime-swarm --agent-name vid-worker --task "生成视频"

# 监控
clawteam board attach anime-swarm
```

## 输入格式

小说原文，纯文本文件，每段话会自动作为一个镜头。
示例 `story.txt`：
```
夕阳西下，少女独自站在天台上，望着远处的城市灯火。
一阵风吹过，她闭上眼睛，深深吸了一口气。
突然，一只白色的猫跳到了她身边。
少女睁开眼睛，惊讶地看着这只不速之客。
猫轻轻叫了一声，仿佛在跟她打招呼。
少女蹲下身，轻轻抚摸着猫的毛发。
就在这时，天空突然亮起了极光般的色彩。
```

## 输出结构

```
output_dir/
├── shot_script.json      # 分镜脚本（JSON）
├── shot_001_img.png      # 第1个镜头的图片
├── shot_001_vid.mp4      # 第1个镜头的视频
├── shot_002_img.png
├── shot_002_vid.mp4
├── ...
└── final_drama.mp4       # 最终合并成片（手动合并后生成）
```

## 手动合并视频

如果 pipeline 因故中断，可手动合并已完成的视频：

```python
import subprocess

videos = [
    "shot_001_vid.mp4",
    "shot_002_vid.mp4",
    # ...
]

# 生成列表文件
with open("/tmp/video_list.txt", "w") as f:
    for v in videos:
        f.write(f"file '{v}'\n")

# 合并
ffmpeg -y -f concat -safe 0 -i /tmp/video_list.txt \
  -c:v libx264 -pix_fmt yuv420p \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  final_drama.mp4
```

## 断点续传

pipeline 支持断点续传：已生成的图片和视频文件不会重复生成。
中断后重新运行命令即可从断点继续。

## RH API 费用参考

- 文生图：约 ¥0.1-0.3/张（取决于应用）
- 图生视频：约 ¥0.5-1.5/个（取决于应用和时长）
- 建议单次任务控制在 10 个镜头以内
