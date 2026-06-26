---
name: diepre-embodied-bridge
version: 1.0.0
author: KingOfZhao
description: DiePre 具身桥接层 —— 将2D视觉检测桥接到3D空间理解和机器人动作规划，vision-action-evolution-loop 的具体实现
tags: [cognition, diepre, embodied-ai, 3d-reconstruction, tool-calling, mcp, robotics, packaging]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# DiePre Embodied Bridge Skill

## 元数据

| 字段       | 值                              |
|------------|-------------------------------|
| 名称       | diepre-embodied-bridge         |
| 版本       | 1.0.0                          |
| 作者       | KingOfZhao                     |
| 发布日期   | 2026-03-31                     |
| 置信度     | 96%                            |

## 核心哲学

`vision-action-evolution-loop` 定义了抽象的五阶段闭环。
本 Skill 是它的**具体实现层**——聚焦于"如何把2D线条变成3D动作"。

认知节点关系：
```
vision-action-evolution-loop (父: 抽象闭环)
    └── diepre-embodied-bridge (本Skill: 具体实现)
            ├── diepre-vision-cognition (上游: 2D检测)
            └── diepre-action-memory (下游: 动作记忆, 未来)
```

## 三大核心认知

### 1. 已知几何估算（非通用3D重建）

包装盒不是复杂场景，是**已知几何体**。不需要 NeRF / Gaussian Splatting / SfM。

```
输入: 2D DXF + FEFCO类型 + 纸板厚度
算法: FEFCO规则引擎 + 2D尺寸 → 3D展开坐标 → 折叠矩阵
输出: 三维空间坐标 (x,y,z) + 折叠顺序 + 面法向量
硬件: M1 Max 轻松运行（纯CPU计算，<100ms）
```

**为什么排除 NeRF/Gaussian Splatting？**
- 包装盒是平面折叠结构，不是复杂3D场景
- NeRF需要数百张照片+GPU集群训练，M1 Max跑不动
- Gaussian Splatting需要密集视角，生产环境不现实
- 已知几何估算：1张照片+FEFCO规则→3D，秒级完成

### 2. MCP 工具链（Tool-Augmented）

OpenCV 管道封装为可调用工具，VLA 模型调用工具而非处理原始图像：

```python
tools = {
    "detect_dieline": {
        "input": "image_path: str",
        "output": "dxf_path: str, confidence: float",
        "impl": "diepre_vision.analyze"
    },
    "estimate_dimensions": {
        "input": "dxf_path: str",
        "output": "length, width, height, thickness_mm",
        "impl": "dimension_estimator.from_dxf"
    },
    "identify_fefco_type": {
        "input": "dxf_path: str, layout_features: dict",
        "output": "fefco_type: str (e.g. 0201, 0427)",
        "impl": "fefco_classifier.classify"
    },
    "calculate_fold_sequence": {
        "input": "fefco_type: str, dimensions: dict, material: str",
        "output": "ordered_steps: list[FoldStep]",
        "impl": "fold_planner.plan"
    },
    "compute_grasp_points": {
        "input": "fold_sequence: list[FoldStep], material_thickness: float",
        "output": "grasp_points: list[GraspPoint] (xyz + force + angle)",
        "impl": "grasp_calculator.compute"
    },
    "estimate_quality": {
        "input": "image_path: str, expected_dimensions: dict",
        "output": "quality_score: float, defects: list",
        "impl": "quality_checker.evaluate"
    }
}
```

### 3. 自迭代进化机制

```
执行任务 → 记录结果 → 提取失败模式 → 调整参数 → 下次优化

具体流程:
1. 每次任务执行完，写入 evolution_log/{task_id}.json:
   {
     "task_id": "diepre_20260331_001",
     "input": {"image": "...", "fefco": "0201", "material": "B flute"},
     "execution": {"steps": [...], "timing_ms": 3400},
     "result": {"success": false, "fail_step": 3, "error": "grasp_slip"},
     "params_used": {"grasp_force": 2.5, "approach_angle": 45}
   }

2. 定期扫描 evolution_log/，提取失败模式:
   - grasp_slip 在 B flute 上发生频率 73% → 提高抓取力
   - fold_sequence 错误在 FEFCO 0427 上频率 40% → 修正折叠规则

3. 更新参数文件 params/evolved_params.json:
   {"B_flute_grasp_force": 3.2, "0427_fold_override": [...]}

4. 下次任务加载 evolved_params.json，用优化后参数执行
```

## 安装命令

```bash
clawhub install diepre-embodied-bridge
# 或手动安装
cp -r skills/diepre-embodied-bridge ~/.openclaw/skills/
```

## 调用方式

```python
from skills.diepre_embodied_bridge import DiePreEmbodiedBridge

bridge = DiePreEmbodiedBridge(workspace=".")

# 单次执行
result = bridge.execute(
    image_path="path/to/box_photo.jpg",
    material="B flute",
    thickness_mm=3.0
)

print(result.fefco_type)          # "0201"
print(result.dimensions)          # {"L": 300, "W": 200, "H": 100}
print(result.fold_sequence)       # [FoldStep(...), ...]
print(result.grasp_points)        # [GraspPoint(x=150,y=0,z=50,force=3.2), ...]
print(result.quality_score)       # 0.92
print(result.confidence)          # 0.96

# 自迭代: 注入失败反馈
bridge.record_failure(
    task_id="diepre_20260331_001",
    fail_step=3,
    error_type="grasp_slip",
    context={"material": "B flute", "grasp_force": 2.5}
)

# 查看进化状态
stats = bridge.evolution_stats()
print(stats.total_tasks)          # 47
print(stats.failure_rate)         # 0.12
print(stats.top_failure_modes)    # [("grasp_slip", 8), ("fold_error", 4)]
```

## 学术参考文献

1. **[From 2D CAD to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892)** — 2D→3D桥接，参数化建模
2. **[Tool-Augmented VLLMs as Generic CAD Task Solvers](https://arxiv.org/) (ICCV 2025)** — 工具增强策略，MCP工具链的理论基础
3. **[Vlaser: Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027)** — 抓取点计算+力控参数
4. **[Efficient VLA Models](https://arxiv.org/abs/2510.17111)** — 本地部署优化（M1 Max适用）
5. **[SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)** — 自迭代进化的学术对应
6. **[Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)** — 记忆自更新+参数进化
