# 中文语义动漫推荐 Skill 技术方案

## 1. 背景和目标

我们要做的不是传统的「按标签找相似番」，也不是让 LLM 凭记忆直接推荐。目标是做一个中文优先、可持续迭代的本地动漫推荐 Skill：

- 能理解用户自然语言里的细腻偏好，例如「有时间流逝后的余韵」「不是王道热血」「世界观大但叙事克制」。
- 能基于可靠数据源生成候选，避免幻觉、年份错误、作品不存在等问题。
- 能根据用户反馈快速变准，例如「这些都看过」「第二个方向对，但别那么致郁」「热门可以，不用强行冷门」。
- 先服务我们自己本地使用，后续再考虑公共服务器版本。

核心原则：

```text
数据源负责事实和候选范围
算法负责质量、边界和排序
LLM 负责语义理解、精排和解释
用户反馈负责持续校准
```

## 2. 产品形态

第一阶段做成本地 Agent Skill + CLI：

```text
用户自然语言
  -> 本地 Skill
  -> Bangumi / AniList API
  -> 本地 SQLite 缓存
  -> experience_profile + embeddings
  -> LLM rerank
  -> 推荐结果
  -> 用户反馈
  -> 更新用户画像
```

暂时不做服务器。服务器会带来运维、成本、隐私、API 合规和数据更新复杂度。先验证推荐质量更重要。

## 3. 数据源选择

### 3.1 Bangumi

Bangumi 是中文优先的主数据源。

主要用途：

- 中文名、原名、简介
- 播出日期、平台、集数
- 评分、评分人数、排名
- 收藏统计：想看、看过、在看、搁置、抛弃
- 用户标签、公共标签
- 章节信息
- 角色、声优、制作人员
- 关联条目：续作、前传、剧场版、外传等

适合：

- 中文 ACG 语境
- 中文标题搜索
- 社区评分和收藏热度
- 推荐解释里的中文展示

限制：

- 社区维护数据，长尾条目字段质量不稳定。
- 搜索接口存在实验性特征，不能假设永远稳定。
- 不适合作为「哪里能看」「版权归属」的数据源。
- 冷门短片、实验动画、国产 Web 动画等可能评分人数少、标签稀疏。

### 3.2 AniList

AniList 是辅助结构化数据源。

主要用途：

- 英文/罗马音/日文标题
- 更结构化的 genre/tag
- 格式、年份、人气、评分
- 跨语种匹配

适合补充 Bangumi 标签稀疏的问题，尤其是内容警告、叙事类型、题材标签等。

### 3.3 暂不作为主数据源

- 豆瓣：中文语境强，但公开 API 和合规性不适合作为后端主源。
- B 站：可后续补充播放入口和国内热度，但公开稳定性不足。
- MAL/Jikan：可作为后续补充，不作为中文 MVP 主路径。

## 4. 本地数据存储

需要在本地保存一份衍生数据，但不是复制完整 Bangumi 全库。

本地保存三类数据：

```text
1. 原始 API 缓存
2. 标准化后的作品元数据
3. LLM 生成的 experience_profile + embeddings
```

建议使用 SQLite：

```text
data/anime.sqlite
  source_cache
  subjects
  experience_profiles
  embeddings
  user_feedback
  user_profile
```

示例表设计：

```text
subjects:
  id
  source
  source_id
  name
  name_cn
  summary
  date
  platform
  eps
  score
  rating_total
  rank
  collection_total
  tags_json
  images_json
  updated_at

experience_profiles:
  subject_id
  profile_text
  facets_json
  profile_json
  model
  confidence
  source_hash
  generated_at

embeddings:
  subject_id
  vector_kind
  vector
  text_hash
  model
  dimensions

user_feedback:
  subject_id
  feedback_type
  comment
  created_at

user_profile:
  profile_json
  updated_at
```

MVP 不抓全库，采用按需缓存 + 高质量候选池预热：

