import { GatewayError } from './common.mjs';

// These protocols belong to the official client's account or billing flow.
// A general gameplay-write grant must never authorize account deletion,
// payment settlement, payment-error reporting, or prepaid-card redemption.
const officialClientCommands = Object.freeze({
  resetaccount: 'Account deletion/reset must be completed by the player in the official client.',
  paypal: 'Payment settlement must be completed in the official client.',
  paypalerr: 'Payment-error reporting belongs to the official client billing flow.',
  googlebilling: 'Google billing must be completed in the official client.',
  gfan_pay: 'Gfan billing must be completed in the official client.',
  joincard: 'Prepaid-card redemption must be completed in the official client.',
});

export function commandPolicy(name) {
  const canonical = name.toLowerCase();
  // The legacy Game_Session.Test handler ignores its argument and writes a
  // fixed greeting. It is an internal diagnostic, not a player action. Keep
  // the catalog entry for compatibility but never forward this protocol.
  if (canonical === 'test') return {
    execution: 'not-player-command',
    errorCode: 'unsupported_command',
    reason: 'The legacy TEST diagnostic is outside player gameplay and is disabled in this gateway. Use earth2037_status for session status.',
  };
  if (!Object.hasOwn(officialClientCommands, canonical)) return null;
  return { execution: 'official-client-only', reason: officialClientCommands[canonical] };
}

export function assertGameCommandAllowed(name, wireName = name) {
  const policy = commandPolicy(name) || commandPolicy(wireName);
  if (policy) throw new GatewayError(policy.errorCode || 'official_client_required', policy.reason);
}
