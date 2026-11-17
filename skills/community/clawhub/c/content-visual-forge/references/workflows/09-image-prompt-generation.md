# Workflow 09 · Image Prompt Generation

根据已经完成的脚本或结构化字段，生成可直接用于图片生成的提示词。

## 全局规则

当用户提供或要求使用画家风格图鉴时，先按 `references/cover-engine/rules/painter-style-atlas.md` 转译为风格因子。提示词应写宽风格家族、线条、色彩、光线、空间、材质、构图和情绪，不默认写“某某画家风格”。

运行时默认读取 `assets/style-atlas/qiaomu-style-atlas.snapshot.json`，不为每次生成查询外部网站。

当 `visual_direction` 存在时，提示词必须继承：

- `recommended_style`
- `page_role_rhythm`
- `visual_tokens`
- `prompt_constraints`
- `anti_pattern_scan`

当 `illustration_grammar` 存在时，提示词必须继承：

- `scene_role`
- `subject_focus`
- `composition_axis`
- `camera_distance`
- `palette_temperature`
- `texture_level`
- `text_load`
- `blocked_mimicry`
- `prompt_style_phrase`

不要只写“高级、科技、极简”。必须说明标题区、主视觉区、证据区、文字安全区、留白和负面提示。小字号中文、精确中文、商业批量文字和截图标注默认交给工程化渲染或后期排版。

## 对 `knowledge-carousel`

每页一条提示词，包含：

- 比例
- 风格系统
- 页面结构
- 页面文案
- 图标 / 插画建议
- 不复制参考图布局的限制

## 对 `social-card`

每页一条提示词或渲染数据，包含：

- `1080 x 1440` / 3:4 平台画幅
- 页面角色：封面、痛点、认知、方法、证据、操作、总结或行动
- 视觉方向：来自 `visual_direction.recommended_style`
- 标题区、主视觉区、证据区、注释区和安全区
- 中文文字策略：后期排版、可编辑文字或占位区
- 配色、字体、线条、卡片、截图 / 产品图处理规则
- 与上一页 / 下一页的视觉关系
- 负面提示：避免 PPT bullet、廉价蓝紫渐变、随机霓虹、小字堆积、文字变形、标题被遮挡和风格断裂

## 对 `character-card`

每卡一条提示词，包含：

- 3:4 竖版
- 童趣学习卡风格
- 主字区
- 拼音区
- 英文义项区
- Common Words 区
- Example Sentence 区
- Useful Phrase 区
- Memory Tip 区
- 可爱贴纸 / 小插画元素
- 禁止自动加入考试名称或考试标签
- 不照搬参考图布局

## 对 `wechat-inline-image`

每张图一条提示词，包含：

- 文章段落位置
- image_role
- scene_role
- subject_focus
- camera_distance
- composition_axis
- environment_density
- text_load
- 画面隐喻或情绪目标
- 不复制参考图布局的限制
