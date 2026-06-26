"use strict";
/**
 * Confirmation Dialog Implementation
 * Terminal-based confirmation for dangerous operations
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.showConfirmationDialog = showConfirmationDialog;
exports.showDestructiveWarning = showDestructiveWarning;
exports.smartConfirm = smartConfirm;
exports.batchConfirm = batchConfirm;
const readline = __importStar(require("readline"));
/**
 * Show confirmation dialog in terminal
 *
 * @param message - Confirmation message to display
 * @param timeout - Timeout in ms (0 = no timeout)
 * @returns Promise<boolean> - true if confirmed, false otherwise
 */
async function showConfirmationDialog(message, timeout = 30000) {
    return new Promise((resolve) => {
        console.log('\n' + message);
        console.log(''); // Empty line for readability
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        let resolved = false;
        // Handle timeout
        let timeoutId;
        if (timeout > 0) {
            timeoutId = setTimeout(() => {
                if (!resolved) {
                    console.log('\n⏱️  Confirmation timeout (30 seconds)\n');
                    rl.close();
                    resolve(false);
                    resolved = true;
                }
            }, timeout);
        }
        rl.question('Your choice (y/n): ', (answer) => {
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
            resolved = true;
            rl.close();
            const confirmed = answer.trim().toLowerCase() === 'y';
            if (confirmed) {
                console.log('✅ Confirmed\n');
            }
            else {
                console.log('❌ Cancelled\n');
            }
            resolve(confirmed);
        });
    });
}
/**
 * Show destructive operation warning
 * Requires explicit "CONFIRM" typing
 *
 * @param operation - Operation name
 * @param params - Operation parameters
 * @returns Promise<boolean> - true if explicitly confirmed
 */
async function showDestructiveWarning(operation, params) {
    const message = [
        '',
        '🔴 ' + '='.repeat(50),
        '🔴 DESTRUCTIVE OPERATION WARNING',
        '🔴 ' + '='.repeat(50),
        '',
        `Operation: ${operation}`,
        '',
        'Parameters:',
        '```json',
        JSON.stringify(params, null, 2),
        '```',
        '',
        '⚠️  This operation is DESTRUCTIVE and IRREVERSIBLE!',
        '⚠️  It may cause permanent data loss or system damage.',
        '',
        'Type CONFIRM (all caps) to proceed, or anything else to cancel:',
        ''
    ].join('\n');
    return new Promise((resolve) => {
        console.log(message);
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        rl.question('', (answer) => {
            rl.close();
            const confirmed = answer.trim() === 'CONFIRM';
            if (confirmed) {
                console.log('\n✅ Destructive operation confirmed\n');
            }
            else {
                console.log('\n❌ Destructive operation cancelled\n');
            }
            resolve(confirmed);
        });
    });
}
/**
 * Smart confirmation based on permission level
 *
 * @param operation - Operation name
 * @param permissionLevel - Permission level
 * @param params - Operation parameters
 * @param confirmMessage - Pre-built confirmation message
 * @returns Promise<boolean> - true if confirmed
 */
async function smartConfirm(operation, permissionLevel, params, confirmMessage) {
    // DESTRUCTIVE requires explicit typing
    if (permissionLevel === 'destructive') {
        return await showDestructiveWarning(operation, params);
    }
    // DANGEROUS and others use standard confirmation
    const message = confirmMessage ||
        `⚠️  Confirm operation: ${operation}\n\nReply y to confirm, n to cancel.`;
    return await showConfirmationDialog(message);
}
/**
 * Batch confirmation for multiple operations
 */
async function batchConfirm(operations) {
    console.log('\n📋 Batch Operation Confirmation');
    console.log('='.repeat(50));
    console.log(`\n${operations.length} operations will be executed:\n`);
    operations.forEach((op, index) => {
        const emoji = getPermissionEmoji(op.permissionLevel);
        console.log(`${index + 1}. ${emoji} ${op.name} (${op.permissionLevel})`);
    });
    console.log('\n' + '='.repeat(50));
    return await showConfirmationDialog(`Execute all ${operations.length} operations? (y/n)`);
}
/**
 * Get emoji for permission level
 */
function getPermissionEmoji(level) {
    const emojis = {
        'safe': '🟢',
        'moderate': '🟡',
        'dangerous': '🟠',
        'destructive': '🔴'
    };
    return emojis[level] || '⚪';
}
//# sourceMappingURL=confirmation-dialog.js.map