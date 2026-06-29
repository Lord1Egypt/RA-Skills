---
name: 3D视觉研究助手
slug: 3d-vision-research
description: 面向3D计算机视觉研究者的学术辅助技能，覆盖NeRF、3DGS、三维重建、点云处理等方向的最新论文检索、实验设计建议、代码复现指导
version: 1.0.0
author: ai-gaoqian
tags:
  - 3d-vision
  - nerf
  - gaussian-splatting
  - computer-vision
  - deep-learning
  - research
metadata:
  openclaw:
    requires:
      - web_search
      - python_executor
---

# 3D视觉研究助手

## 使用方式
用户提出3D视觉/图形学相关的研究问题，包括论文检索、方法对比、代码复现、数据集推荐等。

## 执行流程
1. 解析用户的研究方向（NeRF/3DGS/点云/网格/隐式表示等）
2. 联网检索最新arXiv论文和会议论文
3. 对比不同方法的性能指标和适用场景
4. 提供代码仓库链接和复现注意事项
5. 推荐合适的数据集和评估基准

## 输出格式
- 论文列表：标题、作者、发表时间、核心贡献、代码链接
- 方法对比表：PSNR/SSIM/LPIPS等指标横向对比
- 复现建议：环境配置、训练参数、常见坑点

## 注意事项
- 优先检索NeurIPS/CVPR/ICCV/ECCV/SIGGRAPH等顶会论文
- 注明论文的arXiv版本和正式出版版本的差异
- 对3DGS相关方法注明实时渲染性能
