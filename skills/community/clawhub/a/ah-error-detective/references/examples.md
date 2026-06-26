# Error Detective — Code Examples

## Example 1

```typescript
// error-detective.ts
import { SourceMapConsumer } from 'source-map';
import * as stacktrace from 'stacktrace-js';
import { performance } from 'perf_hooks';
import * as fs from 'fs/promises';
import * as path from 'path';

interface ErrorContext {
  error: Error;
  timestamp: Date;
  environment: Environment;
  metadata: Map<string, any>;
  stackFrames?: StackFrame[];
  relatedErrors?: Error[];
  systemState?: SystemState;
}

interface StackFrame {
  functionName: string;
  fileName: string;
  lineNumber: number;
  columnNumber: number;
  source?: string;
  context?: string[];
  locals?: Map<string, any>;
}

interface SystemState {
  memory: MemoryUsage;
  cpu: CPUUsage;
  disk: DiskUsage;
  network: NetworkState;
  processes: ProcessInfo[];
}

class ErrorDetective {
  private patterns: Map<string, ErrorPattern> = new Map();
  private solutions: Map<string, Solution[]> = new Map();
  private metrics: MetricsCollector;
  private sourceMapCache: Map<string, SourceMapConsumer> = new Map();

  constructor(config: ErrorDetectiveConfig) {
    this.metrics = new MetricsCollector(config.metricsEndpoint);
    this.loadErrorPatterns();
    this.loadKnownSolutions();
  }

  async investigate(error: Error | ErrorContext): Promise<Investigation> {
    const context = this.normalizeErrorContext(error);
    
    // Enhance stack trace with source maps
    await this.enhanceStackTrace(context);
    
    // Analyze error pattern
    const pattern = this.identifyPattern(context);
    
    // Find root cause
    const rootCause = await this.findRootCause(context, pattern);
    
    // Collect related errors
    const relatedErrors = await this.findRelatedErrors(context);
    
    // Generate hypothesis
    const hypothesis = this.generateHypothesis(context, pattern, rootCause);
    
    // Find solutions
    const solutions = this.findSolutions(pattern, rootCause);
    
    // Generate report
    const report = this.generateReport({
      context,
      pattern,
      rootCause,
      relatedErrors,
      hypothesis,
      solutions,
    });
    
    // Track metrics
    this.metrics.track('error.investigated', {
      pattern: pattern?.name,
      rootCause: rootCause.type,
      solutionsFound: solutions.length,
    });
    
    return {
      error: context.error,
      pattern,
      rootCause,
      relatedErrors,
      hypothesis,
      solutions,
      report,
      confidence: this.calculateConfidence(pattern, rootCause, solutions),
    };
  }

  private async enhanceStackTrace(context: ErrorContext): Promise<void> {
    if (!context.error.stack) return;
    
    try {
      // Parse stack trace
      const frames = await stacktrace.fromError(context.error);
      
      // Enhance each frame
      const enhanced = await Promise.all(
        frames.map(frame => this.enhanceStackFrame(frame))
      );
      
      context.stackFrames = enhanced;
    } catch (error) {
      console.error('Failed to enhance stack trace:', error);
    }
  }

  private async enhanceStackFrame(frame: any): Promise<StackFrame> {
    const enhanced: StackFrame = {
      functionName: frame.functionName || '<anonymous>',
      fileName: frame.fileName,
      lineNumber: frame.lineNumber,
      columnNumber: frame.columnNumber,
    };
    
    // Load source code
    if (frame.fileName && frame.lineNumber) {
      try {
        const source = await this.loadSourceCode(frame.fileName);
        const lines = source.split('\n');
        
        // Get the error line
        enhanced.source = lines[frame.lineNumber - 1];
        
        // Get context (5 lines before and after)
        const start = Math.max(0, frame.lineNumber - 6);
        const end = Math.min(lines.length, frame.lineNumber + 5);
        enhanced.context = lines.slice(start, end);
        
        // Apply source maps if available
        const sourceMap = await this.loadSourceMap(frame.fileName);
        if (sourceMap) {
          const original = sourceMap.originalPositionFor({
            line: frame.lineNumber,
            column: frame.columnNumber,
          });
          
          if (original.source) {
            enhanced.fileName = original.source;
            enhanced.lineNumber = original.line || frame.lineNumber;
            enhanced.columnNumber = original.column || frame.columnNumber;
          }
        }
      } catch (error) {
        // Source code not available
      }
    }
    
    return enhanced;
  }

  private identifyPattern(context: ErrorContext): ErrorPattern | null {
    const errorMessage = context.error.message;
    const errorType = context.error.name;
    
    // Check known patterns
    for (const [key, pattern] of this.patterns) {
      if (pattern.matches(errorType, errorMessage, context)) {
        return pattern;
      }
    }
    
    // Try to identify pattern using ML/heuristics
    return this.identifyPatternHeuristic(context);
  }

  private identifyPatternHeuristic(context: ErrorContext): ErrorPattern | null {
    const message = context.error.message.toLowerCase();
    
    // Memory patterns
    if (message.includes('heap') || message.includes('memory') || message.includes('oom')) {
      return this.patterns.get('memory_leak');
    }
    
    // Async patterns
    if (message.includes('promise') || message.includes('async') || message.includes('await')) {
      return this.patterns.get('async_error');
    }
    
    // Network patterns
    if (message.includes('timeout') || message.includes('econnrefused') || message.includes('network')) {
      return this.patterns.get('network_error');
    }
    
    // Permission patterns
    if (message.includes('permission') || message.includes('denied') || message.includes('unauthorized')) {
      return this.patterns.get('permission_error');
    }
    
    // Type patterns
    if (message.includes('undefined') || message.includes('null') || message.includes('type')) {
      return this.patterns.get('type_error');
    }
    
    return null;
  }

  private async findRootCause(
    context: ErrorContext,
    pattern: ErrorPattern | null
  ): Promise<RootCause> {
    const candidates: RootCause[] = [];
    
    // Analyze stack trace
    if (context.stackFrames && context.stackFrames.length > 0) {
      const stackAnalysis = this.analyzeStackTrace(context.stackFrames);
      candidates.push(...stackAnalysis);
    }
    
    // Analyze error message
    const messageAnalysis = this.analyzeErrorMessage(context.error.message);
    candidates.push(...messageAnalysis);
    
    // Pattern-specific analysis
    if (pattern) {
      const patternAnalysis = await pattern.analyzeRootCause(context);
      candidates.push(...patternAnalysis);
    }
    
    // System state analysis
    if (context.systemState) {
      const systemAnalysis = this.analyzeSystemState(context.systemState);
      candidates.push(...systemAnalysis);
    }
    
    // Rank candidates
    const ranked = this.rankRootCauses(candidates);
    
    return ranked[0] || {
      type: 'unknown',
      description: 'Unable to determine root cause',
      confidence: 0,
      evidence: [],
    };
  }

  private analyzeStackTrace(frames: StackFrame[]): RootCause[] {
    const causes: RootCause[] = [];
    
    for (let i = 0; i < frames.length; i++) {
      const frame = frames[i];
      
      // Check for null/undefined access
      if (frame.source && (frame.source.includes('.') || frame.source.includes('['))) {
        const nullPattern = /(\w+)\.(\w+)|(\w+)\[/;
        const match = frame.source.match(nullPattern);
        
        if (match) {
          causes.push({
            type: 'null_reference',
            description: `Possible null/undefined reference at ${frame.fileName}:${frame.lineNumber}`,
            confidence: 0.7,
            evidence: [frame.source],
            location: {
              file: frame.fileName,
              line: frame.lineNumber,
              column: frame.columnNumber,
            },
          });
        }
      }
      
      // Check for infinite recursion
      if (i > 0 && frames[i - 1].functionName === frame.functionName) {
        let recursionDepth = 1;
        for (let j = i + 1; j < frames.length && frames[j].functionName === frame.functionName; j++) {
          recursionDepth++;
        }
        
        if (recursionDepth > 10) {
          causes.push({
            type: 'infinite_recursion',
            description: `Infinite recursion detected in ${frame.functionName}`,
            confidence: 0.9,
            evidence: [`Recursion depth: ${recursionDepth}`],
            location: {
              file: frame.fileName,
              line: frame.lineNumber,
              column: frame.columnNumber,
            },
          });
        }
      }
    }
    
    return causes;
  }

  private analyzeErrorMessage(message: string): RootCause[] {
    const causes: RootCause[] = [];
    
    // Extract file paths
    const filePattern = /([a-zA-Z]:)?[/\\][\w\-/.]+\.\w+/g;
    const files = message.match(filePattern);
    
    if (files) {
      for (const file of files) {
        causes.push({
          type: 'file_error',
          description: `File-related issue: ${file}`,
          confidence: 0.6,
          evidence: [message],
        });
      }
    }
    
    // Extract variable names
    const varPattern = /'([^']+)'|"([^"]+)"|`([^`]+)`/g;
    const variables = Array.from(message.matchAll(varPattern)).map(m => m[1] || m[2] || m[3]);
    
    if (variables.length > 0) {
      causes.push({
        type: 'variable_error',
        description: `Issue with: ${variables.join(', ')}`,
        confidence: 0.5,
        evidence: [message],
      });
    }
    
    return causes;
  }

  private analyzeSystemState(state: SystemState): RootCause[] {
    const causes: RootCause[] = [];
    
    // Memory analysis
    if (state.memory.heapUsed / state.memory.heapTotal > 0.9) {
      causes.push({
        type: 'memory_pressure',
        description: 'High memory usage detected',
        confidence: 0.8,
        evidence: [
          `Heap used: ${Math.round(state.memory.heapUsed / 1024 / 1024)}MB`,
          `Heap total: ${Math.round(state.memory.heapTotal / 1024 / 1024)}MB`,
        ],
      });
    }
    
    // CPU analysis
    if (state.cpu.usage > 90) {
      causes.push({
        type: 'cpu_pressure',
        description: 'High CPU usage detected',
        confidence: 0.7,
        evidence: [`CPU usage: ${state.cpu.usage}%`],
      });
    }
    
    // Disk analysis
    if (state.disk.available / state.disk.total < 0.1) {
      causes.push({
        type: 'disk_pressure',
        description: 'Low disk space available',
        confidence: 0.8,
        evidence: [
          `Available: ${Math.round(state.disk.available / 1024 / 1024 / 1024)}GB`,
          `Total: ${Math.round(state.disk.total / 1024 / 1024 / 1024)}GB`,
        ],
      });
    }
    
    return causes;
  }

  private rankRootCauses(causes: RootCause[]): RootCause[] {
    return causes.sort((a, b) => b.confidence - a.confidence);
  }

  private async findRelatedErrors(context: ErrorContext): Promise<Error[]> {
    const related: Error[] = [];
    
    // Find errors with similar stack traces
    if (context.stackFrames && context.stackFrames.length > 0) {
      const topFrame = context.stackFrames[0];
      // In production, query error tracking service
      // For now, return empty array
    }
    
    return related;
  }

  private generateHypothesis(
    context: ErrorContext,
    pattern: ErrorPattern | null,
    rootCause: RootCause
  ): Hypothesis {
    const factors: string[] = [];
    
    // Add pattern-based factors
    if (pattern) {
      factors.push(`This appears to be a ${pattern.name} error`);
      factors.push(...pattern.commonCauses);
    }
    
    // Add root cause factors
    factors.push(`Root cause: ${rootCause.description}`);
    
    // Add timing factors
    if (context.metadata.has('timing')) {
      const timing = context.metadata.get('timing');
      if (timing === 'startup') {
        factors.push('Error occurred during application startup');
      } else if (timing === 'shutdown') {
        factors.push('Error occurred during application shutdown');
      }
    }
    
    // Generate explanation
    const explanation = this.generateExplanation(factors, context, rootCause);
    
    return {
      summary: `${rootCause.type}: ${rootCause.description}`,
      explanation,
      factors,
      confidence: rootCause.confidence,
      testable: this.generateTests(rootCause),
    };
  }

  private generateExplanation(
    factors: string[],
    context: ErrorContext,
    rootCause: RootCause
  ): string {
    let explanation = `The error "${context.error.message}" `;
    
    switch (rootCause.type) {
      case 'null_reference':
        explanation += 'occurs when attempting to access a property or method on a null or undefined value. ';
        break;
      case 'infinite_recursion':
        explanation += 'is caused by a function calling itself without a proper termination condition. ';
        break;
      case 'memory_pressure':
        explanation += 'is likely related to high memory usage in the application. ';
        break;
      case 'type_error':
        explanation += 'indicates a type mismatch or incorrect data type usage. ';
        break;
      default:
        explanation += 'has been identified based on the analysis. ';
    }
    
    if (rootCause.location) {
      explanation += `The issue originates from ${rootCause.location.file}:${rootCause.location.line}. `;
    }
    
    if (factors.length > 0) {
      explanation += `Contributing factors include: ${factors.slice(0, 3).join(', ')}.`;
    }
    
    return explanation;
  }

  private generateTests(rootCause: RootCause): string[] {
    const tests: string[] = [];
    
    switch (rootCause.type) {
      case 'null_reference':
        tests.push('Add null checks before property access');
        tests.push('Verify object initialization');
        tests.push('Check async operation completion');
        break;
      case 'infinite_recursion':
        tests.push('Add recursion depth limit');
        tests.push('Verify termination condition');
        tests.push('Check base case handling');
        break;
      case 'memory_pressure':
        tests.push('Profile memory usage');
        tests.push('Check for memory leaks');
        tests.push('Verify resource cleanup');
        break;
    }
    
    return tests;
  }

  private findSolutions(pattern: ErrorPattern | null, rootCause: RootCause): Solution[] {
    const solutions: Solution[] = [];
    
    // Get pattern-specific solutions
    if (pattern) {
      const patternSolutions = this.solutions.get(pattern.name);
      if (patternSolutions) {
        solutions.push(...patternSolutions);
      }
    }
    
    // Get root cause-specific solutions
    const rootCauseSolutions = this.solutions.get(rootCause.type);
    if (rootCauseSolutions) {
      solutions.push(...rootCauseSolutions);
    }
    
    // Add generic solutions
    solutions.push({
      title: 'Add Error Handling',
      description: 'Wrap the problematic code in try-catch blocks',
      code: `
try {
  // Problematic code here
} catch (error) {
  console.error('Error occurred:', error);
  // Handle error appropriately
}`,
      confidence: 0.5,
    });
    
    // Rank solutions
    return solutions.sort((a, b) => b.confidence - a.confidence);
  }

  private generateReport(data: any): Report {
    const sections: ReportSection[] = [];
    
    // Executive Summary
    sections.push({
      title: 'Executive Summary',
      content: `
Error: ${data.context.error.name}
Message: ${data.context.error.message}
Pattern: ${data.pattern?.name || 'Unknown'}
Root Cause: ${data.rootCause.description}
Confidence: ${Math.round(data.rootCause.confidence * 100)}%
`,
    });
    
    // Stack Trace Analysis
    if (data.context.stackFrames && data.context.stackFrames.length > 0) {
      sections.push({
        title: 'Stack Trace Analysis',
        content: this.formatStackTrace(data.context.stackFrames),
      });
    }
    
    // Root Cause Analysis
    sections.push({
      title: 'Root Cause Analysis',
      content: `
Type: ${data.rootCause.type}
Description: ${data.rootCause.description}
Evidence:
${data.rootCause.evidence.map(e => `  - ${e}`).join('\n')}
`,
    });
    
    // Hypothesis
    sections.push({
      title: 'Hypothesis',
      content: `
${data.hypothesis.explanation}

Testable Actions:
${data.hypothesis.testable.map(t => `  1. ${t}`).join('\n')}
`,
    });
    
    // Recommended Solutions
    if (data.solutions.length > 0) {
      sections.push({
        title: 'Recommended Solutions',
        content: data.solutions.map((s: Solution, i: number) => `
${i + 1}. ${s.title}
   ${s.description}
   Confidence: ${Math.round(s.confidence * 100)}%
`).join('\n'),
      });
    }
    
    return {
      timestamp: new Date(),
      sections,
      metadata: {
        errorType: data.context.error.name,
        pattern: data.pattern?.name,
        rootCause: data.rootCause.type,
        confidence: data.rootCause.confidence,
      },
    };
  }

  private formatStackTrace(frames: StackFrame[]): string {
    return frames.slice(0, 10).map((frame, i) => `
${i + 1}. ${frame.functionName}
   at ${frame.fileName}:${frame.lineNumber}:${frame.columnNumber}
   ${frame.source ? `   > ${frame.source.trim()}` : ''}
`).join('\n');
  }

  private calculateConfidence(
    pattern: ErrorPattern | null,
    rootCause: RootCause,
    solutions: Solution[]
  ): number {
    let confidence = rootCause.confidence;
    
    // Boost confidence if pattern matched
    if (pattern) {
      confidence = Math.min(1, confidence + 0.1);
    }
    
    // Boost confidence if solutions found
    if (solutions.length > 0) {
      confidence = Math.min(1, confidence + 0.05 * solutions.length);
    }
    
    return confidence;
  }

  private normalizeErrorContext(error: Error | ErrorContext): ErrorContext {
    if (error instanceof Error) {
      return {
        error,
        timestamp: new Date(),
        environment: this.detectEnvironment(),
        metadata: new Map(),
      };
    }
    return error;
  }

  private detectEnvironment(): Environment {
    return {
      node: process.version,
      platform: process.platform,
      arch: process.arch,
      memory: process.memoryUsage(),
      uptime: process.uptime(),
    };
  }

  private async loadSourceCode(fileName: string): Promise<string> {
    try {
      return await fs.readFile(fileName, 'utf-8');
    } catch {
      return '';
    }
  }

  private async loadSourceMap(fileName: string): Promise<SourceMapConsumer | null> {
    const mapFile = fileName + '.map';
    
    if (this.sourceMapCache.has(mapFile)) {
      return this.sourceMapCache.get(mapFile)!;
    }
    
    try {
      const mapContent = await fs.readFile(mapFile, 'utf-8');
      const consumer = await new SourceMapConsumer(JSON.parse(mapContent));
      this.sourceMapCache.set(mapFile, consumer);
      return consumer;
    } catch {
      return null;
    }
  }

  private loadErrorPatterns(): void {
    // Load common error patterns
    this.patterns.set('null_reference', new NullReferencePattern());
    this.patterns.set('type_error', new TypeErrorPattern());
    this.patterns.set('async_error', new AsyncErrorPattern());
    this.patterns.set('memory_leak', new MemoryLeakPattern());
    this.patterns.set('network_error', new NetworkErrorPattern());
    this.patterns.set('permission_error', new PermissionErrorPattern());
  }

  private loadKnownSolutions(): void {
    // Load solutions for common patterns
    this.solutions.set('null_reference', [
      {
        title: 'Add Optional Chaining',
        description: 'Use optional chaining to safely access nested properties',
        code: 'const value = obj?.property?.nested?.value;',
        confidence: 0.9,
      },
      {
        title: 'Add Null Checks',
        description: 'Check for null/undefined before access',
        code: 'if (obj && obj.property) { /* safe to use */ }',
        confidence: 0.8,
      },
    ]);
    
    this.solutions.set('async_error', [
      {
        title: 'Add Async Error Handling',
        description: 'Use try-catch with async/await',
        code: `
async function safeAsync() {
  try {
    await someAsyncOperation();
  } catch (error) {
    handleError(error);
  }
}`,
        confidence: 0.9,
      },
    ]);
  }
}

