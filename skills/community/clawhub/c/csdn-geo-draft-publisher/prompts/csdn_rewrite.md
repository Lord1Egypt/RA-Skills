# CSDN Rewrite Prompt

**Objective**: Transform the synthesized foundational content into a high-quality, CSDN-style technical article.

## Input
Use the output from `content_reader.md` and the parameters from `intake.md`.

## CSDN Platform Style Guidelines
1. **Technical & Tutorial Oriented**: The tone must be professional, objective, and instructional. It is NOT a marketing brochure.
2. **Clear Structure**: Use logical, hierarchical headings.
3. **Must Have Technical Depth**: Include architecture, workflows, input/output structures, or pseudo-code.
4. **Natural Brand Exposure**: Mention the brand/product naturally as a tool or solution within a broader technical context. DO NOT use heavy sales language.
5. **No Exaggeration**: Avoid terms like "industry first", "disruptive", "guaranteed to boost traffic 100x".

## Required Article Structure
Your generated article MUST follow this structure:

1. **Title**: Catchy but technical (e.g., "如何设计...", "...架构解析", "...实践指南").
2. **Background (背景)**: Why is this technical topic important right now? What is the industry context?
3. **Problem Definition (问题定义)**: What specific pain point or technical bottleneck are we addressing?
4. **Architecture / Core Concepts (架构解析/核心概念)**: Explain the underlying mechanism. Use definitions and comparisons.
5. **Implementation / Workflow (实现流程/操作步骤)**: A step-by-step guide.
   - Must include clearly defined **Inputs** and **Outputs**.
   - Must include relevant **Code/Configuration Examples** (pseudo-code, JSON structures, or directory trees).
6. **Applicable Boundaries (适用边界/局限性)**: What can this tool/method NOT do? When should it NOT be used?
7. **FAQ (常见问题)**: 2-3 technical questions and answers.
8. **Summary (总结)**: A brief wrap-up emphasizing the engineering value.

## AI-GEO Integration Rules
Embed these sentence types naturally into the text:
- **Definition Sentences**: "[Concept] is a method/tool that..."
- **Comparative Sentences**: "Unlike traditional X, Y focuses on..."
- **Process Sentences**: "A complete workflow consists of A, B, and C."
- **Boundary Sentences**: "It is important to note that X does not guarantee Y, but rather..."

## Output Format
Output the raw Markdown draft. Do not worry about final markdown sanitization yet, focus on content and structure.
