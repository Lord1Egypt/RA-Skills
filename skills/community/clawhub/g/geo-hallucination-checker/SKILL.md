---
name: geo-hallucination-checker
description: >
  Detect and annotate hallucinations, unsupported claims, fabricated studies, and incorrect conclusions in text so that AI only cites verifiable, trustworthy content. Use this skill whenever the user asks you to fact-check, validate sources, check for hallucinations, or ensure that generated content is grounded in real evidence, even if they do not explicitly use the word "hallucination".
compatibility: []
---

## Overview

The `geo-hallucination-checker` skill is a hallucination and false-information detection tool.
It helps you review any piece of content (articles, landing pages, product descriptions, FAQs, GEO-optimized drafts, etc.) and:

- Identify **unsupported factual claims**
- Flag **fabricated or suspicious studies, reports, and statistics**
- Highlight **incorrect or overconfident conclusions**
- Suggest **safer, evidence-friendly rephrasings**

The primary goal is to ensure that AI systems only cite **truthful, well-grounded content** and clearly mark anything that looks like hallucination risk.

Use this skill aggressively whenever there is any risk that the model might invent data, sources, or conclusions.

## When to use this skill

Use `geo-hallucination-checker` whenever:

- The user asks you to **fact-check, verify, or validate** content.
- The task involves **medical, financial, legal, scientific, or technical** claims.
- A draft includes **numbers, percentages, dates, or strong superlatives** (e.g., “the best”, “number one”, “guaranteed”, “clinically proven”).
- A text mentions **studies, universities, journals, or institutions** without clear, verifiable details.
- You are preparing **GEO-optimized content** that might be quoted by AI models and needs to be extra reliable.
- You are asked to **rewrite content to avoid hallucinations or false claims**.

If you are unsure whether hallucinations are a concern, **assume they are** and apply this skill.

## Inputs this skill supports

This skill can be used on:

- A single paragraph or answer
- A long-form article, blog post, or whitepaper
- A product page or landing page draft
- FAQ content or knowledge base articles
- Generated GEO content that will be cited by AI models

The user may also provide:

- **Explicit sources or references** (links, documents, citations)
- **Constraints** (e.g., “do not use external web search”, “only use these PDFs as ground truth”)

Always respect any constraints the user provides.

## Core workflow

When using this skill, follow this workflow:

1. **Clarify the task mode**
   - If the user only asks to “check for hallucinations” or “verify content”, focus on **analysis**.
   - If the user asks you to “rewrite safely”, “make this citation-safe”, or “fix hallucinations”, perform **analysis first**, then produce a **hallucination-safe rewrite**.

2. **Parse the content and extract claims**
   - Read the entire text carefully before judging specific parts.
   - Break the content into **atomic factual claims**. A claim is a statement that could, in principle, be checked as true or false.
   - Ignore purely stylistic or obviously subjective language unless it is presented as an objective fact.

3. **Check available evidence**
   - Prefer **explicit sources provided by the user** (links, documents, citations).
   - If tools are available and allowed, you may use them to consult:
     - Official documentation or first-party sources
     - Well-known reference material
   - If you **cannot confidently verify a claim**, treat it as **unsupported** rather than assuming it is true.

4. **Classify each claim**
   For each atomic factual claim, assign:

   - `status`:
     - `Supported` – clearly backed by the provided sources or well-established knowledge.
     - `Unsupported` – no clear support; could be true, but you do not see evidence.
     - `Problematic` – exaggerated, misleading, overconfident, or very unlikely without strong evidence.
     - `Contradicted` – clearly conflicts with known facts or given sources.
     - `Speculative` – forward-looking, predictive, or hypothetical, presented without clear caveats.

   - `risk_level`:
     - `Low` – unlikely to cause harm or serious misinformation.
     - `Medium` – could mislead, but impact is moderate or limited.
     - `High` – serious risk of harm, legal issues, medical/financial danger, or major reputational damage.

   - `reason`:
     - A short explanation of **why** you assigned that status and risk (e.g., “no source for extreme 500% performance claim”).

   - `suggested_fix`:
     - A concrete recommendation such as:
       - “Remove this claim unless you can provide a real citation.”
       - “Rephrase as a possibility, not a guarantee.”
       - “Add a specific, verifiable source (e.g., link, DOI, report).”

