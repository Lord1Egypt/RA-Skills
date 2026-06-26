/**
 * BOM物料清单对比工具
 */

const fs = require('fs');

/**
 * 解析BOM文件（支持CSV/XLSX）
 */
function parseBOM(filePath) {
  const xlsx = require('xlsx');
  const ext = filePath.split('.').pop().toLowerCase();
  
  let rows;
  if (ext === 'csv') {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split(/\r?\n/).filter(l => l.trim());
    rows = lines.map(line => line.split(',').map(c => c.trim().replace(/^"|"$/g, '')));
    rows = rows.slice(1).map(r => ({ partNo: r[0], name: r[1], qty: parseFloat(r[2]) || 0, spec: r[3] || '', unit: r[4] || '', price: parseFloat(r[5]) || 0 }));
  } else {
    const wb = xlsx.readFile(filePath);
    const sheet = wb.Sheets[wb.SheetNames[0]];
    rows = xlsx.utils.sheet_to_json(sheet, { defval: '' });
  }
  
  // 构建以物料编号为key的索引
  const index = {};
  rows.forEach(row => {
    const key = row.partNo || row['物料编号'] || row['件号'] || '';
    if (key) {
      index[key] = row;
    }
  });
  
  return { rows, index };
}

/**
 * 对比两个BOM
 */
function compareBOM(oldBOM, newBOM, options = {}) {
  const {
    ignoreFields = ['qty', 'price'], // 不比较的字段
    keyField = 'partNo'
  } = options;
  
  const oldData = parseBOM(oldBOM);
  const newData = parseBOM(newBOM);
  
  const added = [];
  const removed = [];
  const changed = [];
  
  // 找新增和变更
  for (const [key, newRow] of Object.entries(newData.index)) {
    if (!oldData.index[key]) {
      added.push(newRow);
    } else {
      const oldRow = oldData.index[key];
      const changes = {};
      for (const [field, newVal] of Object.entries(newRow)) {
        if (ignoreFields.includes(field)) continue;
        const oldVal = oldRow[field];
        if (String(newVal) !== String(oldVal)) {
          changes[field] = { old: oldVal, new: newVal };
        }
      }
      // 数量变更
      const qtyField = keyField === 'partNo' ? 'qty' : '数量';
      const oldQty = parseFloat(oldRow[qtyField] || oldRow['qty'] || 0);
      const newQty = parseFloat(newRow[qtyField] || newRow['qty'] || 0);
      if (oldQty !== newQty) {
        changes[qtyField] = { old: oldQty, new: newQty, pct: ((newQty - oldQty) / oldQty * 100).toFixed(1) + '%' };
      }
      
      if (Object.keys(changes).length > 0) {
        changed.push({ key, oldRow, newRow, changes });
      }
    }
  }
  
  // 找删除
  for (const [key, oldRow] of Object.entries(oldData.index)) {
    if (!newData.index[key]) {
      removed.push(oldRow);
    }
  }
  
  return { added, removed, changed };
}

/**
 * 生成对比报告
 */
function generateCompareReport(oldFile, newFile, result) {
  const { added, removed, changed } = result;
  
  let totalOld = Object.keys(parseBOM(oldFile).index).length;
  let totalNew = Object.keys(parseBOM(newFile).index).length;
  
  let report = `BOM对比报告\n`;
  report += `${'━'.repeat(50)}\n`;
  report += `旧版：${oldFile}\n`;
  report += `新版：${newFile}\n`;
  report += `${'━'.repeat(50)}\n\n`;
  
  if (added.length > 0) {
    report += `🆕 新增物料（${added.length}项）：\n`;
    added.forEach(item => {
      report += `  ✅ ${item.partNo || item['物料编号']} - ${item.name || item['名称']}\n`;
    });
    report += '\n';
  }
  
  if (removed.length > 0) {
    report += `❌ 删除物料（${removed.length}项）：\n`;
    removed.forEach(item => {
      report += `  ➖ ${item.partNo || item['物料编号']} - ${item.name || item['名称']}\n`;
    });
    report += '\n';
  }
  
  if (changed.length > 0) {
    report += `📝 变更物料（${changed.length}项）：\n`;
    changed.forEach(({ key, changes }) => {
      report += `  ⚠️ ${key}:\n`;
      for (const [field, { old: oldVal, new: newVal, pct }] of Object.entries(changes)) {
        if (pct) {
          report += `     ${field}: ${oldVal} → ${newVal} (${pct})\n`;
        } else {
          report += `     ${field}: ${oldVal} → ${newVal}\n`;
        }
      }
    });
    report += '\n';
  }
  
  if (added.length === 0 && removed.length === 0 && changed.length === 0) {
    report += `✅ 两个BOM版本完全一致，无差异\n\n`;
  }
  
  report += `${'━'.repeat(50)}\n`;
  report += `物料项统计：旧版${totalOld}项 → 新版${totalNew}项（${totalNew > totalOld ? '+' : ''}${totalNew - totalOld}项）\n`;
  
  return report;
}

// CLI
const args = process.argv.slice(2);
if (args.length >= 2) {
  const result = compareBOM(args[0], args[1]);
  console.log(generateCompareReport(args[0], args[1], result));
} else {
  console.log('用法: node compare.js old_bom.xlsx new_bom.xlsx');
}

module.exports = { compareBOM, generateCompareReport };
