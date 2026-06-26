# 音频路由与大文件处理策略

> **何时必须阅读本文件**：
> - 输入是公网 `http://` / `https://` URL
> - 音频超过 2 小时
> - 文件可能超过 100MB
> - 需要在 `asr_flash.py`（极速版）与 `asr_standard.py`（标准版）之间做选择

## 硬阈值

| 常量 | 值 | 说明 |
|------|----|------|
| `EXPRESS_MAX_SECONDS` | 7200（2 小时） | 极速版最大时长 |
| `EXPRESS_MAX_BYTES` | 104857600（100MB） | 极速版最大文件 |
| `STANDARD_MAX_SECONDS` | 18000（5 小时） | 标准版最大时长 |

## 核心路由规则

### 公网 URL

- **默认直接走标准版**：`python3 asr_standard.py --url "<PUBLIC_URL>"`
- 不要先下载到本地、探测、转码再路由
- 只有标准版真实失败时，再按错误分流

### 本地文件

1. **先探测**：
   ```bash
   python3 inspect_audio.py "<LOCAL_AUDIO_FILE>"
   ```
   如果返回 `REQUIRES_FFPROBE`，先执行：
   ```bash
   python3 ensure_ffmpeg.py --execute
   ```

2. **按时长和文件大小选择脚本**：

   | 条件 | 脚本 |
   |------|------|
   | 时长 ≤ 2h 且 大小 ≤ 100MB | `asr_flash.py --file "<FILE>"` （极速版） |
   | 2h < 时长 ≤ 5h | `asr_standard.py --file "<FILE>"` （标准版） |
   | 时长 > 5h | 不支持，需先切分 |
   | 无法获取时长 且 大小 ≤ 100MB | `asr_flash.py --file "<FILE>"` （极速版兜底） |
   | 无法获取时长 且 大小 > 100MB | `asr_standard.py --file "<FILE>"` （标准版兜底） |

3. **时长 > 5h 的切片方案**：
   ```bash
   ffmpeg -y -i "<INPUT>" -f segment -segment_time 7200 \
     -c:a pcm_s16le -ar 16000 -ac 1 "<SEGMENT_DIR>/part_%03d.wav"
   ```
   切片后逐片走 `asr_flash.py`（极速版），最后按文件名顺序拼接文本。

## URL 失败后的处理

当 `asr_standard.py --url` 失败时：

1. **URL 不可访问** → 提示用户换成可公网下载的 URL
2. **时长超过 5h** → 下载到本地 → 切片后逐片走极速版
3. **格式/解码失败** → 下载到本地 → FFmpeg 规范化后走本地链

## 脚本上传方式对照

| 脚本 | 本地文件 | URL |
|------|----------|-----|
| `asr_flash.py`（极速版） | 支持（base64 body） | 支持（url 字段） |
| `asr_standard.py`（标准版） | 支持（base64 body） | 支持（url 字段） |

## 为什么 URL 默认走标准版

- URL 场景下无法预知音频时长和文件大小
- 标准版支持 ≤5h，覆盖范围更广
- 极速版对 URL 也支持，但有 2h/100MB 限制，可能静默失败
