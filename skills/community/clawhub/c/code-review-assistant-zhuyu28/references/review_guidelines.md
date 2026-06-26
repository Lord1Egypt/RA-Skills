# Code Review Guidelines

## General Principles

- Focus on correctness, readability, and maintainability
- Be constructive and specific in feedback
- Consider the context and purpose of the code
- Prioritize critical issues over stylistic preferences

## Language-Specific Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for public functions and classes
- Handle exceptions appropriately

### JavaScript/TypeScript
- Use consistent naming conventions
- Prefer const over let when possible
- Handle async operations properly
- Validate inputs and handle edge cases

### Go
- Follow Go formatting standards
- Use meaningful variable names
- Handle errors explicitly
- Write table-driven tests

## Security Considerations

- Input validation and sanitization
- Proper error handling without leaking sensitive information
- Secure dependency management
- Authentication and authorization checks

## Performance Considerations

- Algorithmic efficiency
- Memory usage optimization
- Database query optimization
- Caching strategies

## Testing Guidelines

- Unit tests should cover edge cases
- Integration tests should verify system behavior
- Test data should be realistic but not sensitive
- Tests should be deterministic and fast