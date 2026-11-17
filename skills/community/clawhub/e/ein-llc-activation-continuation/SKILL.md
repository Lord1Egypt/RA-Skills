---
name: ein-llc-activation-continuation
description: Acquire the public EIN.LLC activation continuation 0.1.5 archive and continue one caller-supplied business context with discover, assess, prepare, resume, status, show, or cancel. Use when the caller has explicit yes/no/unknown facts and a later process must read the same task. Missing files return the next action. The command does not claim, pay, file, or invent a company.
license: MIT
compatibility: Requires Node.js 22. No npm install. Public reads are anonymous GETs of the pinned descriptor and archive. Caller operations use https://ein.llc with agent_assisted_human. Disposable owner QA stays on an owned loopback.
metadata:
  author: ein.llc
  version: "0.1.1"
  hermes:
    tags: [ein-llc, activation, continuation, no-spend]
  openclaw:
    requires:
      bins:
        - node
---

# EIN.LLC activation continuation

Install this skill, then acquire the already released continuation and point it at caller-owned files. The executable is `scripts/continuation.mjs`. The byte pins are `references/continuation-pin.json`. This skill's license is `references/LICENSE.txt`. The continuation archive carries its own MIT license and the vendored `ein-formation-http-client` 0.1.1.

The descriptor field `published` remains false. That is the frozen field. Acquiring the hosted archive does not rewrite it.

## Next action

Acquire the pinned 0.1.5 archive into a new directory:

`node scripts/continuation.mjs acquire --work DIR`

`DIR` must be a new directory. The command does not run npm install and does not execute the archive examples.

Run one existing command against caller-owned files on the canonical service:

`node scripts/continuation.mjs run --caller DIR/ein-activation-continuation --command assess --state STATE.json --task-id TASK --customer-key-file KEY --context CONTEXT.json --base-url https://ein.llc --lane agent_assisted_human`

`discover`, `assess`, `prepare`, `resume`, `status`, `show`, and `cancel` are the continuation commands. `http` is the default transport. `mcp`, `a2a`, and `a2a-rest` are selected with `--transport`. A2A catalog reads need `--catalog-transport http`. Omitting `--lane` selects `agent_assisted_human` for `https://ein.llc` and `disposable_owner_qa` for an owned loopback.

Assess reads `ein.supplied-context.v1` from `--context`. The fields `hasUsEntity`, `hasEin`, `providerRequiresUsEntity`, `providerRequiresEin`, and `jurisdictionKnown` are each `yes`, `no`, or `unknown`. `selectedState` is the supplied state name, for example `Wyoming`. Task prose does not infer a business prerequisite. A missing file returns `missing_input` and the next action.

Prepare needs `--intended-email-file`. The claim URL stays in the mode 0600 continuation file until `show --show-claim-url`. That handoff is for the intended human. This command does not claim, pay, attest, register, or file.

A later process uses the same `--state`, `--task-id`, and `--customer-key-file`. `resume` replays the stored operation. `status` needs a human-issued `--grant-file` and `--grant-origin`. Pending status stays unpaid.

The ordinary service origin is `https://ein.llc` with `agent_assisted_human`. The caller supplies the context, customer key, recipient, and task id. Claim, payment, attestation, and filing stay with the authorized human. A pending case stays unpaid. Owned loopback receiving uses `http://127.0.0.1:PORT` or `http://[::1]:PORT` with `disposable_owner_qa` only:

`node scripts/continuation.mjs run --caller DIR/ein-activation-continuation --command assess --state STATE.json --task-id TASK --customer-key-file KEY --context CONTEXT.json --base-url http://127.0.0.1:PORT --lane disposable_owner_qa`

## Boundaries

Public acquisition uses `https://ein.llc` and the paths in `references/continuation-pin.json`. `--public-root` accepts only `http://127.0.0.1:port` or `http://[::1]:port` and records local receiving. A redirect is followed only when it stays on that origin and the pinned path. The work directory is the directory you pass. An existing output is left in place.

`disposable_owner_qa` is refused on `https://ein.llc`. `agent_assisted_human` is refused on loopback. `autonomous_machine_purchase` is refused. Any other origin is refused. This command does not invent a customer, a grant, or a paid status.

`--pay`, `--settle`, `--sign`, `--wallet`, `--claim`, `--attest`, `--register`, and `--file` stop before any request. Running this command does not select or prove a native model.
