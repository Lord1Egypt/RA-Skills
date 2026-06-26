---
name: abaqus-modeling
description: Abaqus有限元建模完整流程技能。覆盖部件创建、材料属性定义、装配、草图绘制、CAD关联接口。
metadata:
  openclaw:
    emoji: 🏗️
  version: 1.1.0
  created: 2026-04-25
  updated: 2026-04-25
  domain: 有限元分析/结构工程
tags:
  - modeling
  - part
  - assembly
  - material
---

# Abaqus建模技能

> 官方文档: https://help.3ds.com → SIMULIA Established Products → Abaqus
> Abaqus/CAE: https://www.3ds.com/products/simulia/abaqus/cae

## 技能描述
此技能涵盖了使用Abaqus/CAE进行有限元建模的完整流程。Abaqus/CAE集成了建模、分析、作业管理和结果可视化于一体，界面直观一致，新用户易学，老用户高效。

## 核心组件

### 1. 部件创建 (Part)
- **建模方法**：一个模型通常由一个或几个部件组成，部件由特征体组成
- **基本特征体**：挤压(Extrude)、旋转(Revolve)、扫掠(Sweep)三种主要方法创建特征体
- **数据元素**：包括数据点、数据轴、数据平面等辅助建模元素
- **刚体类型**：可变形体(Deformable)、不连续介质刚体(Eulerian)、分析刚体(Analytical Rigid)三种类型
- **独立vs非独立**：
  - 独立实例(Partition)：划分网格时独立划分，与源部件不相关
  - 非独立实例：划分网格时和源部件相关联，源部件修改会影响所有实例
- **参数化建模**：支持基于特征的参数化建模，可通过修改参数快速更新模型

### 2. 材料属性定义 (Material Properties)
- **基本参数**：弹性模量、泊松比、密度等基本材料参数
- **截面特性**：均质的(Homogeneous)、各项同性(Isotropic)、平面应力/平面应变等
- **分配方式**：将截面特性(Section)分配给部件的特定区域(Region)，使该区域与截面特性相关联
- **扩展材料模型**：
  - 线性弹性与粘弹性 (Linear Elasticity & Viscoelasticity)
  - 非线性粘弹性
  - 各向同性与随动塑性 (Isotropic & Kinematic Plasticity)
  - 损伤与断裂力学 (Damage & Fracture Mechanics)
  - 多尺度与平均场均匀化 (Multiscale & Mean-Field Homogenization)
  - 低密度率相关泡沫材料 (Low-density, rate-dependent foam)
  - 状态方程（非牛顿流体、理想气体）(Equation of States)
  - 超弹性材料（橡胶类，需使用杂交单元）
- **用户自定义材料**：通过UMAT/VUMAT子程序扩展材料模型

### 3. 装配 (Assembly)
- **部件实例**：部件实例是部件的代表，与原部件保持关联
- **坐标系**：装配体总体坐标系与创建部件时的总体坐标系不同
- **定位方法**：
  - 移动和旋转方法
  - 专门的定位工具集：平行面、面对面、平行边、边对边、共轴、点重合等
- **CAD关联接口**：
  - CATIA V5、SolidWorks、Pro/ENGINEER 的关联接口
  - 支持CAD与CAE装配体的同步
  - 实现快速模型更新而不丢失用户定义的分析特征

### 4. 草图绘制 (Sketch)
- **绘图区设置**：根据部件近似尺寸决定绘图区网格间距
- **草图工具**：用于创建二维几何形状的基础工具
- **参数化约束**：支持尺寸约束和几何约束

## 应用场景
- 机械结构分析建模
- 土木工程结构建模
- 材料性能分析建模
- 复杂几何体建模
- 复合材料层合板建模（配合 Composites Modeler for Abaqus/CAE）

## 注意事项
- 删除父特征体会同时删除其所有子特征体
- 一个部件如果只包含一个特征体，删除特征体时部件也同时被删除
- 刚体必须指定一个参考点(Reference Point)用于施加约束和定义运动
- 材料定义中**必须包含密度**（尤其是显式分析，F=ma需要密度）
- 超弹性/不可压缩材料必须使用杂交单元（如 C3D8RH）

## 与其它模块的关系
- 材料属性模块：定义部件的材料特性
- 装配模块：将部件组装成完整模型
- 网格模块：基于几何体进行网格划分
- 分析步模块：建模完成后进行分析设置

## 官方模块参考
- Abaqus/CAE: https://www.3ds.com/products/simulia/abaqus/cae
- Abaqus CAD Associative Interface: https://www.3ds.com/products/simulia/abaqus/cad-associative-interface
- Composites Modeler for Abaqus/CAE: https://www.3ds.com/products/simulia/abaqus/composites-modeler
