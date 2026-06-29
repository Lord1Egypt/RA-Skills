"use strict";
(() => {
  // src/browser/setup.ts
  var sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  var swapProbeName = (fam) => "__om-swap-probe-" + encodeURIComponent(fam.toLowerCase());
  async function setup(input) {
    const hideSelectors = Array.isArray(input.hideSelectors) ? input.hideSelectors.filter((s) => typeof s === "string") : [];
    const gfonts = Array.isArray(input.googleFontImports) ? input.googleFontImports.filter((s) => typeof s === "string") : [];
    const swaps = (Array.isArray(input.fontSwaps) ? input.fontSwaps : []).filter(
      (p) => !!p && typeof p.from === "string" && typeof p.to === "string"
    );
    const skipWebSafe = (input.mode ?? "editable") === "editable";
    const width = Number(input.width) || 0;
    const height = Number(input.height) || 0;
    for (const sel of hideSelectors) {
      try {
        document.querySelectorAll(sel).forEach((el) => {
          el.style.display = "none";
        });
      } catch {
      }
    }
    const gfontSet = {};
    for (const g of gfonts) gfontSet[g.toLowerCase()] = 1;
    const localSwaps = swaps.filter((p) => !gfontSet[p.to.toLowerCase()]);
    const localSwapCss = localSwaps.map(
      (p) => "@font-face{font-family:" + JSON.stringify(p.from) + ";src:local(" + JSON.stringify(p.to) + ");}@font-face{font-family:" + JSON.stringify(swapProbeName(p.to)) + ";src:local(" + JSON.stringify(p.to) + ");}"
    ).join("\n");
    if (localSwapCss) {
      const st = document.createElement("style");
      st.setAttribute("data-genpptx", "swap");
      st.textContent = localSwapCss;
      document.head.appendChild(st);
    }
    const webSwaps = swaps.filter((p) => gfontSet[p.to.toLowerCase()]);
    let swapCancelled = false;
    const swapMisses = [];
    const swapMissSet = {};
    const recordSwapMiss = (fam) => {
      const k = fam.toLowerCase();
      if (!swapMissSet[k]) {
        swapMissSet[k] = 1;
        swapMisses.push(fam);
      }
    };
    const webSwapDone = Promise.all(
      webSwaps.map((p) => {
        const fam = "font-family:" + JSON.stringify(p.from);
        const base = "https://fonts.googleapis.com/css2?family=" + encodeURIComponent(p.to);
        return fetch(base + ":wght@400;500;600;700&display=swap").then((r) => r.ok ? r.text() : "").then((css) => css || fetch(base + "&display=swap").then((r) => r.ok ? r.text() : "")).then((css) => {
          if (!css) {
            recordSwapMiss(p.to);
            return;
          }
          if (swapCancelled) return;
          const st = document.createElement("style");
          st.setAttribute("data-genpptx", "swap");
          st.textContent = css.replace(/font-family:\s*['"][^'"]*['"]/gi, () => fam);
          document.head.appendChild(st);
        }).catch(() => recordSwapMiss(p.to));
      })
    );
    for (const family of gfonts) {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = "https://fonts.googleapis.com/css2?family=" + encodeURIComponent(family) + ":wght@400;500;600;700&display=swap";
      link.setAttribute("data-genpptx", "gfont");
      link.onerror = () => {
        if (swapCancelled) return;
        const fb = document.createElement("link");
        fb.rel = "stylesheet";
        fb.href = "https://fonts.googleapis.com/css2?family=" + encodeURIComponent(family) + "&display=swap";
        fb.setAttribute("data-genpptx", "gfont");
        document.head.appendChild(fb);
      };
      document.head.appendChild(link);
    }
    let resetRect = null;
    if (input.resetTransformSelector) {
      const resetEl = document.querySelector(input.resetTransformSelector);
      if (resetEl) {
        resetEl.setAttribute("noscale", "");
        resetEl.setAttribute("width", String(width));
        resetEl.setAttribute("height", String(height));
        resetEl.style.transform = "none";
        resetEl.style.transition = "none";
        resetEl.style.width = width + "px";
        resetEl.style.height = height + "px";
        void resetEl.offsetHeight;
        const measureEl = resetEl.shadowRoot && resetEl.shadowRoot.querySelector(".canvas") || resetEl;
        const r = measureEl.getBoundingClientRect();
        resetRect = { x: r.x, y: r.y, w: r.width, h: r.height };
      }
    }
    let fontsReady = false;
    try {
      await Promise.race([
        webSwapDone.then(() => document.fonts.ready).then(() => {
          fontsReady = true;
        }),
        sleep(8e3)
      ]);
    } catch {
    }
    swapCancelled = true;
    if (localSwaps.length && document.fonts && document.fonts.load) {
      try {
        await Promise.race([
          Promise.all(
            localSwaps.map(
              (p) => document.fonts.load("72px " + JSON.stringify(swapProbeName(p.to))).catch(() => void 0)
            )
          ),
          sleep(500)
        ]);
      } catch {
      }
    }
    try {
      const pctx = document.createElement("canvas").getContext("2d");
      if (pctx) {
        const probeStr = "BESbswy\u2014MWmi0Il1";
        pctx.font = "72px monospace";
        const probeMonoW = pctx.measureText(probeStr).width;
        pctx.font = "72px sans-serif";
        const probeSansW = pctx.measureText(probeStr).width;
        const genericSkip = {
          serif: 1,
          "sans-serif": 1,
          monospace: 1,
          "system-ui": 1,
          cursive: 1,
          fantasy: 1,
          "-apple-system": 1,
          blinkmacsystemfont: 1,
          "ui-serif": 1,
          "ui-sans-serif": 1,
          "ui-monospace": 1,
          "ui-rounded": 1,
          math: 1,
          emoji: 1
        };
        const webSafeFaces = {
          arial: 1,
          helvetica: 1,
          georgia: 1,
          "times new roman": 1,
          times: 1,
          "courier new": 1,
          courier: 1,
          verdana: 1,
          tahoma: 1,
          "trebuchet ms": 1,
          impact: 1,
          "comic sans ms": 1,
          "segoe ui": 1,
          calibri: 1,
          cambria: 1,
          palatino: 1,
          "palatino linotype": 1,
          garamond: 1,
          "book antiqua": 1,
          consolas: 1,
          candara: 1,
          corbel: 1,
          constantia: 1,
          "arial narrow": 1,
          "arial black": 1,
          "century gothic": 1,
          "lucida sans": 1,
          "lucida console": 1,
          "lucida sans unicode": 1,
          "cambria math": 1,
          "segoe ui emoji": 1,
          "microsoft yahei": 1,
          simsun: 1,
          simhei: 1,
          "yu gothic": 1,
          "ms gothic": 1,
          "ms mincho": 1,
          meiryo: 1,
          "malgun gothic": 1,
          batang: 1,
          pmingliu: 1,
          mingliu: 1,
          "microsoft jhenghei": 1
        };
        for (const swap of localSwaps) {
          const lfam = swap.to;
          const lfamLc = lfam.toLowerCase();
          if (genericSkip[lfamLc]) continue;
          if (skipWebSafe && webSafeFaces[lfamLc]) continue;
          if (swapMissSet[lfamLc]) continue;
          const lq = JSON.stringify(swapProbeName(lfam));
          pctx.font = "72px " + lq + ", monospace";
          const lwm = pctx.measureText(probeStr).width;
          pctx.font = "72px " + lq + ", sans-serif";
          const lws = pctx.measureText(probeStr).width;
          if (Math.abs(lwm - probeMonoW) <= 0.01 && Math.abs(lws - probeSansW) <= 0.01) {
            recordSwapMiss(lfam);
          }
        }
      }
    } catch {
    }
    let notes = [];
    let json = [];
    try {
      const notesEl = document.getElementById("speaker-notes");
      if (notesEl && notesEl.textContent) {
        const parsed = JSON.parse(notesEl.textContent);
        if (Array.isArray(parsed)) json = parsed.map(String);
      }
    } catch {
    }
    const ds = document.querySelector("deck-stage");
    if (ds) {
      const slides = Array.prototype.filter.call(
        ds.children,
        (c) => !/^(template|script|style)$/i.test(c.tagName)
      );
      let anyAttr = false;
      notes = slides.map((s, i) => {
        const a = s.getAttribute("data-speaker-notes");
        if (a !== null) {
          anyAttr = true;
          return a;
        }
        return typeof json[i] === "string" ? json[i] : "";
      });
      if (!anyAttr) notes = json;
    } else {
      notes = json;
    }
    return { notes, fontsReady, resetRect, fontSwapMisses: swapMisses };
  }

  // src/browser/dom-style.ts
  var STYLE_KEYS = [
    "color",
    "backgroundColor",
    "backgroundImage",
    "backgroundSize",
    "backgroundPosition",
    "backgroundRepeat",
    "objectFit",
    "objectPosition",
    "borderTopWidth",
    "borderTopStyle",
    "borderTopColor",
    "borderRightWidth",
    "borderRightStyle",
    "borderRightColor",
    "borderBottomWidth",
    "borderBottomStyle",
    "borderBottomColor",
    "borderLeftWidth",
    "borderLeftStyle",
    "borderLeftColor",
    "borderRadius",
    "fontFamily",
    "fontSize",
    "fontWeight",
    "fontStyle",
    "textDecoration",
    "textDecorationStyle",
    "textDecorationColor",
    "textAlign",
    "textTransform",
    "lineHeight",
    "letterSpacing",
    "opacity",
    "textShadow",
    "transform",
    "boxShadow",
    "listStyleType",
    "display",
    "visibility",
    "whiteSpace",
    "textOverflow",
    "paddingTop",
    "paddingRight",
    "paddingBottom",
    "paddingLeft",
    "overflow",
    // Rt:
    "flexDirection",
    "alignItems",
    "justifyContent",
    "verticalAlign"
  ];
  var COLOR_KEYS = [
    "color",
    "backgroundColor",
    "borderTopColor",
    "borderRightColor",
    "borderBottomColor",
    "borderLeftColor",
    "textDecorationColor"
  ];
  var GENERIC_MAP = {
    serif: "Georgia",
    "sans-serif": "Arial",
    monospace: "Courier New",
    "system-ui": "Arial",
    "-apple-system": "Arial",
    blinkmacsystemfont: "Arial",
    "ui-serif": "Georgia",
    "ui-sans-serif": "Arial",
    "ui-monospace": "Courier New",
    "ui-rounded": "Arial",
    cursive: "Comic Sans MS",
    fantasy: "Impact",
    math: "Cambria Math",
    emoji: "Segoe UI Emoji"
  };
  function makeColorNormalizer() {
    const ctx = document.createElement("canvas").getContext("2d");
    const isTransparentColor = (c) => !c || c === "transparent" || c.indexOf("rgba(") === 0 && /,\s*0\)$/.test(c);
    const normColor = (c) => {
      if (!c || !ctx) return c;
      ctx.fillStyle = "#000";
      ctx.fillStyle = c;
      return ctx.fillStyle;
    };
    return { normColor, isTransparentColor };
  }
  function makeFontResolver(swapMap) {
    const ctx = document.createElement("canvas").getContext("2d");
    const cache = {};
    let monoW;
    let sansW;
    const probe = "BESbswy\u2014MWmi0Il1";
    const faceAvailable = (face) => {
      if (!ctx) return true;
      const lc = face.toLowerCase();
      if (lc in cache) return cache[lc];
      if (monoW == null) {
        ctx.font = "72px monospace";
        monoW = ctx.measureText(probe).width;
        ctx.font = "72px sans-serif";
        sansW = ctx.measureText(probe).width;
      }
      const q = JSON.stringify(face);
      ctx.font = `72px ${q}, monospace`;
      const wm = ctx.measureText(probe).width;
      ctx.font = `72px ${q}, sans-serif`;
      const ws = ctx.measureText(probe).width;
      return cache[lc] = Math.abs(wm - monoW) > 0.01 || Math.abs(ws - sansW) > 0.01;
    };
    return (stack) => {
      let first = null;
      for (const part of stack.split(",")) {
        const face = part.trim().replace(/^['"]|['"]$/g, "");
        if (!face) continue;
        if (first === null) first = face;
        const lc = face.toLowerCase();
        if (swapMap[lc]) return swapMap[lc];
        if (GENERIC_MAP[lc]) return GENERIC_MAP[lc];
        if (faceAvailable(face)) return face;
      }
      return first || "Arial";
    };
  }

  // src/browser/capture-editable.ts
  var sleep2 = (ms) => new Promise((r) => setTimeout(r, ms));
  var settleFrame = () => Promise.race([
    new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => r()))),
    sleep2(500)
  ]);
  async function captureEditable(spec, fontSwaps) {
    if (spec.showJs) {
      try {
        new Function(spec.showJs)();
      } catch (e) {
        throw new Error("showJs threw: " + (e?.message || e));
      }
    }
    await settleFrame();
    const delay = Number.isFinite(Number(spec.delay)) ? Number(spec.delay ?? 600) : 600;
    await sleep2(delay);
    const rootEl = document.querySelector(spec.selector);
    if (!rootEl) throw new Error("selector " + JSON.stringify(spec.selector) + " matched nothing");
    const imgBudget = Math.max(1e3, 8500 - delay);
    let waited = 0;
    let settled = 0;
    let failed = 0;
    const pending = [];
    const queue = (img) => {
      waited++;
      pending.push(
        img.decode().then(
          () => {
            settled++;
          },
          () => {
            settled++;
            failed++;
          }
        )
      );
    };
    for (const img of Array.from(rootEl.querySelectorAll("img"))) {
      if (img.complete && img.naturalWidth > 0) continue;
      queue(img);
    }
    for (const host of Array.from(rootEl.querySelectorAll("*"))) {
      if (!host.shadowRoot || host.firstElementChild || host.shadowRoot.querySelector("slot")) continue;
      for (const hImg of Array.from(host.shadowRoot.querySelectorAll("img"))) {
        if (!(hImg.currentSrc || hImg.src)) continue;
        const cs = getComputedStyle(hImg);
        if (cs.display === "none" || cs.visibility === "hidden" || cs.visibility === "collapse") continue;
        const rect = hImg.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) continue;
        if (hImg.complete && hImg.naturalWidth > 0) continue;
        queue(hImg);
      }
    }
    if (pending.length) {
      await Promise.race([Promise.all(pending), sleep2(imgBudget)]);
      failed += pending.length - settled;
    }
    const { normColor, isTransparentColor } = makeColorNormalizer();
    const swapMap = {};
    for (const s of fontSwaps) swapMap[s.from.toLowerCase()] = s.to;
    const resolveFontFace = makeFontResolver(swapMap);
    let h = 5381;
    const hashStr = (s) => {
      for (let i = 0; i < s.length; i++) h = (h << 5) + h + s.charCodeAt(i) | 0;
    };
    const rectOf = (el) => {
      const r = el.getBoundingClientRect();
      return { x: r.x, y: r.y, w: r.width, h: r.height };
    };
    const readStyle = (cs) => {
      const style = {};
      const csm = cs;
      for (const k of STYLE_KEYS) {
        let v = csm[k];
        if (COLOR_KEYS.indexOf(k) >= 0) v = normColor(v) ?? v;
        if (k === "fontFamily" && v) v = resolveFontFace(v);
        style[k] = v;
      }
      return style;
    };
    const walk = (el) => {
      const cs = getComputedStyle(el);
      if (cs.display === "none") return null;
      const r = rectOf(el);
      const kids = el.children;
      if (r.w === 0 && r.h === 0 && kids.length === 0) return null;
      const style = readStyle(cs);
      const node = { tag: el.tagName.toLowerCase(), rect: r, style, children: [] };
      hashStr(`${r.x},${r.y},${r.w},${r.h}`);
      if (el.tagName === "A") {
        const a = el;
        if (a.href && !(el.getAttribute("href") || "").startsWith("#")) node.href = a.href;
      }
      if (el.tagName === "LI") {
        const lst = cs.listStyleType;
        if (lst && lst !== "none" && lst !== "disc" && lst !== "circle" && lst !== "square") {
          const sibs = [];
          for (let s = el.parentElement?.firstElementChild ?? null; s; s = s.nextElementSibling) {
            if (s.tagName === "LI") sibs.push(s);
          }
          node.liIndex = sibs.indexOf(el) + 1;
        }
      }
      if (cs.transform && cs.transform !== "none") {
        const ow = el.offsetWidth;
        const oh = el.offsetHeight;
        if (ow != null && oh != null && (ow !== r.w || oh !== r.h)) {
          node.untransformedRect = { x: r.x + r.w / 2 - ow / 2, y: r.y + r.h / 2 - oh / 2, w: ow, h: oh };
        }
      }
      if (el.tagName === "IMG") {
        const img = el;
        node.imageUrl = img.currentSrc || img.src;
      } else if (el.tagName === "OBJECT" && el.data) {
        node.imageUrl = el.data;
        return node;
      } else if (el.tagName === "CANVAS") {
        try {
          node.imageUrl = el.toDataURL("image/png");
        } catch {
        }
      } else if (el.tagName.toLowerCase() === "svg") {
        const clone = el.cloneNode(true);
        for (const ref of Array.from(clone.querySelectorAll("image"))) {
          const href = ref.getAttribute("href") || ref.getAttributeNS("http://www.w3.org/1999/xlink", "href");
          if (href && href.indexOf("data:") !== 0) {
            try {
              ref.setAttribute("href", new URL(href, location.href).href);
              ref.removeAttributeNS("http://www.w3.org/1999/xlink", "href");
            } catch {
            }
          }
        }
        node.svg = clone.outerHTML;
        return node;
      } else {
        if (el.shadowRoot && !el.firstElementChild && !el.shadowRoot.querySelector("slot")) {
          for (const simg of Array.from(el.shadowRoot.querySelectorAll("img"))) {
            const scs = getComputedStyle(simg);
            if (scs.display === "none" || scs.visibility === "hidden" || scs.visibility === "collapse") continue;
            const ssrc = simg.currentSrc || simg.src;
            if (!ssrc) continue;
            const srect = simg.getBoundingClientRect();
            if (srect.width === 0 || srect.height === 0) continue;
            let sop = parseFloat(scs.opacity);
            if (isNaN(sop)) sop = 1;
            for (let anc = simg.parentElement; anc && sop > 0; anc = anc.parentElement) {
              const aop = parseFloat(getComputedStyle(anc).opacity);
              if (!isNaN(aop)) sop *= aop;
            }
            if (sop === 0) continue;
            node.imageUrl = ssrc;
            let sfit = el.getAttribute("fit");
            if (sfit !== "contain" && sfit !== "fill") {
              sfit = scs.objectFit === "contain" ? "contain" : "cover";
            }
            const override = { objectFit: sfit, backgroundSize: "auto", backgroundImage: "none" };
            const sideBorderPaints = (w, st, col) => (parseFloat(w) || 0) > 0 && !!st && st !== "none" && !isTransparentColor(normColor(col));
            const paintsOutsetShadow = (bs) => {
              if (!bs || bs === "none") return false;
              for (const part of bs.split(/,(?![^(]*\))/)) {
                if (/\binset\b/.test(part)) continue;
                const shCol = part.match(/rgba?\([^)]*\)/);
                if (shCol && isTransparentColor(shCol[0])) continue;
                return true;
              }
              return false;
            };
            const hostHasBox = !isTransparentColor(normColor(cs.backgroundColor)) || paintsOutsetShadow(cs.boxShadow) || sideBorderPaints(cs.borderTopWidth, cs.borderTopStyle, cs.borderTopColor) || sideBorderPaints(cs.borderRightWidth, cs.borderRightStyle, cs.borderRightColor) || sideBorderPaints(cs.borderBottomWidth, cs.borderBottomStyle, cs.borderBottomColor) || sideBorderPaints(cs.borderLeftWidth, cs.borderLeftStyle, cs.borderLeftColor);
            if (!hostHasBox) {
              const sradius = simg.parentElement ? getComputedStyle(simg.parentElement).borderRadius : "";
              if (sradius && sradius !== "0px") override.borderRadius = sradius;
              if (sop < 1) {
                const hop = parseFloat(cs.opacity);
                override.opacity = String((isNaN(hop) ? 1 : hop) * sop);
              } else {
                const fbg = simg.parentElement ? normColor(getComputedStyle(simg.parentElement).backgroundColor) : "";
                if (fbg && !isTransparentColor(fbg)) override.backgroundColor = fbg;
              }
            }
            node.style = Object.assign({}, node.style, override);
            return node;
          }
        }
        const bg = cs.backgroundImage;
        if (bg && bg !== "none") {
          const m = bg.match(/url\("([^"]*)"\)/);
          if (m && m[1].indexOf("data:") !== 0) {
            try {
              node.imageUrl = new URL(m[1], location.href).href;
            } catch {
            }
          }
        }
      }
      const ws = cs.whiteSpace;
      const keepWs = ws === "pre" || ws === "pre-wrap" || ws === "pre-line" || ws === "break-spaces";
      const parts = [];
      let elKids = 0;
      for (let cn = el.firstChild; cn; cn = cn.nextSibling) {
        if (cn.nodeType === 3) {
          const raw = cn.textContent ?? "";
          const t = keepWs ? raw : raw.trim();
          if (!t) continue;
          const rg = document.createRange();
          if (keepWs) {
            rg.selectNodeContents(cn);
          } else {
            const lead = raw.length - raw.replace(/^\s+/, "").length;
            rg.setStart(cn, lead);
            rg.setEnd(cn, lead + t.length);
          }
          const tr = rg.getBoundingClientRect();
          parts.push({
            tag: "#text",
            rect: { x: tr.x, y: tr.y, w: tr.width, h: tr.height },
            style,
            text: t,
            children: []
          });
          hashStr(t);
        } else if (cn.nodeType === 1) {
          const kid = walk(cn);
          if (kid) {
            parts.push(kid);
            elKids++;
          }
        }
      }
      if (elKids === 0) {
        const txt = parts.map((p) => p.text).join(keepWs ? "" : " ");
        if (txt) node.text = txt;
      } else {
        node.children = parts;
      }
      return node;
    };
    const rootRect = rectOf(rootEl);
    const rootNode = walk(rootEl);
    if (!rootNode) throw new Error("slide root walked to null (display:none?)");
    const rootBg = rootNode.style.backgroundColor;
    const rootBgImg = rootNode.style.backgroundImage || "";
    if (rootBgImg.indexOf("gradient(") < 0 && (!rootBg || rootBg === "transparent" || /rgba?\([^)]*,\s*0\)$/.test(rootBg))) {
      for (let p = rootEl.parentElement; p; p = p.parentElement) {
        if (p.shadowRoot) continue;
        const pbg = normColor(getComputedStyle(p).backgroundColor);
        if (pbg && pbg !== "transparent" && !/rgba?\([^)]*,\s*0\)$/.test(pbg)) {
          rootNode.style = Object.assign({}, rootNode.style, { backgroundColor: pbg });
          break;
        }
      }
    }
    return {
      slide: { rect: rootRect, root: rootNode },
      hash: h >>> 0,
      imagesWaited: waited,
      imagesFailed: failed
    };
  }

  // src/browser/capture-screenshot.ts
  var sleep3 = (ms) => new Promise((r) => setTimeout(r, ms));
  async function captureScreenshot(spec) {
    if (spec.showJs) {
      try {
        new Function(spec.showJs)();
      } catch (e) {
        throw new Error("showJs threw: " + (e?.message || e));
      }
    }
    const delay = Number.isFinite(Number(spec.delay)) ? Number(spec.delay ?? 600) : 600;
    await Promise.race([
      new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => r()))),
      sleep3(500)
    ]);
    await sleep3(delay);
  }

  // src/browser/media-browser.ts
  var POOL = 6;
  var MAX_RASTER = 2048;
  async function fetchBlob(url) {
    let u;
    try {
      u = new URL(url, location.href);
    } catch {
      throw new Error("blocked host");
    }
    const sameOrigin = u.origin === location.origin;
    const res = await fetch(u.href, { credentials: sameOrigin ? "same-origin" : "omit" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.blob();
  }
  function blobToDataUrl(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(reader.error);
      reader.readAsDataURL(blob);
    });
  }
  function svgSizeFit(natW, natH, vbW, vbH, reqW, reqH) {
    if (reqW && reqH) {
      const d = Math.max(natW ?? 0, reqW);
      const l = Math.max(natH ?? 0, reqH);
      const a = Math.min(1, MAX_RASTER / Math.max(d, l));
      return { w: Math.max(1, d * a), h: Math.max(1, l * a) };
    }
    if (vbW && vbH) {
      const d = Math.min(1, MAX_RASTER / Math.max(vbW, vbH));
      return { w: Math.max(1, vbW * d), h: Math.max(1, vbH * d) };
    }
    return { w: 300, h: 150 };
  }
  async function rasterizeSvgBlob(blob, reqW, reqH) {
    const objectUrl = URL.createObjectURL(blob);
    try {
      const img = await new Promise((resolve, reject) => {
        const el = new Image();
        el.onload = () => resolve(el);
        el.onerror = () => reject(new Error("SVG decode failed"));
        el.src = objectUrl;
      });
      const natW = img.naturalWidth || void 0;
      const natH = img.naturalHeight || void 0;
      let vbW = natW;
      let vbH = natH;
      if (!vbW || !vbH) {
        try {
          const head = ((await blob.text()).match(/<svg\b[^>]*>/i)?.[0] ?? "").match(
            /\bviewBox\s*=\s*["']\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)/i
          );
          if (head) {
            vbW = parseFloat(head[1]) || void 0;
            vbH = parseFloat(head[2]) || void 0;
          }
        } catch {
        }
      }
      const { w, h } = svgSizeFit(natW, natH, vbW, vbH, reqW, reqH);
      const canvas = document.createElement("canvas");
      canvas.width = Math.max(1, Math.round(w * 2));
      canvas.height = Math.max(1, Math.round(h * 2));
      const ctx = canvas.getContext("2d");
      if (!ctx) return null;
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      return { dataUrl: canvas.toDataURL("image/png"), w: vbW, h: vbH };
    } catch {
      return null;
    } finally {
      URL.revokeObjectURL(objectUrl);
    }
  }
  async function inlineImageRef(url, warnings) {
    try {
      const blob = await fetchBlob(url);
      if (blob.type.includes("svg") || url.toLowerCase().endsWith(".svg")) {
        const entry = await rasterizeSvgBlob(blob);
        if (!entry) warnings.push(`Failed to rasterise SVG from ${url} (decode failed)`);
        return entry;
      }
      const dataUrl = await blobToDataUrl(blob);
      let w;
      let h;
      try {
        const bmp = await createImageBitmap(blob);
        w = bmp.width;
        h = bmp.height;
        bmp.close();
      } catch {
      }
      return { dataUrl, w, h };
    } catch (err) {
      warnings.push(`Failed to inline image ${url}: ${err instanceof Error ? err.message : String(err)}`);
      return null;
    }
  }
  async function inlineSvgMarkup(markup, w, h, warnings) {
    const re = /<image\b[^>]*?\b(?:xlink:)?href=["']([^"']+)["']/gi;
    const hrefs = /* @__PURE__ */ new Set();
    for (let m; m = re.exec(markup); ) {
      if (!m[1].startsWith("data:")) hrefs.add(m[1]);
    }
    for (const href of [...hrefs].sort((a, b) => b.length - a.length)) {
      try {
        const dataUrl = await blobToDataUrl(await fetchBlob(href));
        markup = markup.split(href).join(dataUrl);
      } catch (err) {
        warnings.push(
          `Failed to inline <image href="${href}"> in SVG: ${err instanceof Error ? err.message : String(err)}`
        );
      }
    }
    if (!/^\s*<svg\b[^>]*\bxmlns\s*=/i.test(markup)) {
      markup = markup.replace(/<svg\b/i, '<svg xmlns="http://www.w3.org/2000/svg"');
    }
    const blob = new Blob([markup], { type: "image/svg+xml" });
    const entry = await rasterizeSvgBlob(blob, w, h);
    if (!entry) {
      warnings.push(`Failed to rasterise inline <svg> (${w}\xD7${h}px): ${markup.slice(0, 80)}\u2026`);
    }
    return entry;
  }
  async function resolveMedia(refs) {
    const out = refs.map((r) => ({ key: r.key, value: null, warnings: [] }));
    const tasks = refs.map((ref, idx) => async () => {
      const warnings = [];
      const value = ref.kind === "url" ? await inlineImageRef(ref.url, warnings) : await inlineSvgMarkup(ref.svg, ref.w, ref.h, warnings);
      out[idx] = { key: ref.key, value, warnings };
    });
    let i = 0;
    await Promise.all(
      Array.from({ length: Math.min(POOL, tasks.length) || 1 }, async () => {
        while (i < tasks.length) await tasks[i++]();
      })
    );
    return out;
  }

  // src/browser/entry.ts
  var api = { setup, captureEditable, captureScreenshot, resolveMedia };
  window.__genpptx = api;
})();
