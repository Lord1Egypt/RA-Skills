/**
 * PM2 ecosystem config for Roundtable Web Viewer.
 *
 * Usage:
 *   pm2 start ecosystem.config.cjs -- --port 8199 --discussion-dir /path/to/discussion
 *
 * This is a template — WebPublisher.py generates per-discussion pm2 commands directly.
 */
module.exports = {
  apps: [
    {
      name: "roundtable-web",
      script: "./server.mjs",
      interpreter: "node",
      instances: 1,
      autorestart: true,
      max_restarts: 5,
      restart_delay: 2000,
      watch: false,
      max_memory_restart: "256M",
      env: {
        NODE_ENV: "production",
      },
    },
  ],
};
