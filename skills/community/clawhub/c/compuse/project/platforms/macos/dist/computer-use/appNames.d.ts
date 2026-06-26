type InstalledAppLike = {
    readonly bundleId: string;
    readonly displayName: string;
    readonly path: string;
};
export declare function filterAppsForDescription(installed: readonly InstalledAppLike[], homeDir: string | undefined): string[];
export {};
