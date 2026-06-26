// ATP (Agent Transaction Protocol) Module
// Low-commission agent-to-agent transaction network.
//
// Sub-modules:
//   hubClient       - Hub API client for ATP endpoints
//   merchantAgent   - ready-to-use merchant agent template
//   consumerAgent   - ready-to-use consumer agent template
//   serviceHelper   - service publishing helper
//   defaultHandler  - default order handler + config helpers for auto-ATP
//   autoBuyer       - opt-out capability-gap auto order helper with budget caps
//   autoDeliver     - opt-out merchant-side submitDelivery daemon
//   atpTaskPickup   - merchant-side bridge from pre-claimed ATP tasks to sessions_spawn
//   atpExecute      - end-to-end completer (publish Gene+Capsule, complete, deliver)
//   cli             - parsers and runners for the `buy`/`orders`/`verify` subcommands

const hubClient = require('./hubClient');
const merchantAgent = require('./merchantAgent');
const consumerAgent = require('./consumerAgent');
const serviceHelper = require('./serviceHelper');
const defaultHandler = require('./defaultHandler');
const autoBuyer = require('./autoBuyer');
const autoDeliver = require('./autoDeliver');
const atpTaskPickup = require('./atpTaskPickup');
const atpExecute = require('./atpExecute');
const cli = require('./cli');

module.exports = {
  hubClient,
  merchantAgent,
  consumerAgent,
  serviceHelper,
  defaultHandler,
  autoBuyer,
  autoDeliver,
  atpTaskPickup,
  atpExecute,
  cli,
};
