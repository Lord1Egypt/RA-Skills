/**
 * API Routes
 */

const express = require('express');
const router = express.Router();

// Import route handlers
const paymentsRouter = require('./payments');
const invoicesRouter = require('./invoices');
const expensesRouter = require('./expenses');
const reportsRouter = require('./reports');

// Mount routers
router.use('/payments', paymentsRouter);
router.use('/invoices', invoicesRouter);
router.use('/expenses', expensesRouter);
router.use('/reports', reportsRouter);

// API info
router.get('/', (req, res) => {
  res.json({
    name: 'Finance Automation API',
    version: require('../../package.json').version,
    endpoints: {
      payments: '/api/payments',
      invoices: '/api/invoices',
      expenses: '/api/expenses',
      reports: '/api/reports'
    }
  });
});

module.exports = router;
