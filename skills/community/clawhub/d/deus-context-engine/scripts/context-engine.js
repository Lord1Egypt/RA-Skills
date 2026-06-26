#!/usr/bin/env node
/**
 * Context Engine - Core implementation
 * Handles project state management across OpenClaw sessions
 */

const fs = require('fs');
const path = require('path');

const PROJECTS_DIR = '/home/deus/.openclaw/workspace/memory/projects';
const PROJECTS_FILE = path.join(PROJECTS_DIR, 'projects.json');
const SESSION_FILE = path.join(PROJECTS_DIR, 'session.json');

// Ensure directory exists
function ensureDir() {
  if (!fs.existsSync(PROJECTS_DIR)) {
    fs.mkdirSync(PROJECTS_DIR, { recursive: true });
  }
}

// Get current ISO timestamp
function now() {
  return new Date().toISOString();
}

// Initialize or load projects
function loadProjects() {
  ensureDir();
  if (!fs.existsSync(PROJECTS_FILE)) {
    const initial = { projects: {}, activeProjectId: null, lastUpdated: now() };
    fs.writeFileSync(PROJECTS_FILE, JSON.stringify(initial, null, 2));
    return initial;
  }
  try {
    return JSON.parse(fs.readFileSync(PROJECTS_FILE, 'utf-8'));
  } catch (e) {
    // Backup corrupted file
    const bak = PROJECTS_FILE + '.bak';
    fs.copyFileSync(PROJECTS_FILE, bak);
    const initial = { projects: {}, activeProjectId: null, lastUpdated: now() };
    fs.writeFileSync(PROJECTS_FILE, JSON.stringify(initial, null, 2));
    return initial;
  }
}

// Save projects
function saveProjects(data) {
  data.lastUpdated = now();
  fs.writeFileSync(PROJECTS_FILE, JSON.stringify(data, null, 2));
}

// Load or init session
function loadSession() {
  ensureDir();
  if (!fs.existsSync(SESSION_FILE)) {
    const initial = {
      currentProjectId: null,
      sessionStart: now(),
      contextStack: [],
      heartbeatLast: null
    };
    fs.writeFileSync(SESSION_FILE, JSON.stringify(initial, null, 2));
    return initial;
  }
  try {
    return JSON.parse(fs.readFileSync(SESSION_FILE, 'utf-8'));
  } catch (e) {
    const initial = {
      currentProjectId: null,
      sessionStart: now(),
      contextStack: [],
      heartbeatLast: null
    };
    fs.writeFileSync(SESSION_FILE, JSON.stringify(initial, null, 2));
    return initial;
  }
}

// Save session
function saveSession(data) {
  fs.writeFileSync(SESSION_FILE, JSON.stringify(data, null, 2));
}

// Create a new project
function createProject(name, description = '') {
  const data = loadProjects();
  const id = name.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-');
  
  if (data.projects[id]) {
    return { success: false, message: `Project "${name}" already exists`, project: data.projects[id] };
  }
  
  const project = {
    id,
    name,
    description,
    status: 'active',
    createdAt: now(),
    updatedAt: now(),
    lastSessionAt: now(),
    sessionCount: 1,
    context: {
      lastTopic: '',
      lastFile: '',
      lastCommand: '',
      pendingTasks: [],
      notes: ''
    },
    metadata: {
      tags: [],
      custom: {}
    }
  };
  
  data.projects[id] = project;
  data.activeProjectId = id;
  saveProjects(data);
  
  return { success: true, message: `Created project "${name}"`, project };
}

// Get active project
function getActiveProject() {
  const data = loadProjects();
  if (!data.activeProjectId) return null;
  return data.projects[data.activeProjectId] || null;
}

// Get project by ID
function getProject(id) {
  const data = loadProjects();
  return data.projects[id] || null;
}

// List all projects
function listProjects() {
  const data = loadProjects();
  const projects = Object.values(data.projects);
  const activeId = data.activeProjectId;
  
  const list = projects.map(p => ({
    ...p,
    isActive: p.id === activeId
  })).sort((a, b) => {
    // Active first, then by lastSessionAt
    if (a.isActive) return -1;
    if (b.isActive) return 1;
    return new Date(b.lastSessionAt) - new Date(a.lastSessionAt);
  });
  
  return { projects: list, activeProjectId: activeId };
}

// Set active project
function setActiveProject(id) {
  const data = loadProjects();
  if (!data.projects[id]) {
    return { success: false, message: `Project "${id}" not found` };
  }
  data.activeProjectId = id;
  saveProjects(data);
  return { success: true, message: `Switched to project "${data.projects[id].name}"`, project: data.projects[id] };
}

// Save context for active project
function saveContext(contextData = {}) {
  const data = loadProjects();
  const session = loadSession();
  
  if (!data.activeProjectId) {
    return { success: false, message: 'No active project to save context to' };
  }
  
  const project = data.projects[data.activeProjectId];
  
  // Update context
  if (contextData.lastTopic) project.context.lastTopic = contextData.lastTopic;
  if (contextData.lastFile) project.context.lastFile = contextData.lastFile;
  if (contextData.lastCommand) project.context.lastCommand = contextData.lastCommand;
  if (contextData.pendingTasks) project.context.pendingTasks = contextData.pendingTasks;
  if (contextData.notes) project.context.notes = contextData.notes;
  
  project.updatedAt = now();
  project.lastSessionAt = now();
  
  // Add to context stack
  session.contextStack.push({
    type: 'context_save',
    ref: 'manual',
    timestamp: now(),
    summary: contextData.lastTopic || 'Context saved'
  });
  
  saveProjects(data);
  saveSession(session);
  
  return { success: true, message: `Context saved for "${project.name}"`, project };
}

