# Private credentials for DuoPlus AI

An authorized DuoPlus account/API key and cloud phone are external prerequisites. The skill does not include an account, credits or a device. Python 3.8+ standard library is sufficient; a marketplace installation CLI is not a runtime dependency.

## Supported private channels

1. Have the user configure `DUOPLUS_API_KEY` using the host's secret UI or an existing secure environment injection. The agent must not construct shell commands containing the secret or require permanent shell-profile changes. Never dump the environment to discover credentials.
2. Alternatively, have the user create a private local UTF-8 file containing only the key, using a trusted local editor or secret workflow outside the chat/tool transcript. They provide only its path. Select it with `DUOPLUS_API_KEY_FILE` or `--api-key-file PATH`. No automatic credential persistence or file creation occurs.

On POSIX the file must be a regular file with owner-only permissions (normally 0600). On Windows the user must restrict its ACL to the intended account; the client cannot prove ACL privacy. Keep the file outside the skill directory, public/shared folders and source control. Never print/read its contents with a model-visible tool, attach it to a report, or search arbitrary locations for keys. Do not create one from a key pasted into chat.

Example with a path, not a secret (replace the path with the user's private file):

```text
python "SKILL_DIR/scripts/duoplus_ai.py" --api-key-file "/absolute/private/duoplus.key" list --all
```

On WorkBuddy's independently selected AI script route, its packaged wrapper also accepts the private file path; follow that package's task recipes. Do not treat illustrative output paths or PHONE_ID placeholders as bundled resources. Resolve the client against the installed skill root and save generated images in the user's writable task directory.

Explicit file selection takes precedence over environment defaults; otherwise an injected key precedes an environment-selected file. An invalid explicit file fails closed, without falling back to another credential. Raw-key CLI arguments are not supported: use only secure environment injection or a private file path. Endpoint options accept only the documented official HTTPS destinations, not arbitrary private deployments; requests never follow redirects or use environment HTTP proxies.

## Missing credentials and failures

If setup is missing, do not contact the API or ask the user to paste a key: explain the two private choices and wait for configuration. Never extract OAuth credentials from a connector to supply the script. A successful offline check is not account authentication. A permission failure is not an empty account; never change teams or credentials to bypass it.

Use diagnostics with redacted authentication headers and known secrets. Do not log key-file contents, proxy passwords or Bearer tokens. Raw request bodies may still contain user business data; return only the relevant redacted portion. If a user already posted a key, do not repeat it and recommend revocation/replacement through their control console. No live key, private file, screenshot or account data belongs in a published skill ZIP.
