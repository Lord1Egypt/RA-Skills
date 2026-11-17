## Description:

Generate, regenerate, and validate 2D DXF drawings from Python ezdxf sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubuq-sys](https://clawhub.ai/user/liubuq-sys)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to create, regenerate, and validate 2D DXF files from Python ezdxf sources, including standalone flat drawings and projections from CAD geometry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or edited Python DXF sources are executed locally by the DXF CLI and could perform unintended actions if unsafe code is introduced.

Mitigation: Review Python source files before running the CLI and run only explicit target files from the intended workspace.

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Pin dependencies in the consuming environment when reproducible DXF generation is required.

## Reference(s):

- [ClawHub DXF Skill Page](https://clawhub.ai/liubuq-sys/skills/dxf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell and Python examples, plus generated Python and DXF files when used in an agent workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated DXF artifacts should be validated with ezdxf checks and handed to a CAD viewer when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
