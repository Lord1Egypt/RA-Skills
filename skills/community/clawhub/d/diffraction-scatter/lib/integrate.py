#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
integrate.py — Streaming post-PONI integration runner for common pyFAI modes
integrate.py — 面向常见 pyFAI 模式的流式 PONI 后积分执行器
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Optional

import h5py
import numpy as np
import pyFAI
from pyFAI.integrator.azimuthal import AzimuthalIntegrator
from pyFAI.integrator.fiber import FiberIntegrator
from pyFAI.io.ponifile import PoniFile

from pyfaiskills.lib.common import (
    build_mask,
    emit_event,
    ensure_dir,
    expand_inputs,
    iter_image_frames,
    load_aux_image,
)

FIBER_UNITS_IP = [
    "qip_nm^-1",
    "qip_A^-1",
    "qxgi_nm^-1",
    "qygi_nm^-1",
    "qzgi_nm^-1",
    "qtot_nm^-1",
    "qxgi_A^-1",
    "qygi_A^-1",
    "qzgi_A^-1",
    "qtot_A^-1",
    "scattering_angle_horz_rad",
    "exit_angle_horz_rad",
    "exit_angle_horz_deg",
    "chigi_rad",
    "chigi_deg",
]
FIBER_UNITS_OOP = [
    "qoop_nm^-1",
    "qoop_A^-1",
    "qxgi_nm^-1",
    "qygi_nm^-1",
    "qzgi_nm^-1",
    "qtot_nm^-1",
    "qxgi_A^-1",
    "qygi_A^-1",
    "qzgi_A^-1",
    "qtot_A^-1",
    "scattering_angle_vert_rad",
    "exit_angle_vert_rad",
    "exit_angle_vert_deg",
    "chigi_rad",
    "chigi_deg",
]


def _resolve_1d_unit(unit: str) -> tuple[str, float]:
    """Resolve project-friendly units. / 解析项目友好的 1D 单位。"""
    if unit == "q_A^-1":
        return "q_nm^-1", 0.1
    return unit, 1.0


def _convert_chi_axis(chi: np.ndarray, target_unit: str) -> tuple[np.ndarray, str, float]:
    """Normalize chi axis for export. / 规范化导出的 chi 坐标轴单位。"""
    if target_unit == "chi_rad":
        return np.radians(chi), "chi_deg", math.pi / 180.0
    return chi, "chi_deg", 1.0


def _write_csv_1d(
    path: Path, radial: np.ndarray, intensity: np.ndarray, sigma: Optional[np.ndarray]
) -> None:
    """Write one 1D profile. / 写出单条 1D 曲线。"""
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        header = ["radial", "intensity"]
        if sigma is not None:
            header.append("sigma")
        writer.writerow(header)
        for idx, x_val in enumerate(radial):
            row = [float(x_val), float(intensity[idx])]
            if sigma is not None:
                row.append(float(sigma[idx]))
            writer.writerow(row)


def _write_hdf5_1d(
    path: Path,
    radial: np.ndarray,
    intensity: np.ndarray,
    sigma: Optional[np.ndarray],
    metadata: dict[str, object],
) -> None:
    """Write one 1D profile to HDF5. / 将单条 1D 曲线写入 HDF5。"""
    with h5py.File(path, "w") as handle:
        meta = handle.create_group("metadata")
        for key, value in metadata.items():
            meta.attrs[str(key)] = _normalize_attr_value(value)
        handle.create_dataset("radial", data=radial.astype(np.float64), compression="gzip")
        handle.create_dataset("intensity", data=intensity.astype(np.float32), compression="gzip")
        if sigma is not None:
            handle.create_dataset("sigma", data=sigma.astype(np.float32), compression="gzip")


