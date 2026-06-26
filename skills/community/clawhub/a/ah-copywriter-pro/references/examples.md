# Copywriter Pro — Code Examples

## Example 1

```typescript
// Classic copywriting formulas
interface CopywritingFramework {
  name: string;
  structure: string[];
  bestFor: string[];
  example: string;
}

const COPYWRITING_FRAMEWORKS = {
  AIDA: {
    structure: ['Attention', 'Interest', 'Desire', 'Action'],
    bestFor: ['ads', 'landing pages', 'email subject lines'],
    description: 'Classic framework for guiding readers to action'
  },

  PAS: {
    structure: ['Problem', 'Agitation', 'Solution'],
    bestFor: ['sales pages', 'email copy', 'video scripts'],
    description: 'Highlights pain before presenting solution'
  },

  PASTOR: {
    structure: ['Problem', 'Amplify', 'Story', 'Transformation', 'Offer', 'Response'],
    bestFor: ['long-form sales pages', 'webinar scripts'],
    description: 'Extended framework for complex sales'
  },

  BAB: {
    structure: ['Before', 'After', 'Bridge'],
    bestFor: ['quick pitches', 'social posts', 'testimonials'],
    description: 'Simple transformation narrative'
  },

  QUEST: {
    structure: ['Qualify', 'Understand', 'Educate', 'Stimulate', 'Transition'],
    bestFor: ['consultative selling', 'B2B copy'],
    description: 'Education-first approach'
  },

  FourPs: {
    structure: ['Promise', 'Picture', 'Proof', 'Push'],
    bestFor: ['direct response', 'infomercials', 'VSLs'],
    description: 'Promise-driven persuasion'
  },

  SLAP: {
    structure: ['Stop', 'Look', 'Act', 'Purchase'],
    bestFor: ['print ads', 'billboards', 'quick ads'],
    description: 'Attention-first short format'
  }
};
```

## Example 2

```typescript
// Multi-platform ad copy
interface AdCopy {
  platform: AdPlatform;
  format: AdFormat;
  components: AdComponents;
  variations: number;
}

type AdPlatform = 'facebook' | 'instagram' | 'google' | 'linkedin' | 'tiktok' | 'twitter';

interface AdComponents {
  headline: string;
  primaryText: string;
  description?: string;
  cta: string;
  hooks: string[];
}

// Platform-specific ad specs
const AD_SPECS = {
  facebook: {
    headline: { max: 40, optimal: 25 },
    primaryText: { max: 125, optimal: 80 },
    description: { max: 30 },
    formats: ['single-image', 'carousel', 'video', 'collection']
  },
  google: {
    headlines: { count: 15, max: 30 },
    descriptions: { count: 4, max: 90 },
    formats: ['search', 'display', 'performance-max']
  },
  linkedin: {
    headline: { max: 70 },
    introText: { max: 600, optimal: 150 },
    formats: ['single-image', 'carousel', 'video', 'text']
  },
  tiktok: {
    text: { max: 100 },
    hook: { time: '1-3 seconds' },
    formats: ['in-feed', 'spark', 'topview']
  }
};

// Hook templates by objective
const AD_HOOKS = {
  curiosity: [
    "What if I told you...",
    "Here's what nobody tells you about...",
    "The secret [industry] doesn't want you to know..."
  ],
  pain: [
    "Tired of [problem]?",
    "Still struggling with [issue]?",
    "Why does [problem] keep happening?"
  ],
  transformation: [
    "From [before] to [after] in [time]",
    "How I went from [struggle] to [success]",
    "[Result] without [sacrifice]"
  ],
  social_proof: [
    "[Number] people can't be wrong",
    "Join [number]+ who already...",
    "The [tool/method] trusted by..."
  ],
  urgency: [
    "Last chance to...",
    "Only [number] spots left",
    "Ending [time period]..."
  ]
};
```

## Example 3

