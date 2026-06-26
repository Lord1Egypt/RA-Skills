/**
 * AgentBnB Credit Management adapter for OpenClaw skill integration.
 * Delegates to BudgetManager and getBalance from src/credit/.
 * This is a thin re-export wrapper — no business logic lives here.
 */
import { BudgetManager, DEFAULT_BUDGET_CONFIG } from '../../src/credit/budget.js';
import { getBalance } from '../../src/credit/ledger.js';
import type { BudgetConfig } from '../../src/credit/budget.js';

export { BudgetManager, DEFAULT_BUDGET_CONFIG, getBalance };
export type { BudgetConfig };
