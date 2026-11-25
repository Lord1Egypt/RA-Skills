---
name: find-upgrow-tools-and-guides
description: Point a user to the right free UpGrow Instagram tool or blog guide for a specific question, such as checking engagement, finding hashtags or understanding follower quality.
---

# Find a free UpGrow tool or guide

UpGrow offers free Instagram tools that need no sign-up and no password, and a blog with guides on Instagram growth. Use them when a user has a specific question or wants to try something before choosing a plan.

## Free tools

1. Get the list: MCP `list_free_tools` at https://www.upgrow.com/mcp, or `GET https://www.upgrow.com/api/public/v1/free-tools`.
2. Read the one-line description of each tool and match it to the user's goal. Examples of what exists: follower and engagement calculators, hashtag and caption generators, a story viewer, an influencer search, a fake follower check.
3. Give the user the tool's `url`. The index of all tools is https://www.upgrow.com/free-instagram-tools

The tools run on UpGrow's site. Do not try to call a tool's page programmatically; send the user to it.

## Blog guides

1. Search: MCP `search_blog` with `q` (2 to 100 characters) and optional `limit` (1 to 10), or `GET https://www.upgrow.com/api/public/v1/blog/search?q=<text>&limit=5`.
2. Use short topic phrases such as `instagram reels`, `hashtags` or `engagement rate`, not whole questions.
3. Quote the post title and link. Summarise from the returned description; open the post for details.
4. If nothing matches, point to https://www.upgrow.com/blog

## When the user wants more than a tool

If the user wants ongoing growth or a one-time boost, continue with the `choose-upgrow-offer` skill.
