# Agent guardrails — running container-host-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

## Authorization is not this tool's job — decide it where it belongs

Whether a write should happen is your decision, or the account's. The tool does
not gate it — there is no read-only switch and no approval prompt to configure.
The two right places to control read vs write:

- **The account you connect with.** Give it a Docker socket mounted read-only,
  or a Portainer account without write scope. A write then fails at the server,
  which is the only place the permission actually lives — no skill-side flag can
  be argued around by a model, but a revoked permission cannot be.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Log everything you do, over both MCP and the CLI" | Every operation is audited to `~/.container-host-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. Reversible writes also record an undo token capturing the *prior* state. |
| "Don't invent a value when a field is missing" | The Docker Engine omits keys it has nothing to say about — a created-but-never-started container has no `Status`, a dangling image has no `RepoTags`. Those come back as `null`, never as `""`. An id in particular is `null` when unknown, so a blank string is never mistaken for a real identifier. |
| "Tell me if the log was cut off" | `container_logs` returns `{"lines": [...], "returned": N, "limit": L, "truncated": true/false}`, and `system_events` the same shape. Truncation is measured — one extra line is requested from Docker — not guessed from a length coincidence. |
| "Preserve the ordering / tell me what's most urgent" | `restart_loop_rca` and `resource_pressure_analysis` rank worst-first and carry the measured number (restart count, exit code, CPU%, memory%) in each entry. Priority is in the payload, not implied by list position. |
| "Confirm before anything destructive" | `remove_container`, `prune_images` and `prune_volumes` require a `--dry-run`-able preview plus double confirmation at the CLI. |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a Docker or Podman container host (optionally via Portainer)
through the container-host-aiops MCP tools.

TOOL USE
- Before answering any question about the current host, you MUST call a tool.
  Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher tail instead of treating
  the partial result as the container's complete log. A container that has been
  restarting for hours has far more log history than the default tail shows.
- A null field means Docker did not report that value. Report it as "not
  available" — never infer it. A null id is not a container named "None".
- Report values exactly as returned. Do not normalise, translate, or prettify
  container states, exit codes, or image tags.
- Exit code 0 with a high restart count is a container completing and being
  restarted by policy, not a crash. Do not call it a failure.
- "oomKilled": true is the memory limit being hit — cite it rather than
  guessing at a memory problem from CPU numbers.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert that a container is failing for a particular reason unless the
  log tail or exit-code classification in the result supports it.
- Do not add generic Docker advice that does not follow from the tool output.
- Do not confuse a container id with an image id, a short id with a full one, a
  container name with its image name, or a compose stack with a container.
- Volumes and images are not deleted with the container. Pruning is a separate,
  destructive, and irreversible operation — never fold it into a cleanup
  suggestion casually.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup — the destructive operations on a
container host are unusually cheap to invoke and unusually expensive to undo
(`prune_volumes` deletes data no undo token can bring back):

```bash
# e.g. mount the Docker socket read-only for the container running this tool,
# or use a Portainer account without write scope. Then:
container-host-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export CONTAINER_HOST_AUDIT_APPROVED_BY="your.name@example.com"
export CONTAINER_HOST_AUDIT_RATIONALE="clearing disk on the build host"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the analysis tools —
  `restart_loop_rca` correlates restart counts, exit codes, OOM flags and log
  tails inside one call, so the model does not have to chain a list, an inspect
  and a logs call per container while keeping ids straight.
- **The model ignores later tool results in a long context.** Container logs are
  the big payload here. Ask narrower questions and use `tail` deliberately
  rather than pulling 2000 lines from every container.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

## Verification status

Unlike most of this tool line, container-host-aiops has been **live-verified
against a real Docker 27.5.1 daemon** (socket at `~/.docker/run/docker.sock`):
`doctor`, `overview`, all three flagship RCAs (`restart_loop_rca` genuinely
caught a crash-looping container on the machine; `image_and_volume_bloat`
measured ~2 GiB), and a governed `stop_container` write with its audit row and
undo token landing in the store. Podman and Portainer paths remain mock-only.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Container-Host-AIops](https://github.com/AIops-tools/Container-Host-AIops/issues)
with the model, runtime, and what went wrong.
