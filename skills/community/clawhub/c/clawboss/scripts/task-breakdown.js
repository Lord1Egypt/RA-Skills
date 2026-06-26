/**
 * Task Breakdown - GROW Model Implementation
 *
 * Guides users through goal setting using professional coaching questions.
 * Uses session-based multi-turn dialogue via state-manager sessions.
 */

const stateManager = require('./state-manager');
const questions = require('./coaching-questions');

/**
 * Main GROW session handler
 *
 * - If an active session exists, delegate to processAnswer (resume).
 * - Otherwise start a new GROW session.
 */
async function startGROWSession(userInput = '') {
  try {
    const state = stateManager.loadState();
    const session = stateManager.getActiveSession(state);

    // Resume existing session
    if (session) {
      if (userInput && userInput.trim().length > 0) {
        return await processAnswer(session.growPhase, userInput);
      }
      // No input — remind the user where they are
      return {
        phase: session.growPhase,
        question: questions.getGROWQuestion(session.growPhase),
        instruction: `我们正在进行 GROW 对话（阶段：${session.growPhase}）。请继续回答上面的问题。`
      };
    }

    // No active session — check if user provided initial goal
    if (!userInput || userInput.trim().length === 0) {
      return {
        phase: 'goal-discovery',
        question: questions.getGROWQuestion('goal'),
        instruction: '让我们开始吧！'
      };
    }

    // Start a full session with the provided goal
    return await conductFullSession(userInput, state);
  } catch (error) {
    console.error('startGROWSession error:', error);
    return {
      error: '启动 GROW 对话时出现错误，请稍后重试。'
    };
  }
}

/**
 * Conduct a full GROW session — creates the goal and starts multi-turn dialogue
 */
async function conductFullSession(initialGoal, state) {
  const session = {
    goal: {
      title: extractGoalTitle(initialGoal),
      description: initialGoal,
      motivation: '',
      successCriteria: []
    },
    reality: {
      currentState: '',
      resources: [],
      obstacles: []
    },
    options: {
      approaches: [],
      chosenApproach: ''
    },
    will: {
      firstStep: '',
      timeline: '',
      commitment: 0
    }
  };

  const response = buildGROWResponse(session);

  // Create goal data
  const goalData = {
    title: session.goal.title,
    description: session.goal.description,
    motivation: '待补充 - 通过后续对话完善',
    targetDate: null,
    priority: 'medium'
  };

  const { state: updatedState, goalId } = stateManager.addGoal(state, goalData);

  // Create task file
  const taskContent = stateManager.createTaskFile(goalData);
  const goal = updatedState.goals.find(g => g.id === goalId);
  stateManager.saveTaskFile(goal.taskFile, taskContent);

  // Start session tracking
  stateManager.startSession(updatedState, goalId);
  stateManager.saveState(updatedState);

  return {
    success: true,
    goalId,
    taskPath: goal.taskFile,
    response: response,
    nextSteps: [
      '我已经为你创建了任务追踪文件',
      '让我们继续完善细节...',
      '',
      '**为什么这个目标对你重要？**',
      '达成后你的生活会有什么不同？'
    ].join('\n')
  };
}

/**
 * Extract goal title from user input
 */
function extractGoalTitle(input) {
  // Simple extraction - take first sentence or up to 50 chars
  let title = input.split(/[。.！!？?]/)[0];
  if (title.length > 50) {
    title = title.substring(0, 50) + '...';
  }
  return title.trim();
}

/**
 * Build GROW response message
 */
function buildGROWResponse(session) {
  return `
# 🎯 目标设定 - GROW 框架

很好！让我们用 GROW 模型来规划这个目标。

## Goal (目标)

**你想达成什么：**
${session.goal.title}

接下来我会问你一些问题，帮你把目标变得更清晰可执行。

---

### 第一个问题：

**为什么这个目标对你重要？**

想象一下达成后的场景：
- 你的生活会有什么不同？
- 你会有什么感受？
- 这会带来什么长期价值？

（请详细告诉我，这能帮助你在困难时保持动力）
  `.trim();
}

