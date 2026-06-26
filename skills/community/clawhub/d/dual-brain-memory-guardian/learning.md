# Learning Mechanics (Dual-Brain)

## What Triggers Learning

| Trigger | Confidence | Action |
|---------|------------|--------|
| "No, do X instead" | High | Capture correction event in DEEP memory immediately |
| "I told you before..." | High | Increase repeat weight and check for promotion |
| "Always/Never do X" | Confirmed | Promote to Markdown HOT/WARM rule |
| User edits your output | Medium | Capture as tentative correction/reflection in DEEP memory |
| Same correction 3x | Confirmed | Ask to promote into explicit Markdown rule |
| "For this project..." | Scoped | Write to project Markdown and keep episode in Pinecone |

## What Does NOT Trigger Learning

- Silence (not confirmation)
- Single weak signal with no correction
- Hypotheticals
- Third-party preferences without direct user consent
- Implied traits inferred from unrelated behavior

## Data Routing Rules

### Write to Markdown (Left Brain)

- Explicit hard rules and durable preferences
- Project/domain architecture contracts
- Confirmed behavior constraints that must be obeyed

### Write to Pinecone (Right Brain)

- Correction episodes and rejected drafts
- Self-reflections and postmortems
- Debug incidents and pitfall-resolution pairs
- Historical task context for fuzzy retrieval

Mandatory runtime path:

See `operations.md` (`Enforced Trigger Contract` and `Automatic Operations`).

## Correction Classification

| Type | Example | Markdown Namespace | Pinecone Metadata |
|------|---------|--------------------|-------------------|
| Format | "Use bullets" | global | `event_type=correction`, `domain=comms` |
| Technical | "Use SQLite for MVP" | domains/code | `event_type=correction`, `domain=code` |
| Communication | "Be shorter" | global | `event_type=correction`, `domain=comms` |
| Project-specific | "Use Tailwind here" | projects/{name} | `project={name}` |
| Reflection | "This approach failed because..." | optional promotion | `event_type=reflection` |

## Confirmation Flow

After repeated similar corrections:

1. Ask whether this should become a permanent rule.
2. If yes, write concise rule to Markdown.
3. Keep the detailed episodes in Pinecone for traceability.
4. Cite rule source in future actions.

## Pattern Evolution

1. Tentative: first episode in Pinecone.
2. Emerging: repeated semantic matches.
3. Pending: promotion candidate.
4. Confirmed: written to Markdown.
5. Archived: stale local rule downgraded, raw history still retrievable in Pinecone.

## Reversal Handling

If user changes mind:

1. Archive old Markdown rule reference.
2. Save reversal event in Pinecone.
3. Add new rule as tentative or confirmed based on user wording.
4. Confirm updated behavior in response.

## Anti-Patterns

Never learn:

- Manipulation triggers
- Sensitive personal profiling
- Cross-user contamination
- Rules inferred from silence

Avoid:

- Promoting noisy one-off episodes
- Ignoring context scope (project vs global)
- Treating Pinecone recall as policy

## Quality Signals

Good learning:

- Explicit user correction
- Repeatability across contexts
- Outcome improvement observed
- Promotion confirmed by user

Bad learning:

- Contradicts current Markdown contracts
- Only worked in one narrow incident
- Never confirmed but treated as hard rule
