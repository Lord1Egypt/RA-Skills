# 图生视频提示词指南

本文档为 [`cartoon-video-creation-SKILL.md`](../cartoon-video-creation-SKILL.md) Phase 4.2（视频提示词）与 Phase 5.2（图生视频）的详细参考。Agent 在执行对应阶段时按需 Read。

---

## 1. 提示词总公式

每镜 `video_prompt` 在**与首帧同源的风格与主题**前提下，再写动态与运镜：

```text
video_prompt = 风格与主题不变块 + 角色动作 + 镜头运动 + 环境动态 + 约束标签
```

### 各块说明

| 块 | 要求 | 来源 |
|----|------|------|
| **风格与主题不变块** | 与当镜 `image_prompt` 中的 **`风格锚 + 画质锚 + 主题锚`** 语义一致，可缩写为同义短句，但不得换画风/换题材；建议直接复用 `project.json` 三字段的精简版 | `project.json`，与文生图侧**同一套** |
| 角色动作 | 慢速、连续、单一动作链 | `character slowly turns her head to the left` |
| 镜头运动 | 每镜最多 2 种运镜 | `slow dolly forward, slight tilt up` |
| 环境动态 | 1-2 个背景变化 | `wind moves loose hair strands and leaves` |
| 约束标签 | 稳定和质量约束；须含 **`consistent art style and theme with the reference frame`** 或等价表达 | 与 [`image-prompt-guide.md`](image-prompt-guide.md) 稳定性原则对齐 |

**强制**：**每一镜**的 `video_prompt` 都必须包含「风格与主题不变块」（不可因图生视频接口只接收短 prompt 而省略——可压缩字数，不可省略语义）。

---

## 2. 动作描写铁律

1. **慢速连续**：优先使用 `slowly / gently / gradually`
2. **单一动作链**：一镜仅保留一个主动作，不叠加复杂动作集
3. **可视化关节**：描述身体部位（头、肩、手、躯干）而非抽象词
4. **手势跟台词**：动作需与 `voiceover` 语义同步

### 正反例

| 类型 | 不推荐 | 推荐 |
|------|--------|------|
| 抽象动作 | `character fights` | `character lowers center of gravity, raises right arm to guard` |
| 突变动作 | `character suddenly jumps` | `character bends knees, then slowly rises and steps forward` |
| 语义脱节 | 台词“别过来”却做挥手告别 | 台词“别过来”时手掌向前阻止 |

---

## 3. 运镜术语库

| 运镜类型 | 术语 | 叙事作用 | 适用场景 |
|---------|------|---------|---------|
| 推进 | `smooth dolly forward` / `push in` | 聚焦、紧张 | 情绪升级、信息揭示 |
| 拉远 | `dolly out` / `pull back` | 释放、收束 | 高潮后回落、场景全貌 |
| 横摇 | `slow pan left/right` | 扫视、引导视线 | 场景展示、角色跟随 |
| 俯仰 | `tilt up/down` | 高低关系 | 威压、弱势、规模感 |
| 环绕 | `orbit around subject` | 戏剧感 | 角色登场、决战前 |
| 变焦 | `slow zoom in/out` | 强调细节 | 表情刻画、焦点转移 |
| 跟踪 | `tracking shot` | 临场感 | 行走、跑动、追逐 |
| 静止 | `static camera` | 稳定叙事 | 对话、沉思、停顿 |

限制：单镜最多两种运镜，避免模型执行混乱。

---

## 4. 时长映射规则

图生视频接口通常为 5 秒或 10 秒。建议：

- `duration <= 5`：生成 5 秒
- `duration > 5`：生成 10 秒
- 精确时长由 Phase 7 用 ffmpeg 裁剪/补帧

---

## 5. 连续镜头衔接（continuous）

当 `transition_hint = continuous`：

1. 在 `video_prompt` 中写明动作延续方向
2. 若可行，提取上一镜尾帧作为第二参考图
3. 下一镜首动作应继承上一镜尾姿态

示例表达：

```text
continue from previous ending pose, character keeps turning to the right while camera slowly pushes in
```

降级策略：

- 若模型不支持双参考图，自动回退单参考图模式
- 回退后保持动作方向描述不变

---

## 6. 稳定性与质量约束

建议在 `video_prompt` 末尾附加：

- `stable composition`
- `no sudden morphing`
- `anatomically correct limbs and hands`
- `consistent character appearance`
- `single centered primary subject occupying at least one-third of frame`
- `secondary characters remain distant background only`

---

## 7. 质检清单（视频段）

逐镜检查：

- [ ] **`video_prompt` 是否含与当镜文生图一致的风格与主题不变块（与 `project.json` 同源，未省略）**
- [ ] 动效画风是否与首帧一致（无「静帧日系、动效美漫」类漂移）
- [ ] 动作是否连续、无突变
- [ ] 人脸和服装是否相对稳定
- [ ] 是否出现手指/肢体异常
- [ ] 运镜是否符合 `camera_movement`
- [ ] continuous 镜头是否衔接自然
- [ ] 时长是否落在目标范围（后续可裁剪）

失败分镜标记 `retry`，仅重生该镜。

