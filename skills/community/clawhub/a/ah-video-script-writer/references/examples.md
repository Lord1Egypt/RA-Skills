# Video Script Writer — Code Examples

## Example 1

```typescript
// The Hook Formula - First 30 seconds
interface HookSection {
  pattern: HookPattern;
  script: string;
  duration: number; // seconds
  visualDirection: string;
  goalMetric: 'retention' | 'curiosity' | 'emotion';
}

type HookPattern =
  | 'problem-agitation' // Present a relatable problem
  | 'curiosity-gap'     // Tease information they'll learn
  | 'bold-statement'    // Make a controversial claim
  | 'story-opening'     // Begin with a narrative
  | 'question'          // Ask a compelling question
  | 'statistic'         // Lead with shocking data
  | 'before-after'      // Show transformation
  | 'cold-open'         // Start mid-action;

// Hook templates by video type
const HOOK_TEMPLATES = {
  educational: {
    curiosityGap: "Most people don't know this about [TOPIC], but it could change everything...",
    problemAgitation: "You're probably making this mistake right now, and it's costing you [CONSEQUENCE]...",
    boldStatement: "Everything you've been told about [TOPIC] is wrong. Here's the truth..."
  },
  entertainment: {
    storyOpening: "So there I was, [SITUATION], when suddenly...",
    coldOpen: "[DRAMATIC SCENE] Two weeks earlier...",
    question: "What would you do if [IMPOSSIBLE SCENARIO]?"
  },
  tutorial: {
    promiseValue: "In the next [TIME], you'll learn exactly how to [OUTCOME]...",
    beforeAfter: "This simple change took me from [BEFORE] to [AFTER]...",
    commonMistake: "Stop doing [WRONG THING]. Here's what works instead..."
  }
};

// Retention curve optimization
const RETENTION_STRATEGIES = {
  first30Seconds: 'Maximum intrigue, no filler',
  everyMinute: 'Re-engage with new hook or payoff',
  midRoll: 'Place ads at natural break points',
  endScreen: 'Tease next video or playlist'
};
```

## Example 2

```typescript
// Main content sections
interface BodySection {
  sectionNumber: number;
  title: string;
  script: string;
  keyPoints: string[];
  duration: number;
  visualNotes: string[];
  transitions: TransitionNote;
  engagementPrompts?: EngagementPrompt[];
}

// Content organization patterns
const CONTENT_STRUCTURES = {
  listicle: {
    pattern: 'Number-based sections',
    example: '5 Ways to...', '10 Mistakes to Avoid...',
    tips: 'Tease the best for last'
  },
  problemSolution: {
    pattern: 'Problem → Agitation → Solution',
    phases: ['Identify pain', 'Amplify urgency', 'Present solution']
  },
  storytelling: {
    pattern: 'Setup → Conflict → Resolution',
    elements: ['Character', 'Stakes', 'Journey', 'Transformation']
  },
  tutorial: {
    pattern: 'What → Why → How → Practice',
    phases: ['Explain concept', 'Show importance', 'Demonstrate', 'Apply']
  },
  comparison: {
    pattern: 'A vs B analysis',
    elements: ['Criteria', 'Evaluation', 'Verdict']
  },
  documentary: {
    pattern: 'Acts with rising tension',
    structure: ['Exposition', 'Rising Action', 'Climax', 'Resolution']
  }
};

// Engagement prompts throughout video
interface EngagementPrompt {
  timestamp: number;
  type: 'question' | 'poll' | 'comment-prompt' | 'like-reminder' | 'subscribe';
  script: string;
  visualCue: string;
}
```

## Example 3

```typescript
// YouTube Long-Form (8-15 minutes)
const YOUTUBE_TEMPLATE = {
  hook: { duration: 30, purpose: 'Stop the scroll' },
  intro: { duration: 60, purpose: 'Set expectations' },
  content: {
    sections: 3-5,
    sectionDuration: 120-180,
    format: 'Problem → Solution pattern'
  },
  midRollBreaks: [240, 480], // Seconds
  conclusion: { duration: 60, purpose: 'Summarize and tease' },
  cta: { duration: 30, purpose: 'Subscribe, comment, next video' }
};

// Documentary (20-60 minutes)
const DOCUMENTARY_TEMPLATE = {
  coldOpen: { duration: 120, purpose: 'Immediate immersion' },
  titleSequence: { duration: 30 },
  act1: { duration: '25%', purpose: 'Establish world and stakes' },
  act2: { duration: '50%', purpose: 'Rising tension and revelations' },
  act3: { duration: '25%', purpose: 'Resolution and reflection' },
  interviews: 'Intercut with narration and B-roll'
};

// Course Module (5-10 minutes)
const COURSE_TEMPLATE = {
  learningObjective: { duration: 30, purpose: 'What they will learn' },
  conceptExplanation: { duration: 180, purpose: 'Teach the theory' },
  demonstration: { duration: 180, purpose: 'Show it in action' },
  practice: { duration: 120, purpose: 'Guided exercise' },
  summary: { duration: 60, purpose: 'Key takeaways' },
  quiz: 'Optional end-of-module assessment'
};

// Advertisement (15-60 seconds)
const AD_TEMPLATE = {
  hook: { duration: 3, purpose: 'Attention grab' },
  problem: { duration: 10, purpose: 'Identify pain point' },
  solution: { duration: 15, purpose: 'Introduce product' },
  proof: { duration: 10, purpose: 'Social proof/testimonial' },
  cta: { duration: 5, purpose: 'Clear action step' },
  offer: { duration: 5, purpose: 'Special deal/urgency' }
};
```
