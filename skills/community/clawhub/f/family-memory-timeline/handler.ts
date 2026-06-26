// Family Memory Timeline - 主处理器
// 负责接收请求，分发到各处理模块，生成时间线和故事

import type { 
  CreateStoryRequest, 
  CreateStoryResponse, 
  FamilyStory, 
  TimelineEvent, 
  StoryChapter,
  Timeline,
  EmotionType,
  StoryStyle
} from './engine/types.js';

// 情感分析引擎（模拟）
function analyzeEmotion(text: string): { primary: EmotionType; secondary: EmotionType[]; confidence: number } {
  const emotionKeywords: Record<string, EmotionType[]> = {
    '开心': ['joy', 'happiness'],
    '快乐': ['joy', 'happiness'],
    '幸福': ['warmth', 'contentment'],
    '温馨': ['warmth', 'tenderness'],
    '激动': ['excitement', 'pride'],
    '骄傲': ['pride'],
    '惊喜': ['surprise', 'excitement'],
    '感动': ['warmth', 'gratitude'],
    '想念': ['nostalgia', 'missing'],
    '悲伤': ['sadness', 'melancholy'],
  };
  
  let primary: EmotionType = 'warmth';
  let confidence = 0.7;
  
  for (const [keyword, emotions] of Object.entries(emotionKeywords)) {
    if (text.includes(keyword)) {
      primary = emotions[0];
      confidence = 0.85;
      break;
    }
  }
  
  return { primary, secondary: [], confidence };
}

// 模拟媒体文件分析
function analyzeMediaContent(path: string, description?: string): TimelineEvent['emotion'] {
  const text = description || path;
  return analyzeEmotion(text);
}

// 模拟对话情感分析
function analyzeDialogueEmotion(content: string): TimelineEvent['emotion'] {
  return analyzeEmotion(content);
}

// 计算事件重要性
function calculateSignificance(emotion: TimelineEvent['emotion'], hasMedia: boolean): { personal: number; family: number; calculated: number } {
  let score = emotion.intensity || 5;
  if (hasMedia) score += 2;
  score = Math.min(10, score);
  
  return {
    personal: score,
    family: score * 0.9,
    calculated: score
  };
}

