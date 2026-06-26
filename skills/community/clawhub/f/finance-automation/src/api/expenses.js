/**
 * Expenses API Routes
 */

const express = require('express');
const router = express.Router();
const expenseService = require('../services/expense');

// GET /api/expenses - List expenses
router.get('/', async (req, res, next) => {
  try {
    const { limit, offset, category, status, vendor, from, to } = req.query;
    const result = await expenseService.getExpenses({ limit, offset, category, status, vendor, from, to });
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// POST /api/expenses - Add expense
router.post('/', async (req, res, next) => {
  try {
    const expense = await expenseService.addExpense(req.body);
    res.status(201).json(expense);
  } catch (error) {
    next(error);
  }
});

// GET /api/expenses/:id - Get expense
router.get('/:id', async (req, res, next) => {
  try {
    const expense = await expenseService.getExpenseById(req.params.id);
    res.json(expense);
  } catch (error) {
    next(error);
  }
});

// PUT /api/expenses/:id - Update expense (pending only)
router.put('/:id', async (req, res, next) => {
  try {
    const expense = await expenseService.updateExpense(req.params.id, req.body);
    res.json(expense);
  } catch (error) {
    next(error);
  }
});

// DELETE /api/expenses/:id - Delete expense (pending only)
router.delete('/:id', async (req, res, next) => {
  try {
    const result = await expenseService.deleteExpense(req.params.id);
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// POST /api/expenses/:id/approve - Approve expense
router.post('/:id/approve', async (req, res, next) => {
  try {
    const expense = await expenseService.approveExpense(req.params.id, req.body.approvedBy);
    res.json(expense);
  } catch (error) {
    next(error);
  }
});

// POST /api/expenses/:id/reject - Reject expense
router.post('/:id/reject', async (req, res, next) => {
  try {
    const expense = await expenseService.rejectExpense(req.params.id);
    res.json(expense);
  } catch (error) {
    next(error);
  }
});

module.exports = router;
