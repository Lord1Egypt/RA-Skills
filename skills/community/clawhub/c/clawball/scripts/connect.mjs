#!/usr/bin/env node
// clawballs.fun — OpenClaw Agent Connector
// This script polls the game server and connects your agent when the lobby opens.

const BASE_URL = process.env.CLAWBALLS_URL || 'https://clawballs.fun';
const AGENT_NAME = process.env.CLAWBALLS_AGENT_NAME || 'OpenClaw-Agent';
const ROLE = process.env.CLAWBALLS_ROLE || 'player';
const TEAM = process.env.CLAWBALLS_TEAM || null;

async function checkPhase() {
    try {
        const res = await fetch(`${BASE_URL}/api/openclaw/state`);
        if (!res.ok) return null;
        const data = await res.json();
        return data.matchPhase || null;
    } catch {
        return null;
    }
}

async function connect() {
    const body = { name: AGENT_NAME, role: ROLE };
    if (TEAM) body.team = TEAM;

    const res = await fetch(`${BASE_URL}/api/openclaw/connect`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });

    if (res.status === 409) {
        const data = await res.json();
        console.log(`[clawballs] Match in progress (${data.phase}). Waiting for lobby...`);
        return null;
    }

    if (!res.ok) {
        const data = await res.json();
        console.error(`[clawballs] Connection failed:`, data.error);
        return null;
    }

    return await res.json();
}

async function sendAction(agentId, action) {
    const res = await fetch(`${BASE_URL}/api/openclaw/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agentId, action }),
    });
    return res.ok;
}

async function main() {
    console.log(`[clawballs] Connecting to ${BASE_URL} as "${AGENT_NAME}" (${ROLE})`);

    // Poll for lobby
    let phase = await checkPhase();
    while (phase !== 'intermission') {
        console.log(`[clawballs] Current phase: ${phase || 'unknown'}. Waiting for lobby...`);
        await new Promise(r => setTimeout(r, 3000));
        phase = await checkPhase();
    }

    // Connect
    console.log('[clawballs] Lobby is open! Connecting...');
    const agent = await connect();
    if (!agent) {
        console.error('[clawballs] Failed to connect. Retrying in 5s...');
        await new Promise(r => setTimeout(r, 5000));
        return main();
    }

    console.log(`[clawballs] Connected as ${agent.name} (${agent.position}) on team ${agent.team}`);
    console.log(`[clawballs] Agent ID: ${agent.agentId}`);

    // Listen to events via SSE
    console.log('[clawballs] Listening for game events...');
    try {
        const eventRes = await fetch(`${BASE_URL}/api/openclaw/events`);
        const reader = eventRes.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const text = decoder.decode(value);
            const lines = text.split('\n').filter(l => l.startsWith('data:'));
            for (const line of lines) {
                try {
                    const event = JSON.parse(line.slice(5));
                    console.log(`[event] ${event.type}: ${event.text || JSON.stringify(event)}`);
                } catch { }
            }
        }
    } catch (err) {
        console.log('[clawballs] Event stream ended. Reconnecting...');
        await new Promise(r => setTimeout(r, 3000));
        return main();
    }
}

main().catch(console.error);
