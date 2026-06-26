/**
 * ComfyUI server selection, circuit breaker, and health aggregation.
 *
 * Configure via COMFY_SERVERS env var (JSON array):
 *   COMFY_SERVERS='[{"url":"http://192.168.1.100:8169","id":"pri","priority":true,"weight":1}]'
 */

const defaultServers = [{ url: 'http://127.0.0.1:8188', id: 'local', priority: true, weight: 1 }];

export function getServers() {
  try {
    const env = process.env.COMFY_SERVERS;
    if (env) {
      const parsed = JSON.parse(env);
      if (Array.isArray(parsed) && parsed.length > 0) return parsed;
    }
  } catch {}
  return defaultServers;
}

export const SERVERS = getServers();

/** @type {'priority' | 'round-robin' | 'least-queue' | 'random'} */
export let strategy = process.env.LB_STRATEGY || 'priority';

let roundRobinIndex = 0;

// 1:2 PRI:SEC assignment ratio when both servers are idle (SEC gets 2x)
let priAssignments = 0;
let secAssignments = 0;

/** @type {Map<string, { failures: number, degradedUntil: number }>} */
const circuitState = new Map();

const CIRCUIT_FAILURE_THRESHOLD = 3;
const CIRCUIT_COOLDOWN_MS = 60_000;

export async function fetchJson(url, options = {}) {
  const res = await fetch(url, options);
  const text = await res.text();
  try {
    return { status: res.status, data: JSON.parse(text) };
  } catch {
    return { status: res.status, data: text };
  }
}

function getCircuit(id) {
  if (!circuitState.has(id)) {
    circuitState.set(id, { failures: 0, degradedUntil: 0 });
  }
  return circuitState.get(id);
}

export function recordSuccess(serverId) {
  const c = getCircuit(serverId);
  c.failures = 0;
  c.degradedUntil = 0;
}

export function recordFailure(serverId) {
  const c = getCircuit(serverId);
  c.failures += 1;
  if (c.failures >= CIRCUIT_FAILURE_THRESHOLD) {
    c.degradedUntil = Date.now() + CIRCUIT_COOLDOWN_MS;
    console.error(`Circuit breaker: server ${serverId} degraded for ${CIRCUIT_COOLDOWN_MS / 1000}s`);
  }
}

export function isDegraded(serverId) {
  const c = getCircuit(serverId);
  if (Date.now() < c.degradedUntil) return true;
  if (c.degradedUntil > 0 && Date.now() >= c.degradedUntil) {
    c.failures = 0;
    c.degradedUntil = 0;
  }
  return false;
}

export function availableServers(servers = SERVERS) {
  return servers.filter((s) => !isDegraded(s.id));
}

export async function getQueue(server) {
  try {
    const { data } = await fetchJson(`${server.url}/queue`, {
      signal: AbortSignal.timeout(5000),
    });
    recordSuccess(server.id);
    return data;
  } catch {
    recordFailure(server.id);
    return null;
  }
}

export async function queryAllServers(servers = SERVERS) {
  const results = new Map();
  await Promise.all(
    servers.map(async (s) => {
      const q = await getQueue(s);
      results.set(s.id, q);
    }),
  );
  return results;
}

function runningCount(queueData) {
  if (!queueData) return -1;
  return (queueData.queue_running || []).length;
}

function pendingCount(queueData) {
  if (!queueData) return 999;
  return (queueData.queue_pending || []).length;
}

/**
 * @param {typeof SERVERS} servers
 * @param {Map<string, unknown>} results
 */
export function pickServer(servers, results) {
  const pool = availableServers(servers);
  const active = pool.length > 0 ? pool : servers;

  if (strategy === 'random') {
    return active[Math.floor(Math.random() * active.length)] || null;
  }

  if (strategy === 'round-robin') {
    const s = active[roundRobinIndex % active.length];
    roundRobinIndex += 1;
    return s || null;
  }

  if (strategy === 'least-queue') {
    let best = null;
    let bestScore = Infinity;
    for (const s of active) {
      const q = results.get(s.id);
      const score = runningCount(q) * 10 + pendingCount(q);
      if (score < bestScore) {
        bestScore = score;
        best = s;
      }
    }
    return best;
  }

  // Default: priority — 1:2 PRI:SEC when both idle; pri fallback when sec busy
  const pri = active.find((s) => s.priority);
  const sec = active.find((s) => !s.priority);
  const priQ = pri ? results.get(pri.id) : null;
  const secQ = sec ? results.get(sec.id) : null;

  if (!pri) return sec || null;

  const secRunning = secQ !== undefined ? runningCount(secQ) : 0;
  const secPending = secQ !== undefined ? pendingCount(secQ) : 0;

  // Reset ratio window when both servers are fully idle
  if (
    secRunning === 0 &&
    secPending === 0 &&
    priQ &&
    runningCount(priQ) === 0 &&
    pendingCount(priQ) === 0
  ) {
    priAssignments = 0;
    secAssignments = 0;
  }

  if (secRunning > 0 || secPending > 0) {
    // SEC busy → fallback to PRI, reset ratio for next idle round
    priAssignments = 0;
    secAssignments = 0;
    if (pri) return pri;
    return sec;
  }

  // SEC free — enforce 1:2 ratio over a 3-job window (SEC gets 2, PRI gets 1)
  const totalWindow = priAssignments + secAssignments;
  if (totalWindow >= 3) {
    priAssignments = 0;
    secAssignments = 0;
  }

  if (secAssignments < 2) {
    secAssignments++;
    return sec;
  }

  priAssignments++;
  return pri || sec;
}

export async function getServerHealth() {
  const statuses = {};
  await Promise.all(
    SERVERS.map(async (s) => {
      const circuit = getCircuit(s.id);
      try {
        const [{ status }, queueResult] = await Promise.all([
          fetchJson(`${s.url}/`, { signal: AbortSignal.timeout(3000) }),
          getQueue(s),
        ]);
        const q = queueResult;
        statuses[s.id] = {
          status: status === 200 ? 'online' : 'error',
          url: s.url,
          priority: s.priority,
          weight: s.weight,
          degraded: isDegraded(s.id),
          circuit_failures: circuit.failures,
          queue_running: (q?.queue_running || []).length,
          queue_pending: (q?.queue_pending || []).length,
        };
        try {
          const { data: stats } = await fetchJson(`${s.url}/system_stats`, {
            signal: AbortSignal.timeout(5000),
          });
          if (stats?.devices) {
            statuses[s.id].vram = stats.devices.map((d) => ({
              name: d.name,
              vram_total: d.vram_total,
              vram_free: d.vram_free,
            }));
          }
          if (stats?.system) {
            statuses[s.id].uptime = stats.system.uptime;
          }
        } catch {
          /* optional stats */
        }
      } catch {
        statuses[s.id] = {
          status: 'offline',
          url: s.url,
          priority: s.priority,
          degraded: isDegraded(s.id),
          circuit_failures: circuit.failures,
        };
      }
    }),
  );
  return statuses;
}
