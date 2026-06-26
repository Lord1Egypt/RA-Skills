# Keyword News Monitor Template

Purpose: monitor news or web updates for specific keywords and push summaries periodically.

## Parameters

Required:
- keyword list

Optional:
- language
- number of items per report

## Suggested Default Schedule

Daily or twice daily depending on user preference.

## Task Behavior

1. Search the web using configured search tools (e.g., Tavily).
2. Filter results related to specified keywords.
3. Select top relevant items.
4. Produce summarized output.

## Output Structure

Headline
Summary
Key insights
Source link

## Delivery

Delivery channel handled by delivery router.
