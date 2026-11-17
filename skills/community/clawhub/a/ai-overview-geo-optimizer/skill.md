# Skill: AI Overview & GEO Optimizer (Generative Engine Optimization)

## Description
This skill provides comprehensive instructions for analyzing, restructuring, and optimizing content specifically for **Google AI Overviews**, **Perplexity AI**, and **ChatGPT Search**. It applies Generative Engine Optimization (GEO) concepts such as Information Gain, Semantic Entity Density, Direct Answer Formatting, and Structured Schema integration.

---

## System Instructions & Protocol

### 1. Direct Answer Extraction Formatting
- Convert primary H2/H3 target query responses into **40–60 word standalone definition blocks** directly underneath the heading.
- Use explicit visual cues like bullet points (`-`), bolded entity terms (`**Entity Name**`), and clear quantitative claims.
- Structure key facts into markdown tables whenever comparative metrics are discussed.

### 2. Information Gain & Semantic Density Injection
- Identify missing **LSI/N-gram entity clusters** relevant to the main search intent.
- Suggest 2–3 authoritative external citations or benchmark statistics based on trusted industry sources (e.g., official documentation, whitepapers).
- Include distinct perspective elements (e.g., "In-depth testing showed...", "Key takeaway:") to boost EEAT signals.

### 3. Structured Data (JSON-LD) Output
Always generate a syntactically valid `<script type="application/ld+json">` code snippet tailored to the content type:
- **FAQPage Schema** for Q&A sections.
- **Article / TechArticle Schema** including author credentials and mainEntity.

---

## Workflow Steps

1. **Analysis Phase**:
   - Parse input text for primary topic and intent.
   - Detect current structural flaws (e.g., buried answers, missing sub-headings, vague statistical claims).

2. **Optimization Output**:
   - **Section 1: AI Overview Executive Summary** (Direct Answer Block).
   - **Section 2: Enhanced Content Layout** (Restructured Markdown with bold entities, tables, and lists).
   - **Section 3: GEO Entity & Citation Strategy** (List of high-value entities & authoritative citation recommendations).
   - **Section 4: JSON-LD Schema Markup** (Fully formatted code block).

---

## Reference Benchmarks
- [Google Search Central - Structured Data](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
- [arXiv: Generative Engine Optimization (GEO)](https://arxiv.org/abs/2311.15520)
- [Google Search Quality Evaluator Guidelines (EEAT)](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//googleguidelines.pdf)
