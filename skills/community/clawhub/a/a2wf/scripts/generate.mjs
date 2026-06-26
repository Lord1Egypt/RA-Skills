#!/usr/bin/env node
/**
 * A2WF Generator — creates a spec-compliant siteai.json from parameters or a category template.
 *
 * Usage:
 *   node generate.mjs --domain https://example.com --name "My Store" --language en --category ecommerce
 *   node generate.mjs --domain https://example.com --name "My Bank" --category banking --jurisdiction EU
 *   node generate.mjs --help
 *
 * Output: JSON to stdout. Pipe to file: node generate.mjs ... > siteai.json
 */

// ── Category templates ──────────────────────────────────────────
const TEMPLATES = {
  ecommerce: {
    read: {
      productCatalog: { allowed: true, rateLimit: 60 },
      pricing: { allowed: true, rateLimit: 60 },
      availability: { allowed: true, rateLimit: 30 },
      reviews: { allowed: true, rateLimit: 20 },
      faq: { allowed: true },
      contactInfo: { allowed: true },
      openingHours: { allowed: true },
    },
    action: {
      search: { allowed: true, rateLimit: 30 },
      addToCart: { allowed: false, note: 'Requires human verification' },
      checkout: { allowed: false, note: 'Human-only process' },
      createAccount: { allowed: false },
      submitReview: { allowed: false, humanVerification: true },
      submitContactForm: { allowed: false, humanVerification: true },
    },
    data: {
      customerRecords: { allowed: false },
      orderHistory: { allowed: false },
      paymentInfo: { allowed: false },
    },
    defaults: { agentAccess: 'restricted', requireIdentification: true, maxRequestsPerMinute: 30 },
    scraping: { allowed: false, note: 'Content scraping prohibited. See legal section.' },
  },
  banking: {
    read: {
      faq: { allowed: true },
      contactInfo: { allowed: true },
      companyInfo: { allowed: true },
    },
    action: {
      search: { allowed: true, rateLimit: 10 },
      createAccount: { allowed: false },
      checkout: { allowed: false },
      submitContactForm: { allowed: false, humanVerification: true },
    },
    data: {
      customerRecords: { allowed: false },
      paymentInfo: { allowed: false },
      internalAnalytics: { allowed: false },
      employeeData: { allowed: false },
    },
    defaults: { agentAccess: 'minimal', requireIdentification: true, maxRequestsPerMinute: 10 },
    scraping: { allowed: false },
  },
  healthcare: {
    read: {
      faq: { allowed: true },
      contactInfo: { allowed: true },
      openingHours: { allowed: true },
    },
    action: {
      search: { allowed: true, rateLimit: 10 },
      bookAppointment: { allowed: false, humanVerification: true },
      createAccount: { allowed: false },
      submitContactForm: { allowed: false, humanVerification: true },
    },
    data: {
      customerRecords: { allowed: false },
      employeeData: { allowed: false },
    },
    defaults: { agentAccess: 'minimal', requireIdentification: true, maxRequestsPerMinute: 10 },
    scraping: { allowed: false },
  },
  'news-media': {
    read: {
      companyInfo: { allowed: true },
      contactInfo: { allowed: true },
      faq: { allowed: true },
    },
    action: {
      search: { allowed: true, rateLimit: 20 },
      createAccount: { allowed: false },
      submitContactForm: { allowed: true, humanVerification: true },
    },
    data: {
      customerRecords: { allowed: false },
      internalAnalytics: { allowed: false },
    },
    defaults: { agentAccess: 'restricted', requireIdentification: true, maxRequestsPerMinute: 20 },
    scraping: { allowed: false, note: 'Content is copyrighted. AI training on this content is prohibited.' },
  },
  restaurant: {
    read: {
      productCatalog: { allowed: true, rateLimit: 30, note: 'Menu items' },
      pricing: { allowed: true, rateLimit: 30 },
      openingHours: { allowed: true },
      reviews: { allowed: true, rateLimit: 10 },
      contactInfo: { allowed: true },
      faq: { allowed: true },
    },
    action: {
      search: { allowed: true, rateLimit: 20 },
      bookAppointment: { allowed: true, rateLimit: 5, note: 'Table reservation' },
      createAccount: { allowed: false },
      submitReview: { allowed: false, humanVerification: true },
    },
    data: {
      customerRecords: { allowed: false },
      orderHistory: { allowed: false },
    },
    defaults: { agentAccess: 'open', requireIdentification: false, maxRequestsPerMinute: 30 },
    scraping: { allowed: false },
  },
  saas: {
    read: {
      companyInfo: { allowed: true },
      pricing: { allowed: true, rateLimit: 30 },
      faq: { allowed: true },
      contactInfo: { allowed: true },
    },
    action: {
      search: { allowed: true, rateLimit: 20 },
      createAccount: { allowed: false },
      submitContactForm: { allowed: true, humanVerification: true },
    },
    data: {
      customerRecords: { allowed: false },
      internalAnalytics: { allowed: false },
      employeeData: { allowed: false },
    },
    defaults: { agentAccess: 'restricted', requireIdentification: true, maxRequestsPerMinute: 20 },
    scraping: { allowed: false },
  },
};

// ── Parse args ──────────────────────────────────────────────────
function parseArgs(argv) {
  const opts = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--') && i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
      opts[argv[i].slice(2)] = argv[++i];
    } else if (argv[i] === '--help') {
      opts.help = true;
    }
  }
  return opts;
}

const opts = parseArgs(process.argv.slice(2));

if (opts.help || !opts.domain || !opts.name) {
  console.error(`A2WF Generator — create a siteai.json

Usage:
  node generate.mjs --domain <url> --name <name> [options]

Required:
  --domain <url>       Website URL (e.g., https://example.com)
  --name <name>        Site display name

Options:
  --language <code>    Language code (default: en)
  --category <cat>     Template: ecommerce|banking|healthcare|news-media|restaurant|saas
  --jurisdiction <j>   Jurisdiction (e.g., EU, US, GLOBAL)
  --law <laws>         Comma-separated applicable laws (e.g., "GDPR,EU AI Act")
  --output <file>      Write to file instead of stdout
  --help               Show this help`);
  process.exit(opts.help ? 0 : 2);
}

// ── Build document ──────────────────────────────────────────────
const cat = opts.category?.toLowerCase() || 'saas';
const template = TEMPLATES[cat] || TEMPLATES.saas;

const doc = {
  '@context': 'https://schema.org',
  specVersion: '1.0',
  identity: {
    '@type': 'WebSite',
    domain: opts.domain,
    name: opts.name,
    inLanguage: opts.language || 'en',
    category: cat,
  },
  defaults: template.defaults,
  permissions: {
    read: template.read,
    action: template.action,
    data: template.data,
  },
  scraping: template.scraping,
};

if (opts.jurisdiction) doc.identity.jurisdiction = opts.jurisdiction;
if (opts.law) doc.identity.applicableLaw = opts.law.split(',').map(s => s.trim());

const json = JSON.stringify(doc, null, 2);

if (opts.output) {
  const { writeFileSync } = await import('node:fs');
  writeFileSync(opts.output, json + '\n', 'utf-8');
  console.error(`✅ Written to ${opts.output}`);
} else {
  console.log(json);
}
