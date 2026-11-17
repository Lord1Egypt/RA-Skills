# Workflow 12 · Quality Review & Retry

## 通用检查

- 内容是否忠于当前输入源
- 是否误用了历史示例
- 是否复制了参考图布局
- 中文主标题是否清楚
- 风格是否稳定
- 使用画家图鉴时，是否读取本地 snapshot 并转译为风格因子
- 是否错误地直接仿写画家名、名作构图或图鉴图片
- 是否出现未请求的体系标签
- 布局或文字是否溢出
- 是否命中 `references/config/risk-action-blacklist.md`
- 社交平台组图的视觉导演方向是否具体（内容类型、传播目标、三套差异方向、页面角色节奏）
- 启用插画语法时，scene_role、subject_focus、composition_axis、camera_distance、texture_level 和 text_load 是否稳定且服务来源内容

## cover-card 专项

- 标题是否醒目清晰
- 留白是否足够
- 装饰是否过满
- 是否错误地让小字号中文出现在图像中

## character-card 专项

- 汉字、拼音、英文义项是否正确
- 常用词和例句是否自然
- 是否出现用户未要求的考试标签

## 重试策略

- 内容错误：回到 Source Lock 或 Data Fill
- 模式错误：回到 Output Mode Router
- 视觉错误：微调提示词后单页重试
- 插画语法错误：回到 Illustration Grammar Routing，固定 scene family、composition axis、subject focus 或 text_load 后再重试
- 图鉴风格错误：回到 Style Atlas Routing，重新选择本地 snapshot 家族 / 条目并改写 `style_factors`
- 文字稳定性不足：建议切换工程化渲染
- 命中风险动作黑名单：回到对应路由或脚本修正根因；无法修正时停止交付并记录阻断原因

## 决策表

| 状态 | 判定条件 | 下一步 |
|---|---|---|
| `pass` | 内容忠实、文字可读、风格稳定、无版权/IP 风险 | 交付结果；正式执行时写入 Run Log |
| `minor_revision` | 局部文字、留白、色彩或构图可小修 | 最多微调 2 次；每次复查质量门禁 |
| `regenerate_required` | 主题跑偏、事实错误、严重错字、图鉴仿写、版权/IP 风险 | 回到对应阶段：Source Lock、Data Fill、Style Atlas Routing 或 Prompt Builder |
| `source_unreadable` | 当前输入源不可读取或关键事实缺失 | 停止生成；要求用户补充来源，或仅输出 `prompt_package` 草案并标注风险 |
| `commercial_text_risk` | 批量、商用、中文字段必须精确但当前路径依赖图像模型排字 | 强制切换 `engineering_rendering` |
| `style_atlas_unavailable` | 本地 snapshot 缺失、损坏、过期不可用或不适合当前任务 | 不查询外部网站；退回模板族默认风格并记录风险 |
| `blacklisted_action_hit` | 命中风险动作黑名单，如跳过 Source Lock、硬裁封面对、复制模板、不可读来源硬生成或商用精确文字直接生图 | 回到 Source Lock、Output Mode Router、Execution Mode Router、页面脚本或工程化渲染；连续 2 次仍失败则停止交付 |
| `visual_direction_risk` | 视觉导演方向空泛、风格候选无差异、页面角色单一或反模式未修复 | 回到 Visual Direction Routing，补齐内容类型、传播目标、三套差异方向、页面角色节奏和反模式扫描 |
| `illustration_grammar_risk` | 插画语法缺失、组内场景不连续、主体比例漂移、装饰随机或复制外部参考视觉签名 | 回到 Illustration Grammar Routing，重设 scene family、recurring subjects、composition rules、text_load 和 blocked_mimicry |

## 循环上限

- 同一问题最多连续重试 2 次。
- 2 次后仍未通过，必须升级路径、缩小范围或停止交付，并在 Run Log 中记录原因。
