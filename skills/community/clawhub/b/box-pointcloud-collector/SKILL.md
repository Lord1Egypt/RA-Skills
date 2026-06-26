---
name: box-pointcloud-collector
description: Intel RealSense D455 箱体点云数据采集工具。用于采集箱体的 RGB 彩色图和深度图数据集，支持手动/自动采集模式。触发场景：(1) 采集箱体/物体点云数据 (2) 创建深度学习训练数据集 (3) Bin Picking 项目数据准备 (4) 相机标定数据采集。支持 Intel RealSense D455 相机。
---

# 箱体点云数据采集工具

使用 Intel RealSense D455 相机采集箱体 RGB-D 数据集。

## 快速开始

### 启动采集

```bash
python scripts/collect_v2.py
```

### 操作按键

| 按键 | 功能 |
|------|------|
| **S** | 保存 1 张（RGB + Depth）|
| **A** | 自动保存 10 张（每 5 秒 1 张）|
| **Q** | 退出并打开数据目录 |

## 数据集结构

```
box_dataset/
└── box_YYYYMMDD_HHMMSS/
    ├── camera_intrinsic.json    # 相机内参
    ├── dataset_config.json      # 数据集配置
    ├── capture_stats.json       # 采集统计
    └── raw_data/
        ├── 000001_Color.png     # RGB 彩色图
        ├── 000001_Depth.raw     # 深度图 (uint16)
        └── ...
```

## 文件格式

| 文件 | 格式 | 说明 |
|------|------|------|
| `XXX_Color.png` | PNG 8位 RGB | 彩色图像 |
| `XXX_Depth.raw` | uint16 raw | 深度数据 (640×480×2 bytes) |
| `camera_intrinsic.json` | JSON | 相机内参 (fx, fy, cx, cy) |

## 数据处理

### 读取深度图

```python
import numpy as np

depth = np.fromfile("000001_Depth.raw", dtype=np.uint16)
depth = depth.reshape(480, 640)
depth_m = depth / 1000.0  # 转换为米
```

### 像素坐标 → 3D 坐标

```python
import json

with open("camera_intrinsic.json") as f:
    intr = json.load(f)

def pixel_to_3d(u, v, depth_m):
    X = (u - intr['ppx']) * depth_m / intr['fx']
    Y = (v - intr['ppy']) * depth_m / intr['fy']
    Z = depth_m
    return X, Y, Z
```

## 采集规范

- **有效距离**：0.5m - 2.5m
- **推荐距离**：0.5m - 1.5m
- **每种箱体**：20-30 张
- **变换角度**：调整箱子位置/角度增加多样性

## 注意事项

1. **中文路径问题**：数据集目录使用纯英文命名
2. **键盘焦点**：点击 RGB Camera 窗口后按 S/A 键
3. **相机占用**：关闭 RealSense Viewer 等程序

## 硬件要求

- Intel RealSense D455
- USB 3.0 接口
- Windows 10/11

## 依赖安装

```bash
pip install pyrealsense2 opencv-python numpy
```

---

**作者**：Robot_Qu  
**版本**：v2.0