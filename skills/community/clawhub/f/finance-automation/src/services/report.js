/**
 * Report Service
 */

const db = require('../utils/db');
const logger = require('../utils/logger');

class ReportService {
  /**
   * Daily report: revenue + expenses for a specific date
   */
  async getDailyReport(date) {
    const revenue = await db.get(
      `SELECT * FROM daily_revenue WHERE date = ?`,
      [date]
    );

    const expenses = await db.all(
      `SELECT category, SUM(amount) as total_amount, COUNT(*) as count
       FROM expenses
       WHERE expense_date = ? AND status != 'rejected'
       GROUP BY category`,
      [date]
    );

    const totalExpenses = expenses.reduce((sum, e) => sum + e.total_amount, 0);

    return {
      date,
      revenue: {
        total: revenue?.total_revenue || 0,
        payments: revenue?.total_payments || 0,
        successful: revenue?.successful_payments || 0,
        failed: revenue?.failed_payments || 0
      },
      expenses: {
        total: totalExpenses,
        byCategory: expenses
      },
      profit: (revenue?.total_revenue || 0) - totalExpenses
    };
  }

  /**
   * Monthly report: revenue + expenses for year/month
   */
  async getMonthlyReport(year, month) {
    const monthStr = `${year}-${String(month).padStart(2, '0')}`;

    const revenue = await db.get(
      `SELECT * FROM monthly_revenue WHERE month = ?`,
      [monthStr]
    );

    const expenses = await db.all(
      `SELECT category, SUM(amount) as total_amount, COUNT(*) as count
       FROM expenses
       WHERE strftime('%Y-%m', expense_date) = ? AND status != 'rejected'
       GROUP BY category`,
      [monthStr]
    );

    const totalExpenses = expenses.reduce((sum, e) => sum + e.total_amount, 0);

    const invoices = await db.get(
      `SELECT COUNT(*) as count, SUM(total) as total_amount
       FROM invoices
       WHERE strftime('%Y-%m', issue_date) = ?`,
      [monthStr]
    );

    return {
      month: monthStr,
      revenue: {
        total: revenue?.total_revenue || 0,
        payments: revenue?.total_payments || 0,
        successful: revenue?.successful_payments || 0
      },
      expenses: {
        total: totalExpenses,
        byCategory: expenses
      },
      invoices: {
        count: invoices?.count || 0,
        totalAmount: invoices?.total_amount || 0
      },
      profit: (revenue?.total_revenue || 0) - totalExpenses
    };
  }

  /**
   * Summary for a date range: income / expenses / profit
   */
  async getSummary(from, to) {
    const revenue = await db.get(
      `SELECT SUM(CASE WHEN status = 'succeeded' THEN amount ELSE 0 END) as total_revenue,
              COUNT(*) as total_payments,
              SUM(CASE WHEN status = 'succeeded' THEN 1 ELSE 0 END) as successful_payments,
              SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_payments
       FROM payments
       WHERE DATE(created_at) >= ? AND DATE(created_at) <= ?`,
      [from, to]
    );

    const expenses = await db.get(
      `SELECT SUM(amount) as total, COUNT(*) as count
       FROM expenses
       WHERE expense_date >= ? AND expense_date <= ? AND status != 'rejected'`,
      [from, to]
    );

    const invoices = await db.get(
      `SELECT COUNT(*) as total,
              SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END) as paid,
              SUM(CASE WHEN status = 'sent' THEN 1 ELSE 0 END) as outstanding,
              SUM(CASE WHEN status = 'paid' THEN total ELSE 0 END) as paid_amount,
              SUM(CASE WHEN status = 'sent' THEN total ELSE 0 END) as outstanding_amount
       FROM invoices
       WHERE issue_date >= ? AND issue_date <= ?`,
      [from, to]
    );

    const totalRevenue = revenue?.total_revenue || 0;
    const totalExpenses = expenses?.total || 0;

    return {
      period: { from, to },
      revenue: {
        total: totalRevenue,
        payments: revenue?.total_payments || 0,
        successful: revenue?.successful_payments || 0,
        failed: revenue?.failed_payments || 0
      },
      expenses: {
        total: totalExpenses,
        count: expenses?.count || 0
      },
      invoices: {
        total: invoices?.total || 0,
        paid: invoices?.paid || 0,
        outstanding: invoices?.outstanding || 0,
        paidAmount: invoices?.paid_amount || 0,
        outstandingAmount: invoices?.outstanding_amount || 0
      },
      profit: totalRevenue - totalExpenses
    };
  }

  /**
   * MRR from active subscriptions view
   */
  async getMRR() {
    const rows = await db.all('SELECT * FROM active_subscriptions');

    const totalMRR = rows.reduce((sum, r) => sum + (r.mrr || 0), 0);
    const totalSubscriptions = rows.reduce((sum, r) => sum + (r.count || 0), 0);

    return {
      totalMRR,
      totalSubscriptions,
      byProvider: rows
    };
  }

  /**
   * Profit report: revenue - expenses for a date range
   */
  async getProfitReport(from, to) {
    const dailyRevenue = await db.all(
      `SELECT date, total_revenue, total_payments, successful_payments, failed_payments
       FROM daily_revenue
       WHERE date >= ? AND date <= ?
       ORDER BY date`,
      [from, to]
    );

    const dailyExpenses = await db.all(
      `SELECT expense_date as date, SUM(amount) as total
       FROM expenses
       WHERE expense_date >= ? AND expense_date <= ? AND status != 'rejected'
       GROUP BY expense_date
       ORDER BY expense_date`,
      [from, to]
    );

    const expenseMap = {};
    for (const e of dailyExpenses) {
      expenseMap[e.date] = e.total;
    }

    const totalRevenue = dailyRevenue.reduce((s, r) => s + (r.total_revenue || 0), 0);
    const totalExpenses = dailyExpenses.reduce((s, e) => s + (e.total || 0), 0);

    return {
      period: { from, to },
      totalRevenue,
      totalExpenses,
      netProfit: totalRevenue - totalExpenses,
      profitMargin: totalRevenue > 0
        ? Math.round((totalRevenue - totalExpenses) / totalRevenue * 10000) / 100
        : 0,
      daily: dailyRevenue.map(r => ({
        date: r.date,
        revenue: r.total_revenue || 0,
        expenses: expenseMap[r.date] || 0,
        profit: (r.total_revenue || 0) - (expenseMap[r.date] || 0)
      }))
    };
  }
}

module.exports = new ReportService();
