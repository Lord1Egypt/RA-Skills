import pino from 'pino';
import pinoHttp from 'pino-http';
import { randomUUID } from 'node:crypto';

// Redaction paths for PAN/CVV, keys, and secrets to ensure zero leakage in structured JSON logs.
const redactPaths = [
    'req.headers.authorization',
    'req.headers["x-agent-nonce"]',
    'req.headers["x-ops-signature"]',
    'req.body.details',
    'req.body.detailsEnvelope',
    'req.body.cardNumber',
    'req.body.cvv',
    'req.body.expiryMonth',
    'req.body.expiryYear',
    'res.locals',
    'cardNumber',
    'cvv',
    'expiryMonth',
    'expiryYear',
    'detailsEnvelope',
    '*.cardNumber', // Match any nested cardNumber
    '*.cvv',
    '*.detailsEnvelope',
    'agentNonces',
    'details.cardNumber',
    'details.cvv',
    '*.clientSecret',
    '*.accountSecret'
];

export const appLogger = pino({
    level: process.env.LOG_LEVEL || 'info',
    redact: {
        paths: redactPaths,
        censor: '[REDACTED]'
    },
    serializers: {
        err: (err) => {
            const safeErr = pino.stdSerializers.err(err);
            // Deep scrub potential Axios HTTP Client leaks
            if (safeErr.config && safeErr.config.data) {
                safeErr.config.data = '[REDACTED]';
            }
            if (safeErr.response && safeErr.response.data) {
                safeErr.response.data = '[REDACTED]';
            }
            if (safeErr.requestData) {
                safeErr.requestData = '[REDACTED]';
            }
            return safeErr;
        }
    },
    formatters: {
        level: (label) => {
            return { level: label.toUpperCase() };
        },
    },
    timestamp: pino.stdTimeFunctions.isoTime,
});

// HTTP Request Logger Middleware
export const httpLogger = pinoHttp({
    logger: appLogger,
    genReqId: function (req, res) {
        const existingId = req.id ?? req.headers["x-request-id"];
        if (existingId) return existingId;
        const id = randomUUID();
        res.setHeader('X-Request-Id', id);
        return id;
    },
    customProps: function (req, res) {
        return {
            traceId: req.id,
        }
    },
    // We don't want to log successful health checks to avoid noise
    autoLogging: {
        ignore: (req) => {
            if (req.url === '/health') return true;
            return false;
        }
    }
});
