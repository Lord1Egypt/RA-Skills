# Changelog

All notable changes to the Determinability-Checker Skill will be documented in this file.

## [1.0.2] - 2026-04-26

### Added
- Initial stable release of the Determinability-Checker Skill.
- Implemented `CheckDeterminability` algorithm (Theorem 10.1) from *Target Determinability under Partial Causal Observation* (Wang, 2026).
- Core engine supporting zero-error determinability verification with decision table output.
- Counterexample certificate generation for non-determinability proofs.
- Conflict graph construction and analysis.
- Minimal evidence cover computation via greedy set-cover approximation (Theorem 8.2).
- FastAPI HTTP interface (`/check`, `/health`) compatible with MCP Skill calling conventions.
- Full paper reproduction example (Section 10.2 LLM Agent Audit Case) in `examples/audit_example.py`.
- Unit tests covering determined, non-determined, and evidence-cover scenarios.
- Standard Clawhub `SKILL.md` manifest with YAML frontmatter and JSON schemas.

### Features
- **Gatekeeper Pattern**: Agent calls this skill before executing other skills to verify causal sufficiency.
- **DETERMINED** → returns decision table; Agent proceeds immediately.
- **NOT_DETERMINED** → returns counterexample pair, missing evidence list, and next-skill suggestion.
- Supports arbitrary configuration families, observation functions (`omega_field`), and target functions (`target_field`).
- Extensible evidence field system for constrained causal-evidence coverage analysis.

### References
- Wang, Y. (2026). *Target Determinability under Partial Causal Observation*. Cognitive Emergence Lab.
- Wang, Y. (2026). *JEP: Judgment Event Protocol*. IETF Internet-Draft.
