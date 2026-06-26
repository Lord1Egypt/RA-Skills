const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const os = require('os');
const chalk = require('chalk');

class OpenClawConfigManager {
  constructor() {
    this.configPath = this.getConfigPath();
    this.backupPath = `${this.configPath}.backup`;
  }

  getDefaultConfigCandidates() {
    return [
      path.join(os.homedir(), '.openclaw', 'openclaw.json'),
      path.join(os.homedir(), '.openclaw', 'config.json'),
    ];
  }

  getConfigPath() {
    const envPath = process.env.OPENCLAW_CONFIG_PATH;
    if (envPath) {
      return envPath.replace('~', os.homedir());
    }

    const candidates = this.getDefaultConfigCandidates();
    const detected = candidates.find((candidate) => fs.existsSync(candidate));
    return detected || candidates[0];
  }

  getManagedFragmentPath() {
    const envPath = process.env.EKYBOT_MANAGED_FRAGMENT_PATH;
    if (envPath) {
      return envPath.replace('~', os.homedir());
    }

    return path.join(os.homedir(), '.openclaw', 'managed', 'ekybot.agents.json5');
  }

  resolveHomePath(filePath) {
    return filePath.replace(/^~(?=$|\/|\\)/, os.homedir());
  }

  // Read current OpenClaw configuration
  readConfig() {
    try {
      if (!fs.existsSync(this.configPath)) {
        throw new Error(`OpenClaw config not found at ${this.configPath}`);
      }

      const configData = fs.readFileSync(this.configPath, 'utf8');
      return JSON.parse(configData);
    } catch (error) {
      console.error(chalk.red(`Failed to read OpenClaw config: ${error.message}`));
      throw error;
    }
  }

  // Write updated configuration (atomic: write temp file then rename)
  writeConfig(config) {
    try {
      // Create backup before modifying
      this.createBackup();

      const configData = JSON.stringify(config, null, 2);
      const tmpPath = `${this.configPath}.tmp.${process.pid}`;
      fs.writeFileSync(tmpPath, configData, 'utf8');
      fs.renameSync(tmpPath, this.configPath); // Atomic on same filesystem

      console.log(chalk.green(`✓ Updated OpenClaw config at ${this.configPath}`));
    } catch (error) {
      console.error(chalk.red(`Failed to write OpenClaw config: ${error.message}`));
      throw error;
    }
  }

  writeFileAtomic(targetPath, content) {
    const resolvedPath = this.resolveHomePath(targetPath);
    fs.mkdirSync(path.dirname(resolvedPath), { recursive: true });
    const tmpPath = `${resolvedPath}.tmp.${process.pid}`;
    fs.writeFileSync(tmpPath, content, 'utf8');
    fs.renameSync(tmpPath, resolvedPath);
    return resolvedPath;
  }

  // Create backup of current configuration
  createBackup() {
    try {
      if (fs.existsSync(this.configPath)) {
        fs.copyFileSync(this.configPath, this.backupPath);
        console.log(chalk.yellow(`Created config backup at ${this.backupPath}`));
      }
    } catch (error) {
      console.warn(chalk.yellow(`Warning: Could not create config backup: ${error.message}`));
    }
  }

  // Restore from backup
  restoreBackup() {
    try {
      if (fs.existsSync(this.backupPath)) {
        fs.copyFileSync(this.backupPath, this.configPath);
        console.log(chalk.green(`✓ Restored config from backup`));
        return true;
      } else {
        console.warn(chalk.yellow('No backup file found to restore'));
        return false;
      }
    } catch (error) {
      console.error(chalk.red(`Failed to restore backup: ${error.message}`));
      return false;
    }
  }

