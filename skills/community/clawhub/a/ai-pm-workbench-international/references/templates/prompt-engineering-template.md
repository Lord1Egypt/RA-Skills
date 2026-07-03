# Prompt Engineering Documentation Template

## Document Information

| Field | Content |
|------|------|
| Product/Feature Name | [Name] |
| Prompt Version | V1.0 |
| Date | YYYY-MM-DD |
| Author | [Name] |
| Associated Model | [Model Name + Version] |

---

## 1. Prompt Overview

### 1.1 Usage Scenarios

| Scenario | User Input | Expected Output | Frequency |
|------|---------|---------|------|
| | | | |

### 1.2 Design Goals

| Dimension | Goal | Measurement Method |
|------|------|---------|
| Accuracy | | |
| Consistency | | |
| Safety | | |
| Format Compliance Rate | | |
| Latency | | |

---

## 2. System Prompt

### 2.1 Complete Prompt

```
[Fill in the complete System Prompt here]

# Role
You are [Role Name], [Role Description]

# Core Capabilities
- [Capability 1]
- [Capability 2]

# Core Constraints
- [Constraint 1]
- [Constraint 2]

# Workflow
1. [Step 1]
2. [Step 2]
3. [Step 3]

# Output Format
[Format requirements]
```

### 2.2 Design Rationale

| Design Decision | Rationale | Alternatives |
|---------|------|---------|
| Role Definition | | |
| Constraints | | |
| Output Format | | |

---

## 3. Context Assembly

### 3.1 Context Structure

```
┌─────────────────────────────────┐
│ System Prompt (~X tokens)       │ ← Role + Constraints + Format
├─────────────────────────────────┤
│ User Profile (~X tokens)        │ ← Role/Department/Preferences
├─────────────────────────────────┤
│ Business Context (~X tokens)    │ ← Relevant business data
├─────────────────────────────────┤
│ RAG Retrieval Results (~X tokens)│ ← Knowledge base retrieval
├─────────────────────────────────┤
│ Conversation History (~X tokens)│ ← Last N rounds of dialogue
├─────────────────────────────────┤
│ User Query                      │ ← Current user input
└─────────────────────────────────┘
```

### 3.2 Token Budget Allocation

| Context Type | Token Allocation | Percentage | Notes |
|-----------|----------|------|------|
| System Prompt | | | Fixed, unchanging |
| User Profile | | | Load on demand |
| Business Context | | | Dynamic query |
| RAG Retrieval | | | Real-time retrieval |
| Conversation History | | | Sliding window |
| User Query | | | Reserved space |
| **Total** | | 100% | Must not exceed 80% of context window |

### 3.3 Context Compression Strategy

| Strategy | Trigger Condition | Method |
|------|---------|------|
| Conversation Summarization | Conversation rounds > N | LLM compresses history into summary |
| Sliding Window | Total tokens exceed limit | Keep last K rounds |
| Hierarchical Truncation | Context exceeds limit | Trim by priority |

---

## 4. Few-Shot Example Design

### 4.1 Example Coverage Matrix

| Example No. | Coverage Scenario | Difficulty | Input Summary | Expected Output Summary |
|---------|---------|------|---------|------------|
| Example-1 | Common scenario | Easy | | |
| Example-2 | Common scenario | Medium | | |
| Example-3 | Edge scenario | Hard | | |
| Example-4 | Error handling | Medium | | |

### 4.2 Complete Examples

#### Example-1: [Scenario Name]

**Input:** 
```
[User input content]
```

**Expected Output:**
```
[Expected model output]
```

**Design Key Points:**
- [What capability does this example demonstrate]
- [Why was this example chosen]

#### Example-2: [Scenario Name]
(Same structure as above)

---

## 5. Advanced Technique Application

### 5.1 Technique Selection

| Technique | In Use | Purpose | Implementation |
|------|---------|------|---------|
| Chain-of-Thought | | | |
| ReAct | | | |
| Self-Consistency | | | |
| Tree-of-Thought | | | |
| Structured Output | | | |
| Tool/Function Calling | | | |

### 5.2 CoT Design (if used)

```
Let's think step by step:
1. First, analyze the user input to identify key information: [...]
2. Then, query relevant knowledge: [...]
3. Next, perform reasoning: [...]
4. Finally, generate the output: [...]
```

### 5.3 Chain-of-Thought Verification

| Check Item | Verification Method |
|--------|---------|
| Reasoning steps complete | Manual review of CoT traces |
| Intermediate steps correct | Compare against gold answers |
| No key steps skipped | Step coverage statistics |

---

## 6. Output Format Definition

