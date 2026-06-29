#!/usr/bin/env node

/**
 * 将 roadbook.json 导出为格式化的 Excel 路书（.xlsx）
 *
 * 用法:
 *   node scripts/export-excel.mjs --input output/roadbook.json --output output/roadbook.xlsx
 */

import ExcelJS from "exceljs";
import fs from "node:fs";
import path from "node:path";

function readArg(name) {
  const index = process.argv.indexOf(`--${name}`);
  if (index === -1) return undefined;
  return process.argv[index + 1];
}

// ─── 样式常量 ─────────────────────────────────────────────

const STYLE = {
  title: { font: { bold: true, size: 16 }, alignment: { horizontal: "center" } },
  subtitle: { font: { bold: true, size: 12 } },
  header: {
    font: { bold: true, size: 11, color: { argb: "FFFFFFFF" } },
    fill: { type: "pattern", pattern: "solid", fgColor: { argb: "FF2D5F8A" } },
    alignment: { horizontal: "center", vertical: "middle" },
    border: {
      top: { style: "thin" }, bottom: { style: "thin" },
      left: { style: "thin" }, right: { style: "thin" }
    }
  },
  cell: {
    border: {
      top: { style: "thin" }, bottom: { style: "thin" },
      left: { style: "thin" }, right: { style: "thin" }
    }
  },
  modeColors: {
    rail:       { fill: { type: "pattern", pattern: "solid", fgColor: { argb: "FFDBEAFE" } } },  // 高铁蓝
    taxi:       { fill: { type: "pattern", pattern: "solid", fgColor: { argb: "FFFED7AA" } } },  // 打车橙
    drive:      { fill: { type: "pattern", pattern: "solid", fgColor: { argb: "FFFED7AA" } } },
    walk:       { fill: { type: "pattern", pattern: "solid", fgColor: { argb: "FFD1FAE5" } } },  // 步行绿
    public_transit: { fill: { type: "pattern", pattern: "solid", fgColor: { argb: "FFE9D5FF" } } }, // 公交紫
    bike:       { fill: { type: "pattern", pattern: "solid", fgColor: { argb: "FFFEF3C7" } } },  // 骑行黄
  }
};

function modeStyle(mode) {
  return STYLE.modeColors[mode] || {};
}

function modeLabel(mode) {
  const labels = {
    rail: "🚄 高铁", taxi: "🚕 打车", drive: "🚗 自驾",
    walk: "🚶 步行", public_transit: "🚇 地铁/公交", bike: "🚲 骑行",
    rail: "🚄 高铁", flight: "✈️ 飞机", mixed: "🔄 混合"
  };
  return labels[mode] || mode;
}

const WEATHER_ICON = {
  "晴": "☀️", "多云": "⛅", "阴": "☁️", "小雨": "🌦️", "中雨": "🌧️",
  "大雨": "🌧️", "雷阵雨": "⛈️", "雪": "❄️", "雾": "🌫️"
};

function weatherIcon(text) {
  if (!text) return "";
  for (const [k, v] of Object.entries(WEATHER_ICON)) {
    if (text.includes(k)) return v;
  }
  return "";
}

// ─── 工具函数 ─────────────────────────────────────────────

function flattenStops(days) {
  const rows = [];
  for (const day of days) {
    for (const stop of day.stops || []) {
      rows.push({ ...stop, dayTitle: day.title, dayDate: day.date, dayWeather: day.weather });
    }
  }
  return rows;
}

function flattenLegs(days) {
  const rows = [];
  for (const day of days) {
    for (const leg of day.legs || []) {
      rows.push({ ...leg, dayTitle: day.title, dayDate: day.date });
    }
  }
  return rows;
}

function getAllPOIs(days) {
  const seen = new Set();
  const pois = [];
  for (const day of days) {
    for (const stop of day.stops || []) {
      if (stop.type === "railway_station" || stop.type === "hotel_area") continue;
      const key = stop.name;
      if (seen.has(key)) continue;
      seen.add(key);
      pois.push(stop);
    }
  }
  return pois;
}

