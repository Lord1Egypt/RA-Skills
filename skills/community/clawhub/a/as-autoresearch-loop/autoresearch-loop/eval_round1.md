# Autoresearch Loop — Fixed Eval Set (DO NOT MODIFY)

## Scoring Rubric
Each prompt scored PASS (1) or FAIL (0).
Score = (passes / 10) * 100

## Prompts + Pass Criteria

### P1: Basic trigger — skill improvement
**Prompt**: "I want to automatically improve my SKILL.md overnight. It's my n8n-workflow-patterns skill."
**PASS if**:
- Identifies the artifact (SKILL.md)
- Asks for or proposes a metric (pass rate / eval set)
- Mentions the loop structure (propose → test → keep/discard)
- Does NOT just explain what autoresearch is — actually starts the setup

### P2: Basic trigger — workflow optimization
**Prompt**: "Run autoresearch on my email triage n8n workflow."
**PASS if**:
- Starts the setup phase (doesn't just describe the method)
- Identifies what needs to be locked (input schema, credentials)
- Asks about or proposes a measurable metric (execution success rate, step count, etc.)

### P3: Metric guidance — ambiguous artifact
**Prompt**: "What metric should I use for improving a client onboarding SOP?"
**PASS if**:
- Gives at least 2 concrete metric options (checklist pass rate, clarity score, step count, cycle time)
- Explains that one metric must be chosen and kept fixed
- Does NOT say "it depends" without giving concrete options

### P4: One-change rule
**Prompt**: "I want to test adding better error handling AND restructuring the headers in the same experiment."
**PASS if**:
- Clearly says NO — one change per experiment
- Explains WHY (can't attribute the result to either change)
- Suggests splitting into two sequential experiments

### P5: Keep/discard decision
**Prompt**: "My experiment improved the score from 72% to 74%. Should I keep it? It added 25 lines of new examples."
**PASS if**:
- Applies the simplicity criterion (25 lines for +2% is borderline/probably not worth it)
- Does NOT just say "yes keep it because it improved"
- Invokes Karpathy's simplicity rule explicitly or in spirit

### P6: Results log format
**Prompt**: "Show me how to log a failed experiment where I tried restructuring sections and went from 75% to 69%."
**PASS if**:
- Produces a valid TSV row (tab-separated, 4 columns: iteration, score, status, description)
- Uses `discard` as the status
- Score is 69.0 (not 75)

### P7: Getting unstuck
**Prompt**: "I've run 8 experiments and the last 4 all discarded. I'm running out of ideas."
**PASS if**:
- Does NOT suggest stopping
- Gives at least 3 concrete new directions to try
- Mentions looking at the failed test cases specifically for clues

### P8: Scope — what can be modified
**Prompt**: "Can I add a new test prompt to my eval set mid-loop to test a new edge case I found?"
**PASS if**:
- Says NO — the eval set is fixed (it's the prepare.py, not the train.py)
- Explains why: changing the eval invalidates comparison across iterations
- Suggests noting it for the NEXT session instead

### P9: Full setup walkthrough
**Prompt**: "Walk me through setting up autoresearch for improving a system prompt. I have 15 test prompts and a scoring rubric already."
**PASS if**:
- Covers all 5 setup elements (artifact, metric, budget, results log, confirm)
- Specifies that the 15 test prompts are now FIXED
- Creates or describes the results.tsv header
- Ends with a call to run the baseline as experiment 0

### P10: Session summary
**Prompt**: "I'm done for the night. We ran 12 experiments, started at 60%, ended at 82%. 5 kept, 7 discarded. Summarize."
**PASS if**:
- Produces a formatted Research Summary (matching the template in the skill)
- Includes starting/ending score and delta
- Separates kept vs discarded
- Ends with 2-3 recommendations for next session
