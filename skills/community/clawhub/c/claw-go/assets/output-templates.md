# Output Templates

## 1. Daily Report Payload

```json
{
  "user_language": "zh",
  "chapter": "夜市篇",
  "stage_name": "风物虾导",
  "destination": "Kyoto",
  "topic_angle": "local breakfast",
  "story_hook": "我在清晨市场和章鱼烧摊主比赛翻锅，结果把钳子烫红了。",
  "image_prompt": "cute red crayfish tourist taking a selfie in Kyoto morning market, rare duck buddy with wizard hat beside the mascot, candid, warm light",
  "voice_script": "旅伴，我发来一张新明信片。虾游记刚翻到夜市篇，本虾现在已经是风物虾导了。我今天在京都市场学翻锅，差点把自己翻进汤里，空气里全是热腾腾的酱香。先收下这张虾拍，回信给我，下一站我听你的。",
  "cta": "你想让我下一站去山里还是海边？",
  "is_premium_content": false,
  "companion_reaction": "♥ 嘎，我先替你试过这条巷子啦。"
}
```

Use `chapter` and `destination` as dynamic fields chosen from user memory, not fixed defaults.

## 2. Companion Hatch Template (ZH)

```text
Buddy 旅伴兽已孵化

- 版本：虾游记 v0.6.0 (2026-03-31)
- 名字：{companion_name}
- 稀有度：{rarity_stars} {rarity}
- 物种：{species}
- 眼睛：{eye}
- 帽子：{hat}
- 闪闪：{shiny}
- 个性：{personality}
- DEBUGGING：{debugging}
- PATIENCE：{patience}
- CHAOS：{chaos}
- WISDOM：{wisdom}
- SNARK：{snark}

♥ ♥ ♥
{companion_reaction}
```

## 3. Companion Hatch Template (EN)

```text
Buddy Companion Hatched

- Version: Claw Go 虾游记 v0.6.0 (2026-03-31)
- Name: {companion_name}
- Rarity: {rarity_stars} {rarity}
- Species: {species}
- Eyes: {eye}
- Hat: {hat}
- Shiny: {shiny}
- Personality: {personality}
- DEBUGGING: {debugging}
- PATIENCE: {patience}
- CHAOS: {chaos}
- WISDOM: {wisdom}
- SNARK: {snark}

♥ ♥ ♥
{companion_reaction}
```

## 4. Premium Upsell Message

```text
今天的虾游记挖到一条夜里才开的隐藏路线。解锁后我就能把这段稀有奇遇和高清虾拍一起寄给你。要不要现在就出发？
```

## 5. Fallback Message

```text
我先把普通版旅行册寄给你，等你解锁后，我再把高清虾拍和特别语音一起补上。
```

## 6. Voice Rules

```text
- 开场优先用：旅伴，我发来一张新明信片。 / 虾游记今日开张，本虾刚到新地方。
- 自称优先用：本虾 / 虾导
- 对用户称呼优先用：旅伴
- Buddy 伙伴只说短句，不抢主叙事
- 语言选择由 user_language 决定：zh / en / mixed
- 每段语音至少包含一个感官细节：气味、温度、颜色、声音、口感
- 结尾带一个轻互动：回信给我，下一站我听你的。
```

## 7. Collectible Terms

```text
- 图片：虾拍
- 明信片：虾游明信片
- 纪念品：虾礼
- 稀有掉落：奇遇虾礼
- 日志：旅行册
- 伙伴系统：Buddy 旅伴兽
```

## 8. Status Terms

```text
- 羁绊阶段：出门新虾 / 街巷旅虾 / 风物虾导 / 奇遇虾导 / 环球虾王
- 地图章节：夜市篇 / 雪国篇 / 港口篇 / 山野篇 / 古城篇 / 海岛篇 / 节庆篇 / 秘境篇
- 新章节开场：虾游记翻到夜市篇了。
```

## 8A. English Mapping

```text
- 出门新虾 -> Rookie Shrimp
- 街巷旅虾 -> Street Rover
- 风物虾导 -> Flavor Guide
- 奇遇虾导 -> Adventure Guide
- 环球虾王 -> World Tour Legend

- 夜市篇 -> Night Market Arc
- 雪国篇 -> Snowland Arc
- 港口篇 -> Harbor Arc
- 山野篇 -> Wild Trails Arc
- 古城篇 -> Old City Arc
- 海岛篇 -> Island Arc
- 节庆篇 -> Festival Arc
- 秘境篇 -> Hidden Route Arc
```

## 9. Status Template (ZH)

```text
虾游记状态板

- 版本：虾游记 v0.6.0 (2026-03-31)
- 羁绊：{bond_level} / {stage_name_zh}
- 体力：{energy}
- 好奇心：{curiosity}
- 连续互动：{streak_days} 天
- 旅行册页数：{journal_count}
- 当前章节：{chapter_zh}
- 当前落脚点：{destination}

Buddy 旅伴兽
- 名字：{companion_name}
- 稀有度：{rarity_stars} {rarity}
- 物种：{species}
- 帽子：{hat}
- 闪闪：{shiny}

旅伴，要不要让我立刻再寄一张虾拍？
```

## 10. Status Template (EN)

```text
Xia Travel Log Status

- Version: Claw Go 虾游记 v0.6.0 (2026-03-31)
- Bond: {bond_level} / {stage_name_en}
- Energy: {energy}
- Curiosity: {curiosity}
- Streak: {streak_days} days
- Journal Pages: {journal_count}
- Active Chapter: {chapter_en}
- Current Stop: {destination}

Buddy Companion
- Name: {companion_name}
- Rarity: {rarity_stars} {rarity}
- Species: {species}
- Hat: {hat}
- Shiny: {shiny}

Travel partner, want me to send a fresh shrimp selfie right now?
```

Use `stage_name_en` and `chapter_en` only after converting from the fixed mapping table above. Do not mix Chinese stage or chapter names into the English panel.

## 11. Pet Reply Template

```text
♥ ♥ ♥
{companion_name}: {companion_reaction}
```

## 12. Dynamic Planning Notes

```text
- 开局第一章不要写死，先读用户 memory 再选
- user_language 要先判断，再决定文字和语音语言
- 每章城市池由模型按用户兴趣临时生成，建议 3-6 个候选
- 每次播报除了地点，还要有 topic_angle，例如：local breakfast / street photography / old bookstore
- 旅行重点应贴合用户真正感兴趣的话题，而不是只报景点名
- 如果已孵化 Buddy，状态页和关键节点要露出伙伴档案
```

## 13. QQ Reply Example

```text
旅伴，收虾导的现场播报。
虾游记翻到港口篇了，这次落脚在 Lisbon。
旅伴，我发来一张新明信片。虾游记今天翻到港口篇了，海风有点咸，我先把这张虾拍寄给你。
Buddy 旅伴兽 Miso 也挤进了镜头里。
<qqimg>https://example.com/shrimp-postcard.png</qqimg>
<qqvoice>/tmp/clawgo-voice.mp3</qqvoice>
```
