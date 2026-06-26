---
name: CivilLabClaw-AI
description: "AI+ 土木交叉方向技能包 - 机器学习、深度学习损伤识别、数字孪生、智能监测数据分析"
metadata:
  openclaw:
    emoji: 🤖🏗️
---

# CivilLabClaw-AI 技能包

## 🎯 一句话定义

为土木工程领域提供 AI 赋能的专业技能支持，涵盖机器学习在结构工程中的应用、深度学习损伤识别、数字孪生建模、智能监测数据分析等交叉方向。

---

## 📦 技能包组成

本技能包包含以下 4 个子技能模块：

| 子技能 | 功能 | 触发语句 |
|--------|------|----------|
| **ML-Struct** | 机器学习在结构工程中的应用 | "ML 结构分析" / "机器学习预测" |
| **DL-Damage** | 深度学习损伤识别 | "损伤识别" / "裂缝检测" |
| **DigitalTwin** | 数字孪生建模与仿真 | "数字孪生" / "孪生模型" |
| **SmartMonitor** | 智能监测数据分析 | "监测数据分析" / "传感器数据" |

---

## 📥 如何调用 (How to use me)

### 方式一：直接激活子技能

**触发语句：**
- "激活 ML-Struct 技能"
- "使用损伤识别功能"
- "帮我建立数字孪生模型"
- "分析监测数据"

### 方式二：自然语言描述任务

**触发语句：**
- "用机器学习预测结构响应"
- "识别图片中的裂缝"
- "建立桥梁的数字孪生模型"
- "分析振动台试验的传感器数据"

**需要提供的信息：**
1. **必需：** 任务类型 + 数据/输入
2. **可选：** 模型偏好、精度要求、输出格式

---

## 🔄 执行逻辑 (What I do)

### Step 1: 任务识别与分类
- 解析用户意图，匹配到对应子技能
- 确认输入数据类型（文本/图片/时序数据/模型文件）
- 验证数据完整性与格式

### Step 2: 子技能执行

#### 🔹 ML-Struct（机器学习结构分析）
```
输入：结构参数、荷载条件、材料属性
↓
选择模型：回归/分类/聚类
↓
训练/预测：使用预训练模型或新训练
↓
输出：预测结果 + 置信度 + 特征重要性
```

#### 🔹 DL-Damage（深度学习损伤识别）
```
输入：结构图像/视频/传感器数据
↓
预处理：图像增强/去噪/归一化
↓
模型推理：CNN/YOLO/Transformer
↓
后处理：损伤定位/量化/分级
↓
输出：损伤位置 + 类型 + 严重程度 + 可视化
```

#### 🔹 DigitalTwin（数字孪生）
```
输入：几何模型 + 材料参数 + 边界条件
↓
模型构建：FEM/降阶模型/数据驱动
↓
实时更新：传感器数据同化
↓
仿真预测：响应预测 + 健康评估
↓
输出：孪生模型 + 实时状态 + 预测结果
```

#### 🔹 SmartMonitor（智能监测）
```
输入：传感器时序数据（加速度/位移/应变等）
↓
数据清洗：异常值处理/缺失值插补
↓
特征提取：时域/频域/时频分析
↓
状态识别：模态识别/损伤检测/趋势预测
↓
输出：分析报告 + 异常预警 + 可视化图表
```

### Step 3: 结果验证与交付
- 自检：结果合理性检查
- 不确定性量化：置信区间/误差估计
- 交付：结构化报告 + 可视化 + 原始数据

---

## 📚 核心知识库

### 1. 机器学习在结构工程中的应用

**典型场景：**
| 任务 | 算法 | 输入 | 输出 |
|------|------|------|------|
| 结构响应预测 | GPR/SVR/NN | 荷载、几何、材料 | 位移、应力、加速度 |
| 损伤检测 | 分类器 (RF/SVM) | 模态参数、响应 | 损伤位置/程度 |
| 模型修正 | 贝叶斯更新 | 试验数据、FEM | 更新参数 |
| 可靠性分析 | 代理模型 | 随机变量 | 失效概率 |

**推荐工具：**
- Scikit-learn（传统 ML）
- PyTorch/TensorFlow（深度学习）
- GPy/GPyTorch（高斯过程）

### 2. 深度学习损伤识别

**主流方法：**
| 方法 | 适用场景 | 精度 | 速度 |
|------|---------|------|------|
| CNN 分类 | 裂缝/剥落/锈蚀识别 | 高 | 快 |
| YOLO/SSD | 实时损伤检测 | 中高 | 很快 |
| Mask R-CNN | 损伤分割 | 很高 | 中 |
| Transformer | 复杂场景理解 | 高 | 慢 |

**数据集：**
- SDNET2018（混凝土裂缝）
- Crack500（道路裂缝）
- AEL（钢结构损伤）