// 生成唯一ID
function generateId(prefix: string): string {
  return prefix + '_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// 构建时间线
function buildTimeline(
  media: Array<{ path: string; description?: string; timestamp?: string }>,
  conversations: Array<{ speaker: string; content: string; timestamp: string }>,
  config: CreateStoryRequest['config']
): Timeline {
  const events: TimelineEvent[] = [];
  
  // 处理媒体文件
  for (const m of media) {
    const timestamp = m.timestamp || new Date().toISOString();
    const emotion = analyzeMediaContent(m.path, m.description);
    
    events.push({
      id: generateId('event'),
      timestamp,
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
  
  // 处理对话
  for (const d of conversations) {
    const emotion = analyzeDialogueEmotion(d.content);
    
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
  
  // 按时间排序
  events.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
  
  // 统计数据
  const emotionDistribution: Record<EmotionType, number> = {} as Record<EmotionType, number>;
  for (const e of events) {
    emotionDistribution[e.emotion.primary] = (emotionDistribution[e.emotion.primary] || 0) + 1;
  }
  
  const timeRange = events.length > 0 
    ? { start: events[0].timestamp, end: events[events.length - 1].timestamp }
    : { start: new Date().toISOString(), end: new Date().toISOString() };
  
  return {
    id: generateId('timeline'),
    title: '家庭记忆时间线',
    events,
    timeframe: timeRange,
    statistics: {
      totalEvents: events.length,
      emotionDistribution
    }
  };
}

// 从路径或描述中提取标题
function extractTitle(path: string, description?: string): string {
  if (description) {
    return description.substring(0, 20);
  }
  const filename = path.split('/').pop() || path;
  return filename.substring(0, 20);
}

// 生成分章故事
function generateChapters(timeline: Timeline, config: CreateStoryRequest['config']): StoryChapter[] {
  if (timeline.events.length === 0) {
    return [];
  }
  
  const style: StoryStyle = config?.style?.narrative || 'warm';
  const chapters: StoryChapter[] = [];
  
  // 按月份分组
  const monthGroups = new Map<string, TimelineEvent[]>();
  
  for (const event of timeline.events) {
    const date = new Date(event.timestamp);
    const monthKey = date.getFullYear() + '-' + String(date.getMonth() + 1).padStart(2, '0');
    
    if (!monthGroups.has(monthKey)) {
      monthGroups.set(monthKey, []);
    }
    monthGroups.get(monthKey)!.push(event);
  }
  
  // 为每个月份生成章节
  for (const [month, events] of monthGroups) {
    const firstDate = new Date(events[0].timestamp);
    const lastDate = new Date(events[events.length - 1].timestamp);
    
    const dominantEmotion = events.reduce((acc, e) => {
      acc[e.emotion.primary] = (acc[e.emotion.primary] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    
    const primaryEmotion = Object.entries(dominantEmotion)
      .sort((a, b) => b[1] - a[1])[0]?.[0] as EmotionType || 'warmth';
    
    chapters.push({
      id: generateId('chapter'),
      title: month + '月的温馨时刻',
      timeframe: {
        start: firstDate.toISOString(),
        end: lastDate.toISOString()
      },
      timelineEvents: events.map(e => e.id),
      narrative: generateChapterNarrative(events, style, primaryEmotion),
      emotionalArc: {
        start: 'calm',
        climax: primaryEmotion,
        resolution: 'contentment',
        overallTone: getToneDescription(primaryEmotion, style)
      },
      wordCount: 200 + events.length * 50,
      readingTime: Math.ceil((200 + events.length * 50) / 500)
    });
  }
  
  return chapters;
}

// 生成章节叙述文本
function generateChapterNarrative(events: TimelineEvent[], style: StoryStyle, emotion: EmotionType): StoryChapter['narrative'] {
  const styleTemplates: Record<StoryStyle, { intro: string; dev: string; climax: string; res: string }> = {
    warm: {
      intro: '这个月的家庭生活充满了温暖和甜蜜...',
      dev: '一个个平凡的日子，因为家人的陪伴而变得不平凡...',
      climax: '最让人印象深刻的是那些充满温情的时刻...',
      res: '让我们珍惜每一个与家人在一起的瞬间...'
    },
    humorous: {
      intro: '这个月的家庭生活简直是喜剧片现场...',
      dev: '家里每天都热闹非凡，笑声不断...',
      climax: '最逗的要数那次...',
      res: '生活就像一盒巧克力，你永远不知道下一颗是什么味道...'
    },
    formal: {
      intro: '本月家庭事务记录如下...',
      dev: '家庭成员共同参与了一系列重要活动...',
      climax: '其中具有重要意义的是...',
      res: '总体而言，本月家庭生活秩序井然...'
    },
    poetic: {
      intro: '时光如流水，这个月的记忆如同诗篇...',
      dev: '每一个平凡的瞬间都闪耀着家的光芒...',
      climax: '那最动人的篇章...',
      res: '岁月静好，与家人同行的每一天都是礼物...'
    },
    casual: {
      intro: '这个月家里发生了不少事...',
      dev: '来来来，听我慢慢说...',
      climax: '最精彩的是那次...',
      res: '总之，这个月很开心！'
    }
  };
  
  const template = styleTemplates[style] || styleTemplates.warm;
  const eventSummaries = events.slice(0, 3).map(e => e.description).join('；');
  
  return {
    introduction: template.intro + (eventSummaries ? ' ' + eventSummaries : ''),
    development: template.dev,
    climax: template.climax + ' ' + (events[0]?.title || '那些特别的日子'),
    resolution: template.res
  };
}

// 获取情感风格描述
function getToneDescription(emotion: EmotionType, style: StoryStyle): string {
  const descriptions: Record<string, string> = {
    'warmth': '温馨感人',
    'joy': '欢快愉悦',
    'excitement': '激动人心',
    'pride': '骄傲自豪',
    'love': '充满爱意',
    'nostalgia': '怀念感恩',
    'contentment': '宁静满足',
    'calm': '平和宁静'
  };
  return descriptions[emotion] || '温暖人心';
}

// 生成完整故事
function generateStory(request: CreateStoryRequest): FamilyStory {
  const startTime = Date.now();
  
  const mediaList = (request.media || []).map(m => {
    if (typeof m === 'string') {
      return { path: m, description: undefined, timestamp: undefined };
    }
    return { path: m.path, description: m.description, timestamp: m.timestamp };
  });
  
  const dialogueList = (request.conversations || []).map(d => {
    if (typeof d === 'string') {
      return { speaker: '家人', content: d, timestamp: new Date().toISOString() };
    }
    return { speaker: d.speaker, content: d.content, timestamp: d.timestamp };
  });
  
  const timeline = buildTimeline(mediaList, dialogueList, request.config);
  const chapters = generateChapters(timeline, request.config);
  
  const emotionalHighlights = Object.entries(timeline.statistics.emotionDistribution)
    .map(([emotion, count]) => ({
      emotion: emotion as EmotionType,
      count,
      representativeEvent: timeline.events.find(e => e.emotion.primary === emotion)?.title || ''
    }))
    .sort((a, b) => b.count - a.count);
  
  const keyMoments = [...timeline.events]
    .sort((a, b) => b.significance.calculated - a.significance.calculated)
    .slice(0, 5)
    .map(e => ({
      eventId: e.id,
      title: e.title,
      significance: e.significance.calculated
    }));
  
  const endTime = Date.now();
  
  return {
    id: generateId('story'),
    title: request.projectName || '我们的家庭故事',
    timeline,
    chapters,
    summary: {
      timeframe: timeline.timeframe,
      totalEvents: timeline.events.length,
      totalMedia: mediaList.length,
      totalConversations: dialogueList.length,
      emotionalHighlights,
      keyMoments
    },
    metadata: {
      generatedAt: new Date().toISOString(),
      processingTime: endTime - startTime,
      version: '0.1.0'
    }
  };
}

// 将故事转换为Markdown格式
function toMarkdown(story: FamilyStory): string {
  const lines: string[] = [];
  
  lines.push('# ' + story.title);
  lines.push('');
  lines.push('**生成时间**: ' + new Date(story.metadata.generatedAt).toLocaleString('zh-CN'));
  lines.push('**时间范围**: ' + new Date(story.summary.timeframe.start).toLocaleDateString('zh-CN') + ' - ' + new Date(story.summary.timeframe.end).toLocaleDateString('zh-CN'));
  lines.push('');
  lines.push('## 📊 统计概览');
  lines.push('');
  lines.push('- 总事件数: ' + story.summary.totalEvents);
  lines.push('- 照片/媒体: ' + story.summary.totalMedia);
  lines.push('- 对话记录: ' + story.summary.totalConversations);
  lines.push('');
  lines.push('## 📅 时间线');
  lines.push('');
  
  for (const event of story.timeline.events) {
    lines.push('### ' + new Date(event.timestamp).toLocaleDateString('zh-CN') + ' - ' + event.title);
    lines.push('');
    lines.push('- **类型**: ' + event.type);
    lines.push('- **描述**: ' + event.description);
    lines.push('- **情感**: ' + event.emotion.primary + ' (' + Math.round(event.emotion.confidence * 100) + '%置信度)');
    lines.push('- **重要性**: ' + event.significance.calculated + '/10');
    lines.push('');
  }
  
  lines.push('## 📖 故事章节');
  lines.push('');
  
  for (const chapter of story.chapters) {
    lines.push('### ' + chapter.title);
    lines.push('');
    lines.push('**时期**: ' + new Date(chapter.timeframe.start).toLocaleDateString('zh-CN') + ' - ' + new Date(chapter.timeframe.end).toLocaleDateString('zh-CN'));
    lines.push('');
    lines.push('**情感基调**: ' + chapter.emotionalArc.overallTone);
    lines.push('');
    lines.push('**叙述**: ' + chapter.narrative.introduction);
    lines.push('');
    lines.push('---');
    lines.push('');
  }
  
  lines.push('## 💡 情感亮点');
  lines.push('');
  
  for (const highlight of story.summary.emotionalHighlights) {
    lines.push('- **' + highlight.emotion + '**: ' + highlight.count + '次 (代表: ' + highlight.representativeEvent + ')');
  }
  lines.push('');
  lines.push('## ⭐ 关键时刻');
  lines.push('');
  
  for (const moment of story.summary.keyMoments) {
    lines.push('- ' + moment.title + ' (重要性: ' + moment.significance + '/10)');
  }
  lines.push('');
  lines.push('---');
  lines.push('*由家庭记忆时光机生成 | 版本: ' + story.metadata.version + '*');
  
  return lines.join('\n');
}

// 将故事转换为JSON格式
function toJSON(story: FamilyStory): string {
  return JSON.stringify(story, null, 2);
}

// 主入口函数
export async function handleFamilyMemoryTimeline(request: CreateStoryRequest): Promise<CreateStoryResponse> {
  try {
    const story = generateStory(request);
    const formats = request.config?.output?.formats || ['json'];
    
    let outputContent = '';
    if (formats.includes('markdown')) {
      outputContent = toMarkdown(story);
    } else {
      outputContent = toJSON(story);
    }
    
    return {
      success: true,
      story,
      processing: {
        status: 'completed',
        progress: 100
      }
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'UNKNOWN_ERROR',
        message: error instanceof Error ? error.message : '处理失败'
      },
      processing: {
        status: 'failed',
        progress: 0
      }
    };
  }
}

// 兼容 CommonJS
export default { handleFamilyMemoryTimeline };
