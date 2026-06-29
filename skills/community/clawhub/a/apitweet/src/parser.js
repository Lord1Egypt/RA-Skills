import { DEFAULT_CONFIG_DIR, LEADING_GLOBAL_OPTIONS } from "./constants.js";
import { parseHeader, parseJson, exitWithError } from "./utils.js";

export function parseGlobalArgs(argv) {
  const state = {
    method: "GET",
    data: undefined,
    headers: {},
    appName: "",
    profileName: "",
    apiKey: "",
    baseUrl: "",
    configDir: DEFAULT_CONFIG_DIR,
    dryRun: false,
    raw: false,
    help: false,
    commandArgs: [],
  };

  let index = 0;
  while (index < argv.length) {
    const current = argv[index];
    const descriptor = LEADING_GLOBAL_OPTIONS[current];
    if (!descriptor) {
      break;
    }

    if (descriptor.takesValue) {
      const value = argv[index + 1];
      if (!value) {
        exitWithError(`Missing value for ${current}.`);
      }

      if (descriptor.key === "method") {
        state.method = value.toUpperCase();
      } else if (descriptor.key === "data") {
        state.data = parseJson(current, value);
      } else if (descriptor.key === "header") {
        const [name, headerValue] = parseHeader(value);
        state.headers[name] = headerValue;
      } else {
        state[descriptor.key] = value;
      }

      index += 2;
      continue;
    }

    state[descriptor.key] = true;
    index += 1;
  }

  state.commandArgs = argv.slice(index);
  return state;
}
