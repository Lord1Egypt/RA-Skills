# Technical Writer — Code Examples

## Example 1

```typescript
// technical-writer.ts
import * as fs from 'fs/promises';
import * as path from 'path';
import { marked } from 'marked';
import * as yaml from 'js-yaml';

interface Documentation {
  id: string;
  title: string;
  type: DocumentationType;
  audience: Audience;
  purpose: string;
  scope: string;
  structure: DocumentStructure;
  content: ContentSection[];
  metadata: DocumentMetadata;
  version: string;
  status: DocumentStatus;
}

interface ContentSection {
  id: string;
  title: string;
  level: number;
  content: string;
  type: ContentType;
  examples?: Example[];
  diagrams?: Diagram[];
  code?: CodeSnippet[];
  warnings?: Warning[];
  notes?: Note[];
  references?: Reference[];
  subsections?: ContentSection[];
}

interface DocumentStructure {
  template: string;
  sections: SectionDefinition[];
  navigation: NavigationStructure;
  crossReferences: CrossReference[];
}

class TechnicalDocumentationWriter {
  private templates: Map<string, DocumentTemplate> = new Map();
  private styleGuide: StyleGuide;
  private glossary: Map<string, GlossaryTerm> = new Map();
  private analyzer: ContentAnalyzer;
  private validator: DocumentValidator;

  constructor() {
    this.styleGuide = new StyleGuide();
    this.analyzer = new ContentAnalyzer();
    this.validator = new DocumentValidator();
    this.loadTemplates();
    this.loadGlossary();
  }

  async createDocumentation(
    subject: DocumentationSubject,
    requirements: DocumentationRequirements
  ): Promise<Documentation> {
    // Analyze subject matter
    const analysis = await this.analyzer.analyzeSubject(subject);
    
    // Determine documentation type
    const docType = this.determineDocumentationType(analysis, requirements);
    
    // Select appropriate template
    const template = this.selectTemplate(docType, requirements);
    
    // Generate document structure
    const structure = this.generateStructure(template, analysis, requirements);
    
    // Create content sections
    const content = await this.createContent(structure, analysis, requirements);
    
    // Add examples and code snippets
    const enrichedContent = await this.enrichContent(content, subject);
    
    // Apply style guide
    const styledContent = this.applyStyleGuide(enrichedContent);
    
    // Add diagrams and visuals
    const visualContent = await this.addVisuals(styledContent, analysis);
    
    // Generate metadata
    const metadata = this.generateMetadata(subject, requirements);
    
    // Validate documentation
    await this.validator.validate(visualContent);
    
    return {
      id: this.generateId('DOC'),
      title: requirements.title || this.generateTitle(subject),
      type: docType,
      audience: requirements.audience,
      purpose: requirements.purpose,
      scope: requirements.scope,
      structure,
      content: visualContent,
      metadata,
      version: '1.0.0',
      status: DocumentStatus.DRAFT,
    };
  }

  async createUserGuide(product: Product): Promise<UserGuide> {
    const guide: UserGuide = {
      id: this.generateId('UG'),
      title: `${product.name} User Guide`,
      product: product.name,
      version: product.version,
      audience: Audience.END_USER,
      sections: [],
      quickStart: null,
      troubleshooting: null,
      faq: null,
      glossary: [],
      index: [],
    };
    
    // Introduction section
    guide.sections.push(this.createIntroduction(product));
    
    // Getting Started
    guide.quickStart = this.createQuickStart(product);
    guide.sections.push(guide.quickStart);
    
    // Features and functionality
    for (const feature of product.features) {
      guide.sections.push(this.documentFeature(feature));
    }
    
    // Configuration and settings
    if (product.configuration) {
      guide.sections.push(this.documentConfiguration(product.configuration));
    }
    
    // Troubleshooting
    guide.troubleshooting = this.createTroubleshooting(product);
    guide.sections.push(guide.troubleshooting);
    
    // FAQ
    guide.faq = this.createFAQ(product);
    guide.sections.push(guide.faq);
    
    // Glossary
    guide.glossary = this.createGlossary(product);
    
    // Index
    guide.index = this.createIndex(guide);
    
    return guide;
  }

  private createIntroduction(product: Product): ContentSection {
    return {
      id: 'introduction',
      title: 'Introduction',
      level: 1,
      type: ContentType.CONCEPTUAL,
      content: `
# Introduction

Welcome to ${product.name} version ${product.version}. This guide provides comprehensive information about using ${product.name} effectively.

## About ${product.name}

${product.description}

## Who Should Read This Guide

This guide is intended for:
${this.formatAudience(product.targetAudience)}

## What's in This Guide

