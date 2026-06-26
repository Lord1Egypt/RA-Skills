/**
 * EO Auto Workspace Manager v1.0.0
 * 
 * Automatic session-to-workspace binding system.
 * Solves the memory cross-contamination problem when using OpenClaw
 * across multiple sessions (e.g., multiple Feishu groups).
 * 
 * Key features:
 * - Detect new sessions automatically
 * - Create dedicated workspace per session/project
 * - Manage OpenClaw bindings dynamically
 * - Support session migration and cleanup
 */

import * as fs from 'fs'
import * as path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// ============================================================================
// Constants
// ============================================================================

const WORKSPACE_BASE = '.openclaw/workspace'
const AGENTS_DIR = '.openclaw/agents'
const OPENCLAW_CONFIG = '.openclaw/openclaw.json'

// ============================================================================
// Types
// ============================================================================

export interface SessionInfo {
  sessionId: string
  channel: 'feishu' | 'discord' | 'telegram' | 'web' | 'unknown'
  peerId?: string
  peerType?: 'group' | 'channel' | 'user'
  projectName?: string
  workspace?: string
  agentId?: string
  createdAt: number
  lastActiveAt: number
}

export interface WorkspaceBinding {
  sessionId: string
  workspace: string
  agentId: string
  channel: string
  peerId?: string
  boundAt: number
}

export interface AgentConfig {
  id: string
  name: string
  workspace: string
  channels?: string[]
}

export interface OpenClawConfig {
  agents?: {
    list?: AgentConfig[]
  }
  bindings?: BindingConfig[]
}

export interface BindingConfig {
  type: 'route'
  agentId: string
  match: {
    channel: string
    peer?: {
      kind: 'group' | 'channel' | 'user'
      id: string
    }
  }
}

// ============================================================================
// Auto Workspace Manager Class
// ============================================================================

export class AutoWorkspaceManager {
  private basePath: string
  private sessionRegistryPath: string
  private sessionRegistry: Map<string, SessionInfo> = new Map()
  private bindingRegistry: Map<string, WorkspaceBinding> = new Map()

  constructor(basePath?: string) {
    this.basePath = basePath || process.env.HOME || '/home/zzy'
    this.sessionRegistryPath = path.join(this.basePath, '.openclaw', 'session-registry.json')
    this.loadRegistry()
  }

  // ===========================================================================
  // Registry Management
  // ===========================================================================

  private loadRegistry(): void {
    try {
      if (fs.existsSync(this.sessionRegistryPath)) {
        const data = JSON.parse(fs.readFileSync(this.sessionRegistryPath, 'utf-8'))
        this.sessionRegistry = new Map(data.sessions || [])
        this.bindingRegistry = new Map(data.bindings || [])
      }
    } catch (e) {
      // Start fresh
    }
  }

  private saveRegistry(): void {
    const data = {
      sessions: Array.from(this.sessionRegistry.entries()),
      bindings: Array.from(this.bindingRegistry.entries()),
      updatedAt: new Date().toISOString(),
    }
    fs.mkdirSync(path.dirname(this.sessionRegistryPath), { recursive: true })
    fs.writeFileSync(this.sessionRegistryPath, JSON.stringify(data, null, 2), 'utf-8')
  }

  // ===========================================================================
  // Session Management
  // ===========================================================================

  /**
   * Register a new session or update existing one
   */
  registerSession(sessionId: string, info: Partial<SessionInfo>): SessionInfo {
    const existing = this.sessionRegistry.get(sessionId)
    
    const session: SessionInfo = {
      sessionId,
      channel: info.channel || existing?.channel || 'unknown',
      peerId: info.peerId || existing?.peerId,
      peerType: info.peerType || existing?.peerType,
      projectName: info.projectName || existing?.projectName,
      workspace: info.workspace || existing?.workspace,
      agentId: info.agentId || existing?.agentId,
      createdAt: existing?.createdAt || Date.now(),
      lastActiveAt: Date.now(),
    }

    this.sessionRegistry.set(sessionId, session)
    this.saveRegistry()
    
    return session
  }

  /**
   * Get session info
   */
  getSession(sessionId: string): SessionInfo | undefined {
    return this.sessionRegistry.get(sessionId)
  }

  /**
   * List all registered sessions
   */
  listSessions(): SessionInfo[] {
    return Array.from(this.sessionRegistry.values())
  }