```text
V0: 用户搜到什么、推荐召回到什么，就缓存什么
V1: 预热高质量候选池，例如评分人数 >= 300、收藏数 >= 500
V2: 扩展中腰部和挖宝池，例如评分人数 >= 50、收藏数 >= 100
V3: 定期增量刷新热门、新番和用户高频领域
```

## 5. 体验画像 experience_profile

传统标签只能表达「奇幻」「治愈」「旅行」，但用户真正需要的是更细的语义：

- 时间感
- 关系余韵
- 叙事结构
- 情绪质地
- 冲突风格
- 观看后味
- 适合和不适合的人

因此每部作品需要生成一个 `experience_profile`。这里的关键决策是：**完整体验描述是主索引，拆开的结构化字段只是辅助索引**。

如果只把作品拆成 `plot_vector`、`emotion_vector`、`relationship_vector` 这类碎片，系统会变成高级标签检索，容易丢掉一部作品作为整体的「味道」。所以每部作品首先要有一段完整、自然语言的体验画像，用来承载作品的整体语义。

示例：

```json
{
  "title": "葬送的芙莉莲",
  "experience_profile_text": "这部作品的核心体验不是魔法冒险本身，而是冒险结束多年之后，一个长寿者在新的旅途中重新理解过去的人和关系。它的叙事节奏安静、克制，战斗存在但不是推动爽感和升级的主轴；更重要的是时间流逝、记忆沉淀、人与人错过之后才迟来的理解。观看后味偏温柔和怅然，有余韵但不是强虐，适合想看世界观有厚度、情绪表达不急、关系慢慢展开的人。",
  "facets": {
    "themes": ["时间流逝", "旅途", "记忆", "人与人的错过"],
    "emotional_texture": "安静、克制、温柔、带一点怅然",
    "narrative_core": "冒险结束后重新理解过去的关系",
    "pacing": "慢节奏",
    "conflict_style": "有战斗，但不是热血升级主轴",
    "relationship_pattern": "长寿者与短寿者之间的陪伴和失去",
    "viewer_aftertaste": "有余韵，不强虐",
    "not_for": ["想看高燃战斗", "想看强主线悬疑的人"],
    "content_warnings": []
  },
  "confidence": 0.86
}
```

主检索文本：

```text
experience_profile_text
```

辅助 facet：

```text
plot_facet
emotion_facet
relationship_facet
pacing_facet
visual_style_facet
anti_fit_facet
```

也就是说，我们不是只存一组 embedding，而是存一组 multi-vector：

```text
overall_vector       = experience_profile_text 的整体 embedding
plot_vector          = 叙事和剧情核心
emotion_vector       = 情绪质地和观看后味
relationship_vector  = 人物关系模式
pacing_vector        = 节奏和冲突风格
visual_style_vector  = 美术、演出、时代感
anti_fit_vector      = 不适合点和避雷点
```

其中 `overall_vector` 权重最高。拆分向量只用于补召回、解释命中原因和处理用户反馈，不应该取代完整体验描述。

生成输入：

```text
Bangumi:
  name_cn, name, summary, tags, meta_tags, rating, collection, eps, platform

AniList:
  title, description, genres, tags, format, popularity, score

可选:
  用户自己的反馈、人工补充笔记、精选短评摘要
```

生成要求：

- 先输出一段完整的 `experience_profile_text`，再输出结构化 `facets`。
- `experience_profile_text` 需要像人在描述作品体验，而不是标签堆砌。
- 每个 facet 可以有局部置信度，整体保留 confidence。
- 不确定时不要强行判断。
- 尽量区分「表面题材」和「核心体验」。
- 明确写出「不是因为什么相似」，避免表面标签误导。

## 6. 推荐流程

### 6.1 用户意图解析

用户输入：

```text
想看像芙莉莲那种，有时间流逝后的余韵，但不要王道热血，不要后宫，可以热门也可以中腰部。
```

