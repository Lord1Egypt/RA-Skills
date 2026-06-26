#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
task_pipeline.py — Batch task model and streaming pipeline engine
批任务模型与流式管线引擎

Memory-friendly design:
  - TaskItem stores paths/config, NOT large arrays
  - PipelineEngine yields results one at a time (generator-based)
  - Data is loaded lazily and released after each task completes
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Optional, List, Dict, Any, Callable, Generator, Tuple

import numpy as np

from .curve_data import Curve1D, CurveMetadata, ProcessMode
from .curve_processor import CurveProcessor, CurveProcessorConfig


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TaskItem:
    """
    Describes a single processing task without holding large arrays.
    描述一个处理任务，不持有大数组。
    """

    task_id: str = ""
    source_path: str = ""
    background_path: Optional[str] = None
    transmission: Optional[float] = None
    process_mode: ProcessMode = ProcessMode.MORPH_1D
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Curve1D] = None
    error_msg: Optional[str] = None
    x_column: int = 0
    y_column: int = 1
    skip_header: int = 0
    delimiter: Optional[str] = None
    comment: str = "#"
    extra: Dict[str, Any] = field(default_factory=dict)

    _counter: ClassVar[int] = 0

    def __post_init__(self):
        if not self.task_id:
            TaskItem._counter += 1
            self.task_id = f"task_{TaskItem._counter:06d}"


@dataclass
class TaskResult:
    """Lightweight result for one completed task."""

    task_id: str
    source_path: str
    status: TaskStatus
    curve: Optional[Curve1D] = None
    error_msg: Optional[str] = None
    elapsed_seconds: float = 0.0


@dataclass
class PipelineContext:
    """
    Global settings for the pipeline engine.
    管线引擎的全局设置。
    """

    processor_config: CurveProcessorConfig = field(default_factory=CurveProcessorConfig)
    output_dir: str = ""
    output_format: str = "xy"
    save_results: bool = False
    output_mode: str = "per_file"
    merged_output_path: str = ""
    export_raw: bool = True
    export_bg: bool = False
    export_sub: bool = True
    max_memory_bytes: int = 0
    on_progress: Optional[Callable] = None
    on_task_complete: Optional[Callable] = None
    stop_on_error: bool = False


