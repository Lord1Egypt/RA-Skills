---
name: abaqus-loading
description: Abaqus载荷施加完整流程技能。覆盖分析步骤定义、输出要求、边界条件、载荷类型、接触设置。
metadata:
  openclaw:
    emoji: 📦
  version: 1.1.0
  created: 2026-04-25
  updated: 2026-04-25
  domain: 有限元分析/结构工程
---

# Abaqus施加荷载技能

> 官方文档: https://help.3ds.com → SIMULIA Established Products → Abaqus
> Abaqus/Standard: https://www.3ds.com/products/simulia/abaqus/standard
> Abaqus/Explicit: https://www.3ds.com/products/simulia/abaqus/explicit

## 技能描述
此技能涵盖了在Abaqus中定义分析步骤、施加边界条件和荷载的完整流程。Abaqus的载荷施加基于分析步(Step)定义，不同分析步可以施加不同的载荷和边界条件。

## 核心组件

### 1. 分析步骤定义 (Analysis Steps)
- **创建时机**：在施加荷载和边界条件之前必须定义不同的分析步骤
- **载荷分配**：可以指定在哪个分析步施加荷载，在哪个分析步施加边界条件
- **默认初始步**：Abaqus CAE缺省地创建初始步(Initial)
  - 初始步中只能定义边界条件，不能施加载荷
- **输出变量**：分析步骤创建后，CAE会自动选择相应分析过程的输出变量
- **分析步类型**：
  - **通用分析步 (General Step)**：适用于一般的非线性分析
    - Static, General（隐式静力）
    - Dynamic, Implicit（隐式动力）
    - Dynamic, Explicit（显式动力）
    - Heat Transfer（热传导）
    - Buckle（屈曲分析）
    - Frequency（频率分析）
  - **线性扰动分析步 (Linear Perturbation Step)**：
    - Linear Perturbation（从基础状态进行线性分析）
    - 不改变基础状态，结果可叠加

### 2. 输出要求 (Output Requests)
- **场变量输出 (Field Output)**：
  - 用于后处理模块的变形形状、等值线或矢量图显示
  - 输出整个模型或指定区域的空间分布数据
  - 常用变量：S(应力)、E(应变)、U(位移)、RF(反力)等
- **历程输出 (History Output)**：
  - 针对模型中指定点产生历程输出数据
  - 在XY坐标系中查看变量随时间/频率的变化
  - 常用变量：特定节点的位移、反力、能量等
- **输出频率**：控制写入结果数据库(.odb)的变量值频率
- **传递机制**：第一个分析步创建后，输出要求会自动传递给后续分析步

### 3. 边界条件 (Boundary Conditions)
- **施加对象**：
  - 实体单元只有平动自由度，无转动自由度
  - 刚体的约束只能施加给参考点(Reference Point)
  - 壳/梁单元有平动和转动自由度
- **分析步依赖**：边界条件的施加依赖于所建立的分析步
  - 初始步中的BC在整个分析过程中持续有效
  - 后续分析步中可以修改或新增BC
- **自由度约束**：
  - 1,2,3 = X,Y,Z方向平动
  - 4,5,6 = X,Y,Z方向转动（仅壳/梁单元）
  - 11 = 温度（热分析）
  - 8 = 孔压（渗流分析）

### 4. 载荷类型 (Load Types)
- **集中载荷 (Concentrated Force)**：作用在节点或参考点上的集中力
- **分布载荷 (Pressure)**：压力载荷，作用在面或边上
- **体力 (Body Force)**：重力、离心力等体积力
  - 重力：`model.Gravity(comp1=0, comp2=-9.81, comp3=0)`
- **温度载荷 (Temperature)**：热应力分析中的温度场
- **初速度/初角速度 (Velocity/Angular Velocity)**：
  - 显式分析中常用
  - Region必须覆盖部件的所有面、边、顶点
- **螺栓预紧力 (Bolt Load)**
- **面载荷 (Surface Traction)**：切向分布力

### 5. 载荷步骤控制
- **通用分析步 (General Step)**：适用于一般的非线性分析
- **线性扰动分析步 (Linear Perturbation Step)**：适用于线性扰动分析
- **载荷幅值函数 (Amplitude)**：
  - 定义载荷随时间或频率的变化规律
  - 常用类型：
    - Ramp（线性增长）
    - Step（阶跃）
    - Tabular（表格定义）
    - Smooth Step（光滑过渡）
    - Periodic（周期函数）

### 6. 接触设置 (Interaction)
- **接触对 (Contact Pair)**：定义两个表面之间的接触关系
- **通用接触 (General Contact)**：自动检测所有可能的接触对
- **接触属性 (Contact Property)**：
  - 法向行为 (Normal Behavior)：
    - Hard Contact（硬接触，默认）
    - Softened Contact（软化接触）
  - 切向行为 (Tangential Behavior)：
    - Frictionless（无摩擦）
    - Penalty + 摩擦系数
  - 参考摩擦系数：
    | 接触对 | 摩擦系数 |
    |--------|---------|
    | 钢-钢（干） | 0.3~0.6 |
    | 钢-钢（润滑） | 0.05~0.15 |
    | 钢-混凝土 | 0.4~0.7 |

## 应用场景
- 静力分析载荷施加
- 动力分析载荷施加
- 热力耦合分析载荷
- 模态分析载荷设置
- 显式动力学初速度加载

## 注意事项
- 必须在施加载荷前定义分析步骤
- 不同载荷类型适用于不同分析类型
- 边界条件和载荷都依赖于分析步骤
- 删除分析步会导致相应输出要求的删除
- 显式分析中初速度的Region必须覆盖部件所有面、边、顶点
- 载荷幅值函数需要与分析步时间匹配

## 与其它模块的关系
- 分析步模块：载荷施加基于分析步骤定义
- 交互模块：处理接触、约束等问题
- 作业模块：提交计算任务
- 后处理模块：查看载荷施加效果