This guide covers:
${this.formatTopics(product.features.map(f => f.name))}

## Document Conventions

This guide uses the following conventions:

| Convention | Meaning |
|------------|---------|
| **Bold** | User interface elements |
| \`Code\` | Code, commands, or file names |
| _Italic_ | Emphasis or new terms |
| 📝 Note | Additional information |
| ⚠️ Warning | Important caution |
| 💡 Tip | Helpful suggestion |

## Prerequisites

Before using ${product.name}, ensure you have:
${this.formatPrerequisites(product.prerequisites)}
`,
      notes: [
        {
          type: NoteType.INFO,
          content: 'This guide assumes basic familiarity with ' + product.domain,
        },
      ],
    };
  }

  private createQuickStart(product: Product): ContentSection {
    return {
      id: 'quick-start',
      title: 'Quick Start Guide',
      level: 1,
      type: ContentType.TUTORIAL,
      content: `
# Quick Start Guide

Get up and running with ${product.name} in minutes.

## Step 1: Installation

${this.generateInstallationSteps(product)}

## Step 2: Initial Setup

${this.generateSetupSteps(product)}

## Step 3: First Use

${this.generateFirstUseSteps(product)}

## Step 4: Verify Installation

${this.generateVerificationSteps(product)}

## What's Next?

Now that you have ${product.name} running:
- Explore the [Features](#features) section
- Review [Configuration](#configuration) options
- Check out [Advanced Topics](#advanced)
`,
      examples: [
        {
          title: 'Basic Example',
          description: 'A simple example to get started',
          code: this.generateBasicExample(product),
        },
      ],
    };
  }

  async createAPIDocumentation(api: APISpecification): Promise<APIDocumentation> {
    const doc: APIDocumentation = {
      id: this.generateId('API'),
      title: `${api.name} API Documentation`,
      version: api.version,
      baseUrl: api.baseUrl,
      authentication: this.documentAuthentication(api.authentication),
      endpoints: [],
      schemas: [],
      examples: [],
      errors: this.documentErrorCodes(api.errors),
      rateLimiting: this.documentRateLimiting(api.rateLimiting),
      changelog: [],
    };
    
    // Document each endpoint
    for (const endpoint of api.endpoints) {
      doc.endpoints.push(await this.documentEndpoint(endpoint));
    }
    
    // Document schemas
    for (const schema of api.schemas) {
      doc.schemas.push(this.documentSchema(schema));
    }
    
    // Generate examples
    doc.examples = this.generateAPIExamples(api);
    
    // Add changelog
    doc.changelog = await this.generateChangelog(api);
    
    return doc;
  }

  private async documentEndpoint(endpoint: APIEndpoint): Promise<EndpointDocumentation> {
    return {
      id: endpoint.id,
      method: endpoint.method,
      path: endpoint.path,
      summary: endpoint.summary,
      description: this.expandDescription(endpoint.description),
      parameters: this.documentParameters(endpoint.parameters),
      requestBody: endpoint.requestBody ? this.documentRequestBody(endpoint.requestBody) : null,
      responses: this.documentResponses(endpoint.responses),
      examples: this.generateEndpointExamples(endpoint),
      security: endpoint.security,
      deprecated: endpoint.deprecated || false,
      tags: endpoint.tags || [],
    };
  }

  private documentParameters(parameters: Parameter[]): ParameterDocumentation[] {
    return parameters.map(param => ({
      name: param.name,
      in: param.in,
      description: this.expandDescription(param.description),
      required: param.required,
      type: param.type,
      format: param.format,
      default: param.default,
      enum: param.enum,
      example: param.example || this.generateParameterExample(param),
      constraints: this.documentConstraints(param),
    }));
  }

  private generateEndpointExamples(endpoint: APIEndpoint): EndpointExample[] {
    const examples: EndpointExample[] = [];
    
    // cURL example
    examples.push({
      title: 'cURL',
      language: 'bash',
      code: this.generateCurlExample(endpoint),
    });
    
    // JavaScript example
    examples.push({
      title: 'JavaScript',
      language: 'javascript',
      code: this.generateJavaScriptExample(endpoint),
    });
    
    // Python example
    examples.push({
      title: 'Python',
      language: 'python',
      code: this.generatePythonExample(endpoint),
    });
    
    return examples;
  }

  private generateCurlExample(endpoint: APIEndpoint): string {
    let curl = `curl -X ${endpoint.method} \\\n`;
    curl += `  '${endpoint.baseUrl || 'https://api.example.com'}${endpoint.path}' \\\n`;
    
    if (endpoint.headers) {
      for (const [key, value] of Object.entries(endpoint.headers)) {
        curl += `  -H '${key}: ${value}' \\\n`;
      }
    }
    
    if (endpoint.requestBody) {
      curl += `  -d '${JSON.stringify(endpoint.requestBody.example, null, 2)}'`;
    }
    
    return curl;
  }

  async createTutorial(topic: TutorialTopic): Promise<Tutorial> {
    const tutorial: Tutorial = {
      id: this.generateId('TUT'),
      title: topic.title,
      difficulty: topic.difficulty,
      duration: topic.estimatedDuration,
      objectives: topic.objectives,
      prerequisites: topic.prerequisites,
      sections: [],
      exercises: [],
      solutions: [],
      resources: [],
    };
    
    // Introduction
    tutorial.sections.push(this.createTutorialIntroduction(topic));
    
    // Learning objectives
    tutorial.sections.push(this.createLearningObjectives(topic));
    
    // Main content sections
    for (const section of topic.sections) {
      tutorial.sections.push(await this.createTutorialSection(section));
    }
    
    // Exercises
    tutorial.exercises = this.createExercises(topic);
    
    // Solutions
    tutorial.solutions = this.createSolutions(tutorial.exercises);
    
    // Additional resources
    tutorial.resources = this.compileResources(topic);
    
    // Summary
    tutorial.sections.push(this.createTutorialSummary(topic));
    
    return tutorial;
  }

  private async createTutorialSection(section: TutorialSection): Promise<ContentSection> {
    const content: ContentSection = {
      id: section.id,
      title: section.title,
      level: 2,
      type: ContentType.TUTORIAL,
      content: '',
      examples: [],
      code: [],
      notes: [],
      warnings: [],
    };
    
    // Generate section content
    content.content = await this.generateSectionContent(section);
    
    // Add step-by-step instructions
    if (section.steps) {
      content.content += this.formatSteps(section.steps);
    }
    
    // Add code examples
    if (section.code) {
      content.code = section.code.map(c => this.formatCodeSnippet(c));
    }
    
    // Add explanations
    if (section.explanations) {
      for (const explanation of section.explanations) {
        content.notes?.push({
          type: NoteType.EXPLANATION,
          content: explanation,
        });
      }
    }
    
    // Add tips
    if (section.tips) {
      for (const tip of section.tips) {
        content.notes?.push({
          type: NoteType.TIP,
          content: tip,
        });
      }
    }
    
    // Add warnings
    if (section.warnings) {
      for (const warning of section.warnings) {
        content.warnings?.push({
          type: WarningType.CAUTION,
          content: warning,
        });
      }
    }
    
    return content;
  }

  async createReleaseNotes(release: Release): Promise<ReleaseNotes> {
    const notes: ReleaseNotes = {
      id: this.generateId('RN'),
      version: release.version,
      date: release.date,
      title: `Release Notes - Version ${release.version}`,
      summary: release.summary,
      highlights: release.highlights,
      newFeatures: [],
      improvements: [],
      bugFixes: [],
      breakingChanges: [],
      deprecations: [],
      knownIssues: [],
      upgradeGuide: null,
    };
    
    // Categorize changes
    for (const change of release.changes) {
      switch (change.type) {
        case ChangeType.FEATURE:
          notes.newFeatures.push(this.documentFeatureChange(change));
          break;
        case ChangeType.IMPROVEMENT:
          notes.improvements.push(this.documentImprovement(change));
          break;
        case ChangeType.BUG_FIX:
          notes.bugFixes.push(this.documentBugFix(change));
          break;
        case ChangeType.BREAKING:
          notes.breakingChanges.push(this.documentBreakingChange(change));
          break;
        case ChangeType.DEPRECATION:
          notes.deprecations.push(this.documentDeprecation(change));
          break;
      }
    }
    
    // Known issues
    notes.knownIssues = release.knownIssues.map(issue => 
      this.documentKnownIssue(issue)
    );
    
    // Upgrade guide
    if (notes.breakingChanges.length > 0 || notes.deprecations.length > 0) {
      notes.upgradeGuide = this.createUpgradeGuide(release, notes);
    }
    
    return notes;
  }

  private documentFeatureChange(change: Change): FeatureDocumentation {
    return {
      id: change.id,
      title: change.title,
      description: this.expandDescription(change.description),
      category: change.category,
      impact: change.impact,
      examples: change.examples ? change.examples.map(e => this.formatExample(e)) : [],
      documentation: change.documentationUrl,
      relatedIssues: change.relatedIssues,
    };
  }

  async applyStyleGuide(content: string): Promise<string> {
    let styled = content;
    
    // Apply terminology consistency
    styled = this.applyTerminology(styled);
    
    // Apply tone and voice
    styled = this.applyToneAndVoice(styled);
    
    // Apply formatting rules
    styled = this.applyFormatting(styled);
    
    // Check grammar and spelling
    styled = await this.checkGrammar(styled);
    
    // Apply readability improvements
    styled = this.improveReadability(styled);
    
    return styled;
  }

  private applyTerminology(content: string): string {
    // Replace inconsistent terms with preferred terms
    const terminology = this.styleGuide.getTerminology();
    
    let updated = content;
    for (const [incorrect, correct] of terminology) {
      const regex = new RegExp(`\\b${incorrect}\\b`, 'gi');
      updated = updated.replace(regex, correct);
    }
    
    return updated;
  }

  private applyToneAndVoice(content: string): string {
    // Convert passive voice to active voice
    content = this.convertToActiveVoice(content);
    
    // Use second person for instructions
    content = this.useSecondPerson(content);
    
    // Remove unnecessary jargon
    content = this.simplifyJargon(content);
    
    return content;
  }

  private improveReadability(content: string): string {
    // Break long sentences
    content = this.breakLongSentences(content);
    
    // Add transition words
    content = this.addTransitions(content);
    
    // Use bullet points for lists
    content = this.formatLists(content);
    
    // Add headings for scannability
    content = this.improveHeadings(content);
    
    return content;
  }

  async generateDiagrams(content: Documentation): Promise<Diagram[]> {
    const diagrams: Diagram[] = [];
    
    // Analyze content for diagram opportunities
    const opportunities = this.identifyDiagramOpportunities(content);
    
    for (const opportunity of opportunities) {
      switch (opportunity.type) {
        case DiagramType.FLOWCHART:
          diagrams.push(this.createFlowchart(opportunity));
          break;
        case DiagramType.SEQUENCE:
          diagrams.push(this.createSequenceDiagram(opportunity));
          break;
        case DiagramType.ARCHITECTURE:
          diagrams.push(this.createArchitectureDiagram(opportunity));
          break;
        case DiagramType.CLASS:
          diagrams.push(this.createClassDiagram(opportunity));
          break;
      }
    }
    
    return diagrams;
  }

  private createFlowchart(opportunity: DiagramOpportunity): Diagram {
    const mermaid = `
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process 1]
    B -->|No| D[Process 2]
    C --> E[End]
    D --> E
`;
    
    return {
      id: this.generateId('DG'),
      type: DiagramType.FLOWCHART,
      title: opportunity.title,
      description: opportunity.description,
      format: 'mermaid',
      content: mermaid,
      caption: opportunity.caption,
    };
  }

  private createSequenceDiagram(opportunity: DiagramOpportunity): Diagram {
    const mermaid = `
sequenceDiagram
    participant User
    participant System
    participant Database
    
    User->>System: Request
    System->>Database: Query
    Database-->>System: Result
    System-->>User: Response
`;
    
    return {
      id: this.generateId('DG'),
      type: DiagramType.SEQUENCE,
      title: opportunity.title,
      description: opportunity.description,
      format: 'mermaid',
      content: mermaid,
      caption: opportunity.caption,
    };
  }

  private generateId(prefix: string): string {
    return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private loadTemplates(): void {
    // Load document templates
    this.templates.set('user-guide', new UserGuideTemplate());
    this.templates.set('api-doc', new APIDocTemplate());
    this.templates.set('tutorial', new TutorialTemplate());
    this.templates.set('reference', new ReferenceTemplate());
    this.templates.set('how-to', new HowToTemplate());
    this.templates.set('troubleshooting', new TroubleshootingTemplate());
  }

  private loadGlossary(): void {
    // Load technical terms
    const terms = [
      { term: 'API', definition: 'Application Programming Interface' },
      { term: 'SDK', definition: 'Software Development Kit' },
      { term: 'REST', definition: 'Representational State Transfer' },
      { term: 'JSON', definition: 'JavaScript Object Notation' },
      { term: 'URL', definition: 'Uniform Resource Locator' },
    ];
    
    for (const { term, definition } of terms) {
      this.glossary.set(term, { term, definition, aliases: [] });
    }
  }
}

