#!/usr/bin/env node
/**
 * 简易记账助手
 * 
 * 功能：
 * 1. 记录开销
 * 2. 查看账单
 * 3. 分类统计
 * 4. 月度统计
 * 5. 导出报表
 */

const fs = require('fs');
const path = require('path');

// 数据文件路径
const DATA_DIR = path.join(__dirname, 'data');
const DATA_FILE = path.join(DATA_DIR, 'expenses.json');

// 默认分类
const DEFAULT_CATEGORIES = [
  '餐饮', '交通', '购物', '娱乐', '医疗', '住房', '通讯', '教育', '其他'
];

// 初始化数据
function initData() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  
  if (!fs.existsSync(DATA_FILE)) {
    const initialData = {
      expenses: [],
      categories: DEFAULT_CATEGORIES,
      lastUpdate: new Date().toISOString()
    };
    fs.writeFileSync(DATA_FILE, JSON.stringify(initialData, null, 2));
    console.log('💰 记账系统已初始化');
  }
}

// 加载数据
function loadData() {
  try {
    const data = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('❌ 数据加载失败:', error.message);
    return null;
  }
}

// 保存数据
function saveData(data) {
  try {
    data.lastUpdate = new Date().toISOString();
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
    return true;
  } catch (error) {
    console.error('❌ 数据保存失败:', error.message);
    return false;
  }
}

// 添加开销记录
function addExpense(description, amount, category, notes = '') {
  const data = loadData();
  if (!data) return false;
  
  const expense = {
    id: Date.now(),
    description,
    amount: parseFloat(amount),
    category,
    notes,
    date: new Date().toISOString()
  };
  
  data.expenses.push(expense);
  
  if (saveData(data)) {
    console.log(`✅ 记录成功: ${description} - ¥${amount} (${category})`);
    return true;
  }
  return false;
}

// 查看最近记录
function viewRecentExpenses(limit = 10) {
  const data = loadData();
  if (!data) return;
  
  const expenses = data.expenses.slice(-limit).reverse();
  
  if (expenses.length === 0) {
    console.log('📝 暂无记录');
    return;
  }
  
  console.log('📋 最近记录:');
  console.log('='.repeat(60));
  expenses.forEach(expense => {
    const date = new Date(expense.date).toLocaleDateString('zh-CN');
    console.log(`🆔 ${expense.id}`);
    console.log(`📝 ${expense.description}`);
    console.log(`💰 ¥${expense.amount.toFixed(2)}`);
    console.log(`🏷️  ${expense.category}`);
    console.log(`📅 ${date}`);
    if (expense.notes) {
      console.log(`📝 ${expense.notes}`);
    }
    console.log('-'.repeat(40));
  });
  
  // 显示统计
  const total = expenses.reduce((sum, exp) => sum + exp.amount, 0);
  console.log(`📊 总计: ¥${total.toFixed(2)} (${expenses.length} 条记录)`);
}

// 分类统计
function categoryStatistics() {
  const data = loadData();
  if (!data) return;
  
  if (data.expenses.length === 0) {
    console.log('📊 暂无统计信息');
    return;
  }
  
  // 按分类汇总
  const stats = {};
  data.expenses.forEach(expense => {
    if (!stats[expense.category]) {
      stats[expense.category] = { total: 0, count: 0 };
    }
    stats[expense.category].total += expense.amount;
    stats[expense.category].count++;
  });
  
  console.log('📊 分类统计:');
  console.log('='.repeat(60));
  
  // 排序并显示
  const sortedCategories = Object.entries(stats)
    .sort(([, a], [, b]) => b.total - a.total);
  
  sortedCategories.forEach(([category, stat]) => {
    const percentage = (stat.total / data.expenses.reduce((sum, exp) => sum + exp.amount, 0) * 100).toFixed(1);
    console.log(`${category.padEnd(8)}: ¥${stat.total.toFixed(2).padStart(8)} (${stat.count} 次, ${percentage}%)`);
  });
  
  console.log('='.repeat(60));
  const grandTotal = data.expenses.reduce((sum, exp) => sum + exp.amount, 0);
  console.log(`总计: ¥${grandTotal.toFixed(2)} (${data.expenses.length} 条记录)`);
}