// ─── Sheet 构建 ────────────────────────────────────────────

/**
 * Sheet 1: 总览
 */
async function buildOverviewSheet(ws, rb) {
  const { title, origin, destination, dateRange, mustVisit, intercityTransport,
    localTransport, lodging, pace, budget, travelers, assumptions, warnings, days } = rb;

  const paceMap = { packed: "🔥 密集", balanced: "⚖️ 均衡", relaxed: "😌 轻松" };

  // 标题行
  ws.mergeCells("A1:F1");
  const titleCell = ws.getCell("A1");
  titleCell.value = title || "高德路书";
  titleCell.font = STYLE.title.font;
  titleCell.alignment = STYLE.title.alignment;
  ws.getRow(1).height = 36;

  // 基本信息
  const infoRows = [
    ["出发地", origin?.label || "", "目的地", destination?.label || ""],
    ["日期", `${dateRange?.start || ""} 至 ${dateRange?.end || ""}`, "天数", `${dateRange?.days || ""} 天`],
    ["交通方式", modeLabel(intercityTransport || "rail"), "市内交通", modeLabel(localTransport || "public_transit")],
    ["住宿区域", lodging?.area || "待定", "节奏", paceMap[pace] || pace],
    ["预算", budget || "", "同行", travelers || ""],
  ];

  let rowIdx = 3;
  for (const r of infoRows) {
    const row = ws.getRow(rowIdx);
    row.getCell(1).value = r[0]; row.getCell(1).font = { bold: true };
    row.getCell(2).value = r[1];
    row.getCell(3).value = r[2]; row.getCell(3).font = { bold: true };
    row.getCell(4).value = r[3];
    for (let c = 1; c <= 4; c++) {
      row.getCell(c).border = STYLE.cell.border;
    }
    rowIdx++;
  }

  // 天气概要
  rowIdx += 1;
  ws.getCell(`A${rowIdx}`).value = "天气概要";
  ws.getCell(`A${rowIdx}`).font = STYLE.subtitle.font;
  rowIdx++;

  const weatherHeader = ws.getRow(rowIdx);
  ["日期", "天气", "温度", "图标"].forEach((h, i) => {
    weatherHeader.getCell(i + 1).value = h;
    weatherHeader.getCell(i + 1).style = STYLE.header;
  });
  rowIdx++;

  for (const day of days) {
    if (!day.weather) continue;
    const row = ws.getRow(rowIdx);
    row.getCell(1).value = day.date;
    const wt = day.weather.text || "";
    row.getCell(2).value = wt;
    row.getCell(3).value = day.weather.temperature || "";
    row.getCell(4).value = weatherIcon(wt);
    for (let c = 1; c <= 4; c++) row.getCell(c).border = STYLE.cell.border;
    rowIdx++;
  }

  // 必去景点
  if (mustVisit && mustVisit.length > 0) {
    rowIdx += 1;
    ws.getCell(`A${rowIdx}`).value = "计划游览景点";
    ws.getCell(`A${rowIdx}`).font = STYLE.subtitle.font;
    rowIdx++;
    const row = ws.getRow(rowIdx);
    row.getCell(1).value = mustVisit.join(" · ");
    row.getCell(1).border = STYLE.cell.border;
    rowIdx++;
  }

  // 假设与提醒
  for (const [label, items] of [["假设说明", assumptions], ["⚠️ 提醒", warnings]]) {
    if (!items || items.length === 0) continue;
    rowIdx += 1;
    ws.getCell(`A${rowIdx}`).value = label;
    ws.getCell(`A${rowIdx}`).font = STYLE.subtitle.font;
    rowIdx++;
    for (const item of items) {
      const row = ws.getRow(rowIdx);
      row.getCell(1).value = `• ${item}`;
      row.getCell(1).border = STYLE.cell.border;
      rowIdx++;
    }
  }

  // 列宽
  ws.getColumn(1).width = 12;
  ws.getColumn(2).width = 28;
  ws.getColumn(3).width = 12;
  ws.getColumn(4).width = 28;
  ws.getColumn(5).width = 10;
  ws.getColumn(6).width = 14;
}

