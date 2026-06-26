# repo-tour

Turn any codebase into a self-contained interactive HTML course.

Point it at a repo, get back a single HTML file that teaches how the code works - with scroll-based navigation, code/plain-English side by side, architecture diagrams, data flow walkthrough, application quizzes, and glossary tooltips. No dependencies. Works offline. Host it as a landing page or share it directly.

---


## Activation and Data Boundary

Use this skill for explicit requests to create a Code Decoded course, repo tour, onboarding walkthrough, or stakeholder explanation. It should not trigger for ordinary code review, refactoring, or debugging.

The agent reads repository files and writes one self-contained HTML file. Confirm the output path before generation, avoid overwriting existing files without approval, and review the HTML before sharing because it may include real code snippets, private paths, and architecture details.

## What it generates

- **Architecture overview** - visual diagram of how the main components connect
- **Concept modules** - one concept per section, real code alongside plain-English explanation
- **Data flow walkthrough** - step-by-step trace of a key user action
- **Application quizzes** - "which file would you edit to change X?" not "what does X stand for?"
- **Glossary tooltips** - hover any technical term for a definition
- **Keyboard navigation** - arrow keys between sections

Output: a single `[repo-name]-tour.html` file, self-contained, no build step needed.

---

## Installation

### OpenClaw

Add your workspace skills directory to `openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/your/skills"]
    }
  }
}
```

Clone into that directory:

```bash
git clone https://github.com/LeoStehlik/repo-tour.git /path/to/your/skills/repo-tour
```

### Claude Code / Codex / other agents

Copy the `repo-tour` folder into your project's skills directory, then invoke with `/code-decoded` or describe your goal naturally.

---

## Usage

Invoke it explicitly with a repo-tour request:

```
Turn this codebase into an interactive course
```

```
Generate onboarding material for new developers joining this project
```

```
Explain how this repo works to a non-technical stakeholder
```

The skill will ask (or infer):
- Who is the audience?
- Which area to focus on?
- What is the most important user action to trace?

---

## What's Inside

```
repo-tour/
├── SKILL.md                           Core skill instructions
└── references/
    ├── design-principles.md           Visual rules, module structure, colour, typography
    └── html-structure.md              HTML output spec + self-contained checklist
```

---

## Design Philosophy

- Visual first: every screen at least 50% visual
- Real code only: never modify or simplify actual code snippets
- Application quizzes: test usage, not memorisation
- No AI aesthetic: clean, functional, honest

---

## Inspiration

Inspired by [codebase-to-course](https://github.com/mathiscode/codebase-to-course). Built as our own implementation with a broader audience focus and a stricter design system.

---

## License

MIT - see [LICENSE](LICENSE)