// Supporting classes
class StyleGuide {
  private rules: Map<string, StyleRule> = new Map();
  private terminology: Map<string, string> = new Map();
  
  constructor() {
    this.initializeRules();
    this.initializeTerminology();
  }
  
  private initializeRules(): void {
    this.rules.set('sentence-length', {
      id: 'sentence-length',
      description: 'Keep sentences under 25 words',
      check: (text: string) => {
        const sentences = text.split(/[.!?]+/);
        return sentences.every(s => s.split(/\s+/).length <= 25);
      },
    });
    
    this.rules.set('active-voice', {
      id: 'active-voice',
      description: 'Use active voice',
      check: (text: string) => {
        const passiveIndicators = ['was', 'were', 'been', 'being', 'be'];
        const words = text.toLowerCase().split(/\s+/);
        const passiveCount = words.filter(w => passiveIndicators.includes(w)).length;
        return passiveCount / words.length < 0.05;
      },
    });
  }
  
  private initializeTerminology(): void {
    this.terminology.set('click on', 'click');
    this.terminology.set('fill in', 'enter');
    this.terminology.set('fill out', 'complete');
  }
  
  getTerminology(): Map<string, string> {
    return this.terminology;
  }
}

class ContentAnalyzer {
  async analyzeSubject(subject: DocumentationSubject): Promise<SubjectAnalysis> {
    return {
      complexity: this.assessComplexity(subject),
      audienceLevel: this.determineAudienceLevel(subject),
      requiredSections: this.identifyRequiredSections(subject),
      keywords: this.extractKeywords(subject),
      concepts: this.identifyConcepts(subject),
    };
  }
  
