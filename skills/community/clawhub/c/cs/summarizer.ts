import { defineSkill } from '@openclaw/core';

export const summarizerSkill = defineSkill({
  id: 'summarizer',
  name: '智能摘要助手',
  description: '帮助用户快速总结长文本的核心要点',
  
  match: (context) => {
    const text = context.message?.content || '';
    const hasKeyword = /总结|摘要|summarize|brief/i.test(text);
    return hasKeyword || text.length > 100;
  },

  async run(context, { llm }) {
    const userText = context.message?.content || '';
    const prompt = `请总结以下文本的核心要点，用列表格式返回：\n"""\n${userText}\n"""`;
    
    const response = await llm.chat({
      messages: [
        { role: 'system', content: '你是一个专业的摘要助手，输出简洁清晰。' },
        { role: 'user', content: prompt }
      ],
      temperature: 0.3,
      maxTokens: 1000
    });
    return { content: response.content };
  },
});
