# VERIFICATION_PROTOCOL.md — arxiv-collision-cognition

## 验证目标

确保论文碰撞推理真正产生可操作洞见而非泛泛总结，置信度 ≥ 95%。

## 五步自验证流程

### Step 1 — 已知/未知分离（项目上下文）
- [ ] `collide()` 调用时是否强制传入 `known` 和 `unknown` 字段？
- [ ] 碰撞结论是否仅基于 `known` 与论文内容的交叉点？
- [ ] `unknown` 字段中的条目是否在碰撞后被归类为「可能解决」或「仍未解决」？
- **通过标准**：known/unknown 分离率 100%；unknown 分类覆盖率 100%

### Step 2 — 碰撞日志持久化
- [ ] 每次 `collide()` 是否写入 `collision_log/arxiv_{id}_{date}.json`？
- [ ] 日志是否包含：论文摘要摘录、四向碰撞详情、可操作洞见、置信度？
- **通过标准**：日志写入成功率 100%，字段完整率 100%

### Step 3 — 四向碰撞实质性执行
- [ ] 四个视角（正/反/侧/整体）是否产生了不同的洞见（而非重复）？
- [ ] 「反面碰撞」是否真正分析了论文的局限性而非仅总结优点？
- [ ] 「侧面碰撞」是否检索了论文的 Appendix / Ablation Study？
- **通过标准**：四向洞见差异率 ≥ 60%；反面碰撞覆盖率 100%

### Step 4 — 可操作性验证（人机闭环入口）
- [ ] `actionable_insights` 列表中每条洞见是否包含「可操作动作」字段？
- [ ] 是否提供 `mark_tried(insight_id, result)` 接口，支持人类反馈证伪？
- **通过标准**：可操作洞见率 ≥ 80%；证伪接口可用

### Step 5 — 置信度标注 + 红线
- [ ] 每条洞见是否独立标注置信度？
- [ ] 综合置信度 < 70% 的碰撞是否标记为「低质量碰撞」并提示重试？
- [ ] 是否拦截将论文全文发送到第三方 API（版权保护）？
- **通过标准**：洞见级置信度覆盖率 100%；版权保护拦截率 100%

## 验证结论模板

```
验证日期: YYYY-MM-DD
ArXiv ID: XXXX.XXXXX
Step 1 已知/未知分离:   PASS / FAIL  (置信度: XX%)
Step 2 碰撞日志写入:     PASS / FAIL  (置信度: XX%)
Step 3 四向碰撞实质:     PASS / FAIL  (置信度: XX%)
Step 4 可操作性验证:     PASS / FAIL  (置信度: XX%)
Step 5 置信度+红线:      PASS / FAIL  (置信度: XX%)
综合置信度: XX%  →  [APPROVED / REJECTED]
```
