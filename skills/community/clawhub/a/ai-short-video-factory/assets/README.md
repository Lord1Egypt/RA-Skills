# Assets

此目录存放 SkillHub 展示用素材：

- `cover.png` — 封面图（建议 1200×630px）
- `demo-*.png` — 效果截图（展示视频关键帧）

生成效果截图方法：
```bash
# 从已渲染视频中提取关键帧
ffmpeg -ss 5 -i final.mp4 -frames:v 1 -q:v 2 assets/demo-scene1.png
ffmpeg -ss 15 -i final.mp4 -frames:v 1 -q:v 2 assets/demo-scene2.png
```
