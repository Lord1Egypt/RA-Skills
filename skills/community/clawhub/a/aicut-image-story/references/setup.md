# Setup and exit codes

## Install and sign in

```
npm i -g aicut-cli      # Node 20 or newer
aicut login         # opens the browser and the user approves (--no-browser prints the address instead)
aicut account       # who is signed in, the plan and the token balance
```

`aicut login` stores a session on this machine only. `aicut logout` deletes it locally and prints where to revoke the CLI on every machine (Connected apps in the account settings).

Add tokens at https://www.aicut.pro/billing.

## Output and exit codes

Results go to stdout; prices, progress and hints go to stderr, so `--json` (the raw API JSON on stdout) stays parseable.

| Exit code | Meaning |
| --- | --- |
| 0 | ok |
| 1 | failed (a job failed, or the request was refused) |
| 2 | usage, including a spend without `--max-tokens` and no terminal |
| 3 | `--wait` timed out: the job is still running, not failed |
| 4 | declined, or the price is over `--max-tokens` (nothing was charged) |

## Finding things

- `aicut models list --type video|image|audio --query <words>` and `aicut models get <model-id>` (fields, flags, prices).
- `aicut list videos|images|audio`, `aicut get <id>`, `aicut wait <id>`.
- `aicut upload <path>` uploads an image or video and prints its url; commands that take a picture or a clip also accept a local path and upload it first.
- `aicut --help` lists every command.
