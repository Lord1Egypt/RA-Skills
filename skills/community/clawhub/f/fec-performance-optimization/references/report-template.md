#Performance analysis report template

```markdown
# Front-end performance analysis report

> Generation time: YYYY-MM-DD HH:mm
> Target page/process: ...
> Environment: Device, Browser, Network, Branch or Version

## Performance target

- Focus on metrics: LCP / CLS / INP / TBT / bundle size / memory / FPS
- Project budget or target threshold
- User home path and P95 scene

## Baseline data

| Indicator | Current value | Collection method | Remarks |
| --- | --- | --- | --- |
| LCP | ... | Lighthouse / RUM / trace | ... |

## Bottleneck location

- Problems with loading layer, rendering layer, data layer, main thread or resource layer
- Associated files, routes, chunks, components or requests
- Trace, bundle, log or screenshot evidence to support this judgment

## Candidate access control

| Candidate questions | Indicator support | Positioning scope | Front-end verifiability | Conclusion |
| --- | --- | --- | --- | --- |
| ... | RUM / trace / bundle / network | route / component / chunk / request | Yes / No / Collaboration required | investigate / defer / reject |

## Priority

| Priority | Issues | User Impact | Risks |
| --- | --- | --- | --- |
| P0 / P1 / P2 | ... | ... | ... |

## Optimization plan

- Specific changes to the law
- Alternatives
- Maintainability, accessibility and product behavior impacts

## Verification comparison

| Indicators | Before optimization | After optimization | Collection method |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## Residual risk

- No device, network or browser coverage
- Parts that require backend, design, product or infrastructure collaboration
- Suggest monitoring or follow-up tasks
```

After the analysis is completed, save the report to `reports/performance-review-YYYY-MM-DD-HHmmss.md` and inform the user of the report path.
