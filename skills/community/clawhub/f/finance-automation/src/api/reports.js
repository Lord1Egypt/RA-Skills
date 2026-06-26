/**
 * Reports API Routes
 */

const express = require('express');
const router = express.Router();
const reportService = require('../services/report');

// GET /api/reports/daily?date=YYYY-MM-DD
router.get('/daily', async (req, res, next) => {
  try {
    const { date } = req.query;
    if (!date) {
      return res.status(400).json({ error: 'date query parameter is required' });
    }
    const report = await reportService.getDailyReport(date);
    res.json(report);
  } catch (error) {
    next(error);
  }
});

// GET /api/reports/monthly?year=YYYY&month=MM
router.get('/monthly', async (req, res, next) => {
  try {
    const { year, month } = req.query;
    if (!year || !month) {
      return res.status(400).json({ error: 'year and month query parameters are required' });
    }
    const report = await reportService.getMonthlyReport(year, month);
    res.json(report);
  } catch (error) {
    next(error);
  }
});

// GET /api/reports/summary?from=YYYY-MM-DD&to=YYYY-MM-DD
router.get('/summary', async (req, res, next) => {
  try {
    const { from, to } = req.query;
    if (!from || !to) {
      return res.status(400).json({ error: 'from and to query parameters are required' });
    }
    const report = await reportService.getSummary(from, to);
    res.json(report);
  } catch (error) {
    next(error);
  }
});

// GET /api/reports/mrr
router.get('/mrr', async (req, res, next) => {
  try {
    const report = await reportService.getMRR();
    res.json(report);
  } catch (error) {
    next(error);
  }
});

// GET /api/reports/profit?from=YYYY-MM-DD&to=YYYY-MM-DD
router.get('/profit', async (req, res, next) => {
  try {
    const { from, to } = req.query;
    if (!from || !to) {
      return res.status(400).json({ error: 'from and to query parameters are required' });
    }
    const report = await reportService.getProfitReport(from, to);
    res.json(report);
  } catch (error) {
    next(error);
  }
});

module.exports = router;
