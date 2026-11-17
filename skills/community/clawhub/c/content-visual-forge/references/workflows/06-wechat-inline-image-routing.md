# Workflow 06 · WeChat Inline Image Routing

当输出模式为 `wechat-inline-image` 时执行。

## 目标

根据文章类型、长度与阅读节奏，决定是否需要文内配图、需要几张、每张放在哪里、是否需要文字。

## 判断步骤

### 1. 判断文章类型

- 教程 / 方法论
- 观点文章
- 影评 / 散文 / 情绪随笔
- 产品介绍
- 短文
- 新闻 / 报告解读
- 个人故事

### 2. 判断图片数量

参考：`references/config/wechat-image-count-rules.md`

### 3. 判断每张图的职责

- opening：开头定调
- section-break：段落过渡
- quote-image：承载关键短句
- atmosphere：纯氛围图
- ending：结尾收束

### 3A. 判断是否启用插画语法

当图片职责是 `opening`、`section-break`、`atmosphere` 或 `ending`，且用户强调成图质感、统一性、故事感或插画感时，必须进入 `references/config/illustration-grammar.md` 对应的路由，生成：

- scene_role
- subject_focus
- composition_axis
- camera_distance
- palette_temperature
- texture_level
- text_load
- blocked_mimicry
- prompt_style_phrase

如果文本信息优先于画面情绪，保持普通文内配图路径，不强行启用插画语法。

### 4. 判断文字策略

- 默认无页码
- 默认少文字
- 可以无文字
- 如果有文字，只保留一句短句
- 不做大段解释
- 不做知识卡式列表

## 输出

每张文内图输出：

- 位置：建议放在哪个段落后
- 类型：opening / section-break / quote-image / atmosphere / ending
- 是否放文字
- 文案内容
- 画面隐喻
- 生图提示词
- 质检要点
