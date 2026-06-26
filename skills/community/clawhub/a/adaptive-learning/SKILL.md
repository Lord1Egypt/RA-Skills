---
name: adaptive-learning
description: Create adaptive learning flashcard apps from course materials (URLs, PDFs, or folders). Uses FSRS (Free Spaced Repetition Scheduler) and Bayesian Knowledge Tracing for intelligent review scheduling. Use when asked to create study materials, flashcards, review apps, spaced repetition systems, or adaptive quizzes from course content. Triggers on "make me a study app", "create flashcards for this course", "adaptive learning", "spaced repetition", "review system for [course]".
---

# Adaptive Learning Skill

Create self-contained, browser-based adaptive learning apps from any course material.

## Architecture

- **FSRS** (ts-fsrs): Per-card spaced repetition scheduling (Stability, Difficulty, Retrievability)
- **BKT**: Per-topic Bayesian Knowledge Tracing for mastery estimation
- **Two modes**: Breadth-first (cover all topics, weakest first) / Depth-first (drill one topic deep)
- **Pure frontend**: HTML + CSS + JS, works offline via `file://`, no server needed

## Workflow

### 1. Gather Course Material

From a URL:
```
1. Fetch the course page, extract topic list and resource links
2. Download HW/Discussion/Lecture PDFs to ~/COURSE_NAME/
```

From a local folder:
```
1. List files, identify PDFs and documents
2. Read/parse to understand topics and content
```

### 2. Generate Question Bank

Create `questions.json` with this schema:

```json
[{
  "id": "unique-id",
  "topic": "Topic Name",
  "topicIndex": 0,
  "difficulty": 1,
  "question": "Supports $LaTeX$ via KaTeX",
  "answer": "Supports $LaTeX$ and \\n for line breaks",
  "tags": ["tag1", "tag2"]
}]
```

Guidelines:
- 5-8 questions per topic minimum, across 3 difficulty levels
- **Difficulty 1 (基础)**: Definitions, "what is", simple complexity questions
- **Difficulty 2 (中等)**: Apply algorithms, analyze examples, describe procedures
- **Difficulty 3 (高级)**: Proofs, novel problem design, optimization, "why" questions
- Use LaTeX (`$...$` inline, `$$...$$` block) for math
- Use `\\n` for line breaks in question/answer text
- `topicIndex` controls topic ordering (0-based)

### 3. Build the App

Run the bundler script:

```bash
bash SKILL_DIR/scripts/generate-course.sh <course-id> <questions.json> <output-dir>
```

Then register the course in `engine.js` `COURSE_REGISTRY`:

```javascript
{ id: 'course-id', name: 'Course Name', desc: 'Description', school: 'School', term: 'Term' }
```

### 4. Verify

Open `<output-dir>/index.html` in a browser. Verify:
- Course appears in selector
- Cards render with KaTeX math
- Flip/rating/FSRS scheduling works
- Mode toggle (breadth/depth) works

## Framework Files (assets/framework/)

| File | Purpose |
|------|---------|
| `index.html` | Main page with course selector + learning UI |
| `style.css` | Dark theme, responsive styles |
| `engine.js` | FSRS + BKT engine, question selection, state management |
| `ts-fsrs.umd.js` | FSRS algorithm library (UMD build of ts-fsrs) |

## Key Features

- **FSRS scheduling**: Cards show Stability/Difficulty values; review intervals adapt to performance
- **BKT mastery**: Per-topic mastery percentage in progress drawer
- **Configurable**: Target retention (70-97%), daily new card limit
- **localStorage**: All progress persists across sessions
- **Keyboard shortcuts**: Space=flip, 1=Good, 2=Hard, 3=Again, f=follow-up, n=next-topic
- **KaTeX**: Full LaTeX math rendering
- **Drag & drop**: Import any questions.json directly in the UI
- **Multi-course**: One framework, multiple course data packs

## Adding to Existing Installation

To add a new course to an existing adaptive-learning setup at `~/adaptive-learning/`:

1. Save `questions.json` to `~/adaptive-learning/courses/<id>/`
2. Generate preload: `bash scripts/generate-course.sh <id> questions.json ~/adaptive-learning/framework/`
3. Add to `COURSE_REGISTRY` in `engine.js`