/**
 * Process user's answer to a GROW question (session-aware)
 */
async function processAnswer(phase, answer) {
  try {
    const state = stateManager.loadState();
    const session = stateManager.getActiveSession(state);

    // Determine which goal to work with
    let currentGoal;
    if (session && session.goalId) {
      currentGoal = state.goals.find(g => g.id === session.goalId);
    }

    // Fallback to first active goal if session has no goal or goal not found
    if (!currentGoal) {
      const activeGoals = stateManager.getActiveGoals(state);
      if (activeGoals.length === 0) {
        return { error: '没有找到活跃的目标。请先创建一个目标。' };
      }
      currentGoal = activeGoals[0];
    }

    // Determine current phase from session (preferred) or argument
    const currentPhase = (session && session.growPhase) ? session.growPhase : phase;

    // Load task file
    const taskContent = stateManager.loadTaskFile(currentGoal.taskFile);

    // Update task file based on phase
    let updatedContent = updateTaskFileWithAnswer(taskContent, currentPhase, answer);

    // Save updated task file
    stateManager.saveTaskFile(currentGoal.taskFile, updatedContent);

    // Advance session
    stateManager.advanceSession(state);
    const nextPhase = state.activeSession ? state.activeSession.growPhase : 'complete';

    if (nextPhase === 'complete') {
      stateManager.endSession(state);
      stateManager.saveState(state);

      // Check for emotion in the last answer
      let emotionPrefix = '';
      if (questions.detectEmotion) {
        const detected = questions.detectEmotion(answer);
        if (detected && detected.confidence >= 0.5) {
          emotionPrefix = detected.response + '\n\n';
        }
      }

      return {
        success: true,
        phase: 'complete',
        response: emotionPrefix + buildCompletionMessage(currentGoal),
        nextSteps: '目标设定完成！我会在每天早晚检查你的进度，用coaching方式支持你。'
      };
    }

    stateManager.saveState(state);

    // Check for emotion in the answer
    let emotionPrefix = '';
    if (questions.detectEmotion) {
      const detected = questions.detectEmotion(answer);
      if (detected && detected.confidence >= 0.5) {
        emotionPrefix = detected.response + '\n\n';
      }
    }

    return {
      success: true,
      phase: nextPhase,
      question: questions.getGROWQuestion(nextPhase),
      response: emotionPrefix + buildTransitionMessage(currentPhase, nextPhase)
    };
  } catch (error) {
    console.error('processAnswer error:', error);
    return {
      error: '处理回答时出现错误，请稍后重试。'
    };
  }
}

/**
 * Update task file with user's answer
 */
function updateTaskFileWithAnswer(content, phase, answer) {
  if (!content) return answer;

  if (phase === 'goal') {
    // Update motivation section
    content = content.replace(
      /### 为什么重要？\n待补充/,
      `### 为什么重要？\n${answer}`
    );
  } else if (phase === 'reality') {
    // Update current state
    content = content.replace(
      /### 当前进展\n待评估/,
      `### 当前进展\n${answer}`
    );
  } else if (phase === 'options') {
    // Update action plan
    content = content.replace(
      /### 第一阶段\n- \[ \] 步骤 1/,
      `### 第一阶段\n${answer}`
    );
  } else if (phase === 'will') {
    // Update first action
    content = `${content}\n\n### ✅ 第一步行动\n${answer}\n`;
  }

  return content;
}

/**
 * Build transition message between phases
 */
function buildTransitionMessage(fromPhase, toPhase) {
  const transitions = {
    'goal-reality': '很好！我理解这个目标对你的重要性了。\n\n现在让我们看看**现状**：',
    'reality-options': '了解了。我看到了你的起点和挑战。\n\n接下来我们探索**可能的路径**：',
    'options-will': '不错，有几个方向可以尝试。\n\n最重要的是**开始行动**：'
  };

  const key = `${fromPhase}-${toPhase}`;
  return transitions[key] || '继续...';
}

/**
 * Build completion message
 */