// 月度统计
function monthlyStatistics(monthYear = '') {
  const data = loadData();
  if (!data) return;
  
  let targetMonth = monthYear;
  if (!targetMonth) {
    const now = new Date();
    targetMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  }
  
  const expenses = data.expenses.filter(expense => {
    const expenseDate = new Date(expense.date);
    const expenseMonth = `${expenseDate.getFullYear()}-${String(expenseDate.getMonth() + 1).padStart(2, '0')}`;
    return expenseMonth === targetMonth;
  });
  
  if (expenses.length === 0) {
    console.log(`📅 ${targetMonth} 月暂无记录`);
    return;
  }
  
  console.log(`📅 ${targetMonth} 月统计:`);
  console.log('='.repeat(60));
  
  // 按分类汇总
  const monthlyStats = {};
  expenses.forEach(expense => {
    if (!monthlyStats[expense.category]) {
      monthlyStats[expense.category] = { total: 0, count: 0 };
    }
    monthlyStats[expense.category].total += expense.amount;
    monthlyStats[expense.category].count++;
  });
  
  // 排序并显示
  const sortedStats = Object.entries(monthlyStats)
    .sort(([, a], [, b]) => b.total - a.total);
  
  sortedStats.forEach(([category, stat]) => {
    console.log(`${category.padEnd(8)}: ¥${stat.total.toFixed(2).padStart(8)} (${stat.count} 次)`);
  });
  
  console.log('='.repeat(60));
  const monthlyTotal = expenses.reduce((sum, exp) => sum + exp.amount, 0);
  console.log(`月总计: ¥${monthlyTotal.toFixed(2)} (${expenses.length} 条记录)`);
  
  // 显示平均每日开销
  const daysInMonth = new Date(
    parseInt(targetMonth.split('-')[0]),
    parseInt(targetMonth.split('-')[1]),
    0
  ).getDate();
  const dailyAverage = monthlyTotal / daysInMonth;
  console.log(`日均开销: ¥${dailyAverage.toFixed(2)}`);
}

// 导出报表
function exportReport() {
  const data = loadData();
  if (!data) return;
  
  const report = {
    summary: {
      totalRecords: data.expenses.length,
      totalAmount: data.expenses.reduce((sum, exp) => sum + exp.amount, 0),
      lastUpdate: data.lastUpdate
    },
    categories: DEFAULT_CATEGORIES,
    expenses: data.expenses
  };
  
  const reportFile = path.join(DATA_DIR, `report_${new Date().toISOString().split('T')[0]}.json`);
  fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
  
  console.log(`📤 报表已导出: ${reportFile}`);
  console.log(`📊 统计信息:`);
  console.log(`   记录总数: ${report.summary.totalRecords}`);
  console.log(`   总金额: ¥${report.summary.totalAmount.toFixed(2)}`);
  console.log(`   最后更新: ${new Date(report.summary.lastUpdate).toLocaleString('zh-CN')}`);
}

// 显示帮助
function showHelp() {
  console.log('💰 简易记账助手 - 使用说明');
  console.log('='.repeat(60));
  console.log('命令:');
  console.log('  记账 <描述> <金额> <分类> [备注] - 添加开销记录');
  console.log('  查看账单 [数量]                  - 查看最近记录');
  console.log('  分类统计                         - 按分类统计开销');
  console.log('  月度统计 [年月]                  - 查看月度统计');
  console.log('  导出报表                         - 导出详细报表');
  console.log('  帮助                             - 显示此帮助');
  console.log('');
  console.log('示例:');
  console.log('  记账 午餐 25 餐饮');
  console.log('  记账 交通费 12 交通 "上班打车"');
  console.log('  查看账单 20');
  console.log('  月度统计 2026-03');
  console.log('  分类统计');
  console.log('  导出报表');
  console.log('');
  console.log('可用分类:', DEFAULT_CATEGORIES.join(', '));
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    showHelp();
    return;
  }
  
  initData();
  
  const command = args[0];
  
  switch (command) {
    case '记账':
    case '记一笔':
      if (args.length < 4) {
        console.log('❌ 用法: 记账 <描述> <金额> <分类> [备注]');
        return;
      }
      addExpense(args[1], args[2], args[3], args.slice(4).join(' '));
      break;
      
    case '查看账单':
      const limit = args[1] ? parseInt(args[1]) : 10;
      viewRecentExpenses(limit);
      break;
      
    case '分类统计':
      categoryStatistics();
      break;
      
    case '月度统计':
      monthlyStatistics(args[1]);
      break;
      
    case '导出报表':
      exportReport();
      break;
      
    case '帮助':
    case 'help':
      showHelp();
      break;
      
    default:
      console.log('❌ 未知命令，请输入"帮助"查看使用说明');
  }
}

// 运行主函数
if (require.main === module) {
  main();
}

module.exports = {
  addExpense,
  viewRecentExpenses,
  categoryStatistics,
  monthlyStatistics,
  exportReport
};