# 视频剪辑模块

> 将自然语言剪辑请求解析为 FFmpeg 命令并执行。

## 工作流程

```
自然语言脚本 → 解析时间点/动作 → 生成 FFmpeg 命令 → 执行 → 返回结果
```

## 核心命令模式

| 自然语言模式 | FFmpeg 参数 |
|------------|-----------|
| 删除第 A-B 秒 | `-vf "trim=start=X:end=Y,setpts=PTS-STARTPTS"` |
| 提取第 A-B 秒 | `ffmpeg -i input -ss A -to B -c copy out` |
| 拼接 A 和 B | `ffmpeg -f concat -i list.txt -c copy out` |
| 加 BGM | `-af "amix=inputs=2:duration=first:dropout_transition=2"` |
| 渐变过渡 | `xfade=transition:offset` |
| 音量统一 | `loudnorm=I=-16:TP=-1.5:LRA=11` |
| 放大/特写 | `zoompan=z='min(zoom+0.0015,1.5)':d=25` |
| 加速 | `setpts=0.5*PTS` |
| 减速 | `setpts=2.0*PTS` |

## 视频编码规则

- **编码优先**：H.264 (`libx264`)，除非用户指定 HEVC
- **音频**：AAC 48kHz
- **容器**：MP4
- **参数约定**：`$in` 输入文件，`$out` 输出文件

## 脚本解析规则

识别关键词 → 映射参数：

```
"删除" + 时间范围 → trim/discard
"提取" + 时间范围 → extract segment
"拼接" + 文件列表 → concat demuxer
"加音乐" → amix/adelay
"统一音量" → loudnorm
"过渡"/"转场" → xfade
"特写"/"放大" → zoompan
```

## 时间格式支持

- 秒：`5s`、`10"`、`1:30"`（含引号秒）
- 帧（需先查帧率）：`frame_150` → 除以 fps 得秒

详见 `recipes/` 下的配方文件。