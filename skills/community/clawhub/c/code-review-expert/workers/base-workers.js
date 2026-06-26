/**
 * Base Worker Classes for Code Review
 */

class WorkerAgent {
  constructor(id, skills, capabilities) {
    this.id = id;
    this.skills = skills || [];
    this.capabilities = capabilities || {};
    this.llm = null;
  }

  async execute(subtask) {
    throw new Error('execute() must be implemented by subclass');
  }
}

class ManagerAgent {
  constructor(workers, options = {}) {
    this.workers = workers;
    this.maxRetries = options.maxRetries || 3;
    this.timeout = options.timeout || 30000;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async coordinate(task) {
    if (this.verbose) {
      console.log(`[Manager] Coordinating task: ${task.substring(0, 100)}...`);
    }

    // Decompose task
    const subtasks = await this.decompose(task);
    
    if (this.verbose) {
      console.log(`[Manager] Decomposed into ${subtasks.length} subtasks`);
    }

    // Assign to workers
    const assignments = this.assign(subtasks);
    
    // Execute in parallel
    const results = await this.executeParallel(assignments);
    
    // Integrate results
    const finalResult = await this.integrate(task, results);
    
    return finalResult;
  }

  async decompose(task) {
    const prompt = `
Decompose the following code review task into independent subtasks for different specialists:

${task}

Create subtasks for:
1. Syntax and style checking
2. Logic and bug detection
3. Security vulnerability scan
4. Performance analysis

Return as JSON array:
[
  {
    "id": "task-1",
    "description": "Subtask description",
    "specialist": "syntax-checker|logic-reviewer|security-scanner|performance-analyzer"
  }
]`;

    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      // Fallback: create default subtasks
      return [
        { id: 'task-1', description: task, specialist: 'syntax-checker' },
        { id: 'task-2', description: task, specialist: 'logic-reviewer' },
        { id: 'task-3', description: task, specialist: 'security-scanner' },
        { id: 'task-4', description: task, specialist: 'performance-analyzer' }
      ];
    }
  }

  assign(subtasks) {
    const assignments = new Map();
    
    for (const subtask of subtasks) {
      const worker = this.selectWorker(subtask);
      if (!assignments.has(worker.id)) {
        assignments.set(worker.id, []);
      }
      assignments.get(worker.id).push(subtask);
    }
    
    return assignments;
  }

  selectWorker(subtask) {
    const specialist = subtask.specialist;
    const worker = this.workers.find(w => w.id === specialist);
    return worker || this.workers[0];
  }

  async executeParallel(assignments) {
    const promises = [];
    
    for (const [workerId, subtasks] of assignments) {
      const worker = this.workers.find(w => w.id === workerId);
      
      const workerPromise = Promise.all(
        subtasks.map(subtask => this.executeWithRetry(worker, subtask))
      );
      
      promises.push(workerPromise);
    }
    
    const results = await Promise.all(promises);
    return results.flat();
  }

  async executeWithRetry(worker, subtask) {
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        const result = await worker.execute(subtask);
        return {
          taskId: subtask.id,
          success: true,
          result,
          worker: worker.id
        };
      } catch (error) {
        if (attempt === this.maxRetries) {
          return {
            taskId: subtask.id,
            success: false,
            error: error.message,
            worker: worker.id
          };
        }
        await this.sleep(1000 * attempt);
      }
    }
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async integrate(task, results) {
    const successfulResults = results.filter(r => r.success);
    const failedResults = results.filter(r => !r.success);
    
    const prompt = `
Original task: ${task.substring(0, 200)}...

Review results from specialists (${successfulResults.length} successful):
${successfulResults.map(r => `
=== ${r.worker} ===
${r.result}
`).join('\n')}

${failedResults.length > 0 ? `
Failed reviews (${failedResults.length}):
${failedResults.map(r => `- ${r.worker}: ${r.error}`).join('\n')}
` : ''}

Integrate all review results into a comprehensive code review report with:
1. Overview
2. Issues by severity (Critical, High, Medium, Low)
3. Specific recommendations
4. Overall score (0-10)

Final Report:`;

    return await this.llm.generate(prompt);
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Review complete.';
    }
  };
}

module.exports = { WorkerAgent, ManagerAgent };
