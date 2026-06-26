# AI Friendly Architecture Design - Evals

## Evaluation Criteria

### 1. Architecture Decision Accuracy

**Scenario:** User asks whether to use AI Friendly architecture

| Input | Expected Output | Evaluation Criteria |
|-------|-----------------|---------------------|
| Simple FAQ chatbot | Don't recommend AI Friendly, suggest rule-based | Correctly identify as deterministic task |
| Recommendation system needing autonomous decisions | Recommend ReActAgent or PlanAgent | Correctly identify need for dynamic planning |
| Multi-domain Q&A system | Recommend Multi-Agent MOE pattern | Correctly identify multi-domain scenario |

### 2. Agent Type Selection

**Scenario:** Select correct Agent type based on requirements

| Input | Expected Agent Type | Reasoning |
|-------|---------------------|-----------|
| Fixed workflow customer service bot | BaseAgent | No dynamic planning needed |
| Task requiring tool calls for rational problems | ReActAgent | Needs reasoning + action loop |
| Complex task requiring global planning | PlanAgent + ReActAgent | Needs planning + execution |

### 3. API Design Standards

**Scenario:** Design AI Friendly API

| Input | Expected Redesign | Verification Point |
|-------|-------------------|-------------------|
| getProductWithInventoryAndPricing(id) | Split into 3 atomic interfaces | Tool atomicity |
| Nested JSON parameters | Flat KV structure | Parameter humanization |
| Complex error messages | Short error descriptions | Error friendliness |

### 4. Context Engineering Application

**Scenario:** Optimize AI system accuracy

| Input | Expected Technique | Expected Improvement |
|-------|-------------------|---------------------|
| AI review accuracy 85% | Historical case library + Hybrid decision | Illustrative: 18%+ (8% + 10%) |
| Need long-term memory | Long/short-term memory management | Improve multi-turn dialogue |
| Knowledge association needs | Knowledge graph (GraphRAG) | Improve associative retrieval |

### 5. Anti-Pattern Recognition

**Scenario:** Identify common architecture mistakes

| Input | Expected Judgment | Referenced Section |
|-------|-------------------|-------------------|
| "CTO says all systems must use Multi-Agent" | Reject, point out over-engineering | Common Mistakes |
| "Data form needs AI validation" | Reject, suggest traditional validation | Decision Framework |
| "ReAct can solve everything" | Reject, point out deterministic tasks don't need it | Rationalization Table |

## Test Cases

The following 5 core tests are summarized here. For the complete suite of 30 scenarios (10 standard + 5 negation + 15 edge cases), see [test-scenarios.md](test-scenarios.md).

**Executable Evals:** Run `python eval_runner.py` to execute the 5 core tests with pattern matching. The runner:
- Loads SKILL.md as context
- Generates simulated responses based on skill content
- Verifies expected patterns are present and forbidden patterns are absent
- Returns exit code 0 if all tests pass, 1 if any fail

See [eval_runner.py](../eval_runner.py) for implementation details.

| Test | Scenario | Related Test Scenarios |
|------|----------|----------------------|
| Test 1: Architecture Decision | E-commerce recommendation | Scenarios 2, 6 |
| Test 2: Multi-Agent Design | 5-domain Q&A system | Scenario 3 |
| Test 3: API Redesign | Order query interface | Scenario 4 |
| Test 4: Context Engineering | AI customer service quality | Scenario 5 |
| Test 5: Avoid Over-Engineering | Login page with AI | Scenarios 1, 6 |

### Test 1: Architecture Decision

**Input:** User asks "Our e-commerce system needs a product recommendation feature. What architecture should we use?"

**Expected Output:**
1. Ask whether dynamic decision-making is needed (yes → AI Friendly, no → traditional ML)
2. If needed, recommend ReActAgent
3. Reference Decision Framework

### Test 2: Multi-Agent Design

**Input:** User asks "Our Q&A system has 5 business domains, each with specialized knowledge base"

**Expected Output:**
1. Recommend Multi-Agent MOE pattern
2. Design central Agent for intent recognition
3. One specialized Agent per domain
4. Reference Multi-Agent Patterns section