解析成：

```json
{
  "ideal_profile_text": "用户想要的不是单纯奇幻冒险，而是有时间跨度、关系余韵和克制情绪表达的作品。世界观可以厚，但叙事不应被打怪升级和王道热血占据；战斗可以存在，但不能是主要爽点。整体观看后味应该温柔、怅然、有余韵，但不要强虐、后宫或卖肉。",
  "positive_semantics": [
    "时间流逝",
    "关系余韵",
    "慢节奏",
    "世界观有厚度",
    "战斗不是主轴"
  ],
  "negative_semantics": [
    "王道热血",
    "打怪升级",
    "后宫",
    "卖肉"
  ],
  "hard_filters": {
    "type": "anime",
    "nsfw": false
  },
  "soft_preferences": {
    "popularity": "mixed",
    "novelty": "normal"
  }
}
```

### 6.2 粗召回

候选来源：

```text
1. Bangumi 搜索用户提到的作品，获取锚点作品
2. 根据锚点作品 tags / meta_tags / persons / related subjects 找候选
3. 根据 Bangumi 排名、评分人数、收藏数找高质量候选
4. 根据 AniList tags 做补充召回
5. 用 ideal_profile_text 搜 overall_vector
6. 用情绪、关系、节奏等 facet 查询对应向量
7. 用 anti_fit_vector 排除或降权明显不合适的作品
```

粗召回目标是找 100 到 300 个候选，不追求最终精确。

### 6.3 硬过滤

适合硬过滤的条件：

```text
NSFW
不是动画
用户明确不要的格式，例如剧场版、长篇、续作
评分人数过低
字段严重缺失
用户明确看过且不想重复推荐
```

默认推荐池建议：

```text
rating.total >= 300
collection_total >= 500
tags 数量 >= 3
有 name_cn 或稳定中文别名
有 summary
type = 动画
排除 NSFW
```

探索模式可降低阈值：

```text
rating.total >= 50
collection_total >= 100
```

### 6.4 语义检索

先让 LLM 把用户需求展开成一段 `ideal_profile_text`，再用它和作品的 `experience_profile_text` 做整体向量检索。这一步的主目标不是匹配标签，而是匹配完整观看体验。

示例用户需求：

```text
想看像芙莉莲那种，但不是魔法本身，是很多年后才理解关系的感觉。
```

LLM 展开后的理想画像：

```text
理想作品需要有时间跨度感、迟来的理解、关系余韵和克制情绪表达。它可以有奇幻或科幻设定，但设定不是目的；重点是人物在旅途、日常或回望中过去理解自己和他人。冲突不应主要来自打怪升级或世界危机，而应来自记忆、陪伴、错过和情绪沉淀。
```

检索策略：

```text
overall_vector:
  用完整 ideal_profile_text 检索完整 experience_profile_text。

facet_vectors:
  用 emotion / relationship / pacing 等子需求检索对应 facet。

anti_fit_vector:
  用用户明确不想要的内容检索避雷画像，命中高的候选降权。

hybrid search:
  同时保留 Bangumi 中文名、标签、制作人员、年份等关键词检索，避免纯向量漏掉精确匹配。
```

这一步解决传统标签无法处理的问题：

```text
不是大悲剧，但看完有时间过去了的怅然
不是成长变强，而是重新理解自己和他人
世界观很大，但叙事落在小人物日常
有孤独感，但不要压抑到窒息
```

### 6.5 LLM 精排

对前 30 到 50 个候选做 LLM rerank。

Rerank 不问「你推荐什么」，而是给定 `ideal_profile_text`、用户反馈、候选作品 `experience_profile_text` 和事实字段，让模型判断：

```text
1. 是否匹配用户真正想要的情绪和叙事
2. 是否避开用户明确不想要的内容
3. 匹配点是否来自核心体验，而不是表面标签
4. 风险点是什么
5. 为什么它比其他候选更适合
6. 为什么它不是一个机械标签相似结果
```

