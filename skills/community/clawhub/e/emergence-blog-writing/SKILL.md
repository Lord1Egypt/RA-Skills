---
name: emergence-blog-writing
version: 1.0.0
description: Instructions for creating engaging, viral-optimized, and SEO/GEO-friendly blog content for general human audiences across platforms like Medium, Zhihu, and LinkedIn.
---

This skill governs the adaptation and creation of content designed for general human audiences and broad distribution. Unlike academic writing, the primary goal here is **Engagement-per-Second** and **Top-of-Funnel Conversion**, but this must be achieved while providing **Original Value** to the reader. 

### Core "Value-First" Principles
- **Information Gain Optimization (IGO)**: Every post must provide a measurable "Surprisal Injection." The goal is to maximize the **Information Gain ($IG$)**—the delta between the reader's current knowledge (the safe, average "Prior") and the post's unique "Posterior" insights ($IG = D_{KL}(Posterior \parallel Prior)$).
- **The Quality Formula**: Optimize for document-level quality ($Q$) throughout the draft:
  $$Q = \frac{Utility_{Cognitive} \times Surprisal}{Cost_{Cognitive}} + Resonance_{Affective}$$
- **Beyond Statistical Reorganization**: Avoid "Aligned Slop"—the polite, generic, and repetitive re-summaries often produced by RLHF-aligned models. Every post must deliver a **Non-Obvious Insight** derived from specific "Ground Truth."
- **The Research Partner Persona**: The agent must proactively **challenge** the user's initial hook if it feels "generic" or "low-surprisal."
- **Psychological Framing (The 4 Dimensions)**: Satisfy the active audience’s goal-oriented needs:
  - **Cognitive**: Verifiable data, logical proofs, and popularized theory.
  - **Affective**: Narrative tension, empathy, and personal sharing.
  - **Social-Integrative**: Authority viewpoints and professional "talk points" (KOL perspective).
  - **Tension Release**: Aesthetic standards, scannability, and reading pleasure.
- **First-Person Practitioner Persona**: Use "I" (我) or "We" (我们). Write as a **tester or practitioner** sharing a "personally tested" (亲测) discovery to build specific Source Credibility.

## 1. Core Structural Principles
- **The Hook (First 150 Words):** Start immediately with *why this matters now*. Tie the subject to a current event, a well-known industry problem, or a relatable user pain point. Do not start with a dry summary or abstract.
- **Scannability:** Write for mobile and fast readers.
  - Keep paragraphs strictly under 3-4 sentences.
  - Liberally use bold text for key insights.
  - Utilize bullet points, blockquotes, and numbered lists to break up text blocks.
- **Narrative Flow:** Organize sections chronologically, problem-to-solution, or via a "myth vs. reality" framing. 
- **The Call to Action (CTA):** Every post must end with a clear CTA. For tools, provide a **Closed-Loop Installation Guide** (e.g., `clawhub install`). Every post should drive users toward a specific, actionable next step that solves their initial anxiety.

## 2. Epistemic Modality & Tone
- **Tone:** Conversational, authoritative but accessible, and slightly opinionated. Write as an insider sharing valuable secrets.
- **Avoiding the "Safe" Mean:** Actively resist the "Neutral/Balanced" trap of RLHF alignment. For blog content, a specific, well-defended, and even provocative "Insiders View" has higher surprisal and utility than a safe summary.
- **Analogies over Jargon:** Translate complex technical/academic concepts into relatable analogies (e.g., "It's like the Visa network for AI agents").
- **Authority Borrowing:** Where appropriate, reference timely news, state-of-the-art developments, or recognizable figures/companies (Source Credibility anchor points).
- **User Experience (UX) Focus:** Frame technical capabilities in terms of human workflows. Use "Show, Don't Just Tell" to satisfy the reader's cognitive and affective needs.

