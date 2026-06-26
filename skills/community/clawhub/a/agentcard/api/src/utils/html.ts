/**
 * HTML Utilities — shared escapeHtml for Telegram HTML parse mode.
 *
 * Escaped chars: & < > " (all required for safe HTML in Telegram messages).
 *
 * @module utils/html
 */

/**
 * Escape HTML special characters for safe rendering in Telegram HTML mode.
 * Handles: & < > "
 */
export function escapeHtml(text: string): string {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}
