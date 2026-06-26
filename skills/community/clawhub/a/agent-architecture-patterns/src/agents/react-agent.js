/**
 * ReAct Agent - 单 Agent 架构模式实现
 * 
 * ReAct = Reasoning + Acting
 * 交替进行推理和行动，协同增强
 */

class ReActAgent {
  constructor(options = {}) {
    this.tools = options.tools || {};
    this.maxSteps = options.maxSteps || 10;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  /**
   * 执行任务
   * @param {string} task - 任务描述
   * @returns {Promise<string>} - 最终答案
   */
  async execute(task) {
    const history = [];
    
    if (this.verbose) {
      console.log(`[ReAct] 开始执行任务：${task}`);
    }
    
    for (let step = 0; step < this.maxSteps; step++) {
      if (this.verbose) {
        console.log(`\n[Step ${step + 1}/${this.maxSteps}]`);
      }
      
      // Step 1: Thought - 思考下一步
      const thought = await this.reason(task, history);
      if (this.verbose) {
        console.log(`[Thought] ${thought}`);
      }
      
      // Step 2: Action - 决定行动
      const action = await this.decideAction(thought, history);
      if (this.verbose) {
        console.log(`[Action] ${action.name}(${JSON.stringify(action.args)})`);
      }
      
      // Step 3: Observation - 执行并观察结果
      const observation = await this.observe(action);
      if (this.verbose) {
        console.log(`[Observation] ${observation}`);
      }
      
      // 记录历史
      history.push({ step: step + 1, thought, action, observation });
      
      // 判断是否完成
      if (this.isComplete(thought, observation)) {
        const answer = await this.finalize(task, history);
        if (this.verbose) {
          console.log(`\n[Answer] ${answer}`);
        }
        return answer;
      }
    }
    
    throw new Error(`Max steps (${this.maxSteps}) reached without completion`);
  }

  /**
   * 推理：思考下一步
   */
  async reason(task, history) {
    const context = this.buildContext(task, history);
    
    const prompt = `
当前任务：${task}

历史对话：
${this.formatHistory(history)}

请思考：
1. 当前已知什么信息？
2. 还需要什么信息？
3. 下一步应该做什么？

可用工具：
${this.listTools()}

思考：`;
    
    const response = await this.llm.generate(prompt);
    return response.trim();
  }

  /**
   * 决定行动：根据思考选择工具和参数
   */
  async decideAction(thought, history) {
    const prompt = `
基于以下思考，决定采取什么行动：
${thought}

可用工具：
${this.listTools()}

请以 JSON 格式返回行动（只返回 JSON，不要其他内容）：
{
  "name": "工具名称",
  "args": {
    "参数名": "参数值"
  }
}

行动：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      // 尝试解析 JSON
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      // 如果解析失败，尝试从文本中提取
      return this.extractActionFromText(response);
    }
  }

  /**
   * 观察：执行工具并返回结果
   */
  async observe(action) {
    const tool = this.tools[action.name];
    
    if (!tool) {
      return `Error: Unknown tool "${action.name}". Available tools: ${Object.keys(this.tools).join(', ')}`;
    }
    
    try {
      const result = await tool.execute(action.args);
      return result.toString();
    } catch (error) {
      return `Error: ${error.message}`;
    }
  }

  /**
   * 判断是否完成
   */
  isComplete(thought, observation) {
    const finishKeywords = [
      'finish',
      'answer is',
      '最终答案是',
      '完成任务',
      '可以给出答案',
      '不需要更多'
    ];
    
    const lowerThought = thought.toLowerCase();
    return finishKeywords.some(keyword => lowerThought.includes(keyword));
  }

  /**
   * 生成最终答案
   */
  async finalize(task, history) {
    const prompt = `
任务：${task}

完整历史：
${this.formatHistory(history)}

请给出最终答案（简洁、准确、完整）：

最终答案：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 构建上下文
   */
  buildContext(task, history) {
    return { task, history };
  }

  /**
   * 列出可用工具
   */
  listTools() {
    return Object.entries(this.tools)
      .map(([name, tool]) => `- ${name}: ${tool.description}`)
      .join('\n');
  }

  /**
   * 格式化历史
   */
  formatHistory(history) {
    if (history.length === 0) {
      return '（无历史记录）';
    }
    
    return history.map(h => 
      `步骤 ${h.step}:\n  思考：${h.thought}\n  行动：${h.action.name}(${JSON.stringify(h.action.args)})\n  观察：${h.observation}`
    ).join('\n\n');
  }

  /**
   * 从文本中提取行动（备用方案）
   */
  extractActionFromText(text) {
    // 尝试提取工具名称和参数
    const toolMatch = text.match(/(?:使用 | 调用 | use|call)\s*(\w+)/i);
    const toolName = toolMatch ? toolMatch[1] : Object.keys(this.tools)[0];
    
    // 尝试提取参数
    const args = {};
    const paramMatches = text.matchAll(/(\w+)\s*[=:]\s*["']?([^"'\n,}]+)["']?/g);
    for (const match of paramMatches) {
      args[match[1]] = match[2].trim();
    }
    
    return { name: toolName, args };
  }

  /**
   * 默认 LLM 实现（需要替换为实际 API）
   */
  defaultLLM = {
    generate: async (prompt) => {
      // 这里应该调用实际的 LLM API（OpenAI/Claude/Qwen 等）
      // 示例中返回占位符
      console.warn('[Warning] Using default LLM. Please provide a real LLM implementation.');
      return 'I need more information to complete this task.';
    }
  };
}

module.exports = { ReActAgent };
