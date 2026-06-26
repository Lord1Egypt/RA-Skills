/**
 * Invoice Service
 */

const db = require('../utils/db');
const logger = require('../utils/logger');

class InvoiceService {
  /**
   * Generate next invoice number: INV-YYYYMM-NNN
   */
  async generateInvoiceNumber() {
    const now = new Date();
    const prefix = `INV-${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}`;

    const row = await db.get(
      `SELECT invoice_number FROM invoices
       WHERE invoice_number LIKE ? || '%'
       ORDER BY invoice_number DESC LIMIT 1`,
      [prefix]
    );

    let seq = 1;
    if (row) {
      const parts = row.invoice_number.split('-');
      seq = parseInt(parts[2], 10) + 1;
    }

    return `${prefix}-${String(seq).padStart(3, '0')}`;
  }

  /**
   * Create invoice with items (transactional)
   */
  async createInvoice(data) {
    const {
      customerName, customerEmail, customerBusinessNumber, customerAddress,
      items, issueDate, dueDate, currency = 'KRW', taxRate = 10.0, notes
    } = data;

    if (!items || items.length === 0) {
      throw Object.assign(new Error('At least one item is required'), { status: 400 });
    }

    const invoiceNumber = await this.generateInvoiceNumber();

    const subtotal = items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0);
    const taxAmount = Math.round(subtotal * taxRate / 100);
    const total = subtotal + taxAmount;

    const result = await db.transaction(async (tx) => {
      const inv = await tx.run(
        `INSERT INTO invoices
         (invoice_number, customer_name, customer_email, customer_business_number,
          customer_address, subtotal, tax_rate, tax_amount, total, currency,
          status, issue_date, due_date, notes)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?)`,
        [invoiceNumber, customerName, customerEmail, customerBusinessNumber || null,
         customerAddress || null, subtotal, taxRate, taxAmount, total, currency,
         issueDate, dueDate, notes || null]
      );

      const invoiceId = inv.lastID;

      for (const item of items) {
        const itemTotal = item.quantity * item.unitPrice;
        await tx.run(
          `INSERT INTO invoice_items (invoice_id, name, description, quantity, unit_price, total)
           VALUES (?, ?, ?, ?, ?, ?)`,
          [invoiceId, item.name, item.description || null, item.quantity, item.unitPrice, itemTotal]
        );
      }

      return invoiceId;
    });

