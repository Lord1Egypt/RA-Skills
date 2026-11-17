# What to carry

`exclude-list.md` is what stays behind. This is the other half: where to look
when you build the candidate list in backup step 1, and how each entry goes
into staging in step 3.

## Where to look

- **Dotfiles and shell config**: `~/.zshrc`, `~/.bashrc`, `~/.profile`,
  `~/.gitconfig`, `~/.gitignore_global`, `~/.tmux.conf`, `~/.vimrc`,
  `~/.config/nvim`, `~/.config/starship.toml`, `~/.ssh/config` (the config, not
  the keys — those are credentials).
- **Editor and tool config**: `~/.config/gh`, `~/Library/Application
  Support/Code/User/settings.json` and `keybindings.json`, JetBrains
  `*/config/`. AI coding agents (`~/.claude/`, `~/.codex/`, `~/.gemini/`,
  Cursor, opencode …) are their own step — backup step 6 and `ai-agents.md`;
  they are where the surprise gigabytes and a good share of the secrets are.
- **Package-manager config that is not a cache**: `~/.npmrc`,
  `~/.cargo/config.toml`, `~/.gradle/gradle.properties`, `~/.m2/settings.xml`,
  `~/.pypirc`, `~/.condarc`. See `exclude-list.md` for why these travel while
  everything else under the same directories does not. When one of these also
  appears in `credential-locations.md` — most do: `~/.npmrc` usually holds a
  live registry token — it goes in `credentials/`, not `files/`. The credential
  rules win over the config classification.
- **Work**: project directories, notes, documents. Ask where they live if it is
  not obvious from the shell history and recent files.
- **Credential directories**: see `credential-locations.md`.
- **App data the OS guards**: the next section.

## App data the OS guards

On macOS, Mail, Messages, Safari, Photos, and Notes data lives under TCC
protection — a terminal (and therefore you) cannot read it without Full Disk
Access, and granting that for a backup is the wrong trade. The workflow is
**user-export**: the user exports from the app's own UI (Photos → File →
Export; Safari → File → Export Bookmarks; Notes → export per folder) into a
plain directory, tells you where, and that directory is then an ordinary
`files` entry. Propose it in the plan, wait for the export, never suggest
granting Full Disk Access or copying `~/Library/Mail` directly.

## Into staging

Copy with `scripts/stage_copy.py`, not `cp`. `cp` follows a dangling symlink
and fails, which is how one broken link used to sink a whole directory; the
script keeps modes, copies every link as a link, and skips-and-records
unreadable and special files instead of aborting. `cp -Rp` remains the
fallback if python3 is somehow absent.

**Never pre-archive.** No `zip`, no `tar`, no `.tgz` inside staging — the
staging directory itself goes to `envrelay encrypt`, which does the archiving.
A zip inside the backup is double-wrapped, breaks the manifest's
`archive`-path promise, drops symlinks and permissions on the way through,
and cannot be tree-verified. If something arrives *as* an archive (a user
export that came out as `.zip`), either unpack it into staging or carry it as
the opaque file it is — but never create one.
