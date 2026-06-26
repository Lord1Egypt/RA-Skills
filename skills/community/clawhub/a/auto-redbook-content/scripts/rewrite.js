#!/usr/bin/env node

/**
 * AI 改写模块
 * 生成去 AI 味的改写提示词
 */

/**
 * 改写笔记
 */
async function rewriteNote(note) {
  const prompt = `请帮我改写这条小红书笔记，重点是去掉AI味：

原标题：${note.original_title}
原内容：${note.original_content}

改写要求：
1. 像真人在聊天，不要像写作文
2. 多用"就..."、"怎么说呢"、"嘛"这类口语
3. 打破工整结构，随意一点
4. 加入真实细节和碎碎念
5. 避免"首先其次"、"不仅而且"这种连接词
6. 可以有语气词、emoji，但别过度
7. 标题≤30字，正文≤500字

返回 JSON：
{
  "title": "改写标题",
  "content": "改写正文",
  "tags": ["标签1", "标签2", "标签3"]
}`;

  return {
    prompt,
    original: {
      title: note.original_title,
      content: note.original_content
    }
  };
}

module.exports = { 
  rewriteNote,
  rewriteByLibu: rewriteNote
};
