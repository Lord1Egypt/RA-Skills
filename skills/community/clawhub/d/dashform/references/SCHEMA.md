# Form Schema Reference

Complete reference for Dashform form structure and configuration.

## MCP Integration Note

This schema reference describes the data structures used in Dashform forms. When using the Dashform MCP tools:

- **`create_form` tool**: Now supports the FULL schema including questions, screens, theme, branding, and backgrounds
- **Complete form creation**: You can create fully configured forms via MCP without needing the web builder
- **Structured forms**: Specify complete question lists when creating structured forms
- **Dynamic forms**: Configure snippets and maxFollowUpQuestions for AI-powered forms

For MCP tool parameters and examples, see [API.md](./API.md).

## Form Structure

```typescript
{
  name: string;                    // Form name (1-255 chars)
  description?: string | null;     // Form description
  type: "structured" | "dynamic";  // Form type
  tone?: string | null;            // e.g., "friendly", "professional"
  
  welcomeScreen?: WelcomeScreen | null;
  endScreen?: EndScreen | null;
  endScreenEnabled?: boolean;
  endings?: Ending[];              // For quizzes with multiple results
  
  questions?: Question[] | null;
  snippets?: string[] | null;      // Context for AI to reference
  maxFollowUpQuestions?: number;   // For dynamic forms (0-10)
  
  theme?: Theme | null;
  branding?: Branding | null;
  backgrounds?: Background[];      // Cycling backgrounds (max 10)
}
```

## Form Types

### structured
Traditional form with fixed questions in a predefined order.

```json
{
  "type": "structured",
  "questions": [...]
}
```

### dynamic
AI-powered conversational form that adapts based on responses.

```json
{
  "type": "dynamic",
  "maxFollowUpQuestions": 3,
  "snippets": ["Company info", "Product details"]
}
```

## Question Types

### open-ended
Free-text input for detailed responses.

```json
{
  "key": "feedback",
  "type": "open-ended",
  "description": "What do you think about our service?",
  "required": true
}
```

### single-choice
Radio button selection (one option).

```json
{
  "key": "satisfaction",
  "type": "single-choice",
  "description": "How satisfied are you?",
  "required": true,
  "options": ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied"]
}
```

### multiple-choice
Checkbox selection (multiple options).

```json
{
  "key": "features",
  "type": "multiple-choice",
  "description": "Which features do you use?",
  "required": false,
  "options": ["Dashboard", "Reports", "Integrations", "API"]
}
```

### rating
Star rating from 1-5.

```json
{
  "key": "overall_rating",
  "type": "rating",
  "description": "Rate your overall experience",
  "required": true
}
```

## Welcome Screen

```json
{
  "title": "Customer Feedback Survey",
  "message": "Help us improve by sharing your thoughts",
  "callToActionText": "Start Survey",
  "background": {
    "type": "color",
    "colorValue": "#f0f0f0"
  }
}
```

## End Screen

```json
{
  "title": "Thank You!",
  "message": "Your feedback has been submitted successfully.",
  "callToActionText": "Visit Our Website",
  "callToActionUrl": "https://example.com",
  "background": null
}
```

## Quiz Endings

For personality quizzes or assessments with multiple result types.

```json
{
  "endings": [
    {
      "id": "outcome_expert",
      "title": "The Expert",
      "description": "Matches users who demonstrate deep knowledge and experience",
      "message": "You're an expert! Your knowledge is impressive.",
      "imageUrl": "https://example.com/expert.jpg",
      "callToActionText": "Learn More",
      "callToActionUrl": "https://example.com/expert",
      "background": null
    },
    {
      "id": "outcome_beginner",
      "title": "The Beginner",
      "description": "Matches users who are just starting their journey",
      "message": "You're just getting started, and that's great!",
      "imageUrl": null,
      "callToActionText": null,
      "callToActionUrl": null,
      "background": null
    }
  ]
}
```

## Theme

Customize colors and fonts.

```json
{
  "theme": {
    "colorBackground": "#faf9f5",
    "colorForeground": "#3d3929",
    "colorPrimary": "#c96442",
    "fontFamily": "sans"
  }
}
```

**Font options:** `"sans"`, `"serif"`, `"mono"`

## Branding

```json
{
  "branding": {
    "hideWatermark": false,
    "logoUrl": "https://example.com/logo.png"
  }
}
```

## Backgrounds

Forms support various background types that can cycle through questions.

### Color Background

```json
{
  "type": "color",
  "colorValue": "#ffffff"
}
```

### Gradient Background

