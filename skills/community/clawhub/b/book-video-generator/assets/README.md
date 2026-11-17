# 素材文件说明

本目录用于存放视频合成的可选音频素材。**这些文件是可选的**——如果缺失，视频仍可正常生成，只是没有背景音乐和转场音效。

## 所需文件

| 文件名 | 用途 | 大小 | 必需性 |
|--------|------|------|--------|
| `bgm_reading.mp3` | 背景音乐（全程循环，音量0.15） | ~9MB | 可选 |
| `transition_page_flip.mp3` | 转场音效（翻页声，每3个分镜触发） | ~3KB | 可选 |

## 获取方式

### 方式1：自行下载免费素材

- **BGM**：从 [Pixabay Music](https://pixabay.com/music/) 或 [Free Music Archive](https://freemusicarchive.org/) 下载轻柔的阅读背景音乐，重命名为 `bgm_reading.mp3`
- **翻页音效**：从 [Pixabay Sound Effects](https://pixabay.com/sound-effects/) 搜索 "page flip" 或 "page turn"，下载后重命名为 `transition_page_flip.mp3`

### 方式2：用 ffmpeg 生成简单音效

```bash
# 生成一个简单的翻页音效（白噪声+衰减）
ffmpeg -f lavfi -i "anoisesrc=d=0.15:c=pink:a=0.5" -af "afade=t=in:st=0:d=0.02,afade=t=out:st=0.1:d=0.05" assets/transition_page_flip.mp3
```

### 方式3：从 GitHub 仓库获取

如果本技能有对应的 GitHub 仓库，可以从仓库的 `assets/` 目录下载这些文件。

## 代码处理逻辑

`compose_video.py` 中的 `_find_asset()` 函数会按以下顺序查找：
1. 脚本同级 `assets/` 目录
2. 脚本父级 `assets/` 目录（技能根目录）
3. 脚本同级目录

如果找不到文件，`mix_audio()` 函数会自动跳过混音步骤，直接输出仅含 TTS 旁白的视频。
