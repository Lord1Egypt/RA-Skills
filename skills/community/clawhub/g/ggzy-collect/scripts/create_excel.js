/**
 * ggzy_collect - 创建Excel文件的脚本
 * 用法: node create_excel.js <输出路径>
 * 示例: node create_excel.js D:\\ggzyjy.zb\\2026-03-20_to_2026-03-23.xlsx
 */

const XLSX = require('xlsx');
const fs = require('fs');
const path = process.argv[2] || 'output.xlsx';

// 项目数据数组
const projects = [
  ['项目地点', '项目名称', '发布时间'],
  // 在这里添加从网页抓取的项目数据
  // ['市本级', 'XXX项目', '2026-03-20'],
];

// 创建工作簿
const workbook = XLSX.utils.book_new();
const worksheet = XLSX.utils.aoa_to_sheet(projects);

// 设置列宽
worksheet['!cols'] = [
  { wch: 15 }, // 项目地点
  { wch: 60 }, // 项目名称
  { wch: 15 }, // 发布时间
];

XLSX.utils.book_append_sheet(workbook, worksheet, '项目列表');

// 确保目录存在
const dir = path.substring(0, path.lastIndexOf('\\'));
if (!fs.existsSync(dir)) {
  fs.mkdirSync(dir, { recursive: true });
}

// 写入文件
XLSX.writeFile(workbook, path);
console.log(`Excel文件已创建: ${path}`);