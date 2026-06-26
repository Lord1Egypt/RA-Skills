#!/usr/bin/env node

/**
 * Agent News API - Simplified Free Tier CLI
 * This version is designed for maximum compatibility and security, 
 * removing all environment variables and premium dependencies.
 */

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];
    const apiUrl = 'https://agentnewsapi.com/api/news/free';

    const helpText = `
Agent News API (Free Tier) - OpenClaw Skill CLI

Usage:
  node agent-news-cli.js <command> [options]

Agent Tools / Commands:
  fetch_news_free      Fetch delayed news signals (20m delay, Free, Rate-limited)
                       Alias: fetch
  help                 Show this help message

Options:
  --limit <number>     Number of signals to fetch (Max: 100, Default: 10)
  --q <string>         Search or category query (e.g., "crypto", "macro")
    `;

    if (!command || command === 'help') {
        console.log(helpText);
        process.exit(0);
    }

    // Helper to parse arguments
    const getArgValue = (flag, defaultValue = null) => {
        const index = args.indexOf(flag);
        return index !== -1 ? args[index + 1] : defaultValue;
    };

    try {
        if (command === 'fetch_news_free' || command === 'fetch') {
            const limit = parseInt(getArgValue('--limit', 10));
            const query = getArgValue('--q');

            let url = `${apiUrl}?limit=${limit}`;
            if (query) url += `&q=${encodeURIComponent(query)}`;

            const response = await fetch(url);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const signals = data.articles || [];

            // Output pure JSON for the agent to parse
            console.log(JSON.stringify({
                success: true,
                tier: 'free',
                delay: '20m',
                count: signals.length,
                query: query || null,
                data: signals
            }, null, 2));

        } else {
            console.error(JSON.stringify({
                success: false,
                error: `Unknown command: ${command}`
            }, null, 2));
            process.exit(1);
        }
    } catch (error) {
        console.error(JSON.stringify({
            success: false,
            error: error.message || 'An unknown error occurred.'
        }, null, 2));
        process.exit(1);
    }
}

main();
