#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inspect.py — Inspect PONI files and detector inputs for post-PONI workflows
inspect.py — 检查 PONI 文件与探测器输入，服务于 PONI 后积分流程
"""

from __future__ import annotations

import argparse
import contextlib
import json
from pathlib import Path

from pyFAI.io.ponifile import PoniFile

from pyfaiskills.lib.common import discover_h5_datasets, iter_image_frames


def main() -> int:
    """CLI entrypoint. / 命令行入口。"""
    parser = argparse.ArgumentParser(description="Inspect .poni files and detector data")
    parser.add_argument("--poni", required=True, help="Path to the .poni file")
    parser.add_argument("inputs", nargs="*", help="Optional detector files to inspect")
    args = parser.parse_args()

    poni = PoniFile(data=args.poni)
    print(
        json.dumps(
            {
                "event": "poni",
                "path": args.poni,
                "dist": poni.dist,
                "poni1": poni.poni1,
                "poni2": poni.poni2,
                "rot1": poni.rot1,
                "rot2": poni.rot2,
                "rot3": poni.rot3,
                "wavelength": poni.wavelength,
                "detector": str(poni.detector),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )

    for input_path in args.inputs:
        suffix = Path(input_path).suffix.lower()
        if suffix in {".h5", ".hdf5"}:
            print(
                json.dumps(
                    {
                        "event": "datasets",
                        "path": input_path,
                        "datasets": discover_h5_datasets(input_path),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
        frame_iter = iter_image_frames(input_path)
        with contextlib.closing(frame_iter):
            first = next(frame_iter)
        print(
            json.dumps(
                {
                    "event": "image",
                    "path": input_path,
                    "shape": list(first.data.shape),
                    "frame_count": first.frame_count,
                    "dataset": first.dataset_path,
                    "channel": first.channel,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
