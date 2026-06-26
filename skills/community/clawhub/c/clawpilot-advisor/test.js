#!/usr/bin/env node
/**
 * Clawpilot Test Suite
 * 运行：node test.js
 * 
 * 自测模式（无参数）：使用内置测试用例
 * 指定查询：node test.js "你的问题"
 */

const { spawn } = require("child_process");
const path = require("path");

const HANDLER = path.join(__dirname, "handler.py");

function runPy(query, installed = []) {
  return new Promise((resolve) => {
    const args = [HANDLER, query];
    if (installed.length > 0) {
      args.push("--installed", installed.join(","));
    }
    const proc = spawn("python3", args);
    let stdout = "";
    let stderr = "";
    proc.stdout.on("data", (d) => (stdout += d.toString()));
    proc.stderr.on("data", (d) => (stderr += d.toString()));
    proc.on("close", (code) => {
      resolve({ query, installed, stdout, stderr, code });
    });
  });
}

const TESTS = [
  // --- 低风险：快递 ---
  {
    name: "[低风险] 查快递 - 识别意图",
    query: "我想查快递到哪里了",
    check: (out) =>
      out.includes("快递物流查询") && out.includes("logistics"),
  },
  {
    name: "[低风险] 快递+天气混合 - 命中快递",
    query: "我的快递到了吗，今天天气怎么样",
    check: (out) => out.includes("快递物流查询"),
  },

  // --- 中风险：心理健康 ---
  {
    name: "[中风险] 工作压力 - 识别心理健康意图",
    query: "我最近工作压力好大，感觉快要撑不住了",
    check: (out) =>
      out.includes("心理健康") &&
      out.includes("burnout-checkin"),
  },
  {
    name: "[中风险] 焦虑 - 识别意图",
    query: "我很焦虑，有什么skill能帮到我吗",
    check: (out) =>
      out.includes("心理健康") &&
      (out.includes("burnout-checkin") || out.includes("psych-companion")),
  },

  // --- 高风险：法律 ---
  {
    name: "[高风险] 租房合同 - 识别法律意图+免责",
    query: "我要写一份租房合同，有什么工具帮我吗",
    check: (out) =>
      out.includes("合同法律") &&
      out.includes("clause-redraft") &&
      out.includes("⚠️"),
  },
  {
    name: "[高风险] 法律咨询 - 高风险标注+免责声明",
    query: "有什么法律类的skill吗",
    check: (out) =>
      out.includes("法律") &&
      (out.includes("🔴") || out.includes("高风险")) &&
      out.includes("⚠️"),
  },

  // --- 中风险：相亲 ---
  {
    name: "[中风险] 相亲找对象",
    query: "我想找对象，有什么红娘skill吗",
    check: (out) =>
      out.includes("相亲找对象") &&
      out.includes("xiangqin"),
  },

  // --- 低风险：天气 ---
  {
    name: "[低风险] 天气查询",
    query: "今天天气怎么样",
    check: (out) => out.includes("天气查询") && out.includes("weather"),
  },

  // --- 低风险：外卖 ---
  {
    name: "[低风险] 外卖点餐",
    query: "我想点外卖",
    check: (out) =>
      out.includes("外卖点餐") && out.includes("waimai"),
  },

  // --- 低风险：出行 ---
  {
    name: "[低风险] 打车出行",
    query: "我想打车",
    check: (out) =>
      out.includes("出行交通") && out.includes("didi"),
  },

  // --- 拒绝场景 ---
  {
    name: "[拒绝] 穿衣服 - 友好拒绝",
    query: "你觉得我今天出门应该穿什么",
    check: (out) =>
      out.includes("抱歉") || out.includes("暂无法识别"),
  },

  // --- 边界：已安装过滤 ---
  {
    name: "[边界] 已安装logistics - 跳过并提示",
    query: "我想查快递",
    installed: ["logistics"],
    check: (out) =>
      !out.includes("logistics") ||
      out.includes("已安装") ||
      out.includes("无需"),
  },
];

async function main() {
  // 如果带了参数，直接对指定查询运行并打印结果
  if (process.argv.length > 2) {
    const query = process.argv.slice(2).join(" ");
    const installed = process.argv.includes("--installed")
      ? process.argv[process.argv.indexOf("--installed") + 1].split(",")
      : [];
    const result = await runPy(query, installed);
    console.log(result.stdout);
    if (result.stderr) console.error("STDERR:", result.stderr);
    return;
  }

  // 内置测试套件
  console.log("🧪 Clawpilot Test Suite\n");
  let passed = 0;
  let failed = 0;

  for (const t of TESTS) {
    const { stdout } = await runPy(t.query, t.installed || []);
    const ok = t.check(stdout);
    const status = ok ? "✅ PASS" : "❌ FAIL";
    console.log(`${status}  ${t.name}`);
    if (!ok) {
      console.log(`       查询: ${t.query}`);
      if (t.installed?.length) console.log(`       已安装: ${t.installed.join(", ")}`);
      console.log(`       输出: ${stdout.slice(0, 300).replace(/\n/g, " ")}`);
      failed++;
    } else {
      passed++;
    }
  }

  console.log(`\n📊 结果: ${passed} 通过, ${failed} 失败`);
  process.exit(failed > 0 ? 1 : 0);
}

main().catch(console.error);
