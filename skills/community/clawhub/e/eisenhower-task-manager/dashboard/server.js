/**
 * Eisenhower Task Dashboard Server
 * Express + WebSocket for real-time updates
 */

const express = require('express');
const expressWs = require('express-ws');
const http = require('http');
const WebSocket = require('ws');
const chokidar = require('chokidar');
const path = require('path');
const fs = require('fs');
const os = require('os');
const pty = require('node-pty');
const { 
  loadAllTasks, 
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
  copyTaskToDelegation,
  moveTaskToDelegation,
  reorderDelegationTask,
  reorderMaybeTask,
  completeTask,
  completeCustomerProject,
  completeDelegationTask,
  completeMaybeTask
} = require('./parser');

// Parse command line arguments for port
function parseArgs() {
  const args = process.argv.slice(2);
  let port = 8080;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--port' && args[i + 1]) {
      port = parseInt(args[i + 1], 10);
      i++;
    }
  }

  return { port };
}

const { port } = parseArgs();
const app = express();
const server = http.createServer(app);
expressWs(app, server);

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/node_modules', express.static(path.join(__dirname, 'node_modules')));

// Terminal WebSocket endpoint
let globalPtyProcess = null;
let terminalHistory = '';
const MAX_HISTORY = 100000; // Keep last 100k chars

