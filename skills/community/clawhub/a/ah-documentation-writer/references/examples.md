# Documentation Writer — Code Examples

## Example 1

```typescript
// documentation-generator.ts
import * as fs from 'fs/promises';
import * as path from 'path';
import * as ts from 'typescript';
import { parse as parseJSDoc } from 'comment-parser';
import * as marked from 'marked';
import * as yaml from 'js-yaml';

interface DocumentationConfig {
  projectPath: string;
  outputPath: string;
  format: 'markdown' | 'html' | 'json';
  includes: string[];
  excludes: string[];
  templates?: Map<string, string>;
  plugins?: DocumentationPlugin[];
}

interface DocumentationSection {
  id: string;
  title: string;
  content: string;
  level: number;
  children: DocumentationSection[];
  metadata?: any;
}

class DocumentationGenerator {
  private config: DocumentationConfig;
  private sections: Map<string, DocumentationSection> = new Map();
  private templates: Map<string, HandlebarsTemplate> = new Map();
  private analyzers: Map<string, CodeAnalyzer> = new Map();

  constructor(config: DocumentationConfig) {
    this.config = config;
    this.initializeAnalyzers();
    this.loadTemplates();
  }

  async generate(): Promise<Documentation> {
    // Analyze project structure
    const structure = await this.analyzeProjectStructure();
    
    // Extract code documentation
    const codeDoc = await this.extractCodeDocumentation();
    
    // Generate API documentation
    const apiDoc = await this.generateAPIDocs();
    
    // Create user guides
    const guides = await this.generateUserGuides();
    
    // Generate architecture docs
    const architecture = await this.generateArchitectureDocs();
    
    // Generate README
    const readme = await this.generateREADME({
      structure,
      codeDoc,
      apiDoc,
      guides,
      architecture,
    });
    
    // Compile full documentation
    const documentation = this.compileDocumentation({
      readme,
      architecture,
      api: apiDoc,
      guides,
      code: codeDoc,
      changelog: await this.generateChangelog(),
      contributing: await this.generateContributing(),
    });
    
    // Validate documentation
    await this.validateDocumentation(documentation);
    
    // Write documentation
    await this.writeDocumentation(documentation);
    
    return documentation;
  }

  private async analyzeProjectStructure(): Promise<ProjectStructure> {
    const structure: ProjectStructure = {
      root: this.config.projectPath,
      files: [],
      directories: [],
      languages: new Set(),
      frameworks: new Set(),
      dependencies: new Map(),
    };
    
    // Scan project files
    await this.scanDirectory(this.config.projectPath, structure);
    
    // Detect languages and frameworks
    await this.detectTechnologies(structure);
    
    // Analyze dependencies
    await this.analyzeDependencies(structure);
    
    return structure;
  }

  private async extractCodeDocumentation(): Promise<CodeDocumentation> {
    const docs: CodeDocumentation = {
      classes: [],
      functions: [],
      interfaces: [],
      types: [],
      constants: [],
      modules: [],
    };
    
    // Find all source files
    const sourceFiles = await this.findSourceFiles();
    
    for (const file of sourceFiles) {
      const analyzer = this.getAnalyzer(file);
      if (analyzer) {
        const fileDoc = await analyzer.analyze(file);
        this.mergeDocumentation(docs, fileDoc);
      }
    }
    
    return docs;
  }

  private async generateAPIDocs(): Promise<APIDocumentation> {
    const apiDoc: APIDocumentation = {
      endpoints: [],
      schemas: [],
      authentication: [],
      examples: [],
    };
    
    // Find API definition files
    const openApiFiles = await this.findFiles('**/openapi.{yaml,yml,json}');
    const swaggerFiles = await this.findFiles('**/swagger.{yaml,yml,json}');
    
    // Parse OpenAPI/Swagger
    for (const file of [...openApiFiles, ...swaggerFiles]) {
      const content = await fs.readFile(file, 'utf-8');
      const spec = file.endsWith('.json') 
        ? JSON.parse(content)
        : yaml.load(content);
      
      apiDoc.endpoints.push(...this.extractEndpoints(spec));
      apiDoc.schemas.push(...this.extractSchemas(spec));
    }
    
    // Find route handlers
    const routes = await this.findRouteHandlers();
    apiDoc.endpoints.push(...routes);
    
    // Generate examples
    apiDoc.examples = this.generateAPIExamples(apiDoc.endpoints);
    
    return apiDoc;
  }

  private async generateUserGuides(): Promise<UserGuide[]> {
    const guides: UserGuide[] = [];
    
    // Getting Started Guide
    guides.push({
      id: 'getting-started',
      title: 'Getting Started',
      sections: [
        await this.generateInstallation(),
        await this.generateQuickStart(),
        await this.generateBasicUsage(),
      ],
    });
    
    // User Guide
    guides.push({
      id: 'user-guide',
      title: 'User Guide',
      sections: [
        await this.generateFeatures(),
        await this.generateConfiguration(),
        await this.generateAdvancedUsage(),
      ],
    });
    
    // Troubleshooting Guide
    guides.push({
      id: 'troubleshooting',
      title: 'Troubleshooting',
      sections: [
        await this.generateCommonIssues(),
        await this.generateFAQ(),
        await this.generateSupport(),
      ],
    });
    
    return guides;
  }

  private async generateArchitectureDocs(): Promise<ArchitectureDocumentation> {
    const architecture: ArchitectureDocumentation = {
      overview: await this.generateArchitectureOverview(),
      components: await this.analyzeComponents(),
      dataFlow: await this.analyzeDataFlow(),
      diagrams: await this.generateDiagrams(),
      decisions: await this.findArchitectureDecisions(),
    };
    
    return architecture;
  }

  private async generateREADME(data: any): Promise<string> {
    const template = this.templates.get('readme') || this.getDefaultREADMETemplate();
    
    const context = {
      projectName: await this.detectProjectName(),
      description: await this.generateDescription(data),
      badges: this.generateBadges(),
      installation: await this.generateInstallation(),
      usage: await this.generateBasicUsage(),
      features: await this.generateFeatureList(data),
      documentation: this.generateDocLinks(),
      contributing: 'See [CONTRIBUTING.md](CONTRIBUTING.md)',
      license: await this.detectLicense(),
    };
    
    return template(context);
  }

  private async generateInstallation(): Promise<DocumentationSection> {
    const packageManagers = await this.detectPackageManagers();
    const installCommands: string[] = [];
    
    if (packageManagers.has('npm')) {
      installCommands.push('npm install');
    }
    if (packageManagers.has('yarn')) {
      installCommands.push('yarn install');
    }
    if (packageManagers.has('pip')) {
      installCommands.push('pip install -r requirements.txt');
    }
    if (packageManagers.has('go')) {
      installCommands.push('go get');
    }
    
    return {
      id: 'installation',
      title: 'Installation',
      level: 2,
      content: this.formatInstallation(installCommands),
      children: [],
    };
  }

  private formatInstallation(commands: string[]): string {
    if (commands.length === 0) {
      return 'No installation steps detected.';
    }
    
    return `
