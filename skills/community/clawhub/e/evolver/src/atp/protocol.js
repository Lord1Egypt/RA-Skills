// Protocol-level enum constants for the Agent Transaction Protocol.
//
// These values (verify modes, routing modes, proof statuses, roles,
// execution modes) live in @evomap/atp-sdk. This module is a thin
// CommonJS facade so callsites in src/atp/ can `require('./protocol')`
// for the authoritative sets instead of re-spelling the literals.
//
// Why move them out: ATP is the wire contract between this engine, the
// EvoMap Hub, and (in future) evox-Rust. Hand-maintaining the allowed
// value sets in each implementation is exactly the drift that the
// v1.80.8 "explore" enum incident taught us to avoid for GEP. The ATP
// contract is extracted into its own SDK before a second runtime wires
// in, while it is still cheap. If you find yourself writing an enum
// list literal here again (e.g. ['pending','verified',...]), stop --
// import the constant from this facade instead, and bump
// @evomap/atp-sdk if the set itself needs to change.
//
// Implementation note: @evomap/atp-sdk is published as ESM
// (`"type": "module"`). Node supports `require()` of synchronous ESM
// packages on 22.12.0 and later. The SDK itself stays permissive
// (`engines.node >=18`) so `import`-based consumers on 18/20 aren't
// blocked; the `>=22.12` guarantee that makes the require() below work
// is pinned in THIS package's (evolver's) `engines.node`, not the SDK's.

const {
  ATP_VERIFY_MODES,
  ATP_VERIFY_ACTIONS,
  ATP_ROUTING_MODES,
  ATP_PROOF_STATUSES,
  ATP_ROLES,
  ATP_EXECUTION_MODES,
} = require('@evomap/atp-sdk');

module.exports = {
  ATP_VERIFY_MODES,
  ATP_VERIFY_ACTIONS,
  ATP_ROUTING_MODES,
  ATP_PROOF_STATUSES,
  ATP_ROLES,
  ATP_EXECUTION_MODES,
};
