#!/usr/bin/env node

/**
 * 🏦 银行流水财务分析工具
 * 分析公司银行流水，输出专业财务分析报告
 */

// 设置 UTF-8 编码
if (process.platform === 'win32') {
    process.stdout.setEncoding('utf8');
    process.stderr.setEncoding('utf8');
}

const fs = require('fs');
const path = require('path');

// 尝试加载 xlsx 模块
let xlsx;
try {
    xlsx = require('xlsx');
} catch (e) {
    console.log('请先安装 xlsx: npm install xlsx');
}

// 配置
const DEFAULT_THRESHOLD = 100000; // 大额交易阈值：10万元

/**
 * 读取银行流水文件
 * 支持 UTF-8 和 GBK 编码的 CSV 文件
 */
function readBankFlow(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    
    if (ext === '.csv') {
        // 尝试读取文件，先用 UTF-8
        let data = fs.readFileSync(filePath, 'utf8');
        
        // 如果读取的内容包含乱码特征（常见GBK字符在UTF-8中的表现）
        if (data.includes('\ufffd') || data.includes('���')) {
            console.log('检测到文件可能为 GBK 编码，尝试使用 GBK 解码...');
            try {
                const iconv = require('iconv-lite');
                const buffer = fs.readFileSync(filePath);
                data = iconv.decode(buffer, 'gbk');
                console.log('✅ GBK 解码成功');
            } catch (e) {
                console.log('⚠️ GBK 解码失败，使用 UTF-8');
            }
        }
        
        const lines = data.split('\n').filter(line => line.trim());
        const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
        
        return lines.slice(1).map(line => {
            const values = line.split(',').map(v => v.trim().replace(/"/g, ''));
            const row = {};
            headers.forEach((h, i) => row[h] = values[i] || '');
            return row;
        });
    } else if (ext === '.xlsx' && xlsx) {
        const workbook = xlsx.readFile(filePath);
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
        return xlsx.utils.sheet_to_json(sheet);
    } else {
        throw new Error('不支持的文件格式，请使用 CSV 或 Excel 文件');
    }
}

/**
 * 解析金额
 */
function parseAmount(value) {
    if (typeof value === 'number') return value;
    if (!value) return 0;
    // 移除货币符号和千分位
    const cleaned = value.replace(/[¥$,，]/g, '').trim();
    return parseFloat(cleaned) || 0;
}

/**
 * 分析银行流水
 */
function analyzeBankFlow(data, options = {}) {
    const threshold = options.threshold || DEFAULT_THRESHOLD;
    
    // 识别列名（支持多种命名）
    const dateCol = findColumn(data[0], ['日期', 'date', '交易日期', '记账日期', 'Time']);
    const amountCol = findColumn(data[0], ['金额', 'amount', '交易金额', '收入', '支出', 'Balance', '发生额']);
    const counterpartyCol = findColumn(data[0], ['对方账户', 'counterparty', '对方', '户名', '交易对方', 'Name']);
    const summaryCol = findColumn(data[0], ['摘要', 'summary', '用途', '说明', 'Description', '备注']);
    const companyCol = findColumn(data[0], ['公司', 'company', '公司名称', 'Account']);
    
    // 按公司分组
    const companies = {};
    data.forEach(row => {
        const company = companyCol ? (row[companyCol] || '未知') : '集团汇总';
        if (!companies[company]) {
            companies[company] = { rows: [], totalIncome: 0, totalExpense: 0 };
        }
        companies[company].rows.push(row);
    });
    
    const results = {
        companies: {},
        groupSummary: {
            totalIncome: 0,
            totalExpense: 0,
            netProfit: 0,
            transactionCount: 0,
            largeTransactions: [],
            incomeByType: {},
            expenseByType: {}
        }
    };
    
    // 分析每家公司
    for (const [company, companyData] of Object.entries(companies)) {
        const analysis = analyzeCompany(company, companyData.rows, {
            dateCol, amountCol, counterpartyCol, summaryCol, threshold
        });
        results.companies[company] = analysis;
        
        // 汇总到集团
        results.groupSummary.totalIncome += analysis.totalIncome;
        results.groupSummary.totalExpense += analysis.totalExpense;
        results.groupSummary.transactionCount += analysis.rowCount;
        results.groupSummary.largeTransactions.push(...analysis.largeTransactions);
    }
    
    results.groupSummary.netProfit = results.groupSummary.totalIncome - results.groupSummary.totalExpense;
    
    return results;
}

/**
 * 查找列名
 */
function findColumn(row, possibleNames) {
    for (const name of possibleNames) {
        if (row[name] !== undefined) return name;
        // 忽略大小写匹配
        for (const key of Object.keys(row)) {
            if (key.toLowerCase() === name.toLowerCase()) return key;
        }
    }
    return possibleNames[0]; // 返回第一个作为默认值
}

/**
 * 分析单家公司
 */
function analyzeCompany(company, rows, options) {
    const { dateCol, amountCol, counterpartyCol, summaryCol, threshold } = options;
    
    let totalIncome = 0;
    let totalExpense = 0;
    const largeTransactions = [];
    const incomeByType = {};
    const expenseByType = {};
    const monthlyData = {};
    const counterparties = {};
    
    rows.forEach(row => {
        const amount = parseAmount(row[amountCol]) || 0;
        
        // 确定是收入还是支出
        const isIncome = amount > 0;
        const absAmount = Math.abs(amount);
        
        if (isIncome) {
            totalIncome += absAmount;
            // 按摘要分类
            const category = categorizeTransaction(row[summaryCol] || '', 'income');
            incomeByType[category] = (incomeByType[category] || 0) + absAmount;
        } else {
            totalExpense += absAmount;
            const category = categorizeTransaction(row[summaryCol] || '', 'expense');
            expenseByType[category] = (expenseByType[category] || 0) + absAmount;
        }
        
        // 大额交易
        if (absAmount >= threshold) {
            largeTransactions.push({
                date: row[dateCol],
                amount: amount,
                counterparty: row[counterpartyCol],
                summary: row[summaryCol]
            });
        }
        
        // 交易对手统计
        const counterparty = row[counterpartyCol];
        if (counterparty) {
            counterparties[counterparty] = (counterparties[counterparty] || 0) + absAmount;
        }
        
        // 月度数据
        const date = row[dateCol];
        if (date) {
            const month = date.substring(0, 7); // YYYY-MM
            if (!monthlyData[month]) {
                monthlyData[month] = { income: 0, expense: 0 };
            }
            if (amount > 0) {
                monthlyData[month].income += amount;
            } else {
                monthlyData[month].expense += Math.abs(amount);
            }
        }
    });
    
    // 排序大额交易
    largeTransactions.sort((a, b) => Math.abs(b.amount) - Math.abs(a.amount));
    
    // 主要交易对手
    const topCounterparties = Object.entries(counterparties)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([name, amount]) => ({ name, amount }));
    
    return {
        company,
        rowCount: rows.length,  // 交易笔数
        totalIncome,
        totalExpense,
        netProfit: totalIncome - totalExpense,
        incomeByType,
        expenseByType,
        largeTransactions: largeTransactions.slice(0, 20), // 最多20笔
        topCounterparties,
        monthlyData
    };
}

/**
 * 交易分类
 */
function categorizeTransaction(summary, type) {
    if (!summary) return type === 'income' ? '其他收入' : '其他支出';
    
    const s = summary.toLowerCase();
    
    if (type === 'income') {
        if (s.includes('销售') || s.includes('货款') || s.includes('收入')) return '销售收入';
        if (s.includes('服务') || s.includes('咨询')) return '服务收入';
        if (s.includes('投资') || s.includes('分红')) return '投资收益';
        if (s.includes('退款') || s.includes('退回')) return '退款';
        return '其他收入';
    } else {
        if (s.includes('工资') || s.includes('薪酬') || s.includes('人员')) return '人工成本';
        if (s.includes('采购') || s.includes('进货') || s.includes('材料')) return '采购成本';
        if (s.includes('房租') || s.includes('租金') || s.includes('物业')) return '房租物业';
        if (s.includes('水电') || s.includes('能源') || s.includes('电费')) return '水电能耗';
        if (s.includes('交通') || s.includes('油费') || s.includes('差旅')) return '交通差旅';
        if (s.includes('广告') || s.includes('营销') || s.includes('推广') || s.includes('宣传')) return '营销推广';
        if (s.includes('办公') || s.includes('耗材') || s.includes('文具') || s.includes('设备') || s.includes('软件')) return '办公费用';
        if (s.includes('税') || s.includes('费')) return '税费';
        if (s.includes('还款') || s.includes('贷款') || s.includes('利息') || s.includes('融资')) return '融资还款';
        if (s.includes('投资') || s.includes('支出') || s.includes('支出')) return '投资支出';
        return '其他支出';
    }
}

/**
 * 生成报告 - 完整版（带数据、结论、说明）
 */
function generateReport(results) {
    let report = '# 🏦 银行流水财务分析报告\n\n';
    report += `> **分析时间：** ${new Date().toLocaleString('zh-CN')}\n\n`;
    
    const gs = results.groupSummary;
    // 从公司数据计算交易笔数（更可靠）
    const transactionCount = Object.values(results.companies).reduce((sum, c) => sum + (c.rowCount || 0), 0);
    const totalIncome = gs.totalIncome;
    const totalExpense = gs.totalExpense;
    const profitRate = totalIncome > 0 ? (gs.netProfit / totalIncome * 100) : 0;
    const expenseIncomeRatio = totalIncome > 0 ? (totalExpense / totalIncome * 100) : 0;
    
    // 合并所有公司月度数据
    const allMonths = {};
    for (const company of Object.values(results.companies)) {
        for (const [month, data] of Object.entries(company.monthlyData)) {
            if (!allMonths[month]) {
                allMonths[month] = { income: 0, expense: 0 };
            }
            allMonths[month].income += data.income;
            allMonths[month].expense += data.expense;
        }
    }
    const sortedMonths = Object.keys(allMonths).sort();
    
    // 收入类型统计
    const incomeTypes = {};
    for (const company of Object.values(results.companies)) {
        for (const [type, amount] of Object.entries(company.incomeByType)) {
            incomeTypes[type] = (incomeTypes[type] || 0) + amount;
        }
    }
    
    // 支出类型统计
    const expenseTypes = {};
    for (const company of Object.values(results.companies)) {
        for (const [type, amount] of Object.entries(company.expenseByType)) {
            expenseTypes[type] = (expenseTypes[type] || 0) + amount;
        }
    }
    
    // ==================== 集团总体分析 ====================
    report += '## 📊 一、集团总体分析\n\n';
    
    report += '### 1.1 核心财务指标\n\n';
    report += '| 指标名称 | 数值 | 说明 |\n';
    report += '|-----------|------|------|\n';
    report += `| 总收入 | ¥${formatNumber(gs.totalIncome)} | 期间内全部流入资金 |\n`;
    report += `| 总支出 | ¥${formatNumber(gs.totalExpense)} | 期间内全部流出资金 |\n`;
    report += `| 净利润 | ¥${formatNumber(gs.netProfit)} | 总收入 - 总支出 |\n`;
    report += `| 交易笔数 | ${transactionCount} 笔 | 全部交易记录数量 |\n`;
    report += `| 大额交易 | ${gs.largeTransactions.length} 笔 | ≥¥${formatNumber(DEFAULT_THRESHOLD)} |\n\n`;
    
    report += '**📝 结论：** ';
    if (gs.netProfit > 0) {
        report += `集团整体盈利 ¥${formatNumber(gs.netProfit)}，净利润率 ${profitRate.toFixed(1)}%，经营状况${profitRate > 20 ? '优秀' : '良好'}。\n\n`;
    } else {
        report += `集团整体亏损 ¥${formatNumber(Math.abs(gs.netProfit))}，需关注资金流向。\n\n`;
    }
    
    report += '**💡 说明：** 核心财务指标反映集团整体经营规模，净利润为正表示经营有盈余，可用于后续投资或储备。\n\n';
    
    // 资金流向趋势
    report += '### 1.2 资金流向趋势（月度）\n\n';
    report += '| 月份 | 收入(万) | 支出(万) | 净流入(万) | 状态 |\n';
    report += '|------|----------|----------|------------|------|\n';
    
    sortedMonths.forEach(month => {
        const m = allMonths[month];
        const net = m.income - m.expense;
        const status = net > 0 ? '✅ 净流入' : '❌ 净流出';
        report += `| ${month} | ¥${formatNumber(m.income)} | ¥${formatNumber(m.expense)} | ¥${formatNumber(net)} | ${status} |\n`;
    });
    report += '\n';
    
    report += '**📝 结论：** ';
    const positiveMonths = sortedMonths.filter(m => allMonths[m].income - allMonths[m].expense > 0).length;
    report += `近 ${sortedMonths.length} 个月中，有 ${positiveMonths} 个月实现净流入。${positiveMonths === sortedMonths.length ? '资金回流持续稳定。' : '存在资金流出月份，需关注。'}\n\n`;
    
    report += '**💡 说明：** 月度资金流反映集团资金周转情况，持续净流入说明经营健康；连续净流出需警惕资金链风险。\n\n';
    
    // ==================== 收入分析 ====================
    report += '## 💰 二、收入分析\n\n';
    
    report += '### 2.1 收入构成分析\n\n';
    report += '| 收入类型 | 金额(万) | 占比 | 趋势 |\n';
    report += '|----------|----------|------|------|\n';
    
    Object.entries(incomeTypes)
        .sort((a, b) => b[1] - a[1])
        .forEach(([type, amount]) => {
            const pct = ((amount / totalIncome) * 100).toFixed(1);
            const trend = pct > 50 ? '📈 主要来源' : pct > 20 ? '📊 重要组成' : '📉 补充收入';
            report += `| ${type} | ¥${formatNumber(amount)} | ${pct}% | ${trend} |\n`;
        });
    report += '\n';
    
    const topIncomeType = Object.entries(incomeTypes).sort((a, b) => b[1] - a[1])[0];
    report += '**📝 结论：** ';
    report += `集团收入以 **${topIncomeType[0]}** 为主，占总收入的 ${((topIncomeType[1]/totalIncome)*100).toFixed(1)}%，构成相对${Object.keys(incomeTypes).length > 3 ? '多元化' : '集中'}的收入结构。\n\n`;
    
    report += '**💡 说明：** 收入结构分析有助于评估经营风险。单一收入来源风险较高，建议关注多元化发展可能性。\n\n';
    
    // ==================== 支出分析 ====================
    report += '## 💸 三、支出分析\n\n';
    
    report += '### 3.1 支出构成分析\n\n';
    report += '| 支出类型 | 金额(万) | 占比 | 性质 |\n';
    report += '|----------|----------|------|------|\n';
    
    Object.entries(expenseTypes)
        .sort((a, b) => b[1] - a[1])
        .forEach(([type, amount]) => {
            const pct = ((amount / totalExpense) * 100).toFixed(1);
            const nature = type.includes('人工') || type.includes('采购') ? '🔴 刚性支出' : 
                          type.includes('营销') || type.includes('推广') ? '🟡 可调支出' : '⚪ 其他';
            report += `| ${type} | ¥${formatNumber(amount)} | ${pct}% | ${nature} |\n`;
        });
    report += '\n';
    
    report += '**📝 结论：** ';
    report += `支出主要集中在 **${Object.keys(expenseTypes).sort((a,b) => expenseTypes[b] - expenseTypes[a])[0]}**（占比 ${((Object.values(expenseTypes).sort((a,b) => b-a)[0]/totalExpense)*100).toFixed(1)}%），${expenseIncomeRatio < 80 ? '支出控制良好' : '支出占比较高，需注意成本控制'}。\n\n`;
    
    report += '**💡 说明：** 刚性支出（如人工、采购）难以压缩，可通过优化管理降低可变支出，提高利润率。\n\n';
    
    // ==================== 大额交易 ====================
    report += '## ⚠️ 四、重大款项往来\n\n';
    
    if (gs.largeTransactions.length > 0) {
        report += '### 4.1 大额交易明细\n\n';
        report += '| 序号 | 日期 | 交易对方 | 金额(万) | 类型 | 摘要 |\n';
        report += '|------|------|----------|----------|------|------|\n';
        
        gs.largeTransactions.slice(0, 15).forEach((t, idx) => {
            const amount = t.amount > 0 ? `+¥${formatNumber(t.amount)}` : `-¥${formatNumber(Math.abs(t.amount))}`;
            const type = t.amount > 0 ? '💰 收入' : '💸 支出';
            report += `| ${idx+1} | ${t.date || '-'} | ${t.counterparty || '-'} | ${amount} | ${type} | ${t.summary || '-'} |\n`;
        });
        report += '\n';
        
        const largeIncome = gs.largeTransactions.filter(t => t.amount > 0).reduce((sum, t) => sum + t.amount, 0);
        const largeExpense = gs.largeTransactions.filter(t => t.amount < 0).reduce((sum, t) => sum + Math.abs(t.amount), 0);
        
        report += '### 4.2 大额交易汇总\n\n';
        report += '| 类别 | 金额(万) | 占比 | 说明 |\n';
        report += '|------|----------|------|------|\n';
        report += `| 大额收入 | ¥${formatNumber(largeIncome)} | ${((largeIncome/totalIncome)*100).toFixed(1)}% | 来自大客户的收入 |\n`;
        report += `| 大额支出 | ¥${formatNumber(largeExpense)} | ${((largeExpense/totalExpense)*100).toFixed(1)}% | 主要支出项目 |\n\n`;
        
        report += '**📝 结论：** ';
        report += `共识别 ${gs.largeTransactions.length} 笔大额交易，大额收入占总收入 ${((largeIncome/totalIncome)*100).toFixed(1)}%，${largeIncome > largeExpense ? '资金净流入为主' : '资金净流出为主，需关注'}。\n\n`;
        
        report += '**💡 说明：** 大额交易需重点关注，确保交易真实合理，防范资金挪用风险。\n\n';
    } else {
        report += '未发现大额交易记录\n\n';
        report += '**📝 结论：** 流水金额较小，未触发大额交易预警。\n\n';
    }
    
    // ==================== 风险分析 ====================
    report += '## 🔍 五、风险分析\n\n';
    
    report += '### 5.1 财务健康度评估\n\n';
    report += '| 评估指标 | 数值 | 评分 | 状态 |\n';
    report += '|-----------|------|------|------|\n';
    report += `| 净利润率 | ${profitRate.toFixed(1)}% | ${profitRate > 20 ? '⭐⭐⭐⭐⭐' : profitRate > 10 ? '⭐⭐⭐⭐' : '⭐⭐⭐'} | ${profitRate > 20 ? '✅ 优秀' : profitRate > 10 ? '⚠️ 一般' : '❌ 偏低'} |\n`;
    report += `| 支出收入比 | ${expenseIncomeRatio.toFixed(1)}% | ${expenseIncomeRatio < 80 ? '⭐⭐⭐⭐⭐' : expenseIncomeRatio < 100 ? '⭐⭐⭐⭐' : '⭐⭐⭐'} | ${expenseIncomeRatio < 80 ? '✅ 健康' : expenseIncomeRatio < 100 ? '⚠️ 偏高' : '❌ 亏损风险'} |\n`;
    report += `| 资金回流 | ${positiveMonths}/${sortedMonths.length}月 | ${positiveMonths === sortedMonths.length ? '⭐⭐⭐⭐⭐' : positiveMonths >= sortedMonths*0.5 ? '⭐⭐⭐⭐' : '⭐⭐⭐'} | ${positiveMonths === sortedMonths.length ? '✅ 稳定' : positiveMonths >= sortedMonths*0.5 ? '⚠️ 波动' : '❌ 风险'} |\n`;
    report += `| 大额交易 | ${gs.largeTransactions.length}笔 | ${gs.largeTransactions.length < 5 ? '⭐⭐⭐⭐⭐' : gs.largeTransactions.length < 10 ? '⭐⭐⭐⭐' : '⭐⭐⭐'} | ${gs.largeTransactions.length < 10 ? '✅ 正常' : '⚠️ 关注'} |\n\n`;
    
    report += '### 5.2 风险预警清单\n\n';
    const risks = [];
    if (profitRate < 0) risks.push({ level: '🔴 高', text: '当前为亏损状态，需尽快开源节流' });
    if (expenseIncomeRatio > 100) risks.push({ level: '🔴 高', text: '支出超过收入，存在资金链断裂风险' });
    if (expenseIncomeRatio > 90) risks.push({ level: '🟡 中', text: '支出接近收入，需密切关注现金流' });
    if (gs.largeTransactions.length > 20) risks.push({ level: '🟡 中', text: '大额交易频繁，需核实交易真实性' });
    if (positiveMonths < sortedMonths * 0.5) risks.push({ level: '🟡 中', text: '资金回流不稳定，需关注资金周转' });
    
    if (risks.length === 0) {
        report += '| 状态 | 评估结果 |\n';
        report += '|------|----------|\n';
        report += '| ✅ 安全 | 未发现明显风险点，财务状况良好 |\n\n';
    } else {
        report += '| 风险等级 | 风险描述 | 建议措施 |\n';
        report += '|----------|----------|----------|\n';
        risks.forEach(r => {
            const measure = r.text.includes('亏损') ? '立即制定扭亏计划' :
                          r.text.includes('资金链') ? '暂停非必要支出' :
                          r.text.includes('现金流') ? '加强应收账款催收' :
                          r.text.includes('交易') ? '核查交易背景' : '持续监控';
            report += `| ${r.level} | ${r.text} | ${measure} |\n`;
        });
        report += '\n';
    }
    
    report += '**📝 结论：** ';
    if (risks.length === 0) {
        report += '集团财务状况整体健康，经营风险较低。\n\n';
    } else if (risks.filter(r => r.level === '🔴 高').length > 0) {
        report += `存在 ${risks.filter(r => r.level === '🔴 高').length} 项高风险预警，需立即关注处理。\n\n`;
    } else {
        report += `存在 ${risks.length} 项中低风险预警，建议持续关注。\n\n`;
    }
    
    report += '**💡 说明：** 风险评估综合考虑盈利性、流动性、安全性三个维度，建议定期监控关键指标变化。\n\n';
    
    // ==================== 各公司详情 ====================
    if (Object.keys(results.companies).length > 1) {
        report += '## 📋 六、各公司财务概况\n\n';
        
        for (const [company, data] of Object.entries(results.companies)) {
            const compProfit = data.totalIncome - data.totalExpense;
            const compProfitRate = data.totalIncome > 0 ? (compProfit / data.totalIncome * 100) : 0;
            
            report += `### ${company}\n\n`;
            report += '| 财务指标 | 数值 | 评估 |\n';
            report += '|-----------|------|------|\n';
            report += `| 交易笔数 | ${data.rowCount} 笔 | - |\n`;
            report += `| 收入 | ¥${formatNumber(data.totalIncome)} | ${data.totalIncome > 0 ? '✅' : '❌'} |\n`;
            report += `| 支出 | ¥${formatNumber(data.totalExpense)} | - |\n`;
            report += `| 净利润 | ¥${formatNumber(compProfit)} | ${compProfit >= 0 ? '✅ 盈利' : '❌ 亏损'} |\n`;
            report += `| 净利润率 | ${compProfitRate.toFixed(1)}% | ${compProfitRate > 15 ? '✅ 优秀' : compProfitRate > 0 ? '⚠️ 一般' : '❌ 为负'} |\n`;
            report += `| 大额交易 | ${data.largeTransactions.length} 笔 | ${data.largeTransactions.length < 5 ? '✅ 正常' : '⚠️ 关注'} |\n\n`;
            
            report += `**📝 结论：** ${company} ${compProfit >= 0 ? `盈利 ¥${formatNumber(compProfit)}` : `亏损 ¥${formatNumber(Math.abs(compProfit))}`}，${compProfitRate > 15 ? '经营状况优秀' : compProfitRate > 0 ? '经营状况一般' : '存在亏损'}。\n\n`;
        }
    }
    
    report += '---\n\n';
    report += '*报告由银行流水分析技能自动生成*\n';
    report += `*分析公司数：${Object.keys(results.companies).length} 家，交易记录：${transactionCount} 笔*\n`;
    
    return report;
}

/**
 * 格式化数字
 */
function formatNumber(num) {
    if (Math.abs(num) >= 10000) {
        return (num / 10000).toFixed(2) + '万';
    }
    return num.toFixed(2);
}

/**
 * 主函数
 */
async function main() {
    const args = process.argv.slice(2).join(' ');
    
    if (!args) {
        console.log(`
🏦 银行流水财务分析工具

使用方法:
  node bank-analysis/index.js <excel/csv文件路径> [选项]

选项:
  --threshold <金额>  大额交易阈值（默认10万元）

示例:
  node bank-analysis/index.js ./data/银行流水.xlsx
  node bank-analysis/index.js ./data/流水.csv --threshold 50000

支持格式: .xlsx, .csv
`);
        return;
    }
    
    // 解析参数
    const thresholdMatch = args.match(/--threshold\s+(\d+)/);
    const threshold = thresholdMatch ? parseInt(thresholdMatch[1]) : DEFAULT_THRESHOLD;
    
    // 查找文件路径
    const filePath = args.replace(/--threshold\s+\d+/, '').trim();
    const fullPath = path.isAbsolute(filePath) ? filePath : path.join(process.cwd(), filePath);
    
    if (!fs.existsSync(fullPath)) {
        console.error(`❌ 文件不存在: ${fullPath}`);
        return;
    }
    
    console.log('📖 读取银行流水数据...');
    const data = readBankFlow(fullPath);
    console.log(`✅ 读取成功，共 ${data.length} 条记录\n`);
    
    console.log('🔍 分析中...');
    const results = analyzeBankFlow(data, { threshold });
    
    console.log('📝 生成报告...');
    const report = generateReport(results);
    
    // 保存报告
    const reportPath = fullPath.replace(/\.(xlsx|csv)$/i, '_分析报告.md');
    fs.writeFileSync(reportPath, report, 'utf8');
    
    console.log(`\n✅ 报告已生成: ${reportPath}\n`);
    
    // 打印摘要
    console.log('📊 分析摘要:');
    console.log(`   总收入: ¥${formatNumber(results.groupSummary.totalIncome)}`);
    console.log(`   总支出: ¥${formatNumber(results.groupSummary.totalExpense)}`);
    console.log(`   净利润: ¥${formatNumber(results.groupSummary.netProfit)}`);
    console.log(`   大额交易: ${results.groupSummary.largeTransactions.length} 笔`);
}

// 运行
main().catch(console.error);