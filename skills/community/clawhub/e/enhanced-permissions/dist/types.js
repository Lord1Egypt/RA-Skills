"use strict";
/**
 * OpenClaw Enhanced Permission System
 * Based on Claw Code analysis - 2026-04-01
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.PermissionLevel = void 0;
/**
 * Permission levels for operations
 *
 * - SAFE: Read-only operations, no confirmation needed
 * - MODERATE: Write operations, auto-approve in trusted sessions
 * - DANGEROUS: Delete/Execute operations, always confirm
 * - DESTRUCTIVE: Irreversible operations, explicit confirm + audit
 */
var PermissionLevel;
(function (PermissionLevel) {
    PermissionLevel["SAFE"] = "safe";
    PermissionLevel["MODERATE"] = "moderate";
    PermissionLevel["DANGEROUS"] = "dangerous";
    PermissionLevel["DESTRUCTIVE"] = "destructive";
})(PermissionLevel || (exports.PermissionLevel = PermissionLevel = {}));
//# sourceMappingURL=types.js.map