// Pattern implementations
abstract class ErrorPattern {
  abstract name: string;
  abstract commonCauses: string[];
  
  abstract matches(type: string, message: string, context: ErrorContext): boolean;
  abstract analyzeRootCause(context: ErrorContext): Promise<RootCause[]>;
}

class NullReferencePattern extends ErrorPattern {
  name = 'Null Reference';
  commonCauses = [
    'Accessing property on undefined/null',
    'Missing initialization',
    'Async operation not completed',
  ];
  
  matches(type: string, message: string, context: ErrorContext): boolean {
    return type === 'TypeError' && 
           (message.includes('undefined') || 
            message.includes('null') ||
            message.includes('Cannot read'));
  }
  
  async analyzeRootCause(context: ErrorContext): Promise<RootCause[]> {
    const causes: RootCause[] = [];
    
    // Analyze for common null reference patterns
    causes.push({
      type: 'null_reference',
      description: 'Attempted to access property on null/undefined',
      confidence: 0.85,
      evidence: [context.error.message],
    });
    
    return causes;
  }
}

class AsyncErrorPattern extends ErrorPattern {
  name = 'Async Error';
  commonCauses = [
    'Unhandled promise rejection',
    'Missing await keyword',
    'Race condition',
  ];
  
  matches(type: string, message: string, context: ErrorContext): boolean {
    return message.includes('Promise') || 
           message.includes('async') ||
           type === 'UnhandledPromiseRejection';
  }
  
