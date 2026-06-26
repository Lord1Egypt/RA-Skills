"""
可视化工具

功能：
- 时程曲线
- 频谱图
- 模态振型
- 损伤标注图
"""

import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Any


def plot_time_history(data: np.ndarray, timestamps: Optional[np.ndarray] = None,
                      save_path: Optional[Path] = None, show: bool = False):
    """
    绘制时程曲线
    
    Args:
        data: 数据 (n_samples, n_channels)
        timestamps: 时间戳
        save_path: 保存路径
        show: 是否显示
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(data.shape[1], 1, figsize=(10, 2*data.shape[1]))
    if data.shape[1] == 1:
        axes = [axes]
    
    for i, ax in enumerate(axes):
        if timestamps is not None:
            ax.plot(timestamps, data[:, i])
        else:
            ax.plot(data[:, i])
        ax.set_ylabel(f'Channel {i+1}')
        ax.grid(True, alpha=0.3)
    
    if timestamps is not None:
        axes[-1].set_xlabel('Time (s)')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_spectrum(data: np.ndarray, fs: float, save_path: Optional[Path] = None,
                  show: bool = False):
    """
    绘制频谱图
    
    Args:
        data: 数据
        fs: 采样率 (Hz)
        save_path: 保存路径
        show: 是否显示
    """
    import matplotlib.pyplot as plt
    from scipy import signal
    
    n_channels = data.shape[1] if len(data.shape) > 1 else 1
    
    fig, axes = plt.subplots(n_channels, 1, figsize=(10, 3*n_channels))
    if n_channels == 1:
        axes = [axes]
    
    for i, ax in enumerate(axes):
        f, Pxx = signal.welch(data[:, i] if n_channels > 1 else data, fs, nperseg=1024)
        ax.semilogy(f, Pxx)
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('PSD')
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, fs/2])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_mode_shapes(mode_shapes: List[np.ndarray], save_path: Optional[Path] = None,
                     show: bool = False):
    """
    绘制模态振型
    
    Args:
        mode_shapes: 模态振型列表
        save_path: 保存路径
        show: 是否显示
    """
    import matplotlib.pyplot as plt
    
    n_modes = len(mode_shapes)
    fig, axes = plt.subplots(1, n_modes, figsize=(5*n_modes, 6))
    if n_modes == 1:
        axes = [axes]
    
    for i, ax in enumerate(axes):
        shape = mode_shapes[i]
        heights = np.arange(len(shape))
        ax.plot(shape, heights, 'o-', linewidth=2, markersize=8)
        ax.set_xlabel('Amplitude')
        ax.set_ylabel('Height')
        ax.set_title(f'Mode {i+1}')
        ax.grid(True, alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {save_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def annotate_damage(image: Any, detections: List[Dict[str, Any]], 
                    save_path: Optional[Path] = None, show: bool = False):
    """
    标注损伤检测结果
    
    Args:
        image: 输入图像
        detections: 检测结果列表
        save_path: 保存路径
        show: 是否显示
    """
    from PIL import Image, ImageDraw, ImageFont
    
    # 转换为 PIL Image
    if isinstance(image, np.ndarray):
        img = Image.fromarray(image)
    elif isinstance(image, Image.Image):
        img = image
    else:
        img = Image.open(image)
    
    draw = ImageDraw.Draw(img)
    
    # 颜色映射
    colors = {
        'crack': (255, 0, 0),      # 红色
        'spalling': (0, 255, 0),   # 绿色
        'corrosion': (0, 0, 255),  # 蓝色
    }
    
    for det in detections:
        bbox = det['bbox']
        det_type = det['type']
        confidence = det['confidence']
        
        color = colors.get(det_type, (255, 255, 0))
        
        # 绘制边界框
        draw.rectangle(bbox, outline=color, width=3)
        
        # 绘制标签
        label = f"{det_type}: {confidence:.2f}"
        draw.text((bbox[0], bbox[1]-20), label, fill=color)
    
    if save_path:
        img.save(save_path)
        print(f"Saved to {save_path}")
    
    if show:
        img.show()
    
    return img
