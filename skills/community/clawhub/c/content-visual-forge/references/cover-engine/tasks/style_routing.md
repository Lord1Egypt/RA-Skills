# Task: Style Routing

## 目标
根据文章类型和情绪基调选择合适风格。

## 输出
- recommended_style
- style_reason
- alternative_styles
- rejected_styles
- risk_notes
- cover_design_family（editorial-ink / swiss-grid / default）
- theme_preset
- atlas_snapshot（如使用本地图鉴数据）
- atlas_reference（本地 entry id、family id 或用户提供的图鉴条目）
- atlas_family（宽风格家族，不是直接画家仿写）
- style_factors（线条 / 色彩 / 光线 / 空间 / 材质 / 情绪等可控因子）
- artist_name_policy（none / public_domain_allowed / avoid_artist_name）
- blocked_mimicry（禁止复制的画家签名、名作构图、IP 或装饰组合）

## 外部风格图鉴

当用户要求“更像某类画家 / 插画师 / 电影感 / 图鉴里的风格”时，先读取本地数据：

- `assets/style-atlas/qiaomu-style-atlas.snapshot.json`

再读取规则：

- `references/cover-engine/rules/painter-style-atlas.md`
- `references/cover-engine/rules/safety_copyright.md`

运行时不默认访问外部网站。将本地 snapshot 中的图鉴条目转译为宽风格家族与视觉因子，不默认输出 `in the style of {artist}`。

### 转译顺序

1. 先判断文章主题和传播意图是否适合该风格。
2. 从本地 snapshot 选择图鉴家族或条目，例如印象派空气感、东方线条留白、古典明暗、电影光影、科幻概念设计等。
3. 抽取 4-8 个可控视觉因子。
4. 标记艺术家姓名使用策略。
5. 写入可用于 Prompt Builder 的 `prompt_style_phrase`。
6. 把应避开的画家名、名作构图、IP、品牌或装饰组合写入 `blocked_mimicry`。

## 推荐逻辑
### 情感随笔
名画感、电影感、手绘水彩、治愈二次元

### 商业分析
极简杂志、现代艺术海报、抽象几何

### 技术 / AI / 产品 / 数据
优先考虑 `swiss-grid`：纸白 / 墨黑 / 单一高饱和 accent、严格网格、短标题、大数字或证据图，但数字必须来自 Source Lock。

### AI 入门 / 科普
温柔手绘知识地图、极简 editorial、低科技压迫感的信息视觉

### 历史文化
古典油画、东方美学、复古书籍封面

### 生活方式
手绘插画、印象派柔光、杂志感

## Editorial / Swiss Design System

当用户提到杂志感、瑞士风、发布会感、强网格、PPT 视觉借鉴，或当前封面需要更强信息设计时，读取：

- `references/cover-engine/rules/editorial-design-system.md`

只吸收其中的设计原则和主题预设，不复制外部模板、CSS 类名、shader、slide layout ID 或素材。
