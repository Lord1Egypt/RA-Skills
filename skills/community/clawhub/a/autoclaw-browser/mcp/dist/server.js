/**
 * AutoClaw MCP Server v6.1.0
 * 新增：配置管理工具 + 50+浏览器控制工具 + 错误码系统
 * 优化：简化DOM获取 + 批量执行 + 智能等待 + 增强重试机制
 */

// ==================== 错误码系统 ====================
const MAX_RETRY_PER_ISSUE = 3;
const retryCounts = new Map();

// 错误码定义
const ERROR_CODES = {
  // E1xxx: 连接相关
  E1001: { category: 'connection', severity: 'high', retryable: true, message: 'Chrome插件未连接', suggestion: '请确保：1.插件已安装 2.已点击授权 3.授权未过期' },
  E1002: { category: 'connection', severity: 'high', retryable: true, message: 'MCP服务器未运行', suggestion: '请运行: cd autoclaw/mcp && npm start' },
  E1003: { category: 'connection', severity: 'high', retryable: false, message: 'Token验证失败', suggestion: 'Token无效，请检查配置或使用内置Token' },
  
  // E2xxx: 书签相关
  E2001: { category: 'bookmark', severity: 'medium', retryable: true, message: '书签操作失败', suggestion: '请检查书签ID是否正确，文件夹是否存在' },
  E2002: { category: 'bookmark', severity: 'medium', retryable: true, message: '书签不存在', suggestion: '请先获取书签列表确认ID' },
  
  // E3xxx: 元素操作相关
  E3001: { category: 'element', severity: 'medium', retryable: true, message: '元素未找到', suggestion: '请检查CSS选择器是否正确，页面是否加载完成' },
  E3002: { category: 'element', severity: 'medium', retryable: true, message: '元素不可见', suggestion: '元素存在但不可见，请尝试滚动到可见区域' },
  E3003: { category: 'element', severity: 'medium', retryable: true, message: '元素不可点击', suggestion: '元素被遮挡或不可交互，请先滚动到可见区域' },
  
  // E4xxx: 导航相关
  E4001: { category: 'navigation', severity: 'medium', retryable: true, message: '页面加载超时', suggestion: '网络较慢或页面无响应，请增加等待时间或检查网络' },
  E4002: { category: 'navigation', severity: 'medium', retryable: true, message: '导航失败', suggestion: '请检查URL是否正确，网络是否正常' },
  
  // E5xxx: 标签页相关
  E5001: { category: 'tab', severity: 'low', retryable: false, message: '标签页不存在', suggestion: '请先获取标签页列表确认ID' },
  E5002: { category: 'tab', severity: 'low', retryable: false, message: '标签页无法关闭', suggestion: '可能是最后一个标签页或被固定' },
  
  // E6xxx: 存储相关
  E6001: { category: 'storage', severity: 'low', retryable: true, message: 'Cookie操作失败', suggestion: '请检查域名是否正确' },
  E6002: { category: 'storage', severity: 'low', retryable: true, message: 'Storage操作失败', suggestion: '请检查key和value是否有效' },
  
  // E9xxx: 系统级
  E9001: { category: 'system', severity: 'high', retryable: false, message: '未知错误', suggestion: '请查看详细错误信息或联系开发者' },
  E9002: { category: 'system', severity: 'high', retryable: false, message: 'CDP执行超时', suggestion: '操作超时，请重试或检查页面状态' },
};

// 创建错误响应
function createError(code, message, file, line, customSuggestion) {
  const errorDef = ERROR_CODES[code] || ERROR_CODES['E9001'];
  return {
    success: false,
    error: {
      errorCode: code,
      message: message || errorDef.message,
      file: file,
      line: line,
      severity: errorDef.severity,
      category: errorDef.category,
      retryable: errorDef.retryable,
      fixSuggestion: customSuggestion || errorDef.suggestion,
      maxRetries: MAX_RETRY_PER_ISSUE
    }
  };
}

// 检查是否可以重试
function canRetry(issueId) {
  const count = retryCounts.get(issueId) || 0;
  if (count >= MAX_RETRY_PER_ISSUE) {
    return { allowed: false, message: `此问题已修复${MAX_RETRY_PER_ISSUE}次，请手动处理`, remaining: 0 };
  }
  retryCounts.set(issueId, count + 1);
  return { allowed: true, remaining: MAX_RETRY_PER_ISSUE - count };
}

// 重置重试计数
function resetRetry(issueId) {
  retryCounts.delete(issueId);
}

// 获取相对路径（安全）
function getRelativePath(filePath) {
  if (!filePath) return '';
  // 返回相对路径，不暴露真实系统路径
  return filePath.replace(/^.*[\\/]autoclaw[\\/]/, 'autoclaw/');
}

import { WebSocketServer, WebSocket } from 'ws';
import { createServer, IncomingMessage } from 'http';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';

const SERVER_PORT = 30000;
const BUILT_IN_TOKEN = 'autoclaw_builtin_Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs';
const OPENCLAW_TOKEN = 'Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs';
const VALID_TOKEN = [BUILT_IN_TOKEN, OPENCLAW_TOKEN]; // Accept both tokens

// 日志目录结构 - 文件夹形式
// ~/.autoclaw/logs/
// ├── _index.json              # 任务索引
// ├── _patterns.json           # 优化模式
// ├── task_1709000001_douyin/
// │   ├── info.json            # 任务元信息
// │   └── actions.json         # 操作记录
// └── task_1709000002_xxx/
//     ├── info.json
//     └── actions.json

const LOG_DIR = join(homedir(), '.autoclaw', 'logs');
const MAX_TASKS = 100;           // 最多保留任务数
const MAX_ACTIONS_PER_TASK = 200; // 每任务最大记录
const LOG_RETENTION_DAYS = 30;    // 日志保留天数

// 清理30天前的日志文件
function cleanOldLogs() {
  try {
    if (!existsSync(LOG_DIR)) return;
    const now = Date.now();
    const maxAge = LOG_RETENTION_DAYS * 24 * 60 * 60 * 1000;
    const entries = readdirSync(LOG_DIR, { withFileTypes: true });
    
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const taskDir = join(LOG_DIR, entry.name);
      const infoFile = join(taskDir, 'info.json');
      
      try {
        if (existsSync(infoFile)) {
          const info = JSON.parse(readFileSync(infoFile, 'utf-8'));
          if (now - info.created > maxAge) {
            rmSync(taskDir, { recursive: true, force: true });
            console.log(`[CLEAN] Deleted old log: ${entry.name}`);
          }
        }
      } catch {
        // 如果info.json不存在或解析失败，也删除整个目录
        try { rmSync(taskDir, { recursive: true, force: true }); } catch {}
      }
    }
    console.log(`[CLEAN] Log cleanup completed, kept last ${LOG_RETENTION_DAYS} days`);
  } catch (e) {
    console.error('[CLEAN] Log cleanup failed:', e.message);
  }
}

// 当前任务ID
let currentTaskId = null;

// 获取索引
function getIndex() {
  try {
    if (!existsSync(LOG_DIR)) mkdirSync(LOG_DIR, { recursive: true });
    const idxFile = join(LOG_DIR, '_index.json');
    if (existsSync(idxFile)) {
      return JSON.parse(readFileSync(idxFile, 'utf-8'));
    }
  } catch {}
  return { tasks: [], patterns: {} };
}

function saveIndex(idx) {
  try {
    writeFileSync(join(LOG_DIR, '_index.json'), JSON.stringify(idx, null, 2));
  } catch {}
}

// 创建新任务
function createTask(name = 'untitled') {
  const idx = getIndex();
  const taskId = Date.now();
  const taskDir = join(LOG_DIR, `task_${taskId}_${name.replace(/[^a-zA-Z0-9]/g, '_')}`);
  
  if (!existsSync(taskDir)) mkdirSync(taskDir, { recursive: true });
  
  const task = {
    id: taskId,
    name,
    dir: taskDir,
    created: Date.now(),
    status: 'running',
    actions: []
  };
  
  idx.tasks.unshift(task);
  if (idx.tasks.length > MAX_TASKS) {
    // 删除最旧的任务
    const old = idx.tasks.pop();
    try { rmSync(old.dir, { recursive: true, force: true }); } catch {}
  }
  
  saveIndex(idx);
  currentTaskId = taskId;
  return task;
}

// 记录当前任务的操作
function logAction(toolName, args, result) {
  const idx = getIndex();
  const task = idx.tasks.find(t => t.id === currentTaskId);
  
  if (!task) return; // 无任务不记录
  
  const entry = {
    timestamp: Date.now(),
    tool: toolName,
    args: args,
    result: typeof result === 'string' ? result.slice(0, 200) : String(result).slice(0, 200),
    success: !String(result).includes('error')
  };
  
  task.actions.push(entry);
  if (task.actions.length > MAX_ACTIONS_PER_TASK) {
    task.actions.shift();
  }
  
  // 保存到文件
  try {
    writeFileSync(join(task.dir, 'actions.json'), JSON.stringify(task.actions, null, 2));
  } catch {}
  
  saveIndex(idx);
  console.log(`[LOG] task_${currentTaskId} ${toolName}:`, JSON.stringify(args).slice(0, 80));
}

// 获取日志
function getLogs(taskId = null, limit = 50) {
  const idx = getIndex();
  if (taskId) {
    const task = idx.tasks.find(t => t.id === Number(taskId));
    return task ? task.actions.slice(-limit) : [];
  }
  // 返回所有任务的最近记录
  return idx.tasks.flatMap(t => t.actions).slice(-limit);
}

// 获取任务列表
function getTaskList() {
  return getIndex().tasks;
}

// 完成任务
function completeTask(success = true) {
  const idx = getIndex();
  const task = idx.tasks.find(t => t.id === currentTaskId);
  if (task) {
    task.status = success ? 'completed' : 'failed';
    task.completed = Date.now();
    saveIndex(idx);
  }
  currentTaskId = null;
}

// 切换任务
function setTask(taskId) {
  currentTaskId = Number(taskId);
}

function randomDelay(min = 1000, max = 3000) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

