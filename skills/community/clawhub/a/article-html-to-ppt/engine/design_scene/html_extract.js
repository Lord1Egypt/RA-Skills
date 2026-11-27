// PPT Smith fixed layout extractor. Injected by `engine design html-import`; never authored per task.
// Reads the browser's computed layout of #slide and emits native-object candidates as JSON.
(function () {
  'use strict';
  const slide = document.getElementById('slide');
  const out = { version: 1, items: [], warnings: [] };
  if (!slide) { out.error = 'SLIDE_ROOT_MISSING'; return finish(); }
  const S = slide.getBoundingClientRect();
  out.width = S.width; out.height = S.height;
  out.background = getComputedStyle(slide).backgroundColor;
  const R = (r) => ({ x: r.left - S.left, y: r.top - S.top, w: r.width, h: r.height });
  const visible = (c) => !!c && c !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(c);
  const warn = (code, el) => out.warnings.push({ code, at: describe(el) });
  function describe(el) {
    if (!el || !el.tagName) return '';
    const r = el.getBoundingClientRect();
    return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '') +
      ' @' + Math.round(r.left - S.left) + ',' + Math.round(r.top - S.top);
  }
  function attrUp(el, name) {
    for (let e = el; e && e !== document.body; e = e.parentElement) if (e.hasAttribute && e.hasAttribute(name)) return e.getAttribute(name);
    return null;
  }
  function attrUpTo(el, stop, name) {
    for (let e = el; e && e !== stop && e !== document.body; e = e.parentElement) {
      if (e.hasAttribute && e.hasAttribute(name)) return e.getAttribute(name);
    }
    return null;
  }
  function cornerRadius(value, w, h) {
    if (!value) return 0;
    const parts = String(value).trim().split(/\s+/);
    const rx = parts[0].endsWith('%') ? (parseFloat(parts[0]) / 100) * w : parseFloat(parts[0]);
    const rawY = parts[1] || parts[0];
    const ry = rawY.endsWith('%') ? (parseFloat(rawY) / 100) * h : parseFloat(rawY);
    return Number.isFinite(rx) && Number.isFinite(ry) ? Math.min(rx, ry) : 0;
  }
  const font = (cs) => ({
    stack: cs.fontFamily.split(',').map(s => s.replace(/["']/g, '').trim()).filter(Boolean),
    size: parseFloat(cs.fontSize), weight: parseInt(cs.fontWeight, 10), italic: cs.fontStyle === 'italic',
    color: cs.color, letterSpacing: cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing),
    lineHeight: cs.lineHeight === 'normal' ? parseFloat(cs.fontSize) * 1.3 : parseFloat(cs.lineHeight),
  });
  const isInline = (el) => ['inline', 'contents'].includes(getComputedStyle(el).display) &&
    !el.matches('svg, [data-asset], [data-chart]');
  const hasOwnText = (el) => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  // Only fold uninterrupted inline text. A named or painted child remains its own object.
  function plainInline(el) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none') return true;
    return isInline(el) && !el.matches('[data-cid], [data-src], [data-authored]') &&
      !visible(cs.backgroundColor) && !['Top', 'Right', 'Bottom', 'Left'].some(s => parseFloat(cs['border' + s + 'Width']) > 0) &&
      [...el.children].every(plainInline);
  }

  function runsOf(el, cell = false) {
    const runs = [];
    const cs = getComputedStyle(el);
    for (const n of el.childNodes) {
      if (n.nodeType === 3) {
        if (cs.visibility === 'visible' && n.textContent.length) {
          runs.push({ text: n.textContent.replace(/[ \t\r\n\f]+/g, ' '), ...font(cs) });
        }
        continue;
      }
      if (n.nodeType !== 1 || getComputedStyle(n).display === 'none') continue;
      if (n.localName === 'br') runs.push({ text: '\n', ...font(cs) });
      else if (isInline(n)) runs.push(...runsOf(n, cell));
      else if (cell && n.matches('p,div')) runs.push(null, ...runsOf(n, true), null);
      else if (cell) warn('TABLE_CELL_ELEMENT_UNSUPPORTED', n);
    }
    return runs;
  }
  function trimRuns(runs) {
    // HTML collapses spaces across inline boundaries and trims them at hard line breaks.
    let previous = null;
    for (const run of runs) {
      if (run.text === '\n') {
        if (previous) previous.text = previous.text.replace(/ +$/, '');
        previous = null;
      } else {
        if (!previous || previous.text.endsWith(' ')) run.text = run.text.replace(/^ +/, '');
        if (run.text) previous = run;
      }
    }
    if (previous) previous.text = previous.text.replace(/ +$/, '');
    return runs.filter(r => r.text.length);
  }
  function cellRuns(td) {
    // Block paragraphs delimit editable lines; adjacent block boundaries give a single break.
    const result = [], inline = [];
    for (const run of [...runsOf(td, true), null]) {
      if (run !== null) { inline.push(run); continue; }
      const paragraph = trimRuns(inline);
      if (paragraph.length) {
        if (result.length) result.push({ ...paragraph[0], text: '\n' });
        result.push(...paragraph);
      }
      inline.length = 0;
    }
    return result;
  }
  function meta(el) {
    return { cid: el.getAttribute('data-cid'), src: attrUp(el, 'data-src'), authored: attrUp(el, 'data-authored') };
  }
  function textRects(el) {
    const rects = [];
    function visit(node) {
      const cs = getComputedStyle(node);
      for (const n of node.childNodes) {
        if (n.nodeType === 3) {
          if (cs.visibility === 'visible' && n.textContent.trim()) {
            const rg = document.createRange();
            rg.selectNodeContents(n);
            for (const r of rg.getClientRects()) if (r.width > 0.5 && r.height > 0.5) rects.push(r);
          }
        } else if (n.nodeType === 1 && getComputedStyle(n).display !== 'none' && isInline(n)) {
          visit(n);
        }
      }
    }
    visit(el);
    return rects;
  }
  function unionRect(rects) {
    const left = Math.min(...rects.map(r => r.left)), top = Math.min(...rects.map(r => r.top));
    const right = Math.max(...rects.map(r => r.right)), bottom = Math.max(...rects.map(r => r.bottom));
    return { left, top, right, bottom, width: right - left, height: bottom - top };
  }
  function textItem(el) {
    const cs = getComputedStyle(el);
    const rects = textRects(el);
    if (!rects.length) return null;
    const lh = font(cs).lineHeight; const lines = [];
    rects.map(r => (r.top + r.bottom) / 2).sort((a, b) => a - b).forEach(c => { if (!lines.length || c - lines[lines.length - 1] > lh * 0.6) lines.push(c); });
    const u = unionRect(rects), er = el.getBoundingClientRect();
    const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth), pr = parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth);
    const runs = trimRuns(runsOf(el));
    if (!runs.length) return null;
    if (cs.writingMode && !cs.writingMode.startsWith('horizontal')) warn('VERTICAL_WRITING_MODE_UNSUPPORTED', el);
    return { kind: 'text', ...R(u), lines: lines.length, container: container(el),
      overflow: { x: el.scrollWidth - el.clientWidth, y: el.scrollHeight - el.clientHeight }, align: (cs.textAlign === 'start' || cs.textAlign === 'justify') ? 'left' : cs.textAlign === 'end' ? 'right' : cs.textAlign,
      content: { x: er.left + pl - S.left, w: er.width - pl - pr }, runs, lineHeight: lh, ...meta(el) };
  }
  // Nearest painted ancestor (card, panel, chip): text should stay inside it.
  function container(el) {
    for (let e = el.parentElement; e && e !== slide; e = e.parentElement) {
      const cs = getComputedStyle(e);
      const bordered = ['Top', 'Right', 'Bottom', 'Left'].some(s => cs['border' + s + 'Style'] !== 'none' && parseFloat(cs['border' + s + 'Width']) > 0);
      if (visible(cs.backgroundColor) || bordered) return R(e.getBoundingClientRect());
    }
    return null;
  }
  function checkStyle(el, cs) {
    if (cs.backgroundImage && cs.backgroundImage !== 'none') warn('CSS_BACKGROUND_IMAGE_UNSUPPORTED', el);
    if (cs.boxShadow && cs.boxShadow !== 'none') warn('CSS_SHADOW_IGNORED', el);
    if (cs.transform && cs.transform !== 'none') warn('CSS_TRANSFORM_UNSUPPORTED', el);
    if (parseFloat(cs.opacity) < 0.999) warn('CSS_OPACITY_IGNORED_USE_RGBA', el);
    if (cs.overflow === 'hidden' && el !== slide && el.scrollHeight > el.clientHeight + 1) warn('CONTENT_CLIPPED_BY_OVERFLOW', el);
  }
  function boxItem(el) {
    const cs = getComputedStyle(el);
    checkStyle(el, cs);
    const sides = ['Top', 'Right', 'Bottom', 'Left'].map(s => ({ w: parseFloat(cs['border' + s + 'Width']), c: cs['border' + s + 'Color'], st: cs['border' + s + 'Style'] }));
    const borders = sides.map(b => (b.st !== 'none' && b.w > 0 && visible(b.c)) ? { w: b.w, c: b.c } : null);
    if (!visible(cs.backgroundColor) && !borders.some(Boolean)) return null;
    const rect = el.getBoundingClientRect();
    const radius = ['TopLeft', 'TopRight', 'BottomRight', 'BottomLeft']
      .map(k => cornerRadius(cs['border' + k + 'Radius'], rect.width, rect.height));
    return { kind: 'box', ...R(rect), fill: visible(cs.backgroundColor) ? cs.backgroundColor : null, borders, radius };
  }
  function tableItem(t) {
    const rows = [...t.rows].map(tr => {
      const trBg = getComputedStyle(tr).backgroundColor;
      return { h: tr.getBoundingClientRect().height, cells: [...tr.cells].map(td => {
        const cs = getComputedStyle(td);
        const bounds = td.getBoundingClientRect();
        const groupRowsLeft = tr.parentElement.rows.length - tr.sectionRowIndex;
        const borders = {};
        for (const side of ['Left', 'Right', 'Top', 'Bottom']) {
          const width = parseFloat(cs['border' + side + 'Width']), color = cs['border' + side + 'Color'];
          if (width > 0 && visible(color) && !['none', 'hidden'].includes(cs['border' + side + 'Style'])) {
            borders[side.toLowerCase()] = { w: width, c: color };
            if (cs['border' + side + 'Style'] !== 'solid') warn('TABLE_BORDER_STYLE_RENDERED_SOLID', td);
          }
        }
        const cellAuthored = attrUpTo(td, t, 'data-authored');
        return { x: bounds.left - S.left, w: bounds.width, colSpan: td.colSpan,
          rowSpan: Math.min(td.rowSpan || groupRowsLeft, groupRowsLeft), borders,
          runs: cellRuns(td), font: font(cs),
          align: (cs.textAlign === 'start' || cs.textAlign === 'justify') ? 'left' : cs.textAlign === 'end' ? 'right' : cs.textAlign,
          valign: cs.verticalAlign === 'top' ? 'top' : cs.verticalAlign === 'bottom' ? 'bottom' : 'middle',
          fill: visible(cs.backgroundColor) ? cs.backgroundColor : (visible(trBg) ? trBg : null),
          pad: [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].map(parseFloat),
          ...(cellAuthored !== null ? { authored: cellAuthored } : {}) };
      }) };
    });
    return { kind: 'table', ...R(t.getBoundingClientRect()), rows, ...meta(t) };
  }
  function roundedPath(box, rx, ry) {
    const {x, y, width, height} = box, right = x + width, bottom = y + height;
    rx = Math.min(rx, width / 2); ry = Math.min(ry, height / 2);
    if (!rx || !ry) return 'M ' + [x,y] + ' H ' + right + ' V ' + bottom + ' H ' + x + ' Z';
    // Four cubic quarter-ellipses, including the circle and stadium cases.
    const k = 4 * (Math.sqrt(2) - 1) / 3, dx = rx * (1 - k), dy = ry * (1 - k);
    return [
      'M', x + rx, y, 'H', right - rx, 'C', right - dx, y, right, y + dy, right, y + ry,
      'V', bottom - ry, 'C', right, bottom - dy, right - dx, bottom, right - rx, bottom,
      'H', x + rx, 'C', x + dx, bottom, x, bottom - dy, x, bottom - ry,
      'V', y + ry, 'C', x, y + dy, x + dx, y, x + rx, y, 'Z'
    ].join(' ');
  }
  function geometryPath(el, cs) {
    const tag = el.localName;
    if (tag === 'path') return el.getAttribute('d');
    if (tag === 'line') return ['M', el.x1.baseVal.value, el.y1.baseVal.value,
      'L', el.x2.baseVal.value, el.y2.baseVal.value].join(' ');
    if (tag === 'polygon' || tag === 'polyline') {
      const points = Array.from(el.points, p => p.x + ',' + p.y);
      return points.length < 2 ? null : 'M' + points.join(' L') + (tag === 'polygon' ? ' Z' : '');
    }
    if (tag === 'circle' || tag === 'ellipse' || tag === 'rect') {
      const box = el.getBBox();
      if (!box.width || !box.height) return null;
      if (tag !== 'rect') return roundedPath(box, box.width / 2, box.height / 2);
      // The browser resolves SVG length attributes in the element's coordinate system.
      const length = prop => cs[prop].endsWith('px') ? parseFloat(cs[prop]) : el[prop].baseVal.value;
      const rx = cs.rx === 'auto' ? length('ry') : length('rx');
      const ry = cs.ry === 'auto' ? rx : length('ry');
      return roundedPath(box, rx, ry);
    }
    warn('SVG_ELEMENT_IGNORED_USE_PATH', el);
    return null;
  }
  function svgItems(svg) {
    const result = [];
    function visit(el) {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || el.localName === 'defs') return;
      if (el.localName === 'g') { for (const child of el.children) visit(child); return; }
      if (cs.visibility === 'hidden') return;
      const d = geometryPath(el, cs), m = el.getScreenCTM?.();
      if (!d || !m) return;
      const scale = cs.vectorEffect === 'non-scaling-stroke' ? 1 : Math.sqrt(Math.abs(m.a*m.d - m.b*m.c));
      result.push({ kind: 'path', ox: m.e - S.left, oy: m.f - S.top, matrix: [m.a, m.b, m.c, m.d], d,
        fill: cs.fill === 'none' ? null : cs.fill, fillOpacity: parseFloat(cs.fillOpacity),
        stroke: cs.stroke === 'none' ? null : cs.stroke, strokeWidth: parseFloat(cs.strokeWidth) * scale,
        strokeOpacity: parseFloat(cs.strokeOpacity) });
    }
    for (const child of svg.children) visit(child);
    return result;
  }
  function inlineDecorations(el) {
    for (const c of el.children) {
      if (getComputedStyle(c).display === 'none' || !isInline(c)) continue;
      if (c.matches('[data-cid], [data-authored]')) warn('INLINE_METADATA_IGNORED_IN_TEXT_BLOCK', c);
      const b = boxItem(c);
      if (b) out.items.push(b);
      inlineDecorations(c);
    }
  }
  function walk(el) {
    const tag = el.tagName.toLowerCase();
    if (tag === 'script' || tag === 'style') return;
    if (getComputedStyle(el).display === 'none' || getComputedStyle(el).visibility === 'hidden') return;
    if (el.hasAttribute('data-asset')) {
      const cs = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      const layer = (el.getAttribute('data-image-layer') || '').trim().toLowerCase() || null;
      out.items.push({ kind: 'image', ...R(rect), asset: el.getAttribute('data-asset'),
        fit: el.getAttribute('data-fit') || 'contain',
        radius: cornerRadius(cs.borderTopLeftRadius, rect.width, rect.height),
        ...(layer ? { layer } : {}), ...meta(el) });
      return;
    }
    if (el.hasAttribute('data-chart')) {
      let spec = null;
      try { spec = JSON.parse(el.getAttribute('data-chart')); } catch (e) { warn('CHART_SPEC_INVALID_JSON', el); return; }
      out.items.push({ kind: 'chart', ...R(el.getBoundingClientRect()), spec, ...meta(el) }); return;
    }
    if (tag === 'table') { const b = boxItem(el); if (b) out.items.push(b); out.items.push(tableItem(el)); return; }
    if (tag === 'svg') { if (el.hasAttribute('data-native-svg')) out.items.push(...svgItems(el)); else warn('SVG_WITHOUT_NATIVE_MARKER_IGNORED', el); return; }
    if (el !== slide) { const b = boxItem(el); if (b) out.items.push(b); }
    const own = hasOwnText(el) || (el !== slide && el.children.length > 0 && [...el.children].every(plainInline));
    if (own) {
      inlineDecorations(el);
      const t = textItem(el);
      if (t) out.items.push(t);
    }
    for (const c of el.children) { if (own && isInline(c)) continue; walk(c); }
  }
  function finish() {
    const pre = document.createElement('pre'); pre.id = '__pptsmith_layout'; pre.style.display = 'none';
    pre.textContent = JSON.stringify(out); document.body.appendChild(pre);
  }
  // data-chart is validated by the importer. SVG nodes are tool-owned; labels are literal text.
  function drawChartPreview(el) {
    if (el.children.length || !el.clientWidth || !el.clientHeight) return;
    const spec = JSON.parse(el.getAttribute('data-chart'));
    const cats = spec.categories, series = spec.series;
    if (!Array.isArray(cats) || !cats.length || cats.length > 200 || !Array.isArray(series)
        || !series.length || series.length > 20 || series.some(s => !Array.isArray(s.values)
          || s.values.length !== cats.length || !s.values.every(v => Number.isFinite(Number(v))))) {
      throw new Error('invalid chart data');
    }
    const W = el.clientWidth, H = el.clientHeight;
    const sector = spec.type === 'pie' || spec.type === 'doughnut';
    const palette = spec.colors || (sector && !series[0].color
      ? ['4B4FD6', 'F2804F', '2BB9A9', 'A473D9', 'E0B23F', '688DC4']
      : series.map(s => s.color || '4B4FD6'));
    const color = (i, colors = palette) => {
      const hex = colors[i % colors.length];
      return /^#?[0-9a-f]{6}$/i.test(hex) ? '#' + hex.replace(/^#/, '') : '#4B4FD6';
    };
    const contrastInk = (hex) => {
      const h = hex.replace(/^#/, '');
      const [r, g, b] = [0, 2, 4].map(i => {
        const c = parseInt(h.slice(i, i + 2), 16) / 255;
        return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
      });
      return (0.2126 * r + 0.7152 * g + 0.0722 * b) > 0.36 ? '#1E2235' : '#ffffff';
    };
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('width', W);
    svg.setAttribute('height', H);
    svg.style.fontFamily = spec.font || getComputedStyle(slide).fontFamily;
    function draw(tag, attrs) {
      const node = document.createElementNS(ns, tag);
      for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
      svg.appendChild(node);
      return node;
    }
    function label(x, y, value, fill, anchor = 'middle', size = spec.font_size || 9) {
      draw('text', { x, y, fill, 'font-size': size, 'text-anchor': anchor }).textContent = String(value);
    }
    // Common Excel numeric masks. The exact original format always goes to the native chart.
    const labelFormat = spec.label_number_format || 'General';
    const numberMask = /^(#,##)?0(?:\.(0{1,12}))?(%)?$/.exec(labelFormat);
    if (spec.labels !== false && labelFormat.toLowerCase() !== 'general' && !numberMask) {
      warn('CHART_LABEL_FORMAT_NATIVE_PREVIEW_REQUIRED', el);
    }
    function formatWith(value, mask) {
      if (!mask) return String(value);
      const digits = (mask[2] || '').length;
      return (value * (mask[3] ? 100 : 1)).toLocaleString('en-US', {
        useGrouping: !!mask[1], minimumFractionDigits: digits, maximumFractionDigits: digits
      }) + (mask[3] || '');
    }
    const format = value => formatWith(value, numberMask);
    const axisFormatRaw = (spec.axis && spec.axis.number_format) || spec.axis_number_format || 'General';
    const axisMask = /^(#,##)?0(?:\.(0{1,12}))?(%)?$/.exec(axisFormatRaw);
    const rightLegend = spec.legend && spec.legend_position === 'right';
    const plotW = rightLegend ? W * 0.74 : W;
    const plotH = spec.legend && !rightLegend ? H * 0.83 : H;
    if (spec.legend) {
      const names = sector ? cats : series.map(s => s.name);
      names.forEach((name, i) => {
        const x = rightLegend ? plotW + 3 : i * W / names.length + 4;
        const y = rightLegend ? 8 + i * Math.min(16, (H - 8) / names.length) : plotH + (H - plotH) / 2;
        draw('rect', { x, y, width: 7, height: 7, fill: color(i) });
        label(x + 10, y + 7, name, '#555968', 'start');
      });
    }
    if (sector) {
      const values = series[0].values.map(Number);
      const total = values.reduce((sum, v) => sum + v, 0);
      const cx = plotW / 2, cy = plotH / 2, outer = Math.min(cx, cy) * 0.90;
      const inner = spec.type === 'doughnut' ? outer * (spec.hole_size || 50) / 100 : 0;
      const r = (outer + inner) / 2, stroke = outer - inner, perimeter = 2 * Math.PI * r;
      let angle = -Math.PI / 2;
      values.forEach((v, i) => {
        if (!v) return;
        const fraction = v / total;
        const arc = { cx, cy, r, fill: 'none', stroke: color(i), 'stroke-width': stroke };
        if (fraction < 1) {
          arc['stroke-dasharray'] = (perimeter * fraction) + ' ' + perimeter;
          arc.transform = 'rotate(' + (angle * 180 / Math.PI) + ' ' + cx + ' ' + cy + ')';
        }
        draw('circle', arc);
        angle += 2 * Math.PI * fraction;
      });
      if (spec.labels !== false) {
        angle = -Math.PI / 2;
        values.forEach((v, i) => {
          if (!v) return;
          const half = Math.PI * v / total, mid = angle + half;
          label(cx + r * Math.cos(mid), cy + r * Math.sin(mid) + 3, format(v),
            spec.label_colors ? color(i, spec.label_colors) : '#A0A4B8');
          angle += 2 * half;
        });
      }
    } else {
      const axis = { ...spec, ...spec.axis };
      const stacked = spec.type === 'stacked_column' || spec.type === 'stacked_bar';
      const horiz = spec.type === 'bar' || spec.type === 'stacked_bar';
      let all = series.flatMap(s => s.values.map(Number));
      if (stacked) {
        const pos = cats.map((_, i) => series.reduce((a, s) => a + Math.max(0, Number(s.values[i])), 0));
        const neg = cats.map((_, i) => series.reduce((a, s) => a + Math.min(0, Number(s.values[i])), 0));
        all = [...pos, ...neg];
      }
      let lo = axis.min ?? Math.min(0, ...all), hi = axis.max ?? Math.max(0, ...all);
      if (hi <= lo) {
        if (axis.max !== undefined) lo = hi - 1;
        else hi = lo + 1;
      }
      const range = hi - lo, step = axis.major ?? range / 4;
      const V = v => Math.max(0, Math.min(1, (v - lo) / range));
      const pl = horiz ? Math.min(64, plotW / 4) : Math.min(38, plotW / 4), pt = 16;
      const iw = Math.max(1, plotW - pl - 12), ih = Math.max(1, plotH - pt - 24);
      const slot = (horiz ? ih : iw) / cats.length, baseline = V(0);
      const axisColor = '#' + (axis.label_color || 'A0A4B8');
      const gridColor = '#' + (axis.gridline_color || 'EDEFF5');
      const ticks = Math.min(200, Math.floor(range / step + 1e-9));
      for (let i = 0; i <= ticks; i++) {
        const t = lo + i * step, x = pl + V(t) * iw, y = pt + (1 - V(t)) * ih;
        draw('line', horiz ? { x1: x, x2: x, y1: pt, y2: pt + ih, stroke: gridColor }
                           : { x1: pl, x2: pl + iw, y1: y, y2: y, stroke: gridColor });
        const tickText = axisMask ? formatWith(t, axisMask) : +t.toPrecision(8);
        label(horiz ? x : pl - 5, horiz ? plotH - 6 : y + 3, tickText, axisColor,
          horiz ? 'middle' : 'end', axis.label_size || 8);
      }
      const mid = i => (horiz ? pt : pl) + slot * (i + 0.5);
      cats.forEach((c, i) => label(horiz ? pl - 5 : mid(i), horiz ? mid(i) + 3 : plotH - 6,
        c, axisColor, horiz ? 'end' : 'middle', axis.label_size || 8));
      const posStack = cats.map(() => 0), negStack = cats.map(() => 0);
      series.forEach((s, si) => {
        const values = s.values.map(Number), ink = color(si);
        if (!spec.type || spec.type === 'line') {
          const pts = values.map((v, i) => [mid(i), pt + (1 - V(v)) * ih]);
          const path = 'M' + pts.map(p => p.join(',')).join(' L');
          if (s.area) {
            const baseY = pt + (1 - baseline) * ih;
            draw('path', { d: path + ' L' + mid(cats.length - 1) + ',' + baseY + ' L' + mid(0) + ',' + baseY + ' Z',
              fill: ink, 'fill-opacity': 0.12 });
          }
          draw('path', { d: path, fill: 'none', stroke: ink, 'stroke-width': 2 });
          pts.forEach(([x, y], i) => {
            if (spec.markers !== false) draw('circle', { cx: x, cy: y, r: 2.6, fill: '#fff', stroke: ink });
            if (spec.labels !== false) label(x, y - 6, format(values[i]), ink);
          });
        } else if (stacked) {
          const bw = slot / (1 + (spec.gap_width ?? 100) / 100);
          values.forEach((v, i) => {
            const base = v >= 0 ? posStack[i] : negStack[i];
            const next = base + v;
            if (v >= 0) posStack[i] = next; else negStack[i] = next;
            const a = V(base), b = V(next), len = Math.abs(b - a);
            const off = mid(i) - bw / 2;
            draw('rect', horiz ? { x: pl + Math.min(a, b) * iw, y: off, width: len * iw, height: bw, fill: ink }
                               : { x: off, y: pt + (1 - Math.max(a, b)) * ih, width: bw, height: len * ih, fill: ink });
            if (spec.labels !== false && v !== 0) {
              const cx = horiz ? pl + ((a + b) / 2) * iw : off + bw / 2;
              const cy = horiz ? off + bw / 2 + 3 : pt + (1 - (a + b) / 2) * ih + 3;
              label(cx, cy, format(v), contrastInk(ink));
            }
          });
        } else {
          const bars = slot * series.length / (series.length + (spec.gap_width ?? 100) / 100);
          const bw = bars / series.length;
          values.forEach((v, i) => {
            const off = mid(i) - bars / 2 + bw * si;
            const end = V(v), len = Math.abs(end - baseline);
            draw('rect', horiz ? { x: pl + Math.min(end, baseline) * iw, y: off, width: len * iw, height: bw, fill: ink }
                               : { x: off, y: pt + (1 - Math.max(end, baseline)) * ih, width: bw, height: len * ih, fill: ink });
            if (spec.labels !== false) label(horiz ? pl + end * iw : off + bw / 2,
              horiz ? off + bw / 2 + 3 : pt + (1 - end) * ih - 4, format(v), ink);
          });
        }
      });
    }
    el.appendChild(svg);
  }
  for (const el of slide.querySelectorAll('[data-chart]')) {
    try { drawChartPreview(el); } catch (e) { warn('CHART_PREVIEW_FAILED', el); }
  }
  document.fonts.ready.then(() => { try { walk(slide); } catch (e) { out.error = 'EXTRACT_FAILED: ' + e; } finish(); });
})();
