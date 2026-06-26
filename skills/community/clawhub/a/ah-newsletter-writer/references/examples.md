# Newsletter Writer — Code Examples

## Example 1

```typescript
// Newsletter architecture
interface NewsletterStrategy {
  brand: BrandIdentity;
  audience: AudienceProfile;
  contentPillars: ContentPillar[];
  cadence: PublishingCadence;
  goals: NewsletterGoals;
}

interface ContentPillar {
  name: string;
  description: string;
  frequency: 'every-issue' | 'weekly' | 'monthly';
  format: ContentFormat;
}

// Proven newsletter formats
const NEWSLETTER_FORMATS = {
  curated: {
    description: "Best links/content from around the web",
    structure: ["intro", "top-picks", "categories", "personal-note"],
    examples: ["Morning Brew", "TLDR", "The Hustle"]
  },
  educational: {
    description: "One big idea or lesson per issue",
    structure: ["hook", "concept", "examples", "action-steps"],
    examples: ["James Clear", "Sahil Bloom", "Tim Ferriss"]
  },
  storytelling: {
    description: "Personal stories with insights",
    structure: ["story", "lesson", "application", "cta"],
    examples: ["Ann Handley", "Seth Godin"]
  },
  hybrid: {
    description: "Mix of curation and original content",
    structure: ["main-essay", "curated-links", "updates"],
    examples: ["The Hustle", "Stratechery"]
  },
  product: {
    description: "Updates, tips, and company news",
    structure: ["updates", "tips", "community", "cta"],
    examples: ["Notion", "Superhuman", "Linear"]
  }
};
```

## Example 2

```typescript
// Subject line optimization
interface SubjectLine {
  text: string;
  type: SubjectType;
  preheader: string;
  abVariants?: string[];
}

type SubjectType =
  | 'curiosity' | 'benefit' | 'urgency'
  | 'personalized' | 'question' | 'number'
  | 'story' | 'controversial';

// High-performing subject line patterns
const SUBJECT_PATTERNS = {
  curiosity: {
    templates: [
      "This changed everything...",
      "What nobody tells you about [topic]",
      "I finally figured it out"
    ],
    openRate: "35-45%"
  },
  benefit: {
    templates: [
      "[Outcome] in [timeframe]",
      "How to [achieve result] without [pain]",
      "The [adjective] way to [goal]"
    ],
    openRate: "30-40%"
  },
  number: {
    templates: [
      "[Number] ways to [outcome]",
      "I tested [number] [things]. Here's what worked.",
      "[Number] lessons from [experience]"
    ],
    openRate: "30-35%"
  },
  personal: {
    templates: [
      "Can I be honest with you?",
      "Quick favor to ask",
      "I made a mistake"
    ],
    openRate: "35-50%"
  },
  story: {
    templates: [
      "The story of how I [achievement]",
      "What happened when [event]",
      "I never told anyone this..."
    ],
    openRate: "35-45%"
  }
};

// Preheader optimization
const PREHEADER_TIPS = {
  length: "40-90 characters for full visibility",
  purpose: "Complement subject, add context",
  avoid: "Don't repeat subject line",
  examples: [
    "Subject: The secret to 10x growth | Preheader: (Plus: my biggest mistake)",
    "Subject: Quick question | Preheader: I need your help with something"
  ]
};
```

## Example 3

```typescript
// Newsletter anatomy
interface NewsletterContent {
  intro: IntroSection;
  mainContent: MainContent;
  sections: ContentSection[];
  cta: CTASection;
  footer: FooterSection;
}

interface IntroSection {
  greeting: string;
  hook: string;
  teaser: string;
  length: "2-4 sentences";
}

// Intro templates
const INTRO_TEMPLATES = {
  story: `
    Happy [Day], [First Name]!

    [One sentence about what happened this week]

    This reminded me of something important...
  `,

  direct: `
    Hey [First Name],

    Today I want to share [topic] because [reason].

    Let's dive in.
  `,

  question: `
    Quick question for you:

    [Thought-provoking question]?

    Today's issue might help you answer that.
  `,

  observation: `
    I noticed something interesting this week.

    [Observation about industry/topic]

    Here's why it matters...
  `
};

// Section templates
const SECTION_TEMPLATES = {
  mainIdea: {
    structure: ["headline", "hook", "explanation", "examples", "takeaway"],
    length: "300-600 words"
  },
  quickTips: {
    structure: ["intro", "numbered-tips", "wrap-up"],
    length: "150-300 words"
  },
  curation: {
    structure: ["category-header", "links-with-commentary"],
    count: "3-7 links"
  },
  story: {
    structure: ["setup", "conflict", "resolution", "lesson"],
    length: "200-400 words"
  }
};
```

## Example 4

