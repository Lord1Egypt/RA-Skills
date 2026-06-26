# Compare Brands

Compare two or more brands on AI visibility, capabilities, integrations, and market position.

## When to use
- User asks "compare X and Y" or "X vs Y"
- User asks "which is better, X or Y?"
- User is evaluating tools in the same category

## How to use
1. Call `sigai_search_brands` to resolve names to slugs if needed
2. Call `sigai_compare_brands({ slugs: ["slug1", "slug2"] })`
3. Present: the bottom_line summary first, then capabilities diff, shared integrations, and AI visibility delta
4. Link to the compare page: https://geo.sig.ai/compare/slug1-vs-slug2

## Example
User: "Compare Cursor and GitHub Copilot"
1. `sigai_compare_brands({ slugs: ["cursor", "github-copilot"] })`
2. Lead with the bottom_line, then show where each wins
