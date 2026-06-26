# Course Creator — Code Examples

## Example 1

```typescript
// Complete course structure
interface CourseArchitecture {
  metadata: CourseMetadata;
  curriculum: Curriculum;
  content: CourseContent;
  assessments: AssessmentStrategy;
  delivery: DeliveryMethod;
}

interface CourseMetadata {
  title: string;
  subtitle: string;
  description: string;
  targetAudience: AudienceProfile;
  learningOutcomes: string[];
  prerequisites: string[];
  duration: CourseDuration;
  level: 'beginner' | 'intermediate' | 'advanced';
  category: string;
  tags: string[];
}

interface Curriculum {
  modules: Module[];
  totalDuration: number;
  structure: CurriculumStructure;
  progression: LearningProgression;
}

// Course structure patterns
const CURRICULUM_PATTERNS = {
  linear: {
    description: "Sequential progression through modules",
    bestFor: "Skill building, technical topics",
    structure: "Module 1 → Module 2 → Module 3..."
  },
  modular: {
    description: "Independent modules, flexible order",
    bestFor: "Reference courses, diverse topics",
    structure: "Choose your own path"
  },
  spiral: {
    description: "Return to concepts with increasing depth",
    bestFor: "Complex topics, mastery learning",
    structure: "Intro → Basics → Apply → Advanced → Master"
  },
  projectBased: {
    description: "Learn by building something real",
    bestFor: "Practical skills, creative topics",
    structure: "Project phases with supporting lessons"
  }
};
```

## Example 2

```typescript
// Instructional design principles
interface LearningDesign {
  objectives: LearningObjective[];
  activities: LearningActivity[];
  assessments: Assessment[];
  engagement: EngagementStrategy;
}

// Bloom's Taxonomy for objectives
const BLOOMS_TAXONOMY = {
  remember: {
    verbs: ["define", "list", "recall", "identify", "recognize"],
    activities: ["flashcards", "quizzes", "matching"],
    assessment: "Multiple choice, fill in blank"
  },
  understand: {
    verbs: ["explain", "describe", "summarize", "interpret"],
    activities: ["discussions", "summaries", "examples"],
    assessment: "Short answer, explanations"
  },
  apply: {
    verbs: ["use", "implement", "execute", "demonstrate"],
    activities: ["exercises", "practice problems", "simulations"],
    assessment: "Practical exercises, demonstrations"
  },
  analyze: {
    verbs: ["compare", "contrast", "differentiate", "examine"],
    activities: ["case studies", "research", "breakdowns"],
    assessment: "Analysis papers, comparisons"
  },
  evaluate: {
    verbs: ["judge", "critique", "assess", "justify"],
    activities: ["peer review", "debates", "evaluations"],
    assessment: "Rubric-based evaluation, critiques"
  },
  create: {
    verbs: ["design", "construct", "produce", "develop"],
    activities: ["projects", "portfolios", "original work"],
    assessment: "Project submissions, portfolios"
  }
};

// Learning objective template
const OBJECTIVE_TEMPLATE =
  "By the end of this [lesson/module], you will be able to [action verb] [specific skill/knowledge] [condition/context]";
```

## Example 3

```typescript
// Module template
interface Module {
  number: number;
  title: string;
  description: string;
  objectives: string[];
  lessons: Lesson[];
  resources: Resource[];
  assessment?: Assessment;
  duration: number;
}

interface Lesson {
  number: number;
  title: string;
  type: LessonType;
  content: LessonContent;
  duration: number;
  materials: Material[];
}

type LessonType =
  | 'video' | 'reading' | 'interactive'
  | 'exercise' | 'quiz' | 'project'
  | 'discussion' | 'live-session';

// Lesson structure template
const LESSON_STRUCTURE = {
  video: {
    intro: { duration: "1-2 min", purpose: "Hook and preview" },
    content: { duration: "5-15 min", purpose: "Core teaching" },
    summary: { duration: "1-2 min", purpose: "Recap key points" },
    action: { duration: "1 min", purpose: "What to do next" }
  },
  exercise: {
    intro: { purpose: "Explain the exercise" },
    demonstration: { purpose: "Show example" },
    practice: { purpose: "Student does it" },
    review: { purpose: "Check understanding" }
  }
};

// Optimal lesson duration by format
const LESSON_DURATION = {
  conceptVideo: "5-10 minutes",
  tutorialVideo: "10-20 minutes",
  reading: "10-15 minutes read time",
  exercise: "15-30 minutes",
  project: "1-3 hours",
  quiz: "5-15 minutes"
};
```

## Example 4

```typescript
// Video lesson script structure
interface VideoScript {
  metadata: ScriptMetadata;
  hook: string;
  intro: string;
  sections: ContentSection[];
  summary: string;
  callToAction: string;
  bRoll: BRollNote[];
}

// Educational video script template
const VIDEO_SCRIPT_TEMPLATE = `
# [Lesson Title]

## HOOK (0:00 - 0:30)
[Attention-grabbing opening that creates curiosity]

"Have you ever wondered [question]?"
or
"By the end of this lesson, you'll be able to [outcome]"

## INTRO (0:30 - 1:30)
- What you'll learn
- Why it matters
- What you need to follow along

## CONTENT SECTION 1 (1:30 - 5:00)
### [Section Title]
[Main teaching content]

