# Files and notes

Use this to read or edit text files, write multi-line text safely, or manage notes.

## Read

```bash
agentbox file read report.md
agentbox file read report.md --lines 10:40
```

Use `--lines START:END` for long files.

## Write a whole file

```bash
agentbox file write answer.md --content '# Answer'
agentbox file write answer.md --content '# Answer' --apply
```

The first command only shows `data.diff`. Add `--apply` to write. `data.applied` tells you whether it was written.

## Replace text

```bash
agentbox file replace config.toml --find "debug = true" --replace "debug = false"
agentbox file replace config.toml --find "debug = true" --replace "debug = false" --apply
agentbox file replace notes.md --find "TBD" --replace "done" --all --apply
agentbox file replace report.md --todo 3 --replace "Rocket" --apply
```

- `--find` must match exactly once (spaces and case included). Use `--all` to replace every match.
- `--todo N` replaces the whole `<!-- TODO(N): ... -->` placeholder from `report build`. You do not need to copy the long marker.
- Error `not_found`: the hint names a similar line. Copy the exact text with `file read --lines`.
- Error `ambiguous`: add more surrounding text to `--find`, or use `--all`.
- Error `todo_not_found`: the hint lists the TODO numbers that are left.

## Multi-line text and special characters

Shell quoting breaks text in three ways:

1. In double quotes, `$20` becomes empty. Use single quotes: `'Pro costs $20/month'`.
2. `\n` inside quotes is not a newline. It stays as backslash-n in the file.
3. An apostrophe ends a single-quoted string. Rephrase (`it is`), or use stdin.

Safest: pass `-` and send the text on stdin with a quoted heredoc (`<<'EOF'`). Nothing inside is changed.

```bash
agentbox file replace report.md --todo 2 --replace - --apply <<'EOF'
Nvidia's data-center revenue was $30.8 billion ([nvidia.com](https://nvidianews.nvidia.com/)).
- A second line with "quotes" and $ signs, kept as typed.
EOF
agentbox file write answer.md --content - --apply <<'EOF'
# Answer

Line one.
EOF
```

`--content -` works the same way. One trailing newline is removed.
On Windows PowerShell, pipe a here-string: start with `@'` on its own line, end with `'@`, then `| agentbox file write answer.md --content - --apply`.

## Notes

```bash
agentbox note add 'Starter plan: $10.99/user/month billed yearly' --source https://asana.com/pricing --tag item1
agentbox note list --tag item1
agentbox note list --grep pricing --limit 20
```

- Always give `--source`. A note without a source cannot be cited.
- Tags group notes and decide where `report build` puts them.
- Notes persist between commands. Notes from older tasks may exist: filter with `--tag`.
