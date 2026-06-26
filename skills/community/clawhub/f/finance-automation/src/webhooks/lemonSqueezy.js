/**
 * Lemon Squeezy Webhook Handler (Placeholder)
 */

const express = require('express');
const router = express.Router();
const logger = require('../utils/logger');

router.post('/', async (req, res) => {
  logger.info('Lemon Squeezy webhook received', { type: req.body?.meta?.event_name });
  // TODO: Implement Lemon Squeezy webhook handling
  res.json({ received: true });
});

module.exports = router;
