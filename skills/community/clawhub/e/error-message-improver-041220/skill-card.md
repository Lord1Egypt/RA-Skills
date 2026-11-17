## Description:

Helps application developers, support teams, SaaS operators, and users rewrite vague errors into clearer messages that explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Application developers, support teams, SaaS operators, and users use this skill to turn unclear error text into practical troubleshooting guidance. It supports tailored answers, reusable checklists or workflows, and verification notes for error-message improvement tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation may cause the skill to appear during general debugging or support requests.

Mitigation: Confirm that the user wants error-message improvement help before applying the workflow to unrelated debugging tasks.

Risk: Troubleshooting inputs may include secrets, tokens, private logs, or sensitive customer data.

Mitigation: Ask users to redact sensitive values before sharing logs or error details unless the information is required and safe to disclose.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [[UI] Improve Loading, Empty and Error States](https://github.com/csxark/CryptoViz/issues/98)
- [OpenShift Impersonation for Multi-Cluster Auth](https://github.com/kiali/kiali/issues/10038)
- [error[vg call] No reference paths found](https://github.com/vgteam/vg/issues/4974)
- [When required resources are down what happens](https://github.com/apache/tooling-trusted-releases/issues/1395)
- [HarmonyOS Developer Community](https://segmentfault.com/brand/harmonyos-next)
- [SegmentFault JavaScript](https://segmentfault.com/t/javascript)
- [SegmentFault TypeScript](https://segmentfault.com/t/typescript)
- [ONES R&D Management](https://ones.cn/?utm_term=ONES%C2%A0%E7%A0%94%E5%8F%91%E7%AE%A1%E7%90%86&utm_campaign=%E9%A6%96%E9%A1%B5%E6%A0%87%E7%AD%BE&_channel_track_key=myqX1C0f&utm_source=%E6%80%9D%E5%90%A6%E8%BD%AC%20ONES)
- [C++ singleton compilation answer](https://segmentfault.com/q/1010000004886164/a-1020000004886445)
- [SegmentFault error-messages](https://segmentfault.com/t/error-messages)
- [Vue custom directive error question](https://segmentfault.com/q/1010000009322969)
- [Hyprland 0.55 announced the switch to Lua for its config files](https://news.ycombinator.com/item?id=49002105)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, or task-specific artifacts such as checklists, workflows, analysis, code changes, shell commands, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, limits, validation notes, and next steps when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
