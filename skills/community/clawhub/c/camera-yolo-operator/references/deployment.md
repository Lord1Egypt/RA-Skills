# YOLO Skill 部署指南

本文档说明如何在全新机器上部署 YOLO Skill，实现零配置或最小配置运行。

---

## 目录

1. [系统要求](#系统要求)
2. [快速部署](#快速部署)
3. [手动部署步骤](#手动部署步骤)
4. [模型下载](#模型下载)
5. [常见问题](#常见问题)
6. [平台特定说明](#平台特定说明)

---

## 系统要求

### 硬件
- **摄像头**: 内置或外置 USB 摄像头
- **GPU**: NVIDIA GPU（推荐，CUDA 加速）
  - 如无 GPU，脚本会自动降级到 CPU（速度较慢）
- **内存**: 8GB+ RAM

### 软件
- **Python**: 3.8+
- **CUDA**: 11.8+ (GPU 加速)
- **操作系统**: Linux / Windows / macOS

---

## 快速部署

### Linux / macOS

```bash
# 1. 进入 skill 目录
cd ~/.openclaw/workspace/skills/camera-yolo-operator

# 2. 安装依赖
pip install -r requirements.txt

# 3. 下载模型
bash scripts/download_models.sh

# 4. 运行测试
python3 scripts/capture_webcam.py  # 测试摄像头
python3 scripts/yolo_detection.py  # 测试 YOLO 检测
```

### Windows

```powershell
# 1. 进入 skill 目录
cd $env:USERPROFILE\.openclaw\workspace\skills\camera-yolo-operator

# 2. 安装依赖
pip install -r requirements.txt

# 3. 下载模型（使用 Python 下载）
python scripts\download_models.py

# 4. 运行测试
python scripts/capture_webcam.py
```

---

## 手动部署步骤

### Step 1: 创建工作区目录

```bash
mkdir -p ~/.openclaw/workspace/yolo
mkdir -p ~/.openclaw/workspace/projects/yolo/captures
mkdir -p ~/.openclaw/workspace/projects/yolo/detection
mkdir -p ~/.openclaw/workspace/projects/yolo/depth_distance
```

### Step 2: 安装 Python 依赖

```bash
pip install ultralytics torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install depth-anything-3
pip install opencv-python numpy
```

### Step 3: 下载 YOLO 模型

从 [Ultralytics](https://docs.ultralytics.com/models/yolo11) 下载以下模型到 `~/.openclaw/workspace/yolo/`：

| 模型文件 | 用途 |
|---------|------|
| `yolo26s.pt` | 目标检测（默认）|
| `yolo26s-seg.pt` | 实例分割 |
| `yolo26s-pose.pt` | 姿态估计 |
| `yolo26s-obb.pt` | 旋转框检测 |
| `yolo26s-cls.pt` | 图像分类 |

或使用命令行：

```bash
python3 -c "from ultralytics import YOLO; YOLO('yolo26s.pt')"
```

### Step 4: 验证安装

```bash
# 测试摄像头
python3 scripts/capture_webcam.py --count 3

# 测试 YOLO
python3 scripts/yolo_detection.py --seconds 10

# 测试深度检测
python3 scripts/yolo_depth_distance.py --seconds 10
```

---

## 模型下载

### 方式一: 自动下载脚本

```bash
cd skills/camera-yolo-operator
bash scripts/download_models.sh
```

### 方式二: 手动下载

从以下来源下载：

1. **Ultralytics 官方**: https://docs.ultralytics.com/models/yolo11
2. **HuggingFace**: https://huggingface.co/ultralytics/ (如可用)

### 方式三: Python 下载

```python
from ultralytics import YOLO
model = YOLO('yolo26s.pt')  # 自动下载
```

---

## 常见问题

### Q: HuggingFace 模型下载失败

**原因**: 网络问题或代理干扰

**解决方案**:

1. 清除代理:
```bash
unset all_proxy ALL_PROXY http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
```

2. 使用镜像:
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

3. 或手动下载 DA3Metric-Large:
```bash
git clone https://huggingface.co/depth-anything/DA3Metric-Large ~/.cache/huggingface/modules/depth_anything_3/ddp/
```

### Q: 摄像头无法打开

**解决方案**:

1. 检查摄像头是否被其他应用占用
2. 尝试不同的 camera index:
```bash
python3 scripts/capture_webcam.py --camera-index 0
python3 scripts/capture_webcam.py --camera-index 1
```

3. Linux: 检查设备权限:
```bash
ls -la /dev/video*
# 如果权限不够:
sudo chmod 666 /dev/video0
# 或将用户加入 video 组:
sudo usermod -a -G video $USER
```

### Q: GPU 未被使用

**检查**:

```bash
python3 -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

**解决方案**:

1. 确认 NVIDIA 驱动已安装: `nvidia-smi`
2. 确认 CUDA 版本匹配: `nvcc --version`
3. 重新安装 PyTorch CUDA 版本:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Q: 模型文件找不到

**原因**: 模型未下载或路径错误

**解决**:

1. 运行下载脚本:
```bash
bash scripts/download_models.sh
```

2. 或设置环境变量:
```bash
export YOLO_MODEL_PATH=/path/to/your/yolo26s.pt
```

---

## 平台特定说明

### Linux

- **摄像头后端**: V4L2 (Video4Linux2)
- **设备路径**: `/dev/video0`, `/dev/video1`, ...
- **权限**: 用户需要在 `video` 组中
- **GPU**: 需要 NVIDIA driver + CUDA

### Windows

- **摄像头后端**: DirectShow (DSHOW)
- **设备索引**: 通常 `0` 是默认摄像头
- **GPU**: 需要 NVIDIA driver + CUDA

### macOS

- **摄像头后端**: AVFoundation
- **GPU**: MPS (Apple Silicon) 或 CPU

---

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `OPENCLAW_WORKSPACE` | `~/.openclaw/workspace` | 工作区根目录 |
| `YOLO_MODEL_PATH` | `~/.../workspace/yolo/yolo26s.pt` | YOLO 模型路径 |
| `HF_ENDPOINT` | (官方) | HuggingFace 镜像 |

---

## 目录结构

部署后的完整目录结构：

```
~/.openclaw/workspace/
├── yolo/                          # YOLO 模型文件夹
│   ├── yolo26s.pt
│   ├── yolo26s-seg.pt
│   └── ...
└── projects/yolo/                 # 运行结果
    ├── captures/                  # 原始摄像头抓拍
    ├── detection/                 # YOLO 检测结果
    └── depth_distance/            # 深度+检测结果
```

---

## 故障排查命令

```bash
# 检查 Python 版本
python3 --version

# 检查 PyTorch + CUDA
python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"

# 检查摄像头
python3 -c "import cv2; cap = cv2.VideoCapture(0); print(f'Camera OK: {cap.isOpened()}'); cap.release()"

# 检查模型文件
ls -lh ~/.openclaw/workspace/yolo/*.pt

# 检查依赖
pip list | grep -E "ultralytics|torch|depth-anything|cv2"
```
