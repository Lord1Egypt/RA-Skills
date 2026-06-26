# alon-fact-check

`alon-fact-check` is a fact-checking skill for verifying factual claims from a URL or pasted text.

It extracts explicit, verifiable claims, checks them against authoritative sources, and returns a structured report with verdicts, credibility ratings, source links, and key qualifiers.

[简体中文](./README.zh.md)

## Quick Install

```bash
npx skills add alondotsh/alon-skills --skill alon-fact-check
```

## When to Use

Use this skill when the user wants to:

- Verify whether a factual claim is true, false, misleading, or unverified.
- Check a URL, article, post, or pasted paragraph for factual reliability.
- Compare a claim against official, primary, peer-reviewed, or professional fact-checking sources.
- Understand the narrower accurate version of an overbroad or misleading claim.

Do not use it for opinion editing, general research summaries, lifestyle advice, or personalized medical/legal/financial advice.

## Input Types

### URL

For URL input, the skill first reads and summarizes the source page before fact-checking it.

The final report includes:

- `Source Summary`: what the page argues or claims.
- `Summary`: what the evidence shows after verification.

This prevents external search results from contaminating claim extraction.

### Pasted Text

For long pasted text, article-like text, transcripts, or multi-paragraph input, the skill writes a `Content Summary` before extracting claims.

For short direct claims, the summary field is omitted so the report stays compact.

## Workflow

1. Parse the input as either URL or text.
2. Understand the source content when the input is a URL or long text.
3. Extract 1-5 explicit, verifiable claims.
4. Search authoritative sources, including contradiction-oriented searches for controversial claims.
5. Classify each claim as true, misleading, false, or unverified.
6. Assemble a clean final report once, with no duplicated claim sections or mismatched sources.

## Output Shape

The report is conclusion-first:

```text
Fact-Check Report

Source: ...
Source Summary / Content Summary: ...
Overall Assessment: ...
Summary: ...
Source Note: ...

Claim #1
Claim: ...
Verdict: ...
Credibility: ...
Note: ...
Sources:
- Source title [source type / why credible]
  URL
```

For non-English output, labels and wording should match the user's language consistently.

## Summary Quality

The top summary should be useful, not just short.

When relevant, it should include:

- Conditions and scope.
- Baseline or comparison.
- Time frame.
- Approximate magnitude.
- Mechanism.
- Exceptions that change the verdict.

Example:

```text
"Coffee raises LDL" is too broad. The more accurate claim is that unfiltered coffee, especially at several cups per day, may raise LDL because it retains more cafestol/kahweol, while paper-filtered coffee removes most of these diterpenes and has little LDL effect.
```

## Source Handling

Source labels describe source type or why the source is credible. They are not citation numbers and do not replace the claim-level credibility rating.

Each source must directly support or contradict the specific claim it is listed under.

## Files

- `SKILL.md`: Runtime instructions loaded by compatible agents.
- `.gitignore`: Ignores local runtime output and transient files.

## About Alon

These public skills come from Alon's real daily workflows.

Alon is actively exploring the future of agent skills and is open to connecting with people who want to build useful skills.

- GitHub: https://github.com/alondotsh
- ClawHub: https://clawhub.ai/u/alondotsh
- X: https://x.com/alondotsh
- WeChat Official Account: alondotsh
