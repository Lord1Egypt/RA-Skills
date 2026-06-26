# Tested Workflow - 2026-02-06

## 测试项目：熊市坚守者

**Project ID:** `1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5`

**完整流程运行时间:** ~35-40 分钟

---

## ✅ 实际运行步骤

### 1. 创建项目

```bash
node scripts/giggle-api.js create-project "熊市坚守者" --aspect 9:16
```

- ✅ 成功
- 耗时：<1秒
- 返回：project_id

### 2. 生成剧本

```bash
node scripts/giggle-api.js generate-script 1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5 "一个年轻的crypto交易员在2022年熊市中亏损惨重，女友离开，朋友嘲笑。他在深夜独自看着屏幕上的红色K线，几乎要放弃。但他选择坚持学习和研究。两年后，2024年牛市来临，他的坚持终于得到回报，账户翻了百倍。故事要有情感起伏，从绝望到希望。" --duration 60
```

- ✅ 成功
- 耗时：~20秒
- 自动更新进度：`current_step: character, completed: script`

### 3. 生成角色

```bash
node scripts/giggle-api.js generate-characters 1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5
```

- ✅ 成功
- 耗时：~2分钟
- 生成角色：阿明、小雅（2个角色）
- 自动更新进度：`current_step: storyboard, completed: script,character`

### 4. 生成分镜

```bash
node scripts/giggle-api.js generate-storyboard 1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5
```

- ⚠️ Polling 显示一直 pending，但实际已完成
- 用 `project-status` 确认：12 个 shots 已生成
- 耗时：~30-60秒（实际生成时间）
- **问题**：polling 逻辑有问题，timeout 后需要手动检查状态
- 自动更新进度：`current_step: shot, completed: script,character,storyboard`

### 5. 生成图片

```bash
node scripts/giggle-api.js generate-images 1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5
```

- ✅ 成功
- 耗时：~2分钟（12张图片）
- 状态：12 done, 0 failed
- 自动更新进度：`current_step: video, completed: script,character,storyboard,shot`

### 6. 生成视频

```bash
# ❌ 错误尝试（文档中的模型名）
node scripts/giggle-api.js generate-videos 1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5 --model kling
# 报错：API Error [500]: get storyboard shot price failed: record not found

node scripts/giggle-api.js generate-videos 1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5 --model minimax
# 报错：同样错误

node scripts/giggle-api.js generate-videos 1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5 --model runway
# 报错：同样错误

# ✅ 正确方法（使用默认模型）
node scripts/giggle-api.js generate-videos 1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5
```

- ✅ 成功（使用默认模型 wan25）
- 耗时：~15-20分钟（12个视频）
- 初始状态：1个失败，11个 pending
- 最终状态：12 done, 0 failed
- 自动更新进度：`current_step: export, completed: script,character,storyboard,shot,video`

### 7. 导出

```bash
node scripts/giggle-api.js export 1b6f4d97-7ac0-4a6f-a68e-68e9d0c06bb5
```

- ✅ 成功
- 耗时：~5-10分钟
- 进度显示：1000%, 7500%, 10000%（这是正常的）
- 最终在 assets 中可见

---

## 🔑 关键发现

### 1. 视频模型名称

**文档错误：** `--model kling`、`--model runway`
**正确名称：**

- `wan25`（默认，推荐）
- `kling25`, `kling26`
- `minimax`, `minimax23`
- `sora2`, `sora2-pro`, `sora2-fast`
- `veo31`
- `seedance15-pro`
- `grok`, `grok-fast`

### 2. 分镜生成 Polling

- Polling 可能显示一直 pending
- 实际上分镜已经生成完成
- 需要用 `project-status` 或 `list-storyboard` 验证

### 3. 导出进度

- 显示 1000%+是正常的
- 等待 "Export completed" 消息

### 4. 进度自动同步

每个步骤完成后都会自动调用 `/api/v1/project/update` 更新进度：

- generate-script → `current_step: character, completed: script`
- generate-characters → `current_step: storyboard, completed: script,character`
- generate-storyboard → `current_step: shot, completed: script,character,storyboard`
- generate-images → `current_step: video, completed: script,character,storyboard,shot`
- generate-videos → `current_step: export, completed: script,character,storyboard,shot,video`

---

## 📊 时间估算（基于实际测试）

| 步骤             | 预估时间      | 实际时间    |
| ---------------- | ------------- | ----------- |
| 创建项目         | <1秒          | <1秒        |
| 生成剧本         | 10-30秒       | ~20秒       |
| 生成角色（2个）  | 1-2分钟       | ~2分钟      |
| 生成分镜（12个） | 30秒-1分钟    | ~1分钟      |
| 生成图片（12张） | 2-4分钟       | ~2分钟      |
| 生成视频（12个） | 15-30分钟     | ~18分钟     |
| 导出             | 5-10分钟      | ~7分钟      |
| **总计**         | **25-45分钟** | **~30分钟** |

---

## ✅ 最佳实践

1. **不要指定 --model**，使用默认的 wan25
2. **分镜 polling timeout 后手动检查状态**
3. **视频生成放后台，定期用 video-status 检查**
4. **导出的百分比显示异常是正常的**

---

## 🐛 已知问题

1. 分镜生成的 polling 逻辑不准确
2. 视频生成可能偶尔有单个 shot 失败，但会自动重试成功
3. 导出进度显示为原始值（需要除以100）