Key Point 1:
- Explanation
- Example
- Practice prompt

[B-ROLL: Show example/demonstration]

## CONTENT SECTION 2 (5:00 - 8:30)
### [Section Title]
[Continue teaching]

[SCREEN RECORDING: Demonstrate the process]

## CONTENT SECTION 3 (8:30 - 11:00)
### [Section Title]
[Advanced application or common mistakes]

## SUMMARY (11:00 - 12:00)
"Let's recap what you learned:
1. [Key point 1]
2. [Key point 2]
3. [Key point 3]"

## CALL TO ACTION (12:00 - 12:30)
- Complete the exercise below
- Move to the next lesson
- Share your progress
`;

// Teaching techniques
const TEACHING_TECHNIQUES = {
  chunking: "Break complex topics into digestible pieces",
  scaffolding: "Build from simple to complex",
  modeling: "Demonstrate before asking them to do",
  interleaving: "Mix topics for better retention",
  spaced_repetition: "Return to concepts over time",
  active_recall: "Ask questions, don't just tell"
};
```

## Example 5

```typescript
// Assessment types
interface AssessmentStrategy {
  formative: FormativeAssessment[];
  summative: SummativeAssessment[];
  rubrics: Rubric[];
}

const ASSESSMENT_TYPES = {
  formative: {
    purpose: "Check understanding during learning",
    types: [
      "In-video quizzes",
      "Practice exercises",
      "Reflection prompts",
      "Discussion posts",
      "Self-assessments"
    ],
    grading: "Usually ungraded or low-stakes"
  },
  summative: {
    purpose: "Evaluate learning at end of unit/course",
    types: [
      "Module quizzes",
      "Projects",
      "Final exams",
      "Portfolio submissions",
      "Peer-reviewed assignments"
    ],
    grading: "Graded toward completion/certification"
  }
};

// Quiz question types
const QUESTION_TYPES = {
  multipleChoice: {
    bestFor: "Testing recall and basic understanding",
    tips: "4-5 options, one clearly correct, plausible distractors"
  },
  trueFalse: {
    bestFor: "Quick knowledge checks",
    tips: "Avoid double negatives, test one concept"
  },
  fillInBlank: {
    bestFor: "Testing specific terminology",
    tips: "Clear context, accept synonyms"
  },
  matching: {
    bestFor: "Testing relationships between concepts",
    tips: "More options than items to match"
  },
  shortAnswer: {
    bestFor: "Testing application and understanding",
    tips: "Clear rubric, example answer"
  },
  project: {
    bestFor: "Testing real-world application",
    tips: "Clear requirements, detailed rubric"
  }
};
```

## Example 6

```typescript
// Course platform specs
interface PlatformOptimization {
  platform: CoursePlatform;
  requirements: PlatformRequirements;
  features: PlatformFeatures;
}

const PLATFORM_SPECS = {
  udemy: {
    minDuration: 30, // minutes
    videoFormat: "MP4, 1080p minimum",
    pricing: "$19.99 - $199.99",
    features: ["quizzes", "assignments", "discussions", "certificates"],
    discoverability: "Marketplace, search, promotions"
  },
  teachable: {
    videoFormat: "Any common format",
    pricing: "You set the price",
    features: ["drip content", "quizzes", "coaching", "bundles"],
    customization: "Full branding control"
  },
  thinkific: {
    videoFormat: "MP4, MOV, AVI",
    pricing: "You set the price",
    features: ["communities", "certificates", "memberships"],
    integrations: "Zapier, email marketing"
  },
  kajabi: {
    videoFormat: "Upload or link",
    pricing: "You set the price",
    features: ["all-in-one", "funnels", "email", "community"],
    marketing: "Built-in sales tools"
  },
  skillshare: {
    minDuration: 10, // minutes
    videoFormat: "MP4, 720p minimum",
    pricing: "Revenue share based on watch time",
    features: ["projects", "discussions"],
    discoverability: "Platform marketplace"
  }
};
```

## Example 7

```typescript
// Course launch plan
interface LaunchStrategy {
  prelaunch: PrelaunchPhase;
  launch: LaunchPhase;
  postlaunch: PostlaunchPhase;
}

const LAUNCH_PHASES = {
  prelaunch: {
    timeline: "4-8 weeks before",
    activities: [
      "Build email list with lead magnet",
      "Create anticipation content",
      "Beta testers for feedback",
      "Testimonial collection",
      "Affiliate/partner outreach"
    ]
  },
  launch: {
    timeline: "1-2 weeks",
    activities: [
      "Email sequence (5-7 emails)",
      "Live webinar/workshop",
      "Early bird pricing",
      "Bonus incentives",
      "Social proof showcase"
    ]
  },
  postlaunch: {
    timeline: "Ongoing",
    activities: [
      "Evergreen funnel",
      "Student success stories",
      "Content updates",
      "Upsells and cross-sells",
      "Community building"
    ]
  }
};

// Pricing strategies
const PRICING_STRATEGIES = {
  valueBasedPricing: "Price based on transformation value",
  marketComparison: "Research competitor pricing",
  tieredPricing: "Basic, Pro, Premium options",
  paymentPlans: "Make high-ticket accessible",
  earlyBird: "Reward early action"
};
```
