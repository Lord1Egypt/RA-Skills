"""
关键帧分析器
智能分析视频关键帧位置，提供精确剪辑建议
"""

import json
import subprocess
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import csv


@dataclass
class KeyFrame:
    """关键帧信息"""

    time: float  # 时间戳（秒）
    frame_number: int  # 帧编号
    keyframe_type: str = "I"  # 关键帧类型（I/P/B）


@dataclass
class CutPointQuality:
    """剪辑点质量评估结果"""

    position: float  # 剪辑点位置（秒）
    quality_level: str  # 质量等级: excellent/good/fair/poor
    distance_to_keyframe_before: float  # 到前一个关键帧的距离（秒）
    distance_to_keyframe_after: float  # 到后一个关键帧的距离（秒）
    nearest_keyframe_time: float  # 最近的关键帧时间
    recommended_mode: str  # 推荐的剪辑模式: fast/precise/smart_cut
    precision_estimate: str  # 精度估算
    reason: str  # 评估原因和建议
    encoded_segment_duration: float = 0.0  # 如果使用 smart_cut，需要重编码的片段时长


@dataclass
class TrimStrategy:
    """剪辑策略建议"""

    mode: str  # "fast" 或 "precise"
    reason: str  # 策略原因
    adjusted_start_time: Optional[float] = None  # 调整后的起始时间
    adjusted_end_time: Optional[float] = None  # 调整后的结束时间
    distance_to_nearest_keyframe: float = 0.0  # 到最近关键帧的距离（秒）
    recommended_params: Optional[Dict] = None  # 推荐的 FFmpeg 参数

    def __post_init__(self):
        if self.recommended_params is None:
            self.recommended_params = {}


