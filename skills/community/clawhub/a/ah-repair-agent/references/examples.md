# RepairAgent — Code Examples

## Example 1

```typescript
// repair-agent.ts
interface RepairContext {
  bugReport: BugReport;
  testResults: TestResult[];
  codebase: CodebaseInfo;
  suspiciousLocations: SuspiciousLocation[];
  hypotheses: Hypothesis[];
  patches: Patch[];
}

interface SuspiciousLocation {
  file: string;
  line: number;
  method: string;
  suspiciousness: number;
  evidence: string[];
}

interface Hypothesis {
  id: string;
  description: string;
  rootCause: string;
  confidence: number;
  evidence: Evidence[];
  suggestedFix: string;
}

interface Patch {
  id: string;
  hypothesisId: string;
  changes: FileChange[];
  testsPassed: boolean;
  validationStatus: 'pending' | 'passed' | 'failed' | 'partial';
}

class RepairAgent {
  private maxIterations = 10;
  private currentIteration = 0;

  async repair(context: RepairContext): Promise<RepairResult> {
    // Phase 1: Fault Localization
    const suspiciousLocations = await this.localizeFault(context);

    // Phase 2: Hypothesis Generation
    const hypotheses = await this.generateHypotheses(suspiciousLocations, context);

    // Phase 3: Patch Generation
    const patches = await this.generatePatches(hypotheses, context);

    // Phase 4: Validation
    const validatedPatches = await this.validatePatches(patches, context);

    // Phase 5: Iterative Refinement
    return await this.refineUntilSuccess(validatedPatches, context);
  }

  // Phase 1: Fault Localization
  private async localizeFault(context: RepairContext): Promise<SuspiciousLocation[]> {
    const locations: SuspiciousLocation[] = [];

    // Spectrum-based fault localization (SBFL)
    const spectrumResults = await this.spectrumBasedLocalization(context.testResults);
    locations.push(...spectrumResults);

    // Stack trace analysis
    const stackTraceResults = await this.analyzeStackTraces(context.testResults);
    locations.push(...stackTraceResults);

    // Mutation-based localization
    const mutationResults = await this.mutationBasedLocalization(context);
    locations.push(...mutationResults);

    // Rank and deduplicate
    return this.rankLocations(locations);
  }

  private async spectrumBasedLocalization(testResults: TestResult[]): Promise<SuspiciousLocation[]> {
    // Calculate suspiciousness using Ochiai formula:
    // suspiciousness = failed(s) / sqrt(totalFailed * (failed(s) + passed(s)))

    const coverage = new Map<string, { passed: number; failed: number }>();

    for (const test of testResults) {
      for (const coveredLine of test.coveredLines) {
        const key = `${coveredLine.file}:${coveredLine.line}`;
        if (!coverage.has(key)) {
          coverage.set(key, { passed: 0, failed: 0 });
        }
        const stats = coverage.get(key)!;
        if (test.passed) {
          stats.passed++;
        } else {
          stats.failed++;
        }
      }
    }

    const totalFailed = testResults.filter(t => !t.passed).length;
    const locations: SuspiciousLocation[] = [];

    for (const [key, stats] of coverage) {
      const [file, lineStr] = key.split(':');
      const line = parseInt(lineStr);

      // Ochiai formula
      const suspiciousness = stats.failed /
        Math.sqrt(totalFailed * (stats.failed + stats.passed));

      if (suspiciousness > 0.3) {
        locations.push({
          file,
          line,
          method: await this.getMethodName(file, line),
          suspiciousness,
          evidence: [`Failed: ${stats.failed}, Passed: ${stats.passed}`],
        });
      }
    }

    return locations;
  }

  // Phase 2: Hypothesis Generation
  private async generateHypotheses(
    locations: SuspiciousLocation[],
    context: RepairContext
  ): Promise<Hypothesis[]> {
    const hypotheses: Hypothesis[] = [];

    for (const location of locations.slice(0, 5)) { // Top 5 locations
      // Analyze code at location
      const code = await this.getCodeContext(location.file, location.line);

      // Generate hypotheses based on patterns
      const patternHypotheses = this.generatePatternHypotheses(code, location);
      hypotheses.push(...patternHypotheses);

      // Generate hypotheses from error messages
      const errorHypotheses = this.generateErrorHypotheses(context.testResults, location);
      hypotheses.push(...errorHypotheses);
    }

    return this.rankHypotheses(hypotheses);
  }

  private generatePatternHypotheses(code: string, location: SuspiciousLocation): Hypothesis[] {
    const hypotheses: Hypothesis[] = [];

    // Null pointer patterns
    if (code.includes('.') && !code.includes('!= null') && !code.includes('?')) {
      hypotheses.push({
        id: `null-${location.line}`,
        description: 'Possible null pointer dereference',
        rootCause: 'Missing null check before method call or property access',
        confidence: 0.7,
        evidence: [{ type: 'pattern', value: 'Dot notation without null guard' }],
        suggestedFix: 'Add null check or optional chaining',
      });
    }

    // Off-by-one patterns
    if (code.includes('<=') || code.includes('< length')) {
      hypotheses.push({
        id: `obo-${location.line}`,
        description: 'Possible off-by-one error',
        rootCause: 'Boundary condition may be incorrect',
        confidence: 0.5,
        evidence: [{ type: 'pattern', value: 'Loop boundary comparison' }],
        suggestedFix: 'Check loop boundary conditions',
      });
    }

    // Type coercion patterns
    if (code.includes('==') && !code.includes('===')) {
      hypotheses.push({
        id: `type-${location.line}`,
        description: 'Possible type coercion issue',
        rootCause: 'Loose equality may cause unexpected behavior',
        confidence: 0.6,
        evidence: [{ type: 'pattern', value: 'Loose equality operator' }],
        suggestedFix: 'Use strict equality (===)',
      });
    }

    // Resource leak patterns
    if (code.includes('open') || code.includes('connect') || code.includes('acquire')) {
      hypotheses.push({
        id: `leak-${location.line}`,
        description: 'Possible resource leak',
        rootCause: 'Resource may not be properly closed',
        confidence: 0.5,
        evidence: [{ type: 'pattern', value: 'Resource acquisition' }],
        suggestedFix: 'Ensure resource is closed in finally block or use try-with-resources',
      });
    }

    return hypotheses;
  }

  // Phase 3: Patch Generation
  private async generatePatches(
    hypotheses: Hypothesis[],
    context: RepairContext
  ): Promise<Patch[]> {
    const patches: Patch[] = [];

    for (const hypothesis of hypotheses) {
      // Generate patch based on hypothesis type
      const patch = await this.generatePatchForHypothesis(hypothesis, context);
      if (patch) {
        patches.push(patch);
      }
    }

    return patches;
  }

  private async generatePatchForHypothesis(
    hypothesis: Hypothesis,
    context: RepairContext
  ): Promise<Patch | null> {
    const changes: FileChange[] = [];

    // Extract location from hypothesis ID
    const [type, lineStr] = hypothesis.id.split('-');
    const line = parseInt(lineStr);

    // Find the file containing this line
    for (const location of context.suspiciousLocations) {
      if (location.line === line) {
        const originalCode = await this.getLineContent(location.file, line);
        let newCode: string;

        switch (type) {
          case 'null':
            newCode = this.addNullCheck(originalCode);
            break;
          case 'obo':
            newCode = this.fixOffByOne(originalCode);
            break;
          case 'type':
            newCode = originalCode.replace(/==/g, '===');
            break;
          case 'leak':
            newCode = this.addResourceCleanup(originalCode);
            break;
          default:
            continue;
        }

        changes.push({
          file: location.file,
          line,
          originalCode,
          newCode,
        });

        return {
          id: `patch-${hypothesis.id}`,
          hypothesisId: hypothesis.id,
          changes,
          testsPassed: false,
          validationStatus: 'pending',
        };
      }
    }

    return null;
  }

  // Phase 4: Validation
  private async validatePatches(patches: Patch[], context: RepairContext): Promise<Patch[]> {
    const validated: Patch[] = [];

    for (const patch of patches) {
      // Apply patch temporarily
      await this.applyPatch(patch);

      // Run tests
      const testResults = await this.runTests(context);

      // Check results
      const allPassed = testResults.every(t => t.passed);
      const somePassed = testResults.some(t => t.passed);

      patch.testsPassed = allPassed;
      patch.validationStatus = allPassed ? 'passed' : (somePassed ? 'partial' : 'failed');

      // Revert patch
      await this.revertPatch(patch);

      validated.push(patch);
    }

    return validated.sort((a, b) => {
      if (a.validationStatus === 'passed') return -1;
      if (b.validationStatus === 'passed') return 1;
      if (a.validationStatus === 'partial') return -1;
      if (b.validationStatus === 'partial') return 1;
      return 0;
    });
  }

  // Phase 5: Iterative Refinement
  private async refineUntilSuccess(
    patches: Patch[],
    context: RepairContext
  ): Promise<RepairResult> {
    this.currentIteration++;

    // Check for successful patch
    const successfulPatch = patches.find(p => p.validationStatus === 'passed');
    if (successfulPatch) {
      return {
        success: true,
        patch: successfulPatch,
        iterations: this.currentIteration,
        message: 'Bug successfully fixed!',
      };
    }

    // Check iteration limit
    if (this.currentIteration >= this.maxIterations) {
      return {
        success: false,
        patch: patches[0], // Best partial patch
        iterations: this.currentIteration,
        message: 'Max iterations reached without complete fix',
      };
    }

    // Get partial patches for refinement
    const partialPatches = patches.filter(p => p.validationStatus === 'partial');
    if (partialPatches.length > 0) {
      // Generate refined hypotheses based on remaining failures
      const refinedContext = await this.updateContext(context, partialPatches[0]);
      return this.repair(refinedContext);
    }

    // Generate new hypotheses with different strategies
    const newHypotheses = await this.generateAlternativeHypotheses(context);
    const newPatches = await this.generatePatches(newHypotheses, context);
    const validatedNew = await this.validatePatches(newPatches, context);

    return this.refineUntilSuccess(validatedNew, context);
  }

  // Helper methods
  private addNullCheck(code: string): string {
    // Simple null check addition
    const match = code.match(/(\w+)\./);
    if (match) {
      const varName = match[1];
      return `if (${varName} != null) { ${code} }`;
    }
    return code;
  }

  private fixOffByOne(code: string): string {
    return code
      .replace(/<=/g, '<')
      .replace(/>=/g, '>');
  }

  private addResourceCleanup(code: string): string {
    return `try { ${code} } finally { /* close resource */ }`;
  }

  // ... additional helper methods
}

interface RepairResult {
  success: boolean;
  patch: Patch | null;
  iterations: number;
  message: string;
}

interface TestResult {
  name: string;
  passed: boolean;
  error?: string;
  stackTrace?: string;
  coveredLines: { file: string; line: number }[];
}

interface FileChange {
  file: string;
  line: number;
  originalCode: string;
  newCode: string;
}

interface Evidence {
  type: string;
  value: string;
}

export { RepairAgent, RepairContext, RepairResult };
```
