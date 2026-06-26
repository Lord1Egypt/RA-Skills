# CivilLabClaw-AI 技能设计文档

**版本：** v1.0  
**创建日期：** 2026-03-20  
**作者：** 智能体 (CivilLabClaw 项目)  
**状态：** 设计完成，待实现

---

## 目录

1. [项目概述](#1-项目概述)
2. [技能架构](#2-技能架构)
3. [子技能详细设计](#3-子技能详细设计)
4. [技术实现方案](#4-技术实现方案)
5. [数据流与接口](#5-数据流与接口)
6. [测试与验证](#6-测试与验证)
7. [部署指南](#7-部署指南)
8. [后续扩展计划](#8-后续扩展计划)

---

## 1. 项目概述

### 1.1 背景与动机

土木工程领域正经历数字化转型，AI 技术在以下方面展现巨大潜力：

| 应用领域 | 传统方法局限 | AI 赋能优势 |
|---------|-------------|------------|
| 结构分析 | 计算成本高、简化假设多 | 代理模型快速预测、不确定性量化 |
| 损伤识别 | 人工检测主观、效率低 | 自动化、客观、可量化 |
| 健康监测 | 阈值报警误报率高 | 数据驱动异常检测、早期预警 |
| 数字孪生 | 模型更新滞后 | 实时数据同化、在线预测 |

### 1.2 目标与定位

**目标：** 为土木工程师和研究人员提供一套开箱即用的 AI 工具包，降低 AI 技术使用门槛。

**定位：**
- 🎯 **应用导向**：解决实际问题，而非纯算法研究
- 🔧 **工具化**：命令行/自然语言调用，无需编程
- 📦 **模块化**：4 个子技能可独立使用或组合
- 🔄 **可扩展**：预留接口，支持新算法/新场景

### 1.3 目标用户

| 用户类型 | 典型需求 | 使用频率 |
|---------|---------|---------|
| 科研人员 | 论文方法实现、数据分析 | 高 |
| 工程师 | 快速评估、损伤检测 | 中 |
| 学生 | 学习 AI+ 土木交叉方法 | 中 |
| 实验室 | 试验数据处理、实时监测 | 高 |

---

## 2. 技能架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    CivilLabClaw-AI Skill                    │
├─────────────────────────────────────────────────────────────┤
│  Natural Language Interface (OpenClaw)                      │
├─────────────────────────────────────────────────────────────┤
│  Task Router & Orchestrator                                 │
│  - 意图识别  - 任务分发  - 结果整合                         │
├──────────────┬──────────────┬──────────────┬───────────────┤
│  ML-Struct   │  DL-Damage   │ DigitalTwin  │ SmartMonitor  │
│  机器学习    │  深度学习    │   数字孪生   │   智能监测    │
├──────────────┴──────────────┴──────────────┴───────────────┤
│  Common Utilities                                           │
│  - 数据预处理  - 可视化  - 报告生成  - 模型管理            │
├─────────────────────────────────────────────────────────────┤
│  Backend                                                    │
│  - PyTorch/TensorFlow  - Scikit-learn  - OpenCV  - HDF5    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 模块依赖关系

```
CivilLabClaw-AI
├── core/                    # 核心逻辑
│   ├── router.py           # 任务路由
│   ├── orchestrator.py     # 流程编排
│   └── config.py           # 配置管理
├── ml_struct/              # 机器学习结构分析
│   ├── models/             # 预训练模型
│   ├── predictors.py       # 预测器
│   └── uncertainty.py      # 不确定性量化
├── dl_damage/              # 深度学习损伤识别
│   ├── models/             # CNN/YOLO 模型
│   ├── detector.py         # 检测器
│   └── postprocess.py      # 后处理
├── digital_twin/           # 数字孪生
│   ├── fem_interface.py    # FEM 接口
│   ├── rom.py              # 降阶模型
│   └── data_assimilation.py # 数据同化
├── smart_monitor/          # 智能监测
│   ├── preprocessing.py    # 数据预处理
│   ├── features.py         # 特征提取
│   ├── modal.py            # 模态分析
│   └── anomaly.py          # 异常检测
├── utils/                  # 通用工具
│   ├── io.py               # 输入输出
│   ├── viz.py              # 可视化
│   └── report.py           # 报告生成
└── tests/                  # 测试
    ├── test_ml_struct.py
    ├── test_dl_damage.py
    ├── test_digital_twin.py
    └── test_smart_monitor.py
```

---

## 3. 子技能详细设计

### 3.1 ML-Struct（机器学习结构分析）

#### 3.1.1 功能定义

使用机器学习方法预测结构响应、评估性能、辅助设计决策。

#### 3.1.2 支持任务

| 任务 | 输入 | 输出 | 推荐算法 |
|------|------|------|---------|
| 地震响应预测 | 结构参数 + 地震动 | 位移/加速度时程 | GPR/NN |
| 承载力评估 | 截面 + 材料 + 配筋 | 承载力 + 可靠度 | XGBoost |
| 模型修正 | FEM + 试验数据 | 修正参数 + 置信区间 | 贝叶斯更新 |
| 参数敏感性 | 设计变量范围 | 敏感性排序 | Sobol/GPR |

#### 3.1.3 算法选型

**高斯过程回归 (GPR)：**
- 优势：小样本、不确定性量化、无需大量训练
- 局限：大数据集计算成本高
- 适用：参数研究、可靠性分析

**神经网络 (NN)：**
- 优势：复杂非线性、大数据集
- 局限：需要大量训练数据、黑箱
- 适用：复杂结构响应预测

**集成方法 (XGBoost/LightGBM)：**
- 优势：训练快、可解释性好
- 局限：外推能力有限
- 适用：分类任务、特征重要性分析

#### 3.1.4 数据需求

```python
# 训练数据格式示例
{
    "features": [
        "num_stories",      # 层数
        "story_height",     # 层高
        "bay_width",        # 跨度
        "concrete_strength", # 混凝土强度
        "steel_grade",      # 钢筋等级
        "pga",              # 峰值加速度
        "spectral_accel"    # 谱加速度
    ],
    "targets": [
        "max_idr",          # 最大层间位移角
        "max_accel",        # 最大加速度
        "base_shear"        # 基底剪力
    ]
}
```

#### 3.1.5 输出示例

```json
{
    "task": "地震响应预测",
    "model": "GPR",
    "predictions": {
        "max_idr": {
            "mean": 0.0125,
            "std": 0.0023,
            "ci_95": [0.0080, 0.0170]
        },
        "max_accel": {
            "mean": 0.35,
            "std": 0.08,
            "ci_95": [0.19, 0.51]
        }
    },
    "feature_importance": {
        "pga": 0.45,
        "num_stories": 0.25,
        "concrete_strength": 0.15
    },
    "confidence": "高",
    "recommendations": [
        "预测不确定性主要来自材料变异性",
        "建议增加混凝土强度测试数据"
    ]
}
```

---

### 3.2 DL-Damage（深度学习损伤识别）

#### 3.2.1 功能定义

使用计算机视觉和深度学习技术自动识别和量化结构损伤。

#### 3.2.2 支持任务

| 任务 | 输入 | 输出 | 模型 |
|------|------|------|------|
| 裂缝检测 | 单张图像 | 裂缝位置 + 宽度 | CNN |
| 多损伤识别 | 图像/视频 | 损伤类型 + 位置 | YOLO |
| 损伤分割 | 高分辨率图像 | 像素级分割 | Mask R-CNN |
| 时序损伤演化 | 多时相图像 | 损伤发展曲线 | CNN+LSTM |

#### 3.2.3 模型架构

**裂缝检测 CNN：**
```
输入 (224x224x3)
    ↓
Conv2D(32, 3x3) + BN + ReLU
    ↓
MaxPool(2x2)
    ↓
Conv2D(64, 3x3) + BN + ReLU
    ↓
MaxPool(2x2)
    ↓
Conv2D(128, 3x3) + BN + ReLU
    ↓
GlobalAvgPool
    ↓
Dense(128) + Dropout(0.5)
    ↓
Dense(num_classes) + Softmax
```

**YOLO 损伤检测：**
- Backbone: CSPDarknet53
- Neck: PANet
- Head: YOLOv5 Head
- 输入：640x640
- 输出：损伤框 + 类别 + 置信度

#### 3.2.4 数据集

| 数据集 | 规模 | 损伤类型 | 来源 |
|--------|------|---------|------|
| SDNET2018 | 56,000 张 | 裂缝、剥落、锈蚀 | 公开 |
| Crack500 | 2,000 张 | 道路裂缝 | 公开 |
| 自建数据集 | 可扩展 | 自定义 | 用户上传 |

#### 3.2.5 评估指标

```python
metrics = {
    "precision": TP / (TP + FP),
    "recall": TP / (TP + FN),
    "mAP": mean_average_precision,
    "IoU": intersection_over_union,
    "inference_time": "ms per image"
}
```

#### 3.2.6 输出示例

```json
{
    "image_id": "test_001.jpg",
    "detections": [
        {
            "type": "crack",
            "bbox": [120, 45, 380, 95],
            "confidence": 0.94,
            "width_mm": 0.35,
            "length_mm": 125
        },
        {
            "type": "spalling",
            "bbox": [450, 200, 520, 280],
            "confidence": 0.87,
            "area_cm2": 12.5
        }
    ],
    "summary": {
        "total_detections": 2,
        "max_severity": "中等",
        "recommendation": "建议进一步检测"
    },
    "visualization": "annotated_test_001.jpg"
}
```

---

### 3.3 DigitalTwin（数字孪生）

#### 3.3.1 功能定义

构建结构的数字孪生模型，实现实时状态感知、仿真预测和健康评估。

#### 3.3.2 架构层次

```
┌─────────────────────────────────────┐
│         服务层 (Services)           │
│  健康评估 | 预警 | 决策支持         │
├─────────────────────────────────────┤
│         模型层 (Models)             │
│  FEM | ROM | 数据驱动模型           │
├─────────────────────────────────────┤
│         数据层 (Data)               │
│  采集 | 传输 | 存储 | 清洗          │
├─────────────────────────────────────┤
│         物理层 (Physical)           │
│  实际结构 | 传感器 | 作动器         │
└─────────────────────────────────────┘
```

#### 3.3.3 模型类型

| 模型类型 | 精度 | 计算速度 | 适用场景 |
|---------|------|---------|---------|
| 高保真 FEM | ★★★★★ | 慢 (分钟级) | 离线分析、设计验证 |
| 降阶模型 ROM | ★★★★☆ | 快 (毫秒级) | 实时孪生、控制 |
| 数据驱动 | ★★★☆☆ | 很快 (微秒级) | 快速预测、监测 |

#### 3.3.4 降阶方法

**本征正交分解 (POD)：**
```python
# 快照矩阵
X = [u(t1), u(t2), ..., u(tn)]  # n 个时间步的位移场

# SVD 分解
X = U @ Σ @ V^T

# 保留前 r 阶模态
U_r = U[:, :r]

# 降阶坐标
q = U_r^T @ u
```

**系统识别：**
```python
# 状态空间模型
x(k+1) = A @ x(k) + B @ u(k)
y(k) = C @ x(k) + D @ u(k)

# 使用 ERA/SSI 识别系统矩阵
A, B, C, D = era(hankel_matrix)
```

#### 3.3.5 数据同化

**卡尔曼滤波：**
```python
# 预测步
x_pred = A @ x
P_pred = A @ P @ A^T + Q

# 更新步
K = P_pred @ H^T @ (H @ P_pred @ H^T + R)^(-1)
x = x_pred + K @ (y - H @ x_pred)
P = (I - K @ H) @ P_pred
```

#### 3.3.6 输出示例

```json
{
    "twin_id": "bridge_001",
    "timestamp": "2026-03-20T10:30:00Z",
    "state": {
        "displacement": {
            "node_125": [0.012, -0.003, 0.045],
            "node_256": [0.008, -0.001, 0.032]
        },
        "stress": {
            "element_89": 45.2,  # MPa
            "element_156": 38.7
        }
    },
    "health_index": 0.92,
    "anomalies": [],
    "prediction": {
        "next_1h_max_disp": 0.055,
        "confidence": 0.88
    }
}
```

---

### 3.4 SmartMonitor（智能监测）

#### 3.4.1 功能定义

对结构健康监测数据进行自动化分析，提取特征、识别状态、检测异常。

#### 3.4.2 分析流程

```
原始数据 → 预处理 → 特征提取 → 状态识别 → 报告生成
   ↓          ↓          ↓           ↓           ↓
  CSV      去噪/      时域/      模态/      PDF/
  MAT      归一化     频域      损伤检测    Markdown
```

#### 3.4.3 特征提取

**时域特征：**
```python
features_time = {
    "mean": np.mean(x),
    "std": np.std(x),
    "rms": np.sqrt(np.mean(x**2)),
    "peak": np.max(np.abs(x)),
    "kurtosis": kurtosis(x),
    "skewness": skewness(x),
    "crest_factor": peak / rms
}
```

**频域特征：**
```python
features_freq = {
    "dominant_freq": freq[np.argmax(fft_mag)],
    "spectral_centroid": np.sum(f * fft_mag) / np.sum(fft_mag),
    "spectral_bandwidth": ...,
    "modal_frequencies": [f1, f2, f3, ...]
}
```

#### 3.4.4 模态分析

**频域分解 (FDD)：**
```python
# 功率谱密度矩阵
S_yy(ω) = E[Y(ω) @ Y(ω)^H]

# SVD 分解
S_yy(ω) = U(ω) @ Σ(ω) @ U(ω)^H

# 峰值识别固有频率
freq_peaks = find_peaks(Σ[0, :])
```

**随机子空间识别 (SSI)：**
```python
# 构建 Hankel 矩阵
H = [
    [Y(0), Y(1), ..., Y(j)],
    [Y(1), Y(2), ..., Y(j+1)],
    ...
]

# SVD + 最小二乘
A, C = ssi_data(H)

# 提取模态参数
freq, damping, mode_shapes = extract_modal(A, C)
```

#### 3.4.5 异常检测

**自编码器方法：**
```python
# 训练自编码器
encoder: x → z (压缩表示)
decoder: z → x̂ (重构)

# 异常分数
reconstruction_error = ||x - x̂||²

# 阈值
threshold = percentile(train_errors, 99)
is_anomaly = reconstruction_error > threshold
```

#### 3.4.6 输出示例

```json
{
    "analysis_id": "monitor_20260320_001",
    "data_summary": {
        "duration": "3600s",
        "sampling_rate": "200Hz",
        "channels": 8,
        "missing_rate": 0.001
    },
    "modal_parameters": {
        "mode_1": {"freq": 2.45, "damping": 0.023, "shape": [...]},
        "mode_2": {"freq": 7.82, "damping": 0.018, "shape": [...]},
        "mode_3": {"freq": 15.34, "damping": 0.015, "shape": [...]}
    },
    "anomalies": [
        {
            "timestamp": "2026-03-20T09:15:23Z",
            "type": "frequency_shift",
            "severity": "低",
            "description": "一阶频率下降 2.1%"
        }
    ],
    "trend": {
        "freq_1_7day": [-0.5, -0.8, -1.2, -1.5, -2.1],
        "interpretation": "轻微下降趋势，建议关注"
    },
    "report": "monitor_report_20260320.pdf"
}
```

---

## 4. 技术实现方案

### 4.1 开发环境

```yaml
python: 3.9+
os: Windows 10/11
gpu: NVIDIA CUDA 11.7+ (可选)
ide: VS Code / PyCharm
```

### 4.2 依赖包

```txt
# 核心科学计算
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0

# 机器学习
scikit-learn>=1.0.0
xgboost>=1.5.0
lightgbm>=3.3.0
gpytorch>=1.8.0

# 深度学习
torch>=1.10.0
torchvision>=0.11.0
opencv-python>=4.5.0

# 信号处理
pywt>=1.3.0  # 小波
modalpy>=0.1.0  # 模态分析

# 可视化
matplotlib>=3.5.0
plotly>=5.5.0
seaborn>=0.11.0

# 数据格式
h5py>=3.6.0
hdf5storage>=0.1.18

# 报告生成
jinja2>=3.0.0
weasyprint>=55.0  # PDF 生成
```

### 4.3 项目结构

```
CivilLabClaw-AI/
├── __init__.py
├── main.py                 # 入口
├── config/
│   ├── default.yaml        # 默认配置
│   └── models.yaml         # 模型配置
├── src/
│   ├── core/
│   ├── ml_struct/
│   ├── dl_damage/
│   ├── digital_twin/
│   └── smart_monitor/
├── models/                 # 预训练模型
│   ├── ml_struct/
│   ├── dl_damage/
│   └── digital_twin/
├── data/                   # 示例数据
│   ├── sample_csv/
│   ├── sample_images/
│   └── sample_mat/
├── outputs/                # 输出目录
├── tests/
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

### 4.4 核心代码框架

```python
# src/core/router.py
from enum import Enum
from typing import Dict, Any

class SkillType(Enum):
    ML_STRUCT = "ml_struct"
    DL_DAMAGE = "dl_damage"
    DIGITAL_TWIN = "digital_twin"
    SMART_MONITOR = "smart_monitor"

class TaskRouter:
    def __init__(self):
        self.skills = self._load_skills()
    
    def route(self, intent: str, params: Dict[str, Any]) -> Dict[str, Any]:
        skill_type = self._classify_intent(intent)
        skill = self.skills[skill_type]
        return skill.execute(params)
    
    def _classify_intent(self, intent: str) -> SkillType:
        # 意图分类逻辑
        pass
```

```python
# src/ml_struct/predictor.py
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor

class StructuralPredictor:
    def __init__(self, model_type: str = "gpr"):
        self.model_type = model_type
        self.model = self._load_model()
    
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        pred = self.model.predict(features, return_std=True)
        return {
            "mean": pred[0],
            "std": pred[1],
            "ci_95": self._confidence_interval(pred)
        }
    
    def _load_model(self):
        # 加载预训练模型
        pass
```

---

## 5. 数据流与接口

### 5.1 输入接口

**自然语言输入：**
```
用户："分析这张裂缝图片"
     ↓
意图识别：dl_damage + image_classification
     ↓
参数提取：{"image_path": "xxx.jpg"}
     ↓
执行技能
```

**文件输入：**
- CSV: 传感器数据、结构参数
- Excel: 试验数据、设计参数
- MAT: MATLAB 数据
- Images: JPG/PNG 损伤图片
- HDF5: 大型数据集

### 5.2 输出接口

**结构化数据：**
- JSON: 分析结果
- CSV: 处理后的数据
- MAT: MATLAB 兼容格式

**可视化：**
- PNG/SVG: 图表
- PDF: 完整报告
- HTML: 交互式报告

**API 接口（未来）：**
```python
# REST API 示例
POST /api/v1/ml_struct/predict
Content-Type: application/json

{
    "structure_params": {...},
    "load_params": {...}
}

Response:
{
    "predictions": {...},
    "visualization_url": "..."
}
```

### 5.3 与其他技能集成

```
CivilLabClaw-AI
    ↓
structural-testing  # 试验方案、术语
    ↓
matlab-bridge       # 数据交换、联合仿真
    ↓
paper-assistant     # 论文写作
    ↓
research-paper-writer  # 学术论文
```

---

## 6. 测试与验证

### 6.1 单元测试

```python
# tests/test_ml_struct.py
def test_gpr_prediction():
    predictor = StructuralPredictor(model_type="gpr")
    features = np.array([[3, 3.5, 5, 30, 400, 0.3]])
    result = predictor.predict(features)
    
    assert "mean" in result
    assert "std" in result
    assert result["mean"].shape == (1,)

def test_dl_damage_detection():
    detector = DamageDetector()
    image = load_test_image()
    result = detector.detect(image)
    
    assert "detections" in result
    assert len(result["detections"]) >= 0
```

### 6.2 集成测试

```python
# tests/test_integration.py
def test_end_to_end_workflow():
    # 模拟完整工作流
    router = TaskRouter()
    
    # 测试 ML 预测
    result = router.route("预测结构响应", {
        "num_stories": 5,
        "pga": 0.3
    })
    assert result["status"] == "success"
    
    # 测试损伤识别
    result = router.route("识别裂缝", {
        "image": "test_crack.jpg"
    })
    assert result["status"] == "success"
```

### 6.3 验证数据集

| 子技能 | 验证数据 | 来源 | 规模 |
|--------|---------|------|------|
| ML-Struct | 框架结构地震响应 | OpenSees 仿真 | 1000 组 |
| DL-Damage | 混凝土裂缝图片 | SDNET2018 | 500 张 |
| DigitalTwin | 振动台试验数据 | 自建 | 10 组试验 |
| SmartMonitor | 加速度时程 | 公开数据集 | 100 组 |

### 6.4 性能指标

| 指标 | 目标值 | 测量方法 |
|------|--------|---------|
| ML 预测误差 | < 10% | MAPE |
| 损伤识别准确率 | > 90% | mAP |
| 数字孪生更新延迟 | < 100ms | 端到端延迟 |
| 监测分析吞吐量 | > 1000 样本/s | 批处理速度 |

---

## 7. 部署指南

### 7.1 环境配置

**步骤 1: 创建虚拟环境**
```bash
cd D:\Personal\OpenClaw\skills\CivilLabClaw-AI
python -m venv venv
venv\Scripts\activate
```

**步骤 2: 安装依赖**
```bash
pip install -r requirements.txt
```

**步骤 3: 下载预训练模型**
```bash
python scripts/download_models.py
```

**步骤 4: 配置路径**
```yaml
# config/default.yaml
output_dir: D:\Personal\OpenClaw\civil-ai-outputs
model_dir: D:\Personal\OpenClaw\skills\CivilLabClaw-AI\models
data_dir: D:\Personal\OpenClaw\skills\CivilLabClaw-AI\data
```

### 7.2 快速测试

```bash
# 测试 ML 预测
python main.py ml_struct --test

# 测试损伤识别
python main.py dl_damage --test --image data/sample_images/crack_001.jpg

# 测试监测分析
python main.py smart_monitor --test --data data/sample_csv/vibration.csv
```

### 7.3 OpenClaw 集成

在 OpenClaw 中调用：
```
"激活 CivilLabClaw-AI 技能"
"用 ML-Struct 预测结构响应"
"帮我分析这张裂缝图片"
```

---

## 8. 后续扩展计划

### 8.1 短期（1-3 个月）

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 预训练模型完善 | P0 | 覆盖典型场景 |
| 可视化增强 | P0 | 交互式图表 |
| 报告模板 | P1 | 标准化报告格式 |
| 批量处理 | P1 | 支持多文件处理 |

### 8.2 中期（3-6 个月）

| 功能 | 优先级 | 说明 |
|------|--------|------|
| Web 界面 | P1 | 图形化操作界面 |
| API 服务 | P2 | RESTful API |
| 更多预训练模型 | P1 | 扩展应用场景 |
| 不确定性量化增强 | P2 | 贝叶斯深度学习 |

### 8.3 长期（6-12 个月）

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 实时数字孪生 | P1 | 与传感器实时连接 |
| 联邦学习 | P3 | 多机构协作训练 |
| 自动机器学习 | P2 | AutoML 超参优化 |
| 物理信息神经网络 | P2 | PINN 融合物理约束 |

### 8.4 潜在研究方向

1. **物理信息机器学习**：将物理定律嵌入神经网络
2. **迁移学习**：跨结构类型迁移预训练模型
3. **主动学习**：智能选择最有价值的训练样本
4. **可解释 AI**：提高模型透明度和可信度
5. **多模态融合**：视觉 + 传感器数据联合分析

---

## 附录

### A. 术语表

| 术语 | 英文 | 解释 |
|------|------|------|
| RTHS | Real-Time Hybrid Simulation | 实时混合试验 |
| FEM | Finite Element Method | 有限元方法 |
| ROM | Reduced Order Model | 降阶模型 |
| GPR | Gaussian Process Regression | 高斯过程回归 |
| CNN | Convolutional Neural Network | 卷积神经网络 |
| FDD | Frequency Domain Decomposition | 频域分解 |
| SSI | Stochastic Subspace Identification | 随机子空间识别 |

### B. 参考资源

**书籍：**
- "Machine Learning in Structural Engineering" - Salehi
- "Deep Learning for Computer Vision" - Rajalingappaa
- "Digital Twin: Technology and Applications" - Tao

**开源项目：**
- [OpenSeesPy](https://openseespydoc.readthedocs.io/)
- [PyTorch](https://pytorch.org/)
- [Scikit-learn](https://scikit-learn.org/)

**数据集：**
- [SDNET2018](https://sdnet2018.github.io/)
- [Crack500](https://github.com/leochan1117/Crack500)

---

_文档版本：v1.0_  
_创建日期：2026-03-20_  
_状态：设计完成，待实现_

