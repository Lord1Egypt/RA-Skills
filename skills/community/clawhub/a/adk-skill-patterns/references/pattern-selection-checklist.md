# Pattern Selection Checklist

## Quick Decision Matrix

| If the user wants to... | Use Pattern | File to Load |
|------------------------|-------------|--------------|
| Teach agent about a library | Tool Wrapper | `templates/tool-wrapper-SKILL.md` |
| Generate consistent documents | Generator | `templates/generator-SKILL.md` |
| Review/audit something | Reviewer | `templates/reviewer-SKILL.md` |
| Gather requirements first | Inversion | `templates/inversion-SKILL.md` |
| Multi-step workflow | Pipeline | `templates/pipeline-SKILL.md` |

## Pattern Combinations

### Common Compositions

**Documentation Pipeline (Pipeline + Generator + Reviewer)**
```
1. Parse code (Pipeline Step 1)
2. Generate docstrings (Generator)
3. Review quality (Reviewer)
4. Assemble final docs (Pipeline Step 4)
```

**Requirements → Plan (Inversion + Generator)**
```
1. Interview user for requirements (Inversion)
2. Fill plan template (Generator)
```

**Expert Review (Tool Wrapper + Reviewer)**
```
1. Load framework conventions (Tool Wrapper)
2. Review code against conventions (Reviewer)
```

## When to Use Each Pattern

### Tool Wrapper
✅ Agent needs deep knowledge about specific technology  
✅ Knowledge should only load when relevant  
✅ Multiple technologies need different expertise  
❌ General knowledge tasks  
❌ One-off queries

### Generator
✅ Output must be consistent every time  
✅ Template-based documents  
✅ Standardized formats (reports, docs, messages)  
❌ Creative/open-ended tasks  
❌ Exploratory work

### Reviewer
✅ Quality gates and audits  
✅ Modular criteria that may change  
✅ Consistent scoring/grading  
❌ Tasks without clear criteria  
❌ Subjective assessments

### Inversion
✅ Complex tasks requiring full context  
✅ Preventing premature solutions  
✅ Requirements gathering  
❌ Simple, well-defined tasks  
❌ When user already provided all context

### Pipeline
✅ Multi-phase workflows  
✅ Checkpoints requiring approval  
✅ Complex processes with dependencies  
❌ Single-step tasks  
❌ Exploratory/iterative work

## Anti-Pattern Detection

| Symptom | Likely Problem | Solution |
|---------|---------------|----------|
| Agent gives generic advice | Missing Tool Wrapper | Add domain-specific reference |
| Different output every time | Missing Generator | Create template + style guide |
| Inconsistent review quality | Missing Reviewer | Create modular checklist |
| Agent assumes requirements | Missing Inversion | Add structured interview |
| Steps get skipped | Missing Pipeline | Add explicit gates |
