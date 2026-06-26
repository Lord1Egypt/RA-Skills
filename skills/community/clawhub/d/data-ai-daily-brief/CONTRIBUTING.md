# Contributing to AI Industry Intelligence Daily Brief

Thank you for your interest in contributing! 🎉

## How to Contribute

### 🐛 Bug Reports

- Open an [Issue](../../issues) with a clear description
- Include steps to reproduce, expected vs actual behavior
- Mention your environment (OS, Python version, etc.)

### 💡 Feature Requests

- Open an [Issue](../../issues) with the `enhancement` label
- Describe the use case and why it would be valuable
- Bonus: suggest an implementation approach

### 🔧 Pull Requests

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes** and test them
4. **Commit** with clear messages: `git commit -m "Add: new delivery channel for LINE"`
5. **Push** and open a Pull Request

### 📝 Code Style

- Python scripts: follow PEP 8
- Include docstrings with usage instructions in each script
- Support both environment variables and command-line arguments
- Add error handling with helpful messages

### 🌐 Adding a New Delivery Channel

To add a new push channel (e.g., LINE, WhatsApp):

1. Create `scripts/send_yourplatform.py` following the existing pattern
2. Include a comprehensive docstring with setup guide
3. Support environment variables for credentials
4. Add the channel to `init_config.py` default config
5. Update both `README.md` and `README_zh.md`
6. Update `SKILL.md` with the new channel info

### 🏭 Adding Industry Templates

To contribute a new industry template:

1. Describe the industry focus areas, key vendors, and sources
2. Provide a sample `SKILL.md` prompt section
3. Include example `focus_areas` configuration

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to build something useful together.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
