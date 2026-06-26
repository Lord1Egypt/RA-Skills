# Contributing to Album Pipeline

## How to Contribute

Album Pipeline is a collection of OpenClaw Skills for AI music album production.

### Adding New Experts

Each expert lives in its own directory as a `SKILL.md` file. To add a new expert:

1. Create a directory: `<expert-name>/`
2. Add `SKILL.md` following the existing format
3. Update `FILE_CONTRACTS.md` with input/output paths
4. Wire the expert into the appropriate Phase in `SKILL.md` (root)

### Bug Reports

- File an Issue with the phase/expert name in the title
- Include the input file that triggered the issue
- Describe expected vs actual output

### License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
