## Description:

Create and manage local RPM YUM/DNF repositories with metadata generation, incremental updates, multi-architecture support, syncing, and GPG signing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill for RPM repository operations, including creating YUM/DNF repositories, updating metadata, syncing mirrors, organizing multi-architecture repositories, and applying GPG signing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup examples include destructive file deletion commands that can remove repository metadata or packages if paths are substituted incorrectly.

Mitigation: List target files first, confirm repository paths, keep backups, and avoid wildcard or recursive deletion commands until reviewed.

## Reference(s):

- [Createrepo Docs](https://github.com/rpm-software-management/createrepo_c)
- [DNF Repo Guide](https://dnf.readthedocs.io/en/latest/)
- [YUM Repo Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/creating_customized_rhel_images_using_the_image_builder_creating_rhel_images_in_hybrid_cloud_environments/assembly_creating-repositories_creating-custom-rhel-images)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English reference content with command examples for RPM repository management.]

## Skill Version(s):

1.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