### 3. 数字孪生技术

**架构层次：**
```
物理层（实际结构）
    ↓ ↑ 传感器/作动器
数据层（数据采集/传输）
    ↓ ↑ 模型更新
模型层（FEM/ROM/数据驱动）
    ↓ ↑ 仿真预测
服务层（健康评估/预警/决策）
```

**关键技术：**
- 模型降阶（ROM）：POD、系统识别
- 数据同化：卡尔曼滤波、粒子滤波
- 实时仿真：GPU 加速、并行计算

### 4. 智能监测数据分析

**分析流程：**
```
原始数据 → 预处理 → 特征提取 → 状态识别 → 决策支持
```

**常用特征：**
- 时域：均值、方差、峰值、峭度
- 频域：固有频率、振型、阻尼比
- 时频：小波系数、Hilbert-Huang

**异常检测方法：**
- 统计方法：控制图、马氏距离
- ML 方法：自编码器、One-Class SVM
- 深度学习方法：LSTM-AE

---

## 📝 使用示例

### 示例 1: 机器学习预测结构响应
```
用户："用机器学习预测框架结构在地震作用下的层间位移角"

我：
## ML 结构响应预测

### 输入需求
请提供以下信息：
1. **结构参数**：层数、跨度、层高、截面尺寸
2. **材料属性**：混凝土强度、钢筋等级
3. **地震动参数**：PGA、频谱特性
4. **数据集**：如有历史数据可上传（CSV/Excel）

### 可选模型
| 模型 | 适用场景 | 精度 | 训练时间 |
|------|---------|------|---------|
| 高斯过程回归 | 小样本、不确定性量化 | 高 | 短 |
| 神经网络 | 大样本、复杂非线性 | 很高 | 中 |
| XGBoost | 中等样本、快速训练 | 中高 | 很短 |

### 输出内容
- 预测的层间位移角时程
- 最大层间位移角及位置
- 预测置信区间（95%）
- 特征重要性分析

请提供数据或选择使用预训练模型（基于典型框架结构）。
```

### 示例 2: 深度学习损伤识别
```
用户："帮我识别这张图片中的混凝土裂缝"

我：
## 深度学习损伤识别

### 分析流程
1. ✅ 图像接收（请上传图片）
2. 🔲 预处理：对比度增强、去噪
3. 🧠 模型推理：使用预训练 CNN 模型
4. 📊 结果输出：裂缝位置、宽度、长度

### 输出格式
```
损伤类型：混凝土裂缝
位置：[x1, y1, x2, y2]
最大宽度：0.35 mm
总长度：125 mm
严重程度：中等
建议：进一步检测，考虑修复
```

### 可视化
- 原图 + 标注叠加
- 裂缝骨架提取
- 宽度分布直方图

请上传需要分析的图片（支持 JPG/PNG）。
```

### 示例 3: 数字孪生建模
```
用户："为我的振动台试验建立数字孪生模型"

我：
## 数字孪生模型构建

### 阶段 1: 模型建立
**需要信息：**
1. 结构几何（CAD/图纸/尺寸）
2. 材料参数（E, ρ, 本构关系）
3. 边界条件（约束、连接）
4. 传感器布置（位置、类型）

**模型选择：**
| 类型 | 精度 | 速度 | 适用 |
|------|------|------|------|
| 高保真 FEM | 很高 | 慢 | 离线分析 |
| 降阶模型 ROM | 高 | 快 | 实时孪生 |
| 数据驱动 | 中 | 很快 | 快速原型 |

### 阶段 2: 实时数据同化
- 传感器数据接入（OPC UA/MQTT/HTTP）
- 状态估计（卡尔曼滤波）
- 模型参数在线更新

### 阶段 3: 服务功能
- 实时响应可视化
- 健康状态评估
- 损伤预警
- 剩余寿命预测

请先提供结构基本信息，我帮你选择合适的建模策略。
```

### 示例 4: 监测数据分析
```
用户："分析振动台试验的加速度传感器数据"

我：
## 智能监测数据分析

### 数据接收
支持格式：CSV, Excel, MAT, HDF5
数据要求：时间戳 + 加速度（多通道）

### 分析内容
**1. 数据质量检查**
- 缺失值检测
- 异常值识别
- 信噪比评估

**2. 时域分析**
- 峰值加速度 (PGA)
- 均方根 (RMS)
- 持续时间

**3. 频域分析**
- FFT 频谱
- 功率谱密度 (PSD)
- 固有频率识别

**4. 模态分析**
- 频域分解 (FDD)
- 随机子空间识别 (SSI)
- 振型可视化

**5. 损伤检测**
- 模态参数变化
- 曲率模态差
- 应变能变化

### 输出
- 完整分析报告（PDF/Markdown）
- 可视化图表（PNG/SVG）
- 原始处理数据（CSV/MAT）

请上传数据文件或指定文件路径。
```

