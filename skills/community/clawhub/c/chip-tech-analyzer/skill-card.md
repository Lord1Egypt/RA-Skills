## Description: <br>
Generates CPU and GPU technical analysis reports covering architecture, performance benchmarks, power, thermals, and price-to-performance guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hwl1413520](https://clawhub.ai/user/hwl1413520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, hardware reviewers, and buyers use this skill to collect public CPU/GPU specifications and benchmark data, compare competing chips, and produce structured technical or purchasing reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated analyses can become misleading when benchmark results, prices, drivers, or product availability change. <br>
Mitigation: Check source dates, cite current public data, and review conclusions before using the report for purchasing or planning decisions. <br>
Risk: The included helper script can create report or export files in the working directory. <br>
Mitigation: Run it in an ordinary project workspace and inspect generated files before relying on or sharing them. <br>
Risk: Prompts or report inputs may include unnecessary private purchasing, account, or system details. <br>
Mitigation: Use public chip specifications and benchmark data where possible, and omit private details unless they are required for the analysis. <br>


## Reference(s): <br>
- [Chip specification database](references/CHIP_DATABASE.md) <br>
- [Benchmark guide](references/BENCHMARK_GUIDE.md) <br>
- [Analysis report template](assets/templates/analysis_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional JSON exports and Python helper code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include comparison tables, benchmark summaries, scoring guidance, and generated local report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
