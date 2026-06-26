/**
 * Webhook Routes
 */

const express = require('express');
const router = express.Router();

const stripeWebhook = require('./stripe');
const lemonSqueezyWebhook = require('./lemonSqueezy');

router.use('/stripe', stripeWebhook);
router.use('/lemon-squeezy', lemonSqueezyWebhook);

module.exports = router;
