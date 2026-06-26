# Agent Generator — Code Examples

## Example 1

```typescript
// agent-generator.ts
import * as fs from 'fs/promises';
import * as path from 'path';
import { compile } from 'handlebars';
import * as yaml from 'js-yaml';
import { OpenAI } from 'openai';
import { z } from 'zod';

// Agent capability schema
const AgentCapabilitySchema = z.object({
  name: z.string(),
  description: z.string(),
  category: z.enum(['development', 'infrastructure', 'quality', 'data-ai', 'business', 'creative', 'specialized']),
  expertise: z.array(z.string()),
  tools: z.array(z.string()),
  constraints: z.array(z.string()).optional(),
  examples: z.array(z.object({
    input: z.string(),
    output: z.string(),
    explanation: z.string().optional(),
  })).optional(),
});

type AgentCapability = z.infer<typeof AgentCapabilitySchema>;

class AgentGenerator {
  private templates: Map<string, HandlebarsTemplateDelegate> = new Map();
  private patterns: Map<string, AgentPattern> = new Map();
  private capabilities: Map<string, Capability> = new Map();
  private openai: OpenAI;

  constructor(config: AgentGeneratorConfig) {
    this.openai = new OpenAI({ apiKey: config.openaiApiKey });
    this.loadTemplates();
    this.loadPatterns();
    this.loadCapabilities();
  }

  async generateAgent(requirements: AgentRequirements): Promise<GeneratedAgent> {
    // Analyze requirements
    const analysis = await this.analyzeRequirements(requirements);
    
    // Select appropriate pattern
    const pattern = this.selectPattern(analysis);
    
    // Compose capabilities
    const capabilities = this.composeCapabilities(analysis);
    
    // Generate system prompt
    const systemPrompt = await this.generateSystemPrompt(
      analysis,
      pattern,
      capabilities
    );
    
    // Generate code examples
    const codeExamples = await this.generateCodeExamples(
      analysis,
      capabilities
    );
    
    // Generate test cases
    const testCases = await this.generateTestCases(
      analysis,
      capabilities
    );
    
    // Assemble agent
    const agent = this.assembleAgent({
      ...analysis,
      pattern,
      capabilities,
      systemPrompt,
      codeExamples,
      testCases,
    });
    
    // Validate agent
    await this.validateAgent(agent);
    
    return agent;
  }

  private async analyzeRequirements(
    requirements: AgentRequirements
  ): Promise<RequirementAnalysis> {
    const prompt = `
Analyze the following agent requirements and extract:
1. Primary domain and expertise area
2. Required capabilities and skills
3. Tool requirements
4. Constraints and limitations
5. Expected input/output patterns
6. Performance requirements

Requirements:
${JSON.stringify(requirements, null, 2)}

