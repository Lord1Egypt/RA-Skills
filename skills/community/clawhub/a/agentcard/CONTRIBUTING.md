# Contributing to Agent Card

Thank you for your interest in contributing to Agent Card! 🎉

## Quick Links

- [Issues](https://github.com/ASGCompute/asgcard-public/issues) — Report bugs or request features
- [Docs](https://asgcard.dev/docs) — API documentation
- [Security Policy](SECURITY.md) — Report vulnerabilities responsibly

## How to Contribute

### Reporting Bugs

1. Search [existing issues](https://github.com/ASGCompute/asgcard-public/issues) first
2. Open a new issue using the **Bug Report** template
3. Include reproduction steps, expected vs. actual behavior, and environment details

### Suggesting Features

1. Open an issue using the **Feature Request** template
2. Describe the use case and expected behavior
3. Tag with `enhancement`

### Code Contributions

This is a **public mirror** of an internal monorepo. We accept PRs for:

- Documentation improvements
- Bug fixes with tests
- New MCP tool implementations
- SDK improvements
- CLI enhancements

#### Workflow

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Run tests: `npm test`
5. Commit with a clear message: `feat: add card spending limits`
6. Push and open a PR

#### Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation only
- `refactor:` — Code change that neither fixes a bug nor adds a feature
- `test:` — Adding or updating tests
- `chore:` — Maintenance tasks

### Good First Issues

Look for issues labeled [`good first issue`](https://github.com/ASGCompute/asgcard-public/labels/good%20first%20issue) — these are curated for newcomers.

## Development Setup

```bash
git clone https://github.com/ASGCompute/asgcard-public.git
cd asgcard-public
npm install
npm run build
```

## Code of Conduct

Be respectful, constructive, and inclusive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