  private assessComplexity(subject: DocumentationSubject): ComplexityLevel {
    // Assess subject complexity
    if (subject.technical && subject.specialized) {
      return ComplexityLevel.ADVANCED;
    }
    if (subject.technical || subject.specialized) {
      return ComplexityLevel.INTERMEDIATE;
    }
    return ComplexityLevel.BEGINNER;
  }
  
  private determineAudienceLevel(subject: DocumentationSubject): Audience {
    if (subject.audience) return subject.audience;
    
    if (subject.technical) {
      return Audience.DEVELOPER;
    }
    return Audience.END_USER;
  }
  
  private identifyRequiredSections(subject: DocumentationSubject): string[] {
    const sections: string[] = ['introduction', 'overview'];
    
    if (subject.hasAPI) {
      sections.push('api-reference', 'authentication', 'endpoints');
    }
    
    if (subject.hasUI) {
      sections.push('user-interface', 'navigation', 'features');
    }
    
    sections.push('troubleshooting', 'faq', 'support');
    
    return sections;
  }
  
  private extractKeywords(subject: DocumentationSubject): string[] {
    // Extract important keywords
    return [];
  }
  
  private identifyConcepts(subject: DocumentationSubject): Concept[] {
    // Identify key concepts to explain
    return [];
  }
}

