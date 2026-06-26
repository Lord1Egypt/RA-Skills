import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const bridgeDir = dirname(fileURLToPath(import.meta.url));

export const repoRoot = resolve(bridgeDir, "..");

