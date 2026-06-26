"""Common configuration for all problems."""

from dataclasses import dataclass
import tensorflow as tf


@dataclass
class CommonConfig:
    """通用配置 - 所有问题共享的参数."""
    
    # 问题维度
    dimension: int = 1  # 空间维度（不包括时间）
    
    # 时间边界
    t_low: float = 0.0
    T: float = 1.0
    
    # 空间边界（可以是标量或列表）
    # 对于1D: X_low=0.0, X_high=1.0
    # 对于2D: X_low=[0.0, -1.0], X_high=[1.0, 1.0]
    X_low: any = 0.0
    X_high: any = 1.0
    
    # 网络参数
    num_layers: int = 3
    nodes_per_layer: int = 32
    activation: str = 'swish'
    
    # 训练参数
    sampling_stages: int = 5000
    steps_per_sample: int = 10
    initial_learning_rate: float = 0.001
    end_learning_rate: float = 0.00001
    decay_steps: int = 10000
    decay_power: float = 1.0
    
    # 采样参数
    nSim_interior: int = 2000
    nSim_terminal: int = 1
    X_oversample: float = 0.5
    t_oversample: float = 0.0
    
    # 可视化参数
    n_plot: int = 41
    
    # 保存选项
    saveOutput: bool = True
    save_dir: str = './results'
    
    # 打印配置 - 列出要在训练过程中打印的指标
    # 自动从 metrics 和 losses 中提取
    print_metrics: list = None  # None = 打印所有，或指定列表如 ['maxdiff_V', 'L1', 'L2', 'Z']
    
    # 问题配置 - 在子类中覆盖这些
    num_controls: int = 1
    control_names: list = None  # 如 ['Z', 'alpha', 'beta']
    metrics_config: list = None  # 要记录的指标
    extra_info_mapping: dict = None  # loss extra_info 到 metrics 的映射
    early_stop_metric: str = 'maxdiff_V'
    early_stop_threshold: float = 1e-4
    problem_params_keys: list = None  # 要从 config 自动提取的参数
    
    # 自定义指标计算 - 字典格式: {'指标名': ('操作', [参数名])}
    # 支持操作: 'add', 'subtract', 'multiply', 'divide'
    # 例: {'beta_plus_Z': ('add', ['beta', 'Z'])}
    custom_metrics: dict = None
    
    def get_optimizer_config(self):
        """获取优化器配置."""
        lr_schedule = tf.keras.optimizers.schedules.PolynomialDecay(
            initial_learning_rate=self.initial_learning_rate,
            decay_steps=self.decay_steps,
            end_learning_rate=self.end_learning_rate,
            power=self.decay_power
        )
        return lr_schedule
