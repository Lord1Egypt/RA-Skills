# Genos DNA 序列分析

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange.svg)](https://pytorch.org/)
[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/flowertusi/genos-dna/releases)

基于之江实验室 Genos-1.2B 模型的 DNA 序列分析工具，用于分析和预测 DNA 碱基序列。

## 更新日志

### v1.0.1 (2026-03-22)
- ✅ 修复状态文件路径不一致问题（`./state/.model_loaded` → `./scripts/.model_loaded`）
- ✅ 添加详细的安全说明和风险提示
- ✅ 优化模型下载说明，支持三个下载源（Hugging Face、ModelScope、GitHub）
- ✅ 添加模型信息表格，包含每个版本的下载链接

### v1.0.0 (2026-03-21)
- ✅ 初始版本发布
- ✅ 支持 DNA 序列分析、碱基预测、特征提取
- ✅ 支持命令行和 Python 两种使用方式
- ✅ 支持一键安装脚本

## 功能特点

- 🧬 **DNA 序列分析**：分析 DNA 序列的碱基组成和特征
- 🔮 **碱基预测**：预测 DNA 序列中下一个可能的碱基
- 📊 **特征提取**：提取序列的 GC 含量、AT 含量等特征
- 🚀 **高性能**：支持长达 1M 碱基对的序列分析
- 🎯 **专业模型**：基于 Genos-1.2B 基因组基础模型

## 模型信息

- **模型名称**: Genos-1.2B
- **参数量**: 12 亿
- **架构**: MoE (Mixture of Experts)
- **词汇量**: 128 (A, C, G, T, N + 特殊标记)
- **上下文长度**: 最长 1M 碱基对
- **开发者**: 之江实验室 (Zhejiang Lab)

## 安装

### 环境要求

- Python 3.9+
- PyTorch 2.0+
- 至少 8GB RAM

### 快速安装

```bash
# 克隆仓库
git clone https://github.com/flowertusi/genos-dna.git
cd genos-dna

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 模型下载

Genos 模型支持从以下三个平台下载：

#### 1. Hugging Face（推荐）

```bash
# 安装 huggingface-cli
pip install huggingface-hub

# 登录 Hugging Face（需要先注册账号）
huggingface-cli login

# 下载模型
huggingface-cli download zhejianglab/Genos-1___2B --local-dir ./models/Genos-1___2B
```

#### 2. ModelScope（魔搭社区）

```bash
# 安装 modelscope
pip install modelscope

# 下载模型
python -c "from modelscope import snapshot_download; snapshot_download('zhejianglab/Genos-1___2B', cache_dir='./models')"
```

#### 3. GitHub Releases

```bash
# 访问 Genos GitHub 仓库
# https://github.com/zhejianglab/Genos

# 或使用命令行下载
curl -L -o genos-1.2b.zip https://github.com/zhejianglab/Genos/releases/download/v1.0/Genos-1___2B.zip
unzip genos-1.2b.zip -d ./models/Genos-1___2B
```

或者在代码中自动下载（首次运行时）：

```python
from genos_dna import load_model

# 首次运行会自动下载模型（优先从 Hugging Face 下载）
model, tokenizer = load_model()
```

**模型信息**

| 模型名称 | 参数量 | Hugging Face | ModelScope | GitHub |
|---------|--------|-------------|------------|--------|
| Genos-1.2B | 1.2B | [🤗Hugging Face](https://huggingface.co/ZhejiangLab/Genos-1.2B) | [🤖ModelScope](https://modelscope.cn/models/zhejianglab/Genos-1.2B) | [🔗GitHub](https://github.com/zhejianglab/Genos) |
| Genos-10B | 10B | [🤗Hugging Face](https://huggingface.co/ZhejiangLab/Genos-10B) | [🤖ModelScope](https://modelscope.cn/models/zhejianglab/Genos-10B) | [🔗GitHub](https://github.com/zhejianglab/Genos) |
| Genos-10B-v2 | 10B | [🤗Hugging Face](https://huggingface.co/ZhejiangLab/Genos-10B-v2) | [🤖ModelScope](https://modelscope.cn/models/zhejianglab/Genos-10B-v2) | [🔗GitHub](https://github.com/zhejianglab/Genos) |

**推荐**：Genos-1.2B 模型体积较小，适合快速测试和开发；Genos-10B 和 Genos-10B-v2 模型精度更高，适合生产环境。

## 使用方法

### 命令行使用

```bash
# 分析 DNA 序列
python scripts/genos_dna.py analyze "ACGTACGTACGT"

# 预测下一个碱基
python scripts/genos_dna.py predict "ACGTACGT" --top_k 5

# 提取序列特征
python scripts/genos_dna.py features "ACGTACGTACGT"
```

### Python 使用

```python
from genos_dna import (
    analyze_dna_sequence,
    predict_next_base,
    extract_sequence_features
)

# 1. 分析 DNA 序列
sequence = "ACGTACGTACGTACGT"
result = analyze_dna_sequence(sequence)
print(f"序列长度: {result['cleaned_length']}")
print(f"GC 含量: {result['gc_content']:.2f}%")

# 2. 预测下一个碱基
predictions = predict_next_base(sequence, top_k=3)
for pred in predictions['predictions']:
    print(f"碱基: {pred['base']}, 概率: {pred['probability']:.4f}")

# 3. 提取序列特征
features = extract_sequence_features(sequence)
print(f"GC 含量: {features['gc_content']}")
print(f"AT 含量: {features['at_content']}")
```

### 在通用 Skill 系统中使用

将此技能添加到任意支持 Skill 的系统中：

```bash
# 复制技能到系统目录
cp -r genos_dna /path/to/system/skills/

# 配置模型路径（推荐使用环境变量）
# 方法1: 使用环境变量
export GENOS_MODEL_PATH="/path/to/your/model"

# 方法2: 修改 scripts/genos_dna.py
# 修改 model_path 变量指向你的模型路径
```

或者使用配置文件方式：

```bash
# 复制配置模板
cp config.json.example config.json

# 编辑配置文件
vim config.json
```

## 项目结构

```
genos_dna/
├── scripts/
│   ├── __init__.py
│   └── genos_dna.py          # 核心脚本
├── requirements.txt          # 依赖列表
├── README.md                 # 项目说明
├── LICENSE                   # 许可证
└── example.py               # 使用示例
```

## API 文档

### `analyze_dna_sequence(sequence: str) -> dict`

分析 DNA 序列并返回分析结果。

**参数**:
- `sequence`: DNA 序列字符串

**返回**:
```python
{
    "original_length": int,           # 原始序列长度
    "cleaned_length": int,            # 清理后的序列长度
    "base_frequency": dict,           # 碱基频率
    "gc_content": float,              # GC 含量百分比
    "sequence_preview": str           # 序列预览
}
```

### `predict_next_base(sequence: str, top_k: int = 3) -> dict`

预测 DNA 序列的下一个碱基。

**参数**:
- `sequence`: DNA 序列字符串
- `top_k`: 预测前 K 个可能的碱基（默认 3）

**返回**:
```python
{
    "input_sequence": str,            # 输入序列
    "predictions": list               # 预测结果列表
}
```

### `extract_sequence_features(sequence: str) -> dict`

提取 DNA 序列的特征。

**参数**:
- `sequence`: DNA 序列字符串

**返回**:
```python
{
    "length": int,                    # 序列长度
    "base_composition": dict,         # 碱基组成
    "gc_content": str,                # GC 含量（百分比格式）
    "at_content": str,                # AT 含量（百分比格式）
    "model_info": dict                # 模型信息
}
```

## 示例

### 示例 1: 简单序列分析

```python
from genos_dna import analyze_dna_sequence

sequence = "ACGTACGTACGTACGTACGT"
result = analyze_dna_sequence(sequence)

print(f"序列长度: {result['cleaned_length']}")
print(f"碱基频率: {result['base_frequency']}")
print(f"GC 含量: {result['gc_content']:.2f}%")
```

### 示例 2: 预测下一个碱基

```python
from genos_dna import predict_next_base

sequence = "ACGTACGTACGT"
predictions = predict_next_base(sequence, top_k=5)

print(f"输入序列: {predictions['input_sequence']}")
print("预测结果:")
for i, pred in enumerate(predictions['predictions'], 1):
    print(f"{i}. 碱基: {pred['base']}, 概率: {pred['probability']:.4f}")
```

### 示例 3: 批量分析

```python
from genos_dna import analyze_dna_sequence

sequences = [
    "ACGTACGTACGT",
    "TTATATATATAT",
    "GCGCGCGCGCGC"
]

for seq in sequences:
    result = analyze_dna_sequence(seq)
    print(f"序列: {seq[:10]}... GC含量: {result['gc_content']:.2f}%")
```

## 注意事项

1. **输入格式**: 仅支持 DNA 碱基字符（A, C, G, T, N），其他字符会被自动过滤
2. **内存要求**: 模型加载需要至少 8GB RAM
3. **首次运行**: 首次运行会自动下载模型，可能需要一些时间
4. **GPU 支持**: 当前版本仅支持 CPU 运行，如需 GPU 支持请修改 `device_map` 参数

## 安全说明

### ⚠️ 重要安全提示

本技能使用 `transformers` 库的 `trust_remote_code=True` 参数加载 Genos 模型。这允许执行模型仓库中包含的自定义 Python 代码，存在一定的安全风险。

**请务必注意以下安全建议**：

1. **验证模型来源**：只从官方渠道下载 Genos 模型
   - Hugging Face: https://huggingface.co/ZhejiangLab
   - ModelScope: https://modelscope.cn/models/zhejianglab
   - GitHub: https://github.com/zhejianglab/Genos

2. **验证模型完整性**：下载后建议验证模型文件的校验和或签名

3. **隔离运行环境**：建议在容器或虚拟机中运行，限制权限

4. **检查 install.sh**：安装脚本会从外部源下载模型文件，请在运行前检查脚本内容

5. **谨慎处理 Token**：如果使用 Hugging Face Token，请确保只在信任的环境中使用

### 安装后验证

安装完成后，建议进行以下验证：

```bash
# 检查模型文件完整性
ls -lh ./models/Genos-1___2B/

# 运行测试
python3 example.py
```

## 故障排除

### 模型加载失败

**问题**: `Model not found` 错误

**解决方案**: 
1. 确保已正确下载模型
2. 检查 `MODEL_PATH` 配置是否正确
3. 确保有网络连接以下载模型

### 内存不足

**问题**: `CUDA out of memory` 或内存溢出

**解决方案**:
1. 减少序列长度
2. 增加系统交换空间
3. 使用更小的模型

### 依赖安装失败

**问题**: `transformers` 或 `torch` 安装失败

**解决方案**:
```bash
# 确保 pip 是最新版本
pip install --upgrade pip

# 尝试安装预编译的 wheel
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
```

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 致谢

- 感谢之江实验室提供 Genos 模型
- 感谢 Hugging Face 提供 transformers 库
- 感谢 PyTorch 社区的支持

## 联系方式

- GitHub: [@flowertusi](https://github.com/flowertusi)
- Email: 63704960@qq.com

## 引用

如果你在研究中使用了此工具，请引用：

```bibtex
@software{GenosDNA2024,
  title={Genos DNA Sequence Analysis},
  author={flowertusi},
  year={2024},
  publisher={GitHub},
  url={https://github.com/flowertusi/genos-dna}
}
```
