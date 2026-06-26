# HTML Output Structure

The output is a single self-contained HTML file. All CSS and JS must be inline. No external dependencies.

## Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Repo Name] - Code Decoded</title>
  <style>/* all CSS inline here */</style>
</head>
<body>
  <nav><!-- progress bar + section nav --></nav>
  <main>
    <section id="intro"><!-- hero: what is this codebase? --></section>
    <section id="architecture"><!-- visual overview of components --></section>
    <section id="module-1"><!-- first concept --></section>
    <!-- ... more modules ... -->
    <section id="data-flow"><!-- trace a key user action --></section>
    <section id="quiz"><!-- application quiz --></section>
    <section id="summary"><!-- key takeaways + next steps --></section>
  </main>
  <div id="glossary-tooltip"><!-- hover tooltip for terms --></div>
  <script>/* all JS inline here */</script>
</body>
</html>
```

## Required Sections

### 1. Intro (hero)
- What is this codebase? (one sentence)
- Who built it and why?
- What does a user experience when using it?
- No code yet. Set the scene.

### 2. Architecture Overview
- SVG or CSS diagram showing main components and their relationships
- Labelled boxes with arrows — not a class diagram, a mental model
- 2-3 sentence explanation of the overall structure

### 3. Concept Modules (5-8 modules)
Each module:
```html
<section id="module-N" class="module">
  <div class="module-hook"><!-- one sentence: what problem does this solve? --></div>
  <div class="module-visual"><!-- diagram or animation --></div>
  <div class="code-split">
    <div class="code-real"><!-- exact code from repo --></div>
    <div class="code-plain"><!-- plain English translation --></div>
  </div>
  <div class="module-apply"><!-- practical question --></div>
</section>
```

### 4. Data Flow Walkthrough
- Pick the most important user action (login, submit a form, search, send a message)
- Show step-by-step what happens: numbered steps, each with a code highlight and one-line explanation
- Animate if possible (CSS transitions between steps)

### 5. Quiz
- 3-5 application questions
- Multiple choice, 4 options each
- Immediate feedback (green/red highlight, explanation of correct answer)
- No scoring — the goal is learning, not testing

### 6. Summary
- 5 bullet points: the most important things to remember
- "Where to look" guide: common tasks mapped to file/function names
- Optional: links to further reading (only if they are real, verified URLs)

## Navigation

```javascript
// Keyboard navigation
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') nextSection();
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') prevSection();
});

// Progress bar: update on scroll
// Section nav: highlight current section
// Smooth scroll between sections
```

## Glossary Tooltips

```javascript
// Any element with data-term="..." shows a tooltip on hover
// Tooltip content defined in a glossary object at the top of the script
const glossary = {
  "JWT": "JSON Web Token — a compact way to securely transmit information as a JSON object",
  // ... add all technical terms used in this specific codebase
};
```

## Self-Contained Checklist

Before outputting the file, verify:
- [ ] No `<link>` tags pointing to external CSS
- [ ] No `<script src="...">` pointing to external JS
- [ ] No external image URLs (use inline SVG or data URIs)
- [ ] No `fetch()` or `XMLHttpRequest` calls
- [ ] Opens and works in a browser with no internet connection
