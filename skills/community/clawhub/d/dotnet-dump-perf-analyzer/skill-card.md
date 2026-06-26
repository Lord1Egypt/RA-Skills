## Description: <br>
End-to-end .NET application performance diagnostics using dotnet-dump, dotnet-counters, dotnet-trace, WinDbg, PAL thresholds, and optional HTML reports for ASP.NET Core, IIS, WPF, and console apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexy693](https://clawhub.ai/user/hexy693) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill to triage .NET CPU, GC, memory leak, thread pool, and system-resource issues, then choose diagnostic commands and reporting steps for Windows, Linux, or macOS applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic dumps, traces, and performance logs can contain sensitive application data, secrets, or personal information. <br>
Mitigation: Collect diagnostics only on systems you are authorized to inspect, prefer short traces or heap-only dumps when sufficient, store outputs securely, redact before sharing, and delete artifacts according to retention policy. <br>
Risk: Installing diagnostic tools from untrusted locations could compromise the host being investigated. <br>
Mitigation: Install only the needed diagnostic tools from official sources and verify the tool source before use. <br>


## Reference(s): <br>
- [.NET diagnostic tools](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/) <br>
- [.NET downloads](https://dotnet.microsoft.com/download/dotnet) <br>
- [PerfView releases](https://github.com/Microsoft/perfview/releases) <br>
- [PAL performance thresholds](https://github.com/clinthuffman/PAL) <br>
- [WinDbg](https://apps.microsoft.com/detail/windbg) <br>
- [Windows Performance Toolkit](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/) <br>
- [JetBrains dotMemory](https://www.jetbrains.com/profiler/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic command sequences and an optional HTML reporting script.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
