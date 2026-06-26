"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ComponentManifestManager = void 0;
const PatchSuggestion_1 = require("../common/PatchSuggestion");
class ComponentManifestManager {
    mergeDependency(manifestText, suggestion) {
        const normalizedManifest = this.normalizeManifest(manifestText);
        const lines = normalizedManifest.split('\n');
        const dependencyBlock = this.findDependenciesBlock(lines);
        const entry = dependencyBlock.entries.get(suggestion.dependency);
        if (!dependencyBlock.exists) {
            const manifest = this.appendDependenciesBlock(normalizedManifest, suggestion);
            return {
                status: 'ADDED',
                dependency: suggestion.dependency,
                nextVersion: suggestion.version,
                manifest,
                patch: (0, PatchSuggestion_1.buildPatchSuggestion)({
                    kind: 'append_block',
                    summary: `追加 dependencies 区块并加入 ${suggestion.dependency}。`,
                    before: normalizedManifest || undefined,
                    after: manifest
                })
            };
        }
        if (!entry) {
            const manifest = this.insertDependency(lines, dependencyBlock.endLine, suggestion);
            return {
                status: 'ADDED',
                dependency: suggestion.dependency,
                nextVersion: suggestion.version,
                manifest,
                patch: (0, PatchSuggestion_1.buildPatchSuggestion)({
                    kind: 'insert_block',
                    summary: `向现有 dependencies 区块插入 ${suggestion.dependency}。`,
                    before: normalizedManifest,
                    after: manifest
                })
            };
        }
        if (entry.version === suggestion.version) {
            return {
                status: 'ALREADY_PRESENT',
                dependency: suggestion.dependency,
                currentVersion: entry.version,
                nextVersion: suggestion.version,
                manifest: normalizedManifest
            };
        }
        const manifest = this.replaceDependencyVersion(lines, entry, suggestion.version);
        return {
            status: 'VERSION_CONFLICT',
            dependency: suggestion.dependency,
            currentVersion: entry.version,
            nextVersion: suggestion.version,
            manifest,
            patch: (0, PatchSuggestion_1.buildPatchSuggestion)({
                kind: 'replace_block',
                summary: `将 ${suggestion.dependency} 的版本从 ${entry.version || '未指定'} 更新到 ${suggestion.version}。`,
                before: normalizedManifest,
                after: manifest
            })
        };
    }
    normalizeManifest(value) {
        const normalized = value.replace(/\r\n/g, '\n').trimEnd();
        return normalized;
    }
    appendDependenciesBlock(manifestText, suggestion) {
        const block = [
            'dependencies:',
            `  ${suggestion.dependency}:`,
            `    version: "${suggestion.version}"`
        ].join('\n');
        if (!manifestText.trim()) {
            return `${block}\n`;
        }
        return `${manifestText}\n\n${block}\n`;
    }
    insertDependency(lines, dependencyBlockEndLine, suggestion) {
        const insertion = [
            `  ${suggestion.dependency}:`,
            `    version: "${suggestion.version}"`
        ];
        const nextLines = [...lines];
        nextLines.splice(dependencyBlockEndLine, 0, ...insertion);
        return `${nextLines.join('\n').replace(/\n*$/, '\n')}`;
    }
    replaceDependencyVersion(lines, entry, nextVersion) {
        const nextLines = [...lines];
        if (entry.versionLine !== undefined) {
            nextLines[entry.versionLine] = nextLines[entry.versionLine].replace(/version:\s*["']?[^"'\s]+["']?/, `version: "${nextVersion}"`);
        }
        else {
            nextLines.splice(entry.startLine + 1, 0, `    version: "${nextVersion}"`);
        }
        return `${nextLines.join('\n').replace(/\n*$/, '\n')}`;
    }
    findDependenciesBlock(lines) {
        const dependenciesLine = lines.findIndex((line) => /^dependencies:\s*$/.test(line));
        if (dependenciesLine === -1) {
            return {
                exists: false,
                startLine: -1,
                endLine: lines.length,
                entries: new Map()
            };
        }
        let endLine = lines.length;
        for (let index = dependenciesLine + 1; index < lines.length; index += 1) {
            const line = lines[index];
            if (!line.trim()) {
                continue;
            }
            if (/^[^\s#][^:]*:\s*$/.test(line)) {
                endLine = index;
                break;
            }
        }
        const entries = new Map();
        let current = null;
        for (let index = dependenciesLine + 1; index < endLine; index += 1) {
            const line = lines[index];
            const entryMatch = line.match(/^  ([^\s:#][^:]*):\s*(?:["']?([^"'\s]+)["']?)?\s*$/);
            if (entryMatch) {
                if (current) {
                    current.endLine = index;
                    entries.set(current.dependency, current);
                }
                current = {
                    dependency: entryMatch[1].trim(),
                    version: entryMatch[2],
                    startLine: index,
                    endLine,
                    versionLine: entryMatch[2] ? index : undefined
                };
                continue;
            }
            if (!current) {
                continue;
            }
            const versionMatch = line.match(/^    version:\s*["']?([^"'\s]+)["']?\s*$/);
            if (versionMatch) {
                current.version = versionMatch[1];
                current.versionLine = index;
            }
        }
        if (current) {
            current.endLine = endLine;
            entries.set(current.dependency, current);
        }
        return {
            exists: true,
            startLine: dependenciesLine,
            endLine,
            entries
        };
    }
}
exports.ComponentManifestManager = ComponentManifestManager;
//# sourceMappingURL=ComponentManifest.js.map