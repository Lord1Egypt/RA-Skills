/**
 * Tree of Thoughts Agent - 思维树模式实现
 * 
 * 核心：Branch → Evaluate → Select → Expand
 */

class TreeOfThoughtsAgent {
  constructor(options = {}) {
    this.maxDepth = options.maxDepth || 3;
    this.branchFactor = options.branchFactor || 3;
    this.beamWidth = options.beamWidth || 2;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async execute(task) {
    if (this.verbose) {
      console.log(`[Tree of Thoughts] 开始任务：${task}`);
    }
    
    // 初始化根节点
    const root = {
      id: 'root',
      thought: '',
      depth: 0,
      score: 0,
      parent: null,
      children: []
    };
    
    // 生成初始思考
    const initialThoughts = await this.generateThoughts(task, root);
    root.children = initialThoughts;
    
    if (this.verbose) {
      console.log(`[Initial Thoughts] Generated ${initialThoughts.length} thoughts\n`);
    }
    
    // Beam Search
    let currentLevel = initialThoughts;
    
    for (let depth = 1; depth <= this.maxDepth; depth++) {
      if (this.verbose) {
        console.log(`[Depth ${depth}/${this.maxDepth}]`);
      }
      
      // 评估当前层
      const evaluatedThoughts = await this.evaluateThoughts(task, currentLevel);
      
      if (this.verbose) {
        evaluatedThoughts.forEach(t => {
          console.log(`  [${t.id}] Score: ${t.score.toFixed(1)} - ${t.thought.substring(0, 50)}...`);
        });
        console.log();
      }
      
      // 检查是否找到解决方案
      const solution = evaluatedThoughts.find(t => t.score >= 9);
      if (solution) {
        if (this.verbose) {
          console.log(`[Solution Found] Score: ${solution.score}\n`);
        }
        return this.extractSolution(task, solution);
      }
      
      // 选择 top-k
      const selectedThoughts = this.selectTopK(evaluatedThoughts, this.beamWidth);
      
      if (this.verbose) {
        console.log(`[Selected] Keeping ${selectedThoughts.length} thoughts\n`);
      }
      
      // 生成子思考
      const nextLevel = [];
      for (const thought of selectedThoughts) {
        const children = await this.generateThoughts(task, thought);
        thought.children = children;
        nextLevel.push(...children);
      }
      
      if (nextLevel.length === 0) {
        if (this.verbose) {
          console.log('[No More Thoughts] Cannot expand further\n');
        }
        break;
      }
      
      currentLevel = nextLevel;
    }
    
    // 返回最佳方案
    const bestThought = currentLevel.sort((a, b) => b.score - a.score)[0];
    return this.extractSolution(task, bestThought);
  }

  async generateThoughts(task, parent) {
    const prompt = `
任务：${task}

当前思考：${parent.thought || '(Initial)'}
Depth: ${parent.depth}

请生成 ${this.branchFactor} 个不同的思考方向。

要求：
1. 每个思考应该是不同的角度或方法
2. 思考应该具体、可执行
3. 思考之间应该有差异性

请以 JSON 数组格式返回：
[
  {
    "thought": "思考内容"
  }
]

思考：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        const thoughts = JSON.parse(jsonMatch[0]);
        return thoughts.map((t, i) => ({
          id: `${parent.id}-${i}`,
          thought: t.thought,
          depth: parent.depth + 1,
          score: 0,
          parent: parent.id,
          children: []
        }));
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      return [{
        id: `${parent.id}-0`,
        thought: 'Continue exploring',
        depth: parent.depth + 1,
        score: 0,
        parent: parent.id,
        children: []
      }];
    }
  }

  async evaluateThoughts(task, thoughts) {
    const evaluatedThoughts = [];
    
    for (const thought of thoughts) {
      const score = await this.evaluateThought(task, thought);
      evaluatedThoughts.push({ ...thought, score });
    }
    
    return evaluatedThoughts;
  }

  async evaluateThought(task, thought) {
    const prompt = `
任务：${task}

思考：${thought.thought}

请评估这个思考的质量（1-10 分）：

评分标准：
- 10 分：完美解决方案，直接可以实施
- 8-9 分：很好的方案，少量改进即可
- 6-7 分：可行方案，需要一些改进
- 4-5 分：有潜力，但需要大量改进
- 1-3 分：不可行或方向错误

考虑因素：
1. 可行性：这个方案可以实施吗？
2. 有效性：能解决问题吗？
3. 效率：是高效的方法吗？
4. 完整性：覆盖了关键要点吗？

评分（只返回 1-10 的数字）：`;
    
    const response = await this.llm.generate(prompt);
    const score = parseFloat(response.match(/\d+(\.\d+)?/)?.[0] || '5');
    
    return Math.min(10, Math.max(1, score));
  }

  selectTopK(thoughts, k) {
    return thoughts
      .sort((a, b) => b.score - a.score)
      .slice(0, k);
  }

  async extractSolution(task, thought) {
    const prompt = `
任务：${task}

思考路径：${thought.thought}

请基于这个思考路径，生成最终的解决方案。

解决方案：`;
    
    return await this.llm.generate(prompt);
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Generated thought.';
    }
  };
}

module.exports = { TreeOfThoughtsAgent };
