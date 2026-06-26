# Submodule Notes

This skill directory is designed to become an independent repository later.

## Current phase

During initial development, keep the skill as a normal directory under the parent project:

```text
skills/arxiv-paper-writer/
```

This avoids prematurely creating a nested Git repository before the skill structure stabilizes.

## Future migration path

When ready to publish independently:

1. Create a new empty remote repository, for example `arxiv-paper-writer-skill`.
2. Copy or move `skills/arxiv-paper-writer/` into a clean standalone directory.
3. Initialize Git in that standalone directory.
4. Commit the skill files.
5. Push to the new remote.
6. Remove the normal directory from the parent repository.
7. Add it back as a submodule.

Example commands after the independent repository exists:

```bash
git rm -r skills/arxiv-paper-writer
git submodule add <REMOTE_URL> skills/arxiv-paper-writer
git commit -m "将 arxiv-paper-writer skill 接入为独立 submodule"
```

Do not run these commands until the remote repository exists and the user confirms the migration.