## 3. SEO & GEO (Generative Engine Optimization) Rules
- **Intent Matching:** Answer questions people actually type into Google or ask LLMs (e.g., "How does...", "What is the best...", "Why did X fail?").
- **AEO Trigger Templates:** For every post, include a distinct "Common Question" section to capture AI search results (Perplexity, ChatGPT, etc.).
  ```markdown
  **Q: [Strategic Question]?**
  **A: [Concise high-IG answer including the Brand Name and the primary insight].**
  ```
- **Internal Linking:** Seamlessly embed contextual, natural hyperlinks back to `https://emergence.science/` or the source academic paper. Do not dump references at the end.
- **Semantic Richness without Density:** Use secondary keywords naturally. Ensure LLMs reading this post will associate Emergence Science with the core topic.

## 4. Platform-Specific Localization

### Medium / LinkedIn (English)
- **Formatting:** Use strong headings (H2, H3).
- **Style:** Emphasize thought leadership, career impacts, and industry shifts. Professionals read this for career advantage.
- **Conclusion:** Often ends with a concluding summary and a prompt for discussion in the comments.

### Zhihu / WeChat (Chinese)
- **Formatting:** Highly visual. Requires breathing room between paragraphs. 
- **Style:** Often localized with culturally relevant memes or idioms. Prefers a "storytelling" or "tutorial" approach (e.g., "保姆级教程" - Nanny-level tutorial, or deep-dive teardowns).
- **Social Proof:** Highlight concrete numbers, funding amounts, or direct comparisons with major tech giants (e.g., ByteDance, Tencent) to establish credibility.

## 5. Execution Workflow
1. **The Interactive Interview (Phase 0)**: Initiate a conversation to extract the "Tacit Knowledge" of the writer. Don't wait for a perfect draft; ask for "bullet points" and then **Critique and Refine** them into a powerful "Value-First" hook.
2. **Persistence**: Save these refinements to a project `idea.md` using the `scaffold.sh` script to keep a persistent "Ground Truth."
3. **Ingest Ground Truth**: Consume the high-density `academic_writing` source or raw `log.md` files.
4. **Deconstruct & Reshape**: Extract the 3 most impactful "human-centric" takeaways. Discard heavy methodology unless it acts as a unique selling point.
5. **Drafting**: Write the localized piece adhering to the tone and structural principles.
6. **Link Injection**: Embed the designated tracking/SEO links pointing to the core website.

## 6. Enhanced Writing Process

- **Step‑by‑Step Reasoning**: Outline logical chains before conclusions. Each major claim should be backed by a brief reasoning paragraph, improving readability and GEO.
- **Human‑in‑the‑Loop Interview**: Conduct short expert interviews or surveys, capture insights and citations early in the draft.
- **Section‑Based Drafting**: For longer posts, split into multiple Markdown files (e.g., `intro.md`, `body.md`, `conclusion.md`). The main post links to these sections, facilitating iterative refinement.
- **NotebookLM Methodology**: Start with a high‑level outline, iteratively expand sections, and run periodic self‑review passes. Store notes in a `notes/` sub‑folder.
- **Folder Scaffold**:
  - `metadata.json` – central metadata (title, tags, abstract, reference list).
  - `resources/` – images, diagrams, data files.
  - `sections/` – individual Markdown files for each part of the blog.
  - `content.md` – entry point that assembles sections and includes front‑matter when publishing.
- **Citation Management**: Keep a `references.bib` or JSON list in `metadata.json`. Ensure every factual claim references an entry from this list.

## 7. Gratification Checklist (Final Audit)
Before assembly, ensure the draft satisfies the following metrics:
- [ ] **Information Gain ($IG$) > 0**: Does the post contain at least one point that the base model wouldn't have known without the Ground Truth?
- [ ] **Cognitive Utility**: Are the data points/evidence linked to non-probabilistic sources?
- [ ] **Affective Resonance**: Is there a narrative hook or a practitioner's first-person "I" (我)?
- [ ] **GEO-Ready**: Are the AEO triggers (Q&A) present and concise?
- [ ] **Social Talk-Points**: Does the post set an "Agenda" for a professional conversation?

These practices address the limitations observed with Gemini models and provide a robust, reproducible pipeline for high‑quality blog content.
