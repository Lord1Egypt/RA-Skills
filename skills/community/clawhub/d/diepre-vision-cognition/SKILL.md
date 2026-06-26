---
name: diepre-vision-cognition
version: 1.1.0
author: KingOfZhao
description: DiePre 视觉认知 Skill —— 将包装/模切机器视觉感知与 SOUL 推理融合的认知框架
tags: [cognition, vision, diepre, packaging, manufacturing, quality-control, cad, vlm]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# DiePre Vision Cognition Skill

## 元数据

| 字段       | 值                              |
|------------|-------------------------------|
| 名称       | diepre-vision-cognition        |
| 版本       | 1.0.0                          |
| 作者       | KingOfZhao                     |
| 发布日期   | 2026-03-31                     |
| 置信度     | 96%                            |

## 学术参考文献

本视觉框架的技术路线受以下前沿研究启发：

1. **[Generating CAD Code with Vision-Language Models](https://arxiv.org/abs/2410.05340)** — VLM生成CAD代码+迭代验证（CADCodeVerify），直接升级照片→DXF管道
2. **[From 2D CAD to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892)** — 2D图纸→参数化3D，解决透视矫正和参数化问题
3. **[Tool-Augmented VLLMs as Generic CAD Task Solvers](https://arxiv.org/) (ICCV 2025)** — VLLM+工具调用做通用CAD，封装OpenCV管道为可调用Skill
4. **[Efficient Vision-Language-Action Models](https://arxiv.org/abs/2510.17111)** — VLA高效优化（低延迟+内存优化），适合本地部署
5. **[Vlaser: Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027)** — 具身推理VLA，未来"照片→动作决策"的理论基础

## 核心能力

将 DiePre（模切压痕）机器视觉感知与 SOUL 认知框架融合：

1. **视觉已知/未知分离**：从图像中提取确定特征（已知）与模糊区域（未知）
2. **文件记忆**：每次检测结果写入 `vision_log/YYYY-MM-DD.jsonl`
3. **四向视觉碰撞**：正视角、反转、侧光、整体布局四个维度同时分析
4. **人机闭环质检**：AI 初判 → 人类复核 → 标注反馈 → 模型持续进化
5. **置信度质检输出**：低于 90% 置信度的缺陷自动升级为人工复核

## 安装命令

```bash
clawhub install diepre-vision-cognition
# 或手动安装
cp -r skills/diepre-vision-cognition ~/.openclaw/skills/
```

## 调用方式

```python
from skills.diepre_vision_cognition import DiePrevisionCognition

vision = DiePrevisionCognition(workspace=".")
result = vision.analyze(
    image_path="path/to/dieline.png",
    context={"material": "corrugated", "thickness_mm": 3.0}
)

print(result.confidence)     # 置信度
print(result.defects)        # 检测到的缺陷列表
print(result.collision_log)  # 四向分析详情
```