  async analyzeRootCause(context: ErrorContext): Promise<RootCause[]> {
    return [{
      type: 'async_error',
      description: 'Asynchronous operation failed',
      confidence: 0.75,
      evidence: [context.error.message],
    }];
  }
}

// Additional pattern classes...
class TypeErrorPattern extends ErrorPattern {
  name = 'Type Error';
  commonCauses = ['Type mismatch', 'Invalid type conversion'];
  
  matches(type: string, message: string, context: ErrorContext): boolean {
    return type === 'TypeError';
  }
  
  async analyzeRootCause(context: ErrorContext): Promise<RootCause[]> {
    return [{
      type: 'type_error',
      description: 'Type mismatch detected',
      confidence: 0.7,
      evidence: [context.error.message],
    }];
  }
}

class MemoryLeakPattern extends ErrorPattern {
  name = 'Memory Leak';
  commonCauses = ['Circular references', 'Event listener leaks', 'Large arrays'];
  
  matches(type: string, message: string, context: ErrorContext): boolean {
    return message.includes('heap') || message.includes('memory');
  }
  
  async analyzeRootCause(context: ErrorContext): Promise<RootCause[]> {
    return [{
      type: 'memory_leak',
      description: 'Potential memory leak detected',
      confidence: 0.6,
      evidence: ['High memory usage'],
    }];
  }
}

