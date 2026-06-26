"""
自适应码率控制器 - 基于实际大小迭代优化码率
实现智能的码率调整策略，确保输出文件大小符合目标要求
"""

import os
from typing import List, Optional
from dataclasses import dataclass
from .two_pass_encoder import TwoPassEncoder


@dataclass
class OptimizeResult:
    """优化结果"""

    success: bool
    output_file: str = ""
    actual_size_mb: float = 0.0
    target_size_mb: float = 0.0
    error_pct: float = 0.0
    attempts: int = 0
    final_bitrate: int = 0
    error: str = ""
    history: List[dict] = None


class AdaptiveBitrateController:
    """自适应码率控制器"""

    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        """
        初始化自适应码率控制器

        Args:
            ffmpeg_path: FFmpeg 可执行文件路径
        """
        self.ffmpeg_path = ffmpeg_path
        self.encoder = TwoPassEncoder(ffmpeg_path)
        self.adjust_history: List[dict] = []

        # 码率限制（防止极端值）
        self.min_bitrate = 500  # kbps
        self.max_bitrate = 50000  # kbps

        # 调整参数
        self.tolerance = 0.05  # 容忍误差（5%）
        self.max_history = 10  # 历史记录最大数量

    def refine_bitrate(
        self,
        target_size_mb: float,
        actual_size_mb: float,
        current_bitrate: int,
        duration_seconds: float,
        attempt: int = 1,
    ) -> int:
        """
        基于实际大小调整码率

        Args:
            target_size_mb: 目标文件大小（MB）
            actual_size_mb: 实际文件大小（MB）
            current_bitrate: 当前视频码率（kbps）
            duration_seconds: 视频时长（秒）
            attempt: 当前尝试次数

        Returns:
            调整后的码率（kbps）

        策略：
        - 如果偏差 < 5%，保持当前码率
        - 如果偏差 > 5%，按比例调整码率
        - 使用加权移动平均避免震荡
        - 限制码率范围
        """
        # 计算误差百分比
        error_pct = (actual_size_mb - target_size_mb) / target_size_mb

        # 如果在容忍范围内，不需要调整
        if abs(error_pct) < self.tolerance:
            return current_bitrate

        # 计算调整因子（使用加权策略）
        # 早期尝试使用较大的调整步长，后期使用较小步长
        weight = 1.0 / (1.0 + attempt * 0.3)
        adjustment_factor = 1.0 - (error_pct * weight)

        # 应用调整
        new_bitrate = int(current_bitrate * adjustment_factor)

        # 限制码率范围
        new_bitrate = max(self.min_bitrate, min(new_bitrate, self.max_bitrate))

        # 记录历史
        self.adjust_history.append(
            {
                "attempt": attempt,
                "target_size": target_size_mb,
                "actual_size": actual_size_mb,
                "old_bitrate": current_bitrate,
                "new_bitrate": new_bitrate,
                "error_pct": error_pct,
            }
        )

        # 限制历史记录数量
        if len(self.adjust_history) > self.max_history:
            self.adjust_history.pop(0)

        return new_bitrate

    def optimize_bitrate(
        self,
        input_file: str,
        output_file: str,
        target_size_mb: float,
        duration_seconds: float,
        audio_bitrate_kbps: int = 128,
        initial_bitrate: Optional[int] = None,
        max_attempts: int = 3,
        preset: str = "medium",
        codec: str = "libx264",
    ) -> OptimizeResult:
        """
        迭代优化码率以达到目标文件大小

        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            target_size_mb: 目标文件大小（MB）
            duration_seconds: 视频时长（秒）
            audio_bitrate_kbps: 音频码率（kbps）
            initial_bitrate: 初始码率（kbps），如果为 None 则自动计算
            max_attempts: 最大尝试次数
            preset: 编码预设
            codec: 视频编解码器

        Returns:
            OptimizeResult 优化结果
        """
        # 验证输入文件
        if not os.path.exists(input_file):
            return OptimizeResult(success=False, error=f"输入文件不存在: {input_file}")

        # 计算初始码率
        if initial_bitrate is None:
            current_bitrate = self.encoder.calculate_target_bitrate(
                target_size_mb, duration_seconds, audio_bitrate_kbps
            )
        else:
            current_bitrate = initial_bitrate

        # 清空历史记录
        self.adjust_history.clear()

        history = []

        # 迭代优化
        for attempt in range(1, max_attempts + 1):
            print(f"\n尝试 {attempt}/{max_attempts} (码率: {current_bitrate} kbps)")

            # 生成临时输出文件名
            if attempt < max_attempts:
                temp_output = f"{os.path.splitext(output_file)[0]}_temp_{attempt}.mp4"
            else:
                temp_output = output_file

            # 执行两遍编码
            result = self.encoder.encode(
                input_file,
                temp_output,
                target_size_mb,
                duration_seconds,
                audio_bitrate_kbps,
                preset,
                codec,
            )

            # 记录历史
            history.append(
                {
                    "attempt": attempt,
                    "bitrate": current_bitrate,
                    "actual_size": result.actual_size_mb if result.success else 0,
                    "success": result.success,
                    "error": result.error,
                }
            )

            # 如果编码失败
            if not result.success:
                print(f"编码失败: {result.error}")
                continue

            # 计算误差
            error_pct = abs(result.actual_size_mb - target_size_mb) / target_size_mb
            print(
                f"目标: {target_size_mb:.2f} MB, 实际: {result.actual_size_mb:.2f} MB, 误差: {error_pct*100:.2f}%"
            )

            # 检查是否满足要求
            if error_pct < self.tolerance:
                print(f"✓ 文件大小符合要求（误差 < {self.tolerance*100}%）")

                # 如果是临时文件，重命名为最终文件
                if attempt < max_attempts and os.path.exists(temp_output):
                    if os.path.exists(output_file):
                        os.remove(output_file)
                    os.rename(temp_output, output_file)

                return OptimizeResult(
                    success=True,
                    output_file=output_file,
                    actual_size_mb=result.actual_size_mb,
                    target_size_mb=target_size_mb,
                    error_pct=error_pct,
                    attempts=attempt,
                    final_bitrate=current_bitrate,
                    history=history,
                )

            # 如果是最后一次尝试，返回当前结果
            if attempt == max_attempts:
                print(f"达到最大尝试次数，使用当前结果")

                # 删除临时文件，保留最后一次的输出
                for i in range(1, max_attempts):
                    temp_file = f"{os.path.splitext(output_file)[0]}_temp_{i}.mp4"
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

                return OptimizeResult(
                    success=True,
                    output_file=output_file,
                    actual_size_mb=result.actual_size_mb,
                    target_size_mb=target_size_mb,
                    error_pct=error_pct,
                    attempts=attempt,
                    final_bitrate=current_bitrate,
                    history=history,
                )

            # 调整码率进行下一次尝试
            old_bitrate = current_bitrate
            current_bitrate = self.refine_bitrate(
                target_size_mb, result.actual_size_mb, current_bitrate, duration_seconds, attempt
            )
            print(f"调整码率: {old_bitrate} -> {current_bitrate} kbps")

        # 所有尝试都失败
        return OptimizeResult(
            success=False, error="所有尝试都失败", attempts=max_attempts, history=history
        )

    def get_adjustment_history(self) -> List[dict]:
        """获取码率调整历史"""
        return self.adjust_history.copy()

    def clear_history(self):
        """清空历史记录"""
        self.adjust_history.clear()

    def predict_bitrate(
        self,
        target_size_mb: float,
        duration_seconds: float,
        audio_bitrate_kbps: int = 128,
        safety_factor: float = 0.05,
    ) -> int:
        """
        预测所需码率

        Args:
            target_size_mb: 目标文件大小（MB）
            duration_seconds: 视频时长（秒）
            audio_bitrate_kbps: 音频码率（kbps）
            safety_factor: 安全余量（默认 5%）

        Returns:
            预测的视频码率（kbps）
        """
        target_size_kb = target_size_mb * 1024
        total_bitrate = (target_size_kb * 8) / duration_seconds

        # 应用安全余量
        total_bitrate = total_bitrate * (1.0 - safety_factor)

        video_bitrate = total_bitrate - audio_bitrate_kbps

        return max(self.min_bitrate, min(int(video_bitrate), self.max_bitrate))

    def estimate_attempts_needed(
        self, target_size_mb: float, estimated_size_mb: float, tolerance: float = 0.05
    ) -> int:
        """
        估计需要多少次尝试才能达到目标

        Args:
            target_size_mb: 目标文件大小
            estimated_size_mb: 估计的文件大小
            tolerance: 容忍误差

        Returns:
            预计尝试次数（1-3）
        """
        error_pct = abs(estimated_size_mb - target_size_mb) / target_size_mb

        if error_pct < tolerance:
            return 1
        elif error_pct < tolerance * 3:
            return 2
        else:
            return 3


# 使用示例
if __name__ == "__main__":
    print("=== 自适应码率控制器测试 ===\n")

    controller = AdaptiveBitrateController()

    # 示例 1：码率调整
    print("示例 1：码率调整")
    current_bitrate = controller.refine_bitrate(
        target_size_mb=100,
        actual_size_mb=90,
        current_bitrate=1500,
        duration_seconds=3600,
        attempt=1,
    )
    print(f"目标: 100 MB, 实际: 90 MB")
    print(f"调整后码率: {current_bitrate} kbps")
    print()

    # 示例 2：预测码率
    print("示例 2：预测码率")
    predicted = controller.predict_bitrate(
        target_size_mb=100, duration_seconds=3600, audio_bitrate_kbps=128
    )
    print(f"目标: 100 MB, 时长: 1 小时")
    print(f"预测码率: {predicted} kbps")
    print()

    # 示例 3：估计尝试次数
    print("示例 3：估计尝试次数")
    attempts = controller.estimate_attempts_needed(target_size_mb=100, estimated_size_mb=85)
    print(f"目标: 100 MB, 估计: 85 MB")
    print(f"预计需要: {attempts} 次尝试")
