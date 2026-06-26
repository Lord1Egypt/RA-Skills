# Thumbnail Designer — Code Examples

## Example 1

```typescript
// CTR optimization principles
interface ThumbnailPsychology {
  attention: AttentionTriggers;
  emotion: EmotionalHooks;
  curiosity: CuriosityGaps;
  clarity: VisualClarity;
}

// Attention-grabbing elements
const ATTENTION_TRIGGERS = {
  faces: {
    importance: 'critical',
    expression: 'exaggerated emotions work best',
    eyeContact: 'direct eye contact increases engagement',
    size: 'face should take 40-60% of frame'
  },
  contrast: {
    colorContrast: 'complementary colors pop',
    lightContrast: 'bright subjects on dark backgrounds',
    sizeContrast: 'varying element sizes create hierarchy'
  },
  movement: {
    arrows: 'guide eye direction',
    lines: 'leading lines to focal point',
    dynamicPoses: 'action shots over static'
  },
  text: {
    maxWords: 3-5,
    fontSize: 'readable at small sizes',
    contrast: 'high contrast with background'
  }
};

// Emotional triggers by content type
const EMOTIONAL_TRIGGERS = {
  curiosity: ['?', 'hidden', 'secret', 'reveal', 'shocking'],
  urgency: ['now', 'today', 'limited', 'before/after'],
  fear: ['mistake', 'wrong', 'never', 'avoid', 'warning'],
  desire: ['how to', 'easy', 'fast', 'free', 'best'],
  surprise: ['!', unexpected results, transformations]
};
```

## Example 2

```typescript
// Thumbnail specifications
interface ThumbnailSpecs {
  dimensions: { width: 1280, height: 720 };
  aspectRatio: '16:9';
  fileFormats: ['jpg', 'png'];
  maxFileSize: '2MB';
  minWidth: 640;
}

// Design composition
interface ThumbnailComposition {
  layout: LayoutType;
  focalPoint: FocalPoint;
  textPlacement: TextPlacement;
  colorScheme: ColorScheme;
  brandElements: BrandElements;
}

type LayoutType =
  | 'face-left-text-right'
  | 'face-right-text-left'
  | 'centered-face'
  | 'before-after'
  | 'number-focus'
  | 'product-showcase'
  | 'comparison'
  | 'reaction';

// High-performing layouts by niche
const NICHE_LAYOUTS = {
  tutorial: {
    layout: 'face-left-text-right',
    elements: ['face with expression', 'key benefit text', 'relevant icon'],
    colors: 'bright, clean, professional'
  },
  entertainment: {
    layout: 'reaction',
    elements: ['exaggerated face', 'minimal text', 'context clue'],
    colors: 'bold, saturated, contrasting'
  },
  business: {
    layout: 'centered-face',
    elements: ['professional photo', 'clean text', 'subtle branding'],
    colors: 'professional, muted, trustworthy'
  },
  transformation: {
    layout: 'before-after',
    elements: ['clear comparison', 'arrow or divide', 'result highlight'],
    colors: 'contrast between states'
  },
  listicle: {
    layout: 'number-focus',
    elements: ['large number', 'visual examples', 'curiosity text'],
    colors: 'number in contrasting color'
  }
};
```

## Example 3

```typescript
// Text design principles
interface TextOverlay {
  headline: HeadlineText;
  subtext?: SubText;
  styling: TextStyling;
}

interface HeadlineText {
  text: string;
  maxWords: 5;
  fontSize: 'large'; // Readable at 100px width
  position: TextPosition;
  style: TextStyle;
}

interface TextStyling {
  font: string;
  weight: 'bold' | 'extra-bold' | 'black';
  outline: OutlineConfig;
  shadow: ShadowConfig;
  background?: BackgroundConfig;
}

// Font recommendations by style
const FONT_RECOMMENDATIONS = {
  impact: ['Impact', 'Anton', 'Bebas Neue'], // High energy
  modern: ['Montserrat', 'Poppins', 'Nunito'], // Clean, professional
  playful: ['Fredoka One', 'Bubblegum Sans', 'Comic Neue'], // Fun content
  elegant: ['Playfair Display', 'Lora', 'Cormorant'], // Sophisticated
  tech: ['Roboto', 'Inter', 'Source Sans Pro'] // Tech/tutorial
};

// Text visibility techniques
const TEXT_VISIBILITY = {
  outline: {
    width: '4-8px',
    color: 'contrasting to text',
    effect: 'ensures readability on any background'
  },
  shadow: {
    offset: '2-4px',
    blur: '4-8px',
    color: 'rgba(0,0,0,0.5)',
    effect: 'adds depth and separation'
  },
  background: {
    type: 'solid or gradient',
    opacity: '60-80%',
    shape: 'rectangle or pill',
    effect: 'guaranteed contrast'
  }
};
```

## Example 4

