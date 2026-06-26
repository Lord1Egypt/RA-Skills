#!/bin/bash
# Architecture Decision Template Spawn Prompt
# Use for: Making architectural decisions with debate

cat << 'SPAWNPROMPT'
I need to make an architectural decision: ${TASK_DESCRIPTION}

Target: ${TARGET_DIR}

Spawn 2 advocates using Sonnet (they will debate the options):

1. **Advocate for Option A**
   - Name: advocate-option-a
   - Position: Argue for the first architectural option
   - Output: proposal-option-A.md
   - Tasks:
     * Research strengths of Option A for this use case
     * Address decision criteria (performance, scalability, complexity, team familiarity)
     * Identify weaknesses of Option B
     * Provide concrete examples or evidence
     * Recommend Option A with supporting arguments

2. **Advocate for Option B**
   - Name: advocate-option-b
   - Position: Argue for the alternative architectural option
   - Output: proposal-option-B.md
   - Tasks:
     * Research strengths of Option B for this use case
     * Address decision criteria (performance, scalability, complexity, team familiarity)
     * Identify weaknesses of Option A
     * Provide concrete examples or evidence
     * Recommend Option B with supporting arguments

Coordination rules:
- Use delegate mode: I facilitate, advocates debate (I don't implement)
- Advocates work independently as adversaries
- Advocates must argue honestly (no straw man arguments)
- Advocates should acknowledge trade-offs
- After both complete, facilitate debate via messages

Debate structure:
1. Advocates present positions
2. Rebuttals (respond to opponent's weaknesses)
3. Q&A (ask clarifying questions)
4. Final statements

After debate:
1. Synthesize into Architecture Decision Record (ADR)
2. Include: context, options considered, decision criteria, trade-offs, decision
3. Provide rationale and implications
4. Report completion with final decision
SPAWNPROMPT
