# audio-summary Skill

音频/视频转文本总结助手。

## 功能

1.  **自动音频提取**：使用 `ffmpeg` 从 MP4 等视频文件中提取 16k mono 压缩音频，以适配大模型体积限制。
2.  **转录转总结**：基于百炼 `qwen3-asr-flash` 模型，自动将音频转换为文字并生成内容分段总结。
3.  **大文件支持**：通过 48k 压缩，支持最长约 5-8 分钟的视频单次直接转录。

## 依赖

-   `ffmpeg` (已安装在系统路径)
-   `openai` Python SDK (已安装)
-   百炼 API KEY (已在脚本中配置为 `sk-76735...`)

## 使用方法

### 从命令行运行

```powershell
# 对指定视频进行提取和总结
python .openclaw/workspace/skills/audio-summary/audio_summary_skill.py "C:\Path\To\Your\Video.mp4"
```

### 文件位置
- 提取出的总结文本将自动保存在视频同级目录下，并命名为 `视频名_summary.txt`。

## 注意事项
- 目前单次 Base64 转录限制为 6MB，对于超过 10 分钟的长视频，建议先手动切分或进一步降低码率。
- API 费用按 `qwen3-asr-flash` 模型计费。
