# -*- coding: utf-8 -*-
"""
散点图生成器模块
"""

import os
import matplotlib.pyplot as plt
import matplotlib
from typing import List, Optional

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

from config import SCATTER_PLOT_CONFIG, DEFAULT_OUTPUT_DIR, DEFAULT_OUTPUT_FORMAT
from data_loader import ScatterConfig


class ScatterPlotGenerator:
    """散点图生成器"""

    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR,
                 output_format: str = DEFAULT_OUTPUT_FORMAT,
                 dpi: int = SCATTER_PLOT_CONFIG["dpi"]):
        """
        初始化散点图生成器

        Args:
            output_dir: 输出目录
            output_format: 输出格式（png/pdf等）
            dpi: 图片分辨率
        """
        self.output_dir = output_dir
        self.output_format = output_format
        self.dpi = dpi
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate(self, config: ScatterConfig, show: bool = False) -> str:
        """
        生成单个散点图

        Args:
            config: 散点图配置
            show: 是否显示图片

        Returns:
            保存的文件路径
        """
        # 创建图表
        fig_size = SCATTER_PLOT_CONFIG["figure_size"]
        fig, ax = plt.subplots(figsize=fig_size)

        # 准备数据
        x_data = list(range(1, len(config.result_data) + 1))
        y_data = config.result_data

        # 绘制散点
        ax.scatter(x_data, y_data,
                   marker=SCATTER_PLOT_CONFIG["marker"],
                   s=SCATTER_PLOT_CONFIG["marker_size"],
                   color=SCATTER_PLOT_CONFIG["marker_color"],
                   label='Data Points',
                   zorder=3)

        # 绘制Min Limit线（仅当存在时）
        if config.min_limit is not None:
            ax.axhline(y=config.min_limit,
                      color=SCATTER_PLOT_CONFIG["limit_line_color"],
                      linestyle=SCATTER_PLOT_CONFIG["limit_line_style"],
                      linewidth=SCATTER_PLOT_CONFIG["limit_line_width"],
                      label=f'Min Limit: {config.min_limit}',
                      zorder=2)

        # 绘制Max Limit线（仅当存在时）
        if config.max_limit is not None:
            ax.axhline(y=config.max_limit,
                      color=SCATTER_PLOT_CONFIG["limit_line_color"],
                      linestyle=SCATTER_PLOT_CONFIG["limit_line_style"],
                      linewidth=SCATTER_PLOT_CONFIG["limit_line_width"],
                      label=f'Max Limit: {config.max_limit}',
                      zorder=2)

        # 设置标题（字体增大，更协调美观）
        title = f'{config.item_name} + {config.column_title}'
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

        # 设置X轴
        ax.set_xlabel('Index', fontsize=14)
        ax.set_xlim(0, len(config.result_data) + 1)

        # 设置Y轴
        ax.set_ylabel(config.y_label, fontsize=14)

        # 添加图例
        ax.legend(loc='best', fontsize=10)

        # 添加网格
        ax.grid(True, linestyle=':', alpha=0.6, zorder=1)

        # 调整布局
        plt.tight_layout()

        # 保存图片
        file_name = self._sanitize_filename(title) + f'.{self.output_format}'
        file_path = os.path.join(self.output_dir, file_name)
        plt.savefig(file_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        if show:
            plt.show()

        return file_path

    def generate_batch(self, configs: List[ScatterConfig],
                      show: bool = False) -> List[str]:
        """
        批量生成散点图

        Args:
            configs: 散点图配置列表
            show: 是否显示图片

        Returns:
            保存的文件路径列表
        """
        saved_paths = []

        for config in configs:
            try:
                path = self.generate(config, show=show)
                saved_paths.append(path)
                print(f"已保存: {path}")
            except Exception as e:
                print(f"生成散点图失败 [{config.item_name} + {config.column_title}]: {str(e)}")

        return saved_paths

    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名中的非法字符

        Args:
            filename: 原始文件名

        Returns:
            清理后的文件名
        """
        # 替换非法字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')

        # 限制长度
        max_length = 200
        if len(filename) > max_length:
            filename = filename[:max_length]

        return filename
