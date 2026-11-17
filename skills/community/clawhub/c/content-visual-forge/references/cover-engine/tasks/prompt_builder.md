# Task: Prompt Builder

## 目标
根据执行路径生成不同 Prompt。

## 必须输出
- background_image_prompt
- direct_image_preview_prompt
- negative_prompt
- typography_overlay_spec
- style_atlas（如使用本地图鉴数据）

## Prompt 必须包含
- 文章主题
- 视觉风格
- 风格因子（当风格来自画家图鉴或参考图时）
- 主体场景
- 构图比例
- 留白区域
- cover_design_family 与 theme_preset（如使用 editorial / Swiss 系统）
- grid_axis 与 title_safe_zone
- 文字约束
- 审美约束
- 负面约束

## 画家图鉴风格必须转译

当 `style_routing` 提供 `atlas_snapshot` / `atlas_reference` 或用户要求使用画家风格图鉴时，Prompt Builder 必须使用本地 snapshot 派生出的 `prompt_style_phrase` 和 `style_factors`，不要直接把图鉴画家名塞进提示词，也不要在运行时重新查询外部网站。

必须体现：

- 宽风格家族：例如印象派空气感、东方线条留白、古典明暗、电影光影、科幻概念设计
- 可控因子：线条、色彩、光线、空间、材质、构图、情绪
- 反仿写约束：不要复制特定画家签名、名作构图、角色/IP、品牌元素或装饰组合

如果 `artist_name_policy` 为 `avoid_artist_name`，最终图片 Prompt 不得出现该艺术家姓名。

## 正式背景图 Prompt 的硬约束
必须包含：

```text
Do not generate any readable Chinese text. Do not generate book titles, sticky note text, notebook text, map labels, wall notes, decorative words, captions, or small text. Use blank surfaces, abstract marks, icons, routes, and non-readable textures only.
```

## Editorial / Swiss 封面提示词约束

当 `cover_design_family` 为 `editorial-ink` 或 `swiss-grid`：

- Prompt 写设计原则，不写外部项目名、模板名或 CSS 类名。
- `swiss-grid` 只允许一个 accent 策略，避免渐变、投影、圆角装饰卡和多色混搭。
- `editorial-ink` 保持纸感、墨色、留白和杂志标题轴线。
- 正式封面仍默认背景无文字，标题由 typography overlay 处理。
