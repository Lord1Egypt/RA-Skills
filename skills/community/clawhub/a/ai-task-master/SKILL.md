---
name: task-planner
description: Intelligent task planner using Plan-and-Solve pattern for breaking down goals into actionable steps with timeline and priorities.
---

# Task Planner

AI-powered task planning assistant that breaks down complex goals into manageable action items.

---

## Features

- **Goal Breakdown**: Split big goals into small tasks
- **Timeline Planning**: Realistic scheduling
- **Priority Assignment**: Eisenhower matrix
- **Progress Tracking**: Monitor completion

---

## Usage

```javascript
const planner = new TaskPlanner();
const plan = await planner.createPlan({
  goal: '完成网站重构',
  deadline: '2026-05-01',
  teamSize: 3
});
```

---

## Installation

```bash
clawhub install task-planner
```

---

## License

MIT

---

## Version

1.0.0

---

## Created

2026-04-02
