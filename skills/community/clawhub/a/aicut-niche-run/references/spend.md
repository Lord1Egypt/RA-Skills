# The spend guard

The CLI enforces the order in the SKILL.md (estimate, tell the user, wait for the go, then spend), but a guard cannot read a conversation. It stops accidents; it does not stop an agent that passes `--max-tokens` on its own. Do not treat it as a security control.

| | no `--max-tokens` | `--max-tokens N`, quote at most N | quote over N |
| --- | --- | --- | --- |
| at a terminal | asks y/N | asks y/N (no question with `--yes`) | refuses (exit 4) |
| no terminal | refuses, even with `--yes` (exit 2) | GO | refuses (exit 4) |

- In a pseudo-terminal the CLI believes a person is there and asks y/N, which blocks an agent: pass `--max-tokens <quote> --yes` (both), after the user's go.
- A price the balance cannot pay is refused before anything is charged, with the top-up link https://www.aicut.pro/billing.
- On most paid commands a create that gets no answer is replayed once with the same idempotency key, so it cannot be bought twice; the fire, the cast portraits and a scene change are sent once and never replayed. If it still gets none the CLI says the outcome is unknown and names the list command to check before trying again.
- `aicut story fire` also needs `--confirm-fire`, and `aicut post publish` needs `--confirm-publish`; without a terminal both refuse without their flag (at a terminal they ask y/N), and nothing is charged or posted.
- A local file given to a command that is priced from the media itself (the `transform` family) is uploaded before the quote, even with `--estimate`. The upload costs no tokens.
