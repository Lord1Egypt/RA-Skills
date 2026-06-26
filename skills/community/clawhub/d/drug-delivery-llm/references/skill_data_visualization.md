# **📦 Skill: Data\_Visualization (数据分析与可视化工作流)**

## **1\. 技能概述**

**定位:** 专门负责将分子的属性分布、大模型的生成多样性、图推荐节点关系等数据转化为直观的图表。

**核心模块:** visualization 文件夹

**触发条件:** 当用户请求“画图”、“展示分子分布”、“看看聚类情况”或“生成热力图”时调用。

## **2\. 核心工具与 API**

* **属性分布图 (make\_scatter\_figs.py):**  
  * 工具: calculate\_bin\_counts, plot\_three\_histograms  
  * 用途: 绘制多个模型/数据集在同一指标（如激发光谱、类药性 QED 分布）上的多重直方图对比。  
* **多样性降维图 (make\_diversity\_figs.py):**  
  * 工具: matplotlib.pyplot.scatter, 预配置了多种 cmap (viridis\_r)。  
  * 用途: 将 t-SNE (或 PCA) 降维后的隐变量坐标进行 2D 散点可视化，评估不同语言模型生成分子的空间覆盖率和多样性分布。  
* **关系热力图 (make\_heatmap\_figs.py):**  
  * 工具: seaborn.heatmap  
  * 用途: 将推荐模块生成的邻接矩阵 (adj\_) 或相似性矩阵可视化，展现候选分子间的紧密关联程度。

## **3\. 标准工作流 (SOP)**

**步骤 1: 数据接收**
* 判断需要的图表类型，并向对应的预测或推荐模块拉取特征数组 (array-like)。  
  **步骤 2: 渲染出图**  
* 若为分布对比 \-\> 格式化数据至同一个图层 (plot\_three\_histograms)。  
* 若为降维分布 \-\> 使用 make\_diversity\_figs 定义的样式绘制散点图。  
* 若为网络/矩阵 \-\> 使用 make\_heatmap\_figs 进行渲染。  
  **步骤 3: 导出与呈现**  
* 将生成的图表保存为高精度矢量图 .svg 或 .jpg 格式返回给用户。