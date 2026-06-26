import type { ComponentSuggestion } from './ComponentRegistry';
import { type PatchSuggestion } from '../common/PatchSuggestion';
export interface ManifestMergeResult {
    status: 'ADDED' | 'ALREADY_PRESENT' | 'VERSION_CONFLICT';
    dependency: string;
    currentVersion?: string;
    nextVersion: string;
    manifest: string;
    patch?: PatchSuggestion;
}
export declare class ComponentManifestManager {
    mergeDependency(manifestText: string, suggestion: ComponentSuggestion): ManifestMergeResult;
    private normalizeManifest;
    private appendDependenciesBlock;
    private insertDependency;
    private replaceDependencyVersion;
    private findDependenciesBlock;
}