Provide analysis in JSON format.
`;

    const response = await this.openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are an expert in AI agent design and analysis.' },
        { role: 'user', content: prompt },
      ],
      response_format: { type: 'json_object' },
    });

    const analysis = JSON.parse(response.choices[0].message.content!);
    
    return {
      domain: analysis.domain,
      expertise: analysis.expertise,
      capabilities: analysis.capabilities,
      tools: analysis.tools,
      constraints: analysis.constraints,
      patterns: analysis.patterns,
      performance: analysis.performance,
    };
  }

  private selectPattern(analysis: RequirementAnalysis): AgentPattern {
    // Score each pattern against requirements
    const scores = new Map<string, number>();
    
    for (const [name, pattern] of this.patterns) {
      let score = 0;
      
      // Domain match
      if (pattern.domains.includes(analysis.domain)) {
        score += 10;
      }
      
      // Capability overlap
      const capOverlap = analysis.capabilities.filter(c => 
        pattern.capabilities.includes(c)
      ).length;
      score += capOverlap * 5;
      
      // Tool compatibility
      const toolOverlap = analysis.tools.filter(t => 
        pattern.supportedTools.includes(t)
      ).length;
      score += toolOverlap * 3;
      
      scores.set(name, score);
    }
    
    // Select highest scoring pattern
    const bestPattern = Array.from(scores.entries())
      .sort((a, b) => b[1] - a[1])[0][0];
    
    return this.patterns.get(bestPattern)!;
  }

  private composeCapabilities(
    analysis: RequirementAnalysis
  ): ComposedCapabilities {
    const selected: Capability[] = [];
    const dependencies = new Set<string>();
    
    // Select primary capabilities
    for (const reqCap of analysis.capabilities) {
      const capability = this.capabilities.get(reqCap);
      if (capability) {
        selected.push(capability);
        
        // Add dependencies
        capability.dependencies?.forEach(dep => dependencies.add(dep));
      }
    }
    
    // Add dependency capabilities
    for (const dep of dependencies) {
      const capability = this.capabilities.get(dep);
      if (capability && !selected.includes(capability)) {
        selected.push(capability);
      }
    }
    
    // Resolve conflicts
    const resolved = this.resolveCapabilityConflicts(selected);
    
    return {
      primary: resolved.filter(c => analysis.capabilities.includes(c.id)),
      supporting: resolved.filter(c => !analysis.capabilities.includes(c.id)),
      conflicts: [],
    };
  }

  private async generateSystemPrompt(
    analysis: RequirementAnalysis,
    pattern: AgentPattern,
    capabilities: ComposedCapabilities
  ): Promise<string> {
    const template = this.templates.get(pattern.template)!;
    
    const context = {
      domain: analysis.domain,
      expertise: analysis.expertise,
      capabilities: capabilities.primary.map(c => ({
        name: c.name,
        description: c.description,
        examples: c.examples,
      })),
      supportingCapabilities: capabilities.supporting.map(c => ({
        name: c.name,
        description: c.description,
      })),
      tools: analysis.tools,
      constraints: analysis.constraints,
      bestPractices: this.generateBestPractices(analysis, capabilities),
      approach: this.generateApproach(analysis, pattern),
    };
    
    return template(context);
  }

  private async generateCodeExamples(
    analysis: RequirementAnalysis,
    capabilities: ComposedCapabilities
  ): Promise<CodeExample[]> {
    const examples: CodeExample[] = [];
    
    for (const capability of capabilities.primary) {
      const prompt = `
Generate production-ready code example for:
Domain: ${analysis.domain}
Capability: ${capability.name}
Description: ${capability.description}

Requirements:
- Include error handling
- Add comprehensive comments
- Follow best practices
- Make it practical and reusable

