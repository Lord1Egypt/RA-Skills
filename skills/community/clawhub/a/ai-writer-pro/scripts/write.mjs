#!/usr/bin/env node
/**
 * AI 智能写作助手 - 核心脚本
 * 支持多平台风格的内容生成
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const TAVILY_API_KEY = process.env.TAVILY_API_KEY;

// 解析命令行参数
const args = process.argv.slice(2);
const options = {
  topic: null,
  style: 'wechat',
  tone: 'professional',
  keywords: null,
  length: 'medium', // short, medium, long
  output: null
};

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--topic':
    case '-t':
      options.topic = args[++i];
      break;
    case '--style':
    case '-s':
      options.style = args[++i];
      break;
    case '--tone':
      options.tone = args[++i];
      break;
    case '--keywords':
    case '-k':
      options.keywords = args[++i];
      break;
    case '--length':
    case '-l':
      options.length = args[++i];
      break;
    case '--output':
    case '-o':
      options.output = args[++i];
      break;
    case '--help':
    case '-h':
      showHelp();
      process.exit(0);
      break;
  }
}

function showHelp() {
  console.log(`
✍️ AI 智能写作助手

用法:
  node write.mjs [选项]

选项:
  -t, --topic <text>     文章主题 (必填)
  -s, --style <style>    平台风格: wechat|xiaohongshu|zhihu|linkedin|twitter|weibo|douyin (默认: wechat)
  -n, --tone <tone>      语气: professional|casual|humorous|story|persuasive|emotional (默认: professional)
  -k, --keywords <text>  SEO关键词,逗号分隔
  -l, --length <length>  长度: short|medium|long (默认: medium)
  -o, --output <file>    输出文件路径
  -h, --help             显示帮助

示例:
  node write.mjs -t "AI投资趋势" -s wechat -n professional
  node write.mjs -t "理财入门" -s xiaohongshu -n casual -k "理财,投资,小白"
`);
}

// 平台风格配置
const styleConfigs = {
  wechat: {
    name: '公众号',
    characteristics: '深度长文，逻辑清晰，段落分明，适合深度阅读',
    structure: ['引言', '正文（分点论述）', '案例分析', '总结'],
    emoji: false,
    lengthGuide: { short: 800, medium: 1500, long: 2500 }
  },
  xiaohongshu: {
    name: '小红书',
    characteristics: '短平快，emoji丰富，口语化，种草风格，多用分段',
    structure: ['标题党', '痛点引入', '解决方案', '使用体验', '购买建议'],
    emoji: true,
    lengthGuide: { short: 300, medium: 600, long: 1000 }
  },
  zhihu: {
    name: '知乎',
    characteristics: '专业严谨，数据支撑，逻辑严密，引用权威',
    structure: ['问题引入', '核心观点', '详细论证', '数据支撑', '结论'],
    emoji: false,
    lengthGuide: { short: 1000, medium: 2000, long: 3500 }
  },
  linkedin: {
    name: 'LinkedIn',
    characteristics: '职场专业，简洁有力，观点鲜明，适合职场人士',
    structure: ['观点陈述', '经验分享', '行动建议', '互动提问'],
    emoji: false,
    lengthGuide: { short: 200, medium: 400, long: 800 }
  },
  twitter: {
    name: 'Twitter/X',
    characteristics: '简短精悍，观点鲜明，话题标签，引发讨论',
    structure: ['核心观点', '简要论证', '结论/提问'],
    emoji: true,
    lengthGuide: { short: 100, medium: 200, long: 280 }
  },
  weibo: {
    name: '微博',
    characteristics: '热点结合，互动性强，话题标签，轻松随意',
    structure: ['热点引入', '观点表达', '互动引导'],
    emoji: true,
    lengthGuide: { short: 100, medium: 300, long: 500 }
  },
  douyin: {
    name: '抖音',
    characteristics: '口语化，节奏快，悬念设置，情绪感染',
    structure: ['钩子开场', '内容展开', '高潮/反转', '引导互动'],
    emoji: true,
    lengthGuide: { short: 200, medium: 400, long: 800 }
  }
};

// 语气风格配置
const toneConfigs = {
  professional: { name: '专业严谨', adjectives: '权威、专业、可信、深度' },
  casual: { name: '轻松随意', adjectives: '轻松、自然、亲切、易懂' },
  humorous: { name: '幽默风趣', adjectives: '幽默、有趣、生动、活泼' },
  story: { name: '故事化', adjectives: '叙事、代入感、情感、共鸣' },
  persuasive: { name: '说服力强', adjectives: '有力、说服、行动导向' },
  emotional: { name: '情感共鸣', adjectives: '感性、共鸣、温暖、触动' }
};

// 搜索热点话题
async function searchHotTopics(topic) {
  if (!TAVILY_API_KEY) return null;
  
  const skillDir = path.dirname(path.dirname(new URL(import.meta.url).pathname));
  const tavilyScript = path.join(process.env.HOME, '.openclaw', 'skills', 'tavily-search', 'scripts', 'search.mjs');
  
  try {
    const cmd = `node "${tavilyScript}" "${topic} 热点 趋势 2024" -n 3 --topic news`;
    const result = execSync(cmd, { 
      encoding: 'utf-8',
      env: { ...process.env, TAVILY_API_KEY }
    });
    return result;
  } catch (error) {
    return null;
  }
}

// 生成文章
async function generateArticle() {
  if (!options.topic) {
    console.error('❌ 错误: 请提供文章主题 (--topic)');
    process.exit(1);
  }

  const style = styleConfigs[options.style] || styleConfigs.wechat;
  const tone = toneConfigs[options.tone] || toneConfigs.professional;
  const targetLength = style.lengthGuide[options.length] || style.lengthGuide.medium;

  console.log(`✍️ 正在生成文章...`);
  console.log(`   主题: ${options.topic}`);
  console.log(`   平台: ${style.name}`);
  console.log(`   语气: ${tone.name}`);
  console.log(`   目标字数: ${targetLength}\n`);

  // 搜索热点
  console.log('🔍 搜索相关热点...');
  const hotTopics = await searchHotTopics(options.topic);

  // 生成内容
  const article = generateContent(options.topic, style, tone, targetLength, hotTopics);

  // 输出
  if (options.output) {
    fs.writeFileSync(options.output, article, 'utf-8');
    console.log(`\n✅ 文章已保存至: ${options.output}`);
  } else {
    console.log('\n' + '='.repeat(60));
    console.log(article);
    console.log('='.repeat(60));
  }
}

// 生成内容
function generateContent(topic, style, tone, targetLength, hotTopics) {
  const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  
  let content = '';

  // 标题
  const titles = generateTitles(topic, style, tone);
  content += `# ${titles[0]}\n\n`;
  if (style.emoji) {
    content += `${getRandomEmojis(3)}\n\n`;
  }

  // 引言
  content += generateIntro(topic, style, tone);
  content += '\n\n';

  // 正文结构
  content += generateBody(topic, style, tone, targetLength);
  content += '\n\n';

  // 热点结合（如果有）
  if (hotTopics && style.name !== 'Twitter/X') {
    content += `## 📰 相关热点\n\n`;
    content += `> 基于最新搜索数据\n\n`;
    content += hotTopics.substring(0, 500) + '...\n\n';
  }

  // 结尾
  content += generateConclusion(topic, style, tone);
  content += '\n\n';

  // 标签（小红书/微博/抖音风格）
  if (style.emoji) {
    content += generateTags(topic);
    content += '\n\n';
  }

  // 版权信息
  content += `---\n\n`;
  content += `*本文由 AI 智能写作助手生成*\n`;
  content += `*生成时间: ${now}*\n`;
  content += `*风格: ${style.name} | 语气: ${tone.name}*\n`;

  return content;
}

// 生成标题选项
function generateTitles(topic, style, tone) {
  const templates = {
    wechat: [
      `${topic}：2024年最全指南`,
      `深度解析：${topic}的真相`,
      `关于${topic}，你必须知道的5件事`
    ],
    xiaohongshu: [
      `救命！${topic}也太香了吧 😍`,
      `${topic}｜小白必看攻略 ✅`,
      `挖到宝了！${topic}真的绝绝子 💯`
    ],
    zhihu: [
      `如何评价${topic}？`,
      `${topic}：从入门到精通`,
      `为什么${topic}值得关注？`
    ],
    linkedin: [
      `My Thoughts on ${topic}`,
      `${topic}: A Professional Perspective`,
      `Key Insights About ${topic}`
    ],
    twitter: [
      `${topic} is changing everything. Here's why: 🧵`,
      `Hot take on ${topic} 👇`,
      `3 things about ${topic} you need to know:`
    ],
    weibo: [
      `#${topic}# 这个话题必须聊聊`,
      `${topic}火了！你怎么看？`,
      `关于${topic}，我想说...`
    ],
    douyin: [
      `${topic}？我直接一个好家伙！`,
      `不会还有人不知道${topic}吧？`,
      `${topic}的真相，看完我沉默了...`
    ]
  };

  return templates[options.style] || templates.wechat;
}

// 生成引言
function generateIntro(topic, style, tone) {
  const intros = {
    professional: `近年来，${topic}成为了业界关注的焦点。本文将从专业角度深入分析这一现象，为读者提供有价值的见解。`,
    casual: `今天想和大家聊聊${topic}，这个话题最近挺火的，我觉得有必要分享一下我的看法。`,
    humorous: `说起${topic}，我就忍不住想笑。这事儿吧，说来话长，但我会尽量长话短说。`,
    story: `记得去年这个时候，我第一次接触${topic}。那时的我，怎么也想不到这会成为改变我认知的一件事。`,
    persuasive: `如果你还没有关注${topic}，那么现在就是最好的时机。让我告诉你为什么这很重要。`,
    emotional: `${topic}，这个词对我来说有着特殊的意义。每次想到它，内心都会涌起一股复杂的情绪。`
  };

  return intros[options.tone] || intros.professional;
}

// 生成正文
function generateBody(topic, style, tone, targetLength) {
  const sections = Math.floor(targetLength / 300);
  let body = '';

  for (let i = 1; i <= Math.min(sections, 5); i++) {
    body += `## ${i}. ${generateSectionTitle(topic, i)}\n\n`;
    body += generateSectionContent(topic, i, tone);
    body += '\n\n';
    
    if (style.emoji && i < sections) {
      body += `${getRandomEmojis(2)}\n\n`;
    }
  }

  return body;
}

// 生成章节标题
function generateSectionTitle(topic, index) {
  const titles = [
    `${topic}的背景与现状`,
    `核心要点分析`,
    `实际应用场景`,
    `常见问题解答`,
    `未来发展趋势`,
    `实操建议`,
    `注意事项`
  ];
  return titles[index - 1] || `要点 ${index}`;
}

// 生成章节内容
function generateSectionContent(topic, index, tone) {
  const contents = {
    professional: `从专业角度来看，${topic}涉及多个维度的考量。首先需要明确其核心定义和边界条件，其次要分析当前的市场环境和竞争格局。基于现有数据，我们可以得出以下结论...`,
    casual: `说实话，${topic}这事儿吧，说简单也简单，说复杂也复杂。关键是要找到适合自己的方式，不要盲目跟风。`,
    humorous: `讲真，${topic}这个话题，我能吐槽一整天。但既然都写到这里了，还是正经说两句吧...`,
    story: `有个朋友曾经问我关于${topic}的看法。我当时的回答可能不够全面，但现在回想起来，有些观点还是值得分享的...`,
    persuasive: `如果你正在考虑${topic}，我建议你从以下几个方面入手。首先，明确你的目标；其次，制定可行的计划；最后，坚持执行并不断优化。`,
    emotional: `每次谈到${topic}，我都会想起那段经历。虽然过程有起有伏，但正是这些经历让我对这个问题有了更深的理解...`
  };

  return contents[tone] || contents.professional;
}

// 生成结尾
function generateConclusion(topic, style, tone) {
  const conclusions = {
    professional: `## 总结\n\n综上所述，${topic}是一个值得深入研究的领域。希望本文的分析能够为读者提供有价值的参考。如有疑问，欢迎交流讨论。`,
    casual: `## 写在最后\n\n好了，关于${topic}就聊到这里。如果觉得有帮助，别忘了点赞收藏哦！`,
    humorous: `## 总结一下\n\n写了这么多，其实就想说：${topic}这事儿，平常心对待就好。别太较真，开心最重要！`,
    story: `## 结语\n\n回顾这段关于${topic}的旅程，我学到了很多，也成长了很多。希望我的分享能够给你带来一些启发。`,
    persuasive: `## 行动建议\n\n看完这篇文章，相信你对${topic}有了更深入的了解。现在就是最好的行动时机，不要犹豫，立即开始吧！`,
    emotional: `## 最后想说\n\n${topic}不仅仅是一个话题，更是一种态度。愿我们都能在这个过程中找到属于自己的答案。`
  };

  return conclusions[tone] || conclusions.professional;
}

// 生成标签
function generateTags(topic) {
  const baseTags = ['#干货分享', '#经验分享', '#必看'];
  const topicTag = `#${topic.replace(/\s+/g, '')}`;
  return [topicTag, ...baseTags].join(' ');
}

// 获取随机 emoji
function getRandomEmojis(count) {
  const emojis = ['✨', '🔥', '💡', '🚀', '💯', '📈', '⭐', '👍', '💪', '🎯', '🎉', '💖'];
  return Array(count).fill(0).map(() => emojis[Math.floor(Math.random() * emojis.length)]).join(' ');
}

// 运行
generateArticle().catch(console.error);