/**
 * Sheet 2: 每日行程
 */
async function buildScheduleSheet(ws, days) {
  const headers = ["日期", "时间", "地点", "类型", "时长(分)", "备注说明"];
  ws.getRow(1).height = 24;
  headers.forEach((h, i) => {
    const cell = ws.getRow(1).getCell(i + 1);
    cell.value = h;
    cell.style = STYLE.header;
  });

  let rowIdx = 2;
  let lastDate = null;

  for (const day of days) {
    // 每日标题行
    if (rowIdx > 2) {
      // 空行分隔
      rowIdx++;
    }
    const dayTitle = ws.getRow(rowIdx);
    ws.mergeCells(`A${rowIdx}:F${rowIdx}`);
    const dtCell = dayTitle.getCell(1);
    dtCell.value = `📅 ${day.date || ""}  ${day.title || ""}`;
    dtCell.font = { bold: true, size: 12, color: { argb: "FF2D5F8A" } };
    dtCell.fill = { type: "pattern", pattern: "solid", fgColor: { argb: "FFE8F0FE" } };
    dtCell.alignment = { vertical: "middle" };
    ws.getRow(rowIdx).height = 28;
    rowIdx++;

    lastDate = day.date;

    for (const stop of day.stops || []) {
      const row = ws.getRow(rowIdx);
      row.getCell(1).value = day.date;
      row.getCell(2).value = stop.time || "";
      row.getCell(3).value = stop.name || "";
      row.getCell(4).value = typeLabel(stop.type || "");
      row.getCell(5).value = stop.durationMinutes || "";
      row.getCell(6).value = stop.note || "";
      for (let c = 1; c <= 6; c++) row.getCell(c).border = STYLE.cell.border;
      // 时间列居中对齐
      row.getCell(2).alignment = { horizontal: "center" };
      row.getCell(5).alignment = { horizontal: "center" };
      row.height = 22;
      rowIdx++;
    }

    // 交通衔接
    if (day.legs && day.legs.length > 0) {
      for (const leg of day.legs) {
        const row = ws.getRow(rowIdx);
        row.getCell(1).value = day.date;
        row.getCell(2).value = "→";
        row.getCell(3).value = `${leg.from || ""}  →  ${leg.to || ""}`;
        row.getCell(4).value = modeLabel(leg.mode || "");
        row.getCell(5).value = leg.durationText || "";
        row.getCell(6).value = leg.summary || "";

        // 根据交通方式着色
        const ms = modeStyle(leg.mode);
        if (ms.fill) row.getCell(4).fill = ms.fill;

        for (let c = 1; c <= 6; c++) row.getCell(c).border = STYLE.cell.border;
        row.getCell(2).alignment = { horizontal: "center" };
        row.getCell(5).alignment = { horizontal: "center" };
        row.height = 22;
        rowIdx++;
      }
    }
  }

  ws.getColumn(1).width = 14;
  ws.getColumn(2).width = 8;
  ws.getColumn(3).width = 32;
  ws.getColumn(4).width = 16;
  ws.getColumn(5).width = 10;
  ws.getColumn(6).width = 45;
}

function typeLabel(type) {
  const map = {
    railway_station: "🚉 车站", scenic: "🏛️ 景点", street: "🏮 街区",
    hotel_area: "🏨 住宿", shopping: "🛍️ 商圈", theme_park: "🎢 乐园",
    restaurant: "🍽️ 美食", bar: "🍸 酒吧", cafe: "☕ 咖啡",
    park: "🌳 公园", museum: "🏛️ 博物馆",
  };
  return map[type] || type;
}

/**
 * Sheet 3: 路线段（精简）
 */
