# 质检和重做完整流程

## 概览

质检是确保短剧质量的关键环节。本文档详细说明如何进行质检、如何根据质检结果重做、以及自动化流程。

---

## 🎯 质检流程

### 1. 何时进行质检

**推荐时机：**

- ✅ 视频生成完成后（export 之前）
- ✅ 单个镜头生成失败后重试前
- ❌ 不要在图片阶段质检（浪费成本）

### 2. 运行质检

```bash
# 基础质检（使用配置的模型和阈值）
node scripts/quality-check.js <project_id>

# 自定义参数
node scripts/quality-check.js <project_id> --model opus --threshold 85

# JSON 输出（便于 AI agent 解析）
node scripts/quality-check.js <project_id> --json
```

### 3. 质检输出

**终端输出：**

```
Extracting frames...
Analyzing shot 1... Score: 85 ✅
Analyzing shot 2... Score: 72 ⚠️
Analyzing shot 3... Score: 65 ❌
...
Average score: 74.3
❌ QC failed (threshold: 80)

Low-score shots:
  Shot 2 (72): Face inconsistency
  Shot 3 (65): Motion blur, Lighting issue
```

**JSON 报告：** `output/<project_id>/qc-report.json`

```json
{
  "project_id": "proj_xxx",
  "timestamp": "2026-02-06T23:00:00Z",
  "average_score": 74.3,
  "passed": false,
  "threshold": 80,
  "shots": [
    {
      "shot_id": 1,
      "score": 85,
      "passed": true,
      "breakdown": {
        "temporal_consistency": 88,
        "motion_dynamics": 82,
        "visual_clarity": 86,
        "lighting_interaction": 84
      },
      "issues": []
    },
    {
      "shot_id": 2,
      "score": 72,
      "passed": false,
      "breakdown": {...},
      "issues": [
        "Face inconsistency detected",
        "Minor color shift"
      ],
      "suggested_action": "regenerate_with_same_model"
    },
    {
      "shot_id": 3,
      "score": 65,
      "passed": false,
      "breakdown": {...},
      "issues": [
        "Severe motion blur",
        "Lighting mismatch with previous shot"
      ],
      "suggested_action": "regenerate_with_different_model"
    }
  ],
  "retry_recommendations": {
    "retry_same_model": [2],
    "retry_different_model": [3],
    "modify_prompt": []
  }
}
```

---

## 🔄 重做流程

### 1. 自动重试低分镜头

```bash
# 方法1：基于质检报告自动重试
node scripts/giggle-api.js retry-low-score <project_id> --threshold 80

# 方法2：重试所有失败的
node scripts/giggle-api.js retry-all-failed <project_id>
```

**逻辑：**

1. 读取质检报告
2. 找出低于阈值的 shots
3. 根据 `suggested_action` 决定策略：
   - `regenerate_with_same_model` → 用相同模型重试
   - `regenerate_with_different_model` → 换模型（wan25 → kling25 → minimax）
   - `modify_prompt` → 简化/修改 prompt 后重试

### 2. 手动重试单个镜头

```bash
# 用相同模型重试
node scripts/giggle-api.js retry-video <project_id> <shot_id>

# 换模型重试
node scripts/giggle-api.js retry-video <project_id> <shot_id> --model kling25

# 修改 prompt 后重试（需要先 update-shot）
node scripts/giggle-api.js update-shot <project_id> <shot_id> --prompt "简化的描述"
node scripts/giggle-api.js retry-video <project_id> <shot_id>
```

### 3. 重做更早期的步骤

如果问题出在更早期（角色、分镜），需要级联重做：

#### 🔄 修改角色后重做

```bash
# 1. 更新角色描述
node scripts/giggle-api.js update-character <char_id> --prompt "更清晰的描述"

# 2. 重新生成角色图片
node scripts/giggle-api.js regenerate-character <project_id> --name "角色名"

# 3. 受影响的需要重做：
#    ❌ 剧本 - 不需要
#    ❌ 分镜 - 不需要
#    ✅ 图片 - 需要重新生成（使用新的角色）
#    ✅ 视频 - 需要重新生成

# 重新生成图片
node scripts/giggle-api.js generate-images <project_id>

# 重新生成视频
node scripts/giggle-api.js generate-videos <project_id>
```

#### 🔄 修改分镜后重做

```bash
# 1. 更新分镜描述
node scripts/giggle-api.js update-shot <project_id> <shot_id> --prompt "新的镜头描述"

# 2. 受影响的需要重做：
#    ✅ 该镜头的图片
#    ✅ 该镜头的视频

# 重新生成单个镜头的图片（需要手动调用单镜头生成API）
# 重新生成单个镜头的视频
node scripts/giggle-api.js retry-video <project_id> <shot_id>
```

#### 🔄 修改剧本后重做

```bash
# ⚠️ 注意：修改剧本影响最大，需要重做几乎所有步骤

# 1. 更新剧本
node scripts/giggle-api.js update-script <project_id> --ai "新剧本内容"

# 2. 受影响的需要重做：
#    ✅ 角色 - 可能需要重新生成
#    ✅ 分镜 - 需要重新生成
#    ✅ 图片 - 需要重新生成
#    ✅ 视频 - 需要重新生成

# 建议：除非必要，否则不要修改剧本！
```

