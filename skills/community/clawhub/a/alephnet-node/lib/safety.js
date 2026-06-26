/**
 * Safety Layer
 * 
 * Re-exports from @aleph-ai/tinyaleph npm library.
 * Uses async loading since tinyaleph is an ESM package.
 * 
 * @module @sschepis/alephnet-node/lib/safety
 */

'use strict';

// Lazy-load the ESM module
let tinyalephModule = null;
const tinyalephPromise = import('@aleph-ai/tinyaleph').then(m => {
    tinyalephModule = m;
    return m;
}).catch(err => {
    console.warn('[Safety] Failed to load @aleph-ai/tinyaleph:', err.message);
    return null;
});

// Fallback implementation
class SafetyLayerFallback {
    constructor(options = {}) {
        this.rules = [];
        this.violations = [];
        this.enabled = options.enabled !== false;
        this.monitor = { alerts: [] };
        this.emergencyShutdown = false;
    }
    
    addRule(rule) {
        this.rules.push({
            id: `rule_${this.rules.length}`,
            ...rule,
            timestamp: Date.now()
        });
    }
    
    check(action, context = {}) {
        return this.isActionPermissible(action, context);
    }

    checkConstraints(metrics) {
        return { safe: true, violations: [], alertLevel: 0 };
    }

    isActionPermissible(action, context) {
         if (!this.enabled) return { permissible: true, safe: true, violations: [] };
         return { permissible: true, safe: true, violations: [] };
    }

    getCorrection(violationName, state) { return null; }
    
    getViolations() {
        return [...this.violations];
    }
    
    clearViolations() {
        this.violations = [];
    }
    
    enable() { this.enabled = true; }
    disable() { this.enabled = false; }
    isEnabled() { return this.enabled; }

    reset() {
        this.violations = [];
        this.monitor.alerts = [];
        this.emergencyShutdown = false;
    }

    toJSON() { return {}; }
    loadFromJSON(data) {}
    getStats() { return {}; }
    generateReport() { return {}; }
}

// Export getters that use the loaded module or fallbacks
module.exports = {
    // Async getter for when you need the full module
    getTinyaleph: () => tinyalephPromise,
    
    get SafetyLayer() {
        return tinyalephModule?.SafetyLayer || SafetyLayerFallback;
    },

    get SafetyMonitor() {
        return tinyalephModule?.SafetyMonitor || class SafetyMonitorFallback {};
    },
    
    get createSafetyLayer() {
        return tinyalephModule?.createSafetyLayer || ((options) => new SafetyLayerFallback(options));
    },
    
    // Fallback export
    SafetyLayerFallback
};