class NetworkErrorPattern extends ErrorPattern {
  name = 'Network Error';
  commonCauses = ['Connection timeout', 'DNS resolution', 'Firewall blocking'];
  
  matches(type: string, message: string, context: ErrorContext): boolean {
    return message.includes('ECONNREFUSED') || message.includes('timeout');
  }
  
  async analyzeRootCause(context: ErrorContext): Promise<RootCause[]> {
    return [{
      type: 'network_error',
      description: 'Network connection issue',
      confidence: 0.8,
      evidence: [context.error.message],
    }];
  }
}

class PermissionErrorPattern extends ErrorPattern {
  name = 'Permission Error';
  commonCauses = ['Insufficient permissions', 'File system restrictions'];
  
  matches(type: string, message: string, context: ErrorContext): boolean {
    return message.includes('permission') || message.includes('denied');
  }
  
  async analyzeRootCause(context: ErrorContext): Promise<RootCause[]> {
    return [{
      type: 'permission_error',
      description: 'Permission denied',
      confidence: 0.9,
      evidence: [context.error.message],
    }];
  }
}

// Supporting classes
class MetricsCollector {
  constructor(private endpoint: string) {}
  
  track(event: string, data: any): void {
    // Send metrics to endpoint
  }
}

// Type definitions
interface ErrorDetectiveConfig {
  metricsEndpoint: string;
  sourceMapPath?: string;
  patternConfig?: string;
}

