/**
 * Confirmation Dialog Implementation
 * Terminal-based confirmation for dangerous operations
 */
/**
 * Show confirmation dialog in terminal
 *
 * @param message - Confirmation message to display
 * @param timeout - Timeout in ms (0 = no timeout)
 * @returns Promise<boolean> - true if confirmed, false otherwise
 */
export declare function showConfirmationDialog(message: string, timeout?: number): Promise<boolean>;
/**
 * Show destructive operation warning
 * Requires explicit "CONFIRM" typing
 *
 * @param operation - Operation name
 * @param params - Operation parameters
 * @returns Promise<boolean> - true if explicitly confirmed
 */
export declare function showDestructiveWarning(operation: string, params: any): Promise<boolean>;
/**
 * Smart confirmation based on permission level
 *
 * @param operation - Operation name
 * @param permissionLevel - Permission level
 * @param params - Operation parameters
 * @param confirmMessage - Pre-built confirmation message
 * @returns Promise<boolean> - true if confirmed
 */
export declare function smartConfirm(operation: string, permissionLevel: string, params: any, confirmMessage?: string): Promise<boolean>;
/**
 * Batch confirmation for multiple operations
 */
export declare function batchConfirm(operations: Array<{
    name: string;
    permissionLevel: string;
    params: any;
}>): Promise<boolean>;
//# sourceMappingURL=confirmation-dialog.d.ts.map