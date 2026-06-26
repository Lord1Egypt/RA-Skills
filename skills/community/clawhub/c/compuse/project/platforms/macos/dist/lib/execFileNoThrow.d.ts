export declare function execFileNoThrow(file: string, args: string[], options?: {
    input?: string;
    useCwd?: boolean;
}): Promise<{
    code: number;
    stdout: string;
    stderr: string;
}>;
