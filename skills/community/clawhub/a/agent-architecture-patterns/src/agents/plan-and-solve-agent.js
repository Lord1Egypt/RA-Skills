/**
 * Plan-and-Solve Agent - 规划与执行模式实现
 * 
 * 核心：Understand → Plan → Execute → Synthesize
 */

class PlanAndSolveAgent {
  constructor(options = {}) {
    this.maxSteps = options.maxSteps || 20;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async execute(task) {
    if (this.verbose) {
      console.log(`[Plan-and-Solve] 开始任务：${task}`);
    }
    
    // Phase 1: Understand
    const understanding = await this.understand(task);
    
    if (this.verbose) {
      console.log('\n[Understanding]');
      console.log(`  Goal: ${understanding.goal}`);
      console.log(`  Constraints: ${understanding.constraints.join(', ')}`);
      console.log(`  Success Criteria: ${understanding.successCriteria.join(', ')}\n`);
    }
    
    // Phase 2: Plan
    const plan = await this.plan(task, understanding);
    
    if (this.verbose) {
      console.log(`[Plan] Total ${plan.steps.length} steps`);
      plan.steps.forEach((step, i) => {
        console.log(`  ${i + 1}. ${step.description}`);
      });
      console.log();
    }
    
    // Phase 3: Execute
    const executionResults = await this.executePlan(task, plan);
    
    if (this.verbose) {
      console.log(`\n[Execution Complete] ${executionResults.completed}/${executionResults.total} steps`);
    }
    
    // Phase 4: Synthesize
    const finalResult = await this.synthesize(task, understanding, executionResults);
    
    if (this.verbose) {
      console.log(`\n[Final Result]\n${finalResult}`);
    }
    
    return finalResult;
  }

  async understand(task) {
    const prompt = `
任务：${task}

请分析这个任务：

1. **任务目标**：要达成什么？
2. **约束条件**：有哪些限制？（时间、资源、技术等）
3. **成功标准**：如何判断任务完成？

请以 JSON 格式返回：
{
  "goal": "任务目标",
  "constraints": ["约束 1", "约束 2"],
  "successCriteria": ["标准 1", "标准 2"]
}

分析结果：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      return {
        goal: task,
        constraints: [],
        successCriteria: ['Task completed']
      };
    }
  }

  async plan(task, understanding) {
    const prompt = `
任务：${task}

目标：${understanding.goal}

约束：${understanding.constraints.join(', ')}

成功标准：${understanding.successCriteria.join(', ')}

请制定详细的执行计划：

要求：
1. 将任务分解为具体的、可执行的步骤
2. 步骤之间可能有依赖关系
3. 每个步骤应该有清晰的完成标准
4. 步骤数量适中（5-15 步）

请以 JSON 格式返回：
{
  "steps": [
    {
      "id": 1,
      "description": "步骤描述",
      "dependencies": [],
      "expectedOutput": "预期输出"
    }
  ]
}

计划：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      return {
        steps: [{
          id: 1,
          description: task,
          dependencies: [],
          expectedOutput: 'Complete task'
        }]
      };
    }
  }

  async executePlan(task, plan) {
    const results = {
      total: plan.steps.length,
      completed: 0,
      failed: 0,
      stepResults: []
    };
    
    const completedSteps = new Set();
    
    for (let stepNum = 0; stepNum < plan.steps.length; stepNum++) {
      const executableStep = plan.steps.find(step => 
        !completedSteps.has(step.id) &&
        step.dependencies.every(depId => completedSteps.has(depId))
      );
      
      if (!executableStep) {
        break;
      }
      
      if (this.verbose) {
        console.log(`[Step ${executableStep.id}/${plan.steps.length}] ${executableStep.description}`);
      }
      
      const result = await this.executeStep(task, executableStep, results.stepResults);
      
      results.stepResults.push({
        stepId: executableStep.id,
        description: executableStep.description,
        success: result.success,
        output: result.output,
        error: result.error
      });
      
      if (result.success) {
        completedSteps.add(executableStep.id);
        results.completed++;
        
        if (this.verbose) {
          console.log('  ✅ Done\n');
        }
      } else {
        results.failed++;
        
        if (this.verbose) {
          console.log(`  ❌ Failed: ${result.error}\n`);
        }
      }
    }
    
    return results;
  }

  async executeStep(task, step, previousResults) {
    const context = previousResults.map(r => 
      `Step ${r.stepId}: ${r.output}`
    ).join('\n');
    
    const prompt = `
任务：${task}

当前步骤：${step.description}
预期输出：${step.expectedOutput}

之前的执行结果：
${context || '(None)'}

请执行当前步骤。

结果：`;
    
    try {
      const output = await this.llm.generate(prompt);
      return { success: true, output };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async synthesize(task, understanding, executionResults) {
    const resultsText = executionResults.stepResults.map(r => 
      `Step ${r.stepId}: ${r.success ? '✅' : '❌'} ${r.output || r.error}`
    ).join('\n');
    
    const prompt = `
任务：${task}

目标：${understanding.goal}

成功标准：${understanding.successCriteria.join(', ')}

执行结果：
${resultsText}

完成进度：${executionResults.completed}/${executionResults.total} steps

请整合所有执行结果，生成最终输出。

最终输出：`;
    
    return await this.llm.generate(prompt);
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Task completed.';
    }
  };
}

module.exports = { PlanAndSolveAgent };
