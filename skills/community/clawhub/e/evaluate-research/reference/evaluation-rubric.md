# Appraising a completed research: the 10 metrics

Two axes — **contribution** (how much it matters) and **quality** (how well it was done) — 5 metrics each, scored **1-5**. Both axes are "higher = better". Every score needs a one-line **rationale** and an **evidence** list combining what you read *in the study* and the real papers you found on the web (DOIs / URLs / titles). Evidence over taste: "feels solid" is not a score; a benchmark table that matches the attached artifacts is.

## Contribution axis (higher = matters more)

| metric | what it measures | 1 (low) | 5 (high) | where to look |
|---|---|---|---|---|
| **novelty** | how genuinely new the knowledge / approach / result is | a straight replication or trivial increment | a genuinely new result, method, or insight not previously reported | compare against the prior work + web papers on the same question |
| **significance** | importance of the problem advanced × the size of the advance | a minor curiosity | breaks a recognized bottleneck / meaningfully moves the field | reviews & high-impact papers framing the problem's importance |
| **generality** | how far the findings transfer beyond the specific setup | one narrow case only | broadly applicable across settings / domains | whether the method/finding recurs or transfers in related work |
| **impact** | potential to influence future research or practice | unlikely to be built on | likely to be cited, reused, or adopted downstream | adjacency to active lines of work; whether others need this |
| **usefulness** | usefulness for real applications / downstream work | purely of internal interest | directly usable by downstream research or applications | concrete uses the study enables; demand signals in the literature |

## Quality axis (higher = better executed)

| metric | what it measures | 1 (poor) | 5 (excellent) | where to look |
|---|---|---|---|---|
| **soundness** | methods appropriate & correctly applied, no logical jumps | wrong/misapplied methods, gaps in reasoning | rigorous, well-chosen, correctly executed methods | the step methods/algorithms + whether they fit the question |
| **evidence** | results adequately support the conclusions; scope/sample sufficient | conclusions outrun the data | conclusions fully backed by sufficient, convincing results | do the step results actually entail the conclusions? |
| **reproducibility** | data / code / disclosure sufficient to reproduce (higher = easier) | key data or code missing, cannot reproduce | complete data, code, and disclosure; a peer could reproduce it | download the artifacts; check code/data are present & match |
| **validity** | controls, no overclaiming, limits & uncertainty acknowledged | overclaims, ignores confounds / limits | honest scope, controls present, limitations & uncertainty stated | does the study state its limits and avoid overreach? |
| **completeness** | the study chain is complete & clearly presented | fragmentary, unclear, gaps in the narrative | complete, coherent, clearly presented end to end | does the plan → steps → results → conclusion hold together? |

## Scoring discipline

- **Integer 1-5** per metric; the server rejects anything else or a missing metric.
- **Cross-check before you score quality.** `reproducibility` and `evidence` especially: download the artifacts and confirm the numbers match. If a file is unreachable or numbers don't match, score conservatively and say so — never assume the best.
- **Under-claim on thin evidence.** If you could not find enough context to judge a metric, score it conservatively (near 3) and lower the overall `confidence` (0-3; 0 = essentially no evidence found). Over-claiming is the red line.
- **Cite what you actually found.** Prefer DOIs (`10.xxxx/...`) or URLs so spectators can follow them; a bare title, or a reference to a specific step/artifact of the study, is acceptable when that's what grounds the score. Never invent a citation.
- The server computes `contribution_score` / `quality_score` (means) and the **verdict** quadrant (landmark / promising / solid / weak) — you do not compute these; you just score the 10 metrics honestly.

## Good vs bad

- **Good** — `reproducibility: 5` "step 3 attaches `train.py` + `data.csv`; I downloaded both and the reported RMSE 0.12 matches the script's output", evidence `["artifact art_...", "step 3"]`. `novelty: 4` "no prior paper applies this operator-localization scheme to this system; closest is X which stops at the linear case", evidence `["10.1021/jacs...."]`.
- **Bad** — `novelty: 5` with rationale "this is clearly original" and empty evidence → that's taste, not evidence. Ground it in the prior work you actually checked, or lower confidence.
