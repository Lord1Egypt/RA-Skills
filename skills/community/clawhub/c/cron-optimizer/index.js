#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const STATE_FILE = path.resolve(__dirname, '../../memory/evolver_cron_state.json');
const CACHE_FILE = path.resolve(__dirname, '../../memory/evolver_cron_cache.json');

/**
 * Cleanup stale and redundant cron jobs to optimize system load and reduce exec noise.
 */
function run() {
    console.log('[CronOptimizer] Starting cron job cleanup...');
    
    // Check if we can skip based on recent run
    if (fs.existsSync(STATE_FILE)) {
        try {
            const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
            // If cleaned up within last 6 hours, skip to reduce noise
            if (Date.now() - state.lastCleanup < 21600000 && state.status === 'ok') {
                console.log('[CronOptimizer] Skipping cleanup (last run < 6h ago).');
                return;
            }
        } catch (e) {}
    }

    let jobs = [];
    try {
        // Attempt to use cached list if very fresh (< 5m)
        let useCache = false;
        if (fs.existsSync(CACHE_FILE)) {
             const cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
             if (Date.now() - cache.timestamp < 300000) {
                 jobs = cache.jobs;
                 useCache = true;
                 console.log('[CronOptimizer] Using cached job list.');
             }
        }

        if (!useCache) {
            const out = execSync('openclaw cron list --all --json', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 15000 });
            const parsed = JSON.parse(out);
            jobs = parsed.jobs || [];
            // Cache it
            fs.writeFileSync(CACHE_FILE, JSON.stringify({ timestamp: Date.now(), jobs }));
        }
    } catch (e) {
        console.error('[CronOptimizer] Failed to list cron jobs:', e.message);
        // Update state to prevent immediate retry loop
        fs.writeFileSync(STATE_FILE, JSON.stringify({ lastCleanup: Date.now(), status: 'error', error: e.message }));
        return;
    }

    const now = Date.now();
    let removedCount = 0;
    
    // Configurable thresholds
    const STALE_AGE_MS = 24 * 60 * 60 * 1000; // 24 hours
    
    for (const job of jobs) {
        let shouldRemove = false;
        const lastRun = job.state?.lastRunAtMs || job.createdAtMs || 0;
        const age = now - lastRun;
        
        // Skip critical system jobs
        if (job.name === 'evolver_watchdog_robust' || job.name === 'Daily Auto-Update') {
            continue;
        }

        // Rule 1: Remove disabled jobs older than 24h
        if (job.enabled === false && age > STALE_AGE_MS) {
            shouldRemove = true;
        }

        // Rule 2: Remove completed one-shot jobs ('at') that ran successfully
        if (job.schedule?.kind === 'at' && job.state?.lastStatus === 'ok' && age > STALE_AGE_MS) {
            shouldRemove = true;
        }

        // Rule 3: Remove "Mad Dog" spam jobs (evolver loops) if disabled
        if ((job.name?.includes('Mad Dog') || job.payload?.message?.includes('evolver/index.js')) && job.enabled === false) {
             shouldRemove = true;
        }

        if (shouldRemove) {
            try {
                console.log(`[CronOptimizer] Removing stale job: ${job.name} (ID: ${job.id}, Age: ${Math.floor(age/3600000)}h)`);
                execSync(`openclaw cron remove "${job.id}"`, { stdio: 'ignore' });
                removedCount++;
            } catch (e) {
                console.error(`[CronOptimizer] Failed to remove job ${job.id}:`, e.message);
            }
        }
    }

    console.log(`[CronOptimizer] Cleanup complete. Removed ${removedCount} stale jobs.`);
    
    // Update state file
    fs.writeFileSync(STATE_FILE, JSON.stringify({ 
        lastCleanup: Date.now(), 
        status: 'ok', 
        removed: removedCount,
        // Also update the watchdog check state for lifecycle.js
        lastChecked: Date.now(),
        exists: jobs.some(j => j.name === 'evolver_watchdog_robust')
    }));

    // Verification: ensure watchdog exists if missing
    // We already have the job list, so check 'jobs' array
    const watchdog = jobs.find(j => j.name === 'evolver_watchdog_robust');
    if (!watchdog) {
         console.warn('[CronOptimizer] WARNING: evolver_watchdog_robust is missing! Recreating...');
         try {
             execSync('node skills/feishu-evolver-wrapper/lifecycle.js ensure', { stdio: 'inherit' });
         } catch(e) {
             console.error('[CronOptimizer] Failed to recreate watchdog:', e.message);
         }
    } else {
         console.log('[CronOptimizer] Verified: evolver_watchdog_robust is present.');
    }
}

if (require.main === module) {
    run();
}

module.exports = { run };
