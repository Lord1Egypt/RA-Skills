// CLAW Agent 智控驾驶舱 - PM2 Configuration
// Replace __WORKSPACE__ with your actual workspace path
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.cwd();

module.exports = {
  apps: [
    {
      name: 'dashboard-frontend',
      script: 'python3',
      args: `-m http.server 8888 --bind 0.0.0.0 --directory ${WORKSPACE}`,
      cwd: WORKSPACE,
      autorestart: true,
      max_restarts: 50,
      restart_delay: 3000,
      watch: false,
    },
    {
      name: 'dashboard-api',
      script: `${WORKSPACE}/agent-api.js`,
      cwd: WORKSPACE,
      autorestart: true,
      max_restarts: 50,
      restart_delay: 3000,
      watch: false,
    },
    {
      name: 'dashboard-updater',
      script: `${WORKSPACE}/update-agent-data.js`,
      cwd: WORKSPACE,
      autorestart: true,
      max_restarts: 50,
      restart_delay: 3000,
      watch: false,
    }
  ]
};
