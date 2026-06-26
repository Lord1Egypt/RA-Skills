## Description: <br>
帮助用户设置带有中国镜像支持的RSS订阅系统，包括安装feed工具、导入RSS订阅源和聚合订阅内容。特别适合部署在阿里云火山云腾讯云上的openclaw使用，本地安装请按操作系统切换。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roryyu](https://clawhub.ai/user/roryyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users in China use this skill to set up RSS aggregation with China mirror configuration, import an OPML feed list, and aggregate subscriptions through the rss-digest skill. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to run sudo package installation and network-based Go module installation commands. <br>
Mitigation: Review commands before execution, run them only on a trusted Linux host, and consider using a container or non-production machine. <br>
Risk: The feed tool is installed with @latest, so future upstream changes could alter installed behavior. <br>
Mitigation: Verify the feed tool source and consider pinning the Go module version before installation. <br>
Risk: The workflow depends on a separately installed rss-digest skill. <br>
Mitigation: Review and verify the rss-digest skill before importing OPML content or aggregating feeds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roryyu/china-rss-feed) <br>
- [Andrej Karpathy recommended RSS source link](https://x.com/zodchiii/status/2034924354337714642?s=46) <br>
- [Go China module proxy](https://goproxy.cn,direct) <br>
- [feed tool module](https://github.com/odysseus0/feed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and OPML content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Linux apt setup steps, Go module installation guidance, rss-digest prompts, and a bundled OPML feed list.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
