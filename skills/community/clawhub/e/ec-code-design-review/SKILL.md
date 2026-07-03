---
name: code-design-review
description: Auto-review code and designs using Jeff Dean (architecture) and Luke W / Ryan Singer (UX) principles. Runs automatically after coding events.
---

# Code & Design Review Skill

Automatic code and design reviews using world-class principles:
- **Jeff Dean** - Architecture, scalability, maintainability
- **Luke W + Ryan Singer** - UX, jobs-to-be-done, friction removal

## Auto-Trigger Rule

**After ANY coding task, automatically run the appropriate review:**

| Task Type | Review to Run |
|-----------|---------------|
| Code changes (*.js, *.ts, *.py, etc.) | Jeff Dean Code Review |
| UI/UX changes (*.tsx, *.vue, *.css, etc.) | Both reviews |
| Design files, wireframes | Luke W / Ryan Singer Review |
| Architecture docs, system design | Jeff Dean Review |

## Jeff Dean Code Review Prompt

Use after code/architecture changes:

```
## CHANNEL JEFF "GLOBAL SCALE" DEAN

Thoroughly and thoughtfully review the following code/system:

{paste code or describe system}

Consider how following Jeff Dean's principles would improve this to make it best in class.

### Jeff Dean's Principles:

1. **Focus on Design and Architecture**
   - Evaluate overall system design
   - How does new code integrate with existing systems?
   - Does logic belong here or in a library?
   - Does it align with broader architecture?

2. **Prioritize Functionality over Style**
   - Focus on functionality, logic, maintainability
   - Let linters handle style
   - Human review = critical design aspects

3. **Learning and Collaboration**
   - Collaborative process
   - Comfortable asking questions
   - Improve code AND team understanding

4. **Encourage Discussion**
   - Diverse perspectives enhance quality

5. **Build Incrementally, Test Continuously**
   - Small, focused changes
   - Easier to review and test
   - Keeps system stable

6. **Automate Where Possible**
   - Catch common errors with tools
   - Free humans for architecture discussions

7. **Optimize for Clarity and Maintainability**
   - Code maintained by others
   - Clear, well-documented, modular
   - Small functions, easy to debug
```

## Luke W / Ryan Singer UX Review Prompt

Use after UI/UX or design changes:

```
## CHANNEL LUKE W AND RYAN SINGER

Thoroughly and thoughtfully review the following:

{paste UI code, screenshot, or describe interface}

Consider how they would audit and improve this to make it best in class.

### LukeW's UX Principles:
- **Mobile First** - Responsive design
- **Progressive Disclosure** - Hide complexity until needed
- **Obvious Next Actions** - Clear CTAs
- **Reduce Cognitive Load** - Less is more
- **Visual Hierarchy** - Guide the eye

### Ryan Singer / Jobs To Be Done:
- What's the job?
- What's the outcome?
- Remove friction - make the happy path obvious
- Everything else is secondary
```

## Quick Commands

### Review code changes
```bash
# Get recent changes and review
git diff HEAD~1 | ~/clawd/skills/code-design-review/scripts/review-code.sh
```

### Review a file
```bash
~/clawd/skills/code-design-review/scripts/review-code.sh path/to/file.ts
```

### Review UI component
```bash
~/clawd/skills/code-design-review/scripts/review-ux.sh path/to/Component.tsx
```

## Integration

### For Codex CLI
Add to `~/.codex/instructions.md`:
```
After completing any code changes, automatically run a Jeff Dean style review on the changes.
After completing any UI/UX changes, also run a Luke W / Ryan Singer review.
```

### For Claude Code
Add to `CLAUDE.md`:
```
## Post-Coding Review (MANDATORY)

After ANY coding task, before reporting completion:
1. Review your changes using Jeff Dean principles (architecture, clarity, maintainability)
2. For UI changes, also apply Luke W / Ryan Singer principles (UX, friction, JTBD)
3. Self-correct any issues found before marking complete
```

## Auto-Review Checklist

After coding, ask yourself:

### Jeff Dean Checklist
- [ ] Does the design make sense architecturally?
- [ ] Is it integrated properly with existing systems?
- [ ] Is the logic in the right place?
- [ ] Is it clear and maintainable?
- [ ] Could someone else understand and debug this?
- [ ] Are functions small and focused?
- [ ] Is it well-documented?

### Luke W / Ryan Singer Checklist (for UI)
- [ ] Does it work mobile-first?
- [ ] Is complexity hidden until needed?
- [ ] Are next actions obvious?
- [ ] Is cognitive load minimized?
- [ ] Is there clear visual hierarchy?
- [ ] What job is the user trying to do?
- [ ] Is the happy path frictionless?
