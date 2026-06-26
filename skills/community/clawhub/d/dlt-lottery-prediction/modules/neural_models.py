"""
神经网络模型模块 (neural_models.py)

占位模块：TabNet / LSTM / Transformer 等神经网络模型尚未实现。
当前 DLT 预测系统基于 LightGBM + 贝叶斯模型，暂不需要神经网络组件。

如需启用，请安装依赖：
    pip install torch torch-geometric pytorch-tabnet

预留接口（暂未实现）：
    - NeuralEnsemble
    - TabNetTrainer
    - LSTMTrainer  
    - TransformerTrainer
    - NeuralFeatureBuilder
"""

__all__ = [
    'NeuralEnsemble',
    'TabNetTrainer',
    'LSTMTrainer',
    'TransformerTrainer',
    'NeuralFeatureBuilder',
]


class NeuralEnsemble:
    """神经网络集成器（占位）"""
    pass


class TabNetTrainer:
    """TabNet训练器（占位）"""
    pass


class LSTMTrainer:
    """LSTM训练器（占位）- 预留 Attention 层实现"""
    pass


class TransformerTrainer:
    """Transformer训练器（占位）"""
    pass


class NeuralFeatureBuilder:
    """神经网络特征构建器（占位）"""
    pass


# Alias for framework compatibility
DLTFusionNet = NeuralEnsemble
