# **📦 Skill: LLM\_Generation (大模型分子生成工作流)**

## **1\. 技能概述**

**定位:** 负责药物递送可见光响应分子材料的“从头设计”与候选物生成。

**核心模块:** ddllms\_v1 (生成模型、分词器)

**触发条件:** 当用户请求“生成一批新的药物递送分子”、“训练大模型”或“根据特定条件生成分子”时调用。

## **2\. 核心工具与 API**

* **分词器处理 (dd\_tokenzier\_v1.py & dd\_tokenzier\_base\_v1.py):**  
  * 使用 SMILESBPETokenizer 将 SMILES 序列进行 BPE 分词，构建适用于 Transformer 架构的输入。  
* **模型训练与管理 (ddllms\_moe\_v1.py & ddllms\_dense\_v1.py):**  
  * **MoE 架构:** 支持加载和训练 DeepseekV3, Qwen3MoE, Olmoe, GraniteMoe。  
  * **Dense 架构:** 支持加载和训练 GPT2, GPTNeoX, Gemma, Gemma2。  
  * **工具包:** PyTorch-Lightning (ddllms\_trainer\_v1.py)。  
* **候选物生成 (ddllms\_generator\_v1.py):**  
  * 加载基础模型 (Base) 及可选的 LoRA 权重。  
  * 基于超参 (top\_p=0.96, max\_length=64) 批量生成分子，默认输出为 .npy 格式。  
* **条件生成 (ddllms\_condition\_v1.py):**  
  * 基于预训练的 T5 模型 (t5-v1\_1-base-caption2smiles)，接收自然语言描述（如 "This molecule can be excited by visible light"）直接生成目标 SMILES。

## **3\. 标准工作流 (SOP)**

**步骤 1: 确定生成模式**
* 判断是无条件批量生成（走 ddllms\_generator\_v1.py）还是文本条件生成（走 ddllms\_condition\_v1.py）。  
  **步骤 2: 加载环境与模型**  
* 加载对应的 Tokenizer 配置（vocab\_size 等）。  
* 初始化选定的语言模型（根据 GPU 资源优先选择 4090 适配模型）。如果有微调权重，加载 LoRA path。  
  **步骤 3: 运行生成任务**  
* 自回归生成设定数量的候选物（如 n\_generate=1000）。  
  **步骤 4: 数据导出**  
* 将生成的 SMILES 列表保存为 numpy 的 .npy 数组文件，供下游模块（清洗、过滤）使用。