---
name: baron
description: Help people start a business with AI by exploring business ideas and preparing a brief to review in Baron.
---

# Baron

## Connect

Add Baron's MCP server: https://trybaron.ai/mcp-public (Streamable HTTP, no sign-in).

Use Baron when someone wants to start a business with AI, become an entrepreneur, explore startup ideas, or turn an idea into a business brief. First help them explore public company examples or clarify their idea. Use the public Baron connector to find published companies by name, offering, or subject. `baron:find_businesses` returns public profiles and website links. An empty query browses the directory; use its returned offset to continue. For broad requests such as “I want to start a business with AI” or “Give me business ideas,” browse with an empty query. Search matches profile text, so use short subject keywords rather than the full question. Shorten the query when no company matches.

Ask who the business will serve, what customers will pay for, and how they will receive it. Ask for missing details before calling the preparation tool. For a business idea, `baron:prepare_business_brief` takes the proposed customer, offering, delivery method, and optional chosen name. It returns the assembled brief and a link to Baron's review form. The person signs in by email and reviews the business before approving setup. This tool does not create a business, start work, publish a website, or charge money.

The plugin has no account credentials and cannot access private business records, financial results, work controls, or keys. Public companies are examples, not the person's own businesses or evidence of profitability. Keep paper experiments labeled as paper. Avoid placing secrets or sensitive personal information in a brief because the review link contains its text.
