# Workflow Orchestration

Use this reference when the user wants a one-command investment workflow.

## Goal

Turn multiple separate tools into one practical pipeline:

1. Rank symbols from live market data
2. Allocate capital by risk and market regime
3. Produce a staged execution plan for the best candidate
4. Optionally log the top pick for later review

## When to use

- The user wants a quick decision workflow
- The user provides a basket of symbols and total capital
- The user asks for a ranked list plus allocation and next action

## Output expectations

The workflow should produce:
- ranked assets
- suggested allocation mix
- top pick action and staged size
- optional snapshot record path if logging is enabled
