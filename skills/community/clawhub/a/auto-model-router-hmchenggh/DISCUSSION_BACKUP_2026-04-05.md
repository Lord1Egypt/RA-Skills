# Auto Model Router Skill - 讨论记录备份

> 创建时间：2026-04-05
> 讨论时长：约1-2小时

---

## 一、项目背景

用户希望为 OpenClaw 设计一个名为 **Auto Model Router** 的技能，功能是：
- 根据任务类型自动选择最佳模型
- 用户只需提供 N 个模型（1-8个），系统自动分配到8个工作范畴
- 支持 Plan A（国际模型）和 Plan B（国内模型）
- 处理未知任务和未知模型的降级机制
- 使用多智能体架构处理突发/中断任务

---

## 二、8个工作范畴定义

| # | 范畴 | 说明 | 关键词示例 |
|---|------|------|-----------|
| 1 | high_logic | 高逻辑推理 | 逻辑分析、数学证明、复杂推理 |
| 2 | code_generation | 代码生成 | 写代码、debug、函数实现 |
| 3 | creative_writing | 创意写作 | 写故事、写文案、内容创作 |
| 4 | info_reading | 信息阅读 | 总结文档、提取信息、问答 |
| 5 | simple_repeat | 简单重复 | 格式转换、复制粘贴、简单翻译 |
| 6 | image_understanding | 图片理解 | 分析图片、OCR、图表解读 |
| 7 | image_generation | 图片生成 | 生成图片、设计图、海报 |
| 8 | video_audio | 视频/音频 | 视频理解、音频处理 |

---

## 三、Plan A - 国际模型配置

```json
{
  "high_logic": {"primary": "anthropic/claude-opus-4", "fallback": "deepseek/deepseek-r1"},
  "code_generation": {"primary": "openai/gpt-4.5", "fallback": "anthropic/claude-sonnet-4"},
  "creative_writing": {"primary": "openai/gpt-4o", "fallback": "minimax/minimax-2.7"},
  "info_reading": {"primary": "anthropic/claude-haiku", "fallback": "google/gemini-flash"},
  "simple_repeat": {"primary": "google/gemini-flash-lite", "fallback": "openai/gpt-4o-mini"},
  "image_understanding": {"primary": "anthropic/claude-sonnet-4", "fallback": "google/gemini-2.0"},
  "image_generation": {"primary": "openai/dall-e-3", "fallback": "stability/stable-diffusion"},
  "video_audio": {"primary": "openai/gpt-4o", "fallback": "google/gemini-2.0"}
}
```

---

## 四、Plan B - 国内模型配置

```json
{
  "high_logic": {"primary": "deepseek/deepseek-r1", "fallback": "zhipu/glm-5"},
  "code_generation": {"primary": "zhipu/glm-5", "fallback": "moonshot/kimi-k2"},
  "creative_writing": {"primary": "minimax/minimax-m2.5", "fallback": "baidu/wenxin-5.0"},
  "info_reading": {"primary": "minimax/minimax-01", "fallback": "zhipu/glm-4-long"},
  "simple_repeat": {"primary": "zhipu/glm-4-flash", "fallback": "deepseek/deepseek-v3"},
  "image_understanding": {"primary": "minimax/minimax-vl-01", "fallback": "zhipu/glm-4.6v"},
  "image_generation": {"primary": "tencent/hunyuan-image", "fallback": "bytedance/doubao-seed"},
  "video_audio": {"primary": "vidu/vidu-q3", "fallback": "kuaishou/kling-2.6"}
}
```

---

## 五、智能分配算法

用户输入 N 个模型（1-8个），系统按优先级自动分配：

1. **N = 1**：所有范畴使用同一模型
2. **N = 2-3**：
   - 高优先级范畴（high_logic, code_generation）优先分配
   - 其他范畴使用 fallback 或复制最近似的模型
3. **N >= 4**：按范畴优先级顺序分配，确保每个关键范畴有专属模型

---

## 六、未知处理机制

### 未知任务类型
- 关键词匹配失败时，使用 intent detection 分析
- 仍无法判断时，默认归类为 `info_reading`
- 记录为"未知任务"，返回给用户确认

### 未知模型
- 用户提供的模型不在配置列表中
- 系统尝试语义匹配最相似的范畴
- 无法匹配时，标记为"待配置"，提示用户提供

---

## 七、GitHub 上传信息

- **仓库地址**：https://github.com/HMCHENGGH/auto-model-router
- **上传时间**：2026-04-05
- **上传内容**：
  - SKILL.md - 技能规格文档
  - README.md - 用户指南
  - config/plan-a.json - 国际模型配置
  - config/plan-b.json - 国内模型配置
  - config/default.json - 默认配置
  - task-rules.json - 任务分类规则

---

## 八、后续步骤

1. **等待期**：在 GitHub 上放置一周（2026-04-12）
2. **检查**：确认无 PR 或 merges
3. **发布**：如有改动，合并后发布到 ClawHub
4. **如无变动**：一周后直接发布到 ClawHub

---

## 九、关键决定

1. 用户提供 N 个模型，系统自动分配到 8 个范畴
2. 不需要用户手动配置每个范畴
3. Plan A 和 Plan B 分开，用户按需选择
4. 多智能体架构处理突发任务
5. 未知情况有明确的降级 fallback

---

## 十、文件清单

```
auto-model-router/
├── SKILL.md              # 技能规格文档
├── README.md             # 用户使用指南
├── config/
│   ├── plan-a.json       # Plan A 国际模型
│   ├── plan-b.json       # Plan B 国内模型
│   └── default.json      # 默认配置
└── task-rules.json       # 任务分类规则
```

---

*备份记录结束*
