## Description: <br>
Create and manage local RPM YUM/DNF repositories with metadata generation, incremental updates, multi-architecture support, syncing, and GPG signing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to create, update, synchronize, sign, and troubleshoot local RPM/YUM/DNF repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deletion examples can remove repository metadata or packages if paths or wildcard matches are wrong. <br>
Mitigation: Confirm resolved paths and wildcard matches before deletion; back up repositories or move files aside before removing them. <br>
Risk: Mismanaged GPG signing keys or disabled GPG checks can weaken repository integrity. <br>
Mitigation: Protect signing keys and keep GPG checks enabled except for temporary local testing. <br>


## Reference(s): <br>
- [Createrepo Docs](https://github.com/rpm-software-management/createrepo_c) <br>
- [DNF Repo Guide](https://dnf.readthedocs.io/en/latest/) <br>
- [YUM Repo Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/creating_customized_rhel_images_using_the_image_builder_creating_rhel_images_in_hybrid_cloud_environments/assembly_creating-repositories_creating-custom-rhel-images) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash and INI code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese/English examples for RPM repository creation, synchronization, signing, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
