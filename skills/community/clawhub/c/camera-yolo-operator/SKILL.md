---
name: Camera YOLO Operator | 摄像头 YOLO 操控者
description: Webcam YOLO and depth detection. 摄像头 YOLO 目标检测与 DA3Metric 深度估计；模型放 modules 缓存，输出放 projects。
---

# Camera YOLO Operator | 摄像头 YOLO 操控者 🐾

操作本地摄像头，运行 YOLO 目标检测和 DA3Metric 深度估计。

---

## 目录

1. [概述](#概述)
2. [快速开始](#快速开始)
3. [运行模式](#运行模式)
4. [模型管理](#模型管理)
5. [输出目录](#输出目录)
6. [深度校正](#深度校正)
7. [环境变量](#环境变量)
8. [故障排查](#故障排查)

---

## 概述

### 平台支持

| 平台 | 摄像头后端 | GPU |
|------|-----------|-----|
| Linux | V4L2 | NVIDIA CUDA |
| Windows | DirectShow | NVIDIA CUDA |
| macOS | AVFoundation | Apple MPS / CPU |

### 模型

- **YOLO26s 系列**: 目标检测、分割、姿态、旋转框、分类
- **DA3Metric-Large**: HuggingFace 深度估计模型，首次运行自动下载

---

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/camera-yolo-operator
pip install -r requirements.txt
```

### 2. 下载 YOLO 模型

```bash
bash scripts/download_models.sh
```

### 3. 运行

```bash
# 测试摄像头
python3 scripts/capture_webcam.py --count 3

# YOLO 检测
python3 scripts/yolo_detection.py --seconds 30

# 深度距离检测
python3 scripts/yolo_depth_distance.py --seconds 30
```

---

## 运行模式

### 模式一: 纯摄像头抓拍

不运行任何 AI 模型，只抓拍图片。用于测试摄像头是否正常工作。

```bash
python3 scripts/capture_webcam.py \
    --count 3 \
    --interval 0.5 \
    --camera-index 0
```

**参数说明**:
- `--count`: 抓拍数量（默认 3）
- `--interval`: 每次抓拍间隔秒数（默认 0.5）
- `--camera-index`: 摄像头索引（默认 0）
- `--warmup`: 预热帧数（默认 5）

---

### 模式二: YOLO 纯检测

使用 YOLO 进行目标检测，可选多种模型（检测/分割/姿态等）。

```bash
python3 scripts/yolo_detection.py \
    --seconds 30 \
    --save-every 10 \
    --max-saves 3 \
    --yolo-model yolo26s.pt \
    --conf 0.5
```

**参数说明**:
- `--seconds`: 运行时间（默认 30）
- `--save-every`: 每隔多少秒保存一张（默认 10）
- `--max-saves`: 最大保存数量（默认 3）
- `--yolo-model`: YOLO 模型路径或名称
- `--conf`: 置信度阈值（默认 0.5）
- `--device`: 设备，"0"=GPU，"cpu"=CPU（默认 "0"）

**可用 YOLO 模型**:

| 模型 | 用途 | 命令示例 |
|------|------|---------|
| `yolo26s.pt` | 目标检测（默认） | `--yolo-model yolo26s.pt` |
| `yolo26s-seg.pt` | 实例分割 | `--yolo-model yolo26s-seg.pt` |
| `yolo26s-pose.pt` | 姿态估计 | `--yolo-model yolo26s-pose.pt` |
| `yolo26s-obb.pt` | 旋转框检测 | `--yolo-model yolo26s-obb.pt` |
| `yolo26s-cls.pt` | 图像分类 | `--yolo-model yolo26s-cls.pt` |

---

### 模式三: YOLO 检测 + 深度距离叠加

将 YOLO 检测框与 DA3Metric 深度图融合，在每个检测框上标注物体类别、置信度和到摄像头的距离（米）。

```bash
python3 scripts/yolo_depth_distance.py \
    --seconds 30 \
    --save-every 5 \
    --max-saves 6 \
    --yolo-model yolo26s.pt \
    --depth-scale 1.0 \
    --output-dir ~/.openclaw/workspace/projects/camera-yolo-operator/depth_distance
```

**参数说明**:
- `--depth-scale`: 深度校正系数（详见下文）
- `--depth-model`: 深度模型，默认 `depth-anything/DA3Metric-Large`
- `--device`: 深度模型运行设备（默认 `cuda:0`）

**输出内容**:
- 绿色检测框 + 标签格式：`{类别} {置信度} | {距离}m`
- 背景叠加伪彩色深度图（INFERNO 配色，暖色=近，冷色=远）

---

### 模式四: 通用目标轨迹跟踪

使用 YOLO 检测任意目标 + ByteTrack 分配持续 ID + Supervision 绘制轨迹线。行人、车辆、鸟类——只要 YOLO 能检测的类别都能跟踪。统计输出为**独立目标数量**（去重后的车辆数、行人数），而非帧次出现次数。

```bash
# 摄像头实时检测（默认纯检测，画框不画轨迹）
python3 scripts/yolo_pedestrian_tracker.py --source 0 --seconds 30

# 摄像头实时跟踪（开启轨迹线）
python3 scripts/yolo_pedestrian_tracker.py --source 0 --seconds 30 --track

# 视频文件：标注并输出完整带轨迹的视频
python3 scripts/yolo_pedestrian_tracker.py --source /path/to/video.mp4 --track --output-video out.mp4

# 指定类别跟踪
python3 scripts/yolo_pedestrian_tracker.py --source 0 --seconds 30 --track --classes 0       # 仅行人
python3 scripts/yolo_pedestrian_tracker.py --source 0 --seconds 30 --track --classes 2 3         # 车+摩托车

# 调轨迹线长度
python3 scripts/yolo_pedestrian_tracker.py --source 0 --trail-length 50
```

**参数说明**:
- `--track`: 开启轨迹跟踪模式（默认关闭）
- `--classes`: 要检测的目标类别，默认全部检测。`0`=人，`2`=车，`3`=摩托车，`15`=猫，`16`=狗等
- `--source`: 视频源，`0`=摄像头，或本地视频文件路径
- `--seconds`: 运行时间（默认 30，仅摄像头模式有效）
- `--trail-length`: 轨迹线长度，按帧计（默认 30）
- `--conf`: 置信度阈值（默认 0.5）
- `--device`: 设备，`0`=GPU，`cpu`=CPU
- `--output-video`: 输出带标注的完整视频路径（推荐使用）
- `--save-every`: 截图保存间隔秒数（默认 5，仅视频文件模式）
- `--max-saves`: 最大截图数量（默认 10）

**输出**:
- 带标注的视频（`--output-video` 指定路径）
- 控制台输出独立目标统计（独立车辆数、独立行人数等）

**新增依赖**（supervision 已内置 ByteTrack）：
```bash
pip install supervision
```

**输出目录**:
```
projects/camera-yolo-operator/pedestrian_track/
├── annotated_video.mp4  # 带标注的视频（--output-video 指定）
└── frame_*.jpg         # 截图
```

---

## 模式五: 纯深度图（无 YOLO）

单独输出深度图，不叠加检测结果。

```python
from depth_anything_3.api import DepthAnything3
import cv2
import numpy as np

model = DepthAnything3.from_pretrained('depth-anything/DA3Metric-Large')
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

pred = model.inference([frame])
depth = pred.depth[0]  # [H, W] 米制深度

# 灰度版
gray = (depth / depth.max() * 255).astype(np.uint8)
cv2.imwrite('depth_gray.jpg', gray)

# 伪彩色版
color = cv2.applyColorMap(
    cv2.convertScaleAbs((depth / depth.max() * 255).astype(np.uint8)),
    cv2.COLORMAP_INFERNO)
cv2.imwrite('depth_color.jpg', color)
print(f"深度范围: {depth.min():.2f}~{depth.max():.2f}m")
```

---

## 模型管理

### 模型存放位置

⚠️ 大型模型文件（>50MB）禁止直接放入技能文件夹，统一存放在：
```
~/.cache/huggingface/modules/camera-yolo-operator/
├── yolo26s.pt                      # YOLO 目标检测（ Ultralytics 官方下载）
└── DA3Metric-Large → ~/.cache/huggingface/hub/models--depth-anything--DA3Metric-Large/
```

DA3Metric-Large 由 `depth_anything_3` 包调用 HuggingFace 官方下载，存放在 hub 缓存，通过符号链接在模块目录对外保持路径统一。

技能文件夹本身（`~/.openclaw/workspace/skills/camera-yolo-operator/`）仅含技能代码，不存放任何大型模型文件。

### 下载模型

```bash
# YOLO26s（下载后移动到模块缓存）
mkdir -p ~/.cache/huggingface/modules/camera-yolo-operator/
python3 -c "from ultralytics import YOLO; YOLO('yolo26s.pt')"
mv yolo26s.pt ~/.cache/huggingface/modules/camera-yolo-operator/

# DA3Metric-Large（自动下载到 hub 缓存，再做符号链接）
python3 -c "from depth_anything_3.api import DepthAnything3; DepthAnything3.from_pretrained('depth-anything/DA3Metric-Large')"
ln -s ~/.cache/huggingface/hub/models--depth-anything--DA3Metric-Large \
   ~/.cache/huggingface/modules/camera-yolo-operator/DA3Metric-Large
```

### 模型搜索路径

脚本按以下顺序查找 YOLO 模型：
1. 环境变量 `YOLO_MODEL_PATH`
2. `~/.cache/huggingface/modules/camera-yolo-operator/`
3. `~/.openclaw/workspace/yolo/`（兼容旧路径）
4. 当前目录

### 指定模型路径

```bash
# 通过命令行
python3 scripts/yolo_detection.py --yolo-model /path/to/custom/model.pt

# 或通过环境变量
export YOLO_MODEL_PATH=/path/to/custom/model.pt
python3 scripts/yolo_detection.py
```

---

## 输出目录

运行结果统一保存在工作区的 `projects/camera-yolo-operator/` 目录下：

```
~/.openclaw/workspace/projects/camera-yolo-operator/
├── captures/          # capture_webcam.py 的原始抓拍
├── detection/         # yolo_detection.py 的检测结果
├── depth_distance/    # yolo_depth_distance.py 的深度+检测结果
└── pedestrian_track/  # yolo_pedestrian_tracker.py 的目标轨迹标注结果
    └── track_*.jpg
```

可使用 `--output-dir` 参数指定其他目录。

---

## 深度校正

### 问题现象

深度模型输出的距离值与实际距离不符。

### 校正方法

1. 在摄像头前放置物体，记录模型显示的距离 `D_model`
2. 用尺子测量实际距离 `D_real`
3. 校正系数 = `D_real / D_model`
4. 使用 `--depth-scale {系数}` 运行脚本

**示例**:

- 物体实际距离: 3m
- 模型显示距离: 1.9m
- 校正系数: `3.0 / 1.9 ≈ 1.574`
- 运行命令: `python3 scripts/yolo_depth_distance.py --depth-scale 1.574`

---

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `OPENCLAW_WORKSPACE` | `~/.openclaw/workspace` | 工作区根目录 |
| `YOLO_MODEL_PATH` | `~/.cache/huggingface/modules/camera-yolo-operator/yolo26s.pt` | YOLO 模型路径 |
| `HF_ENDPOINT` | (官方) | HuggingFace 镜像，解决下载问题 |

**设置镜像加速下载**:

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

---

## 故障排查

### 摄像头无法打开

```bash
# 检查摄像头设备
ls -la /dev/video*          # Linux
# 或设备管理器              # Windows

# 测试摄像头是否被占用
python3 scripts/capture_webcam.py --count 1
```

**解决方案**:
- 关闭其他占用摄像头的应用（微信、QQ、Zoom 等）
- 尝试不同的 `--camera-index`
- Linux: 检查用户权限 `sudo usermod -a -G video $USER`

### HuggingFace 模型下载失败

```bash
# 方法一: 清除代理
unset all_proxy ALL_PROXY http_proxy https_proxy

# 方法二: 使用镜像
export HF_ENDPOINT=https://hf-mirror.com

# 方法三: 手动下载
git lfs install
git clone https://huggingface.co/depth-anything/DA3Metric-Large ~/.cache/huggingface/modules/depth_anything_3/ddp/
```

### GPU 未被使用

```bash
# 检查 PyTorch CUDA
python3 -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# 检查 NVIDIA 驱动
nvidia-smi
```

**解决方案**:
- 确认 CUDA 版本匹配（当前环境 CUDA 12.1）
- 重新安装 PyTorch: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121`

### 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 目录结构

```
camera-yolo-operator/
├── SKILL.md                    # 本文档
├── requirements.txt            # Python 依赖
├── scripts/
│   ├── capture_webcam.py       # 纯摄像头抓拍
│   ├── yolo_detection.py       # YOLO 目标检测
│   ├── yolo_depth_distance.py  # YOLO + 深度距离
│   ├── yolo_pedestrian_tracker.py  # 行人轨迹跟踪
│   └── download_models.sh      # 模型下载脚本
├── models/
│   └── .gitkeep                # YOLO 模型目录（需单独下载）
└── references/
    ├── platform.md            # 平台假设与维护笔记
    └── deployment.md           # 详细部署指南
```

---

## 依赖

```
# requirements.txt
ultralytics>=8.0.0
torch>=2.0.0
torchvision>=0.15.0
depth-anything-3>=0.1.0
opencv-python>=4.8.0
numpy>=1.24.0
```

---

## 维护笔记

- **模型更新**: 定期检查 Ultralytics 官网获取新版本 YOLO
- **深度模型**: DA3Metric-Large 由 HuggingFace 托管，需网络访问
- **GPU 兼容性**: 确认 PyTorch CUDA 版本与 NVIDIA 驱动兼容