// Restore context - called on session start
function restoreContext() {
  const data = loadProjects();
  const session = loadSession();
  
  if (!data.activeProjectId) {
    return { 
      success: true, 
      message: 'No active project to restore',
      hasProject: false,
      project: null 
    };
  }
  
  const project = data.projects[data.activeProjectId];
  
  // Update session
  session.currentProjectId = data.activeProjectId;
  session.sessionStart = now();
  saveSession(session);
  
  // Increment session count
  project.sessionCount = (project.sessionCount || 0) + 1;
  project.lastSessionAt = now();
  saveProjects(data);
  
  return { 
    success: true, 
    message: `Welcome back to ${project.name}`,
    hasProject: true,
    project,
    pendingTasks: project.context.pendingTasks || []
  };
}

// Switch project
function switchProject(projectName) {
  const data = loadProjects();
  
  // First save current context
  if (data.activeProjectId && data.projects[data.activeProjectId]) {
    data.projects[data.activeProjectId].lastSessionAt = now();
  }
  
  // Try to find existing project (by name or id)
  const searchId = projectName.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-');
  let targetId = searchId;
  let project = data.projects[searchId];
  
  // If not found by ID, search by name
  if (!project) {
    const found = Object.values(data.projects).find(p => 
      p.name.toLowerCase() === projectName.toLowerCase()
    );
    if (found) {
      targetId = found.id;
      project = found;
    }
  }
  
  // Create if doesn't exist
  if (!project) {
    const result = createProject(projectName);
    return result;
  }
  
  // Switch to existing
  data.activeProjectId = targetId;
  project.lastSessionAt = now();
  project.sessionCount = (project.sessionCount || 0) + 1;
  saveProjects(data);
  
  return { success: true, message: `Switched to "${project.name}"`, project };
}

// Summarize active project
function summarize() {
  const project = getActiveProject();
  
  if (!project) {
    return { 
      success: true, 
      message: 'No active project',
      summary: 'No active project. Create one with "switch to [name]".'
    };
  }
  
  const summary = {
    name: project.name,
    status: project.status,
    sessions: project.sessionCount,
    lastSeen: project.lastSessionAt,
    lastTopic: project.context.lastTopic || 'None',
    lastFile: project.context.lastFile || 'None',
    pendingTasks: project.context.pendingTasks || [],
    notes: project.context.notes || ''
  };
  
  return { success: true, project: summary };
}

// Add pending task
function addPendingTask(task) {
  const data = loadProjects();
  if (!data.activeProjectId) {
    return { success: false, message: 'No active project' };
  }
  
  const project = data.projects[data.activeProjectId];
  project.context.pendingTasks = project.context.pendingTasks || [];
  project.context.pendingTasks.push(task);
  project.updatedAt = now();
  saveProjects(data);
  
  return { success: true, message: `Added task: ${task}` };
}

// Remove pending task
function removePendingTask(taskIndex) {
  const data = loadProjects();
  if (!data.activeProjectId) {
    return { success: false, message: 'No active project' };
  }
  
  const project = data.projects[data.activeProjectId];
  const tasks = project.context.pendingTasks || [];
  
  if (taskIndex < 0 || taskIndex >= tasks.length) {
    return { success: false, message: 'Invalid task index' };
  }
  
  const removed = tasks.splice(taskIndex, 1);
  project.context.pendingTasks = tasks;
  project.updatedAt = now();
  saveProjects(data);
  
  return { success: true, message: `Removed task: ${removed[0]}` };
}

// Update project status
function setProjectStatus(status) {
  const data = loadProjects();
  if (!data.activeProjectId) {
    return { success: false, message: 'No active project' };
  }
  
  const project = data.projects[data.activeProjectId];
  project.status = status;
  project.updatedAt = now();
  saveProjects(data);
  
  return { success: true, message: `Project status set to "${status}"` };
}

// Heartbeat - periodic save
function heartbeat() {
  const session = loadSession();
  session.heartbeatLast = now();
  saveSession(session);
  
  // Also save context if there's an active project
  const project = getActiveProject();
  if (project) {
    project.lastSessionAt = now();
    const data = loadProjects();
    data.projects[project.id] = project;
    saveProjects(data);
  }
  
  return { success: true, message: 'Heartbeat recorded', timestamp: now() };
}

// Parse CLI args and run command
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  let result;
  
  switch (command) {
    case 'create':
      result = createProject(args[1], args[2] || '');
      break;
    case 'list':
      result = listProjects();
      break;
    case 'get-active':
      result = getActiveProject();
      break;
    case 'get':
      result = getProject(args[1]);
      break;
    case 'switch':
      result = switchProject(args[1]);
      break;
    case 'save':
      const contextData = args[1] ? JSON.parse(args[1]) : {};
      result = saveContext(contextData);
      break;
    case 'restore':
      result = restoreContext();
      break;
    case 'summarize':
      result = summarize();
      break;
    case 'add-task':
      result = addPendingTask(args.slice(1).join(' '));
      break;
    case 'remove-task':
      result = removePendingTask(parseInt(args[1], 10));
      break;
    case 'set-status':
      result = setProjectStatus(args[1]);
      break;
    case 'heartbeat':
      result = heartbeat();
      break;
    default:
      result = { 
        success: false, 
        message: `Unknown command: ${command}`,
        usage: 'create|list|get-active|get|switch|save|restore|summarize|add-task|remove-task|set-status|heartbeat'
      };
  }
  
  console.log(JSON.stringify(result, null, 2));
}

main();
