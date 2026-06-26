/**
 * OpenClaw lifecycle hooks for the FairygitMother skill.
 *
 * These integrate with OpenClaw's event system if the runtime supports
 * programmatic skill hooks. The SKILL.md is the primary interface —
 * these hooks are optional automation for advanced setups.
 */

export interface OpenClawHooks {
	onActivate?: () => Promise<void>;
	onDeactivate?: () => Promise<void>;
	onIdle?: () => Promise<void>;
	onCommand?: (command: string, args: string[]) => Promise<string>;
}
