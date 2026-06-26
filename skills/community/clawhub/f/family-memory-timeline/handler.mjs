// Family Memory Timeline - 主处理器
// 负责接收请求，分发到各处理模块，生成时间线和故事

const EmotionType = {
  JOY: 'joy', HAPPINESS: 'happiness', EXCITEMENT: 'excitement', PRIDE: 'pride',
  WARMTH: 'warmth', TENDERNESS: 'tenderness', LOVE: 'love', PEACE: 'peace',
  CALM: 'calm', CONTENTMENT: 'contentment', NOSTALGIA: 'nostalgia', SURPRISE: 'surprise', SADNESS: 'sadness'
};

const StoryStyle = {
  WARM: 'warm', HUMOROUS: 'humorous', FORMAL: 'formal', POETIC: 'poetic', CASUAL: 'casual'
};

function generateId(prefix) {
  return prefix + '_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function analyzeEmotion(text) {
  const emotionKeywords = {
    '开心': 'joy', '快乐': 'joy', '幸福': 'warmth', '温馨': 'warmth',
    '激动': 'excitement', '骄傲': 'pride', '惊喜': 'surprise',
    '感动': 'warmth', '想念': 'nostalgia', '悲伤': 'sadness'
  };
  let primary = 'warmth';
  for (const [keyword, emotion] of Object.entries(emotionKeywords)) {
    if (text.includes(keyword)) { primary = emotion; break; }
  }
  return { primary, secondary: [], confidence: 0.85 };
}

function analyzeMediaContent(path, description) {
  return analyzeEmotion(description || path);
}

function calculateSignificance(emotion, hasMedia) {
  let score = 5;
  if (hasMedia) score += 2;
  return { personal: Math.min(10, score), family: Math.min(10, score) * 0.9, calculated: Math.min(10, score) };
}

function extractTitle(path, description) {
  if (description) return description.substring(0, 20);
  const filename = path.split('/').pop() || path;
  return filename.substring(0, 20);
}

function buildTimeline(media, conversations) {
  const events = [];
  
  for (const m of media) {
    const emotion = analyzeMediaContent(m.path, m.description);
    events.push({
      id: generateId('event'),
      timestamp: m.timestamp || new Date().toISOString(),
      type: 'media',
      title: extractTitle(m.path, m.description),
      description: m.description || '照片记录',
      mediaRefs: [m.path],
      conversationRefs: [],
      emotion,
      significance: calculateSignificance(emotion, true),
      tags: [],
      processed: true,
      narrativeGenerated: false
    });
  }
  
  for (const d of conversations) {
    const emotion = analyzeEmotion(d.content);
    events.push({
      id: generateId('event'),
      timestamp: d.timestamp,
      type: 'conversation',
      title: d.speaker + '的重要分享',
      description: d.content,
      mediaRefs: [],
      conversationRefs: [d.content],
      emotion,
      significance: calculateSignificance(emotion, false),
      tags: [],
      processed: true,
      narrativeGenerated: false
    });
  }
  
  events.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
  
  const emotionDistribution = {};
  for (const e of events) {
    emotionDistribution[e.emotion.primary] = (emotionDistribution[e.emotion.primary] || 0) + 1;
  }
  
  return {
    id: generateId('timeline'),
    title: '家庭记忆时间线',
    events,
    timeframe: events.length > 0 
      ? { start: events[0].timestamp, end: events[events.length - 1].timestamp }
      : { start: new Date().toISOString(), end: new Date().toISOString() },
    statistics: { totalEvents: events.length, emotionDistribution }
  };
}

function getStyleNarrative(style) {
  const templates = {
    warm: { intro: '这个月的家庭生活充满了温暖和甜蜜...', dev: '一个个平凡的日子，因为家人的陪伴而变得不平凡...', climax: '最让人印象深刻的是那些充满温情的时刻...', res: '让我们珍惜每一个与家人在一起的瞬间...' },
    humorous: { intro: '这个月的家庭生活简直是喜剧片现场...', dev: '家里每天都热闹非凡，笑声不断...', climax: '最逗的要数那次...', res: '生活就像一盒巧克力，你永远不知道下一颗是什么味道...' },
    formal: { intro: '本月家庭事务记录如下...', dev: '家庭成员共同参与了一系列重要活动...', climax: '其中具有重要意义的是...', res: '总体而言，本月家庭生活秩序井然...' },
    poetic: { intro: '时光如流水，这个月的记忆如同诗篇...', dev: '每一个平凡的瞬间都闪耀着家的光芒...', climax: '那最动人的篇章...', res: '岁月静好，与家人同行的每一天都是礼物...' },
    casual: { intro: '这个月家里发生了不少事...', dev: '来来来，听我慢慢说...', climax: '最精彩的是那次...', res: '总之，这个月很开心！' }
  };
  return templates[style] || templates.warm;
}

function getToneDescription(emotion) {
  const desc = { warmth: '温馨感人', joy: '欢快愉悦', excitement: '激动人心', pride: '骄傲自豪', love: '充满爱意', nostalgia: '怀念感恩', contentment: '宁静满足', calm: '平和宁静' };
  return desc[emotion] || '温暖人心';
}

