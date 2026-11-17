(function () {
  window.CPM = window.CPM || {};
  window.AutoArticle = window.AutoArticle || {};
  window.AutoArticle.plugins = window.AutoArticle.plugins || {};
})();

function createMarkdownParser() {
  const hljs = window.hljs;
  const parser = new window.markdownit({
    html: true,
    linkify: true,
    typographer: true,
    highlight: function (str, lang) {
      if (lang === undefined || lang === "") lang = "bash";
      if (lang && hljs && hljs.getLanguage(lang)) {
        try {
          const formatted = hljs.highlight(str, { language: lang, ignoreIllegals: true }).value;
          return '<pre class="custom"><code class="hljs">' + formatted + '</code></pre>';
        } catch (e) {}
      }
      return '<pre class="custom"><code class="hljs">' + parser.utils.escapeHtml(str) + '</code></pre>';
    },
  });

  const plugins = window.AutoArticle ? window.AutoArticle.plugins : {};
  if (plugins.markdownitSpan) parser.use(plugins.markdownitSpan);
  if (plugins.markdownItUrlAddSpan) parser.use(plugins.markdownItUrlAddSpan);
  if (plugins.markdownItTableContainer) parser.use(plugins.markdownItTableContainer);
  if (plugins.markdownItMath) parser.use(plugins.markdownItMath);
  if (plugins.markdownItLiReplacer) parser.use(plugins.markdownItLiReplacer);
  if (plugins.markdownItImageFlow) parser.use(plugins.markdownItImageFlow);
  if (plugins.markdownItLinkfoot) parser.use(plugins.markdownItLinkfoot);
  if (plugins.markdownitRuby) parser.use(plugins.markdownitRuby);
  if (plugins.markdownitImplicitFigures) parser.use(plugins.markdownitImplicitFigures, { figcaption: true });
  if (plugins.markdownitDeflist) parser.use(plugins.markdownitDeflist);

  return parser;
}

function renderToHtml(markdown) {
  const parser = createMarkdownParser();
  return parser.render(markdown);
}