5. **Look for common hallucination patterns**

   Pay special attention to:

   - **Fabricated studies and journals**
     - Vague references like “a 2026 MIT study” or “Journal of Advanced AI Research” with no details.
     - Journals or conferences that do not exist or sound suspiciously generic.
   - **Overconfident medical or scientific claims**
     - “Clinically proven to cure…”
     - “Guaranteed to reduce X by 80%.”
   - **Overly precise unsourced statistics**
     - Very specific percentages, sample sizes, or timeframes with no citation.
   - **Superlatives and absolutes**
     - “The only solution that…”
     - “Best in the world”, “100% safe”, “zero risk”.
   - **Misuse of authority**
     - Name-dropping famous institutions or companies without any concrete evidence.

   Treat these as **high-risk** unless there is strong, clear evidence.

6. **Produce a structured hallucination analysis**

   Always output a clear, structured analysis with two parts:

   1. **High-level summary**
      - Briefly describe:
        - Overall hallucination risk (low/medium/high)
        - The most critical issues to fix before publication or citation

   2. **Claim-level table**
      - Use a markdown table with the following columns:
        - `#` – sequential index
        - `claim_text` – the exact or paraphrased claim
        - `status` – Supported / Unsupported / Problematic / Contradicted / Speculative
        - `risk_level` – Low / Medium / High
        - `reason` – a short explanation
        - `suggested_fix` – what to do about it

   Example structure (illustrative, not prescriptive content):

   | # | claim_text | status | risk_level | reason | suggested_fix |
   | - | ---------- | ------ | ---------- | ------ | ------------- |
   | 1 | “Clinically proven to reduce depression by 80% in 2 weeks” | Problematic | High | No specific clinical trial or citation provided; extreme effect size is unlikely without strong evidence. | Add concrete trial details with citation or downgrade to cautious, non-clinical language. |

7. **(Optional) Hallucination-safe rewrite**

   If the user explicitly requests a rewrite or safer version, after the table:

   - Provide a section titled **“Hallucination-safe version”**.
   - Rewrite the original content:
     - Remove or soften high-risk claims.
     - Replace overconfident language with cautious, transparent wording.
     - Explicitly signal uncertainty where facts are not known (e.g., “Some users report…”, “Early results suggest…”).
   - Do **not** invent:
     - Study names, DOIs, journal titles, or URLs.
     - Exact statistics or dates you cannot justify.
   - If a strong claim is important but currently unsupported, suggest a placeholder note such as:
     - “[Insert verified statistic with citation here]”

## Constraints and safety rules

- **Never invent sources.**
  - Do not fabricate papers, DOIs, journal names, or institutional reports.
  - If you are not sure a source exists, treat the claim as unsupported or problematic.

- **Err on the side of caution.**
  - It is better to mark a real claim as “Unsupported” than to let a hallucinated claim pass as fact.

- **Separate facts from marketing.**
  - Marketing language is acceptable **only if** it is not masquerading as hard evidence.
  - When in doubt, suggest softer, more honest language and disclose uncertainty.

- **Respect user constraints about tools and data.**
  - If the user forbids external web search or asks you to rely only on given documents, follow that rule strictly.
  - Under such constraints, label claims based on what you can see, and explain that some might be true but remain “Unsupported” due to limited data.

## How this skill interacts with other GEO skills

When used together with other GEO-oriented skills (e.g., content optimization, schema generation, or conversion optimization):

- Run `geo-hallucination-checker` **after** content is drafted but **before** finalizing output that might be cited.
- Use the hallucination analysis to:
  - Remove or soften risky claims.
  - Add explicit “needs citation” notes where appropriate.
  - Ensure all structured data (e.g., Schema.org fields) does not encode hallucinated facts.

If there is a conflict between persuasive copywriting and factual accuracy, **prioritize factual accuracy and safety**.

## Output format summary

Unless the user specifies a different format, always:

1. Start with a **short summary**:
   - Overall hallucination risk level.
   - 2–5 bullets with the most important issues.

2. Provide a **markdown table** as described in the workflow section.

3. If requested, append a **“Hallucination-safe version”** that rewrites the content according to your analysis.

Aim for clarity and directness so that humans and AI systems can easily see which parts of the text are safe to cite and which require caution or correction.

