// src/lib/config.ts
import * as path from "path";
function getVaultPath() {
  const vaultPath = process.env.CLAWVAULT_PATH;
  if (!vaultPath) {
    throw new Error("CLAWVAULT_PATH environment variable not set");
  }
  return path.resolve(vaultPath);
}

export {
  getVaultPath
};
