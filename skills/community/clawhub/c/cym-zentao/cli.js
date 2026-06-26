#!/usr/bin/env node
import { readFileSync } from 'fs';
import { join, resolve } from 'path';

const args = process.argv.slice(2);
const command = args[0];

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
  // 禅道 API 路径格式: /zentao/api.php/v1/tokens
  const apiPath = config.apiUrl.endsWith('/zentao') ? '/api.php/v1/tokens' : '/zentao/api.php/v1/tokens';
  const res = await fetch(`${config.apiUrl}${apiPath}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ account: config.username, password: config.password })
  });
  if (!res.ok) throw new Error(`登录失败: ${res.status}`);
  const data = await res.json();
  if (!data.token) throw new Error('未获取到 token');
  return data.token;
}

async function login() {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    console.log(JSON.stringify({ success: true, token, message: '登录成功' }));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

async function listExecutions(keyword = '') {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    const executions = [];
    let page = 1;
    
    // 禅道 API 路径格式
    const apiPath = config.apiUrl.endsWith('/zentao') ? '/api.php/v1/executions' : '/zentao/api.php/v1/executions';
    
    while (page <= 10) {
      const res = await fetch(`${config.apiUrl}${apiPath}?page=${page}&limit=100`, {
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
    
    console.log(JSON.stringify({ success: true, count: executions.length, executions: executions.map(e => ({ id: e.id, name: e.name, project: e.project, status: e.status, begin: e.begin, end: e.end })) }));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

async function findExecutionByName(config, token, name) {
  let page = 1;
  // 禅道 API 路径格式
  const apiPath = config.apiUrl.endsWith('/zentao') ? '/api.php/v1/executions' : '/zentao/api.php/v1/executions';
  
  while (page <= 10) {
    const res = await fetch(`${config.apiUrl}${apiPath}?page=${page}&limit=100`, {
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

async function createTask(executionIdOrName, name, assignedTo, options = {}) {
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
    
    // 禅道 API 路径格式
    const apiPath = config.apiUrl.endsWith('/zentao') ? `/api.php/v1/executions/${executionId}/tasks` : `/zentao/api.php/v1/executions/${executionId}/tasks`;
    const res = await fetch(`${config.apiUrl}${apiPath}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'token': token },
      body: JSON.stringify(taskData)
    });
    
    if (!res.ok) throw new Error(`创建失败: ${await res.text()}`);
    const result = await res.json();
    console.log(JSON.stringify({ success: true, taskId: result.id, name: result.name, assignedTo: result.assignedTo, message: `任务创建成功！ID: ${result.id}` }));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

