/**
 * Payment Service
 */

const db = require('../utils/db');
const logger = require('../utils/logger');

class PaymentService {
  async recordPayment(data) {
    const {
      externalId, provider, customerEmail, amount, currency,
      status, description, metadata
    } = data;

    const result = await db.run(
      `INSERT INTO payments
       (external_id, provider, customer_email, amount, currency, status, description, metadata)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
      [externalId, provider, customerEmail, amount, currency || 'KRW',
       status, description || null, metadata ? JSON.stringify(metadata) : null]
    );

    logger.info('Payment recorded', { id: result.lastID, externalId, status });
    return result.lastID;
  }

  async recordSubscription(data) {
    const {
      externalId, provider, customerEmail, planName, amount, currency,
      interval, status, currentPeriodStart, currentPeriodEnd
    } = data;

    const result = await db.run(
      `INSERT INTO subscriptions
       (external_id, provider, customer_email, plan_name, amount, currency,
        interval, status, current_period_start, current_period_end)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [externalId, provider, customerEmail, planName, amount, currency || 'KRW',
       interval, status, currentPeriodStart, currentPeriodEnd]
    );

    logger.info('Subscription recorded', { id: result.lastID, externalId });
    return result.lastID;
  }

  async updateSubscriptionStatus(externalId, status) {
    await db.run(
      `UPDATE subscriptions SET status = ?, updated_at = CURRENT_TIMESTAMP
       WHERE external_id = ?`,
      [status, externalId]
    );
    logger.info('Subscription status updated', { externalId, status });
  }

  async updateSubscription(externalId, data) {
    const sets = ['updated_at = CURRENT_TIMESTAMP'];
    const params = [];

    if (data.status) {
      sets.push('status = ?');
      params.push(data.status);
    }
    if (data.currentPeriodEnd) {
      sets.push('current_period_end = ?');
      params.push(data.currentPeriodEnd);
    }
    if (data.cancelledAt) {
      sets.push('cancelled_at = ?');
      params.push(data.cancelledAt);
    }

    params.push(externalId);
    await db.run(
      `UPDATE subscriptions SET ${sets.join(', ')} WHERE external_id = ?`,
      params
    );
    logger.info('Subscription updated', { externalId });
  }

  async getPayments(filters = {}) {
    const { status, provider, limit = 50, offset = 0 } = filters;
    const conditions = [];
    const params = [];

    if (status) { conditions.push('status = ?'); params.push(status); }
    if (provider) { conditions.push('provider = ?'); params.push(provider); }

    const where = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    const countRow = await db.get(`SELECT COUNT(*) as total FROM payments ${where}`, params);
    const payments = await db.all(
      `SELECT * FROM payments ${where} ORDER BY created_at DESC LIMIT ? OFFSET ?`,
      [...params, parseInt(limit), parseInt(offset)]
    );

    return { payments, total: countRow.total, limit: parseInt(limit), offset: parseInt(offset) };
  }

  async getPaymentById(id) {
    return db.get('SELECT * FROM payments WHERE id = ?', [id]);
  }

  async getPaymentStats(from, to) {
    const conditions = [];
    const params = [];
    if (from) { conditions.push('DATE(created_at) >= ?'); params.push(from); }
    if (to) { conditions.push('DATE(created_at) <= ?'); params.push(to); }

    const where = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    const row = await db.get(
      `SELECT
        SUM(CASE WHEN status = 'succeeded' THEN amount ELSE 0 END) as totalRevenue,
        COUNT(*) as totalPayments,
        CASE WHEN COUNT(*) > 0
          THEN ROUND(SUM(CASE WHEN status='succeeded' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2)
          ELSE 0 END as successRate,
        CASE WHEN SUM(CASE WHEN status='succeeded' THEN 1 ELSE 0 END) > 0
          THEN ROUND(SUM(CASE WHEN status='succeeded' THEN amount ELSE 0 END) * 1.0
                     / SUM(CASE WHEN status='succeeded' THEN 1 ELSE 0 END), 0)
          ELSE 0 END as averageAmount
       FROM payments ${where}`,
      params
    );

    return row;
  }
}

module.exports = new PaymentService();