```typescript
// Email sequence templates
interface EmailSequence {
  type: SequenceType;
  emails: EmailCopy[];
  timing: EmailTiming;
  goal: string;
}

type SequenceType =
  | 'welcome' | 'nurture' | 'launch'
  | 'abandoned-cart' | 'onboarding'
  | 're-engagement' | 'post-purchase';

interface EmailCopy {
  subject: SubjectLine;
  preheader: string;
  body: EmailBody;
  cta: EmailCTA;
  ps?: string;
}

// Subject line formulas
const SUBJECT_LINE_FORMULAS = {
  curiosity: [
    "This changed everything...",
    "You won't believe what happened",
    "I have to tell you something"
  ],
  benefit: [
    "[Outcome] in [timeframe]",
    "Get [result] without [pain]",
    "The fastest way to [goal]"
  ],
  urgency: [
    "Last chance: [offer]",
    "[Hours] left to claim your...",
    "Don't miss this"
  ],
  personalized: [
    "{FirstName}, I noticed...",
    "Quick question, {FirstName}",
    "Thought of you when..."
  ],
  newsworthy: [
    "[Breaking] [news]",
    "Just announced: [update]",
    "You're invited to..."
  ],
  story: [
    "The story of [outcome]",
    "How [person] achieved [result]",
    "What [experience] taught me"
  ]
};

// Email sequence examples
const EMAIL_SEQUENCES = {
  welcome: [
    { day: 0, subject: "Welcome! Here's what's next", goal: "deliver lead magnet + set expectations" },
    { day: 1, subject: "The biggest mistake I see...", goal: "identify problem" },
    { day: 3, subject: "How [result] is actually achieved", goal: "position solution" },
    { day: 5, subject: "Your next step", goal: "soft pitch" },
    { day: 7, subject: "Quick question for you", goal: "engagement + qualify" }
  ],
  launch: [
    { day: -3, subject: "Something exciting is coming...", goal: "build anticipation" },
    { day: -1, subject: "Tomorrow: [product] launches", goal: "reminder" },
    { day: 0, subject: "[Product] is LIVE", goal: "launch announcement" },
    { day: 1, subject: "Did you see this?", goal: "reminder" },
    { day: 3, subject: "FAQ: Your questions answered", goal: "objection handling" },
    { day: 5, subject: "Closing soon + bonuses expire", goal: "urgency" },
    { day: 7, subject: "Final call: [product]", goal: "last chance" }
  ]
};
```

## Example 4

```typescript
// Long-form sales page
interface SalesPageCopy {
  sections: SalesSection[];
  length: 'short' | 'medium' | 'long';
  style: SalesStyle;
}

type SalesStyle = 'story-driven' | 'proof-heavy' | 'benefit-focused' | 'educational';

// Sales page section templates
const SALES_PAGE_SECTIONS = {
  headline: {
    purpose: "Stop scroll, create intrigue",
    length: "5-15 words",
    formula: "Promise + Timeframe + Without Pain"
  },
  openingStory: {
    purpose: "Build connection, establish credibility",
    length: "200-400 words",
    structure: "Before struggle → Turning point → After success"
  },
  problemAgitation: {
    purpose: "Make reader feel understood",
    length: "300-500 words",
    technique: "List problems, amplify consequences"
  },
  solutionIntro: {
    purpose: "Position product as answer",
    length: "100-200 words",
    approach: "Bridge from problem to product"
  },
  benefits: {
    purpose: "Show what's in it for them",
    format: "Bullet points with headlines",
    count: "7-12 benefits"
  },
  features: {
    purpose: "Explain what they get",
    format: "Feature + Benefit pairs",
    count: "5-10 main features"
  },
  socialProof: {
    purpose: "Remove doubt with evidence",
    types: ["testimonials", "case studies", "numbers", "logos"],
    quantity: "Minimum 3-5 testimonials"
  },
  objectionHandling: {
    purpose: "Address hesitations",
    format: "FAQ or direct addressing",
    common: ["price", "time", "complexity", "trust"]
  },
  offer: {
    purpose: "Make the deal irresistible",
    elements: ["main product", "bonuses", "guarantee", "urgency"]
  },
  guarantee: {
    purpose: "Remove risk",
    types: ["money-back", "results-based", "double-your-money"]
  },
  cta: {
    purpose: "Drive action",
    placement: "Every 500-800 words",
    style: "Action-oriented, benefit-driven"
  }
};
```

## Example 5

```typescript
// Brand voice configuration
interface BrandVoice {
  personality: PersonalityTraits;
  tone: ToneSettings;
  vocabulary: VocabularyRules;
  examples: VoiceExamples;
}

interface PersonalityTraits {
  primary: string; // e.g., "friendly expert"
  attributes: string[]; // e.g., ["approachable", "knowledgeable", "witty"]
  avoid: string[]; // e.g., ["corporate speak", "jargon"]
}

// Voice presets by industry
const VOICE_PRESETS = {
  saas: {
    personality: "Helpful tech friend",
    traits: ["clear", "confident", "slightly casual"],
    vocabulary: ["simple words", "active voice", "specific numbers"],
    avoid: ["buzzwords", "passive voice", "vague claims"]
  },
  ecommerce: {
    personality: "Enthusiastic curator",
    traits: ["excited", "descriptive", "personal"],
    vocabulary: ["sensory words", "lifestyle language", "social proof"],
    avoid: ["pushy sales language", "generic descriptions"]
  },
  coach: {
    personality: "Supportive mentor",
    traits: ["empathetic", "motivating", "direct"],
    vocabulary: ["you-focused", "transformation words", "action verbs"],
    avoid: ["talking down", "overpromising"]
  },
  luxury: {
    personality: "Sophisticated insider",
    traits: ["refined", "exclusive", "confident"],
    vocabulary: ["premium words", "understated", "aspirational"],
    avoid: ["discounts focus", "desperation", "commonplace"]
  }
};
```
