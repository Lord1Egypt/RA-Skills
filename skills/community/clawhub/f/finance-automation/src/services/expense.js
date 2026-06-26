/**
 * Expense Service
 */

const db = require('../utils/db');
const logger = require('../utils/logger');

class ExpenseService {
  /**
   * Add a new expense
   */
  async addExpense(data) {
    const {
      amount, currency = 'KRW', category, subcategory, description,
      vendor, expenseDate, receiptPath, tags, metadata
    } = data;

    const result = await db.run(
      `INSERT INTO expenses
       (amount, currency, category, subcategory, description, vendor,
        expense_date, receipt_path, status, tags, metadata)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)`,
      [amount, currency, category, subcategory || null, description,
       vendor || null, expenseDate, receiptPath || null,
       tags ? JSON.stringify(tags) : null,
       metadata ? JSON.stringify(metadata) : null]
    );

    logger.info('Expense added', { id: result.lastID, category, amount });
    return this.getExpenseById(result.lastID);
  }

  /**
   * List expenses with filters and pagination
   */
  async getExpenses(filters = {}) {
    const { category, status, vendor, from, to, limit = 50, offset = 0 } = filters;
    const conditions = [];
    const params = [];

    if (category) {
      conditions.push('category = ?');
      params.push(category);
    }
    if (status) {
      conditions.push('status = ?');
      params.push(status);
    }
    if (vendor) {
      conditions.push('vendor LIKE ?');
      params.push(`%${vendor}%`);
    }
    if (from) {
      conditions.push('expense_date >= ?');
      params.push(from);
    }
    if (to) {
      conditions.push('expense_date <= ?');
      params.push(to);
    }

    const where = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    const countRow = await db.get(`SELECT COUNT(*) as total FROM expenses ${where}`, params);

    const expenses = await db.all(
      `SELECT * FROM expenses ${where} ORDER BY expense_date DESC LIMIT ? OFFSET ?`,
      [...params, parseInt(limit), parseInt(offset)]
    );

    return {
      expenses,
      total: countRow.total,
      limit: parseInt(limit),
      offset: parseInt(offset)
    };
  }

  /**
   * Get expense by ID
   */
  async getExpenseById(id) {
    const expense = await db.get('SELECT * FROM expenses WHERE id = ?', [id]);
    if (!expense) {
      throw Object.assign(new Error('Expense not found'), { status: 404 });
    }
    return expense;
  }

  /**
   * Update expense (pending only)
   */
  async updateExpense(id, data) {
    const expense = await db.get('SELECT * FROM expenses WHERE id = ?', [id]);
    if (!expense) {
      throw Object.assign(new Error('Expense not found'), { status: 404 });
    }
    if (expense.status !== 'pending') {
      throw Object.assign(new Error('Only pending expenses can be updated'), { status: 400 });
    }

    const fieldMap = {
      amount: 'amount', currency: 'currency', category: 'category',
      subcategory: 'subcategory', description: 'description', vendor: 'vendor',
      expenseDate: 'expense_date', receiptPath: 'receipt_path'
    };

    const sets = [];
    const params = [];

    for (const [key, col] of Object.entries(fieldMap)) {
      if (data[key] !== undefined) {
        sets.push(`${col} = ?`);
        params.push(data[key]);
      }
    }

    if (data.tags !== undefined) {
      sets.push('tags = ?');
      params.push(JSON.stringify(data.tags));
    }

    if (sets.length > 0) {
      sets.push('updated_at = CURRENT_TIMESTAMP');
      params.push(id);
      await db.run(`UPDATE expenses SET ${sets.join(', ')} WHERE id = ?`, params);
    }

    logger.info('Expense updated', { id });
    return this.getExpenseById(id);
  }

  /**
   * Delete expense (pending only)
   */
  async deleteExpense(id) {
    const expense = await db.get('SELECT * FROM expenses WHERE id = ?', [id]);
    if (!expense) {
      throw Object.assign(new Error('Expense not found'), { status: 404 });
    }
    if (expense.status !== 'pending') {
      throw Object.assign(new Error('Only pending expenses can be deleted'), { status: 400 });
    }

    await db.run('DELETE FROM expenses WHERE id = ?', [id]);
    logger.info('Expense deleted', { id });
    return { deleted: true };
  }

  /**
   * Approve expense
   */
  async approveExpense(id, approvedBy) {
    const expense = await db.get('SELECT * FROM expenses WHERE id = ?', [id]);
    if (!expense) {
      throw Object.assign(new Error('Expense not found'), { status: 404 });
    }
    if (expense.status !== 'pending') {
      throw Object.assign(new Error('Only pending expenses can be approved'), { status: 400 });
    }

    await db.run(
      `UPDATE expenses SET status = 'approved', approved_by = ?,
       approved_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
       WHERE id = ?`,
      [approvedBy || 'system', id]
    );

    logger.info('Expense approved', { id, approvedBy });
    return this.getExpenseById(id);
  }

  /**
   * Reject expense
   */
  async rejectExpense(id) {
    const expense = await db.get('SELECT * FROM expenses WHERE id = ?', [id]);
    if (!expense) {
      throw Object.assign(new Error('Expense not found'), { status: 404 });
    }
    if (expense.status !== 'pending') {
      throw Object.assign(new Error('Only pending expenses can be rejected'), { status: 400 });
    }

    await db.run(
      `UPDATE expenses SET status = 'rejected', updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
      [id]
    );

    logger.info('Expense rejected', { id });
    return this.getExpenseById(id);
  }

  /**
   * Get category summary for a date range
   */
  async getCategorySummary(from, to) {
    const rows = await db.all(
      `SELECT category,
              COUNT(*) as count,
              SUM(amount) as total_amount,
              AVG(amount) as avg_amount
       FROM expenses
       WHERE expense_date >= ? AND expense_date <= ?
         AND status != 'rejected'
       GROUP BY category
       ORDER BY total_amount DESC`,
      [from, to]
    );

    return rows;
  }
}

module.exports = new ExpenseService();
