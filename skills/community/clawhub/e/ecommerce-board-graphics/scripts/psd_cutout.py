# -*- coding: utf-8 -*-
"""extract the TOPMOST visible non-background layer from a psd as the cutout.
   psd_tools iterates bottom-first, so the last visible non-background layer
   is the topmost one (图层2 = 装饰/荧光部位). 用户要求直接读取最上方图层。"""
import numpy as np
from psd_tools import PSDImage


def cutout_layer(psd_path):
    psd = PSDImage.open(psd_path)
    best = None
    for layer in psd:  # bottom-first; last one = topmost layer
        if layer.is_group():
            continue
        if not layer.visible or "背景" in layer.name:
            continue
        try:
            img = layer.composite(psd.bbox)
        except Exception:
            continue
        if img is None:
            continue
        a = img.split()[-1]
        if a.getbbox() is None:
            continue
        best = img
    return best


if __name__ == "__main__":
    import sys
    p = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\terri\Desktop\1\BDSM（15张）\00000-oneObsession_v23_2-3655560629.psd"
    img = cutout_layer(p)
    print("cutout:", img.size, img.mode)
