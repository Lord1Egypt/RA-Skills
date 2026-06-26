# **📦 Skill: Property\_Classification (分子性质分类与评估工作流)**

## **1\. 技能概述**

**定位:** 针对已生成的分子候选物，进行光响应信号等物理化学性质的分类标注、评估和特征归因（可解释AI）。

**核心模块:** vis\_classifier

**触发条件:** 当用户请求“预测分子性质”、“评估这批分子的光响应能力”或“解释为什么这个分子有这个性质”时调用。

## **2\. 核心工具与 API**

* **经典机器学习 (sklearn\_ML.py):**  
  * 读取指纹 (Fingerprint)，调用随机森林、逻辑回归、SVM 等执行快速批量预测。  
* **量子机器学习 (qiskit\_ML.py & braket\_ML.py):**  
  * **Qiskit:** 基于 ZZFeatureMap 构建 QSVM 量子支持向量机模型。  
  * **Braket:** 构建含变分量子线路的混合量子-经典神经网络 (QFPNN, QuantumMLP)。  
* **大语言模型/多模态分类 (T5\_langauge\_model.py & Graph/BLIP\_embedding\_model.py):**  
  * 使用 T5 提取文本隐变量；使用 GIN 提取分子图结构隐变量。  
  * BLIP 模块融合文本与图模态，通过交叉注意力实现高精度预测。  
* **可解释 AI (XAI\_ML.py):**  
  * 调用 shap 库 (TreeExplainer) 评估特征重要性。  
  * 使用 extract\_substructure 追溯具体起作用的化学子结构（Atom Map）。

## **3\. 标准工作流 (SOP)**

**步骤 1: 数据准备**
* 读取 XY-c2.csv 格式的分子数据集，清洗并提取 SMILES。  
  **步骤 2: 选择分类器引擎**  
* **速度优先:** 调用 sklearn\_ML (Random Forest)。  
* **前沿验证:** 调用量子模块 (qiskit\_ML 或 braket\_ML)。  
* **高精度多模态:** 调用 BLIP\_embedding\_model 融合架构。  
  **步骤 3: 预测与标注**  
* 输出准确率 (Accuracy)、分类报告 (Classification Report)，将预测标签附着到分子列表。  
  **步骤 4: 特征归因 (可选)**  
* 若需解释，运行 XAI\_ML.py 生成 SHAP 值和子结构依赖图，输出分析报告。