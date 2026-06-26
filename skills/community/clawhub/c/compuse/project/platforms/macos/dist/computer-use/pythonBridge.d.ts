export declare function callPythonHelper<T>(command: string, payload?: Record<string, unknown>): Promise<T>;
export declare function getRuntimePaths(): {
    projectRoot: string;
    runtimeRoot: string;
    venvRoot: string;
};
