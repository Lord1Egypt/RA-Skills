# Prompt Engineering Techniques Reference

## 1. Persona Assignment

Assign a role before the task to dramatically improve output quality. The AI adopts the expertise, tone, and focus of the role.

**Format:**
```
You are a [role] with expertise in [domain]. [Optional: "Your goal is to..."]
```

**Examples by task type:**
| Task | Persona |
|------|---------|
| Code review | `"You are a senior software engineer specializing in Node.js security"` |
| Email drafting | `"You are a professional business writer known for concise, friendly communication"` |
| Data analysis | `"You are a data analyst with 10 years in e-commerce metrics"` |
| Debugging | `"You are a debugging expert who traces root causes before suggesting fixes"` |
| System design | `"You are a senior systems architect focused on scalability and reliability"` |

**Why it works:** The persona narrows the model's "attention" to relevant knowledge and adjusts tone, vocabulary, and decision-making to match the role.

---

## 2. Few-Shot Examples

Provide 1–3 input/output examples when format consistency matters. Examples beat instructions.

**When to use:**
- Output format is non-standard (custom JSON, specific markdown, tables)
- Task involves classification or labeling
- Style/tone needs to match an existing sample

**Format:**
```
Here are examples of the format I want:

Input: "Q3 revenue dropped 15%"
Output: ⚠️ Revenue | Q3 | -15% | Investigate

Input: "New user signups up 40%"
Output: ✅ Signups | Q3 | +40% | Positive trend

Now apply this to: [your actual data]
```

**Few-shot vs zero-shot:**
- Zero-shot: No examples — works for well-defined tasks with clear instructions
- One-shot: 1 example — good for format/style guidance
- Few-shot (2-3): Best for classification, labeling, pattern matching

---

## 3. Chain of Thought (CoT)

Ask the AI to reason step by step before giving the final answer. Dramatically improves accuracy on complex tasks.

**When to use:**
- Multi-step reasoning (math, logic, debugging)
- Root cause analysis
- Decision-making with tradeoffs
- Any task where "the right answer requires thinking"

**Trigger phrases:**
- `"Think step by step:"`
- `"Walk me through your reasoning:"`
- `"Before answering, break this down into steps:"`
- `"Explain your reasoning at each step, then give the final answer:"`

**Example:**
```
You are a senior Node.js engineer.

Task: Debug why the login endpoint returns 403 for valid users.

Think step by step:
1. What could cause a 403 for a valid user?
2. What should I check in the auth middleware?
3. What should I check in the token validation?
4. What's the most likely root cause?

After reasoning, provide: root cause + fix.
```

**Zero-shot CoT:** Just adding `"Let's think step by step"` at the end of any prompt activates reasoning — no examples needed.

---

## 4. Prompt Chaining

Break complex tasks into a sequence of smaller, connected prompts. Each output feeds the next prompt.

**When to use:**
- Tasks with 3+ distinct phases (research → draft → review)
- Output of step 1 is needed to define step 2
- Long tasks that would exceed context or lose focus
- Iterative refinement workflows

**Pattern:**
```
Prompt 1: "Generate 3 one-sentence summaries of this document."
    ↓ [Use output as input]
Prompt 2: "Using these 3 summaries: [output], write a single tagline that captures the core message."
    ↓ [Use output as input]
Prompt 3: "Using this tagline: [output], write a 3-tweet thread to promote this content."
```

**Real example (code review chain):**
1. "List all functions in this file that handle user input" 
2. "For these functions: [output], identify which ones lack input validation"
3. "For these vulnerable functions: [output], write the missing validation code"

**Benefits:** Each step is focused, verifiable, and correctable before moving forward.

---

## 5. Meta Prompting

Ask the AI to help improve or generate its own prompt. Use when you're unsure how to structure a complex request.

**When to use:**
- You know what you want but not how to prompt it
- A prompt isn't performing well and you want to iterate
- You want the AI to identify what information it needs

**Formats:**

*Ask AI to write a better prompt:*
```
I want to achieve: [goal]
Here's my current prompt: [prompt]
What's a better way to prompt this to get [specific result]?
```

*Ask AI what it needs:*
```
I want you to [task]. What information do you need from me to do this well?
```

*Ask AI to self-critique:*
```
Here is your previous output: [output]
What's missing or could be improved? Then revise it.
```

---

## 6. Tree of Thought (ToT)

Extension of CoT — ask the AI to explore multiple reasoning paths before choosing the best one.

**When to use:**
- High-stakes decisions with multiple valid approaches
- Creative tasks where you want diverse options
- Troubleshooting when root cause is unclear

**Format:**
```
Consider 3 different approaches to [problem]:
- Approach A: [brief description]
- Approach B: [brief description]  
- Approach C: [brief description]

Evaluate each approach for [criteria: speed/safety/cost/complexity].
Then recommend the best one and explain why.
```

---

## 7. Iteration Strategies

When output isn't right, iterate using one of these methods:

| Strategy | When to use | Example |
|---|---|---|
| **Add context** | Output is too generic | "Also consider that this runs on macOS ARM64" |
| **Add persona** | Tone/expertise is off | "You are a security expert, not a general helper" |
| **Add examples** | Format is wrong | "Here's an example of what I want: [sample]" |
| **Separate sentences** | Prompt is too complex | Break into shorter, focused sentences |
| **Introduce constraints** | Output is too broad | "Limit to 3 items. Only focus on security issues." |
| **Rephrase** | AI misunderstood | Use analogous task framing |

---

## 8. Constraint Injection

Adding constraints improves focus and prevents scope creep:

- **Length**: `"Respond in under 100 words"` / `"Give exactly 3 bullet points"`
- **Scope**: `"Only check the authentication module, not the entire codebase"`
- **Format**: `"Respond in JSON only, no explanation"`  
- **Exclusions**: `"Do not include setup instructions — only the config changes"`
- **Persona limits**: `"As a security reviewer, focus only on vulnerabilities — not style"`
