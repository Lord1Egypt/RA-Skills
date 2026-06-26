import crypto from 'crypto';

export const API_KEY =
  process.env.API_KEY || process.env.GCG_API_KEY || '';

export function generateKey() {
  process.env.API_KEY || process.env.GCG_API_KEY || '';
}

/** @param {import('express').Request} req */
function isLocalhost(req) {
  const ip = req.ip || req.socket?.remoteAddress || '';
  return ip === '127.0.0.1' || ip === '::1' || ip === '::ffff:127.0.0.1';
}

/**
 * API key auth — localhost bypasses key check.
 * @type {import('express').RequestHandler}
 */
export function auth(req, res, next) {
  if (isLocalhost(req)) return next();
  const provided = req.headers['x-api-key'] || req.query.api_key;
  if (provided !== API_KEY) {
    return res.status(403).json({ error: 'Invalid or missing API key' });
  }
  next();
}