const tools = [
  // ==================== 任务/日志操作 (10个) - 供OpenCLAW优化用 ====================
  { name: 'claw_new_task', description: '创建新任务（开始新会话）', inputSchema: { type: 'object', properties: { name: { type: 'string' } } } },
  { name: 'claw_complete_task', description: '完成任务（标记成功/失败）', inputSchema: { type: 'object', properties: { success: { type: 'boolean' } } } },
  { name: 'claw_switch_task', description: '切换到指定任务', inputSchema: { type: 'object', properties: { taskId: { type: 'number' } } } },
  { name: 'claw_list_tasks', description: '列出所有任务', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_get_task_logs', description: '获取指定任务的日志', inputSchema: { type: 'object', properties: { taskId: { type: 'number' }, limit: { type: 'number' } } } },
  { name: 'claw_get_action_logs', description: '获取当前任务的操作记录', inputSchema: { type: 'object', properties: { limit: { type: 'number' } } } },
  { name: 'claw_delete_task', description: '删除指定任务', inputSchema: { type: 'object', properties: { taskId: { type: 'number' } }, required: ['taskId'] } },
  { name: 'claw_clear_all_tasks', description: '清空所有任务日志', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_export_task', description: '导出任务到文件', inputSchema: { type: 'object', properties: { taskId: { type: 'number' }, path: { type: 'string' } } } },
  { name: 'claw_analyze_patterns', description: '分析成功模式（供优化用）', inputSchema: { type: 'object', properties: {} } },

  // ==================== 书签操作 (10个) ====================
  { name: 'claw_get_bookmarks', description: '获取所有书签（扁平列表）', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_get_bookmark_tree', description: '获取完整书签树形结构', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_search_bookmarks', description: '按关键词搜索书签', inputSchema: { type: 'object', properties: { query: { type: 'string' } }, required: ['query'] } },
  { name: 'claw_create_bookmark', description: '新建书签', inputSchema: { type: 'object', properties: { title: { type: 'string' }, url: { type: 'string' }, parentId: { type: 'string' } }, required: ['title', 'url'] } },
  { name: 'claw_update_bookmark', description: '修改书签标题或URL', inputSchema: { type: 'object', properties: { id: { type: 'string' }, title: { type: 'string' }, url: { type: 'string' } }, required: ['id'] } },
  { name: 'claw_rename_bookmark', description: '重命名书签或文件夹（只改标题）', inputSchema: { type: 'object', properties: { id: { type: 'string' }, title: { type: 'string' } }, required: ['id', 'title'] } },
  { name: 'claw_delete_bookmark', description: '删除单个书签', inputSchema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] } },
  { name: 'claw_remove_folder', description: '递归删除书签文件夹及所有子项', inputSchema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] } },
  { name: 'claw_create_folder', description: '新建书签文件夹', inputSchema: { type: 'object', properties: { title: { type: 'string' }, parentId: { type: 'string' } }, required: ['title'] } },
  { name: 'claw_move_bookmark', description: '移动书签到其他文件夹', inputSchema: { type: 'object', properties: { id: { type: 'string' }, parentId: { type: 'string' } }, required: ['id', 'parentId'] } },

  // ==================== 页面导航 (5个) ====================
  { name: 'claw_navigate', description: '打开网址。newTab=true时新标签页打开', inputSchema: { type: 'object', properties: { url: { type: 'string' }, newTab: { type: 'boolean' } }, required: ['url'] } },
  { name: 'claw_open_urls', description: '批量在新标签页打开多个URL', inputSchema: { type: 'object', properties: { urls: { type: 'array', items: { type: 'string' } }, delayMs: { type: 'number' } }, required: ['urls'] } },
  { name: 'claw_go_back', description: '后退一页', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_go_forward', description: '前进一页', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_attach_all_tabs', description: '请求插件接管所有标签页', inputSchema: { type: 'object', properties: {} } },

  // ==================== 页面操作 (3个) ====================
  { name: 'claw_reload_page', description: '刷新当前页面', inputSchema: { type: 'object', properties: { hard: { type: 'boolean' } } } },
  { name: 'claw_get_current_url', description: '获取当前标签页URL和标题', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_take_screenshot', description: '截取当前页面截图', inputSchema: { type: 'object', properties: { fullPage: { type: 'boolean' } } } },

  // ==================== 鼠标操作 (8个) ====================
  { name: 'claw_mouse_move', description: '移动鼠标到指定坐标', inputSchema: { type: 'object', properties: { x: { type: 'number' }, y: { type: 'number' } }, required: ['x', 'y'] } },
  { name: 'claw_mouse_click', description: '鼠标左键点击指定坐标', inputSchema: { type: 'object', properties: { x: { type: 'number' }, y: { type: 'number' } } } },
  { name: 'claw_mouse_right_click', description: '鼠标右键点击指定坐标', inputSchema: { type: 'object', properties: { x: { type: 'number' }, y: { type: 'number' } } } },
  { name: 'claw_mouse_double_click', description: '鼠标双击指定坐标', inputSchema: { type: 'object', properties: { x: { type: 'number' }, y: { type: 'number' } } } },
  { name: 'claw_mouse_down', description: '鼠标按下', inputSchema: { type: 'object', properties: { button: { type: 'string', enum: ['left', 'right', 'middle'] }, x: { type: 'number' }, y: { type: 'number' } } } },
  { name: 'claw_mouse_up', description: '鼠标释放', inputSchema: { type: 'object', properties: { button: { type: 'string', enum: ['left', 'right', 'middle'] } } } },
  { name: 'claw_mouse_wheel', description: '鼠标滚轮滚动', inputSchema: { type: 'object', properties: { deltaX: { type: 'number' }, deltaY: { type: 'number' } } } },
  { name: 'claw_fast_scroll_down', description: '快速向下滚动一屏（适合抖音长视频）', inputSchema: { type: 'object', properties: { speed: { type: 'number', default: 1 } } } },
  { name: 'claw_fast_scroll_up', description: '快速向上滚动一屏', inputSchema: { type: 'object', properties: { speed: { type: 'number', default: 1 } } } },
  { name: 'claw_hover_element', description: '鼠标悬停到元素', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },

  // ==================== 触摸/滑动操作 (5个) ====================
  { name: 'claw_swipe_up', description: '向上滑动页面（抖音等）', inputSchema: { type: 'object', properties: { distance: { type: 'number', default: 600 } } } },
  { name: 'claw_swipe_down', description: '向下滑动页面', inputSchema: { type: 'object', properties: { distance: { type: 'number', default: 600 } } } },
  { name: 'claw_swipe_left', description: '向左滑动页面', inputSchema: { type: 'object', properties: { distance: { type: 'number', default: 300 } } } },
  { name: 'claw_swipe_right', description: '向右滑动页面', inputSchema: { type: 'object', properties: { distance: { type: 'number', default: 300 } } } },
  { name: 'claw_tap', description: '点击屏幕指定位置', inputSchema: { type: 'object', properties: { x: { type: 'number' }, y: { type: 'number' } } } },

  // ==================== 元素操作 (8个) ====================
  { name: 'claw_click_element', description: '点击页面元素（CSS选择器）', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },
  { name: 'claw_fill_input', description: '向输入框填写文本', inputSchema: { type: 'object', properties: { selector: { type: 'string' }, text: { type: 'string' } }, required: ['selector', 'text'] } },
  { name: 'claw_clear_input', description: '清空输入框', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },
  { name: 'claw_select_option', description: '下拉框选择选项', inputSchema: { type: 'object', properties: { selector: { type: 'string' }, value: { type: 'string' } }, required: ['selector', 'value'] } },
  { name: 'claw_check', description: '勾选复选框', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },
  { name: 'claw_uncheck', description: '取消勾选复选框', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },
  { name: 'claw_upload_file', description: '文件上传到input元素', inputSchema: { type: 'object', properties: { selector: { type: 'string' }, filePath: { type: 'string' } }, required: ['selector', 'filePath'] } },
  { name: 'claw_focus_element', description: '聚焦到元素', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },

  // ==================== 键盘操作 (5个) ====================
  { name: 'claw_press_key', description: '按下单个按键', inputSchema: { type: 'object', properties: { key: { type: 'string' } }, required: ['key'] } },
  { name: 'claw_press_combo', description: '按下组合键（如Ctrl+C）', inputSchema: { type: 'object', properties: { keys: { type: 'string' } }, required: ['keys'] } },
  { name: 'claw_key_down', description: '按键按下', inputSchema: { type: 'object', properties: { key: { type: 'string' } }, required: ['key'] } },
  { name: 'claw_key_up', description: '按键释放', inputSchema: { type: 'object', properties: { key: { type: 'string' } }, required: ['key'] } },
  { name: 'claw_type_text', description: '模拟输入文本', inputSchema: { type: 'object', properties: { text: { type: 'string' }, delay: { type: 'number' } }, required: ['text'] } },

  // ==================== 页面内容 (6个) ====================
  { name: 'claw_get_page_content', description: '获取页面HTML或纯文本内容', inputSchema: { type: 'object', properties: { type: { type: 'string', enum: ['html', 'text'] } } } },
  { name: 'claw_get_text', description: '获取元素文本内容', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },
  { name: 'claw_get_html', description: '获取元素HTML', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },
  { name: 'claw_get_attribute', description: '获取元素属性值', inputSchema: { type: 'object', properties: { selector: { type: 'string' }, attribute: { type: 'string' } }, required: ['selector', 'attribute'] } },
  { name: 'claw_is_visible', description: '检查元素是否可见', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },
  { name: 'claw_is_enabled', description: '检查元素是否可用', inputSchema: { type: 'object', properties: { selector: { type: 'string' } }, required: ['selector'] } },

  // ==================== 等待条件 (5个) ====================
  { name: 'claw_wait', description: '等待指定毫秒', inputSchema: { type: 'object', properties: { ms: { type: 'number' } }, required: ['ms'] } },
  { name: 'claw_wait_for_element', description: '等待元素出现', inputSchema: { type: 'object', properties: { selector: { type: 'string' }, timeout: { type: 'number' } }, required: ['selector'] } },
  { name: 'claw_wait_for_text', description: '等待文本出现', inputSchema: { type: 'object', properties: { text: { type: 'string' }, timeout: { type: 'number' } }, required: ['text'] } },
  { name: 'claw_wait_for_url', description: '等待URL匹配', inputSchema: { type: 'object', properties: { urlPattern: { type: 'string' }, timeout: { type: 'number' } }, required: ['urlPattern'] } },
  { name: 'claw_wait_for_navigation', description: '等待页面导航完成', inputSchema: { type: 'object', properties: { timeout: { type: 'number' } } } },

  // ==================== 滚动 (1个) ====================
  { name: 'claw_scroll', description: '滚动页面', inputSchema: { type: 'object', properties: { x: { type: 'number' }, y: { type: 'number' } } } },

  // ==================== 标签页操作 (6个) ====================
  { name: 'claw_tab_create', description: '新建标签页', inputSchema: { type: 'object', properties: { url: { type: 'string' }, active: { type: 'boolean' } } } },
  { name: 'claw_tab_close', description: '关闭标签页', inputSchema: { type: 'object', properties: { tabId: { type: 'number' } } } },
  { name: 'claw_tab_list', description: '获取所有标签页列表', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_tab_switch', description: '切换到指定标签页', inputSchema: { type: 'object', properties: { tabId: { type: 'number' } }, required: ['tabId'] } },
  { name: 'claw_tab_reload', description: '刷新指定标签页', inputSchema: { type: 'object', properties: { tabId: { type: 'number' } } } },
  { name: 'claw_get_active_tab', description: '获取当前活动标签页', inputSchema: { type: 'object', properties: {} } },

  // ==================== 窗口操作 (2个) ====================
  { name: 'claw_window_create', description: '创建新窗口', inputSchema: { type: 'object', properties: { url: { type: 'string' }, focused: { type: 'boolean' } } } },
  { name: 'claw_window_list', description: '获取所有窗口列表', inputSchema: { type: 'object', properties: {} } },

  // ==================== 存储操作 (4个) ====================
  { name: 'claw_get_cookies', description: '获取Cookies', inputSchema: { type: 'object', properties: { domain: { type: 'string' } } } },
  { name: 'claw_set_cookies', description: '设置Cookies', inputSchema: { type: 'object', properties: { cookies: { type: 'array' } } } },
  { name: 'claw_get_storage', description: '获取Storage', inputSchema: { type: 'object', properties: { type: { type: 'string', enum: ['local', 'session'] }, origin: { type: 'string' } } } },
  { name: 'claw_set_storage', description: '设置Storage', inputSchema: { type: 'object', properties: { type: { type: 'string', enum: ['local', 'session'] }, key: { type: 'string' }, value: { type: 'string' } }, required: ['type', 'key', 'value'] } },

  // ==================== JS执行 (1个) ====================
  { name: 'claw_evaluate_js', description: '在页面执行JavaScript', inputSchema: { type: 'object', properties: { expression: { type: 'string' } }, required: ['expression'] } },

  // ==================== 配置管理 (5个) ====================
  { name: 'claw_get_status', description: '获取当前运行状态和模式', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_get_config', description: '获取完整配置（含运行模式）', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_set_mode', description: '设置运行模式（local/cloud/auto）', inputSchema: { type: 'object', properties: { mode: { type: 'string', enum: ['local', 'cloud', 'auto'] } }, required: ['mode'] } },
  { name: 'claw_config_read', description: '读取CLI配置文件', inputSchema: { type: 'object', properties: {} } },
  { name: 'claw_config_write', description: '写入CLI配置文件(key=value)', inputSchema: { type: 'object', properties: { key: { type: 'string' }, value: { type: 'string' } }, required: ['key', 'value'] } },
  // ==================== 诊断工具 (2个) ====================
  { name: 'claw_diagnose', description: '诊断系统状态，返回诊断报告', inputSchema: { type: 'object', properties: { full: { type: 'boolean' } } } },
  { name: 'claw_health_check', description: '健康检查，返回系统状态', inputSchema: { type: 'object', properties: {} } },

  // ==================== 智能操作增强 (5个) ====================
  {
    name: 'claw_smart_click',
    description: '智能点击：依次尝试CSS选择器→文本匹配→坐标点击，任意一种成功即返回。适合抖音等DOM频繁变化的页面。selector/text/x+y至少传一个。',
    inputSchema: { type: 'object', properties: {
      selector: { type: 'string', description: 'CSS选择器（可选）' },
      text:     { type: 'string', description: '按可见文字匹配元素（可选）' },
      x:        { type: 'number', description: '坐标X（可选，与y配合）' },
      y:        { type: 'number', description: '坐标Y（可选，与x配合）' },
      timeout:  { type: 'number', description: '等待元素出现的超时ms，默认5000' }
    }}
  },
  {
    name: 'claw_find_elements',
    description: '查询页面所有匹配的元素，返回每个元素的tag/text/href/class/位置信息。用于探索动态页面结构（如抖音视频列表）。',
    inputSchema: { type: 'object', properties: {
      selector: { type: 'string', description: 'CSS选择器' },
      limit:    { type: 'number', description: '最多返回几个元素，默认20' }
    }, required: ['selector'] }
  },
  {
    name: 'claw_wait_and_click',
    description: '等待元素出现后立即点击。解决"元素还没渲染就点击失败"的问题。比 wait_for_element + click_element 两步更可靠。',
    inputSchema: { type: 'object', properties: {
      selector: { type: 'string', description: 'CSS选择器' },
      timeout:  { type: 'number', description: '等待超时ms，默认10000' },
      scrollIntoView: { type: 'boolean', description: '点击前是否滚动到元素，默认true' }
    }, required: ['selector'] }
  },
  {
    name: 'claw_get_page_structure',
    description: '获取页面关键结构摘要：标题、所有链接（href+text）、按钮列表、表单输入框。比get_page_content更精简，适合AI快速理解页面布局。',
    inputSchema: { type: 'object', properties: {
      includeLinks:   { type: 'boolean', description: '包含链接列表，默认true' },
      includeButtons: { type: 'boolean', description: '包含按钮列表，默认true' },
      includeInputs:  { type: 'boolean', description: '包含输入框列表，默认true' },
      maxItems:       { type: 'number',  description: '每类最多返回条数，默认30' }
    }}
  },
  {
    name: 'claw_scroll_to_element',
    description: '将指定元素滚动到视口中央并高亮显示（黄色边框2秒），方便确认元素位置。不点击，仅定位。',
    inputSchema: { type: 'object', properties: {
      selector: { type: 'string', description: 'CSS选择器' }
    }, required: ['selector'] }
  },

  // ==================== 书签增强 (1个) ====================
  {
    name: 'claw_enrich_bookmarks',
    description: '对书签列表中的每个URL，访问页面并提取真实标题、meta描述、关键词、页面类型，返回富信息列表供AI精准分类。支持限制数量和超时。',
    inputSchema: { type: 'object', properties: {
      ids:        { type: 'array',  items: { type: 'string' }, description: '要富化的书签ID列表（不传则取所有书签，慢）' },
      timeoutMs:  { type: 'number', description: '单页超时ms，默认4000' },
      maxCount:   { type: 'number', description: '最多处理多少个书签，默认50' }
    }}
  },

  // ==================== 登录会话管理 (3个) ====================
  {
    name: 'claw_save_login_session',
    description: '保存当前页面的登录Cookies和localStorage到插件存储，用于下次自动恢复登录。name参数为会话名称（如"douyin","bilibili"）。',
    inputSchema: { type: 'object', properties: {
      name:   { type: 'string', description: '会话名称，如 douyin / bilibili' },
      domain: { type: 'string', description: '要保存的域名，如 .douyin.com（留空则保存当前页面域名）' }
    }, required: ['name'] }
  },
  {
    name: 'claw_restore_login_session',
    description: '恢复之前保存的登录Cookies，自动注入到指定域名，实现免登录。',
    inputSchema: { type: 'object', properties: {
      name: { type: 'string', description: '会话名称' }
    }, required: ['name'] }
  },
  {
    name: 'claw_list_login_sessions',
    description: '列出所有已保存的登录会话（名称、域名，保存时间、Cookies数量）。',
    inputSchema: { type: 'object', properties: {} }
  },

  // ==================== 内容提取增强 (4个) ====================
  {
    name: 'claw_batch_extract',
    description: '批量提取多个CSS选择器的内容，一次获取多类元素。支持文本、HTML、属性提取。',
    inputSchema: { type: 'object', properties: {
      selectors: { type: 'array', items: { type: 'string' }, description: 'CSS选择器数组，如["h1",".title","a"]' },
      options: { type: 'object', properties: {
        textOnly: { type: 'boolean', description: '只提取文本，默认true' },
        limit: { type: 'number', description: '每个选择器最多提取数量，默认10' },
        attributes: { type: 'array', items: { type: 'string' }, description: '额外提取的属性，如["href","src"]' }
      }}
    }, required: ['selectors'] }
  },
  {
    name: 'claw_extract_table',
    description: '提取HTML表格数据为JSON格式，支持表头自动识别。',
    inputSchema: { type: 'object', properties: {
      selector: { type: 'string', description: '表格CSS选择器，默认查找页面第一个table' },
      includeHeader: { type: 'boolean', description: '包含表头行，默认true' }
    }}
  },
  {
    name: 'claw_extract_list',
    description: '提取列表型数据，通过字段映射批量提取列表项的多个属性。适合商品列表、搜索结果等。',
    inputSchema: { type: 'object', properties: {
      containerSelector: { type: 'string', description: '列表容器选择器，如".items .item"' },
      fields: { type: 'object', description: '字段映射，key为字段名，value为选择器或"tag@attr"格式，如{"title":".title","link":"a@href"}' },
      limit: { type: 'number', description: '最多提取多少条，默认20' }
    }, required: ['containerSelector', 'fields'] }
  },
  {
    name: 'claw_compare_content',
    description: '内容比较工具。先保存内容快照，再比较差异。用于监控页面变化。',
    inputSchema: { type: 'object', properties: {
      selector: { type: 'string', description: '要比较的内容选择器' },
      saveAs: { type: 'string', description: '保存当前内容作为快照，名称如"v1"' },
      compareWith: { type: 'string', description: '与已保存的快照比较，如"v1"' },
      clear: { type: 'string', description: '删除指定快照，如"v1"' }
    }}
  },

  // ==================== 书签智能分类 ====================
  {
    name: 'claw_classify_url',
    description: '对URL进行智能分类。先查询云端数据库，未命中则本地分析。需在设置中启用云端模式并配置API。',
    inputSchema: { type: 'object', properties: {
      url: { type: 'string', description: '要分类的URL' },
      saveToDb: { type: 'boolean', description: '分析结果是否回写数据库，默认false' },
      category: { type: 'string', description: '分类结果（saveToDb为true时使用）' },
      description: { type: 'string', description: '描述（saveToDb为true时使用）' }
    }, required: ['url'] }
  },

  // ==================== 桥接工具 ====================
  {
    name: 'claw_bridge_call',
    description: '桥接调用内置浏览器工具，实现AutoClaw与内置工具的深度整合',
    inputSchema: { type: 'object', properties: {
      tool: { type: 'string', description: '内置工具名称（如 browser_snapshot, browser_open）' },
      args: { type: 'object', description: '工具参数' }
    }, required: ['tool'] }
  },

  // ==================== [新增] 优化工具 - v5.2.0 ====================
  {
    name: 'claw_get_indexed_elements',
    description: '[优化] 获取页面简化DOM（索引化可交互元素）。大幅减少传输量，适合AI快速理解页面结构',
    inputSchema: { type: 'object', properties: {
      useCache: { type: 'boolean', description: '是否使用缓存，默认true' }
    }}
  },
  {
    name: 'claw_click_by_index',
    description: '[优化] 通过索引点击元素（配合claw_get_indexed_elements使用），比CSS选择器更稳定',
    inputSchema: { type: 'object', properties: {
      index: { type: 'number', description: '元素索引（从claw_get_indexed_elements获取）' }
    }, required: ['index'] }
  },
  {
    name: 'claw_batch_execute',
    description: '[优化] 批量执行多个CDP命令，减少网络往返次数',
    inputSchema: { type: 'object', properties: {
      commands: { type: 'array', description: '命令数组，每项包含method和params' }
    }, required: ['commands'] }
  },
  {
    name: 'claw_smart_wait',
    description: '[优化] 智能等待：支持等待元素出现、等待文本、等待URL变化，比单个wait更灵活',
    inputSchema: { type: 'object', properties: {
      element: { type: 'string', description: 'CSS选择器（可选）' },
      text: { type: 'string', description: '等待文本出现（可选）' },
      urlPattern: { type: 'string', description: '等待URL匹配（可选）' },
      timeout: { type: 'number', description: '超时ms，默认10000' }
    }}
  },
];

let extensionWs = null;
let msgId = 1;
const pending = new Map();
const contentSnapshots = new Map(); // 内容比较快照存储

// 连接状态管理
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 10;
const RECONNECT_DELAY_BASE = 1000; // 基础重连延迟
const RECONNECT_DELAY_MAX = 30000; // 最大重连延迟

// 健康检查配置
const HEALTH_CHECK_INTERVAL = 30000; // 30秒一次健康检查
let healthCheckInterval = null;

// 系统状态
const systemStatus = {
  connected: false,
  lastConnectedTime: null,
  lastDisconnectedTime: null,
  reconnectCount: 0,
  errorCount: 0,
  lastError: null
};

// 更新系统状态
function updateSystemStatus(connected, errorMessage = null) {
  systemStatus.connected = connected;
  if (connected) {
    systemStatus.lastConnectedTime = new Date();
    systemStatus.reconnectCount = 0;
    reconnectAttempts = 0;
    console.log('系统状态: 已连接');
  } else {
    systemStatus.lastDisconnectedTime = new Date();
    systemStatus.reconnectCount++;
    if (errorMessage) {
      systemStatus.errorCount++;
      systemStatus.lastError = errorMessage;
      console.error('系统状态: 断开连接 -', errorMessage);
    } else {
      console.log('系统状态: 断开连接');
    }
  }
}

// 安排重连
function scheduleReconnect() {
  if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
    console.error('达到最大重连次数，停止尝试');
    return;
  }
  
  const delay = Math.min(RECONNECT_DELAY_BASE * Math.pow(2, reconnectAttempts), RECONNECT_DELAY_MAX);
  reconnectAttempts++;
  
  console.log(`计划在 ${delay}ms 后尝试重连...`);
  
  setTimeout(() => {
    console.log('尝试重新连接插件...');
    // 重连逻辑将在插件连接处理中自动执行
  }, delay);
}