---

## ⚙️ 配置参数

### 全局配置
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `output_dir` | string | `./civil-ai-outputs/` | 输出目录 |
| `model_backend` | string | `pytorch` | 深度学习后端 |
| `visualization` | bool | `true` | 是否生成可视化 |
| `report_format` | string | `markdown` | 报告格式 |

### 子技能配置

**ML-Struct:**
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `default_model` | `GPR` | 默认回归模型 |
| `uncertainty_quant` | `true` | 不确定性量化 |

**DL-Damage:**
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `detection_threshold` | `0.5` | 检测置信度阈值 |
| `min_crack_width` | `0.1mm` | 最小可检测宽度 |

**DigitalTwin:**
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `update_frequency` | `100Hz` | 数据更新频率 |
| `rom_order` | `10` | 降阶模型阶数 |

**SmartMonitor:**
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `sampling_rate` | `auto` | 采样率（自动检测） |
| `anomaly_method` | `AE` | 异常检测方法 |

---

## 🔧 依赖与安装

### Python 环境
```bash
# 创建虚拟环境
python -m venv civil-ai-env
cd civil-ai-env
Scripts\activate

# 安装核心依赖
pip install numpy pandas scipy matplotlib
pip install scikit-learn xgboost lightgbm
pip install torch torchvision torchaudio
pip install opencv-python pillow
pip install h5py hdf5storage

# 可选：结构分析专用
pip install openseespy
pip install modalpy  # 模态分析
```

### MATLAB 依赖（可选）
```matlab
% 需要 MATLAB 工具箱
- System Identification Toolbox
- Signal Processing Toolbox
- Deep Learning Toolbox
```

### 预训练模型
```bash
# 下载预训练损伤识别模型
mkdir models
cd models
# 从指定 URL 下载
wget [模型链接]
```

---

## 📊 输出目录结构

```
D:\Personal\OpenClaw\civil-ai-outputs\
├── ml-struct\           # 机器学习分析结果
│   ├── predictions.csv
│   ├── model_info.json
│   └── figures\
├── dl-damage\           # 损伤识别结果
│   ├── detections.json
│   ├── annotated_images\
│   └── metrics.csv
├── digital-twin\        # 数字孪生模型
│   ├── model.fem
│   ├── rom.mat
│   ├── realtime_data\
│   └── reports\
└── smart-monitor\       # 监测分析结果
    ├── processed_data\
    ├── features.csv
    ├── modal_params.json
    └── reports\
```

---

## 🔍 故障排除

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 模型加载失败 | 模型文件缺失 | 检查 models/ 目录，重新下载 |
| 内存不足 | 数据量过大 | 分批处理或增加虚拟内存 |
| GPU 不可用 | CUDA 未安装 | 使用 CPU 模式或安装 CUDA |
| 数据格式错误 | 文件格式不支持 | 转换为 CSV/Excel 标准格式 |
| 预测结果异常 | 输入超出训练范围 | 检查输入参数合理性 |

### 性能优化建议
1. **大数据集**：使用 GPU 加速，批量处理
2. **实时应用**：使用降阶模型 (ROM)
3. **高精度需求**：集成多模型预测
4. **存储优化**：使用 HDF5 格式存储大数据

---

## 📚 参考文献与资源

### 核心文献

**机器学习结构工程：**
1. Salehi et al. (2020). "Machine learning in structural engineering"
2. Rafiei & Ghahramani (2020). "Deep learning for structural health monitoring"

**深度学习损伤识别：**
1. Zhang et al. (2020). "Deep learning-based crack detection"
2. Li et al. (2021). "Vision-based damage identification"

**数字孪生：**
1. Tao et al. (2019). "Digital twin in industry"
2. Weddell et al. (2021). "Digital twin for civil infrastructure"

### 开源资源
- [Structural Health Monitoring GitHub](https://github.com/topics/structural-health-monitoring)
- [Deep Learning for Civil Engineering](https://github.com/topics/deep-learning-civil-engineering)
- [OpenSeesPy](https://openseespydoc.readthedocs.io/)

---

## 🎯 与其他技能协作

| 协作技能 | 协作内容 |
|---------|---------|
| `structural-testing` | 试验方案设计、技术术语规范 |
| `matlab-bridge` | MATLAB 仿真数据交换、联合分析 |
| `paper-assistant` | 论文写作、方法描述 |
| `research-paper-writer` | 学术论文生成 |

---

_技能版本：v1.0_  
_创建日期：2026-03-20_  
_作者：智能体 (CivilLabClaw 项目)_  
_适用领域：结构工程 | 智能监测 | 数字孪生 | 损伤识别_

