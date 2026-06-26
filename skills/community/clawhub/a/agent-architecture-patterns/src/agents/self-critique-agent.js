/**
 * Self-Critique Agent - 自我批评与修正模式实现
 * 
 * 核心：Generate → Critique (找错) → Fix → Repeat
 */

class SelfCritiqueAgent {
  constructor(options = {}) {
    this.maxIterations = options.maxIterations || 3;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
    this.errorTypes = options.errorTypes || this.defaultErrorTypes;
  }

  async execute(task) {
    if (this.verbose) {
      console.log(`[Self-Critique] 开始任务：${task}`);
    }
    
    // Generate: 初始输出
    let output = await this.generate(task);
    
    if (this.verbose) {
      console.log(`\n[Initial Output]\n${output}\n`);
    }
    
    // Critique & Fix 循环
    for (let iteration = 1; iteration <= this.maxIterations; iteration++) {
      if (this.verbose) {
        console.log(`\n[Iteration ${iteration}/${this.maxIterations}]`);
      }
      
      // Critique: 结构化批评
      const critique = await this.critique(task, output);
      
      if (this.verbose) {
        console.log(`[Critique]\n${JSON.stringify(critique, null, 2)}\n`);
      }
      
      // 如果没有错误，结束
      if (!critique.errors || critique.errors.length === 0) {
        if (this.verbose) {
          console.log('[Complete] 未发现错误');
        }
        break;
      }
      
      // Fix: 修正错误
      output = await this.fix(task, output, critique);
      
      if (this.verbose) {
        console.log(`[Fixed Output]\n${output}\n`);
      }
    }
    
    return output;
  }

  async generate(task) {
    const prompt = `
任务：${task}

请生成初始答案。

答案：`;
    
    return await this.llm.generate(prompt);
  }

  async critique(task, output) {
    const prompt = `
任务：${task}

待检查的输出：
${output}

请按照以下错误类型进行系统检查：

${this.formatErrorTypes()}

对于每种错误类型：
1. 仔细检查是否存在此类错误
2. 如果存在，明确指出错误位置和内容
3. 说明为什么这是错误
4. 提供正确的信息或建议

请以 JSON 格式返回检查结果：
{
  "errors": [
    {
      "type": "错误类型",
      "location": "错误位置",
      "description": "错误描述",
      "reason": "为什么这是错误",
      "suggestion": "修正建议"
    }
  ],
  "summary": "总体评价"
}

检查结果：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      console.warn('Failed to parse critique, assuming no errors');
      return { errors: [], summary: '检查完成' };
    }
  }

  async fix(task, output, critique) {
    const errorsText = critique.errors.map((e, i) => 
      `${i + 1}. [${e.type}] ${e.location}: ${e.description}\n   修正建议：${e.suggestion}`
    ).join('\n');
    
    const prompt = `
任务：${task}

原始输出：
${output}

发现的错误：
${errorsText}

请修正所有错误，生成改进后的版本。

要求：
1. 逐一修正每个错误
2. 保持原有的正确信息
3. 不要引入新错误
4. 保持格式一致

修正后的输出：`;
    
    return await this.llm.generate(prompt);
  }

  formatErrorTypes() {
    return this.errorTypes.map((et, i) => 
      `${i + 1}. **${et.name}**: ${et.description}\n   检查要点：${et.checkpoints.join('; ')}`
    ).join('\n\n');
  }

  defaultErrorTypes = [
    {
      name: '事实错误',
      description: '信息是否真实、准确、可验证',
      checkpoints: ['数据准确性', '引用真实性', '无幻觉']
    },
    {
      name: '逻辑错误',
      description: '推理是否严密、自洽',
      checkpoints: ['前提成立', '推理严密', '无矛盾']
    },
    {
      name: '计算错误',
      description: '数学计算、统计是否正确',
      checkpoints: ['加减乘除', '百分比', '单位换算']
    },
    {
      name: '遗漏错误',
      description: '是否缺少关键信息',
      checkpoints: ['回答问题', '背景信息', '限制条件']
    }
  ];

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Generated output.';
    }
  };
}

module.exports = { SelfCritiqueAgent };
