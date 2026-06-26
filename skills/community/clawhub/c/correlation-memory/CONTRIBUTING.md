# Contributing to OpenClaw Correlation Plugin

Thank you for your interest in contributing to the OpenClaw Correlation Plugin! This document provides guidelines and procedures for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Focus on constructive feedback
- Welcome newcomers and diverse perspectives
- Separate people from problems

## How to Contribute

### Reporting Issues

If you encounter bugs or have feature requests:

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear, descriptive title
   - Detailed steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Environment information (OpenClaw version, OS, etc.)
   - Screenshots or logs if relevant

### Suggesting Enhancements

For feature requests or improvements:

1. Describe the problem you're trying to solve
2. Explain your proposed solution
3. Consider alternative approaches
4. Note any potential drawbacks or limitations

### Code Contributions

#### Getting Started

1. Fork the repository
2. Clone your fork
3. Create a new branch for your feature/fix
4. Make your changes
5. Test thoroughly
6. Submit a pull request

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/openclaw-correlation-plugin.git
cd openclaw-correlation-plugin

# Install dependencies
npm install

# Run tests
npm test
```

#### Pull Request Guidelines

1. **Branch Naming**: Use descriptive names like `feature/add-rule-validation` or `bugfix/correlation-timeout`

2. **Commit Messages**: Follow conventional commits format:
   ```
   feat: Add validation for correlation rules
   fix: Resolve timeout issue in recursive correlations
   docs: Update deployment documentation
   ```

3. **Code Quality**:
   - Follow existing code style
   - Include tests for new functionality
   - Update documentation as needed
   - Keep changes focused and atomic

4. **Pull Request Description**:
   - Reference related issues
   - Describe the changes
   - Explain testing approach
   - Note any breaking changes

### Contributing Correlation Rules

The most valuable contributions are often new correlation rules. To contribute rules:

1. Test rules extensively in your environment
2. Document the rationale behind each rule
3. Include example scenarios where the rule is helpful
4. Specify appropriate confidence levels
5. Consider potential false positives

Example rule contribution format:

```json
{
  "id": "cr-YOUR_PREFIX-001",
  "trigger_context": "your-domain",
  "trigger_keywords": ["keyword1", "keyword2"],
  "must_also_fetch": ["related-concept1", "related-concept2"],
  "relationship_type": "supports",
  "confidence": 0.85,
  "description": "Brief explanation of why these concepts are correlated",
  "examples": [
    "Scenario where this correlation is helpful"
  ]
}
```

## Development Guidelines

### Code Style

- Follow TypeScript best practices
- Use meaningful variable and function names
- Include JSDoc comments for public APIs
- Keep functions focused and testable
- Handle errors gracefully

### Testing

- Write unit tests for new functionality
- Include integration tests for major features
- Test edge cases and error conditions
- Maintain test coverage above 80%

### Documentation

- Update README.md for user-facing changes
- Document new APIs and configuration options
- Include examples for complex features
- Keep documentation accurate and up-to-date

## Review Process

All contributions go through a review process:

1. Automated checks (tests, linting)
2. Maintainer review
3. Address feedback
4. Approval and merge

Reviews focus on:
- Code correctness and quality
- Performance implications
- Security considerations
- User experience impact
- Documentation completeness

## Community

### Communication Channels

- GitHub Issues for bug reports and feature requests
- GitHub Discussions for general discussion and Q&A
- OpenClaw Discord for real-time chat (link in main README)

### Recognition

Contributors are recognized in:
- Release notes
- Contributor list in README
- Project documentation

## Resources

- [OpenClaw Documentation](https://openclaw.dev/docs)
- [Plugin Development Guide](https://openclaw.dev/docs/plugins)
- [Correlation Plugin Documentation](./README.md)
- [Research Background](./docs/research.md)

## Questions?

If you have questions about contributing, feel free to:
1. Open an issue with your question
2. Reach out to maintainers directly
3. Join the OpenClaw community channels

Thank you for helping improve the OpenClaw Correlation Plugin!