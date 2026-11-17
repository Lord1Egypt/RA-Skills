# Template Family · wechat-inline-image

## 定位

公众号文内配图 / 情绪过渡图 / 分节图 / 尾图。

它不是小红书知识卡，也不是系列解释卡。它的任务是服务公众号正文阅读体验。

## 适合场景

- 文章段落之间的情绪过渡
- 影评 / 散文 / 随笔中的氛围图
- 观点文中的关键句配图
- 文章末尾的尾图收束
- 长文中的视觉呼吸点

## 默认规则

- 不使用页码胶囊
- 不强制标题
- 不强制信息卡片
- 不强制列表
- 不默认生成固定数量
- 文字极少，必要时只保留一句短句
- 图像重氛围、留白、节奏、情绪

## 视觉原则

- 画面应像“文章的一次停顿”
- 可以无文字
- 可以是一句短句
- 不需要解释完整观点
- 不要把文章重新讲一遍

## 插画增强版

当用户要求插画感、场景连续性、高质量成图，或文章类型适合用氛围图承接阅读节奏时，启用 `Illustration Grammar Routing`。

注意：这只是一组数据与提示词约束，不表示 `wechat-inline-image` 模板本身会生成插画。插画主体仍应来自生成图、授权图或已记录来源的素材。

必须补齐：

- scene_role
- subject_focus
- composition_axis
- camera_distance
- motion_state
- environment_density
- palette_temperature
- line_character
- texture_level
- text_load
- prompt_style_phrase
- blocked_mimicry

推荐用于：

- 文章段落之间的场景化停顿
- 影评 / 散文 / 随笔中的连续氛围图
- 观点文结尾的情绪收束图
- 需要统一视觉叙事的公众号文内图组

如果文字精确度高于画面情绪，退回普通文内配图模板或工程化渲染文本层。

## 与其他模式的区别

| 模式 | 目标 | 文案量 | 画面重点 |
|---|---|---|---|
| cover-card | 点击与定调 | 中低 | 标题感、识别度 |
| wechat-inline-image | 阅读节奏 | 极低 | 氛围、留白、情绪 |
| knowledge-carousel | 信息传播 | 中高 | 结构、要点、可转发 |
| character-card | 学习记忆 | 中 | 字段准确、教学性 |