输出：

```json
{
  "subject_id": 123,
  "fit_score": 0.84,
  "why": "匹配的是温柔、克制、人与非人之间的短暂相遇和余韵，而不是奇幻战斗。",
  "risk": "单元剧结构较强，主线推进慢。",
  "not_because": "不是因为它也是奇幻，而是因为它有类似的情绪密度和关系主题。"
}
```

## 7. 排序公式

推荐分不是单纯按评分排序：

```text
final_score =
  semantic_fit
+ quality_score
+ confidence_score
+ popularity_fit
+ novelty_fit
- seen_penalty
- disliked_similarity_penalty
```

字段解释：

```text
semantic_fit:
  ideal_profile_text 和作品 experience_profile_text 的整体匹配度，facet 匹配只作为辅助

quality_score:
  贝叶斯修正后的评分，避免小样本高分乱飞

confidence_score:
  评分人数、收藏数、标签密度、简介完整度、跨源一致性

popularity_fit:
  用户是否接受热门/经典作品

novelty_fit:
  发现感，不是为了冷门而冷门

seen_penalty:
  已看过作品直接降权或排除

disliked_similarity_penalty:
  和用户不喜欢作品太相似时降权
```

贝叶斯评分示例：

```text
quality_score =
  (rating.score * rating.total + global_average * prior_weight)
  / (rating.total + prior_weight)
```

## 8. 反馈闭环

第一轮不要预判用户一定看过热门，也不要强行避开热门。采用混合推荐：

```text
40% 热门/经典高匹配
40% 中腰部高匹配
20% 探索项
```

用户反馈类型：

```text
看过，喜欢
看过，一般
看过，不喜欢
没看过，想看
没看过，但不感兴趣
太热门
太冷门
方向对了
方向不对
```

本地用户画像：

```json
{
  "seen": [],
  "liked": [],
  "disliked": [],
  "not_interested": [],
  "positive_semantics": [],
  "negative_semantics": [],
  "popularity_tolerance": 0.7,
  "novelty_preference": 0.5,
  "length_preference": "unknown"
}
```

更新逻辑：

```text
用户说「这些都看过」:
  seen_penalty 增强
  overexposure_penalty 增强
  候选池下潜

用户说「热门可以」:
  popularity_penalty 降低
  经典长篇候选恢复

用户说「太冷门」:
  min_rating_total 提高
  min_collection_total 提高
  探索项比例降低

用户说「方向对，但别那么致郁」:
  保留正向语义
  增加 darkness / tragedy 负向约束
```

## 9. 技术栈

建议 MVP 技术栈：

```text
TypeScript
Node.js
SQLite
sqlite-vec 或 LanceDB
Zod
Vitest
Bangumi API
AniList GraphQL
OpenAI embeddings / rerank 模型
```

初始目录结构：

```text
animate_recommand/
  SKILL.md
  package.json
  docs/
    technical-plan.md
  src/
    sources/
      bangumi.ts
      anilist.ts
    storage/
      db.ts
    semantic/
      profile-schema.ts
      build-profile.ts
      build-ideal-profile.ts
      embed.ts
    recommender/
      recall.ts
      filter.ts
      scoring.ts
      rerank.ts
      feedback.ts
    cli.ts
  data/
    anime.sqlite
  tests/
```

## 10. MVP 里程碑

### V0: CLI 跑通

目标：

```text
recommend "想看像芙莉莲那种，有余韵但不要王道热血"
```

能力：

- Bangumi 搜索和条目详情
- AniList 补充标签
- SQLite 缓存
- 用户意图解析
- 简单候选召回
- LLM rerank
- 输出 8 到 10 个推荐

### V1: 反馈闭环

目标：

```text
feedback --seen --liked "少女终末旅行"
feedback --seen --disliked "某作品"
recommend "继续推荐，但别太致郁"
```

