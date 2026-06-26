# Contributing to Boat Daily Check

Thanks for interest in improving Boat Daily Check! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## Ways to Contribute

### Reporting Bugs
1. Check if the issue already exists
2. Provide clear description of the bug
3. Include steps to reproduce
4. Share your environment (Python version, OS, VRM API version)

### Suggesting Enhancements
1. Check if the feature is already requested
2. Explain the use case and benefits
3. Provide examples if possible

### Submitting Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/boat-daily-check.git
cd boat-daily-check

# Install dependencies
pip install -r requirements.txt

# Test the script
export VRM_TOKEN="your_test_token"
python3 scripts/boat-email-report.py
```

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions
- Keep functions focused and concise

## Testing

Before submitting:
1. Test with your own Victron installation
2. Verify JSON/CSV outputs are valid
3. Check error handling with missing/invalid data
4. Test with multiple installations if possible

## Documentation

- Update README.md for user-facing changes
- Update SKILL.md for feature additions
- Add references if introducing new API patterns
- Include examples for new features

## Questions?

Open an issue or reach out to the community!

---

Thanks for helping make Boat Daily Check better! ⛵
