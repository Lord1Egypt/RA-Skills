/**
 * Reflection Agent - 自我反思与改进模式实现
 * 
 * 核心：Generate → Reflect → Revise → Repeat
 */

class ReflectionAgent {
  constructor(options = {}) {
    this.maxIterations = options.maxIterations || 5;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
    this.criteria = options.criteria || this.defaultCriteria;
  }

  async execute(task) {
    if (this.verbose) {
      console.log(`[Reflection] 开始任务：${task}`);
    }
    
    // Generate: 初始输出
    let output = await this.generate(task);
    
    if (this.verbose) {
      console.log(`\n[Initial Output]\n${output}\n`);
    }
    
    // Reflect & Revise 循环
    for (let iteration = 1; iteration <= this.maxIterations; iteration++) {
      if (this.verbose) {
        console.log(`\n[Iteration ${iteration}/${this.maxIterations}]`);
      }
      
      // Reflect: 评估
      const feedback = await this.reflect(task, output);
      
      if (this.verbose) {
        console.log(`[Feedback]\n${feedback}\n`);
      }
      
      // 检查是否满足标准
      if (this.isSatisfactory(feedback)) {
        if (this.verbose) {
          console.log('[Complete] 输出质量满足要求');
        }
        break;
      }
      
      // Revise: 修改
      output = await this.revise(task, output, feedback);
      
      if (this.verbose) {
        console.log(`[Revised Output]\n${output}\n`);
      }
    }
    
    return output;
  }

  async generate(task) {
    const prompt = `
任务：${task}

请生成初始输出。

初始输出：`;
    
    return await this.llm.generate(prompt);
  }

  async reflect(task, output) {
    const prompt = `
任务：${task}

当前输出：
${output}

请评估这个输出，考虑以下标准：
${this.formatCriteria()}

反馈要求：
1. 指出具体问题（至少 3 个）
2. 说明为什么是问题
3. 提供改进建议

反馈：`;
    
    return await this.llm.generate(prompt);
  }

  async revise(task, output, feedback) {
    const prompt = `
任务：${task}

当前输出：
${output}

反馈：
${feedback}

请根据反馈修改输出，改进所有指出的问题。

修改后的输出：`;
    
    return await this.llm.generate(prompt);
  }

  isSatisfactory(feedback) {
    // 检查是否有严重问题
    const criticalKeywords = ['严重问题', '重大错误', '完全不符合', '无法接受'];
    const hasCriticalIssues = criticalKeywords.some(keyword => 
      feedback.includes(keyword)
    );
    
    // 如果没有严重问题，认为满足要求
    return !hasCriticalIssues;
  }

  formatCriteria() {
    return this.criteria.map((c, i) => `${i + 1}. ${c}`).join('\n');
  }

  defaultCriteria = [
    '准确性：信息是否正确、无误',
    '完整性：是否覆盖所有要点',
    '清晰性：表达是否清晰易懂',
    '逻辑性：推理是否严密、自洽',
    '相关性：是否紧扣任务要求'
  ];

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Generated output.';
    }
  };
}

module.exports = { ReflectionAgent };
