import { resolve } from "path";
import { DATA_DIR, PATTERNS_PATH, PLANS_PATH, WORKFLOWS_PATH, loadJson, debouncedSave } from "./persistence.ts";
import { spawnCLI } from "./cli.ts";
import { addMemory } from "./memory.ts";
import { notifySoulActivity } from "./notify.ts";
import { extractJSON } from "./utils.ts";
const taskState = {
  pendingTasks: /* @__PURE__ */ new Map(),
  requestPatterns: [],
  activePlans: [],
  workflows: []
};
function initTasks() {
  taskState.requestPatterns = loadJson(PATTERNS_PATH, []);
  taskState.activePlans = loadJson(PLANS_PATH, []);
  taskState.workflows = loadJson(WORKFLOWS_PATH, []);
  skills = loadJson(SKILLS_PATH, []);
  if (skills.length > 0) {
    console.log(`[cc-soul][skills] loaded ${skills.length} skills from disk`);
  }
}
function detectActionIntent(userMsg, botResponse) {
  if (botResponse.includes("```") && botResponse.length > 200) return true;
  if (/\d+\.\s/.test(botResponse) && ["\u521B\u5EFA", "\u4FEE\u6539", "\u5199\u5165", "\u6267\u884C", "\u5B89\u88C5", "\u90E8\u7F72"].some((w) => botResponse.includes(w))) return true;
  if (["\u5E2E\u6211\u505A", "\u5E2E\u6211\u5199", "\u5E2E\u6211\u6539", "\u5E2E\u6211\u521B\u5EFA", "\u5E2E\u6211\u90E8\u7F72"].some((w) => userMsg.includes(w))) return true;
  return false;
}
function detectAndDelegateTask(userMsg, botResponse, event) {
  if (!detectActionIntent(userMsg, botResponse)) return;
  const chatId = event.context?.conversationId || event.sessionKey || "default";
  const taskDoc = [
    "# \u4EFB\u52A1",
    `\u7528\u6237\u9700\u6C42: ${userMsg.slice(0, 500)}`,
    "",
    "# \u65B9\u6848",
    botResponse.slice(0, 1500),
    "",
    "# \u8981\u6C42",
    "\u6309\u65B9\u6848\u6267\u884C\uFF0C\u5B8C\u6210\u540E\u7B80\u8981\u62A5\u544A\u7ED3\u679C\u3002"
  ].join("\n");
  taskState.pendingTasks.set(chatId, {
    taskDoc,
    userPrompt: userMsg.slice(0, 200),
    ts: Date.now()
  });
  console.log(`[cc-soul][task] \u68C0\u6D4B\u5230\u4EFB\u52A1\u610F\u56FE\uFF0C\u7B49\u5F85\u786E\u8BA4: ${userMsg.slice(0, 40)}`);
}
function checkTaskConfirmation(msg, chatId) {
  const task = taskState.pendingTasks.get(chatId);
  if (!task) return false;
  if (Date.now() - task.ts > 6e5) {
    taskState.pendingTasks.delete(chatId);
    return false;
  }
  const m = msg.trim().toLowerCase();
  if (["\u505A", "\u6267\u884C", "\u786E\u8BA4", "\u5F00\u59CB", "go", "ok", "\u597D", "\u53EF\u4EE5", "\u641E", "\u5E72", "\u884C"].includes(m)) {
    executeCLITask(chatId, task);
    return true;
  }
  if (["\u7B97\u4E86", "\u4E0D\u7528", "\u53D6\u6D88", "\u522B\u505A"].some((w) => m.includes(w))) {
    taskState.pendingTasks.delete(chatId);
    console.log(`[cc-soul][task] \u7528\u6237\u53D6\u6D88\u4EFB\u52A1`);
    return false;
  }
  return false;
}
function executeCLITask(chatId, task, stats, saveStats) {
  taskState.pendingTasks.delete(chatId);
  console.log(`[cc-soul][task] \u5F00\u59CB\u6267\u884C: ${task.userPrompt.slice(0, 40)}`);
  spawnCLI(task.taskDoc, (output) => {
    const result = output.slice(0, 2e3);
    console.log(`[cc-soul][task] CLI \u5B8C\u6210: ${result.slice(0, 80)}`);
    addMemory(`[\u5DF2\u5B8C\u6210\u4EFB\u52A1] ${task.userPrompt.slice(0, 60)} \u2192 ${result.slice(0, 100)}`, "task");
    if (stats && saveStats) {
      stats.tasks++;
      saveStats();
    }
  }, 12e4, `task-${task.userPrompt.slice(0, 20)}`);
}
function trackRequestPattern(msg) {
  if (msg.length < 10) return;
  const words = (msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
  if (words.length < 2) return;
  for (const pattern of taskState.requestPatterns) {
    const overlap = pattern.keywords.filter((k) => words.includes(k)).length;
    const similarity = overlap / Math.max(pattern.keywords.length, words.length);
    if (similarity >= 0.4) {
      pattern.count++;
      pattern.lastSeen = Date.now();
      pattern.example = msg.slice(0, 200);
      debouncedSave(PATTERNS_PATH, taskState.requestPatterns);
      return;
    }
  }
  taskState.requestPatterns.push({
    keywords: words.slice(0, 10),
    count: 1,
    lastSeen: Date.now(),
    example: msg.slice(0, 200),
    skillCreated: false
  });
  if (taskState.requestPatterns.length > 100) {
    taskState.requestPatterns.sort((a, b) => b.count - a.count);
    taskState.requestPatterns = taskState.requestPatterns.slice(0, 80);
  }
  debouncedSave(PATTERNS_PATH, taskState.requestPatterns);
}
function detectSkillOpportunity(msg) {
  for (const pattern of taskState.requestPatterns) {
    if (pattern.skillCreated) continue;
    if (pattern.count < 3) continue;
    const words = (msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map((w) => w.toLowerCase());
    const overlap = pattern.keywords.filter((k) => words.includes(k)).length;
    if (overlap < 2) continue;
    pattern.skillCreated = true;
    debouncedSave(PATTERNS_PATH, taskState.requestPatterns);
    return `[\u6280\u80FD\u5EFA\u8BAE] \u4F60\u5DF2\u7ECF\u7B2C${pattern.count}\u6B21\u5904\u7406\u7C7B\u4F3C\u8BF7\u6C42\u4E86\uFF08\u5982: "${pattern.example.slice(0, 40)}"\uFF09\u3002\u5EFA\u8BAE\u521B\u5EFA\u4E00\u4E2A\u53EF\u590D\u7528\u7684\u5DE5\u5177/\u811A\u672C\u6765\u81EA\u52A8\u5316\u8FD9\u7C7B\u64CD\u4F5C\uFF0C\u4E0B\u6B21\u76F4\u63A5\u7528\u3002`;
  }
  return null;
}
function autoCreateSkill(description, example) {
  const prompt = [
    `\u8BF7\u4E3A\u4EE5\u4E0B\u91CD\u590D\u6027\u4EFB\u52A1\u521B\u5EFA\u4E00\u4E2A bash \u811A\u672C\u6216 Python \u5DE5\u5177\u3002`,
    ``,
    `\u4EFB\u52A1\u63CF\u8FF0: ${description}`,
    `\u793A\u4F8B\u8BF7\u6C42: ${example}`,
    ``,
    `\u8981\u6C42:`,
    `1. \u521B\u5EFA\u53EF\u6267\u884C\u811A\u672C`,
    `2. \u4FDD\u5B58\u5230 ~/.openclaw/skills/ \u76EE\u5F55`,
    `3. \u6DFB\u52A0\u4F7F\u7528\u8BF4\u660E`
  ].join("\n");
  spawnCLI(prompt, (output) => {
    if (output) {
      addMemory(`[\u6280\u80FD\u521B\u5EFA] ${description.slice(0, 60)} \u2192 ${output.slice(0, 100)}`, "task");
      console.log(`[cc-soul][skill] created: ${description.slice(0, 40)}`);
      notifySoulActivity(`\u{1F527} \u81EA\u521B\u6280\u80FD: ${description.slice(0, 40)}`).catch(() => {
      });
    }
  }, 6e4, `skill-create-${description.slice(0, 20)}`);
}
function getActivePlanHint() {
  const active = taskState.activePlans.filter((p) => Array.isArray(p.steps) && p.steps.some((s) => s.status === "pending" || s.status === "running"));
  if (active.length === 0) return "";
  const latest = active[active.length - 1];
  const next = latest.steps.find((s) => s.status === "pending");
  if (!next) return "";
  return `[\u8FDB\u884C\u4E2D\u7684\u8BA1\u5212] ${latest.goal.slice(0, 40)} \u2192 \u4E0B\u4E00\u6B65: ${next.desc}`;
}
function createWorkflow(name, trigger, steps) {
  if (taskState.workflows.some((w) => w.name === name)) return;
  taskState.workflows.push({ name, trigger, steps, lastRun: 0, runCount: 0 });
  if (taskState.workflows.length > 30) taskState.workflows = taskState.workflows.slice(-25);
  debouncedSave(WORKFLOWS_PATH, taskState.workflows);
  console.log(`[cc-soul][workflow] created: ${name} (${steps.length} steps)`);
  notifySoulActivity(`\u2699\uFE0F \u65B0\u5DE5\u4F5C\u6D41: ${name} (${steps.length}\u6B65)`).catch(() => {
  });
}
function executeWorkflow(wf) {
  wf.lastRun = Date.now();
  wf.runCount++;
  debouncedSave(WORKFLOWS_PATH, taskState.workflows);
  let stepIdx = 0;
  function runNextStep() {
    if (stepIdx >= wf.steps.length) {
      console.log(`[cc-soul][workflow] ${wf.name} completed (${wf.steps.length} steps)`);
      notifySoulActivity(`\u2705 \u5DE5\u4F5C\u6D41\u5B8C\u6210: ${wf.name}`).catch(() => {
      });
      addMemory(`[\u5DE5\u4F5C\u6D41\u5B8C\u6210] ${wf.name}`, "task");
      return;
    }
    const step = wf.steps[stepIdx];
    console.log(`[cc-soul][workflow] ${wf.name} step ${stepIdx + 1}/${wf.steps.length}: ${step.slice(0, 40)}`);
    spawnCLI(step, (output) => {
      addMemory(`[\u5DE5\u4F5C\u6D41\u6B65\u9AA4] ${wf.name} #${stepIdx + 1}: ${output.slice(0, 80)}`, "task");
      stepIdx++;
      setTimeout(runNextStep, 2e3);
    });
  }
  runNextStep();
}
function detectWorkflowTrigger(msg) {
  for (const wf of taskState.workflows) {
    const triggerWords = wf.trigger.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || [];
    const msgWords = msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || [];
    const overlap = triggerWords.filter((w) => msgWords.some((m) => m.toLowerCase() === w.toLowerCase())).length;
    if (overlap >= 2) return wf;
  }
  return null;
}
const SKILLS_PATH = resolve(DATA_DIR, "skills.json");
let skills = loadJson(SKILLS_PATH, []);
function saveSkills() {
  debouncedSave(SKILLS_PATH, skills);
}
function saveSkill(name, description, solution, keywords) {
  if (skills.some((s) => s.name === name)) return;
  skills.push({
    name,
    description,
    solution: solution.slice(0, 2e3),
    keywords: keywords.map((k) => k.toLowerCase()),
    verified: false,
    usedCount: 0,
    createdAt: Date.now(),
    lastUsed: 0
  });
  if (skills.length > 100) {
    skills.sort((a, b) => b.usedCount - a.usedCount);
    skills = skills.slice(0, 80);
  }
  saveSkills();
  console.log(`[cc-soul][skills] saved: ${name}`);
}
function findSkills(msg, topN = 2) {
  if (skills.length === 0) return [];
  const lower = msg.toLowerCase();
  const scored = skills.map((s) => {
    const keywordHits = s.keywords.filter((k) => lower.includes(k)).length;
    const descHits = (s.description.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).filter((w) => lower.includes(w.toLowerCase())).length;
    return { skill: s, score: keywordHits * 2 + descHits };
  }).filter((s) => s.score > 0);
  scored.sort((a, b) => b.score - a.score);
  const results = scored.slice(0, topN).map((s) => {
    s.skill.usedCount++;
    s.skill.lastUsed = Date.now();
    return s.skill;
  });
  if (results.length > 0) saveSkills();
  return results;
}
function autoExtractSkill(userMsg, botResponse) {
  if (!botResponse.includes("```") || botResponse.length < 100) return;
  if (userMsg.length < 10) return;
  spawnCLI(
    `\u4EE5\u4E0B\u5BF9\u8BDD\u5305\u542B\u4E00\u4E2A\u6280\u672F\u95EE\u9898\u7684\u89E3\u51B3\u65B9\u6848\u3002\u5224\u65AD\u662F\u5426\u503C\u5F97\u4FDD\u5B58\u4E3A\u53EF\u590D\u7528\u6280\u80FD\u3002

\u95EE\u9898: "${userMsg.slice(0, 200)}"
\u65B9\u6848: "${botResponse.slice(0, 500)}"

\u5982\u679C\u503C\u5F97\u4FDD\u5B58\uFF0C\u8F93\u51FAJSON: {"name":"\u6280\u80FD\u540D","description":"\u89E3\u51B3\u4EC0\u4E48\u95EE\u9898","keywords":["\u5173\u952E\u8BCD"],"solution":"\u6838\u5FC3\u65B9\u6848(\u7B80\u5316\u7248)"}
\u5982\u679C\u4E0D\u503C\u5F97\uFF08\u592A\u5177\u4F53/\u4E00\u6B21\u6027\uFF09\uFF0C\u56DE\u7B54"\u5426"`,
    (output) => {
      if (!output || output.includes("\u5426")) return;
      try {
        const match = output.match(/\{[\s\S]*\}/);
        if (match) {
          const skill = JSON.parse(match[0]);
          if (skill.name && skill.solution) {
            saveSkill(skill.name, skill.description || "", skill.solution, skill.keywords || []);
          }
        }
      } catch {
      }
    }
  );
}
const GOALS_PATH = resolve(DATA_DIR, "goals.json");
let activeGoals = loadJson(GOALS_PATH, []).filter((g) => Array.isArray(g.steps));
function saveGoals() {
  debouncedSave(GOALS_PATH, activeGoals);
}
function startAutonomousGoal(goal, callback) {
  console.log(`[cc-soul][goal] starting: ${goal.slice(0, 60)}`);
  spawnCLI(
    `Break this goal into 3-7 concrete executable steps. Each step should be a single actionable task.

Goal: "${goal}"

Format: one step per line, just the action (no numbering, no explanation).`,
    (output) => {
      if (!output) {
        if (callback) callback("Failed to decompose goal");
        return;
      }
      const steps = output.split("\n").map((l) => l.replace(/^\d+[.)\s]+/, "").trim()).filter((l) => l.length > 5).map((desc) => ({ desc, status: "pending", result: void 0 }));
      if (steps.length < 2) {
        if (callback) callback("Could not break goal into steps");
        return;
      }
      const goalObj = {
        id: Date.now().toString(36),
        goal,
        steps,
        createdAt: Date.now(),
        completedAt: 0,
        maxRetries: 2,
        currentStep: 0,
        evaluation: ""
      };
      activeGoals.push(goalObj);
      if (activeGoals.length > 10) activeGoals = activeGoals.slice(-8);
      saveGoals();
      console.log(`[cc-soul][goal] decomposed into ${steps.length} steps`);
      executeNextStep(goalObj, callback);
    }
  );
}
function executeNextStep(goal, callback) {
  const step = goal.steps.find((s) => s.status === "pending");
  if (!step) {
    evaluateGoal(goal, callback);
    return;
  }
  const stepIdx = goal.steps.indexOf(step);
  step.status = "running";
  goal.currentStep = stepIdx;
  saveGoals();
  console.log(`[cc-soul][goal] executing step ${stepIdx + 1}/${goal.steps.length}: ${step.desc.slice(0, 50)}`);
  const prevResults = goal.steps.filter((s) => s.status === "done" && s.result).map((s, i) => `Step ${i + 1}: ${s.desc} \u2192 ${s.result}`).join("\n");
  const prompt = prevResults ? `Previous steps completed:
${prevResults}

Now execute this step:
"${step.desc}"

Do it and report the result briefly.` : `Execute this step:
"${step.desc}"

Do it and report the result briefly.`;
  spawnCLI(prompt, (output) => {
    if (output && output.length > 5) {
      step.status = "done";
      step.result = output.slice(0, 500);
      console.log(`[cc-soul][goal] step ${stepIdx + 1} done: ${output.slice(0, 60)}`);
    } else {
      step.status = "failed";
      step.result = "No output";
      console.log(`[cc-soul][goal] step ${stepIdx + 1} failed`);
    }
    saveGoals();
    setTimeout(() => executeNextStep(goal, callback), 3e3);
  }, 6e4);
}
function evaluateGoal(goal, callback) {
  const stepResults = goal.steps.map((s, i) => `${i + 1}. ${s.desc} \u2192 ${s.status === "done" ? s.result : "FAILED"}`).join("\n");
  spawnCLI(
    `Evaluate this completed goal:

Goal: "${goal.goal}"

Steps and results:
${stepResults}

Was the goal achieved? Rate 1-10 and explain in 1 sentence.`,
    (output) => {
      goal.evaluation = output?.slice(0, 200) || "No evaluation";
      goal.completedAt = Date.now();
      saveGoals();
      addMemory(
        `[goal completed] ${goal.goal} \u2192 ${goal.evaluation}`,
        "task",
        void 0,
        "global"
      );
      const summary = `Goal "${goal.goal.slice(0, 40)}": ${goal.steps.filter((s) => s.status === "done").length}/${goal.steps.length} steps done. ${goal.evaluation}`;
      console.log(`[cc-soul][goal] ${summary}`);
      if (callback) callback(summary);
    }
  );
}
function getActiveGoalHint() {
  const active = activeGoals.find((g) => !g.completedAt && Array.isArray(g.steps) && g.steps.some((s) => s.status === "pending" || s.status === "running"));
  if (!active) return "";
  const done = active.steps.filter((s) => s.status === "done").length;
  const total = active.steps.length;
  const next = active.steps.find((s) => s.status === "pending");
  return `[Active Goal] "${active.goal.slice(0, 40)}" \u2014 ${done}/${total} steps done${next ? `. Next: ${next.desc.slice(0, 40)}` : ""}`;
}
function detectGoalIntent(msg) {
  const m = msg.toLowerCase();
  return ["goal:", "objective:", "mission:", "\u76EE\u6807:", "\u76EE\u6807\u662F"].some((w) => m.includes(w)) || m.includes("\u5E2E\u6211") && m.length > 50 || m.includes("help me") && m.length > 50;
}
function detectWorkflowOpportunity(msg, response) {
  const stepIndicators = response.match(/\d+\.\s/g);
  if (!stepIndicators || stepIndicators.length < 3) return;
  spawnCLI(
    `\u4EE5\u4E0B\u56DE\u590D\u5305\u542B\u591A\u6B65\u64CD\u4F5C\u3002\u5224\u65AD\u8FD9\u662F\u5426\u9002\u5408\u53D8\u6210\u4E00\u4E2A\u53EF\u590D\u7528\u7684\u5DE5\u4F5C\u6D41\uFF1F

\u7528\u6237: ${msg.slice(0, 200)}
\u56DE\u590D: ${response.slice(0, 500)}

\u5982\u679C\u9002\u5408\uFF0C\u8F93\u51FAJSON: {"name":"\u5DE5\u4F5C\u6D41\u540D","trigger":"\u89E6\u53D1\u6761\u4EF6","steps":["\u6B65\u9AA41","\u6B65\u9AA42"]}
\u5982\u679C\u4E0D\u9002\u5408\uFF0C\u56DE\u7B54"\u5426"`,
    (output) => {
      try {
        const result = extractJSON(output);
        if (result && result.name && result.steps?.length >= 2) {
          createWorkflow(result.name, result.trigger || msg.slice(0, 50), result.steps);
        }
      } catch (e) {
        console.error(`[cc-soul] JSON parse error: ${e.message}`);
      }
    }
  );
}
const tasksModule = {
  id: "tasks",
  name: "\u4EFB\u52A1\u7CFB\u7EDF",
  dependencies: ["memory"],
  priority: 50,
  init() {
    initTasks();
  }
};
export {
  autoCreateSkill,
  autoExtractSkill,
  checkTaskConfirmation,
  createWorkflow,
  detectActionIntent,
  detectAndDelegateTask,
  detectGoalIntent,
  detectSkillOpportunity,
  detectWorkflowOpportunity,
  detectWorkflowTrigger,
  executeCLITask,
  executeWorkflow,
  findSkills,
  getActiveGoalHint,
  getActivePlanHint,
  initTasks,
  saveSkill,
  skills as skillLibrary,
  startAutonomousGoal,
  taskState,
  tasksModule,
  trackRequestPattern
};