```typescript
// Engagement techniques
interface WritingTechniques {
  hooks: HookTypes[];
  formatting: FormattingRules;
  voice: VoiceGuidelines;
  engagement: EngagementTactics;
}

// Hook types for newsletters
const HOOK_TYPES = {
  boldStatement: {
    example: "Everything you know about productivity is wrong.",
    when: "When challenging conventional wisdom"
  },
  question: {
    example: "What would you do with an extra 10 hours per week?",
    when: "When addressing pain points"
  },
  statistic: {
    example: "91% of New Year's resolutions fail by February.",
    when: "When establishing credibility"
  },
  story: {
    example: "Last Tuesday, I almost quit.",
    when: "When building personal connection"
  },
  confession: {
    example: "I have to be honest about something.",
    when: "When building trust through vulnerability"
  }
};

// Formatting for readability
const FORMATTING_RULES = {
  paragraphs: "2-3 sentences max",
  lineBreaks: "Between every 2-3 paragraphs",
  bulletPoints: "For lists of 3+ items",
  bold: "Key phrases and takeaways",
  headers: "Break up long content",
  links: "Descriptive anchor text",
  images: "1-3 per newsletter max",
  width: "600px or less for readability"
};
```

## Example 5

```typescript
// Dynamic personalization
interface Personalization {
  fields: PersonalizationField[];
  segments: AudienceSegment[];
  dynamicContent: DynamicBlock[];
}

// Personalization strategies
const PERSONALIZATION_TYPES = {
  basic: {
    fields: ["first_name", "company"],
    example: "Hey {first_name},"
  },
  behavioral: {
    fields: ["last_purchase", "content_interest", "engagement_level"],
    example: "Since you loved our [last_topic] content..."
  },
  preference: {
    fields: ["preferred_topics", "industry", "role"],
    example: "Curated specifically for [role]s in [industry]"
  },
  lifecycle: {
    fields: ["subscriber_age", "customer_status", "engagement_score"],
    example: "Special content for our VIP subscribers"
  }
};

// Segmentation examples
const SEGMENT_STRATEGIES = {
  newSubscribers: {
    content: "Welcome series, onboarding",
    tone: "Welcoming, educational"
  },
  engagedReaders: {
    content: "Exclusive content, early access",
    tone: "Insider, rewarding"
  },
  inactiveSubscribers: {
    content: "Re-engagement, best-of",
    tone: "We miss you, highlight reel"
  },
  customers: {
    content: "Product updates, advanced tips",
    tone: "Supportive, exclusive"
  }
};
```

## Example 6

```typescript
// Newsletter growth tactics
interface GrowthStrategy {
  acquisition: AcquisitionTactics;
  retention: RetentionTactics;
  monetization: MonetizationModels;
}

// Growth tactics
const GROWTH_TACTICS = {
  organic: [
    "Referral program with incentives",
    "Social media content repurposing",
    "SEO-optimized newsletter archive",
    "Cross-promotions with complementary newsletters",
    "Guest writing and features"
  ],
  paid: [
    "Newsletter sponsorship swaps",
    "Social media ads to lead magnet",
    "Podcast sponsorships",
    "Newsletter advertising platforms"
  ],
  viral: [
    "Share buttons in emails",
    "Quotable snippets for social",
    "Forward-to-friend incentives",
    "User-generated content features"
  ]
};

// Monetization models
const MONETIZATION_MODELS = {
  sponsorships: {
    format: ["dedicated", "classified", "featured"],
    pricing: "CPM: $20-50, CPO varies",
    requirements: "5K+ engaged subscribers"
  },
  paidNewsletter: {
    platforms: ["Substack", "Ghost", "Beehiiv"],
    pricing: "$5-50/month",
    conversionRate: "1-5% of free subscribers"
  },
  products: {
    types: ["courses", "ebooks", "templates", "coaching"],
    integration: "Native promotion in content"
  },
  affiliates: {
    approach: "Genuine recommendations only",
    disclosure: "Clear affiliate disclosure required"
  }
};
```

## Example 7

```typescript
// Ready-to-use templates
const NEWSLETTER_TEMPLATES = {
  weekly_roundup: `
    Subject: This Week in [Topic] 🔥

    Hey {first_name},

    Happy [Day]! Here's what caught my attention this week:

    ## 🎯 Big Idea
    [Main insight of the week - 100-200 words]

    ## 📚 Worth Reading
    • [Link 1] - Why this matters: [1 sentence]
    • [Link 2] - Why this matters: [1 sentence]
    • [Link 3] - Why this matters: [1 sentence]

    ## 💡 Quick Tip
    [Actionable tip they can use today]

    ## 🎤 Quote of the Week
    "[Inspiring quote]" - [Author]

    That's it for this week!

    [Sign off]
  `,

  deep_dive: `
    Subject: [Intriguing subject line]

    {first_name},

    [Hook - bold statement or question]

    [Story or context - 2-3 paragraphs]

    **Here's what I learned:**

    [Main lesson 1]
    [Main lesson 2]
    [Main lesson 3]

    **The takeaway:**
    [Actionable conclusion]

    What do you think? Hit reply and let me know.

    [Sign off]
  `,

  product_update: `
    Subject: [Product] Update: [Exciting feature/news]

    Hey {first_name}!

    Quick update for you today...

    **What's New:**
    [Update 1]
    [Update 2]

    **Why It Matters:**
    [How this helps them]

    **Get Started:**
    [CTA Button]

    Questions? Just reply to this email.

    [Sign off]
  `
};
```
