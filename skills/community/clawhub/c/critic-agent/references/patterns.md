## Critic Agent Integration Patterns

### Pattern 1: Gatekeeper (Synchronous)
Use when output quality is critical and you cannot proceed without approval.

```
[Agent generates output] → [Critic evaluates] → if score >= threshold: deliver
                                               else: reject and revise
```
- Synchronous blocking call
- Guarantees quality before delivery
- Use for: customer contracts, security code, public releases

### Pattern 2: Advisor (Asynchronous)
Use when you want feedback but not a hard block.

```
[Agent generates output] → [Critic evaluates in background] → deliver immediately
                                     ↓
                            [Feedback logged for future improvement]
```
- Non-blocking: deliver first, critique later
- Feedback stored for training data, post-mortem
- Use for: internal drafts, exploratory work

### Pattern 3: Iterative Refinement
Use when multiple improvement cycles are acceptable.

```
[Output v1] → [Critic] → revision → [Critic] → revision → ... → deliver
```
- Each revision incorporates previous feedback
- Can auto-retry up to max attempts
- Use for: important documents, polished content

### Pattern 4: Multi-Critic Consensus
Use for high-stakes outputs where single critic may be biased or error-prone.

```
[Output] → [Critic A] → [Critic B] → [Critic C] → aggregate scores
                                   ↓
                          If consensus >= threshold: deliver
                          If major disagreement: escalate to human
```
- Multiple independent evaluations
- Consensus increases confidence
- Use for: legal documents, executive reports

### Model Selection Guide
- **Default**: Use the same model as the writer agent
- **Elevated**: Use a more capable model (Claude Opus, GPT-4) for nuanced critique
- **Specialized**: Use a model fine-tuned for the domain (code review models, fact-checking models)
- **Budget**: Use a smaller, faster model (Haiku, GPT-4o Mini) for high-volume cases

### Prompt Customization
Modify `scripts/critic-system-prompt.txt` to add domain-specific criteria:

**For code:**
```
Also evaluate:
- Code complexity (cyclomatic)
- Performance characteristics
- Test coverage
- Security practices (OWASP)
```

**For writing:**
```
Also evaluate:
- Argument flow and persuasion
- Tone appropriateness for audience
- Evidence quality and sourcing
- SEO considerations
```

**For data analysis:**
```
Also evaluate:
- Statistical methodology soundness
- Data visualization effectiveness
- Conclusion validity
- Assumption transparency
```

### Threshold Calibration Strategy
1. Run 20-30 outputs through critic with human validation
2. Calculate correlation between critic score and human acceptance
3. Set threshold at point where false positive rate < 5%
4. Review and adjust quarterly

### Logging and Monitoring
Every critique should be logged to `memory/critic-log.json`:

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "task": "Generate API documentation",
  "outputHash": "abc123...",
  "score": 82,
  "verdict": "good",
  "dimensionScores": {...},
  "model": "claude-3.5-sonnet",
  "retryCount": 0,
  "delivered": true
}
```

Use this log to:
- Monitor quality trends over time
- Identify model degradation
- Spot systematic weaknesses in agent outputs
