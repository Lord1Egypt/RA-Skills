---
name: audio-rename
description: Rename audio files with Chinese/special characters to simple English names for mlx-stt compatibility.
version: 1.0.0
author: rinko
metadata: {"openclaw":{"emoji":"🔠","os":["darwin","linux"]}}
triggers:
- "重命名音频"
- "rename audio"
- "fix filename"
---

# Audio Rename Skill

将带有中文/特殊字符的音频文件重命名为纯英文名称，避免 mlx-stt 等工具处理时出现路径问题。

## Usage

**推荐使用 Python 版本（更好地处理 Unicode 文件名）：**

```bash
# 重命名单个文件为默认名称 video_audio.m4a
python3 ${baseDir}/audio-rename.py <文件路径>

# 重命名为指定名称
python3 ${baseDir}/audio-rename.py <文件路径> <新名称>

# 批量重命名目录下所有音频文件
python3 ${baseDir}/audio-rename.py <目录路径> --all
```

## Examples

```bash
# 重命名为 video_audio.m4a
python3 skills/audio-rename/audio-rename.py "/path/to/中文文件.m4a"

# 重命名为指定名称
python3 skills/audio-rename/audio-rename.py "/path/to/文件.m4a" "my_audio"

# 批量重命名
python3 skills/audio-rename/audio-rename.py "/path/to/audio/" --all
```

## Workflow (推荐)

配合 bili + mlx-stt 使用：

```bash
# 1. 下载音频
bili audio BV1xxx --no-split -o /Users/linyi/.openclaw/workspace/audio/

# 2. 重命名（如有中文）
python3 skills/audio-rename/audio-rename.py /Users/linyi/.openclaw/workspace/audio/*.m4a

# 3. 转录
bash skills/mlx-stt/mlx-stt.sh /Users/linyi/.openclaw/workspace/audio/video_audio.m4a
```

## Default Naming

- 单个文件：`video_audio.m4a`（如已存在则自动添加序号）
- 批量处理：`audio_001.m4a`, `audio_002.m4a`, ...
