"""
箱体点云数据处理示例
- 读取彩色图和深度图
- 像素坐标转 3D 坐标
- 计算箱体中心坐标
"""

import numpy as np
import cv2
import json
import os

def load_intrinsics(json_path):
    """加载相机内参"""
    with open(json_path, 'r') as f:
        return json.load(f)

def load_depth(raw_path, width=640, height=480):
    """读取深度图 (.raw 文件)"""
    depth = np.fromfile(raw_path, dtype=np.uint16)
    return depth.reshape(height, width)

def load_color(png_path):
    """读取彩色图"""
    return cv2.imread(png_path)

def pixel_to_3d(u, v, depth_value, intrinsics):
    """
    像素坐标转 3D 坐标
    
    参数:
        u, v: 像素坐标
        depth_value: 深度值（米）
        intrinsics: 相机内参
    
    返回:
        (X, Y, Z) 3D 坐标（米）
    """
    fx = intrinsics['fx']
    fy = intrinsics['fy']
    cx = intrinsics['ppx']
    cy = intrinsics['ppy']
    
    Z = depth_value
    X = (u - cx) * Z / fx
    Y = (v - cy) * Z / fy
    
    return X, Y, Z

def get_depth_at_pixel(depth_image, u, v):
    """获取某像素点的深度值（米）"""
    depth_mm = depth_image[v, u]  # 注意：图像坐标是 (y, x)
    return depth_mm / 1000.0  # 转换为米

def detect_box_center_simple(color_image, depth_image, intrinsics):
    """
    简单的箱体中心检测（示例）
    实际应用中需要更复杂的算法（如 YOLO、深度学习分割等）
    """
    h, w = color_image.shape[:2]
    
    # 这里使用图像中心作为示例
    # 实际应用中应该使用目标检测算法
    center_u = w // 2
    center_v = h // 2
    
    # 获取中心点深度
    depth_m = get_depth_at_pixel(depth_image, center_u, center_v)
    
    # 转换为 3D 坐标
    X, Y, Z = pixel_to_3d(center_u, center_v, depth_m, intrinsics)
    
    return {
        'pixel': (center_u, center_v),
        'depth_m': depth_m,
        'position_3d': (X, Y, Z)
    }

def process_dataset(dataset_dir):
    """处理整个数据集"""
    print(f"处理数据集: {dataset_dir}")
    
    # 加载内参
    intrinsic_path = os.path.join(dataset_dir, 'camera_intrinsic.json')
    if not os.path.exists(intrinsic_path):
        print(f"错误：找不到内参文件 {intrinsic_path}")
        return
    
    intrinsics = load_intrinsics(intrinsic_path)
    print(f"内参: fx={intrinsics['fx']:.2f}, fy={intrinsics['fy']:.2f}")
    
    # 遍历 raw_data 目录
    raw_data_dir = os.path.join(dataset_dir, 'raw_data')
    if not os.path.exists(raw_data_dir):
        print(f"错误：找不到原始数据目录 {raw_data_dir}")
        return
    
    files = os.listdir(raw_data_dir)
    color_files = sorted([f for f in files if f.endswith('_Color.png')])
    
    print(f"\n找到 {len(color_files)} 对图像")
    
    results = []
    
    for color_file in color_files:
        fid = color_file.replace('_Color.png', '')
        depth_file = f"{fid}_Depth.raw"
        
        color_path = os.path.join(raw_data_dir, color_file)
        depth_path = os.path.join(raw_data_dir, depth_file)
        
        if not os.path.exists(depth_path):
            print(f"警告：找不到深度图 {depth_file}")
            continue
        
        # 加载数据
        color = load_color(color_path)
        depth = load_depth(depth_path)
        
        # 检测箱体中心
        result = detect_box_center_simple(color, depth, intrinsics)
        result['frame_id'] = fid
        results.append(result)
        
        print(f"  {fid}: 中心点深度={result['depth_m']:.3f}m, 3D=({result['position_3d'][0]:.3f}, {result['position_3d'][1]:.3f}, {result['position_3d'][2]:.3f})")
    
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        dataset_dir = sys.argv[1]
    else:
        # 默认使用最新的数据集
        base_dir = r"C:\Users\Administrator\.openclaw\workspace\box_dataset"
        dirs = sorted([d for d in os.listdir(base_dir) if d.startswith('box_')], reverse=True)
        if not dirs:
            print("未找到数据集")
            sys.exit(1)
        dataset_dir = os.path.join(base_dir, dirs[0])
    
    results = process_dataset(dataset_dir)
    
    print(f"\n处理完成！共 {len(results)} 帧")