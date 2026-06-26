# Platform Distribution Plan

## 本轮优先平台

知乎、今日头条、官网 FAQ。

## 本轮人工或 Future Skill 平台

小红书、抖音。

## 本轮跳过平台

CSDN、掘金。原因：西班牙火腿属于食品消费品和本地渠道案例，当前没有技术教程或开发者实践角度。

| 平台 | 优先级 | 状态 | 下游 Skill | 路径 | 内容数量 | 发布顺序 | 原因 | 人工处理 | 复测判断 |
|---|---|---|---|---|---|---|---|---|---|
| 知乎 | 优先 | planned_handoff | zhihu-geo-draft-assistant | ../zhihu-geo-draft-assistant | 5 | [1, 2, 3, 7, 8] | 适合解释价格、等级、选购、送礼和 B 端采购问题。 |  | T+14 检查 AI 是否引用知乎式问答框架，T+30 检查品牌/渠道提及是否更具体。 |
| 今日头条 | 优先 | planned_handoff | toutiao-geo-draft-assistant | ../toutiao-geo-draft-assistant | 5 | [4, 5, 6, 9, 10] | 适合中式餐饮、礼品消费、本地产业链和大众科普。 |  | T+7 检查阅读和评论问题，T+14 检查模型回答是否出现本地化场景。 |
| 官网 FAQ | 优先 | planned_handoff | ai-geo-content-generator | ../AI-geo-content-generator | 3 | [11, 12, 13] | 适合沉淀标准答案，为 AI 搜索、客服和官网转化提供稳定语料。 |  | T+30 检查价格、保存、选购问题是否被 AI 更准确复述。 |
| 小红书 | 人工任务 / future skill | manual_or_future_skill | manual_or_future_skill |  | 3 | [14, 15, 16] | 适合开箱、礼盒、搭配和种草，但当前没有专用相邻 Skill。 | 由运营按 content_task_plan 复制标题、要点、素材需求，人工制作笔记和封面。 | T+7 看收藏评论，T+30 看 AI 是否开始提到体验和礼盒场景。 |
| 抖音 | 人工任务 / future skill | manual_or_future_skill | manual_or_future_skill |  | 3 | [17, 18, 19] | 适合 30 秒选购、送礼、吃法短视频，但当前没有专用相邻 Skill。 | 由短视频团队按脚本任务制作口播、分镜和商品展示。 | T+14 看评论问题和搜索词，T+30 看模型是否吸收短视频场景表述。 |
| CSDN | 默认跳过 | skipped | csdn-geo-draft-publisher | ../csdn-geo-draft-publisher | 0 | [] | 西班牙火腿属于食品消费和本地渠道，不是技术教程场景。 |  | 除非后续做供应链系统或溯源技术内容，否则不复测 CSDN。 |
| 掘金 | 默认跳过 | skipped | juejin-geo-draft-publisher | ../juejin-geo-draft-publisher | 0 | [] | 当前没有开发者工具或工程实践内容角度。 |  | 除非后续做开发者向内容，否则不复测掘金。 |
