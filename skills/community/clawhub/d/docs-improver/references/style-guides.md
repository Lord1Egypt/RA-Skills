# Documentation Style Guides

Comprehensive style guides for technical documentation.

## Writing Style

### General Principles

1. **Clarity First** - Write for your audience
2. **Consistency** - Use consistent terminology
3. **Conciseness** - Be brief but complete
4. **Active Voice** - Prefer active over passive
5. **Present Tense** - Use present tense for instructions

### Tone

- Professional but approachable
- Avoid jargon when possible
- Define technical terms on first use
- Use inclusive language

## Documentation Types

### README.md

**Purpose:** Project overview and quick start

**Required Sections:**
- Project title and description
- Badges (license, build status, version)
- Table of contents
- Installation instructions
- Usage examples
- Contributing guidelines
- License

**Length:** 500-3000 words

### API Documentation

**Purpose:** Complete API reference

**Required Sections:**
- Overview
- Authentication
- Endpoints (method, path, parameters, responses)
- Error codes
- Rate limits
- Examples

**Format:** OpenAPI/Swagger preferred

### Architecture Documentation

**Purpose:** System design and structure

**Required Sections:**
- System overview
- Architecture diagram
- Component descriptions
- Data flow
- Technology stack
- Design decisions (ADRs)

**Length:** 2000-10000 words

### User Guides

**Purpose:** How to use features

**Required Sections:**
- Prerequisites
- Step-by-step instructions
- Screenshots/diagrams
- Troubleshooting
- FAQ

**Format:** Task-oriented

## Code Examples

### Best Practices

```python
# Good: Clear, complete, tested
from package import Client

client = Client(api_key="your-key")
result = client.process(data)
print(result)
```

```python
# Bad: Incomplete, unclear
import package
p = package.Client()
p.do_something()
```

### Formatting

- Use syntax highlighting
- Keep examples under 30 lines
- Include expected output
- Test all examples

## Diagrams

### When to Use

- System architecture
- Data flow
- Component relationships
- Process workflows

### Tools

- **Mermaid** - Markdown-native diagrams
- **Draw.io** - Free, web-based
- **PlantUML** - Text-based UML
- **Excalidraw** - Hand-drawn style

## Linking

### Internal Links

```markdown
[See Architecture](#architecture)
[See API Docs](./API.md)
```

### External Links

- Use descriptive link text
- Include URL for important references
- Check links regularly

## Versioning

### Documentation Versions

- Match software versions
- Maintain changelog
- Deprecation notices
- Migration guides

## Review Process

### Before Publishing

- [ ] Technical accuracy review
- [ ] Grammar and spelling check
- [ ] Link validation
- [ ] Code example testing
- [ ] Accessibility check

### Regular Maintenance

- Quarterly review
- Update after major changes
- Remove outdated content
- Add missing sections

## Accessibility

### Guidelines

- Use heading hierarchy properly
- Add alt text to images
- Use sufficient color contrast
- Make tables accessible
- Provide text alternatives

## Internationalization

### Best Practices

- Write translation-friendly content
- Avoid idioms and slang
- Use simple sentence structures
- Provide context for examples
- Consider cultural differences

## Metrics

### Quality Indicators

- Page views
- Time on page
- Search queries
- Support tickets reduced
- User feedback

### Review Frequency

- Critical docs: Monthly
- Important docs: Quarterly
- Reference docs: Bi-annually
