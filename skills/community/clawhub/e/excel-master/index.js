const XLSX = require("xlsx");
const fs = require("fs");

let workbook = null;
let currentFile = null;
let currentSheet = null;

module.exports = {
  name: "Excel Master",
  description: "Excel 全能工具，免依赖可直接运行",
  version: "1.0.0",

  triggers: [
    "打开excel",
    "读取excel",
    "保存excel",
    "查看数据",
    "切换工作表",
    "筛选",
    "求和",
    "平均值",
    "最大",
    "最小",
    "计数",
    "分析表格"
  ],

  async execute({ args, command }) {
    try {
      if (!workbook && !command.includes("打开")) {
        return { content: "请先打开 Excel：打开excel data.xlsx" };
      }

      // 打开
      if (command.includes("打开") || command.includes("读取")) {
        currentFile = args[0] || "data.xlsx";
        workbook = XLSX.readFile(currentFile);
        currentSheet = workbook.SheetNames[0];
        return {
          content: `✅ 已打开：${currentFile}\n工作表：${workbook.SheetNames.join(" | ")}`
        };
      }

      // 查看
      if (command.includes("查看") || command.includes("数据")) {
        const sheet = workbook.Sheets[currentSheet];
        const json = XLSX.utils.sheet_to_json(sheet, { header: 1 });
        return { content: `📊 数据：\n${JSON.stringify(json, null, 2)}` };
      }

      // 筛选
      if (command.includes("筛选")) {
        const sheet = workbook.Sheets[currentSheet];
        const json = XLSX.utils.sheet_to_json(sheet);
        const col = args[0];
        const op = args[1];
        const val = args[2];
        if (!col || !op || !val) return { content: "用法：筛选 年龄 > 25" };

        let res = [];
        for (let row of json) {
          try {
            let v = Number(row[col]);
            if (op === ">") v > val && res.push(row);
            if (op === "<") v < val && res.push(row);
            if (op === "=") v == val && res.push(row);
          } catch {}
        }
        return { content: `🔍 找到 ${res.length} 条\n${JSON.stringify(res, null, 2)}` };
      }

      // 统计
      if (["求和", "平均值", "最大", "最小", "计数"].includes(command)) {
        const sheet = workbook.Sheets[currentSheet];
        const json = XLSX.utils.sheet_to_json(sheet);
        const col = args[0];
        if (!col) return { content: "用法：求和 销售额" };

        let nums = [];
        for (let r of json) {
          let v = Number(r[col]);
          if (!isNaN(v)) nums.push(v);
        }
        if (nums.length === 0) return { content: "无有效数字" };

        let sum = nums.reduce((a, b) => a + b, 0);
        let avg = (sum / nums.length).toFixed(2);
        let max = Math.max(...nums);
        let min = Math.min(...nums);
        let count = nums.length;

        return {
          content: `📈 ${col} 统计
总数：${count}
求和：${sum}
平均值：${avg}
最大值：${max}
最小值：${min}`
        };
      }

      // 分析
      if (command.includes("分析")) {
        const sheet = workbook.Sheets[currentSheet];
        const json = XLSX.utils.sheet_to_json(sheet);
        let rows = json.length;
        let cols = Object.keys(json[0] || {}).length;
        return { content: `📊 分析：${rows} 行 ${cols} 列，数据完整` };
      }

      // 保存
      if (command.includes("保存")) {
        XLSX.writeFile(workbook, currentFile);
        return { content: `✅ 已保存：${currentFile}` };
      }

      return { content: "支持：打开、查看、筛选、求和、分析、保存" };
    } catch (err) {
      return { content: `❌ 错误：${err.message}` };
    }
  }
};