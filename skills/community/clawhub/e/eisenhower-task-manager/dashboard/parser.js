/**
 * Markdown Parser for Eisenhower Task Manager
 * Parses tasks.md, customer-projects.md, delegation.md, maybe.md
 */

const fs = require('fs');
const path = require('path');

// Tasks are located in workspace/tasks/ directory (4 levels up from dashboard)
const EISENHOWER_TASKS_DIR = process.env.EISENHOWER_TASKS_DIR || path.join(__dirname, '../tasks');

/**
 * Parse tasks.md - Four Quadrants Format
 */
function parseTasks(content) {
  const result = {
    q1: [],
    q2: [],
    q3: [],
    q4: [],
    stats: { q1: 0, q2: 0, q3: 0, q4: 0, total: 0 }
  };

  // Stats will be calculated based on actual parsed tasks (more accurate than header text)

  // Split by quadrants - support both half-width () and full-width () parentheses and varying emoji presence
  const q1Match = content.match(/## (?:🔥 )?Q1[\s\S]*?(?=## (?:💼 )?Q2|$)/);
  const q2Match = content.match(/## (?:💼 )?Q2[\s\S]*?(?=## (?:⚡ )?Q3|$)/);
  const q3Match = content.match(/## (?:⚡ )?Q3[\s\S]*?(?=## (?:🧘 )?Q4|$)/);
  const q4Match = content.match(/## (?:🧘 )?Q4[\s\S]*?(?=## (?:👑 )?|## Completed|$)/);

  if (q1Match) result.q1 = parseQuadrantTasks(q1Match[0], 'Q1');
  if (q2Match) result.q2 = parseQuadrantTasks(q2Match[0], 'Q2');
  if (q3Match) result.q3 = parseQuadrantTasks(q3Match[0], 'Q3');
  if (q4Match) result.q4 = parseQuadrantTasks(q4Match[0], 'Q4');

  // Calculate stats based on actual parsed tasks (more accurate than header text)
  result.stats.q1 = result.q1.length;
  result.stats.q2 = result.q2.length;
  result.stats.q3 = result.q3.length;
  result.stats.q4 = result.q4.length;
  result.stats.total = result.q1.length + result.q2.length + result.q3.length + result.q4.length;

  return result;
}

function parseQuadrantTasks(content, quadrant) {
  const tasks = [];
  // Match task sections: ### X. Task Name [tags]
  const taskRegex = /### (\d+)\.\s*(.+?)(?:\s*\[([^\]]+)\])?\n([\s\S]*?)(?=### \d+\.|## |\n## |\n---|$)/g;

  let match;
  while ((match = taskRegex.exec(content)) !== null) {
    const taskContent = match[4];
    const task = {
      id: parseInt(match[1]),
      title: match[2].trim(),
      tags: match[3] ? match[3].split('/').map(t => t.trim()) : [],
      quadrant: quadrant,
      status: extractStatus(taskContent),
      priority: extractPriority(taskContent),
      description: extractDescription(taskContent),
      created: extractDate(taskContent, '创建'),
      updated: extractDate(taskContent, '更新'),
      blocked: taskContent.includes('🚫') || taskContent.includes('阻塞'),
      subtasks: extractSubtasks(taskContent),
      raw: match[0]
    };
    tasks.push(task);
  }

  return tasks;
}

function extractStatus(content) {
  const statusMatch = content.match(/\*\*状态\*\*:(.+)/);
  if (statusMatch) {
    const status = statusMatch[1].trim();
    if (status.includes('P0')) return 'P0';
    if (status.includes('P1')) return 'P1';
    if (status.includes('P2')) return 'P2';
    return status;
  }
  return '';
}

function extractPriority(content) {
  if (content.includes('P0')) return 'P0';
  if (content.includes('P1')) return 'P1';
  if (content.includes('P2')) return 'P2';
  return '';
}

function extractDescription(content) {
  const descMatch = content.match(/\*\*描述\*\*:(.+)/);
  return descMatch ? descMatch[1].trim() : '';
}

function extractDate(content, type) {
  const dateMatch = content.match(new RegExp(`\\*\\*${type}\\*\\*:(.+)`));
  return dateMatch ? dateMatch[1].trim() : '';
}

function extractSubtasks(content) {
  const subtasks = [];
  const subtaskRegex = /-\s*\*\*(.+?)\*\*\n([\s\S]*?)(?=\n\s*-\s*\*\*|\n### |\n## |$)/g;

  let match;
  while ((match = subtaskRegex.exec(content)) !== null) {
    subtasks.push({
      title: match[1].trim(),
      content: match[2].trim()
    });
  }

  return subtasks;
}

/**
 * Parse customer-projects.md - Customer Project List Format
 */
function parseCustomerProjects(content) {
  const result = {
    customers: [],
    stats: { active: 0, blocked: 0, pending: 0, total: 0 }
  };

  // Extract stats from overview table (support both Chinese and English)
  const activeMatch = content.match(/🟢\s*(?:Active|进行中)\s*\|\s*(\d+)/);
  const blockedMatch = content.match(/🟡\s*(?:Blocked|阻塞中|阻塞)\s*\|\s*(\d+)/);
  const pendingMatch = content.match(/🔵\s*(?:Pending|待开始)\s*\|\s*(\d+)/);
  const totalMatch = content.match(/\*\*\s*(?:Total|总计)\s*\*\*\s*\|\s*\*\*(\d+)\*\*/);

  if (activeMatch) result.stats.active = parseInt(activeMatch[1]);
  if (blockedMatch) result.stats.blocked = parseInt(blockedMatch[1]);
  if (pendingMatch) result.stats.pending = parseInt(pendingMatch[1]);
  if (totalMatch) result.stats.total = parseInt(totalMatch[1]);

  // Parse customers and their projects
  // Support format: ### 🔴 优先级1：Name (Chinese colon)
  // Note: Emoji is 2 UTF-16 code units (surrogate pair)
  // Use split parsing: first find customer headers, then extract sections manually
  const customerHeaders = Array.from(content.matchAll(/^###\s+(.{1,2})\s+优先级[\d一二三四五]+[：:](.+)$/gmu));

  for (let i = 0; i < customerHeaders.length; i++) {
    const headerMatch = customerHeaders[i];
    const startPos = headerMatch.index + headerMatch[0].length;
    const endPos = i < customerHeaders.length - 1 ? customerHeaders[i + 1].index : content.length;
    const section = content.substring(startPos, endPos);

    const customer = {
      name: headerMatch[2].trim(),
      priority: headerMatch[1].trim(),
      projects: []
    };

    // Parse projects within customer section
    // Match #### (project level)
    const projectRegex = /^#### (\d+)\.\s*(.+?)\n/gm;
    let projMatch;
    while ((projMatch = projectRegex.exec(section)) !== null) {
      const projStart = projMatch.index + projMatch[0].length;
      // Find where this project ends (next #### or end of section)
      const nextProjMatch = /^#### \d+\./m.exec(section.substring(projStart));
      const projEnd = nextProjMatch ? projStart + nextProjMatch.index : section.length;
      const projContent = section.substring(projStart, projEnd);

      const project = {
        id: parseInt(projMatch[1]),
        name: projMatch[2].trim(),
        status: extractField(projContent, '状态') || extractField(projContent, 'Status'),
        type: extractField(projContent, '类型') || extractField(projContent, 'Type'),
        priority: extractField(projContent, '优先级') || extractField(projContent, 'Priority'),
        created: extractField(projContent, '创建时间') || extractField(projContent, 'Created'),
        lastReview: extractField(projContent, '上次回顾') || extractField(projContent, 'Last Review'),
        nextReview: extractField(projContent, '下次检查') || extractField(projContent, 'Next Review'),
        notes: extractField(projContent, '备注') || extractField(projContent, 'Notes'),
        quadrantTask: extractField(projContent, '象限任务') || extractField(projContent, 'Quadrant Task'),
        blocked: projContent.includes('🟡') || projContent.includes('阻塞'),
        raw: projMatch[0] + projContent  // Save original content for regeneration
      };
      customer.projects.push(project);
    }

    result.customers.push(customer);
  }

  return result;
}

function extractField(content, fieldName) {
  // Escape special regex characters in fieldName
  const escapedFieldName = fieldName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // Support Chinese colon (:) - the document uses Chinese colons
  // Support optional markdown checkbox: - [ ], - [x], or just - 
  const regex = new RegExp(`-(?: \\[[ xX]\\])? \\*\\*${escapedFieldName}\\*\\*:(.+)`, 'im');
  const match = content.match(regex);
  return match ? match[1].trim() : '';
}

/**
 * Parse delegation.md - Delegation List Format
 */
function parseDelegation(content) {
  const result = {
    tasks: [],
    stats: { total: 0, inProgress: 0, delegated: 0, overdue: 0 }
  };

  // Extract total count
  const totalMatch = content.match(/总任务数:(\d+) 个/);
  if (totalMatch) result.stats.total = parseInt(totalMatch[1]);

  // Parse delegation tasks
  const taskRegex = /#### (\d+)\.\s*(.+?)\n([\s\S]*?)(?=#### \d+\.|## |\n---|$)/g;

  let match;
  while ((match = taskRegex.exec(content)) !== null) {
    const taskContent = match[3];
    const task = {
      id: parseInt(match[1]),
      title: match[2].trim(),
      status: extractField(taskContent, '状态'),
      assignee: extractAssignee(taskContent),
      description: extractField(taskContent, '说明'),
      deadline: extractField(taskContent, 'Deadline'),
      created: extractField(taskContent, '创建时间'),
      lastReview: extractField(taskContent, 'Last Review'),
      nextReview: extractField(taskContent, 'Next Review'),
      overdue: taskContent.includes('⚠️') || taskContent.includes('已过期'),
      raw: match[0]
    };
    result.tasks.push(task);
  }

  // Calculate stats based on actual parsed tasks
  result.stats.total = result.tasks.length;
  result.stats.inProgress = result.tasks.filter(t => t.status === '进行中').length;
  result.stats.delegated = result.tasks.filter(t => t.status === '待开始').length;
  result.stats.overdue = result.tasks.filter(t => t.overdue).length;

  return result;
}

function extractAssignee(content) {
  const match = content.match(/\*\*责任人\*\*:(.+)/);
  return match ? match[1].trim() : '';
}

/**
 * Parse maybe.md - Maybe List Format
 */
function parseMaybeList(content) {
  const result = {
    tasks: [],
    stats: { total: 0 }
  };

  // Parse maybe tasks
  const taskRegex = /#### (\d+)\.\s*(.+?)\n([\s\S]*?)(?=#### \d+\.|## |\n---|$)/g;

  let match;
  while ((match = taskRegex.exec(content)) !== null) {
    const taskContent = match[3];
    const rawTitle = match[2].trim();

    // Extract category from title (e.g., "任务名【分类】" -> category: "分类")
    const categoryMatch = rawTitle.match(/【(.+?)】$/);
    const category = categoryMatch ? categoryMatch[1] : '';
    // Remove category marker from title
    const title = rawTitle.replace(/【.+?】$/, '').trim();

    const task = {
      id: parseInt(match[1]),
      title: title,
      status: extractField(taskContent, '状态'),
      description: extractField(taskContent, '说明'),
      content: taskContent.trim(),
      created: extractField(taskContent, '创建时间'),
      category: category,
      raw: match[0]
    };
    result.tasks.push(task);
  }

  // Calculate stats based on actual parsed tasks
  result.stats.total = result.tasks.length;

  return result;
}

function extractCategory(content) {
  const match = content.match(/【(.+?)】/);
  return match ? match[1] : '';
}

/**
 * Load and parse all task files
 */
function loadAllTasks() {
  const data = {
    timestamp: new Date().toISOString()
  };

  try {
    const tasksContent = fs.readFileSync(path.join(EISENHOWER_TASKS_DIR, 'tasks.md'), 'utf8');
    data.tasks = parseTasks(tasksContent);
  } catch (e) {
    data.tasks = { error: e.message, q1: [], q2: [], q3: [], q4: [], stats: {} };
  }

  try {
    const customerContent = fs.readFileSync(path.join(EISENHOWER_TASKS_DIR, 'customer-projects.md'), 'utf8');
    data.customerProjects = parseCustomerProjects(customerContent);
  } catch (e) {
    data.customerProjects = { error: e.message, customers: [], stats: {} };
  }

  try {
    const delegationContent = fs.readFileSync(path.join(EISENHOWER_TASKS_DIR, 'delegation.md'), 'utf8');
    data.delegation = parseDelegation(delegationContent);
  } catch (e) {
    data.delegation = { error: e.message, tasks: [], stats: {} };
  }

  try {
    const maybeContent = fs.readFileSync(path.join(EISENHOWER_TASKS_DIR, 'maybe.md'), 'utf8');
    data.maybe = parseMaybeList(maybeContent);
  } catch (e) {
    data.maybe = { error: e.message, tasks: [], stats: {} };
  }

  return data;
}

/**
 * Move a task between quadrants or reorder within the same quadrant
 * @param {number} taskId - The task ID to move
 * @param {string} sourceQuadrant - Source quadrant (Q1, Q2, Q3, Q4)
 * @param {string} targetQuadrant - Target quadrant (Q1, Q2, Q3, Q4)
 * @param {number} insertIndex - Position to insert in target quadrant (-1 for append)
 */
async function moveTask(taskId, sourceQuadrant, targetQuadrant, insertIndex = -1) {
  try {
    console.log(`[Parser] Moving task ${taskId} from ${sourceQuadrant} to ${targetQuadrant} at index ${insertIndex}`);

    const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
    const content = fs.readFileSync(tasksFile, 'utf8');

    // Parse current tasks
    const tasks = parseTasks(content);

    // Find the task to move
    const sourceList = tasks[sourceQuadrant.toLowerCase()];
    const targetList = tasks[targetQuadrant.toLowerCase()];

    if (!sourceList || !targetList) {
      return { success: false, error: `Invalid quadrant: ${sourceQuadrant} or ${targetQuadrant}` };
    }

    const taskIndex = sourceList.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: `Task ${taskId} not found in ${sourceQuadrant}` };
    }

    const taskToMove = sourceList[taskIndex];

    // Update task quadrant
    taskToMove.quadrant = targetQuadrant;

    // Remove from source
    sourceList.splice(taskIndex, 1);

    // Insert into target
    if (insertIndex === -1 || insertIndex >= targetList.length) {
      targetList.push(taskToMove);
    } else {
      targetList.splice(insertIndex, 0, taskToMove);
    }

    // Generate new markdown content (this will handle renumbering)
    const newContent = generateTasksMarkdown(tasks, content);

    // Write back to file
    fs.writeFileSync(tasksFile, newContent, 'utf8');

    // Calculate the new ID for the moved task
    let newId;
    if (targetQuadrant === 'Q1') {
      newId = insertIndex === -1 ? tasks.q1.length : insertIndex + 1;
    } else if (targetQuadrant === 'Q2') {
      newId = tasks.q1.length + (insertIndex === -1 ? tasks.q2.length : insertIndex + 1);
    } else if (targetQuadrant === 'Q3') {
      newId = tasks.q1.length + tasks.q2.length + (insertIndex === -1 ? tasks.q3.length : insertIndex + 1);
    } else {
      newId = tasks.q1.length + tasks.q2.length + tasks.q3.length + (insertIndex === -1 ? tasks.q4.length : insertIndex + 1);
    }

    console.log(`[Parser] Task moved successfully. New ID: ${newId}`);

    return {
      success: true,
      message: `Task moved from ${sourceQuadrant} to ${targetQuadrant}`,
      newId: newId
    };

  } catch (error) {
    console.error('[Parser] Move task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Generate tasks.md content from parsed tasks
 * Uses task.raw to preserve original formatting, only updates task numbers
 */
function generateTasksMarkdown(tasks, originalContent) {
  // Extract header (everything before ## 🔥 Q1)
  const headerMatch = originalContent.match(/^(.*?)(?=## 🔥 Q1)/s);
  const header = headerMatch ? headerMatch[1] : '# 任务清单\n\n';

  // Calculate totals
  const totalTasks = tasks.q1.length + tasks.q2.length + tasks.q3.length + tasks.q4.length;

  // Update stats line in header (match both Chinese and English colons)
  let updatedHeader = header.replace(
    /总任务数[：:]\d+ \(Q1: \d+ \+ Q2: \d+ \+ Q3: \d+ \+ Q4: \d+\)/,
    `总任务数：${totalTasks} (Q1: ${tasks.q1.length} + Q2: ${tasks.q2.length} + Q3: ${tasks.q3.length} + Q4: ${tasks.q4.length})`
  );

  // Generate content
  let content = updatedHeader;

  // Q1
  content += '## 🔥 Q1(重要+紧急)\n\n';
  tasks.q1.forEach((task, index) => {
    content += formatTaskMarkdown(task, index + 1);
  });

  // Q2
  content += '\n## 💼 Q2(重要+不紧急)\n\n';
  tasks.q2.forEach((task, index) => {
    content += formatTaskMarkdown(task, tasks.q1.length + index + 1);
  });

  // Q3
  content += '\n## ⚡ Q3(不重要+紧急)\n\n';
  tasks.q3.forEach((task, index) => {
    content += formatTaskMarkdown(task, tasks.q1.length + tasks.q2.length + index + 1);
  });

  // Q4
  content += '\n## 🧘 Q4(不重要+不紧急)\n\n';
  tasks.q4.forEach((task, index) => {
    content += formatTaskMarkdown(task, tasks.q1.length + tasks.q2.length + tasks.q3.length + index + 1);
  });

  return content;
}

/**
 * Format a single task as markdown
 * Uses raw content if available, otherwise constructs from fields
 * Updates the task number to the new sequential number
 */
function formatTaskMarkdown(task, newId) {
  // If we have raw content, use it and just update the task number
  if (task.raw) {
    // Replace the task number in the raw content
    // Pattern: ### N. Title → ### newId. Title
    return task.raw.replace(/^### \d+\./, `### ${newId}.`);
  }

  // Fallback: construct from fields
  let md = `### ${newId}. ${task.title}`;

  if (task.tags && task.tags.length > 0) {
    md += ` [${task.tags.join('/')}]`;
  }

  md += '\n';

  if (task.priority) {
    md += `- **状态**:${task.priority}\n`;
  }
  if (task.description) {
    md += `- **描述**:${task.description}\n`;
  }
  if (task.created) {
    md += `- **创建**:${task.created}\n`;
  }
  if (task.blocked) {
    md += `- 🚫 **阻塞**\n`;
  }

  md += '\n';
  return md;
}

/**
 * Move a customer project within its customer section or between customers
 * @param {number} projectId - The project ID to move
 * @param {string} sourceCustomer - Source customer name
 * @param {string} targetCustomer - Target customer name
 * @param {number} insertIndex - Position to insert in target customer project list (-1 for append)
 */
async function moveCustomerProject(projectId, sourceCustomer, targetCustomer, insertIndex = -1) {
  try {
    console.log(`[Parser] Moving customer project ${projectId} from "${sourceCustomer}" to "${targetCustomer}" at index ${insertIndex}`);

    const customerFile = path.join(EISENHOWER_TASKS_DIR, 'customer-projects.md');
    const content = fs.readFileSync(customerFile, 'utf8');

    // Parse current customer projects
    const data = parseCustomerProjects(content);

    // Find source and target customers
    const sourceCust = data.customers.find(c => c.name === sourceCustomer);
    const targetCust = data.customers.find(c => c.name === targetCustomer);

    if (!sourceCust) {
      return { success: false, error: `Source customer "${sourceCustomer}" not found` };
    }
    if (!targetCust) {
      return { success: false, error: `Target customer "${targetCustomer}" not found` };
    }

    // Find the project to move
    const projectIndex = sourceCust.projects.findIndex(p => p.id === projectId);
    if (projectIndex === -1) {
      return { success: false, error: `Project ${projectId} not found in "${sourceCustomer}"` };
    }

    const projectToMove = sourceCust.projects[projectIndex];

    // Remove from source
    sourceCust.projects.splice(projectIndex, 1);

    // Insert into target
    if (insertIndex === -1 || insertIndex >= targetCust.projects.length) {
      targetCust.projects.push(projectToMove);
    } else {
      targetCust.projects.splice(insertIndex, 0, projectToMove);
    }

    // Generate new markdown content with renumbered projects
    const newContent = generateCustomerProjectsMarkdown(data, content);

    // Write back to file
    fs.writeFileSync(customerFile, newContent, 'utf8');

    console.log(`[Parser] Customer project moved successfully`);

    return {
      success: true,
      message: `Project moved from "${sourceCustomer}" to "${targetCustomer}"`
    };

  } catch (error) {
    console.error('[Parser] Move customer project error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Generate customer-projects.md content from parsed data
 * Rebuilds each customer section with projects in new order
 */
function generateCustomerProjectsMarkdown(data, originalContent) {
  // Update stats in overview table first
  let content = originalContent;
  const totalProjects = data.customers.reduce((sum, c) => sum + c.projects.length, 0);
  const activeProjects = data.customers.reduce((sum, c) => sum + c.projects.filter(p => !p.blocked && p.status?.toLowerCase().includes('active')).length, 0);
  const blockedProjects = data.customers.reduce((sum, c) => sum + c.projects.filter(p => p.blocked).length, 0);

  content = content.replace(
    /\|\s*🟢\s*(?:Active|进行中)\s*\|\s*\d+\s*\|/,
    `| 🟢 进行中 | ${activeProjects} |`
  );
  content = content.replace(
    /\|\s*🟡\s*(?:Blocked|阻塞中|阻塞)\s*\|\s*\d+\s*\|/,
    `| 🟡 阻塞中 | ${blockedProjects} |`
  );
  content = content.replace(
    /\*\*\s*(?:Total|总计)\s*\*\*\s*\|\s*\*\*\d+\*\*/,
    `**总计** | **${totalProjects}**`
  );

  // Process each customer: rebuild their section with projects in new order
  data.customers.forEach(customer => {
    // Find the customer section in the content
    const customerHeaderPattern = new RegExp(`(###\\s+.{1,2}\\s+优先级[\\d一二三四五]+[：:]${escapeRegex(customer.name)})(\\n*)`);
    const headerMatch = content.match(customerHeaderPattern);
    
    if (!headerMatch) return;
    
    const headerStart = headerMatch.index;
    const headerEnd = headerStart + headerMatch[0].length;
    
    // Find where this customer section ends (next ### or end of file)
    const nextCustomerMatch = content.substring(headerEnd).match(/\n###\s+.{1,2}\s+优先级/);
    const sectionEnd = nextCustomerMatch ? headerEnd + nextCustomerMatch.index : content.length;
    
    // Build new customer section content
    let newSection = headerMatch[1] + '\n\n';
    
    // Add projects in new order with updated numbers
    customer.projects.forEach((project, index) => {
      const newId = index + 1;
      if (project.raw) {
        // Update the project number in raw content
        newSection += project.raw.replace(/^#### \d+\./, `#### ${newId}.`);
      } else {
        newSection += formatCustomerProjectMarkdown(project, newId);
      }
    });
    
    // Replace the old section with new section
    content = content.substring(0, headerStart) + newSection + content.substring(sectionEnd);
  });

  return content;
}

/**
 * Format a single customer project as markdown
 * Uses raw content if available to preserve original formatting
 */
function formatCustomerProjectMarkdown(project, newId) {
  // If we have raw content, use it and just update the project number
  if (project.raw) {
    // Replace the project number in the raw content
    // Pattern: #### N. Project Name → #### newId. Project Name
    return project.raw.replace(/^#### \d+\./, `#### ${newId}.`);
  }

  // Fallback: construct from fields
  let md = `#### ${newId}. ${project.name}\n`;

  if (project.status) {
    md += `- **状态**：${project.status}\n`;
  }
  if (project.type) {
    md += `- **类型**：${project.type}\n`;
  }
  if (project.priority) {
    md += `- **优先级**：${project.priority}\n`;
  }
  if (project.created) {
    md += `- **创建时间**：${project.created}\n`;
  }
  if (project.lastReview) {
    md += `- **上次回顾**：${project.lastReview}\n`;
  }
  if (project.nextReview) {
    md += `- **下次检查**：${project.nextReview}\n`;
  }
  if (project.notes) {
    md += `- **备注**：${project.notes}\n`;
  }
  if (project.quadrantTask) {
    md += `- **象限任务**：${project.quadrantTask}\n`;
  }

  md += '\n';
  return md;
}

/**
 * Escape special regex characters
 */
function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Delete a task from tasks.md and renumber remaining tasks
 * @param {number} taskId - The task ID to delete
 * @param {string} quadrant - The quadrant the task is in (Q1, Q2, Q3, Q4)
 */
async function deleteTask(taskId, quadrant) {
  try {
    console.log(`[Parser] Deleting task ${taskId} from ${quadrant}`);

    const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
    const content = fs.readFileSync(tasksFile, 'utf8');

    // Parse current tasks
    const tasks = parseTasks(content);

    // Find the task to delete
    const taskList = tasks[quadrant.toLowerCase()];
    const taskIndex = taskList.findIndex(t => t.id === taskId);

    if (taskIndex === -1) {
      return { success: false, error: `Task ${taskId} not found in ${quadrant}` };
    }

    // Remove the task
    taskList.splice(taskIndex, 1);

    // Generate new markdown with renumbered tasks
    const newContent = generateTasksMarkdown(tasks, content);

    // Write back to file
    fs.writeFileSync(tasksFile, newContent, 'utf8');

    console.log(`[Parser] Task ${taskId} deleted successfully`);

    return {
      success: true,
      message: `Task ${taskId} deleted from ${quadrant}`
    };

  } catch (error) {
    console.error('[Parser] Delete task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Delete a customer project and renumber remaining projects
 * @param {number} projectId - The project ID to delete
 * @param {string} customerName - The customer name
 */
async function deleteCustomerProject(projectId, customerName) {
  try {
    console.log(`[Parser] Deleting project ${projectId} from "${customerName}"`);

    const customerFile = path.join(EISENHOWER_TASKS_DIR, 'customer-projects.md');
    const content = fs.readFileSync(customerFile, 'utf8');

    // Parse current customer projects
    const data = parseCustomerProjects(content);

    // Find the customer
    const customer = data.customers.find(c => c.name === customerName);
    if (!customer) {
      return { success: false, error: `Customer "${customerName}" not found` };
    }

    // Find the project to delete
    const projectIndex = customer.projects.findIndex(p => p.id === projectId);
    if (projectIndex === -1) {
      return { success: false, error: `Project ${projectId} not found in "${customerName}"` };
    }

    // Remove the project
    customer.projects.splice(projectIndex, 1);

    // Generate new markdown with renumbered projects
    const newContent = generateCustomerProjectsMarkdown(data, content);

    // Write back to file
    fs.writeFileSync(customerFile, newContent, 'utf8');

    console.log(`[Parser] Project ${projectId} deleted successfully`);

    return {
      success: true,
      message: `Project ${projectId} deleted from "${customerName}"`
    };

  } catch (error) {
    console.error('[Parser] Delete customer project error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Delete a delegation task and renumber remaining tasks
 * @param {number} taskId - The task ID to delete
 */
async function deleteDelegationTask(taskId) {
  try {
    console.log(`[Parser] Deleting delegation task ${taskId}`);

    const delegationFile = path.join(EISENHOWER_TASKS_DIR, 'delegation.md');
    const content = fs.readFileSync(delegationFile, 'utf8');

    // Parse current delegation tasks
    const data = parseDelegation(content);

    // Find the task to delete
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: `Delegation task ${taskId} not found` };
    }

    // Remove the task
    data.tasks.splice(taskIndex, 1);

    // Generate new markdown with renumbered tasks
    const newContent = generateDelegationMarkdown(data, content);

    // Write back to file
    fs.writeFileSync(delegationFile, newContent, 'utf8');

    console.log(`[Parser] Delegation task ${taskId} deleted successfully`);

    return {
      success: true,
      message: `Delegation task ${taskId} deleted`
    };

  } catch (error) {
    console.error('[Parser] Delete delegation task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Delete a maybe list task and renumber remaining tasks
 * @param {number} taskId - The task ID to delete
 */
async function deleteMaybeTask(taskId) {
  try {
    console.log(`[Parser] Deleting maybe task ${taskId}`);

    const maybeFile = path.join(EISENHOWER_TASKS_DIR, 'maybe.md');
    const content = fs.readFileSync(maybeFile, 'utf8');

    // Parse current maybe tasks
    const data = parseMaybeList(content);

    // Find the task to delete
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: `Maybe task ${taskId} not found` };
    }

    // Remove the task
    data.tasks.splice(taskIndex, 1);

    // Generate new markdown with renumbered tasks
    const newContent = generateMaybeMarkdown(data, content);

    // Write back to file
    fs.writeFileSync(maybeFile, newContent, 'utf8');

    console.log(`[Parser] Maybe task ${taskId} deleted successfully`);

    return {
      success: true,
      message: `Maybe task ${taskId} deleted`
    };

  } catch (error) {
    console.error('[Parser] Delete maybe task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Generate delegation.md content from parsed data
 */
function generateDelegationMarkdown(data, originalContent) {
  // Extract header (everything before first ####)
  const headerMatch = originalContent.match(/^(.*?)(?=####\s+\d+\.)/s);
  let content = headerMatch ? headerMatch[1] : '';

  // Update total count
  content = content.replace(/总任务数:\d+ 个/, `总任务数:${data.tasks.length} 个`);

  // Add tasks in order with updated numbers
  data.tasks.forEach((task, index) => {
    const newId = index + 1;
    if (task.raw) {
      content += task.raw.replace(/^#### \d+\./, `#### ${newId}.`);
    } else {
      content += formatDelegationTaskMarkdown(task, newId);
    }
  });

  return content;
}

/**
 * Format a single delegation task as markdown
 */
function formatDelegationTaskMarkdown(task, newId) {
  let md = `#### ${newId}. ${task.title}\n`;

  if (task.status) {
    md += `- **状态**: ${task.status}\n`;
  }
  if (task.assignee) {
    md += `- **责任人**: ${task.assignee}\n`;
  }
  if (task.description) {
    md += `- **说明**: ${task.description}\n`;
  }
  if (task.deadline) {
    md += `- **Deadline**: ${task.deadline}\n`;
  }
  if (task.created) {
    md += `- **创建时间**: ${task.created}\n`;
  }

  md += '\n';
  return md;
}

/**
 * Generate maybe.md content from parsed data
 */
function generateMaybeMarkdown(data, originalContent) {
  // Extract header (everything before first ####)
  const headerMatch = originalContent.match(/^(.*?)(?=####\s+\d+\.)/s);
  let content = headerMatch ? headerMatch[1] : '';

  // Update total count
  content = content.replace(/总任务数:\d+ 个/, `总任务数:${data.tasks.length} 个`);

  // Add tasks in order with updated numbers
  data.tasks.forEach((task, index) => {
    const newId = index + 1;
    if (task.raw) {
      content += task.raw.replace(/^#### \d+\./, `#### ${newId}.`);
    } else {
      content += formatMaybeTaskMarkdown(task, newId);
    }
  });

  return content;
}

/**
 * Format a single maybe task as markdown
 */
function formatMaybeTaskMarkdown(task, newId) {
  let md = `#### ${newId}. ${task.title}\n`;

  if (task.status) {
    md += `- **状态**: ${task.status}\n`;
  }
  if (task.description) {
    md += `- **说明**: ${task.description}\n`;
  }
  if (task.created) {
    md += `- **创建时间**: ${task.created}\n`;
  }

  md += '\n';
  return md;
}

/**
 * Copy a task from one quadrant to another
 * @param {number} taskId - The task ID to copy
 * @param {string} sourceQuadrant - Source quadrant (Q1, Q2, Q3, Q4)
 * @param {string} target - Target quadrant (Q1, Q2, Q3, Q4)
 * @returns {Object} Result object with success status and new task ID
 */
async function copyTask(taskId, sourceQuadrant, target) {
  try {
    console.log(`[Parser] Copying task ${taskId} from ${sourceQuadrant} to ${target}`);

    const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
    const content = fs.readFileSync(tasksFile, 'utf8');

    // Parse current tasks
    const tasks = parseTasks(content);

    // Find the source task
    const sourceList = tasks[sourceQuadrant.toLowerCase()];
    const sourceTask = sourceList.find(t => t.id === taskId);

    if (!sourceTask) {
      return { success: false, error: `Task ${taskId} not found in ${sourceQuadrant}` };
    }

    // Get target list
    const targetList = tasks[target.toLowerCase()];
    
    // Calculate new task ID (append to end of target quadrant)
    // First, calculate the starting ID for the target quadrant
    let startId = 1;
    if (target === 'Q2') startId = tasks.q1.length + 1;
    else if (target === 'Q3') startId = tasks.q1.length + tasks.q2.length + 1;
    else if (target === 'Q4') startId = tasks.q1.length + tasks.q2.length + tasks.q3.length + 1;
    
    const newTaskId = startId + targetList.length;

    // Create a copy of the task with new ID
    const copiedTask = {
      ...sourceTask,
      id: newTaskId,
      quadrant: target,
      created: new Date().toISOString().split('T')[0] // Update creation date
    };

    // Add to target list
    targetList.push(copiedTask);

    // Generate new markdown with renumbered tasks
    const newContent = generateTasksMarkdown(tasks, content);

    // Write back to file
    fs.writeFileSync(tasksFile, newContent, 'utf8');

    console.log(`[Parser] Task copied successfully as ${newTaskId}`);

    return {
      success: true,
      message: `Task copied from ${sourceQuadrant} to ${target} as #${newTaskId}`,
      newTaskId: newTaskId
    };

  } catch (error) {
    console.error('[Parser] Copy task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Copy a customer project to quadrants or delegation list
 * @param {number} projectId - The project ID to copy
 * @param {string} sourceCustomer - Source customer name
 * @param {string} target - Target location (Q1, Q2, Q3, Q4, or 'delegation')
 * @returns {Object} Result object with success status and new task ID
 */
async function copyCustomerProject(projectId, sourceCustomer, target) {
  try {
    console.log(`[Parser] Copying project ${projectId} from "${sourceCustomer}" to ${target}`);

    const customerFile = path.join(EISENHOWER_TASKS_DIR, 'customer-projects.md');
    const customerContent = fs.readFileSync(customerFile, 'utf8');

    // Parse customer projects
    const customerData = parseCustomerProjects(customerContent);
    const sourceCust = customerData.customers.find(c => c.name === sourceCustomer);

    if (!sourceCust) {
      return { success: false, error: `Customer "${sourceCustomer}" not found` };
    }

    // Find the project
    const project = sourceCust.projects.find(p => p.id === projectId);
    if (!project) {
      return { success: false, error: `Project ${projectId} not found in "${sourceCustomer}"` };
    }

    if (target === 'delegation') {
      // Copy to delegation list
      const delegationFile = path.join(EISENHOWER_TASKS_DIR, 'delegation.md');
      const delegationContent = fs.readFileSync(delegationFile, 'utf8');
      const delegationData = parseDelegation(delegationContent);

      // Calculate new task ID
      const newTaskId = delegationData.tasks.length + 1;

      // Create delegation task from project
      const delegationTask = {
        id: newTaskId,
        title: project.name,
        status: '待开始',
        assignee: '@' + (sourceCustomer.includes('PH') ? 'wutong' : '待定'),
        description: `[${sourceCustomer}] ${project.notes || project.name}`,
        deadline: project.nextReview || '待定',
        created: new Date().toISOString().split('T')[0],
        category: sourceCustomer
      };

      delegationData.tasks.push(delegationTask);

      // Generate new markdown
      const newContent = generateDelegationMarkdown(delegationData, delegationContent);
      fs.writeFileSync(delegationFile, newContent, 'utf8');

      console.log(`[Parser] Project copied to delegation list as #${newTaskId}`);

      return {
        success: true,
        message: `Project copied to delegation list as #${newTaskId}`,
        newTaskId: newTaskId
      };

    } else {
      // Copy to quadrants (Q1, Q2, Q3, Q4)
      const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
      const tasksContent = fs.readFileSync(tasksFile, 'utf8');
      const tasks = parseTasks(tasksContent);

      const targetList = tasks[target.toLowerCase()];

      // Calculate new task ID
      let startId = 1;
      if (target === 'Q2') startId = tasks.q1.length + 1;
      else if (target === 'Q3') startId = tasks.q1.length + tasks.q2.length + 1;
      else if (target === 'Q4') startId = tasks.q1.length + tasks.q2.length + tasks.q3.length + 1;

      const newTaskId = startId + targetList.length;

      // Create task from project
      const quadrantTask = {
        id: newTaskId,
        title: `[${sourceCustomer}/${project.name}]`,
        tags: [sourceCustomer, project.type || 'Customer'],
        quadrant: target,
        status: 'P1',
        priority: 'P1',
        description: project.notes || `Copied from customer project: ${project.name}`,
        created: new Date().toISOString().split('T')[0],
        updated: new Date().toISOString().split('T')[0],
        blocked: project.blocked || false,
        subtasks: []
      };

      targetList.push(quadrantTask);

      // Generate new markdown
      const newContent = generateTasksMarkdown(tasks, tasksContent);
      fs.writeFileSync(tasksFile, newContent, 'utf8');

      console.log(`[Parser] Project copied to ${target} as #${newTaskId}`);

      return {
        success: true,
        message: `Project copied to ${target} as #${newTaskId}`,
        newTaskId: newTaskId
      };
    }

  } catch (error) {
    console.error('[Parser] Copy customer project error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Move a maybe task to a quadrant (cut operation)
 * @param {number} taskId - The task ID to move
 * @param {string} targetQuadrant - Target quadrant (Q1, Q2, Q3, Q4)
 * @returns {Object} Result object with success status and new task ID
 */
async function moveMaybeTaskToQuadrant(taskId, targetQuadrant) {
  try {
    console.log(`[Parser] Moving maybe task ${taskId} to ${targetQuadrant}`);

    const maybeFile = path.join(EISENHOWER_TASKS_DIR, 'maybe.md');
    const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
    
    // Read both files
    const maybeContent = fs.readFileSync(maybeFile, 'utf8');
    const tasksContent = fs.readFileSync(tasksFile, 'utf8');

    // Parse current data
    const maybeData = parseMaybeList(maybeContent);
    const tasks = parseTasks(tasksContent);

    // Find the maybe task to move
    const taskIndex = maybeData.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: `Maybe task ${taskId} not found` };
    }

    const maybeTask = maybeData.tasks[taskIndex];

    // Get target list
    const targetList = tasks[targetQuadrant.toLowerCase()];

    // Calculate new task ID for target quadrant
    let startId = 1;
    if (targetQuadrant === 'Q2') startId = tasks.q1.length + 1;
    else if (targetQuadrant === 'Q3') startId = tasks.q1.length + tasks.q2.length + 1;
    else if (targetQuadrant === 'Q4') startId = tasks.q1.length + tasks.q2.length + tasks.q3.length + 1;

    const newTaskId = startId + targetList.length;

    // Create task for quadrant
    const quadrantTask = {
      id: newTaskId,
      title: maybeTask.title,
      tags: maybeTask.category ? [maybeTask.category] : [],
      quadrant: targetQuadrant,
      status: 'P1',
      priority: 'P1',
      description: maybeTask.description || `Moved from Maybe List`,
      created: new Date().toISOString().split('T')[0],
      updated: new Date().toISOString().split('T')[0],
      blocked: false,
      subtasks: []
    };

    // Add to target quadrant
    targetList.push(quadrantTask);

    // Remove from maybe list
    maybeData.tasks.splice(taskIndex, 1);

    // Generate new markdown for both files
    const newTasksContent = generateTasksMarkdown(tasks, tasksContent);
    const newMaybeContent = generateMaybeMarkdown(maybeData, maybeContent);

    // Write back to files
    fs.writeFileSync(tasksFile, newTasksContent, 'utf8');
    fs.writeFileSync(maybeFile, newMaybeContent, 'utf8');

    console.log(`[Parser] Maybe task moved to ${targetQuadrant} as #${newTaskId}`);

    return {
      success: true,
      message: `Task moved from Maybe List to ${targetQuadrant} as #${newTaskId}`,
      newTaskId: newTaskId
    };

  } catch (error) {
    console.error('[Parser] Move maybe task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Move a task from quadrant to Maybe List
 * @param {number} taskId - The task ID to move
 * @param {string} sourceQuadrant - Source quadrant (Q1, Q2, Q3, Q4)
 * @returns {Object} Result object with success status and new task ID
 */
async function moveQuadrantTaskToMaybe(taskId, sourceQuadrant) {
  try {
    console.log(`[Parser] Moving task ${taskId} from ${sourceQuadrant} to Maybe List`);

    const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
    const maybeFile = path.join(EISENHOWER_TASKS_DIR, 'maybe.md');
    
    // Read both files
    const tasksContent = fs.readFileSync(tasksFile, 'utf8');
    const maybeContent = fs.readFileSync(maybeFile, 'utf8');

    // Parse current data
    const tasks = parseTasks(tasksContent);
    const maybeData = parseMaybeList(maybeContent);

    // Find the task to move
    const sourceList = tasks[sourceQuadrant.toLowerCase()];
    const taskIndex = sourceList.findIndex(t => t.id === taskId);
    
    if (taskIndex === -1) {
      return { success: false, error: `Task ${taskId} not found in ${sourceQuadrant}` };
    }

    const quadrantTask = sourceList[taskIndex];

    // Calculate new task ID for Maybe List (append to end)
    const newTaskId = maybeData.tasks.length + 1;

    // Create maybe task from quadrant task
    const maybeTask = {
      id: newTaskId,
      title: quadrantTask.title,
      status: '待评估',
      description: quadrantTask.description || `Moved from ${sourceQuadrant}`,
      created: new Date().toISOString().split('T')[0],
      category: quadrantTask.tags && quadrantTask.tags.length > 0 ? quadrantTask.tags[0] : 'General'
    };

    // Add to Maybe List
    maybeData.tasks.push(maybeTask);

    // Remove from source quadrant
    sourceList.splice(taskIndex, 1);

    // Generate new markdown for both files
    const newTasksContent = generateTasksMarkdown(tasks, tasksContent);
    const newMaybeContent = generateMaybeMarkdown(maybeData, maybeContent);

    // Write back to files
    fs.writeFileSync(tasksFile, newTasksContent, 'utf8');
    fs.writeFileSync(maybeFile, newMaybeContent, 'utf8');

    console.log(`[Parser] Task moved to Maybe List as #${newTaskId}`);

    return {
      success: true,
      message: `Task moved from ${sourceQuadrant} to Maybe List as #${newTaskId}`,
      newTaskId: newTaskId
    };

  } catch (error) {
    console.error('[Parser] Move task to maybe error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Copy a task from quadrant to Customer Project
 * @param {number} taskId - The task ID to copy
 * @param {string} sourceQuadrant - Source quadrant (Q1, Q2, Q3, Q4)
 * @param {string} targetCustomer - Target customer name
 * @returns {Object} Result object with success status and new project ID
 */
async function copyTaskToCustomer(taskId, sourceQuadrant, targetCustomer) {
  try {
    console.log(`[Parser] Copying task ${taskId} from ${sourceQuadrant} to customer "${targetCustomer}"`);

    const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
    const customerFile = path.join(EISENHOWER_TASKS_DIR, 'customer-projects.md');
    
    // Read both files
    const tasksContent = fs.readFileSync(tasksFile, 'utf8');
    const customerContent = fs.readFileSync(customerFile, 'utf8');

    // Parse current data
    const tasks = parseTasks(tasksContent);
    const customerData = parseCustomerProjects(customerContent);

    // Find the task to copy
    const sourceList = tasks[sourceQuadrant.toLowerCase()];
    const task = sourceList.find(t => t.id === taskId);
    
    if (!task) {
      return { success: false, error: `Task ${taskId} not found in ${sourceQuadrant}` };
    }

    // Find the target customer
    const customer = customerData.customers.find(c => c.name === targetCustomer);
    if (!customer) {
      return { success: false, error: `Customer "${targetCustomer}" not found` };
    }

    // Calculate new project ID (append to end of customer's projects)
    const newProjectId = customer.projects.length + 1;

    // Create customer project from task
    const project = {
      id: newProjectId,
      name: task.title,
      status: '🔵 待开始',
      type: '实施交付',
      priority: task.priority || '中',
      created: new Date().toISOString().split('T')[0],
      lastReview: new Date().toISOString().split('T')[0],
      notes: task.description || `Copied from ${sourceQuadrant} task #${taskId}`,
      quadrantTask: `${sourceQuadrant} #${taskId}`,
      blocked: false
    };

    // Add to customer's projects
    customer.projects.push(project);

    // Generate new markdown
    const newCustomerContent = generateCustomerProjectsMarkdown(customerData, customerContent);

    // Write back to file
    fs.writeFileSync(customerFile, newCustomerContent, 'utf8');

    console.log(`[Parser] Task copied to "${targetCustomer}" as project #${newProjectId}`);

    return {
      success: true,
      message: `Task copied to "${targetCustomer}" as project #${newProjectId}`,
      newProjectId: newProjectId
    };

  } catch (error) {
    console.error('[Parser] Copy task to customer error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Move a task from quadrant to Delegation List
 * @param {number} taskId - The task ID to move
 * @param {string} sourceQuadrant - Source quadrant (Q1, Q2, Q3, Q4)
 * @returns {Object} Result object with success status and new task ID
 */
async function moveTaskToDelegation(taskId, sourceQuadrant) {
  try {
    // Ensure taskId is a number
    const taskIdNum = parseInt(taskId, 10);
    console.log(`[Parser] Moving task ${taskIdNum} from ${sourceQuadrant} to Delegation List`);

    const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
    const delegationFile = path.join(EISENHOWER_TASKS_DIR, 'delegation.md');
    
    // Read both files
    const tasksContent = fs.readFileSync(tasksFile, 'utf8');
    const delegationContent = fs.readFileSync(delegationFile, 'utf8');

    // Parse current data
    const tasks = parseTasks(tasksContent);
    const delegationData = parseDelegation(delegationContent);

    // Find the task to move
    const sourceList = tasks[sourceQuadrant.toLowerCase()];
    const taskIndex = sourceList.findIndex(t => t.id === taskIdNum);
    
    if (taskIndex === -1) {
      return { success: false, error: `Task ${taskIdNum} not found in ${sourceQuadrant}` };
    }

    const quadrantTask = sourceList[taskIndex];

    // Calculate new task ID for Delegation List (append to end)
    const newTaskId = delegationData.tasks.length + 1;

    // Create delegation task from quadrant task
    const delegationTask = {
      id: newTaskId,
      title: quadrantTask.title,
      status: '待开始',
      assignee: '@待定',
      description: quadrantTask.description || `Moved from ${sourceQuadrant}`,
      deadline: '待定',
      created: new Date().toISOString().split('T')[0]
    };

    // Add to Delegation List
    delegationData.tasks.push(delegationTask);

    // Remove from source quadrant
    sourceList.splice(taskIndex, 1);

    // Generate new markdown for both files
    const newTasksContent = generateTasksMarkdown(tasks, tasksContent);
    const newDelegationContent = generateDelegationMarkdown(delegationData, delegationContent);

    // Write back to files
    fs.writeFileSync(tasksFile, newTasksContent, 'utf8');
    fs.writeFileSync(delegationFile, newDelegationContent, 'utf8');

    console.log(`[Parser] Task moved to Delegation List as #${newTaskId}`);

    return {
      success: true,
      message: `Task moved from ${sourceQuadrant} to Delegation List as #${newTaskId}`,
      newTaskId: newTaskId
    };

  } catch (error) {
    console.error('[Parser] Move task to delegation error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Copy a quadrant task to Delegation List (without removing from source)
 * @param {number} taskId - The task ID to copy
 * @param {string} sourceQuadrant - The source quadrant (Q1, Q2, Q3, Q4)
 * @returns {Object} Result object with success status
 */
async function copyTaskToDelegation(taskId, sourceQuadrant) {
  try {
    // Ensure taskId is a number
    const taskIdNum = parseInt(taskId, 10);
    console.log(`[Parser] Copying task ${taskIdNum} from ${sourceQuadrant} to Delegation List`);

    const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
    const delegationFile = path.join(EISENHOWER_TASKS_DIR, 'delegation.md');
    
    // Read both files
    const tasksContent = fs.readFileSync(tasksFile, 'utf8');
    const delegationContent = fs.readFileSync(delegationFile, 'utf8');

    // Parse current data
    const tasks = parseTasks(tasksContent);
    const delegationData = parseDelegation(delegationContent);

    // Find the task to copy
    const sourceList = tasks[sourceQuadrant.toLowerCase()];
    const taskIndex = sourceList.findIndex(t => t.id === taskIdNum);
    
    if (taskIndex === -1) {
      return { success: false, error: `Task ${taskIdNum} not found in ${sourceQuadrant}` };
    }

    const quadrantTask = sourceList[taskIndex];

    // Calculate new task ID for Delegation List (append to end)
    const newTaskId = delegationData.tasks.length + 1;

    // Create delegation task from quadrant task
    const delegationTask = {
      id: newTaskId,
      title: quadrantTask.title,
      status: '待开始',
      assignee: '@待定',
      description: quadrantTask.description || `Copied from ${sourceQuadrant}`,
      deadline: '待定',
      created: new Date().toISOString().split('T')[0]
    };

    // Add to Delegation List
    delegationData.tasks.push(delegationTask);

    // Generate new markdown for delegation file only (source task stays)
    const newDelegationContent = generateDelegationMarkdown(delegationData, delegationContent);

    // Write back to delegation file only
    fs.writeFileSync(delegationFile, newDelegationContent, 'utf8');

    console.log(`[Parser] Task copied to Delegation List as #${newTaskId}`);

    return {
      success: true,
      message: `Task copied from ${sourceQuadrant} to Delegation List as #${newTaskId}`,
      newTaskId: newTaskId
    };

  } catch (error) {
    console.error('[Parser] Copy task to delegation error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Reorder a delegation task within the list
 * @param {number} taskId - The task ID to reorder
 * @param {number} insertIndex - The index to insert at (-1 for end)
 * @returns {Object} Result object with success status
 */
async function reorderDelegationTask(taskId, insertIndex) {
  try {
    console.log(`[Parser] Reordering delegation task ${taskId} to index ${insertIndex}`);

    const delegationFile = path.join(EISENHOWER_TASKS_DIR, 'delegation.md');
    const content = fs.readFileSync(delegationFile, 'utf8');

    // Parse current delegation tasks
    const data = parseDelegation(content);

    // Find the task to reorder
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: `Delegation task ${taskId} not found` };
    }

    // Get the task and remove it from current position
    const task = data.tasks[taskIndex];
    data.tasks.splice(taskIndex, 1);

    // Insert at new position
    if (insertIndex === -1 || insertIndex >= data.tasks.length) {
      data.tasks.push(task);
    } else {
      data.tasks.splice(insertIndex, 0, task);
    }

    // Generate new markdown with renumbered tasks
    const newContent = generateDelegationMarkdown(data, content);

    // Write back to file
    fs.writeFileSync(delegationFile, newContent, 'utf8');

    console.log(`[Parser] Delegation task ${taskId} reordered successfully`);

    return {
      success: true,
      message: `Task reordered successfully`
    };

  } catch (error) {
    console.error('[Parser] Reorder delegation task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Reorder a maybe task within the list
 * @param {number} taskId - The task ID to reorder
 * @param {number} insertIndex - The index to insert at (-1 for end)
 * @returns {Object} Result object with success status
 */
async function reorderMaybeTask(taskId, insertIndex) {
  try {
    console.log(`[Parser] Reordering maybe task ${taskId} to index ${insertIndex}`);

    const maybeFile = path.join(EISENHOWER_TASKS_DIR, 'maybe.md');
    const content = fs.readFileSync(maybeFile, 'utf8');

    // Parse current maybe tasks
    const data = parseMaybeList(content);

    // Find the task to reorder
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: `Maybe task ${taskId} not found` };
    }

    // Get the task and remove it from current position
    const task = data.tasks[taskIndex];
    data.tasks.splice(taskIndex, 1);

    // Insert at new position
    if (insertIndex === -1 || insertIndex >= data.tasks.length) {
      data.tasks.push(task);
    } else {
      data.tasks.splice(insertIndex, 0, task);
    }

    // Generate new markdown with renumbered tasks
    const newContent = generateMaybeMarkdown(data, content);

    // Write back to file
    fs.writeFileSync(maybeFile, newContent, 'utf8');

    console.log(`[Parser] Maybe task ${taskId} reordered successfully`);

    return {
      success: true,
      message: `Task reordered successfully`
    };

  } catch (error) {
    console.error('[Parser] Reorder maybe task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Complete a task from quadrant and move to archive
 * @param {number} taskId - The task ID to complete
 * @param {string} quadrant - The quadrant (Q1, Q2, Q3, Q4)
 * @returns {Object} Result object with success status
 */
async function completeTask(taskId, quadrant) {
  try {
    console.log(`[Parser] Completing task ${taskId} from ${quadrant}`);

    const tasksFile = path.join(EISENHOWER_TASKS_DIR, 'tasks.md');
    const archiveFile = path.join(EISENHOWER_TASKS_DIR, 'archived.md');
    
    // Read files
    const tasksContent = fs.readFileSync(tasksFile, 'utf8');
    let archiveContent = fs.readFileSync(archiveFile, 'utf8');

    // Parse tasks
    const tasks = parseTasks(tasksContent);
    const sourceList = tasks[quadrant.toLowerCase()];
    
    // Find the task
    const taskIndex = sourceList.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: `Task ${taskId} not found in ${quadrant}` };
    }

    const task = sourceList[taskIndex];
    const today = new Date().toISOString().split('T')[0];

    // Calculate next archive ID
    const archiveMatch = archiveContent.match(/####\s+(\d+)\./g);
    let nextArchiveId = 1;
    if (archiveMatch) {
      const ids = archiveMatch.map(m => parseInt(m.match(/\d+/)[0]));
      nextArchiveId = Math.max(...ids) + 1;
    }

    // Build archive entry
    const quadrantNames = {
      'Q1': '第一象限（重要且紧急）',
      'Q2': '第二象限（重要不紧急）',
      'Q3': '第三象限（不重要但紧急）',
      'Q4': '第四象限（不重要不紧急）'
    };

    let archiveEntry = `\n### ${today} 归档\n\n#### ${nextArchiveId}. ${task.title}\n- ✅ 已完成\n- 完成时间：${today}\n- 原象限：${quadrantNames[quadrant] || quadrant}\n- 原优先级：${task.priority || 'P1'}\n- 原编号：任务 #${task.id}\n`;
    if (task.description) {
      archiveEntry += `- 描述：${task.description}\n`;
    }
    if (task.created) {
      archiveEntry += `- 创建：${task.created}\n`;
    }

    // Add to archive
    archiveContent += archiveEntry;

    // Remove from source list
    sourceList.splice(taskIndex, 1);

    // Generate new tasks content
    const newTasksContent = generateTasksMarkdown(tasks, tasksContent);

    // Write files
    fs.writeFileSync(tasksFile, newTasksContent, 'utf8');
    fs.writeFileSync(archiveFile, archiveContent, 'utf8');

    console.log(`[Parser] Task ${taskId} completed and archived`);

    return {
      success: true,
      message: `Task ${taskId} completed and archived`
    };

  } catch (error) {
    console.error('[Parser] Complete task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Complete a customer project and move to archive
 * @param {number} projectId - The project ID to complete
 * @param {string} customerName - The customer name
 * @returns {Object} Result object with success status
 */
async function completeCustomerProject(projectId, customerName) {
  try {
    console.log(`[Parser] Completing project ${projectId} from "${customerName}"`);

    const customerFile = path.join(EISENHOWER_TASKS_DIR, 'customer-projects.md');
    const archiveFile = path.join(EISENHOWER_TASKS_DIR, 'archived.md');
    
    // Read files
    const customerContent = fs.readFileSync(customerFile, 'utf8');
    let archiveContent = fs.readFileSync(archiveFile, 'utf8');

    // Parse customer projects
    const customerData = parseCustomerProjects(customerContent);
    const customer = customerData.customers.find(c => c.name === customerName);
    
    if (!customer) {
      return { success: false, error: `Customer "${customerName}" not found` };
    }

    // Find the project
    const projectIndex = customer.projects.findIndex(p => p.id === projectId);
    if (projectIndex === -1) {
      return { success: false, error: `Project ${projectId} not found in "${customerName}"` };
    }

    const project = customer.projects[projectIndex];
    const today = new Date().toISOString().split('T')[0];

    // Calculate next archive ID
    const archiveMatch = archiveContent.match(/####\s+(\d+)\./g);
    let nextArchiveId = 1;
    if (archiveMatch) {
      const ids = archiveMatch.map(m => parseInt(m.match(/\d+/)[0]));
      nextArchiveId = Math.max(...ids) + 1;
    }

    // Build archive entry
    let archiveEntry = `\n### ${today} 归档\n\n#### ${nextArchiveId}. ${project.name}【${customerName}】\n- ✅ 已完成\n- 完成时间：${today}\n- 原客户：${customerName}\n- 原编号：项目 #${project.id}\n`;
    if (project.type) {
      archiveEntry += `- 类型：${project.type}\n`;
    }
    if (project.notes) {
      archiveEntry += `- 备注：${project.notes}\n`;
    }

    // Add to archive
    archiveContent += archiveEntry;

    // Remove from customer projects
    customer.projects.splice(projectIndex, 1);

    // Generate new customer content
    const newCustomerContent = generateCustomerProjectsMarkdown(customerData, customerContent);

    // Write files
    fs.writeFileSync(customerFile, newCustomerContent, 'utf8');
    fs.writeFileSync(archiveFile, archiveContent, 'utf8');

    console.log(`[Parser] Project ${projectId} completed and archived`);

    return {
      success: true,
      message: `Project ${projectId} completed and archived`
    };

  } catch (error) {
    console.error('[Parser] Complete customer project error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Complete a delegation task and move to archive
 * @param {number} taskId - The task ID to complete
 * @returns {Object} Result object with success status
 */
async function completeDelegationTask(taskId) {
  try {
    console.log(`[Parser] Completing delegation task ${taskId}`);

    const delegationFile = path.join(EISENHOWER_TASKS_DIR, 'delegation.md');
    const archiveFile = path.join(EISENHOWER_TASKS_DIR, 'archived.md');
    
    // Read files
    const delegationContent = fs.readFileSync(delegationFile, 'utf8');
    let archiveContent = fs.readFileSync(archiveFile, 'utf8');

    // Parse delegation tasks
    const delegationData = parseDelegation(delegationContent);
    
    // Find the task
    const taskIndex = delegationData.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: `Delegation task ${taskId} not found` };
    }

    const task = delegationData.tasks[taskIndex];
    const today = new Date().toISOString().split('T')[0];

    // Calculate next archive ID
    const archiveMatch = archiveContent.match(/####\s+(\d+)\./g);
    let nextArchiveId = 1;
    if (archiveMatch) {
      const ids = archiveMatch.map(m => parseInt(m.match(/\d+/)[0]));
      nextArchiveId = Math.max(...ids) + 1;
    }

    // Build archive entry
    let archiveEntry = `\n### ${today} 归档\n\n#### ${nextArchiveId}. ${task.title}【委派】${task.assignee ? `- ${task.assignee}` : ''}\n- ✅ 已完成\n- 完成时间：${today}\n- 原清单：委派清单\n- 原编号：任务 #${task.id}\n`;
    if (task.assignee) {
      archiveEntry += `- 责任人：${task.assignee}\n`;
    }
    if (task.description) {
      archiveEntry += `- 说明：${task.description}\n`;
    }

    // Add to archive
    archiveContent += archiveEntry;

    // Remove from delegation list
    delegationData.tasks.splice(taskIndex, 1);

    // Generate new delegation content
    const newDelegationContent = generateDelegationMarkdown(delegationData, delegationContent);

    // Write files
    fs.writeFileSync(delegationFile, newDelegationContent, 'utf8');
    fs.writeFileSync(archiveFile, archiveContent, 'utf8');

    console.log(`[Parser] Delegation task ${taskId} completed and archived`);

    return {
      success: true,
      message: `Delegation task ${taskId} completed and archived`
    };

  } catch (error) {
    console.error('[Parser] Complete delegation task error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Complete a maybe task and move to archive
 * @param {number} taskId - The task ID to complete
 * @returns {Object} Result object with success status
 */
async function completeMaybeTask(taskId) {
  try {
    console.log(`[Parser] Completing maybe task ${taskId}`);

    const maybeFile = path.join(EISENHOWER_TASKS_DIR, 'maybe.md');
    const archiveFile = path.join(EISENHOWER_TASKS_DIR, 'archived.md');
    
    // Read files
    const maybeContent = fs.readFileSync(maybeFile, 'utf8');
    let archiveContent = fs.readFileSync(archiveFile, 'utf8');

    // Parse maybe tasks
    const maybeData = parseMaybeList(maybeContent);
    
    // Find the task
    const taskIndex = maybeData.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: `Maybe task ${taskId} not found` };
    }

    const task = maybeData.tasks[taskIndex];
    const today = new Date().toISOString().split('T')[0];

    // Calculate next archive ID
    const archiveMatch = archiveContent.match(/####\s+(\d+)\./g);
    let nextArchiveId = 1;
    if (archiveMatch) {
      const ids = archiveMatch.map(m => parseInt(m.match(/\d+/)[0]));
      nextArchiveId = Math.max(...ids) + 1;
    }

    // Build archive entry
    let archiveEntry = `\n### ${today} 归档\n\n#### ${nextArchiveId}. ${task.title}【未来清单】\n- ✅ 已完成\n- 完成时间：${today}\n- 原清单：未来清单 (Maybe List)\n- 原编号：任务 #${task.id}\n`;
    if (task.category) {
      archiveEntry += `- 分类：${task.category}\n`;
    }
    if (task.description) {
      archiveEntry += `- 说明：${task.description}\n`;
    }

    // Add to archive
    archiveContent += archiveEntry;

    // Remove from maybe list
    maybeData.tasks.splice(taskIndex, 1);

    // Generate new maybe content
    const newMaybeContent = generateMaybeMarkdown(maybeData, maybeContent);

    // Write files
    fs.writeFileSync(maybeFile, newMaybeContent, 'utf8');
    fs.writeFileSync(archiveFile, archiveContent, 'utf8');

    console.log(`[Parser] Maybe task ${taskId} completed and archived`);

    return {
      success: true,
      message: `Maybe task ${taskId} completed and archived`
    };

  } catch (error) {
    console.error('[Parser] Complete maybe task error:', error);
    return { success: false, error: error.message };
  }
}

module.exports = {
  loadAllTasks,
  parseTasks,
  parseCustomerProjects,
  parseDelegation,
  parseMaybeList,
  moveTask,
  moveCustomerProject,
  deleteTask,
  deleteCustomerProject,
  deleteDelegationTask,
  deleteMaybeTask,
  copyTask,
  copyCustomerProject,
  moveMaybeTaskToQuadrant,
  moveQuadrantTaskToMaybe,
  copyTaskToCustomer,
  moveTaskToDelegation,
  copyTaskToDelegation,
  reorderDelegationTask,
  reorderMaybeTask,
  completeTask,
  completeCustomerProject,
  completeDelegationTask,
  completeMaybeTask
};
