#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
common.py — Shared IO and streaming helpers for post-PONI integration skills
common.py — PONI 后积分技能的共享 IO 与流式处理辅助工具
"""

from __future__ import annotations

import glob
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

import fabio
import h5py
import numpy as np

EIGER_4D_CHANNELS = ["LowThresholdData", "HighThresholdData", "DiffData"]
H5_DEAD_PIXEL_THRESHOLD = 4.25e9
SUPPORTED_EXTS = {".edf", ".tif", ".tiff", ".h5", ".hdf5", ".npy"}


@dataclass
class FrameRecord:
    """One lazily-loaded frame plus metadata. / 单帧数据及其元信息。"""

    data: np.ndarray
    dead_mask: Optional[np.ndarray]
    source_file: str
    frame_index: int
    frame_count: int
    dataset_path: Optional[str] = None
    channel: Optional[str] = None

    @property
    def stem(self) -> str:
        """Return a stable output stem. / 返回稳定的输出文件名前缀。"""
        base = Path(self.source_file).stem
        if self.channel:
            base = f"{base}_{self.channel}"
        if self.frame_count > 1:
            return f"{base}_fr{self.frame_index:04d}"
        return base


def emit_event(event: str, **payload: object) -> None:
    """Emit JSONL progress to stdout. / 向标准输出发出 JSONL 进度事件。"""
    record = {"event": event, **payload}
    print(json.dumps(record, ensure_ascii=False), flush=True)


def ensure_dir(path: str | Path) -> Path:
    """Create directory if needed. / 如有需要则创建目录。"""
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target


def expand_inputs(inputs: list[str], recursive: bool = True) -> list[str]:
    """Expand files, directories, and globs. / 展开文件、目录和通配模式。"""
    results: list[str] = []
    seen: set[str] = set()
    for item in inputs:
        if any(ch in item for ch in "*?[]"):
            matches = glob.glob(item, recursive=recursive)
            for match in sorted(matches):
                if os.path.isfile(match) and match not in seen:
                    ext = Path(match).suffix.lower()
                    if ext in SUPPORTED_EXTS:
                        results.append(match)
                        seen.add(match)
            continue

        path = Path(item)
        if path.is_dir():
            pattern = "**/*" if recursive else "*"
            for child in sorted(path.glob(pattern)):
                if child.is_file() and child.suffix.lower() in SUPPORTED_EXTS:
                    child_str = str(child)
                    if child_str not in seen:
                        results.append(child_str)
                        seen.add(child_str)
            continue

        if path.is_file():
            path_str = str(path)
            if path.suffix.lower() in SUPPORTED_EXTS and path_str not in seen:
                results.append(path_str)
                seen.add(path_str)
    return results


def discover_h5_datasets(file_path: str) -> list[str]:
    """List datasets inside HDF5 file. / 列出 HDF5 内部数据集。"""
    datasets: list[str] = []
    with h5py.File(file_path, "r") as handle:

        def _visitor(name: str, obj: object) -> None:
            if isinstance(obj, h5py.Dataset):
                datasets.append(name)

        handle.visititems(_visitor)
    return datasets


def pick_default_dataset(dataset_paths: list[str]) -> Optional[str]:
    """Pick most likely image dataset. / 选择最可能的图像数据集。"""
    if not dataset_paths:
        return None
    data_paths = [item for item in dataset_paths if item.endswith("/data") or item == "data"]
    if data_paths:
        data_paths.sort(key=lambda item: item.count("/"), reverse=True)
        return data_paths[0]
    return dataset_paths[0]


def _pick_channel_index(channel: Optional[str], n_channels: int) -> int:
    """Resolve channel string to integer index. / 将通道字符串解析为索引。"""
    if channel in EIGER_4D_CHANNELS and n_channels == len(EIGER_4D_CHANNELS):
        return EIGER_4D_CHANNELS.index(channel)
    if channel is None:
        return 0
    try:
        index = int(channel)
    except ValueError:
        index = 0
    return max(0, min(index, n_channels - 1))


def _to_frame(raw_2d: np.ndarray, is_uint32: bool) -> tuple[np.ndarray, np.ndarray]:
    """Convert raw slice to float32 plus dead-pixel mask. / 原始切片转 float32 与死像素掩膜。"""
    raw_np = np.asarray(raw_2d)
    if is_uint32:
        threshold = np.uint32(min(H5_DEAD_PIXEL_THRESHOLD, np.iinfo(np.uint32).max))
        dead_mask = raw_np > threshold
    else:
        dead_mask = raw_np > H5_DEAD_PIXEL_THRESHOLD
    data = raw_np.astype(np.float32)
    data[dead_mask] = -1.0
    return data, dead_mask


def iter_image_frames(
    file_path: str,
    h5_dataset: Optional[str] = None,
    h5_channel: Optional[str] = None,
) -> Iterator[FrameRecord]:
    """Yield image frames lazily. / 惰性逐帧产出图像数据。"""
    ext = Path(file_path).suffix.lower()
    if ext == ".npy":
        array = np.load(file_path)
        if array.ndim == 2:
            yield FrameRecord(array.astype(np.float32), None, file_path, 0, 1)
            return
        if array.ndim == 3:
            total = array.shape[0]
            for idx in range(total):
                yield FrameRecord(array[idx].astype(np.float32), None, file_path, idx, total)
            return
        raise ValueError(f"Unsupported NPY shape: {array.shape}")

    if ext in {".edf", ".tif", ".tiff"}:
        with fabio.open(file_path) as image:
            raw = np.asarray(image.data)
        if raw.ndim == 2:
            yield FrameRecord(raw.astype(np.float32), None, file_path, 0, 1)
            return
        total = raw.shape[0]
        for idx in range(total):
            yield FrameRecord(raw[idx].astype(np.float32), None, file_path, idx, total)
        return

    if ext not in {".h5", ".hdf5"}:
        raise ValueError(f"Unsupported input format: {file_path}")

    datasets = discover_h5_datasets(file_path)
    dataset_path = h5_dataset or pick_default_dataset(datasets)
    if dataset_path is None:
        raise ValueError(f"No dataset found in HDF5 file: {file_path}")

    with h5py.File(file_path, "r") as handle:
        dataset = handle[dataset_path]
        if not isinstance(dataset, h5py.Dataset):
            raise TypeError(f"HDF5 path is not a dataset: {dataset_path}")
        is_uint32 = dataset.dtype == np.uint32
        if dataset.ndim == 2:
            data, dead = _to_frame(dataset[()], is_uint32)
            yield FrameRecord(data, dead, file_path, 0, 1, dataset_path, h5_channel)
            return
        if dataset.ndim == 3:
            total = dataset.shape[0]
            for idx in range(total):
                data, dead = _to_frame(dataset[idx], is_uint32)
                yield FrameRecord(data, dead, file_path, idx, total, dataset_path, h5_channel)
            return
        if dataset.ndim == 4:
            total = dataset.shape[0]
            channel_index = _pick_channel_index(h5_channel, dataset.shape[1])
            channel_name = h5_channel or str(channel_index)
            for idx in range(total):
                data, dead = _to_frame(dataset[idx, channel_index, :, :], is_uint32)
                yield FrameRecord(data, dead, file_path, idx, total, dataset_path, channel_name)
            return
        raise ValueError(f"Unsupported HDF5 dataset shape: {dataset.shape}")


def load_aux_image(file_path: Optional[str]) -> Optional[np.ndarray]:
    """Load mask/dark/flat arrays. / 加载 mask、dark、flat 辅助数组。"""
    if not file_path:
        return None
    ext = Path(file_path).suffix.lower()
    if ext == ".npy":
        return np.load(file_path).astype(np.float32)
    if ext in {".h5", ".hdf5"}:
        datasets = discover_h5_datasets(file_path)
        dataset_path = pick_default_dataset(datasets)
        if dataset_path is None:
            raise ValueError(f"No dataset found in aux HDF5 file: {file_path}")
        with h5py.File(file_path, "r") as handle:
            dataset = handle[dataset_path]
            if not isinstance(dataset, h5py.Dataset):
                raise TypeError(f"HDF5 path is not a dataset: {dataset_path}")
            return np.asarray(dataset[()]).astype(np.float32)
    with fabio.open(file_path) as image:
        raw = np.asarray(image.data)
    if raw.ndim > 2:
        raw = raw[0]
    return raw.astype(np.float32)


def build_mask(
    data: np.ndarray,
    valid_min: Optional[float],
    valid_max: Optional[float],
    dead_mask: Optional[np.ndarray],
    custom_mask: Optional[np.ndarray],
) -> np.ndarray:
    """Combine threshold/dead/custom masks. / 组合阈值、死像素与自定义掩膜。"""
    mask = np.zeros(data.shape, dtype=bool)
    if valid_min is not None:
        mask |= data < valid_min
    if valid_max is not None:
        mask |= data > valid_max
    mask |= ~np.isfinite(data)
    mask |= data == -1.0
    if dead_mask is not None and dead_mask.shape == data.shape:
        mask |= dead_mask
    if custom_mask is not None:
        if custom_mask.shape != data.shape:
            raise ValueError(f"Custom mask shape mismatch: {custom_mask.shape} vs {data.shape}")
        mask |= custom_mask.astype(bool)
    return mask
