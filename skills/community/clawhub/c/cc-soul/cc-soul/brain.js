import { isEnabled } from "./features.ts";
const TRIP_THRESHOLD = 5;
const RESET_TIMEOUT = 5 * 6e4;
class Brain {
  modules = /* @__PURE__ */ new Map();
  breakers = /* @__PURE__ */ new Map();
  manualEnabled = /* @__PURE__ */ new Set();
  // override enabled:false at runtime
  manualDisabled = /* @__PURE__ */ new Set();
  // override enabled:true at runtime
  initDone = false;
  // ── Registration ──
  register(mod) {
    if (this.modules.has(mod.id)) {
      console.log(`[brain] replacing module: ${mod.id}`);
    }
    this.modules.set(mod.id, mod);
    this.breakers.set(mod.id, { failures: 0, lastFailure: 0, state: "closed" });
    console.log(`[brain] registered: ${mod.id} (${mod.name})`);
  }
  // ── Lifecycle ──
  async initAll() {
    if (this.initDone) return;
    this.initDone = true;
    const sorted = this.topoSort();
    for (const id of sorted) {
      const mod = this.modules.get(id);
      if (!mod.init) continue;
      try {
        await mod.init();
        console.log(`[brain] init ok: ${id}`);
      } catch (e) {
        console.error(`[brain] init FAILED: ${id} \u2014 ${e.message}`);
        this.trip(id, e);
      }
    }
    console.log(`[brain] ${this.modules.size} modules initialized`);
  }
  disposeAll() {
    for (const [id, mod] of this.modules) {
      try {
        mod.dispose?.();
      } catch (e) {
        console.error(`[brain] dispose error: ${id} \u2014 ${e.message}`);
      }
    }
    this.initDone = false;
  }
  // ── Event dispatch (fault-isolated) ──
  /** Fire a hook on all modules, collect Augment[] results (for onPreprocessed) */
  firePreprocessed(event) {
    const allAugments = [];
    for (const mod of this.sorted()) {
      if (!mod.onPreprocessed || !this.isAvailable(mod.id)) continue;
      try {
        const result = mod.onPreprocessed(event);
        if (result && result.length > 0) allAugments.push(...result);
        this.success(mod.id);
      } catch (e) {
        this.fail(mod.id, "onPreprocessed", e);
      }
    }
    return allAugments;
  }
  /** Fire a hook on all modules, collect string results (for onBootstrap) */
  fireBootstrap(event) {
    const snippets = [];
    for (const mod of this.sorted()) {
      if (!mod.onBootstrap || !this.isAvailable(mod.id)) continue;
      try {
        const result = mod.onBootstrap(event);
        if (result) snippets.push(result);
        this.success(mod.id);
      } catch (e) {
        this.fail(mod.id, "onBootstrap", e);
      }
    }
    return snippets;
  }
  /** Fire a void hook on all modules (for onSent, onCommand, onHeartbeat) */
  fire(hook, event) {
    for (const mod of this.sorted()) {
      const fn = mod[hook];
      if (!fn || !this.isAvailable(mod.id)) continue;
      try {
        fn.call(mod, event);
        this.success(mod.id);
      } catch (e) {
        this.fail(mod.id, hook, e);
      }
    }
  }
  // ── Query ──
  getModule(id) {
    return this.modules.get(id);
  }
  /** Enable a module at runtime (overrides enabled:false) */
  enableModule(id) {
    if (!this.modules.has(id)) return false;
    this.manualDisabled.delete(id);
    this.manualEnabled.add(id);
    console.log(`[brain] ${id}: enabled`);
    return true;
  }
  /** Disable a module at runtime */
  disableModule(id) {
    if (!this.modules.has(id)) return false;
    this.manualEnabled.delete(id);
    this.manualDisabled.add(id);
    console.log(`[brain] ${id}: disabled`);
    return true;
  }
  listModules() {
    return [...this.modules.values()].map((mod) => {
      const b = this.breakers.get(mod.id);
      const featureOff = mod.features?.length && mod.features.some((f) => !isEnabled(f));
      return {
        id: mod.id,
        name: mod.name,
        status: featureOff ? "disabled" : b.state === "closed" ? "ok" : b.state === "open" ? "tripped" : "recovering"
      };
    });
  }
  getHealth() {
    const mods = this.listModules();
    const ok = mods.filter((m) => m.status === "ok").length;
    const tripped = mods.filter((m) => m.status === "tripped");
    if (tripped.length === 0) return `${ok}/${mods.length} modules ok`;
    return `${ok}/${mods.length} ok, tripped: ${tripped.map((m) => m.id).join(", ")}`;
  }
  // ── Circuit breaker internals ──
  isAvailable(id) {
    const mod = this.modules.get(id);
    if (this.manualDisabled.has(id)) return false;
    if (mod?.enabled === false && !this.manualEnabled.has(id)) return false;
    if (mod?.features && mod.features.length > 0) {
      if (mod.features.some((f) => !isEnabled(f))) return false;
    }
    const b = this.breakers.get(id);
    if (!b) return false;
    if (b.state === "closed") return true;
    if (b.state === "open") {
      if (Date.now() - b.lastFailure > RESET_TIMEOUT) {
        b.state = "half-open";
        console.log(`[brain] ${id}: half-open (retrying)`);
        return true;
      }
      return false;
    }
    return true;
  }
  success(id) {
    const b = this.breakers.get(id);
    if (!b) return;
    if (b.state !== "closed") {
      console.log(`[brain] ${id}: recovered \u2713`);
    }
    b.failures = 0;
    b.state = "closed";
  }
  fail(id, hook, e) {
    console.error(`[brain] ${id}.${hook} error: ${e.message}`);
    this.trip(id, e);
  }
  trip(id, e) {
    const b = this.breakers.get(id);
    if (!b) return;
    b.failures++;
    b.lastFailure = Date.now();
    if (b.failures >= TRIP_THRESHOLD && b.state === "closed") {
      b.state = "open";
      console.error(`[brain] \u26A1 ${id}: TRIPPED after ${b.failures} failures \u2014 disabled for ${RESET_TIMEOUT / 1e3}s`);
    }
  }
  // ── Topological sort by dependencies ──
  topoSort() {
    const visited = /* @__PURE__ */ new Set();
    const result = [];
    const visit = (id) => {
      if (visited.has(id)) return;
      visited.add(id);
      const mod = this.modules.get(id);
      if (mod?.dependencies) {
        for (const dep of mod.dependencies) {
          if (this.modules.has(dep)) visit(dep);
        }
      }
      result.push(id);
    };
    for (const id of this.modules.keys()) visit(id);
    return result;
  }
  /** Get modules sorted by priority (descending) */
  sorted() {
    return [...this.modules.values()].filter((m) => this.isAvailable(m.id)).sort((a, b) => (b.priority ?? 50) - (a.priority ?? 50));
  }
}
const brain = new Brain();
export {
  brain
};
