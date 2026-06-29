# Validation Cycle Closure

Use this reference when finishing a validation cycle for `ai-expert-team` or a similar evidence-first skill.

## Trigger

The user asks to finish the last validation target, add README or public proof points, and remove remaining unfinished items instead of continuing them.

## Closure Pattern

1. **Add public proof packaging**
   - Create or update README-level onboarding.
   - Include what the skill does, when to use it, runtime flow, included references, validation proof, evidence boundaries, output contract, and maintenance status.
   - Summarize completed validation cases as proof points instead of copying the full validation log.

2. **Separate historical evidence from active work**
   - Keep historical statements such as missing README or partial market evidence only when labeled as historical or scoped.
   - Do not let old `pending`, `next action`, or `remaining work` language survive beside a new closed status.

3. **Close intentionally abandoned work**
   - If the user says remaining items will not be done, remove or rewrite active follow-up sections.
   - Replace dangling follow-ups with a closure statement: future expansion requires a fresh request and fresh scope.
   - Do not keep clean install, adoption analytics, marketplace conversion, broad discoverability, board mode, or other expansion work as active debt unless the user explicitly wants it retained.

4. **Update both summary and detail docs**
   - Main project page: status, facts/reasoning, completed list, artifact traceability, roadmap/closure sections.
   - Validation log: frontmatter facts/reasoning, final verdicts, historical findings, and closed-scope sections.
   - README: public proof package and evidence boundaries.

5. **Verify stale language**
   - Search for active-work phrases after editing:
     - `Next Actions`
     - `High-priority follow-ups`
     - `Not Yet Proven`
     - `Recommended next action`
     - `pending`
     - `still untested`
     - `still unwritten`
     - `still unavailable`
     - old inventory outputs such as `README files: []`
   - Keep matches only if they are part of a generic template or clearly historical and not active follow-up language.

## Pitfalls

- Do not convert intentionally abandoned work into a new backlog just because it is technically useful.
- Do not erase historical evidence; relabel it as historical if it explains why the current README or closure exists.
- Do not claim out-of-scope items are proven. Say they are closed out of this cycle, not validated.
- Do not use a README as a substitute for validation evidence; README proof points summarize completed validation cases.

## Verification Checklist

- [ ] README exists and is non-empty.
- [ ] Main project page says the validation cycle is closed.
- [ ] Detail validation log says README proof packaging is complete.
- [ ] No active `Next Actions` / follow-up sections remain for abandoned work.
- [ ] Stale pending phrases are removed or historicalized.
- [ ] Diff check passes for edited tracked files.