  getIncludePaths() {
    try {
      const config = this.readConfig();
      const includes = [];

      if (Array.isArray(config.$include)) {
        includes.push(...config.$include);
      }

      if (Array.isArray(config.include)) {
        includes.push(...config.include);
      }

      if (typeof config.$include === 'string') {
        includes.push(config.$include);
      }

      if (typeof config.include === 'string') {
        includes.push(config.include);
      }

      return includes;
    } catch (error) {
      return [];
    }
  }

  getManagedIncludePath(managedFragmentPath = this.getManagedFragmentPath()) {
    const resolvedFragmentPath = this.resolveHomePath(managedFragmentPath);
    const configDir = path.dirname(this.configPath);
    const relativePath = path.relative(configDir, resolvedFragmentPath);

    if (relativePath && !relativePath.startsWith('..') && !path.isAbsolute(relativePath)) {
      return relativePath.split(path.sep).join('/');
    }

    return resolvedFragmentPath;
  }

  ensureManagedInclude(managedFragmentPath = this.getManagedFragmentPath()) {
    const config = this.readConfig();
    const includePath = this.getManagedIncludePath(managedFragmentPath);
    const managedBasename = path.basename(this.resolveHomePath(managedFragmentPath));
    const currentIncludes = this.getIncludePaths();

    const nextIncludes = [...currentIncludes.filter((candidate) => {
      const normalized = this.resolveHomePath(candidate);
      return path.basename(normalized) !== managedBasename;
    }), includePath];

    const updated = JSON.stringify(nextIncludes) !== JSON.stringify(currentIncludes);

    if (!updated) {
      return { updated: false, includePath, configPath: this.configPath };
    }

    config.$include = nextIncludes;

    if ('include' in config) {
      delete config.include;
    }

    this.writeConfig(config);
    return { updated: true, includePath, configPath: this.configPath };
  }

  _getRootConfigAgentsList(config) {
    if (Array.isArray(config?.agents)) {
      return { agentsList: config.agents, isDirectArray: true };
    }

    if (Array.isArray(config?.agents?.list)) {
      return { agentsList: config.agents.list, isDirectArray: false };
    }

    return { agentsList: [], isDirectArray: false };
  }

  _getAgentExtrasFromRootConfig(openclawAgentId) {
    try {
      const config = this.readConfig();
      const { agentsList } = this._getRootConfigAgentsList(config);
      const match = agentsList.find((agent) => {
        const candidateId = agent?.id || agent?.key || null;
        return candidateId === openclawAgentId;
      });

      if (!match || typeof match !== 'object') {
        return {};
      }

      const {
        id,
        key,
        name,
        model,
        workspace,
        workspacePath,
        ...extras
      } = match;

      return extras;
    } catch (_error) {
      return {};
    }
  }

  _removeManagedAgentsFromRootConfig(managedAgentIds) {
    if (!managedAgentIds || managedAgentIds.size === 0) {
      return { updated: false, removedCount: 0 };
    }

    try {
      const config = this.readConfig();
      const { agentsList, isDirectArray } = this._getRootConfigAgentsList(config);

      if (!Array.isArray(agentsList) || agentsList.length === 0) {
        return { updated: false, removedCount: 0 };
      }

      const before = agentsList.length;
      const filtered = agentsList.filter((agent) => {
        const agentId = agent?.id || agent?.key || null;
        return !managedAgentIds.has(agentId);
      });

      const removedCount = before - filtered.length;
      if (removedCount === 0) {
        return { updated: false, removedCount: 0 };
      }

      if (isDirectArray) {
        config.agents = filtered;
      } else if (config?.agents && typeof config.agents === 'object') {
        config.agents.list = filtered;
      }

      this.writeConfig(config);

      console.log(
        chalk.yellow(
          `⚠ Removed ${removedCount} managed agent(s) from openclaw.json (now in managed fragment only)`
        )
      );

      return { updated: true, removedCount };
    } catch (error) {
      console.warn(
        chalk.yellow(`Warning: failed to clean managed agents from root config: ${error.message}`)
      );
      return { updated: false, removedCount: 0 };
    }
  }

