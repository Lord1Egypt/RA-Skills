# AutoSpec — Code Examples

## Example 1

```typescript
// autospec.ts
interface SpecificationContext {
  code: CodeUnit;
  existingSpecs: Specification[];
  testCases: TestCase[];
  verificationGoals: VerificationGoal[];
}

interface Specification {
  type: 'precondition' | 'postcondition' | 'invariant' | 'assertion';
  expression: string;
  location: CodeLocation;
  confidence: number;
  evidence: Evidence[];
}

interface VerificationGoal {
  property: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
}

class AutoSpec {
  private prover: TheoremProver;
  private analyzer: StaticAnalyzer;
  private synthesizer: SpecSynthesizer;

  constructor(config: AutoSpecConfig) {
    this.prover = new TheoremProver(config.proverBackend);
    this.analyzer = new StaticAnalyzer(config.analysisDepth);
    this.synthesizer = new SpecSynthesizer(config.synthesisStrategy);
  }

  async synthesizeSpecifications(context: SpecificationContext): Promise<SpecificationResult> {
    // Step 1: Analyze code structure
    const codeAnalysis = await this.analyzeCode(context.code);

    // Step 2: Infer preconditions
    const preconditions = await this.inferPreconditions(codeAnalysis, context);

    // Step 3: Infer postconditions
    const postconditions = await this.inferPostconditions(codeAnalysis, context);

    // Step 4: Infer loop invariants
    const invariants = await this.inferLoopInvariants(codeAnalysis, context);

    // Step 5: Verify synthesized specs
    const verified = await this.verifySpecifications(
      [...preconditions, ...postconditions, ...invariants],
      context
    );

    return {
      specifications: verified,
      coverage: this.calculateCoverage(verified, context),
      verificationStatus: this.getVerificationStatus(verified),
    };
  }

  // Precondition Inference
  private async inferPreconditions(
    analysis: CodeAnalysis,
    context: SpecificationContext
  ): Promise<Specification[]> {
    const preconditions: Specification[] = [];

    for (const func of analysis.functions) {
      // Parameter nullability
      for (const param of func.parameters) {
        if (this.isUsedWithoutNullCheck(param, func.body)) {
          preconditions.push({
            type: 'precondition',
            expression: `${param.name} != null`,
            location: { file: func.file, line: func.startLine },
            confidence: 0.9,
            evidence: [{ type: 'usage', value: 'Parameter dereferenced without null check' }],
          });
        }
      }

      // Numeric bounds
      for (const param of func.parameters.filter(p => this.isNumeric(p.type))) {
        const bounds = this.inferNumericBounds(param, func.body);
        if (bounds) {
          preconditions.push({
            type: 'precondition',
            expression: bounds.expression,
            location: { file: func.file, line: func.startLine },
            confidence: bounds.confidence,
            evidence: bounds.evidence,
          });
        }
      }

      // Array bounds
      for (const param of func.parameters.filter(p => this.isArray(p.type))) {
        const indexAccesses = this.findArrayAccesses(param, func.body);
        for (const access of indexAccesses) {
          preconditions.push({
            type: 'precondition',
            expression: `${access.index} >= 0 && ${access.index} < ${param.name}.length`,
            location: { file: func.file, line: access.line },
            confidence: 0.85,
            evidence: [{ type: 'access', value: `Array access at index ${access.index}` }],
          });
        }
      }

      // From test cases (dynamic inference)
      const testDerivedPre = this.inferFromTests(func, context.testCases, 'pre');
      preconditions.push(...testDerivedPre);
    }

    return this.deduplicateAndRank(preconditions);
  }

  // Postcondition Inference
  private async inferPostconditions(
    analysis: CodeAnalysis,
    context: SpecificationContext
  ): Promise<Specification[]> {
    const postconditions: Specification[] = [];

    for (const func of analysis.functions) {
      // Return value properties
      if (func.returnType !== 'void') {
        // Non-null return
        if (this.alwaysReturnsNonNull(func)) {
          postconditions.push({
            type: 'postcondition',
            expression: 'result != null',
            location: { file: func.file, line: func.endLine },
            confidence: 0.85,
            evidence: [{ type: 'analysis', value: 'All return paths return non-null' }],
          });
        }

        // Return bounds
        const returnBounds = this.inferReturnBounds(func);
        if (returnBounds) {
          postconditions.push({
            type: 'postcondition',
            expression: returnBounds.expression,
            location: { file: func.file, line: func.endLine },
            confidence: returnBounds.confidence,
            evidence: returnBounds.evidence,
          });
        }
      }

      // State modifications
      const modifications = this.trackStateModifications(func);
      for (const mod of modifications) {
        postconditions.push({
          type: 'postcondition',
          expression: mod.postcondition,
          location: { file: func.file, line: func.endLine },
          confidence: mod.confidence,
          evidence: [{ type: 'modification', value: mod.description }],
        });
      }

      // Relationship between input and output
      const relationships = this.inferInputOutputRelations(func, context.testCases);
      postconditions.push(...relationships);
    }

    return this.deduplicateAndRank(postconditions);
  }

  // Loop Invariant Inference
  private async inferLoopInvariants(
    analysis: CodeAnalysis,
    context: SpecificationContext
  ): Promise<Specification[]> {
    const invariants: Specification[] = [];

    for (const loop of analysis.loops) {
      // Induction variable bounds
      const inductionVar = this.findInductionVariable(loop);
      if (inductionVar) {
        invariants.push({
          type: 'invariant',
          expression: `${inductionVar.name} >= ${inductionVar.init} && ${inductionVar.name} <= ${inductionVar.bound}`,
          location: { file: loop.file, line: loop.startLine },
          confidence: 0.9,
          evidence: [{ type: 'induction', value: 'Loop counter bounds' }],
        });
      }

      // Array index bounds in loop
      const arrayAccesses = this.findArrayAccessesInLoop(loop);
      for (const access of arrayAccesses) {
        invariants.push({
          type: 'invariant',
          expression: `${access.index} >= 0 && ${access.index} < ${access.array}.length`,
          location: { file: loop.file, line: loop.startLine },
          confidence: 0.85,
          evidence: [{ type: 'bounds', value: 'Array access within loop' }],
        });
      }

      // Partial result properties (for accumulating loops)
      const partialResult = this.inferPartialResultProperty(loop);
      if (partialResult) {
        invariants.push({
          type: 'invariant',
          expression: partialResult.expression,
          location: { file: loop.file, line: loop.startLine },
          confidence: partialResult.confidence,
          evidence: partialResult.evidence,
        });
      }

      // Termination metrics
      const termination = this.inferTerminationMetric(loop);
      if (termination) {
        invariants.push({
          type: 'invariant',
          expression: termination.expression,
          location: { file: loop.file, line: loop.startLine },
          confidence: 0.8,
          evidence: [{ type: 'termination', value: 'Loop termination guarantee' }],
        });
      }
    }

    return this.deduplicateAndRank(invariants);
  }

  // Verification
  private async verifySpecifications(
    specs: Specification[],
    context: SpecificationContext
  ): Promise<Specification[]> {
    const verified: Specification[] = [];

    for (const spec of specs) {
      // Generate verification conditions
      const vc = this.generateVerificationCondition(spec, context);

      // Attempt to prove
      const proofResult = await this.prover.prove(vc);

      if (proofResult.status === 'valid') {
        spec.confidence = Math.min(1.0, spec.confidence + 0.1);
        verified.push(spec);
      } else if (proofResult.status === 'unknown') {
        // Keep but mark as unverified
        spec.evidence.push({ type: 'verification', value: 'Could not verify automatically' });
        verified.push(spec);
      }
      // Drop if proven invalid
    }

    return verified;
  }

  // Hierarchical decomposition for complex specs
  private async decomposeComplexSpec(spec: Specification): Promise<Specification[]> {
    const subSpecs: Specification[] = [];

    // Parse the expression into sub-components
    const parts = this.parseLogicalExpression(spec.expression);

    for (const part of parts) {
      const subSpec: Specification = {
        ...spec,
        expression: part,
        confidence: spec.confidence * 0.9, // Slightly lower confidence for sub-specs
      };

      // Verify sub-spec independently
      subSpecs.push(subSpec);
    }

    return subSpecs;
  }

  // Output generation
  generateSpecificationCode(specs: Specification[], language: string): string {
    switch (language) {
      case 'dafny':
        return this.generateDafnySpecs(specs);
      case 'jml':
        return this.generateJMLSpecs(specs);
      case 'frama-c':
        return this.generateFramaCSpecs(specs);
      default:
        return this.generateGenericSpecs(specs);
    }
  }

  private generateDafnySpecs(specs: Specification[]): string {
    let output = '';

    const preconditions = specs.filter(s => s.type === 'precondition');
    const postconditions = specs.filter(s => s.type === 'postcondition');
    const invariants = specs.filter(s => s.type === 'invariant');

    for (const pre of preconditions) {
      output += `requires ${pre.expression}\n`;
    }

    for (const post of postconditions) {
      output += `ensures ${post.expression}\n`;
    }

    for (const inv of invariants) {
      output += `invariant ${inv.expression}\n`;
    }

    return output;
  }

  private generateJMLSpecs(specs: Specification[]): string {
    let output = '/*@\n';

    for (const spec of specs) {
      switch (spec.type) {
        case 'precondition':
          output += `  @ requires ${spec.expression};\n`;
          break;
        case 'postcondition':
          output += `  @ ensures ${spec.expression};\n`;
          break;
        case 'invariant':
          output += `  @ loop_invariant ${spec.expression};\n`;
          break;
      }
    }

    output += '  @*/\n';
    return output;
  }
}

interface SpecificationResult {
  specifications: Specification[];
  coverage: CoverageMetrics;
  verificationStatus: VerificationStatus;
}

interface CodeAnalysis {
  functions: FunctionInfo[];
  loops: LoopInfo[];
  variables: VariableInfo[];
}

interface CoverageMetrics {
  functionsWithPreconditions: number;
  functionsWithPostconditions: number;
  loopsWithInvariants: number;
  totalFunctions: number;
  totalLoops: number;
}

interface VerificationStatus {
  proven: number;
  unproven: number;
  invalid: number;
}

export { AutoSpec, Specification, SpecificationResult };
```
