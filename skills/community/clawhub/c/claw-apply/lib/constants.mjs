/**
 * constants.mjs — Shared constants for claw-apply
 */

// --- Timeouts (ms) ---
export const NAVIGATION_TIMEOUT = 25000;
export const SEARCH_NAVIGATION_TIMEOUT = 30000;
export const FEED_NAVIGATION_TIMEOUT = 20000;
export const PAGE_LOAD_WAIT = 6000;
export const SCROLL_WAIT = 1500;
export const SEARCH_LOAD_WAIT = 5000;
export const SEARCH_SCROLL_WAIT = 2000;
export const LOGIN_WAIT = 2000;
export const CLICK_WAIT = 1500;
export const MODAL_STEP_WAIT = 600;
export const SUBMIT_WAIT = 2500;
export const FORM_FILL_WAIT = 2500;
export const DISMISS_TIMEOUT = 3000;
export const APPLY_CLICK_TIMEOUT = 5000;
export const APPLY_BETWEEN_DELAY_BASE = 2000;
export const APPLY_BETWEEN_DELAY_WF_BASE = 1500;
export const APPLY_BETWEEN_DELAY_JITTER = 1000;

// --- LinkedIn ---
export const LINKEDIN_BASE = 'https://www.linkedin.com';
export const LINKEDIN_EASY_APPLY_MODAL_SELECTOR = '[role="dialog"]';
export const LINKEDIN_APPLY_BUTTON_SELECTOR = '[aria-label*="Easy Apply"], [aria-label*="Continue applying"]';
export const LINKEDIN_MAX_MODAL_STEPS = 20;

// --- Wellfound ---
export const WELLFOUND_BASE = 'https://wellfound.com';

// --- Browser ---
export const KERNEL_SDK_PATH = '/home/ubuntu/.openclaw/workspace/node_modules/@onkernel/sdk/index.js';
export const DEFAULT_PLAYWRIGHT_PATH = '/home/ubuntu/.npm-global/lib/node_modules/playwright/index.mjs';

// --- Search ---
export const LINKEDIN_MAX_SEARCH_PAGES = 40;
export const WELLFOUND_MAX_INFINITE_SCROLL = 10;
export const LINKEDIN_SECONDS_PER_DAY = 86400;

// --- Session ---
export const SESSION_REFRESH_POLL_TIMEOUT = 30000;
export const SESSION_REFRESH_POLL_WAIT = 2000;
export const SESSION_LOGIN_VERIFY_WAIT = 3000;

// --- Form Filler ---
export const AUTOCOMPLETE_WAIT = 800;
export const AUTOCOMPLETE_TIMEOUT = 2000;

// --- Form Filler Defaults ---
export const DEFAULT_YEARS_EXPERIENCE = 7;
export const DEFAULT_DESIRED_SALARY = 150000;
export const MINIMUM_SALARY_FACTOR = 0.85;
export const DEFAULT_SKILL_RATING = '8';
export const FORM_PATTERN_MAX_LENGTH = 200;
export const DEFAULT_FIRST_RUN_DAYS = 90;
export const SEARCH_RESULTS_MAX = 30;

// --- Anthropic API ---
export const ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';
export const ANTHROPIC_BATCH_API_URL = 'https://api.anthropic.com/v1/messages/batches';
export const FILTER_DESC_MAX_CHARS = 800;
export const FILTER_BATCH_MAX_TOKENS = 1024;
export const DEFAULT_FILTER_MODEL = 'claude-sonnet-4-6-20251101';
export const DEFAULT_FILTER_MIN_SCORE = 5;

// --- Notification ---
export const TELEGRAM_API_BASE = 'https://api.telegram.org/bot';
export const NOTIFY_RATE_LIMIT_MS = 1500;

// --- ATS platforms (for URL-based detection) ---
export const EXTERNAL_ATS_PATTERNS = [
  { name: 'greenhouse',      pattern: /greenhouse\.io/i },
  { name: 'lever',           pattern: /lever\.co/i },
  { name: 'workday',         pattern: /workday\.com|myworkdayjobs\.com/i },
  { name: 'ashby',           pattern: /ashbyhq\.com/i },
  { name: 'jobvite',         pattern: /jobvite\.com/i },
  { name: 'smartrecruiters', pattern: /smartrecruiters\.com/i },
  { name: 'icims',           pattern: /icims\.com/i },
  { name: 'taleo',           pattern: /taleo\.net/i },
  { name: 'bamboohr',        pattern: /bamboohr\.com/i },
  { name: 'rippling',        pattern: /rippling\.com/i },
  { name: 'workable',        pattern: /workable\.com/i },
  { name: 'dover',           pattern: /dover\.com/i },
];

// --- Queue ---
export const DEFAULT_MAX_RETRIES = 2;

// --- Run limits ---
export const APPLY_RUN_TIMEOUT_MS = 45 * 60 * 1000; // 45 minutes
export const PER_JOB_TIMEOUT_MS = 10 * 60 * 1000; // 10 minutes per job
