/**
 * Feishu CRM Lite - 飞书客户管理技能
 * 支持客户信息管理、跟进记录、自动提醒、销售漏斗等功能
 */

const fs = require('fs');
const path = require('path');

/**
 * 客户数据模型
 */
class Customer {
  constructor(data) {
    this.id = data.id || `cust_${Date.now()}`;
    this.companyName = data.companyName || '';
    this.contactName = data.contactName || '';
    this.phone = data.phone || '';
    this.email = data.email || '';
    this.source = data.source || ''; // 公众号/网站/推荐/广告等
    this.status = data.status || '新建'; // 新建/联系中/已成交/流失
    this.tags = data.tags || [];
    this.notes = data.notes || '';
    this.createdAt = data.createdAt || new Date().toISOString();
    this.updatedAt = new Date().toISOString();
    this.lastFollowUp = data.lastFollowUp || null;
    this.nextFollowUp = data.nextFollowUp || null;
    this.dealValue = data.dealValue || 0;
    this.dealDate = data.dealDate || null;
  }
}

/**
 * 跟进记录模型
 */
class FollowUp {
  constructor(data) {
    this.id = data.id || `follow_${Date.now()}`;
    this.customerId = data.customerId;
    this.method = data.method || '电话'; // 电话/微信/邮件/面谈
    this.content = data.content || '';
    this.outcome = data.outcome || ''; // 结果
    this.nextStep = data.nextStep || '';
    this.createdAt = data.createdAt || new Date().toISOString();
    this.createdBy = data.createdBy || 'system';
  }
}

/**
 * CRM 数据存储
 */
class CRMStore {
  constructor(dataPath) {
    this.dataPath = dataPath || path.join(process.cwd(), 'data', 'feishu-crm');
    this.customersFile = path.join(this.dataPath, 'customers.json');
    this.followUpsFile = path.join(this.dataPath, 'followups.json');
    this.remindersFile = path.join(this.dataPath, 'reminders.json');
    
    // 初始化数据存储
    this.init();
  }
  
  init() {
    if (!fs.existsSync(this.dataPath)) {
      fs.mkdirSync(this.dataPath, { recursive: true });
    }
    
    if (!fs.existsSync(this.customersFile)) {
      fs.writeFileSync(this.customersFile, JSON.stringify([], null, 2));
    }
    
    if (!fs.existsSync(this.followUpsFile)) {
      fs.writeFileSync(this.followUpsFile, JSON.stringify([], null, 2));
    }
    
    if (!fs.existsSync(this.remindersFile)) {
      fs.writeFileSync(this.remindersFile, JSON.stringify([], null, 2));
    }
  }
  
  // 客户管理
  addCustomer(customerData) {
    const customers = this.getCustomers();
    const customer = new Customer(customerData);
    customers.push(customer);
    this.saveCustomers(customers);
    return customer;
  }
  
  updateCustomer(id, updates) {
    const customers = this.getCustomers();
    const index = customers.findIndex(c => c.id === id);
    if (index === -1) return null;
    
    customers[index] = { ...customers[index], ...updates, updatedAt: new Date().toISOString() };
    this.saveCustomers(customers);
    return customers[index];
  }
  
  deleteCustomer(id) {
    const customers = this.getCustomers();
    const filtered = customers.filter(c => c.id !== id);
    if (filtered.length === customers.length) return false;
    
    this.saveCustomers(filtered);
    return true;
  }
  
  getCustomer(id) {
    const customers = this.getCustomers();
    return customers.find(c => c.id === id);
  }
  
  getCustomers(filters = {}) {
    const data = fs.readFileSync(this.customersFile, 'utf8');
    let customers = JSON.parse(data);
    
    if (filters.status) {
      customers = customers.filter(c => c.status === filters.status);
    }
    
    if (filters.tag) {
      customers = customers.filter(c => c.tags.includes(filters.tag));
    }
    
    if (filters.source) {
      customers = customers.filter(c => c.source === filters.source);
    }
    
    return customers;
  }
  
  saveCustomers(customers) {
    fs.writeFileSync(this.customersFile, JSON.stringify(customers, null, 2));
  }
  
  // 跟进记录
  addFollowUp(followUpData) {
    const followUps = this.getFollowUps();
    const followUp = new FollowUp(followUpData);
    followUps.push(followUp);
    this.saveFollowUps(followUps);
    
    // 更新客户最后跟进时间
    if (followUpData.customerId) {
      this.updateCustomer(followUpData.customerId, {
        lastFollowUp: new Date().toISOString(),
        nextFollowUp: followUpData.nextStep ? new Date(followUpData.nextStep).toISOString() : null
      });
    }
    
    return followUp;
  }
  