class DocumentValidator {
  async validate(content: ContentSection[]): Promise<ValidationResult> {
    const issues: ValidationIssue[] = [];
    
    // Check for completeness
    issues.push(...this.checkCompleteness(content));
    
    // Check for consistency
    issues.push(...this.checkConsistency(content));
    
    // Check for accuracy
    issues.push(...await this.checkAccuracy(content));
    
    // Check for readability
    issues.push(...this.checkReadability(content));
    
    return {
      valid: issues.filter(i => i.severity === 'error').length === 0,
      issues,
      score: this.calculateScore(issues),
    };
  }
  
  private checkCompleteness(content: ContentSection[]): ValidationIssue[] {
    const issues: ValidationIssue[] = [];
    
    // Check for missing sections
    const requiredSections = ['introduction', 'overview', 'conclusion'];
    const sectionTitles = content.map(s => s.title.toLowerCase());
    
    for (const required of requiredSections) {
      if (!sectionTitles.some(title => title.includes(required))) {
        issues.push({
          type: 'missing-section',
          severity: 'warning',
          message: `Missing ${required} section`,
        });
      }
    }
    
    return issues;
  }
  
  private checkConsistency(content: ContentSection[]): ValidationIssue[] {
    // Check for consistent terminology, formatting, etc.
    return [];
  }
  
  private async checkAccuracy(content: ContentSection[]): Promise<ValidationIssue[]> {
    // Check for technical accuracy
    return [];
  }
  
  private checkReadability(content: ContentSection[]): ValidationIssue[] {
    // Check readability metrics
    return [];
  }
  
  private calculateScore(issues: ValidationIssue[]): number {
    const errorCount = issues.filter(i => i.severity === 'error').length;
    const warningCount = issues.filter(i => i.severity === 'warning').length;
    
    return Math.max(0, 100 - (errorCount * 10) - (warningCount * 5));
  }
}

// Template classes
abstract class DocumentTemplate {
  abstract generate(data: any): DocumentStructure;
}