app.ws('/terminal', (ws, req) => {
  console.log('[WebSocket] Terminal Client connected');
  termClients.add(ws);
  
  // Lazy initialize global PTY process
  if (!globalPtyProcess) {
    try {
      globalPtyProcess = pty.spawn(shell, [], {
        name: 'xterm-color',
        cols: 80,
        rows: 24,
        cwd: process.env.HOME || process.cwd(),
        env: process.env
      });
      
      globalPtyProcess.on('data', (data) => {
        terminalHistory += data;
        if (terminalHistory.length > MAX_HISTORY) {
          terminalHistory = terminalHistory.substring(terminalHistory.length - MAX_HISTORY);
        }
        
        // Broadcast to all active terminal clients
        termClients.forEach(clientWs => {
          if (clientWs.readyState === WebSocket.OPEN) {
            clientWs.send(data);
          }
        });
      });
    } catch (e) {
      console.error('[Terminal] Failed to spawn terminal process:', e.message);
      globalPtyProcess = {
        write: () => {},
        kill: () => {},
        resize: () => {},
        on: () => {}
      };
    }
  }
  
  // Send history to the new client
  if (terminalHistory && ws.readyState === WebSocket.OPEN) {
    // Clean terminal history to remove query escape sequences (like color or cursor position queries).
    // If we replay these queries to a new xterm.js instance, it will automatically respond to them
    // over the WebSocket, which results in garbage text being printed at the shell prompt.
    const cleanHistory = terminalHistory
      .replace(/\x1b\]1[01];\?(?:\x07|\x1b\\)/g, '') // OSC 10/11 color queries
      .replace(/\x1b\[[>?]*[0-9]*c/g, '')            // Device Attributes queries
      .replace(/\x1b\[6n/g, '');                     // Cursor position queries
      
    ws.send(cleanHistory);
  }
  
  // Handle client input and resize
  ws.on('message', (msg) => {
    try {
      const message = msg.toString();
      if (message.startsWith('{"type":"resize"')) {
        const size = JSON.parse(message);
        if (globalPtyProcess && typeof globalPtyProcess.resize === 'function') {
          globalPtyProcess.resize(size.cols, size.rows);
        }
        return;
      }
    } catch(e) {
      // Not a JSON message, handle as normal terminal input
    }
    
    if (globalPtyProcess && typeof globalPtyProcess.write === 'function') {
      globalPtyProcess.write(msg);
    }
  });
  
  ws.on('close', () => {
    console.log('[WebSocket] Terminal Client disconnected');
    termClients.delete(ws);
  });
  
  ws.on('error', (err) => {
    console.error('[WebSocket] Terminal Error:', err);
    termClients.delete(ws);
  });
});

// API endpoint to get all tasks
app.get('/api/tasks', (req, res) => {
  const data = loadAllTasks();
  res.json(data);
});

// API endpoint for health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API endpoint to move/reorder a customer project
app.post('/api/customer-projects/move', async (req, res) => {
  try {
    const { projectId, sourceCustomer, targetCustomer, insertIndex } = req.body;

    console.log('[API] Move customer project request:', { projectId, sourceCustomer, targetCustomer, insertIndex });

    if (!projectId || !sourceCustomer || !targetCustomer) {
      return res.status(400).json({
        error: 'Missing required fields: projectId, sourceCustomer, targetCustomer'
      });
    }

    const result = await moveCustomerProject(projectId, sourceCustomer, targetCustomer, insertIndex);

    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Move customer project error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to move a task between quadrants or reorder within quadrant
app.post('/api/tasks/move', async (req, res) => {
  try {
    const { taskId, sourceQuadrant, targetQuadrant, insertIndex } = req.body;
    
    console.log('[API] Move task request:', { taskId, sourceQuadrant, targetQuadrant, insertIndex });
    
    if (!taskId || !sourceQuadrant || !targetQuadrant) {
      return res.status(400).json({ 
        error: 'Missing required fields: taskId, sourceQuadrant, targetQuadrant' 
      });
    }
    
    const result = await moveTask(taskId, sourceQuadrant, targetQuadrant, insertIndex);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Move task error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to delete a task from tasks.md
app.post('/api/tasks/delete', async (req, res) => {
  try {
    const { taskId, quadrant } = req.body;
    
    console.log('[API] Delete task request:', { taskId, quadrant });
    
    if (!taskId || !quadrant) {
      return res.status(400).json({ 
        error: 'Missing required fields: taskId, quadrant' 
      });
    }
    
    const result = await deleteTask(taskId, quadrant);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Delete task error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to delete a customer project
app.post('/api/customer-projects/delete', async (req, res) => {
  try {
    const { projectId, customerName } = req.body;
    
    console.log('[API] Delete customer project request:', { projectId, customerName });
    
    if (!projectId || !customerName) {
      return res.status(400).json({ 
        error: 'Missing required fields: projectId, customerName' 
      });
    }
    
    const result = await deleteCustomerProject(projectId, customerName);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Delete customer project error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to delete a delegation task
app.post('/api/delegation/delete', async (req, res) => {
  try {
    const { taskId } = req.body;
    
    console.log('[API] Delete delegation task request:', { taskId });
    
    if (!taskId) {
      return res.status(400).json({ 
        error: 'Missing required field: taskId' 
      });
    }
    
    const result = await deleteDelegationTask(taskId);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Delete delegation task error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to delete a maybe list task
app.post('/api/maybe/delete', async (req, res) => {
  try {
    const { taskId } = req.body;
    
    console.log('[API] Delete maybe task request:', { taskId });
    
    if (!taskId) {
      return res.status(400).json({ 
        error: 'Missing required field: taskId' 
      });
    }
    
    const result = await deleteMaybeTask(taskId);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Delete maybe task error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to copy a task to another quadrant
app.post('/api/tasks/copy', async (req, res) => {
  try {
    const { taskId, sourceQuadrant, target } = req.body;
    
    console.log('[API] Copy task request:', { taskId, sourceQuadrant, target });
    
    if (!taskId || !sourceQuadrant || !target) {
      return res.status(400).json({ 
        error: 'Missing required fields: taskId, sourceQuadrant, target' 
      });
    }
    
    const result = await copyTask(taskId, sourceQuadrant, target);
    
    if (result.success) {
      res.json({ success: true, message: result.message, newTaskId: result.newTaskId });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Copy task error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to copy a customer project to quadrants or delegation
app.post('/api/customer-projects/copy', async (req, res) => {
  try {
    const { projectId, sourceCustomer, target } = req.body;
    
    console.log('[API] Copy customer project request:', { projectId, sourceCustomer, target });
    
    if (!projectId || !sourceCustomer || !target) {
      return res.status(400).json({ 
        error: 'Missing required fields: projectId, sourceCustomer, target' 
      });
    }
    
    const result = await copyCustomerProject(projectId, sourceCustomer, target);
    
    if (result.success) {
      res.json({ success: true, message: result.message, newTaskId: result.newTaskId });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Copy customer project error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to move a maybe task to a quadrant
app.post('/api/maybe/move', async (req, res) => {
  try {
    const { taskId, targetQuadrant } = req.body;
    
    console.log('[API] Move maybe task request:', { taskId, targetQuadrant });
    
    if (!taskId || !targetQuadrant) {
      return res.status(400).json({ 
        error: 'Missing required fields: taskId, targetQuadrant' 
      });
    }
    
    const result = await moveMaybeTaskToQuadrant(taskId, targetQuadrant);
    
    if (result.success) {
      res.json({ success: true, message: result.message, newTaskId: result.newTaskId });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Move maybe task error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to move a quadrant task to maybe list
app.post('/api/tasks/move-to-maybe', async (req, res) => {
  try {
    const { taskId, sourceQuadrant } = req.body;
    
    console.log('[API] Move task to maybe request:', { taskId, sourceQuadrant });
    
    if (!taskId || !sourceQuadrant) {
      return res.status(400).json({ 
        error: 'Missing required fields: taskId, sourceQuadrant' 
      });
    }
    
    const result = await moveQuadrantTaskToMaybe(taskId, sourceQuadrant);
    
    if (result.success) {
      res.json({ success: true, message: result.message, newTaskId: result.newTaskId });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Move task to maybe error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to copy a quadrant task to customer project
app.post('/api/tasks/copy-to-customer', async (req, res) => {
  try {
    const { taskId, sourceQuadrant, targetCustomer } = req.body;
    
    console.log('[API] Copy task to customer request:', { taskId, sourceQuadrant, targetCustomer });
    
    if (!taskId || !sourceQuadrant || !targetCustomer) {
      return res.status(400).json({ 
        error: 'Missing required fields: taskId, sourceQuadrant, targetCustomer' 
      });
    }
    
    const result = await copyTaskToCustomer(taskId, sourceQuadrant, targetCustomer);
    
    if (result.success) {
      res.json({ success: true, message: result.message, newProjectId: result.newProjectId });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Copy task to customer error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to move a quadrant task to delegation list
app.post('/api/tasks/move-to-delegation', async (req, res) => {
  try {
    const { taskId, sourceQuadrant } = req.body;
    
    console.log('[API] Move task to delegation request:', { taskId, sourceQuadrant });
    
    if (!taskId || !sourceQuadrant) {
      return res.status(400).json({ 
        error: 'Missing required fields: taskId, sourceQuadrant' 
      });
    }
    
    const result = await moveTaskToDelegation(taskId, sourceQuadrant);
    
    if (result.success) {
      res.json({ success: true, message: result.message, newTaskId: result.newTaskId });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Move task to delegation error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to copy a quadrant task to delegation list
app.post('/api/tasks/copy-to-delegation', async (req, res) => {
  try {
    const { taskId, sourceQuadrant } = req.body;
    
    console.log('[API] Copy task to delegation request:', { taskId, sourceQuadrant });
    
    if (!taskId || !sourceQuadrant) {
      return res.status(400).json({ 
        error: 'Missing required fields: taskId, sourceQuadrant' 
      });
    }
    
    const result = await copyTaskToDelegation(taskId, sourceQuadrant);
    
    if (result.success) {
      res.json({ success: true, message: result.message, newTaskId: result.newTaskId });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Copy task to delegation error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to reorder delegation tasks
app.post('/api/delegation/reorder', async (req, res) => {
  try {
    const { taskId, insertIndex } = req.body;
    
    console.log('[API] Reorder delegation task:', { taskId, insertIndex });
    
    if (!taskId) {
      return res.status(400).json({ error: 'Missing required field: taskId' });
    }
    
    const result = await reorderDelegationTask(taskId, insertIndex);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Reorder delegation error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to reorder maybe tasks
app.post('/api/maybe/reorder', async (req, res) => {
  try {
    const { taskId, insertIndex } = req.body;
    
    console.log('[API] Reorder maybe task:', { taskId, insertIndex });
    
    if (!taskId) {
      return res.status(400).json({ error: 'Missing required field: taskId' });
    }
    
    const result = await reorderMaybeTask(taskId, insertIndex);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Reorder maybe error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to complete a task
app.post('/api/tasks/complete', async (req, res) => {
  try {
    const { taskId, quadrant } = req.body;
    
    console.log('[API] Complete task:', { taskId, quadrant });
    
    if (!taskId || !quadrant) {
      return res.status(400).json({ error: 'Missing required fields: taskId, quadrant' });
    }
    
    const result = await completeTask(taskId, quadrant);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Complete task error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to complete a customer project
app.post('/api/customer-projects/complete', async (req, res) => {
  try {
    const { projectId, customerName } = req.body;
    
    console.log('[API] Complete customer project:', { projectId, customerName });
    
    if (!projectId || !customerName) {
      return res.status(400).json({ error: 'Missing required fields: projectId, customerName' });
    }
    
    const result = await completeCustomerProject(projectId, customerName);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Complete customer project error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to complete a delegation task
app.post('/api/delegation/complete', async (req, res) => {
  try {
    const { taskId } = req.body;
    
    console.log('[API] Complete delegation task:', { taskId });
    
    if (!taskId) {
      return res.status(400).json({ error: 'Missing required field: taskId' });
    }
    
    const result = await completeDelegationTask(taskId);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Complete delegation task error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to complete a maybe task
app.post('/api/maybe/complete', async (req, res) => {
  try {
    const { taskId } = req.body;
    
    console.log('[API] Complete maybe task:', { taskId });
    
    if (!taskId) {
      return res.status(400).json({ error: 'Missing required field: taskId' });
    }
    
    const result = await completeMaybeTask(taskId);
    
    if (result.success) {
      res.json({ success: true, message: result.message });
    } else {
      res.status(400).json({ success: false, error: result.error });
    }
  } catch (error) {
    console.error('[API] Complete maybe task error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Setup Terminal
let defaultShell = '/bin/bash';
if (os.platform() === 'win32') {
  defaultShell = 'powershell.exe';
} else {
  try {
    defaultShell = os.userInfo().shell || '/bin/bash';
  } catch (e) {
    defaultShell = '/bin/bash';
  }
}
const shell = process.env.SHELL || defaultShell;

// WebSocket connection handling
const clients = new Set();
const termClients = new Set();

app.ws('/ws', (ws, req) => {
  console.log('[WebSocket] Client connected');
  
  clients.add(ws);

  // Send initial data
  const initialData = loadAllTasks();
  ws.send(JSON.stringify({ type: 'init', data: initialData }));

  ws.on('close', () => {
    console.log('[WebSocket] Client disconnected');
    clients.delete(ws);
  });

  ws.on('error', (err) => {
    console.error('[WebSocket] Error:', err);
    clients.delete(ws);
  });
});

// Broadcast data to all connected clients
function broadcast(data) {
  const message = JSON.stringify({ type: 'update', data });
  clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

// Watch for file changes
// Tasks are located in workspace/tasks/ directory (4 levels up from dashboard)
const tasksDir = process.env.EISENHOWER_TASKS_DIR || path.join(__dirname, '../tasks');
const watchFiles = [
  path.join(tasksDir, 'tasks.md'),
  path.join(tasksDir, 'customer-projects.md'),
  path.join(tasksDir, 'delegation.md'),
  path.join(tasksDir, 'maybe.md')
];

console.log('[Watcher] Watching files:');
watchFiles.forEach(f => console.log(`  - ${f}`));

const watcher = chokidar.watch(watchFiles, {
  persistent: true,
  ignoreInitial: true,
  usePolling: false,
  interval: 1000
});

let debounceTimer = null;

watcher.on('change', (filePath) => {
  console.log(`[Watcher] File changed: ${path.basename(filePath)}`);

  // Debounce to avoid multiple rapid updates
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }

  debounceTimer = setTimeout(() => {
    console.log('[Watcher] Broadcasting update to clients');
    const data = loadAllTasks();
    broadcast(data);
  }, 500);
});

watcher.on('error', (error) => {
  console.error('[Watcher] Error:', error);
});

// Save port to config file for next time
const PORT_FILE = path.join(__dirname, 'port.conf');
fs.writeFileSync(PORT_FILE, port.toString());

// Start server
server.listen(port, () => {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║  Eisenhower Task Dashboard                                 ║
╠════════════════════════════════════════════════════════════╣
║  Server running at: http://localhost:${port}                   ║
║  API endpoint:      http://localhost:${port}/api/tasks         ║
║  WebSocket:         ws://localhost:${port}                     ║
╚════════════════════════════════════════════════════════════╝
  `);
});

// Handle server startup errors (e.g., port already in use)
server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`[Error] Port ${port} is already in use. Please use a different port with: ./start.sh --port <port>`);
  } else {
    console.error('[Error] Server error:', err);
  }
  process.exit(1);
});

// Global error handlers to prevent crashes
process.on('uncaughtException', (err) => {
  console.error('[Fatal] Uncaught Exception:', err);
  // Don't exit immediately, try to keep running
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('[Fatal] Unhandled Rejection at:', promise, 'reason:', reason);
  // Don't exit immediately, try to keep running
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n[Server] SIGINT received, shutting down gracefully...');
  watcher.close();
  wss.close();
  server.close(() => {
    console.log('[Server] Closed');
    process.exit(0);
  });
});

process.on('SIGTERM', () => {
  console.log('\n[Server] SIGTERM received, shutting down gracefully...');
  watcher.close();
  wss.close();
  server.close(() => {
    console.log('[Server] Closed');
    process.exit(0);
  });
});
