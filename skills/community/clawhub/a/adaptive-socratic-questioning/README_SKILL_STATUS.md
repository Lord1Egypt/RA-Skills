# Adaptive Socratic Questioning Skill

## Skill Created Successfully

I've created your **Adaptive Socratic Questioning** skill with the following structure:

```
adaptive-socratic-questioning/
├── SKILL.md                          # Main skill file with complete implementation
└── evals/
    └── evals.json                    # 5 test cases covering different scenarios
```

## What Was Created

### SKILL.md
- Complete YAML metadata with evidence-based research citations
- Detailed implementation algorithm
- 7 question type templates (explanation, evidence, causality, comparison, counterexample, generalization, creative)
- Level adaptation strategies for elementary through university
- 2 complete examples (university science and elementary math)
- Research foundation from Socratic Method, Bloom's Taxonomy, and modern pedagogy
- Edge case handling and known limitations

### Test Cases (evals/evals.json)
5 comprehensive test scenarios:
1. **University science** - Materials science, lithium diffusion
2. **Elementary math** - Place value, carrying in addition
3. **High school literature** - Romeo and Juliet thematic analysis
4. **Mixed-level physics** - Gravity, differentiated questions
5. **Chemistry wrong answer** - Guiding student from misconception without direct correction

## Key Features

✅ **Evidence-based** - Grounded in 6+ research citations
✅ **Adaptive levels** - Supports elementary through university
✅ **7 question types** - Comprehensive questioning toolkit
✅ **JSON output** - Structured, parseable results
✅ **Teacher guidance** - Actionable implementation advice
✅ **Misconception detection** - Identifies common student errors
✅ **Research citations** - Connects to educational science

## Next Steps Options

### Option 1: Run Full Evaluation (Recommended)
- Launch parallel test runs with and without the skill
- Generate eval viewer for qualitative review
- Run quantitative assertions
- Iterate based on results

### Option 2: Quick Validation
- Run a few test cases to verify basic functionality
- Review outputs informally
- Skip formal benchmarking

### Option 3: Skill Description Optimization
- Generate trigger eval queries (should-trigger / should-not-trigger)
- Optimize the description for better triggering accuracy
- Test trigger performance

### Option 4: Package and Install
- Package as .skill file
- Install for immediate use
- Skip formal evaluation

## Your Skill Description

The current description is designed to be slightly "pushy" to improve triggering:

> "Use adaptive follow-up questioning to deepen student reasoning and uncover misconceptions. Use when the user needs to guide students through deeper thinking, wants to develop critical thinking skills, asks about questioning techniques, needs to scaffold complex topics, wants to identify student misconceptions, mentions Socratic method, or needs to build reasoning chains. Always use this skill when the user mentions questioning, deeper understanding, student reasoning, critical thinking, or wants to guide students from surface-level to deeper understanding."

This includes multiple trigger phrases and contexts to maximize the chance Claude will invoke this skill when appropriate.

---

**Which option would you like to proceed with?** Or would you like me to explain any part of the skill in more detail first?