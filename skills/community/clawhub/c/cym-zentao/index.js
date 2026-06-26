import { readFileSync } from 'fs';
import { join } from 'path';

function loadConfig() {
  const toolsPath = join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace', 'TOOLS.md');
  const content = readFileSync(toolsPath, 'utf-8');
  const section = content.match(/## 禅道 API \(ZenTao API\)([\s\S]*?)(?=##|$)/)?.[1];
  if (!section) throw new Error('未找到禅道 API 配置');
  
  const apiUrl = section.match(/API 地址[:：]\s*(.+)/)?.[1]?.trim()?.replace(/\*\*/g, '').trim();
  const username = section.match(/用户名[:：]\s*(.+)/)?.[1]?.trim()?.replace(/\*\*/g, '').trim();
  const password = section.match(/密码[:：]\s*(.+)/)?.[1]?.trim()?.replace(/\*\*/g, '').trim();
  
  if (!apiUrl || !username || !password) throw new Error('禅道 API 配置不完整');
  
  return { apiUrl: apiUrl.replace(/\/$/, ''), username, password };
}

async function getToken(config) {
  const res = await fetch(`${config.apiUrl}/api.php/v1/tokens`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ account: config.username, password: config.password })
  });
  if (!res.ok) throw new Error(`登录失败: ${res.status}`);
  const data = await res.json();
  if (!data.token) throw new Error('未获取到 token');
  return data.token;
}

async function findExecutionByName(config, token, name) {
  let page = 1;
  while (page <= 10) {
    const res = await fetch(`${config.apiUrl}/api.php/v1/executions?page=${page}&limit=100`, {
      headers: { 'Content-Type': 'application/json', 'token': token }
    });
    if (!res.ok) throw new Error(`获取执行列表失败: ${res.status}`);
    const data = await res.json();
    if (!data.executions?.length) break;
    
    const match = data.executions.find(e => e.name?.includes(name));
    if (match) return match;
    page++;
  }
  return null;
}

export async function zentao_login() {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    return { success: true, token, message: '登录成功' };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export async function zentao_list_executions(keyword = '') {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    const executions = [];
    let page = 1;
    
    while (page <= 10) {
      const res = await fetch(`${config.apiUrl}/api.php/v1/executions?page=${page}&limit=100`, {
        headers: { 'Content-Type': 'application/json', 'token': token }
      });
      if (!res.ok) throw new Error(`获取失败: ${res.status}`);
      const data = await res.json();
      if (!data.executions?.length) break;
      
      if (keyword) {
        executions.push(...data.executions.filter(e => e.name?.includes(keyword) || String(e.project || '').includes(keyword)));
      } else {
        executions.push(...data.executions);
      }
      page++;
    }
    
    return { success: true, count: executions.length, executions: executions.map(e => ({ id: e.id, name: e.name, project: e.project, status: e.status, begin: e.begin, end: e.end })) };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export async function zentao_create_task(executionIdOrName, name, assignedTo, options = {}) {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    
    // 判断是ID还是名称
    let executionId = executionIdOrName;
    if (isNaN(parseInt(executionIdOrName))) {
      // 是名称，需要查找
      const execution = await findExecutionByName(config, token, executionIdOrName);
      if (!execution) throw new Error(`未找到执行: ${executionIdOrName}`);
      executionId = execution.id;
    } else {
      executionId = parseInt(executionIdOrName);
    }
    
    const tomorrow = new Date(); tomorrow.setDate(tomorrow.getDate() + 1);
    const dayAfter = new Date(); dayAfter.setDate(dayAfter.getDate() + 2);
    const fmt = d => d.toISOString().split('T')[0];
    
    const taskData = {
      name, assignedTo,
      pri: options.pri || 3,
      estimate: options.estimate || 6,
      type: options.type || 'test',
      estStarted: options.estStarted || fmt(tomorrow),
      deadline: options.deadline || fmt(dayAfter),
      desc: options.desc || ''
    };
    
    const res = await fetch(`${config.apiUrl}/api.php/v1/executions/${executionId}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'token': token },
      body: JSON.stringify(taskData)
    });
    
    if (!res.ok) throw new Error(`创建失败: ${await res.text()}`);
    const result = await res.json();
    return { success: true, taskId: result.id, name: result.name, assignedTo: result.assignedTo, message: `任务创建成功！ID: ${result.id}` };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export async function zentao_list_tasks(executionIdOrName, status = '') {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    
    // 判断是ID还是名称
    let executionId = executionIdOrName;
    if (isNaN(parseInt(executionIdOrName))) {
      // 是名称，需要查找
      const execution = await findExecutionByName(config, token, executionIdOrName);
      if (!execution) throw new Error(`未找到执行: ${executionIdOrName}`);
      executionId = execution.id;
    } else {
      executionId = parseInt(executionIdOrName);
    }
    
    let url = `${config.apiUrl}/api.php/v1/executions/${executionId}/tasks`;
    if (status) url += `?status=${status}`;
    
    const res = await fetch(url, { headers: { 'Content-Type': 'application/json', 'token': token } });
    if (!res.ok) throw new Error(`获取失败: ${res.status}`);
    const data = await res.json();
    const tasks = data.tasks || [];
    
    return { success: true, count: tasks.length, tasks: tasks.map(t => ({ id: t.id, name: t.name, assignedTo: t.assignedTo, status: t.status, pri: t.pri, estimate: t.estimate, consumed: t.consumed, left: t.left })) };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export default { zentao_login, zentao_list_executions, zentao_create_task, zentao_list_tasks };
