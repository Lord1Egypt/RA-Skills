"""
优化的批量处理器
集成重试、智能跳过、进度跟踪和报告生成
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum
from typing import Callable, List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from .retry_handler import RetryHandler, RetryStrategy
from .smart_skipper import SmartSkipper

try:
    from ..utils.batch_reporter import BatchReportGenerator, ProcessResult, BatchStatistics
    from ..progress.progress_display import BatchProgressDisplay
except ImportError:
    from utils.batch_reporter import BatchReportGenerator, ProcessResult, BatchStatistics
    from progress.progress_display import BatchProgressDisplay


class SkipStrategy(Enum):
    """跳过策略枚举"""

    NONE = "none"  # 不跳过任何文件
    SMART = "smart"  # 智能跳过（默认）
    FORCE = "force"  # 强制跳过所有已存在的文件


class OptimizedBatchProcessor:
    """优化的批量处理器"""

    def __init__(
        self,
        max_workers: Optional[int] = None,
        enable_retry: bool = True,
        enable_smart_skip: bool = True,
        enable_report: bool = True,
        retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
    ):
        """
        初始化优化的批量处理器

        Args:
            max_workers: 最大并行工作线程数，None 则自动检测
            enable_retry: 是否启用重试机制
            enable_smart_skip: 是否启用智能跳过
            enable_report: 是否启用报告生成
            retry_strategy: 重试策略
        """
        # 智能确定并行度
        if max_workers is None:
            cpu_count = os.cpu_count() or 4
            # 预留 2 个核心给系统
            self.max_workers = max(2, cpu_count - 2)
        else:
            self.max_workers = max(1, max_workers)

        self.enable_retry = enable_retry
        self.enable_smart_skip = enable_smart_skip
        self.enable_report = enable_report

        # 初始化组件
        self.retry_handler = (
            RetryHandler(max_retries=3, strategy=retry_strategy) if enable_retry else None
        )

        self.smart_skipper = (
            SmartSkipper(use_hash=False, validate_output=True, check_duration=True)
            if enable_smart_skip
            else None
        )

        self.report_generator = BatchReportGenerator() if enable_report else None
        self.progress_display = BatchProgressDisplay()

    def process_batch(
        self,
        files: List[Dict[str, str]],
        processor_func: Callable[[str, str], Any],
        skip_strategy: SkipStrategy = SkipStrategy.SMART,
        batch_title: str = "",
        batch_description: str = "",
    ) -> BatchStatistics:
        """
        批量处理文件

        Args:
            files: 文件列表，每个元素是包含 input 和 output 的字典
                   例如: [{"input": "in.mp4", "output": "out.mkv"}, ...]
            processor_func: 处理函数，接收 (input_file, output_file)，返回处理结果
            skip_strategy: 跳过策略
            batch_title: 批处理标题（用于报告）
            batch_description: 批处理描述（用于报告）

        Returns:
            BatchStatistics: 批量处理统计信息
        """
        # 初始化批处理
        self._initialize_batch(batch_title, batch_description, len(files))

        # 第一阶段：过滤需要处理的文件
        files_to_process = self._filter_files_to_process(files, skip_strategy)

        # 第二阶段：并行处理文件
        results = self._process_files_parallel(files_to_process, processor_func)

        # 第三阶段：完成批处理并生成报告
        return self._finalize_batch(results)

    def _initialize_batch(self, title: str, description: str, total_files: int) -> None:
        """
        初始化批处理

        Args:
            title: 批处理标题
            description: 批处理描述
            total_files: 总文件数
        """
        if self.report_generator:
            self.report_generator.start_batch(title=title, description=description)
        self.progress_display.start_batch(total_files)

    def _filter_files_to_process(
        self, files: List[Dict[str, str]], skip_strategy: SkipStrategy
    ) -> List[Dict[str, str]]:
        """
        过滤需要处理的文件（第一阶段）

        Args:
            files: 文件列表
            skip_strategy: 跳过策略

        Returns:
            需要处理的文件列表
        """
        files_to_process = []

        for file_info in files:
            input_file = file_info["input"]
            output_file = file_info["output"]

            should_skip, skip_reason = self._should_skip_file(
                input_file, output_file, skip_strategy
            )

            if should_skip:
                self._record_skipped_file(input_file, output_file, skip_reason)
            else:
                files_to_process.append(file_info)

        return files_to_process

    def _should_skip_file(
        self, input_file: str, output_file: str, skip_strategy: SkipStrategy
    ) -> tuple:
        """
        判断是否应该跳过文件

        Returns:
            (should_skip, skip_reason) 元组
        """
        if skip_strategy == SkipStrategy.NONE or not self.smart_skipper:
            return False, ""

        decision = self.smart_skipper.should_skip(input_file, output_file)

        if skip_strategy == SkipStrategy.FORCE and decision.output_exists:
            return True, "强制跳过（输出文件已存在）"

        if skip_strategy == SkipStrategy.SMART and decision.should_skip:
            return True, decision.reason

        return False, ""

    def _record_skipped_file(
        self, input_file: str, output_file: str, skip_reason: str
    ) -> None:
        """记录跳过的文件"""
        self.progress_display.finish_file(Path(input_file).name, success=True)

        if self.report_generator:
            result = ProcessResult(
                input_file=input_file,
                output_file=output_file,
                success=True,
                status="skipped",
                skip_reason=skip_reason,
            )
            self.report_generator.add_result(result)

    def _process_files_parallel(
        self, files: List[Dict[str, str]], processor_func: Callable[[str, str], Any]
    ) -> List[ProcessResult]:
        """
        并行处理文件（第二阶段）

        Args:
            files: 需要处理的文件列表
            processor_func: 处理函数

        Returns:
            处理结果列表
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_file = {
                executor.submit(self._process_with_retry, file_info, processor_func): file_info
                for file_info in files
            }

            # 收集结果
            for future in as_completed(future_to_file):
                file_info = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                    self.progress_display.finish_file(
                        Path(file_info["input"]).name, result.success
                    )
                except Exception as e:
                    error_result = self._create_error_result(file_info, str(e))
                    results.append(error_result)
                    self.progress_display.show_error(
                        Path(file_info["input"]).name, str(e)[:100]
                    )

        return results

    def _create_error_result(self, file_info: Dict[str, str], error: str) -> ProcessResult:
        """创建错误结果对象"""
        return ProcessResult(
            input_file=file_info["input"],
            output_file=file_info["output"],
            success=False,
            status="failed",
            error=f"未捕获的异常: {error}",
        )

    def _finalize_batch(self, results: List[ProcessResult]) -> BatchStatistics:
        """
        完成批处理并生成报告（第三阶段）

        Args:
            results: 处理结果列表

        Returns:
            批量处理统计信息
        """
        # 添加结果到报告生成器
        if self.report_generator:
            for result in results:
                self.report_generator.add_result(result)
            self.report_generator.finish_batch()

        # 获取统计信息
        stats = (
            self.report_generator._calculate_statistics()
            if self.report_generator
            else BatchStatistics()
        )

        # 显示摘要
        self.progress_display.show_summary(stats.total_duration, stats.total_size_mb)

        return stats

    def _process_with_retry(
        self, file_info: Dict[str, str], processor_func: Callable[[str, str], Any]
    ) -> ProcessResult:
        """
        带重试机制处理单个文件

        Args:
            file_info: 文件信息字典
            processor_func: 处理函数

        Returns:
            ProcessResult: 处理结果
        """
        input_file = file_info["input"]
        output_file = file_info["output"]

        start_time = datetime.now()

        # 如果启用重试
        if self.retry_handler:
            retry_result = self.retry_handler.execute_with_retry(
                processor_func, input_file, output_file
            )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            if retry_result.success:
                # 成功处理
                file_size = None
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file) / (1024 * 1024)

                return ProcessResult(
                    input_file=input_file,
                    output_file=output_file,
                    success=True,
                    status="completed",
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    file_size_mb=file_size,
                    retries=retry_result.attempts - 1,
                )
            else:
                # 处理失败
                return ProcessResult(
                    input_file=input_file,
                    output_file=output_file,
                    success=False,
                    status="failed",
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    error=str(retry_result.error) if retry_result.error else "未知错误",
                    retries=retry_result.attempts - 1,
                )

        # 不启用重试，直接处理
        else:
            try:
                processor_func(input_file, output_file)

                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                file_size = None
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file) / (1024 * 1024)

                return ProcessResult(
                    input_file=input_file,
                    output_file=output_file,
                    success=True,
                    status="completed",
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    file_size_mb=file_size,
                    retries=0,
                )

            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                return ProcessResult(
                    input_file=input_file,
                    output_file=output_file,
                    success=False,
                    status="failed",
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    error=str(e),
                    retries=0,
                )

    def generate_report(self, output_path: str, formats: Optional[List[str]] = None) -> Dict[str, str]:
        """
        生成批量处理报告

        Args:
            output_path: 输出文件路径（不含扩展名）
            formats: 报告格式列表

        Returns:
            Dict[str, str]: 生成的文件路径字典
        """
        if not self.report_generator:
            return {}

        if formats is None:
            formats = ["markdown", "json"]

        return self.report_generator.generate_report(output_path, formats)

    def get_stats(self) -> Dict[str, Any]:
        """
        获取处理器统计信息

        Returns:
            Dict: 统计信息字典
        """
        stats = {
            "max_workers": self.max_workers,
            "enable_retry": self.enable_retry,
            "enable_smart_skip": self.enable_smart_skip,
            "enable_report": self.enable_report,
        }

        if self.smart_skipper:
            stats["skipper_stats"] = self.smart_skipper.get_stats()

        return stats


