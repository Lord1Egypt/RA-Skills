# 前端与设计到代码预设

## domain_id

`frontend_design`

## common_jobs

- 生成网页或应用界面
- 根据设计稿实现代码
- Figma 写入或读取
- 建设计系统规则
- 页面重构与视觉升级
- 生成信息图、信息卡片和视觉说明页
- 生成网页型视觉叙事产物，如 narrative infographic、展示页、报告型页面

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 当前任务更偏视觉设计、设计到代码，还是现有前端重构
- 是否已有 Figma、截图、品牌规范或参考页面
- 在继续设计前，风格来源是什么
  - 用户指定风格
  - 用户提供 `DESIGN.md`
  - 用户详细描述
  - 用户从本地 `ref/design-md/` 中选择
- 更看重还原度、风格感，还是开发效率
- 是否需要移动端适配
- 是否接受额外设计执行面，如 Figma MCP

## recommended_execution_planes

- `Skill + Figma MCP + 前端工具链`
  适合设计稿实现、设计系统、界面同步
- `Skill + structured-visual-storytelling + 本地前端工程`
  适合先走统一视觉叙事主线，再落到网页信息图或展示页
- `Skill + imagegen`
  适合单张信息图、视觉海报和传播型图像成品
- `Skill + 本地前端工程`
  适合直接改现有页面
- `Skill-only`
  只适合做设计决策和结构方案，不适合最终视觉落地

## risk_and_gates

- 先确认风格偏好和品牌约束
- 视觉优先任务在风格来源未明确前，不进入具体设计
- 如果任务是信息图，先确认它是单张位图成品还是可编辑页面
- 要区分“视觉方案”与“生产代码”
- 如果没有明确设计输入，先补视觉方向，不直接实现
- 设计执行面不可用时，要保留纯文档降级路径

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 需要时补 Figma 或前端实现方向的 adapter 说明