class UserGuideTemplate extends DocumentTemplate {
  generate(data: any): DocumentStructure {
    return {
      template: 'user-guide',
      sections: [
        { id: 'intro', title: 'Introduction', required: true },
        { id: 'getting-started', title: 'Getting Started', required: true },
        { id: 'features', title: 'Features', required: true },
        { id: 'configuration', title: 'Configuration', required: false },
        { id: 'troubleshooting', title: 'Troubleshooting', required: true },
        { id: 'faq', title: 'FAQ', required: true },
      ],
      navigation: {
        type: 'hierarchical',
        depth: 3,
      },
      crossReferences: [],
    };
  }
}

class APIDocTemplate extends DocumentTemplate {
  generate(data: any): DocumentStructure {
    return {
      template: 'api-doc',
      sections: [
        { id: 'overview', title: 'API Overview', required: true },
        { id: 'authentication', title: 'Authentication', required: true },
        { id: 'endpoints', title: 'Endpoints', required: true },
        { id: 'schemas', title: 'Schemas', required: true },
        { id: 'errors', title: 'Error Codes', required: true },
        { id: 'examples', title: 'Examples', required: true },
      ],
      navigation: {
        type: 'sidebar',
        depth: 2,
      },
      crossReferences: [],
    };
  }
}

class TutorialTemplate extends DocumentTemplate {
  generate(data: any): DocumentStructure {
    return {
      template: 'tutorial',
      sections: [
        { id: 'objectives', title: 'Learning Objectives', required: true },
        { id: 'prerequisites', title: 'Prerequisites', required: true },
        { id: 'steps', title: 'Step-by-Step Guide', required: true },
        { id: 'exercises', title: 'Exercises', required: false },
        { id: 'solutions', title: 'Solutions', required: false },
        { id: 'summary', title: 'Summary', required: true },
      ],
      navigation: {
        type: 'linear',
        depth: 2,
      },
      crossReferences: [],
    };
  }
}

class ReferenceTemplate extends DocumentTemplate {
  generate(data: any): DocumentStructure {
    return {
      template: 'reference',
      sections: [],
      navigation: {
        type: 'alphabetical',
        depth: 1,
      },
      crossReferences: [],
    };
  }
}

class HowToTemplate extends DocumentTemplate {
  generate(data: any): DocumentStructure {
    return {
      template: 'how-to',
      sections: [],
      navigation: {
        type: 'task-based',
        depth: 2,
      },
      crossReferences: [],
    };
  }
}

class TroubleshootingTemplate extends DocumentTemplate {
  generate(data: any): DocumentStructure {
    return {
      template: 'troubleshooting',
      sections: [],
      navigation: {
        type: 'problem-solution',
        depth: 2,
      },
      crossReferences: [],
    };
  }
}

// Type definitions
enum DocumentationType {
  USER_GUIDE = 'user_guide',
  API_DOCUMENTATION = 'api_documentation',
  TUTORIAL = 'tutorial',
  REFERENCE = 'reference',
  HOW_TO = 'how_to',
  RELEASE_NOTES = 'release_notes',
  TECHNICAL_SPEC = 'technical_spec',
}

enum Audience {
  END_USER = 'end_user',
  DEVELOPER = 'developer',
  ADMIN = 'admin',
  BUSINESS = 'business',
  TECHNICAL = 'technical',
}

enum ContentType {
  CONCEPTUAL = 'conceptual',
  PROCEDURAL = 'procedural',
  REFERENCE = 'reference',
  TUTORIAL = 'tutorial',
  TROUBLESHOOTING = 'troubleshooting',
}

enum DocumentStatus {
  DRAFT = 'draft',
  REVIEW = 'review',
  APPROVED = 'approved',
  PUBLISHED = 'published',
  ARCHIVED = 'archived',
}

enum NoteType {
  INFO = 'info',
  TIP = 'tip',
  IMPORTANT = 'important',
  EXPLANATION = 'explanation',
}

enum WarningType {
  CAUTION = 'caution',
  WARNING = 'warning',
  DANGER = 'danger',
}

enum DiagramType {
  FLOWCHART = 'flowchart',
  SEQUENCE = 'sequence',
  ARCHITECTURE = 'architecture',
  CLASS = 'class',
  ERD = 'erd',
  NETWORK = 'network',
}

enum ComplexityLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced',
}

enum ChangeType {
  FEATURE = 'feature',
  IMPROVEMENT = 'improvement',
  BUG_FIX = 'bug_fix',
  BREAKING = 'breaking',
  DEPRECATION = 'deprecation',
}

// Interface definitions
interface DocumentationSubject {
  name: string;
  type: string;
  description: string;
  technical: boolean;
  specialized: boolean;
  hasAPI: boolean;
  hasUI: boolean;
  audience?: Audience;
}

