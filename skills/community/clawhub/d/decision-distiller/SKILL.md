---
name: decision-distiller
description: Distill decision contexts, options, trade-offs, and outcomes into structured decision records. Use when the user is facing a choice, has made a decision they want to document, or needs to analyze past decisions for patterns. Captures rationale, alternatives considered, and lessons learned.
version: v1.0.0
tags: decision-records, rationale-documentation, tradeoff-analysis
---

# Decision Distiller

## Usage Scenarios

### Scenario 1: Document a Technology Choice
**User input:** "We decided to use React instead of Vue for this project. Record that decision."
**Expected output:** A structured decision record with context (project requirements), options (React vs Vue), evaluation criteria (ecosystem, team expertise, performance), chosen option (React), rationale, and trade-offs accepted.

### Scenario 2: Compare Options Before Deciding
**User input:** "Help me decide between AWS and Azure for deploying our microservices"
**Expected output:** The skill walks through context gathering, lists both options with pros/cons and estimated impact, defines decision criteria with weights, and produces a pending decision record awaiting the final choice.

### Scenario 3: Review Past Decisions for Patterns
**User input:** "What deployment decisions have we made this quarter and what patterns do you see?"
**Expected output:** A decision status report listing all relevant decisions by date and status, followed by pattern analysis showing common criteria used, recurring trade-offs, and lessons extracted from outcomes.
### Scenario 4: 纠结要不要辞职去读研
**User input:** "工作了三年想去读个全日制研究生，但又怕读完回来不好找工作，还损失三年收入，太纠结了。"
**Expected output:** 用决策矩阵分析：列出选择'辞职读研'和'在职工作'的评估维度（薪资影响、职业发展、人脉资源、时间成本、心理回报等），按权重打分。给出量化对比结果。推荐折中方案：1）非全日制研究生（周末上课，不影响工作）；2）如果决定脱产，建议先积累到足够的经济储备（预留6个月生活费+学费）；3）选择就业前景明确的专业方向（如MBA、计算机、新传等）。

## Overview

Decision Distiller helps capture, structure, and learn from decisions made during OpenClaw sessions. It transforms informal decision-making into documented, reviewable records that build organizational knowledge over time.

## When to Use

Use this skill when:
- A user is weighing multiple options and needs clarity
- A decision has been made and should be documented
- Past decisions need review or analysis
- Decision patterns across sessions should be identified
- The user asks to "document this decision" or "record why we chose X"

## Core Concepts

### Decision Record
A structured document capturing:
- **Context**: Situation requiring a decision
- **Options**: Alternatives considered
- **Criteria**: How options were evaluated
- **Decision**: The choice made
- **Rationale**: Why this choice was made
- **Trade-offs**: What was gained/lost
- **Outcome**: Result of the decision (filled later)
- **Lessons**: What was learned

### Decision Status
- **pending**: Decision not yet made
- **decided**: Decision made, awaiting outcome
- **validated**: Decision proven correct
- **revised**: Decision changed based on new information
- **archived**: Decision no longer relevant

## Input

Accepts decision information in various forms:
- Conversation about options
- Pros/cons lists
- Direct statements of choice
- Retrospective analysis

## Output

Produces:
- Dated decision records (Markdown)
- Decision summaries
- Pattern analysis across decisions
- Decision status reports

## Workflow

### Capturing a New Decision

1. **Identify Context**
   - What situation required a decision?
   - What was at stake?
   - Who was involved?

2. **List Options**
   - What alternatives were considered?
   - What was eliminated early?
   - What made it to final consideration?

3. **Define Criteria**
   - How were options evaluated?
   - What mattered most?
   - Were there constraints?

4. **Record Decision**
   - What was chosen?
   - When was it decided?
   - Who decided?

5. **Document Rationale**
   - Why was this option selected?
   - What tipped the balance?
   - What assumptions were made?

6. **Note Trade-offs**
   - What was sacrificed?
   - What risks were accepted?
   - What opportunities were passed?

### Reviewing Past Decisions

1. **Gather Records**
   - Collect relevant decision records
   - Filter by topic, date, or status

2. **Analyze Patterns**
   - Common criteria used
   - Recurring trade-offs
   - Typical decision timelines

3. **Extract Lessons**
   - What worked well?
   - What would change?
   - What patterns emerge?

## Output Format

### Decision Record

```markdown
# Decision: [Title] - YYYY-MM-DD

**ID**: DEC-2024-001
**Status**: decided
**Decided By**: [Name/Role]
**Date**: YYYY-MM-DD

## Context
[Description of the situation requiring a decision]

## Options Considered

### Option 1: [Name]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Estimated Impact**: 

### Option 2: [Name]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Estimated Impact**: 

## Decision Criteria
1. [Criterion 1] - Weight: High/Medium/Low
2. [Criterion 2] - Weight: High/Medium/Low

## Decision
**Chosen**: [Option X]

## Rationale
[Why this option was selected over others]

## Trade-offs
- **Accepted**: [What we gave up]
- **Mitigated**: [How we reduced risks]

## Expected Outcome
[What we expect to happen]

## Actual Outcome
[Filled in later - what actually happened]

## Lessons Learned
[Filled in later - insights from the outcome]

## Related Decisions
- [Link to related decision]
```

## Commands

### Create Decision Record
```
decision create "Decision title" --status pending
```

### Update Decision
```
decision update DEC-2024-001 --status validated
```

### List Decisions
```
decision list --status decided --since 2024-01-01
```

### Analyze Patterns
```
decision analyze --topic architecture
```

## Quality Rules

- Be specific: vague decisions teach no lessons
- Include alternatives: decisions without options aren't decisions
- Document rationale: future you needs to know why
- Review outcomes: a decision isn't complete until its outcome is known
- Link related decisions: build decision networks

## Good Trigger Examples

- "Document this decision: we're going with X"
- "Help me decide between A and B"
- "What decisions have we made about architecture?"
- "Review our deployment decisions from last month"
- "I decided to use Y instead of Z, record that"

## Resources

### references/
- `references/decision-templates.md`: Variations for different decision types
- `references/analysis-frameworks.md`: Tools for analyzing decisions
