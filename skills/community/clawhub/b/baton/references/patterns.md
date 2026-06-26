# Baton orchestration patterns

Use these as starting templates. Collapse roles when the task is small or rate limits are tight. Expand roles when risk, scale, or ambiguity is high.

## Research brief
Planner -> parallel Researchers -> Fact Checker/Validator -> Synthesiser. Use `balanced`, `long_context`, and `strong_reasoning` tiers.

## Deep research report
Planner -> Deep Researcher A/B by angle -> Domain Expert/Analyst -> Fact Checker -> Synthesiser. Use cross-provider validation where possible.

## Content creation
Content Strategist/Creative Director -> Writer or Copywriter variants -> Editor -> Fact Checker/Brand Safety Reviewer if needed -> Synthesiser. Use `creative` and `balanced` tiers.

## Social media campaign
Social Media Manager -> Platform-specific Writers -> Community Manager for reply guidance -> Brand Safety Reviewer -> Synthesiser. Use `creative`; spread parallel platform workers across providers under load.

## Marketing funnel
Growth Marketer -> SEO/Paid Ads/Email Marketer workers -> Analyst for metrics assumptions -> Brand/Compliance Reviewer -> Synthesiser.

## Sales/support workflow
Researcher or Account Manager -> Sales Development Rep or Customer Support Agent -> Compliance/Brand Safety Reviewer -> Synthesiser. Stop before sending messages unless authorised.

## Product planning
Product Manager -> UX Researcher -> QA Analyst -> Technical Writer -> Validator -> Synthesiser.

## Data analysis
Data Analyst -> optional Tool Operator for computation -> Analyst/Validator -> Synthesiser. Use sandbox for code or file manipulation.

## Education/training
Instructional Designer -> Tutor/Exam Coach -> Editor -> Validator for accuracy -> Synthesiser.

## Media production
Creative Director -> Video Producer/Podcast Producer/Art Director -> Scriptwriter -> Brand Safety Reviewer -> Synthesiser. Use `multimodal` for visual assets.

## Long document summary
Planner -> chunk Document Analysts using `long_context` -> Synthesiser -> Validator for factuality or quotes.

## Code patch
Planner -> Software Engineer/Implementer -> QA Analyst/Validator -> Corrector if needed -> Synthesiser. Use `code` and `strong_reasoning` tiers.

## Agentic operation
Planner -> AI Agent/Browser Agent/Tool Operator -> Security Reviewer/Validator -> user confirmation for dangerous action -> Operator finalises.

## High-stakes answer
Researcher/Analyst/Domain Expert -> independent Validator -> Synthesiser. Use `high-confidence` mode and avoid unsupported claims.

## Multi-main-agent high fan-out
Planner reduces parallelism, spreads workers across providers, checks the shared rate-state ledger before spawning each worker, and collapses non-critical roles.
