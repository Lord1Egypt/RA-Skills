import { e as SessionRecap } from '../types-DO8rJ490.js';
import { RecoveryInfo } from './recover.js';
import './checkpoint.js';

interface WakeOptions {
    vaultPath: string;
    handoffLimit?: number;
    brief?: boolean;
}
interface WakeResult {
    recovery: RecoveryInfo;
    recap: SessionRecap;
    recapMarkdown: string;
    summary: string;
}
declare function buildWakeSummary(recovery: RecoveryInfo, recap: SessionRecap): string;
declare function wake(options: WakeOptions): Promise<WakeResult>;

export { type WakeOptions, type WakeResult, buildWakeSummary, wake };