## Prerequisites

- Node.js >= 14.0.0 (if using npm/yarn)
- Python >= 3.7 (if using pip)
- Go >= 1.16 (if using go modules)

## Install Dependencies

\`\`\`bash
${commands[0]}
\`\`\`

${commands.length > 1 ? `
### Alternative Package Managers

${commands.slice(1).map(cmd => `\`\`\`bash\n${cmd}\n\`\`\``).join('\n\n')}
` : ''}
`;
  }

  private async generateQuickStart(): Promise<DocumentationSection> {
    const examples = await this.findExamples();
    
    return {
      id: 'quick-start',
      title: 'Quick Start',
      level: 2,
      content: `
## Quick Start

### Basic Example

\`\`\`javascript
${examples[0] || '// Add your first example here'}
\`\`\`

### Running the Application

\`\`\`bash
npm start
\`\`\`

### Verify Installation

\`\`\`bash
npm test
\`\`\`
`,
      children: [],
    };
  }

  private async generateChangelog(): Promise<DocumentationSection> {
    const changelog = await this.parseChangelog();
    
    if (!changelog) {
      return this.generateDefaultChangelog();
    }
    
    return {
      id: 'changelog',
      title: 'Changelog',
      level: 1,
      content: changelog,
      children: [],
    };
  }

  private async generateContributing(): Promise<DocumentationSection> {
    return {
      id: 'contributing',
      title: 'Contributing',
      level: 1,
      content: `
# Contributing

We welcome contributions! Please see our [Code of Conduct](CODE_OF_CONDUCT.md) first.

## How to Contribute

1. Fork the repository
2. Create your feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit your changes (\`git commit -m 'Add some amazing feature'\`)
4. Push to the branch (\`git push origin feature/amazing-feature\`)
5. Open a Pull Request

## Development Setup

\`\`\`bash
# Clone your fork
git clone https://github.com/your-username/project-name.git

# Install dependencies
npm install

# Run tests
npm test

# Run development server
npm run dev
\`\`\`

## Coding Standards

- Follow existing code style
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and descriptive

## Pull Request Process

1. Update the README.md with details of changes
2. Update the CHANGELOG.md with your changes
3. Ensure all tests pass
4. Request review from maintainers
`,
      children: [],
    };
  }

  private compileDocumentation(sections: any): Documentation {
    return {
      version: '1.0.0',
      generated: new Date(),
      format: this.config.format,
      sections: Object.entries(sections).map(([key, value]) => ({
        id: key,
        title: this.titleCase(key),
        content: value,
        level: 1,
        children: [],
      })),
      metadata: {
        generator: 'documentation-writer',
        config: this.config,
      },
    };
  }

  private async validateDocumentation(doc: Documentation): Promise<void> {
    const errors: string[] = [];
    
    // Check for broken links
    const links = this.extractLinks(doc);
    for (const link of links) {
      if (!await this.validateLink(link)) {
        errors.push(`Broken link: ${link}`);
      }
    }
    
    // Check for missing sections
    const requiredSections = ['readme', 'installation', 'usage'];
    for (const section of requiredSections) {
      if (!doc.sections.find(s => s.id === section)) {
        errors.push(`Missing required section: ${section}`);
      }
    }
    
    // Check code examples
    const codeBlocks = this.extractCodeBlocks(doc);
    for (const block of codeBlocks) {
      if (!this.validateCodeBlock(block)) {
        errors.push(`Invalid code block: ${block.language}`);
      }
    }
    
    if (errors.length > 0) {
      console.warn('Documentation validation warnings:', errors);
    }
  }

  private async writeDocumentation(doc: Documentation): Promise<void> {
    const outputPath = this.config.outputPath;
    
    // Create output directory
    await fs.mkdir(outputPath, { recursive: true });
    
    // Write main documentation
    for (const section of doc.sections) {
      const fileName = `${section.id}.md`;
      const filePath = path.join(outputPath, fileName);
      await fs.writeFile(filePath, this.formatSection(section));
    }
    
    // Generate index
    const index = this.generateIndex(doc);
    await fs.writeFile(path.join(outputPath, 'index.md'), index);
    
    // Generate HTML if requested
    if (this.config.format === 'html') {
      await this.generateHTML(doc);
    }
    
    // Generate JSON if requested
    if (this.config.format === 'json') {
      await fs.writeFile(
        path.join(outputPath, 'documentation.json'),
        JSON.stringify(doc, null, 2)
      );
    }
  }

  private formatSection(section: DocumentationSection): string {
    const heading = '#'.repeat(section.level) + ' ' + section.title;
    const content = section.content;
    const children = section.children
      .map(child => this.formatSection(child))
      .join('\n\n');
    
    return `${heading}\n\n${content}\n\n${children}`.trim();
  }

  private generateIndex(doc: Documentation): string {
    const toc = this.generateTableOfContents(doc);
    
    return `# Documentation

${toc}

## Overview

This documentation was automatically generated on ${doc.generated.toISOString()}.

## Sections

${doc.sections.map(s => `- [${s.title}](${s.id}.md)`).join('\n')}

## Quick Links

- [Getting Started](getting-started.md)
- [API Reference](api.md)
- [Contributing](contributing.md)
- [Changelog](changelog.md)
`;
  }

  private generateTableOfContents(doc: Documentation): string {
    const toc: string[] = ['## Table of Contents\n'];
    
    for (const section of doc.sections) {
      toc.push(this.generateTOCEntry(section, 0));
    }
    
    return toc.join('\n');
  }

  private generateTOCEntry(section: DocumentationSection, depth: number): string {
    const indent = '  '.repeat(depth);
    const entry = `${indent}- [${section.title}](#${section.id})`;
    const children = section.children
      .map(child => this.generateTOCEntry(child, depth + 1))
      .join('\n');
    
    return children ? `${entry}\n${children}` : entry;
  }

  private async generateHTML(doc: Documentation): Promise<void> {
    const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.min.css">
    <style>
        body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }
    </style>
