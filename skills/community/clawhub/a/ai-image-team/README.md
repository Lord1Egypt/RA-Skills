# 🎨 AI 电商图片创作团队 - 使用说明

## 快速开始

### 方法 1：团队自动协作（推荐）

在聊天中直接说：
```
帮我生成一张电商海报，产品是新款运动鞋，风格科技感
```

团队会自动完成：
1. 🧠 策划师分析需求
2. 🎭 执行师生成图片
3. ✅ 质检师质量把关
4. 📤 交付成品

### 方法 2：单独使用成员技能

每个成员都是独立技能，可单独调用：

```bash
# 策划师 - 分析需求
openclaw skills run ai-planner --input "分析：淘宝主图，女士连衣裙，简约优雅"

# 执行师 - 生成图片
openclaw skills run ai-maker --input "用即梦生成一张海报，产品是运动鞋"

# 质检师 - 质检图片
openclaw skills run ai-reviewer --input "质检这些图片：[...]"
```

## 使用示例

### 示例 1：淘宝主图
```
我需要一张淘宝主图，产品是女士连衣裙，白色雪纺材质，
风格简约优雅，目标人群是 25-35 岁职场女性
```

### 示例 2：食品海报
```
用即梦生成一张食品海报，产品是手工巧克力，
要突出食欲感和高级感，用于微信公众号推文
```

### 示例 3：数码产品
```
生成一张蓝牙耳机主图，科技感，用于京东店铺，
背景要简洁，突出产品细节
```

## 工作流

```
用户输入
   ↓
🧠 策划师 → 创意简报（Prompt + 负面词 + 工具推荐）
   ↓
🎭 执行师 → 生成 1-4 张初稿
   ↓
✅ 质检师 → 质检报告
   ↓
┌─────────────────────────────────┐
│ 通过 → 交付 ✅                   │
│ 小问题 → 微调后交付 ⚠️          │
│ 大问题 → 重新规划 ❌             │
└─────────────────────────────────┘
```

## 配置说明

### 启用/禁用成员

编辑 `config/team_config.json`：
```json
{
  "members": {
    "planner": {"enabled": true},
    "maker": {"enabled": true},
    "reviewer": {"enabled": true}
  }
}
```

### 质量阈值

```json
{
  "quality_threshold": 0.8,
  "max_iterations": 3
}
```

### 添加工具

编辑 `skills/ai-maker/config/tools_config.json`：
```json
{
  "image_tools": [
    {"id": "jimeng", "name": "即梦", "enabled": true},
    {"id": "liblib", "name": "LiblibAI", "enabled": true},
    {"id": "midjourney", "name": "Midjourney", "enabled": false}
  ]
}
```

## 扩展功能

### 启用视频生成

编辑 `skills/ai-maker/config/tools_config.json`：
```json
{
  "video_tools": [
    {"id": "jimeng_video", "name": "即梦视频", "enabled": true}
  ]
}
```

### 添加新成员

1. 创建新技能目录：`skills/新技能/`
2. 在 `config/team_config.json` 注册
3. 在 `agent.py` 中集成

## 独立技能说明

### 🧠 策划师 (ai-planner)

**职责**：需求分析、创意简报、Prompt 优化

**使用**：
```
帮我分析这个需求：我需要一张淘宝主图，产品是...
```

**输出**：创意简报（Prompt、负面词、工具推荐）

---

### 🎭 执行师 (ai-maker)

**职责**：调用 AI 工具生成图片

**使用**：
```
用即梦生成一张海报，产品是...
```

**输出**：1-4 张图片 + 生成参数

**工具**：即梦、LiblibAI（可扩展）

---

### ✅ 质检师 (ai-reviewer)

**职责**：质量评估、迭代建议

**使用**：
```
质检这些图片：[...]
```

**输出**：质检报告（通过/微调/返工）

**标准**：80 分通过，常开模式

---

## 常见问题

### Q: 如何指定使用哪个工具？
A: 在需求中说明，如"用即梦生成..."或"用 Liblib 生成..."

### Q: 可以批量生成吗？
A: 可以，说明需要数量，如"生成 4 张不同风格的方案"

### Q: 生成不满意怎么办？
A: 质检师会给出迭代建议，团队会自动微调或重新规划

### Q: 如何启用视频生成？
A: 在 `skills/ai-maker/config/tools_config.json` 中启用视频工具

## 项目记录

所有项目记录保存在 `memory/project_history.md`

---

*技能版本：1.0.0*
*最后更新：2026-03-31*
