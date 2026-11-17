## 📌 When to Use This Skill
- Scenario 1 (e.g., "Evaluating a new AI model before deployment")
- Scenario 2 (e.g., "Responding to a prompt injection incident")

## ⚠️ Authorization Limits
- Explicitly state that this skill must only be used on systems you own or have explicit permission to test.
- "Do not produce functional malware or content that violates security for real-world harmful purposes."

## 🎯 Attack Taxonomy
Define the attack categories your skill will test. Example (inspired by real frameworks):

- **Direct Injection**: User input that overrides system policies.
- **Indirect Injection**: Hostile content in documents, web pages, or tool outputs.
- **Jailbreak**: Role‑playing, hypotheticals, encoding, obfuscation.
- **Tool Abuse**: Forcing the agent to use tools (e.g., shell, browse) outside its intended scope.
- **Data Exfiltration**: Attempting to extract system prompts, secrets, training data.
- **Agent Hijack**: Overwriting the agent's plans, calling unauthorised sub‑agents.
- **Resource Exhaustion**: DoS attacks via token bombs or recursive calls.

## 🧪 Evaluation Workflow
Provide a clear step‑by‑step process for each test:

1. **Mapping** – Identify model, system prompt, tools, memories, and output sinks.
2. **Threat Modelling** – Create a threat model for every identified surface.
3. **Corpus Building** – Generate an attack set (`attacks.jsonl`) with IDs, techniques, payloads, and severity.
4. **Execution** – Run the test harness and log results (pass/fail/partial).
5. **Scoring** – Calculate attack success rate and any "blast radius".

## 📊 Expected Outputs
List the deliverables the skill should produce:

- `surface.md` – Mapped attack surface.
- `threats.md` – Threat model.
- `attacks.jsonl` – Attack corpus.
- `results.csv` – Test results.
- `report.md` – Final vulnerability report with recommendations.