# 使用示例
if __name__ == "__main__":
    print("=== 优化的批量处理器测试 ===\n")

    # 示例处理函数
    def example_processor(input_file: str, output_file: str) -> None:
        """
        示例处理函数（模拟视频转码）

        Args:
            input_file: 输入文件
            output_file: 输出文件
        """
        import time
        import random

        print(f"  处理: {Path(input_file).name} -> {Path(output_file).name}")

        # 模拟处理时间
        time.sleep(0.5)

        # 模拟 10% 的失败率
        if random.random() < 0.1:
            raise RuntimeError("模拟随机失败")

        # 模拟成功处理
        with open(output_file, "w") as f:
            f.write("模拟输出文件")

    # 创建处理器
    processor = OptimizedBatchProcessor(
        max_workers=4, enable_retry=True, enable_smart_skip=True, enable_report=True
    )

    # 准备文件列表
    test_files = []
    output_dir = Path("/tmp/batch_test")
    output_dir.mkdir(exist_ok=True)

    for i in range(1, 11):
        input_file = f"/tmp/input_{i}.mp4"
        output_file = str(output_dir / f"output_{i}.mkv")

        # 创建模拟输入文件
        Path(input_file).touch()

        test_files.append({"input": input_file, "output": output_file})

    # 执行批量处理
    print("开始批量处理...\n")
    stats = processor.process_batch(
        files=test_files,
        processor_func=example_processor,
        skip_strategy=SkipStrategy.SMART,
        batch_title="测试批量处理",
        batch_description="优化的批量处理器功能测试",
    )

    print("\n" + "=" * 60)
    print("处理完成！统计信息:")
    print("=" * 60)
    print(f"总计: {stats.total} 个文件")
    print(f"成功: {stats.success} 个")
    print(f"失败: {stats.failed} 个")
    print(f"跳过: {stats.skipped} 个")
    print(f"总耗时: {stats.total_duration:.2f} 秒")
    if stats.total_size_mb > 0:
        print(f"总大小: {stats.total_size_mb:.2f} MB")

    # 生成报告
    print("\n生成报告...")
    report_files = processor.generate_report("/tmp/batch_test_report", formats=["markdown", "json"])

    print("✅ 报告已生成:")
    for format_type, path in report_files.items():
        print(f"  - {format_type}: {path}")

    # 清理测试文件
    print("\n清理测试文件...")
    import shutil

    if output_dir.exists():
        shutil.rmtree(output_dir)
    for f in test_files:
        if Path(f["input"]).exists():
            Path(f["input"]).unlink()

    print("✅ 清理完成")
