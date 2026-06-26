#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
image_io.py — Image file I/O
图像文件输入输出

Adapted from substract_bg_gui.py for standalone use.
从 substract_bg_gui.py 适配，支持 TIFF/EDF/H5 格式。
"""

from __future__ import annotations

import os
import re
import json
import tempfile
import uuid
from contextlib import nullcontext
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

import h5py
import numpy as np

try:
    import fabio

    HAS_FABIO = True
except ImportError:
    fabio = None
    HAS_FABIO = False


TIFF_EXTS = {".tif", ".tiff", ".edf"}
H5_EXTS = {".h5", ".hdf5"}
H5_TRANSMISSION_KEYS: Tuple[str, ...] = (
    "transmission",
    "Transmission",
    "T",
    "trans",
    "Trans",
    "transmittance",
    "Transmittance",
    "t_percent",
    "T_percent",
)


def load_image_file(path: str) -> Tuple[Optional[np.ndarray], Optional[dict]]:
    """
    Load a 2D image file (TIFF/EDF) using fabio.
    使用 fabio 加载 2D 图像文件。

    Parameters
    ----------
    path : str
        Path to the image file / 图像文件路径

    Returns
    -------
    data : np.ndarray or None
        Image data as float32 for memory efficiency / 图像数据（为节省内存使用float32）
    header : dict or None
        Image header metadata / 图像头信息
    """
    if not HAS_FABIO:
        raise ImportError("fabio is required for image loading. Install with: pip install fabio")

    try:
        fabio_module: Any = fabio
        with fabio_module.open(path) as img:
            # Use float32 to save 50% memory compared to float64
            # 使用float32节省50%内存
            return img.data.astype(np.float32), dict(img.header)
    except Exception:
        return None, None


def load_h5_stack(path: str) -> Optional[Dict[str, Any]]:
    """
    Load an HDF5 file and extract the best image dataset.
    加载 HDF5 文件并提取最佳图像数据集。

    Supports shapes:
      (H, W)         -> normalized to (1, H, W)
      (N, H, W)      -> 3D stack
      (N, C, H, W)   -> 4D Eiger-style

    Parameters
    ----------
    path : str
        Path to HDF5 file / HDF5 文件路径

    Returns
    -------
    dict with keys:
        data : np.ndarray (float64)
        ndim : int (3 or 4)
        shape : tuple
        n_frames : int
        n_channels : int or None
        dataset_path : str
        transmissions : np.ndarray or None
        filename : str
    """
    candidates: Dict[str, Dict[str, Any]] = {}
    try:
        with h5py.File(path, "r") as fh:

            def _visitor(name: str, obj) -> None:
                if isinstance(obj, h5py.Dataset) and obj.ndim >= 2:
                    candidates[name] = {
                        "shape": obj.shape,
                        "ndim": obj.ndim,
                        "size": obj.size,
                    }

            fh.visititems(_visitor)
    except Exception:
        return None

    if not candidates:
        return None

    best_path = max(candidates, key=lambda k: (candidates[k]["ndim"], candidates[k]["size"]))

    with h5py.File(path, "r") as fh:
        dataset: Any = fh[best_path]
        if not isinstance(dataset, h5py.Dataset):
            return None
        # Use float32 to save 50% memory / 使用float32节省50%内存
        raw = np.asarray(dataset[...], dtype=np.float32)

    ndim = raw.ndim
    if ndim == 2:
        raw = raw[np.newaxis, :]
        ndim = 3

    if ndim == 3:
        n_frames, n_channels = raw.shape[0], None
    elif ndim == 4:
        n_frames, n_channels = raw.shape[0], raw.shape[1]
    else:
        return None

    return {
        "data": raw,
        "ndim": ndim,
        "shape": raw.shape,
        "n_frames": n_frames,
        "n_channels": n_channels,
        "dataset_path": best_path,
        "transmissions": find_h5_transmissions(path),
        "filename": os.path.basename(path),
    }


def find_h5_transmissions(h5_path: str) -> Optional[np.ndarray]:
    """
    Search an HDF5 file for per-frame transmission values.
    在 HDF5 文件中搜索逐帧透过率数据。

    Parameters
    ----------
    h5_path : str
        Path to HDF5 file / HDF5 文件路径

    Returns
    -------
    np.ndarray or None
        Transmission values / 透过率值数组
    """
    keys_lower = {k.lower() for k in H5_TRANSMISSION_KEYS}
    try:
        with h5py.File(h5_path, "r") as fh:
            for key in H5_TRANSMISSION_KEYS:
                if key in fh:
                    dataset: Any = fh[key]
                    if isinstance(dataset, h5py.Dataset):
                        return np.asarray(dataset[...], dtype=np.float64)

            found: List[Tuple[str, np.ndarray]] = []

            def _visit(name: str, obj) -> None:
                leaf = name.split("/")[-1].lower()
                if isinstance(obj, h5py.Dataset) and leaf in keys_lower:
                    found.append((name, np.asarray(obj[...], dtype=np.float64)))

            fh.visititems(_visit)
            if found:
                return found[0][1]

            for key in H5_TRANSMISSION_KEYS:
                if key in fh.attrs:
                    return np.atleast_1d(np.asarray(fh.attrs[key], dtype=np.float64))

    except Exception:
        pass
    return None


def save_image(
    data: np.ndarray,
    path: str,
    format: str = "auto",
    header: Optional[dict] = None,
) -> bool:
    """
    Save image data to file.
    保存图像数据到文件。

    Parameters
    ----------
    data : np.ndarray
        Image data / 图像数据
    path : str
        Output path / 输出路径
    format : str
        'auto', 'edf', 'tif', 'tiff' / 格式
    header : dict, optional
        Header metadata for EDF files / EDF 文件头信息

    Returns
    -------
    bool
        Success / 是否成功
    """
    if not HAS_FABIO:
        raise ImportError("fabio is required for image saving")

    try:
        fabio_module: Any = fabio
        ext = os.path.splitext(path)[1].lower()
        if format == "auto":
            if ext in {".edf"}:
                format = "edf"
            elif ext in {".tif", ".tiff"}:
                format = "tif"
            else:
                format = "edf"

        data = np.asarray(data, dtype=np.float32)

        if format == "edf":
            h = header.copy() if header else {}
            h.update(
                {
                    "Dim_1": str(data.shape[1]),
                    "Dim_2": str(data.shape[0]),
                    "DataType": "Float32",
                }
            )
            img = fabio_module.edfimage.EdfImage(data=data, header=h)
            img.write(path)
        else:
            img = fabio_module.tifimage.TifImage(data=data, header=header or {})
            img.write(path)

        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Cache directory lifecycle / 缓存目录生命周期
# ---------------------------------------------------------------------------


class CacheDir:
    """
    Managed temporary cache directory with guaranteed cleanup.
    受控临时缓存目录，保证清理。

    Usage / 用法::

        with CacheDir() as cache:
            path = cache.make_path("output.tif")
            fabio.tifimage.TifImage(data, hdr).write(path)
            with open(path, "rb") as f:
                zf.writestr("output.tif", f.read())
        # cache directory is automatically cleaned up
        # 缓存目录自动清理

    Cleanup guarantee / 清理保证:
        - Normal exit: ``__exit__`` calls ``cleanup()``
          正常退出时 ``__exit__`` 调用 ``cleanup()``
        - Exception: ``__exit__`` calls ``cleanup()`` before propagating
          异常时 ``__exit__`` 在传播前调用 ``cleanup()``
        - SIGKILL: OS temp dir cleanup (best-effort)
          SIGKILL 时由操作系统清理临时目录（尽力而为）
    """

    _MARKER = ".bgsub_cache_marker"

    def __init__(self, prefix: str = "bgsub_pkg_"):
        self._tmpdir: Optional[tempfile.TemporaryDirectory] = None
        self._prefix = prefix

    @property
    def path(self) -> str:
        """Return the cache directory path / 返回缓存目录路径。"""
        if self._tmpdir is None:
            raise RuntimeError("CacheDir not entered — use 'with' statement")
        return self._tmpdir.name

    def make_path(self, name: str) -> str:
        """Create a unique file path in the cache directory.
        在缓存目录中创建唯一文件路径。"""
        return os.path.join(self.path, name)

    def cleanup(self) -> None:
        """Force cleanup of the cache directory.
        强制清理缓存目录。"""
        if self._tmpdir is not None:
            try:
                self._tmpdir.cleanup()
            except (OSError, PermissionError):
                pass
            self._tmpdir = None

    def __enter__(self) -> "CacheDir":
        self._tmpdir = tempfile.TemporaryDirectory(prefix=self._prefix)
        # Write marker file for identification / 写入标记文件用于识别
        marker = os.path.join(self.path, self._MARKER)
        try:
            with open(marker, "w") as f:
                f.write("BGsub cache directory\n")
        except OSError:
            pass
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        self.cleanup()
        return False  # Do not suppress exceptions / 不抑制异常


# ---------------------------------------------------------------------------
# In-memory image encoding (no disk I/O for EDF) / 内存图像编码（EDF无磁盘I/O）
# ---------------------------------------------------------------------------


def encode_edf_to_bytes(
    data: np.ndarray,
    header: Optional[dict] = None,
) -> bytes:
    """
    Encode a 2D array as EDF format bytes (no disk I/O).
    将2D数组编码为EDF格式字节（无磁盘I/O）。

    Produces a valid EDF file readable by ``fabio.open()``.
    产生可被 ``fabio.open()`` 读取的有效EDF文件。

    Parameters
    ----------
    data : np.ndarray
        2D image data / 2D图像数据
    header : dict, optional
        Additional header metadata / 额外文件头信息

    Returns
    -------
    bytes
        Complete EDF file content / 完整EDF文件内容
    """
    data = np.asarray(data, dtype=np.float32)
    if data.ndim != 2:
        raise ValueError(f"Expected 2D array, got {data.ndim}D")

    rows, cols = data.shape
    data_bytes_size = data.size * data.dtype.itemsize

    h: Dict[str, str] = {}
    if header:
        h.update({str(k): str(v) for k, v in header.items()})
    h["Dim_1"] = str(cols)
    h["Dim_2"] = str(rows)
    h["DataType"] = "FloatValue"
    h["Size"] = str(data_bytes_size)
    h["EDF_BinarySize"] = str(data_bytes_size)
    h["ByteOrder"] = "LowByteFirst"

    lines = ["{"]
    for k, v in h.items():
        lines.append(f"{k} = {v} ;")
    lines.append("}")
    header_text = "\n".join(lines) + "\n"

    header_bytes = header_text.encode("latin-1", errors="replace")
    h["EDF_HeaderSize"] = str(len(header_bytes))
    lines_with_hdr = ["{"]
    for k, v in h.items():
        lines_with_hdr.append(f"{k} = {v} ;")
    lines_with_hdr.append("}")
    header_text = "\n".join(lines_with_hdr) + "\n"
    header_bytes = header_text.encode("latin-1", errors="replace")

    data_bytes = data.astype("<f4").tobytes()

    return header_bytes + data_bytes


def encode_image_to_bytes(
    data: np.ndarray,
    fmt: str = "edf",
    header: Optional[dict] = None,
    cache: Optional[CacheDir] = None,
) -> bytes:
    """
    Encode a 2D array as image format bytes.
    将2D数组编码为图像格式字节。

    - EDF: Pure Python encoder, zero disk I/O
      EDF: 纯Python编码器，零磁盘I/O
    - TIFF: Uses fabio with managed cache directory (preserves float32)
      TIFF: 使用fabio和受控缓存目录（保留float32精度）

    Parameters
    ----------
    data : np.ndarray
        2D image data / 2D图像数据
    fmt : str
        ``'edf'`` or ``'tif'`` / 格式
    header : dict, optional
        Header metadata / 文件头信息
    cache : CacheDir, optional
        Required for TIFF — provides managed temp directory
        TIFF必须提供 — 提供受控临时目录

    Returns
    -------
    bytes
        Encoded image data / 编码后的图像数据

    Raises
    ------
    ValueError
        If TIFF encoding requested without a CacheDir
    ImportError
        If fabio is not available for TIFF encoding
    """
    if fmt == "edf":
        return encode_edf_to_bytes(data, header)
    elif fmt in ("tif", "tiff"):
        if cache is None:
            raise ValueError(
                "CacheDir is required for TIFF in-memory encoding. TIFF 内存编码需要 CacheDir。"
            )
        return _encode_tiff_via_cache(data, header, cache)
    else:
        # Default to EDF / 默认使用EDF
        return encode_edf_to_bytes(data, header)


def _encode_tiff_via_cache(
    data: np.ndarray,
    header: Optional[dict],
    cache: CacheDir,
) -> bytes:
    """
    Encode TIFF via managed cache file (preserves float32 precision).
    通过受控缓存文件编码TIFF（保留float32精度）。

    Uses fabio's TifImage writer to ensure byte-level compatibility
    with the existing ``save_image()`` output.
    使用 fabio 的 TifImage 写入器确保与现有 ``save_image()`` 输出字节级兼容。
    """
    if not HAS_FABIO:
        raise ImportError("fabio is required for TIFF encoding. Install with: pip install fabio")

    fabio_module: Any = fabio

    unique_name = f"_{uuid.uuid4().hex[:8]}.tif"
    tmp_path = cache.make_path(unique_name)

    data = np.asarray(data, dtype=np.float32)
    img = fabio_module.tifimage.TifImage(data=data, header=header or {})
    img.write(tmp_path)

    with open(tmp_path, "rb") as f:
        return f.read()


# ---------------------------------------------------------------------------
# H5 export / H5导出
# ---------------------------------------------------------------------------


def export_h5_results(
    processed_data: np.ndarray,
    transmission_values: np.ndarray,
    bg_name: str,
    sample_name: str,
    dataset_path: str,
) -> bytes:
    """
    Export background subtraction results to HDF5.
    将背景扣除结果导出为 HDF5。

    Parameters
    ----------
    processed_data : np.ndarray
        Processed image data / 处理后的图像数据
    transmission_values : np.ndarray
        Per-frame transmission values / 逐帧透过率
    bg_name : str
        Background filename / 背景文件名
    sample_name : str
        Sample filename / 样品文件名
    dataset_path : str
        Source dataset path / 源数据集路径

    Returns
    -------
    bytes
        HDF5 file content as bytes / HDF5 文件内容
    """
    from io import BytesIO

    buf = BytesIO()
    ndim = processed_data.ndim
    formula = (
        "processed[n,c] = sample[n,c] / T[n] - background[n,c]"
        if ndim == 4
        else "processed[n]   = sample[n]   / T[n] - background[n]"
    )

    with h5py.File(buf, "w") as fh:
        meta = fh.create_group("metadata")
        meta.attrs["created"] = datetime.now().isoformat()
        meta.attrs["background_file"] = bg_name
        meta.attrs["sample_file"] = sample_name
        meta.attrs["source_dataset"] = dataset_path
        meta.attrs["processing_formula"] = formula
        meta.attrs["transmission_unit"] = "percent"

        fh.create_dataset(
            "transmissions",
            data=transmission_values.astype(np.float32),
            compression="gzip",
        )
        fh.create_dataset(
            "data",
            data=processed_data.astype(np.float32),
            compression="gzip",
            compression_opts=4,
        )

    buf.seek(0)
    return buf.read()


# ---------------------------------------------------------------------------
# Index-first probe: header-only reads (no pixel data loaded)
# 索引优先探针：仅读取头信息（不加载像素数据）
# ---------------------------------------------------------------------------


def _probe_tiff_header(path: str) -> Tuple[Optional[tuple], Optional[dict]]:
    """
    Parse TIFF IFD tags for image dimensions WITHOUT loading pixel data.
    解析 TIFF IFD 标签获取图像尺寸，不加载像素数据。

    Only reads the first ~200 bytes of the file to extract width/height.
    仅读取文件前约200字节以提取宽高信息。
    """
    import struct

    with open(path, "rb") as f:
        # Byte order mark / 字节序标记
        bom = f.read(2)
        if bom == b"II":
            endian = "<"
        elif bom == b"MM":
            endian = ">"
        else:
            return None, None

        magic = struct.unpack(endian + "H", f.read(2))[0]
        if magic != 42:
            return None, None

        ifd_offset = struct.unpack(endian + "I", f.read(4))[0]
        f.seek(ifd_offset)
        num_entries = struct.unpack(endian + "H", f.read(2))[0]

        width = height = None
        header: Dict[str, str] = {}

        for _ in range(num_entries):
            tag_bytes = f.read(12)
            if len(tag_bytes) < 12:
                break
            tag, typ, count = struct.unpack(endian + "HHI", tag_bytes[:8])
            val_bytes = tag_bytes[8:12]

            if tag == 256:  # ImageWidth
                if typ == 3:  # SHORT
                    width = struct.unpack(endian + "H", val_bytes[:2])[0]
                elif typ == 4:  # LONG
                    width = struct.unpack(endian + "I", val_bytes)[0]
            elif tag == 257:  # ImageLength
                if typ == 3:
                    height = struct.unpack(endian + "H", val_bytes[:2])[0]
                elif typ == 4:
                    height = struct.unpack(endian + "I", val_bytes)[0]

        if width and height:
            header["Dim_1"] = str(width)
            header["Dim_2"] = str(height)
            return (height, width), header

    return None, None


def _probe_edf_header(path: str) -> Tuple[Optional[tuple], Optional[dict]]:
    """
    Parse EDF plain-text header for image dimensions WITHOUT loading pixel data.
    解析 EDF 纯文本头信息获取图像尺寸，不加载像素数据。

    Reads only up to the closing '}' character of the header block.
    仅读取到头信息块的 '}' 结束符。
    """
    header: Dict[str, str] = {}
    dim_1 = dim_2 = None

    with open(path, "rb") as f:
        # Read chunks until we find the header end marker '}'
        # 分块读取直到找到头结束标记 '}'
        buf = b""
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            buf += chunk
            end = buf.find(b"}")
            if end >= 0:
                buf = buf[:end]
                break

    text = buf.lstrip(b"{").decode("ascii", errors="replace")
    for line in text.split("\n"):
        line = line.strip()
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().rstrip(";").strip()
        if not key:
            continue
        header[key] = val
        if key == "Dim_1":
            try:
                dim_1 = int(val.split()[0])
            except (ValueError, IndexError):
                pass
        elif key == "Dim_2":
            try:
                dim_2 = int(val.split()[0])
            except (ValueError, IndexError):
                pass

    if dim_1 is not None and dim_2 is not None:
        # EDF convention: Dim_1 = columns, Dim_2 = rows
        # EDF 约定：Dim_1 = 列数，Dim_2 = 行数
        return (dim_2, dim_1), header

    return None, None


def probe_image_file(path: str) -> Tuple[Optional[tuple], Optional[dict]]:
    """
    Read image dimensions and header metadata WITHOUT loading pixel data.
    仅读取图像尺寸和头信息/元数据，不加载像素数据。

    Uses lightweight format-specific header parsers (TIFF IFD / EDF text)
    instead of fabio, avoiding full pixel array decompression.
    使用轻量级格式专用头解析器（TIFF IFD / EDF 文本），
    而非 fabio，避免完整像素数组解压。

    Parameters
    ----------
    path : str
        Path to the image file / 图像文件路径

    Returns
    -------
    shape : tuple or None
        Image shape as (rows, cols) / 图像形状（行，列）
    header : dict or None
        Header key-value metadata / 头信息键值对
    """
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".edf":
            return _probe_edf_header(path)
        elif ext in (".tif", ".tiff"):
            return _probe_tiff_header(path)
    except Exception:
        pass
    return None, None


def probe_h5_datasets(path: str) -> Optional[Dict[str, Any]]:
    """
    Scan HDF5 file for the best image dataset using metadata only.
    仅使用元数据扫描 HDF5 文件中的最佳图像数据集。

    Reads shape, ndim, and path from h5py.Dataset objects.
    Does NOT execute ``[:]`` or read any array data.
    读取 h5py.Dataset 对象的 shape、ndim 和路径。
    不执行 ``[:]`` 或读取任何数组数据。

    Parameters
    ----------
    path : str
        Path to HDF5 file / HDF5 文件路径

    Returns
    -------
    dict or None
        Metadata for the best dataset:
        {
            "dataset_path": str,
            "shape": tuple,
            "ndim": int,          # raw ndim (2/3/4)
            "effective_ndim": int, # normalized (3 for 2D input)
            "n_frames": int,
            "n_channels": int or None,
            "filename": str,
            "has_transmissions": bool,
        }
        Returns None if no suitable dataset found.
    """
    candidates: Dict[str, Dict[str, Any]] = {}
    has_transmissions = False

    try:
        with h5py.File(path, "r") as fh:

            def _visitor(name: str, obj) -> None:
                if isinstance(obj, h5py.Dataset) and obj.ndim >= 2:
                    candidates[name] = {
                        "shape": obj.shape,
                        "ndim": obj.ndim,
                        "size": obj.size,
                    }

            fh.visititems(_visitor)

            # Check for transmission data existence (no array reads)
            # 检查透过率数据是否存在（不读取数组）
            keys_lower = {k.lower() for k in H5_TRANSMISSION_KEYS}

            for key in H5_TRANSMISSION_KEYS:
                if key in fh and isinstance(fh[key], h5py.Dataset):
                    has_transmissions = True
                    break

            if not has_transmissions:
                found = [False]

                def _check_trans(name: str, obj) -> None:
                    if found[0]:
                        return
                    leaf = name.split("/")[-1].lower()
                    if isinstance(obj, h5py.Dataset) and leaf in keys_lower:
                        found[0] = True

                fh.visititems(_check_trans)
                has_transmissions = found[0]

            if not has_transmissions:
                for key in H5_TRANSMISSION_KEYS:
                    if key in fh.attrs:
                        has_transmissions = True
                        break
    except Exception:
        return None

    if not candidates:
        return None

    best_path = max(candidates, key=lambda k: (candidates[k]["ndim"], candidates[k]["size"]))

    meta = candidates[best_path]
    ndim = meta["ndim"]
    shape = meta["shape"]

    # Normalize ndim: 2D → 3D (single frame), same as load_h5_stack
    # 标准化 ndim：2D → 3D（单帧），与 load_h5_stack 一致
    effective_ndim = 3 if ndim == 2 else ndim
    if ndim == 2:
        n_frames, n_channels = 1, None
    elif ndim == 3:
        n_frames, n_channels = shape[0], None
    elif ndim == 4:
        n_frames, n_channels = shape[0], shape[1]
    else:
        return None

    return {
        "dataset_path": best_path,
        "shape": shape,
        "ndim": ndim,
        "effective_ndim": effective_ndim,
        "n_frames": n_frames,
        "n_channels": n_channels,
        "filename": os.path.basename(path),
        "has_transmissions": has_transmissions,
    }


# ---------------------------------------------------------------------------
# TIFF-to-H5 export / TIFF 转 H5 导出
# ---------------------------------------------------------------------------


def _safe_h5_name(name: str) -> str:
    """Sanitize a string for use as an HDF5 dataset name.
    安全化字符串用于 HDF5 数据集名称。"""
    return re.sub(r"[^A-Za-z0-9_\-]", "_", name)


def export_tiff_to_h5(
    processed: list,
    trans_dict: Dict[str, float],
    bg_name: str,
    stacked: bool = True,
) -> bytes:
    """
    Export processed TIFF results into a single HDF5 file.
    将处理后的 TIFF 结果导出为单个 HDF5 文件。

    Parameters
    ----------
    processed : list of dict
        Each dict has ``"name"`` and ``"data"`` (np.ndarray) keys.
        每个字典包含 ``"name"`` 和 ``"data"`` 键。
    trans_dict : dict
        Mapping from sample name to transmission percent.
        样品名到透过率百分比的映射。
    bg_name : str
        Background filename / 背景文件名
    stacked : bool
        If True, store as (N, H, W); if False, store as separate datasets.
        如果为 True，存储为 (N, H, W)；如果为 False，存储为独立数据集。

    Returns
    -------
    bytes
        HDF5 file content / HDF5 文件内容
    """
    from io import BytesIO

    buf = BytesIO()
    orig = [pf["name"] for pf in processed]
    T = np.array(
        [trans_dict.get(pf["name"].replace("processed_", "", 1), 100.0) for pf in processed],
        dtype=np.float32,
    )
    with h5py.File(buf, "w") as fh:
        m = fh.create_group("metadata")
        m.attrs.update(
            {
                "created": datetime.now().isoformat(),
                "background_file": bg_name,
                "n_files": len(processed),
                "processing_formula": "processed = sample / T - background",
                "transmission_unit": "percent",
                "h5_mode": "stacked" if stacked else "split",
            }
        )
        g = fh.require_group("entry/sub_bg")
        dt = g.create_dataset("transmission", data=T, compression="gzip")
        dt.attrs["unit"] = "percent"
        dt.attrs["filenames"] = json.dumps(orig, ensure_ascii=False)
        if stacked:
            stack = np.stack([pf["data"].astype(np.float32) for pf in processed])
            ds = g.create_dataset(
                "data",
                data=stack,
                compression="gzip",
                compression_opts=4,
            )
            ds.attrs["shape_description"] = "(N_frames, Height, Width)"
            ds.attrs["filenames"] = json.dumps(orig, ensure_ascii=False)
        else:
            for pf, o, t in zip(processed, orig, T):
                ds = g.create_dataset(
                    _safe_h5_name(o),
                    data=pf["data"].astype(np.float32),
                    compression="gzip",
                    compression_opts=4,
                )
                ds.attrs["original_name"] = pf["name"]
                ds.attrs["transmission_percent"] = float(t)
    buf.seek(0)
    return buf.read()