  /**
   * Find sessions by criteria
   */
  findSessions(criteria: Partial<SessionInfo>): SessionInfo[] {
    return Array.from(this.sessionRegistry.values()).filter(s => {
      for (const [key, value] of Object.entries(criteria)) {
        if (s[key as keyof SessionInfo] !== value) return false
      }
      return true
    })
  }

  // ===========================================================================
  // Workspace Management
  // ===========================================================================

  /**
   * Create a new workspace for a session/project
   */
  createWorkspace(projectName: string, template?: string): WorkspaceInfo {
    const safeName = projectName.toLowerCase().replace(/[^a-z0-9]+/g, '-')
    const workspacePath = path.join(this.basePath, WORKSPACE_BASE, `workspace-${safeName}`)
    
    if (fs.existsSync(workspacePath)) {
      return {
        path: workspacePath,
        name: projectName,
        alreadyExisted: true,
      }
    }

    // Create directory structure
    fs.mkdirSync(workspacePath, { recursive: true })
    fs.mkdirSync(path.join(workspacePath, 'memory'), { recursive: true })
    fs.mkdirSync(path.join(workspacePath, 'topics'), { recursive: true })

    // Create essential files
    const memoryContent = `# MEMORY.md

This workspace is for project: ${projectName}
Created: ${new Date().toISOString()}
`
    fs.writeFileSync(path.join(workspacePath, 'MEMORY.md'), memoryContent, 'utf-8')

    const agentsContent = `# AGENTS.md

## Workspace: ${projectName}

This workspace is dedicated to the "${projectName}" project.
`
    fs.writeFileSync(path.join(workspacePath, 'AGENTS.md'), agentsContent, 'utf-8')

    const soulContent = `# SOUL.md

_Project: ${projectName} Workspace Agent_

## Identity

- **Role**: Project-specific AI assistant
- **Scope**: Limited to "${projectName}" project
- **Memory**: This workspace has its own memory system

## Guidelines

- Stay focused on ${projectName} project tasks
- Maintain clear separation from other projects
- Proactively update memory with project context
`
    fs.writeFileSync(path.join(workspacePath, 'SOUL.md'), soulContent, 'utf-8')

    return {
      path: workspacePath,
      name: projectName,
      alreadyExisted: false,
    }
  }

  /**
   * Get or create workspace for a project
   */
  getOrCreateWorkspace(projectName: string): WorkspaceInfo {
    const existing = this.findSessions({ projectName }).find(s => s.workspace)
    if (existing?.workspace) {
      return { path: existing.workspace, name: projectName, alreadyExisted: true }
    }
    return this.createWorkspace(projectName)
  }

  // ===========================================================================
  // Agent Management
  // ===========================================================================

  /**
   * Create an agent configuration
   */
  createAgent(projectName: string, workspace: string): AgentConfig {
    const safeName = projectName.toLowerCase().replace(/[^a-z0-9]+/g, '-')
    const agentId = `${safeName}-admin`
    
    const agent: AgentConfig = {
      id: agentId,
      name: `${projectName} 管理员`,
      workspace,
    }

    // Register in session registry
    this.bindingRegistry.set(agentId, {
      sessionId: '',
      workspace,
      agentId,
      channel: '',
      boundAt: Date.now(),
    })

    return agent
  }

  // ===========================================================================
  // OpenClaw Config Binding
  // ===========================================================================

  /**
   * Add a session binding to OpenClaw config
   */
  addSessionBinding(sessionId: string, agentId: string, channel: string, peerId?: string): boolean {
    const configPath = path.join(this.basePath, OPENCLAW_CONFIG)
    
    let config: OpenClawConfig = {}
    try {
      config = JSON.parse(fs.readFileSync(configPath, 'utf-8'))
    } catch {
      // Config doesn't exist or invalid
    }

    // Initialize arrays if needed
    if (!config.agents) config.agents = { list: [] }
    if (!config.agents.list) config.agents.list = []
    if (!config.bindings) config.bindings = []

    // Check if agent already exists
    const existingAgent = config.agents.list.find(a => a.id === agentId)
    
    // Create binding
    const binding: BindingConfig = {
      type: 'route',
      agentId,
      match: {
        channel,
      },
    }

    if (peerId) {
      binding.match.peer = {
        kind: this.inferPeerKind(peerId, channel),
        id: peerId,
      }
    }

    // Remove existing binding for this session if any
    config.bindings = config.bindings.filter(b => {
      if (b.type !== 'route') return true
      return b.match?.peer?.id !== peerId && b.agentId !== agentId
    })

    // Add new binding
    config.bindings.push(binding)

    // Write config
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8')

    return true
  }