async function listTasks(executionIdOrName, status = '') {
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
    
    // 禅道 API 路径格式
    const apiPath = config.apiUrl.endsWith('/zentao') ? `/api.php/v1/executions/${executionId}/tasks` : `/zentao/api.php/v1/executions/${executionId}/tasks`;
    let url = `${config.apiUrl}${apiPath}`;
    if (status) url += `?status=${status}`;
    
    const res = await fetch(url, { headers: { 'Content-Type': 'application/json', 'token': token } });
    if (!res.ok) throw new Error(`获取失败: ${res.status}`);
    const data = await res.json();
    const tasks = data.tasks || [];
    
    console.log(JSON.stringify({ success: true, count: tasks.length, tasks: tasks.map(t => ({ id: t.id, name: t.name, assignedTo: t.assignedTo, status: t.status, pri: t.pri, estimate: t.estimate, consumed: t.consumed, left: t.left })) }));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

async function createTasksBatch(executionIdOrName, tasksFile) {
  try {
    const config = loadConfig();
    const token = await getToken(config);
    
    // 判断是ID还是名称
    let executionId = executionIdOrName;
    if (isNaN(parseInt(executionIdOrName))) {
      const execution = await findExecutionByName(config, token, executionIdOrName);
      if (!execution) throw new Error(`未找到执行: ${executionIdOrName}`);
      executionId = execution.id;
    } else {
      executionId = parseInt(executionIdOrName);
    }
    
    // 读取任务文件
    const fileContent = readFileSync(tasksFile, 'utf-8');
    const tasks = JSON.parse(fileContent);
    
    if (!Array.isArray(tasks) || tasks.length === 0) {
      throw new Error('任务文件必须是包含至少一个任务的数组');
    }
    
    const results = [];
    const errors = [];
    
    for (let i = 0; i < tasks.length; i++) {
      const task = tasks[i];
      try {
        if (!task.name || !task.assignedTo) {
          throw new Error('任务必须包含 name 和 assignedTo');
        }
        
        const taskData = {
          name: task.name,
          assignedTo: task.assignedTo,
          pri: task.pri || 3,
          estimate: task.estimate || 6,
          type: task.type || 'test',
          estStarted: task.estStarted || '',
          deadline: task.deadline || '',
          desc: task.desc || ''
        };
        
        // 禅道 API 路径格式
        const apiPath = config.apiUrl.endsWith('/zentao') ? `/api.php/v1/executions/${executionId}/tasks` : `/zentao/api.php/v1/executions/${executionId}/tasks`;
        const res = await fetch(`${config.apiUrl}${apiPath}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json; charset=utf-8', 'token': token },
          body: JSON.stringify(taskData)
        });
        
        if (!res.ok) {
          const errorText = await res.text();
          throw new Error(`创建失败: ${errorText}`);
        }
        
        const result = await res.json();
        results.push({ index: i + 1, taskId: result.id, name: result.name, assignedTo: result.assignedTo });
      } catch (error) {
        errors.push({ index: i + 1, name: task.name, error: error.message });
      }
    }
    
    console.log(JSON.stringify({ 
      success: true, 
      total: tasks.length,
      created: results.length,
      failed: errors.length,
      results,
      errors
    }));
  } catch (error) {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exit(1);
  }
}

// CLI 路由
switch (command) {
  case 'login':
    await login();
    break;
  case 'list-executions':
    await listExecutions(args[1] || '');
    break;
  case 'create-task':
    if (args.length < 4) {
      console.error('用法: cym-zentao create-task <executionId|executionName> <name> <assignedTo> [options]');
      process.exit(1);
    }
    let options = {};
    if (args[4]) {
      const optsStr = args[4].trim();
      if (optsStr.startsWith('{')) {
        options = JSON.parse(optsStr);
      } else if (optsStr.startsWith('@')) {
        // 从文件读取
        const filePath = optsStr.slice(1);
        const fileContent = readFileSync(filePath, 'utf-8');
        options = JSON.parse(fileContent);
      }
    }
    await createTask(args[1], args[2], args[3], options);
    break;
  case 'list-tasks':
    if (args.length < 2) {
      console.error('用法: cym-zentao list-tasks <executionId|executionName> [status]');
      process.exit(1);
    }
    await listTasks(args[1], args[2] || '');
    break;
  case 'create-tasks-batch':
    if (args.length < 3) {
      console.error('用法: cym-zentao create-tasks-batch <executionId|executionName> <tasksFile>');
      process.exit(1);
    }
    await createTasksBatch(args[1], args[2]);
    break;
  default:
    console.log(`
禅道项目管理 CLI

用法:
  cym-zentao login                          测试登录
  cym-zentao list-executions [keyword]      列出执行
  cym-zentao create-task <executionId|executionName> <name> <assignedTo> [options]  创建任务
  cym-zentao create-tasks-batch <executionId|executionName> <tasksFile>  批量创建任务
  cym-zentao list-tasks <executionId|executionName> [status]  列出任务

示例:
  cym-zentao list-executions "日常任务"
  cym-zentao create-task 6159 "测试功能" "陈跃美"
  cym-zentao create-task "日常事务-郑太相" "测试功能" "陈跃美"
  cym-zentao create-task 6159 "测试功能" "陈跃美" '{"pri":2,"estimate":8}'
  cym-zentao create-tasks-batch "日常事务-郑太相" tasks.json
  cym-zentao list-tasks "日常事务-郑太相"
`);
    process.exit(1);
}