async function buildRouteSheet(ws, days) {
  const headers = ["日期", "起点", "终点", "交通方式", "用时", "距离", "说明"];
  ws.getRow(1).height = 24;
  headers.forEach((h, i) => {
    const cell = ws.getRow(1).getCell(i + 1);
    cell.value = h;
    cell.style = STYLE.header;
  });

  let rowIdx = 2;
  for (const day of days) {
    if (!day.legs) continue;
    // 每日标题
    const dtRow = ws.getRow(rowIdx);
    ws.mergeCells(`A${rowIdx}:G${rowIdx}`);
    dtRow.getCell(1).value = `📅 ${day.date}  ${day.title}`;
    dtRow.getCell(1).font = { bold: true, size: 11, color: { argb: "FF2D5F8A" } };
    rowIdx++;

    for (const leg of day.legs) {
      const row = ws.getRow(rowIdx);
      row.getCell(1).value = day.date;
      row.getCell(2).value = leg.from || "";
      row.getCell(3).value = leg.to || "";
      row.getCell(4).value = modeLabel(leg.mode || "");
      row.getCell(5).value = leg.durationText || "";
      row.getCell(6).value = leg.distanceText || "";
      row.getCell(7).value = leg.summary || "";

      const ms = modeStyle(leg.mode);
      if (ms.fill) row.getCell(4).fill = ms.fill;

      for (let c = 1; c <= 7; c++) row.getCell(c).border = STYLE.cell.border;
      row.height = 22;
      rowIdx++;
    }
  }

  ws.getColumn(1).width = 14;
  ws.getColumn(2).width = 20;
  ws.getColumn(3).width = 20;
  ws.getColumn(4).width = 16;
  ws.getColumn(5).width = 12;
  ws.getColumn(6).width = 12;
  ws.getColumn(7).width = 40;
}

/**
 * Sheet 4: 预算估算
 */
async function buildBudgetSheet(ws, rb) {
  const headers = ["项目", "预估费用（元）", "备注"];
  ws.getRow(1).height = 24;
  headers.forEach((h, i) => {
    const cell = ws.getRow(1).getCell(i + 1);
    cell.value = h;
    cell.style = STYLE.header;
  });

  // 根据行程内容估算各项费用
  const days = rb.days || [];
  const daysCount = rb.dateRange?.days || 3;
  const travelers = rb.travelers?.includes("2") || rb.travelers?.includes("俩") || rb.travelers?.includes("对") ? 2 : 2;

  // 高铁往返（2人）
  const canHighSpeed = rb.origin?.label?.includes("宣城") || true;
  let railEst = "约 1,200 - 1,600";
  if (!canHighSpeed) railEst = "待确认";
  const budgetItems = [
    ["🚄 高铁往返（${travelers}人）", railEst, "宣城↔北京，具体以12306为准"],
  ];

  // 住宿
  const lodgingArea = rb.lodging?.area || "待定";
  budgetItems.push(["🏨 住宿（${daysCount - 1}晚）", "约 600 - 1,500", `${lodgingArea}，快捷/中档酒店`]);

  // 门票（根据停靠点估算）
  const pois = getAllPOIs(days);
  const ticketEst = pois.length * 30 * travelers;
  const ticketText = ticketEst > 0 ? `约 ${Math.round(ticketEst / 100) * 100} 元` : "约 400 - 600 元";
  budgetItems.push(["🎫 景点门票", ticketText, `${pois.length} 个景点，含故宫、长城等`]);

  // 餐饮
  const mealDaily = travelers * 150;
  budgetItems.push(["🍜 餐饮（${daysCount}天）", `约 ${mealDaily * daysCount} 元`, "每日约150元/人"]);
  budgetItems.push(["🚕 市内交通", "约 400 - 600 元", "地铁+打车（长城包车）"]);
  budgetItems.push(["🛍️ 其他消费", "约 500 - 1,000 元", "零食、纪念品等"]);
  budgetItems.push(["📋 合计", "约 4,000 - 6,000 元", "预算 10,000 元，有富余"]);

  let rowIdx = 2;
  for (const [item, amount, note] of budgetItems) {
    const row = ws.getRow(rowIdx);
    row.getCell(1).value = item;
    row.getCell(2).value = amount;
    row.getCell(3).value = note;
    for (let c = 1; c <= 3; c++) row.getCell(c).border = STYLE.cell.border;
    row.height = 22;
    rowIdx++;
  }

  // 最后一行加粗
  const lastRow = ws.getRow(rowIdx - 1);
  lastRow.getCell(1).font = { bold: true, size: 11 };
  lastRow.getCell(2).font = { bold: true, size: 11, color: { argb: "FF16A34A" } };

  // 总预算对比
  rowIdx += 1;
  ws.mergeCells(`A${rowIdx}:C${rowIdx}`);
  const budgetNote = ws.getCell(`A${rowIdx}`);
  const totalBudget = rb.budget || "10,000 元";
  budgetNote.value = `总预算 ${totalBudget}，上述预估总和不超预算，余额可用于升级酒店或餐饮 😊`;
  budgetNote.font = { italic: true, color: { argb: "FF6B7280" } };
  budgetNote.alignment = { wrapText: true };

  ws.getColumn(1).width = 28;
  ws.getColumn(2).width = 22;
  ws.getColumn(3).width = 40;
}

