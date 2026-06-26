/**
 * Invoices API Routes
 */

const express = require('express');
const router = express.Router();
const invoiceService = require('../services/invoice');

// GET /api/invoices - List invoices
router.get('/', async (req, res, next) => {
  try {
    const { limit, offset, status, customer } = req.query;
    const result = await invoiceService.getInvoices({ limit, offset, status, customer });
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// POST /api/invoices - Create invoice
router.post('/', async (req, res, next) => {
  try {
    const invoice = await invoiceService.createInvoice(req.body);
    res.status(201).json(invoice);
  } catch (error) {
    next(error);
  }
});

// GET /api/invoices/:id - Get invoice with items
router.get('/:id', async (req, res, next) => {
  try {
    const invoice = await invoiceService.getInvoiceById(req.params.id);
    res.json(invoice);
  } catch (error) {
    next(error);
  }
});

// PUT /api/invoices/:id - Update invoice (draft only)
router.put('/:id', async (req, res, next) => {
  try {
    const invoice = await invoiceService.updateInvoice(req.params.id, req.body);
    res.json(invoice);
  } catch (error) {
    next(error);
  }
});

// DELETE /api/invoices/:id - Delete invoice (draft only)
router.delete('/:id', async (req, res, next) => {
  try {
    const result = await invoiceService.deleteInvoice(req.params.id);
    res.json(result);
  } catch (error) {
    next(error);
  }
});

// POST /api/invoices/:id/send - Send invoice
router.post('/:id/send', async (req, res, next) => {
  try {
    const invoice = await invoiceService.sendInvoice(req.params.id);
    res.json(invoice);
  } catch (error) {
    next(error);
  }
});

// POST /api/invoices/:id/mark-paid - Mark as paid
router.post('/:id/mark-paid', async (req, res, next) => {
  try {
    const invoice = await invoiceService.markAsPaid(req.params.id);
    res.json(invoice);
  } catch (error) {
    next(error);
  }
});

module.exports = router;
