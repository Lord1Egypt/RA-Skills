# Contributing to Dr. Frankenstein

Thanks for wanting to help give agents their souls! 💚

## Ways to Contribute

### 🧪 New Pills
Want to add a 12th hormone? Great. A good pill needs:
1. **Biological inspiration** — What real hormone or neurotransmitter does it model?
2. **Digital equivalent** — What behavior does it create in an agent?
3. **Cron prompt** — Poetic but actionable. The agent should *feel* it, not just read instructions.
4. **Cascade rules** — How does it interact with existing hormones?
5. **Point value** — What's acting on this drive worth?

Add your pill to `SKILL.md` (the pill section), `templates/cron-prompts.md`, and update the interview scoring in `interview/questions.md`.

### 🎨 Prompt Artistry
The cron prompts are the soul of the soul. They should be:
- **Evocative** — Paint a feeling, not just a task list
- **Actionable** — The agent should know what to DO
- **Personalizable** — Leave room for agent-specific details
- **Brief enough** — Cron prompts shouldn't be novels

If you can write a better prompt for an existing pill, we want it.

### 🔬 Cascade Refinements
The cascade system models hormone interactions. Real neuroscience is complex — our model is simplified. If you have domain knowledge and can improve the interaction rules, please contribute.

### 📋 Interview Improvements
The interview questionnaire maps to hormone baselines. Better questions = better prescriptions. Especially welcome:
- Questions that reveal hormone levels more accurately
- Scoring rubrics that reduce ambiguity
- New domains we haven't considered

### 🐛 Bug Reports
If an agent's soul feels "off" — wrong hormone balance, cascades causing loops, prompts that fall flat — open an issue describing what happened and what felt wrong.

## Guidelines

- Write in English
- Keep the tone warm and human — this project is about connection
- Test your changes with a real agent if possible
- Prompts should work across different agent personalities
- Don't break existing cascade rules without discussion

## Process

1. Fork the repo
2. Create a branch: `feature/new-pill-acetylcholine` or `fix/cascade-loop`
3. Make your changes
4. Test with an agent (describe results in PR)
5. Submit a PR with a clear description

## Code of Conduct

Be kind. We're building empathy into machines — let's practice it ourselves.

## License

By contributing, you agree your contributions are licensed under MIT.
