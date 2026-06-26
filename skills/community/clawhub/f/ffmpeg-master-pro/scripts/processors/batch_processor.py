"""
批量处理器
支持多线程并行批量处理视频文件
"""

import os
import shlex
import subprocess
import threading
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BatchTask:
    """批量任务数据类"""

    input_file: str
    output_file: str
    command: str
    task_id: int = 0
    status: str = "pending"  # pending, running, completed, failed
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    output_size_mb: Optional[float] = None


@dataclass
class BatchConfig:
    """批量处理配置"""

    max_workers: int = 4  # 最大并行任务数
    continue_on_error: bool = True  # 出错后是否继续
    output_dir: Optional[str] = None  # 输出目录
    overwrite: bool = False  # 是否覆盖已存在的文件
    log_file: Optional[str] = None  # 日志文件路径
    progress_callback: Optional[Callable[[BatchTask], None]] = None  # 进度回调
    show_progress: bool = True  # 是否显示进度条


class BatchProcessor:
    """批量处理器"""

    def __init__(self, config: BatchConfig):
        """
        初始化批量处理器

        Args:
            config: 批量处理配置
        """
        self.config = config
        self.tasks: List[BatchTask] = []
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.total_size_mb = 0
        self.lock = threading.Lock()

        # 导入进度显示器
        self.batch_progress_display = None
        if config.show_progress:
            try:
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
                from progress import BatchProgressDisplay

                self.batch_progress_display = BatchProgressDisplay()
            except ImportError:
                pass

    def discover_videos(self, input_dir: str, extensions: List[str] = None) -> List[str]:
        """
        发现目录中的视频文件

        Args:
            input_dir: 输入目录
            extensions: 视频文件扩展名列表

        Returns:
            视频文件路径列表
        """
        if extensions is None:
            extensions = [
                ".mp4",
                ".mkv",
                ".avi",
                ".mov",
                ".flv",
                ".wmv",
                ".webm",
                ".m4v",
                ".mpg",
                ".mpeg",
            ]

        video_files = []
        input_path = Path(input_dir)

        if not input_path.exists():
            raise Exception(f"目录不存在: {input_dir}")

        for ext in extensions:
            video_files.extend(input_path.rglob(f"*{ext}"))

        return [str(f) for f in video_files]

    def create_tasks(
        self,
        input_files: List[str],
        command_generator: Callable[[str, int], str],
        output_generator: Optional[Callable[[str], str]] = None,
    ) -> List[BatchTask]:
        """
        创建批量任务

        Args:
            input_files: 输入文件列表
            command_generator: 命令生成函数，接收 (input_file, task_id)，返回 FFmpeg 命令
            output_generator: 输出文件路径生成函数，接收 input_file，返回 output_file

        Returns:
            任务列表
        """
        tasks = []

        for i, input_file in enumerate(input_files):
            output_file = (
                output_generator(input_file)
                if output_generator
                else self._default_output_generator(input_file)
            )
            command = command_generator(input_file, i)

            task = BatchTask(
                input_file=input_file, output_file=output_file, command=command, task_id=i
            )
            tasks.append(task)

        self.tasks = tasks
        return tasks

    def _default_output_generator(self, input_file: str) -> str:
        """默认输出文件生成器"""
        input_path = Path(input_file)

        if self.config.output_dir:
            output_dir = Path(self.config.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            return str(output_dir / input_path.name)
        else:
            # 在原文件名后添加 _output
            return str(input_path.with_stem(f"{input_path.stem}_output"))

    def execute(self) -> Dict:
        """
        执行批量处理

        Returns:
            处理结果统计
        """
        if not self.tasks:
            return {"total": 0, "completed": 0, "failed": 0, "tasks": []}

        # 开始批量进度显示
        if self.batch_progress_display:
            self.batch_progress_display.start_batch(len(self.tasks))

        start_time = datetime.now()

        # 创建线程池
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            # 提交所有任务
            future_to_task = {
                executor.submit(self._execute_task, task): task for task in self.tasks
            }

            # 等待任务完成
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    future.result()
                except Exception as e:
                    with self.lock:
                        task.status = "failed"
                        task.error_message = str(e)
                        self.failed_tasks += 1

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # 生成结果报告
        results = {
            "total": len(self.tasks),
            "completed": self.completed_tasks,
            "failed": self.failed_tasks,
            "duration": duration,
            "total_size_mb": self.total_size_mb,
            "tasks": [
                {
                    "input": task.input_file,
                    "output": task.output_file,
                    "status": task.status,
                    "error": task.error_message,
                    "duration": (
                        (task.end_time - task.start_time).total_seconds()
                        if task.start_time and task.end_time
                        else None
                    ),
                }
                for task in self.tasks
            ],
        }

        # 显示摘要
        if self.batch_progress_display:
            self.batch_progress_display.show_summary(duration, self.total_size_mb)

        # 写入日志
        if self.config.log_file:
            self._write_log(results)

        return results

    def _execute_task(self, task: BatchTask) -> None:
        """
        执行单个任务

        Args:
            task: 任务对象
        """
        with self.lock:
            task.status = "running"
            task.start_time = datetime.now()

        # 调用进度回调
        if self.config.progress_callback:
            self.config.progress_callback(task)

        try:
            # 执行 FFmpeg 命令
            result = subprocess.run(
                shlex.split(task.command), shell=False, capture_output=True, text=True, check=True
            )

            # 获取输出文件大小
            if Path(task.output_file).exists():
                task.output_size_mb = Path(task.output_file).stat().st_size / (1024 * 1024)

            with self.lock:
                task.status = "completed"
                task.end_time = datetime.now()
                self.completed_tasks += 1
                self.total_size_mb += task.output_size_mb or 0

            # 更新批量进度显示
            if self.batch_progress_display:
                filename = os.path.basename(task.input_file)
                self.batch_progress_display.finish_file(filename, success=True)

        except subprocess.CalledProcessError as e:
            with self.lock:
                task.status = "failed"
                task.error_message = e.stderr
                task.end_time = datetime.now()
                self.failed_tasks += 1

            # 更新批量进度显示（失败）
            if self.batch_progress_display:
                filename = os.path.basename(task.input_file)
                self.batch_progress_display.show_error(filename, str(e.stderr)[:100])

            if not self.config.continue_on_error:
                raise Exception(f"任务失败（停止批量处理）: {e.stderr}")

        except Exception as e:
            with self.lock:
                task.status = "failed"
                task.error_message = str(e)
                task.end_time = datetime.now()
                self.failed_tasks += 1

            # 更新批量进度显示（失败）
            if self.batch_progress_display:
                filename = os.path.basename(task.input_file)
                self.batch_progress_display.show_error(filename, str(e)[:100])

            if not self.config.continue_on_error:
                raise

        finally:
            # 调用进度回调
            if self.config.progress_callback:
                self.config.progress_callback(task)

    def _write_log(self, results: Dict) -> None:
        """写入处理日志"""
        if self.config.log_file is None:
            return

        log_path = Path(self.config.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(log_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"批量处理日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"总任务数: {results['total']}\n")
            f.write(f"成功: {results['completed']}\n")
            f.write(f"失败: {results['failed']}\n")
            f.write(f"总耗时: {results['duration']:.2f} 秒\n")
            f.write(f"总输出大小: {results['total_size_mb']:.2f} MB\n\n")

            f.write("-" * 80 + "\n")
            f.write("任务详情:\n")
            f.write("-" * 80 + "\n")

            for task in results["tasks"]:
                f.write(f"\n文件: {task['input']}\n")
                f.write(f"输出: {task['output']}\n")
                f.write(f"状态: {task['status']}\n")
                if task["error"]:
                    f.write(f"错误: {task['error']}\n")
                if task["duration"]:
                    f.write(f"耗时: {task['duration']:.2f} 秒\n")

    def get_progress(self) -> Dict:
        """获取当前进度"""
        with self.lock:
            return {
                "total": len(self.tasks),
                "completed": self.completed_tasks,
                "failed": self.failed_tasks,
                "running": sum(1 for t in self.tasks if t.status == "running"),
                "pending": sum(1 for t in self.tasks if t.status == "pending"),
                "progress_percent": (
                    (self.completed_tasks / len(self.tasks) * 100) if self.tasks else 0
                ),
            }

    def cancel(self) -> None:
        """取消所有正在运行的任务"""
        # 这是一个简化实现，实际需要更复杂的取消机制
        with self.lock:
            for task in self.tasks:
                if task.status == "running":
                    task.status = "cancelled"


# 使用示例
if __name__ == "__main__":
    print("=== 批量处理器测试 ===\n")

    # 示例：批量转码
    print("示例：批量转码 MP4 到 MKV")

    def command_generator(input_file: str, task_id: int) -> str:
        """命令生成器"""
        output_file = f"output_{task_id}.mkv"
        return f'ffmpeg -i "{input_file}" -c copy "{output_file}"'

    # 创建配置
    config = BatchConfig(
        max_workers=4, continue_on_error=True, output_dir="./output", log_file="./batch_log.txt"
    )

    # 创建处理器
    processor = BatchProcessor(config)

    # 发现视频文件
    print("发现视频文件...")
    # video_files = processor.discover_videos("./input")
    # print(f"找到 {len(video_files)} 个视频文件")

    # 创建任务
    # tasks = processor.create_tasks(video_files, command_generator)

    # 执行批量处理
    # results = processor.execute()

    # 打印结果
    # print(f"\n处理完成!")
    # print(f"总计: {results['total']} 个文件")
    # print(f"成功: {results['completed']}")
    # print(f"失败: {results['failed']}")
    # print(f"耗时: {results['duration']:.2f} 秒")
