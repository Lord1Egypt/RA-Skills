# openclaw-kpass

An [OpenClaw skill](https://docs.openclaw.ai/tools/skills) for working with KeePass KDBX vaults through [kpass](https://github.com/Lanjelin/kpass), a pass-like CLI designed for agents.

The instructions in [SKILL.md](SKILL.md) cover finding, reading, creating, and updating entries, generating passwords, TOTP, and vault credential management. This repository contains the skill, not the CLI.

## Install

1. Install kpass 0.2.0 or newer using [pipx](https://pipx.pypa.io/) and Python 3.11 or newer:

   ```sh
   pipx install 'kpass-cli>=0.2.0'
   kpass --version
   ```

   For an existing installation, run `pipx upgrade kpass-cli`. This skill requires kpass 0.2.0 or newer for `--non-interactive`, `generate --quiet`, and the credential-handling fixes.

2. Install the skill in OpenClaw's shared skills directory (default state directory shown):

   ```sh
   mkdir -p ~/.openclaw/skills
   git clone https://github.com/Lanjelin/openclaw-kpass.git ~/.openclaw/skills/kpass
   ```

   For one agent only, clone into `<workspace>/skills/kpass` instead. With a custom `OPENCLAW_STATE_DIR`, use `$OPENCLAW_STATE_DIR/skills/kpass`.

3. Configure access to your existing vault. Replace these example paths:

   ```sh
   export KPASS_DB="/absolute/path/to/vault.kdbx"
   export KPASS_PASSWORD_FILE="/absolute/path/to/vault-password"
   # If your vault also requires a keyfile:
   # export KPASS_KEYFILE="/absolute/path/to/vault.keyx"
   ```

   The password file must contain the vault password on its first line. Restrict its permissions (for example, `chmod 600` on Unix). `KPASS_PASSWORD` is an alternative to the password file; do not put real passwords in shell history, this repository, or chat.

   Make the binary, environment variables, and vault files available to the process that runs agent commands—not just your interactive shell. Sandboxed execution needs access inside the sandbox too. A skill does not grant filesystem or tool access.

4. Start a new OpenClaw session. Check discovery with `openclaw skills info kpass` and try asking: “Use kpass to find entries matching example.com.”

## Safety

Use a dedicated agent vault containing only the credentials the agent needs, and keep backups before allowing writes. `generate` can replace an existing password and prints it unless `--quiet` is used. Default entry views and XML exports can also expose secrets to tool logs; clipboard access requires a working local GUI and is not a headless secret-delivery mechanism.

The skill instructs the agent to use targeted searches and field reads, use `--non-interactive` and `generate --quiet` for unattended execution, and seek authorization for destructive operations. These are instructions, not enforced access controls. Interactive editing still requires a suitable local session. Review [SKILL.md](SKILL.md) before granting vault access.

Never commit vaults, passwords, password files, or keyfiles. Only authorize deletion or vault credential changes when intended.

## License

[MIT](LICENSE), copyright 2026 Lanjelin. See the upstream kpass repository for its own licensing and documentation.

## Security disclaimer

**An agent with vault access can use—or leak—everything it can unlock.** KDBX encryption protects the vault at rest; it does not constrain OpenClaw after you provide the unlock credentials. The skill's safety rules guide the agent, but **they are instructions, not access controls**.

### Main risks

| Risk | What it means here |
| --- | --- |
| **Secrets enter model context or logs** | `show -p`, OTP output, default entry views, and XML exports can expose secrets through tool results, session history, or logging. Depending on your configuration, they may also reach the model provider. |
| **Prompt injection** | A malicious webpage, message, document, or vault note could persuade the agent to retrieve credentials, send them elsewhere, or alter the vault. Skill instructions cannot reliably prevent this alone. |
| **Whole-vault access** | Giving the execution process the database and unlock credentials effectively grants access to the entire vault—not just the entry the user requested. |
| **Credential exposure on the host** | Unlock passwords in environment variables or password files remain accessible to sufficiently privileged processes. A password file readable by the agent is not a security boundary against that agent. |
| **Unwanted mutations** | An agent can overwrite passwords, delete entries, or change vault credentials. Requests for authorization in the skill are not enforced by kpass. |
| **Plaintext handling** | Interactive editing creates a temporary plaintext file. Clipboards and clipboard managers can retain copied secrets. Neither is an appropriate default for a headless agent. |
| **Shared execution environments** | Agents or users sharing the same OS identity, credentials, and execution environment should not be treated as securely isolated from each other. |

`--non-interactive` prevents prompts; **it does not restrict permissions**. `generate --quiet` avoids one source of secret output; **it does not make other commands secret-safe**.

### Recommended setup

1. **Use a dedicated agent vault.** Never give it your personal password database. Include only credentials you are willing to expose to that agent's execution environment.

2. **Prefer narrowly scoped, revocable credentials.** Use service-specific tokens, limited permissions, and short lifetimes where supported. Avoid primary account passwords, recovery codes, and administrative credentials.

3. **Enforce access outside the skill.** Use a dedicated OS user or sandbox with access only to the intended vault and credential files. Restrict network destinations and command capabilities where practical. OpenClaw's skill dependency check does not grant or limit those permissions.

4. **Keep secret values out of model-visible tool output.** Ideally, an approved helper retrieves a credential and uses it directly for a specific operation, returning only the result—not the credential. This skill does **not** implement such a broker.

5. **Restrict writes unless needed.** Use filesystem permissions or a constrained execution interface for read-only workflows. Keep protected, versioned backups outside the agent's write access.

6. **Review logging and transcript retention.** Prevent secret output from being captured in the first place; redacting it after it has reached a session transcript is too late.

**Storing a password and its TOTP seed in the same agent-accessible vault removes their separation against compromise of that agent.**

This setup is suitable for a dedicated automation vault containing limited, replaceable credentials—not unrestricted access to a personal or administrative vault.
