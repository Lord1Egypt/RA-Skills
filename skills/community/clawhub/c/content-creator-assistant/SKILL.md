---
name: content-creator-assistant
description: AI writing assistant using Reflection + Tree of Thoughts for high-quality content creation. Generates articles, blogs, and documentation with iterative refinement.
---

# Content Creator Assistant

AI-powered writing assistant that combines creative exploration (Tree of Thoughts) with iterative refinement (Reflection) to produce high-quality content.

---

## Features

### ✨ Creative Ideation

- **Multi-path Exploration**: Generate multiple content angles
- **Angle Selection**: Choose the best approach based on audience and goals
- **Outline Generation**: Structured content planning

### 📝 Iterative Refinement

- **Self-Reflection**: Identify weaknesses in drafts
- **Quality Improvement**: Iterative enhancement cycles
- **Style Consistency**: Maintain tone and voice

### 🎯 Content Types

- Blog posts
- Technical articles
- Documentation
- Marketing copy
- Social media content

---

## Usage

### Basic Writing

```javascript
const writer = new ContentCreatorAssistant();

const article = await writer.write({
  topic: 'The Future of AI in Healthcare',
  type: 'blog-post',
  audience: 'general public',
  length: 'medium'  // short, medium, long
});

console.log(article.content);
```

### Advanced Options

```javascript
const writer = new ContentCreatorAssistant({
  style: 'professional',
  tone: 'informative',
  iterations: 3,  // Reflection cycles
  branches: 4,    // ToT exploration paths
  verbose: true
});

const article = await writer.write({
  topic: 'Microservices Architecture',
  type: 'technical-article',
  audience: 'developers',
  keyPoints: ['scalability', 'maintainability', 'trade-offs'],
  wordCount: 2000
});
```

---

## Workflow

```
1. Tree of Thoughts (Creative Phase)
   ├─ Generate 4 content angles
   ├─ Evaluate each angle
   └─ Select best approach

2. Outline Generation
   ├─ Create structured outline
   └─ Validate flow

3. Draft Writing
   └─ Write initial draft

4. Reflection (Refinement Phase)
   ├─ Evaluate draft quality
   ├─ Identify improvements
   ├─ Revise content
   └─ Repeat (3 iterations)

5. Final Polish
   ├─ Grammar check
   ├─ Style consistency
   └─ Format output
```

---

## Example Output

```markdown
# The Future of AI in Healthcare

## Introduction
Artificial Intelligence is revolutionizing healthcare, from diagnosis to treatment planning...

## Current Applications

### Diagnostic Imaging
AI-powered image analysis can detect diseases earlier and more accurately...

### Personalized Medicine
Machine learning algorithms analyze patient data to recommend tailored treatments...

## Future Outlook

By 2030, we expect to see...

## Conclusion
AI in healthcare is not just a trend—it's a transformation that will...
```

---

## Architecture

```
User Request
    ↓
Tree of Thoughts Agent
    ├─ Angle 1: Technical deep-dive
    ├─ Angle 2: Case studies
    ├─ Angle 3: Future predictions
    └─ Angle 4: Practical guide
    ↓
Best Angle Selection
    ↓
Outline Generation
    ↓
Draft Writing
    ↓
Reflection Agent (3 iterations)
    ├─ Iteration 1: Structure & flow
    ├─ Iteration 2: Content quality
    └─ Iteration 3: Style & polish
    ↓
Final Content
```

---

## Installation

```bash
clawhub install content-creator-assistant
```

---

## License

MIT

---

## Author

AI-Agent

---

## Version

1.0.0

---

## Created

2026-04-02
