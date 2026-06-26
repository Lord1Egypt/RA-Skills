export type AcquireResult = {
    kind: 'acquired';
    fresh: boolean;
} | {
    kind: 'blocked';
    by: string;
};
export type CheckResult = {
    kind: 'free';
} | {
    kind: 'held_by_self';
} | {
    kind: 'blocked';
    by: string;
};
export declare function checkComputerUseLock(): Promise<CheckResult>;
export declare function tryAcquireComputerUseLock(): Promise<AcquireResult>;
export declare function releaseComputerUseLock(): Promise<boolean>;
export declare function isLockHeldLocally(): boolean;
