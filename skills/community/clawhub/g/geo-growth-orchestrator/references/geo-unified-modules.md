# Unified GEO Modules

Use this reference for full workflow execution or when a user asks to merge, replace, or avoid separate GEO skills.

## Module A: Brand Knowledge Base

Inputs:

- brand materials
- website/source text
- target market
- compliance constraints
- existing brand profile

Outputs:

- `brand_profile.json`
- `brand_profile.md`
- `faq.md`
- `llms.txt`
- missing fields list

Minimum fields:

- brand name and aliases
- business/category
- target users
- service/product list
- scenarios
- selling points with evidence
- FAQ
- contact/channel information
- compliance boundary

## Module B: Doubao Readiness Review

Purpose: evaluate whether supplied brand materials are easy for Doubao-like Chinese LLMs to understand, summarize, quote, and recommend.

Score dimensions:

- brand definition clarity: 20
- target user clarity: 15
- problem/scenario clarity: 15
- structure: 20
- quotability: 15
- recommendation trigger: 15

This is content readiness, not live Doubao ranking. Only discuss real ranking when raw Doubao answer/source evidence exists.

## Module C: DeepSeek Readiness Review

Purpose: evaluate whether supplied materials are easy for DeepSeek-like models to classify, compare, summarize, and include in recommendation/analysis answers.

Score dimensions:

- brand definition clarity: 20
- category clarity: 15
- target user clarity: 10
- problem/scenario clarity: 15
- structure: 15
- quotability/summarizability: 15
- recommendation/comparison trigger: 10

## Module D: Live/Manual GEO Audit

Use natural probes across:

- spontaneous recommendation
- competitor comparison
- buying guide
- direct awareness
- price/channel
- localized use case
- social seeding
- supply chain/authority/regional market

For every probe save:

- question
- model/platform
- raw answer
- source/citation list if available
- checked time
- evidence level
- body mention
- citation mention
- source/answer rank
- alias hits
- competitor hits
- score dimensions

## Module E: Content Gap Analysis

Classify gaps:

- brand entity not recognized
- brand only cited but not explained
- category recognized but brand absent
- competitor dominates answer
- answer lacks purchase/channel clarity
- answer has factual uncertainty
- local scenario missing
- platform/social proof missing
- FAQ or comparison content missing

Each gap must include commercial impact and next action.

## Module F: Content Asset Generation

Generate:

- website FAQ
- `llms.txt`
- quote sentence library
- glossary
- comparison article
- buying guide
- platform seed content
- visual/video brief when needed

Rules:

- Use confirmed facts only.
- Mark unknown facts as `待确认`.
- Keep definitions extractable and quotable.
- Include boundary and non-promise language.
- Avoid "guarantee ranking", "guarantee citation", "industry first", and fake authority claims.

## Module G: Delivery Reports

Client report:

- plain language
- what was checked
- what was found
- what it means commercially
- what to do next

Internal report:

- evidence level
- raw paths
- missing artifacts
- scoring notes
- risk and compliance notes
- tool/API status
- schema validation

## Module H: Retest

7 days:

- check content completion and publication status
- collect platform comments/questions

14 days:

- run light model check on core probes
- compare mention/citation quality

30 days:

- rerun full probe matrix
- compare body mentions, citation mentions, source rank, answer rank, competitor mentions, and answer quality
