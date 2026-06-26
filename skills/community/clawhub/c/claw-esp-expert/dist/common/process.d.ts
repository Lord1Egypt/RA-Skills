export declare function execFileText(command: string, args: string[], options?: {
    cwd?: string;
    env?: NodeJS.ProcessEnv;
}): Promise<string>;
export declare function spawnCombined(command: string, args: string[], options?: {
    cwd?: string;
    env?: NodeJS.ProcessEnv;
    timeoutMs?: number;
    onData?: (chunk: string) => void;
}): Promise<{
    output: string;
    code: number;
    timedOut: boolean;
}>;
