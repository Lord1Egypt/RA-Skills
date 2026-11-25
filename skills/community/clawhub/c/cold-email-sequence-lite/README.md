# cold-email-sequence-lite

Minimal 2-touch cold outreach skeleton (opener + polite breakup) from an ICP brief — subject options, skeleton copy, spam-trigger and subject-length checks. Offline, zero deps, Node 18+.

## Install

```bash
npx skills add NenadZivotic/lite-agent-skills --skill cold-email-sequence-lite
```

## Run

```bash
echo '{"product":"ACME scheduler","icp":"clinic managers","painPoints":["no-show appointments"],"cta":"worth a quick look?","senderName":"N","company":"ACME"}' | node scripts/sequence.js -
```

## Full version

The full `cold-email-sequence` skill ($6) builds the standard 4-touch cadence (days 0/3/7/14 — opener, proof bump, reframe, breakup) with proof-point and tone handling. Ask for it by slug.
