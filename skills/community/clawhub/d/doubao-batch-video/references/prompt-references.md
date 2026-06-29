# GEO 视频生成提示词参考

## 视频主题示例

### 主题1：GEO 概念科普
**提示词**：
> 科技感蓝色背景，数字大脑与搜索引擎融合，AI对话界面展示，动态文字"GEO生成引擎优化"，8k分辨率，电影级画质

### 主题2：传统 SEO vs GEO 对比
**提示词**：
> 分屏画面对比，左侧传统搜索引擎结果页，右侧AI对话直接给出答案，箭头从左侧流向右侧，科技感，蓝色橙色对比色

### 主题3：GEO 给企业带来的价值
**提示词**：
> 企业品牌在AI回答中被提及的演示动画，聊天界面中AI推荐某品牌产品，品牌logo发光效果，商务科技风格

### 主题4：如何做GEO优化
**提示词**：
> 优化流程图动画，关键词研究、内容优化、AI平台适配三个步骤依次高亮，现代化UI设计，蓝色主色调

### 主题5：GEO 未来趋势
**提示词**：
> 未来城市夜景，全息投影显示AI搜索数据，趋势曲线向上增长，科技感十足，赛博朋克风格

---

## 多模态生成参数建议

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `duration` | `5` | 每条5秒，5条共25秒 |
| `aspect_ratio` | `16:9` | 横屏，适合视频号/B站 |
| `aspect_ratio` | `9:16` | 竖屏，适合抖音/视频号竖屏 |
| `prompt` | 中文描述 | 描述画面内容+风格+质量关键词 |

---

## 文案模板

### 标题模板（20字内）
- GEO：让AI帮你做营销
- 什么是生成引擎优化？
- AI搜索时代，品牌如何占位
- GEO vs SEO：营销新战场
- 3分钟看懂GEO优化

### 描述模板（50字内）
- 🔍 什么是GEO？生成引擎优化（Generative Engine Optimization）让您的品牌在AI回答中被提及！#GEO #AI营销
- 💡 AI搜索已来，传统SEO还不够！GEO优化让品牌在AI回答中脱颖而出 #生成引擎优化
- ⚡ GEO（生成引擎优化）：下一代搜索营销，现在布局正当时！#AI #营销

---

## ffmpeg 常用命令

### 查看视频信息
```bash
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

### 仅拼接（不重编码，快速）
```bash
ffmpeg -f concat -safe 0 -i concat-list.txt -c copy output.mp4
```

### 重编码拼接（兼容性好）
```bash
ffmpeg -f concat -safe 0 -i concat-list.txt -c:v libx264 -c:a aac output.mp4
```

### 调整视频分辨率（适配平台）
```bash
ffmpeg -i input.mp4 -vf scale=1920:1080 output-1080p.mp4
```

### 提取音频
```bash
ffmpeg -i video.mp4 -vn -c:a copy audio.aac
```
