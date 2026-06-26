"""
批量处理报告生成器
生成详细的 Markdown 和 JSON 格式报告
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProcessResult:
    """单个文件的处理结果"""

    input_file: str
    output_file: str
    success: bool
    status: str = "pending"  # pending, running, completed, failed, skipped
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[float] = None  # 秒
    error: Optional[str] = None
    retries: int = 0
    file_size_mb: Optional[float] = None
    skip_reason: Optional[str] = None


@dataclass
class BatchStatistics:
    """批量处理统计信息"""

    total: int = 0
    success: int = 0
    failed: int = 0
    skipped: int = 0
    total_duration: float = 0.0
    total_size_mb: float = 0.0
    total_retries: int = 0
    avg_duration: float = 0.0
    avg_size_mb: float = 0.0
    throughput_mb_per_sec: float = 0.0
    files_per_sec: float = 0.0


class BatchReportGenerator:
    """批量处理报告生成器"""

    def __init__(self):
        """初始化报告生成器"""
        self.results: List[ProcessResult] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.title: str = "批量处理报告"
        self.description: str = ""

    def start_batch(self, title: str = "", description: str = "") -> None:
        """
        开始批量处理

        Args:
            title: 报告标题
            description: 报告描述
        """
        self.start_time = datetime.now()
        self.title = title or "批量处理报告"
        self.description = description
        self.results.clear()

    def add_result(self, result: ProcessResult) -> None:
        """
        添加处理结果

        Args:
            result: 处理结果对象
        """
        self.results.append(result)

    def finish_batch(self) -> None:
        """结束批量处理"""
        self.end_time = datetime.now()

    def generate_report(self, output_path: str, formats: Optional[List[str]] = None) -> Dict[str, str]:
        """
        生成详细的处理报告

        Args:
            output_path: 输出文件路径（不含扩展名）
            formats: 报告格式列表，可选：['markdown', 'json']

        Returns:
            Dict[str, str]: 生成的文件路径字典
        """
        if formats is None:
            formats = ["markdown", "json"]

        # 计算统计信息
        stats = self._calculate_statistics()

        generated_files = {}

        # 生成 Markdown 报告
        if "markdown" in formats:
            md_path = f"{output_path}.md"
            md_content = self._generate_markdown_report(stats)
            self._save_file(md_path, md_content)
            generated_files["markdown"] = md_path

        # 生成 JSON 报告
        if "json" in formats:
            json_path = f"{output_path}.json"
            json_content = self._generate_json_report(stats)
            self._save_file(json_path, json_content)
            generated_files["json"] = json_path

        return generated_files

    def _calculate_statistics(self) -> BatchStatistics:
        """
        计算统计信息

        Returns:
            BatchStatistics: 统计信息对象
        """
        stats = BatchStatistics()
        stats.total = len(self.results)

        for result in self.results:
            if result.status == "completed":
                stats.success += 1
            elif result.status == "failed":
                stats.failed += 1
            elif result.status == "skipped":
                stats.skipped += 1

            if result.duration:
                stats.total_duration += result.duration

            if result.file_size_mb:
                stats.total_size_mb += result.file_size_mb

            stats.total_retries += result.retries

        # 计算平均值
        if stats.success > 0:
            stats.avg_duration = stats.total_duration / stats.success
            stats.avg_size_mb = stats.total_size_mb / stats.success

        # 计算吞吐量
        if self.start_time and self.end_time:
            total_time = (self.end_time - self.start_time).total_seconds()
            if total_time > 0:
                stats.throughput_mb_per_sec = stats.total_size_mb / total_time
                stats.files_per_sec = stats.success / total_time

        return stats

    def _generate_markdown_report(self, stats: BatchStatistics) -> str:
        """
        生成 Markdown 格式报告

        Args:
            stats: 统计信息

        Returns:
            str: Markdown 内容
        """
        sections = []

        # 添加各个部分
        sections.append(self._generate_header())
        sections.append(self._generate_summary(stats))
        sections.append(self._generate_performance(stats))
        sections.append(self._generate_failed_files())
        sections.append(self._generate_skipped_files())
        sections.append(self._generate_success_files(stats))
        sections.append(self._generate_details_table())

        return "\n".join(sections)

    def _generate_header(self) -> str:
        """生成报告头部"""
        lines = []
        lines.append(f"# {self.title}\n")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        if self.description:
            lines.append(f"{self.description}\n")

        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
            lines.append(f"**处理时间**: {self._format_duration(duration)}\n")
            lines.append(f"**开始时间**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            lines.append(f"**结束时间**: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        lines.append("")
        return "\n".join(lines)

    def _generate_summary(self, stats: BatchStatistics) -> str:
        """生成统计摘要"""
        lines = []
        lines.append("## 📊 统计摘要\n")
        lines.append(f"- **总文件数**: {stats.total}")
        lines.append(f"- **成功**: {stats.success} ({stats.success/max(stats.total,1)*100:.1f}%)")
        lines.append(f"- **失败**: {stats.failed} ({stats.failed/max(stats.total,1)*100:.1f}%)")
        lines.append(f"- **跳过**: {stats.skipped} ({stats.skipped/max(stats.total,1)*100:.1f}%)")

        if stats.total_retries > 0:
            lines.append(f"- **总重试次数**: {stats.total_retries}")

        lines.append("")
        return "\n".join(lines)

    def _generate_performance(self, stats: BatchStatistics) -> str:
        """生成性能指标"""
        lines = []
        lines.append("## ⚡ 性能指标\n")
        lines.append(f"- **总耗时**: {self._format_duration(stats.total_duration)}")
        if stats.avg_duration > 0:
            lines.append(f"- **平均耗时**: {self._format_duration(stats.avg_duration)}/文件")

        lines.append(f"- **总输出大小**: {stats.total_size_mb:.2f} MB")
        if stats.avg_size_mb > 0:
            lines.append(f"- **平均大小**: {stats.avg_size_mb:.2f} MB/文件")

        if stats.throughput_mb_per_sec > 0:
            lines.append(f"- **吞吐量**: {stats.throughput_mb_per_sec:.2f} MB/秒")
        if stats.files_per_sec > 0:
            lines.append(f"- **处理速度**: {stats.files_per_sec:.2f} 文件/秒")

        lines.append("")
        return "\n".join(lines)

    def _generate_failed_files(self) -> str:
        """生成失败文件列表"""
        lines = []
        failed_results = [r for r in self.results if r.status == "failed"]

        if not failed_results:
            return ""

        lines.append("## ❌ 失败文件\n")
        for result in failed_results:
            lines.append(f"### {Path(result.input_file).name}\n")
            lines.append(f"**路径**: `{result.input_file}`\n")
            lines.append(f"**输出**: `{result.output_file}`\n")
            if result.error:
                lines.append(f"**错误**: {result.error[:200]}\n")
            if result.retries > 0:
                lines.append(f"**重试次数**: {result.retries}\n")
            if result.duration:
                lines.append(f"**耗时**: {self._format_duration(result.duration)}\n")
            lines.append("")

        return "\n".join(lines)

    def _generate_skipped_files(self) -> str:
        """生成跳过文件列表"""
        lines = []
        skipped_results = [r for r in self.results if r.status == "skipped"]

        if not skipped_results:
            return ""

        lines.append("## ⏭️ 跳过文件\n")
        for result in skipped_results:
            lines.append(f"- **{Path(result.input_file).name}**")
            if result.skip_reason:
                lines.append(f"  - 原因: {result.skip_reason}")
        lines.append("")

        return "\n".join(lines)

    def _generate_success_files(self, stats: BatchStatistics) -> str:
        """生成成功文件列表"""
        if stats.success > 20:
            return ""

        lines = []
        lines.append("## ✅ 成功文件\n")
        for result in self.results:
            if result.status == "completed":
                filename = Path(result.input_file).name
                duration_str = (
                    self._format_duration(result.duration) if result.duration else "N/A"
                )
                size_str = f"{result.file_size_mb:.2f} MB" if result.file_size_mb else "N/A"
                retries_str = f" (重试 {result.retries} 次)" if result.retries > 0 else ""
                lines.append(f"- **{filename}** - {duration_str} - {size_str}{retries_str}")
        lines.append("")

        return "\n".join(lines)

    def _generate_details_table(self) -> str:
        """生成详细结果表格"""
        lines = []
        lines.append("## 📋 详细结果\n")
        lines.append("| 文件名 | 状态 | 耗时 | 大小 | 重试 |")
        lines.append("|--------|------|------|------|------|")

        status_emoji_map = {
            "completed": "✅",
            "failed": "❌",
            "skipped": "⏭️",
            "pending": "⏳",
            "running": "🔄",
        }

        for result in self.results:
            filename = Path(result.input_file).name[:30]
            status_emoji = status_emoji_map.get(result.status, "❓")
            duration_str = self._format_duration(result.duration) if result.duration else "N/A"
            size_str = f"{result.file_size_mb:.1f}M" if result.file_size_mb else "N/A"
            retries_str = str(result.retries) if result.retries > 0 else "-"

            lines.append(
                f"| {filename} | {status_emoji} {result.status} | {duration_str} | {size_str} | {retries_str} |"
            )

        lines.append("")
        return "\n".join(lines)

    def _generate_json_report(self, stats: BatchStatistics) -> str:
        """
        生成 JSON 格式报告

        Args:
            stats: 统计信息

        Returns:
            str: JSON 内容
        """
        report = {
            "title": self.title,
            "description": self.description,
            "generated_at": datetime.now().isoformat(),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "statistics": {
                "total": stats.total,
                "success": stats.success,
                "failed": stats.failed,
                "skipped": stats.skipped,
                "success_rate": stats.success / max(stats.total, 1) * 100,
                "total_duration": stats.total_duration,
                "average_duration": stats.avg_duration,
                "total_size_mb": stats.total_size_mb,
                "average_size_mb": stats.avg_size_mb,
                "total_retries": stats.total_retries,
                "throughput_mb_per_sec": stats.throughput_mb_per_sec,
                "files_per_sec": stats.files_per_sec,
            },
            "results": [],
        }

        # 添加详细结果
        for result in self.results:
            result_dict = {
                "input_file": result.input_file,
                "output_file": result.output_file,
                "status": result.status,
                "success": result.success,
                "duration": result.duration,
                "file_size_mb": result.file_size_mb,
                "retries": result.retries,
                "error": result.error,
                "skip_reason": result.skip_reason,
                "start_time": result.start_time.isoformat() if result.start_time else None,
                "end_time": result.end_time.isoformat() if result.end_time else None,
            }
            report["results"].append(result_dict)

        return json.dumps(report, indent=2, ensure_ascii=False)

    def _save_file(self, path: str, content: str) -> None:
        """
        保存文件

        Args:
            path: 文件路径
            content: 文件内容
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def _format_duration(self, seconds: Optional[float]) -> str:
        """
        格式化持续时间

        Args:
            seconds: 秒数

        Returns:
            str: 格式化的时间字符串
        """
        if seconds is None or seconds < 0:
            return "N/A"

        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}分{secs}秒"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}小时{minutes}分"


