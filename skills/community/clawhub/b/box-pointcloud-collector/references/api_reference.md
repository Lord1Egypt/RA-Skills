# API 参考

## 深度图读取

```python
import numpy as np

def load_depth(raw_path, width=640, height=480):
    """
    读取深度图 (.raw 文件)
    
    参数:
        raw_path: .raw 文件路径
        width: 图像宽度（默认 640）
        height: 图像高度（默认 480）
    
    返回:
        numpy.ndarray: 深度图 (height, width), dtype=uint16, 单位 mm
    """
    depth = np.fromfile(raw_path, dtype=np.uint16)
    return depth.reshape(height, width)

# 使用示例
depth = load_depth("raw_data/000001_Depth.raw")
depth_m = depth / 1000.0  # 转换为米

# 获取某点深度
depth_value_mm = depth[v, u]  # 注意：图像坐标是 (y, x)
depth_value_m = depth_value_mm / 1000.0
```

## 彩色图读取

```python
import cv2

def load_color(png_path):
    """
    读取彩色图 (.png 文件)
    
    参数:
        png_path: .png 文件路径
    
    返回:
        numpy.ndarray: 彩色图 (height, width, 3), BGR 格式
    """
    return cv2.imread(png_path)

# 使用示例
color = load_color("raw_data/000001_Color.png")
```

## 坐标转换

### 像素坐标 → 3D 坐标

```python
import json

def load_intrinsics(json_path):
    """加载相机内参"""
    with open(json_path, 'r') as f:
        return json.load(f)

def pixel_to_3d(u, v, depth_m, intrinsics):
    """
    像素坐标转 3D 坐标（相机坐标系）
    
    参数:
        u, v: 像素坐标 (u=x, v=y)
        depth_m: 深度值（米）
        intrinsics: 相机内参字典
    
    返回:
        (X, Y, Z): 3D 坐标（米，相机坐标系）
    """
    fx = intrinsics['fx']
    fy = intrinsics['fy']
    cx = intrinsics['ppx']
    cy = intrinsics['ppy']
    
    Z = depth_m
    X = (u - cx) * Z / fx
    Y = (v - cy) * Z / fy
    
    return X, Y, Z

# 使用示例
intrinsics = load_intrinsics("camera_intrinsic.json")
depth = load_depth("raw_data/000001_Depth.raw")

# 图像中心点
u, v = 320, 240
depth_m = depth[v, u] / 1000.0

X, Y, Z = pixel_to_3d(u, v, depth_m, intrinsics)
print(f"3D 坐标: X={X:.3f}m, Y={Y:.3f}m, Z={Z:.3f}m")
```

### 获取某区域中心 3D 坐标

```python
def get_region_center_3d(depth, bbox, intrinsics):
    """
    获取某区域的中心 3D 坐标
    
    参数:
        depth: 深度图 (H, W)
        bbox: 边界框 (x_min, y_min, x_max, y_max)
        intrinsics: 相机内参
    
    返回:
        (X, Y, Z): 区域中心 3D 坐标
    """
    x_min, y_min, x_max, y_max = bbox
    
    # 取区域中心
    u = (x_min + x_max) // 2
    v = (y_min + y_max) // 2
    
    # 获取深度（取周围 5x5 区域平均）
    depth_region = depth[v-2:v+3, u-2:u+3]
    depth_m = np.mean(depth_region[depth_region > 0]) / 1000.0
    
    return pixel_to_3d(u, v, depth_m, intrinsics)
```

## 点云生成

```python
def depth_to_pointcloud(depth, intrinsics, color=None):
    """
    深度图转点云
    
    参数:
        depth: 深度图 (H, W), 单位 mm
        intrinsics: 相机内参
        color: 可选彩色图 (H, W, 3)
    
    返回:
        points: (N, 3) 点云坐标
        colors: (N, 3) 点云颜色（如果提供 color）
    """
    h, w = depth.shape
    fx, fy = intrinsics['fx'], intrinsics['fy']
    cx, cy = intrinsics['ppx'], intrinsics['ppy']
    
    # 生成像素坐标网格
    u, v = np.meshgrid(np.arange(w), np.arange(h))
    
    # 有效深度掩码
    mask = depth > 0
    
    # 转换为 3D
    z = depth[mask] / 1000.0
    x = (u[mask] - cx) * z / fx
    y = (v[mask] - cy) * z / fy
    
    points = np.stack([x, y, z], axis=-1)
    
    if color is not None:
        colors = color[mask].reshape(-1, 3) / 255.0
        return points, colors
    
    return points

# 使用示例
depth = load_depth("raw_data/000001_Depth.raw")
color = load_color("raw_data/000001_Color.png")
intrinsics = load_intrinsics("camera_intrinsic.json")

points, colors = depth_to_pointcloud(depth, intrinsics, color)
print(f"点云大小: {points.shape}")
```

---

**作者**：Robot_Qu