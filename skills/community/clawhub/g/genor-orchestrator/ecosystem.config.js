// PM2 ecosystem config for the orchestration dashboard
// All paths derived from WORKSPACE root. Override with env vars.
const WORKSPACE = process.env.WORKSPACE || require('os').homedir() + '/.openclaw/workspace';
const SKILL = WORKSPACE + '/skills/genor-orchestrator';

module.exports = {
  apps: [{
    name: 'orchestration-dashboard',
    cwd: SKILL + '/dashboard',
    script: 'server.py',
    interpreter: 'python3',
    env: {
      ORCHESTRATOR_DATA_DIR: process.env.ORCHESTRATOR_DATA_DIR || WORKSPACE + '/orchestrator-data',
      DASHBOARD_PORT: process.env.DASHBOARD_PORT || '8766'
    },
    max_memory_restart: '512M',
    watch: false,
    log_file: SKILL + '/logs/dashboard.log',
    error_file: SKILL + '/logs/dashboard-error.log',
    out_file: SKILL + '/logs/dashboard-out.log'
  }]
};
