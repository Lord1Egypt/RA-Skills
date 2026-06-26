---
name: Genos基因序列分析
description: 使用 Genos 模型进行 DNA 序列分析。当用户提到 DNA、基因、基因组、碱基序列、ACGT 等生物信息学相关问题时使用此技能。
---

# Genos DNA 序列分析技能

## 概述

此技能使用之江实验室的 Genos-1.2B 模型进行 DNA 序列分析。该模型是人类基因组基础模型，专门用于分析 DNA 碱基序列。

## 使用场景

- DNA 序列分析
- 基因组预测
- 碱基频率统计
- 序列模式识别
- 基因组学研究相关问题

## 模型信息

- **模型**: Genos-1.2B
- **参数**: 12 亿
- **架构**: MoE (Mixture of Experts)
- **词汇量**: 128 (A, C, G, T, N + 特殊标记)
- **上下文长度**: 最长 1M 碱基对

## 使用方法

### 1. DNA 碱基序列分析

当用户提供 DNA 序列（如 ACGTACGT...）时，调用 `analyze_dna_sequence` 函数进行分析。

### 2. 预测下一个碱基

调用 `predict_next_base` 函数预测 DNA 序列中下一个可能的碱基。

### 3. 序列特征提取

调用 `extract_sequence_features` 函数提取序列的特征信息。

## 示例

### 输入格式

用户可能提供：
- DNA 序列: `ACGTACGTACGT...`
- FASTA 格式的基因序列
- 简单描述: "帮我分析这段 DNA 序列"

### 输出格式

返回分析结果，包括：
- 碱基组成统计
- 序列长度
- 预测结果

## 注意事项

1. 此模型仅支持 DNA 碱基字符（A, C, G, T, N）
2. 不支持中文或英文自然语言输入
3. 输入前需去除空格、换行等非碱基字符
4. 模型主要用于基因组学研究，不适用于对话任务

## 模型状态检查与启动

**重要：在调用技能前，必须先检查模型是否已启动！**

### 检查模型状态

模型状态记录在 `./scripts/.model_loaded` 文件中（相对于项目根目录）。

- 如果文件存在且内容为 `loaded`，表示模型已启动
- 如果文件不存在或内容不是 `loaded`，需要先启动模型

### 启动模型

如果模型未启动，执行以下命令启动：

```bash
# 设置模型路径（可选，默认为 ./models/Genos-1___2B）
export GENOS_MODEL_PATH="./models/Genos-1___2B"

# 启动模型
python3 -c "
import sys
sys.path.insert(0, './scripts')
from genos_dna import load_model
load_model()
with open('./.model_loaded', 'w') as f:
    f.write('loaded')
print('Model loaded and status saved')
"
```

### 自动化检查

AI 助手在调用技能时应自动完成以下步骤：
1. 检查 `./.model_loaded` 文件是否存在且内容为 `loaded`
2. 如果模型未启动，先执行上述启动命令
3. 确认模型启动后再调用技能函数

### 使用环境变量配置

你也可以通过环境变量自定义路径：

```bash
# 设置模型路径
export GENOS_MODEL_PATH="/path/to/your/model"

# 设置状态文件路径
export GENOS_STATUS_FILE="/path/to/your/state/.model_loaded"

# 然后运行脚本
python3 your_script.py
```

### 配置文件方式

你也可以创建 `config.json` 文件来配置路径：

```json
{
    "model_path": "./models/Genos-1___2B",
    "state_file": "./scripts/.model_loaded"
}
```
