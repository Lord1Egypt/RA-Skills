# VERIFICATION_PROTOCOL.md — diepre-vision-cognition

## 验证目标

确保视觉认知 Skill 在 DiePre 场景下严格遵循 SOUL 框架，置信度 ≥ 95%。

## 五步自验证流程

### Step 1 — 视觉已知/未知分离
- [ ] `analyze()` 是否返回 `known_features`（清晰可测量特征）和 `uncertain_regions`（模糊区域）？
- [ ] 最终缺陷判断是否仅从 `known_features` 推导？
- **通过标准**：不确定区域不参与最终判决，置信度单独标注

### Step 2 — 视觉日志持久化
- [ ] 每次 `analyze()` 是否写入 `vision_log/YYYY-MM-DD.jsonl`？
- [ ] 日志是否包含原始图像路径、特征向量、置信度、判决结果？
- **通过标准**：日志写入成功率 100%，字段完整率 100%

### Step 3 — 四向视觉碰撞
- [ ] 是否从「正视角」「反转180°」「侧光增强」「整体布局」四个维度分析同一图像？
- [ ] 四个视角结果是否参与最终置信度加权？
- **通过标准**：四向覆盖率 100%，单视角独裁率 0%

### Step 4 — 人机闭环质检
- [ ] 是否提供 `add_human_label(image_id, label, notes)` 接口？
- [ ] 人工标注是否触发本地模型微调或规则更新？
- **通过标准**：标注注入后，同类图像识别准确率提升 ≥ 5%

### Step 5 — 置信度阈值 + 红线
- [ ] 置信度 < 90% 的结果是否自动标记为 `REQUIRES_HUMAN_REVIEW`？
- [ ] 是否拦截将原始图像数据发送到外部接口的行为？
- **通过标准**：低置信度升级率 100%；数据外泄拦截率 100%

## 验证结论模板

```
验证日期: YYYY-MM-DD
Step 1 视觉已知/未知:     PASS / FAIL  (置信度: XX%)
Step 2 视觉日志写入:       PASS / FAIL  (置信度: XX%)
Step 3 四向视觉碰撞:       PASS / FAIL  (置信度: XX%)
Step 4 人机闭环质检:       PASS / FAIL  (置信度: XX%)
Step 5 置信度阈值+红线:    PASS / FAIL  (置信度: XX%)
综合置信度: XX%  →  [APPROVED / REJECTED]
```
