interface ShellInitOptions {
    cwd?: string;
    env?: NodeJS.ProcessEnv;
}
declare function shellInit(options?: ShellInitOptions): string;

export { type ShellInitOptions, shellInit };
