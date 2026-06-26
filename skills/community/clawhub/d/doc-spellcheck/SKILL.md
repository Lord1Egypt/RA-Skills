# Document Spell Check Skill

## Purpose
Automatically detect and fix spelling errors in documentation files across any project. This skill provides comprehensive spell checking for Markdown, plain text, and other documentation formats.

## Features

### 1. Multi-Format Support
- **Markdown files** (`.md`, `.mdx`)
- **Plain text files** (`.txt`)
- **Documentation directories** (recursive scanning)
- **Specific file patterns** (glob support)

### 2. Comprehensive Error Detection
- Common misspellings (`recieve` → `receive`, `teh` → `the`)
- Word form errors (`formating` → `formatting`, `occured` → `occurred`)
- Contextual spelling mistakes
- Custom dictionary support for technical terms

### 3. Automated Fixing
- Interactive correction suggestions
- Batch auto-fix for common patterns
- Safe dry-run mode to preview changes
- Git integration for clean commits

### 4. Integration Capabilities
- Works with existing project structures
- Respects `.gitignore` and excluded paths
- Configurable severity levels
- CI/CD compatible output format

## Usage

### Basic Commands
```bash
# Check single file
doc-spellcheck check docs/guide.md

# Check entire directory  
doc-spellcheck check docs/

# Auto-fix common errors
doc-spellcheck fix docs/guide.md

# Dry-run to preview fixes
doc-spellcheck fix --dry-run docs/
```

### Advanced Options
```bash
# Custom dictionary
doc-spellcheck check --dict custom-words.txt docs/

# Exclude patterns
doc-spellcheck check --exclude "**/node_modules/**" docs/

# Specific error types
doc-spellcheck check --errors "misspelling,word-form" docs/

# Output format for CI
doc-spellcheck check --format json docs/
```

## Implementation Details

### Core Dependencies
- **Aspell**: Primary spell checking engine
- **Custom word lists**: Project-specific terminology
- **File system walker**: Efficient directory traversal
- **Git integration**: Safe commit management

### Error Categories
1. **Basic Misspellings**: Common typos and transpositions
2. **Word Form Errors**: Incorrect verb/noun forms
3. **Technical Terms**: Domain-specific vocabulary validation
4. **Contextual Errors**: Words that are spelled correctly but used incorrectly

### Safety Measures
- **Backup creation**: Automatic file backups before fixing
- **Atomic operations**: Changes applied as single git commits
- **Rollback support**: Easy revert of applied fixes
- **Permission checks**: Respects file system permissions

## Workflow Integration

### Local Development
1. Run spell check before committing changes
2. Use interactive mode for manual review
3. Add custom dictionaries for project terminology

### CI/CD Pipeline
1. Integrate as pre-commit hook
2. Fail builds on critical spelling errors
3. Generate reports for documentation quality metrics

### Team Collaboration
1. Shared custom dictionaries across team members
2. Consistent terminology enforcement
3. Automated documentation quality gates

## Configuration

### Default Settings
- **File extensions**: `.md`, `.mdx`, `.txt`, `.rst`
- **Excluded paths**: `node_modules/`, `.git/`, `dist/`
- **Severity level**: `warning` (non-blocking)
- **Auto-fix**: `disabled` by default

### Customization Options
- Language selection (en-US, en-GB, etc.)
- Custom ignore lists
- Severity thresholds
- Output verbosity levels

## Best Practices

### For Maintainers
- Run comprehensive checks before major releases
- Maintain project-specific dictionaries
- Document accepted terminology variations
- Set up automated CI checks

### For Contributors  
- Check spelling before submitting PRs
- Use consistent terminology
- Respect project style guides
- Include new terms in dictionaries when appropriate

## Examples

### Fixing Common Errors
```bash
# Before: "The recieve function handles incoming data"
# After:  "The receive function handles incoming data"

# Before: "This occured during the formating process"  
# After:  "This occurred during the formatting process"
```

### Batch Processing
```bash
# Process entire documentation directory
doc-spellcheck fix --batch docs/

# Review changes interactively
doc-spellcheck fix --interactive docs/guide.md
```

## Limitations

### Known Constraints
- Cannot detect contextually incorrect but correctly spelled words without AI
- May flag technical terms as errors without custom dictionaries
- Performance impact on very large documentation sets
- Requires proper language pack installation

### Workarounds
- Use custom dictionaries for technical terminology
- Combine with grammar checking tools for comprehensive validation
- Run incrementally on large projects
- Pre-install required language packs in CI environments

## Maintenance

### Updates
- Regular dictionary updates for new terminology
- Engine version upgrades for improved accuracy
- Pattern library expansion based on common errors
- Performance optimizations for large-scale usage

### Monitoring
- Track false positive rates
- Monitor performance metrics
- Collect user feedback on suggestions
- Maintain compatibility with documentation standards