function generateChapters(timeline, config) {
  if (timeline.events.length === 0) return [];
  
  const style = config?.style?.narrative || 'warm';
  const chapters = [];
  const monthGroups = new Map();
  
  for (const event of timeline.events) {
    const date = new Date(event.timestamp);
    const monthKey = date.getFullYear() + '-' + String(date.getMonth() + 1).padStart(2, '0');
    if (!monthGroups.has(monthKey)) monthGroups.set(monthKey, []);
    monthGroups.get(monthKey).push(event);
  }
  
  for (const [month, events] of monthGroups) {
    const firstDate = new Date(events[0].timestamp);
    const lastDate = new Date(events[events.length - 1].timestamp);
    const dominant = {};
    for (const e of events) dominant[e.emotion.primary] = (dominant[e.emotion.primary] || 0) + 1;
    const primaryEmotion = Object.entries(dominant).sort((a, b) => b[1] - a[1])[0]?.[0] || 'warmth';
    const tmpl = getStyleNarrative(style);
    const eventSummaries = events.slice(0, 3).map(e => e.description).join('；');
    
    chapters.push({
      id: generateId('chapter'),
      title: month + '月的温馨时刻',
      timeframe: { start: firstDate.toISOString(), end: lastDate.toISOString() },
      timelineEvents: events.map(e => e.id),
      narrative: { introduction: tmpl.intro + (eventSummaries ? ' ' + eventSummaries : ''), development: tmpl.dev, climax: tmpl.climax + ' ' + (events[0]?.title || '那些特别的日子'), resolution: tmpl.res },
      emotionalArc: { start: 'calm', climax: primaryEmotion, resolution: 'contentment', overallTone: getToneDescription(primaryEmotion) },
      wordCount: 200 + events.length * 50,
      readingTime: Math.ceil((200 + events.length * 50) / 500)
    });
  }
  return chapters;
}

function generateStory(request) {
  const startTime = Date.now();
  const mediaList = (request.media || []).map(m => typeof m === 'string' ? { path: m } : { path: m.path, description: m.description, timestamp: m.timestamp });
  const dialogueList = (request.conversations || []).map(d => typeof d === 'string' ? { speaker: '家人', content: d, timestamp: new Date().toISOString() } : { speaker: d.speaker, content: d.content, timestamp: d.timestamp });
  
  const timeline = buildTimeline(mediaList, dialogueList);
  const chapters = generateChapters(timeline, request.config);
  
  const emotionalHighlights = Object.entries(timeline.statistics.emotionDistribution).map(([emotion, count]) => ({ emotion, count, representativeEvent: timeline.events.find(e => e.emotion.primary === emotion)?.title || '' })).sort((a, b) => b.count - a.count);
  const keyMoments = [...timeline.events].sort((a, b) => b.significance.calculated - a.significance.calculated).slice(0, 5).map(e => ({ eventId: e.id, title: e.title, significance: e.significance.calculated }));
  
  return {
    id: generateId('story'),
    title: request.projectName || '我们的家庭故事',
    timeline,
    chapters,
    summary: { timeframe: timeline.timeframe, totalEvents: timeline.events.length, totalMedia: mediaList.length, totalConversations: dialogueList.length, emotionalHighlights, keyMoments },
    metadata: { generatedAt: new Date().toISOString(), processingTime: Date.now() - startTime, version: '0.1.0' }
  };
}

function toMarkdown(story) {
  const lines = [];
  lines.push('# ' + story.title);
  lines.push('');
  lines.push('**生成时间**: ' + new Date(story.metadata.generatedAt).toLocaleString('zh-CN'));
  lines.push('**时间范围**: ' + new Date(story.summary.timeframe.start).toLocaleDateString('zh-CN') + ' - ' + new Date(story.summary.timeframe.end).toLocaleDateString('zh-CN'));
  lines.push('');
  lines.push('## 统计概览');
  lines.push('- 总事件数: ' + story.summary.totalEvents);
  lines.push('- 照片/媒体: ' + story.summary.totalMedia);
  lines.push('- 对话记录: ' + story.summary.totalConversations);
  lines.push('');
  lines.push('## 时间线');
  for (const event of story.timeline.events) {
    lines.push('### ' + new Date(event.timestamp).toLocaleDateString('zh-CN') + ' - ' + event.title);
    lines.push('- 类型: ' + event.type);
    lines.push('- 描述: ' + event.description);
    lines.push('- 情感: ' + event.emotion.primary + ' (' + Math.round(event.emotion.confidence * 100) + '%置信度)');
    lines.push('- 重要性: ' + event.significance.calculated + '/10');
    lines.push('');
  }
  lines.push('## 故事章节');
  for (const ch of story.chapters) {
    lines.push('### ' + ch.title);
    lines.push('时期: ' + new Date(ch.timeframe.start).toLocaleDateString('zh-CN') + ' - ' + new Date(ch.timeframe.end).toLocaleDateString('zh-CN'));
    lines.push('情感基调: ' + ch.emotionalArc.overallTone);
    lines.push('叙述: ' + ch.narrative.introduction);
    lines.push('');
  }
  lines.push('## 情感亮点');
  for (const h of story.summary.emotionalHighlights) lines.push('- ' + h.emotion + ': ' + h.count + '次 (代表: ' + h.representativeEvent + ')');
  lines.push('');
  lines.push('## 关键时刻');
  for (const m of story.summary.keyMoments) lines.push('- ' + m.title + ' (重要性: ' + m.significance + '/10)');
  lines.push('');
  lines.push('---');
  lines.push('*由家庭记忆时光机生成 | 版本: ' + story.metadata.version + '*');
  return lines.join('\n');
}

export async function handleFamilyMemoryTimeline(request) {
  try {
    const story = generateStory(request);
    const outputContent = (request.config?.output?.formats || []).includes('markdown') ? toMarkdown(story) : JSON.stringify(story, null, 2);
    return { success: true, story, processing: { status: 'completed', progress: 100 }, outputContent };
  } catch (error) {
    return { success: false, error: { code: 'UNKNOWN_ERROR', message: error.message }, processing: { status: 'failed', progress: 0 } };
  }
}

export default { handleFamilyMemoryTimeline };