interface Environment {
  node: string;
  platform: string;
  arch: string;
  memory: any;
  uptime: number;
}

interface RootCause {
  type: string;
  description: string;
  confidence: number;
  evidence: string[];
  location?: {
    file: string;
    line: number;
    column: number;
  };
}

interface Hypothesis {
  summary: string;
  explanation: string;
  factors: string[];
  confidence: number;
  testable: string[];
}

interface Solution {
  title: string;
  description: string;
  code?: string;
  confidence: number;
}

interface Investigation {
  error: Error;
  pattern: ErrorPattern | null;
  rootCause: RootCause;
  relatedErrors: Error[];
  hypothesis: Hypothesis;
  solutions: Solution[];
  report: Report;
  confidence: number;
}

interface Report {
  timestamp: Date;
  sections: ReportSection[];
  metadata: any;
}

interface ReportSection {
  title: string;
  content: string;
}

interface MemoryUsage {
  heapUsed: number;
  heapTotal: number;
  external: number;
  rss: number;
}

interface CPUUsage {
  usage: number;
  user: number;
  system: number;
}

interface DiskUsage {
  total: number;
  available: number;
  used: number;
}

interface NetworkState {
  connections: number;
  bandwidth: number;
}

interface ProcessInfo {
  pid: number;
  name: string;
  cpu: number;
  memory: number;
}

// Export the detective
export { ErrorDetective, ErrorContext, Investigation };
```
