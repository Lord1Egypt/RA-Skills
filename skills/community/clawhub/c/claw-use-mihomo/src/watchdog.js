import { testEndpoints, switchNode, status } from './api.js';
import { log } from './logger.js';

export async function watch(config) {
  const { checkInterval, failThreshold, cooldown } = config.watchdog;
  let failCount = 0;
  let lastSwitch = 0;
  let running = true;

  function shutdown(signal) {
    log(`Received ${signal}, shutting down watchdog`);
    console.log(JSON.stringify({ event: 'shutdown', signal }));
    running = false;
  }

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));

  const current = await status(config).catch(() => ({ node: 'unknown' }));
  log(`Watchdog started: interval=${checkInterval}s threshold=${failThreshold} node=${current.node}`);
  console.log(JSON.stringify({ event: 'started', node: current.node, interval: checkInterval, threshold: failThreshold }));

  while (running) {
    const result = await testEndpoints(config);

    if (result.ok) {
      if (failCount > 0) {
        log(`Recovered after ${failCount} failures`);
        console.log(JSON.stringify({ event: 'recovered', failCount }));
      }
      failCount = 0;
    } else {
      failCount++;
      const s = await status(config).catch(() => ({ node: 'unknown' }));
      log(`Fail #${failCount} on '${s.node}'`);
      console.log(JSON.stringify({ event: 'fail', count: failCount, node: s.node }));

      if (failCount >= failThreshold) {
        const now = Date.now() / 1000;
        if (now - lastSwitch >= cooldown) {
          lastSwitch = now;
          try {
            const switchResult = await switchNode(config);
            log(`Switched: ${switchResult.from} -> ${switchResult.to}`);
            console.log(JSON.stringify({ event: 'switch', ...switchResult }));
          } catch (e) {
            log(`Switch failed: ${e.message}`);
            console.log(JSON.stringify({ event: 'switch_failed', error: e.message }));
          }
        } else {
          log('Cooldown active, skipping switch');
        }
        failCount = 0;
      }
    }

    // Interruptible sleep
    await new Promise(r => {
      const timer = setTimeout(r, checkInterval * 1000);
      if (!running) { clearTimeout(timer); r(); }
    });
  }

  log('Watchdog stopped');
  process.exit(0);
}
