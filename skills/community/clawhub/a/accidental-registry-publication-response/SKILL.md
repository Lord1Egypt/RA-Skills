---
name: "accidental-registry-publication-response"
description: "Accidental ClawHub publish or leaked package files: scope, remove, and verify one affected version."
---

# Accidental registry publication response

Use when a ClawHub skill version accidentally contains private, copyrighted, generated, cached, or otherwise unintended files.

## Contain

1. Do not delete yet. Record the skill slug and exact affected version.
2. Confirm publisher identity with `clawhub whoami`.
3. Inspect CLI capabilities before relying on remembered syntax:
   - `clawhub inspect --help`
   - `clawhub delete --help`
4. Inspect the exact version, not only `latest`:
   - `clawhub inspect <skill> --version <version> --files --json`
5. Record exposed file paths, sizes, hashes, selected version, latest version, and whether exact-version retrieval still works.
6. Check whether a corrected replacement is already latest. A replacement does not remove an older retrievable version.

## Scope Git separately

1. Resolve the skill path and its actual repository root:
   - `readlink -f <skill-path>`
   - `git -C <skill-path> rev-parse --show-toplevel`
2. From that root, test affected paths with:
   - `git -C <repo-root> ls-files -- '<affected-path>'`
   - `git -C <repo-root> check-ignore -v <affected-path>`
3. Only investigate Git history when the files were tracked. Do not infer Git exposure from ClawHub exposure.
4. Avoid a broad `git log --all` before resolving the correct repository root and tracked paths; it can be slow and answers the wrong question in nested repositories.

## Remove

Treat exact-version deletion as irreversible. Obtain explicit user approval before running it.

Use the syntax shown by the installed CLI help:

`clawhub delete <skill> --version <version> --yes`

Do not delete the whole skill when one version is affected. The observed CLI says exact-version deletion is permanent and cannot be restored or republished; publish a replacement first when deleting the current latest version.

## Verify

After deletion:

1. Repeat `clawhub inspect <skill> --version <version> --files --json`.
2. Confirm the affected version and its files are no longer retrievable.
3. Inspect the skill normally and confirm the intended latest version remains available.
4. Recheck the registry independently of local Git state; ignored or untracked local files do not prove registry removal.
5. Report registry exposure, Git exposure, local cache state, and conversation/log exposure as separate findings. Escalate credentials, personal data, or private communications beyond package deletion; required notification, cache purge, access review, or credential rotation depends on the exposed material and registry capabilities.
