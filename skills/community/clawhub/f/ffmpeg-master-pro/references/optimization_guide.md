# FFmpeg Master - 优化算法详解

本文档详细说明 FFmpeg Master 技能中的各种优化算法和智能决策系统。

## 目录

- [内容类型识别算法](#内容类型识别算法)
- [智能码率计算](#智能码率计算)
- [GPU 加速检测](#gpu-加速检测)
- [质量验证系统](#质量验证系统)
- [性能优化策略](#性能优化策略)

---

## 内容类型识别算法

### 算法原理

技能使用多维度特征分析来自动识别视频内容类型，包括：

1. **运动幅度分析**
   - 使用 FFmpeg 的 `select` 过滤器检测帧间差异
   - 计算平均运动向量幅度
   - 识别快速运动场景（体育、动作片）

2. **场景复杂度分析**
   - 检测场景切换频率（使用 `scene` 滤镜）
   - 分析画面细节程度（边缘检测）
   - 评估色彩分布和对比度

3. **时间特征分析**
   - 检测帧率稳定性
   - 分析画面节奏和剪辑频率
   - 识别重复模式（动画、屏幕录制）

4. **元数据启发式**
   - 分析分辨率比例（16:9, 9:16 等）
   - 检查编码历史（是否二次编码）
   - 评估音频特征（音乐、对话、静音）

### 内容类型判定

基于上述特征，技能将视频分类为以下类型：

| 内容类型 | 特征模式 | 编码策略 |
|---------|---------|---------|
| **电影/电视剧** | 高场景复杂度、中等运动、自然节奏 | slow + CRF 23 + VBR |
| **动画/动漫** | 低场景复杂度、画面平滑、高对比度 | medium + CRF 20 + VBR |
| **屏幕录制** | 极低运动、静态画面、文字为主 | veryfast + CRF 18 + CBR |
| **体育/运动** | 极高运动、快速节奏、场景切换少 | fast + CRF 22 + VBR |
| **音乐视频** | 高频剪辑、节奏感强、视觉特效 | medium + CRF 21 + VBR |
| **老旧视频** | 低分辨率、噪声多、质量差 | slow + CRF 24 + 去噪滤镜 |

### 优化参数映射

每种内容类型都有对应的优化参数组合：

```python
CONTENT_TYPE_PARAMS = {
    "movie": {
        "codec": "libx264",
        "preset": "slow",
        "crf": 23,
        "tune": "film",
        "bitrate_mode": "VBR",
        "profile": "high",
        "level": "4.1"
    },
    "anime": {
        "codec": "libx264",
        "preset": "medium",
        "crf": 20,
        "tune": "animation",
        "bitrate_mode": "VBR",
        "profile": "high",
        "level": "4.1"
    },
    "screencast": {
        "codec": "libx264",
        "preset": "veryfast",
        "crf": 18,
        "tune": "zerolatency",
        "bitrate_mode": "CBR",
        "profile": "high",
        "level": "4.1"
    },
    "sports": {
        "codec": "libx264",
        "preset": "fast",
        "crf": 22,
        "tune": "fastdecode",
        "bitrate_mode": "VBR",
        "profile": "high",
        "level": "4.2"
    },
    "music_video": {
        "codec": "libx264",
        "preset": "medium",
        "crf": 21,
        "tune": "film",
        "bitrate_mode": "VBR",
        "profile": "high",
        "level": "4.1"
    },
    "legacy": {
        "codec": "libx264",
        "preset": "slow",
        "crf": 24,
        "tune": "film",
        "bitrate_mode": "VBR",
        "filters": ["hqdn3d=4:3:6:4.5"],  # 去噪滤镜
        "profile": "high",
        "level": "4.0"
    }
}
```

---

## 智能码率计算

### 三模型融合算法

技能使用三种模型来计算最优目标码率：

#### 1. 分辨率模型

基于视频分辨率和帧率估算基础码率：

```python
def calculate_bitrate_by_resolution(width, height, fps):
    """基于分辨率计算推荐码率"""
    pixels = width * height
    frames_per_second = fps

    # 基础码率（Mbps）
    if pixels <= 640 * 480:  # SD
        base_bitrate = 1.5
    elif pixels <= 1280 * 720:  # 720p
        base_bitrate = 3.0
    elif pixels <= 1920 * 1080:  # 1080p
        base_bitrate = 5.0
    elif pixels <= 2560 * 1440:  # 1440p
        base_bitrate = 9.0
    else:  # 4K and above
        base_bitrate = 20.0

    # 帧率调整因子
    fps_factor = frames_per_second / 30.0

    return base_bitrate * fps_factor
```

#### 2. 复杂度模型

基于内容类型和运动幅度调整码率：

```python
def calculate_bitrate_by_complexity(content_type, motion_score):
    """基于内容复杂度计算码率调整因子"""
    complexity_factors = {
        "screencast": 0.6,    # 静态画面，低码率
        "anime": 0.8,         # 动画细节少
        "movie": 1.0,         # 标准
        "music_video": 1.1,   # 音乐视频稍高
        "sports": 1.3,        # 运动画面需要高码率
        "legacy": 0.9         # 老旧视频
    }

    base_factor = complexity_factors.get(content_type, 1.0)

    # 运动幅度调整（0-1 范围）
    motion_adjustment = 1.0 + (motion_score * 0.3)

    return base_factor * motion_adjustment
```

#### 3. 目标大小模型

基于目标文件大小计算精确码率：

```python
def calculate_bitrate_by_target_size(target_size_mb, duration_seconds, audio_bitrate_kbps):
    """基于目标文件大小计算所需视频码率"""
    # 总比特数 = 目标大小 * 8 * 1024 (KB)
    total_bits = target_size_mb * 8 * 1024

    # 音频比特数
    audio_bits = audio_bitrate_kbps * duration_seconds

    # 视频可用比特数
    video_bits = total_bits - audio_bits

    # 视频码率 (Kbps → Mbps)
    video_bitrate_kbps = video_bits / duration_seconds

    return video_bitrate_kbps / 1024  # 转换为 Mbps
```

#### 融合策略

```python
def calculate_optimal_bitrate(target_size_mb, duration, video_info, content_type):
    """融合三种模型计算最优码率"""
    # 模型 1：分辨率模型
    bitrate_res = calculate_bitrate_by_resolution(
        video_info['width'],
        video_info['height'],
        video_info['fps']
    )

    # 模型 2：复杂度模型
    complexity_factor = calculate_bitrate_by_complexity(
        content_type,
        video_info['motion_score']
    )
    bitrate_complexity = bitrate_res * complexity_factor

    # 模型 3：目标大小模型
    bitrate_target = calculate_bitrate_by_target_size(
        target_size_mb,
        duration,
        video_info['audio_bitrate']
    )

    # 融合策略（加权平均）
    # 如果有明确目标大小，优先使用目标大小模型
    if target_size_mb:
        weight_target = 0.7
        weight_res = 0.2
        weight_complexity = 0.1
    else:
        weight_target = 0.0
        weight_res = 0.5
        weight_complexity = 0.5

    optimal_bitrate = (
        bitrate_target * weight_target +
        bitrate_res * weight_res +
        bitrate_complexity * weight_complexity
    )

    return optimal_bitrate
```

---

## GPU 加速检测

### 检测优先级

技能按照以下优先级检测 GPU 加速：

```python
def detect_gpu_acceleration():
    """检测可用的 GPU 加速"""
    detection_order = [
        ("nvidia", check_nvidia_gpu),
        ("amd", check_amd_gpu),
        ("intel", check_intel_qsv),
        ("cpu", lambda: None)  # 回退到 CPU
    ]

    for gpu_type, check_func in detection_order:
        try:
            result = check_func()
            if result:
                return {
                    "type": gpu_type,
                    "encoder": result["encoder"],
                    "available": True
                }
        except Exception:
            continue

    return {"type": "cpu", "encoder": "libx264", "available": False}
```

### NVIDIA GPU 检测

```python
def check_nvidia_gpu():
    """检测 NVIDIA GPU 和 NVENC 支持"""
    try:
        # 检查 nvidia-smi
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,encoder.version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            # 检查 FFmpeg 是否支持 NVENC
            ffmpeg_result = subprocess.run(
                ["ffmpeg", "-encoders"],
                capture_output=True,
                text=True
            )

            if "h264_nvenc" in ffmpeg_result.stdout:
                return {
                    "encoder": "h264_nvenc",
                    "fallback": "libx264"
                }
    except Exception:
        pass

    return None
```

### AMD GPU 检测

```python
def check_amd_gpu():
    """检测 AMD GPU 和 AMF 支持"""
    try:
        # 检查 amdgpu-info
        result = subprocess.run(
            ["amdgpu-info", "--show-gpu-info"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            # 检查 FFmpeg 是否支持 AMF
            ffmpeg_result = subprocess.run(
                ["ffmpeg", "-encoders"],
                capture_output=True,
                text=True
            )

            if "h264_amf" in ffmpeg_result.stdout:
                return {
                    "encoder": "h264_amf",
                    "fallback": "libx264"
                }
    except Exception:
        pass

    return None
```

### Intel QSV 检测

```python
def check_intel_qsv():
    """检测 Intel QSV 支持"""
    try:
        # 检查 FFmpeg 是否支持 QSV
        result = subprocess.run(
            ["ffmpeg", "-encoders"],
            capture_output=True,
            text=True
        )

        if "h264_qsv" in result.stdout:
            return {
                "encoder": "h264_qsv",
                "fallback": "libx264"
            }
    except Exception:
        pass

    return None
```

### GPU 参数优化

不同 GPU 有不同的优化参数：

```python
GPU_OPTIMIZATION_PARAMS = {
    "nvidia": {
        "encoder": "h264_nvenc",
        "preset": "p4",  # 平衡速度和质量
        "profile": "high",
        "level": "4.1",
        "rc": "vbr",  # 可变码率
        "cq": "23",   # 恒定质量
        "extra_args": [
            "-surfaces", "32",  # 提高性能
            "-b_ref", "3"       # B 帧参考
        ]
    },
    "amd": {
        "encoder": "h264_amf",
        "preset": "balanced",
        "profile": "high",
        "level": "4.1",
        "rc": "vbr",
        "cq": "23",
        "extra_args": [
            "-quality", "balanced"
        ]
    },
    "intel": {
        "encoder": "h264_qsv",
        "preset": "medium",
        "profile": "high",
        "level": "4.1",
        "rc": "vbr",
        "extra_args": [
            "-look_ahead", "1",     # 前瞻编码
            "-async_depth", "4"     # 异步深度
        ]
    }
}
```

---

## 质量验证系统

### 基础验证指标

```python
def validate_output_quality(input_file, output_file, target_size_mb=None):
    """验证输出质量"""
    validation_results = {}

    # 1. 文件大小验证
    output_size_mb = os.path.getsize(output_file) / (1024 * 1024)

    if target_size_mb:
        error_pct = abs(output_size_mb - target_size_mb) / target_size_mb
        validation_results['size_error'] = error_pct
        validation_results['size_valid'] = error_pct < 0.05  # 偏差 < 5%

    # 2. 分辨率验证
    input_info = get_video_info(input_file)
    output_info = get_video_info(output_file)

    validation_results['resolution_match'] = (
        input_info['width'] == output_info['width'] and
        input_info['height'] == output_info['height']
    )

    # 3. 时长验证
    duration_diff = abs(input_info['duration'] - output_info['duration'])
    validation_results['duration_valid'] = duration_diff < 0.1  # 差异 < 0.1 秒

    # 4. 码率验证
    validation_results['bitrate_match'] = (
        abs(output_info['video_bitrate'] - target_bitrate) / target_bitrate < 0.1
    )

    # 5. 同步性验证
    validation_results['av_sync'] = check_av_sync(output_file)

    # 6. 完整性验证
    validation_results['playable'] = check_playable(output_file)

    return validation_results
```

### 高级质量指标（可选）

#### VMAF 评分

```python
def calculate_vmaf(input_file, output_file):
    """计算 VMAF 评分（Netflix 视频质量评估）"""
    try:
        cmd = [
            "ffmpeg", "-i", input_file, "-i", output_file,
            "-filter_complex", "[0:v][1:v]libvmaf=log_path=vmaf.log",
            "-f", "null", "-"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # 解析 VMAF 日志
        with open("vmaf.log") as f:
            scores = [float(line.split(',')[1]) for line in f]

        avg_vmaf = sum(scores) / len(scores)

        return {
            "score": avg_vmaf,
            "interpretation": interpret_vmaf(avg_vmaf)
        }
    except Exception:
        return None
```

#### SSIM 指标

```python
def calculate_ssim(input_file, output_file):
    """计算结构相似性指数"""
    try:
        cmd = [
            "ffmpeg", "-i", input_file, "-i", output_file,
            "-filter_complex", "[0:v][1:v]ssim=ssim.log",
            "-f", "null", "-"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # 解析 SSIM 日志
        with open("ssim.log") as f:
            for line in f:
                if "SSIM" in line:
                    ssim_value = float(line.split('=')[-1].strip())
                    return ssim_value

        return None
    except Exception:
        return None
```

#### PSNR 值

```python
def calculate_psnr(input_file, output_file):
    """计算峰值信噪比"""
    try:
        cmd = [
            "ffmpeg", "-i", input_file, "-i", output_file,
            "-filter_complex", "[0:v][1:v]psnr=psnr.log",
            "-f", "null", "-"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # 解析 PSNR 日志
        with open("psnr.log") as f:
            for line in f:
                if "PSNR" in line:
                    psnr_value = float(line.split(':')[-1].strip())
                    return psnr_value

        return None
    except Exception:
        return None
```

---

## 性能优化策略

### 编码预设选择

不同的预设对编码速度和质量有显著影响：

| 预设 | 编码速度 | 压缩效率 | 适用场景 |
|------|---------|---------|---------|
| **ultrafast** | 极快 | 最低 | 实时编码、预览 |
| **superfast** | 很快 | 很低 | 快速转码 |
| **veryfast** | 快 | 低 | 屏幕录制、直播 |
| **faster** | 较快 | 较低 | 快速处理 |
| **fast** | 中等 | 中等 | 日常使用 |
| **medium** | 中等 | 中等 | 推荐默认值 |
| **slow** | 慢 | 高 | 高质量输出 |
| **slower** | 很慢 | 很高 | 存档质量 |
| **veryslow** | 极慢 | 极高 | 最高质量 |

### 并行处理

```python
def optimize_parallel_processing(file_list, max_workers=None):
    """优化并行处理"""
    if not max_workers:
        # 根据 CPU 核心数自动确定
        cpu_count = os.cpu_count()
        max_workers = min(cpu_count - 1, 4)  # 最多 4 个并行

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for file in file_list:
            future = executor.submit(process_video, file)
            futures.append(future)

        results = []
        for future in as_completed(futures):
            try:
                result = future.result(timeout=300)  # 5 分钟超时
                results.append(result)
            except TimeoutException:
                results.append({"error": "timeout"})

    return results
```

### 内存优化

```python
def optimize_memory_usage(input_file, output_file):
    """优化内存使用"""
    # 使用分段处理大文件
    file_size_mb = os.path.getsize(input_file) / (1024 * 1024)

    if file_size_mb > 1000:  # 大于 1GB
        # 使用流式处理
        return process_large_file_streaming(input_file, output_file)
    else:
        # 使用标准处理
        return process_video_standard(input_file, output_file)
```

---

## 总结

FFmpeg Master 技能的优化系统包含：

1. **内容类型识别**：多维度特征分析，自动选择最优编码参数
2. **智能码率计算**：三模型融合，精确控制文件大小
3. **GPU 加速检测**：自动检测并使用可用的硬件加速
4. **质量验证**：基础验证 + 高级质量指标（VMAF/SSIM/PSNR）
5. **性能优化**：编码预设、并行处理、内存优化

这些优化算法确保视频处理既快速又高质量，同时满足不同的使用场景需求。
