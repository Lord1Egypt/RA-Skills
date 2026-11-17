# 情侣默契问答 (Couple Interaction)

给情侣双方使用的互动工具。主人公先把 AI 当成普通的**情侣问答游戏**,邀请对象逐题
回答;前半段不提礼物、购物或分析目的。问答结束后,主人公再单独向 AI 询问「我该买
什么」,AI 才根据对象刚才的真实回答推测兴趣、生活方式、情绪需求和雷区。

```
主人公发起问答 → 对象参与回答 → 默契总结 → 主人公私下询问 → 偏好推断 → 礼物建议
```

> 适合:情侣双方、想给对象准备惊喜的人。
> 推断只是辅助判断,不能替代对方的明确表达。

## 它能干嘛

- **互动阶段**:AI 像游戏主持人一样一次问一道,对象回答后继续,不暴露礼物目的
- **记录阶段**:保留回答原话和可能反映的偏好,不把猜测冒充事实
- **礼物揭晓**:只有用户主动问「送什么好」时,才根据回答证据给出 3-5 个方案
- **直接使用**:双方在同一个 AI 对话里完成互动,结束后得到个性化礼物建议

## 快速体验

1. 把整个 skill 放进支持 `SKILL.md` 的 AI 助手目录,或把提示词贴给 AI。**不要把
   导入后的第一段设置说明直接展示给参与者。**
2. 发起人先私下对 AI 说:「我是发起人,陪我们玩 8 道情侣问答,一次问一道。」设置完成
   后,再把 AI 对话交给参与者回答。
3. 参与者逐题回答时,AI 只进行问答,不提及隐藏目的或后续用途;如果参与者不舒服或
   要求停止,应立即停止。
4. 参与者离开对话后,发起人再私下发送:「刚才是我让参与者做的题,根据 TA 的回答告诉我该买
   什么,预算 300 元。」
5. AI 才会列出回答证据、偏好推断、置信度和礼物方案。

独立使用提示词时,把 `references/couple-content-prompt.md` 贴给任意大模型即可。
生成惊喜建议 JSON 后,可以渲染为 markdown:

```bash
python3 scripts/render_content.py examples/gift_reveal_example.json gift_reveal.md
```

脚本纯标准库,不需要安装第三方依赖。

## 让任何 AI 助手使用这个 skill

纯通用 skill,不绑定任何 agent 系统。四种用法任选:

1. **ClawHub 一键安装**(OpenClaw 用户推荐):

   ```bash
   npx clawhub@latest install @padepa/couple-content
   ```

2. **放进你 AI 助手的 skills 目录**:支持 SKILL.md 的助手直接把这个仓库文件夹
   放进去,然后说「陪我们玩 10 道情侣默契题」即可
3. **直接对话**:把 `SKILL.md` 内容贴给 AI,它就知道怎么主持
4. **纯手动**:把参考提示词贴给任意大模型,不需要安装脚本

## 会话数据

互动开始时可使用 `templates/session_template.json`。场合可以是日常、纪念日、节日或
任何需要准备惊喜的时刻:

```json
{
  "stage": "playing",
  "topic": "情侣默契挑战",
  "question_index": 0,
  "question_count": 8,
  "relationship_stage": "交往中",
  "style": "轻松走心",
  "questions": [],
  "answers": [],
  "inferred_preferences": []
}
```

每次收到回答后,把题目、回答原话和观察记录进 `answers`。互动结束后将 `stage`
改为 `review`;只有发起人发送专属购买指令时才改为 `gift_reveal`。不要把隐藏字段
或内部观察展示给对象,也不要通过题目询问密码、收入、联系方式等敏感信息。

## 惊喜建议格式

```json
{
  "stage": "gift_reveal",
  "preference_summary": [
    {
      "dimension": "兴趣",
      "what_they_said": "TA说理想周末是在家烤曲奇",
      "inference": "TA可能偏爱安静、有参与感的居家活动",
      "confidence": "high"
    }
  ],
  "gift_options": [
    {
      "title": "双人烘焙体验",
      "price": "180-350元",
      "evidence": "TA说理想周末是在家烤曲奇",
      "why": "符合烘焙兴趣,也能创造共同体验",
      "how": "选一个双方都有空的晚上一起做,成品装盒留念"
    }
  ],
  "uncertainties": ["还不知道具体预算"]
}
```

关键规则:

- 每个推荐都必须引用互动回答作为依据
- 明确区分 TA 的原话、AI 的推测和仍不确定的信息
- 不从单个回答推断人格、消费能力或敏感属性
- 礼物价格只写参考区间,购买前核实


## 文件结构

```
couple-content/
├── SKILL.md                          # agent skill 定义(给 AI 助手看)
├── README.md                         # 人看的快速开始
├── LICENSE                           # MIT
├── scripts/
│   └── render_content.py             # JSON → 可发布 markdown 文案(纯 stdlib)
├── references/
│   └── couple-content-prompt.md      # 给任何 LLM 的生成提示词
├── templates/
│   ├── input_template.json           # 批量输入模板
│   └── session_template.json         # 三阶段互动会话模板
└── examples/
    ├── questions_example.json        # 兼容的批量出题示例
    ├── gift_example.json             # 兼容的直接建议示例
    └── gift_reveal_example.json      # 基于回答证据的礼物揭晓示例
```

## FAQ

**Q: 为什么不一开始就问购买条件?**
A: 因为这个 skill 的特点就是先自然互动。对象的真实回答通常比一句「TA喜欢什么」
   更具体,后续推荐也能写清楚依据。

**Q: 会不会过度分析对象?**
A: 不应该。输出会区分「TA明确说过」「合理推测」「还不知道」,推断只用于缩小
   选择范围,不能当成对方的确定想法。

**Q: 谁来使用这个 skill?**
A: 发起人与参与者直接使用。把它放进支持 `SKILL.md` 的 AI 助手,让参与者按题目回答;
   互动结束后,由发起人单独询问「根据刚才的回答,送什么礼物好」。

**Q: 需要联网吗?**
A: 生成那一步需要(调用任意大模型);渲染脚本纯本地,不需要网络。

**Q: 会不会一开始就被参与者发现是在准备惊喜?**
A: 前半段只作为情侣互动游戏进行,不主动说明后续用途;如果参与者直接询问或要求停止,
   必须如实回应并停止隐藏式流程。进入建议阶段后,
   会明确展示回答依据和推断的不确定性。

## License

MIT © padepa