# 使用示例
if __name__ == "__main__":
    print("=== 批量处理报告生成器测试 ===\n")

    # 创建报告生成器
    reporter = BatchReportGenerator()

    # 开始批量处理
    reporter.start_batch(title="视频转码批量处理", description="将 MP4 格式转换为 MKV 格式")

    # 模拟添加处理结果
    from datetime import datetime

    results = [
        ProcessResult(
            input_file="/path/to/video1.mp4",
            output_file="/path/to/video1.mkv",
            success=True,
            status="completed",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=45.2,
            file_size_mb=125.5,
            retries=0,
        ),
        ProcessResult(
            input_file="/path/to/video2.mp4",
            output_file="/path/to/video2.mkv",
            success=True,
            status="completed",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=52.8,
            file_size_mb=198.3,
            retries=1,
        ),
        ProcessResult(
            input_file="/path/to/video3.mp4",
            output_file="/path/to/video3.mkv",
            success=False,
            status="failed",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.5,
            error="编码失败：码率超出范围",
            retries=3,
        ),
        ProcessResult(
            input_file="/path/to/video4.mp4",
            output_file="/path/to/video4.mkv",
            success=True,
            status="skipped",
            skip_reason="输出文件已是最新",
            duration=0,
            file_size_mb=0,
        ),
    ]

    for result in results:
        reporter.add_result(result)

    # 结束批量处理
    reporter.finish_batch()

    # 生成报告
    print("生成报告到 /tmp/batch_report...")
    generated_files = reporter.generate_report("/tmp/batch_report", formats=["markdown", "json"])

    print(f"\n✅ 已生成报告文件:")
    for format_type, path in generated_files.items():
        print(f"  - {format_type}: {path}")

    # 打印 Markdown 报告预览
    print("\n" + "=" * 60)
    print("Markdown 报告预览:")
    print("=" * 60)
    stats = reporter._calculate_statistics()
    markdown_preview = reporter._generate_markdown_report(stats)
    print(markdown_preview[:1000] + "..." if len(markdown_preview) > 1000 else markdown_preview)
