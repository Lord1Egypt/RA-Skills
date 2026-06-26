export declare function getChromeUserDataDir(): string;
/**
 * Copy a Chrome profile from the real user data dir to a temporary directory.
 * This avoids SingletonLock conflicts with the user's running Chrome.
 * The caller is responsible for deleting the temp dir when done.
 */
export declare function copyChromeProfileToTemp(profileId: string): string;
export declare function isChromeRunning(): boolean;
export interface EnsureChromeClosedOptions {
    profileName: string;
    allowQuit: boolean;
    isUnattended: boolean;
}
export declare function ensureChromeClosedForProfile(opts: EnsureChromeClosedOptions): Promise<void>;
