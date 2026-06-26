/**
 * Configuration Management
 */

module.exports = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT, 10) || 3000,

  // Stripe
  stripe: {
    secretKey: process.env.STRIPE_SECRET_KEY,
    publishableKey: process.env.STRIPE_PUBLISHABLE_KEY,
    webhookSecret: process.env.STRIPE_WEBHOOK_SECRET
  },

  // Lemon Squeezy
  lemonSqueezy: {
    apiKey: process.env.LEMON_SQUEEZY_API_KEY,
    storeId: process.env.LEMON_SQUEEZY_STORE_ID,
    webhookSecret: process.env.LEMON_SQUEEZY_WEBHOOK_SECRET
  },

  // Database
  database: {
    url: process.env.DATABASE_URL || 'sqlite:./db/finance.db'
  },

  // JWT
  jwt: {
    secret: process.env.JWT_SECRET || 'change-this-secret',
    expiresIn: '7d'
  },

  // Email
  email: {
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT, 10) || 587,
    secure: process.env.SMTP_SECURE === 'true',
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
    from: process.env.SMTP_FROM || 'noreply@yourdomain.com'
  },

  // Telegram
  telegram: {
    botToken: process.env.TELEGRAM_BOT_TOKEN,
    chatId: process.env.TELEGRAM_CHAT_ID
  },

  // OpenClaw
  openclaw: {
    apiUrl: process.env.OPENCLAW_API_URL || 'http://localhost:7777',
    token: process.env.OPENCLAW_TOKEN
  },

  // PDF
  pdf: {
    storagePath: process.env.PDF_STORAGE_PATH || './storage/pdfs'
  },

  // OCR
  ocr: {
    enabled: process.env.ENABLE_OCR === 'true',
    tesseractPath: process.env.TESSERACT_PATH
  },

  // Security
  cors: {
    origin: process.env.CORS_ORIGIN || 'http://localhost:3000'
  },
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS, 10) || 15 * 60 * 1000,
    max: parseInt(process.env.RATE_LIMIT_MAX, 10) || 100
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    filePath: process.env.LOG_FILE_PATH || './logs/app.log'
  },

  // Features
  features: {
    autoInvoice: process.env.FEATURE_AUTO_INVOICE === 'true',
    ocr: process.env.FEATURE_OCR === 'true',
    aiCategorization: process.env.FEATURE_AI_CATEGORIZATION !== 'false'
  }
};
