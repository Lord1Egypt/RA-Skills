# Output Templates

Use these templates as the default output shape.

Use the full template when the user asks for a blueprint/review explicitly, or when ambiguity, risk, or hybrid classification makes the extra structure valuable.

For quick asks, compress to:
- purpose or inferred intent
- classification
- short classification reasoning
- top design consequences or highest-priority improvements
- only the unresolved questions that could materially change the answer

## Design Blueprint Template

### 1. Purpose
One-sentence statement of what the CLI is for.

### 2. Classification
- Primary role:
- Primary user type:
- Primary interaction form:
- Statefulness:
- Risk profile:
- Secondary surfaces:
- Confidence level:
- Hybrid notes: (if subcommands or surfaces span multiple roles, note the split here; omit if not applicable)
- Evolution trajectory: (if the CLI is evolving toward a different type, note the direction; omit if not applicable)

### 2b. Classification reasoning
State why this classification was chosen. Specifically address:
- Why this role and not a plausible alternative.
- If there is classification tension, state it and explain how it was resolved.
- If interaction form could be confused with role, clarify the distinction.

### 3. Primary design stance
State the central optimization target in one paragraph.
Also state what the CLI is **not** trying to be.

### 4. Command structure
State the recommended command shape and why.
Do not list commands without explaining how the classification drives the shape.

### 5. Input model
State whether the CLI should be:
- flags-first
- raw-payload-first
- dual-track
- interactive-first

Explain the reason.
If there is a machine path, state where it belongs and where it does not.

### 6. Output model
State the recommended output defaults.
State the primary output surface.
State the secondary output surfaces.
If structured output exists, state the expected contract level.
Per-surface contract details (who, what, strong-vs-convenience) belong in §11, not here.

### 7. Help / discoverability / introspection
State the expected level of:
- help/examples
- discoverability
- describe/explain
- schema / fields support

### 8. State / session model
State whether the CLI needs:
- session identity
- resume/fork
- attach/detach
- history/transcript
- state inspection

If the CLI is mostly stateless, say so explicitly and avoid inventing session semantics.

### 9. Risk / safety model
State the expected guardrails:
- low-risk operations:
- medium-risk operations:
- high-risk operations:
- confirm:
- dry-run:
- impact preview:
- audit:
- sanitization:

### 10. Hardening model
State the expected validation and defensive design level.
If machine-readable surfaces exist, mention:
- field stability
- selector ambiguity rules
- exit-code expectations
- timeout / retry / idempotency expectations where relevant

### 11. Secondary surface contract
§6 establishes what surfaces exist and their defaults. This section specifies the contract for each.
Describe secondary human or machine surfaces explicitly.
For each important secondary surface, state:
- who it is for
- what it is for
- whether it is a strong contract or a convenience layer

### 12. v1 boundaries
State explicitly:
- what v1 should include
- what v1 should defer
- what would be premature abstraction

### 13. Direction for implementation
State:
- what to optimize for
- what not to optimize for
- acceptable patterns
- what would be a category mistake

---

## Review Template

### 1. Inferred intent
State what the CLI appears designed to do.

### 2. Classification
- Primary role:
- Primary user type:
- Primary interaction form:
- Statefulness:
- Risk profile:
- Secondary surfaces:
- Confidence level:
- Hybrid notes: (if subcommands span multiple roles, note the split here; omit if not applicable)
- Evolution trajectory: (if the CLI is evolving toward a different type, note the direction; omit if not applicable)

### 2b. Classification reasoning
If the classification involved tension or ambiguity, explain the resolution:
- Why this primary role and not a plausible alternative.
- If the CLI straddles two roles, explain where the center of gravity lies and why.
- If interaction form could be confused with role, clarify the distinction.
This section may be omitted when the classification is straightforward and high-confidence.

### 3. Evidence
List the evidence used:
- help output
- command structure
- code paths
- output contract
- docs/tests
- runtime behavior

### 4. What fits the category well
List strengths relative to the inferred category.

### 5. Classification mismatches
List places where the CLI appears designed like the wrong kind of CLI.
Keep true category mistakes separate from ordinary implementation weakness.

### 6. In-category design weaknesses
List places where the CLI is the right type but executed weakly.
When relevant, explicitly cover:
- discoverability/help
- secondary surface clarity
- structured output contract
- risk separation
- state handling
- v1 boundary discipline

### 7. Highest-priority improvements
List the top improvements in ranked order.
Prefer contract-level improvements over generic polish.

### 8. Questions to confirm with the user
Ask only the unresolved questions that could materially change the review.
