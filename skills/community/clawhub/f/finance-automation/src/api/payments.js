/**
 * Payments API Routes
 */

const express = require('express');
const router = express.Router();
const paymentService = require('../services/payment');

// GET /api/payments - List payments
router.get('/', async (req, res, next) => {
  try {
    const { limit, offset, status, provider } = req.query;
    const result = await paymentService.getPayments({ limit, offset, status, provider });
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// GET /api/payments/stats - Payment statistics
router.get('/stats', async (req, res, next) => {
  try {
    const { from, to } = req.query;
    const stats = await paymentService.getPaymentStats(from, to);
    res.json(stats);
  } catch (error) {
    next(error);
  }
});

// GET /api/payments/:id - Get payment by ID
router.get('/:id', async (req, res, next) => {
  try {
    const payment = await paymentService.getPaymentById(req.params.id);
    if (!payment) {
      return res.status(404).json({ error: 'Payment not found' });
    }
    res.json(payment);
  } catch (error) {
    next(error);
  }
});

module.exports = router;