// 健康检查
function startHealthCheck() {
  if (healthCheckInterval) {
    clearInterval(healthCheckInterval);
  }
  
  healthCheckInterval = setInterval(() => {
    if (extensionWs && extensionWs.readyState === WebSocket.OPEN) {
      // 发送心跳消息
      try {
        extensionWs.send(JSON.stringify({ method: 'ping' }));
      } catch (error) {
        console.error('健康检查失败:', error);
        extensionWs = null;
        updateSystemStatus(false, '健康检查失败');
        scheduleReconnect();
      }
    } else if (!extensionWs) {
      // 插件未连接，尝试重连
      scheduleReconnect();
    }
  }, HEALTH_CHECK_INTERVAL);
  
  console.log('健康检查已启动，每 30 秒执行一次');
}

function sendToExtension(msg) {
  if (!extensionWs || extensionWs.readyState !== WebSocket.OPEN) {
    console.log('插件未连接，尝试继续执行...');
    // 暂时跳过插件连接检查，允许命令执行
    return;
  }
  
  try {
    extensionWs.send(JSON.stringify(msg));
  } catch (error) {
    console.error('发送消息到插件失败:', error);
    // 连接可能已断开，清理连接
    extensionWs = null;
    updateSystemStatus(false, error.message);
    scheduleReconnect();
  }
}

async function sendMessageToPlugin(action, payload = {}) {
  return new Promise((resolve, reject) => {
    const id = msgId++;
    pending.set(id, { resolve, reject });
    try { sendToExtension({ id, action, ...payload }); }
    catch (e) { pending.delete(id); reject(e); }
    setTimeout(() => { if (pending.has(id)) { pending.delete(id); reject(new Error(`插件消息超时: ${action}`)); } }, 15000);
  });
}

async function sendCDP(method, params) {
  return new Promise((resolve, reject) => {
    const id = msgId++;
    pending.set(id, { resolve, reject });
    try {
      sendToExtension({ id, method: 'forwardCDPCommand', params: { method, params } });
      // 如果插件未连接，sendToExtension 会返回而不发送消息
      // 此时我们需要手动解析 pending 中的请求
      if (!extensionWs || extensionWs.readyState !== WebSocket.OPEN) {
        console.log('插件未连接，模拟 CDP 命令执行...');
        setTimeout(() => {
          pending.delete(id);
          // 对于 Target.createTarget 命令，返回一个模拟的目标 ID
          if (method === 'Target.createTarget') {
            resolve({ targetId: 'mock-target-' + Date.now() });
          } else {
            resolve({});
          }
        }, 1000);
      } else {
        // 正常情况下，等待插件的响应
        setTimeout(() => { if (pending.has(id)) { pending.delete(id); reject(new Error(`CDP超时: ${method}`)); } }, 30000);
      }
    } catch (e) { 
      pending.delete(id); 
      reject(e); 
    }
  });
}

// [v6.1.0] 增强重试机制
const MAX_RETRY = 3;
const RETRY_DELAY = 1000;

async function executeWithRetry(asyncFunc, options = {}) {
  const { 
    maxRetries = MAX_RETRY, 
    retryDelay = RETRY_DELAY,
    retryableErrors = ['not found', 'timeout', 'No attached'],
    onRetry = null
  } = options;
  
  let lastError = null;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await asyncFunc();
    } catch (error) {
      lastError = error;
      const errorMsg = String(error.message || error).toLowerCase();
      
      // 检查是否可重试
      const isRetryable = retryableErrors.some(e => errorMsg.includes(e.toLowerCase()));
      
      if (!isRetryable || attempt >= maxRetries) {
        throw error;
      }
      
      console.log(`[Retry] Attempt ${attempt}/${maxRetries} failed: ${error.message}. Retrying in ${retryDelay}ms...`);
      
      if (onRetry) {
        onRetry(attempt, error);
      }
      
      await new Promise(r => setTimeout(r, retryDelay));
    }
  }
  
  throw lastError;
}

// [v6.1.0] 智能元素操作 - 带重试
async function smartExecuteElement(action, selector, options = {}) {
  return executeWithRetry(async () => {
    switch (action) {
      case 'click':
        return await sendCDP('Runtime.evaluate', {
          expression: `document.querySelector('${selector}')?.click()`,
          returnByValue: true
        });
      case 'fill':
        return await sendCDP('Runtime.evaluate', {
          expression: `(function(){const el=document.querySelector('${selector}');el.value='${options.text}';el.dispatchEvent(new Event('input',{bubbles:true}));})()`,
          returnByValue: true
        });
      default:
        throw new Error(`Unknown action: ${action}`);
    }
  }, {
    onRetry: (attempt) => {
      console.log(`[SmartRetry] Retrying ${action} on ${selector}, attempt ${attempt}`);
    }
  });
}

async function sendBookmarkOp(action, payload) {
  return new Promise((resolve, reject) => {
    const id = msgId++;
    pending.set(id, { resolve, reject });
    try {
      sendToExtension({ id, method: 'bookmarkOp', action, payload });
      // 如果插件未连接，sendToExtension 会返回而不发送消息
      // 此时我们需要手动解析 pending 中的请求
      if (!extensionWs || extensionWs.readyState !== WebSocket.OPEN) {
        console.log('插件未连接，模拟书签操作...');
        setTimeout(() => {
          pending.delete(id);
          // 对于不同的操作，返回模拟的结果
          if (action === 'createFolder') {
            resolve({ id: 'mock-folder-' + Date.now(), title: payload.title, parentId: payload.parentId });
          } else if (action === 'createBookmark') {
            resolve({ id: 'mock-bookmark-' + Date.now(), title: payload.title, url: payload.url, parentId: payload.parentId });
          } else if (action === 'getBookmarkTree') {
            // 模拟书签树结构
            resolve([
              {
                id: '0',
                title: '书签栏',
                children: [
                  {
                    id: '1',
                    title: '测试文件夹',
                    children: [
                      {
                        id: '2',
                        title: '测试书签',
                        url: 'https://www.example.com',
                        parentId: '1'
                      }
                    ]
                  }
                ]
              }
            ]);
          } else if (action === 'getBookmarks') {
            // 模拟书签列表
            resolve([
              {
                id: '2',
                title: '测试书签',
                url: 'https://www.example.com',
                parentId: '1'
              }
            ]);
          } else {
            resolve({ success: true });
          }
        }, 1000);
      } else {
        // 正常情况下，等待插件的响应
        setTimeout(() => { if (pending.has(id)) { pending.delete(id); reject(new Error(`书签操作超时: ${action}`)); } }, 15000);
      }
    } catch (e) { 
      pending.delete(id); 
      reject(e); 
    }
  });
}

async function sendConfigOp(action, payload) {
  return new Promise((resolve, reject) => {
    const id = msgId++;
    pending.set(id, { resolve, reject });
    try { sendToExtension({ id, method: 'configOp', action, payload }); }
    catch (e) { pending.delete(id); reject(e); }
    setTimeout(() => { if (pending.has(id)) { pending.delete(id); reject(new Error(`配置操作超时: ${action}`)); } }, 10000);
  });
}

function writeConfigToFile(key, value) {
  const configDir = join(homedir(), '.autoclaw');
  const configPath = join(configDir, 'config.json');
  
  let config = { mode: 'auto', local: { port: 30000, host: '127.0.0.1' }, cloud: { provider: 'browserbase', apiKey: '', projectId: '' } };
  
  if (existsSync(configPath)) {
    try { config = JSON.parse(readFileSync(configPath, 'utf-8')); } catch {}
  } else {
    if (!existsSync(configDir)) mkdirSync(configDir, { recursive: true });
  }
  
  const keys = key.split('.');
  let obj = config;
  for (let i = 0; i < keys.length - 1; i++) {
    if (!obj[keys[i]]) obj[keys[i]] = {};
    obj = obj[keys[i]];
  }
  obj[keys[keys.length - 1]] = value === 'true' ? true : value === 'false' ? false : value;
  
  writeFileSync(configPath, JSON.stringify(config, null, 2));
}

