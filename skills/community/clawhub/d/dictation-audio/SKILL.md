---
name: dictation-audio
description: 根据英语单词生成听写音频，每个单词读两遍，中间停顿1秒
author:
  name: Maosi English Team
  github: https://github.com/effecE
homepage: https://clawhub.com
license: Apache-2.0
metadata:
  {
    "openclaw":
      {
        "version": "1.1.0",
        "emoji": "🔊",
        "tags": ["english", "dictation", "audio", "education"],
        "requires": { "bins": ["edge-tts", "ffmpeg"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "edge-tts",
              "label": "Install edge-tts (pip)",
            },
          ],
      },
  }
---

# Dictation Audio Generator

根据英语单词生成听写音频，每个单词读两遍，中间停顿1秒。

## 作者
**Maosi English Team**

## 使用方法

```bash
# 交互式输入
python3 dictation.py

# 或使用管道
echo -e "band\npractise\nsharp" | python3 dictation.py
```

## 输入格式
每行一个单词，支持格式：
- `word` - 纯英文单词
- `word中文` - 带中文注释（如 `band乐队` 会自动提取 `band`）

## 输出
生成 `/tmp/dictation.mp3` 文件

## 音频格式
- 语音：en-GB-RyanNeural
- 语速：-20%
- 停顿：1秒
- 朗读顺序：单词1 → 停顿 → 单词1 → 停顿 → 单词2 → 停顿 → 单词2 → ...

## 示例

**输入：**
```
band
practise
sharp
need
```

**输出：** 4个单词的听写音频，每个单词读两遍，单词间停顿1秒

## 技术实现

1. **输入验证**：正则过滤，只保留英文字母、空格和连字符
2. **依赖检查**：使用 `shutil.which()` 验证工具存在
3. **音频生成**：调用 edge-tts 生成单词音频
4. **静音生成**：ffmpeg 生成1秒静音片段
5. **音频合并**：ffmpeg concat 合并所有片段

## 安全设计

- ✅ **依赖验证**：启动时检查 edge-tts 和 ffmpeg 是否可用
- ✅ **输入过滤**：正则验证，只允许英文字母、空格和连字符
- ✅ **长度限制**：单词最大100字符
- ✅ **临时目录**：所有中间文件在系统临时目录，不暴露敏感路径
- ✅ **subprocess安全**：使用 `shutil.which()` 验证工具路径，参数列表传递
- ✅ **超时保护**：30秒超时防止进程挂起
- ✅ **资源清理**：临时文件自动清理

## License
Apache License 2.0
