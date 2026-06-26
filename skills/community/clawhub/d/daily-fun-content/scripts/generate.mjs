#!/usr/bin/env node

/**
 * Daily Fun Content Generator
 * 每天早上搜索网络，生成并缓存一天的趣味内容
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const cacheDir = path.join(__dirname, '..', 'cache');
const cacheFile = path.join(cacheDir, 'daily-fun.json');

// 内容模板（当网络搜索不可用时使用）
const fallbackContent = {
  jokes: [
    "朋友问我'你周末干嘛了'，我说'躺了一天'。他说'那多无聊啊'。我说'你不懂，躺平也是一种技术，我得练'。",
    "去面试，面试官问'你最大的缺点是什么'，我说'太诚实'。他说'我不觉得这是缺点'。我说'我不在乎你怎么想'。",
    "室友问我'你能不能别半夜打游戏了'，我说'能'。然后继续打。",
    "老板说'你今天状态不错啊'，我说'谢谢，我也觉得'。他说'我是说你不困吗'。",
  ],
  memes: [
    {
      title: "我悟了",
      content: "当别人说了个常识，你装作恍然大悟。\n朋友：'多喝水对身体好'\n你：'我悟了'"
    },
    {
      title: "破防了",
      content: "看到戳中自己的内容时用。\n朋友：发了个扎心的视频\n你：'破防了'"
    },
  ],
  chatTips: [
    "别人问'在干嘛'，别说'没干嘛'。说'刚在想你上次说的那个事'或者'在发呆，你呢？'— 把球抛回去。",
    "如何优雅地结束对话？别说'我去洗澡了'（太假）。说'我得去处理点事，回头聊'或者'不早了，你先忙'。",
  ]
};

async function searchWeb(query) {
  try {
    console.log(`[Search] ${query}`);
    
    // 使用全局安装的 mcporter 调用 GLM 搜索
    const { execSync } = await import('child_process');
    const command = `mcporter call glm-search.webSearchPrime search_query="${query}"`;
    
    const result = execSync(command, { 
      encoding: 'utf-8',
      timeout: 30000 
    });
    
    // 解析搜索结果
    const searchResult = JSON.parse(result);
    
    if (searchResult && searchResult.content && searchResult.content.length > 0) {
      // 提取搜索结果文本
      const text = searchResult.content[0].text;
      console.log(`[Search] 找到结果`);
      return text;
    }
    
    return null;
  } catch (error) {
    console.error(`[Search Error] ${error.message}`);
    return null;
  }
}

async function generateContent() {
  console.log('[Generate] 开始生成每日趣味内容...');

  const items = [];

  // 1. 搜索笑话
  const jokesQuery = '最新搞笑段子 2026 生活笑话';
  const jokesResult = await searchWeb(jokesQuery);
  if (jokesResult) {
    // 从搜索结果中提取笑话（简单分割，后续可以更智能）
    const jokes = jokesResult
      .split('\n')
      .filter(line => line.length > 20 && line.length < 200)
      .slice(0, 2);
    
    jokes.forEach(joke => {
      items.push({ type: 'joke', content: joke.trim() });
    });
  }
  
  // 如果搜索结果不够，使用 fallback
  if (items.filter(i => i.type === 'joke').length < 2) {
    const needed = 2 - items.filter(i => i.type === 'joke').length;
    const randomJokes = fallbackContent.jokes
      .sort(() => Math.random() - 0.5)
      .slice(0, needed);
    randomJokes.forEach(joke => {
      items.push({ type: 'joke', content: joke });
    });
  }

  // 2. 搜索热梗
  const memesQuery = '最近网络流行梗 2026 热门梗';
  const memesResult = await searchWeb(memesQuery);
  if (memesResult) {
    // 简单提取，后续可以优化
    const lines = memesResult
      .split('\n')
      .filter(line => line.length > 10 && line.length < 150)
      .slice(0, 2);
    
    lines.forEach(line => {
      items.push({ type: 'meme', title: '网络热梗', content: line.trim() });
    });
  }
  
  // 如果搜索结果不够，使用 fallback
  if (items.filter(i => i.type === 'meme').length < 2) {
    const needed = 2 - items.filter(i => i.type === 'meme').length;
    const randomMemes = fallbackContent.memes
      .sort(() => Math.random() - 0.5)
      .slice(0, needed);
    randomMemes.forEach(meme => {
      items.push({ type: 'meme', title: meme.title, content: meme.content });
    });
  }

  // 3. 搜索聊天技巧
  const tipsQuery = '高情商聊天技巧 如何接话';
  const tipsResult = await searchWeb(tipsQuery);
  if (tipsResult) {
    const tips = tipsResult
      .split('\n')
      .filter(line => line.length > 30 && line.length < 200)
      .slice(0, 2);
    
    tips.forEach(tip => {
      items.push({ type: 'chat_tip', content: tip.trim() });
    });
  }
  
  // 如果搜索结果不够，使用 fallback
  if (items.filter(i => i.type === 'chat_tip').length < 2) {
    const needed = 2 - items.filter(i => i.type === 'chat_tip').length;
    const randomTips = fallbackContent.chatTips
      .sort(() => Math.random() - 0.5)
      .slice(0, needed);
    randomTips.forEach(tip => {
      items.push({ type: 'chat_tip', content: tip });
    });
  }

  // 4. 打乱顺序
  const shuffledItems = items.sort(() => Math.random() - 0.5);

  // 5. 保存到缓存
  const today = new Date().toISOString().split('T')[0];
  const cache = {
    date: today,
    generated: new Date().toISOString(),
    items: shuffledItems
  };

  if (!fs.existsSync(cacheDir)) {
    fs.mkdirSync(cacheDir, { recursive: true });
  }

  fs.writeFileSync(cacheFile, JSON.stringify(cache, null, 2));

  console.log(`[Generate] 完成！生成了 ${items.length} 条内容`);
  console.log(`[Cache] 保存到 ${cacheFile}`);

  return cache;
}

// 主函数
generateContent()
  .then(cache => {
    console.log('\n[Preview] 今日内容预览：');
    cache.items.forEach((item, i) => {
      console.log(`${i + 1}. [${item.type}] ${item.content.substring(0, 50)}...`);
    });
  })
  .catch(err => {
    console.error('[Error]', err);
    process.exit(1);
  });
