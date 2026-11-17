import { readFileSync } from 'node:fs';
import Ajv from 'ajv';
import { GatewayError, requireValue } from './common.mjs';
import { format } from 'node:util';
import { commandPolicy } from './command-policy.mjs';

export const catalog = JSON.parse(readFileSync(new URL('../catalog.json', import.meta.url), 'utf8'));
export const commands = new Map(catalog.commands.map(e => [e.name, e]));
const ajv = new Ajv({ strict: false, allErrors: true });
export const alias = Object.fromEntries(catalog.commands.filter(e=>e.wireCommand).map(e=>[e.name,e.wireCommand]));
export function describeCommand(entry) {
  const policy = commandPolicy(entry.name) || commandPolicy(entry.wireCommand || entry.name);
  return policy ? { ...entry, gatewayPolicy: policy } : entry;
}
const describedCommands = [];
let restrictedCommands = 0;
for (const entry of catalog.commands) {
  const described = describeCommand(entry);
  describedCommands.push(described);
  if (entry.route === 'game' && described.gatewayPolicy && (entry.serverSources.length || alias[entry.name])) restrictedCommands++;
}
export const gatewayCatalog = { ...catalog, commands: describedCommands, coverage: { ...catalog.coverage,
  policyRestrictedGameCommands: restrictedCommands,
  gatewayForwardableGameCommands: catalog.coverage.forwardableGameCommands - restrictedCommands } };
const wireValue = value => {
  const check = v => {
    if (typeof v === 'number' && (!Number.isFinite(v) || (Number.isInteger(v) && !Number.isSafeInteger(v)))) throw new GatewayError('unsafe_number', 'Pass bigint IDs as decimal strings through rawArgs.');
    if (v && typeof v === 'object') for (const child of Object.values(v)) check(child);
  };
  check(value); return typeof value === 'object' ? JSON.stringify(value) : String(value);
};
export function commandSchema(entry) {
  const extra = { operationKey: { type: 'string', minLength: 8, maxLength: 128, description: 'Stable ID for one user intent. Reuse it for retries; never invent a new ID after an unknown outcome.' } };
  const branches = entry.variants.map(v => ({ ...v.schema, properties: { ...v.schema.properties, ...extra },
    required: [...v.schema.required, ...(!entry.readOnly ? ['operationKey'] : [])] }));
  branches.push({ type: 'object', properties: { rawArgs: { type: 'array', maxItems: 64,
    items: { type: ['string', 'number', 'boolean', 'object', 'array'] }, description: 'Exact positional arguments; objects/arrays become compact JSON strings. No automatic parameter guessing.' }, ...extra },
    required: ['rawArgs', ...(!entry.readOnly ? ['operationKey'] : [])], additionalProperties: false });
  return { type: 'object', anyOf: branches };
}
const validators = new Map();
export function serialize(entry, input) {
  let validate = validators.get(entry.name);
  if (!validate) { validate = ajv.compile(commandSchema(entry)); validators.set(entry.name, validate); }
  if (!validate(input)) throw new GatewayError('invalid_arguments', 'Arguments do not match the command schema', { errors: validate.errors });
  if (Object.hasOwn(input, 'rawArgs')) return input.rawArgs.map(wireValue);
  const values = { ...input }; delete values.operationKey;
  const variant = entry.variants.find(v => ajv.validate(v.schema, values));
  requireValue(variant, 'invalid_arguments', 'No matching command variant');
  if (entry.name === 'citybuildlist2') return [String(input.tileId), '1'];
  if (entry.name === 'maprect' || entry.name === 'qm') return [String(input.mapId), input.rects.join(';')];
  // Match Creator cmdToArgs: omit optional fields; declared field order is stable.
  return variant.order.filter(k => input[k] !== undefined && input[k] !== null).map(k => wireValue(input[k]));
}
export function toolFor(entry) {
  const supported = entry.serverSources.length > 0 || alias[entry.name];
  let description = entry.variants[0]?.description || format('Earth2037 %s: positional game protocol command.', entry.name);
  if (!supported) {
    const reason = entry.availability === 'disabled-server-handler'
      ? 'Historical server handler is disabled (empty dispatch branch); returns unsupported_command.'
      : 'Client declaration only: current server has no dispatch; returns unsupported_command.';
    description = format('%s %s', description, reason);
  }
  if (!entry.readOnly) description = format('%s %s', description, 'May change game state. Requires a stable operationKey. No automatic retries.');
  const policy = commandPolicy(entry.name) || commandPolicy(entry.wireCommand || entry.name);
  if (policy) description = format('%s Gateway policy %s: this tool always returns %s; enabling gameplay writes does not unlock it. %s',
    description, policy.execution, policy.errorCode || 'official_client_required', policy.reason);
  return { name: 'e2037_' + entry.name,
    description,
    inputSchema: commandSchema(entry),
    annotations: { readOnlyHint: entry.readOnly, destructiveHint: !entry.readOnly, idempotentHint: false, openWorldHint: true } };
}
