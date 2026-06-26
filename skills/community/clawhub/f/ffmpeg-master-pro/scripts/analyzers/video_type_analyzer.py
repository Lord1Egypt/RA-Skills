"""
视频类型分析器
基于视频内容特征（运动、复杂度、色彩）自动识别视频类型
"""

import os
import subprocess
import tempfile
from typing import Tuple, List
import numpy as np

from . import VideoContentType, VideoAnalysisResult


class VideoTypeAnalyzer:
    """
    视频内容类型分析器

    通过分析视频的运动幅度、场景复杂度和色彩分布，
    自动识别视频类型（屏幕录制、动漫、体育、电影等）
    """

    def __init__(self, use_opencv: bool = False):
        """
        初始化分析器

        Args:
            use_opencv: 是否使用 OpenCV 进行图像处理（如果可用）
                      如果为 False，则使用纯 FFmpeg 方式（降级方案）
        """
        self.use_opencv = use_opencv
        self.opencv_available = False
        self.cv2 = None  # 初始化为 None，确保始终有属性

        # 尝试导入 OpenCV
        if use_opencv:
            try:
                import cv2

                self.cv2 = cv2
                self.opencv_available = True
            except ImportError:
                self.opencv_available = False

        # 分析样本配置
        self.sample_count = 5  # 采样点数量
        self.sample_interval = 10  # 采样间隔（秒）

    def analyze(self, video_path: str) -> VideoAnalysisResult:
        """
        分析视频内容类型

        Args:
            video_path: 视频文件路径

        Returns:
            VideoAnalysisResult: 分析结果
        """
        # 1. 获取视频基本信息
        duration, width, height, fps = self._get_video_info(video_path)

        # 2. 分析各个维度
        motion_score = self._analyze_motion(video_path, duration)
        complexity_score = self._analyze_complexity(video_path, duration)
        color_score = self._analyze_color(video_path, duration)

        # 3. 基于特征分类
        content_type, confidence = self._classify_type(
            motion_score, complexity_score, color_score, width, height, fps
        )

        # 4. 生成备注
        notes = self._generate_analysis_notes(
            motion_score, complexity_score, color_score, content_type, confidence
        )

        return VideoAnalysisResult(
            content_type=content_type,
            confidence=confidence,
            motion_score=motion_score,
            complexity_score=complexity_score,
            color_score=color_score,
            analysis_notes=notes,
        )

    def _get_video_info(self, video_path: str) -> Tuple[float, int, int, float]:
        """
        获取视频基本信息

        Returns:
            (duration, width, height, fps)
        """
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            video_path,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"无法获取视频信息: {result.stderr}")

        import json

        info = json.loads(result.stdout)

        stream = info["streams"][0]
        width = int(stream["width"])
        height = int(stream["height"])

        # 解析帧率（如 "30000/1001"）
        fps_str = stream.get("r_frame_rate", "30/1")
        num, den = map(int, fps_str.split("/"))
        fps = num / den if den != 0 else 30.0

        duration = float(info["format"]["duration"])

        return duration, width, height, fps

    def _analyze_motion(self, video_path: str, duration: float) -> float:
        """
        分析运动幅度

        通过计算相邻帧之间的差异来评估运动幅度

        Returns:
            motion_score: 运动分数 (0-1)，越高表示运动越剧烈
        """
        # 提取样本帧
        sample_timestamps = self._calculate_sample_timestamps(duration)

        # 提取帧并计算差异
        frame_diffs = []
        prev_frame = None

        for timestamp in sample_timestamps:
            frame = self._extract_frame(video_path, timestamp, grayscale=True)

            if prev_frame is not None:
                # 计算帧间差异
                diff = self._calculate_frame_difference(prev_frame, frame)
                frame_diffs.append(diff)

            prev_frame = frame

        # 计算平均运动分数
        if not frame_diffs:
            return 0.5  # 默认中等运动

        avg_diff = np.mean(frame_diffs)

        # 归一化到 0-1
        # 经验值：屏幕录制差异 < 20，体育视频差异 > 100
        motion_score = min(1.0, avg_diff / 100.0)

        return motion_score

    def _analyze_complexity(self, video_path: str, duration: float) -> float:
        """
        分析场景复杂度

        通过边缘检测评估场景的细节丰富程度

        Returns:
            complexity_score: 复杂度分数 (0-1)，越高表示细节越丰富
        """
        # 提取样本帧
        sample_timestamps = self._calculate_sample_timestamps(duration)

        edge_densities = []

        for timestamp in sample_timestamps:
            frame = self._extract_frame(video_path, timestamp, grayscale=True)

            # 计算边缘密度
            edge_density = self._calculate_edge_density(frame)
            edge_densities.append(edge_density)

        # 计算平均复杂度
        if not edge_densities:
            return 0.5

        avg_density = np.mean(edge_densities)

        # 归一化到 0-1
        # 经验值：简单场景 < 0.1，复杂场景 > 0.3
        complexity_score = min(1.0, avg_density / 0.4)

        return complexity_score

    def _analyze_color(self, video_path: str, duration: float) -> float:
        """
        分析色彩分布

        通过计算色彩方差和饱和度评估色彩丰富度

        Returns:
            color_score: 色彩分数 (0-1)，越高表示色彩越丰富
        """
        # 提取样本帧
        sample_timestamps = self._calculate_sample_timestamps(duration)

        color_scores = []

        for timestamp in sample_timestamps:
            frame = self._extract_frame(video_path, timestamp, grayscale=False)

            # 计算色彩特征
            saturation = self._calculate_saturation(frame)
            variance = self._calculate_color_variance(frame)

            # 综合色彩分数
            # 饱和度权重 0.6，方差权重 0.4
            frame_color_score = saturation * 0.6 + variance * 0.4
            color_scores.append(frame_color_score)

        # 计算平均色彩分数
        if not color_scores:
            return 0.5

        avg_color_score = np.mean(color_scores)

        # 归一化到 0-1
        color_score = min(1.0, avg_color_score)

        return color_score

    def _classify_type(
        self, motion: float, complexity: float, color: float, width: int, height: int, fps: float
    ) -> Tuple[VideoContentType, float]:
        """
        基于特征判断视频类型（决策树分类器）

        Returns:
            (content_type, confidence)
        """
        # 1. 屏幕录制特征判断
        # 低运动 + 低复杂度 + 典型分辨率
        is_screen_res = self._is_typical_screen_resolution(width, height)
        if motion < 0.3 and complexity < 0.4 and is_screen_res:
            confidence = 0.85
            return VideoContentType.SCREEN_RECORDING, confidence

        # 2. 老旧视频特征判断（放在动漫之前以避免冲突）
        # 极低色彩 + 极低复杂度 + 低运动
        if color < 0.3 and complexity < 0.4 and motion < 0.4:
            confidence = 0.70
            return VideoContentType.OLD_VIDEO, confidence

        # 3. 动漫特征判断
        # 低色彩（色块为主）+ 低复杂度 + 中低运动
        # 排除极低色彩（已匹配老旧视频）
        if 0.3 <= color < 0.5 and complexity < 0.5 and motion < 0.6:
            confidence = 0.80
            return VideoContentType.ANIME, confidence

        # 4. 体育特征判断
        # 高运动 + 高复杂度
        if motion > 0.7 and complexity > 0.6:
            confidence = 0.85
            return VideoContentType.SPORTS, confidence

        # 5. 音乐视频特征判断
        # 高复杂度 + 中高色彩 + 节奏性运动
        if complexity > 0.6 and color > 0.5 and 0.4 < motion < 0.8:
            confidence = 0.75
            return VideoContentType.MUSIC_VIDEO, confidence

        # 6. 默认：电影/电视剧
        confidence = 0.60
        return VideoContentType.MOVIE, confidence

    def _is_typical_screen_resolution(self, width: int, height: int) -> bool:
        """判断是否为典型的屏幕录制分辨率"""
        common_resolutions = [
            (1920, 1080),
            (2560, 1440),
            (3840, 2160),  # 16:9
            (2560, 1600),
            (1920, 1200),  # 16:10
            (1366, 768),
            (1440, 900),
            (1680, 1050),  # 常见笔记本
            (1280, 720),  # 720p
        ]

        for w, h in common_resolutions:
            if width == w and height == h:
                return True

        return False

    def _calculate_sample_timestamps(self, duration: float) -> List[float]:
        """计算采样时间点"""
        if duration < self.sample_count * self.sample_interval:
            # 视频太短，均匀分布
            return np.linspace(0, duration, self.sample_count).tolist()

        timestamps = []
        for i in range(self.sample_count):
            timestamp = i * self.sample_interval
            if timestamp < duration:
                timestamps.append(timestamp)

        return timestamps

    def _extract_frame(
        self, video_path: str, timestamp: float, grayscale: bool = True
    ) -> np.ndarray:
        """
        从视频中提取指定时间戳的帧

        Returns:
            frame: numpy 数组，shape=(height, width) 或 (height, width, 3)
        """
        # 创建临时文件保存帧
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # 使用 FFmpeg 提取帧
            cmd = [
                "ffmpeg",
                "-ss",
                str(timestamp),
                "-i",
                video_path,
                "-vframes",
                "1",
                "-q:v",
                "2",  # 高质量
                "-y",  # 覆盖输出文件
            ]

            if grayscale:
                cmd.extend(["-pix_fmt", "gray"])

            cmd.append(tmp_path)

            subprocess.run(cmd, capture_output=True, text=True, check=True)

            # 读取帧
            if self.opencv_available:
                frame = self.cv2.imread(tmp_path, self.cv2.IMREAD_UNCHANGED)
            else:
                # 使用 PIL 作为降级方案
                from PIL import Image

                img = Image.open(tmp_path)
                frame = np.array(img)

            return frame

        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _calculate_frame_difference(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """计算两帧之间的差异（使用简单的像素差异）"""
        # 确保帧大小相同
        if frame1.shape != frame2.shape:
            # 调整到较小尺寸
            min_h = min(frame1.shape[0], frame2.shape[0])
            min_w = min(frame1.shape[1], frame2.shape[1])
            frame1 = frame1[:min_h, :min_w]
            frame2 = frame2[:min_h, :min_w]

        # 计算绝对差异
        diff = np.abs(frame1.astype(float) - frame2.astype(float))
        avg_diff = np.mean(diff)

        return avg_diff

    def _calculate_edge_density(self, frame: np.ndarray) -> float:
        """
        计算边缘密度

        使用简单的 Sobel 边缘检测
        """
        if self.opencv_available:
            # 使用 OpenCV 的 Sobel 算子
            sobelx = self.cv2.Sobel(frame, self.cv2.CV_64F, 1, 0, ksize=3)
            sobely = self.cv2.Sobel(frame, self.cv2.CV_64F, 0, 1, ksize=3)
            edges = np.sqrt(sobelx**2 + sobely**2)

            # 计算边缘像素比例
            edge_threshold = 50
            edge_pixels = np.sum(edges > edge_threshold)
            total_pixels = edges.shape[0] * edges.shape[1]
            edge_density = edge_pixels / total_pixels

            return edge_density
        else:
            # 降级方案：使用梯度近似
            gradient_x = np.diff(frame, axis=1)
            gradient_y = np.diff(frame, axis=0)
            edges = np.sqrt(gradient_x**2 + gradient_y**2)

            edge_threshold = 30
            edge_pixels = np.sum(edges > edge_threshold)
            total_pixels = edges.shape[0] * edges.shape[1]
            edge_density = edge_pixels / total_pixels

            return edge_density

    def _calculate_saturation(self, frame: np.ndarray) -> float:
        """
        计算色彩饱和度

        Returns:
            saturation: 饱和度分数 (0-1)
        """
        if len(frame.shape) == 2:
            # 灰度图，饱和度为 0
            return 0.0

        # 转换到 HSV（如果使用 OpenCV）
        if self.opencv_available:
            hsv = self.cv2.cvtColor(frame, self.cv2.COLOR_RGB2HSV)
            saturation = hsv[:, :, 1]
            avg_saturation = np.mean(saturation) / 255.0
            return avg_saturation
        else:
            # 降级方案：使用 RGB 近似计算饱和度
            max_rgb = np.max(frame, axis=2)
            min_rgb = np.min(frame, axis=2)
            saturation = (max_rgb - min_rgb) / (max_rgb + 1e-6)
            avg_saturation = np.mean(saturation)
            return avg_saturation

    def _calculate_color_variance(self, frame: np.ndarray) -> float:
        """
        计算色彩方差

        Returns:
            variance: 色彩方差分数 (0-1)
        """
        if len(frame.shape) == 2:
            return 0.0

        # 计算每个通道的方差
        variances = []
        for channel in range(frame.shape[2]):
            channel_var = np.var(frame[:, :, channel])
            variances.append(channel_var)

        # 归一化（假设最大方差为 10000）
        avg_variance = np.mean(variances)
        normalized_variance = min(1.0, avg_variance / 10000.0)

        return normalized_variance

    def _generate_analysis_notes(
        self,
        motion: float,
        complexity: float,
        color: float,
        content_type: VideoContentType,
        confidence: float,
    ) -> str:
        """生成分析备注"""
        notes = []

        # 特征描述
        if motion < 0.3:
            notes.append("低运动")
        elif motion < 0.7:
            notes.append("中等运动")
        else:
            notes.append("高运动")

        if complexity < 0.4:
            notes.append("低复杂度")
        elif complexity < 0.7:
            notes.append("中等复杂度")
        else:
            notes.append("高复杂度")

        if color < 0.4:
            notes.append("低色彩")
        elif color < 0.7:
            notes.append("中等色彩")
        else:
            notes.append("高色彩")

        # 置信度说明
        if confidence < 0.7:
            notes.append(f"低置信度({confidence:.2f})，建议手动指定类型")
        else:
            notes.append(f"置信度({confidence:.2f})")

        # 类型说明
        type_names = {
            VideoContentType.SCREEN_RECORDING: "屏幕录制",
            VideoContentType.ANIME: "动漫",
            VideoContentType.SPORTS: "体育",
            VideoContentType.MUSIC_VIDEO: "音乐视频",
            VideoContentType.MOVIE: "电影/电视剧",
            VideoContentType.OLD_VIDEO: "老旧视频",
        }

        notes.insert(0, f"识别为: {type_names.get(content_type, '未知')}")

        return ", ".join(notes)


__all__ = ["VideoTypeAnalyzer"]
