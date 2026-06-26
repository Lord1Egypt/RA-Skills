/**
 * ExpenseLog — Conversational Expense Tracking
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');

const CATEGORIES = {
  groceries: ['grocery', 'groceries', 'food', 'whole foods', 'trader joe', 'costco', 'walmart'],
  dining: ['restaurant', 'lunch', 'dinner', 'coffee', 'cafe', 'uber eats', 'doordash'],
  transport: ['gas', 'uber', 'lyft', 'parking', 'bus', 'transit', 'fuel'],
  housing: ['rent', 'mortgage', 'utilities', 'electric', 'water', 'internet'],
  health: ['pharmacy', 'doctor', 'medical', 'gym', 'health'],
  entertainment: ['movie', 'game', 'netflix', 'spotify', 'concert', 'streaming'],
  shopping: ['amazon', 'clothes', 'shoes', 'electronics'],
  subscriptions: ['subscription', 'monthly', 'annual plan']
};

class ExpenseLog {
  constructor(options = {}) {
    this.dataFile = options.dataFile || './expenses.json';
    this.budgets = options.budgets || {};
    this.expenses = this._load();
  }

  add(amount, description, category) {
    const cat = category || this._autoCategory(description);
    const entry = {
      amount: parseFloat(amount),
      description,
      category: cat,
      date: new Date().toISOString().split('T')[0],
      timestamp: Date.now()
    };
    this.expenses.push(entry);
    this._save();
    const monthly = this.monthlyTotal(cat);
    const budget = this.budgets[cat];
    let budgetMsg = '';
    if (budget) {
      const diff = budget - monthly;
      budgetMsg = diff >= 0
        ? ` ($${monthly.toFixed(2)} of $${budget} budget, $${diff.toFixed(2)} remaining)`
        : ` ($${monthly.toFixed(2)} of $${budget} budget, over by $${Math.abs(diff).toFixed(2)})`;
    }
    return { ...entry, monthlyTotal: monthly, message: `Logged: $${amount} ${cat}${budgetMsg}` };
  }

  monthlyTotal(category, month) {
    const m = month || new Date().toISOString().slice(0, 7);
    return this.expenses
      .filter(e => e.date.startsWith(m) && (!category || e.category === category))
      .reduce((sum, e) => sum + e.amount, 0);
  }

  monthlyReport(month) {
    const m = month || new Date().toISOString().slice(0, 7);
    const monthly = this.expenses.filter(e => e.date.startsWith(m));
    const total = monthly.reduce((s, e) => s + e.amount, 0);
    const byCategory = {};
    for (const e of monthly) {
      byCategory[e.category] = (byCategory[e.category] || 0) + e.amount;
    }
    return { month: m, total: Math.round(total * 100) / 100, byCategory, count: monthly.length };
  }

  export(month) {
    const m = month || new Date().toISOString().slice(0, 7);
    const monthly = this.expenses.filter(e => e.date.startsWith(m));
    const csv = 'Date,Amount,Category,Description\n' +
      monthly.map(e => `${e.date},${e.amount},${e.category},"${e.description.replace(/"/g, '""')}"`).join('\n');
    return csv;
  }

  _autoCategory(desc) {
    const lower = desc.toLowerCase();
    for (const [cat, keywords] of Object.entries(CATEGORIES)) {
      if (keywords.some(k => lower.includes(k))) return cat;
    }
    return 'other';
  }

  _load() { try { return JSON.parse(fs.readFileSync(this.dataFile, 'utf8')); } catch { return []; } }
  _save() { try { fs.writeFileSync(this.dataFile, JSON.stringify(this.expenses, null, 2)); } catch {} }
}

module.exports = { ExpenseLog };