</head>
<body class="markdown-body">
    ${doc.sections.map(s => this.sectionToHTML(s)).join('\n')}
</body>
</html>
`;
    
    await fs.writeFile(
      path.join(this.config.outputPath, 'index.html'),
      html
    );
  }

  private sectionToHTML(section: DocumentationSection): string {
    const html = marked.parse(this.formatSection(section));
    return `<section id="${section.id}">${html}</section>`;
  }

  private initializeAnalyzers(): void {
    this.analyzers.set('.ts', new TypeScriptAnalyzer());
    this.analyzers.set('.js', new JavaScriptAnalyzer());
    this.analyzers.set('.py', new PythonAnalyzer());
    this.analyzers.set('.go', new GoAnalyzer());
    this.analyzers.set('.java', new JavaAnalyzer());
  }

  private getAnalyzer(file: string): CodeAnalyzer | undefined {
    const ext = path.extname(file);
    return this.analyzers.get(ext);
  }

  private async findSourceFiles(): Promise<string[]> {
    const files: string[] = [];
    const extensions = ['.ts', '.js', '.py', '.go', '.java', '.rs'];
    
    for (const ext of extensions) {
      const pattern = `**/*${ext}`;
      const found = await this.findFiles(pattern);
      files.push(...found);
    }
    
    return files;
  }

  private async findFiles(pattern: string): Promise<string[]> {
    // Implementation would use glob or similar
    return [];
  }

  private extractLinks(doc: Documentation): string[] {
    const links: string[] = [];
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    
    for (const section of doc.sections) {
      const matches = section.content.matchAll(linkRegex);
      for (const match of matches) {
        links.push(match[2]);
      }
    }
    
    return links;
  }

  private async validateLink(link: string): Promise<boolean> {
    if (link.startsWith('http')) {
      // Check external link
      try {
        const response = await fetch(link, { method: 'HEAD' });
        return response.ok;
      } catch {
        return false;
      }
    } else {
      // Check local file
      try {
        await fs.access(path.join(this.config.projectPath, link));
        return true;
      } catch {
        return false;
      }
    }
  }

  private extractCodeBlocks(doc: Documentation): CodeBlock[] {
    const blocks: CodeBlock[] = [];
    const codeRegex = /```(\w+)?\n([\s\S]*?)```/g;
    
    for (const section of doc.sections) {
      const matches = section.content.matchAll(codeRegex);
      for (const match of matches) {
        blocks.push({
          language: match[1] || 'text',
          code: match[2],
        });
      }
    }
    
    return blocks;
  }

  private validateCodeBlock(block: CodeBlock): boolean {
    // Basic validation - could be extended with syntax checking
    return block.code.trim().length > 0;
  }

  private titleCase(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1).replace(/-/g, ' ');
  }

  private getDefaultREADMETemplate(): HandlebarsTemplate {
    return (context: any) => `# ${context.projectName}

${context.badges}

${context.description}

## Installation

${context.installation}

## Usage

${context.usage}

## Features

${context.features}

## Documentation

${context.documentation}

## Contributing

${context.contributing}

## License

${context.license}
`;
  }

  // Additional helper methods...
  private async detectProjectName(): Promise<string> {
    try {
      const packageJson = await fs.readFile(
        path.join(this.config.projectPath, 'package.json'),
        'utf-8'
      );
      return JSON.parse(packageJson).name;
    } catch {
      return path.basename(this.config.projectPath);
    }
  }

  private async generateDescription(data: any): Promise<string> {
    // Generate description based on analyzed data
    return 'A comprehensive project with excellent documentation.';
  }

  private generateBadges(): string {
    return `
[![Build Status](https://img.shields.io/github/workflow/status/user/repo/CI)](https://github.com/user/repo/actions)
[![Coverage](https://img.shields.io/codecov/c/github/user/repo)](https://codecov.io/gh/user/repo)
[![License](https://img.shields.io/github/license/user/repo)](LICENSE)
[![Version](https://img.shields.io/npm/v/package)](https://www.npmjs.com/package/package)
`;
  }

  private async generateFeatureList(data: any): Promise<string> {
    const features = [
      '✨ Feature 1',
      '🚀 Feature 2',
      '🔧 Feature 3',
    ];
    
    return features.join('\n');
  }

  private generateDocLinks(): string {
    return `
- [Getting Started](docs/getting-started.md)
- [API Reference](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Contributing](CONTRIBUTING.md)
`;
  }

  private async detectLicense(): Promise<string> {
    try {
      await fs.access(path.join(this.config.projectPath, 'LICENSE'));
      return 'This project is licensed under the terms in the [LICENSE](LICENSE) file.';
    } catch {
      return 'License information not available.';
    }
  }
}

// Analyzer implementations
abstract class CodeAnalyzer {
  abstract analyze(file: string): Promise<CodeDocumentation>;
}

class TypeScriptAnalyzer extends CodeAnalyzer {
  async analyze(file: string): Promise<CodeDocumentation> {
    const source = await fs.readFile(file, 'utf-8');
    const sourceFile = ts.createSourceFile(
      file,
      source,
      ts.ScriptTarget.Latest,
      true
    );
    
    const docs: CodeDocumentation = {
      classes: [],
      functions: [],
      interfaces: [],
      types: [],
      constants: [],
      modules: [],
    };
    
    ts.forEachChild(sourceFile, node => {
      if (ts.isClassDeclaration(node) && node.name) {
        docs.classes.push(this.extractClass(node));
      } else if (ts.isFunctionDeclaration(node) && node.name) {
        docs.functions.push(this.extractFunction(node));
      } else if (ts.isInterfaceDeclaration(node)) {
        docs.interfaces.push(this.extractInterface(node));
      }
    });
    
    return docs;
  }

  private extractClass(node: ts.ClassDeclaration): any {
    return {
      name: node.name?.getText(),
      documentation: this.extractJSDoc(node),
      members: [],
    };
  }

  private extractFunction(node: ts.FunctionDeclaration): any {
    return {
      name: node.name?.getText(),
      documentation: this.extractJSDoc(node),
      parameters: node.parameters.map(p => p.name.getText()),
    };
  }

  private extractInterface(node: ts.InterfaceDeclaration): any {
    return {
      name: node.name.getText(),
      documentation: this.extractJSDoc(node),
      properties: [],
    };
  }

  private extractJSDoc(node: ts.Node): string {
    const text = node.getFullText();
    const match = text.match(/\/\*\*([\s\S]*?)\*\//);
    return match ? match[1].trim() : '';
  }
}

class JavaScriptAnalyzer extends CodeAnalyzer {
  async analyze(file: string): Promise<CodeDocumentation> {
    // Similar to TypeScript but for JavaScript
    return {
      classes: [],
      functions: [],
      interfaces: [],
      types: [],
      constants: [],
      modules: [],
    };
  }
}

class PythonAnalyzer extends CodeAnalyzer {
  async analyze(file: string): Promise<CodeDocumentation> {
    // Python-specific analysis
    return {
      classes: [],
      functions: [],
      interfaces: [],
      types: [],
      constants: [],
      modules: [],
    };
  }
}

class GoAnalyzer extends CodeAnalyzer {
  async analyze(file: string): Promise<CodeDocumentation> {
    // Go-specific analysis
    return {
      classes: [],
      functions: [],
      interfaces: [],
      types: [],
      constants: [],
      modules: [],
    };
  }
}

class JavaAnalyzer extends CodeAnalyzer {
  async analyze(file: string): Promise<CodeDocumentation> {
    // Java-specific analysis
    return {
      classes: [],
      functions: [],
      interfaces: [],
      types: [],
      constants: [],
      modules: [],
    };
  }
}

// Type definitions
interface Documentation {
  version: string;
  generated: Date;
  format: string;
  sections: DocumentationSection[];
  metadata: any;
}

interface ProjectStructure {
  root: string;
  files: string[];
  directories: string[];
  languages: Set<string>;
  frameworks: Set<string>;
  dependencies: Map<string, string>;
}

interface CodeDocumentation {
  classes: any[];
  functions: any[];
  interfaces: any[];
  types: any[];
  constants: any[];
  modules: any[];
}

interface APIDocumentation {
  endpoints: any[];
  schemas: any[];
  authentication: any[];
  examples: any[];
}

interface UserGuide {
  id: string;
  title: string;
  sections: DocumentationSection[];
}

interface ArchitectureDocumentation {
  overview: DocumentationSection;
  components: any[];
  dataFlow: any[];
  diagrams: any[];
  decisions: any[];
}

interface CodeBlock {
  language: string;
  code: string;
}

interface HandlebarsTemplate {
  (context: any): string;
}

interface DocumentationPlugin {
  name: string;
  process(doc: Documentation): Promise<Documentation>;
}

// Export the generator
export { DocumentationGenerator, DocumentationConfig, Documentation };
```

## Example 2

```typescript
// api-templates.ts
export const apiTemplates = {
  endpoint: `
## {{method}} {{path}}

{{description}}

### Parameters

{{#if pathParams}}
#### Path Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
{{#each pathParams}}
| {{name}} | {{type}} | {{required}} | {{description}} |
{{/each}}
{{/if}}

{{#if queryParams}}
#### Query Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
{{#each queryParams}}
| {{name}} | {{type}} | {{required}} | {{description}} |
{{/each}}
{{/if}}

### Request Body

\`\`\`json
{{requestExample}}
\`\`\`

### Response

#### Success Response ({{successCode}})

\`\`\`json
{{responseExample}}
\`\`\`

#### Error Responses

{{#each errorResponses}}
- **{{code}}**: {{description}}
{{/each}}

### Example

\`\`\`bash
curl -X {{method}} \\
  {{curlExample}}
\`\`\`
`,

  schema: `
## {{name}}

{{description}}

### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
{{#each properties}}
| {{name}} | {{type}} | {{required}} | {{description}} |
{{/each}}

### Example

\`\`\`json
{{example}}
\`\`\`
`,
};
```
