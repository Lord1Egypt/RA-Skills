import {
  buildTemplateVariables,
  renderTemplate
} from "./chunk-7766SIJP.js";
import {
  ClawVault,
  createVault,
  findVault
} from "./chunk-MXNXWOPL.js";
import {
  setupCommand
} from "./chunk-QYJI73KF.js";
import {
  DEFAULT_CATEGORIES,
  DEFAULT_CONFIG,
  MEMORY_TYPES,
  QMD_INSTALL_COMMAND,
  QMD_INSTALL_URL,
  QmdUnavailableError,
  SearchEngine,
  TYPE_TO_CATEGORY,
  extractTags,
  extractWikiLinks,
  hasQmd,
  qmdEmbed,
  qmdUpdate
} from "./chunk-VJIFT5T5.js";

// src/index.ts
import * as fs from "fs";
function readPackageVersion() {
  try {
    const pkgUrl = new URL("../package.json", import.meta.url);
    const pkg = JSON.parse(fs.readFileSync(pkgUrl, "utf-8"));
    return pkg.version ?? "0.0.0";
  } catch {
    return "0.0.0";
  }
}
var VERSION = readPackageVersion();
export {
  ClawVault,
  DEFAULT_CATEGORIES,
  DEFAULT_CONFIG,
  MEMORY_TYPES,
  QMD_INSTALL_COMMAND,
  QMD_INSTALL_URL,
  QmdUnavailableError,
  SearchEngine,
  TYPE_TO_CATEGORY,
  VERSION,
  buildTemplateVariables,
  createVault,
  extractTags,
  extractWikiLinks,
  findVault,
  hasQmd,
  qmdEmbed,
  qmdUpdate,
  renderTemplate,
  setupCommand
};
