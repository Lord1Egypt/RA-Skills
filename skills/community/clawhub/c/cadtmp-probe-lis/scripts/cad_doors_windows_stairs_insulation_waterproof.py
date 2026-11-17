#!/usr/bin/env python3
# 入口：门窗/楼梯/保温/防水识图候选（统一候选契约）
import runpy, sys
runpy.run_path(__file__.replace('cad_doors_windows_stairs_insulation_waterproof.py','cad_deep_geometry.py'), run_name='__cad_deep_geometry__')
