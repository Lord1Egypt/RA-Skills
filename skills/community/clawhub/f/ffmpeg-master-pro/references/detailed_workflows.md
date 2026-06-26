# 详细工作流文档

本文档提供 ffmpeg-master 技能所有工作流的详细说明和实现细节。

## 目录

- [工作流 1：智能转码与压缩](#工作流1智能转码与压缩)
- [工作流 2：智能参数优化](#工作流2智能参数优化)
- [工作流 3：预设模板系统](#工作流3预设模板系统)
- [工作流 4：精确文件大小控制](#工作流4精确文件大小控制)
- [工作流 5：Smart Cut 混合剪辑](#工作流5smart-cut-混合剪辑)
- [工作流 6：关键帧分析](#工作流6关键帧分析)
- [工作流 7：字幕处理](#工作流7字幕处理)
- [工作流 8：滤镜与特效](#工作流8滤镜与特效)
- [工作流 9：GIF 转换](#工作流9gif转换)
- [工作流 10：翻转与镜像](#工作流10翻转与镜像)
- [工作流 11：速度调节](#工作流11速度调节)
- [工作流 12：音频提取与移除](#工作流12音频提取与移除)
- [工作流 13：视频合并](#工作流13视频合并)
- [工作流 14：宽高比调整](#工作流14宽高比调整)
- [附录：批量处理](#附录批量处理)
- [附录：实时进度反馈](#附录实时进度反馈)

---

## 工作流1：智能转码与压缩

### 触发条件

- 用户提到"压缩""转码""格式转换""减小文件"
- 需要指定目标大小或质量要求

### 执行步骤

#### 1. 输入分析

使用 FFmpeg probe 分析源视频：

```python
import subprocess
import json

def analyze_video(input_file):
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        input_file
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    metadata = json.loads(result.stdout)

    # 提取关键信息
    video_stream = next(s for s in metadata['streams'] if s['codec_type'] == 'video')
    audio_stream = next(s for s in metadata['streams'] if s['codec_type'] == 'audio')

    return {
        'format': metadata['format']['format_name'],
        'codec': video_stream['codec_name'],
        'width': int(video_stream['width']),
        'height': int(video_stream['height']),
        'fps': eval(video_stream['r_frame_rate']),
        'bitrate': int(metadata['format']['bitrate']) if 'bitrate' in metadata['format'] else 0,
        'duration': float(metadata['format']['duration'])
    }
```

#### 2. 码率计算

三模型融合算法：

```python
def calculate_bitrate(video_info, target_size_mb=None):
    # 模型 1：基于分辨率的基础码率
    base_bitrate = (
        video_info['width'] *
        video_info['height'] *
        video_info['fps'] *
        0.05  # 运动因子
    ) / 1000

    # 模型 2：基于内容复杂度的调整
    complexity_multiplier = 1.0  # 可通过内容分析调整
    complexity_bitrate = base_bitrate * complexity_multiplier

    # 模型 3：基于目标大小的反推
    if target_size_mb:
        target_bitrate = (
            target_size_mb * 1024 * 8 /
            video_info['duration']
        ) * 0.95  # 5% 缓冲
    else:
        target_bitrate = complexity_bitrate

    # 融合决策（加权平均）
    final_bitrate = (
        base_bitrate * 0.25 +
        complexity_bitrate * 0.35 +
        target_bitrate * 0.40
    )

    return final_bitrate
```

#### 3. GPU 检测

自动检测可用的硬件加速：

```python
def detect_gpu():
    # 检测 NVIDIA GPU
    try:
        subprocess.run(['nvidia-smi'], check=True, capture_output=True)
        return {
            'type': 'nvidia',
            'encoder': 'h264_nvenc',
            'preset': 'p4'
        }
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 检测 AMD GPU
    try:
        subprocess.run(['amdgpu-info'], check=True, capture_output=True)
        return {
            'type': 'amd',
            'encoder': 'h264_amf',
            'preset': 'balanced'
        }
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 检测 Intel QSV
    try:
        subprocess.run(['vainfo'], check=True, capture_output=True)
        return {
            'type': 'intel',
            'encoder': 'h264_qsv',
            'preset': 'medium'
        }
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 回退到 CPU
    return {
        'type': 'cpu',
        'encoder': 'libx264',
        'preset': 'medium'
    }
```

#### 4. 参数优化

根据内容类型选择最优编码预设：

```python
def optimize_parameters(video_info, gpu_info, target_bitrate):
    params = {
        'codec': gpu_info['encoder'],
        'preset': gpu_info['preset'],
        'crf': 23,  # 默认质量因子
        'bitrate': target_bitrate,
        'maxrate': target_bitrate * 1.2,
        'bufsize': target_bitrate * 2
    }

    # 根据分辨率调整
    if video_info['width'] >= 3840:  # 4K
        params['crf'] = 20
    elif video_info['width'] >= 1920:  # 1080p
        params['crf'] = 23
    else:  # 720p 或更低
        params['crf'] = 25

    return params
```

#### 5. 执行转换

构建并执行 FFmpeg 命令：

```python
def transcode(input_file, output_file, params):
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', params['codec'],
        '-b:v', f"{params['bitrate']}k",
        '-maxrate', f"{params['maxrate']}k",
        '-bufsize', f"{params['bufsize']}k",
        '-preset', params['preset'],
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        output_file
    ]

    subprocess.run(cmd, check=True)
```

#### 6. 质量验证

验证输出文件：

```python
def validate_output(input_file, output_file, target_size_mb=None):
    # 检查文件大小
    output_size = os.path.getsize(output_file) / (1024 * 1024)

    if target_size_mb:
        error = abs(output_size - target_size_mb) / target_size_mb
        if error > 0.05:  # 5% 误差阈值
            return False, f"文件大小偏差 {error*100:.2f}%"

    # 检查时长
    input_duration = get_duration(input_file)
    output_duration = get_duration(output_file)

    if abs(input_duration - output_duration) > 1:  # 1秒误差
        return False, "时长不匹配"

    return True, "验证通过"
```

---

## 工作流2：智能参数优化

### 视频类型识别

自动识别 6 种视频类型：

```python
from enum import Enum
from dataclasses import dataclass

class VideoContentType(Enum):
    SCREEN_RECORDING = "screen_recording"
    ANIME = "anime"
    SPORTS = "sports"
    MUSIC_VIDEO = "music_video"
    MOVIE = "movie"
    VINTAGE = "vintage"

@dataclass
class VideoAnalysisResult:
    content_type: VideoContentType
    confidence: float
    motion_score: float
    complexity_score: float
    color_score: float

def analyze_video_type_deep(video_path):
    """深度分析视频类型"""

    # 1. 分析运动幅度
    motion_score = analyze_motion(video_path)

    # 2. 分析场景复杂度
    complexity_score = analyze_complexity(video_path)

    # 3. 分析色彩分布
    color_score = analyze_color(video_path)

    # 4. 融合分析结果
    result = classify_video_type(
        motion_score,
        complexity_score,
        color_score
    )

    return result
```

### 智能参数选择

```python
def get_optimized_encoding_params(
    video_path,
    quality_preference="balanced",
    manual_content_type=None
):
    """获取优化的编码参数"""

    # 1. 识别视频类型（或使用手动指定）
    if manual_content_type:
        content_type = manual_content_type
    else:
        analysis = analyze_video_type_deep(video_path)
        if analysis.confidence < 0.5:
            # 低置信度，建议用户确认
            return suggest_manual_selection(analysis)
        content_type = analysis.content_type

    # 2. 获取该类型的预设参数
    preset_params = CONTENT_TYPE_PRESETS[content_type]

    # 3. 根据质量偏好调整
    params = adjust_for_quality_preference(
        preset_params,
        quality_preference
    )

    # 4. 检测并应用 GPU 加速
    gpu_info = detect_gpu()
    if gpu_info['type'] != 'cpu':
        params = apply_gpu_optimization(params, gpu_info)

    return params

# 内容类型预设参数
CONTENT_TYPE_PRESETS = {
    VideoContentType.SCREEN_RECORDING: {
        'codec': 'libx264',
        'preset': 'veryfast',
        'crf': 18,
        'tune': 'zerolatency',
        'description': '屏幕录制：低运动、低复杂度，快速编码低延迟'
    },
    VideoContentType.ANIME: {
        'codec': 'libx264',
        'preset': 'slow',
        'crf': 20,
        'tune': 'animation',
        'description': '动漫：低色彩、线条清晰，保护线条和色块'
    },
    VideoContentType.SPORTS: {
        'codec': 'libx264',
        'preset': 'fast',
        'crf': 22,
        'tune': 'fastdecode',
        'description': '体育：高运动、高复杂度，处理快速运动'
    },
    VideoContentType.MUSIC_VIDEO: {
        'codec': 'libx264',
        'preset': 'medium',
        'crf': 21,
        'tune': None,
        'description': '音乐视频：高复杂度、色彩丰富'
    },
    VideoContentType.MOVIE: {
        'codec': 'libx264',
        'preset': 'slow',
        'crf': 23,
        'tune': 'film',
        'description': '电影：中等运动、叙事内容'
    },
    VideoContentType.VINTAGE: {
        'codec': 'libx264',
        'preset': 'veryslow',
        'crf': 22,
        'tune': 'grain',
        'description': '老旧视频：低色彩、高噪声，保护胶片颗粒'
    }
}
```

---

## 工作流3：预设模板系统

### 内置预设模板

每个预设都是 JSON 格式：

```json
{
  "name": "预设名称",
  "description": "预设描述",
  "version": "1.0",
  "video": {
    "codec": "libx264",
    "preset": "medium",
    "crf": 23,
    "profile": "high",
    "level": "4.1",
    "pixel_format": "yuv420p",
    "movflags": "+faststart"
  },
  "audio": {
    "codec": "aac",
    "bitrate": "192k",
    "sample_rate": 48000,
    "channels": 2
  },
  "recommendations": {
    "1080p": {
      "resolution": "1920x1080",
      "bitrate": "8000k",
      "audio_bitrate": "192k"
    }
  },
  "requirements": {
    "max_bitrate": "6000k",
    "supported_codecs": ["H.264", "H.265"],
    "max_file_size": "8GB"
  }
}
```

### 预设管理

```python
import json
import os
from pathlib import Path

class PresetManager:
    def __init__(self):
        self.builtin_presets_dir = Path(__file__).parent.parent / 'assets' / 'presets'
        self.user_presets_dir = Path.home() / '.config' / 'ffmpeg-master' / 'presets'
        self.user_presets_dir.mkdir(parents=True, exist_ok=True)

    def list_available_presets(self):
        """列出所有可用预设"""
        presets = {}

        # 加载内置预设
        for preset_file in self.builtin_presets_dir.glob('*.json'):
            with open(preset_file, 'r', encoding='utf-8') as f:
                preset = json.load(f)
                presets[preset['name']] = preset

        # 加载用户预设
        if self.user_presets_dir.exists():
            for preset_file in self.user_presets_dir.glob('*.json'):
                with open(preset_file, 'r', encoding='utf-8') as f:
                    preset = json.load(f)
                    presets[preset['name']] = preset

        return presets

    def get_preset_info(self, preset_name):
        """获取预设详细信息"""
        presets = self.list_available_presets()
        return presets.get(preset_name)

    def create_custom_preset(self, name, preset_config):
        """创建自定义预设"""
        output_file = self.user_presets_dir / f'{name}.json'

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(preset_config.dict(), f, indent=2, ensure_ascii=False)

        return True

    def recognize_preset_from_nlu(self, user_input):
        """从自然语言识别预设"""
        user_input_lower = user_input.lower()

        # 关键词映射
        keywords = {
            'bilibili': ['b站', 'bilibili', '哔哩哔哩'],
            'youtube': ['youtube', 'yt', '油管'],
            'wechat': ['微信', 'wechat'],
            'douyin': ['抖音', 'douyin'],
            'social_media': ['社交', 'social', 'instagram', 'tiktok'],
            'archival': ['存档', '备份', 'archive'],
            'preview': ['预览', 'preview'],
            'web_optimized': ['网站', 'web', '在线']
        }

        for preset_name, keywords_list in keywords.items():
            if any(keyword in user_input_lower for keyword in keywords_list):
                return preset_name

        return None
```

---

## 工作流4：精确文件大小控制

### 两遍编码实现

```python
class TwoPassEncoder:
    def __init__(self):
        self.gpu_info = detect_gpu()

    def encode(self, input_file, output_file, target_size_mb, duration_seconds, progress_callback=None):
        """两遍编码"""

        # 1. 计算目标码率
        audio_bitrate = 128  # kbps
        target_bitrate = (
            target_size_mb * 1024 * 8 /
            duration_seconds
        ) - audio_bitrate

        # 2. 第一遍：分析
        if progress_callback:
            progress_callback(ProgressUpdate(
                pass_number=1,
                percentage=0,
                status="分析视频..."
            ))

        pass1_cmd = [
            'ffmpeg',
            '-i', input_file,
            '-c:v', self.gpu_info['encoder'],
            '-b:v', f'{target_bitrate}k',
            '-pass', '1',
            '-f', 'null',
            '-'
        ]

        subprocess.run(pass1_cmd, check=True)

        # 3. 第二遍：编码
        if progress_callback:
            progress_callback(ProgressUpdate(
                pass_number=2,
                percentage=0,
                status="编码视频..."
            ))

        pass2_cmd = [
            'ffmpeg',
            '-i', input_file,
            '-c:v', self.gpu_info['encoder'],
            '-b:v', f'{target_bitrate}k',
            '-pass', '2',
            '-c:a', 'aac',
            '-b:a', f'{audio_bitrate}k',
            output_file
        ]

        subprocess.run(pass2_cmd, check=True)

        # 4. 验证结果
        actual_size = os.path.getsize(output_file) / (1024 * 1024)
        error = abs(actual_size - target_size_mb) / target_size_mb

        return {
            'success': error < 0.05,
            'actual_size_mb': actual_size,
            'target_size_mb': target_size_mb,
            'error_pct': error
        }
```

### 自适应码率控制

```python
class AdaptiveBitrateController:
    def __init__(self):
        self.min_bitrate = 500  # kbps
        self.max_bitrate = 50000  # kbps

    def adjust_bitrate(self, current_bitrate, target_size_mb, actual_size_mb, attempt):
        """自适应调整码率"""

        error = (actual_size_mb - target_size_mb) / target_size_mb

        if abs(error) < 0.05:
            # 误差在 5% 以内，保持当前码率
            return current_bitrate

        # 按比例调整（使用加权移动平均避免震荡）
        adjustment_factor = 1.0 - error

        # 限制调整幅度（避免过度调整）
        adjustment_factor = max(0.7, min(1.3, adjustment_factor))

        new_bitrate = current_bitrate * adjustment_factor

        # 限制在合理范围内
        return max(self.min_bitrate, min(self.max_bitrate, new_bitrate))
```

### 质量评估

```python
def assess_quality(input_file, output_file, metric='basic'):
    """评估视频质量"""

    if metric == 'basic':
        # 基础检查
        input_info = get_video_info(input_file)
        output_info = get_video_info(output_file)

        # 检查分辨率
        if input_info['resolution'] != output_info['resolution']:
            return {'passed': False, 'score': 0, 'reason': '分辨率不匹配'}

        # 检查时长
        if abs(input_info['duration'] - output_info['duration']) > 1:
            return {'passed': False, 'score': 0, 'reason': '时长不匹配'}

        # 检查文件大小合理性
        compression_ratio = (
            os.path.getsize(output_file) /
            os.path.getsize(input_file)
        )

        if compression_ratio > 1.0:
            return {'passed': False, 'score': 0, 'reason': '文件变大'}
        elif compression_ratio < 0.1:
            return {'passed': False, 'score': 0, 'reason': '压缩过度'}

        return {'passed': True, 'score': 0.8, 'metric': 'basic'}

    elif metric == 'psnr':
        # PSNR 评估
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-i', output_file,
            '-lavfi', 'psnr',
            '-f', 'null',
            '-'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        # 解析 PSNR 值
        psnr = parse_psnr(result.stderr)

        return {
            'passed': psnr > 30,
            'score': psnr,
            'metric': 'psnr',
            'threshold': 30
        }

    elif metric == 'ssim':
        # SSIM 评估
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-i', output_file,
            '-lavfi', 'ssim',
            '-f', 'null',
            '-'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        # 解析 SSIM 值
        ssim = parse_ssim(result.stderr)

        return {
            'passed': ssim > 0.90,
            'score': ssim,
            'metric': 'ssim',
            'threshold': 0.90
        }
```

---

## 工作流5：Smart Cut 混合剪辑

Smart Cut 混合剪辑是一种智能剪辑策略，结合了快速模式和精确模式的优势，在关键帧附近进行精确切割，在非关键帧区域使用快速模式。

### 主要特性

- **自动检测关键帧位置**：智能识别视频中的所有关键帧
- **三种剪辑模式**：
  - 快速模式：在最近的关键帧处剪切，速度最快
  - 精确模式：在指定位置精确剪切，质量最高
  - Smart Cut 混合模式：根据场景自动选择最佳策略
- **自动音视频同步修复**：剪辑后自动修复音视频同步问题
- **剪辑点质量评估**：评估每个剪辑点的质量等级（excellent/good/fair/poor）

### 详细文档

Smart Cut 的完整实现细节、使用方法和最佳实践，请参考：

📖 [Smart Cut 详细指南 →](smart_cut_guide.md)

### 快速示例

```bash
# 快速模式剪辑（在最近关键帧处剪切）
ffmpeg -y -hide_banner -ss 00:01:00 -i "input.mp4" -to 00:00:30 -c copy "output.mp4"

# 精确模式剪辑（精确到指定位置）
ffmpeg -y -hide_banner -i "input.mp4" -ss 00:01:00 -t 00:00:30 -c:v libx264 -c:a aac "output.mp4"

# Smart Cut 混合模式（自动选择最佳策略）
# 请参考 smart_cut_guide.md 中的 Python 实现
```

---

## 工作流6：关键帧分析

关键帧分析是智能剪辑的基础，它可以帮助识别视频中最佳的剪辑点位置。

### 主要功能

- **关键帧时间轴导出**：支持导出为 JSON、CSV、Markdown、TXT 格式
- **剪辑点质量评估**：自动评估每个关键帧的质量等级
- **智能分段策略建议**：根据视频内容提供最优的分段建议
- **场景变化检测**：识别场景转换点

### 详细文档

关键帧分析的完整实现、使用方法和 API 参考，请参考：

📖 [关键帧分析详细指南 →](keyframe_analysis.md)

### 快速示例

```python
# 导出关键帧时间轴（JSON 格式）
ffmpeg -y -hide_banner -i "input.mp4" -vf "select=eq(pict_type\,I)" -vsync 0 -f json "keyframes.json"

# 导出关键帧时间轴（CSV 格式）
ffmpeg -y -hide_banner -i "input.mp4" -vf "select=eq(pict_type\,I)" -vsync 0 -f csv "keyframes.csv"

# 导出关键帧时间轴（Markdown 格式）
ffmpeg -y -hide_banner -i "input.mp4" -vf "select=eq(pict_type\,I)" -vsync 0 "keyframes.txt"
```

---

## 工作流7：字幕处理

### 字幕提取

```python
def extract_subtitle(input_file, output_file, stream_index):
    """提取字幕流"""

    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-map', f'0:s:{stream_index}',
        '-c', 'srt',
        output_file
    ]

    subprocess.run(cmd, check=True)
```

### 字幕嵌入

```python
def embed_subtitle(input_file, subtitle_file, output_file):
    """嵌入字幕（软字幕）"""

    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-i', subtitle_file,
        '-c', 'copy',
        '-c:s', 'mov_text',
        '-metadata:s:s:0', 'language=chi',
        output_file
    ]

    subprocess.run(cmd, check=True)
```

### 字幕烧录

```python
def burn_subtitle(input_file, subtitle_file, output_file):
    """烧录字幕（硬字幕）"""

    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', f"subtitles={subtitle_file}:force_style='FontName=Microsoft YaHei,FontSize=24'",
        '-c:a', 'copy',
        output_file
    ]

    subprocess.run(cmd, check=True)
```

---

## 工作流8：滤镜与特效

### 水印叠加

```python
def add_watermark(input_file, watermark_file, output_file, position='bottom-right'):
    """添加水印"""

    # 计算水印位置
    video_info = get_video_info(input_file)
    width, height = video_info['resolution']

    positions = {
        'top-left': (10, 10),
        'top-right': (width - 210, 10),
        'bottom-left': (10, height - 110),
        'bottom-right': (width - 210, height - 110)
    }

    x, y = positions[position]

    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-i', watermark_file,
        '-filter_complex',
        f"[0:v][1:v]overlay={x}:{y}:format=auto,format=yuv420p",
        '-c:a', 'copy',
        output_file
    ]

    subprocess.run(cmd, check=True)
```

### 视频旋转

```python
def rotate_video(input_file, output_file, degrees):
    """旋转视频"""

    radians = degrees * math.pi / 180

    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vf', f"rotate={radians}:transpose=clock",
        '-c:a', 'copy',
        output_file
    ]

    subprocess.run(cmd, check=True)
```

### 帧翻转

```python
def flip_video(input_file, output_file, flip_type='horizontal'):
    """翻转视频画面"""

    flip_filters = {
        'horizontal': 'hflip',      # 水平翻转（左右镜像）
        'vertical': 'vflip',        # 垂直翻转（上下镜像）
        'both': 'hflip,vflip'       # 组合翻转（180°旋转）
    }

    if flip_type not in flip_filters:
        raise ValueError(f"不支持的翻转类型: {flip_type}")

    cmd = [
        'ffmpeg',
        '-y',
        '-hide_banner',
        '-i', input_file,
        '-vf', flip_filters[flip_type],
        '-c:a', 'copy',
        output_file
    ]

    subprocess.run(cmd, check=True)
```

#### 帧翻转使用示例

```bash
# 水平翻转（左右镜像）
ffmpeg -y -hide_banner -i "input.mp4" -vf "hflip" -c:a copy "output.mp4"

# 垂直翻转（上下镜像）
ffmpeg -y -hide_banner -i "input.mp4" -vf "vflip" -c:a copy "output.mp4"

# 组合翻转（180°旋转）
ffmpeg -y -hide_banner -i "input.mp4" -vf "hflip,vflip" -c:a copy "output.mp4"
```

#### 翻转类型说明

| 滤镜 | 效果 | 使用场景 |
|------|------|---------|
| `hflip` | 水平翻转（左右镜像） | 自拍镜像、文字左右翻转 |
| `vflip` | 垂直翻转（上下镜像） | 倒置视频效果 |
| `hflip,vflip` | 组合翻转（180°旋转） | 完全倒置 |

---

## 工作流9：GIF转换

### 触发条件
- 用户提到"GIF""动图""转GIF""做动图"

### 执行步骤

#### 基础 GIF 转换

```bash
ffmpeg -y -hide_banner -i "INPUT" -ss START -t DURATION -vf "fps=15,scale=480:-1:flags=lanczos" -loop 0 "OUTPUT.gif"
```

#### 高质量 GIF（两遍调色板优化）

第一遍生成调色板，第二遍使用调色板生成 GIF，色彩保真度更高：

```bash
# 第一遍：生成调色板
ffmpeg -y -i "INPUT" -ss START -t DURATION -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" "palette.png"

# 第二遍：使用调色板
ffmpeg -y -i "INPUT" -i "palette.png" -ss START -t DURATION -lavfi "fps=15,scale=480:-1:flags=lanczos [x]; [x][1:v] paletteuse" "OUTPUT.gif"
```

### 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| fps | 帧率，越低文件越小 | 10-15（动图），24-30（流畅） |
| scale | 分辨率，宽度固定高度自适应 | 480（标准），640（高清） |
| flags=lanczos | 高质量缩放算法 | 固定 |
| -loop 0 | 无限循环 | 固定 |
| -t | 持续时长（秒） | 建议≤10秒，避免文件过大 |

### 示例

```bash
# 将 0:10-0:15 的片段转为 GIF
ffmpeg -y -hide_banner -i "video.mp4" -ss 00:00:10 -t 5 -vf "fps=15,scale=480:-1:flags=lanczos" -loop 0 "clip.gif"

# 高质量 GIF（带调色板优化）
ffmpeg -y -i "video.mp4" -ss 00:00:10 -t 5 -vf "fps=15,scale=640:-1:flags=lanczos,palettegen" "palette.png"
ffmpeg -y -i "video.mp4" -i "palette.png" -ss 00:00:10 -t 5 -lavfi "fps=15,scale=640:-1:flags=lanczos [x]; [x][1:v] paletteuse" "clip_hq.gif"
```

---

## 工作流10：翻转与镜像

### 触发条件
- 用户提到"翻转""镜像""左右翻转""上下翻转""水平翻转""垂直翻转"

### 翻转类型

#### 水平翻转（左右镜像）

```bash
ffmpeg -y -hide_banner -i "INPUT" -vf "hflip" -c:a copy "OUTPUT"
```

#### 垂直翻转（上下翻转）

```bash
ffmpeg -y -hide_banner -i "INPUT" -vf "vflip" -c:a copy "OUTPUT"
```

#### 180°旋转（组合翻转）

```bash
ffmpeg -y -hide_banner -i "INPUT" -vf "hflip,vflip" -c:a copy "OUTPUT"
```

### 与旋转工作流的区别

| 操作 | 滤镜 | 说明 |
|------|------|------|
| 顺时针90° | transpose=1 | 带元数据旋转，兼容性好 |
| 逆时针90° | transpose=2 | 带元数据旋转，兼容性好 |
| 水平镜像 | hflip | 像素级翻转，不改变分辨率方向 |
| 垂直镜像 | vflip | 像素级翻转，不改变分辨率方向 |

### 示例

```bash
# 左右镜像
ffmpeg -y -hide_banner -i "selfie.mp4" -vf "hflip" -c:a copy "selfie_mirror.mp4"

# 上下翻转
ffmpeg -y -hide_banner -i "video.mp4" -vf "vflip" -c:a copy "video_flipped.mp4"
```

---

## 工作流11：速度调节

### 触发条件
- 用户提到"加速""慢动作""2倍速""0.5倍速""延时""timelapse""slowmo"

### 速度公式

| 速度 | 视频滤镜 | 音频滤镜 |
|------|---------|---------|
| 2x 加速 | setpts=0.5\*PTS | atempo=2.0 |
| 4x 加速 | setpts=0.25\*PTS | atempo=2.0,atempo=2.0（链式） |
| 0.5x 慢动作 | setpts=2.0\*PTS | atempo=0.5 |
| 0.25x 慢动作 | setpts=4.0\*PTS | atempo=0.5,atempo=0.5（链式） |

### 注意事项
- `atempo` 范围：0.5 ~ 2.0，超出范围需链式调用（如 4x = atempo=2.0,atempo=2.0）
- 视频无此限制，任意倍速均可

### 仅视频变速（无音频）

```bash
# 2倍速
ffmpeg -y -hide_banner -i "INPUT" -vf "setpts=0.5*PTS" -an "OUTPUT"

# 慢动作 0.5x
ffmpeg -y -hide_banner -i "INPUT" -vf "setpts=2.0*PTS" -an "OUTPUT"
```

### 音视频同步变速

```bash
# 2倍速（音视频同步）
ffmpeg -y -hide_banner -i "INPUT" -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" "OUTPUT"

# 0.5x 慢动作（音视频同步）
ffmpeg -y -hide_banner -i "INPUT" -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" "OUTPUT"

# 4倍速（链式 atempo）
ffmpeg -y -hide_banner -i "INPUT" -filter_complex "[0:v]setpts=0.25*PTS[v];[0:a]atempo=2.0,atempo=2.0[a]" -map "[v]" -map "[a]" "OUTPUT"
```

### 链式 atempo 速查表

| 目标倍速 | atempo 链 |
|---------|----------|
| 0.25x | atempo=0.5,atempo=0.5 |
| 0.125x | atempo=0.5,atempo=0.5,atempo=0.5 |
| 4x | atempo=2.0,atempo=2.0 |
| 8x | atempo=2.0,atempo=2.0,atempo=2.0 |
| 16x | atempo=2.0,atempo=2.0,atempo=2.0,atempo=2.0 |

---

## 工作流12：音频提取与移除

### 触发条件
- 用户提到"提取音频""导出音乐""去音频""静音""只要音频""去掉声音"

### 提取音频

```bash
# 提取为 MP3
ffmpeg -y -hide_banner -i "INPUT" -vn -acodec libmp3lame -q:a 2 "OUTPUT.mp3"

# 提取为 AAC
ffmpeg -y -hide_banner -i "INPUT" -vn -acodec aac -b:a 192k "OUTPUT.m4a"

# 提取为 WAV（无损）
ffmpeg -y -hide_banner -i "INPUT" -vn -acodec pcm_s16le "OUTPUT.wav"

# 提取为 FLAC（无损压缩）
ffmpeg -y -hide_banner -i "INPUT" -vn -acodec flac "OUTPUT.fla"

# 提取为 OGG
ffmpeg -y -hide_banner -i "INPUT" -vn -acodec libvorbis -q:a 5 "OUTPUT.ogg"
```

### 移除音频

```bash
# 移除音频轨道（静音视频）
ffmpeg -y -hide_banner -i "INPUT" -an -c:v copy "OUTPUT"

# 替换为另一段音频
ffmpeg -y -hide_banner -i "VIDEO" -i "AUDIO" -c:v copy -c:a aac -map 0:v -map 1:a "OUTPUT"
```

### 音频编码参数参考

| 格式 | 编解码器 | 质量 | 说明 |
|------|---------|------|------|
| MP3 | libmp3lame -q:a 0-9 | 0最佳/2高/5中 | VBR 模式 |
| AAC | aac -b:a 128k-320k | 192k推荐 | 通用格式 |
| WAV | pcm_s16le | 无损 | 文件较大 |
| FLAC | flac | 无损压缩 | 无损体积小 |
| OGG | libvorbis -q:a 0-10 | 5推荐 | 开源格式 |

---

## 工作流13：视频合并

### 触发条件
- 用户提到"合并""拼接""连起来""concat""merge""join"

### 方法一：流复制快速合并（推荐）

适用于编码参数相同的视频，无需重编码，速度极快：

```bash
# Step 1: 创建文件列表
cat > files.txt << 'EOF'
file 'video1.mp4'
file 'video2.mp4'
file 'video3.mp4'
EOF

# Step 2: 执行合并
ffmpeg -y -hide_banner -f concat -safe 0 -i "files.txt" -c copy "merged.mp4"
```

### 方法二：重编码合并（兼容不同编码）

适用于编码/分辨率不同的视频：

```bash
# Step 1: 创建文件列表
cat > files.txt << 'EOF'
file 'video1.mkv'
file 'video2.avi'
file 'video3.webm'
EOF

# Step 2: 统一编码后合并
ffmpeg -y -hide_banner -f concat -safe 0 -i "files.txt" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k "merged.mp4"
```

### 注意事项
- 确保 concat 文件中的路径使用单引号包裹
- 路径支持相对路径和绝对路径
- 如文件包含特殊字符，建议使用绝对路径
- 合并前可用 `ffprobe` 检查各视频参数是否一致
- `files.txt` 合并完成后可安全删除

### 智能参数归一化

当合并的视频参数不一致时，自动统一为中间参数：

```python
def normalize_for_concat(video_files):
    """分析多个视频并计算统一的编码参数"""
    infos = [analyze_video(f) for f in video_files]

    # 取最大的分辨率
    max_width = max(i['width'] for i in infos)
    max_height = max(i['height'] for i in infos)

    # 取最常见的帧率
    fps_counter = Counter(i['fps'] for i in infos)
    target_fps = fps_counter.most_common(1)[0][0]

    return {
        'width': max_width,
        'height': max_height,
        'fps': target_fps,
        'codec': 'libx264',
        'preset': 'medium',
        'crf': 23
    }
```

---

## 工作流14：宽高比调整

### 触发条件
- 用户提到"宽高比""比例""16:9""9:16""竖屏""横屏""方块""cinema""画幅"

### 常见宽高比

| 比例 | 分辨率 | 典型用途 |
|------|--------|---------|
| 16:9 | 1920×1080 | YouTube、电视、标准横屏 |
| 4:3 | 1440×1080 | 老电视、PPT |
| 1:1 | 1080×1080 | Instagram 方块 |
| 9:16 | 1080×1920 | 抖音、TikTok、竖屏短视频 |
| 21:9 | 2560×1080 | 超宽屏、电影 |

### 带黑边填充

```bash
ffmpeg -y -hide_banner -i "INPUT" -vf "scale=WIDTH:HEIGHT:force_original_aspect_ratio=decrease,pad=WIDTH:HEIGHT:(ow-iw)/2:(oh-ih)/2:black" -c:a copy "OUTPUT"
```

### 无黑边裁剪

```bash
# 裁剪为 9:16 竖屏（居中裁剪）
ffmpeg -y -hide_banner -i "INPUT" -vf "crop=ih*9/16:ih" -c:a copy "OUTPUT"
```

### 示例

```bash
# 转为 9:16 竖屏（带黑边，适合抖音）
ffmpeg -y -hide_banner -i "video.mp4" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:a copy "video_vertical.mp4"

# 转为 1:1 方块（带黑边，适合 Instagram）
ffmpeg -y -hide_banner -i "video.mp4" -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black" -c:a copy "video_square.mp4"

# 转为 16:9 横屏（带黑边，适合 YouTube）
ffmpeg -y -hide_banner -i "video.mp4" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" -c:a copy "video_16x9.mp4"
```

---

## 附录：批量处理

### 错误重试处理器

```python
from enum import Enum
import time

class RetryStrategy(Enum):
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    FIXED_DELAY = "fixed_delay"
    IMMEDIATE = "immediate"

class RetryHandler:
    def __init__(self, max_retries=3, strategy=RetryStrategy.EXPONENTIAL_BACKOFF):
        self.max_retries = max_retries
        self.strategy = strategy

    def execute_with_retry(self, func, *args, **kwargs):
        """带重试执行函数"""
        last_error = None
        total_wait_time = 0

        for attempt in range(self.max_retries + 1):
            try:
                result = func(*args, **kwargs)
                return RetryResult(
                    success=True,
                    result=result,
                    attempts=attempt + 1,
                    total_wait_time=total_wait_time
                )
            except Exception as e:
                last_error = e

                if attempt < self.max_retries:
                    wait_time = self._get_wait_time(attempt)
                    total_wait_time += wait_time
                    time.sleep(wait_time)

        return RetryResult(
            success=False,
            error=str(last_error),
            attempts=self.max_retries + 1,
            total_wait_time=total_wait_time
        )

    def _get_wait_time(self, attempt):
        """计算等待时间"""
        if self.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            return [0, 5, 15][attempt]
        elif self.strategy == RetryStrategy.FIXED_DELAY:
            return 5
        else:  # IMMEDIATE
            return 0
```

### 智能跳过处理器

```python
class SmartSkipper:
    def __init__(self, use_hash=False, validate_output=True, check_duration=True):
        self.use_hash = use_hash
        self.validate_output = validate_output
        self.check_duration = check_duration

    def should_skip(self, input_file, output_file):
        """判断是否应该跳过"""

        # 1. 输出文件不存在
        if not os.path.exists(output_file):
            return SkipDecision(False, "输出文件不存在")

        # 2. 输入文件比输出文件新
        input_mtime = os.path.getmtime(input_file)
        output_mtime = os.path.getmtime(output_file)

        if input_mtime > output_mtime:
            return SkipDecision(False, "输入文件已更新")

        # 3. 验证输出文件
        if self.validate_output:
            try:
                get_video_info(output_file)
            except:
                return SkipDecision(False, "输出文件损坏")

        # 4. 检查时长
        if self.check_duration:
            input_duration = get_duration(input_file)
            output_duration = get_duration(output_file)

            if abs(input_duration - output_duration) > 1:
                return SkipDecision(False, "时长不匹配")

        # 所有检查通过，跳过
        return SkipDecision(True, "文件未修改，跳过处理")
```

### 优化的批量处理器

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Dict, Any

class OptimizedBatchProcessor:
    def __init__(
        self,
        max_workers=None,
        enable_retry=True,
        enable_smart_skip=True,
        enable_report=True
    ):
        self.max_workers = max_workers or os.cpu_count() - 1
        self.enable_retry = enable_retry
        self.enable_smart_skip = enable_smart_skip
        self.enable_report = enable_report

        self.retry_handler = RetryHandler() if enable_retry else None
        self.skipper = SmartSkipper() if enable_smart_skip else None
        self.reporter = BatchReportGenerator() if enable_report else None

    def process_batch(
        self,
        files: List[Dict[str, Any]],
        processor_func: Callable,
        skip_strategy=SkipStrategy.SMART,
        batch_title="批量处理",
        batch_description=""
    ):
        """批量处理文件"""

        if self.reporter:
            self.reporter.start_batch(batch_title, batch_description)

        results = []
        success_count = 0
        failed_count = 0
        skipped_count = 0

        # 使用线程池并行处理
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}

            for file_info in files:
                input_file = file_info['input']
                output_file = file_info['output']

                # 检查是否跳过
                if self.skipper and skip_strategy != SkipStrategy.NONE:
                    if skip_strategy == SkipStrategy.FORCE:
                        decision = SkipDecision(True, "强制跳过")
                    else:
                        decision = self.skipper.should_skip(input_file, output_file)

                    if decision.should_skip:
                        skipped_count += 1
                        results.append(ProcessResult(
                            input_file=input_file,
                            output_file=output_file,
                            success=True,
                            status='skipped',
                            duration=0,
                            file_size_mb=0,
                            retries=0,
                            reason=decision.reason
                        ))
                        continue

                # 提交处理任务
                future = executor.submit(self._process_single, processor_func, file_info)
                futures[future] = file_info

            # 收集结果
            for future in as_completed(futures):
                file_info = futures[future]

                try:
                    result = future.result()
                    results.append(result)

                    if result.status == 'completed':
                        success_count += 1
                    elif result.status == 'failed':
                        failed_count += 1
                    elif result.status == 'skipped':
                        skipped_count += 1

                except Exception as e:
                    failed_count += 1
                    results.append(ProcessResult(
                        input_file=file_info['input'],
                        output_file=file_info['output'],
                        success=False,
                        status='failed',
                        duration=0,
                        file_size_mb=0,
                        retries=0,
                        reason=str(e)
                    ))

        # 生成报告
        stats = BatchStats(
            total=len(files),
            success=success_count,
            failed=failed_count,
            skipped=skipped_count
        )

        if self.reporter:
            for result in results:
                self.reporter.add_result(result)

            self.reporter.finish_batch()

        return stats

    def _process_single(self, processor_func, file_info):
        """处理单个文件（带重试）"""

        if self.retry_handler:
            retry_result = self.retry_handler.execute_with_retry(
                processor_func,
                **file_info
            )

            if retry_result.success:
                return ProcessResult(
                    input_file=file_info['input'],
                    output_file=file_info['output'],
                    success=True,
                    status='completed',
                    duration=0,
                    file_size_mb=0,
                    retries=retry_result.attempts - 1
                )
            else:
                return ProcessResult(
                    input_file=file_info['input'],
                    output_file=file_info['output'],
                    success=False,
                    status='failed',
                    duration=0,
                    file_size_mb=0,
                    retries=retry_result.attempts - 1,
                    reason=retry_result.error
                )
        else:
            # 不使用重试
            processor_func(**file_info)
            return ProcessResult(
                input_file=file_info['input'],
                output_file=file_info['output'],
                success=True,
                status='completed',
                duration=0,
                file_size_mb=0,
                retries=0
            )
```

---

## 附录：实时进度反馈

### 进度跟踪器

```python
import re
import time
from dataclasses import dataclass

@dataclass
class ProgressUpdate:
    pass_number: int
    percentage: float
    current_time: float
    elapsed: float
    speed: float
    remaining_seconds: float
    status: str = ""

class ProgressTracker:
    def __init__(self):
        self.duration = 0
        self.start_time = None
        self.current_percentage = 0

    def start_tracking(self, duration_seconds):
        """开始跟踪进度"""
        self.duration = duration_seconds
        self.start_time = time.time()
        self.current_percentage = 0

    def update(self, ffmpeg_output):
        """解析 FFmpeg 输出并更新进度"""

        # 解析 frame=123 fps=25 time=00:30:00.50 bitrate=1234.5kbits/s
        match = re.search(r'time=(\d+):(\d+):(\d+)\.(\d+)', ffmpeg_output)

        if not match:
            return None

        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        centiseconds = int(match.group(4))

        current_time = hours * 3600 + minutes * 60 + seconds + centiseconds / 100

        # 计算进度百分比
        percentage = (current_time / self.duration) * 100
        self.current_percentage = percentage

        # 计算已用时间
        elapsed = time.time() - self.start_time

        # 计算处理速度
        speed = current_time / elapsed if elapsed > 0 else 0

        # 预计剩余时间
        remaining_seconds = (self.duration - current_time) / speed if speed > 0 else 0

        return ProgressUpdate(
            pass_number=1,
            percentage=percentage,
            current_time=current_time,
            elapsed=elapsed,
            speed=speed,
            remaining_seconds=remaining_seconds
        )

    def get_progress(self):
        """获取当前进度百分比"""
        return self.current_percentage
```

### 简洁进度显示

```python
class SimpleProgressDisplay:
    def __init__(self):
        self.current_line = ""

    def update(self, progress: ProgressUpdate):
        """更新进度显示"""

        line = (
            f"处理中 | "
            f"[{'=' * int(progress.percentage / 5):.<20}] "
            f"{progress.percentage:.1f}% | "
            f"预计 {int(progress.remaining_seconds / 60)}分{int(progress.remaining_seconds % 60)}秒"
        )

        # 使用 \r 覆盖当前行
        print(f'\r{line}', end='', flush=True)
        self.current_line = line

    def finish(self):
        """完成进度显示"""
        print()  # 换行
```

### 批量处理进度显示

```python
class BatchProgressDisplay:
    def __init__(self, total_files):
        self.total_files = total_files
        self.completed = 0

    def update(self, file_index, progress: ProgressUpdate):
        """更新批量处理进度"""

        line = (
            f"处理 {file_index + 1}/{self.total_files} | "
            f"[{'=' * int(progress.percentage / 5):.<20}] "
            f"{progress.percentage:.1f}% | "
            f"预计 {int(progress.remaining_seconds / 60)}分{int(progress.remaining_seconds % 60)}秒"
        )

        print(f'\r{line}', end='', flush=True)

    def finish_file(self):
        """完成单个文件"""
        self.completed += 1

    def finish_batch(self, total_time, success_count):
        """完成批量处理"""
        avg_time = total_time / self.total_files

        print(f"\n{'='*60}")
        print("批量处理完成")
        print(f"{'='*60}")
        print(f"  总计:     {self.total_files} 个文件")
        print(f"  成功:     {success_count} 个")
        print(f"  总耗时:   {int(total_time / 60)}分{int(total_time % 60)}秒")
        print(f"  平均:     {avg_time:.1f}秒/文件")
        print(f"{'='*60}")
```

---

本文档持续更新中。如有疑问，请参考 [API 参考手册](api_reference.md)、[最佳实践](best_practices.md) 或 [故障排除](troubleshooting.md)。
