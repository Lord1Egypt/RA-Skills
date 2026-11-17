# General Agent Skills platform adaptation

## Adaptation target

Maintain a platform-agnostic domain core for reuse on Codex, Claude, and other Agent Skills-compatible platforms. Platform differences are placed in the installation, interface, permissions and runtime adaptation layers, and business rules are not copied or forked.

## Three-tier structure

| Layer | Content | Whether to allow changes due to platform |
|---|---|---|
| Portable core |`SKILL.md`, business rules, input and output, guardrails, evaluation cases | No semantic changes allowed |
| Run Adaptation | Script Runtime, Tools/MCP, Files, Network, Sandbox, Manual Approval | Can be mapped, but capability gaps must be reported |
| Distribution adaptation | Installation directory, Zip, plug-ins, interface metadata, version and market copy | Can be maintained separately by platform |

When the platform lacks a certain capability, priority is given to disabling the corresponding path, changing to manual steps, or outputting the adaptation gap; guardrails, acceptance criteria, or evidence requirements are not allowed to be silently deleted.

## Portable core directory

```text
skill-name/
SKILL.md# Required: name, description and core workflow
references/ # Read rules, templates and cases on demand
scripts/ # Optional: deterministic check or conversion
assets/ # Optional: output templates and static resources
agents/openai.yaml# Optional:Codex/ChatGPTinterface and dependency metadata
```In order to be compatible with both Codex and Claude, the default frontmatter only uses`name`and`description`. License, author, version, and compatibility are placed in the repository, market metadata, or platform adaptation layer; optional fields are added only if the target platform clearly supports it and will not break another platform.

## Codex and ChatGPT

### Core compatible

- Codex discovery skills `name`and`description`using`SKILL.md`;
- Can be called via `$skill-name`,`/skills` or implicit matching;
-`references/`,`scripts/`and`assets/`are reserved as needed;
-`agents/openai.yaml` can set the display name, brief description, default prompts and dependencies, and is not part of the core of the domain.

### Installation and distribution

- Project skills:`.agents/skills/<skill-name>/` placed in the current directory or repository level;
-Personal skills: put `$HOME/.agents/skills/<skill-name>/`;
- Multi-skill set: can be installed side by side locally; can be repackaged as a plug-in for large-scale distribution ofCodex/ChatGPT;
- Do not copy skill text to `AGENTS.md`.`AGENTS.md`is suitable for repository conventions, and Skill is suitable for reusable task workflows.

### Notes on this set

- The core files in nine directories can be used directly as independent skills;
-`fde-delivery-router` needs to be able to discover eight sub-skills; if the platform only installs one directory, the router should output the required skill name and handover without forging calls;
- TheNode.jsscript is an enhancement. When there is noNode.jsat run time, it is manually completed according to the check items in `SKILL.md`, and the quality gate will not be skipped.

## Claude

### Core compatible

- Claude's custom Skills also use the directory containing `SKILL.md`;
-`name` Use only lowercase letters, numbers and hyphens to avoid platform reserved words;
-`description` Also write down what to do and when to use it;
- Keep references and scripts loaded on demand, don't cram everything into `SKILL.md`.

### Claude Code

- Project skills:`.claude/skills/<skill-name>/`;
- Personal skills:`~/.claude/skills/<skill-name>/`;
- Claude Code automatically discovers skills based on the file system and does not require uploading through API;
-`agents/openai.yaml` is not a required file for Claude Code, retaining it should not change core execution.

### claude.ai and Claude API

- claude.ai: Package a single skill directory into a Zip upload according to platform requirements;
- Claude API: Upload and obtain `skill_id` through the Skills API, which is referenced together with the code execution environment at runtime;
- It is not assumed that different Claude surfaces will be automatically synchronized, and the same version needs to be published and recorded separately;
- API sandboxes may not have network access and may not be able to install dependencies at runtime. All external packages, network and system commands must be preflighted before release;
- The dependency-freeNode.jsscript of this package still needs to confirm whether the target container provides a compatible runtime. Cannot be run using equivalent manual checks or run in advance during the build phase.

## Other Agent Skills compatible platforms

Minimum fitness check:

| Capabilities | Must be confirmed |
|---|---|
| Skill discovery | Whether to read `SKILL.md`, directory name and frontmatter restrictions |
| Trigger | Explicit, implicit, keyword, skill selector or market installation method |
| Progressive loading | Is it possible to read references on demand instead of cramming them all at once |
| Scripts | Supported runtimes, dependencies, file permissions, timeouts and output limits |
| Tools | Tools/MCP/Plugin Mapping, Authentication, Approval, Returns and Auditing |
| Status | Multi-round status, handovers, versions and long task saving methods |
| Multi-skills | Whether eight sub-skills can be discovered and called by the router |
| Security | Sandboxing, networking, external writing, data retention and supply chain auditing |
| Release | Zip/Directory/Repository, Version, License, Scanning and Update Mechanism |
| Evaluation | Whether to support isolation input, running traces, scorers and failure evidence |

If the platform does not natively support sub-skill calling, use the delivery router as a manual navigator: it only determines the stage and tells the user the next skill that should be installed or called, and does not copy the eight-ring text to the delivery router.

## Adaptation test matrix

| Test | Pass Standard |
|---|---|
| Structure | Platform identification directory, name and description |
| Explicit trigger | Load correctly when specifying skill name |
| Implicit trigger | Typical request trigger, counterexample will not trigger by mistake |
| Progressive loading | Only read references needed for the current task |
| Script | Can run or give explicit compatibility downgrade, does not fail silently |
| Tool Boundaries | Unauthorized tools are not available, high-impact actions require confirmation |
| Consistent output | The same input maintains key decisions, numbers and access control across different platforms |
| Routing | The delivery router selects the correct single ring and does not forge calls when skills are not installed |
| Fallback on failure | Execute the same stop/fallback logic for lack of evidence, override or hard failure |
| Data security | No unauthorized data will be uploaded, the platform’s retention and sharing scope has been confirmed |

Only after the corresponding platform test is completed, the market page will write "Verified Support"; for platforms that have not been tested, it will be written "Based on the open Agent Skills structure design, and need to be pre-checked according to the platform."

## Version strategy

- The Chinese version and the English version use the same skill ID and field version;
- The platform adaptation layer records the adaptation version separately and does not change the domain version number;
- Synchronously update the core packages of all platforms when modifying business rules;
- When only the installation instructions, icons or marketing copy are modified, a new version of the domain rules will not be created;
- Records of each release: core version, platform, surface, scriptability, run reviews and known limitations.

## Output format

Adaptation task output:

```markdown
- Core skills and versions:
- Target platform/surface:
- Installation or upload method:
- Native support capabilities:
- Tools and permissions required for mapping:
- Script/runtime preflight:
- Abilities and downgrades are not supported:
- Test cases and results:
- Release package and known limitations:
```
