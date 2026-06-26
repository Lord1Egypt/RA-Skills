interface LinkOptions {
    all?: boolean;
    dryRun?: boolean;
    backlinks?: string;
    orphans?: boolean;
    rebuild?: boolean;
}
declare function linkCommand(file: string | undefined, options: LinkOptions): Promise<void>;

export { linkCommand };
