import process from "node:process";

const docsIndexUrl = "https://opendocs.echotik.live/llms.txt";
const minNodeMajor = 18;

function requireSupportedNodeVersion() {
  const major = Number(process.versions.node.split(".")[0]);
  if (Number.isNaN(major) || major < minNodeMajor) {
    throw new Error(`Node.js >= ${minNodeMajor} is required. Current version: ${process.versions.node}`);
  }
}

function parseArgs(argv) {
  const args = {
    limit: 8
  };

  for (let index = 2; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }

    const [rawKey, inlineValue] = token.split("=", 2);
    const key = rawKey.slice(2);
    const nextValue = inlineValue ?? argv[index + 1];

    if (!nextValue || nextValue.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    if (inlineValue === undefined) {
      index += 1;
    }

    if (key === "query") args.query = nextValue;
    else if (key === "limit") args.limit = Number(nextValue);
    else throw new Error(`Unsupported argument: --${key}`);
  }

  return args;
}

function scoreLine(line, queryTerms) {
  const normalized = line.toLowerCase();
  let score = 0;
  for (const term of queryTerms) {
    if (normalized.includes(term)) {
      score += 1;
    }
  }
  return score;
}

async function main() {
  requireSupportedNodeVersion();
  const args = parseArgs(process.argv);
  if (!args.query) {
    throw new Error("Missing required argument: --query");
  }

  const queryTerms = args.query
    .toLowerCase()
    .split(/\s+/)
    .map((term) => term.trim())
    .filter(Boolean);

  const response = await fetch(docsIndexUrl);
  if (!response.ok) {
    throw new Error(`Failed to fetch ${docsIndexUrl}: ${response.status}`);
  }

  const text = await response.text();
  const matches = text
    .split(/\r?\n/)
    .map((line) => ({ line, score: scoreLine(line, queryTerms) }))
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, Math.max(1, args.limit));

  process.stdout.write(
    `${JSON.stringify({ query: args.query, indexUrl: docsIndexUrl, matches }, null, 2)}\n`
  );
}

try {
  await main();
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
