"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.pathExists = pathExists;
exports.readJsonFile = readJsonFile;
const promises_1 = require("node:fs/promises");
const node_fs_1 = require("node:fs");
async function pathExists(filePath) {
    try {
        await (0, promises_1.access)(filePath, node_fs_1.constants.F_OK);
        return true;
    }
    catch {
        return false;
    }
}
async function readJsonFile(filePath) {
    return JSON.parse(await (0, promises_1.readFile)(filePath, 'utf8'));
}
//# sourceMappingURL=fs.js.map