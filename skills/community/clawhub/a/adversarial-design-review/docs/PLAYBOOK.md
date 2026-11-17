# Adversarial Design Review — Field Playbook

The longer guide behind `SKILL.md`. Read this when you want the full lens
prompts, reconciliation examples, and the reasoning behind the pattern.

## Why attack the design, not the code

The cost of a defect scales with how far it travels before you catch it:

```
found in the design brief   → minutes to fix (edit a paragraph)
found in code review        → hours (rewrite, re-test)
found in a headless emulator → a debugging session (no printf on the wire)
found in production          → data loss / a level-triggered IRQ storm in the field
```

A design is a paragraph. A device driver is 300 lines of register pokes you
can't single-step easily. Attacking the paragraph is the cheapest possible
place to be wrong. And because the attackers must read the real prior-art
code, their "this is already correct" verdicts are load-bearing too — they
tell you the risky parts are sound, so you implement without second-guessing.

## The four steps, in practice

### 1. Write the brief like an attacker's target

A good brief is concrete enough to bite. Include:

- **Environment invariants**: single CPU or SMP? Interrupts on or off in
  this code path? What does the emulator guarantee (e.g. "QEMU's IDE model
  completes PIO synchronously")? What real hardware quirk applies?
- **Prior art to read**: the files whose idioms the new code must match
  (the existing I/O helpers, the boot/init order, the CI gate style). Name
  them so the agents read real code, not a strawman.
- **The exact plan**: register sequences, struct layouts and sizes, buffer
  bounds, ordering, and the gate strings the CI will grep.

Weak briefs produce weak attacks. "Add a NIC driver" gets platitudes;
"reset via CR=0x10 poll-until-clear, RX ring 8192+16+1500 with WRAP,
CAPR = read_offset − 16, ISR write-1-clear" gets the CAPR-quirk bug found.

### 2. Pick 2–4 lenses; don't over-panel

More agents ≠ better. Pick the lenses the design *touches*:

| The design involves… | Use lens |
|---|---|
| a device (NIC, disk, UART, timer) | **hardware correctness** |
| IRQ handlers, shared state, "interrupts off" | **interrupts & concurrency** |
| a packet/wire format, byte order | **protocol / byte-order** |
| a disk/on-disk format, a superblock, sync | **data format & crash consistency** |
| syscalls, authority, "who is allowed" | **security / capability** |
| the test that proves it | **CI / test integrity** — *almost always include this one* |

Two focused lenses beat five vague ones. The CI-integrity lens earns its
place on nearly every design: the gate that "proves" your feature is itself
a design that can pass for the wrong reason.

### 3. Reconcile honestly

Read every finding and sort it:

- **Blocker / major, confirmed on the real code** → fix before shipping.
- **"Already correct, don't regress"** → note it; these are guardrails
  against a later well-meaning edit.
- **Overstated or refuted** → discard *with a reason*. (Agents sometimes
  attack a strawman or miss that the code already handles the case; that's
  fine, it's cheap.)

You are the judge. The panel surfaces candidates; you decide. A typical run
confirms most choices and surfaces one or two real gaps — exactly the
signal you want.

### 4. Gate every claim on a real runtime signal

Implementation isn't done when it compiles; it's done when a test greps a
real signal:

- a **boot-log line** the code prints when the behavior actually happens,
- a **captured packet** or a **disk readback**,
- a **capless caller denied** line, proving the security gate by attack.

And degrade **honestly**: absent hardware prints its absence and changes
nothing else, gated on both the present and the absent path so neither can
silently rot.

## Full lens prompts

Copy these into the `LENSES` array of the workflow template. Each is a
`focus` string appended to the shared preamble.

**Hardware correctness**
> hardware correctness: register/reset/power-on sequences (which config
> register, the exact reset poll), status-bit semantics (BSY vs DRQ vs
> ready, and never reading data while BSY), UNBOUNDED spins (there must be
> none — every wait bounded), DMA address correctness given the memory map,
> buffer sizing vs what the device may over-write, cache-flush ordering
> (never issue a command while the device is still busy), and what the
> emulator models vs real silicon (a bug invisible under emulation can be
> illegal on hardware).

**Interrupts & concurrency**
> interrupts & concurrency: level- vs edge-triggered lines and the
> consequence for acking (a level line must have the device's status
> register cleared before EOI or it re-fires forever), the IF=0 window
> inside interrupt handlers / syscalls and what therefore cannot run there
> (e.g. a syscall cannot pump its own device's receive interrupt — that
> deadlocks), producer/consumer races on a shared ring/queue between an ISR
> and a consumer, and routing an IRQ line that is assigned dynamically
> rather than at compile time.

**Protocol / byte-order**
> protocol and byte order: every multi-byte field's endianness (network
> order is big-endian; miss one htons/htonl and the parse silently fails),
> header layout and offsets, checksum computation and coverage, minimum
> frame/segment padding, state-machine transitions and what a lost/duplicate
> message does, and parser traps (name-compression pointers, length fields
> that include or exclude a trailing CRC, options walking).

**Data format & crash consistency**
> data format and crash consistency: the write ordering (the commit record
> — superblock, pointer, magic — must be written LAST, after the data it
> describes is durable), torn-write detection (a checksum in the commit
> record AND per-record, so a crash mid-write is caught at restore rather
> than restored as truth), clamping attacker-or-corruption-controlled sizes
> BEFORE allocating (a scribbled length field must not demand a huge
> allocation), and routing restored/received data through the SAME
> validation the live-create path uses so a hostile input can create
> nothing the normal path could not.

**Security / capability**
> security and capability: is authority gated exactly where it must be
> (and proven by a capless caller being denied, as an attack, on every
> run), stale-id / recycled-id use-after-free (an id captured earlier that
> now names a different object), dangling references pinned open by dead
> owners, and ambient reads that expose more than intended (enumerating
> everything when the caller should see only its own).

**CI / test integrity**
> CI and test integrity: can the gate go green for the WRONG reason? Stale
> build artifacts or images surviving between runs (recreate them inside
> the recipe), the tested input being ECHOED into the same log the gate
> greps (so it matches without the feature working — split logs, check the
> content only where it was never typed), non-hermetic external
> dependencies, "count == 0 so skip the check" holes, silent truncation
> presented as full coverage, and timeouts too tight for a slow runner.
> A green gate that proves nothing is worse than a red one.

## Reconciliation examples (from real runs)

- *Blocker, fixed*: "CACHE FLUSH issued while the write is still BSY — the
  emulator silently drops it, so the flush is a no-op; illegal on real
  hardware." → Wait for the write-completion handshake, then one flush per
  run.
- *Confirmed-correct, kept as a guardrail*: "the CAPR−16 quirk and the
  ISR-clear-before-EOI ordering are already right — flag so a reviewer
  doesn't regress them." → Noted in the code comment so a later edit
  doesn't undo it.
- *Refuted, discarded with reason*: "the DNS test is non-hermetic" — true
  in the abstract, but the runner reliably resolves the chosen name and the
  hermetic ICMP gate proves the unicast path independently, so the DNS gate
  ships with the dependency documented rather than removed.

## The post-facto sibling

The same panel pattern runs *after* implementation, over the diff, as a
find → adversarially-verify pipeline: dimension agents find candidate
defects, then a second stage of skeptics tries to *refute* each one
(default to "not a bug" unless the failure concretely reproduces on the
code as written). Only findings that survive refutation are believed. This
catches what the design attack couldn't foresee — and, run on a shipped
shell, once surfaced three genuine kernel races that were then fixed.