  writeManagedFragment(desiredState) {
    const fragmentPath = this.resolveHomePath(
      desiredState.managedFragmentPath || this.getManagedFragmentPath()
    );

    const managedAgentIds = new Set(
      (desiredState.agents || [])
        .map((agent) => agent?.openclawAgentId)
        .filter((agentId) => typeof agentId === 'string' && agentId.trim().length > 0)
    );

    const fragment = {
      agents: {
        list: (desiredState.agents || []).map((agent) => {
          const baseEntry = {
            id: agent.openclawAgentId,
            name: agent.name,
            model: agent.model,
            workspace: agent.workspacePath || null,
          };
          const rootExtras = this._getAgentExtrasFromRootConfig(agent.openclawAgentId);
          return { ...rootExtras, ...baseEntry };
        }),
      },
    };

    const content = `${JSON.stringify(fragment, null, 2)}\n`;
    this.writeFileAtomic(fragmentPath, content);
    this._removeManagedAgentsFromRootConfig(managedAgentIds);

    return {
      fragmentPath,
      fragmentHash: crypto.createHash('sha256').update(content).digest('hex'),
    };
  }

  removeAgentFromManagedFragment({ openclawAgentId, workspacePath, name } = {}) {
    const fragmentPath = this.resolveHomePath(this.getManagedFragmentPath());

    if (!fs.existsSync(fragmentPath)) {
      return { updated: false, fragmentPath, reason: 'fragment_missing' };
    }

    try {
      const raw = fs.readFileSync(fragmentPath, 'utf8');
      const parsed = JSON.parse(raw);
      const sourceAgents = Array.isArray(parsed?.agents)
        ? parsed.agents
        : Array.isArray(parsed?.agents?.list)
          ? parsed.agents.list
          : [];

      const matchesAgent = (agent) => {
        const candidateId = agent?.id || agent?.key || agent?.name || null;
        const candidateWorkspace = agent?.workspace || agent?.workspacePath || agent?.path || null;

        if (openclawAgentId && candidateId === openclawAgentId) {
          return true;
        }

        if (workspacePath && candidateWorkspace) {
          return this.resolveHomePath(String(candidateWorkspace)) === this.resolveHomePath(workspacePath);
        }

        if (name && agent?.name === name) {
          return true;
        }

        return false;
      };

      const nextAgents = sourceAgents.filter((agent) => !matchesAgent(agent));
      if (nextAgents.length === sourceAgents.length) {
        return { updated: false, fragmentPath, reason: 'agent_not_found' };
      }

      const nextFragment = Array.isArray(parsed?.agents)
        ? { ...parsed, agents: nextAgents }
        : {
            ...parsed,
            agents: {
              ...(parsed?.agents && typeof parsed.agents === 'object' ? parsed.agents : {}),
              list: nextAgents,
            },
          };

      const content = `${JSON.stringify(nextFragment, null, 2)}\n`;
      this.writeFileAtomic(fragmentPath, content);

      return {
        updated: true,
        fragmentPath,
        fragmentHash: crypto.createHash('sha256').update(content).digest('hex'),
      };
    } catch (error) {
      console.warn(chalk.yellow(`Warning: failed to remove agent from managed fragment at ${fragmentPath}: ${error.message}`));
      return { updated: false, fragmentPath, reason: 'parse_failed' };
    }
  }

