import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

const { autoPull, autoPush } = require('@any-sync/cli') as {
  autoPull: (lockfilePath?: string) => { pulled: string[] } | null;
  autoPush: (lockfilePath?: string) => { pushed: string[] } | null;
};

/**
 * OpenClaw plugin entry point for Any Sync.
 *
 * Registers session lifecycle hooks for auto-pull on session start
 * and auto-push on session end. Skills are loaded from the skills/
 * directory as declared in openclaw.plugin.json.
 */
const plugin = {
  id: 'any-sync',
  name: 'Any Sync',
  description: 'Cross-device sync for OpenClaw workspace (skills, memory, settings) via GitHub',
  register(api: {
    registerHook: (name: string, hook: Record<string, unknown>) => void;
    pluginConfig: Record<string, unknown>;
    logger: { info: (msg: string) => void; error: (msg: string) => void };
  }) {
    const autoSync = api.pluginConfig?.autoSync !== false;

    if (autoSync) {
      api.registerHook('session_start', {
        handler: async () => {
          try {
            const result = autoPull();
            const count = result?.pulled?.length ?? 0;
            if (count > 0) {
              api.logger.info(`Any Sync: auto-pulled ${count} file(s) from GitHub`);
            }
          } catch {
            // Silent failure
          }
        },
      });

      api.registerHook('session_end', {
        handler: async () => {
          try {
            const result = autoPush();
            const count = result?.pushed?.length ?? 0;
            if (count > 0) {
              api.logger.info(`Any Sync: auto-pushed ${count} file(s) to GitHub`);
            }
          } catch {
            // Silent failure
          }
        },
      });
    }
  },
};

export default plugin;