  /**
   * Infer peer kind from peer ID pattern
   */
  private inferPeerKind(peerId: string, channel: string): 'group' | 'channel' | 'user' {
    if (channel === 'feishu') {
      if (peerId.startsWith('oc_')) return 'group'
      if (peerId.startsWith('ou_')) return 'user'
    }
    if (channel === 'discord') {
      if (peerId.startsWith('g_')) return 'group'
      if (peerId.startsWith('c_')) return 'channel'
    }
    return 'group'
  }

  // ===========================================================================
  // One-Click Session Setup
  // ===========================================================================

  /**
   * Complete one-click setup for a new session
   * This is the main entry point for the skill
   */
  async setupNewSession(params: {
    sessionId: string
    channel: string
    peerId?: string
    projectName?: string
    agentName?: string
  }): Promise<SessionSetupResult> {
    const { sessionId, channel, peerId, projectName, agentName } = params

    // 1. Determine project name if not provided
    const finalProjectName = projectName || this.extractProjectFromPeer(peerId, sessionId)

    // 2. Create or get workspace
    const workspaceInfo = this.getOrCreateWorkspace(finalProjectName)

    // 3. Create agent
    const agent = this.createAgent(finalProjectName, workspaceInfo.path)

    // 4. Register session
    this.registerSession(sessionId, {
      channel: channel as SessionInfo['channel'],
      peerId,
      projectName: finalProjectName,
      workspace: workspaceInfo.path,
      agentId: agent.id,
    })

    // 5. Add binding to OpenClaw config
    const bindingAdded = this.addSessionBinding(sessionId, agent.id, channel, peerId)

    // 6. Save registry
    this.saveRegistry()

    return {
      success: true,
      sessionId,
      projectName: finalProjectName,
      workspace: workspaceInfo.path,
      agentId: agent.id,
      bindingAdded,
      message: `Session ${sessionId} bound to workspace ${workspaceInfo.path}${bindingAdded ? '' : ' (binding pending restart)'}`,
    }
  }

  /**
   * Extract project name from peer ID
   */
  private extractProjectFromPeer(peerId?: string, sessionId?: string): string {
    if (peerId) {
      // Try to extract meaningful name from Feishu group ID
      if (peerId.startsWith('oc_')) {
        return `project-${peerId.slice(0, 8)}`
      }
    }
    if (sessionId) {
      return `session-${sessionId.slice(0, 8)}`
    }
    return `workspace-${Date.now()}`
  }

  // ===========================================================================
  // Gateway Management
  // ===========================================================================

  /**
   * Check if gateway restart is needed
   */
  needsGatewayRestart(): boolean {
    // For now, always return true after config change
    // In future, could track if config has changed since last restart
    return true
  }

  /**
   * Get command to restart gateway
   */
  getRestartCommand(): string {
    return 'openclaw gateway restart'
  }

  /**
   * Generate status report
   */
  generateStatusReport(): StatusReport {
    const sessions = this.listSessions()
    const workspaces = new Set(sessions.map(s => s.workspace).filter(Boolean))
    
    return {
      totalSessions: sessions.length,
      totalWorkspaces: workspaces.size,
      activeSessions: sessions.filter(s => Date.now() - s.lastActiveAt < 3600000).length,
      recentBindings: Array.from(this.bindingRegistry.values())
        .sort((a, b) => b.boundAt - a.boundAt)
        .slice(0, 5),
    }
  }
}

// ============================================================================
// Types
// ============================================================================

export interface WorkspaceInfo {
  path: string
  name: string
  alreadyExisted: boolean
}

export interface SessionSetupResult {
  success: boolean
  sessionId: string
  projectName: string
  workspace: string
  agentId: string
  bindingAdded: boolean
  message: string
}

export interface StatusReport {
  totalSessions: number
  totalWorkspaces: number
  activeSessions: number
  recentBindings: WorkspaceBinding[]
}

// ============================================================================
// Export singleton factory
// ============================================================================

let managerInstance: AutoWorkspaceManager | null = null

export function createWorkspaceManager(basePath?: string): AutoWorkspaceManager {
  if (!managerInstance) {
    managerInstance = new AutoWorkspaceManager(basePath)
  }
  return managerInstance
}