  getFollowUps(customerId = null) {
    const data = fs.readFileSync(this.followUpsFile, 'utf8');
    let followUps = JSON.parse(data);
    
    if (customerId) {
      followUps = followUps.filter(f => f.customerId === customerId);
    }
    
    return followUps;
  }
  
  saveFollowUps(followUps) {
    fs.writeFileSync(this.followUpsFile, JSON.stringify(followUps, null, 2));
  }
  
  // 提醒管理
  addReminder(reminderData) {
    const reminders = this.getReminders();
    reminders.push({
      id: `rem_${Date.now()}`,
      ...reminderData,
      createdAt: new Date().toISOString(),
      completed: false
    });
    this.saveReminders(reminders);
    return reminders[reminders.length - 1];
  }
  
  getReminders(filters = {}) {
    const data = fs.readFileSync(this.remindersFile, 'utf8');
    let reminders = JSON.parse(data);
    
    if (filters.completed !== undefined) {
      reminders = reminders.filter(r => r.completed === filters.completed);
    }
    
    if (filters.dueDate) {
      const dueDate = new Date(filters.dueDate);
      reminders = reminders.filter(r => new Date(r.dueTime) <= dueDate);
    }
    
    return reminders;
  }
  
  completeReminder(id) {
    const reminders = this.getReminders();
    const reminder = reminders.find(r => r.id === id);
    if (!reminder) return null;
    
    reminder.completed = true;
    reminder.completedAt = new Date().toISOString();
    this.saveReminders(reminders);
    return reminder;
  }
  
  saveReminders(reminders) {
    fs.writeFileSync(this.remindersFile, JSON.stringify(reminders, null, 2));
  }
  
  // 销售漏斗统计
  getFunnelStats() {
    const customers = this.getCustomers();
    const stats = {
      total: customers.length,
      byStatus: {},
      totalDealValue: 0,
      conversionRate: 0
    };
    
    customers.forEach(c => {
      stats.byStatus[c.status] = (stats.byStatus[c.status] || 0) + 1;
      if (c.status === '已成交') {
        stats.totalDealValue += c.dealValue || 0;
      }
    });
    
    if (stats.total > 0) {
      stats.conversionRate = ((stats.byStatus['已成交'] || 0) / stats.total * 100).toFixed(2) + '%';
    }
    
    return stats;
  }
  
  // 生成报表
  generateReport(period = 'month') {
    const customers = this.getCustomers();
    const followUps = this.getFollowUps();
    const now = new Date();
    
    let startDate;
    if (period === 'week') {
      startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    } else if (period === 'month') {
      startDate = new Date(now.getFullYear(), now.getMonth(), 1);
    } else {
      startDate = new Date(now.getFullYear(), 0, 1);
    }
    
    const newCustomers = customers.filter(c => new Date(c.createdAt) >= startDate);
    const dealCustomers = customers.filter(c => c.status === '已成交' && c.dealDate && new Date(c.dealDate) >= startDate);
    
    return {
      period,
      startDate: startDate.toISOString(),
      endDate: now.toISOString(),
      newCustomers: newCustomers.length,
      dealCustomers: dealCustomers.length,
      totalDealValue: dealCustomers.reduce((sum, c) => sum + (c.dealValue || 0), 0),
      totalFollowUps: followUps.filter(f => new Date(f.createdAt) >= startDate).length,
      funnelStats: this.getFunnelStats()
    };
  }
}

// 导出
module.exports = {
  Customer,
  FollowUp,
  CRMStore
};

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const crm = new CRMStore();
  
  if (command === 'add-customer' && args[1]) {
    const customer = crm.addCustomer({
      companyName: args[1],
      contactName: args[2] || '',
      phone: args[3] || '',
      email: args[4] || '',
      source: args[5] || '未知'
    });
    console.log('客户已添加:', JSON.stringify(customer, null, 2));
  } else if (command === 'list-customers') {
    const customers = crm.getCustomers();
    console.log('客户列表:');
    customers.forEach(c => {
      console.log(`  - ${c.companyName} (${c.contactName}) - ${c.status}`);
    });
  } else if (command === 'stats') {
    const stats = crm.getFunnelStats();
    console.log('销售漏斗统计:');
    console.log(JSON.stringify(stats, null, 2));
  } else if (command === 'report') {
    const report = crm.generateReport(args[1] || 'month');
    console.log('销售报表:');
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log('用法:');
    console.log('  node index.js add-customer <公司名> [联系人] [电话] [邮箱] [来源]');
    console.log('  node index.js list-customers');
    console.log('  node index.js stats');
    console.log('  node index.js report [week|month|year]');
  }
}
