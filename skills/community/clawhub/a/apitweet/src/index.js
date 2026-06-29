import { loadConfig } from "./config.js";
import { printHelp } from "./help.js";
import { parseGlobalArgs } from "./parser.js";
import { runCommand } from "./commands.js";

export async function main(argv = process.argv.slice(2)) {
  const state = parseGlobalArgs(argv);
  if (state.help || state.commandArgs.length === 0) {
    printHelp();
    return;
  }

  const config = await loadConfig(state.configDir);
  await runCommand(state, config);
}
