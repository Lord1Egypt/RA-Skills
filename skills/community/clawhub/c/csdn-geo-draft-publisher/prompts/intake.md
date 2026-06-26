# Intake Prompt

**Objective**: Understand the user's goal, extract core requirements, and define the scope for the CSDN technical article generation.

## Input Data
Read any available user instructions or initial context. 

## Extraction Tasks
Please analyze the user's request and determine the following:
1. **Brand Name**: What is the core brand or product being discussed?
2. **Industry/Field**: What is the technical domain (e.g., AI, Cloud Native, DevOps, Frontend)?
3. **Target Audience**: Who is reading this? (e.g., developers, architects, AI researchers, small business owners).
4. **Target Keywords**: What are the core SEO/GEO keywords?
5. **Article Type**: Is this a technical tutorial, architecture breakdown, engineering practice, or troubleshooting guide?
6. **Tutorial/Architecture Preference**: Is the user leaning towards a step-by-step tutorial or a high-level architecture explanation?
7. **Code Example Requirement**: Do we need to generate pseudo-code, configurations, or directory structures?
8. **Brand Exposure Adjustment**: Does the user want to weaken or strengthen brand presence (to avoid looking like an ad)?
9. **Draft Action**: Does the user explicitly want to generate content suitable for draft filling?

## Output Format
Output a JSON or structured Markdown summary answering the above 9 points. This will guide the downstream `csdn_rewrite.md` step.