def _write_bundle_2d(
    npz_path: Path,
    h5_path: Path,
    intensity: np.ndarray,
    axis_x: np.ndarray,
    axis_y: np.ndarray,
    metadata: dict[str, object],
    axis_x_name: str,
    axis_y_name: str,
) -> None:
    """Write 2D bundle as NPZ and HDF5. / 将 2D 结果写为 NPZ 与 HDF5。"""
    np.savez_compressed(
        npz_path,
        intensity=intensity,
        axis_x=axis_x,
        axis_y=axis_y,
        metadata=json.dumps(metadata, ensure_ascii=False),
    )
    with h5py.File(h5_path, "w") as handle:
        meta = handle.create_group("metadata")
        for key, value in metadata.items():
            meta.attrs[str(key)] = _normalize_attr_value(value)
        handle.create_dataset("intensity", data=intensity.astype(np.float32), compression="gzip")
        handle.create_dataset(axis_x_name, data=axis_x.astype(np.float64), compression="gzip")
        handle.create_dataset(axis_y_name, data=axis_y.astype(np.float64), compression="gzip")


def _build_fiber_integrator(
    poni: PoniFile, use_poni_rot3: bool, override_rot3_deg: float
) -> FiberIntegrator:
    """Build FiberIntegrator from PONI. / 基于 PONI 构建 FiberIntegrator。"""
    rot3 = poni.rot3 if use_poni_rot3 else math.radians(override_rot3_deg)
    return FiberIntegrator(
        dist=poni.dist,
        poni1=poni.poni1,
        poni2=poni.poni2,
        wavelength=poni.wavelength,
        rot1=poni.rot1,
        rot2=poni.rot2,
        rot3=rot3,
        detector=poni.detector,
    )


def _normalize_attr_value(value: object) -> object:
    """Normalize metadata for HDF5 attrs. / 规范化 HDF5 属性元数据。"""
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False)
    return value


def _base_metadata(
    args: argparse.Namespace, frame_stem: str, source_file: str
) -> dict[str, object]:
    """Common output metadata. / 输出的公共元信息。"""
    return {
        "mode": args.mode,
        "source_file": source_file,
        "frame_stem": frame_stem,
        "poni": args.poni,
        "pyfai_version": pyFAI.version,
        "method": args.method,
        "polarization": args.polarization,
        "correct_solid_angle": args.correct_solid_angle,
    }


