# Security and privacy

Do not place credentials in project setup, requirements, task handoffs, logs or
examples. Refer to credential stores, authenticated CLI profiles or environment
variable names. Keep configuration values separate from executable commands.

Before public distribution, export a clean skill snapshot and scan it as
described in the source repository's [publication guide](https://github.com/aminekhettat/engineering-project-manager/blob/main/docs/PUBLICATION.md). Review the files and manifest as well as
the automated findings. Pattern scanning cannot prove the absence of every
secret, personal fact or proprietary detail.

Do not mirror the private development repository to a public service. Deleted
files and author metadata remain in Git history. Publication is a separate
action using a reviewed history-free export.

If a credential was ever disclosed, remove it from the public material and
revoke or rotate it at its issuer. Editing the current file does not revoke a
credential or remove it from previous releases.

For a vulnerability, use the hosting service's private vulnerability reporting
feature when available. Otherwise contact the maintainers through a private
channel they advertise. Do not post exploitable details or real private data
in a public issue. This project does not currently promise a security response
time or independent security certification.
