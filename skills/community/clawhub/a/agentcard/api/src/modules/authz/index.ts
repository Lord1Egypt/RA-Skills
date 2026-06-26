/**
 * Authz/Audit Module — public interface
 *
 * Owner-only authorization, audit trail, rate limiting.
 *
 * @module modules/authz
 */
export { requireOwnerBinding } from "./ownerPolicy";
export { AuditService } from "./auditService";
