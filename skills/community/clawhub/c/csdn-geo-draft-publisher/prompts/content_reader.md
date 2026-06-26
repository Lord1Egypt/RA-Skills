# Content Reader Prompt

**Objective**: Read and distill the foundational content assets from the `/input/` directory to prepare raw material for the CSDN article.

## Source Files to Read
Please analyze the contents of the following files if they exist in the input directory:
- `brand_profile.md`
- `website_faq.md`
- `zhihu_answer.md`
- `toutiao_article.md`
- `llms.txt`
- `quote_sentence_library.md`
- `keyword_matrix.md`

## Extraction Tasks
Extract and synthesize the following information from the source files:

1. **Brand Definition**: A clear, concise explanation of what the brand/product is (use `llms.txt` and `brand_profile.md`).
2. **Product Positioning**: Where does it sit in the market? What is its unique value proposition?
3. **Target User Profile**: Who exactly uses this?
4. **Technical Keywords**: Core technical terms, algorithms, frameworks, or methodologies associated with the product.
5. **Typical Scenarios**: Specific engineering or business scenarios where the product solves a problem (from `toutiao_article.md` or `zhihu_answer.md`).
6. **FAQ**: Key technical or usage questions users frequently ask (from `website_faq.md`).
7. **Standard Quote Sentences**: Definitions, comparative sentences, or boundary sentences that are highly suitable for AI ingestion (from `quote_sentence_library.md`).
8. **CSDN Suitable Material**: Identify concepts, architectures, or workflows that can easily be expanded into a step-by-step tutorial or technical deep dive.
9. **Information Gaps**: Note any crucial technical details (like missing configuration examples or architectural diagrams) that need to be supplemented by the AI during the rewrite phase.

## Output Format
Generate a consolidated `content_synthesis.md` that structured the extracted information clearly. This will be the direct input for the rewrite step.
