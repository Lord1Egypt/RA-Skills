# GitHub Trending Monitor Template

Purpose: periodically monitor trending GitHub repositories in selected domains (AI, programming languages, infrastructure, etc.) and send summarized updates.

## Suggested Default Schedule

Daily:
- 18:00 local time

## Task Behavior

1. Query GitHub trending repositories or related search results.
2. Select the most interesting 5 projects.
3. Produce a concise summary for each project.

## Output Structure

Title
Short description
Key points
Repository URL

## Delivery

Delivery channel should be chosen by the user through the delivery router.