function cleanMathElements(html) {
  const div = document.createElement("div");
  div.innerHTML = html;
  const mjxs = div.getElementsByTagName("mjx-container");
  for (let i = 0; i < mjxs.length; i++) {
    const mjx = mjxs[i];
    if (!mjx.hasAttribute("jax")) break;
    mjx.removeAttribute("jax");
    mjx.removeAttribute("display");
    mjx.removeAttribute("tabindex");
    mjx.removeAttribute("ctxtmenu_counter");
    const svg = mjx.firstChild;
    if (svg) {
      const width = svg.getAttribute("width");
      const height = svg.getAttribute("height");
      svg.removeAttribute("width");
      svg.removeAttribute("height");
      svg.style.width = width;
      svg.style.height = height;
    }
  }
  let result = div.innerHTML;
  result = result.replace(/<mjx-container (class="inline.+?)<\/mjx-container>/g, "<span $1</span>");
  result = result.replace(/\s<span class="inline/g, "&nbsp;<span class=\"inline");
  result = result.replace(/svg><\/span>\s/g, "svg></span>&nbsp;");
  result = result.replace(/mjx-container/g, "section");
  result = result.replace(/class="mjx-solid"/g, 'fill="none" stroke-width="70"');
  result = result.replace(/<mjx-assistive-mml.+?<\/mjx-assistive-mml>/g, "");
  return result;
}

let _mermaidInitialized = false;
function ensureMermaid() {
  if (_mermaidInitialized || !window.mermaid) return;
  try {
    window.mermaid.initialize({
      startOnLoad: false,
      theme: 'default',
      securityLevel: 'strict',
    });
    _mermaidInitialized = true;
  } catch (e) {
    console.warn('[Mermaid] init failed:', e.message);
  }
}

// 本地浏览器端渲染 Mermaid（不依赖任何外部服务），与预览自身一样完全在用户机器上运行
async function renderMermaidBlockLocal(content) {
  ensureMermaid();
  if (!window.mermaid || !window.mermaid.render) {
    console.warn('[Mermaid] library not available');
    return null;
  }
  try {
    const id = 'mermaid-' + Math.random().toString(36).slice(2, 10);
    const result = await window.mermaid.render(id, content);
    const svg = typeof result === 'string' ? result : (result && result.svg);
    return svg || null;
  } catch (e) {
    console.warn('[Mermaid] render error:', e.message);
    return null;
  }
}

async function renderMermaidBlocks(container) {
  const blocks = container.querySelectorAll('code.language-mermaid');
  if (!blocks.length) return;
  const renders = [];
  for (let i = 0; i < blocks.length; i++) {
    const code = blocks[i];
    const content = code.textContent.trim();
    if (!content) continue;
    const pre = code.parentElement;
    renders.push(
      renderMermaidBlockLocal(content).then(svg => {
        if (svg) {
          const wrapper = document.createElement('div');
          wrapper.className = 'mermaid-svg';
          wrapper.innerHTML = svg;
          pre.parentElement.replaceChild(wrapper, pre);
        }
      })
    );
  }
  return Promise.all(renders);
}

function ensureFigureStyles(html) {
  const container = document.createElement("div");
  container.innerHTML = html;
  const figures = container.querySelectorAll("figure");
  for (const figure of figures) {
    applyStyle(figure, {
      display: "flex", flexDirection: "column",
      justifyContent: "center", alignItems: "center", margin: "10px 0",
    });
    const links = figure.querySelectorAll("a");
    for (const link of links) {
      applyStyle(link, {
        display: "flex", justifyContent: "center", alignItems: "center", border: "none",
      });
      const imgsInLink = link.querySelectorAll("img");
      for (const img of imgsInLink) {
        overrideStyle(img, { margin: "0" });
      }
    }
    const figcaptions = figure.querySelectorAll("figcaption");
    for (const figcaption of figcaptions) {
      applyStyle(figcaption, {
        display: "block", fontSize: "13px", color: "#2b2b2b",
        textAlign: "center", marginTop: "5px",
      });
    }
  }
  return container.innerHTML;
}

function applyStyle(element, styles) {
  const existing = element.getAttribute("style") || "";
  const existingProps = new Set(
    existing.split(";").map(s => s.split(":")[0].trim().toLowerCase()).filter(Boolean)
  );
  const newParts = [];
  for (const [prop, value] of Object.entries(styles)) {
    const kebab = camelToKebab(prop);
    if (!existingProps.has(kebab)) {
      newParts.push(kebab + ": " + value);
    }
  }
  if (newParts.length) {
    element.setAttribute("style", existing + (existing && !existing.endsWith(";") ? "; " : " ") + newParts.join("; "));
  }
}

function overrideStyle(element, overrides) {
  const existing = element.getAttribute("style") || "";
  let styleStr = existing;
  for (const [prop, value] of Object.entries(overrides)) {
    const kebab = camelToKebab(prop);
    const regex = new RegExp("(^|;\\s*)" + kebab + "\\s*:\\s*[^;]+", "i");
    if (regex.test(styleStr)) {
      styleStr = styleStr.replace(regex, "$1" + kebab + ": " + value);
    } else {
      styleStr += (styleStr && !styleStr.endsWith(";") ? "; " : " ") + kebab + ": " + value;
    }
  }
  element.setAttribute("style", styleStr);
}

function camelToKebab(str) {
  return str.replace(/[A-Z]/g, function (letter) { return "-" + letter.toLowerCase(); });
}

function convertPseudoElementsToRealNodes(element) {
  if (!element || element.nodeType !== Node.ELEMENT_NODE) return;
  const styleProps = [
    "color", "font-size", "font-weight", "line-height", "font-style",
    "display", "position", "float", "margin-top", "margin-right",
    "margin-bottom", "margin-left", "padding-top", "padding-right",
    "padding-bottom", "padding-left", "vertical-align"
  ];
  const beforeComputed = window.getComputedStyle(element, "::before");
  const beforeContent = beforeComputed.getPropertyValue("content");
  if (beforeContent && beforeContent !== "none" && beforeContent !== "normal" && beforeContent !== '""' && beforeContent !== "''") {
    const beforeSpan = document.createElement("span");
    beforeSpan.className = "pseudo-before";
    let styleStr = "";
    for (const prop of styleProps) {
      const val = beforeComputed.getPropertyValue(prop).trim();
      if (val && val !== "initial" && val !== "auto" && val !== "normal") {
        styleStr += prop + ": " + val + "; ";
      }
    }
    if (styleStr) beforeSpan.setAttribute("style", styleStr);
    let textContent = beforeContent.replace(/^["']|["']$/g, "");
    beforeSpan.textContent = textContent;
    element.insertBefore(beforeSpan, element.firstChild);
  }
  const afterComputed = window.getComputedStyle(element, "::after");
  const afterContent = afterComputed.getPropertyValue("content");
  if (afterContent && afterContent !== "none" && afterContent !== "normal" && afterContent !== '""' && afterContent !== "''") {
    const afterSpan = document.createElement("span");
    afterSpan.className = "pseudo-after";
    let styleStr = "";
    for (const prop of styleProps) {
      const val = afterComputed.getPropertyValue(prop).trim();
      if (val && val !== "initial" && val !== "auto" && val !== "normal") {
        styleStr += prop + ": " + val + "; ";
      }
    }
    if (styleStr) afterSpan.setAttribute("style", styleStr);
    let textContent = afterContent.replace(/^["']|["']$/g, "");
    afterSpan.textContent = textContent;
    element.appendChild(afterSpan);
  }
}

function convertAllPseudoElements(container) {
  const allElements = container.querySelectorAll("*");
  allElements.forEach(function (el) { convertPseudoElementsToRealNodes(el); });
  convertPseudoElementsToRealNodes(container);
}

function splitGradientTokens(str) {
  var tokens = [];
  var depth = 0;
  var current = "";
  for (var i = 0; i < str.length; i++) {
    var ch = str[i];
    if (ch === "(") { depth++; current += ch; }
    else if (ch === ")") { depth--; current += ch; }
    else if (ch === "," && depth === 0) { tokens.push(current.trim()); current = ""; }
    else { current += ch; }
  }
  if (current.trim()) tokens.push(current.trim());
  return tokens;
}

function matchStyleProperty(styleStr, propName) {
  var prefix = propName + ":";
  var startIdx = styleStr.indexOf(prefix);
  if (startIdx === -1) return null;
  var i = startIdx + prefix.length;
  while (i < styleStr.length && styleStr[i] === " ") i++;
  var value = "";
  var depth = 0;
  while (i < styleStr.length) {
    var ch = styleStr[i];
    if (ch === "(") { depth++; value += ch; }
    else if (ch === ")") { depth--; value += ch; }
    else if (ch === ";" && depth === 0) break;
    else { value += ch; }
    i++;
  }
  return value.trim() || null;
}

function convertLinearGradientToBase64Svg(cssValue, bgSize) {
  var gradients = [];
  var searchFrom = 0;
  while (true) {
    var funcStart = cssValue.indexOf("linear-gradient(", searchFrom);
    if (funcStart === -1) break;
    var depth = 1;
    var i = funcStart + "linear-gradient(".length;
    while (i < cssValue.length && depth > 0) {
      if (cssValue[i] === "(") depth++;
      else if (cssValue[i] === ")") depth--;
      i++;
    }
    gradients.push(cssValue.substring(funcStart, i));
    searchFrom = i;
  }
  if (gradients.length === 0) return null;

  var parsedGradients = gradients.map(function (g) {
    var inner = g.slice("linear-gradient(".length, -1);
    var tokens = splitGradientTokens(inner);
    var direction = tokens[0].trim();
    var colorStops = tokens.slice(1);
    var angle = 0;
    if (direction.endsWith("deg")) { angle = parseFloat(direction); }
    else if (direction === "to right") { angle = 90; }
    else if (direction === "to left") { angle = 270; }
    else if (direction === "to bottom") { angle = 180; }
    else if (direction === "to top") { angle = 0; }
    else { angle = 180; }
    var stops = colorStops.map(function (stop) {
      var s = stop.trim();
      var depth2 = 0;
      var colorEnd = s.length;
      for (var j = 0; j < s.length; j++) {
        if (s[j] === "(") depth2++;
        else if (s[j] === ")") depth2--;
        else if (depth2 === 0 && /\s/.test(s[j])) { colorEnd = j; break; }
      }
      var color = s.substring(0, colorEnd).trim();
      var offset = s.substring(colorEnd).trim();
      return { color: color, offset: offset || "" };
    });
    return { angle: angle, stops: stops };
  });

  var sizeParts = bgSize.trim().split(/\s+/);
  var svgWidth = parseFloat(sizeParts[0]) || 20;
  var svgHeight = parseFloat(sizeParts[1]) || svgWidth;

  if (parsedGradients.length === 2 && isGridPattern(parsedGradients)) {
    return generateGridSvg(parsedGradients, svgWidth, svgHeight);
  }

  function angleToSvgCoords(angleDeg, w, h) {
    var rad = ((angleDeg - 90) * Math.PI) / 180;
    var dx = Math.cos(rad);
    var dy = Math.sin(rad);
    var cx = w / 2;
    var cy = h / 2;
    var len = Math.max(w, h);
    return {
      x1: (cx - (dx * len) / 2).toFixed(2),
      y1: (cy - (dy * len) / 2).toFixed(2),
      x2: (cx + (dx * len) / 2).toFixed(2),
      y2: (cy + (dy * len) / 2).toFixed(2),
    };
  }

  var svgContent = '<svg xmlns="http://www.w3.org/2000/svg" width="' + svgWidth + '" height="' + svgHeight + '">';
  parsedGradients.forEach(function (g, idx) {
    var coords = angleToSvgCoords(g.angle, svgWidth, svgHeight);
    var gradId = 'g' + idx;
    svgContent += '<defs><linearGradient id="' + gradId + '" x1="' + coords.x1 + '" y1="' + coords.y1 + '" x2="' + coords.x2 + '" y2="' + coords.y2 + '">';
    g.stops.forEach(function (stop) {
      var offsetAttr = stop.offset ? ' offset="' + stop.offset + '"' : '';
      var rgbaMatch = stop.color.match(/^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)$/);
      if (rgbaMatch) {
        var r = rgbaMatch[1], g2 = rgbaMatch[2], b = rgbaMatch[3], a = rgbaMatch[4];
        svgContent += '<stop stop-color="rgb(' + r + ',' + g2 + ',' + b + ')"' + (a !== undefined ? ' stop-opacity="' + a + '"' : '') + offsetAttr + '/>';
      } else {
        svgContent += '<stop stop-color="' + stop.color + '"' + offsetAttr + '/>';
      }
    });
    svgContent += '</linearGradient></defs>';
    svgContent += '<rect width="100%" height="100%" fill="url(#' + gradId + ')"/>';
  });
  svgContent += '</svg>';

  var base64 = btoa(unescape(encodeURIComponent(svgContent)));
  return 'url("data:image/svg+xml;base64,' + base64 + '")';
}

function isGridPattern(parsedGradients) {
  if (parsedGradients.length !== 2) return false;
  var g1 = parsedGradients[0];
  var g2 = parsedGradients[1];
  var angleDiff = Math.abs(g1.angle - g2.angle);
  var isOrthogonal = Math.abs(angleDiff - 90) < 1 || Math.abs(angleDiff - 270) < 1;
  if (!isOrthogonal) return false;
  function isStripe(stops) {
    if (stops.length !== 2) return false;
    return stops[0].offset === stops[1].offset;
  }
  return isStripe(g1.stops) && isStripe(g2.stops);
}

function generateGridSvg(parsedGradients, svgWidth, svgHeight) {
  var horizontalGrad, verticalGrad;
  if (Math.abs(parsedGradients[0].angle - 90) < 1) {
    horizontalGrad = parsedGradients[0];
    verticalGrad = parsedGradients[1];
  } else {
    horizontalGrad = parsedGradients[1];
    verticalGrad = parsedGradients[0];
  }
  var hColor = horizontalGrad.stops[0].color;
  var hOffset = parseFloat(horizontalGrad.stops[0].offset) || 3;
  var vOffset = parseFloat(verticalGrad.stops[0].offset) || 3;
  function colorToSvg(color) {
    var rgbaMatch = color.match(/^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)$/);
    if (rgbaMatch) {
      return 'rgb(' + rgbaMatch[1] + ',' + rgbaMatch[2] + ',' + rgbaMatch[3] + ')';
    }
    return color;
  }
  function colorOpacity(color) {
    var rgbaMatch = color.match(/^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)$/);
    if (rgbaMatch && rgbaMatch[4] !== undefined) return rgbaMatch[4];
    return "1";
  }
  var lineColor = colorToSvg(hColor);
  var lineOpacity = colorOpacity(hColor);
  var vStrokeWidth = (svgWidth * hOffset) / 100;
  var hStrokeWidth = (svgHeight * vOffset) / 100;
  var svgContent = '<svg xmlns="http://www.w3.org/2000/svg" width="' + svgWidth + '" height="' + svgHeight + '">';
  svgContent += '<line x1="0" y1="0" x2="0" y2="' + svgHeight + '" stroke="' + lineColor + '" stroke-width="' + vStrokeWidth + '" stroke-opacity="' + lineOpacity + '"/>';
  svgContent += '<line x1="0" y1="0" x2="' + svgWidth + '" y2="0" stroke="' + lineColor + '" stroke-width="' + hStrokeWidth + '" stroke-opacity="' + lineOpacity + '"/>';
  svgContent += '</svg>';
  var base64 = btoa(unescape(encodeURIComponent(svgContent)));
  return 'url("data:image/svg+xml;base64,' + base64 + '")';
}

function convertGradientBackgroundsToSvg(container) {
  if (!container || container.nodeType !== Node.ELEMENT_NODE) return;
  var allElements = [container].concat(Array.from(container.querySelectorAll("*")));
  allElements.forEach(function (el) {
    var style = el.getAttribute("style") || "";
    var bgImage = matchStyleProperty(style, "background-image");
    if (!bgImage || !bgImage.includes("linear-gradient")) return;
    var bgSize = matchStyleProperty(style, "background-size") || "20px 20px";
    var bgPosition = matchStyleProperty(style, "background-position") || "center center";
    var bgRepeat = matchStyleProperty(style, "background-repeat") || "repeat";
    var svgDataUri = convertLinearGradientToBase64Svg(bgImage, bgSize);
    if (!svgDataUri) return;
    var bgSection = document.createElement("section");
    bgSection.setAttribute("style",
      "position: absolute; top: 0; left: 0; right: 0; bottom: 0; " +
      "background-image: " + svgDataUri + "; " +
      "background-size: " + bgSize + "; " +
      "background-position: " + bgPosition + "; " +
      "background-repeat: " + bgRepeat + "; " +
      "pointer-events: none; z-index: 0;");
    var existingStyle = el.getAttribute("style") || "";
    var newStyle = existingStyle
      .replace(/background-image:\s*[^;]+;?/g, "")
      .replace(/background-size:\s*[^;]+;?/g, "")
      .replace(/background-position:\s*[^;]+;?/g, "")
      .replace(/background-repeat:\s*[^;]+;?/g, "");
    if (!newStyle.includes("position:")) { newStyle += " position: relative;"; }
    else { newStyle = newStyle.replace(/position:\s*[^;]+;?/g, "position: relative;"); }
    if (!newStyle.includes("overflow:")) { newStyle += " overflow: hidden;"; }
    el.setAttribute("style", newStyle.trim());
    Array.from(el.children).forEach(function (child) {
      var childStyle = child.getAttribute("style") || "";
      if (!childStyle.includes("position:")) { child.setAttribute("style", childStyle + " position: relative;"); }
      if (!childStyle.includes("z-index:")) { child.setAttribute("style", (child.getAttribute("style") || "") + " z-index: 1;"); }
    });
    el.insertBefore(bgSection, el.firstChild);
  });
}

function getThemeCssText(themeName) {
  var cssText = "";
  for (var si = 0; si < document.styleSheets.length; si++) {
    var sheet = document.styleSheets[si];
    try {
      var isThemeSheet = sheet.href && sheet.href.indexOf("/" + themeName + ".css") >= 0;
      var isPreviewSheet = sheet.href && sheet.href.indexOf("preview.css") >= 0;
      var isCodeThemeSheet = sheet.href && sheet.href.indexOf("code-themes/") >= 0;
      if (isThemeSheet || isPreviewSheet || isCodeThemeSheet) {
        for (var ri = 0; ri < sheet.cssRules.length; ri++) {
          var rule = sheet.cssRules[ri];
          if (rule.selectorText && (rule.selectorText.indexOf("markdown-body") >= 0 ||
            rule.selectorText.indexOf("hljs") >= 0 || rule.selectorText.indexOf("custom") >= 0 ||
            rule.selectorText === ":root")) {
            cssText += rule.cssText + "\n";
          }
        }
      }
    } catch (e) {}
  }
  return cssText;
}

function inlineCssViaBrowser(html, cssText, themeClassName) {
  var tempDiv = document.createElement('div');
  tempDiv.style.cssText = 'position:absolute;left:-9999px;top:0;';
  tempDiv.innerHTML = html;
  if (themeClassName) {
    var body = tempDiv.querySelector('.markdown-body');
    if (body) body.classList.add(themeClassName);
  }
  var style = document.createElement('style');
  style.textContent = cssText;
  tempDiv.appendChild(style);
  document.body.appendChild(tempDiv);

  var propRe = /([\w-]+)\s*:\s*([^;]+);/g;
  var elementStyles = new Map();

  try {
    for (var r = 0; r < style.sheet.cssRules.length; r++) {
      var rule = style.sheet.cssRules[r];
      if (rule.type !== 1) continue;
      var selector = rule.selectorText;
      if (!selector) continue;
      var elements;
      try { elements = tempDiv.querySelectorAll(selector); } catch (e) { continue; }
      var bodyStart = rule.cssText.indexOf('{');
      var bodyEnd = rule.cssText.lastIndexOf('}');
      if (bodyStart === -1 || bodyEnd <= bodyStart) continue;
      var declText = rule.cssText.slice(bodyStart + 1, bodyEnd);
      for (var ei = 0; ei < elements.length; ei++) {
        var el = elements[ei];
        if (!elementStyles.has(el)) elementStyles.set(el, new Map());
        var elProps = elementStyles.get(el);
        propRe.lastIndex = 0;
        var m;
        while ((m = propRe.exec(declText)) !== null) {
          var prop = m[1].trim();
          var val = m[2].trim();
          if (prop !== 'content' && prop !== 'src' && val) {
            elProps.set(prop, val);
          }
        }
      }
    }

    elementStyles.forEach(function (props, el) {
      var prev = el.getAttribute('style') || '';
      var parts = [];
      props.forEach(function (val, prop) { parts.push(prop + ': ' + val); });
      if (parts.length) {
        el.setAttribute('style', prev + (prev && !prev.endsWith(';') ? '; ' : '') + parts.join('; ') + ';');
      }
    });

    var varEls = tempDiv.querySelectorAll('[style*="var("]');
    for (var vei = 0; vei < varEls.length; vei++) {
      var varEl = varEls[vei];
      var cur = varEl.getAttribute('style') || '';
      if (!cur.includes('var(')) continue;
      var computed = getComputedStyle(varEl);
      var resolved = cur.replace(/var\(\s*[^)]+\s*\)/g, function (match) {
        var varName = match.slice(4, -1).trim();
        return computed.getPropertyValue(varName) || match;
      });
      varEl.setAttribute('style', resolved);
    }
  } catch (e) {
    console.warn('[inlineCssViaBrowser] CSS rule parse failed:', e.message);
  }

  style.remove();
  var result = tempDiv.innerHTML;
  document.body.removeChild(tempDiv);
  return result;
}

async function copyRichText(md) {
  if (!md) throw new Error('内容为空');

  var html = renderToHtml(md);
  html = cleanMathElements(html);

  var mermaidDiv = document.createElement("div");
  mermaidDiv.style.cssText = "position:absolute;left:-9999px;top:0;";
  mermaidDiv.innerHTML = html;
  document.body.appendChild(mermaidDiv);
  await renderMermaidBlocks(mermaidDiv);
  html = mermaidDiv.innerHTML;
  document.body.removeChild(mermaidDiv);

  html = '<div class="markdown-body">' + html + '</div>';

  var themeSelect = document.getElementById('previewStyleSelect');
  var themeKey = themeSelect ? themeSelect.value : 'docsify';
  var cssText = getThemeCssText(themeKey);
  if (cssText) {
    try {
      html = inlineCssViaBrowser(html, cssText, themeKey);
    } catch (e) {
      console.warn('[copyRichText] CSS inline failed:', e.message);
    }
  }

  html = ensureFigureStyles(html);

  var tempDiv = document.createElement("div");
  tempDiv.style.cssText = "position:absolute;left:-9999px;top:0;";
  tempDiv.innerHTML = html;
  document.body.appendChild(tempDiv);
  convertAllPseudoElements(tempDiv);
  convertGradientBackgroundsToSvg(tempDiv);

  // 将本地图片 URL 转换为 base64（公众号需要内联图片）
  await convertLocalImagesToBase64(tempDiv);

  html = tempDiv.innerHTML;
  document.body.removeChild(tempDiv);

  html = html.replace(
    /(<div\s+class="markdown-body[^"]*"\s+style=")([^"]*?)(\s*;\s*)?(?:padding|margin)(-[a-z]+)?\s*:\s*[^;]+;?\s*/gi,
    '$1$2$3'
  );
  html = html.replace(
    /(<div\s+class="markdown-body[^"]*")\s+style="\s*"\s*>/g,
    '$1>'
  );

  try {
    var blob = new Blob([html], { type: 'text/html' });
    var textBlob = new Blob([html.replace(/<[^>]+>/g, '')], { type: 'text/plain' });
    await navigator.clipboard.write([
      new ClipboardItem({ 'text/html': blob, 'text/plain': textBlob })
    ]);
  } catch (e) {
    console.warn('[copyRichText] Clipboard API failed, trying execCommand:', e.message);
    var helper = document.getElementById('clipboardHelper');
    if (!helper) {
      helper = document.createElement('div');
      helper.id = 'clipboardHelper';
      helper.contentEditable = 'true';
      helper.style.cssText = 'position:fixed;left:-9999px;top:0;width:1px;height:1px;overflow:hidden;white-space:pre-wrap';
      document.body.appendChild(helper);
    }
    helper.innerHTML = html;
    helper.focus();
    document.getSelection().removeAllRanges();
    var range = document.createRange();
    range.selectNodeContents(helper);
    document.getSelection().addRange(range);
    document.execCommand('copy');
    document.getSelection().removeAllRanges();
  }
}

async function convertLocalImagesToBase64(container) {
  var imgs = container.querySelectorAll('img');
  var promises = [];
  for (var i = 0; i < imgs.length; i++) {
    (function (img) {
      var src = img.getAttribute('src') || '';
      // 只处理本地 HTTP 图片（http://127.0.0.1:port/images/...）
      if (src.indexOf('http://') !== 0 && src.indexOf('https://') !== 0) return;
      if (src.indexOf('127.0.0.1') === -1 && src.indexOf('localhost') === -1) return;
      promises.push(
        fetch(src)
          .then(function (r) { return r.blob(); })
          .then(function (blob) {
            return new Promise(function (resolve, reject) {
              var reader = new FileReader();
              reader.onload = function () { resolve(reader.result); };
              reader.onerror = reject;
              reader.readAsDataURL(blob);
            });
          })
          .then(function (dataUri) {
            img.setAttribute('src', dataUri);
          })
          .catch(function (err) {
            console.warn('[convertLocalImagesToBase64] Failed:', src, err.message);
          })
      );
    })(imgs[i]);
  }
  await Promise.all(promises);
}

window.CPM = {
  createMarkdownParser: createMarkdownParser,
  renderToHtml: renderToHtml,
  cleanMathElements: cleanMathElements,
  renderMermaidBlocks: renderMermaidBlocks,
  ensureFigureStyles: ensureFigureStyles,
  copyRichText: copyRichText,
  getThemeCssText: getThemeCssText,
  inlineCssViaBrowser: inlineCssViaBrowser,
  convertAllPseudoElements: convertAllPseudoElements,
  convertGradientBackgroundsToSvg: convertGradientBackgroundsToSvg,
};
