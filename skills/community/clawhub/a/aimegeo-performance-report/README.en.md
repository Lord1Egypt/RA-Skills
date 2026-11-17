# Period data checks

Aggregate article, publication, AI-response, and business exports for a selected period into `summary.json` and `指标明细.csv`. The script validates inputs and calculates metrics; the Agent interprets the results using their sources without inferring causation.

See [SKILL.md](SKILL.md), [input fields](references/input-schema.md), and [metric notes](references/metric-notes.md). Fixtures use synthetic data. Run offline checks with:

```sh
python3 -B scripts/self_test.py
python3 -B scripts/aggregate.py --input examples/success/config.json --output report-output
```

## Carry a finding into aimeGeo

Give the Agent a report row with its source and article, publication, or question ID, together with the original facts and article. It can revise evidence-supported text in the existing aimeGeo content task, add an image when useful, and continue through the configured project, account, and platform workflow. If the user already authorized the end-to-end work, continue and retain real receipts. Leave public submissions outside that scope as drafts; do not ask again for existing authorization. A later measurement can repeat the same AI question and record actual answers and native sources. Missing observations remain unknown.

Official resources: [new GitHub repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [official help](https://geo.aimmme.com/docs/). See the current guides for [content creation](https://geo.aimmme.com/docs/content-production/), [covers](https://geo.aimmme.com/docs/cover-generation/), and [publishing](https://geo.aimmme.com/docs/publish-flow/). Package provenance is in [SOURCE-ORIGIN.md](SOURCE-ORIGIN.md). Version 1.0.2, MIT-0.
