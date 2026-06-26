# Trae Agent — Code Examples

## Example 1

```typescript
// trae-agent.ts
interface RepositoryTask {
  instruction: string;
  repository: RepositoryInfo;
  constraints?: TaskConstraints;
  context?: TaskContext;
}

interface RepositoryInfo {
  path: string;
  language: string;
  framework?: string;
  structure: DirectoryStructure;
  dependencies: DependencyGraph;
}

interface SearchResult {
  file: string;
  content: string;
  relevance: number;
  type: 'exact' | 'semantic' | 'structural';
}

interface EditPlan {
  files: FileEdit[];
  order: number[];
  dependencies: EditDependency[];
  validation: ValidationStep[];
}

class TraeAgent {
  private indexer: CodebaseIndexer;
  private searcher: EnsembleSearcher;
  private planner: EditPlanner;
  private executor: CodeExecutor;

  constructor(config: TraeAgentConfig) {
    this.indexer = new CodebaseIndexer(config.indexConfig);
    this.searcher = new EnsembleSearcher(config.searchConfig);
    this.planner = new EditPlanner(config.planConfig);
    this.executor = new CodeExecutor(config.execConfig);
  }

  async executeTask(task: RepositoryTask): Promise<TaskResult> {
    // Step 1: Index repository
    await this.indexRepository(task.repository);

    // Step 2: Understand task requirements
    const understanding = await this.understandTask(task);

    // Step 3: Search for relevant code
    const relevantCode = await this.ensembleSearch(understanding, task.repository);

    // Step 4: Generate edit plan
    const plan = await this.planEdits(understanding, relevantCode);

    // Step 5: Execute plan with validation
    const result = await this.executePlan(plan, task);

    return result;
  }

  // Repository Indexing
  private async indexRepository(repo: RepositoryInfo): Promise<void> {
    // Parse all source files
    const files = await this.indexer.discoverFiles(repo.path);

    for (const file of files) {
      // Build AST
      const ast = await this.indexer.parseFile(file);

      // Extract symbols
      const symbols = await this.indexer.extractSymbols(ast);

      // Build embeddings for semantic search
      const embeddings = await this.indexer.generateEmbeddings(file, symbols);

      // Store in index
      await this.indexer.store(file, { ast, symbols, embeddings });
    }

    // Build cross-file references
    await this.indexer.buildCallGraph(repo.path);
    await this.indexer.buildDependencyGraph(repo.path);
  }

  // Task Understanding
  private async understandTask(task: RepositoryTask): Promise<TaskUnderstanding> {
    // Decompose natural language instruction
    const parsed = await this.parseInstruction(task.instruction);

    // Identify task type
    const taskType = this.classifyTask(parsed);

    // Extract entities (files, functions, variables mentioned)
    const entities = await this.extractEntities(parsed, task.repository);

    // Determine scope
    const scope = this.determineScope(parsed, entities);

    return {
      taskType,
      entities,
      scope,
      requirements: parsed.requirements,
      constraints: task.constraints,
    };
  }

  private classifyTask(parsed: ParsedInstruction): TaskType {
    const keywords = parsed.keywords;

    if (keywords.some(k => ['add', 'create', 'implement', 'new'].includes(k))) {
      return 'create';
    }
    if (keywords.some(k => ['fix', 'bug', 'error', 'issue'].includes(k))) {
      return 'fix';
    }
    if (keywords.some(k => ['refactor', 'improve', 'optimize'].includes(k))) {
      return 'refactor';
    }
    if (keywords.some(k => ['delete', 'remove'].includes(k))) {
      return 'delete';
    }
    if (keywords.some(k => ['test', 'testing'].includes(k))) {
      return 'test';
    }
    if (keywords.some(k => ['explain', 'how', 'what', 'why'].includes(k))) {
      return 'understand';
    }

    return 'modify';
  }

  // Ensemble Search
  private async ensembleSearch(
    understanding: TaskUnderstanding,
    repo: RepositoryInfo
  ): Promise<SearchResult[]> {
    const results: SearchResult[] = [];

    // Strategy 1: Exact keyword search
    const keywordResults = await this.searcher.keywordSearch(
      understanding.entities.map(e => e.name),
      repo.path
    );
    results.push(...keywordResults.map(r => ({ ...r, type: 'exact' as const })));

    // Strategy 2: Semantic search
    const semanticQuery = this.buildSemanticQuery(understanding);
    const semanticResults = await this.searcher.semanticSearch(semanticQuery, repo.path);
    results.push(...semanticResults.map(r => ({ ...r, type: 'semantic' as const })));

    // Strategy 3: Structural search (AST-based)
    const structuralResults = await this.searcher.structuralSearch(
      understanding.entities,
      repo.path
    );
    results.push(...structuralResults.map(r => ({ ...r, type: 'structural' as const })));

    // Ensemble ranking
    return this.rankAndDeduplicate(results);
  }

  private rankAndDeduplicate(results: SearchResult[]): SearchResult[] {
    // Group by file
    const byFile = new Map<string, SearchResult[]>();
    for (const result of results) {
      if (!byFile.has(result.file)) {
        byFile.set(result.file, []);
      }
      byFile.get(result.file)!.push(result);
    }

    // Score each file
    const fileScores: Array<{ file: string; score: number; content: string }> = [];

    for (const [file, fileResults] of byFile) {
      // Weighted combination of search types
      let score = 0;
      const weights = { exact: 1.0, semantic: 0.7, structural: 0.8 };

      for (const result of fileResults) {
        score += result.relevance * weights[result.type];
      }

      // Normalize by number of results (diversity bonus)
      score *= 1 + 0.1 * Math.min(fileResults.length, 5);

      fileScores.push({
        file,
        score,
        content: fileResults[0].content,
      });
    }

    // Sort by score and take top results
    return fileScores
      .sort((a, b) => b.score - a.score)
      .slice(0, 20)
      .map(f => ({
        file: f.file,
        content: f.content,
        relevance: f.score,
        type: 'exact' as const, // Merged
      }));
  }

  // Edit Planning
  private async planEdits(
    understanding: TaskUnderstanding,
    relevantCode: SearchResult[]
  ): Promise<EditPlan> {
    const edits: FileEdit[] = [];

    // Determine which files need modification
    const filesToModify = this.selectFilesToModify(understanding, relevantCode);

    for (const file of filesToModify) {
      // Read current content
      const content = await this.readFile(file);

      // Generate edit based on task type
      const edit = await this.generateEdit(understanding, file, content, relevantCode);

      if (edit) {
        edits.push(edit);
      }
    }

    // Determine edit order based on dependencies
    const order = this.topologicalSort(edits);

    // Create validation steps
    const validation = this.createValidationSteps(edits, understanding);

    return {
      files: edits,
      order,
      dependencies: this.findEditDependencies(edits),
      validation,
    };
  }

  private async generateEdit(
    understanding: TaskUnderstanding,
    file: string,
    content: string,
    context: SearchResult[]
  ): Promise<FileEdit | null> {
    // Build prompt with context
    const prompt = this.buildEditPrompt(understanding, file, content, context);

    // Generate edit using LLM
    const response = await this.generateWithLLM(prompt);

    // Parse response into structured edit
    return this.parseEditResponse(response, file, content);
  }

  // Execution with Validation
  private async executePlan(plan: EditPlan, task: RepositoryTask): Promise<TaskResult> {
    const executedEdits: ExecutedEdit[] = [];
    const errors: ExecutionError[] = [];

    // Execute edits in order
    for (const index of plan.order) {
      const edit = plan.files[index];

      try {
        // Apply edit
        await this.applyEdit(edit);
        executedEdits.push({ edit, status: 'applied' });

        // Run relevant validations
        const validations = plan.validation.filter(v => v.affectedFile === edit.file);
        for (const validation of validations) {
          const result = await this.runValidation(validation);
          if (!result.passed) {
            // Rollback and try alternative
            await this.rollbackEdit(edit);
            const alternative = await this.generateAlternativeEdit(edit, result.error);
            if (alternative) {
              await this.applyEdit(alternative);
              executedEdits.push({ edit: alternative, status: 'applied_alternative' });
            } else {
              errors.push({ edit, error: result.error });
            }
          }
        }
      } catch (error) {
        errors.push({ edit, error: error.message });
      }
    }

    // Final validation
    const finalValidation = await this.runFinalValidation(task);

    return {
      success: errors.length === 0 && finalValidation.passed,
      edits: executedEdits,
      errors,
      validation: finalValidation,
    };
  }

  private createValidationSteps(edits: FileEdit[], understanding: TaskUnderstanding): ValidationStep[] {
    const steps: ValidationStep[] = [];

    // Syntax validation for each file
    for (const edit of edits) {
      steps.push({
        type: 'syntax',
        affectedFile: edit.file,
        command: `npx tsc --noEmit ${edit.file}`,
      });
    }

    // Type checking if TypeScript
    if (edits.some(e => e.file.endsWith('.ts') || e.file.endsWith('.tsx'))) {
      steps.push({
        type: 'typecheck',
        affectedFile: '*',
        command: 'npx tsc --noEmit',
      });
    }

    // Linting
    steps.push({
      type: 'lint',
      affectedFile: '*',
      command: 'npm run lint',
    });

    // Tests if task is not 'understand'
    if (understanding.taskType !== 'understand') {
      steps.push({
        type: 'test',
        affectedFile: '*',
        command: 'npm test',
      });
    }

    return steps;
  }

  // Helper methods
  private buildSemanticQuery(understanding: TaskUnderstanding): string {
    const parts: string[] = [];

    parts.push(`Task: ${understanding.taskType}`);

    for (const entity of understanding.entities) {
      parts.push(`${entity.type}: ${entity.name}`);
    }

    parts.push(`Scope: ${understanding.scope}`);

    return parts.join('\n');
  }

  private topologicalSort(edits: FileEdit[]): number[] {
    // Simple dependency-based ordering
    const order: number[] = [];
    const visited = new Set<number>();

    const visit = (index: number) => {
      if (visited.has(index)) return;
      visited.add(index);

      // Visit dependencies first
      const deps = this.findDependencies(edits[index], edits);
      for (const dep of deps) {
        visit(dep);
      }

      order.push(index);
    };

    for (let i = 0; i < edits.length; i++) {
      visit(i);
    }

    return order;
  }
}

// Types
interface TaskUnderstanding {
  taskType: TaskType;
  entities: Entity[];
  scope: 'file' | 'module' | 'repository';
  requirements: string[];
  constraints?: TaskConstraints;
}

type TaskType = 'create' | 'fix' | 'refactor' | 'delete' | 'test' | 'understand' | 'modify';

interface Entity {
  name: string;
  type: 'file' | 'function' | 'class' | 'variable' | 'module';
  location?: string;
}

interface FileEdit {
  file: string;
  originalContent: string;
  newContent: string;
  changes: Change[];
}

interface Change {
  type: 'insert' | 'delete' | 'replace';
  startLine: number;
  endLine: number;
  content: string;
}

interface ValidationStep {
  type: 'syntax' | 'typecheck' | 'lint' | 'test' | 'custom';
  affectedFile: string;
  command: string;
}

interface TaskResult {
  success: boolean;
  edits: ExecutedEdit[];
  errors: ExecutionError[];
  validation: ValidationResult;
}

export { TraeAgent, RepositoryTask, TaskResult };
```