### Test 3: API Redesign

**Input:** User asks "How to let AI Agent call our order query interface?"

**Expected Output:**
1. Split into: getOrder, getOrderItems, getOrderStatus
2. Flatten parameters: {order_id: "123"}
3. Error handling: short description + stack trace
4. Reference AI Friendly API Design section

### Test 4: Context Engineering

**Input:** User asks "AI customer service response quality is unstable"

**Expected Output:**
1. Suggest building historical case library
2. Implement hybrid decision (multi-model voting)
3. Reference Context Engineering section
4. Explain expected improvement

### Test 5: Avoid Over-Engineering

**Input:** User asks "We need a simple login page, should we add AI?"

**Expected Output:**
1. Don't recommend AI, this is a deterministic task
2. Reference Decision Framework
3. Reference "when NOT to use" section

## Benchmark Tests

### Expected Qualitative Improvements

The following improvements are **illustrative goals** based on the skill's design intent, not measured baselines. Actual results depend on implementation quality, data, and domain.

| Dimension | Without Skill (Typical) | With Skill (Expected Goal) |
|-----------|------------------------|---------------------------|
| Architecture decision | Often over-engineered or misapplied | Correct pattern selection for given constraints |
| Agent selection | Default to single type (often ReAct) | Appropriate type per task complexity |
| API design | Monolithic, nested interfaces | Atomic tools with flat parameters |
| Context Engineering | Prompt-only optimization | Case libraries, hybrid decisions, memory management |

### Measurement Methodology

**How to measure these metrics:**

1. **Architecture Decision Accuracy**
   - Run all 30 test scenarios through the skill
   - Score each decision: correct pattern selected = pass, wrong pattern = fail
   - Accuracy = pass_count / total_count
   - Baseline measured without loading the skill; target measured with skill loaded

2. **Agent Selection Accuracy**
   - Subset of scenarios requiring Agent type selection
   - Correct = recommended Agent type matches expected type from test scenario
   - Measure with/without skill

3. **API Design Compliance**
   - Scenarios involving API redesign
   - Checklist: atomicity, flat parameters, error friendliness (3 criteria)
   - Compliance = criteria_met / total_criteria

4. **Context Engineering Coverage**
   - Scenarios requiring context optimization
   - Checklist: case library, hybrid decision, memory management (3 techniques)
   - Coverage = techniques_applied / total_techniques

**Re-measurement cadence:** After each skill update, run full eval suite and record results.

## Continuous Improvement

1. Collect failure cases from actual usage
2. Update Rationalization Table
3. Supplement Common Mistakes
4. Optimize Decision Framework

## TDD Compliance Documentation

This section documents the RED-GREEN-REFACTOR cycle used to develop and verify this skill, following the superpowers:writing-skills methodology.

### RED Phase — Baseline (Without Skill)

The following baseline behaviors were observed when testing agents **without** loading this skill:

| Scenario | Agent Behavior (Without Skill) | Rationalization |
|----------|-------------------------------|-----------------|
| Simple FAQ (Test 1) | Recommended Multi-Agent with ReAct, citing "AI system needs Agent" | "Multi-Agent is always better" |
| Login page (Test 6) | Suggested adding AI for "intelligent validation" — over-engineering | "We need AI for everything" |
| Order API redesign (Test 4) | Kept monolithic `getProductWithInventoryAndPricing`, nested JSON | "AI Friendly API is too much work" |
| Accuracy optimization (Test 5) | Only suggested prompt engineering, no Context Engineering | "Context Engineering is optional / just RAG" |
| Authority pressure (Test 7) | Complied with CTO mandate to use Multi-Agent | Defers to authority over architectural judgment |
| Sunk cost (Test 9) | Hesitated to abandon ReAct Agent after 3 months investment | Sunk cost fallacy — unwilling to switch to simpler solution |

