#!/usr/bin/env node

const path = require('path');
const { AgentNewsClient } = require('./lib/agent-news-client');

// Load environment variables if dotenv is available
try {
    const dotenv = require('dotenv');
    dotenv.config();
} catch (e) {
    // dotenv not found, skipping
}

const apiKey = process.env.AGENT_NEWS_API_KEY;
const privateKey = process.env.SOLANA_PRIVATE_KEY;
const apiUrl = process.env.AGENT_NEWS_API_URL || 'https://api.agentnewsapi.com';

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    // Map the human-readable CLI commands to the OpenClaw Agent Tools
    const helpText = `
Agent News API - OpenClaw Skill CLI

Usage:
  node agent-news-cli.js <command> [options]

Agent Tools / Commands:
  fetch_news_premium   Fetch the latest curated news signals (Real-time, Paid)
                       Alias: fetch
  fetch_news_free      Fetch delayed news signals (20m delay, Free, Rate-limited)
                       Alias: fetch-free
  check_credit_balance Check your current API credit balance
                       Alias: balance
  autonomous_onboard   Self-issue a persistent API key via Solana (Zero-HITL)
                       Alias: onboard
  get_deposit_address  Get the Protocol Hot Wallet address for autonomous funding
                       Alias: deposit-address
  stream               Connect to the live WebSocket firehose (Premium)
                       Alias: listen
  help                 Show this help message

Options (for fetch commands):
  --limit <number>     Number of signals to fetch (Max: Premium 500, Free 100)
  --q <string>         Search or category query (e.g., "crypto", "macro")

Environment Variables:
  AGENT_NEWS_API_KEY   Your API Key
  SOLANA_PRIVATE_KEY   Your Solana Private Key (Base58) for Zero-HITL Auth
  AGENT_NEWS_API_URL   Override API URL (default: https://api.agentnewsapi.com)
    `;

    if (!command || command === 'help') {
        console.log(helpText);
        process.exit(0);
    }

    const client = new AgentNewsClient({
        apiKey,
        privateKey,
        apiUrl
    });

    // Helper to parse arguments
    const getArgValue = (flag, defaultValue = null) => {
        const index = args.indexOf(flag);
        return index !== -1 ? args[index + 1] : defaultValue;
    };

    try {
        if (command === 'fetch_news_premium' || command === 'fetch') {
            const limit = parseInt(getArgValue('--limit', 10));
            const query = getArgValue('--q');

            const params = { limit };
            if (query) params.q = query;

            const signals = await client.getLatestSignals(params);

            // Output pure JSON for OpenClaw to parse
            console.log(JSON.stringify({
                success: true,
                tier: 'premium',
                count: signals.length,
                query: query || null,
                data: signals
            }, null, 2));

        } else if (command === 'fetch_news_free' || command === 'fetch-free') {
            const limit = parseInt(getArgValue('--limit', 10));
            const query = getArgValue('--q');

            const params = { limit };
            if (query) params.q = query;

            const signals = await client.getFreeSignals(params);

            console.log(JSON.stringify({
                success: true,
                tier: 'free',
                delay: '20m',
                count: signals.length,
                query: query || null,
                data: signals
            }, null, 2));

        } else if (command === 'check_credit_balance' || command === 'balance') {
            const balance = await client.getCreditBalance();

            console.log(JSON.stringify({
                success: true,
                balance_sol: balance,
                currency: 'SOL'
            }, null, 2));

        } else if (command === 'autonomous_onboard' || command === 'onboard') {
            // Initiate the Zero-HITL signature flow
            await client.connect();
            console.log(JSON.stringify({
                success: true,
                message: "Zero-HITL Onboarding Successful",
                apiKey: client.apiKey,
                instructions: "Save this apiKey in your environment variables as AGENT_NEWS_API_KEY"
            }, null, 2));
            client.disconnect();

        } else if (command === 'get_deposit_address' || command === 'deposit-address') {
            const hotWallet = '6rSLPtj9Ef7aifNHHFzEPkY5hWECJXryivWx1YhPuXSa';
            console.log(JSON.stringify({
                success: true,
                protocolHotWallet: hotWallet,
                instructions: "Transfer Native SOL to this address to fund your API credits."
            }, null, 2));

        } else if (command === 'stream' || command === 'listen') {
            // Require socket.io-client dynamically so it doesn't load for simple REST commands
            const io = require('socket.io-client');

            if (!apiKey && !client.apiKey) {
                console.error(JSON.stringify({
                    success: false,
                    error: "API Key required for the Premium WebSocket stream. Run 'onboard' first or set AGENT_NEWS_API_KEY."
                }, null, 2));
                process.exit(1);
            }

            // Using console.error for human-readable logs so stdout remains pure JSON for the agent
            console.error("Initiating connection to the Agent News Firehose... (Press Ctrl+C to exit)");

            const socket = io(apiUrl, {
                auth: { apiKey: apiKey || client.apiKey }
            });

            socket.on('connect', () => {
                console.log(JSON.stringify({
                    success: true,
                    event: "connection_established",
                    message: "Sub-second real-time stream active."
                }, null, 2));
            });

            socket.on('news_update', (data) => {
                // Output pure JSON for each event so an agent can parse the stdout stream line-by-line
                console.log(JSON.stringify({
                    success: true,
                    event: 'news_update',
                    data: data
                }, null, 2));
            });

            socket.on('error', (err) => {
                console.error(JSON.stringify({
                    success: false,
                    event: 'socket_error',
                    error: err.code || err.message || err
                }, null, 2));

                if (err.code === 'INSUFFICIENT_CREDITS') {
                    console.error(JSON.stringify({
                        success: false,
                        suggestion: "Refill $SOL balance to resume stream. Use the 'deposit-address' command."
                    }, null, 2));
                    process.exit(1);
                }
            });

            socket.on('disconnect', () => {
                console.error(JSON.stringify({
                    success: true,
                    event: 'disconnect',
                    message: "Disconnected from Firehose."
                }, null, 2));
                process.exit(0);
            });

            // Prevent the Node process from exiting while the socket is open
            return;

        } else {
            console.error(JSON.stringify({
                success: false,
                error: `Unknown command: ${command}`
            }, null, 2));
            process.exit(1);
        }
    } catch (error) {
        // Ensure errors are also returned as valid JSON so the agent doesn't crash
        console.error(JSON.stringify({
            success: false,
            error: error.message || 'An unknown error occurred in the Agent News CLI.'
        }, null, 2));
        process.exit(1);
    }
}

main();