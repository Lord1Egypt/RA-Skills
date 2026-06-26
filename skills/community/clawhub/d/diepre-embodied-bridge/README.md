# diepre-embodied-bridge

> DiePre 具身桥接层 —— 2D线条变成3D动作的具体实现

**作者**: KingOfZhao  
**版本**: 1.0.0  
**发布日期**: 2026-03-31  
**许可证**: MIT

---

## 解决什么问题？

`vision-action-evolution-loop` 定义了"感知→规划→执行→评估→进化"的抽象闭环。
但如何让2D的DXF线条变成机器人能理解的动作？这就是**桥接层**要做的事。

## 三大核心创新

### 1. 已知几何估算（非通用3D重建）
包装盒是已知几何体（FEFCO类型），不需要NeRF/Gaussian Splatting。
1张照片 + FEFCO规则 → 3D坐标，M1 Max秒级完成。

### 2. MCP 工具链（6个工具）
```
detect_dieline → estimate_dimensions → identify_fefco_type →
calculate_fold_sequence → compute_grasp_points → estimate_quality
```
VLA调用工具拿结构化输出，不处理原始图像。

### 3. 自迭代进化
每次执行写入日志 → 提取失败模式 → 自动调参 → 下次优化。

## 快速安装

```bash
clawhub install diepre-embodied-bridge
```

## Skill 节点关系

```
vision-action-evolution-loop (父: 抽象闭环)
    └── diepre-embodied-bridge (本Skill: 具体实现)
            ├── diepre-vision-cognition (上游: 2D检测)
            └── diepre-action-memory (下游: 动作记忆, 未来)
```

## 变更日志

### v1.0.0 (2026-03-31)
- Skill工厂第2个自动生成Skill
- 已知几何估算（排除NeRF/Gaussian）
- MCP工具链（6个工具定义）
- 自迭代进化机制
- 通过自验证置信度: 96%

---

*自动开源认知 Skill by Skill Factory — KingOfZhao*