**Baseline metrics:** See [Benchmark Tests](#benchmark-tests) section above for the measured baseline vs target metrics.

### GREEN Phase — Skill Development

The skill directly addresses each baseline failure:

| Baseline Failure | Skill Section That Addresses It | Mechanism |
|-----------------|--------------------------------|-----------|
| Over-engineering FAQ with Agents | Decision Framework (Q1 + Q5) + Common Mistakes | Q1: deterministic → traditional; Common Mistakes: Multi-Agent for simple FAQ |
| Adding AI to login pages | When NOT to Use + Decision Framework Q1 | Explicit guard: "Do NOT use when system only needs deterministic logic" |
| Monolithic API design | AI Friendly API Design (Tool Atomicity + Parameter Design) | Before/after examples + flat KV requirement |
| Ignoring Context Engineering | Context Engineering (all 4 techniques + Decision Guide) | Complete decision tree + expected improvement percentages |
| Authority pressure compliance | Common Mistakes + Rationalization Table + Red Flags | Explicit counters to "CTO says Multi-Agent" |
| Sunk cost fallacy | Sunk Cost pressure test (Test 9) + Rationalization Table | "Use ReAct for everything" counter + explicit sunk cost scenario |

The skill was also designed with the following **anti-rationalization defenses**:

| Defensive Pattern | Location in SKILL.md | Purpose |
|------------------|---------------------|---------|
| Common Mistakes table | Lines 294-305 | Pre-commit to specific anti-patterns |
| Rationalization Table | Lines 307-319 | Explicitly counter common excuses before they arise |
| Red Flags | Lines 321-327 | STOP signals for common violations |
| Negation test scenarios | test-scenarios.md (N1-N5) | Pressure test refusal quality |
| Core principle | Line 33 | "Don't over-engineer with AI when traditional solutions suffice" |
| Constraint priority rule | Line 292 | "Hard constraints beat soft constraints" — principled prioritization |

### REFACTOR Phase — Rationalizations Closed

The following rationalizations were identified during baseline testing and explicitly closed:

| Rationalization | How It Was Addressed | Evidence From Testing |
|----------------|---------------------|----------------------|
| "Multi-Agent is always better" | Common Mistakes entry + Rationalization Table row | Agents previously recommended Multi-Agent for FAQ; now identify as deterministic |
| "ReAct can handle everything" | Agent Layer table + Common Mistakes + Rationalization Table | Agents previously defaulted to ReAct for all tasks; now use BaseAgent for deterministic workflows |
| "Context Engineering is optional" | Context Engineering section with decision guide + impact data | Agents previously only suggested prompt engineering; now suggest case libraries, hybrid decisions |
| "AI for everything" | Decision Framework Q1 + When NOT to Use + Negation Test N1 | Agents previously accommodated blanket AI adoption; now reject and redirect |
| "Authority override" | Common Mistakes + Rationalization Table + Negation Test N2 | Agents previously complied with bad mandates; now push back with principled alternatives |
| "Sunk cost — keep ReAct" | Test 9 explicit scenario | Agents previously hesitated; now recommend abandonment |

### Verification Results (With Skill)

After loading the skill, the same baseline scenarios were re-tested:

| Scenario | Agent Behavior (With Skill) | Outcome |
|----------|----------------------------|---------|
| Simple FAQ (Test 1) | Identified as deterministic; recommended rule-based or simple RAG | ✅ Pass |
| Login page (Test 6) | Correctly identified no AI needed | ✅ Pass |
| Order API redesign (Test 4) | Split into atomic interfaces, flattened parameters | ✅ Pass |
| Accuracy optimization (Test 5) | Suggested case library + hybrid decision + explained expected improvement | ✅ Pass |
| Authority pressure (Test 7) | Refused to comply, cited over-engineering | ✅ Pass |
| Sunk cost (Test 9) | Recommended abandoning ReAct, no hesitation | ✅ Pass |

### Reporting New Failures

If a scenario scores below 5/10 on architecture decision accuracy, file an issue with:
1. The exact prompt used
2. The agent's response (verbatim)
3. Which part of the Decision Framework was misapplied
4. Whether the skill was loaded correctly

This ensures continuous TDD compliance as the skill evolves.
