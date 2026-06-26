import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);

const { autoPush } = require('@any-sync/cli') as {
  autoPush: (lockfilePath?: string) => { pushed: string[] } | null;
};

const handler = async (event: { type: string; messages: string[] }) => {
  try {
    const result = autoPush();
    const pushCount = result?.pushed?.length ?? 0;
    if (pushCount > 0) {
      event.messages.push(`Any Sync: auto-pushed ${pushCount} file(s) to GitHub.`);
    }
  } catch {
    // Silent failure — don't block session end
  }
};

export default handler;
