"""
FFmpeg 命令构建器
根据参数生成完整的 FFmpeg 命令
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class FFmpegCommand:
    """FFmpeg 命令数据类"""

    input_files: List[str] = field(default_factory=list)
    output_file: str = ""
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    video_bitrate: Optional[str] = None
    audio_bitrate: Optional[str] = "128k"
    crf: Optional[int] = None
    preset: str = "medium"
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    filters: List[str] = field(default_factory=list)
    subtitle_file: Optional[str] = None
    subtitle_burn: bool = False
    start_time: Optional[str] = None
    duration: Optional[str] = None
    hardware_accel: bool = False
    audio_sample_rate: Optional[int] = None
    audio_channels: Optional[int] = None
    extra_args: List[str] = field(default_factory=list)
    copy_streams: bool = False  # 流拷贝模式
    two_pass: bool = False  # 两遍编码模式
    pass_number: int = 1  # 编码遍数（1 或 2）
    enable_sync_fix: bool = False  # 启用音视频同步修复
    trim_strategy: Optional[Dict] = None  # 剪辑策略（由 KeyFrameAnalyzer 生成）


class FFmpegBuilder:
    """FFmpeg 命令构建器"""

    def __init__(self):
        """初始化构建器"""
        self.presets = {
            "ultrafast": {"speed": "fastest", "compression": "lowest"},
            "superfast": {"speed": "faster", "compression": "lower"},
            "veryfast": {"speed": "fast", "compression": "low"},
            "faster": {"speed": "medium-fast", "compression": "medium-low"},
            "fast": {"speed": "medium", "compression": "medium"},
            "medium": {"speed": "medium-slow", "compression": "good"},
            "slow": {"speed": "slow", "compression": "better"},
            "slower": {"speed": "slower", "compression": "best"},
            "veryslow": {"speed": "slowest", "compression": "bestest"},
        }

        self.codec_profiles = {
            "h264": {"profile": "high", "level": "4.1"},
            "h265": {"profile": "main", "level": "4.1"},
            "hevc": {"profile": "main", "level": "4.1"},
            "av1": {"profile": "main", "level": "5.0"},
        }

    def build(self, command: FFmpegCommand) -> str:
        """
        构建 FFmpeg 命令

        Args:
            command: FFmpeg 命令参数

        Returns:
            完整的 FFmpeg 命令字符串
        """
        cmd_parts = ["ffmpeg"]

        # 添加输入文件
        for input_file in command.input_files:
            cmd_parts.extend(["-i", input_file])

        # 添加字幕文件（如果需要）
        if command.subtitle_file:
            cmd_parts.extend(["-i", command.subtitle_file])

        # 处理时间范围
        if command.start_time:
            # 如果有剪辑策略且指定了调整后的起始时间，使用调整后的时间
            if command.trim_strategy and command.trim_strategy.get("adjusted_start_time"):
                adjusted_start = command.trim_strategy["adjusted_start_time"]
                cmd_parts.extend(["-ss", f"{adjusted_start:.2f}"])
            else:
                cmd_parts.extend(["-ss", command.start_time])
        if command.duration:
            cmd_parts.extend(["-t", command.duration])

        # 音视频同步修复参数（必须在 -ss 之后）
        if command.enable_sync_fix:
            cmd_parts.extend(["-avoid_negative_ts", "make_zero"])
            cmd_parts.extend(["-fflags", "+genpts"])

        # 视频编码参数
        if not command.copy_streams:
            cmd_parts.extend(self._build_video_params(command))

        # 音频编码参数
        if not command.copy_streams:
            cmd_parts.extend(self._build_audio_params(command))

        # 滤镜
        if command.filters:
            filter_str = self._build_filter_complex(command.filters, command.subtitle_burn)
            cmd_parts.extend(
                ["-vf", filter_str]
                if not command.subtitle_burn
                else ["-filter_complex", filter_str]
            )

        # 流拷贝模式
        if command.copy_streams:
            cmd_parts.append("-c copy")

        # 两遍编码参数
        if command.two_pass:
            cmd_parts.extend(["-pass", str(command.pass_number)])
            if command.pass_number == 2:
                # 添加 passlogfile（仅在第二遍）
                import tempfile

                cmd_parts.extend(["-passlogfile", tempfile.gettempdir() + "/ffmpeg2pass"])

        # 额外参数
        cmd_parts.extend(command.extra_args)

        # 输出文件
        # 第一遍编码输出到 null
        if command.two_pass and command.pass_number == 1:
            import os

            cmd_parts.extend(["-an", "-f", "null"])
            if os.name == "nt":  # Windows
                cmd_parts.append("NUL")
            else:  # Unix
                cmd_parts.append("/dev/null")
        else:
            cmd_parts.append(command.output_file)

        # 构建命令字符串
        return " ".join(cmd_parts)

    def _build_video_params(self, command: FFmpegCommand) -> List[str]:
        """构建视频编码参数"""
        params = []

        # 视频编解码器
        if command.video_codec:
            params.extend(["-c:v", command.video_codec])

        # 硬件加速特定参数
        if command.hardware_accel:
            if "nvenc" in command.video_codec:
                params.extend(["-rc", "vbr", "-cq", "23", "-qmin", "18", "-qmax", "28"])
            elif "amf" in command.video_codec:
                params.extend(["-quality", "speed"])
            elif "qsv" in command.video_codec:
                params.extend(["-global_quality", "23"])

        # CRF 模式（两遍编码时不使用 CRF）
        if command.crf is not None and not command.two_pass:
            params.extend(["-crf", str(command.crf)])

        # 码率模式
        if command.video_bitrate:
            params.extend(["-b:v", command.video_bitrate])

            # 添加码率控制参数（仅在非硬件加速或两遍编码时）
            if not command.hardware_accel or command.two_pass:
                # 提取数值部分
                bitrate_value = (
                    float(command.video_bitrate[:-1])
                    if command.video_bitrate[-1].isalpha()
                    else float(command.video_bitrate)
                )
                bitrate_unit = (
                    command.video_bitrate[-1] if command.video_bitrate[-1].isalpha() else "k"
                )

                params.extend(["-maxrate", f"{int(bitrate_value * 1.2)}{bitrate_unit}"])
                params.extend(["-bufsize", f"{int(bitrate_value * 2)}{bitrate_unit}"])

        # 预设
        if command.preset:
            params.extend(["-preset", command.preset])

        # 分辨率
        if command.width and command.height:
            params.extend(["-s", f"{command.width}x{command.height}"])

        # 帧率
        if command.fps:
            params.extend(["-r", str(command.fps)])

        # 编码配置文件
        codec_name = (
            command.video_codec.replace("lib", "")
            .replace("_nvenc", "")
            .replace("_amf", "")
            .replace("_qsv", "")
        )
        if codec_name in self.codec_profiles:
            profile_info = self.codec_profiles[codec_name]
            params.extend(["-profile:v", profile_info["profile"]])
            params.extend(["-level", profile_info["level"]])

        # 像素格式
        params.extend(["-pix_fmt", "yuv420p"])

        return params

    def _build_audio_params(self, command: FFmpegCommand) -> List[str]:
        """构建音频编码参数"""
        params = []

        if command.audio_codec:
            params.extend(["-c:a", command.audio_codec])

        if command.audio_bitrate:
            params.extend(["-b:a", command.audio_bitrate])

        if command.audio_sample_rate:
            params.extend(["-ar", str(command.audio_sample_rate)])

        if command.audio_channels:
            params.extend(["-ac", str(command.audio_channels)])

        return params

    def _build_filter_complex(self, filters: List[str], subtitle_burn: bool) -> str:
        """构建滤镜链"""
        if not filters:
            return ""

        # FFmpeg 滤镜语法：滤镜之间用逗号分隔
        filter_str = ",".join(filters)

        # 如果需要烧录字幕
        if subtitle_burn:
            # 假设最后一个输入是字幕文件
            filter_str = f"[0:v]{filter_str}[v];[v][1:s]overlay"

        return filter_str

    def build_crop_filter(self, width: int, height: int, x: int = 0, y: int = 0) -> str:
        """构建裁剪滤镜"""
        return f"crop={width}:{height}:{x}:{y}"

    def build_scale_filter(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect: bool = True,
    ) -> str:
        """构建缩放滤镜"""
        if width and height:
            if maintain_aspect:
                return f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
            else:
                return f"scale={width}:{height}"
        elif width:
            return f"scale={width}:-1"
        elif height:
            return f"scale=-1:{height}"
        else:
            return "scale=iw/2:ih/2"

    def build_overlay_filter(self, x: str = "0", y: str = "0", input_index: int = 1) -> str:
        """构建叠加滤镜（水印）"""
        return f"[0:v][{input_index}:v]overlay={x}:{y}:format=auto,format=yuv420p"

    def build_rotate_filter(self, angle: float) -> str:
        """构建旋转滤镜"""
        # angle 单位是弧度
        rad = angle * 3.14159 / 180
        return f"rotate={rad}:transpose=clock"

    def build_brightness_filter(self, value: float) -> str:
        """构建亮度滤镜"""
        return f"eq=brightness={value}"

    def build_contrast_filter(self, value: float) -> str:
        """构建对比度滤镜"""
        return f"eq=contrast={value}"

    def build_saturation_filter(self, value: float) -> str:
        """构建饱和度滤镜"""
        return f"eq=saturation={value}"

    def build_grayscale_filter(self) -> str:
        """构建灰度滤镜"""
        return "format=gray"

    def build_fade_filter(
        self, in_duration: float = 1.0, out_duration: float = 1.0, total_duration: float = 0
    ) -> str:
        """构建淡入淡出滤镜"""
        filters = []
        if in_duration > 0:
            filters.append(f"fade=t=in:st=0:d={in_duration}")
        if out_duration > 0 and total_duration > 0:
            filters.append(f"fade=t=out:st={total_duration - out_duration}:d={out_duration}")
        return ",".join(filters)

    def build_speed_filter(self, speed_factor: float) -> str:
        """构建变速滤镜"""
        # 使用 setpts 滤镜实现视频变速
        return f"setpts={1.0/speed_factor}*PTS"

    def build_volume_filter(self, volume_factor: float) -> str:
        """构建音量滤镜"""
        # volume_factor = 1.0 表示原音量
        return f"volume={volume_factor}"

    def build_trim_filter(self, start: str, end: str, setpts: bool = True) -> str:
        """构建修剪滤镜"""
        if setpts:
            return f"trim=start={start}:end={end},setpts=PTS-STARTPTS"
        else:
            return f"trim=start={start}:end={end}"

    def build_concat_filter(self, num_inputs: int) -> str:
        """构建拼接滤镜"""
        # 生成输入映射
        inputs = []
        for i in range(num_inputs):
            inputs.extend([f"[{i}:v][{i}:a]"])
        input_str = "".join(inputs)

        return f"{input_str}concat=n={num_inputs}:v=1:a=1[outv][outa]"

    def build_watermark_filter(
        self, position: str = "bottom-right", margin_x: int = 10, margin_y: int = 10
    ) -> str:
        """
        构建水印滤镜（智能位置）

        Args:
            position: 水印位置 (top-left, top-right, bottom-left, bottom-right, center)
            margin_x: X 边距
            margin_y: Y 边距
        """
        position_map = {
            "top-left": f"{margin_x}:{margin_y}",
            "top-right": "W-w-{margin_x}:{margin_y}",
            "bottom-left": f"{margin_x}:H-h-{margin_y}",
            "bottom-right": "W-w-{margin_x}:H-h-{margin_y}",
            "center": "(W-w)/2:(H-h)/2",
        }

        coords = position_map.get(position, position_map["bottom-right"])
        return f"[0:v][1:v]overlay={coords}:format=auto,format=yuv420p"

    def build_subtitle_burn_filter(self, force_style: Optional[str] = None) -> str:
        """
        构建字幕烧录滤镜

        Args:
            force_style: 强制样式，例如 "FontSize=24,PrimaryColour=&Hffffff&"
        """
        if force_style:
            return f"subtitles='{force_style}'"
        else:
            return "subtitles"

    def build_complex_filter(self, filter_graph: List[Tuple[str, List[str]]]) -> str:
        """
        构建复杂滤镜图

        Args:
            filter_graph: 滤镜图，格式为 [(input1, input2, ...), (filter_name, params), (output1, output2, ...)]

        Returns:
            滤镜字符串
        """
        # 这是一个高级功能，允许构建复杂的滤镜图
        # 暂时返回简单滤镜的串联
        filters = []
        for item in filter_graph:
            if isinstance(item, str):
                filters.append(item)
        return ",".join(filters)

    def should_enable_sync_fix(
        self,
        start_time: Optional[float] = None,
        video_duration: Optional[float] = None,
        copy_mode: bool = False
    ) -> Tuple[bool, str]:
        """
        判断是否需要启用音视频同步修复

        Args:
            start_time: 起始时间（秒）
            video_duration: 视频总时长（秒）
            copy_mode: 是否使用流拷贝模式

        Returns:
            (是否需要修复, 原因说明)
        """
        if not start_time:
            return False, "未进行剪辑操作"

        # 从开头剪辑（< 1秒）
        if start_time <= 1.0:
            return False, "从视频开头剪辑，不会出现同步问题"

        # 从中间剪辑
        if start_time < (video_duration or 0) - 10.0:
            if copy_mode:
                return True, "从中间剪辑 + 流拷贝模式，强烈建议启用同步修复"
            else:
                return True, "从中间剪辑，建议启用同步修复以防时间戳问题"

        # 从结尾剪辑
        if copy_mode:
            return True, "从结尾剪辑 + 流拷贝模式，可能产生负时间戳"
        else:
            return True, "从结尾剪辑，可能产生负时间戳"

        return False, "未检测到需要同步修复的情况"

    def build_smart_trim_params(
        self,
        start_time: float,
        duration: float,
        video_path: str,
        prefer_mode: str = "auto"
    ) -> Dict:
        """
        根据关键帧分析生成智能剪辑参数

        Args:
            start_time: 起始时间（秒）
            duration: 持续时间（秒）
            video_path: 视频文件路径
            prefer_mode: 偏好模式 ("auto", "fast", "precise")

        Returns:
            剪辑策略字典
        """
        try:
            # 动态导入 KeyFrameAnalyzer
            from ..analyzers.keyframe_analyzer import KeyFrameAnalyzer
        except ImportError:
            try:
                from analyzers.keyframe_analyzer import KeyFrameAnalyzer
            except ImportError:
                # 如果无法导入，返回基础策略
                return {
                    "mode": "precise",
                    "reason": "关键帧分析器不可用，使用默认精确模式",
                    "adjusted_start_time": start_time,
                    "adjusted_end_time": start_time + duration,
                    "recommended_params": {
                        "codec": "libx264",
                        "preset": "medium",
                        "crf": 23,
                        "audio_codec": "aac"
                    }
                }

        analyzer = KeyFrameAnalyzer()
        strategy = analyzer.suggest_trim_strategy(
            start_time=start_time,
            duration=duration,
            video_path=video_path,
            prefer_mode=prefer_mode
        )

        return {
            "mode": strategy.mode,
            "reason": strategy.reason,
            "adjusted_start_time": strategy.adjusted_start_time,
            "adjusted_end_time": strategy.adjusted_end_time,
            "distance_to_nearest_keyframe": strategy.distance_to_nearest_keyframe,
            "recommended_params": strategy.recommended_params
        }

    def apply_sync_fix_params(self, command: FFmpegCommand) -> FFmpegCommand:
        """
        应用音视频同步修复参数到命令对象

        Args:
            command: FFmpeg 命令对象

        Returns:
            修改后的命令对象
        """
        command.enable_sync_fix = True
        return command


# 使用示例
if __name__ == "__main__":
    builder = FFmpegBuilder()

    print("=== FFmpeg 命令构建器测试 ===\n")

    # 示例 1：基本转码
    print("示例 1：基本转码")
    cmd1 = builder.build(
        FFmpegCommand(
            input_files=["input.mp4"],
            output_file="output.mp4",
            video_codec="libx264",
            audio_codec="aac",
            crf=23,
            preset="medium",
        )
    )
    print(cmd1)
    print()

    # 示例 2：调整分辨率
    print("示例 2：调整分辨率到 720p")
    cmd2 = builder.build(
        FFmpegCommand(
            input_files=["input.mp4"],
            output_file="output_720p.mp4",
            video_codec="libx264",
            width=1280,
            height=720,
            preset="fast",
        )
    )
    print(cmd2)
    print()

    # 示例 3：添加水印
    print("示例 3：添加水印")
    cmd3 = builder.build(
        FFmpegCommand(
            input_files=["input.mp4", "watermark.png"],
            output_file="output_watermarked.mp4",
            video_codec="libx264",
            filters=[builder.build_watermark_filter("bottom-right", 10, 10)],
        )
    )
    print(cmd3)
    print()

    # 示例 4：剪辑片段
    print("示例 4：剪辑片段（从 00:01:00 到 00:02:00）")
    cmd4 = builder.build(
        FFmpegCommand(
            input_files=["input.mp4"],
            output_file="output_clip.mp4",
            start_time="00:01:00",
            duration="00:01:00",
            copy_streams=True,
        )
    )
    print(cmd4)
    print()

    # 示例 5：调整亮度和对比度
    print("示例 5：调整亮度和对比度")
    cmd5 = builder.build(
        FFmpegCommand(
            input_files=["input.mp4"],
            output_file="output_adjusted.mp4",
            video_codec="libx264",
            filters=[builder.build_brightness_filter(0.2), builder.build_contrast_filter(1.1)],
        )
    )
    print(cmd5)
    print()

    # 示例 6：灰度 + 旋转
    print("示例 6：灰度 + 旋转 90 度")
    cmd6 = builder.build(
        FFmpegCommand(
            input_files=["input.mp4"],
            output_file="output_effect.mp4",
            video_codec="libx264",
            filters=[builder.build_grayscale_filter(), builder.build_rotate_filter(90)],
        )
    )
    print(cmd6)