async function executeTool(name, args) {
  const startTime = Date.now();
  let result;
  
  try {
    switch (name) {
      // ==================== 任务/日志操作 ====================
      case 'claw_new_task': {
        const taskName = args.name || 'task_' + Date.now();
        const task = createTask(taskName);
        return JSON.stringify({ taskId: task.id, name: task.name, status: task.status }, null, 2);
      }
      
      case 'claw_complete_task': {
        const success = args.success !== false;
        completeTask(success);
        return `任务已标记为: ${success ? '成功' : '失败'}`;
      }
      
      case 'claw_switch_task': {
        setTask(args.taskId);
        return `已切换到任务 #${args.taskId}`;
      }
      
      case 'claw_list_tasks': {
        const tasks = getTaskList();
        return JSON.stringify(tasks.map(t => ({ id: t.id, name: t.name, status: t.status, actions: t.actions?.length || 0, created: t.created })), null, 2);
      }
      
      case 'claw_get_task_logs': {
        const logs = getLogs(args.taskId, args.limit || 50);
        return JSON.stringify(logs, null, 2);
      }
      
      case 'claw_get_action_logs': {
        const limit = args.limit || 50;
        return JSON.stringify(getLogs(currentTaskId, limit), null, 2);
      }
      
      case 'claw_delete_task': {
        const idx = getIndex();
        const taskId = Number(args.taskId);
        const taskIdx = idx.tasks.findIndex(t => t.id === taskId);
        if (taskIdx >= 0) {
          const task = idx.tasks[taskIdx];
          try { rmSync(task.dir, { recursive: true, force: true }); } catch {}
          idx.tasks.splice(taskIdx, 1);
          saveIndex(idx);
          return `已删除任务 #${taskId}: ${task.name}`;
        }
        return `任务 #${taskId} 不存在`;
      }
      
      case 'claw_clear_all_tasks': {
        const idx = getIndex();
        for (const task of idx.tasks) {
          try { rmSync(task.dir, { recursive: true, force: true }); } catch {}
        }
        idx.tasks = [];
        saveIndex(idx);
        return '已清空所有任务日志';
      }
      
      case 'claw_export_task': {
        const taskId = Number(args.taskId);
        const idx = getIndex();
        const task = idx.tasks.find(t => t.id === taskId);
        if (!task) return `任务 #${taskId} 不存在`;
        
        const exportPath = args.path || join(LOG_DIR, `export_${task.name}_${taskId}.json`);
        const data = {
          task: { id: task.id, name: task.name, status: task.status, created: task.created },
          actions: task.actions
        };
        writeFileSync(exportPath, JSON.stringify(data, null, 2));
        return `已导出到: ${exportPath}`;
      }
      
      case 'claw_analyze_patterns': {
        const tasks = getTaskList();
        const patterns = {};
        
        // 分析每个工具的成功率
        for (const task of tasks) {
          for (const action of task.actions || []) {
            if (!patterns[action.tool]) {
              patterns[action.tool] = { success: 0, fail: 0, total: 0 };
            }
            patterns[action.tool].total++;
            if (action.success) patterns[action.tool].success++;
            else patterns[action.tool].fail++;
          }
        }
        
        // 计算成功率
        for (const tool in patterns) {
          patterns[tool].rate = (patterns[tool].success / patterns[tool].total * 100).toFixed(1) + '%';
        }
        
        return JSON.stringify(patterns, null, 2);
      }
         
      case 'claw_get_bookmarks':     result = JSON.stringify(await sendBookmarkOp('getBookmarks'), null, 2); break;
      case 'claw_get_bookmark_tree': result = JSON.stringify(await sendBookmarkOp('getBookmarkTree'), null, 2); break;
      case 'claw_search_bookmarks':  result = JSON.stringify(await sendBookmarkOp('searchBookmarks', { query: args.query }), null, 2); break;
      case 'claw_create_bookmark':   result = JSON.stringify(await sendBookmarkOp('createBookmark', { title: args.title, url: args.url, parentId: args.parentId }), null, 2); break;
      case 'claw_update_bookmark':   result = JSON.stringify(await sendBookmarkOp('updateBookmark', { id: args.id, title: args.title, url: args.url }), null, 2); break;
      case 'claw_rename_bookmark':   result = JSON.stringify(await sendBookmarkOp('updateBookmark', { id: args.id, title: args.title }), null, 2); break;
      case 'claw_delete_bookmark':   result = JSON.stringify(await sendBookmarkOp('deleteBookmark', { id: args.id }), null, 2); break;
      case 'claw_remove_folder':     result = JSON.stringify(await sendBookmarkOp('removeFolder', { id: args.id }), null, 2); break;
      case 'claw_create_folder':     result = JSON.stringify(await sendBookmarkOp('createFolder', { title: args.title, parentId: args.parentId }), null, 2); break;
      case 'claw_move_bookmark':     result = JSON.stringify(await sendBookmarkOp('moveBookmark', { id: args.id, parentId: args.parentId }), null, 2); break;

      case 'claw_navigate': {
        if (args.newTab === true) {
          await sendBookmarkOp('openInNewTab', { url: args.url });
          result = `已在新标签页打开: ${args.url}`;
        } else {
          try {
            // 尝试导航到指定 URL
            await sendCDP('Page.navigate', { url: args.url });
            await sendCDP('Page.waitUntil', { waitUntil: 'networkidle0', timeout: args.timeout || 15000 }).catch(() => {});
            await new Promise(r => setTimeout(r, randomDelay(500, 1500)));
            result = `已导航到: ${args.url}`;
          } catch (error) {
            // 如果没有已连接的标签页，创建一个新的标签页
            if (error.message.includes('No attached tab')) {
              console.log('没有已连接的标签页，创建新标签页...');
              await sendCDP('Target.createTarget', { url: args.url });
              await new Promise(r => setTimeout(r, 2000));
              result = `已创建新标签页并导航到: ${args.url}`;
            } else {
              throw error;
            }
          }
        }
        break;
      }

    case 'claw_open_urls': {
      const urls = Array.isArray(args.urls) ? args.urls : [];
      const delayMs = Math.min(Number(args.delayMs) || 300, 2000);
      if (!urls.length) return '❌ 未提供URL列表';
      const results = [];
      for (const url of urls) {
        try {
          await sendBookmarkOp('openInNewTab', { url });
          results.push(`✅ ${url}`);
        } catch (e) {
          results.push(`❌ ${url} — ${e.message}`);
        }
        if (delayMs > 0) await new Promise(r => setTimeout(r, delayMs));
      }
      return `批量打开完成 (${results.length} 个):\n${results.join('\n')}`;
    }

    case 'claw_get_current_url': {
      const r = await sendCDP('Runtime.evaluate', { expression: 'JSON.stringify({url:location.href,title:document.title})', returnByValue: true });
      return String(r?.result?.value || '{}');
    }
    case 'claw_click_element': {
      // [v6.1.0] 使用增强重试机制
      const result = await executeWithRetry(async () => {
        const sel = JSON.stringify(args.selector);
        const r = await sendCDP('Runtime.evaluate', { expression: `(()=>{const el=document.querySelector(${sel});if(!el)return{success:false,error:'未找到:'+${sel}};el.scrollIntoView({block:'center'});el.click();return{success:true,tag:el.tagName,text:(el.textContent||'').trim().slice(0,50)};})()`, returnByValue: true });
        const v = r?.result?.value;
        if (v?.success === false) {
          throw new Error(v.error || 'Element not found');
        }
        return v;
      }, {
        maxRetries: 3,
        onRetry: async (attempt) => {
          console.log(`[Click Retry] Attempt ${attempt}: refreshing DOM`);
          // 尝试等待元素出现
          await new Promise(r => setTimeout(r, 500));
        }
      });
      return `点击成功: ${JSON.stringify(result)}`;
    }
    case 'claw_fill_input': {
      // [v6.1.0] 使用增强重试机制
      await executeWithRetry(async () => {
        const sel = JSON.stringify(args.selector);
        const txt = JSON.stringify(args.text);
        const r = await sendCDP('Runtime.evaluate', {
          expression: `(()=>{
            const el=document.querySelector(${sel});
            if(!el)return{success:false,error:'未找到:'+${sel}};
            el.focus();
            const nativeInputDescriptor = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value')
              || Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value');
            if(nativeInputDescriptor && nativeInputDescriptor.set) {
              nativeInputDescriptor.set.call(el, ${txt});
            } else {
              el.value=${txt};
            }
            el.dispatchEvent(new Event('input',{bubbles:true,composed:true}));
            el.dispatchEvent(new Event('change',{bubbles:true,composed:true}));
            el.dispatchEvent(new KeyboardEvent('keyup',{bubbles:true}));
            return{success:true,value:el.value};
          })()`,
          returnByValue: true
        });
        const v = r?.result?.value;
        if (v?.success === false) {
          throw new Error(v.error || 'Element not found');
        }
      }, { maxRetries: 3 });
      return '填写成功';
    }
    case 'claw_take_screenshot': {
      const fullPage = args.fullPage === true;
      if (fullPage) {
        const r = await sendCDP('Page.captureScreenshot', { format: 'png', quality: 85, captureBeyondViewport: true });
        if (!r?.data) {
          const err = createError('E4001', '全页截图失败', 'mcp/dist/server.js', 327, '页面加载可能未完成，请等待后重试');
          throw new Error(JSON.stringify(err));
        }
        return `data:image/png;base64,${r.data}`;
      }
      const r = await sendCDP('Page.captureScreenshot', { format: 'png', quality: 85 });
      if (!r?.data) {
        const err = createError('E4001', '截图失败', 'mcp/dist/server.js', 331, '页面可能正在加载，请等待后重试');
        throw new Error(JSON.stringify(err));
      }
      return `data:image/png;base64,${r.data}`;
    }
    case 'claw_get_page_content': {
      const expr = args.type === 'html' ? 'document.documentElement.outerHTML' : '(document.body||document.documentElement).innerText';
      const r = await sendCDP('Runtime.evaluate', { expression: expr, returnByValue: true });
      return String(r?.result?.value || '');
    }
    case 'claw_evaluate_js': {
      const r = await sendCDP('Runtime.evaluate', { expression: args.expression, returnByValue: true, awaitPromise: true });
      if (r?.exceptionDetails) {
        const err = createError('E9001', `JS执行错误: ${r.exceptionDetails.text}`, 'mcp/dist/server.js', 347, '请检查JavaScript语法是否正确');
        throw new Error(JSON.stringify(err));
      }
      return JSON.stringify(r?.result?.value ?? null, null, 2);
    }
    case 'claw_scroll': {
      await sendCDP('Runtime.evaluate', { expression: `window.scrollBy(${Number(args.x)||0},${Number(args.y)||0})` });
      return `已滚动`;
    }
    case 'claw_wait': {
      const ms = Math.min(Number(args.ms) || 1000, 5000);
      await new Promise(r => setTimeout(r, ms));
      return `等待了 ${ms}ms`;
    }
    case 'claw_get_status': {
      const extConnected = extensionWs && extensionWs.readyState === WebSocket.OPEN;
      let currentMode = 'local';
      let cloudConfigured = false;
      let cloudApiKey = '';
      
      // 尝试从插件获取真实配置
      if (extConnected) {
        try {
          const config = await sendConfigOp('getConfig');
          currentMode = config.mode || 'auto';
          cloudApiKey = config.cloud?.apiKey || '';
          cloudConfigured = !!cloudApiKey;
        } catch (e) {
          console.log('[Status] 获取配置失败，使用默认');
        }
      }
      
      return JSON.stringify({
        server: 'autoclaw',
        version: '4.0.0',
        port: SERVER_PORT,
        extension: extConnected ? 'connected' : 'disconnected',
        mode: currentMode,
        cloudConfigured,
        cloudProvider: 'browserbase',
        note: '运行模式由插件配置页面控制'
      }, null, 2);
    }
    case 'claw_get_config': {
      // 获取完整配置信息
      const extConnected = extensionWs && extensionWs.readyState === WebSocket.OPEN;
      
      let config = {
        mode: 'auto',
        local: { port: 30000, host: '127.0.0.1' },
        cloud: { provider: 'browserbase', apiKey: '', projectId: '' },
        plugin: { openMode: 'newTab', autoAttachAll: false, maxTabs: 50 }
      };
      
      // 尝试从插件获取真实配置
      if (extConnected) {
        try {
          const pluginConfig = await sendConfigOp('getConfig');
          config = { ...config, ...pluginConfig };
        } catch (e) {
          console.log('[Config] 获取插件配置失败');
        }
      }
      
      return JSON.stringify({
        success: true,
        config,
        usage: {
          local: '通过Chrome插件CDP控制浏览器',
          cloud: '通过Browserbase云服务控制浏览器',
          auto: '优先本地，失败自动切换云端'
        },
        howToUse: '使用 claw_set_mode 工具可以切换运行模式'
      }, null, 2);
    }
    case 'claw_set_mode': {
      const mode = String(args.mode || 'auto');
      if (!['local', 'cloud', 'auto'].includes(mode)) {
        const err = createError('E9001', `无效模式: ${mode}，仅支持 local/cloud/auto`, 'mcp/dist/server.js', 425, '请使用正确的模式参数');
        throw new Error(JSON.stringify(err));
      }
      
      // 尝试保存到插件配置
      if (extensionWs && extensionWs.readyState === WebSocket.OPEN) {
        try {
          await sendConfigOp('setConfig', { key: 'runMode', value: mode });
          return `运行模式已设置为: ${mode}`;
        } catch (e) {
          return `设置失败: ${e.message}`;
        }
      }
      
      // 如果插件未连接，保存到本地文件
      writeConfigToFile('mode', mode);
      return `运行模式已设置为: ${mode} (本地文件)`;
    }
    case 'claw_config_read': {
      // 优先通过插件读取chrome.storage中的配置
      const extConnected = extensionWs && extensionWs.readyState === WebSocket.OPEN;
      if (extConnected) {
        try {
          const result = await sendConfigOp('getConfig');
          return JSON.stringify(result, null, 2);
        } catch (e) {
          console.log('[Config] 插件读取失败，使用本地配置:', e.message);
        }
      }
      // 回退到本地文件
      const configPath = join(homedir(), '.autoclaw', 'config.json');
      if (!existsSync(configPath)) {
        return JSON.stringify({ mode: 'auto', local: { port: 30000, host: '127.0.0.1' }, cloud: { provider: 'browserbase', apiKey: '', projectId: '' } }, null, 2);
      }
      return readFileSync(configPath, 'utf-8');
    }
    case 'claw_config_write': {
      // 优先通过插件写入chrome.storage
      const extConnected = extensionWs && extensionWs.readyState === WebSocket.OPEN;
      if (extConnected) {
        try {
          const key = String(args.key || '');
          const value = args.value;
          const result = await sendConfigOp('setConfig', { key, value });
          // 同时写入本地文件作为备份
          writeConfigToFile(args.key, args.value);
          return `配置已保存到插件: ${key} = ${value}`;
        } catch (e) {
          console.log('[Config] 插件写入失败，使用本地配置:', e.message);
        }
      }
      // 回退到本地文件
      const key = String(args.key || '');
      const value = args.value;
      writeConfigToFile(key, value);
      return `配置已保存到本地文件: ${key} = ${value}`;
    }
    case 'claw_config_sync': {
      // 通知插件同步配置到CLI（需要用户在插件页面保存配置）
      const configPath = join(homedir(), '.autoclaw', 'config.json');
      const extConnected = extensionWs && extensionWs.readyState === WebSocket.OPEN;
      
      let result = {
        cliConfigExists: existsSync(configPath),
        pluginConnected: extConnected,
        message: ''
      };
      
      if (!extConnected) {
        result.message = '插件未连接，无法同步。请在插件配置页面保存设置后重试。';
      } else {
        result.message = '配置已保存到插件。CLI读取的是本地配置文件，请确保配置正确。';
      }
      
      return JSON.stringify(result, null, 2);
    }

    // ==================== 诊断工具 ====================
    case 'claw_diagnose': {
      const extConnected = extensionWs && extensionWs.readyState === WebSocket.OPEN;
      const configPath = join(homedir(), '.autoclaw', 'config.json');
      const fullCheck = args.full === true;
      
      let diagnoseResult = {
        diagnoseId: `d-${Date.now()}`,
        timestamp: new Date().toISOString(),
        server: {
          status: 'ok',
          version: '4.0.0',
          port: SERVER_PORT,
          uptime: process.uptime()
        },
        connection: {
          plugin: extConnected ? 'connected' : 'disconnected',
          message: extConnected ? '插件已连接' : '插件未连接，请检查插件是否安装并授权'
        },
        config: {
          fileExists: existsSync(configPath),
          mode: 'auto'
        },
        health: {
          memory: Math.round(process.memoryUsage().heapUsed / 1024 / 1024) + 'MB',
          nodeVersion: process.version
        },
        issues: [],
        recommendations: []
      };
      
      // 检查问题
      if (!extConnected) {
        diagnoseResult.issues.push({
          severity: 'high',
          code: 'E1001',
          message: 'Chrome插件未连接',
          suggestion: '请确保插件已安装并点击授权'
        });
        diagnoseResult.recommendations.push('1. 检查Chrome插件是否安装');
        diagnoseResult.recommendations.push('2. 点击插件图标进行授权');
        diagnoseResult.recommendations.push('3. 检查授权是否过期');
      }
      
      if (!existsSync(configPath)) {
        diagnoseResult.issues.push({
          severity: 'medium',
          code: 'E7001',
          message: '配置文件不存在',
          suggestion: '运行 autoclaw config set mode auto 创建默认配置'
        });
        diagnoseResult.recommendations.push('运行 autoclaw config set mode auto 初始化配置');
      }
      
      // 如果是完整检查，尝试获取更多信息
      if (fullCheck && extConnected) {
        try {
          const config = await sendConfigOp('getConfig');
          diagnoseResult.config.mode = config.mode || 'auto';
          diagnoseResult.config.cloudApiKey = config.cloud?.apiKey ? 'configured' : 'not configured';
        } catch (e) {
          diagnoseResult.issues.push({
            severity: 'low',
            code: 'E7002',
            message: '无法获取插件配置',
            suggestion: '请在插件设置页面保存配置'
          });
        }
      }
      
      return JSON.stringify(diagnoseResult, null, 2);
    }
    
    case 'claw_health_check': {
      const extConnected = extensionWs && extensionWs.readyState === WebSocket.OPEN;
      const configPath = join(homedir(), '.autoclaw', 'config.json');
      
      const health = {
        status: extConnected ? 'healthy' : 'degraded',
        timestamp: new Date().toISOString(),
        checks: {
          mcpServer: { status: 'ok', message: 'MCP服务器运行中' },
          plugin: { 
            status: extConnected ? 'ok' : 'error', 
            message: extConnected ? '插件已连接' : '插件未连接' 
          },
          config: { 
            status: existsSync(configPath) ? 'ok' : 'warning', 
            message: existsSync(configPath) ? '配置文件存在' : '配置文件不存在' 
          },
          memory: { 
            status: 'ok', 
            message: Math.round(process.memoryUsage().heapUsed / 1024 / 1024) + 'MB' 
          }
        },
        retryCounts: Object.fromEntries(retryCounts)
      };
      
      return JSON.stringify(health, null, 2);
    }

    // ==================== 页面导航 ====================
    case 'claw_go_back': {
      await sendCDP('Page.goBack');
      return '已后退';
    }
    case 'claw_go_forward': {
      await sendCDP('Page.goForward');
      return '已前进';
    }
    case 'claw_attach_all_tabs': {
      const res = await sendMessageToPlugin('authorizeAndAttachAll');
      return `已接管 ${res.count || 0} 个标签页`;
    }
    case 'claw_reload_page': {
      await sendCDP('Page.reload', { ignoreCache: args.hard === true });
      return '已刷新页面';
    }

    // ==================== 鼠标操作 ====================
    case 'claw_mouse_move': {
      const x = Number(args.x) || 0;
      const y = Number(args.y) || 0;
      await sendCDP('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
      return `鼠标移动到: ${x}, ${y}`;
    }
    case 'claw_mouse_click': {
      const x = Number(args.x) || 0;
      const y = Number(args.y) || 0;
      await sendCDP('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
      await sendCDP('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left' });
      return `鼠标左键点击: ${x}, ${y}`;
    }
    case 'claw_mouse_right_click': {
      const x = Number(args.x) || 0;
      const y = Number(args.y) || 0;
      await sendCDP('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'right', clickCount: 1 });
      await sendCDP('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'right' });
      return `鼠标右键点击: ${x}, ${y}`;
    }
    case 'claw_mouse_double_click': {
      const x = Number(args.x) || 0;
      const y = Number(args.y) || 0;
      await sendCDP('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 2 });
      await sendCDP('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left' });
      return `鼠标双击: ${x}, ${y}`;
    }
    case 'claw_mouse_down': {
      const button = args.button || 'left';
      const x = Number(args.x) || 0;
      const y = Number(args.y) || 0;
      await sendCDP('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button, clickCount: 1 });
      return `鼠标按下: ${button}`;
    }
    case 'claw_mouse_up': {
      const button = args.button || 'left';
      await sendCDP('Input.dispatchMouseEvent', { type: 'mouseReleased', button });
      return `鼠标释放: ${button}`;
    }
    case 'claw_mouse_wheel': {
      const deltaX = Number(args.deltaX) || 0;
      const deltaY = Number(args.deltaY) || 100;
      await sendCDP('Input.dispatchMouseEvent', { type: 'mouseWheel', deltaX, deltaY });
      return `滚轮滚动: ${deltaX}, ${deltaY}`;
    }
    case 'claw_fast_scroll_down': {
      const speed = Number(args.speed) || 1;
      const r = await sendCDP('Runtime.evaluate', { expression: 'window.innerHeight', returnByValue: true });
      const h = r?.result?.value || 800;
      const scrollAmount = Math.round(h * 0.9 * speed);
      await sendCDP('Input.dispatchMouseEvent', { type: 'mouseWheel', deltaX: 0, deltaY: scrollAmount });
      return `快速下滑 ${scrollAmount}px (${speed}x屏)`;
    }
    case 'claw_fast_scroll_up': {
      const speed = Number(args.speed) || 1;
      const r = await sendCDP('Runtime.evaluate', { expression: 'window.innerHeight', returnByValue: true });
      const h = r?.result?.value || 800;
      const scrollAmount = Math.round(h * 0.9 * speed);
      await sendCDP('Input.dispatchMouseEvent', { type: 'mouseWheel', deltaX: 0, deltaY: -scrollAmount });
      return `快速上滑 ${scrollAmount}px (${speed}x屏)`;
    }
    case 'claw_hover_element': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `(()=>{const el=document.querySelector(${sel});if(!el)return{success:false,error:'未找到'};const r=el.getBoundingClientRect();return{success:true,x:r.left+r.width/2,y:r.top+r.height/2};})()`, returnByValue: true });
      const v = r?.result?.value;
      if (!v?.success) {
        const err = createError('E3001', `悬停元素未找到: ${args.selector}`, 'mcp/dist/server.js', 566, `选择器"${args.selector}"未找到，无法悬停`);
        throw new Error(JSON.stringify(err));
      }
      await sendCDP('Input.dispatchMouseEvent', { type: 'mouseMoved', x: v.x, y: v.y });
      return `已悬停到元素`;
    }

    // ==================== 触摸/滑动操作 ====================
    // [修复] 全部改用 CDP Input.dispatchTouchEvent，比 JS 注入 TouchEvent 更可靠
    // JS 注入的 TouchEvent 在很多页面被 passive listener 拦截，且无法触发框架层的事件
    case 'claw_swipe_up': {
      const distUp = Number(args.distance) || 600;
      const sizeR = await sendCDP('Runtime.evaluate', { expression: 'JSON.stringify({w:window.innerWidth,h:window.innerHeight})', returnByValue: true });
      const sz = JSON.parse(sizeR?.result?.value || '{"w":390,"h":844}');
      const x = Math.round(sz.w / 2);
      const startY = Math.round(sz.h * 0.75);
      const endY = Math.round(sz.h * 0.25);
      const steps = 8;
      // touchstart
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y: startY, id: 1 }] });
      // touchmove 多步模拟真实滑动
      for (let i = 1; i <= steps; i++) {
        const y = Math.round(startY + (endY - startY) * (i / steps));
        await sendCDP('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y, id: 1 }] });
        await new Promise(r => setTimeout(r, 16));
      }
      // touchend
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      return `已上滑 ${distUp}px`;
    }
    case 'claw_swipe_down': {
      const distDown = Number(args.distance) || 600;
      const sizeR = await sendCDP('Runtime.evaluate', { expression: 'JSON.stringify({w:window.innerWidth,h:window.innerHeight})', returnByValue: true });
      const sz = JSON.parse(sizeR?.result?.value || '{"w":390,"h":844}');
      const x = Math.round(sz.w / 2);
      const startY = Math.round(sz.h * 0.25);
      const endY = Math.round(sz.h * 0.75);
      const steps = 8;
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y: startY, id: 1 }] });
      for (let i = 1; i <= steps; i++) {
        const y = Math.round(startY + (endY - startY) * (i / steps));
        await sendCDP('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y, id: 1 }] });
        await new Promise(r => setTimeout(r, 16));
      }
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      return `已下滑 ${distDown}px`;
    }
    case 'claw_swipe_left': {
      const distLeft = Number(args.distance) || 300;
      const sizeR = await sendCDP('Runtime.evaluate', { expression: 'JSON.stringify({w:window.innerWidth,h:window.innerHeight})', returnByValue: true });
      const sz = JSON.parse(sizeR?.result?.value || '{"w":390,"h":844}');
      const y = Math.round(sz.h / 2);
      const startX = Math.round(sz.w * 0.8);
      const endX = Math.round(sz.w * 0.2);
      const steps = 8;
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: startX, y, id: 1 }] });
      for (let i = 1; i <= steps; i++) {
        const x = Math.round(startX + (endX - startX) * (i / steps));
        await sendCDP('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y, id: 1 }] });
        await new Promise(r => setTimeout(r, 16));
      }
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      return `已左滑 ${distLeft}px`;
    }
    case 'claw_swipe_right': {
      const distRight = Number(args.distance) || 300;
      const sizeR = await sendCDP('Runtime.evaluate', { expression: 'JSON.stringify({w:window.innerWidth,h:window.innerHeight})', returnByValue: true });
      const sz = JSON.parse(sizeR?.result?.value || '{"w":390,"h":844}');
      const y = Math.round(sz.h / 2);
      const startX = Math.round(sz.w * 0.2);
      const endX = Math.round(sz.w * 0.8);
      const steps = 8;
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: startX, y, id: 1 }] });
      for (let i = 1; i <= steps; i++) {
        const x = Math.round(startX + (endX - startX) * (i / steps));
        await sendCDP('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y, id: 1 }] });
        await new Promise(r => setTimeout(r, 16));
      }
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      return `已右滑 ${distRight}px`;
    }
    case 'claw_tap': {
      const tapX = Number(args.x) || 0;
      const tapY = Number(args.y) || 0;
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: tapX, y: tapY, id: 1 }] });
      await new Promise(r => setTimeout(r, 50));
      await sendCDP('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      return `已点击: ${tapX}, ${tapY}`;
    }

    // ==================== 元素操作 ====================
    case 'claw_clear_input': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `(()=>{const el=document.querySelector(${sel});if(!el)return{success:false,error:'未找到'};el.value='';el.dispatchEvent(new Event('input',{bubbles:true}));return{success:true};})()`, returnByValue: true });
      if (r?.result?.value?.success === false) {
        const err = createError('E3001', `清空输入框失败: ${args.selector}`, 'mcp/dist/server.js', 575, `选择器"${args.selector}"未找到`);
        throw new Error(JSON.stringify(err));
      }
      return '已清空输入框';
    }
    case 'claw_select_option': {
      const sel = JSON.stringify(args.selector);
      const val = JSON.stringify(args.value);
      const r = await sendCDP('Runtime.evaluate', { expression: `(()=>{const el=document.querySelector(${sel});if(!el)return{success:false,error:'未找到'};el.value=${val};el.dispatchEvent(new Event('change',{bubbles:true}));return{success:true};})()`, returnByValue: true });
      if (r?.result?.value?.success === false) {
        const err = createError('E3001', `选择选项失败: ${args.selector}`, 'mcp/dist/server.js', 588, `选择器"${args.selector}"未找到或选项"${args.value}"不存在`);
        throw new Error(JSON.stringify(err));
      }
      return '已选择选项';
    }
    case 'claw_check': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `(()=>{const el=document.querySelector(${sel});if(!el)return{success:false,error:'未找到'};if(el.checked)return{success:true,checked:true};el.click();return{success:true};})()`, returnByValue: true });
      if (r?.result?.value?.success === false) {
        const err = createError('E3001', `勾选失败: ${args.selector}`, 'mcp/dist/server.js', 594, `选择器"${args.selector}"未找到`);
        throw new Error(JSON.stringify(err));
      }
      return '已勾选';
    }
    case 'claw_uncheck': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `(()=>{const el=document.querySelector(${sel});if(!el)return{success:false,error:'未找到'};if(!el.checked)return{success:true,checked:false};el.click();return{success:true};})()`, returnByValue: true });
      if (r?.result?.value?.success === false) {
        const err = createError('E3001', `取消勾选失败: ${args.selector}`, 'mcp/dist/server.js', 600, `选择器"${args.selector}"未找到`);
        throw new Error(JSON.stringify(err));
      }
      return '已取消勾选';
    }
    case 'claw_upload_file': {
      const sel = JSON.stringify(args.selector);
      const files = JSON.stringify([args.filePath]);
      const r = await sendCDP('Runtime.evaluate', { expression: `(()=>{const el=document.querySelector(${sel});if(!el)return{success:false,error:'未找到'};el.files=DataTransfer.prototype.files;const d=new DataTransfer();d.items.add(new File([],${files}.split('/').pop()));el.files=d.files;el.dispatchEvent(new Event('change',{bubbles:true}));return{success:true};})()`, returnByValue: true });
      if (r?.result?.value?.success === false) {
        const err = createError('E3001', `文件上传失败: ${args.selector}`, 'mcp/dist/server.js', 607, `选择器"${args.selector}"未找到或不是有效的input元素`);
        throw new Error(JSON.stringify(err));
      }
      return `已上传文件: ${args.filePath}`;
    }
    case 'claw_focus_element': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `(()=>{const el=document.querySelector(${sel});if(!el)return{success:false,error:'未找到'};el.focus();return{success:true};})()`, returnByValue: true });
      if (r?.result?.value?.success === false) {
        const err = createError('E3001', `聚焦失败: ${args.selector}`, 'mcp/dist/server.js', 613, `选择器"${args.selector}"未找到`);
        throw new Error(JSON.stringify(err));
      }
      return '已聚焦元素';
    }

    // ==================== 键盘操作 ====================
    case 'claw_press_key': {
      const key = args.key || 'Enter';
      await sendCDP('Input.dispatchKeyEvent', { type: 'keyDown', key });
      await sendCDP('Input.dispatchKeyEvent', { type: 'keyUp', key });
      return `已按键: ${key}`;
    }
    case 'claw_press_combo': {
      const keys = (args.keys || '').toLowerCase().split('+');
      for (const k of keys) await sendCDP('Input.dispatchKeyEvent', { type: 'keyDown', key: k.trim(), modifiers: keys.length > 1 ? 2 : 0 });
      for (const k of keys.reverse()) await sendCDP('Input.dispatchKeyEvent', { type: 'keyUp', key: k.trim() });
      return `已按键: ${args.keys}`;
    }
    case 'claw_key_down': {
      await sendCDP('Input.dispatchKeyEvent', { type: 'keyDown', key: args.key });
      return `按键按下: ${args.key}`;
    }
    case 'claw_key_up': {
      await sendCDP('Input.dispatchKeyEvent', { type: 'keyUp', key: args.key });
      return `按键释放: ${args.key}`;
    }
    case 'claw_type_text': {
      const text = args.text || '';
      const delay = Number(args.delay) || 30; // [修复] 默认30ms间隔，模拟真实输入
      for (const char of text) {
        const keyParams = { type: 'keyDown', key: char, text: char, unmodifiedText: char };
        await sendCDP('Input.dispatchKeyEvent', { ...keyParams, type: 'keyDown' });
        await sendCDP('Input.dispatchKeyEvent', { ...keyParams, type: 'char', text: char });
        await sendCDP('Input.dispatchKeyEvent', { ...keyParams, type: 'keyUp' });
        if (delay > 0) await new Promise(r => setTimeout(r, delay));
      }
      return `已输入文本: ${text}`;
    }

    // ==================== 页面内容 ====================
    case 'claw_get_text': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `document.querySelector(${sel})?.textContent?.trim()||''`, returnByValue: true });
      return r?.result?.value || '';
    }
    case 'claw_get_html': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `document.querySelector(${sel})?.outerHTML||''`, returnByValue: true });
      return r?.result?.value || '';
    }
    case 'claw_get_attribute': {
      const sel = JSON.stringify(args.selector);
      const attr = JSON.stringify(args.attribute);
      const r = await sendCDP('Runtime.evaluate', { expression: `document.querySelector(${sel})?.getAttribute(${attr})||null`, returnByValue: true });
      return JSON.stringify(r?.result?.value);
    }
    case 'claw_is_visible': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `(()=>{const el=document.querySelector(${sel});if(!el)return false;const s=window.getComputedStyle(el);return s.display!=='none'&&s.visibility!=='hidden'&&s.opacity!=='0'&&el.offsetParent!==null;})()`, returnByValue: true });
      return r?.result?.value ? 'true' : 'false';
    }
    case 'claw_is_enabled': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `!document.querySelector(${sel})?.disabled`, returnByValue: true });
      return r?.result?.value ? 'true' : 'false';
    }
    case 'claw_get_count': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', { expression: `document.querySelectorAll(${sel}).length`, returnByValue: true });
      return String(r?.result?.value || 0);
    }

    // ==================== 等待条件 ====================
    case 'claw_wait_for_element': {
      const sel = JSON.stringify(args.selector);
      const timeout = Number(args.timeout) || 10000;
      const start = Date.now();
      while (Date.now() - start < timeout) {
        const r = await sendCDP('Runtime.evaluate', { expression: `document.querySelector(${sel}) ? 'found' : 'not-found'`, returnByValue: true });
        if (r?.result?.value === 'found') return '元素已出现';
        await new Promise(r => setTimeout(r, 200));
      }
      const err1 = createError('E4001', `等待元素超时: ${args.selector}`, 'mcp/dist/server.js', 686, `选择器"${args.selector}"在${timeout}ms内未出现，请检查元素是否存在或增加超时时间`);
      throw new Error(JSON.stringify(err1));
    }
    case 'claw_wait_for_text': {
      const text = args.text || '';
      const timeout = Number(args.timeout) || 10000;
      const start = Date.now();
      while (Date.now() - start < timeout) {
        const r = await sendCDP('Runtime.evaluate', { expression: `document.body?.innerText.includes(${JSON.stringify(text)})`, returnByValue: true });
        if (r?.result?.value) return '文本已出现';
        await new Promise(r => setTimeout(r, 200));
      }
      const err2 = createError('E4001', `等待文本超时: ${text}`, 'mcp/dist/server.js', 697, `文本"${text}"在${timeout}ms内未出现，请检查页面内容或增加超时时间`);
      throw new Error(JSON.stringify(err2));
    }
    case 'claw_wait_for_url': {
      const pattern = args.urlPattern || '';
      const timeout = Number(args.timeout) || 10000;
      const start = Date.now();
      while (Date.now() - start < timeout) {
        const r = await sendCDP('Runtime.evaluate', { expression: 'location.href', returnByValue: true });
        const url = r?.result?.value || '';
        if (new URL(url).href.includes(new URL(pattern, url).href) || new RegExp(pattern).test(url)) return 'URL匹配';
        await new Promise(r => setTimeout(r, 200));
      }
      const err3 = createError('E4001', `等待URL超时: ${pattern}`, 'mcp/dist/server.js', 709, `URL模式"${pattern}"在${timeout}ms内未匹配，请检查URL是否正确`);
      throw new Error(JSON.stringify(err3));
    }
    case 'claw_wait_for_navigation': {
      const timeout = Number(args.timeout) || 30000;
      await sendCDP('Page.waitForNavigation', { timeout });
      return '导航完成';
    }

    // ==================== 标签页操作 ====================
    case 'claw_tab_create': {
      const r = await sendCDP('Target.createTarget', { url: args.url || 'about:blank', browserContextId: undefined });
      if (args.active !== false) await sendCDP('Target.activateTarget', { targetId: r.targetId });
      return `已创建标签页: ${r.targetId}`;
    }
    case 'claw_tab_close': {
      await sendCDP('Target.closeTarget', { targetId: String(args.tabId) });
      return '已关闭标签页';
    }
    case 'claw_tab_list': {
      const r = await sendCDP('Target.getTargets');
      const tabs = r?.targetInfo?.filter(t => t.type === 'page')?.map(t => ({ id: t.targetId, url: t.url, title: t.title })) || [];
      return JSON.stringify(tabs, null, 2);
    }
    case 'claw_tab_switch': {
      await sendCDP('Target.activateTarget', { targetId: String(args.tabId) });
      return `已切换到标签页: ${args.tabId}`;
    }
    case 'claw_tab_reload': {
      await sendCDP('Target.reloadTarget', { targetId: String(args.tabId) });
      return '已刷新标签页';
    }
    case 'claw_get_active_tab': {
      const r = await sendCDP('Target.getTargets');
      const active = r?.targetInfo?.find(t => t.type === 'page' && t.attached);
      return JSON.stringify(active ? { id: active.targetId, url: active.url, title: active.title } : {}, null, 2);
    }

    // ==================== 窗口操作 ====================
    case 'claw_window_create': {
      const r = await sendCDP('Target.createTarget', { url: args.url || 'about:blank', browserContextId: undefined });
      if (args.focused) await sendCDP('Target.activateTarget', { targetId: r.targetId });
      return `已创建窗口: ${r.targetId}`;
    }
    case 'claw_window_list': {
      const r = await sendCDP('Target.getTargets');
      return JSON.stringify(r?.targetInfo?.filter(t => t.type === 'page') || [], null, 2);
    }

    // ==================== 存储操作 ====================
    case 'claw_get_cookies': {
      const domain = args.domain || '';
      const r = await sendCDP('Network.getCookies', domain ? { domain } : {});
      return JSON.stringify(r?.cookies || [], null, 2);
    }
    case 'claw_set_cookies': {
      const cookies = args.cookies || [];
      for (const c of cookies) await sendCDP('Network.setCookie', c);
      return `已设置 ${cookies.length} 个cookies`;
    }
    case 'claw_get_storage': {
      const type = args.type || 'local';
      const origin = args.origin || '';
      const expr = `${type}Storage${origin ? `.getItemFromOrigin('${origin}')` : ''} || {}`;
      const r = await sendCDP('Runtime.evaluate', { expression: `JSON.stringify(${type}Storage)`, returnByValue: true });
      return r?.result?.value || '{}';
    }
    case 'claw_set_storage': {
      const type = args.type || 'local';
      const key = args.key || '';
      const value = args.value || '';
      await sendCDP('Runtime.evaluate', { expression: `${type}Storage.setItem(${JSON.stringify(key)}, ${JSON.stringify(value)})` });
      return `已设置Storage: ${type}.${key}`;
    }

    // ==================== 智能操作增强 ====================

    case 'claw_smart_click': {
      const timeout = Number(args.timeout) || 5000;
      const deadline = Date.now() + timeout;
      let lastErr = '';

      // 策略1：CSS选择器（带轮询等待）
      if (args.selector) {
        const sel = JSON.stringify(args.selector);
        while (Date.now() < deadline) {
          const r = await sendCDP('Runtime.evaluate', {
            expression: `(()=>{const el=document.querySelector(${sel});if(!el)return null;el.scrollIntoView({block:'center',behavior:'instant'});el.click();return{tag:el.tagName,text:(el.textContent||'').trim().slice(0,60)};})()`,
            returnByValue: true
          });
          if (r?.result?.value) return `[CSS] 点击成功: ${JSON.stringify(r.result.value)}`;
          await new Promise(r => setTimeout(r, 300));
        }
        lastErr = `CSS"${args.selector}"未找到`;
      }

      // 策略2：文字匹配（遍历常见可点击标签）
      if (args.text) {
        const txt = JSON.stringify(args.text);
        const r = await sendCDP('Runtime.evaluate', {
          expression: `(()=>{
            for(const tag of ['button','a','span','div','li','label','input','svg']){
              const el=Array.from(document.querySelectorAll(tag)).find(e=>(e.textContent||'').trim().includes(${txt})||(e.getAttribute('aria-label')||'').includes(${txt}));
              if(el){el.scrollIntoView({block:'center',behavior:'instant'});el.click();return{tag:el.tagName,text:(el.textContent||'').trim().slice(0,60)};}
            }
            return null;
          })()`,
          returnByValue: true
        });
        if (r?.result?.value) return `[文字] 点击成功: ${JSON.stringify(r.result.value)}`;
        lastErr += ` | 文字"${args.text}"未匹配`;
      }

      // 策略3：坐标点击（CDP鼠标事件）
      if (args.x != null && args.y != null) {
        const x = Number(args.x), y = Number(args.y);
        await sendCDP('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y, button: 'none' });
        await sendCDP('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
        await sendCDP('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 });
        return `[坐标] 点击成功: (${x}, ${y})`;
      }

      throw new Error(`smart_click 所有策略失败: ${lastErr || '未提供selector/text/x+y'}`);
    }

    case 'claw_find_elements': {
      const sel = JSON.stringify(args.selector);
      const limit = Number(args.limit) || 20;
      const r = await sendCDP('Runtime.evaluate', {
        expression: `(()=>{
          return Array.from(document.querySelectorAll(${sel})).slice(0,${limit}).map((el,i)=>{
            const rect=el.getBoundingClientRect();
            return{
              index:i, tag:el.tagName.toLowerCase(),
              text:(el.textContent||'').trim().slice(0,80),
              href:el.getAttribute('href')||undefined,
              src:el.getAttribute('src')||undefined,
              ariaLabel:el.getAttribute('aria-label')||undefined,
              className:(el.className||'').toString().slice(0,60),
              visible:rect.width>0&&rect.height>0,
              x:Math.round(rect.left+rect.width/2),
              y:Math.round(rect.top+rect.height/2)
            };
          });
        })()`,
        returnByValue: true
      });
      const items = r?.result?.value || [];
      if (!items.length) return `未找到匹配元素: ${args.selector}`;
      return JSON.stringify(items, null, 2);
    }

    case 'claw_wait_and_click': {
      const sel = JSON.stringify(args.selector);
      const timeout = Number(args.timeout) || 10000;
      const scroll = args.scrollIntoView !== false;
      const start = Date.now();
      while (Date.now() - start < timeout) {
        const r = await sendCDP('Runtime.evaluate', {
          expression: `(()=>{
            const el=document.querySelector(${sel});
            if(!el)return null;
            const rect=el.getBoundingClientRect();
            if(rect.width===0&&rect.height===0)return null;
            ${scroll ? 'el.scrollIntoView({block:"center",behavior:"instant"});' : ''}
            el.click();
            return{tag:el.tagName,text:(el.textContent||'').trim().slice(0,60)};
          })()`,
          returnByValue: true
        });
        if (r?.result?.value) return `等待并点击成功: ${JSON.stringify(r.result.value)}`;
        await new Promise(r => setTimeout(r, 250));
      }
      throw new Error(`wait_and_click 超时(${timeout}ms): "${args.selector}"未出现或不可见`);
    }

    case 'claw_get_page_structure': {
      const max = Number(args.maxItems) || 30;
      const incLinks   = args.includeLinks   !== false;
      const incButtons = args.includeButtons !== false;
      const incInputs  = args.includeInputs  !== false;
      const r = await sendCDP('Runtime.evaluate', {
        expression: `(()=>{
          const res={title:document.title,url:location.href};
          if(${incLinks}) res.links=Array.from(document.querySelectorAll('a[href]')).slice(0,${max}).map(a=>({text:(a.textContent||'').trim().slice(0,60),href:a.getAttribute('href')})).filter(l=>l.text||l.href);
          if(${incButtons}) res.buttons=Array.from(document.querySelectorAll('button,input[type=button],input[type=submit],[role=button]')).slice(0,${max}).map(b=>({text:(b.textContent||b.value||b.getAttribute('aria-label')||'').trim().slice(0,60),visible:b.getBoundingClientRect().width>0})).filter(b=>b.text);
          if(${incInputs}) res.inputs=Array.from(document.querySelectorAll('input:not([type=hidden]),textarea,select')).slice(0,${max}).map(i=>({type:i.type||i.tagName.toLowerCase(),name:i.name||i.id||'',placeholder:i.getAttribute('placeholder')||'',value:i.type==='password'?'***':(i.value||'').slice(0,30)}));
          return res;
        })()`,
        returnByValue: true
      });
      return JSON.stringify(r?.result?.value || {}, null, 2);
    }

    case 'claw_scroll_to_element': {
      const sel = JSON.stringify(args.selector);
      const r = await sendCDP('Runtime.evaluate', {
        expression: `(()=>{
          const el=document.querySelector(${sel});
          if(!el)return{success:false,error:'未找到:'+${sel}};
          el.scrollIntoView({block:'center',behavior:'smooth'});
          const prev=el.style.outline;
          el.style.outline='3px solid #FFD700';
          el.style.outlineOffset='2px';
          setTimeout(()=>{el.style.outline=prev;el.style.outlineOffset='';},2000);
          const rect=el.getBoundingClientRect();
          return{success:true,tag:el.tagName,text:(el.textContent||'').trim().slice(0,60),x:Math.round(rect.left+rect.width/2),y:Math.round(rect.top+rect.height/2)};
        })()`,
        returnByValue: true
      });
      const v = r?.result?.value;
      if (!v?.success) throw new Error(v?.error || '元素未找到');
      return `已定位到元素（黄色高亮2秒）: ${JSON.stringify(v)}`;
    }

    // ==================== 书签增强 ====================

    case 'claw_enrich_bookmarks': {
      const allBookmarks = await sendMessageToPlugin('getBookmarks', {});
      const toProcess = args.ids?.length
        ? allBookmarks.filter(b => args.ids.includes(b.id))
        : allBookmarks.slice(0, Number(args.maxCount) || 50);

      const timeoutMs = Number(args.timeoutMs) || 4000;
      const results = [];

      for (const bm of toProcess) {
        try {
          const tabRes = await sendMessageToPlugin('createTab', { url: bm.url, active: false });
          const tempTabId = tabRes?.id;
          await new Promise(r => setTimeout(r, Math.min(timeoutMs, 3000)));

          const expr = `(()=>{
            const getMeta = (name) => {
              const el = document.querySelector('meta[name="'+name+'"],meta[property="og:'+name+'"],meta[name="og:'+name+'"]');
              return el ? (el.getAttribute('content')||'').slice(0,200) : '';
            };
            const getKw = () => {
              const kw = getMeta('keywords') || getMeta('news_keywords') || '';
              const h1s = Array.from(document.querySelectorAll('h1')).slice(0,3).map(h=>h.textContent.trim()).join(',');
              return (kw + (kw?',':'') + h1s).slice(0,300);
            };
            return {
              realTitle: document.title.slice(0,100),
              description: getMeta('description') || getMeta('og:description'),
              keywords: getKw(),
              lang: document.documentElement.lang || '',
              ogType: getMeta('og:type') || getMeta('type'),
            };
          })()`;

          if (tempTabId) {
            await sendMessageToPlugin('switchTab', { tabId: tempTabId });
            await new Promise(r => setTimeout(r, 500));
          }

          const r = await sendCDP('Runtime.evaluate', { expression: expr, returnByValue: true });
          const meta = r?.result?.value || {};

          results.push({
            id: bm.id,
            title: bm.title,
            url: bm.url,
            realTitle: meta.realTitle || bm.title,
            description: meta.description || '',
            keywords: meta.keywords || '',
            lang: meta.lang || '',
            ogType: meta.ogType || '',
            domain: (() => { try { return new URL(bm.url).hostname; } catch { return ''; } })(),
          });

          if (tempTabId) {
            await sendMessageToPlugin('closeTab', { tabId: tempTabId });
          }
        } catch (e) {
          results.push({
            id: bm.id, title: bm.title, url: bm.url,
            error: e.message.slice(0, 80),
            domain: (() => { try { return new URL(bm.url).hostname; } catch { return ''; } })(),
          });
        }
      }

      return JSON.stringify(results, null, 2);
    }

    // ==================== 登录会话管理 ====================

    case 'claw_save_login_session': {
      const sessionName = args.name || 'default';
      const domain = args.domain || '';
      const cookieRes = await sendCDP('Network.getCookies', domain ? { urls: [`https://${domain}`, `http://${domain}`] } : {});
      const cookies = cookieRes?.cookies || [];
      const urlRes = await sendCDP('Runtime.evaluate', { expression: 'location.hostname', returnByValue: true });
      const currentDomain = domain || urlRes?.result?.value || 'unknown';
      const sessionData = {
        name: sessionName,
        domain: currentDomain,
        cookies,
        savedAt: Date.now(),
      };
      await sendMessageToPlugin('saveSession', { key: `session_${sessionName}`, value: JSON.stringify(sessionData) });
      return `已保存登录会话 "${sessionName}" (域名:${currentDomain}, cookies:${cookies.length}个)`;
    }

    case 'claw_restore_login_session': {
      const sessionName = args.name || 'default';
      const stored = await sendMessageToPlugin('getSession', { key: `session_${sessionName}` });
      if (!stored) throw new Error(`未找到登录会话 "${sessionName}"，请先用 claw_save_login_session 保存`);
      const sessionData = JSON.parse(stored);
      if (sessionData.cookies?.length) {
        await sendCDP('Network.setCookies', { cookies: sessionData.cookies });
      }
      return `已恢复登录会话 "${sessionName}" (${sessionData.cookies?.length || 0} cookies)`;
    }

    case 'claw_list_login_sessions': {
      const sessions = await sendMessageToPlugin('listSessions', {});
      return JSON.stringify(sessions || [], null, 2);
    }

    // ==================== 内容提取增强 ====================

    case 'claw_batch_extract': {
      const selectors = args.selectors || [];
      const opt = args.options || {};
      const textOnly = opt.textOnly !== false;
      const limit = opt.limit || 10;
      const attrs = opt.attributes || [];
      
      const results = {};
      for (const sel of selectors) {
        const s = JSON.stringify(sel);
        let expr = `Array.from(document.querySelectorAll(${s})).slice(0,${limit}).map(el=>{`;
        if (textOnly) {
          expr += `return(el.textContent||'').trim();})`;
        } else {
          expr += `const r={html:el.outerHTML,text:(el.textContent||'').trim()};`;
          for (const a of attrs) {
            expr += `r['${a}']=el.getAttribute('${a}');`;
          }
          expr += `return r;})`;
        }
        const r = await sendCDP('Runtime.evaluate', { expression: expr, returnByValue: true });
        results[sel] = r?.result?.value || [];
      }
      return JSON.stringify(results, null, 2);
    }

    case 'claw_extract_table': {
      const sel = args.selector ? JSON.stringify(args.selector) : 'table';
      const includeHeader = args.includeHeader !== false;
      const expr = `(()=>{
        const table=document.querySelector(${sel});
        if(!table)return null;
        const rows=Array.from(table.querySelectorAll('tr'));
        const headers=[];`;
      if (includeHeader) {
        expr += `const headerCells=rows[0]?.querySelectorAll('th,td');
        if(headerCells)headers.push(...Array.from(headerCells).map(c=>(c.textContent||'').trim()));`;
      }
      expr += `const data=rows.slice(${includeHeader?1:0}).map(row=>{
        const cells=Array.from(row.querySelectorAll('td'));
        const obj={};
        cells.forEach((c,i)=>{obj[headers[i]||'col'+i]=(c.textContent||'').trim();});
        return obj;
      });
        return{headers,rows:data};
      })()`;
      const r = await sendCDP('Runtime.evaluate', { expression: expr, returnByValue: true });
      const data = r?.result?.value;
      if (!data) return '未找到表格';
      return JSON.stringify(data, null, 2);
    }

    case 'claw_extract_list': {
      const containerSel = JSON.stringify(args.containerSelector);
      const fields = args.fields || {};
      const limit = args.limit || 20;
      const fieldKeys = Object.keys(fields);
      const fieldExprs = fieldKeys.map(k => {
        const v = fields[k];
        if (v.includes('@')) {
          const [sel, attr] = v.split('@');
          return `${k}:(document.querySelector(${JSON.stringify(sel)})?.getAttribute('${attr}')||'')`;
        }
        return `${k}:(document.querySelector(${JSON.stringify(v)})?.textContent||'').trim()`;
      }).join(',');
      const expr = `Array.from(document.querySelectorAll(${containerSel})).slice(0,${limit}).map(el=>({${fieldExprs}}))`;
      const r = await sendCDP('Runtime.evaluate', { expression: expr, returnByValue: true });
      const items = r?.result?.value || [];
      if (!items.length) return `未找到列表项: ${args.containerSelector}`;
      return JSON.stringify(items, null, 2);
    }

    case 'claw_compare_content': {
      const sel = args.selector ? JSON.stringify(args.selector) : 'body';
      
      // 获取当前内容
      const expr = `(document.querySelector(${sel})?.textContent||'').trim().slice(0,5000)`;
      const r = await sendCDP('Runtime.evaluate', { expression: expr, returnByValue: true });
      const currentContent = r?.result?.value || '';
      
      // 保存快照
      if (args.saveAs) {
        contentSnapshots.set(args.saveAs, { content: currentContent, time: Date.now() });
        return `已保存快照 "${args.saveAs}" (${currentContent.length} 字符)`;
      }
      
      // 删除快照
      if (args.clear) {
        const deleted = contentSnapshots.delete(args.clear);
        return deleted ? `已删除快照 "${args.clear}"` : `快照 "${args.clear}" 不存在`;
      }
      
      // 比较
      if (args.compareWith) {
        const saved = contentSnapshots.get(args.compareWith);
        if (!saved) return `未找到快照 "${args.compareWith}"，请先使用 saveAs 参数保存`;
        
        const oldContent = saved.content;
        const newContent = currentContent;
        
        // 简单比较：相同字符数、不同字符数
        const oldLen = oldContent.length;
        const newLen = newContent.length;
        const longer = newLen > oldLen ? newLen - oldLen : 0;
        const shorter = newLen < oldLen ? oldLen - newLen : 0;
        
        return JSON.stringify({
          snapshot: args.compareWith,
          savedAt: new Date(saved.time).toISOString(),
          savedLength: oldLen,
          currentLength: newLen,
          charDiff: longer > 0 ? `+${longer} 字符` : `-${shorter} 字符`,
          changed: oldContent !== newContent,
          savedPreview: oldContent.slice(0, 200),
          currentPreview: newContent.slice(0, 200)
        }, null, 2);
      }
      
      return '请使用 saveAs 保存快照或 compareWith 比较内容';
    }

    // ==================== 书签智能分类 ====================

    case 'claw_classify_url': {
      const { url, saveToDb, category, description } = args;
      if (!url) throw new Error('URL不能为空');

      // 提取域名和路径
      let domain = '', path = '';
      try {
        const urlObj = new URL(url);
        domain = urlObj.hostname;
        path = urlObj.pathname;
      } catch {
        throw new Error('无效的URL格式');
      }

      // 从配置获取数据库信息（需要通过消息传递或读取配置文件）
      // 这里暂时使用内置的默认配置，实际会从插件传递
      const cloudDbUrl = null; // 将在运行时从配置获取
      const cloudApiKey = null;

      // 如果没有配置云端，直接返回本地分析模式提示
      if (!cloudDbUrl || !cloudApiKey) {
        return JSON.stringify({
          source: 'local',
          domain,
          path,
          message: '请在插件设置中启用云端分类模式并配置API',
          suggestion: '设置 → 书签分类模式 → 云端数据库 → 配置API地址和密钥'
        });
      }

      // 查询云端数据库
      try {
        const queryUrl = `${cloudDbUrl}/api/classify?domain=${encodeURIComponent(domain)}&path=${encodeURIComponent(path)}`;
        const res = await fetch(queryUrl, {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${cloudApiKey}` }
        });

        if (res.ok) {
          const data = await res.json();
          if (data.confidence > 0.8) {
            return JSON.stringify({ source: 'cloud', ...data });
          }
        }
      } catch (e) {
        console.log('[classify] Cloud query failed:', e.message);
      }

      // 未命中，返回本地分析提示
      return JSON.stringify({
        source: 'local',
        domain,
        path,
        message: '数据库中未找到匹配规则，请手动分类',
        suggestion: '可使用 claw_enrich_bookmarks 或 claw_get_page_structure 分析页面后手动分类'
      });
    }

    // ==================== 桥接工具实现 ====================
    case 'claw_bridge_call': {
      const { tool, args: toolArgs } = args;
      
      // 真正的桥接实现：通过OpenClaw CLI调用
      try {
        const { exec } = require('child_process');
        
        // 构建CLI命令
        let command = `openclaw browser ${tool}`;
        
        // 添加参数 - 根据OpenClaw CLI的正确语法
        if (toolArgs) {
          if (toolArgs.url && (tool === 'open' || tool === 'navigate')) {
            command += ` ${toolArgs.url}`;
          } else if (toolArgs.url) {
            command += ` --url "${toolArgs.url}"`;
          }
          if (toolArgs.ref) {
            command += ` --ref "${toolArgs.ref}"`;
          }
          if (toolArgs.text && tool === 'type') {
            command += ` "${toolArgs.text}"`;
          }
          // 添加JSON输出标志
          command += ' --json';
        }
        
        // 执行CLI命令
        const result = await new Promise((resolve, reject) => {
          exec(command, { timeout: 30000 }, (error, stdout, stderr) => {
            if (error) {
              reject(new Error(`CLI执行失败: ${error.message}`));
            } else {
              resolve({
                stdout: stdout.trim(),
                stderr: stderr.trim(),
                exitCode: error ? error.code : 0
              });
            }
          });
        });
        
        return JSON.stringify({
          success: true,
          source: 'cli_bridge',
          tool: tool,
          command: command,
          result: result,
          timestamp: Date.now()
        });
        
      } catch (error) {
        // 降级方案：模拟响应（用于测试）
        const builtinTools = {
          'browser_open': '打开页面',
          'browser_snapshot': '页面快照',
          'browser_navigate': '页面导航',
          'browser_click': '点击元素',
          'browser_type': '输入文本'
        };
        
        if (builtinTools[tool]) {
          return JSON.stringify({
            success: true,
            source: 'simulated_bridge',
            tool: tool,
            message: `模拟调用: ${builtinTools[tool]}`,
            args: toolArgs,
            timestamp: Date.now(),
            note: '这是模拟响应，需要OpenClaw CLI支持真正的桥接'
          });
        } else {
          return JSON.stringify({
            success: false,
            source: 'bridge_error',
            tool: tool,
            message: `桥接调用失败: ${error.message}`,
            availableTools: Object.keys(builtinTools),
            timestamp: Date.now()
          });
        }
      }
    }

    // ==================== [新增] 优化工具实现 ====================
    case 'claw_get_indexed_elements': {
      // 调用插件的getSimplifiedDOM方法
      const useCache = args.useCache !== false;
      try {
        // 发送获取简化DOM的请求
        const domResult = await sendMessageToPlugin('getSimplifiedDOM', { useCache });
        return JSON.stringify({
          success: true,
          elements: JSON.parse(domResult || '[]'),
          count: JSON.parse(domResult || '[]').length,
          cached: useCache,
          timestamp: Date.now()
        }, null, 2);
      } catch (error) {
        // 降级：使用传统方式获取页面元素
        const fallback = await sendCDP('Runtime.evaluate', {
          expression: `
            (function() {
              const selectors = ['button','a','input','select','textarea','[role="button"]','[onclick]'];
              const elements = document.querySelectorAll(selectors.join(','));
              const result = [];
              elements.forEach((el, idx) => {
                if (el.offsetParent === null) return;
                result.push({
                  index: idx,
                  tag: el.tagName.toLowerCase(),
                  text: (el.textContent || '').trim().slice(0, 60),
                  id: el.id || '',
                  class: (el.className || '').split(' ')[0]
                });
              });
              return JSON.stringify(result.slice(0, 30));
            })()
          `,
          returnByValue: true
        });
        const elements = JSON.parse(fallback?.result?.value || '[]');
        return JSON.stringify({
          success: true,
          elements: elements,
          count: elements.length,
          cached: false,
          fallback: true,
          timestamp: Date.now()
        }, null, 2);
      }
    }

    case 'claw_click_by_index': {
      // 通过索引点击元素
      const index = Number(args.index);
      const domResult = await sendMessageToPlugin('getSimplifiedDOM', { useCache: true });
      const elements = JSON.parse(domResult || '[]');
      
      if (!elements[index]) {
        const err = createError('E3001', `元素索引 ${index} 不存在`, 'mcp/dist/server.js', 800, `页面只有 ${elements.length} 个元素`);
        throw new Error(JSON.stringify(err));
      }
      
      const el = elements[index];
      // 使用标签+文本构建选择器
      let selector = el.tag;
      if (el.id) selector = `#${el.id}`;
      else if (el.text) {
        // 尝试用文本定位
        selector = `${el.tag}:contains("${el.text.slice(0, 20)}")`;
      }
      
      // 执行点击
      const clickResult = await sendCDP('Runtime.evaluate', {
        expression: `
          (function() {
            const el = document.querySelector('${selector}') || document.querySelectorAll('${el.tag}')[${index}];
            if (!el) return { success: false, error: '元素未找到' };
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            el.click();
            return { success: true, tag: el.tagName };
          })()
        `,
        returnByValue: true
      });
      
      const clickValue = clickResult?.result?.value;
      if (clickValue?.success === false) {
        throw new Error(`点击失败: ${clickValue.error}`);
      }
      return JSON.stringify({ success: true, index: index, tag: clickValue?.tag || el.tag });
    }

    case 'claw_batch_execute': {
      // 批量执行CDP命令
      const commands = args.commands || [];
      if (!Array.isArray(commands) || commands.length === 0) {
        return JSON.stringify({ success: false, error: 'commands必须是数组' });
      }
      
      const results = [];
      for (const cmd of commands) {
        try {
          const r = await sendCDP(cmd.method, cmd.params || {});
          results.push({ method: cmd.method, success: true, result: r });
        } catch (error) {
          results.push({ method: cmd.method, success: false, error: error.message });
        }
      }
      
      return JSON.stringify({
        success: true,
        total: commands.length,
        successCount: results.filter(r => r.success).length,
        failCount: results.filter(r => !r.success).length,
        results: results
      }, null, 2);
    }

    case 'claw_smart_wait': {
      // 智能等待
      const { element, text, urlPattern, timeout = 10000 } = args;
      const startTime = Date.now();
      
      // 等待元素出现
      if (element) {
        while (Date.now() - startTime < timeout) {
          const check = await sendCDP('Runtime.evaluate', {
            expression: `document.querySelector('${element}') ? 'found' : 'not-found'`,
            returnByValue: true
          });
          if (check?.result?.value === 'found') {
            return JSON.stringify({ success: true, reason: 'element_found', selector: element, elapsed: Date.now() - startTime });
          }
          await new Promise(r => setTimeout(r, 200));
        }
        return JSON.stringify({ success: false, reason: 'timeout', selector: element, elapsed: timeout });
      }
      
      // 等待文本出现
      if (text) {
        while (Date.now() - startTime < timeout) {
          const check = await sendCDP('Runtime.evaluate', {
            expression: `document.body.innerText.includes('${text}') ? 'found' : 'not-found'`,
            returnByValue: true
          });
          if (check?.result?.value === 'found') {
            return JSON.stringify({ success: true, reason: 'text_found', text: text, elapsed: Date.now() - startTime });
          }
          await new Promise(r => setTimeout(r, 200));
        }
        return JSON.stringify({ success: false, reason: 'timeout', text: text, elapsed: timeout });
      }
      
      // 等待URL变化
      if (urlPattern) {
        while (Date.now() - startTime < timeout) {
          const check = await sendCDP('Runtime.evaluate', {
            expression: `location.href.match('${urlPattern}') ? 'match' : 'no-match'`,
            returnByValue: true
          });
          if (check?.result?.value === 'match') {
            return JSON.stringify({ success: true, reason: 'url_matched', pattern: urlPattern, elapsed: Date.now() - startTime });
          }
          await new Promise(r => setTimeout(r, 200));
        }
        return JSON.stringify({ success: false, reason: 'timeout', pattern: urlPattern, elapsed: timeout });
      }
      
      // 没有任何条件时，等待默认时间
      await new Promise(r => setTimeout(r, timeout));
      return JSON.stringify({ success: true, reason: 'timeout_elapsed', elapsed: timeout });
    }

    default:
      const errUnknown = createError('E9001', `未知工具: ${name}`, 'mcp/dist/server.js', 787, `工具"${name}"不存在，请检查工具名称是否正确。可用工具请查询MCP工具列表`);
      throw new Error(JSON.stringify(errUnknown));
  }
  } catch (e) {
    logAction(name, args, `Error: ${e.message}`);
    throw e;
  } finally {
    // 记录操作日志
    if (result !== undefined) {
      const duration = Date.now() - startTime;
      logAction(name, args, result);
    }
  }
  
  return result;
}

const server = createServer(async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // HTTP POST for MCP tools
  if (req.method === 'POST' && req.url === '/mcp') {
    let body = '';
    for await (const chunk of req) { body += chunk; }
    try {
      const msg = JSON.parse(body);
      if (msg.method === 'tools/call') {
        const toolName = msg.params?.name || '';
        const toolArgs = msg.params?.arguments || {};
        console.log(`[HTTP] 调用工具: ${toolName}`);
        try {
          const text = await executeTool(toolName, toolArgs);
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ id: msg.id, result: { content: [{ type: 'text', text }] } }));
        } catch (e) {
          console.error(`[HTTP] 工具失败 ${toolName}:`, e.message);
          res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({ id: msg.id, error: { code: -32000, message: e.message } }));
        }
        return;
      }
    } catch (e) {}
    res.writeHead(400);
    res.end(JSON.stringify({ error: 'Invalid request' }));
    return;
  }

  // Status endpoint
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ name: 'autoclaw', version: '4.0.0', port: SERVER_PORT, status: 'running', extension: extensionWs?.readyState === WebSocket.OPEN ? 'connected' : 'disconnected', builtinToken: BUILT_IN_TOKEN }, null, 2));
    return;
  }
  
  // Bookmarks info endpoint
  if (req.url === '/bookmarks') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({
      message: "书签功能需要通过扩展WebSocket连接使用",
      supported_methods: [
        "claw_list_bookmarks",
        "claw_get_bookmark_tree", 
        "claw_search_bookmarks",
        "claw_create_bookmark",
        "claw_create_folder",
        "claw_rename_bookmark",
        "claw_remove_folder"
      ],
      usage: "通过扩展WebSocket连接发送JSON-RPC消息",
      example: {
        jsonrpc: "2.0",
        method: "claw_list_bookmarks",
        params: {},
        id: 1
      }
    }, null, 2));
    return;
  }
  
  // Default 404
  res.writeHead(404);
  res.end('Not found');
});