```typescript
// Color psychology for thumbnails
interface ColorStrategy {
  primary: string;
  secondary: string;
  accent: string;
  text: string;
  psychology: ColorPsychology;
}

const COLOR_PSYCHOLOGY = {
  red: {
    emotion: 'urgency, excitement, passion',
    use: 'CTAs, warnings, high-energy content',
    pairs: ['white', 'yellow', 'black']
  },
  yellow: {
    emotion: 'optimism, attention, energy',
    use: 'highlights, backgrounds, positivity',
    pairs: ['black', 'purple', 'blue']
  },
  blue: {
    emotion: 'trust, calm, professionalism',
    use: 'tech, business, educational',
    pairs: ['orange', 'white', 'yellow']
  },
  green: {
    emotion: 'growth, money, health',
    use: 'finance, wellness, success',
    pairs: ['white', 'yellow', 'purple']
  },
  purple: {
    emotion: 'luxury, creativity, mystery',
    use: 'premium content, entertainment',
    pairs: ['yellow', 'gold', 'white']
  },
  orange: {
    emotion: 'enthusiasm, action, fun',
    use: 'entertainment, sports, energy',
    pairs: ['blue', 'white', 'black']
  }
};

// High-CTR color combinations
const PROVEN_COMBINATIONS = [
  { primary: 'yellow', secondary: 'black', accent: 'red' },
  { primary: 'red', secondary: 'white', accent: 'yellow' },
  { primary: 'blue', secondary: 'orange', accent: 'white' },
  { primary: 'green', secondary: 'white', accent: 'yellow' },
  { primary: 'purple', secondary: 'yellow', accent: 'white' }
];
```

## Example 5

```typescript
// Thumbnail templates by content type
interface ThumbnailTemplate {
  name: string;
  category: ContentCategory;
  structure: TemplateStructure;
  customizableElements: string[];
  exampleTitles: string[];
}

const TEMPLATE_LIBRARY = {
  howTo: {
    layout: 'face-left-text-right',
    elements: [
      { type: 'face', position: 'left-40%', expression: 'confident/helpful' },
      { type: 'text', position: 'right', content: 'How To [X]' },
      { type: 'icon', position: 'accent', relevant: true }
    ],
    colors: ['clean', 'professional', 'trustworthy']
  },

  reaction: {
    layout: 'face-centered',
    elements: [
      { type: 'face', position: 'center', expression: 'shocked/surprised' },
      { type: 'text', position: 'top-or-bottom', content: 'minimal' },
      { type: 'context', position: 'corner', hints: 'what video is about' }
    ],
    colors: ['bold', 'saturated', 'attention-grabbing']
  },

  listicle: {
    layout: 'number-prominent',
    elements: [
      { type: 'number', position: 'left', size: 'large', style: 'bold' },
      { type: 'text', position: 'right', content: 'what the list is about' },
      { type: 'examples', position: 'background', count: '2-3 visual hints' }
    ],
    colors: ['number contrasts heavily', 'clean background']
  },

  comparison: {
    layout: 'split-screen',
    elements: [
      { type: 'option-a', position: 'left', label: 'clear' },
      { type: 'option-b', position: 'right', label: 'clear' },
      { type: 'vs', position: 'center', style: 'prominent' },
      { type: 'face', position: 'optional', expression: 'curious' }
    ],
    colors: ['contrasting sides', 'neutral divider']
  },

  transformation: {
    layout: 'before-after',
    elements: [
      { type: 'before', position: 'left', label: 'BEFORE' },
      { type: 'after', position: 'right', label: 'AFTER' },
      { type: 'arrow', position: 'center', direction: 'right' }
    ],
    colors: ['before: muted', 'after: vibrant']
  }
};
```

## Example 6

```typescript
// Prompts for AI image generation
interface ThumbnailPrompt {
  subject: string;
  style: string;
  composition: string;
  lighting: string;
  mood: string;
  negative: string[];
}

// Prompt templates
const PROMPT_TEMPLATES = {
  professional: `
    Professional YouTube thumbnail, {subject},
    high-key lighting, clean background,
    rule of thirds composition,
    4K quality, sharp focus,
    vibrant colors, commercial photography style
  `,

  dramatic: `
    Dramatic YouTube thumbnail, {subject},
    cinematic lighting, dark moody background,
    high contrast, intense colors,
    epic composition, movie poster style
  `,

  friendly: `
    Friendly YouTube thumbnail, {subject},
    warm natural lighting, bright background,
    welcoming expression, soft colors,
    lifestyle photography, approachable vibe
  `,

  energetic: `
    High-energy YouTube thumbnail, {subject},
    dynamic pose, bold saturated colors,
    action shot, motion blur effects,
    extreme close-up, impactful composition
  `
};

// Negative prompts (what to avoid)
const NEGATIVE_PROMPTS = [
  'blurry', 'low quality', 'pixelated',
  'text', 'watermark', 'logo',
  'busy background', 'cluttered',
  'bad lighting', 'overexposed', 'underexposed',
  'distorted face', 'weird proportions'
];
```