  removeAgentFromConfig({ openclawAgentId, workspacePath, name } = {}) {
    const config = this.readConfig();
    let updated = false;

    const matchesAgent = (agent) => {
      const candidateId = agent?.id || agent?.key || agent?.name || null;
      const candidateWorkspace = agent?.workspace || agent?.workspacePath || agent?.path || null;

      if (openclawAgentId && candidateId === openclawAgentId) {
        return true;
      }

      if (workspacePath && candidateWorkspace) {
        return this.resolveHomePath(String(candidateWorkspace)) === this.resolveHomePath(workspacePath);
      }

      if (name && agent?.name === name) {
        return true;
      }

      return false;
    };

    if (Array.isArray(config.agents)) {
      const nextAgents = config.agents.filter((agent) => !matchesAgent(agent));
      if (nextAgents.length !== config.agents.length) {
        config.agents = nextAgents;
        updated = true;
      }
    } else if (Array.isArray(config?.agents?.list)) {
      const nextAgents = config.agents.list.filter((agent) => !matchesAgent(agent));
      if (nextAgents.length !== config.agents.list.length) {
        config.agents.list = nextAgents;
        updated = true;
      }
    }

    if (updated) {
      this.writeConfig(config);
    }

    return { updated, configPath: this.configPath };
  }

  deleteWorkspace(workspacePath) {
    if (!workspacePath) {
      return { deleted: false, reason: 'missing_workspace_path' };
    }

    const resolvedPath = this.resolveHomePath(workspacePath);
    if (!fs.existsSync(resolvedPath)) {
      return { deleted: false, reason: 'workspace_missing', workspacePath: resolvedPath };
    }

    const normalizedPath = resolvedPath.replace(/\\/g, '/');
    const looksLikeOpenClawWorkspace =
      normalizedPath.includes('/.openclaw/') ||
      normalizedPath.includes('/openclaw/') ||
      path.basename(resolvedPath).startsWith('workspace-');

    if (!looksLikeOpenClawWorkspace) {
      return { deleted: false, reason: 'workspace_path_not_safe', workspacePath: resolvedPath };
    }

    fs.rmSync(resolvedPath, { recursive: true, force: true });
    return { deleted: true, workspacePath: resolvedPath };
  }

  readManagedFragmentAgents() {
    const fragmentPath = this.getManagedFragmentPath();

    if (!fs.existsSync(fragmentPath)) {
      return [];
    }

    try {
      const raw = fs.readFileSync(fragmentPath, 'utf8');
      const parsed = JSON.parse(raw);
      const sourceAgents = Array.isArray(parsed?.agents)
        ? parsed.agents
        : Array.isArray(parsed?.agents?.list)
          ? parsed.agents.list
          : [];

      return sourceAgents.map((agent, index) => this.normalizeAgentRecord(agent, index));
    } catch (error) {
      console.warn(chalk.yellow(`Warning: failed to parse managed fragment at ${fragmentPath}: ${error.message}`));
      return [];
    }
  }

  normalizeAgentRecord(agent, index) {
    return {
      externalId: agent.id || agent.key || agent.name || `agent-${index + 1}`,
      name: agent.name || agent.id || agent.key || `Agent ${index + 1}`,
      ownership: this.inferAgentOwnership(agent),
      model: agent.model || agent.engine || agent.provider_model || null,
      workspacePath: agent.workspace || agent.workspacePath || agent.path || null,
      channelKey: agent.channelKey || agent.channel || null,
      projectKey: agent.projectKey || agent.project || agent.projectId || null,
      metadata: {
        provider: agent.provider || null,
        tools: Array.isArray(agent.tools) ? agent.tools : [],
        rawId: agent.id || null,
        bindings: Array.isArray(agent.bindings) ? agent.bindings : [],
      },
    };
  }

  listAgents() {
    try {
      const config = this.readConfig();
      const sourceAgents = Array.isArray(config?.agents)
        ? config.agents
        : Array.isArray(config?.agents?.list)
          ? config.agents.list
          : [];
      const normalizedBaseAgents = sourceAgents.map((agent, index) =>
        this.normalizeAgentRecord(agent, index)
      );
      const managedFragmentAgents = this.readManagedFragmentAgents();
      const mergedById = new Map();

      for (const agent of normalizedBaseAgents) {
        mergedById.set(agent.externalId, agent);
      }

      for (const agent of managedFragmentAgents) {
        mergedById.set(agent.externalId, {
          ...(mergedById.get(agent.externalId) || {}),
          ...agent,
          ownership: 'managed',
        });
      }

      return Array.from(mergedById.values());
    } catch (error) {
      return [];
    }
  }

