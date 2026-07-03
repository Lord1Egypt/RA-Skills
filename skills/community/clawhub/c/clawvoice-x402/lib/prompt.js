"use strict";

const readline = require("readline");

function isInteractive() {
  return Boolean(process.stdin.isTTY && process.stdout.isTTY);
}

// Resolves null when stdin ends (EOF) before an answer arrives.
function ask(question) {
  if (process.stdin.readableEnded || process.stdin.destroyed) return Promise.resolve(null);
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    let answered = false;
    rl.question(question, (answer) => {
      answered = true;
      rl.close();
      resolve(answer.trim());
    });
    rl.once("close", () => {
      if (!answered) resolve(null);
    });
  });
}

async function askYesNo(question, defaultYes) {
  const hint = defaultYes ? "[Y/n]" : "[y/N]";
  const answer = ((await ask(`${question} ${hint} `)) || "").toLowerCase();
  if (!answer) return defaultYes;
  return answer === "y" || answer === "yes";
}

async function askChoice(question, choices, defaultIndex) {
  console.log(question);
  choices.forEach((choice, i) => console.log(`  ${i + 1}) ${choice}`));
  const answer = await ask(`Choose 1-${choices.length} [${defaultIndex + 1}]: `);
  const n = parseInt(answer || "", 10);
  if (Number.isInteger(n) && n >= 1 && n <= choices.length) return n - 1;
  return defaultIndex;
}

module.exports = { isInteractive, ask, askYesNo, askChoice };