```json
{
  "type": "gradient",
  "gradient": {
    "type": "linear",
    "colors": ["#667eea", "#764ba2"],
    "angle": 45
  }
}
```

### Image Background

```json
{
  "type": "image",
  "url": "https://images.pexels.com/photos/123/photo.jpg",
  "source": "pexels",
  "pexelsId": "123",
  "pexelsPhotographer": "John Doe",
  "pexelsPhotographerUrl": "https://pexels.com/@johndoe",
  "display": {
    "position": "center",
    "size": "cover"
  },
  "overlay": {
    "opacity": 30,
    "type": "solid",
    "color": "#000000"
  },
  "effects": {
    "blur": 0,
    "brightness": 100,
    "contrast": 100,
    "saturate": 100
  }
}
```

### Video Background

```json
{
  "type": "video",
  "url": "https://videos.pexels.com/video-files/123/video.mp4",
  "source": "pexels",
  "display": {
    "position": "center",
    "size": "cover"
  },
  "overlay": {
    "opacity": 50,
    "type": "solid"
  }
}
```

## Branching Logic

Questions can have conditional branching based on previous answers.

```json
{
  "key": "follow_up",
  "type": "open-ended",
  "description": "What could we improve?",
  "required": false,
  "branches": [
    {
      "targetQuestionKey": "positive_feedback",
      "groups": [
        [
          {
            "questionKey": "satisfaction",
            "operator": "equals",
            "negate": false,
            "value": "Very satisfied"
          }
        ]
      ]
    }
  ]
}
```

### Branch Operators

- `equals` - Exact match
- `contains` - Substring match
- `startsWith` - Prefix match
- `endsWith` - Suffix match
- `regex` - Regular expression match
- `exists` - Check if answered (no value needed)

### Branch Logic (DNF)

Branches use Disjunctive Normal Form (DNF):
- **groups** = OR (any group matches)
- **conditions within group** = AND (all conditions must match)

## Complete Example: Customer Survey

```json
{
  "name": "Customer Satisfaction Survey",
  "description": "Collect feedback from customers",
  "type": "structured",
  "tone": "friendly",
  
  "welcomeScreen": {
    "title": "We Value Your Feedback",
    "message": "This survey takes about 2 minutes",
    "callToActionText": "Begin",
    "background": {
      "type": "color",
      "colorValue": "#f0f9ff"
    }
  },
  
  "questions": [
    {
      "key": "satisfaction",
      "type": "single-choice",
      "description": "How satisfied are you with our product?",
      "required": true,
      "options": ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very dissatisfied"]
    },
    {
      "key": "recommend",
      "type": "rating",
      "description": "How likely are you to recommend us?",
      "required": true
    },
    {
      "key": "feedback",
      "type": "open-ended",
      "description": "Any additional comments?",
      "required": false
    }
  ],
  
  "endScreen": {
    "title": "Thank You!",
    "message": "Your feedback helps us improve.",
    "callToActionText": null,
    "callToActionUrl": null
  },
  
  "theme": {
    "colorBackground": "#ffffff",
    "colorForeground": "#1a1a1a",
    "colorPrimary": "#0066cc",
    "fontFamily": "sans"
  }
}
```

## Complete Example: Personality Quiz

```json
{
  "name": "Work Style Quiz",
  "description": "Discover your work personality",
  "type": "dynamic",
  "tone": "fun and engaging",
  
  "welcomeScreen": {
    "title": "Discover Your Work Style",
    "message": "Answer a few questions to find out!",
    "callToActionText": "Start Quiz"
  },
  
  "questions": [
    {
      "key": "decision_making",
      "type": "single-choice",
      "description": "How do you make decisions?",
      "required": true,
      "options": ["Data-driven", "Intuition-based", "Collaborative", "Quick and decisive"]
    },
    {
      "key": "work_environment",
      "type": "single-choice",
      "description": "What's your ideal work environment?",
      "required": true,
      "options": ["Quiet and focused", "Collaborative and social", "Flexible and varied", "Structured and organized"]
    }
  ],
  
  "endings": [
    {
      "id": "analyst",
      "title": "The Analyst",
      "description": "Data-driven, methodical, prefers structure",
      "message": "You're an Analyst! You excel at breaking down complex problems.",
      "callToActionText": "Learn More",
      "callToActionUrl": "https://example.com/analyst"
    },
    {
      "id": "innovator",
      "title": "The Innovator",
      "description": "Creative, intuitive, embraces change",
      "message": "You're an Innovator! You thrive on new ideas and possibilities.",
      "callToActionText": "Learn More",
      "callToActionUrl": "https://example.com/innovator"
    }
  ]
}
```
