/**
 * Suggestion Trigger System
 * Manages when to show suggestions
 *
 * Phase 4 Enhancement - Step 3: Smart Suggestions
 */
/**
 * Trigger configuration
 */
export interface TriggerConfig {
    minMessages: number;
    confidenceThreshold: number;
    maxSuggestions: number;
    cooldownMinutes: number;
    enabled: boolean;
}
/**
 * Trigger state
 */
export interface TriggerState {
    messageCount: number;
    lastSuggestionTime: number;
    shownSuggestions: Set<string>;
    dismissedSuggestions: Set<string>;
}
/**
 * Suggestion Trigger Class
 *
 * Features:
 * - Message counting
 * - Cooldown management
 * - Suggestion tracking
 * - Configurable triggers
 */
export declare class SuggestionTrigger {
    private config;
    private state;
    constructor(config?: Partial<TriggerConfig>);
    /**
     * Check if suggestions should be shown
     */
    shouldShowSuggestion(): boolean;
    /**
     * Increment message count
     */
    onMessage(): void;
    /**
     * Track shown suggestion
     */
    trackShown(suggestionId: string): void;
    /**
     * Track dismissed suggestion
     */
    trackDismissed(suggestionId: string): void;
    /**
     * Check if suggestion was already shown
     */
    wasShown(suggestionId: string): boolean;
    /**
     * Check if suggestion was dismissed
     */
    wasDismissed(suggestionId: string): boolean;
    /**
     * Get trigger state
     */
    getState(): TriggerState;
    /**
     * Reset trigger state
     */
    reset(): void;
    /**
     * Update configuration
     */
    updateConfig(config: Partial<TriggerConfig>): void;
    /**
     * Get configuration
     */
    getConfig(): TriggerConfig;
}
/**
 * Default suggestion trigger instance
 */
export declare const defaultSuggestionTrigger: SuggestionTrigger;
//# sourceMappingURL=suggestion-trigger.d.ts.map