# `BIFROST_SKILL_PRIVATEKEY` — missing env or “how do I configure the private key?”

When the CLI or workflow indicates the env var is unset, or the user asks how to set the key:

1. **Detect the user’s shell** (run in the environment where they will use the CLI), e.g.:
   - `echo $SHELL` (path suffix: `bash`, `zsh`, `fish`, …), and/or
   - `ps -p $$ -o comm=` (current process name, e.g. `-zsh`, `bash`).
2. **Tell them to end this agent session** before writing secrets to disk, so they do not paste a raw private key into the chat.
3. **Map shell → init file** (typical):
   - **bash** → `~/.bashrc` (on macOS login shells, `~/.bash_profile` is also common if `~/.bashrc` is not sourced—mention both if relevant).
   - **zsh** → `~/.zshrc`.
   - **fish** → `~/.config/fish/config.fish`.
   - **Other** (e.g. tcsh) → point them to that shell’s standard user config file.
4. **Simple local append** (they run this themselves in Terminal; **never** paste the real key into the agent):

   ```bash
   # zsh example — adjust the file for bash/fish as above
   echo 'export BIFROST_SKILL_PRIVATEKEY=0xYOUR_PRIVATE_KEY' >> ~/.zshrc
   ```

   For **fish**, use `set -Ux` or the fish-native export style in `config.fish` instead of POSIX `export` if they prefer.

5. After editing: **open a new terminal** (or `source` the file) so the variable is loaded, then start a **new** agent session if they still need help.

Remind them: keep the key out of version control, shared dotfiles repos, and screen recordings; rotating the key is recommended if it was ever exposed in chat or logs.