interface DocumentationRequirements {
  title?: string;
  audience: Audience;
  purpose: string;
  scope: string;
  format?: string;
  style?: string;
}

interface DocumentMetadata {
  author: string;
  created: Date;
  modified: Date;
  reviewers: string[];
  approvers: string[];
  tags: string[];
  keywords: string[];
}

interface SectionDefinition {
  id: string;
  title: string;
  required: boolean;
  template?: string;
}

interface NavigationStructure {
  type: string;
  depth: number;
  items?: NavigationItem[];
}

interface NavigationItem {
  title: string;
  href: string;
  children?: NavigationItem[];
}

interface CrossReference {
  from: string;
  to: string;
  type: string;
}

interface Example {
  title: string;
  description: string;
  code: string;
  language?: string;
  output?: string;
}

interface Diagram {
  id: string;
  type: DiagramType;
  title: string;
  description: string;
  format: string;
  content: string;
  caption?: string;
}

interface CodeSnippet {
  id: string;
  language: string;
  code: string;
  title?: string;
  description?: string;
  lineNumbers?: boolean;
  highlight?: number[];
}

interface Warning {
  type: WarningType;
  content: string;
}

interface Note {
  type: NoteType;
  content: string;
}

interface Reference {
  id: string;
  title: string;
  url?: string;
  page?: string;
}

interface GlossaryTerm {
  term: string;
  definition: string;
  aliases: string[];
  seeAlso?: string[];
}

interface UserGuide extends Documentation {
  product: string;
  quickStart: ContentSection | null;
  troubleshooting: ContentSection | null;
  faq: ContentSection | null;
  glossary: GlossaryTerm[];
  index: IndexEntry[];
}

interface IndexEntry {
  term: string;
  pages: string[];
}

interface Product {
  name: string;
  version: string;
  description: string;
  features: Feature[];
  configuration?: Configuration;
  prerequisites: string[];
  targetAudience: string[];
  domain: string;
}

interface Feature {
  id: string;
  name: string;
  description: string;
  category: string;
}

interface Configuration {
  settings: Setting[];
  files: ConfigFile[];
}

interface Setting {
  name: string;
  type: string;
  default: any;
  description: string;
  required: boolean;
}

interface ConfigFile {
  path: string;
  format: string;
  example: string;
}

interface APISpecification {
  name: string;
  version: string;
  baseUrl: string;
  authentication: Authentication;
  endpoints: APIEndpoint[];
  schemas: Schema[];
  errors: ErrorCode[];
  rateLimiting?: RateLimiting;
}

interface APIDocumentation extends Documentation {
  baseUrl: string;
  authentication: AuthenticationDoc;
  endpoints: EndpointDocumentation[];
  schemas: SchemaDocumentation[];
  examples: APIExample[];
  errors: ErrorDocumentation[];
  rateLimiting: RateLimitingDoc;
  changelog: ChangelogEntry[];
}

interface APIEndpoint {
  id: string;
  method: string;
  path: string;
  summary: string;
  description: string;
  parameters: Parameter[];
  requestBody?: RequestBody;
  responses: Response[];
  security?: Security[];
  deprecated?: boolean;
  tags?: string[];
  baseUrl?: string;
  headers?: Record<string, string>;
}

interface EndpointDocumentation {
  id: string;
  method: string;
  path: string;
  summary: string;
  description: string;
  parameters: ParameterDocumentation[];
  requestBody: RequestBodyDoc | null;
  responses: ResponseDoc[];
  examples: EndpointExample[];
  security: Security[];
  deprecated: boolean;
  tags: string[];
}

interface Parameter {
  name: string;
  in: string;
  description: string;
  required: boolean;
  type: string;
  format?: string;
  default?: any;
  enum?: any[];
  example?: any;
}

interface ParameterDocumentation {
  name: string;
  in: string;
  description: string;
  required: boolean;
  type: string;
  format?: string;
  default?: any;
  enum?: any[];
  example: any;
  constraints: string[];
}

interface RequestBody {
  description: string;
  required: boolean;
  content: any;
  example?: any;
}

interface RequestBodyDoc {
  description: string;
  required: boolean;
  schema: any;
  examples: any[];
}

interface Response {
  status: number;
  description: string;
  content?: any;
  headers?: any;
}

interface ResponseDoc {
  status: number;
  description: string;
  schema: any;
  examples: any[];
  headers: any;
}

interface EndpointExample {
  title: string;
  language: string;
  code: string;
}

interface Authentication {
  type: string;
  description: string;
  details: any;
}

interface AuthenticationDoc {
  type: string;
  description: string;
  setup: string;
  examples: any[];
}

interface Schema {
  name: string;
  type: string;
  properties: any;
  required?: string[];
  example?: any;
}

