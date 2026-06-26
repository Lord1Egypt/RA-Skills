import { v4 as uuidv4 } from 'uuid';
import { createRequire } from 'module';
import WebSocket from 'ws';
const require = createRequire(import.meta.url);
const vault = require('./scripts/vault.js');
const relayConnections = new Map();
const updateCallbacks = new Map();
export async function run(action, params, context) {
    try {
        switch (action) {
            case 'agent.register': return await registerIdentity(params);
            case 'message.sign': return await signMessage(params);
            case 'message.verify': return await verifyMessage(params);
            case 'network.connect': return await connectWithAuth(params);
            case 'network.broadcast': return await broadcastUpdate(params);
            case 'secret.genKey': return { success: true, data: { key: await vault.generateSessionKey() } };
            case 'secret.encrypt': return await encryptAction(params);
            case 'secret.decrypt': return await decryptAction(params);
            default: return { success: false, error: `Action ${action} unsupported` };
        }
    }
    catch (err) {
        return { success: false, error: err.message };
    }
}
async function registerIdentity(params) {
    const localAgentId = params.alias || `agent-${uuidv4()}`;
    const keys = await vault.getOrGenerateIdentity(localAgentId);
    const pubKeyHex = Buffer.from(keys.publicKey).toString('hex');
    return { success: true, data: { localId: localAgentId, did: `did:claw:ed25519:${pubKeyHex}`, publicKey: pubKeyHex } };
}
async function connectWithAuth(params) {
    const { sessionId, localId, did, relayUrl = 'ws://localhost:3001', onUpdate } = params;
    if (onUpdate)
        updateCallbacks.set(sessionId, onUpdate);
    return new Promise((resolve, reject) => {
        const ws = new WebSocket(relayUrl);
        ws.on('message', async (data) => {
            const msg = JSON.parse(data.toString());
            if (msg.action === 'challenge') {
                const signRes = await vault.signPayload(localId, msg.challenge);
                ws.send(JSON.stringify({ action: 'subscribe', sessionId, did, challenge: msg.challenge, signature: signRes }));
            }
            if (msg.action === 'authorized') {
                relayConnections.set(sessionId, ws);
                resolve({ success: true, data: { status: 'Authorized' } });
            }
            if (msg.action === 'update') {
                const cb = updateCallbacks.get(sessionId);
                if (cb)
                    cb(msg.payload);
            }
        });
        ws.on('open', () => ws.send(JSON.stringify({ action: 'auth_request' })));
        ws.on('error', (err) => reject({ success: false, error: err.message }));
    });
}
async function broadcastUpdate(params) {
    const { sessionId, payload } = params;
    const ws = relayConnections.get(sessionId);
    if (!ws || ws.readyState !== 1)
        return { success: false, error: "Not connected" };
    ws.send(JSON.stringify({ action: 'broadcast', sessionId, payload }));
    return { success: true };
}
async function signMessage(params) {
    const { localId, payload } = params;
    const contentStr = typeof payload === 'string' ? payload : JSON.stringify(payload);
    const signatureHex = await vault.signPayload(localId, contentStr);
    return { success: true, data: { signature: signatureHex } };
}
async function verifyMessage(params) {
    const { publicKeyHex, payload, signatureHex } = params;
    const contentStr = typeof payload === 'string' ? payload : JSON.stringify(payload);
    const isValid = await vault.verifySignature(publicKeyHex, contentStr, signatureHex);
    return { success: true, data: { verified: isValid } };
}
async function encryptAction(params) {
    const res = await vault.encryptSecret(typeof params.payload === 'string' ? params.payload : JSON.stringify(params.payload), params.sessionKey);
    return { success: true, data: res };
}
async function decryptAction(params) {
    const decrypted = await vault.decryptSecret(params.ciphertext, params.nonce, params.sessionKey);
    return decrypted ? { success: true, data: { decrypted } } : { success: false, error: "Decryption failed" };
}
