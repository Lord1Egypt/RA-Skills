# ClawHub Publish Copy

## Canonical name
Agent Architecture Evaluator

## Recommended slug
agent-architecture-evaluator

## Short description
Evaluate and optimize an agent or multi-agent architecture.

## Marketplace one-liner
Assess an agent architecture for routing, memory, coordination, observability, latency, cost, and system-level failure modes.

## Long description
Use this skill when the main issue is architectural rather than prompt-level or skill-level.

It is designed for evaluating agent and multi-agent systems that include planners, routers, specialists, tool-use layers, memory systems, approval gates, and coordination flows. The goal is to diagnose structural weaknesses, design architecture-level test scenarios, and prioritize the smallest high-leverage improvements.

This skill is especially useful when a system feels unreliable, expensive, hard to debug, or overly complex, and you need a structured architecture review instead of ad hoc prompt tweaks.

Typical outputs include an architecture inventory, failure mode map, architecture test plan, optimization roadmap, measurement plan, and an architecture recommendation.

## Recommended positioning
Best for evaluating the system design of an agent or multi-agent workflow, not for creating a new skill and not for reviewing only the attached skill portfolio.

## Suggested changelog
Initial release. Adds structured evaluation for agent and multi-agent architectures, including failure-mode mapping, architecture-level testing, optimization planning, and measurement guidance.

## Example publish command
clawhub publish ./skills/agent-architecture-evaluator --slug agent-architecture-evaluator --name "Agent Architecture Evaluator" --version 1.0.0 --changelog "Initial release. Adds structured evaluation for agent and multi-agent architectures, including failure-mode mapping, architecture-level testing, optimization planning, and measurement guidance."
