#!/usr/bin/env node

function usage() {
    console.error(`Usage: search.mjs "query" [-n <count>] [--sources news,dic,web] [--no-reranking]`);
    process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

let query = "";
let max_results = 10;
let search_sources = ["news", "dic", "web"];
let reranking = "on";

for (let i = 0; i < args.length; i++) {
    if (args[i] === "-n" && i + 1 < args.length) {
        max_results = parseInt(args[++i], 10);
    } else if (args[i] === "--sources" && i + 1 < args.length) {
        search_sources = args[++i].split(",");
    } else if (args[i] === "--no-reranking") {
        reranking = "off";
    } else if (!args[i].startsWith("-")) {
        query = args[i];
    }
}

if (!query) usage();

const apiKey = process.env.DAUM_TOY_SEARCH_API_KEY;
if (!apiKey) {
    console.error("Error: DAUM_TOY_SEARCH_API_KEY environment variable is missing.");
    process.exit(1);
}

async function search() {
    const url = "https://daum-perplexity-search-adapter.toy.x.upstage.ai/search";
    const payload = {
        query: query,
        max_results: max_results,
        search_sources: search_sources,
        reranking: reranking
    };

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            console.error(`Error: API returned status ${response.status}`);
            const text = await response.text();
            console.error(text);
            process.exit(1);
        }

        const data = await response.json();

        // Output formatted Markdown for agents
        if (data.results && data.results.length > 0) {
            console.log(`## Search Results for "${query}"\n`);
            data.results.forEach((res, index) => {
                console.log(`### ${index + 1}. [${res.title}](${res.url})`);
                console.log(`**Source:** ${res.source} | **Date:** ${res.date}`);
                console.log(`${res.snippet}\n`);
            });
        } else {
            console.log("No results found.");
        }
    } catch (error) {
        console.error("Request failed:", error);
        process.exit(1);
    }
}

search().then(() => {
    // Done
}).catch(err => {
    console.error("Unhandled error:", err);
    process.exit(1);
});