---

## 🤖 完整的质检+重做循环

### 手动流程

```bash
# 1. 生成视频
node scripts/giggle-api.js generate-videos <project_id>

# 2. 质检
node scripts/quality-check.js <project_id>

# 3. 如果不通过，查看报告
cat output/<project_id>/qc-report.json

# 4. 根据建议重试
node scripts/giggle-api.js retry-low-score <project_id> --threshold 80

# 5. 等待重试完成，再次质检
node scripts/giggle-api.js video-status <project_id>
node scripts/quality-check.js <project_id>

# 6. 重复步骤 4-5，直到通过

# 7. 导出
node scripts/giggle-api.js export <project_id>
```

### 自动化流程（未来实现）

```bash
# 一键生成 + 自动质检 + 自动重试
node scripts/auto-generate.js <project_id> \
  --quality-check \
  --auto-retry \
  --max-iterations 3
```

**逻辑：**

```
生成视频
  ↓
质检打分
  ↓
平均分 >= 80? ──Yes──> 导出
  ↓ No
找出低分镜头
  ↓
分析原因
  ↓
应用修复策略：
  - 相同模型重试
  - 换模型重试
  - 简化 prompt 重试
  ↓
重新生成
  ↓
质检打分
  ↓
迭代次数 < 3? ──Yes──> 继续循环
  ↓ No
报告失败的镜头，等待人工决策
```

---

## 📊 质检评分标准

### 单片段质量（Single Clip）

| 维度       | 权重 | 说明                                 |
| ---------- | ---- | ------------------------------------ |
| 时空一致性 | 35%  | 角色特征、服装、环境在镜头内保持稳定 |
| 动态动力学 | 30%  | 运动符合物理规律，无跳帧、畸变       |
| 视觉纯净度 | 20%  | 画面清晰，无 AI 噪点、液化           |
| 光影交互   | 15%  | 光影随物体运动同步变化               |

### 评分等级

| 分数   | 等级      | 建议             |
| ------ | --------- | ---------------- |
| 80-100 | 优良 ✅   | 可直接使用       |
| 60-79  | 及格 ⚠️   | 可考虑使用或重试 |
| <60    | 不合格 ❌ | 必须重新生成     |

---

## 💰 成本考虑

### 质检成本

使用 Claude vision 评分：

- **单镜头**：~0.5 credits ($0.005)
- **12镜头项目**：~6 credits ($0.06)
- **带重试（3次迭代）**：~18 credits ($0.18)

### 重做成本

- **重试视频**：与首次生成相同（wan25: 88 credits/shot）
- **换模型重试**：可能更贵或更便宜（kling25: 不同价格）

**优化建议：**

- ✅ 首次生成时就用高质量模型，减少重试
- ✅ 质检只在视频阶段，不在图片阶段
- ✅ 设置合理阈值（80 是平衡点）

---

## 🎯 最佳实践

### 1. 预防优于治疗

**在生成前优化：**

- ✅ 剧本清晰、逻辑连贯
- ✅ 角色描述详细、特征明确
- ✅ 分镜描述具体、动作简单

### 2. 分阶段质检

**不要等到最后：**

- 生成角色后 → 人工检查角色一致性
- 生成图片后 → 人工检查构图和角色
- 生成视频后 → 自动质检 + 人工验收

### 3. 建立重试策略

**根据问题类型决定：**

- 角色不一致 → 重新生成角色
- 动作异常 → 简化 prompt
- 光影问题 → 换模型
- 小瑕疵 → 接受或微调

### 4. 记录和学习

**每次重试都记录：**

- 原因是什么？
- 用了什么策略？
- 结果如何？
- 下次如何避免？

---

## 🚨 常见问题

### Q: 质检一直不通过怎么办？

**A: 降低阈值或接受瑕疵**

- 阈值 80 是理想值，70-75 也可接受
- 单个镜头不佳，整体流畅即可
- 重试 3 次以上，成本效益下降

### Q: 重试后分数反而更低？

**A: 换策略或回退**

- 尝试不同模型
- 简化 prompt
- 使用之前较好的版本

### Q: 什么时候该放弃重试？

**A: 时间和成本达到预算时**

- 重试超过 3 次
- 成本超过预期 50%
- 时间超过 2 小时

### Q: 能否跳过质检？

**A: 可以，但不推荐**

- 快速原型：可以跳过
- 正式项目：必须质检
- 面向用户：强烈建议质检

---

## 📝 总结

**质检和重做是确保质量的关键，遵循以下原则：**

1. ✅ **预防为主**：在生成前做好准备
2. ✅ **分阶段检查**：不要等到最后
3. ✅ **自动化优先**：用工具减少人工
4. ✅ **建立策略**：根据问题类型决定重试方式
5. ✅ **控制成本**：设置重试上限

**记住：质量和成本需要平衡，80分是合理的目标！**
