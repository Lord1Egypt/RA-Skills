# Hallucination Guide for geo-hallucination-checker

This reference file defines key concepts, patterns, and examples for the
`geo-hallucination-checker` skill. Use it when you need more nuance about
what counts as a hallucination and how to classify different kinds of claims.

## 1. Core definitions

- **Factual claim**: A statement that can be true or false in the real world.
- **Hallucination**: A confident factual claim that is not supported by
  available evidence or that contradicts known facts.
- **Unsupported claim**: A factual statement that might be true but for which
  you cannot see or access evidence in the current context.
- **Problematic claim**: A statement that is misleading, exaggerated, or
  overconfident relative to the evidence.
- **Speculative claim**: A forward-looking or hypothetical statement that is
  acceptable only when clearly labeled as such (e.g., “may”, “could”, “might”).

The practical rule: when in doubt, prefer labeling a claim as
**Unsupported** or **Speculative** rather than silently treating it as true.

## 2. Taxonomy of hallucination patterns

Use this taxonomy to guide your analysis:

1. **Fabricated sources**
   - Non-existent journals, conferences, or organizations.
   - Vague references like “a 2024 study from a leading university” without
     authors, title, or venue.
   - Citations that cannot be traced back to a real publication, given the
     information provided.

2. **Invented statistics**
   - Precise numbers (e.g., “83.7% of users”) with no clear data source.
   - Sample sizes, p-values, or confidence intervals that appear simply as
     decoration.

3. **Overconfident medical, financial, or legal claims**
   - “Clinically proven to cure…”
   - “Guaranteed returns of 30% per year.”
   - “Zero risk of side effects.”

4. **Misuse of authority**
   - Name-dropping famous institutions (e.g., “Harvard”, “MIT”, “World Health
     Organization”) without specific, verifiable details.
   - Claims that rest entirely on “big names” instead of evidence.

5. **Out-of-date or oversimplified facts**
   - Presenting old information as current without context.
   - Ignoring known exceptions or important caveats.

6. **Over-generalization**
   - Turning limited or early findings into universal laws.
   - “Works for everyone”, “in all cases”, “across every industry”.

## 3. Classification guidance

When assigning `status` and `risk_level`, consider:

- **Domain sensitivity**:
  - Medical, financial, legal, and safety-related claims usually warrant
    a higher risk level.
  - Marketing fluff may be lower risk unless it crosses into deception.

- **Specificity and extremeness**:
  - Extreme performance or effect size claims (e.g., “500% faster”, “80% cure
    rate in two weeks”) are high risk without strong evidence.
  - Vague, modest claims (e.g., “many users find this helpful”) are lower risk.

- **Availability of evidence**:
  - If the user provides detailed sources (links, PDFs, citations), prefer
    checking those before labeling something problematic.
  - If tools are restricted and you cannot verify, it is fine to say:
    “This might be true, but appears unsupported given the available data.”

## 4. Example classifications

Example 1:
- Claim: “Clinically proven to reduce depression by 80% in just 2 weeks.”
- Classification:
  - `status`: Problematic
  - `risk_level`: High
  - Reason: Extreme medical effect size, no trial details or citation.
  - Suggested fix: Add real clinical trial details and citation, or downgrade
    to cautious language (e.g., “Some users report feeling better after two
    weeks, but results vary.”).

Example 2:
- Claim: “Used by hundreds of creators worldwide.”
- Classification:
  - `status`: Unsupported (if no data is shown)
  - `risk_level`: Low to Medium
  - Reason: Vague, modest marketing claim; could be true but not proven.
  - Suggested fix: Either supply real usage data or soften language.

Example 3:
- Claim: “A 2026 MIT study in the Journal of Impossible Physics proved a 500%
  increase in performance over all existing CPUs.”
- Classification:
  - `status`: Problematic or Contradicted (depending on context)
  - `risk_level`: High
  - Reason: Suspicious journal name, extreme claim, no accessible details.
  - Suggested fix: Treat as hallucinated until a real, verifiable citation is
    provided; otherwise, remove or replace with a modest, clearly hypothetical
    statement.

## 5. Integration with content rewriting

When rewriting content to be hallucination-safe:

- Preserve the **legitimate core value proposition** where possible.
- Remove or soften claims that:
  - Rely on fabricated or unverifiable sources.
  - Overstate certainty or effect sizes.
  - Could mislead users about safety or guarantees.
- Use cautious language:
  - “may help”, “can support”, “is designed to”, “early results suggest”.
- Make uncertainty explicit instead of hiding it.

The goal is not to make content bland, but to keep it **honest, grounded,
and safe to cite**.

