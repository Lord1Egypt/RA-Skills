"use strict";
/**
 * Suggestion Trigger System
 * Manages when to show suggestions
 *
 * Phase 4 Enhancement - Step 3: Smart Suggestions
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultSuggestionTrigger = exports.SuggestionTrigger = void 0;
/**
 * Suggestion Trigger Class
 *
 * Features:
 * - Message counting
 * - Cooldown management
 * - Suggestion tracking
 * - Configurable triggers
 */
class SuggestionTrigger {
    constructor(config = {}) {
        this.config = {
            minMessages: 5,
            confidenceThreshold: 0.7,
            maxSuggestions: 3,
            cooldownMinutes: 10,
            enabled: true,
            ...config
        };
        this.state = {
            messageCount: 0,
            lastSuggestionTime: 0,
            shownSuggestions: new Set(),
            dismissedSuggestions: new Set()
        };
    }
    /**
     * Check if suggestions should be shown
     */
    shouldShowSuggestion() {
        // Check if enabled
        if (!this.config.enabled) {
            return false;
        }
        // Check message count
        if (this.state.messageCount < this.config.minMessages) {
            return false;
        }
        // Check cooldown
        const now = Date.now();
        const timeSinceLastSuggestion = now - this.state.lastSuggestionTime;
        const cooldownMs = this.config.cooldownMinutes * 60 * 1000;
        if (timeSinceLastSuggestion < cooldownMs) {
            return false;
        }
        return true;
    }
    /**
     * Increment message count
     */
    onMessage() {
        this.state.messageCount++;
    }
    /**
     * Track shown suggestion
     */
    trackShown(suggestionId) {
        this.state.shownSuggestions.add(suggestionId);
        this.state.lastSuggestionTime = Date.now();
        this.state.messageCount = 0; // Reset message count
    }
    /**
     * Track dismissed suggestion
     */
    trackDismissed(suggestionId) {
        this.state.dismissedSuggestions.add(suggestionId);
    }
    /**
     * Check if suggestion was already shown
     */
    wasShown(suggestionId) {
        return this.state.shownSuggestions.has(suggestionId);
    }
    /**
     * Check if suggestion was dismissed
     */
    wasDismissed(suggestionId) {
        return this.state.dismissedSuggestions.has(suggestionId);
    }
    /**
     * Get trigger state
     */
    getState() {
        return { ...this.state };
    }
    /**
     * Reset trigger state
     */
    reset() {
        this.state = {
            messageCount: 0,
            lastSuggestionTime: 0,
            shownSuggestions: new Set(),
            dismissedSuggestions: new Set()
        };
    }
    /**
     * Update configuration
     */
    updateConfig(config) {
        this.config = { ...this.config, ...config };
    }
    /**
     * Get configuration
     */
    getConfig() {
        return { ...this.config };
    }
}
exports.SuggestionTrigger = SuggestionTrigger;
/**
 * Default suggestion trigger instance
 */
exports.defaultSuggestionTrigger = new SuggestionTrigger();
//# sourceMappingURL=suggestion-trigger.js.map