请先为下面这篇文章设计一个“摘要结构规划”。

输出规则：
- 只输出合法 JSON，不要输出解释文字，不要加 Markdown 代码块。
- `angle`：一句话说明这篇文章最适合从什么角度总结。
- `one_sentence_focus`：一句话说明最终的一句话总结应该聚焦什么。
- `sections`：2 到 4 个章节，每个章节都要说明该章节要回答的问题。
- `tags`：3 到 8 个短标签，用于最终输出尾部展示。
- `closing_focus`：一句话说明最终结尾应该落在哪个结论或提醒上。

JSON 结构：
{
  "angle": "这篇文章应该从什么角度总结",
  "one_sentence_focus": "最终一句话总结应该聚焦什么",
  "sections": [
    {
      "heading": "章节标题",
      "purpose": "这一节应该回答什么问题"
    }
  ],
  "tags": ["标签1", "标签2"],
  "closing_focus": "最终收束时应该强调什么"
}

文章标题：
{{title}}

文章来源：
{{source}}

文章正文：
{{article_text}}