Provide code in the most appropriate language.
`;

      const response = await this.openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          { role: 'system', content: 'You are an expert programmer.' },
          { role: 'user', content: prompt },
        ],
      });

      const code = response.choices[0].message.content!;
      
      examples.push({
        capability: capability.name,
        title: `${capability.name} Implementation`,
        code,
        language: this.detectLanguage(code),
        explanation: capability.description,
      });
    }
    
    return examples;
  }

  private async generateTestCases(
    analysis: RequirementAnalysis,
    capabilities: ComposedCapabilities
  ): Promise<TestCase[]> {
    const testCases: TestCase[] = [];
    
    for (const capability of capabilities.primary) {
      // Generate test scenarios
      const scenarios = await this.generateTestScenarios(capability);
      
      for (const scenario of scenarios) {
        testCases.push({
          id: `test_${capability.id}_${scenario.id}`,
          capability: capability.name,
          scenario: scenario.description,
          input: scenario.input,
          expectedOutput: scenario.expectedOutput,
          validation: scenario.validation,
        });
      }
    }
    
    return testCases;
  }

  private assembleAgent(components: AgentComponents): GeneratedAgent {
    const metadata: AgentMetadata = {
      name: this.generateAgentName(components.domain, components.expertise),
      description: this.generateDescription(components),
      category: this.determineCategory(components.domain),
      color: this.selectColor(components.domain),
      tools: components.tools,
      version: '1.0.0',
      created: new Date(),
      generator: 'agent-generator-v1',
    };
    
    const content = this.formatAgentContent(
      metadata,
      components.systemPrompt,
      components.codeExamples,
      components.testCases
    );
    
    return {
      metadata,
      content,
      systemPrompt: components.systemPrompt,
      codeExamples: components.codeExamples,
      testCases: components.testCases,
      pattern: components.pattern.name,
      capabilities: components.capabilities,
    };
  }

  private async validateAgent(agent: GeneratedAgent): Promise<void> {
    const validations = [
      this.validateMetadata(agent.metadata),
      this.validateSystemPrompt(agent.systemPrompt),
      this.validateCodeExamples(agent.codeExamples),
      this.validateTestCases(agent.testCases),
      this.validateCapabilities(agent.capabilities),
    ];
    
    const results = await Promise.all(validations);
    
    const errors = results.filter(r => !r.valid);
    if (errors.length > 0) {
      throw new ValidationError('Agent validation failed', errors);
    }
  }

  private formatAgentContent(
    metadata: AgentMetadata,
    systemPrompt: string,
    codeExamples: CodeExample[],
    testCases: TestCase[]
  ): string {
    const frontmatter = yaml.dump({
      name: metadata.name,
      description: metadata.description,
      category: metadata.category,
      color: metadata.color,
      tools: metadata.tools.join(', '),
    });
    
    const examples = codeExamples.map(ex => `
