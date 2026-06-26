"""
字幕处理器
处理字幕的提取、嵌入、烧录和格式转换
"""

import subprocess
import json
from typing import Dict, List, Optional
from pathlib import Path
from enum import Enum


class SubtitleFormat(Enum):
    """字幕格式枚举"""

    SRT = "srt"
    ASS = "ass"
    SSA = "ssa"
    VTT = "vtt"
    SUB = "sub"
    TXT = "txt"


class SubtitleAction(Enum):
    """字幕操作类型"""

    EXTRACT = "extract"  # 提取
    EMBED = "embed"  # 嵌入（软字幕）
    BURN = "burn"  # 烧录（硬字幕）
    CONVERT = "convert"  # 格式转换
    REMOVE = "remove"  # 移除


class SubtitleProcessor:
    """字幕处理器"""

    def __init__(self):
        """初始化字幕处理器"""
        self.format_codecs = {
            SubtitleFormat.SRT: "srt",
            SubtitleFormat.ASS: "ass",
            SubtitleFormat.SSA: "ssa",
            SubtitleFormat.VTT: "webvtt",
            SubtitleFormat.SUB: "microdvd",
        }

    def scan_subtitles(self, video_path: str) -> List[Dict]:
        """
        扫描视频中的所有字幕流

        Args:
            video_path: 视频文件路径

        Returns:
            字幕流信息列表
        """
        probe_cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-select_streams",
            "s",  # 只选择字幕流
            "-print_format",
            "json",
            "-show_entries",
            "stream=index,codec_name,codec_type,language:stream_tags=language,title",
            video_path,
        ]

        try:
            result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)

            subtitles = []
            for stream in info.get("streams", []):
                subtitles.append(
                    {
                        "index": stream.get("index"),
                        "codec": stream.get("codec_name"),
                        "language": stream.get("tags", {}).get("language", "unknown"),
                        "title": stream.get("tags", {}).get("title", ""),
                    }
                )

            return subtitles

        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            raise Exception(f"扫描字幕失败: {e}")

    def extract_subtitle(
        self,
        video_path: str,
        output_path: str,
        stream_index: Optional[int] = None,
        language: Optional[str] = None,
        output_format: SubtitleFormat = SubtitleFormat.SRT,
    ) -> str:
        """
        提取字幕到独立文件

        Args:
            video_path: 视频文件路径
            output_path: 输出文件路径
            stream_index: 字幕流索引（如果指定，优先使用）
            language: 字幕语言（如果未指定 stream_index）
            output_format: 输出格式

        Returns:
            提取的字幕文件路径
        """
        # 如果未指定流索引，先扫描并查找
        if stream_index is None:
            subtitles = self.scan_subtitles(video_path)
            if language:
                # 查找指定语言的字幕
                for sub in subtitles:
                    if sub["language"] == language:
                        stream_index = sub["index"]
                        break
            elif subtitles:
                # 使用第一个字幕流
                stream_index = subtitles[0]["index"]
            else:
                raise Exception("视频中没有字幕流")

        # 构建输出路径
        output_file = Path(output_path)
        if output_file.suffix.lower()[1:] != output_format.value:
            output_file = output_file.with_suffix(f".{output_format.value}")

        # 构建提取命令
        cmd = [
            "ffmpeg",
            "-i",
            video_path,
            "-map",
            f"0:s:{stream_index}",  # 映射字幕流
            "-c:s",
            self.format_codecs[output_format],
            str(output_file),
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return str(output_file)
        except subprocess.CalledProcessError as e:
            raise Exception(f"提取字幕失败: {e.stderr}")

    def embed_subtitle(
        self,
        video_path: str,
        subtitle_path: str,
        output_path: str,
        language: Optional[str] = None,
        title: Optional[str] = None,
    ) -> str:
        """
        嵌入字幕到视频（软字幕）

        Args:
            video_path: 视频文件路径
            subtitle_path: 字幕文件路径
            output_path: 输出视频路径
            language: 字幕语言代码
            title: 字幕标题

        Returns:
            输出视频路径
        """
        cmd = [
            "ffmpeg",
            "-i",
            video_path,
            "-i",
            subtitle_path,
            "-c",
            "copy",  # 流拷贝，不重新编码
            "-c:s",
            "mov_text",  # 字幕编码
            "-metadata:s:s:0",
            f"language={language if language else 'und'}",
        ]

        if title:
            cmd.extend(["-metadata:s:s:0", f"title={title}"])

        cmd.extend(["-map", "0", "-map", "1"])  # 映射所有流
        cmd.append(output_path)

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise Exception(f"嵌入字幕失败: {e.stderr}")

    def burn_subtitle(
        self,
        video_path: str,
        subtitle_path: Optional[str] = None,
        stream_index: Optional[int] = None,
        output_path: str = "",
        font: Optional[str] = None,
        font_size: int = 24,
        font_color: str = "&HFFFFFF&",  # 白色
        force_style: Optional[str] = None,
    ) -> str:
        """
        烧录字幕到视频（硬字幕）

        Args:
            video_path: 视频文件路径
            subtitle_path: 外挂字幕文件路径（如果使用外挂字幕）
            stream_index: 视频内字幕流索引（如果使用内嵌字幕）
            output_path: 输出视频路径
            font: 字体名称
            font_size: 字体大小
            font_color: 字体颜色（ASS 格式）
            force_style: 强制样式字符串

        Returns:
            输出视频路径
        """
        if not output_path:
            output_path = str(Path(video_path).with_stem(f"{Path(video_path).stem}_burned"))

        # 构建强制样式
        if force_style is None:
            force_style = f"FontSize={font_size},PrimaryColour={font_color}"

        # 构建字幕滤镜
        if subtitle_path:
            # 外挂字幕
            subtitle_filter = f"subtitles='{subtitle_path}':force_style='{force_style}'"
        else:
            # 内嵌字幕（需要更复杂的处理）
            if stream_index is None:
                # 使用第一个字幕流
                subtitles = self.scan_subtitles(video_path)
                if not subtitles:
                    raise Exception("视频中没有字幕流")
                stream_index = subtitles[0]["index"]

            # 对于内嵌字幕，需要提取后再烧录
            import tempfile

            with tempfile.NamedTemporaryFile(suffix=".srt", delete=False) as tmp:
                tmp_subtitle = tmp.name

            self.extract_subtitle(video_path, tmp_subtitle, stream_index=stream_index)
            subtitle_filter = f"subtitles='{tmp_subtitle}':force_style='{force_style}'"

        # 构建烧录命令
        cmd = [
            "ffmpeg",
            "-i",
            video_path,
            "-vf",
            subtitle_filter,
            "-c:a",
            "copy",  # 音频直接拷贝
            output_path,
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise Exception(f"烧录字幕失败: {e.stderr}")

    def convert_subtitle(
        self, input_path: str, output_path: str, output_format: SubtitleFormat
    ) -> str:
        """
        转换字幕格式

        Args:
            input_path: 输入字幕文件路径
            output_path: 输出字幕文件路径
            output_format: 输出格式

        Returns:
            输出字幕文件路径
        """
        output_file = Path(output_path)
        if output_file.suffix.lower()[1:] != output_format.value:
            output_file = output_file.with_suffix(f".{output_format.value}")

        cmd = ["ffmpeg", "-i", input_path, str(output_file)]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return str(output_file)
        except subprocess.CalledProcessError as e:
            raise Exception(f"转换字幕格式失败: {e.stderr}")

    def remove_subtitle(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        stream_indices: Optional[List[int]] = None,
    ) -> str:
        """
        移除视频中的字幕

        Args:
            video_path: 视频文件路径
            output_path: 输出视频路径
            stream_indices: 要移除的字幕流索引列表

        Returns:
            输出视频路径
        """
        if output_path is None:
            output_path = str(Path(video_path).with_stem(f"{Path(video_path).stem}_no_sub"))

        # 构建命令
        cmd = ["ffmpeg", "-i", video_path]

        # 映射除字幕外的所有流
        cmd.extend(["-map", "0:v"])  # 视频
        cmd.extend(["-map", "0:a"])  # 音频
        # 不映射字幕流

        cmd.extend(["-c", "copy", output_path])

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise Exception(f"移除字幕失败: {e.stderr}")

    def process_multiple_subtitles(self, video_path: str, actions: List[Dict]) -> List[str]:
        """
        批量处理多个字幕

        Args:
            video_path: 视频文件路径
            actions: 操作列表，每个操作是包含 action_type 和相关参数的字典

        Returns:
            处理结果列表
        """
        results = []
        subtitles = self.scan_subtitles(video_path)

        for action in actions:
            action_type = action.get("action")
            stream_index = action.get("stream_index")

            try:
                if action_type == "extract":
                    result = self.extract_subtitle(
                        video_path,
                        action["output_path"],
                        stream_index=stream_index,
                        output_format=SubtitleFormat(action.get("format", "srt")),
                    )
                    results.append({"success": True, "output": result})

                elif action_type == "convert":
                    result = self.convert_subtitle(
                        action["input_path"],
                        action["output_path"],
                        SubtitleFormat(action.get("format", "srt")),
                    )
                    results.append({"success": True, "output": result})

            except Exception as e:
                results.append({"success": False, "error": str(e)})

        return results


# 使用示例
if __name__ == "__main__":
    processor = SubtitleProcessor()

    print("=== 字幕处理器测试 ===\n")

    # 示例：扫描字幕
    print("扫描视频字幕:")
    print("请提供视频文件路径进行测试")
    # subtitles = processor.scan_subtitles("test.mp4")
    # print(json.dumps(subtitles, indent=2, ensure_ascii=False))

    # 示例：提取字幕
    print("\n提取字幕:")
    print("processor.extract_subtitle('test.mp4', 'output.srt')")

    # 示例：嵌入字幕
    print("\n嵌入字幕:")
    print("processor.embed_subtitle('test.mp4', 'subtitle.srt', 'output.mp4', language='chi')")

    # 示例：烧录字幕
    print("\n烧录字幕:")
    print(
        "processor.burn_subtitle('test.mp4', subtitle_path='subtitle.srt', output_path='output_burned.mp4')"
    )
