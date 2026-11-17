---
name: Adversarial Design Review
description: Attack a risky design with a multi-agent workflow BEFORE writing the code. Use before implementing anything hard-to-debug or hard-to-reverse — device drivers, on-disk/wire formats, concurrency and interrupt handling, crash-consistency, protocols, or the CI gates that will "prove" it. Spins up specialist agents that each attack the design from a different lens (hardware, protocol/concurrency, security/capability, data-format/crash-consistency, CI/test-integrity), hunting concrete failure scenarios with specific fixes, then you reconcile and implement. Triggers: "design review", "attack this design", "before I build", "is this driver/format/protocol correct", "review before implementing", risky/low-level/systems code.
---

# Adversarial Design Review

## What this is

A structured way to find the blockers in a risky design **before you write
a line of it** — by spinning up a small panel of specialist agents that
each attack the design from a different angle, hunting concrete failure
scenarios with specific fixes. You then reconcile their findings, apply the
real gaps, and implement with confidence.

The payoff is asymmetric: attacking a *design* (a paragraph) costs minutes;
discovering the same flaw after it ships in a *device driver* or an
*on-disk format* costs hours of headless debugging — or silent data loss.
It also **validates the load-bearing choices**, so you don't waste time
second-guessing code that is already correct.

This is not a code review (the code doesn't exist yet). It is a *design*
review, run adversarially, in parallel, before implementation.

## When to use it

Use it before implementing anything **hard to debug or hard to reverse**:

- **Device drivers** — a NIC, disk, UART, timer: register sequences,
  interrupt handshakes, DMA, bounded waits.
- **On-disk / wire formats** — a filesystem, a superblock, a packet layout,
  a serialization scheme, and their **crash-consistency**.
- **Concurrency & interrupts** — anything touching IRQ handlers, shared
  state, lock-free queues, "runs with interrupts off", or scheduler races.
- **Protocols** — byte order, checksums, state machines, retransmission,
  handshakes.
- **The CI gate itself** — the test that will "prove" the feature works is
  a design too, and it can pass for the wrong reason (stale artifacts,
  echoed input, non-hermetic dependencies).

**Skip it** for routine, easily-reversible code (a CRUD handler, a config
change, a UI tweak): the reconciliation overhead isn't worth it. Reserve it
for the pieces where being wrong is expensive.

## The procedure

### 1. Write the design down (one tight brief)

Capture the design as a concrete plan an attacker can bite: the exact
register sequence, the struct layout, the buffer sizes, the ordering, the
gate strings. Include the **environment facts** an attacker needs (single
CPU vs SMP, interrupts on/off in this context, what the emulator/hardware
guarantees, existing prior-art files to read). Vague designs get vague
attacks.

### 2. Launch the panel (parallel, one lens each)

Spawn 2–4 specialists with the `Workflow` tool, each attacking the **same
design** from a different lens. Every agent should:
- Read the *real* code the design extends (prior art, the idioms it must
  match, the boot/init order) — not just the brief.
- Hunt **concrete** defects: a specific input/state → a specific wrong
  output/crash/corruption. No style notes.
- Return each finding with a **specific fix**, ranked by severity.

Pick lenses from the **catalog** below by what the design touches. A
ready-to-run script template is in
[`resources/attack-workflow.template.js`](resources/attack-workflow.template.js).

### 3. Reconcile — apply the real gaps, keep the validations

Read every finding. For each:
- **Real blocker/major** → fix it in the design (or the first
  implementation) before shipping.
- **Confirmed-correct** ("this is already right, don't regress") → note it
  so a later edit doesn't undo it.
- **Overstated / refuted on the real code** → discard, but say why.

The agents will often *confirm* most of your choices and surface one or two
genuine gaps. That confirmation is a feature: it tells you the risky code is
sound and you can implement without hesitation.

### 4. Implement, then gate every claim

Build it, then prove each behavior with a test that **greps a real
runtime signal** (a boot-log line, a captured packet, a readback) — not
just a unit test. And make the feature **degrade honestly** when its
hardware/dependency is absent, gated on both sides (present *and* absent).

### 5. (Optional) Review the diff adversarially too

The same panel pattern works *after* implementation, over the diff, to
catch what slipped through — a find → adversarially-verify pipeline where
skeptics try to refute each finding before it's believed.

## Lens catalog

Pick the lenses the design actually touches:

- **Hardware correctness** — register order, reset/power sequences,
  status-bit polling (BSY vs DRQ vs ready), bounded waits (never an
  unbounded spin), DMA address/alignment/overflow, cache-flush ordering,
  what the emulator models vs real silicon.
- **Interrupts & concurrency** — level vs edge triggering, ISR-clear
  *before* EOI, IF=0 windows and what can't run in them (a syscall can't
  pump its own device's RX IRQ), shared-state producer/consumer races,
  IRQ routing for dynamically-assigned lines.
- **Protocol / byte-order** — endianness on every wide field, header
  layout, checksums, min-frame padding, state-machine transitions,
  name-compression and other parser traps.
- **Data format & crash consistency** — write ordering (commit record
  *last*), torn-write detection (checksums at two layers), bounds-clamp
  attacker-controlled sizes *before* allocating, route restored data
  through the same validation as the live path.
- **Security / capability** — is authority gated where it should be,
  capless-caller-denied proven by attack, stale-fd/recycled-id
  use-after-free, ambient reads that leak more than intended.
- **CI / test integrity** — can the gate pass for the wrong reason? Stale
  build artifacts, echoed input matching the gate string, non-hermetic
  external dependencies, "0 found → skip" holes, silent truncation. A
  green gate that proves nothing is worse than a red one.

## Evidence it works

Applied while building [flaukowski/QuantumOS](https://github.com/flaukowski/QuantumOS)
into a functional OS (2026), pre-implementation attacks caught real
blockers that would each have been painful to find post-ship:

- **ATA disk**: a `CACHE FLUSH` issued while the drive was still `BSY` from
  the write — silently a no-op under the emulator, illegal on real
  hardware. Fix: complete the write handshake first, then one flush per run.
- **RTL8139 NIC**: clearing the device's interrupt-status register *after*
  the shared PIC EOI on a level-triggered line → an interrupt storm. Fix:
  write-1-clear the ISR at the top of the handler, before EOI.
- **Filesystem**: an unlink "is it still open?" scan that counted
  *terminated* processes' stale file descriptors → the file could never be
  unlinked. Fix: only count live processes; clear fds on process destroy.
- **CI gates**: a persistence test that could pass off a *stale disk image*
  from a previous run, and a shell test whose gate string was *echoed by
  the typed command itself* (proving nothing). Fixes: recreate the image
  inside the recipe every run; check the content only in the second boot's
  log, which never types it.

Each of these was a paragraph in a design brief, killed in minutes, instead
of a heisenbug in a headless emulator.

## Companion practices

The review is strongest alongside three habits it assumes:
1. **Every claim is a runtime gate** — CI greps a real boot-log line /
   captured packet / disk readback, not just a passing unit test.
2. **Honest degradation** — absent hardware logs its absence and changes
   nothing else; gate both the present and the absent path.
3. **A post-facto adversarial review** of the diff, using the same
   find→verify panel, for what the design attack couldn't foresee.

See [`resources/attack-workflow.template.js`](resources/attack-workflow.template.js)
for a copy-paste Workflow script, and
[`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) for the longer field guide with more
lens prompts and reconciliation examples.
