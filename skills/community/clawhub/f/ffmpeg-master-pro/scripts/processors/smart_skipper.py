"""
智能跳过处理器
避免重复处理未修改的文件
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, Set
from dataclasses import dataclass
import hashlib


@dataclass
class SkipDecision:
    """跳过决策结果"""

    should_skip: bool
    reason: str
    output_valid: bool = False
    output_exists: bool = False


class SmartSkipper:
    """智能跳过处理器"""

    def __init__(
        self, use_hash: bool = False, validate_output: bool = True, check_duration: bool = True
    ):
        """
        初始化智能跳过器

        Args:
            use_hash: 是否使用文件哈希检测变化（较慢但更准确）
            validate_output: 是否验证输出文件的有效性
            check_duration: 是否检查视频时长匹配
        """
        self.use_hash = use_hash
        self.validate_output = validate_output
        self.check_duration = check_duration

        # 缓存已处理的文件信息
        self.processed_files: Set[str] = set()
        self.file_hashes: Dict[str, str] = {}

    def should_skip(self, input_file: str, output_file: str) -> SkipDecision:
        """
        判断是否应该跳过此文件

        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径

        Returns:
            SkipDecision: 跳过决策结果

        跳过条件：
        1. 输出文件已存在
        2. 输出文件比输入文件新
        3. 输出文件有效（可播放）
        4. 如果启用哈希，输入文件哈希未变化
        """
        # 检查输出文件是否存在
        if not os.path.exists(output_file):
            return SkipDecision(should_skip=False, reason="输出文件不存在", output_exists=False)

        # 比较修改时间
        input_mtime = os.path.getmtime(input_file)
        output_mtime = os.path.getmtime(output_file)

        if output_mtime < input_mtime:
            return SkipDecision(
                should_skip=False, reason="输入文件已更新（较新）", output_exists=True
            )

        # 如果启用了哈希检查，验证输入文件是否变化
        if self.use_hash:
            current_hash = self._calculate_file_hash(input_file)
            if input_file in self.file_hashes:
                if current_hash != self.file_hashes[input_file]:
                    return SkipDecision(
                        should_skip=False,
                        reason="输入文件内容已变化（哈希不同）",
                        output_exists=True,
                    )
            else:
                # 首次处理此文件，记录哈希
                self.file_hashes[input_file] = current_hash

        # 验证输出文件
        if self.validate_output:
            if not self._validate_output(output_file):
                return SkipDecision(
                    should_skip=False,
                    reason="输出文件损坏或无效",
                    output_exists=True,
                    output_valid=False,
                )

            # 如果需要，检查时长匹配
            if self.check_duration:
                if not self._check_duration_match(input_file, output_file):
                    return SkipDecision(
                        should_skip=False,
                        reason="输出文件时长不匹配",
                        output_exists=True,
                        output_valid=False,
                    )

        # 所有检查通过，可以跳过
        self.processed_files.add(input_file)
        return SkipDecision(
            should_skip=True, reason="输出文件已是最新且有效", output_exists=True, output_valid=True
        )

    def _validate_output(self, file_path: str) -> bool:
        """
        验证输出文件是否有效

        Args:
            file_path: 文件路径

        Returns:
            bool: 文件是否有效
        """
        try:
            # 使用 FFprobe 验证文件
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    file_path,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                return False

            # 检查是否有输出
            duration = result.stdout.strip()
            if not duration or float(duration) <= 0:
                return False

            # 检查文件大小
            file_size = os.path.getsize(file_path)
            if file_size < 1024:  # 小于 1KB 认为无效
                return False

            return True

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError):
            return False
        except Exception:
            return False

    def _check_duration_match(
        self, input_file: str, output_file: str, tolerance: float = 1.0
    ) -> bool:
        """
        检查输入和输出文件的时长是否匹配

        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            tolerance: 允许的时长差异（秒）

        Returns:
            bool: 时长是否匹配
        """
        try:
            # 获取输入文件时长
            input_duration = self._get_duration(input_file)
            if input_duration is None:
                return False

            # 获取输出文件时长
            output_duration = self._get_duration(output_file)
            if output_duration is None:
                return False

            # 比较时长（允许一定的误差）
            diff = abs(input_duration - output_duration)
            return diff <= tolerance

        except Exception:
            return False

    def _get_duration(self, file_path: str) -> Optional[float]:
        """
        获取视频文件时长

        Args:
            file_path: 文件路径

        Returns:
            Optional[float]: 时长（秒），失败返回 None
        """
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    file_path,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration

            return None

        except Exception:
            return None

    def _calculate_file_hash(self, file_path: str, chunk_size: int = 8192) -> str:
        """
        计算文件哈希值

        Args:
            file_path: 文件路径
            chunk_size: 读取块大小

        Returns:
            str: 文件的 SHA256 哈希值（前16位）
        """
        try:
            sha256 = hashlib.sha256()

            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    sha256.update(chunk)

            # 返回前16位，节省内存
            return sha256.hexdigest()[:16]

        except Exception:
            return ""

    def mark_processed(self, input_file: str) -> None:
        """
        标记文件为已处理

        Args:
            input_file: 输入文件路径
        """
        self.processed_files.add(input_file)

    def clear_cache(self) -> None:
        """清除缓存"""
        self.processed_files.clear()
        self.file_hashes.clear()

    def get_stats(self) -> Dict:
        """
        获取统计信息

        Returns:
            Dict: 统计信息字典
        """
        return {
            "processed_files_count": len(self.processed_files),
            "cached_hashes_count": len(self.file_hashes),
            "use_hash": self.use_hash,
            "validate_output": self.validate_output,
            "check_duration": self.check_duration,
        }


# 使用示例
if __name__ == "__main__":
    print("=== 智能跳过处理器测试 ===\n")

    # 注意：此示例需要实际的视频文件才能运行
    # 这里仅展示 API 使用方法

    skipper = SmartSkipper(
        use_hash=False,  # 不使用哈希（更快）
        validate_output=True,  # 验证输出文件
        check_duration=True,  # 检查时长匹配
    )

    # 示例 1：基本使用
    print("示例 1：基本使用")
    print("-" * 40)

    input_file = "/path/to/input.mp4"
    output_file = "/path/to/output.mp4"

    # 判断是否应该跳过
    decision = skipper.should_skip(input_file, output_file)

    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"是否跳过: {decision.should_skip}")
    print(f"原因: {decision.reason}")
    print(f"输出文件存在: {decision.output_exists}")
    print(f"输出文件有效: {decision.output_valid}")

    # 示例 2：批量处理
    print("\n\n示例 2：批量处理场景")
    print("-" * 40)

    file_pairs = [
        ("/path/to/video1.mp4", "/path/to/output1.mp4"),
        ("/path/to/video2.mp4", "/path/to/output2.mp4"),
        ("/path/to/video3.mp4", "/path/to/output3.mp4"),
    ]

    skip_count = 0
    process_count = 0

    for input_f, output_f in file_pairs:
        decision = skipper.should_skip(input_f, output_f)

        if decision.should_skip:
            skip_count += 1
            print(f"✓ 跳过: {Path(input_f).name} - {decision.reason}")
        else:
            process_count += 1
            print(f"→ 处理: {Path(input_f).name} - {decision.reason}")

            # 处理完成后标记
            # skipper.mark_processed(input_f)

    print(f"\n统计: 跳过 {skip_count} 个，需要处理 {process_count} 个")

    # 示例 3：查看统计信息
    print("\n\n示例 3：统计信息")
    print("-" * 40)

    stats = skipper.get_stats()
    print(f"已处理文件数: {stats['processed_files_count']}")
    print(f"缓存哈希数: {stats['cached_hashes_count']}")
    print(f"使用哈希检查: {stats['use_hash']}")
    print(f"验证输出文件: {stats['validate_output']}")
    print(f"检查时长匹配: {stats['check_duration']}")

    # 示例 4：清除缓存
    print("\n\n示例 4：清除缓存")
    print("-" * 40)
    skipper.clear_cache()
    print("缓存已清除")
    stats = skipper.get_stats()
    print(f"已处理文件数: {stats['processed_files_count']}")
    print(f"缓存哈希数: {stats['cached_hashes_count']}")

    print("\n\n提示：实际使用时需要提供真实的视频文件路径")
