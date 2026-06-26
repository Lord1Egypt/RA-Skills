# GEO AI Plugin Patterns

This reference file describes common patterns for GEO-aware AI plugins
and tools. Use these patterns as starting points when designing a
plugin catalog with the `geo-ai-plugin-builder` skill.

The patterns below are platform-agnostic but map cleanly to:

- OpenAI tools / function calling
- Claude Tools
- Perplexity and Gemini tool-like integrations
- Internal AI agents in your own stack

---

## 1. Diagnostic / Assessment Tool

**Purpose:** Quickly assess a user's current situation and segment them
into a few actionable profiles or next steps.

**Typical GEO role:** Discovery and early-funnel qualification.

**Good for:**

- "Maturity" assessments (marketing, security, analytics).
- Health checks (site performance, SEO/GEO readiness).
- Fit checkers (ideal plan/product recommendation starting point).

**Key design tips:**

- Limit outputs to a small number of clear segments or scores.
- Always attach a recommended next action.
- Map segments to existing GEO content (guides, playbooks, case studies).

**Example output structure (simplified):**

```json
{
  "segment_id": "intermediate",
  "score": 67,
  "summary": "You have solid foundations but lack automation.",
  "recommended_next_steps": [
    {
      "label": "Implement automated campaign reporting",
      "url": "https://example.com/docs/auto-reporting"
    }
  ]
}
```

---

## 2. Calculator / Estimator Tool

**Purpose:** Turn business inputs into numerical outputs that support
decisions (ROI, pricing, savings, risk).

**Typical GEO role:** Evaluation and decision support.

**Good for:**

- ROI and payback period calculators.
- Cost comparison between plans or vendors.
- "What if" scenario analysis.

**Key design tips:**

- Require only a few high-leverage inputs.
- Make assumptions explicit in the description and output.
- Include fields for uncertainty or ranges when appropriate.
- Point to deeper content for methodology and disclaimers.

**Example input schema (simplified):**

```json
{
  "type": "object",
  "properties": {
    "monthly_spend": { "type": "number" },
    "expected_lift_percent": { "type": "number" },
    "time_horizon_months": { "type": "integer" }
  },
  "required": ["monthly_spend", "expected_lift_percent"],
  "additionalProperties": false
}
```

---

## 3. Recommendation / Matching Tool

**Purpose:** Recommend products, plans, or configurations based on user
preferences, constraints, or behavior.

**Typical GEO role:** Evaluation and conversion.

**Good for:**

- Product finders (ecommerce, SaaS plans, financial products).
- Content recommendation engines (next best article, video, guide).
- Partner or expert matching (consultants, agencies, clinics).

**Key design tips:**

- Normalize preferences into a small set of parameters.
- Return ranked options with reasons and trade-offs.
- Include stable IDs and URLs for tracking and deep links.

**Example response snippet:**

```json
{
  "recommendations": [
    {
      "id": "shoe_123",
      "name": "Marathon Pro Runner",
      "reason": "Best for neutral runners doing high weekly mileage.",
      "url": "https://example.com/products/shoe_123"
    }
  ]
}
```

---

## 4. Workflow Orchestrator Tool

**Purpose:** Guide a multi-step process where the AI assistant and the
user collaborate over several turns.

**Typical GEO role:** Deep engagement, onboarding, or configuration.

**Good for:**

- Onboarding flows (setting up an account or workspace).
- Implementation checklists (migrations, integrations).
- Configuration wizards (complex products or stacks).

**Key design tips:**

- Model each step explicitly and include a `next_step` field.
- Store partial state in a structured way (session or context object).
- Keep each tool call focused on one step or transition.

**Example stateful pattern (simplified):**

```json
{
  "step": "collect_requirements",
  "completed_steps": ["introduction"],
  "pending_questions": [
    "Which CRM do you use?",
    "How many monthly active users do you expect?"
  ]
}
```

---

## 5. Knowledge / Retrieval Tool

**Purpose:** Bring in authoritative, curated content from your corpus
rather than letting the model hallucinate or guess.

**Typical GEO role:** Authority building and accurate answers.

**Good for:**

- Answering detailed FAQs from your docs.
- Pulling in canonical definitions, limits, or policies.
- Linking back to long-form content that supports answers.

**Key design tips:**

- Return stable identifiers and URLs for each piece of content.
- Include short summaries plus "read more" links.
- Indicate content type (guide, API doc, case study, legal).

**Example response snippet:**

```json
{
  "results": [
    {
      "id": "doc_analytics_basics",
      "title": "Marketing Analytics Basics",
      "snippet": "An overview of attribution models and ROAS.",
      "url": "https://example.com/docs/analytics-basics"
    }
  ]
}
```

---

## Naming and description conventions

- Prefer **short, descriptive, action-oriented names**, e.g.:
  - `campaign_performance_analyzer`
  - `shoe_fit_recommender`
  - `roi_savings_calculator`
- In descriptions, explicitly tell the AI **when** to use the tool:
  - "Use this tool whenever the user asks to compare…"
  - "Call this tool when the user provides concrete numbers and wants…"

Clear, consistent naming and descriptions increase the chance that
AI models will choose the right tool at the right time and keep your
brand visible and authoritative inside AI ecosystems.