def run(args: argparse.Namespace) -> int:
    """Execute integration. / 执行积分。"""
    output_dir = ensure_dir(args.output_dir)
    input_files = expand_inputs(args.inputs, recursive=not args.no_recursive)
    if not input_files:
        raise FileNotFoundError("No input detector files were found.")

    poni = PoniFile(data=args.poni)
    ai = AzimuthalIntegrator()
    ai.load(args.poni)

    dark = load_aux_image(args.dark)
    flat = load_aux_image(args.flat)
    custom_mask_arr = load_aux_image(args.mask)
    custom_mask = None if custom_mask_arr is None else custom_mask_arr.astype(bool)

    manifest_path = output_dir / "manifest.jsonl"
    processed = 0
    with manifest_path.open("w", encoding="utf-8") as manifest:
        for input_file in input_files:
            emit_event("file_start", file=input_file, mode=args.mode)
            for frame in iter_image_frames(input_file, args.h5_dataset, args.h5_channel):
                frame_stem = frame.stem
                final_mask = build_mask(
                    frame.data, args.valid_min, args.valid_max, frame.dead_mask, custom_mask
                )
                metadata = _base_metadata(args, frame_stem, input_file)
                metadata.update(
                    {
                        "dataset": frame.dataset_path,
                        "channel": frame.channel,
                        "frame_index": frame.frame_index,
                        "frame_count": frame.frame_count,
                    }
                )

                if args.mode == "radial1d":
                    pyfai_unit, factor = _resolve_1d_unit(args.unit)
                    result = ai.integrate1d_ng(
                        frame.data,
                        args.npt,
                        unit=pyfai_unit,
                        method=args.method,
                        correctSolidAngle=args.correct_solid_angle,
                        polarization_factor=args.polarization,
                        dark=dark,
                        flat=flat,
                        mask=final_mask,
                        error_model=args.error_model,
                    )
                    radial = result.radial * factor
                    sigma = getattr(result, "sigma", None)
                    csv_path = output_dir / f"{frame_stem}.csv"
                    h5_path = output_dir / f"{frame_stem}.h5"
                    metadata.update(
                        {
                            "unit": args.unit,
                            "raw_pyfai_unit": pyfai_unit,
                            "unit_conversion_factor": factor,
                            "npt": args.npt,
                            "error_model": args.error_model,
                        }
                    )
                    _write_csv_1d(csv_path, radial, result.intensity, sigma)
                    _write_hdf5_1d(h5_path, radial, result.intensity, sigma, metadata)
                    outputs = {"csv": str(csv_path), "h5": str(h5_path)}

                elif args.mode == "sector1d":
                    pyfai_unit, factor = _resolve_1d_unit(args.unit)
                    result = ai.integrate1d_ng(
                        frame.data,
                        args.npt,
                        unit=pyfai_unit,
                        method=args.method,
                        correctSolidAngle=args.correct_solid_angle,
                        polarization_factor=args.polarization,
                        dark=dark,
                        flat=flat,
                        mask=final_mask,
                        azimuth_range=(args.azimuth_min, args.azimuth_max),
                        error_model=args.error_model,
                    )
                    radial = result.radial * factor
                    sigma = getattr(result, "sigma", None)
                    csv_path = output_dir / f"{frame_stem}.csv"
                    h5_path = output_dir / f"{frame_stem}.h5"
                    metadata.update(
                        {
                            "unit": args.unit,
                            "raw_pyfai_unit": pyfai_unit,
                            "unit_conversion_factor": factor,
                            "npt": args.npt,
                            "azimuth_min": args.azimuth_min,
                            "azimuth_max": args.azimuth_max,
                            "error_model": args.error_model,
                        }
                    )
                    _write_csv_1d(csv_path, radial, result.intensity, sigma)
                    _write_hdf5_1d(h5_path, radial, result.intensity, sigma, metadata)
                    outputs = {"csv": str(csv_path), "h5": str(h5_path)}

                elif args.mode == "azimuthal1d":
                    chi, intensity = ai.integrate_radial(
                        frame.data,
                        npt=args.npt,
                        npt_rad=args.npt_rad,
                        radial_range=(args.radial_min, args.radial_max),
                        unit=args.azimuthal_unit,
                        radial_unit=args.radial_unit,
                        method=args.method,
                        correctSolidAngle=args.correct_solid_angle,
                        polarization_factor=args.polarization,
                        dark=dark,
                        flat=flat,
                        mask=final_mask.astype(np.uint8),
                    )
                    csv_path = output_dir / f"{frame_stem}.csv"
                    h5_path = output_dir / f"{frame_stem}.h5"
                    metadata.update(
                        {
                            "azimuthal_unit": args.azimuthal_unit,
                            "radial_unit": args.radial_unit,
                            "radial_min": args.radial_min,
                            "radial_max": args.radial_max,
                            "npt": args.npt,
                            "npt_rad": args.npt_rad,
                        }
                    )
                    _write_csv_1d(csv_path, chi, intensity, None)
                    _write_hdf5_1d(h5_path, chi, intensity, None, metadata)
                    outputs = {"csv": str(csv_path), "h5": str(h5_path)}

                elif args.mode == "cake2d":
                    intensity, radial, chi = ai.integrate2d_ng(
                        frame.data,
                        npt_rad=args.npt_rad,
                        npt_azim=args.npt_azim,
                        unit=args.unit,
                        method=args.method,
                        correctSolidAngle=args.correct_solid_angle,
                        polarization_factor=args.polarization,
                        dark=dark,
                        flat=flat,
                        mask=final_mask,
                    )
                    chi, raw_chi_unit, chi_conversion_factor = _convert_chi_axis(chi, args.chi_unit)
                    npz_path = output_dir / f"{frame_stem}.npz"
                    h5_path = output_dir / f"{frame_stem}.h5"
                    metadata.update(
                        {
                            "unit": args.unit,
                            "npt_rad": args.npt_rad,
                            "npt_azim": args.npt_azim,
                            "chi_unit": args.chi_unit,
                            "raw_pyfai_chi_unit": raw_chi_unit,
                            "chi_conversion_factor": chi_conversion_factor,
                        }
                    )
                    _write_bundle_2d(
                        npz_path, h5_path, intensity, radial, chi, metadata, "radial", "chi"
                    )
                    outputs = {"npz": str(npz_path), "h5": str(h5_path)}

                elif args.mode == "fiber2d":
                    fiber_integrator = _build_fiber_integrator(
                        poni, args.use_poni_rot3, args.override_rot3
                    )
                    kwargs = {
                        "data": frame.data,
                        "npt_ip": args.npt_ip,
                        "npt_oop": args.npt_oop,
                        "unit_ip": args.unit_ip,
                        "unit_oop": args.unit_oop,
                        "sample_orientation": args.sample_orientation,
                        "incident_angle": math.radians(args.incident_angle),
                        "tilt_angle": math.radians(args.tilt_angle),
                        "angle_unit": "rad",
                        "correctSolidAngle": args.correct_solid_angle,
                        "mask": final_mask.astype(np.uint8),
                    }
                    if args.polarization is not None:
                        kwargs["polarization_factor"] = args.polarization
                    if not args.auto_range:
                        kwargs["ip_range"] = (args.ip_min, args.ip_max)
                        kwargs["oop_range"] = (args.oop_min, args.oop_max)
                    result = fiber_integrator.integrate2d_grazing_incidence(**kwargs)
                    if hasattr(result, "intensity"):
                        intensity = result.intensity
                        axis_ip = result.radial
                        axis_oop = result.azimuthal
                    else:
                        intensity, axis_ip, axis_oop = result
                    npz_path = output_dir / f"{frame_stem}.npz"
                    h5_path = output_dir / f"{frame_stem}.h5"
                    metadata.update(
                        {
                            "unit_ip": args.unit_ip,
                            "unit_oop": args.unit_oop,
                            "npt_ip": args.npt_ip,
                            "npt_oop": args.npt_oop,
                            "sample_orientation": args.sample_orientation,
                            "incident_angle_deg": args.incident_angle,
                            "tilt_angle_deg": args.tilt_angle,
                            "auto_range": args.auto_range,
                        }
                    )
                    _write_bundle_2d(
                        npz_path,
                        h5_path,
                        intensity,
                        axis_ip,
                        axis_oop,
                        metadata,
                        "axis_ip",
                        "axis_oop",
                    )
                    outputs = {"npz": str(npz_path), "h5": str(h5_path)}

                else:
                    raise ValueError(f"Unsupported mode: {args.mode}")

                record = {"frame": frame_stem, "source": input_file, "outputs": outputs}
                manifest.write(json.dumps(record, ensure_ascii=False) + "\n")
                manifest.flush()
                emit_event("frame_done", frame=frame_stem, outputs=outputs)
                processed += 1

    emit_event("done", processed=processed, manifest=str(manifest_path), output_dir=str(output_dir))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Create argument parser. / 创建参数解析器。"""
    parser = argparse.ArgumentParser(description="Streaming post-PONI pyFAI integration runner")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["radial1d", "azimuthal1d", "sector1d", "cake2d", "fiber2d"],
        help="Integration mode",
    )
    parser.add_argument("--poni", required=True, help="Path to .poni file")
    parser.add_argument(
        "-i", "--inputs", nargs="+", required=True, help="Files, directories, or globs"
    )
    parser.add_argument("-o", "--output-dir", required=True, help="Output directory")
    parser.add_argument("--h5-dataset", help="Dataset path for HDF5 inputs")
    parser.add_argument("--h5-channel", help="Channel name or index for 4D HDF5")
    parser.add_argument(
        "--no-recursive", action="store_true", help="Disable recursive directory scan"
    )
    parser.add_argument("--mask", help="Custom mask file (.npy/.edf/.tif/.h5)")
    parser.add_argument("--dark", help="Dark image file")
    parser.add_argument("--flat", help="Flat-field image file")
    parser.add_argument("--valid-min", type=float, default=None, help="Minimum valid intensity")
    parser.add_argument("--valid-max", type=float, default=None, help="Maximum valid intensity")
    parser.add_argument(
        "--polarization", type=float, default=None, help="Polarization factor [-1, 1]"
    )
    parser.add_argument("--method", default="csr", help="pyFAI integration method")
    parser.add_argument(
        "--correct-solid-angle", dest="correct_solid_angle", action="store_true", default=True
    )
    parser.add_argument(
        "--no-correct-solid-angle", dest="correct_solid_angle", action="store_false"
    )

    parser.add_argument("--npt", type=int, default=1000, help="1D points")
    parser.add_argument("--unit", default="q_nm^-1", help="1D or cake radial unit")
    parser.add_argument("--error-model", default=None, help="Error model for integrate1d_ng")
    parser.add_argument(
        "--azimuth-min", type=float, default=-180.0, help="Sector min angle in degrees"
    )
    parser.add_argument(
        "--azimuth-max", type=float, default=180.0, help="Sector max angle in degrees"
    )
    parser.add_argument(
        "--npt-rad", type=int, default=256, help="Radial points for azimuthal or cake integration"
    )
    parser.add_argument(
        "--npt-azim", type=int, default=360, help="Azimuthal points for cake integration"
    )
    parser.add_argument(
        "--chi-unit",
        default="chi_deg",
        choices=["chi_deg", "chi_rad"],
        help="Chi axis unit for cake2d output",
    )
    parser.add_argument("--radial-unit", default="q_nm^-1", help="Radial unit for azimuthal1d")
    parser.add_argument(
        "--radial-min", type=float, default=1.0, help="Azimuthal radial lower bound"
    )
    parser.add_argument(
        "--radial-max", type=float, default=20.0, help="Azimuthal radial upper bound"
    )
    parser.add_argument("--azimuthal-unit", default="chi_deg", help="Output unit for azimuthal1d")

    parser.add_argument("--npt-ip", type=int, default=800, help="Fiber in-plane points")
    parser.add_argument("--npt-oop", type=int, default=800, help="Fiber out-of-plane points")
    parser.add_argument(
        "--unit-ip", default="qip_nm^-1", choices=FIBER_UNITS_IP, help="Fiber in-plane unit"
    )
    parser.add_argument(
        "--unit-oop", default="qoop_nm^-1", choices=FIBER_UNITS_OOP, help="Fiber out-of-plane unit"
    )
    parser.add_argument(
        "--sample-orientation",
        type=int,
        choices=range(1, 9),
        default=1,
        help="Fiber sample orientation 1-8",
    )
    parser.add_argument(
        "--incident-angle", type=float, default=0.0, help="Incident angle in degrees"
    )
    parser.add_argument("--tilt-angle", type=float, default=0.0, help="Tilt angle in degrees")
    parser.add_argument("--auto-range", action="store_true", help="Use pyFAI-inferred GI range")
    parser.add_argument("--ip-min", type=float, default=-20.0, help="Fiber ip lower bound")
    parser.add_argument("--ip-max", type=float, default=20.0, help="Fiber ip upper bound")
    parser.add_argument("--oop-min", type=float, default=-20.0, help="Fiber oop lower bound")
    parser.add_argument("--oop-max", type=float, default=20.0, help="Fiber oop upper bound")
    parser.add_argument(
        "--use-poni-rot3", action="store_true", default=True, help="Use rot3 stored in .poni"
    )
    parser.add_argument(
        "--override-rot3", type=float, default=0.0, help="Override rot3 in degrees when needed"
    )
    return parser


def main() -> int:
    """CLI entrypoint. / 命令行入口。"""
    parser = build_parser()
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
