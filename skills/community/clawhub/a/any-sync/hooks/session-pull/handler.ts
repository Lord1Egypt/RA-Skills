import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

const { autoPull } = require('@any-sync/cli') as {
  autoPull: (lockfilePath?: string) => { pulled: string[] } | null;
};

const handler = async (event: { type: string; messages: string[] }) => {
  try {
    const result = autoPull();
    const pullCount = result?.pulled?.length ?? 0;
    if (pullCount > 0) {
      event.messages.push(`Any Sync: auto-pulled ${pullCount} file(s) from GitHub.`);
    }
  } catch {
    // Silent failure — don't block session start
  }
};

export default handler;