interface SchemaDocumentation {
  name: string;
  description: string;
  properties: PropertyDoc[];
  example: any;
  validation: any;
}

interface PropertyDoc {
  name: string;
  type: string;
  description: string;
  required: boolean;
  constraints: string[];
}

interface ErrorCode {
  code: string;
  message: string;
  description: string;
}

interface ErrorDocumentation {
  code: string;
  message: string;
  description: string;
  resolution: string;
}

interface RateLimiting {
  requests: number;
  window: string;
  description: string;
}

interface RateLimitingDoc {
  limits: any[];
  headers: string[];
  handling: string;
}

interface APIExample {
  title: string;
  description: string;
  request: any;
  response: any;
}

interface Security {
  type: string;
  scopes?: string[];
}

interface ChangelogEntry {
  version: string;
  date: Date;
  changes: string[];
}

interface TutorialTopic {
  title: string;
  difficulty: string;
  estimatedDuration: string;
  objectives: string[];
  prerequisites: string[];
  sections: TutorialSection[];
}

interface Tutorial extends Documentation {
  difficulty: string;
  duration: string;
  objectives: string[];
  prerequisites: string[];
  exercises: Exercise[];
  solutions: Solution[];
  resources: Resource[];
}

interface TutorialSection {
  id: string;
  title: string;
  content?: string;
  steps?: Step[];
  code?: CodeExample[];
  explanations?: string[];
  tips?: string[];
  warnings?: string[];
}

interface Step {
  number: number;
  instruction: string;
  explanation?: string;
  code?: string;
  expected?: string;
}

interface CodeExample {
  title: string;
  language: string;
  code: string;
  explanation?: string;
}

interface Exercise {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  hints?: string[];
}

interface Solution {
  exerciseId: string;
  solution: string;
  explanation: string;
}

interface Resource {
  title: string;
  url: string;
  type: string;
  description: string;
}

interface Release {
  version: string;
  date: Date;
  summary: string;
  highlights: string[];
  changes: Change[];
  knownIssues: Issue[];
}

interface ReleaseNotes extends Documentation {
  date: Date;
  summary: string;
  highlights: string[];
  newFeatures: FeatureDocumentation[];
  improvements: ImprovementDoc[];
  bugFixes: BugFixDoc[];
  breakingChanges: BreakingChangeDoc[];
  deprecations: DeprecationDoc[];
  knownIssues: KnownIssueDoc[];
  upgradeGuide: UpgradeGuide | null;
}

interface Change {
  id: string;
  type: ChangeType;
  title: string;
  description: string;
  category: string;
  impact: string;
  examples?: any[];
  documentationUrl?: string;
  relatedIssues?: string[];
}

interface FeatureDocumentation {
  id: string;
  title: string;
  description: string;
  category: string;
  impact: string;
  examples: Example[];
  documentation?: string;
  relatedIssues?: string[];
}

interface ImprovementDoc {
  title: string;
  description: string;
  impact: string;
  before?: string;
  after?: string;
}

interface BugFixDoc {
  id: string;
  title: string;
  description: string;
  severity: string;
  affectedVersions: string[];
}

interface BreakingChangeDoc {
  title: string;
  description: string;
  migration: string;
  alternatives: string[];
}

interface DeprecationDoc {
  feature: string;
  description: string;
  alternative: string;
  removalVersion: string;
}

interface Issue {
  id: string;
  title: string;
  description: string;
  workaround?: string;
}

interface KnownIssueDoc {
  id: string;
  title: string;
  description: string;
  workaround: string;
  affectedVersions: string[];
  fixVersion?: string;
}

interface UpgradeGuide {
  fromVersion: string;
  toVersion: string;
  steps: Step[];
  breakingChanges: string[];
  migrations: Migration[];
}

interface Migration {
  component: string;
  description: string;
  before: string;
  after: string;
}

interface SubjectAnalysis {
  complexity: ComplexityLevel;
  audienceLevel: Audience;
  requiredSections: string[];
  keywords: string[];
  concepts: Concept[];
}

interface Concept {
  name: string;
  definition: string;
  related: string[];
}

interface DiagramOpportunity {
  type: DiagramType;
  title: string;
  description: string;
  caption: string;
  data: any;
}

interface StyleRule {
  id: string;
  description: string;
  check: (text: string) => boolean;
}

interface ValidationResult {
  valid: boolean;
  issues: ValidationIssue[];
  score: number;
}

interface ValidationIssue {
  type: string;
  severity: string;
  message: string;
  line?: number;
  column?: number;
}

// Export the writer
export { TechnicalDocumentationWriter, Documentation };
```
