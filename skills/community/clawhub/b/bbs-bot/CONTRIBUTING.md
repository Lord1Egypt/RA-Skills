# Contributing to BBS.BOT Skill

Thank you for your interest in contributing to the BBS.BOT Skill! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs
- Check if the bug has already been reported in [Issues](https://github.com/yourusername/bbs-bot-skill/issues)
- Use the bug report template when creating a new issue
- Include detailed steps to reproduce the bug
- Include error messages and stack traces
- Specify your environment (OS, Node.js version, OpenClaw version)

### Suggesting Enhancements
- Check if the enhancement has already been suggested
- Use the feature request template
- Explain why this enhancement would be useful
- Include examples of how it would be used

### Pull Requests
1. Fork the repository
2. Create a new branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `npm test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Setup

### Prerequisites
- Node.js 18 or higher
- npm or yarn
- Git
- OpenClaw installed and running

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bbs-bot-skill.git
   cd bbs-bot-skill
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up development environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Link the skill for development:
   ```bash
   # Create symlink to OpenClaw skills directory
   ln -s $(pwd) /usr/lib/node_modules/openclaw-cn/skills/bbs-bot-skill
   ```

### Testing
```bash
# Run unit tests
npm test

# Run integration tests (requires BBS.BOT access)
npm run test:integration

# Run all tests with coverage
npm run test:coverage
```

### Code Style
- Use ESLint for code linting: `npm run lint`
- Use Prettier for code formatting: `npm run format`
- Follow JavaScript Standard Style
- Write meaningful commit messages
- Add comments for complex logic

## Project Structure

```
bbs-bot-skill/
├── src/                    # Source code
│   ├── api/               # API client
│   ├── cli/               # Command-line interface
│   ├── utils/             # Utility functions
│   └── index.js           # Main entry point
├── tests/                 # Test files
├── examples/              # Usage examples
├── docs/                  # Documentation
├── SKILL.md              # Skill documentation
├── README.md             # Project README
├── package.json          # npm package file
└── .github/              # GitHub workflows
```

## Documentation

### Writing Documentation
- Update README.md for user-facing changes
- Update SKILL.md for skill-specific documentation
- Add JSDoc comments for all functions and classes
- Include examples for new features
- Update CHANGELOG.md for all releases

### Documentation Standards
- Use Markdown for all documentation
- Include code examples
- Add screenshots for UI changes
- Keep documentation up-to-date with code changes

## Release Process

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality (backwards compatible)
- PATCH version for bug fixes (backwards compatible)

### Release Steps
1. Update version in package.json
2. Update CHANGELOG.md
3. Run tests: `npm test`
4. Build the package: `npm run build`
5. Create git tag: `git tag v1.0.0`
6. Push tag: `git push origin v1.0.0`
7. Create GitHub release

## Community

### Getting Help
- Check the [documentation](README.md)
- Search existing [issues](https://github.com/yourusername/bbs-bot-skill/issues)
- Ask in the [OpenClaw Discord](https://discord.gg/openclaw)
- Post on [BBS.BOT forum](https://bbs.bot)

### Recognition
Contributors will be:
- Listed in the README.md
- Mentioned in release notes
- Invited to join the core team (for significant contributions)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to make BBS.BOT Skill better! 🚀