class KeyFrameAnalyzer:
    """关键帧分析器"""

    def __init__(self):
        """初始化关键帧分析器"""
        self.fast_mode_threshold = 2.0  # 快速模式阈值：距离关键帧 < 2秒
        self.precise_mode_threshold = 5.0  # 精确模式建议阈值：距离关键帧 > 5秒

    def _execute_keyframe_detection(
        self,
        video_path: str,
        time_range: Optional[Tuple[float, float]] = None,
        buffer_seconds: float = 10.0,
        max_frames: Optional[int] = None,
        skip_frames: int = 1,
    ) -> Optional[List[KeyFrame]]:
        """
        执行关键帧检测的核心方法（私有）

        Args:
            video_path: 视频文件路径
            time_range: 目标时间范围 (min_time, max_time)，None 表示检测全部
            buffer_seconds: 缓冲区大小（秒），仅在指定 time_range 时使用
            max_frames: 最大检测帧数（None 表示全部检测）
            skip_frames: 跳过帧数（提高检测速度）

        Returns:
            关键帧列表，检测失败返回 None
        """
        # 构建 ffprobe 命令
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-select_streams",
            "v:0",
            "-show_entries",
            "frame=pkt_pts_time,pict_type,coded_picture_number",
            "-of",
            "json",
        ]

        # 如果指定了时间范围，添加时间和持续时间的参数
        if time_range:
            min_time, max_time = time_range
            search_start = max(0, min_time - buffer_seconds)
            search_duration = (max_time - min_time) + (buffer_seconds * 2)
            cmd.extend(["-ss", str(search_start), "-t", str(search_duration)])

        cmd.append(video_path)

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            data = json.loads(result.stdout)
            frames = data.get("frames", [])

            keyframes = []
            processed_count = 0

            for frame in frames:
                # 只处理关键帧（I帧）
                if frame.get("pict_type") == "I":
                    time = float(frame.get("pkt_pts_time", 0))

                    # 如果指定了时间范围，过滤掉不在范围内的关键帧
                    if time_range:
                        min_time, max_time = time_range
                        if not (min_time <= time <= max_time):
                            continue

                    # 跳过帧策略
                    if len(keyframes) % skip_frames == 0:
                        keyframes.append(
                            KeyFrame(
                                time=time,
                                frame_number=int(frame.get("coded_picture_number", 0)),
                                keyframe_type="I",
                            )
                        )
                        processed_count += 1

                    # 检查是否达到最大帧数
                    if max_frames and processed_count >= max_frames:
                        break

            return keyframes if keyframes else None

        except subprocess.CalledProcessError:
            # FFmpeg 进程执行失败，返回 None
            return None
        except json.JSONDecodeError:
            # JSON 解析失败，返回 None
            return None
        except Exception:
            # 其他异常，返回 None
            return None

    def detect_keyframes(
        self, video_path: str, max_frames: Optional[int] = None, skip_frames: int = 1
    ) -> Optional[List[KeyFrame]]:
        """
        检测视频中的所有关键帧

        Args:
            video_path: 视频文件路径
            max_frames: 最大检测帧数（None 表示全部检测）
            skip_frames: 跳过帧数（提高检测速度）

        Returns:
            关键帧列表，检测失败返回 None
        """
        return self._execute_keyframe_detection(
            video_path=video_path,
            time_range=None,
            max_frames=max_frames,
            skip_frames=skip_frames,
        )

    def detect_keyframes_localized(
        self,
        video_path: str,
        target_range: Tuple[float, float],
        buffer_seconds: float = 10.0,
        max_frames: Optional[int] = None,
        skip_frames: int = 1,
    ) -> Optional[List[KeyFrame]]:
        """
        局部化检测关键帧，只检测指定时间范围内的关键帧

        相比 detect_keyframes，这个方法可以显著减少检测时间，特别适合长视频的剪辑操作。

        Args:
            video_path: 视频文件路径
            target_range: 目标时间范围 (min_time, max_time)，单位：秒
            buffer_seconds: 缓冲区大小（秒），在目标范围前后各扩展的时间，默认10秒
            max_frames: 最大检测帧数（None 表示全部检测）
            skip_frames: 跳过帧数（提高检测速度）

        Returns:
            关键帧列表，检测失败返回 None

        示例:
            >>> analyzer = KeyFrameAnalyzer()
            >>> # 只检测 20-100 秒范围内的关键帧
            >>> keyframes = analyzer.detect_keyframes_localized(
            ...     video_path="input.mp4",
            ...     target_range=(20.0, 100.0)
            ... )
        """
        return self._execute_keyframe_detection(
            video_path=video_path,
            time_range=target_range,
            buffer_seconds=buffer_seconds,
            max_frames=max_frames,
            skip_frames=skip_frames,
        )

    def find_nearest_keyframe(
        self, keyframes: List[KeyFrame], target_time: float, direction: str = "nearest"
    ) -> Optional[KeyFrame]:
        """
        查找距离目标时间最近的关键帧

        Args:
            keyframes: 关键帧列表
            target_time: 目标时间（秒）
            direction: 搜索方向 ("nearest", "before", "after")

        Returns:
            最近的关键帧，如果不存在返回 None
        """
        if not keyframes:
            return None

        if direction == "before":
            # 查找目标时间之前最近的关键帧
            result = None
            for kf in keyframes:
                if kf.time <= target_time:
                    result = kf
                else:
                    break
            return result

        elif direction == "after":
            # 查找目标时间之后最近的关键帧
            for kf in keyframes:
                if kf.time >= target_time:
                    return kf
            return None

        else:  # "nearest"
            # 查找距离目标时间最近的关键帧
            nearest = keyframes[0]
            min_distance = abs(nearest.time - target_time)

            for kf in keyframes[1:]:
                distance = abs(kf.time - target_time)
                if distance < min_distance:
                    min_distance = distance
                    nearest = kf

            return nearest

    def suggest_trim_strategy(
        self,
        start_time: float,
        duration: float,
        video_path: str,
        prefer_mode: str = "auto",
    ) -> TrimStrategy:
        """
        根据关键帧位置建议剪辑策略

        Args:
            start_time: 起始时间（秒）
            duration: 持续时间（秒）
            video_path: 视频文件路径
            prefer_mode: 偏好模式 ("auto", "fast", "precise")

        Returns:
            剪辑策略建议
        """
        end_time = start_time + duration

        keyframes = self.detect_keyframes_localized(
            video_path=video_path,
            target_range=(start_time, end_time),
            buffer_seconds=10.0,
            max_frames=1000,
        )

        if not keyframes or keyframes is None:
            # 如果无法检测关键帧，默认使用精确模式
            return TrimStrategy(
                mode="precise",
                reason="无法检测关键帧，建议使用精确剪辑模式",
                recommended_params={
                    "codec": "libx264",
                    "preset": "medium",
                    "audio_codec": "aac",
                },
            )

        # 查找起始位置附近的关键帧
        start_keyframe_before = self.find_nearest_keyframe(
            keyframes, start_time, "before"
        )
        start_keyframe_after = self.find_nearest_keyframe(
            keyframes, start_time, "after"
        )

        # 查找结束位置附近的关键帧
        end_keyframe_before = self.find_nearest_keyframe(keyframes, end_time, "before")
        end_keyframe_after = self.find_nearest_keyframe(keyframes, end_time, "after")

        # 计算到最近关键帧的距离
        start_distances = []
        if start_keyframe_before:
            start_distances.append(abs(start_time - start_keyframe_before.time))
        if start_keyframe_after:
            start_distances.append(abs(start_keyframe_after.time - start_time))

        end_distances = []
        if end_keyframe_before:
            end_distances.append(abs(end_time - end_keyframe_before.time))
        if end_keyframe_after:
            end_distances.append(abs(end_keyframe_after.time - end_time))

        min_start_distance = min(start_distances) if start_distances else float("inf")
        min_end_distance = min(end_distances) if end_distances else float("inf")
        max_distance = max(min_start_distance, min_end_distance)

        # 决策逻辑
        if prefer_mode == "fast":
            # 用户偏好快速模式
            adjusted_start = (
                start_keyframe_before.time if start_keyframe_before else start_time
            )
            adjusted_end = end_keyframe_before.time if end_keyframe_before else end_time

            return TrimStrategy(
                mode="fast",
                reason=f"用户偏好快速模式，使用关键帧对齐剪辑（-c copy）",
                adjusted_start_time=adjusted_start,
                adjusted_end_time=adjusted_end,
                distance_to_nearest_keyframe=max_distance,
                recommended_params={
                    "copy_mode": True,
                    "avoid_negative_ts": "make_zero",
                    "fflags": "+genpts",
                },
            )

        elif prefer_mode == "precise":
            # 用户偏好精确模式
            return TrimStrategy(
                mode="precise",
                reason=f"用户偏好精确模式，重新编码以确保精确剪辑点",
                adjusted_start_time=start_time,
                adjusted_end_time=end_time,
                distance_to_nearest_keyframe=max_distance,
                recommended_params={
                    "codec": "libx264",
                    "preset": "medium",
                    "crf": 23,
                    "audio_codec": "aac",
                    "avoid_negative_ts": "make_zero",
                    "fflags": "+genpts",
                },
            )

        else:  # "auto"
            # 自动决策
            if max_distance < self.fast_mode_threshold:
                # 距离关键帧很近，使用快速模式
                adjusted_start = (
                    start_keyframe_before.time if start_keyframe_before else start_time
                )
                adjusted_end = (
                    end_keyframe_before.time if end_keyframe_before else end_time
                )

                return TrimStrategy(
                    mode="fast",
                    reason=f"剪辑点距离关键帧很近（{max_distance:.2f}秒），建议使用快速模式（流拷贝）",
                    adjusted_start_time=adjusted_start,
                    adjusted_end_time=adjusted_end,
                    distance_to_nearest_keyframe=max_distance,
                    recommended_params={
                        "copy_mode": True,
                        "avoid_negative_ts": "make_zero",
                        "fflags": "+genpts",
                    },
                )

            elif max_distance > self.precise_mode_threshold:
                # 距离关键帧较远，建议精确模式
                return TrimStrategy(
                    mode="precise",
                    reason=f"剪辑点距离关键帧较远（{max_distance:.2f}秒），建议使用精确模式（重新编码）",
                    adjusted_start_time=start_time,
                    adjusted_end_time=end_time,
                    distance_to_nearest_keyframe=max_distance,
                    recommended_params={
                        "codec": "libx264",
                        "preset": "medium",
                        "crf": 23,
                        "audio_codec": "aac",
                        "avoid_negative_ts": "make_zero",
                        "fflags": "+genpts",
                    },
                )

            else:
                # 中等距离，提供两种选择
                adjusted_start = (
                    start_keyframe_before.time if start_keyframe_before else start_time
                )
                adjusted_end = (
                    end_keyframe_before.time if end_keyframe_before else end_time
                )

                return TrimStrategy(
                    mode="hybrid",
                    reason=f"剪辑点距离关键帧中等距离（{max_distance:.2f}秒），可选择快速或精确模式",
                    adjusted_start_time=adjusted_start,
                    adjusted_end_time=adjusted_end,
                    distance_to_nearest_keyframe=max_distance,
                    recommended_params={
                        "fast_option": {
                            "description": "快速模式（流拷贝）",
                            "adjusted_start": adjusted_start,
                            "adjusted_end": adjusted_end,
                            "params": {
                                "copy_mode": True,
                                "avoid_negative_ts": "make_zero",
                                "fflags": "+genpts",
                            },
                        },
                        "precise_option": {
                            "description": "精确模式（重新编码）",
                            "params": {
                                "codec": "libx264",
                                "preset": "medium",
                                "crf": 23,
                                "audio_codec": "aac",
                                "avoid_negative_ts": "make_zero",
                                "fflags": "+genpts",
                            },
                        },
                    },
                )

    def analyze_edit_position(self, start_time: float, video_duration: float) -> str:
        """
        分析剪辑位置类型

        Args:
            start_time: 起始时间
            video_duration: 视频总时长

        Returns:
            位置类型 ("start", "middle", "end")
        """
        if start_time <= 1.0:
            return "start"
        elif start_time >= video_duration - 10.0:
            return "end"
        else:
            return "middle"

    def should_enable_sync_fix(
        self,
        start_time: Optional[float] = None,
        duration: Optional[float] = None,
        video_duration: Optional[float] = None,
        copy_mode: bool = False,
    ) -> Tuple[bool, str]:
        """
        判断是否需要启用音视频同步修复

        Args:
            start_time: 起始时间（秒）
            duration: 持续时间（秒）
            video_duration: 视频总时长（秒）
            copy_mode: 是否使用流拷贝模式

        Returns:
            (是否需要修复, 原因说明)
        """
        # 处理 start_time 为 0 的情况
        if start_time is None:
            start_time = 0

        if start_time == 0 and not duration:
            # 没有剪辑操作，不需要修复
            return False, "未进行剪辑操作"

        position = self.analyze_edit_position(start_time, video_duration or 0)

        if position == "start":
            # 从开头剪辑，通常不需要同步修复
            if copy_mode:
                return False, "从视频开头剪辑，流拷贝模式下通常不会出现同步问题"
            else:
                return False, "从视频开头剪辑，重新编码模式下不会出现同步问题"

        elif position == "middle":
            # 从中间剪辑，强烈建议启用同步修复
            if copy_mode:
                return True, "从中间剪辑 + 流拷贝模式，强烈建议启用同步修复参数"
            else:
                return True, "从中间剪辑，建议启用同步修复参数以防时间戳问题"

        elif position == "end":
            # 从结尾剪辑，建议启用同步修复
            if copy_mode:
                return True, "从结尾剪辑 + 流拷贝模式，建议启用同步修复参数"
            else:
                return True, "从结尾剪辑，可能产生负时间戳，建议启用同步修复参数"

        return False, "未知剪辑位置"

    def get_sync_fix_params(self) -> List[str]:
        """
        获取音视频同步修复的 FFmpeg 参数

        Returns:
            FFmpeg 参数列表
        """
        return ["-avoid_negative_ts", "make_zero", "-fflags", "+genpts"]

    def suggest_trim_strategy_smart_cut(
        self,
        start_time: float,
        duration: float,
        video_path: str,
        max_encoded_segment: float = 5.0,
    ) -> TrimStrategy:
        """
        Smart Cut 混合剪辑模式策略
        只重编码剪辑点附近的小片段（通常几秒），其余使用流拷贝

        Args:
            start_time: 起始时间（秒）
            duration: 持续时间（秒）
            video_path: 视频文件路径
            max_encoded_segment: 最大重编码片段时长（秒），默认5秒

        Returns:
            Smart Cut 剪辑策略
        """
        end_time = start_time + duration

        keyframes = self.detect_keyframes_localized(
            video_path=video_path,
            target_range=(start_time, end_time),
            buffer_seconds=10.0,
            max_frames=2000,
        )

        if not keyframes or keyframes is None:
            # 无法检测关键帧，回退到精确模式
            return TrimStrategy(
                mode="precise",
                reason="无法检测关键帧，Smart Cut 不可用，回退到精确模式",
                adjusted_start_time=start_time,
                adjusted_end_time=end_time,
                recommended_params={
                    "codec": "libx264",
                    "preset": "medium",
                    "crf": 23,
                    "audio_codec": "aac",
                    "avoid_negative_ts": "make_zero",
                    "fflags": "+genpts",
                },
            )

        # 查找起始点附近的关键帧
        start_kf_after = self.find_nearest_keyframe(keyframes, start_time, "after")

        # 查找结束点附近的关键帧
        end_kf_before = self.find_nearest_keyframe(keyframes, end_time, "before")
        end_kf_after = self.find_nearest_keyframe(keyframes, end_time, "after")

        # 计算需要重编码的片段时长
        start_encode_duration = 0.0
        end_encode_duration = 0.0

        if start_kf_after:
            # 起始点到后一个关键帧的时长
            start_encode_duration = start_kf_after.time - start_time

        if end_kf_after:
            # 结束点到后一个关键帧的时长
            end_encode_duration = end_kf_after.time - end_time

        total_encode_duration = start_encode_duration + end_encode_duration

        # 如果需要重编码的片段太长，建议使用纯精确模式
        if total_encode_duration > max_encoded_segment * 2:
            return TrimStrategy(
                mode="precise",
                reason=f"需要重编码的片段过长（{total_encode_duration:.2f}秒），建议使用完全重编码模式",
                adjusted_start_time=start_time,
                adjusted_end_time=end_time,
                distance_to_nearest_keyframe=max(
                    start_encode_duration, end_encode_duration
                ),
                recommended_params={
                    "codec": "libx264",
                    "preset": "medium",
                    "crf": 23,
                    "audio_codec": "aac",
                    "avoid_negative_ts": "make_zero",
                    "fflags": "+genpts",
                },
            )

        # Smart Cut 分段策略
        segments = []

        # 片段1：起始重编码段（如果需要）
        if start_kf_after and start_encode_duration > 0.1:
            segments.append(
                {
                    "type": "encoded",
                    "start": start_time,
                    "end": start_kf_after.time,
                    "duration": start_encode_duration,
                }
            )

        # 片段2：中间流拷贝段
        middle_start = start_time
        middle_end = end_time
        if start_kf_after:
            middle_start = start_kf_after.time
        if end_kf_before:
            middle_end = end_kf_before.time

        if middle_end > middle_start:
            segments.append(
                {
                    "type": "copy",
                    "start": middle_start,
                    "end": middle_end,
                    "duration": middle_end - middle_start,
                }
            )

        # 片段3：结束重编码段（如果需要）
        if end_kf_after and end_encode_duration > 0.1:
            segments.append(
                {
                    "type": "encoded",
                    "start": end_time,
                    "end": end_kf_after.time,
                    "duration": end_encode_duration,
                }
            )

        return TrimStrategy(
            mode="smart_cut",
            reason=f"Smart Cut 模式：只需重编码 {total_encode_duration:.2f} 秒，其余使用流拷贝",
            adjusted_start_time=start_time,
            adjusted_end_time=end_time,
            distance_to_nearest_keyframe=max(
                start_encode_duration, end_encode_duration
            ),
            recommended_params={
                "segments": segments,
                "total_encoded_duration": total_encode_duration,
                "copy_duration": middle_end - middle_start,
                "num_segments": len(segments),
                "codec": "libx264",
                "preset": "fast",  # 使用快速预设，因为只是小片段
                "crf": 18,  # 使用较高质量，因为是重编码
                "audio_codec": "aac",
                "avoid_negative_ts": "make_zero",
                "fflags": "+genpts",
            },
        )

    def export_keyframe_timeline(
        self,
        video_path: str,
        output_format: str = "json",
        output_file: Optional[str] = None,
        max_frames: Optional[int] = None,
    ) -> Optional[Union[str, Dict]]:
        """
        导出关键帧时间轴为多种格式

        Args:
            video_path: 视频文件路径
            output_format: 输出格式 ("json", "csv", "markdown", "txt")
            output_file: 输出文件路径（可选，如果不提供则返回字符串）
            max_frames: 最大检测帧数（None 表示全部检测）

        Returns:
            如果 output_file 为 None，返回格式化的字符串或字典
            如果 output_file 指定，返回 None，结果写入文件
        """
        # 检测关键帧
        keyframes = self.detect_keyframes(video_path, max_frames=max_frames)

        if not keyframes:
            return None

        # 根据格式生成输出
        if output_format == "json":
            result = {
                "video_path": video_path,
                "total_keyframes": len(keyframes),
                "keyframes": [
                    {
                        "index": i,
                        "time": kf.time,
                        "time_formatted": self._format_time(kf.time),
                        "frame_number": kf.frame_number,
                        "type": kf.keyframe_type,
                    }
                    for i, kf in enumerate(keyframes)
                ],
            }

            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                return None
            else:
                return result

        elif output_format == "csv":
            lines = []
            lines.append(["索引", "时间(秒)", "时间码", "帧编号", "类型"])
            for i, kf in enumerate(keyframes):
                lines.append(
                    [
                        str(i),
                        f"{kf.time:.6f}",
                        self._format_time(kf.time),
                        str(kf.frame_number),
                        kf.keyframe_type,
                    ]
                )

            if output_file:
                with open(output_file, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(lines)
                return None
            else:
                # 返回 CSV 格式字符串
                return "\n".join([",".join(line) for line in lines])

        elif output_format == "markdown":
            lines = []
            lines.append(f"# 关键帧时间轴")
            lines.append(f"\n**视频**: {video_path}")
            lines.append(f"**总关键帧数**: {len(keyframes)}")
            lines.append(f"\n| 索引 | 时间 (秒) | 时间码 | 帧编号 | 类型 |")
            lines.append(f"|------|-----------|--------|--------|------|")

            for i, kf in enumerate(keyframes):
                lines.append(
                    f"| {i} | {kf.time:.6f} | {self._format_time(kf.time)} | "
                    f"{kf.frame_number} | {kf.keyframe_type} |"
                )

            result = "\n".join(lines)

            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result)
                return None
            else:
                return result

        elif output_format == "txt":
            lines = []
            lines.append(f"关键帧时间轴 - {video_path}")
            lines.append(f"总关键帧数: {len(keyframes)}")
            lines.append("=" * 80)
            lines.append("")

            for i, kf in enumerate(keyframes):
                lines.append(
                    f"[{i:4d}] 时间: {kf.time:12.6f}s | "
                    f"时间码: {self._format_time(kf.time)} | "
                    f"帧号: {kf.frame_number:8d} | "
                    f"类型: {kf.keyframe_type}"
                )

            result = "\n".join(lines)

            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result)
                return None
            else:
                return result

        else:
            raise ValueError(f"不支持的输出格式: {output_format}")

    def assess_cut_point_quality(
        self, video_path: str, cut_point: float, max_frames: Optional[int] = None
    ) -> Optional[CutPointQuality]:
        """
        评估剪辑点的质量并提供建议

        Args:
            video_path: 视频文件路径
            cut_point: 剪辑点位置（秒）
            max_frames: 最大检测帧数（None 表示全部检测）

        Returns:
            剪辑点质量评估结果，检测失败返回 None
        """
        keyframes = self.detect_keyframes_localized(
            video_path=video_path,
            target_range=(max(0, cut_point - 10), cut_point + 10),
            buffer_seconds=5.0,
            max_frames=max_frames,
        )

        if not keyframes:
            return None

        # 查找前后的关键帧
        kf_before = self.find_nearest_keyframe(keyframes, cut_point, "before")
        kf_after = self.find_nearest_keyframe(keyframes, cut_point, "after")

        if not kf_before or not kf_after:
            return None

        # 计算距离
        dist_before = cut_point - kf_before.time
        dist_after = kf_after.time - cut_point

        # 找出最近的关键帧
        min_distance = min(dist_before, dist_after)
        nearest_kf_time = kf_before.time if dist_before < dist_after else kf_after.time

        # 评估质量等级
        if min_distance < 0.5:
            quality_level = "excellent"
            precision = "±0.5秒内，关键帧对齐"
            recommended = "fast"
            reason = "剪辑点非常接近关键帧，强烈推荐使用快速模式（流拷贝），速度极快且质量无损"
        elif min_distance < 2.0:
            quality_level = "good"
            precision = "±2秒内，轻微偏差"
            recommended = "fast"
            reason = "剪辑点接近关键帧，推荐使用快速模式（流拷贝），偏差很小且速度极快"
        elif min_distance < 5.0:
            quality_level = "fair"
            precision = "±5秒内，中等偏差"
            recommended = "smart_cut"
            # 估算 smart_cut 需要重编码的时长
            encoded_duration = min(dist_before, 2.0) + min(dist_after, 2.0)
            reason = (
                f"剪辑点距离关键帧中等距离，推荐使用 Smart Cut 模式，"
                f"只需重编码约 {encoded_duration:.1f} 秒的片段"
            )
        else:
            quality_level = "poor"
            precision = f"±{min_distance:.1f}秒，较大偏差"
            recommended = "precise"
            # 如果使用 smart_cut，需要重编码较多
            encoded_duration = min(dist_before, 5.0) + min(dist_after, 5.0)
            reason = (
                f"剪辑点距离关键帧较远（{min_distance:.2f}秒），推荐使用精确模式（完全重编码）"
                f"以确保精确剪辑点。Smart Cut 需要重编码约 {encoded_duration:.1f} 秒"
            )

        return CutPointQuality(
            position=cut_point,
            quality_level=quality_level,
            distance_to_keyframe_before=dist_before,
            distance_to_keyframe_after=dist_after,
            nearest_keyframe_time=nearest_kf_time,
            recommended_mode=recommended,
            precision_estimate=precision,
            reason=reason,
            encoded_segment_duration=encoded_duration
            if quality_level in ["fair", "poor"]
            else 0.0,
        )

    def _format_time(self, seconds: float) -> str:
        """
        格式化时间为 HH:MM:SS.mmm 格式

        Args:
            seconds: 时间（秒）

        Returns:
            格式化的时间字符串
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


# 使用示例
if __name__ == "__main__":
    analyzer = KeyFrameAnalyzer()

    print("=== 关键帧分析器测试 ===\n")

    # 示例 1：检测关键帧
    print("示例 1：检测关键帧")
    print("请提供视频文件路径进行测试")
    # keyframes = analyzer.detect_keyframes("test.mp4")
    # print(f"检测到 {len(keyframes)} 个关键帧")
    # for kf in keyframes[:5]:  # 显示前5个
    #     print(f"  时间: {kf.time:.2f}s, 帧号: {kf.frame_number}")

    # 示例 2：建议剪辑策略
    print("\n示例 2：建议剪辑策略")
    print("从第 30 秒开始剪辑 60 秒")
    # strategy = analyzer.suggest_trim_strategy(30.0, 60.0, "test.mp4")
    # print(f"推荐模式: {strategy.mode}")
    # print(f"原因: {strategy.reason}")
    # print(f"调整后的起始时间: {strategy.adjusted_start_time}s")
    # print(f"调整后的结束时间: {strategy.adjusted_end_time}s")
    # print(f"推荐参数: {strategy.recommended_params}")

    print("\n测试完成")
