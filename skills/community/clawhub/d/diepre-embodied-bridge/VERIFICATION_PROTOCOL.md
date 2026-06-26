# VERIFICATION_PROTOCOL.md — diepre-embodied-bridge

## 验证目标

确保桥接层的三个核心认知（已知几何估算、MCP工具链、自迭代）都有完整实现路径。

## 五步自验证流程

### Step 1 — 已知几何估算验证
- [ ] 是否明确排除了 NeRF/Gaussian Splatting/SfM 并给出理由？
- [ ] 是否使用 FEFCO 规则 + 2D 尺寸 → 3D 坐标作为核心算法？
- [ ] 算法是否可在 M1 Max CPU 上 <100ms 完成？
- **通过标准**: 排除理由充分 + 算法路径明确 + 硬件可行性

### Step 2 — MCP 工具链验证
- [ ] 是否定义了完整的工具链（detect→estimate→classify→plan→grasp→quality）？
- [ ] 每个工具是否有明确的 input/output schema？
- [ ] VLA 调用工具的方式是否与原始图像处理区分？
- **通过标准**: ≥6个工具定义 + schema完整 + 架构清晰

### Step 3 — 自迭代进化验证
- [ ] 每次执行是否写入 evolution_log/{task_id}.json？
- [ ] 是否有失败模式提取机制（模式聚合+频率统计）？
- [ ] 参数更新是否自动加载到下次执行？
- **通过标准**: 日志写入+模式提取+参数回注三环节完整

### Step 4 — 节点关系验证
- [ ] 是否明确定义了与父/子 Skill 的关系？
- [ ] 是否标注了未来下游 Skill（diepre-action-memory）？
- **通过标准**: 节点关系图完整 + 演进方向明确

### Step 5 — 置信度 + 学术引用
- [ ] 核心技术是否有学术参考文献支撑？
- [ ] 每个输出是否有独立置信度标注？
- [ ] 综合置信度是否 ≥ 95%？
- **通过标准**: 6篇引用 + 置信度覆盖 + ≥95%

## 验证结论模板

```
验证日期: YYYY-MM-DD
Step 1 已知几何估算:      PASS / FAIL  (置信度: XX%)
Step 2 MCP工具链:         PASS / FAIL  (置信度: XX%)
Step 3 自迭代进化:        PASS / FAIL  (置信度: XX%)
Step 4 节点关系:          PASS / FAIL  (置信度: XX%)
Step 5 置信度+学术引用:   PASS / FAIL  (置信度: XX%)
综合置信度: XX%  →  [APPROVED / REJECTED]
```
