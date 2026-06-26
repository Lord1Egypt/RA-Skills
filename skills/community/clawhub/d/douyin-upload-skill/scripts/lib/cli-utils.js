const readline = require("readline");

function parseArgs(argv) {
  const args = Array.from(argv || []);
  const positionals = [];
  const options = {};

  for (let i = 0; i < args.length; i += 1) {
    const token = args[i];
    if (!token.startsWith("--")) {
      positionals.push(token);
      continue;
    }

    const eqIdx = token.indexOf("=");
    if (eqIdx > -1) {
      const key = token.slice(2, eqIdx);
      const value = token.slice(eqIdx + 1);
      options[key] = value;
      continue;
    }

    const key = token.slice(2);
    if (key.startsWith("no-")) {
      options[key.slice(3)] = false;
      continue;
    }

    const next = args[i + 1];
    if (next && !next.startsWith("--")) {
      options[key] = next;
      i += 1;
      continue;
    }

    options[key] = true;
  }

  return { positionals, options };
}

function parseBoolean(value, defaultValue = false) {
  if (typeof value === "boolean") {
    return value;
  }
  if (value === undefined || value === null || value === "") {
    return defaultValue;
  }

  const normalized = String(value).trim().toLowerCase();
  if (["1", "true", "yes", "y", "on"].includes(normalized)) {
    return true;
  }
  if (["0", "false", "no", "n", "off"].includes(normalized)) {
    return false;
  }

  throw new Error(`Invalid boolean value: ${value}`);
}

function parseInteger(value, defaultValue = null) {
  if (value === undefined || value === null || value === "") {
    return defaultValue;
  }
  const parsed = Number.parseInt(String(value), 10);
  if (Number.isNaN(parsed)) {
    throw new Error(`Invalid integer value: ${value}`);
  }
  return parsed;
}

function printJson(payload) {
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}

function prompt(question) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

async function confirm(question, defaultYes = false) {
  const suffix = defaultYes ? "[Y/n]" : "[y/N]";
  const answer = (await prompt(`${question} ${suffix} `)).trim().toLowerCase();
  if (!answer) {
    return defaultYes;
  }
  return ["y", "yes"].includes(answer);
}

function toErrorPayload(error) {
  return {
    ok: false,
    error: {
      message: error.message,
      code: error.code || null,
      details: error.details || null,
    },
  };
}

module.exports = {
  confirm,
  parseArgs,
  parseBoolean,
  parseInteger,
  printJson,
  prompt,
  toErrorPayload,
};