    logger.info('Invoice created', { id: result, invoiceNumber });
    return this.getInvoiceById(result);
  }

  /**
   * List invoices with filters and pagination
   */
  async getInvoices(filters = {}) {
    const { status, customer, limit = 50, offset = 0 } = filters;
    const conditions = [];
    const params = [];

    if (status) {
      conditions.push('status = ?');
      params.push(status);
    }
    if (customer) {
      conditions.push('(customer_name LIKE ? OR customer_email LIKE ?)');
      params.push(`%${customer}%`, `%${customer}%`);
    }

    const where = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    const countRow = await db.get(`SELECT COUNT(*) as total FROM invoices ${where}`, params);

    const invoices = await db.all(
      `SELECT * FROM invoices ${where} ORDER BY created_at DESC LIMIT ? OFFSET ?`,
      [...params, parseInt(limit), parseInt(offset)]
    );

    return {
      invoices,
      total: countRow.total,
      limit: parseInt(limit),
      offset: parseInt(offset)
    };
  }

  /**
   * Get invoice by ID with items
   */
  async getInvoiceById(id) {
    const invoice = await db.get('SELECT * FROM invoices WHERE id = ?', [id]);
    if (!invoice) {
      throw Object.assign(new Error('Invoice not found'), { status: 404 });
    }

    const items = await db.all('SELECT * FROM invoice_items WHERE invoice_id = ?', [id]);
    return { ...invoice, items };
  }

  /**
   * Update invoice (draft only)
   */
  async updateInvoice(id, data) {
    const invoice = await db.get('SELECT * FROM invoices WHERE id = ?', [id]);
    if (!invoice) {
      throw Object.assign(new Error('Invoice not found'), { status: 404 });
    }
    if (invoice.status !== 'draft') {
      throw Object.assign(new Error('Only draft invoices can be updated'), { status: 400 });
    }

    const allowed = ['customer_name', 'customer_email', 'customer_business_number',
      'customer_address', 'issue_date', 'due_date', 'notes', 'currency'];
    const sets = [];
    const params = [];

    // Map camelCase to snake_case
    const fieldMap = {
      customerName: 'customer_name', customerEmail: 'customer_email',
      customerBusinessNumber: 'customer_business_number',
      customerAddress: 'customer_address', issueDate: 'issue_date',
      dueDate: 'due_date', notes: 'notes', currency: 'currency'
    };

    for (const [key, col] of Object.entries(fieldMap)) {
      if (data[key] !== undefined && allowed.includes(col)) {
        sets.push(`${col} = ?`);
        params.push(data[key]);
      }
    }

    if (sets.length > 0) {
      sets.push('updated_at = CURRENT_TIMESTAMP');
      params.push(id);
      await db.run(`UPDATE invoices SET ${sets.join(', ')} WHERE id = ?`, params);
    }

    // If items are provided, replace them
    if (data.items && data.items.length > 0) {
      await db.run('DELETE FROM invoice_items WHERE invoice_id = ?', [id]);

      const subtotal = data.items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0);
      const taxRate = data.taxRate ?? invoice.tax_rate;
      const taxAmount = Math.round(subtotal * taxRate / 100);
      const total = subtotal + taxAmount;

      await db.run(
        `UPDATE invoices SET subtotal = ?, tax_rate = ?, tax_amount = ?, total = ?,
         updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
        [subtotal, taxRate, taxAmount, total, id]
      );

      for (const item of data.items) {
        const itemTotal = item.quantity * item.unitPrice;
        await db.run(
          `INSERT INTO invoice_items (invoice_id, name, description, quantity, unit_price, total)
           VALUES (?, ?, ?, ?, ?, ?)`,
          [id, item.name, item.description || null, item.quantity, item.unitPrice, itemTotal]
        );
      }
    }

    logger.info('Invoice updated', { id });
    return this.getInvoiceById(id);
  }

  /**
   * Delete invoice (draft only)
   */
  async deleteInvoice(id) {
    const invoice = await db.get('SELECT * FROM invoices WHERE id = ?', [id]);
    if (!invoice) {
      throw Object.assign(new Error('Invoice not found'), { status: 404 });
    }
    if (invoice.status !== 'draft') {
      throw Object.assign(new Error('Only draft invoices can be deleted'), { status: 400 });
    }

    await db.run('DELETE FROM invoices WHERE id = ?', [id]);
    logger.info('Invoice deleted', { id });
    return { deleted: true };
  }

  /**
   * Send invoice (status → sent)
   */
  async sendInvoice(id) {
    const invoice = await db.get('SELECT * FROM invoices WHERE id = ?', [id]);
    if (!invoice) {
      throw Object.assign(new Error('Invoice not found'), { status: 404 });
    }
    if (invoice.status !== 'draft') {
      throw Object.assign(new Error('Only draft invoices can be sent'), { status: 400 });
    }

    await db.run(
      `UPDATE invoices SET status = 'sent', sent_at = CURRENT_TIMESTAMP,
       updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
      [id]
    );

    logger.info('Invoice sent', { id, invoiceNumber: invoice.invoice_number });
    return this.getInvoiceById(id);
  }

  /**
   * Mark invoice as paid
   */
  async markAsPaid(id) {
    const invoice = await db.get('SELECT * FROM invoices WHERE id = ?', [id]);
    if (!invoice) {
      throw Object.assign(new Error('Invoice not found'), { status: 404 });
    }
    if (invoice.status === 'paid') {
      throw Object.assign(new Error('Invoice is already paid'), { status: 400 });
    }

    await db.run(
      `UPDATE invoices SET status = 'paid', paid_date = DATE('now'),
       updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
      [id]
    );

    logger.info('Invoice marked as paid', { id, invoiceNumber: invoice.invoice_number });
    return this.getInvoiceById(id);
  }
}

module.exports = new InvoiceService();