class PipelineEngine:
    """
    Generator-based streaming pipeline that processes TaskItems one at a time.
    基于生成器的流式管线，逐个处理 TaskItem。

    Memory-friendly: only one task's data is in memory at a time.
    Results are yielded as TaskResult objects.
    """

    def __init__(self, context: Optional[PipelineContext] = None):
        self.ctx = context or PipelineContext()
        self._results: List[TaskResult] = []

    def _make_processor(self, task: TaskItem) -> CurveProcessor:
        cfg = self.ctx.processor_config
        overrides: Dict[str, Any] = {}
        if task.transmission is not None:
            overrides["transmission"] = task.transmission
        if overrides:
            import copy

            new_cfg = copy.deepcopy(cfg)
            for k, v in overrides.items():
                if hasattr(new_cfg, k):
                    setattr(new_cfg, k, v)
            new_cfg.process_mode = task.process_mode
            return CurveProcessor(new_cfg)
        cfg_copy = CurveProcessorConfig(**{k: v for k, v in cfg.__dict__.items()})
        cfg_copy.process_mode = task.process_mode
        return CurveProcessor(cfg_copy)

    def _load_input(self, task: TaskItem):
        """Load input as 1D curve file. / 将输入加载为一维曲线文件。"""
        from .curve_io import load_curve_file

        return load_curve_file(
            task.source_path,
            x_column=task.x_column,
            y_column=task.y_column,
            skip_header=task.skip_header,
            comment=task.comment,
            delimiter=task.delimiter,
        )

    def _save_result(self, task: TaskItem, curve: Curve1D) -> Optional[str]:
        if not self.ctx.save_results or not self.ctx.output_dir:
            return None
        from .curve_io import save_curve_file

        os.makedirs(self.ctx.output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(task.source_path))[0]
        suffix = str(task.extra.get("output_suffix", "")).strip()
        if suffix:
            base = f"{base}_{suffix}"
        ext_map = {
            "xy": ".xy",
            "csv": ".csv",
            "txt": ".txt",
            "gr": ".gr",
            "npy": ".npy",
            "h5": ".h5",
        }
        ext = ext_map.get(self.ctx.output_format, f".{self.ctx.output_format}")
        saved_paths = []

        # Save raw curve / 保存原始曲线
        if self.ctx.export_raw:
            raw_path = os.path.join(self.ctx.output_dir, f"{base}_raw{ext}")
            if save_curve_file(curve, raw_path, fmt=self.ctx.output_format, data_type="raw"):
                saved_paths.append(raw_path)

        # Save background / 保存背景
        if self.ctx.export_bg and curve.background is not None:
            bg_path = os.path.join(self.ctx.output_dir, f"{base}_bg{ext}")
            if save_curve_file(curve, bg_path, fmt=self.ctx.output_format, data_type="background"):
                saved_paths.append(bg_path)

        # Save subtracted / 保存扣除后曲线
        if self.ctx.export_sub and curve.subtracted is not None:
            sub_path = os.path.join(self.ctx.output_dir, f"{base}_sub{ext}")
            if save_curve_file(curve, sub_path, fmt=self.ctx.output_format, data_type="subtracted"):
                saved_paths.append(sub_path)

        # Fallback for cases where no exports were enabled / 无导出项时的降级处理
        if not saved_paths:
            default_path = os.path.join(self.ctx.output_dir, f"{base}{ext}")
            save_curve_file(curve, default_path, fmt=self.ctx.output_format, data_type="raw")
            saved_paths.append(default_path)

        return "; ".join(saved_paths) if saved_paths else None

    def _process_one(self, task: TaskItem) -> TaskResult:
        t0 = time.monotonic()
        task.status = TaskStatus.RUNNING

        if self.ctx.on_progress:
            self.ctx.on_progress(0.0, task.task_id, "running")

        if not os.path.isfile(task.source_path):
            task.status = TaskStatus.FAILED
            task.error_msg = f"File not found: {task.source_path}"
            return TaskResult(
                task_id=task.task_id,
                source_path=task.source_path,
                status=TaskStatus.FAILED,
                error_msg=task.error_msg,
                elapsed_seconds=time.monotonic() - t0,
            )

        try:
            processor = self._make_processor(task)
            if task.process_mode == ProcessMode.T_BG_SUBTRACT:
                if not task.background_path:
                    raise ValueError("T_BG_SUBTRACT requires background_path")
                if not os.path.isfile(task.background_path):
                    raise FileNotFoundError(f"Background file not found: {task.background_path}")
                if task.transmission is None:
                    raise ValueError("T_BG_SUBTRACT requires transmission")

                sample_curve = self._load_input(task)
                background_task = TaskItem(
                    source_path=task.background_path,
                    x_column=task.x_column,
                    y_column=task.y_column,
                    skip_header=task.skip_header,
                    delimiter=task.delimiter,
                    comment=task.comment,
                )
                background_curve = self._load_input(background_task)

                if sample_curve is None:
                    task.status = TaskStatus.FAILED
                    task.error_msg = f"Failed to load: {task.source_path}"
                    return TaskResult(
                        task_id=task.task_id,
                        source_path=task.source_path,
                        status=TaskStatus.FAILED,
                        error_msg=task.error_msg,
                        elapsed_seconds=time.monotonic() - t0,
                    )

                if background_curve is None:
                    task.status = TaskStatus.FAILED
                    task.error_msg = f"Failed to load background: {task.background_path}"
                    return TaskResult(
                        task_id=task.task_id,
                        source_path=task.source_path,
                        status=TaskStatus.FAILED,
                        error_msg=task.error_msg,
                        elapsed_seconds=time.monotonic() - t0,
                    )

                # 若 x 轴不一致，则将背景插值到样品 x 轴。
                # If x axes differ, interpolate background onto sample x axis.
                if sample_curve.n_points != background_curve.n_points or not np.allclose(
                    sample_curve.x,
                    background_curve.x,
                    rtol=1e-7,
                    atol=1e-12,
                ):
                    interp_y = np.interp(sample_curve.x, background_curve.x, background_curve.y)
                    background_curve = Curve1D(
                        x=sample_curve.x.copy(),
                        y=interp_y,
                        metadata=CurveMetadata(
                            source_file=background_curve.metadata.source_file,
                            source_type=background_curve.metadata.source_type,
                            x_label=sample_curve.metadata.x_label,
                            y_label=background_curve.metadata.y_label,
                            x_unit=sample_curve.metadata.x_unit,
                            process_mode=background_curve.metadata.process_mode,
                            extra={
                                **background_curve.metadata.extra,
                                "interpolated_to": task.source_path,
                            },
                        ),
                    )

                result_curve = processor.process_t_bg_subtract(
                    sample_curve,
                    background_curve,
                    task.transmission,
                )
            else:
                input_data = self._load_input(task)

                if input_data is None:
                    task.status = TaskStatus.FAILED
                    task.error_msg = f"Failed to load: {task.source_path}"
                    return TaskResult(
                        task_id=task.task_id,
                        source_path=task.source_path,
                        status=TaskStatus.FAILED,
                        error_msg=task.error_msg,
                        elapsed_seconds=time.monotonic() - t0,
                    )

                result_curve = processor.process(input_data)

            if result_curve is None:
                task.status = TaskStatus.FAILED
                task.error_msg = "Processing returned None"
                return TaskResult(
                    task_id=task.task_id,
                    source_path=task.source_path,
                    status=TaskStatus.FAILED,
                    error_msg=task.error_msg,
                    elapsed_seconds=time.monotonic() - t0,
                )

            if not result_curve.metadata.source_file:
                result_curve.metadata.source_file = task.source_path

            saved_path = self._save_result(task, result_curve)
            if saved_path and result_curve.metadata.extra is not None:
                result_curve.metadata.extra["saved_to"] = saved_path

            task.status = TaskStatus.COMPLETED
            task.result = result_curve
            elapsed = time.monotonic() - t0

            if self.ctx.on_progress:
                self.ctx.on_progress(1.0, task.task_id, "completed")

            return TaskResult(
                task_id=task.task_id,
                source_path=task.source_path,
                status=TaskStatus.COMPLETED,
                curve=result_curve,
                elapsed_seconds=elapsed,
            )

        except Exception as exc:
            task.status = TaskStatus.FAILED
            task.error_msg = str(exc)
            elapsed = time.monotonic() - t0
            return TaskResult(
                task_id=task.task_id,
                source_path=task.source_path,
                status=TaskStatus.FAILED,
                error_msg=str(exc),
                elapsed_seconds=elapsed,
            )

    def run(self, tasks: List[TaskItem]) -> Generator[TaskResult, None, None]:
        """
        Execute tasks one at a time, yielding results as they complete.
        逐个执行任务，完成即产出结果。

        Memory-friendly: each task's data is loaded, processed, and
        optionally saved before the next task begins.
        """
        total = len(tasks)
        for i, task in enumerate(tasks):
            pct = i / total if total > 0 else 0.0
            if self.ctx.on_progress:
                self.ctx.on_progress(pct, task.task_id, "starting")

            result = self._process_one(task)
            self._results.append(result)

            if self.ctx.on_task_complete:
                self.ctx.on_task_complete(result)

            yield result

            if self.ctx.stop_on_error and result.status == TaskStatus.FAILED:
                for remaining_task in tasks[i + 1 :]:
                    remaining_task.status = TaskStatus.SKIPPED
                    skip_result = TaskResult(
                        task_id=remaining_task.task_id,
                        source_path=remaining_task.source_path,
                        status=TaskStatus.SKIPPED,
                    )
                    self._results.append(skip_result)
                    yield skip_result
                break

    def run_all(self, tasks: List[TaskItem]) -> List[TaskResult]:
        """
        Run all tasks and collect results into a list.
        WARNING: This loads all results into memory.
        For large batches, use ``run()`` instead.
        """
        return list(self.run(tasks))

    @staticmethod
    def build_tasks(
        paths: List[str],
        process_mode: Optional[ProcessMode] = None,
        background_path: Optional[str] = None,
        transmission: Optional[float] = None,
        transmissions: Optional[Dict[str, float]] = None,
        x_column: int = 0,
        y_column: int = 1,
        skip_header: int = 0,
        delimiter: Optional[str] = None,
        comment: str = "#",
    ) -> List[TaskItem]:
        """
        Build TaskItem list from file paths.
        从文件路径构建 TaskItem 列表。
        """
        from .curve_io import is_1d_curve_file

        tasks = []
        for p in paths:
            mode = process_mode
            if mode is None:
                if is_1d_curve_file(p):
                    mode = ProcessMode.MORPH_1D
                else:
                    mode = ProcessMode.MORPH_1D

            tasks.append(
                TaskItem(
                    source_path=p,
                    background_path=background_path,
                    transmission=(
                        transmissions.get(p)
                        if transmissions is not None and p in transmissions
                        else transmission
                    ),
                    process_mode=mode,
                    x_column=x_column,
                    y_column=y_column,
                    skip_header=skip_header,
                    delimiter=delimiter,
                    comment=comment,
                )
            )
        return tasks

    def summary(self) -> Dict[str, Any]:
        """Get pipeline execution summary."""
        completed = sum(1 for r in self._results if r.status == TaskStatus.COMPLETED)
        failed = sum(1 for r in self._results if r.status == TaskStatus.FAILED)
        skipped = sum(1 for r in self._results if r.status == TaskStatus.SKIPPED)
        pending = sum(1 for r in self._results if r.status == TaskStatus.PENDING)
        total = len(self._results)
        total_time = sum(r.elapsed_seconds for r in self._results)

        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "skipped": skipped,
            "pending": pending,
            "total_seconds": round(total_time, 3),
            "avg_seconds": round(total_time / total, 3) if total > 0 else 0.0,
        }
