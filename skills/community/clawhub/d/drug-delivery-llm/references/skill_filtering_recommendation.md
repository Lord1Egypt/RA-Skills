# **📦 Skill: Filtering & Recommendation (候选物特征过滤与推荐工作流)**

## **1\. 技能概述**

**定位:** 对大量生成的初级分子进行清洗、特征计算、降维，并基于图神经网络进行顶级候选物的筛选与推荐。

**核心模块:** chem\_utils, ddllms\_recommend\_v1.py

**触发条件:** 当用户要求“找出最好的分子”、“对生成的分子进行过滤”、“计算分子的QED/SA”时调用。

## **2\. 核心工具与 API**

* **数据清洗 (chem\_utils.preprocessing):**  
  * 执行去空、去短串、去重、以及 RDkit 有效性校验 (preprocess\_smiles)。  
* **描述符计算 (chem\_utils.descriptors & utils.cal\_SA):**  
  * compute\_qed\_from\_smiles(): 计算类药性评分 (QED)。  
  * compute\_sa\_from\_smiles(): 计算合成可及性惩罚评分 (SA Score)。  
* **指纹与相似性 (chem\_utils.fingerprints & similarity):**  
  * 将分子映射为 Morgan 指纹。计算余弦相似度，构建 similarity\_matrix。  
* **图推荐算法 (ddllms\_recommend\_v1.py):**  
  * **特征融合 (FeatureEngineer):** 拼合多种指纹、QED、SA 等指标，使用 PCA / t-SNE 降维。  
  * **PageRank 推荐 (SimilarityGraph):** 构建分子关系图，运用 PageRank 算法挖掘最具代表性、最优的 top\_k (如 Top 40\) 候选节点。

## **3\. 标准工作流 (SOP)**

**步骤 1: 读取与预处理**
* 读取大模型生成的原始 .npy 数据。  
* 调用 chem\_utils.preprocessing 清除无法通过 RDkit 解析的“死分子”。  
  **步骤 2: 特征工程**  
* 批量计算每个分子的 Morgan 分子指纹、QED 和 SA 分数。  
  **步骤 3: 降维与建图**  
* 运行 FeatureEngineer 拼接特征，通过 t-SNE 投射到低维空间。  
* 使用 SimilarityGraph 在低维空间计算节点相似度，生成邻接矩阵构建 Graph。  
  **步骤 4: 推荐输出**  
* 应用 PageRank 算法，按分数降序排序，输出最终推荐的 Top-N 分子列表及相关分数。