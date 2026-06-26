/**
 * Admin Module — public interface
 *
 * Admin bot for operational notifications.
 * Separate from @ASGCardbot — uses its own token.
 *
 * @module modules/admin
 */
export { adminRouter } from "./webhook";
export { AdminBot } from "./adminBot";
