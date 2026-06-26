/**
 * Tree of Thoughts Agent (Simplified for Content Creator)
 */
class TreeOfThoughtsAgent {
  constructor(options = {}) {
    this.maxDepth = options.maxDepth || 2;
    this.branchFactor = options.branchFactor || 4;
    this.beamWidth = options.beamWidth || 2;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async execute(task) {
    if (this.verbose) console.log('[ToT] Generating thought branches...');
    
    // Generate initial thoughts
    const thoughts = await this.generateThoughts(task);
    
    if (this.verbose) console.log(`[ToT] Generated ${thoughts.length} thoughts`);
    
    // Evaluate and select best
    const evaluated = await this.evaluateThoughts(task, thoughts);
    const best = evaluated.sort((a, b) => b.score - a.score)[0];
    
    if (this.verbose) console.log(`[ToT] Best thought score: ${best.score}`);
    
    return best.thought;
  }

  async generateThoughts(task) {
    const prompt = `Generate ${this.branchFactor} different approaches:

${task}

Return as JSON array:
[{"thought": "approach 1"}, {"thought": "approach 2"}]`;

    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        const thoughts = JSON.parse(jsonMatch[0]);
        return thoughts.map((t, i) => ({
          id: `thought-${i}`,
          thought: t.thought,
          score: 0
        }));
      }
    } catch (e) {}
    
    // Fallback
    return [{ id: 'thought-0', thought: 'Standard approach', score: 0 }];
  }

  async evaluateThoughts(task, thoughts) {
    for (const thought of thoughts) {
      thought.score = await this.evaluateThought(task, thought.thought);
    }
    return thoughts;
  }

  async evaluateThought(task, thought) {
    const prompt = `Rate this approach (1-10):

Task: ${task}
Approach: ${thought}

Consider: creativity, feasibility, audience engagement, uniqueness.

Score (1-10):`;

    const response = await this.llm.generate(prompt);
    const score = parseFloat(response.match(/\d+(\.\d+)?/)?.[0] || '5');
    return Math.min(10, Math.max(1, score));
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Generated thought.';
    }
  };
}

/**
 * Reflection Agent (Simplified for Content Creator)
 */
class ReflectionAgent {
  constructor(options = {}) {
    this.maxIterations = options.maxIterations || 3;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
    this.criteria = options.criteria || [];
  }

  async execute(task) {
    if (this.verbose) console.log('[Reflection] Starting refinement...');
    
    // Extract content from task
    const contentMatch = task.match(/(?:content|draft)[:\s]+([\s\S]+)/i);
    let content = contentMatch ? contentMatch[1] : task;
    
    for (let i = 0; i < this.maxIterations; i++) {
      if (this.verbose) console.log(`[Reflection] Iteration ${i + 1}/${this.maxIterations}`);
      
      const feedback = await this.reflect(content);
      
      if (this.isSatisfactory(feedback)) {
        if (this.verbose) console.log('[Reflection] Satisfactory quality');
        break;
      }
      
      content = await this.revise(content, feedback);
    }
    
    return content;
  }

  async reflect(content) {
    const prompt = `Evaluate this content:

${content}

Consider:
${this.criteria.join('\n')}

Provide specific feedback on what can be improved.`;

    return await this.llm.generate(prompt);
  }

  async revise(content, feedback) {
    const prompt = `Revise this content based on feedback:

Original:
${content}

Feedback:
${feedback}

Improved version:`;

    return await this.llm.generate(prompt);
  }

  isSatisfactory(feedback) {
    return !feedback.toLowerCase().includes('major issues');
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Content looks good.';
    }
  };
}

module.exports = { TreeOfThoughtsAgent, ReflectionAgent };
