# Quiz Templates for Book Deep Study

## Quiz Modes

### Choice Quiz (选择题)
Generate 3-5 multiple choice questions per chapter.
Each question must:
- Test understanding of the chapter's core concept, not surface recall
- Have 4 options (A/B/C/D), exactly one correct
- All options should be plausible and similar length
- Include explanation with page/section reference

Format:
```
Q1: [question]
A) ...
B) ...
C) ...
D) ...
Answer: [letter]
Explanation: [why, with reference to the text]
```

### Written Quiz (简答题)
Generate 2-3 open-ended questions per chapter.
Each question must:
- Require the reader to articulate the concept in their own words
- Not be answerable with a simple yes/no
- Reference a specific mechanism, example, or argument from the chapter

Format:
```
Q1: [question]
Reference answer: [what a good answer would cover]
Key points to hit: [2-3 bullet points]
```

### Application Quiz (应用题)
Generate 1-2 scenario-based questions per chapter.
Each question must:
- Present a realistic situation
- Ask the reader to apply the chapter's framework
- Have no single "right" answer but clear better/worse approaches

Format:
```
Scenario: [situation description]
Question: [what would you do / how would you analyze this]
Framework to apply: [which concept from this chapter]
What a strong answer looks like: [key elements]
```

## Quiz Difficulty Levels

- **Recall**: Can you remember what the author said?
- **Comprehension**: Can you explain it in your own words?
- **Application**: Can you use it in a new situation?
- **Analysis**: Can you identify the assumptions and limitations?

Default: mix of Comprehension + Application.