function buildCompletionMessage(goal) {
  return `
# ✅ 目标设定完成！

**目标：** ${goal.title}

我已经帮你建立了完整的追踪系统：

📁 **任务文件：** \`${goal.taskFile}\`
- 包含目标、现状、行动计划
- 记录每日进展
- 积累经验教训

💓 **自动检查：**
- 早上：回顾今日计划，设定意图
- 晚上：进度检查，coaching 反馈
- 每周：深度复盘，模式识别

🎯 **我的角色：**
我不是监工，是教练。我会：
- 用问题引导，而非命令
- 关注学习，而非批评
- 根据你的状态调整支持强度

---

**现在，让我们开始吧！**

第一步是什么？什么时候开始？
  `.trim();
}

/**
 * Quick start - simplified flow for testing
 */
async function quickStart(goalTitle) {
  try {
    const state = stateManager.loadState();

    const goalData = {
      title: goalTitle,
      description: goalTitle,
      motivation: '待通过对话完善',
      targetDate: null,
      priority: 'medium'
    };

    const { state: updatedState, goalId } = stateManager.addGoal(state, goalData);

    const taskContent = stateManager.createTaskFile(goalData);
    const goal = updatedState.goals.find(g => g.id === goalId);
    stateManager.saveTaskFile(goal.taskFile, taskContent);

    // Start a session for the new goal
    stateManager.startSession(updatedState, goalId);
    stateManager.saveState(updatedState);

    return {
      success: true,
      goalId,
      message: `✅ 目标 "${goalTitle}" 已创建！\n\n让我们通过几个问题来完善它...\n\n**为什么这个目标对你重要？**`
    };
  } catch (error) {
    console.error('quickStart error:', error);
    return {
      success: false,
      message: '创建目标时出现错误，请稍后重试。'
    };
  }
}

/**
 * Break down a goal into milestones and update the task file
 *
 * @param {string} goalId - Target goal ID
 * @param {Array<{title:string, targetDate?:string, description?:string}>} milestones
 * @returns {object} result
 */
async function breakdownGoal(goalId, milestones) {
  try {
    const state = stateManager.loadState();
    const goal = state.goals.find(g => g.id === goalId);
    if (!goal) return { error: '目标不存在' };

    // Store milestones in state
    const { error } = stateManager.addMilestones(state, goalId, milestones);
    if (error) return { error };

    // Update task file with milestone plan
    let content = stateManager.loadTaskFile(goal.taskFile);
    if (content) {
      const milestoneMd = milestones.map((ms, i) => {
        const datePart = ms.targetDate ? ` (截止: ${ms.targetDate})` : '';
        const descPart = ms.description ? `\n  ${ms.description}` : '';
        return `- [ ] **阶段 ${i + 1}：${ms.title}**${datePart}${descPart}`;
      }).join('\n');

      // Replace the default placeholder steps or append after action plan header
      if (content.includes('- [ ] 步骤 2')) {
        content = content.replace(
          /### 第一阶段\n- \[ \] 步骤 1\n- \[ \] 步骤 2/,
          `### 里程碑计划\n${milestoneMd}`
        );
      } else {
        content = content.replace(
          /(## 🛤️ 行动计划 \(Options → Will\))/,
          `$1\n\n### 里程碑计划\n${milestoneMd}`
        );
      }

      stateManager.saveTaskFile(goal.taskFile, content);
    }

    stateManager.saveState(state);

    // Build response
    const plan = milestones.map((ms, i) => {
      const datePart = ms.targetDate ? ` — 截止 ${ms.targetDate}` : '';
      return `${i + 1}. **${ms.title}**${datePart}`;
    }).join('\n');

    return {
      success: true,
      goalId,
      message: `✅ 已为「${goal.title}」制定 ${milestones.length} 个里程碑：\n\n${plan}\n\n我会在每个里程碑临近和到期时主动提醒你。`
    };
  } catch (error) {
    console.error('breakdownGoal error:', error);
    return { error: '拆解任务时出现错误，请稍后重试。' };
  }
}

module.exports = {
  startGROWSession,
  processAnswer,
  quickStart,
  breakdownGoal
};
