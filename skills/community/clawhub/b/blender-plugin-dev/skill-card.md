## Description:

Develop, debug, and upgrade Blender add-ons/plugins and `bpy` scripts with Blender 4.x and 5.x compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seekerzero](https://clawhub.ai/user/seekerzero)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, debug, scaffold, and migrate Blender add-ons or standalone `bpy` scripts while accounting for Blender 4.x and 5.x Python API changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted add-on metadata can be embedded into generated Python scaffold files and later executed by Blender.

Mitigation: Use trusted metadata, review generated files before enabling the add-on, and prefer scaffold code that serializes metadata with safe Python literals such as repr().

## Reference(s):

- [Blender 4.x to 5.x Compatibility Notes](references/blender4_to_5_compat.md)
- [Blender Script Generation Patterns](references/script_generation_patterns.md)
- [Blender 4.0 Python API release notes](https://developer.blender.org/docs/release_notes/4.0/python_api/)
- [Blender 5.0 Python API release notes](https://developer.blender.org/docs/release_notes/5.0/python_api/)
- [Blender 4.0 API changelog](https://docs.blender.org/api/4.0/change_log.html)
- [Blender 5.0 API changelog](https://docs.blender.org/api/5.0/change_log.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated Blender add-on files, migration patches, validation commands, and compatibility guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