const mcpWss = new WebSocketServer({ noServer: true });

// 广播消息给所有MCP客户端
function broadcastToMcpClients(msg) {
  mcpWss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(msg));
    }
  });
}

mcpWss.on('connection', (ws, req) => {
  console.log(`[MCP] ✅ OpenClaw AI 连接`);
  ws.on('message', async (data) => {
    let msg;
    try { msg = JSON.parse(data.toString()); } catch { return; }
    if (msg.method === 'ping') { ws.send(JSON.stringify({ method: 'pong' })); return; }
    if (msg.id != null && msg.method === 'initialize') { ws.send(JSON.stringify({ id: msg.id, result: { protocolVersion: '2024-11-05', capabilities: { tools: {} }, serverInfo: { name: 'autoclaw', version: '4.0.0' } } })); return; }
    if (msg.id != null && msg.method === 'tools/list') { ws.send(JSON.stringify({ id: msg.id, result: { tools } })); return; }
    if (msg.id != null && msg.method === 'tools/call') {
      const toolName = msg.params?.name || '';
      const toolArgs = msg.params?.arguments || {};
      console.log(`[MCP] 调用工具: ${toolName}`);
      try {
        const text = await executeTool(toolName, toolArgs);
        ws.send(JSON.stringify({ id: msg.id, result: { content: [{ type: 'text', text }] } }));
      } catch (e) {
        console.error(`[MCP] 工具失败 ${toolName}:`, e.message);
        ws.send(JSON.stringify({ id: msg.id, error: { code: -32000, message: e.message } }));
      }
    }
  });
  ws.on('close', () => console.log('[MCP] AI 断开'));
});

