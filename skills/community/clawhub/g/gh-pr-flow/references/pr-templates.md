# PR Templates

## Feature PR Template
```
## Description
<!-- What does this PR do? -->

## Related Issue
Closes #ISSUE_NUMBER

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Refactoring
- [ ] Documentation
- [ ] Performance improvement

## How Has This Been Tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] Code follows project style
- [ ] Self-reviewed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No new warnings

## Screenshots (if applicable)
<!-- Add screenshots for UI changes -->
```

## Bug Fix Template
```
## Bug Description
<!-- Clear description of the bug -->

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
<!-- What should happen -->

## Actual Behavior
<!-- What actually happens -->

## Root Cause
<!-- What caused the bug -->

## Fix
<!-- How it was fixed -->

## Testing
- [ ] Bug scenario verified fixed
- [ ] Regression tests pass
```

## How to set template per repo
```bash
# Create the template
mkdir -p .github
cat > .github/PULL_REQUEST_TEMPLATE.md << 'EOF'
# Template content here
EOF

# Or with directory structure for multiple templates
mkdir -p .github/PULL_REQUEST_TEMPLATE
```