## ${ex.title}
\`\`\`${ex.language}
${ex.code}
\`\`\`
${ex.explanation}
`).join('\n');
    
    return `---
${frontmatter}---

${systemPrompt}

${examples}

## Test Cases
${this.formatTestCases(testCases)}

## Best Practices
${this.formatBestPractices(metadata)}

## Approach
${this.formatApproach(metadata)}
`;
  }

  private generateAgentName(domain: string, expertise: string[]): string {
    const primaryExpertise = expertise[0].toLowerCase().replace(/\s+/g, '-');
    return `${domain}-${primaryExpertise}`;
  }

  private generateDescription(components: AgentComponents): string {
    return `Expert in ${components.domain} specializing in ${components.expertise.join(', ')}`;
  }

  private determineCategory(domain: string): string {
    const categoryMap: Record<string, string> = {
      'web': 'development',
      'backend': 'development',
      'frontend': 'development',
      'mobile': 'development',
      'cloud': 'infrastructure',
      'devops': 'infrastructure',
      'testing': 'quality',
      'security': 'quality',
      'data': 'data-ai',
      'ml': 'data-ai',
      'ai': 'data-ai',
      'product': 'business',
      'design': 'creative',
    };
    
    return categoryMap[domain.toLowerCase()] || 'specialized';
  }

  private selectColor(domain: string): string {
    const colorMap: Record<string, string> = {
      'development': 'blue',
      'infrastructure': 'green',
      'quality': 'red',
      'data-ai': 'purple',
      'business': 'orange',
      'creative': 'pink',
      'specialized': 'gray',
    };
    
    const category = this.determineCategory(domain);
    return colorMap[category] || 'gray';
  }

  private resolveCapabilityConflicts(capabilities: Capability[]): Capability[] {
    // Simple conflict resolution - in production, use more sophisticated logic
    const resolved: Capability[] = [];
    const seen = new Set<string>();
    
    for (const cap of capabilities) {
      if (!seen.has(cap.id)) {
        resolved.push(cap);
        seen.add(cap.id);
      }
    }
    
    return resolved;
  }

  private generateBestPractices(
    analysis: RequirementAnalysis,
    capabilities: ComposedCapabilities
  ): string[] {
    const practices: string[] = [];
    
    // Domain-specific practices
    practices.push(...this.getDomainBestPractices(analysis.domain));
    
    // Capability-specific practices
    for (const cap of capabilities.primary) {
      if (cap.bestPractices) {
        practices.push(...cap.bestPractices);
      }
    }
    
    return practices;
  }

  private generateApproach(
    analysis: RequirementAnalysis,
    pattern: AgentPattern
  ): string[] {
    return [
      `Analyze ${analysis.domain} requirements thoroughly`,
      `Apply ${pattern.name} pattern for optimal results`,
      `Leverage ${analysis.expertise.join(', ')} expertise`,
      'Follow established best practices and conventions',
      'Ensure code quality and maintainability',
      'Provide comprehensive documentation',
    ];
  }

  private getDomainBestPractices(domain: string): string[] {
    const practices: Record<string, string[]> = {
      'web': [
        'Follow responsive design principles',
        'Ensure accessibility compliance',
        'Optimize for performance',
        'Implement proper SEO',
      ],
      'backend': [
        'Design RESTful APIs',
        'Implement proper authentication',
        'Handle errors gracefully',
        'Optimize database queries',
      ],
      'cloud': [
        'Follow cloud-native principles',
        'Implement proper security',
        'Design for scalability',
        'Monitor and log everything',
      ],
    };
    
    return practices[domain] || [];
  }

  private detectLanguage(code: string): string {
    // Simple language detection - in production, use proper detection
    if (code.includes('function') || code.includes('const')) return 'typescript';
    if (code.includes('def ') || code.includes('import ')) return 'python';
    if (code.includes('func ') || code.includes('package ')) return 'go';
    if (code.includes('public class') || code.includes('private ')) return 'java';
    return 'text';
  }

  private async generateTestScenarios(capability: Capability): Promise<TestScenario[]> {
    // Generate test scenarios based on capability
    return [
      {
        id: 'happy_path',
        description: `Test ${capability.name} with valid input`,
        input: this.generateValidInput(capability),
        expectedOutput: this.generateExpectedOutput(capability),
        validation: 'exact_match',
      },
      {
        id: 'edge_case',
        description: `Test ${capability.name} with edge cases`,
        input: this.generateEdgeCase(capability),
        expectedOutput: this.generateEdgeCaseOutput(capability),
        validation: 'contains',
      },
      {
        id: 'error_handling',
        description: `Test ${capability.name} error handling`,
        input: this.generateInvalidInput(capability),
        expectedOutput: this.generateErrorOutput(capability),
        validation: 'error',
      },
    ];
  }

  private generateValidInput(capability: Capability): any {
    // Generate valid input based on capability type
    return {
      type: 'valid',
      data: 'sample input',
    };
  }

  private generateExpectedOutput(capability: Capability): any {
    return {
      success: true,
      result: 'expected output',
    };
  }

  private generateEdgeCase(capability: Capability): any {
    return {
      type: 'edge',
      data: '',
    };
  }

  private generateEdgeCaseOutput(capability: Capability): any {
    return {
      success: true,
      result: 'handled edge case',
    };
  }

  private generateInvalidInput(capability: Capability): any {
    return {
      type: 'invalid',
      data: null,
    };
  }

  private generateErrorOutput(capability: Capability): any {
    return {
      success: false,
      error: 'Invalid input',
    };
  }

  private formatTestCases(testCases: TestCase[]): string {
    return testCases.map(tc => `
### ${tc.scenario}
- **Input**: \`${JSON.stringify(tc.input)}\`
- **Expected**: \`${JSON.stringify(tc.expectedOutput)}\`
- **Validation**: ${tc.validation}
`).join('\n');
  }

  private formatBestPractices(metadata: AgentMetadata): string {
    return `
1. Follow ${metadata.category} best practices
2. Ensure code quality and maintainability
3. Provide comprehensive error handling
4. Document all decisions and trade-offs
5. Optimize for performance and scalability
`;
  }

  private formatApproach(metadata: AgentMetadata): string {
    return `
1. Understand requirements thoroughly
2. Apply appropriate design patterns
3. Implement with best practices
4. Test comprehensively
5. Document clearly
6. Iterate based on feedback
`;
  }

  private async validateMetadata(metadata: AgentMetadata): Promise<ValidationResult> {
    const errors: string[] = [];
    
    if (!metadata.name || metadata.name.length < 3) {
      errors.push('Agent name must be at least 3 characters');
    }
    
    if (!metadata.description || metadata.description.length < 10) {
      errors.push('Agent description must be at least 10 characters');
    }
    
    if (!metadata.tools || metadata.tools.length === 0) {
      errors.push('Agent must have at least one tool');
    }
    
    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private async validateSystemPrompt(prompt: string): Promise<ValidationResult> {
    const errors: string[] = [];
    
    if (prompt.length < 100) {
      errors.push('System prompt too short');
    }
    
    if (!prompt.includes('expertise') && !prompt.includes('expert')) {
      errors.push('System prompt should establish expertise');
    }
    
    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private async validateCodeExamples(examples: CodeExample[]): Promise<ValidationResult> {
    const errors: string[] = [];
    
    if (examples.length === 0) {
      errors.push('At least one code example required');
    }
    
    for (const example of examples) {
      if (!example.code || example.code.length < 50) {
        errors.push(`Code example ${example.title} too short`);
      }
    }
    
    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private async validateTestCases(testCases: TestCase[]): Promise<ValidationResult> {
    const errors: string[] = [];
    
    if (testCases.length < 3) {
      errors.push('At least 3 test cases required');
    }
    
    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private async validateCapabilities(capabilities: ComposedCapabilities): Promise<ValidationResult> {
    const errors: string[] = [];
    
    if (capabilities.primary.length === 0) {
      errors.push('At least one primary capability required');
    }
    
    if (capabilities.conflicts.length > 0) {
      errors.push(`Unresolved conflicts: ${capabilities.conflicts.join(', ')}`);
    }
    
    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private async loadTemplates(): Promise<void> {
    // Load Handlebars templates
    const templatesDir = path.join(__dirname, 'templates');
    const files = await fs.readdir(templatesDir);
    
    for (const file of files) {
      if (file.endsWith('.hbs')) {
        const name = path.basename(file, '.hbs');
        const content = await fs.readFile(path.join(templatesDir, file), 'utf-8');
        this.templates.set(name, compile(content));
      }
    }
  }

  private async loadPatterns(): Promise<void> {
    // Load agent patterns
    // In production, load from configuration
    this.patterns.set('specialist', {
      name: 'specialist',
      template: 'specialist',
      domains: ['web', 'backend', 'frontend', 'mobile'],
      capabilities: ['coding', 'debugging', 'optimization'],
      supportedTools: ['Write', 'Read', 'MultiEdit', 'Bash'],
    });
    
    this.patterns.set('architect', {
      name: 'architect',
      template: 'architect',
      domains: ['cloud', 'infrastructure', 'system'],
      capabilities: ['design', 'planning', 'documentation'],
      supportedTools: ['Write', 'Read', 'Grep', 'Glob'],
    });
  }

  private async loadCapabilities(): Promise<void> {
    // Load capability definitions
    // In production, load from configuration
    this.capabilities.set('coding', {
      id: 'coding',
      name: 'Coding',
      description: 'Write production-ready code',
      examples: ['Implement features', 'Fix bugs', 'Refactor code'],
      dependencies: ['debugging'],
      bestPractices: ['Follow SOLID principles', 'Write clean code'],
    });
    
    this.capabilities.set('debugging', {
      id: 'debugging',
      name: 'Debugging',
      description: 'Debug and troubleshoot issues',
      examples: ['Find root causes', 'Fix errors', 'Analyze logs'],
      bestPractices: ['Use proper debugging tools', 'Document findings'],
    });
  }
}

// Type definitions
interface AgentGeneratorConfig {
  openaiApiKey: string;
  templatesDir?: string;
  patternsConfig?: string;
  capabilitiesConfig?: string;
}

interface AgentRequirements {
  domain: string;
  tasks: string[];
  constraints?: string[];
  examples?: string[];
  performance?: PerformanceRequirements;
}

interface PerformanceRequirements {
  responseTime?: number;
  accuracy?: number;
  reliability?: number;
}

interface RequirementAnalysis {
  domain: string;
  expertise: string[];
  capabilities: string[];
  tools: string[];
  constraints: string[];
  patterns: string[];
  performance: PerformanceRequirements;
}

interface AgentPattern {
  name: string;
  template: string;
  domains: string[];
  capabilities: string[];
  supportedTools: string[];
}

interface Capability {
  id: string;
  name: string;
  description: string;
  examples?: string[];
  dependencies?: string[];
  bestPractices?: string[];
}

interface ComposedCapabilities {
  primary: Capability[];
  supporting: Capability[];
  conflicts: string[];
}

interface CodeExample {
  capability: string;
  title: string;
  code: string;
  language: string;
  explanation: string;
}

interface TestCase {
  id: string;
  capability: string;
  scenario: string;
  input: any;
  expectedOutput: any;
  validation: string;
}

interface TestScenario {
  id: string;
  description: string;
  input: any;
  expectedOutput: any;
  validation: string;
}

interface AgentComponents {
  domain: string;
  expertise: string[];
  pattern: AgentPattern;
  capabilities: ComposedCapabilities;
  systemPrompt: string;
  codeExamples: CodeExample[];
  testCases: TestCase[];
  tools: string[];
}

interface AgentMetadata {
  name: string;
  description: string;
  category: string;
  color: string;
  tools: string[];
  version: string;
  created: Date;
  generator: string;
}

interface GeneratedAgent {
  metadata: AgentMetadata;
  content: string;
  systemPrompt: string;
  codeExamples: CodeExample[];
  testCases: TestCase[];
  pattern: string;
  capabilities: ComposedCapabilities;
}

interface ValidationResult {
  valid: boolean;
  errors: string[];
}

class ValidationError extends Error {
  constructor(message: string, public errors: ValidationResult[]) {
    super(message);
  }
}

// Export the generator
export { AgentGenerator, AgentRequirements, GeneratedAgent };
```

## Example 2

```typescript
// agent-templates.ts
export const agentTemplates = {
  specialist: `
You are a {{domain}} specialist with deep expertise in {{#each expertise}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}.

## Core Expertise
{{#each capabilities}}
- {{this.name}}: {{this.description}}
{{/each}}

## Technical Stack
{{#each tools}}
- {{this}}
{{/each}}

## Best Practices
{{#each bestPractices}}
1. {{this}}
{{/each}}

## Approach
{{#each approach}}
- {{this}}
{{/each}}
`,

  architect: `
You are a {{domain}} architect specializing in system design and architecture.

## Architecture Principles
{{#each principles}}
- {{this}}
{{/each}}

## Design Patterns
{{#each patterns}}
- {{this.name}}: {{this.description}}
{{/each}}

## Quality Attributes
{{#each qualityAttributes}}
- {{this}}
{{/each}}
`,

  reviewer: `
You are a {{domain}} reviewer focused on quality assurance and best practices.

## Review Criteria
{{#each criteria}}
- {{this}}
{{/each}}

## Common Issues
{{#each commonIssues}}
- {{this.issue}}: {{this.solution}}
{{/each}}
`,
};
```

## Example 3

```typescript
// agent-dsl.ts
import { Parser } from 'chevrotain';

class AgentDSL {
  private parser: AgentDSLParser;
  private interpreter: AgentDSLInterpreter;

  constructor() {
    this.parser = new AgentDSLParser();
    this.interpreter = new AgentDSLInterpreter();
  }

  parse(dsl: string): AgentDefinition {
    const ast = this.parser.parse(dsl);
    return this.interpreter.interpret(ast);
  }
}

// Example DSL:
const agentDSL = `
agent WebDeveloper {
  domain: "web development"
  
  capabilities {
    frontend: "React, Vue, Angular"
    backend: "Node.js, Python, Go"
    database: "PostgreSQL, MongoDB"
  }
  
  tools: [Write, Read, MultiEdit, Bash]
  
  patterns {
    mvc: "Model-View-Controller"
    rest: "RESTful API design"
    responsive: "Responsive web design"
  }
  
  workflow {
    1. analyze_requirements
    2. design_architecture
    3. implement_features
    4. write_tests
    5. optimize_performance
  }
  
  constraints {
    - "Follow accessibility guidelines"
    - "Ensure mobile compatibility"
    - "Optimize for SEO"
  }
}
`;

class AgentDSLParser {
  parse(input: string): AST {
    // Simplified parser implementation
    const lines = input.split('\n');
    const ast: AST = { type: 'agent', children: [] };
    
    let current: any = ast;
    const stack: any[] = [ast];
    
    for (const line of lines) {
      const trimmed = line.trim();
      
      if (trimmed.startsWith('agent ')) {
        const name = trimmed.split(' ')[1].replace('{', '').trim();
        current.name = name;
      } else if (trimmed.includes(':')) {
        const [key, value] = trimmed.split(':').map(s => s.trim());
        current[key] = value.replace(/[",]/g, '');
      } else if (trimmed.endsWith('{')) {
        const key = trimmed.replace('{', '').trim();
        const newNode = { type: key, children: [] };
        current.children.push(newNode);
        stack.push(current);
        current = newNode;
      } else if (trimmed === '}') {
        current = stack.pop();
      }
    }
    
    return ast;
  }
}

class AgentDSLInterpreter {
  interpret(ast: AST): AgentDefinition {
    // Convert AST to agent definition
    return {
      name: ast.name,
      domain: this.extractValue(ast, 'domain'),
      capabilities: this.extractCapabilities(ast),
      tools: this.extractTools(ast),
      patterns: this.extractPatterns(ast),
      workflow: this.extractWorkflow(ast),
      constraints: this.extractConstraints(ast),
    };
  }

  private extractValue(ast: AST, key: string): string {
    return ast[key] || '';
  }

  private extractCapabilities(ast: AST): Map<string, string> {
    const capabilities = new Map();
    const capNode = ast.children.find(c => c.type === 'capabilities');
    
    if (capNode) {
      for (const child of capNode.children) {
        capabilities.set(child.key, child.value);
      }
    }
    
    return capabilities;
  }

  private extractTools(ast: AST): string[] {
    const toolsStr = this.extractValue(ast, 'tools');
    return toolsStr.replace(/[\[\]]/g, '').split(',').map(s => s.trim());
  }

  private extractPatterns(ast: AST): Map<string, string> {
    const patterns = new Map();
    const patternNode = ast.children.find(c => c.type === 'patterns');
    
    if (patternNode) {
      for (const child of patternNode.children) {
        patterns.set(child.key, child.value);
      }
    }
    
    return patterns;
  }

  private extractWorkflow(ast: AST): string[] {
    const workflow: string[] = [];
    const workflowNode = ast.children.find(c => c.type === 'workflow');
    
    if (workflowNode) {
      for (const child of workflowNode.children) {
        workflow.push(child.step);
      }
    }
    
    return workflow;
  }

  private extractConstraints(ast: AST): string[] {
    const constraints: string[] = [];
    const constraintNode = ast.children.find(c => c.type === 'constraints');
    
    if (constraintNode) {
      for (const child of constraintNode.children) {
        constraints.push(child.value);
      }
    }
    
    return constraints;
  }
}

interface AST {
  type: string;
  name?: string;
  children: any[];
  [key: string]: any;
}

interface AgentDefinition {
  name: string;
  domain: string;
  capabilities: Map<string, string>;
  tools: string[];
  patterns: Map<string, string>;
  workflow: string[];
  constraints: string[];
}
```
