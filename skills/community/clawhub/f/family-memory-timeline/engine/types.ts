// Family Memory Timeline 类型定义

export type MediaType = 'photo' | 'video' | 'audio';
export type EmotionType = 
  | 'joy' | 'happiness' | 'excitement' | 'pride'
  | 'warmth' | 'tenderness' | 'love' | 'gratitude'
  | 'peace' | 'calm' | 'contentment' | 'nostalgia'
  | 'surprise' | 'amazement' | 'wonder'
  | 'sadness' | 'melancholy' | 'missing';

export type StoryStyle = 'warm' | 'humorous' | 'formal' | 'poetic' | 'casual';
export type OutputFormat = 'json' | 'markdown' | 'html';

export interface MediaFile {
  id: string;
  path: string;
  type: MediaType;
  timestamp?: string;
  description?: string;
  metadata: {
    size: number;
    format: string;
    dimensions?: { width: number; height: number };
    duration?: number;
  };
}

export interface DialogueMessage {
  id: string;
  speaker: string;
  content: string;
  timestamp: string;
  platform?: string;
}

export interface TimelineEvent {
  id: string;
  timestamp: string;
  type: 'media' | 'conversation' | 'milestone' | 'custom';
  title: string;
  description: string;
  mediaRefs: string[];
  conversationRefs: string[];
  emotion: {
    primary: EmotionType;
    secondary: EmotionType[];
    intensity: number;
    confidence: number;
    triggers: string[];
  };
  significance: {
    personal: number;
    family: number;
    calculated: number;
  };
  tags: string[];
  processed: boolean;
  narrativeGenerated: boolean;
}

export interface Timeline {
  id: string;
  title: string;
  events: TimelineEvent[];
  timeframe: { start: string; end: string };
  statistics: {
    totalEvents: number;
    emotionDistribution: Record<EmotionType, number>;
  };
}

export interface StoryChapter {
  id: string;
  title: string;
  timeframe: { start: string; end: string };
  timelineEvents: string[];
  narrative: {
    introduction: string;
    development: string;
    climax: string;
    resolution: string;
  };
  emotionalArc: {
    start: EmotionType;
    climax: EmotionType;
    resolution: EmotionType;
    overallTone: string;
  };
  wordCount: number;
  readingTime: number;
}

export interface FamilyStory {
  id: string;
  title: string;
  timeline: Timeline;
  chapters: StoryChapter[];
  summary: {
    timeframe: { start: string; end: string };
    totalEvents: number;
    totalMedia: number;
    totalConversations: number;
    emotionalHighlights: Array<{ emotion: EmotionType; count: number; representativeEvent: string }>;
    keyMoments: Array<{ eventId: string; title: string; significance: number }>;
  };
  metadata: {
    generatedAt: string;
    processingTime: number;
    version: string;
  };
}

export interface StoryConfig {
  timeframe?: { start?: string; end?: string };
  style: {
    narrative: StoryStyle;
    tone: 'formal' | 'casual' | 'intimate';
    perspective: 'first-person' | 'third-person' | 'collective';
    detailLevel: 'brief' | 'standard' | 'detailed';
  };
  filters: {
    minSignificance: number;
    requiredPeople?: string[];
    excludedEmotions?: EmotionType[];
  };
  output: {
    formats: OutputFormat[];
    includeVisualizations: boolean;
    privacyLevel: 'private' | 'family' | 'public';
  };
  processing: {
    enableSentimentAnalysis: boolean;
    language: 'zh' | 'en' | 'auto';
    parallelProcessing: boolean;
  };
}

export interface CreateStoryRequest {
  media?: Array<string | MediaFile>;
  conversations?: Array<string | DialogueMessage>;
  config: Partial<StoryConfig>;
  projectName?: string;
  description?: string;
}

export interface CreateStoryResponse {
  success: boolean;
  story?: FamilyStory;
  error?: { code: string; message: string };
  processing: {
    status: 'pending' | 'processing' | 'completed' | 'failed';
    progress: number;
    currentStep?: string;
  };
}
