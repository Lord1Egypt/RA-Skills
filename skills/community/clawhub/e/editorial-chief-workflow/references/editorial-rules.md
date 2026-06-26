# Editorial Rules Reference

## 1. High-value rules extracted from recent work

### 1.1 Chief-editor principle
For Prime Stone's content workflows, act as chief editor, not sole writer.

Operational meaning:
- decompose by business goal
- delegate by function
- retain final acceptance authority
- synthesize outputs into one coherent deliverable

### 1.2 Obsidian vault-path discipline
When the user says the article lives in Obsidian, treat paths as vault-relative until the real vault root is resolved.

Do:
- locate the real vault path first
- create article assets there
- embed with Obsidian-relative links

Do not:
- default to the OpenClaw workspace as the publication target
- generate images into the wrong filesystem and patch later

### 1.3 Publication sequence discipline
Correct order:
1. text draft
2. images/assets
3. embed into final article
4. proof/layout QA
5. user review
6. publish

Reason:
Proof/layout before visual embedding is low-value QA against a non-final state.

### 1.4 WeChat staging rule
Before publication, create a final reviewable file in the target Obsidian directory.
That file must already contain image embeds.
The user reviews that version, not an abstract draft.

## 2. Assignment templates

### 2.1 Structure agent template
Required fields:
- fixed topic
- fixed audience
- fixed channel
- fixed boundaries
- fixed output
- failure conditions

Focus:
- angle
- section hierarchy
- argument order
- key retained facts

Reject if:
- it writes the whole article instead of structure
- it changes the topic
- it drifts into generic advice

### 2.2 Style-optimization agent template
Mission:
Optimize channel fit, not article topic.

Must preserve:
- fixed topic
- fixed audience
- fixed tool/case/object
- factual spine

Allowed:
- title optimization
- hook optimization
- section rhythm
- marketing expression
- CTA polish

Forbidden:
- changing the topic
- replacing the core example
- turning the draft into generic platform commentary

### 2.3 Review agent template
Mission:
Inspect, challenge, and score against acceptance.

Allowed:
- logic checks
- risk spotting
- channel-fit critique
- checklist output

Forbidden:
- stealth rewriting of the entire article
- taking over the writer role unless explicitly requested

### 2.4 Proof/layout agent template
Mission:
Perform final QA on the real final article state.

Checklist:
- no duplicate H1 if frontmatter already contains title
- spacing consistent
- images embedded correctly
- hierarchy clear
- list/quote/code formatting consistent
- obvious publication risks listed

## 3. Common failure patterns

### 3.1 Monolithic execution failure
Symptom:
The lead agent tries to do everything directly.

Why it fails:
It optimizes for local speed instead of business workflow quality.

Correction:
Split by function and keep orchestration at the center.

### 3.2 Wrong-path asset failure
Symptom:
Images or final files are created in the OpenClaw workspace instead of the Obsidian vault.

Correction:
Resolve vault root first.

### 3.3 Early-review failure
Symptom:
Review/layout starts before images are embedded.

Correction:
Treat proof/layout as last QA before publication.

### 3.4 Topic-drift failure
Symptom:
A style agent changes the article subject while trying to improve channel fit.

Correction:
Write the topic and immutable boundaries explicitly in the assignment.

### 3.5 Documentation-smell failure
Symptom:
A public-channel article reads like product documentation or engineering notes.

Correction:
- sharpen the hook
- foreground reader pain and consequences
- cut implementation detail
- keep only credibility-supporting technical detail

## 4. Cross-channel writing standards

### 4.1 Start hard
Good:
- a sharp diagnosis
- a clear contradiction
- a visible pain point

Bad:
- slow setup
- literary warmup
- generic "have you ever" framing when sharper framing is available

### 4.2 Preserve the value anchor before rewriting
Identify what must survive any rewrite:
- the key judgment
- the comparison or framework
- the concrete examples
- the most valuable phrasing if it carries the insight

### 4.3 Write for light-technical readers without writing like documentation
Target state:
- clear, fast, judgment-rich
- valuable for workplace learners who want to use OpenClaw
- technically credible without becoming engineer-only writing
- not overloaded with engineering detail

Reader definition:
- has higher-education-level reading ability
- understands common office software and basic computer concepts
- has basic AI application vocabulary
- wants to learn and adopt useful workflows
- is not the same as a deep technical expert audience

### 4.4 Optimize for mobile reading
Use:
- shorter paragraphs
- explicit contrast
- bullets where helpful
- subheads that carry meaning

## 5. Acceptance checklist for the chief editor

### 5.1 Goal alignment
- does the piece serve the stated business goal?
- is the target audience still correct?
- is the channel fit right?

### 5.2 Boundary discipline
- did any agent change the topic?
- did anyone replace core examples/tools/cases without approval?
- did review stay review, style stay style, structure stay structure?

### 5.3 Deliverable completeness
- does the final article exist in the intended Obsidian directory?
- are images actually embedded?
- has proof/layout reviewed the visual-final version?

### 5.4 Reader experience
- does the hook grab attention quickly?
- is the argument easy to follow?
- are paragraphs too long for the channel?
- is there unnecessary explanation that should be cut?

## 6. Reflection prompts for weak agent outputs

Use these after a failed or weak delivery.

### 6.1 Boundary reflection
- Which role boundary did you cross?
- What did you change that was explicitly fixed?

### 6.2 Goal reflection
- How did your output fail the business objective?
- What reader outcome did you optimize for instead?

### 6.3 Revision reflection
- What must be preserved in the next version?
- What exactly must change in the next version?
- What evidence will show the next version is better?