  inferAgentOwnership(agent) {
    const managedFragmentPath = this.getManagedFragmentPath();
    const includesManagedFragment = this.getIncludePaths().some((includePath) =>
      includePath.includes(path.basename(managedFragmentPath))
    );

    if (agent?.metadata?.ekybotManaged || agent?.ekybotManaged) {
      return 'managed';
    }

    if (includesManagedFragment && agent?.workspace && String(agent.workspace).includes('ekybot')) {
      return 'adoptable';
    }

    return 'external';
  }

  // Add Ekybot integration to OpenClaw config
  addEkybotIntegration(workspaceId) {
    try {
      const config = this.readConfig();

      // Initialize integrations if not exists
      if (!config.integrations) {
        config.integrations = {};
      }

      // Add Ekybot configuration (NO API KEY stored here!)
      config.integrations.ekybot = {
        enabled: true,
        workspace_id: workspaceId,
        telemetry_enabled: false, // Disabled by default - requires opt-in
        telemetry_interval: 60000,
        endpoints: {
          api: process.env.EKYBOT_API_URL || 'https://api.ekybot.com',
          websocket: process.env.EKYBOT_WS_URL || 'wss://api.ekybot.com/ws',
        },
        added_at: new Date().toISOString(),
        version: '1.0.0',
      };

      this.writeConfig(config);
      return true;
    } catch (error) {
      console.error(chalk.red(`Failed to add Ekybot integration: ${error.message}`));
      return false;
    }
  }

  // Remove Ekybot integration from OpenClaw config
  removeEkybotIntegration() {
    try {
      const config = this.readConfig();

      if (config.integrations && config.integrations.ekybot) {
        delete config.integrations.ekybot;

        // Remove integrations object if empty
        if (Object.keys(config.integrations).length === 0) {
          delete config.integrations;
        }

        this.writeConfig(config);
        console.log(chalk.green('✓ Removed Ekybot integration from OpenClaw config'));
        return true;
      } else {
        console.log(chalk.yellow('No Ekybot integration found in config'));
        return false;
      }
    } catch (error) {
      console.error(chalk.red(`Failed to remove Ekybot integration: ${error.message}`));
      return false;
    }
  }

  // Check if Ekybot integration is configured
  isEkybotConfigured() {
    try {
      const config = this.readConfig();
      return !!(
        config.integrations &&
        config.integrations.ekybot &&
        config.integrations.ekybot.enabled
      );
    } catch (error) {
      return false;
    }
  }

  // Get current Ekybot configuration (with API key from environment)
  getEkybotConfig() {
    try {
      const config = this.readConfig();
      const ekybotConfig = config.integrations?.ekybot || null;

      if (ekybotConfig) {
        // Add API key from environment (not stored in config)
        ekybotConfig.api_key = process.env.EKYBOT_API_KEY || null;
      }

      return ekybotConfig;
    } catch (error) {
      return null;
    }
  }

  // Validate OpenClaw installation
  validateOpenClawInstallation() {
    const checks = {
      configExists: fs.existsSync(this.configPath),
      configValid: false,
      agentsDir: false,
      managedFragmentExists: fs.existsSync(this.getManagedFragmentPath()),
    };

    // Check config validity
    if (checks.configExists) {
      try {
        const config = this.readConfig();
        checks.configValid = typeof config === 'object' && config !== null;
      } catch (error) {
        checks.configValid = false;
      }
    }

    // Check agents directory
    const agentsPath =
      process.env.OPENCLAW_AGENTS_PATH || path.join(os.homedir(), '.openclaw', 'agents');
    checks.agentsDir = fs.existsSync(agentsPath);

    return checks;
  }
}

module.exports = OpenClawConfigManager;
