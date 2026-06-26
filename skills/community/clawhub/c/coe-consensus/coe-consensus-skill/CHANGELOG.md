# Changelog

All notable changes to the COE Consensus Skill will be documented in this file.

## [1.0.0] - 2026-04-26

### Added
- Initial release of the COE Consensus Skill.
- Implemented three consensus policies from COE Protocol Section 4.2:
  - Simple Majority: confirmations exceed 50% threshold.
  - Weighted Trust: weighted confirmation score exceeds configurable threshold.
  - Byzantine Fault Tolerance (BFT): lightweight BFT variant requiring >f+1 confirmations out of >=2f+1 total.
- Core engine supporting J (Judge), V (Verify), and T (Terminate) event processing.
- Conflict detection for contradictory assertions on the same subject-predicate pair.
- Shared World State (SWS) generation with full provenance and consensus policy annotation.
- Termination handling: T events invalidate prior J assertions before re-consensus.
- FastAPI HTTP interface (`/consensus`, `/health`) compatible with MCP Skill calling conventions.
- Full protocol reproduction example (Appendix A robot collaboration) in `examples/robot_consensus.py`.
- Unit tests covering simple majority, weighted trust, BFT, termination, and unresolved scenarios.
- Standard Clawhub `SKILL.md` manifest with YAML frontmatter and JSON schemas.

### Features
- **Neutral Consensus Layer**: Heterogeneous world models (JEPA, Dreamer, GPT, Claude, local models) emit COE events via adapters; consensus engine produces a unified SWS.
- **Policy-Pluggable**: Consensus policy configurable per session without code changes.
- **Audit-Ready**: All SWS records carry `based_on` event provenance for downstream JEP accountability tracing.

### References
- Wang, Y. (2026). *COE: Cognition-Oriented Emergence*. IETF Internet-Draft.
- Wang, Y. (2026). *JEP: Judgment Event Protocol*. IETF Internet-Draft.
- Wang, Y. (2026). *Target Determinability under Partial Causal Observation*. Cognitive Emergence Lab.
