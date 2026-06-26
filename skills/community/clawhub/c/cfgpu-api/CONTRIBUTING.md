# Contributing to CFGPU API Skill

Thank you for considering contributing to the CFGPU API Skill!

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   sudo apt-get install jq curl
   ```

3. Set up test environment:
   ```bash
   export CFGPU_API_TOKEN="test_token"
   ```

## Code Style

- Use shellcheck for shell scripts
- Follow Google Shell Style Guide
- Add comments for complex logic
- Include error handling

## Testing

1. Test scripts with different inputs
2. Verify API responses are handled correctly
3. Test edge cases and error conditions

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure no sensitive data is included
4. Update CHANGELOG.md

## Security

- Never include real API tokens
- Use environment variables for configuration
- Validate all user inputs
- Sanitize output data

## Questions?

Open an issue or start a discussion!