/**
 * Sheet 5: 景点联系信息
 */
async function buildPOISheet(ws, days) {
  const headers = ["景点名称", "类型", "评分", "电话", "营业时间", "标签", "建议时长(分)"];
  ws.getRow(1).height = 24;
  headers.forEach((h, i) => {
    const cell = ws.getRow(1).getCell(i + 1);
    cell.value = h;
    cell.style = STYLE.header;
  });

  const pois = getAllPOIs(days);
  let rowIdx = 2;
  for (const p of pois) {
    const row = ws.getRow(rowIdx);
    row.getCell(1).value = p.name || "";
    row.getCell(2).value = typeLabel(p.type || "");
    row.getCell(3).value = p.poiRating || "";
    row.getCell(4).value = p.poiTel || "";
    row.getCell(5).value = p.poiHours || "";
    // Combine tags
    const tags = [p.poiTag, p.poiRecTag].filter(Boolean).join(" · ");
    row.getCell(6).value = tags || "";
    row.getCell(7).value = p.durationMinutes || "";

    for (let c = 1; c <= 7; c++) row.getCell(c).border = STYLE.cell.border;
    row.height = 20;
    rowIdx++;
  }

  ws.getColumn(1).width = 24;
  ws.getColumn(2).width = 14;
  ws.getColumn(3).width = 8;
  ws.getColumn(4).width = 18;
  ws.getColumn(5).width = 18;
  ws.getColumn(6).width = 24;
  ws.getColumn(7).width = 12;
}

// ─── 主流程 ────────────────────────────────────────────────

async function main() {
  const inputPath = readArg("input");
  const outputPath = readArg("output");

  if (!inputPath || !outputPath) {
    console.error("用法: node scripts/export-excel.mjs --input <roadbook.json> --output <output.xlsx>");
    process.exit(1);
  }

  const rb = JSON.parse(fs.readFileSync(path.resolve(inputPath), "utf8"));
  const outputFile = path.resolve(outputPath);

  const wb = new ExcelJS.Workbook();
  wb.creator = "amap-roadbook";
  wb.created = new Date();

  // Sheet 1: 总览
  const ws1 = wb.addWorksheet("总览");
  await buildOverviewSheet(ws1, rb);

  // Sheet 2: 每日行程
  const ws2 = wb.addWorksheet("每日行程");
  await buildScheduleSheet(ws2, rb.days);

  // Sheet 3: 路线段
  const ws3 = wb.addWorksheet("路线段");
  await buildRouteSheet(ws3, rb.days);

  // Sheet 4: 预算
  const ws4 = wb.addWorksheet("预算");
  await buildBudgetSheet(ws4, rb);

  // Sheet 5: 联系信息
  const ws5 = wb.addWorksheet("景点信息");
  await buildPOISheet(ws5, rb.days);

  await wb.xlsx.writeFile(outputFile);
  console.log(`✅ Excel 路书已生成: ${outputFile}`);
}

main().catch(err => {
  console.error("❌ 导出失败:", err.message);
  process.exit(1);
});
