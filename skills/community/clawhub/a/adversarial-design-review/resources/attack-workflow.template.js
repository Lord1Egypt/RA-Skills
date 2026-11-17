/**
 * Adversarial Design Review — Workflow template.
 *
 * Copy this, fill in DESIGN_BRIEF and pick your LENSES, and run it with the
 * Claude Code `Workflow` tool. Each lens agent attacks the SAME design from a
 * different angle and returns concrete findings with fixes; the script
 * collects them, ranked, for you to reconcile.
 *
 * The agents run in parallel (one barrier). Each is told to read the real
 * code the design extends, hunt concrete failure scenarios (a specific
 * input/state -> a specific wrong output/crash/corruption), and return a
 * specific fix per finding — no style notes.
 */

export const meta = {
  name: 'attack-design',
  description: 'Adversarially attack a risky design before implementation',
  phases: [{ title: 'Attack', detail: 'specialists attack the design in parallel' }],
}

// ---------------------------------------------------------------------------
// 1. Describe the design concretely. Include the environment facts an
//    attacker needs (CPU model, interrupt state, emulator guarantees, the
//    prior-art files to read) and the exact plan (registers, structs, sizes,
//    ordering, CI gate strings). Vague briefs get vague attacks.
// ---------------------------------------------------------------------------
const DESIGN_BRIEF = `
<PASTE THE DESIGN HERE>

Context the attacker needs:
- Environment: <e.g. single-CPU x86_64, QEMU 8.2, interrupts off in syscalls>
- Read the real code it extends: <paths to prior-art files and idioms to match>
- The exact plan: <register sequences / struct layouts / buffer sizes / ordering>
- The CI gate that will "prove" it: <the exact command + gate strings>
`

// ---------------------------------------------------------------------------
// 2. Pick the lenses the design actually touches. Keep 2–4. Each `focus`
//    steers one specialist; the shared preamble keeps them concrete.
// ---------------------------------------------------------------------------
const LENSES = [
  {
    key: 'hardware',
    focus: `hardware correctness: register/reset/power sequences, status-bit polling
(BSY vs DRQ vs ready), UNBOUNDED spins (there must be none), DMA address/alignment/overflow,
cache-flush ordering, and what the emulator models vs real silicon.`,
  },
  {
    key: 'concurrency',
    focus: `interrupts & concurrency: level vs edge triggering, clearing the device ISR
BEFORE the shared EOI, IF=0 windows and what cannot run in them, producer/consumer races on
shared queues, and routing dynamically-assigned IRQ lines.`,
  },
  {
    key: 'ci-integrity',
    focus: `CI/test integrity: can the gate pass for the WRONG reason? Stale build artifacts,
input echoed by the test itself matching the gate string, non-hermetic external dependencies,
"0 found -> skip" holes, silent truncation. A green gate that proves nothing is the target.`,
  },
  // Add as needed:
  // { key: 'crash-consistency', focus: `data format & crash consistency: write ordering
  //   (commit record last), torn-write detection, clamp attacker-controlled sizes before
  //   allocating, route restored data through the same validation as the live path.` },
  // { key: 'capability', focus: `security/capability: is authority gated where it must be,
  //   capless-caller-denied proven by attack, stale-id/recycled-id use-after-free, ambient
  //   reads that leak more than intended.` },
]

const FINDINGS_SCHEMA = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          detail: { type: 'string', description: 'concrete input/state -> wrong result' },
          severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
          fix: { type: 'string', description: 'the specific fix' },
        },
        required: ['title', 'detail', 'severity', 'fix'],
      },
    },
  },
  required: ['findings'],
}

const PREAMBLE = `You are a design-correctness specialist attacking a PLANNED design BEFORE it
is implemented. Read the real code the design references (do not attack a strawman). Hunt only
CONCRETE defects — a specific input or state leading to a specific wrong output, crash, or data
corruption — and give each one a specific fix. No style notes. If a design choice is correct,
say so explicitly so a reviewer does not regress it.\n\nDESIGN:\n${DESIGN_BRIEF}\n\nYOUR LENS: `

phase('Attack')
const results = await parallel(
  LENSES.map((l) => () =>
    agent(PREAMBLE + l.focus, { label: `attack:${l.key}`, schema: FINDINGS_SCHEMA })
  )
)

const all = results.filter(Boolean).flatMap((r) => r.findings || [])
const order = { blocker: 0, major: 1, minor: 2 }
all.sort((a, b) => (order[a.severity] ?? 3) - (order[b.severity] ?? 3))
log(`${all.length} findings (${all.filter((f) => f.severity === 'blocker').length} blockers)`)
return { findings: all }
