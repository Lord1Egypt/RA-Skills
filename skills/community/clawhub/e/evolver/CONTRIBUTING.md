## Contributing

Thank you for contributing. Please follow these rules:

- Do not use emoji (except the DNA emoji in documentation if needed).
- Keep changes small and reviewable.
- Update related documentation when you change behavior.
- Run `node index.js` for a quick sanity check.

Submit PRs with clear intent and scope.

### Engineering conventions

- **Spawn child CLIs as `node <entry.js>` — never via a `.cmd` shim, npm symlink, or bare command name.** When launching a harness/tool subprocess (claude-code, openclaw, codex, ...), resolve the JS entry behind the launcher and hand it to `node` directly. Two reasons:
  1. On Windows, `child_process.spawn` without `shell:true` on a `.cmd`/`.bat` throws `EINVAL` since the CVE-2024-27980 fix (Node >=18.20.2 / 20.12.2 / 21.7.3) — this silently broke the auto-exec bridge on Windows.
  2. Across platforms, shims/wrappers can emit warnings or silently exit on some machines. `node <entry>` is zero-shell, deterministic, and passes args via argv (no shell-injection surface).

  `runChild` in `src/gep/execBridge.js` implements this for Windows npm shims (`_resolveNpmCmdShim`: parse the shim's `"%dp0%\<entry>" %*` exec line and rewrite `(bin, args)` -> `(process.execPath, [<entry>, ...args])`), falling back to the original target when it is not a recognized npm shim. POSIX binaries / wrappers spawn natively and are left unchanged. A unit test (`test/execBridgeSpawnNpmShim.test.js`) enforces the parser.

