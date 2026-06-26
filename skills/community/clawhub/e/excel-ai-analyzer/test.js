/**
 * Excel AI Analyzer 测试脚本
 */

const analyzer = require('./index.js');
const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

// 创建测试 Excel 文件
function createTestFile() {
  const testData = [
    { name: '张三', age: 25, sales: 5000, date: '2024-01-01' },
    { name: '李四', age: 30, sales: 8000, date: '2024-01-02' },
    { name: '王五', age: 28, sales: 6500, date: '2024-01-03' },
    { name: '赵六', age: 35, sales: 12000, date: '2024-01-04' },
    { name: '钱七', age: 22, sales: 3000, date: '2024-01-05' },
    { name: '孙八', age: 40, sales: 15000, date: '2024-01-06' },
    { name: '周九', age: 32, sales: 7500, date: '2024-01-07' },
    { name: '吴十', age: 27, sales: 50000, date: '2024-01-08' }, // 异常值
  ];

  const ws = XLSX.utils.json_to_sheet(testData);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
  
  const testPath = path.join(__dirname, 'test-data.xlsx');
  XLSX.writeFile(wb, testPath);
  
  return testPath;
}

// 运行测试
async function runTest() {
  console.log('🧪 Excel AI Analyzer 测试开始...\n');

  try {
    // 1. 创建测试文件
    console.log('1️⃣ 创建测试 Excel 文件...');
    const testFile = createTestFile();
    console.log(`✅ 测试文件已创建：${testFile}\n`);

    // 2. 执行分析
    console.log('2️⃣ 执行数据分析...');
    const result = await analyzer.execute({ filePath: testFile });
    
    if (result.success) {
      console.log('✅ 分析成功!\n');
      
      // 3. 显示结果摘要
      console.log('📊 数据概览:');
      console.log(`   - 行数：${result.data.rowCount}`);
      console.log(`   - 列数：${result.data.columns.length}`);
      console.log(`   - 列名：${result.data.columns.join(', ')}\n`);

      console.log('📈 统计分析:');
      Object.entries(result.analysis.statistics).forEach(([col, stats]) => {
        if (stats.type === 'numeric') {
          console.log(`   ${col}: 平均=${stats.average}, 范围=[${stats.min}, ${stats.max}]`);
        }
      });
      console.log('');

      if (result.analysis.anomalies.length > 0) {
        console.log('🚨 异常检测:');
        console.log(`   发现 ${result.analysis.anomalies.length} 个异常值`);
        result.analysis.anomalies.forEach(a => {
          console.log(`   - 行${a.row} 列${a.column}: ${a.value} (${a.deviation}σ)`);
        });
        console.log('');
      }

      console.log('💡 数据洞察:');
      result.analysis.insights.forEach(insight => {
        console.log(`   ${insight}`);
      });
      console.log('');

      // 4. 保存报告
      const reportPath = path.join(__dirname, 'test-report.md');
      fs.writeFileSync(reportPath, result.report);
      console.log(`📝 报告已保存：${reportPath}\n`);

      console.log('✅ 所有测试通过!\n');
    } else {
      console.error('❌ 分析失败:', result.error);
    }

  } catch (error) {
    console.error('❌ 测试出错:', error.message);
  } finally {
    // 清理测试文件
    const testFile = path.join(__dirname, 'test-data.xlsx');
    if (fs.existsSync(testFile)) {
      fs.unlinkSync(testFile);
    }
  }
}

runTest();
