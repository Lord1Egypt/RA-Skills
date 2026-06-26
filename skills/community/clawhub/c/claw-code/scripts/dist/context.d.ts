export interface PortContext {
    readonly source_root: string;
    readonly tests_root: string;
    readonly assets_root: string;
    readonly archive_root: string;
    readonly python_file_count: number;
    readonly test_file_count: number;
    readonly asset_file_count: number;
    readonly archive_available: boolean;
}
export declare function buildPortContext(_base?: string): PortContext;
export declare function renderContext(context: PortContext): string;
