/**
 * ClientTracker — Freelancer CRM
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');
const path = require('path');

class ClientTracker {
  constructor(options = {}) {
    this.dataDir = options.dataDir || './clients';
    this.dbFile = path.join(this.dataDir, 'clients.json');
    if (!fs.existsSync(this.dataDir)) fs.mkdirSync(this.dataDir, { recursive: true });
    this.clients = this._load();
  }

  addClient(name, email, company, notes) {
    const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 5);
    const client = { id, name, email, company, notes, projects: [], invoices: [], pipeline: 'lead', created: new Date().toISOString() };
    this.clients.push(client);
    this._save();
    return client;
  }

  addProject(clientId, project) {
    const client = this.clients.find(c => c.id === clientId || c.name.toLowerCase() === clientId.toLowerCase());
    if (!client) return null;
    const proj = { id: Date.now().toString(36) + Math.random().toString(36).slice(2, 5), name: project.name, budget: project.budget || 0, status: 'active', deadline: project.deadline, started: new Date().toISOString() };
    client.projects.push(proj);
    client.pipeline = 'active';
    this._save();
    return proj;
  }

  addInvoice(clientId, amount, description) {
    const client = this.clients.find(c => c.id === clientId || c.name.toLowerCase() === clientId.toLowerCase());
    if (!client) return null;
    const inv = { id: 'INV-' + Date.now().toString(36).toUpperCase(), amount, description, status: 'sent', date: new Date().toISOString().split('T')[0] };
    client.invoices.push(inv);
    this._save();
    return inv;
  }

  markPaid(clientId, invoiceId) {
    const client = this.clients.find(c => c.id === clientId || c.name.toLowerCase() === clientId.toLowerCase());
    if (!client) return null;
    const inv = client.invoices.find(i => i.id === invoiceId);
    if (inv) { inv.status = 'paid'; inv.paidDate = new Date().toISOString().split('T')[0]; }
    this._save();
    return inv;
  }

  pipeline() {
    const stages = { lead: [], proposal: [], negotiating: [], active: [], completed: [], followup: [] };
    for (const c of this.clients) {
      const stage = c.pipeline || 'lead';
      if (!stages[stage]) stages[stage] = [];
      stages[stage].push({ name: c.name, company: c.company });
    }
    return stages;
  }

  revenue(month) {
    const m = month || new Date().toISOString().slice(0, 7);
    let paid = 0, outstanding = 0;
    for (const c of this.clients) {
      for (const inv of c.invoices) {
        if (inv.date.startsWith(m)) {
          if (inv.status === 'paid') paid += inv.amount;
          else outstanding += inv.amount;
        }
      }
    }
    return { month: m, paid, outstanding, total: paid + outstanding };
  }

  search(query) {
    const q = query.toLowerCase();
    return this.clients.filter(c => c.name.toLowerCase().includes(q) || (c.company || '').toLowerCase().includes(q) || (c.email || '').toLowerCase().includes(q));
  }

  _load() { try { return JSON.parse(fs.readFileSync(this.dbFile, 'utf8')); } catch { return []; } }
  _save() { fs.writeFileSync(this.dbFile, JSON.stringify(this.clients, null, 2)); }
}

module.exports = { ClientTracker };