### 6.1 Structured Output Schema

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["success", "partial", "failed"],
      "description": "Execution status"
    },
    "data": {
      "type": "object",
      "description": "Return data"
    },
    "reasoning": {
      "type": "string",
      "description": "Reasoning process"
    },
    "citations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source": {"type": "string"},
          "content": {"type": "string"}
        }
      }
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  },
  "required": ["status", "data"]
}
```

### 6.2 Format Constraints

| Constraint Item | Rule |
|--------|------|
| Language | |
| Length Limit | |
| Markdown Format | |
| Code Blocks | |
| Tables | |
| Special Characters | |

---

## 7. Error Handling Design

### 7.1 Error Scenario Handling

| Error Scenario | Trigger Condition | Expected Output | Prompt Design |
|---------|---------|---------|-----------|
| Incomplete Input | Missing required parameters | Guide user to supplement | Follow-up template |
| Beyond Capability | Unhandleable task | Clearly inform + suggest | Refusal template |
| Sensitive Content | Unsafe input | Safe refusal | Guardrail interception |
| No Relevant Information | No match in knowledge base | Honest disclosure | "Unable to determine" |
| Format Exception | Unparseable input | Request re-input | Format hint |

### 7.2 Refusal Templates

```
# Safe Refusal
Sorry, I cannot process this request because [reason].
Suggestion: [alternative]

# Capability Boundary
Sorry, this question is beyond my capabilities.
I can help you with: [list related capabilities]

# Insufficient Information
Based on available materials, I cannot determine [specific question].
Suggestion: [ways to obtain the information]
```

---

## 8. Version Iteration Record

### 8.1 Version History

| Version | Date | Changes | Reason for Change | Evaluation Impact |
|------|------|---------|---------|---------|
| V1.0 | | Initial version | - | Baseline |
| V1.1 | | | | |

### 8.2 A/B Test Records

| Test | Variant A | Variant B | Winner | Improvement |
|------|-------|-------|------|------|
| | | | | |

---

## 9. Evaluation Plan

### 9.1 Prompt Evaluation Metrics

| Metric | Target Value | Measurement Method | Current Value |
|------|--------|---------|--------|
| Format Compliance Rate | >95% | Automated validation | |
| Factual Accuracy Rate | >90% | Golden Dataset | |
| Refusal Accuracy Rate | >95% | Safety test set | |
| Output Consistency | >90% | Repeated testing (N=10) | |
| Instruction Following Rate | >90% | Automated + Manual | |

### 9.2 Evaluation Datasets

| Dataset | Sample Count | Coverage Scenario | Update Frequency |
|--------|--------|---------|---------|
| Golden Dataset | | Core scenarios | Monthly |
| Regression Test Set | | Historical bad cases | Continuously appended |
| Safety Test Set | | Jailbreak/Injection | Monthly |
| Robustness Test Set | | Edge/Exception | Quarterly |

### 9.3 Evaluation Script

```python
# Pseudocode: Prompt evaluation pipeline
def evaluate_prompt(prompt, test_dataset):
    results = []
    for case in test_dataset:
        response = call_llm(prompt, case.input)
        score = auto_evaluate(response, case.expected_output)
        results.append({
            "case_id": case.id,
            "score": score,
            "response": response
        })
    return aggregate(results)
```

---

## 10. Monitoring & Continuous Optimization

### 10.1 Monitoring Metrics

| Metric | Alert Threshold | Review Frequency |
|------|---------|---------|
| Output Format Error Rate | >5% | Daily |
| Refusal Rate Abnormal Change | Fluctuation >20% | Daily |
| Average Output Length Anomaly | Fluctuation >30% | Daily |
| User Negative Feedback Rate | >10% | Weekly |

### 10.2 Optimization Iteration Loop

```
Discover Bad Case → Analyze root cause (Unclear instructions? Insufficient Few-Shot? Missing context?)
  → Modify Prompt → Run regression test → Pass → A/B Verify → Full rollout
```


---

## v1.1.0 Added: Agent Prompt Engineering

### Agent System Prompt Design Template
```
You are a [Role Name], responsible for [Core Responsibilities].

## Capability Boundaries
You can:
- [Capability 1]
- [Capability 2]

You cannot:
- [Limitation 1]
- [Limitation 2]

## Tool Usage
You may use the following tools:
- tool_1: [Description] — Parameters: [params]
- tool_2: [Description] — Parameters: [params]

## Decision Rules
1. When [Condition] → Use [Tool]
2. When [Condition] → [Action] to user
3. When [Condition] → Terminate and [Output]

## Output Format
[Expected output format and examples]

## Safety Constraints
- [Safety rule 1]
- [Safety rule 2]
```

### Multi-Agent Orchestration Prompt
```
Main Agent: [Role] — Responsible for task decomposition and coordination
  ├── Sub-Agent 1: [Role] — Responsible for [Sub-task]
  │   System Prompt: [Complete prompt for sub-agent]
  │   Input: [What it receives]
  │   Output: [What it produces]
  ├── Sub-Agent 2: [Role] — Responsible for [Sub-task]
  │   System Prompt: [Complete prompt for sub-agent]
  │   Input: [What it receives]
  │   Output: [What it produces]
  └── Coordination Rules:
      - Parallel Execution: [Which agents can run simultaneously]
      - Serial Dependency: [Agent 2 depends on Agent 1's output]
      - Conflict Resolution: [How to handle contradictory agent outputs]
```