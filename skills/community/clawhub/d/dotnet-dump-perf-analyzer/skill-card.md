## Description:

Provides an end-to-end workflow for diagnosing .NET application performance issues with dotnet-dump, dotnet-counters, dotnet-trace, WinDbg, PAL thresholds, and optional HTML reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexy693](https://clawhub.ai/user/hexy693)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to triage high CPU, GC pressure, memory leaks, thread pool exhaustion, and related .NET application performance issues across ASP.NET Core, ASP.NET on IIS, WPF, and console applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Process dumps, traces, CSV exports, and generated reports may contain sensitive application data.

Mitigation: Run diagnostics only against processes you own or administer, and review generated dump, CSV, trace, and report files before sharing them.

Risk: Diagnostic tooling installed from untrusted locations can introduce supply-chain or operational risk.

Mitigation: Install dotnet diagnostic tools, WinDbg, PerfView, PAL, and related utilities from their official sources.

## Reference(s):

- [.NET diagnostics documentation](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/)
- [.NET downloads](https://dotnet.microsoft.com/download/dotnet)
- [PerfView releases](https://github.com/Microsoft/perfview/releases)
- [PAL performance analysis tool](https://github.com/clinthuffman/PAL)
- [WinDbg](https://apps.microsoft.com/detail/windbg)
- [Windows Performance Toolkit](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/)
- [JetBrains dotMemory](https://www.jetbrains.com/profiler/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Bash, PowerShell, Python, and diagnostic command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include instructions for generating CSV data and interactive HTML performance reports.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
