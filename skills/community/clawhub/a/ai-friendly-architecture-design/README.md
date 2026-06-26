# AI Friendly Architecture Design Skill

A skill for guiding AI agents to design architectures that incorporate AI/LLM capabilities following the AI Friendly architecture principles.

**Core principle:** Use appropriate architecture for the problem—don't over-engineer with AI when traditional solutions suffice.

## Files

| File | Lines | Description |
|------|-------|-------------|
| `SKILL.md` | 342 | Main skill document with architecture guidance |
| `references/evals.md` | 242 | Evaluation criteria, benchmark tests, and TDD compliance docs |
| `references/test-scenarios.md` | 561 | 30 test scenarios (10 standard + 5 negation + 15 edge cases) |
| `references/article-summary.md` | 37 | English supplement to original article |
| `eval_runner.py` | - | Executable eval runner for 5 core tests |

**Total:** ~1103 lines across 4 files (excluding this README), all in English.

## Usage

Load as a skill when designing systems that incorporate AI/LLM capabilities or evaluating AI Friendly vs traditional architecture:

- **SKILL.md** — Load this file as the active skill document
- **references/evals.md** — Evaluation criteria, benchmarks, and TDD compliance documentation
- **references/test-scenarios.md** — 30 test scenarios for verification

### Quick Loading

In Claude Code / Copilot CLI: use the `Skill` tool and reference `SKILL.md`.
For other AI coding agents: load the contents of `SKILL.md` into context.

### Running Evaluations

The skill includes an executable eval runner to verify core functionality:

```bash
# Run with simulated responses (no dependencies required)
python eval_runner.py

# Run with LLM integration (requires openai or anthropic package)
python eval_runner.py --llm openai
python eval_runner.py --llm anthropic
```

**Requirements:**
- Python 3.8+
- For LLM integration: `openai` or `anthropic` package (install via `pip install openai` or `pip install anthropic`)

**Exit codes:**
- `0` - All tests passed
- `1` - One or more tests failed

## References

- [Article Summary](references/article-summary.md) (English)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (Yao et al., 2022)
- [Skill Authoring Guide](https://github.com/GanJiaKouN16/Function-Point-Skill/blob/main/skill-authoring-guide.md)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-improvement`)
3. Update `SKILL.md` for content changes
4. Update `references/evals.md` and `references/test-scenarios.md` for evaluation changes
5. Run evaluation suite: `python eval_runner.py` to verify core tests pass
   - All 5 tests should pass before submitting PR
   - If tests fail, update SKILL.md or test scenarios as needed
6. Submit a Pull Request with description of changes and test results

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-06-03 | Major improvements: removed self-assigned quality score, reframed metrics as illustrative, added executable eval runner (10 tests), cleaned frontmatter, expanded article summary, improved decision framework with detailed criteria |
| 1.1.0 | 2026-06-03 | Added triggers, expanded Context Engineering, cost/performance decision branches, negation tests, scoring improvements, English article supplement |
| 1.0.0 | Initial | First release |