能力：

- 保存用户反馈
- 更新用户画像
- 已看作品降权或排除
- 根据反馈调整热门/冷门、题材、情绪权重

### V2: Skill 化

目标：

- 编写 `SKILL.md`
- Codex/Claude 可以自然调用本地推荐器
- 输出稳定、可解释、有来源

### V3: 更强语义索引

目标：

- 批量生成高质量候选池 experience_profile
- 建立本地向量索引
- 支持 overall_vector + facet_vectors 的多向量语义检索和 rerank

### V4: 服务器版本评估

只有在本地版证明推荐质量之后再考虑。

服务器可能负责：

- 公共作品索引
- experience_profile 预计算
- multi-vector embedding 预计算
- 数据增量刷新
- 多用户冷启动加速

用户本地仍保存：

- 看过列表
- 喜好反馈
- Bangumi/AniList token
- 个性化画像

## 11. 风险和边界

### 数据风险

- Bangumi 长尾条目可能字段稀疏。
- AniList 中文支持弱。
- API 可能限流或字段变动。
- 社区标签可能噪声较大。

缓解：

- 本地缓存。
- 多源交叉验证。
- 对低评分人数、低收藏数、低标签密度条目降低置信度。
- 输出推荐时标注风险和不适合点。

### 推荐风险

- LLM 可能过度解读简介。
- 热门和冷门平衡不好。
- 用户首次反馈不足，冷启动不准。

缓解：

- 第一轮采用混合推荐。
- experience_profile 输出 confidence，并区分整体画像和 facet 的置信度。
- LLM rerank 必须基于候选数据，不允许凭空新增作品。
- 反馈闭环优先。

### 合规风险

- 不复制完整站点数据。
- 尊重 API 使用限制和缓存策略。
- 对来源做清晰标注。
- 后续商业化前重新评估 Bangumi、AniList、图片和简介的使用许可。

## 12. 当前决策

当前阶段先采用轻量方法论优先，工程化推荐器保留为实验：

```text
默认路径：
  LLM 直接做 taste analysis
  按体验维度分层推荐
  用户反馈后即时收窄

实验路径：
  本地 CLI
  Bangumi/AniList 缓存
  SQLite
  experience_profile
  未来可接 multi-vector embeddings
```

一句话定义：

> 先把推荐思维产品化，再视需要把推荐系统工程化。

## 13. MVP 实现状态

当前本地版本已经落成一个 TypeScript CLI，但它是实验工具，不是默认推荐路径：

```text
SKILL.md
package.json
src/
  cli.ts
  data/seeds.ts
  llm/openai.ts
  recommender/
  semantic/
  sources/
  storage/
data/
  anime.sqlite
```

已实现能力：

```text
recommend:
  根据自然语言口味生成推荐，支持 --no-network、--limit、--json。

search:
  调 Bangumi/AniList 搜索并写入本地缓存。

feedback:
  记录看过、喜欢、不喜欢、想看、太热门、太冷门等反馈。

profile:
  查看本地反馈摘要。
```

第一版实现选择：

```text
1. 内置一小批 curated seed anime，保证无网络也能验证推荐闭环。
2. 默认使用本地启发式 experience_profile 生成和词项 cosine 打分。
3. 如果存在 OPENAI_API_KEY，则可选启用 LLM 画像生成和 rerank。
4. 暂未启用真正向量库；multi-vector 结构已在数据模型和设计中预留。
5. SQLite 使用 Node 内置 node:sqlite，避免第一版引入 native 第三方依赖。
```

常用命令：

```bash
npm run recommend -- "想看像芙莉莲那种，有余韵但不要王道热血"
npm run recommend -- "想看安静的旅途感" -- --no-network --limit 5
npm run feedback -- "少女终末旅行" -- --seen --liked --comment "方向对"
npm run profile
```
