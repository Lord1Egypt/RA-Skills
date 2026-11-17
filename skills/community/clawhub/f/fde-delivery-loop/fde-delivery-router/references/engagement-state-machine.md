# FDE project state machine

## The state is not a linear waterfall

The eight links represent eight types of decision-making responsibilities, which does not mean that all projects can only be completed once in sequence. The following variations are allowed:

| Event | Back to stage | Reason |
|---|---|---|
| New interviews overturn the original question | 1 | Re-establish the boundaries between evidence and questions |
| Client no longer provides data or personnel | 2 | Renegotiation of mutual commitments and scope |
| Acceptance criteria cannot be achieved or tested | 3 | Correct specifications, not left to downstream guesswork |
| Integration/security risks beyond POC | 4 | Change architecture, mock boundaries or discontinue |
| Agents frequently overstep their authority or fail to complete tasks stably | 5 | Narrow responsibilities, tools, and guardrails |
| Evaluation data is underrepresented | 6 | Rebuild the data set and start a new running round |
| Low usage but passing technical indicators | 7 | Research on adoption resistance and workflow embedding |
| Insufficient evidence of commonality | 8→1 | Rediscover productization candidates as hypotheses |

## Parallel rules

- Rings 4 and 5 can be explored in parallel after the PRD is stable, but tools, permissions, data, and environments must be verified against each other before the POC is run.
- The baseline collection of Stage 7 should start in Rings 2 and 3, collect real usage signals in Stage 6, and complete attribution and scaling decisions in Stage 7.
- Security, privacy, legal and procurement pre-screening of high-risk projects can be conducted in advance, but cannot replace the verification of business issues.

## Project termination status

The following conclusions are all valid results:

- The problem is not worth solving;
- The customer is unable to provide the necessary input;
- Unacceptable technology or risk;
- POC does not meet freezing standards;
- Has technical effect but no adoption or business value;
- Only suitable for a single customer and should not be productized.

Preserve evidence, reasons, reusable learning and re-entry conditions upon termination.
