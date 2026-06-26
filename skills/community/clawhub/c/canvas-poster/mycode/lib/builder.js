const { FONT, DARK_THEME: C, createCanvas, roundRect, formatMoney, drawPieChart, truncateText, drawDivider, drawAxes, sanitizeText } = require('./core');
const fs = require('fs');

const W_DEFAULT = 800;
const P = 40;
const PIE_R = 70;
const DIVIDER_H = 15;

function txt(s) { return sanitizeText(String(s || '')); }

// ===== Section 高度计算 =====

function sectionHeight(section) {
  const { type } = section;
  switch (type) {
    case 'kpi-cards': {
      const cards = section.cards || section.data || [];
      const rows = Math.ceil(cards.length / 2);
      return DIVIDER_H + 28 + rows * 58;
    }
    case 'bar-chart': {
      const bars = section.bars || section.data || [];
      return DIVIDER_H + 38 + bars.length * 32 + 18;
    }
    case 'pie-chart': {
      const slices = section.slices || section.data || [];
      const legendH = slices.length * 26;
      return DIVIDER_H + 30 + Math.max(PIE_R * 2, legendH) + 20;
    }
    case 'table': {
      const rows = section.rows || section.data || [];
      return DIVIDER_H + 30 + 25 + rows.length * 36 + 10;
    }
    case 'tips': {
      const items = section.items || section.data || [];
      return DIVIDER_H + 28 + 12 + items.length * 32 + 30;
    }
    case 'line-chart': {
      const lines = section.lines || section.data || [];
      const hasLegend = section.showLegend !== false && lines.length > 1;
      return DIVIDER_H + 30 + 160 + (hasLegend ? 30 : 0) + 20;
    }
    case 'area-chart': {
      const areas = section.areas || section.data || [];
      const hasLegend = section.showLegend !== false && areas.length > 1;
      return DIVIDER_H + 30 + 160 + (hasLegend ? 30 : 0) + 20;
    }
    case 'scatter-chart': {
      return DIVIDER_H + 30 + 160 + 20;
    }
    case 'divider':
      return 30;
    default:
      return 0;
  }
}

// ===== Section 绘制 =====

