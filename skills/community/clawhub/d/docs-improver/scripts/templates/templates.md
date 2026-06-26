# Documentation Templates

Ready-to-use templates for common documentation types.

## README.md Template

```markdown
# {{Project Name}}

[![License](https://img.shields.io/badge/license-{{License}}-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/circleci/build/github/{{user}}/{{repo}})]()
[![Version](https://img.shields.io/github/v/release/{{user}}/{{repo}})]()

{{Brief project description (1-2 sentences)}}

## 🚀 Quick Start

```bash
{{Installation command}}
{{Quick usage example}}
```

## 📖 Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## 📝 About

{{Detailed project description}}

### Why {{Project Name}}?

{{Problem this project solves}}

## ✨ Features

- {{Feature 1}}
- {{Feature 2}}
- {{Feature 3}}

## 📦 Installation

### Prerequisites

- {{Requirement 1}}
- {{Requirement 2}}

### Quick Install

```bash
{{Install command}}
```

### From Source

```bash
git clone {{repository}}
cd {{project}}
{{Build commands}}
```

## 💡 Usage

### Basic Example

```{{language}}
{{Basic usage example}}
```

### Advanced Example

```{{language}}
{{Advanced usage example}}
```

### API Reference

See [API Documentation](docs/API.md) for complete API reference.

## 📚 Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/API.md)
- [User Guide](docs/guides/)
- [FAQ](docs/faq.md)

## 🛠️ Development

### Setup

```bash
{{Development setup commands}}
```

### Running Tests

```bash
{{Test commands}}
```

### Building

```bash
{{Build commands}}
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

### Quick Guide

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the {{License}} - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- {{Acknowledgment 1}}
- {{Acknowledgment 2}}

## 📞 Support

- Documentation: {{docs_url}}
- Issues: {{issues_url}}
- Email: {{support_email}}
```

## API Documentation Template

```markdown
# API Documentation

**Version:** {{version}}  
**Base URL:** `{{base_url}}`

## Overview

{{API overview}}

## Authentication

{{Authentication method}}

```{{language}}
{{Authentication example}}
```

## Endpoints

{{For each endpoint:}}

### {{HTTP Method}} {{Path}}

{{Description}}

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| {{param}} | {{type}} | {{yes/no}} | {{description}} |

#### Request Example

```{{language}}
{{Request example}}
```

#### Response

**Status Codes:**

- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

#### Response Example

```json
{{Response example}}
```

## Error Handling

{{Error handling documentation}}

## Rate Limiting

{{Rate limit information}}

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for version history.
```

## Architecture Document Template

```markdown
# Architecture Documentation

## System Overview

{{High-level system description}}

## Architecture Diagram

```mermaid
graph TB
    {{Architecture diagram}}
```

## Components

### {{Component Name}}

**Purpose:** {{Component purpose}}

**Responsibilities:**
- {{Responsibility 1}}
- {{Responsibility 2}}

**Technologies:** {{Technologies used}}

**Interfaces:**
- {{Interface 1}}
- {{Interface 2}}

## Data Flow

{{Data flow description}}

## Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | {{tech}} | {{version}} |
| Backend | {{tech}} | {{version}} |
| Database | {{tech}} | {{version}} |

## Design Decisions

### Decision: {{Decision}}

**Context:** {{Why this decision was needed}}

**Options Considered:**
1. {{Option 1}} - Pros/Cons
2. {{Option 2}} - Pros/Cons

**Decision:** {{Chosen option}}

**Consequences:** {{Impact of this decision}}

## Deployment

{{Deployment architecture}}

## Monitoring

{{Monitoring and observability}}

## Security

{{Security considerations}}
```

## Contributing Guide Template

```markdown
# Contributing Guide

## Welcome!

Thank you for considering contributing to {{Project Name}}!

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- Clear title and description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details

### Suggesting Features

Feature suggestions are welcome! Please provide:

- Use case
- Proposed solution
- Alternatives considered

### Pull Requests

1. Fork the repository
2. Create a branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit PR

## Development Setup

```bash
{{Setup instructions}}
```

## Coding Standards

{{Coding standards}}

## Testing

```bash
{{Testing instructions}}
```

## Documentation

{{Documentation guidelines}}

## Code Review Process

{{Code review process}}

## Questions?

Feel free to ask in our {{communication_channel}}!
```

## CHANGELOG Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- {{New features}}

### Changed
- {{Changes in existing functionality}}

### Deprecated
- {{Soon-to-be removed features}}

### Removed
- {{Removed features}}

### Fixed
- {{Bug fixes}}

### Security
- {{Security improvements}}

## [{{version}}] - {{date}}

### Added
- {{list of additions}}

### Changed
- {{list of changes}}

### Fixed
- {{list of fixes}}
```

## Usage Tips

1. **Copy the template** you need
2. **Replace {{placeholders}}** with your content
3. **Remove unused sections**
4. **Add project-specific details**
5. **Review and customize**

## Best Practices

- Keep templates up to date
- Share templates across projects
- Gather feedback on templates
- Evolve templates based on usage