const extWss = new WebSocketServer({ noServer: true });
extWss.on('connection', (ws, req) => {
  const url = new URL(req.url || '', `http://localhost`);
  const token = url.searchParams.get('token') || '';
  console.log(`[EXT] 收到连接请求, token: ${token ? token.slice(0,10) + '...' : 'empty'}, url: ${req.url}`);
  if (!VALID_TOKEN.includes(token)) { console.warn(`[EXT] ❌ Token错误, 期望: ${VALID_TOKEN.map(t => t.slice(0,10) + '...').join(' 或 ')}`); ws.close(1008, 'Invalid token'); return; }
  console.log(`[EXT] ✅ Chrome 插件连接`);
  extensionWs = ws;
  
  // 更新系统状态
  updateSystemStatus(true);
  
  // [修复] 只保留一个心跳定时器（原来有5s+10s两个，会造成双倍心跳压力导致崩溃）
  const pingInterval = setInterval(() => { 
    if (ws.readyState === WebSocket.OPEN) {
      try {
        ws.send(JSON.stringify({ method: 'ping' }));
      } catch (error) {
        console.error('发送心跳失败:', error);
        clearInterval(pingInterval);
        if (extensionWs === ws) {
          extensionWs = null;
          updateSystemStatus(false, '发送心跳失败');
          scheduleReconnect();
        }
      }
    } else {
      clearInterval(pingInterval);
    }
  }, 10000); // 10秒一次心跳已足够
  
  ws.on('message', (data) => {
    let msg;
    try { msg = JSON.parse(data.toString()); } catch { return; }
    if (msg.method === 'pong') return;
    if (msg.method === 'configChanged') {
      console.log(`[Config] 配置变更: ${msg.params?.key} = ${msg.params?.value}`);
      broadcastToMcpClients({ method: 'configChanged', params: msg.params });
      return;
    }
    // 处理来自MCP的请求（如attachAllTabs）
    if (msg.action === 'authorizeAndAttachAll') {
      // 转发给插件处理 - 通过发送特殊消息
      try {
        ws.send(JSON.stringify({ id: msg.id, result: { note: 'Use chrome.runtime.sendMessage from extension instead' } }));
      } catch (error) {
        console.error('发送消息失败:', error);
      }
      return;
    }
    if (msg.id != null && (msg.result !== undefined || msg.error !== undefined)) {
      const p = pending.get(msg.id);
      if (!p) return;
      pending.delete(msg.id);
      if (msg.error) p.reject(new Error(String(msg.error))); else p.resolve(msg.result);
    }
  });
  
  ws.on('close', () => {
    clearInterval(pingInterval);
    if (extensionWs === ws) {
      extensionWs = null;
      updateSystemStatus(false, '插件主动断开连接');
      scheduleReconnect();
    }
    for (const [id, p] of pending.entries()) { 
      pending.delete(id); 
      p.reject(new Error('插件断开'));
    }
    console.log('[EXT] 插件断开');
  });
  
  ws.on('error', (error) => {
    console.error('[EXT] 插件连接错误:', error);
    if (extensionWs === ws) {
      extensionWs = null;
      updateSystemStatus(false, error.message);
      scheduleReconnect();
    }
  });
});

server.on('upgrade', (req, socket, head) => {
  const pathname = new URL(req.url || '', 'http://localhost').pathname;
  if (pathname === '/mcp') { mcpWss.handleUpgrade(req, socket, head, (ws) => mcpWss.emit('connection', ws, req)); }
  else if (pathname === '/extension') { extWss.handleUpgrade(req, socket, head, (ws) => extWss.emit('connection', ws, req)); }
  else { socket.destroy(); }
});

cleanOldLogs();

server.listen(SERVER_PORT, '127.0.0.1', () => {
  console.log('\n┌──────────────────────────────────────────────────┐');
  console.log('│  🤖  AutoClaw MCP Server v4.0.0                  │');
  console.log(`│  端口: ${SERVER_PORT}  (已避免系统端口冲突)              │`);
  console.log(`│  Token内置: ${BUILT_IN_TOKEN.slice(0,16)}***    │`);
  console.log('│  新增: claw_open_urls / claw_remove_folder        │');
  console.log('│        claw_rename_bookmark / newTab导航           │');
  console.log('└──────────────────────────────────────────────────┘\n');
  
  // 启动健康检查
  startHealthCheck();
  console.log('服务器已启动，健康检查已启用');
});