function drawSection(ctx, section, y, W) {
  const { type, title } = section;

  drawDivider(ctx, P, y, W);
  y += DIVIDER_H;

  switch (type) {
    case 'kpi-cards': {
      const cards = section.cards || section.data || [];

      ctx.font = `bold 18px "${FONT}"`;
      ctx.fillStyle = C.accent;
      ctx.textAlign = 'left';
      ctx.fillText(txt(title || '📊 概览'), P, y + 18);
      y += 28;

      const cardW = (W - P * 2 - 12) / 2;
      const cardH = 50;
      for (let i = 0; i < cards.length; i++) {
        const item = cards[i];
        const col = i % 2;
        const row = Math.floor(i / 2);
        const cx = P + col * (cardW + 12);
        const cy = y + row * (cardH + 8);

        roundRect(ctx, cx, cy, cardW, cardH, 8);
        ctx.fillStyle = C.cardBg;
        ctx.fill();
        ctx.strokeStyle = C.cardBorder;
        ctx.lineWidth = 1;
        ctx.stroke();

        ctx.font = `14px "${FONT}"`;
        ctx.fillStyle = C.subtle;
        ctx.textAlign = 'left';
        ctx.fillText(txt(item.label), cx + 12, cy + 20);

        ctx.font = `bold 20px "${FONT}"`;
        const valColor = item.color === 'red' ? C.red : item.color === 'orange' ? C.orange : item.color === 'green' ? C.green : C.white;
        ctx.fillStyle = valColor;
        ctx.fillText(txt(item.value), cx + 12, cy + 44);

        if (item.sub) {
          ctx.font = `12px "${FONT}"`;
          ctx.fillStyle = C.subtle;
          ctx.textAlign = 'right';
          ctx.fillText(txt(item.sub), cx + cardW - 12, cy + 44);
          ctx.textAlign = 'left';
        }
      }
      y += Math.ceil(cards.length / 2) * (cardH + 8);
      break;
    }

    case 'bar-chart': {
      const bars = section.bars || section.data || [];

      ctx.font = `bold 18px "${FONT}"`;
      ctx.fillStyle = C.accent;
      ctx.textAlign = 'left';
      ctx.fillText(txt(title || '📊 数据'), P, y + 18);
      y += 38;

      const barMax = Math.max(...bars.map(d => d.value), 1);
      for (let i = 0; i < bars.length; i++) {
        const item = bars[i];
        const bx = P + 70;
        const bw = W - P * 2 - 170;

        ctx.font = `14px "${FONT}"`;
        ctx.fillStyle = C.text;
        ctx.textAlign = 'right';
        ctx.fillText(txt(item.name), P + 60, y + 14);

        const barW = (item.value / barMax) * bw;
        roundRect(ctx, bx, y, barW, 18, 4);
        ctx.fillStyle = item.color || C.barColors[i % C.barColors.length];
        ctx.fill();

        ctx.font = `12px "${FONT}"`;
        ctx.fillStyle = C.subtle;
        ctx.textAlign = 'left';
        const pct = item.pct != null ? ` (${item.pct}%)` : '';
        ctx.fillText(`${formatMoney(item.value)}${pct}`, bx + barW + 8, y + 14);
        ctx.textAlign = 'left';

        y += 32;
      }
      y += 18;
      break;
    }

    case 'pie-chart': {
      const slices = section.slices || section.data || [];

      ctx.font = `bold 18px "${FONT}"`;
      ctx.fillStyle = C.accent;
      ctx.textAlign = 'left';
      ctx.fillText(txt(title || '📊 分布'), P, y + 18);
      y += 30;

      const legendH = slices.length * 26;
      const areaH = Math.max(PIE_R * 2, legendH);
      const pieCx = P + PIE_R + 20;
      const pieCy = y + areaH / 2;
      drawPieChart(ctx, pieCx, pieCy, PIE_R, slices, {
        donut: section.donut || false,
        center: section.center,
        centerColor: section.centerColor,
        centerFont: section.centerFont,
      });

      const legendX = P + PIE_R * 2 + 60;
      const legendStartY = y + (areaH - legendH) / 2;
      for (let i = 0; i < slices.length; i++) {
        const r = slices[i];
        const ly = legendStartY + i * 26;
        ctx.fillStyle = C.barColors[i % C.barColors.length];
        roundRect(ctx, legendX, ly, 12, 12, 2);
        ctx.fill();
        ctx.font = `13px "${FONT}"`;
        ctx.fillStyle = C.text;
        ctx.fillText(txt(r.name), legendX + 18, ly + 11);
        ctx.fillStyle = C.subtle;
        const pct = r.pct != null ? ` (${r.pct}%)` : '';
        ctx.fillText(`${formatMoney(r.value)}${pct}`, legendX + 130, ly + 11);
      }
      y += areaH + 20;
      break;
    }

    case 'table': {
      const headers = section.headers || [];
      const rows = section.rows || section.data || [];

      ctx.font = `bold 18px "${FONT}"`;
      ctx.fillStyle = section.color || C.accent;
      ctx.textAlign = 'left';
      ctx.fillText(txt(title || '📋 数据'), P, y + 18);
      y += 30;

      const colW = (W - P * 2) / headers.length;

      ctx.font = `bold 13px "${FONT}"`;
      ctx.fillStyle = C.subtle;
      for (let c = 0; c < headers.length; c++) {
        ctx.fillText(txt(headers[c]), P + c * colW + 10, y + 14);
      }
      y += 25;

      for (let r = 0; r < rows.length; r++) {
        if (r % 2 === 0) {
          roundRect(ctx, P, y - 12, W - P * 2, 32, 4);
          ctx.fillStyle = section.rowBg || 'rgba(239,68,68,0.06)';
          ctx.fill();
        }
        ctx.font = `14px "${FONT}"`;
        for (let c = 0; c < rows[r].length; c++) {
          ctx.fillStyle = c === 1 && section.color ? section.color : C.text;
          ctx.fillText(txt(rows[r][c]), P + c * colW + 10, y + 6);
        }
        y += 36;
      }
      y += 10;
      break;
    }

    case 'tips': {
      const items = section.items || section.data || [];

      ctx.font = `bold 18px "${FONT}"`;
      ctx.fillStyle = C.green;
      ctx.textAlign = 'left';
      ctx.fillText(txt(title || '💡 建议'), P, y + 18);
      y += 28;

      const boxH = items.length * 32 + 40;
      roundRect(ctx, P, y, W - P * 2, boxH, 8);
      ctx.fillStyle = 'rgba(34,197,94,0.08)';
      ctx.fill();

      y += 12;
      ctx.font = `14px "${FONT}"`;
      const maxTextW = W - P * 2 - 40;
      for (const tip of items) {
        ctx.fillStyle = C.green;
        ctx.beginPath();
        ctx.moveTo(P + 12, y - 2);
        ctx.lineTo(P + 20, y + 4);
        ctx.lineTo(P + 12, y + 10);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = C.text;
        ctx.fillText(truncateText(ctx, txt(tip), maxTextW), P + 28, y + 4);
        y += 32;
      }
      y += 30;
      break;
    }

    case 'line-chart': {
      const lines = section.lines || section.data || [];

      ctx.font = `bold 18px "${FONT}"`;
      ctx.fillStyle = C.accent;
      ctx.textAlign = 'left';
      ctx.fillText(txt(title || '📈 趋势'), P, y + 18);
      y += 30;

      if (lines.length > 0 && lines[0].data && lines[0].data.length > 0) {
        const allVals = lines.flatMap(l => l.data);
        const yMin = Math.min(...allVals);
        const yMax = Math.max(...allVals);
        const pad = (yMax - yMin) * 0.1 || 1;
        const xLabels = section.xLabels || lines[0].data.map((_, i) => i + 1);

        const { scaleX, scaleY } = drawAxes(ctx, {
          x: P, y, w: W - P * 2, h: 160,
          xLabels, yMin: yMin - pad, yMax: yMax + pad,
        });

        const total = lines[0].data.length;
        for (let li = 0; li < lines.length; li++) {
          const line = lines[li];
          const color = line.color || C.barColors[li % C.barColors.length];
          ctx.strokeStyle = color;
          ctx.lineWidth = 2;
          ctx.beginPath();
          for (let i = 0; i < line.data.length; i++) {
            const px = scaleX(i, total);
            const py = scaleY(line.data[i]);
            if (i === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
          }
          ctx.stroke();

          if (section.showDots !== false) {
            ctx.fillStyle = color;
            for (let i = 0; i < line.data.length; i++) {
              ctx.beginPath();
              ctx.arc(scaleX(i, total), scaleY(line.data[i]), 3, 0, Math.PI * 2);
              ctx.fill();
            }
          }
        }
      }
      y += 160;

      const showLineLegend = section.showLegend !== false && lines.length > 1;
      if (showLineLegend) {
        let lx = P;
        ctx.font = `12px "${FONT}"`;
        for (let li = 0; li < lines.length; li++) {
          const color = lines[li].color || C.barColors[li % C.barColors.length];
          ctx.fillStyle = color;
          ctx.fillRect(lx, y + 8, 16, 3);
          ctx.fillStyle = C.text;
          ctx.fillText(txt(lines[li].name || `Line ${li + 1}`), lx + 20, y + 14);
          lx += ctx.measureText(txt(lines[li].name || `Line ${li + 1}`)).width + 36;
        }
        y += 30;
      }
      y += 20;
      break;
    }

    case 'area-chart': {
      const areas = section.areas || section.data || [];

      ctx.font = `bold 18px "${FONT}"`;
      ctx.fillStyle = C.accent;
      ctx.textAlign = 'left';
      ctx.fillText(txt(title || '📈 面积图'), P, y + 18);
      y += 30;

      if (areas.length > 0 && areas[0].data && areas[0].data.length > 0) {
        const allVals = areas.flatMap(a => a.data);
        const yMin = Math.min(...allVals);
        const yMax = Math.max(...allVals);
        const pad = (yMax - yMin) * 0.1 || 1;
        const xLabels = section.xLabels || areas[0].data.map((_, i) => i + 1);

        const { scaleX, scaleY, plotY: pY, plotH } = drawAxes(ctx, {
          x: P, y, w: W - P * 2, h: 160,
          xLabels, yMin: yMin - pad, yMax: yMax + pad,
        });

        const total = areas[0].data.length;
        const opacity = section.opacity != null ? section.opacity : 0.3;
        const baseline = pY + plotH;

        for (let ai = 0; ai < areas.length; ai++) {
          const area = areas[ai];
          const color = area.color || C.barColors[ai % C.barColors.length];

          // fill
          ctx.beginPath();
          ctx.moveTo(scaleX(0, total), baseline);
          for (let i = 0; i < area.data.length; i++) {
            ctx.lineTo(scaleX(i, total), scaleY(area.data[i]));
          }
          ctx.lineTo(scaleX(area.data.length - 1, total), baseline);
          ctx.closePath();
          ctx.globalAlpha = opacity;
          ctx.fillStyle = color;
          ctx.fill();
          ctx.globalAlpha = 1;

          // stroke
          ctx.strokeStyle = color;
          ctx.lineWidth = 2;
          ctx.beginPath();
          for (let i = 0; i < area.data.length; i++) {
            const px = scaleX(i, total);
            const py = scaleY(area.data[i]);
            if (i === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
          }
          ctx.stroke();

          if (section.showDots) {
            ctx.fillStyle = color;
            for (let i = 0; i < area.data.length; i++) {
              ctx.beginPath();
              ctx.arc(scaleX(i, total), scaleY(area.data[i]), 3, 0, Math.PI * 2);
              ctx.fill();
            }
          }
        }
      }
      y += 160;

      const showAreaLegend = section.showLegend !== false && areas.length > 1;
      if (showAreaLegend) {
        let lx = P;
        ctx.font = `12px "${FONT}"`;
        for (let ai = 0; ai < areas.length; ai++) {
          const color = areas[ai].color || C.barColors[ai % C.barColors.length];
          ctx.fillStyle = color;
          ctx.fillRect(lx, y + 6, 12, 12);
          ctx.fillStyle = C.text;
          ctx.fillText(txt(areas[ai].name || `Area ${ai + 1}`), lx + 16, y + 14);
          lx += ctx.measureText(txt(areas[ai].name || `Area ${ai + 1}`)).width + 32;
        }
        y += 30;
      }
      y += 20;
      break;
    }

    case 'scatter-chart': {
      const points = section.points || section.data || [];

      ctx.font = `bold 18px "${FONT}"`;
      ctx.fillStyle = C.accent;
      ctx.textAlign = 'left';
      ctx.fillText(txt(title || '📊 散点图'), P, y + 18);
      y += 30;

      if (points.length > 0) {
        const xs = points.map(p => p.x);
        const ys = points.map(p => p.y);
        const xMin = Math.min(...xs);
        const xMax = Math.max(...xs);
        const yMinVal = Math.min(...ys);
        const yMaxVal = Math.max(...ys);
        const xPad = (xMax - xMin) * 0.1 || 1;
        const yPad = (yMaxVal - yMinVal) * 0.1 || 1;

        const xTicks = 5;
        const xLabels = [];
        for (let i = 0; i < xTicks; i++) {
          const v = (xMin - xPad) + (i / (xTicks - 1)) * ((xMax + xPad) - (xMin - xPad));
          xLabels.push(Number.isInteger(v) ? v : v.toFixed(1));
        }

        const { plotX, plotW, scaleY } = drawAxes(ctx, {
          x: P, y, w: W - P * 2, h: 160,
          xLabels, yMin: yMinVal - yPad, yMax: yMaxVal + yPad,
        });

        const scaleXVal = (val) => plotX + ((val - (xMin - xPad)) / ((xMax + xPad) - (xMin - xPad) || 1)) * plotW;
        const dotR = section.dotRadius || 4;

        for (const pt of points) {
          const px = scaleXVal(pt.x);
          const py = scaleY(pt.y);
          ctx.beginPath();
          ctx.arc(px, py, dotR, 0, Math.PI * 2);
          ctx.fillStyle = pt.color || C.accent;
          ctx.fill();
        }
      }
      y += 160;
      y += 20;
      break;
    }

    case 'divider':
      y += 15;
      break;

    default:
      console.warn(`Unknown section type: ${type}`);
  }

  return y;
}

// ===== 计算总高度 =====

function calcTotalHeight(config) {
  let h = 0;
  if (config.header) h += 120;
  for (const sec of config.sections || []) {
    h += sectionHeight(sec);
  }
  if (config.footer) h += 70;
  h += 60;
  return h;
}

// ===== 主入口 =====

function buildPoster(config) {
  const W = config.width || W_DEFAULT;
  const totalH = config.height || calcTotalHeight(config);

  const canvas = createCanvas(W, totalH);
  const ctx = canvas.getContext('2d');
  let y = 0;

  ctx.fillStyle = config.bg || C.bg;
  ctx.fillRect(0, 0, W, totalH);

  if (config.header) {
    const h = config.header;
    const grad = ctx.createLinearGradient(0, 0, W, 120);
    grad.addColorStop(0, h.bg || C.headerGrad1);
    grad.addColorStop(1, h.bgEnd || C.headerGrad2);
    ctx.fillStyle = grad;
    ctx.fillRect(0, y, W, 120);

    ctx.fillStyle = C.white;
    ctx.font = `bold 32px "${FONT}"`;
    ctx.textAlign = 'center';
    ctx.fillText(txt(h.title), W / 2, y + 50);

    if (h.subtitle) {
      ctx.font = `18px "${FONT}"`;
      ctx.fillStyle = 'rgba(255,255,255,0.85)';
      ctx.fillText(txt(h.subtitle), W / 2, y + 82);
    }
    ctx.textAlign = 'left';
    y += 120;
  }

  for (const sec of config.sections || []) {
    y = drawSection(ctx, sec, y, W);
  }

  if (config.footer) {
    y += 10;
    ctx.fillStyle = 'rgba(0,0,0,0.4)';
    ctx.fillRect(0, y, W, 45);
    ctx.font = `12px "${FONT}"`;
    ctx.fillStyle = C.subtle;
    ctx.textAlign = 'center';
    ctx.fillText(txt(config.footer), W / 2, y + 28);
  }

  const result = { canvas, width: W, height: totalH };

  if (config.output) {
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync(config.output, buffer);
    result.buffer = buffer;
    result.output = config.output;
  }

  return result;
}

// ===== CLI 模式 =====

if (require.main === module) {
  const configPath = process.argv[2];
  const outputPath = process.argv[3] || '/tmp/poster.png';

  if (!configPath) {
    console.error('Usage: node builder.js <config.json> [output.png]');
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  config.output = config.output || outputPath;
  const { width, height, buffer } = buildPoster(config);

  console.log(JSON.stringify({
    success: true,
    output: config.output,
    width,
    height,
    size: `${(buffer.length / 1024).toFixed(1)} KB`,
  }));
}

module.exports = { buildPoster, calcTotalHeight, sectionHeight, drawSection };
