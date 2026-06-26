#!/usr/bin/env python3
"""
Documentation Generator
Generates README, API docs, and other documentation from code.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class DocsGenerator:
    """Generate documentation from code"""
    
    def __init__(self, path: str):
        self.root_path = Path(path).resolve()
        self.generated_files: List[str] = []
    
    def generate_readme(self, output: Optional[str] = None) -> str:
        """Generate README.md"""
        print("📝 Generating README.md...")
        
        project_name = self.root_path.name
        description = self._get_description()
        install_steps = self._get_install_steps()
        usage_examples = self._get_usage_examples()
        
        quick_start = install_steps if install_steps else '# Clone and install\ngit clone <repository-url>\nnpm install'
        
        content = f"""# {project_name.title().replace('-', ' ')}

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

## 🚀 Quick Start

```bash
{quick_start}
```

## 📝 About

{description if description else 'A brief description of the project goes here.'}

## ✨ Features

- Feature 1
- Feature 2
- Feature 3

## 📦 Installation

```bash
{install_steps if install_steps else '# Add installation steps here'}
```

## 💡 Usage

{usage_examples if usage_examples else '```python\n# Example usage\n# Add your usage examples here\n```'}

## 📚 Documentation

- [API Reference](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [User Guide](docs/guides/)

## 🛠️ Development

```bash
# Setup development environment
# Add your development setup steps here
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
"""
        
        output_path = output or (self.root_path / 'README.md')
        if isinstance(output_path, str):
            output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.generated_files.append(str(output_path))
        print(f"✅ Generated: {output_path}")
        return content
    
    def generate_api_docs(self, output: Optional[str] = None) -> str:
        """Generate API.md"""
        print("📝 Generating API.md...")
        
        endpoints = self._extract_api_endpoints()
        
        content = f"""# API Documentation

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This document describes the API endpoints available in this project.

## Base URL

```text
{{base_url}}
```

## Authentication

{{Authentication method and examples}}

## Endpoints

"""
        
        if endpoints:
            for endpoint in endpoints:
                content += f"""
### {endpoint.get('method', 'GET')} `{endpoint.get('path', '/unknown')}`

{endpoint.get('description', 'API endpoint')}

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| - | - | - | - |

**Response:**

```json
{{}}
```

**Example:**

```{{}}
{{Example code}}
```

"""
        else:
            content += "\n*No API endpoints detected. Add API documentation manually.*\n"
        
        output_path = output or (self.root_path / 'docs' / 'API.md')
        if isinstance(output_path, str):
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.generated_files.append(str(output_path))
        print(f"✅ Generated: {output_path}")
        return content
    
    def generate_architecture(self, output: Optional[str] = None) -> str:
        """Generate ARCHITECTURE.md"""
        print("📝 Generating ARCHITECTURE.md...")
        
        components = self._detect_components()
        
        content = f"""# Architecture Documentation

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## System Overview

{{High-level system description}}

## Architecture Diagram

```mermaid
graph TB
    A[Client] --> B[API Gateway]
    B --> C[Service Layer]
    C --> D[Data Layer]
```

## Components

"""
        
        if components:
            for comp in components:
                content += f"""
### {comp}

**Purpose:** {{Component purpose}}

**Responsibilities:**
- {{Responsibility 1}}
- {{Responsibility 2}}

**Technologies:** {{Technologies}}

"""
        else:
            content += "\n*Components not detected automatically. Add architecture details manually.*\n"
        
        content += """
## Data Flow

{{Data flow description}}

## Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | | |
| Backend | | |
| Database | | |

## Design Decisions

### Decision: {{Decision}}

**Context:** {{Why this decision was needed}}

**Options Considered:**
1. {{Option 1}}
2. {{Option 2}}

**Decision:** {{Chosen option}}

**Consequences:** {{Impact}}
"""
        
        output_path = output or (self.root_path / 'docs' / 'ARCHITECTURE.md')
        if isinstance(output_path, str):
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.generated_files.append(str(output_path))
        print(f"✅ Generated: {output_path}")
        return content
    
    def _get_description(self) -> str:
        """Extract project description"""
        # Try package.json
        pkg_json = self.root_path / 'package.json'
        if pkg_json.exists():
            try:
                with open(pkg_json) as f:
                    data = json.load(f)
                    return data.get('description', '')
            except:
                pass
        
        # Try setup.py
        setup_py = self.root_path / 'setup.py'
        if setup_py.exists():
            try:
                with open(setup_py, 'r') as f:
                    content = f.read()
                    match = re.search(r'description=[\'"]([^\'"]+)[\'"]', content)
                    if match:
                        return match.group(1)
            except:
                pass
        
        return ''
    
    def _get_install_steps(self) -> str:
        """Detect installation steps"""
        steps = []
        
        if (self.root_path / 'package.json').exists():
            steps.append('npm install')
        
        if (self.root_path / 'requirements.txt').exists():
            steps.append('pip install -r requirements.txt')
        
        if (self.root_path / 'Cargo.toml').exists():
            steps.append('cargo build')
        
        if (self.root_path / 'go.mod').exists():
            steps.append('go mod download')
        
        return '\n'.join(steps)
    
    def _get_usage_examples(self) -> str:
        """Find usage examples"""
        examples_dir = self.root_path / 'examples'
        if examples_dir.exists():
            for file_path in examples_dir.glob('*'):
                if file_path.is_file():
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read(1000)
                            return f"```{file_path.suffix[1:]}\n{content}\n```"
                    except:
                        pass
        return ''
    
    def _extract_api_endpoints(self) -> List[Dict]:
        """Extract API endpoints from code"""
        endpoints = []
        
        for file_path in self.root_path.rglob('*.py'):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                    # Flask/FastAPI routes
                    for match in re.finditer(r'@(?:app|router)\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]', content, re.IGNORECASE):
                        endpoints.append({
                            'method': match.group(1).upper(),
                            'path': match.group(2),
                            'file': str(file_path.relative_to(self.root_path)),
                            'description': 'API endpoint'
                        })
            except:
                pass
        
        return endpoints[:20]
    
    def _detect_components(self) -> List[str]:
        """Detect system components from directory structure"""
        components = []
        
        for dir_path in self.root_path.iterdir():
            if dir_path.is_dir() and not dir_path.name.startswith('.'):
                if dir_path.name in ['src', 'app', 'services', 'api', 'web', 'client', 'server']:
                    components.append(dir_path.name.title())
        
        return components if components else ['API', 'Service', 'Database']
    
    def generate_all(self, output_dir: Optional[str] = None):
        """Generate all documentation"""
        target_dir = Path(output_dir) if output_dir else self.root_path
        
        self.generate_readme(str(target_dir / 'README.md'))
        self.generate_api_docs(str(target_dir / 'docs' / 'API.md'))
        self.generate_architecture(str(target_dir / 'docs' / 'ARCHITECTURE.md'))
        
        print(f"\n✅ Generated {len(self.generated_files)} files")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate documentation')
    parser.add_argument('--path', '-p', default='.', help='Path to project')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--type', '-t', choices=['readme', 'api', 'architecture', 'all'], default='all')
    
    args = parser.parse_args()
    
    generator = DocsGenerator(args.path)
    
    if args.type == 'readme':
        generator.generate_readme()
    elif args.type == 'api':
        generator.generate_api_docs()
    elif args.type == 'architecture':
        generator.generate_architecture()
    else:
        generator.generate_all(args.output)


if __name__ == '__main__':
    main()
