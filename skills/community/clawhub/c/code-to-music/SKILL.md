---
name: code-to-music
description: 把代码文件转换成音乐 — 分析代码结构特征（行数、函数、缩进、关键字等），映射成音乐参数（BPM、调性、乐器、节奏），调用 MiniMax music-2.6 API 生成独一无二的"代码交响曲"。适合给老大玩、记录代码、或者纯粹中二一下。
---

# Code to Music — 代码交响曲

把代码文件转成音乐，听起来像什么由代码结构决定。

## 工作原理

代码特征 → 音乐参数的映射：

| 代码特征 | 音乐参数 | 说明 |
|---------|---------|------|
| 总行数 | BPM | 行数越多→节奏越快 |
| 最大缩进深度 | 调性 | 深缩进→低音调，浅→高音调 |
| 函数数量 | 乐器丰富度 | 函数越多→乐器越丰富 |
| 关键字数量 | 节奏复杂度 | 关键字越多→节奏越碎 |
| 字符串数量 | 情绪张力 | 字符串多→更戏剧化 |
| 注释比例 | 人声比例 | 注释多→加入人声和声 |

## 使用方法

### 1. 准备

确保环境变量已配置：
```bash
set MINIMAX_API_KEY=your-api-key
set MINIMAX_API_HOST=https://api.minimaxi.com
```

### 2. 运行

```bash
python scripts/code2music.py "代码文件路径" [输出路径]
```

**示例：**
```bash
# 生成音乐到默认路径
python scripts/code2music.py "C:\project\app.js"

# 指定输出路径
python scripts/code2music.py "C:\project\app.js" "C:\music\my_code.mp3"
```

### 3. 听取

生成完成后，文件保存在 `code_symphony.mp3`，直接用播放器打开即可。

## 示例输出

以 `content.js`（333行，115函数）为例：
- BPM: 126
- 调性: G major
- 乐器: piano, strings, brass ensemble
- 情绪: dramatic, emotional crescendo
- 人声: whispers

生成约 1.1MB 的 MP3 文件。

## 依赖

- Python 3.x
- requests 库
- MiniMax API Key（需要 music-2.6 权限）

## 限制

- MiniMax music-2.6 模型需要账号有音乐生成额度
- 歌词固定为英文（后续可扩展多语言）
- 最大支持文件大小视 API 限制而定
