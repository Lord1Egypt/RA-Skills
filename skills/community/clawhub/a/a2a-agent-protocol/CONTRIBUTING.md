# Contributing to a2a-protocol

Thank you for your interest in contributing to the A2A Protocol skill.

## How to Contribute

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/<your-username>/a2a-protocol.git
   cd a2a-protocol
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feat/your-feature-name
   ```
4. **Make your changes** — follow the SKILL.md structure standards
5. **Run the audit**:
   ```bash
   python ~/.openclaw/workspace/skills/skill-factory/scripts/audit_skill.py . --all
   ```
6. **Commit and push**:
   ```bash
   git commit -m "feat(<feature>): add ..."
   git push origin feat/your-feature-name
   ```
7. **Open a Pull Request** with a clear description of what and why

## Skill Structure Standards

- `SKILL.md` must have valid YAML frontmatter with `name`, `description`, `license`, `metadata`
- `description` must contain trigger conditions, not just capability statements
- All scripts must have shebangs and `requirements.txt`
- No hardcoded API keys or secrets

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Search existing issues before creating a new one
- Include A2A protocol version reference when applicable

## Code of Conduct

This project follows the [A2A Protocol Code of Conduct](https://github.com/a2aproject/A2A/blob/main/CODE_OF_CONDUCT.md).