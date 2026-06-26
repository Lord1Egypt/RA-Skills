import { Subsystem } from './models.js';
export interface PortManifest {
    readonly src_root: string;
    readonly total_python_files: number;
    readonly top_level_modules: readonly Subsystem[];
}
export declare function buildPortManifest(_srcRoot?: string): PortManifest;
