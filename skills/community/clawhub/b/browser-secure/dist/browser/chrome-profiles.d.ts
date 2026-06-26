export interface ChromeProfile {
    id: string;
    name: string;
    path: string;
}
export declare function listChromeProfiles(): ChromeProfile[];
export declare function getProfileById(profileIdOrName: string): ChromeProfile | undefined;
export declare function promptProfileSelection(): Promise<ChromeProfile | null>;
export declare function createChromeProfile(name: string): ChromeProfile & {
    welcomePage: string;
};
