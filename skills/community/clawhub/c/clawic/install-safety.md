# Install Safety - Clawic CLI

## Destination Rules

- Default install root is `./skills`
- Final path is always `<root>/<slug>/`
- Use `--dir` whenever the workspace already has its own vendor or tool folder

## Before Running `install`

Check these first:
1. Is the slug confirmed?
2. Is the destination directory correct?
3. Is the target folder empty, disposable, or intentionally replaceable?
4. Does the user want inspection first via `show`?

## Overwrite Behavior

Without `--force`, the package writes with exclusive-create semantics.
That means the install stops on the first existing path instead of silently replacing files.

Use `--force` only when:
- the existing folder is disposable
- the user wants a refresh from the registry
- the destination is not a mixed folder with unrelated files

## Safer Review Patterns

For review-first work:

```bash
clawic show pocketbase
clawic install pocketbase --dir ./tmp-skill-review
```

For project-local vendor placement:

```bash
clawic install pocketbase --dir ./tools/skills
```

For explicit refresh:

```bash
clawic install pocketbase --dir ./tools/skills --force
```
