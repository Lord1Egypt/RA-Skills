/**
 * Manager-Worker Agent - 多 Agent 协作模式实现
 * 
 * 主从模式：1 个 Manager 协调多个 Worker
 */

class ManagerAgent {
  constructor(workers, options = {}) {
    this.workers = workers;
    this.maxRetries = options.maxRetries || 3;
    this.timeout = options.timeout || 30000;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  /**
   * 协调任务执行
   * @param {string} task - 任务描述
   * @returns {Promise<string>} - 最终结果
   */
  async coordinate(task) {
    if (this.verbose) {
      console.log(`[Manager] 接收任务：${task}`);
    }
    
    // Step 1: 任务分解
    const subtasks = await this.decompose(task);
    if (this.verbose) {
      console.log(`[Manager] 分解为 ${subtasks.length} 个子任务`);
      subtasks.forEach((st, i) => {
        console.log(`  ${i + 1}. ${st.description}`);
      });
    }
    
    // Step 2: 任务分配
    const assignments = this.assign(subtasks);
    if (this.verbose) {
      console.log(`[Manager] 分配任务给 Worker`);
    }
    
    // Step 3: 并行执行
    const results = await this.executeParallel(assignments);
    if (this.verbose) {
      console.log(`[Manager] 收到 ${results.length} 个结果`);
    }
    
    // Step 4: 结果整合
    const finalResult = await this.integrate(task, results);
    if (this.verbose) {
      console.log(`[Manager] 任务完成`);
    }
    
    return finalResult;
  }

  /**
   * 任务分解
   */
  async decompose(task) {
    const prompt = `
将以下任务分解为独立的子任务：
${task}

要求：
1. 每个子任务应该是独立的（可并行执行）
2. 子任务数量适中（3-10 个）
3. 明确每个子任务的目标
4. 识别每个子任务需要的技能

请以 JSON 数组格式返回（只返回 JSON）：
[
  {
    "id": "task-1",
    "description": "子任务描述",
    "requiredSkills": ["技能 1", "技能 2"]
  }
]

子任务列表：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      console.warn('Failed to parse subtasks, using fallback');
      // 降级方案：返回单个子任务
      return [{
        id: 'task-1',
        description: task,
        requiredSkills: []
      }];
    }
  }

  /**
   * 任务分配
   */
  assign(subtasks) {
    const assignments = new Map();
    
    for (const subtask of subtasks) {
      const worker = this.selectWorker(subtask);
      
      if (!assignments.has(worker.id)) {
        assignments.set(worker.id, []);
      }
      assignments.get(worker.id).push(subtask);
      
      if (this.verbose) {
        console.log(`  ${subtask.description} → ${worker.id}`);
      }
    }
    
    return assignments;
  }

  /**
   * 选择最合适的 Worker
   */
  selectWorker(subtask) {
    const requiredSkills = subtask.requiredSkills || [];
    
    let bestWorker = null;
    let bestScore = -1;
    
    for (const worker of this.workers) {
      const score = this.calculateMatchScore(worker, requiredSkills);
      if (score > bestScore) {
        bestScore = score;
        bestWorker = worker;
      }
    }
    
    return bestWorker || this.workers[0];
  }

  /**
   * 计算技能匹配分数
   */
  calculateMatchScore(worker, requiredSkills) {
    if (requiredSkills.length === 0) {
      return 0.5; // 无技能要求，默认分数
    }
    
    const workerSkills = new Set(worker.skills || []);
    const matchedSkills = requiredSkills.filter(skill => 
      workerSkills.has(skill)
    );
    
    return matchedSkills.length / requiredSkills.length;
  }

  /**
   * 并行执行
   */
  async executeParallel(assignments) {
    const promises = [];
    
    for (const [workerId, subtasks] of assignments) {
      const worker = this.workers.find(w => w.id === workerId);
      
      if (!worker) {
        console.warn(`Worker ${workerId} not found`);
        continue;
      }
      
      const workerPromise = Promise.all(
        subtasks.map(subtask => this.executeWithRetry(worker, subtask))
      );
      
      promises.push(workerPromise);
    }
    
    const results = await Promise.all(promises);
    return results.flat();
  }

  /**
   * 带重试的执行
   */
  async executeWithRetry(worker, subtask) {
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        const result = await Promise.race([
          worker.execute(subtask),
          this.timeoutPromise(this.timeout)
        ]);
        
        if (this.verbose) {
          console.log(`[Worker ${worker.id}] ✅ ${subtask.description}`);
        }
        
        return {
          taskId: subtask.id,
          success: true,
          result,
          worker: worker.id
        };
      } catch (error) {
        if (this.verbose) {
          console.warn(`[Worker ${worker.id}] ❌ 尝试 ${attempt} 失败：${error.message}`);
        }
        
        if (attempt === this.maxRetries) {
          return {
            taskId: subtask.id,
            success: false,
            error: error.message,
            worker: worker.id
          };
        }
        
        // 指数退避
        await this.sleep(1000 * Math.pow(2, attempt));
      }
    }
  }

  /**
   * 超时 Promise
   */
  timeoutPromise(timeout) {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Timeout')), timeout);
    });
  }

  /**
   * 睡眠
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * 整合结果
   */
  async integrate(task, results) {
    const successfulResults = results.filter(r => r.success);
    const failedResults = results.filter(r => !r.success);
    
    const prompt = `
原始任务：${task}

成功执行的结果 (${successfulResults.length}个):
${JSON.stringify(successfulResults.map(r => ({
  taskId: r.taskId,
  result: r.result
})), null, 2)}

失败的结果 (${failedResults.length}个):
${JSON.stringify(failedResults, null, 2)}

请整合所有成功结果，生成最终答案。
如果有失败的任务，说明影响。

要求：
1. 结构清晰
2. 信息完整
3. 语言简洁

最终答案：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 默认 LLM 实现
   */
  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM. Please provide a real LLM implementation.');
      return 'Task completed.';
    }
  };
}

/**
 * Worker Agent
 */
class WorkerAgent {
  constructor(id, skills, capabilities) {
    this.id = id;
    this.skills = skills || [];
    this.capabilities = capabilities || {};
    this.llm = capabilities.llm || this.defaultLLM;
  }

  /**
   * 执行子任务
   */
  async execute(subtask) {
    if (this.verbose) {
      console.log(`[Worker ${this.id}] 执行：${subtask.description}`);
    }
    
    // 根据能力选择执行方式
    if (this.capabilities.codeReview) {
      return await this.reviewCode(subtask);
    } else if (this.capabilities.webSearch) {
      return await this.searchWeb(subtask);
    } else if (this.capabilities.dataAnalysis) {
      return await this.analyzeData(subtask);
    } else {
      return await this.genericExecute(subtask);
    }
  }

  /**
   * 代码审查
   */
  async reviewCode(subtask) {
    const code = subtask.code || '';
    
    const prompt = `
审查以下代码：
${code}

关注点：
- 代码质量
- 潜在 bug
- 性能问题
- 安全漏洞
- 最佳实践

审查结果：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 网络搜索
   */
  async searchWeb(subtask) {
    const query = subtask.query || subtask.description;
    
    // 实际实现调用搜索 API
    const prompt = `
搜索以下信息：
${query}

提供准确、相关的信息：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 数据分析
   */
  async analyzeData(subtask) {
    const data = subtask.data || {};
    
    const prompt = `
分析以下数据：
${JSON.stringify(data, null, 2)}

提供：
1. 数据摘要
2. 关键发现
3. 趋势分析
4. 建议

分析结果：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 通用执行
   */
  async genericExecute(subtask) {
    const prompt = `
执行以下任务：
${subtask.description}

结果：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 默认 LLM
   */
  defaultLLM = {
    generate: async (prompt) => {
      console.warn(`[Worker ${this.id}] Using default LLM.`);
      return 'Task completed.';
    }
  };
}

module.exports = { ManagerAgent, WorkerAgent };
