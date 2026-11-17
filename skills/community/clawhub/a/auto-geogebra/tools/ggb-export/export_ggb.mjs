#!/usr/bin/env node
/**
 * ggb_export —— 把「GeoGebra 指令脚本」导出为 .ggb 文件（真机引擎，零第三方依赖）
 *
 * 原理：本地 Chrome/Edge 无头实例加载官方 deployggb.js 引擎
 *      → 逐条 evalCommand → getBase64() 取 .ggb 字节
 *      → 回读校验（setBase64 重新载入并对比对象集合）→ 落盘。
 *
 * 用法：
 *   node export_ggb.mjs --page <page.html> --cmds <commands.txt> --out <out.ggb>
 *                       [--png <preview.png>] [--browser <可执行文件>] [--timeout 毫秒] [--headful] [--trace]
 *   注：--png 预览在检测到三维对象时自动切换到 3D 视图。
 *
 * 依赖：Node 18+（全局 fetch/WebSocket；本机 Node 22 已带）+ 本机 Chrome 或 Edge。
 * 退出码：0=成功；1=失败；2=有指令未通过（见 failedList）；3=有软失败（见 softList）。
 */
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { mkdtempSync, readFileSync, writeFileSync, existsSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function parseArgs(argv) {
  const a = {};
  for (let i = 2; i < argv.length; i++) {
    const k = argv[i];
    if (k.startsWith("--")) {
      const nxt = argv[i + 1];
      const v = nxt && !nxt.startsWith("--") ? argv[++i] : "true";
      a[k.slice(2)] = v;
    }
  }
  return a;
}

function findBrowser(explicit) {
  const cands = [
    explicit,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ].filter(Boolean);
  for (const p of cands) {
    if (existsSync(p)) return p;
  }
  return null;
}

class CDP {
  constructor(ws) {
    this.ws = ws;
    this.nextId = 0;
    this.pending = new Map();
    ws.addEventListener("message", (ev) => {
      let m;
      try { m = JSON.parse(ev.data); } catch { return; }
      if (m.id && this.pending.has(m.id)) {
        const { res, rej } = this.pending.get(m.id);
        this.pending.delete(m.id);
        if (m.error) rej(new Error(m.error.message)); else res(m.result);
      }
    });
  }
  send(method, params = {}) {
    const id = ++this.nextId;
    const p = new Promise((res, rej) => this.pending.set(id, { res, rej }));
    this.ws.send(JSON.stringify({ id, method, params }));
    return p;
  }
}

async function main() {
  const args = parseArgs(process.argv);
  for (const req of ["page", "cmds", "out"]) {
    if (!args[req]) throw new Error("缺少参数 --" + req);
  }
  const deadline = Date.now() + Number(args.timeout || 120000);
  const pageHtml = readFileSync(resolve(args.page), "utf8");
  const cmds = readFileSync(resolve(args.cmds), "utf8")
    .split(/\r?\n/)
    .map((s) => s.trim())
    .filter((s) => s && !s.startsWith("#") && !s.startsWith("//"));

  const server = createServer((_, res) => {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    res.end(pageHtml);
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  const httpPort = server.address().port;

  const profile = mkdtempSync(join(tmpdir(), "ggb-export-"));
  const browser = findBrowser(args.browser);
  if (!browser) throw new Error("未找到 Chrome/Edge 可执行文件（可用 --browser 指定）");
  const flags = [
    ...(args.headful ? [] : ["--headless=new"]),
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-extensions",
    "--disable-sync",
    "--mute-audio",
    "--window-size=1100,860",
    "--force-device-scale-factor=1",
    "--remote-debugging-port=0",
    "--user-data-dir=" + profile,
    "--remote-allow-origins=*",
    "http://127.0.0.1:" + httpPort + "/",
  ];
  const proc = spawn(browser, flags, { stdio: "ignore" });

  let ws = null;
  try {
    const portFile = join(profile, "DevToolsActivePort");
    while (!existsSync(portFile)) {
      if (Date.now() > deadline) throw new Error("等待浏览器 DevTools 端口超时");
      await sleep(120);
    }
    const devPort = readFileSync(portFile, "utf8").split("\n")[0].trim();
    const list = await (await fetch("http://127.0.0.1:" + devPort + "/json/list")).json();
    const target = list.find((t) => t.type === "page" && (t.url || "").startsWith("http://127.0.0.1:"))
      || list.find((t) => t.type === "page");
    if (!target) throw new Error("未找到浏览器页面目标");
    ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((res, rej) => {
      ws.addEventListener("open", res, { once: true });
      ws.addEventListener("error", () => rej(new Error("CDP WebSocket 连接失败")), { once: true });
    });
    const cdp = new CDP(ws);
    await cdp.send("Runtime.enable");

    const evalJS = async (expression, opts) => {
      const params = { expression, returnByValue: true };
      if (opts && opts.awaitPromise) params.awaitPromise = true;
      const r = await cdp.send("Runtime.evaluate", params);
      if (r.exceptionDetails) {
        const d = r.exceptionDetails.exception?.description || r.exceptionDetails.text;
        throw new Error("页面脚本异常：" + d);
      }
      return r.result ? r.result.value : undefined;
    };

    // 1) 等待 GeoGebra 引擎就绪
    let ready = false;
    while (Date.now() < deadline) {
      const st = await evalJS("({ready: !!window.__ggbReady, err: window.__ggbError || null, hasApplet: typeof window.ggbApplet !== 'undefined' && !!window.ggbApplet})");
      if (st && st.err) throw new Error("引擎加载出错：" + st.err);
      if (st && st.ready && st.hasApplet) { ready = true; break; }
      await sleep(400);
    }
    if (!ready) throw new Error("等待 GeoGebra 引擎就绪超时（检查网络与 deployggb.js 可达性）");

    // 2) 逐条执行指令（含脚本型命令的效果核验 + 静默不创建检测）
    const results = await evalJS(`(function(cmds){
      var out = [];
      var prev = [];
      function verifyScript(cmd){
        var open = cmd.indexOf("(") >= 0 ? cmd.indexOf("(") : cmd.indexOf("[");
        if (open < 0) return null;
        var fname = cmd.slice(0, open).trim();
        var close2 = Math.max(cmd.lastIndexOf(")"), cmd.lastIndexOf("]"));
        if (close2 <= open) return null;
        var args = cmd.slice(open + 1, close2).split(",").map(function(s){ return s.trim(); });
        if (fname === "SetValue" && args.length >= 2) {
          var v = null;
          try { v = window.ggbApplet.getValue(args[0]); } catch (e) {}
          var target = parseFloat(args[1]);
          return { ok: v !== null && !isNaN(target) && Math.abs(v - target) < 1e-9, note: "SetValue 核验：实际=" + v };
        }
        if (fname === "SetColor" && args.length >= 4) {
          var c = null;
          try { c = window.ggbApplet.getColor(args[0]); } catch (e) {}
          var okc = false;
          if (c && c.charAt(0) === "#" && c.length >= 7) {
            var wantCh = [1, 2, 3].map(function(i2){ return Math.round(parseFloat(args[i2]) * 255); });
            var gotCh = [1, 3, 5].map(function(p2){ return parseInt(c.substr(p2, 2), 16); });
            okc = gotCh.every(function(g2, idx2){ return Math.abs(g2 - wantCh[idx2]) <= 1; });
          }
          return { ok: okc, note: "SetColor 核验：实际=" + c + "（容差 ±1/255）" };
        }
        if (fname === "ShowLabel" && args.length >= 2) {
          var lv = null;
          try { lv = window.ggbApplet.getLabelVisible(args[0]); } catch (e) {}
          return { ok: lv === (args[1] === "true"), note: "ShowLabel 核验：实际=" + lv };
        }
        if (fname === "SetCoords" && args.length >= 3) {
          var x2 = null, y2 = null;
          try {
            var xml3 = window.ggbApplet.getXML();
            var pos3 = xml3.indexOf('label="' + args[0] + '"');
            if (pos3 >= 0) {
              var seg3 = xml3.slice(pos3, pos3 + 4000);
              var e3 = seg3.indexOf("</element>");
              if (e3 >= 0) seg3 = seg3.slice(0, e3);
              var lo3 = seg3.indexOf("<labelOffset");
              if (lo3 >= 0) {
                var part3 = seg3.slice(lo3, lo3 + 90);
                var xm3 = part3.match(/x="([-0-9.]+)"/);
                var ym3 = part3.match(/y="([-0-9.]+)"/);
                if (xm3) x2 = xm3[1];
                if (ym3) y2 = ym3[1];
              }
            }
          } catch (e) {}
          return { ok: x2 !== null && Math.abs(parseFloat(x2) - parseFloat(args[1])) < 0.5 && Math.abs(parseFloat(y2) - parseFloat(args[2])) < 0.5, note: "SetCoords 核验：labelOffset=(" + x2 + "," + y2 + ")" };
        }
        return null;
      }
      function isScriptish(cmd){
        var names = ["SetValue", "SetColor", "ShowLabel", "SetVisible", "SetVisibleInView", "SetLineStyle", "SetLineThickness", "SetFilling", "SetCaption", "SetCoords", "StartAnimation", "SetDynamicColor", "SetPointStyle", "SetPointSize", "SetTextValue", "SetAxesVisible", "ZoomIn", "ZoomOut", "CenterView"];
        for (var k = 0; k < names.length; k++) {
          if (cmd.indexOf(names[k]) === 0 && (cmd.indexOf("(", names[k].length) >= 0 || cmd.indexOf("[", names[k].length) >= 0)) return true;
        }
        return false;
      }
      for (var i = 0; i < cmds.length; i++) {
        var cmd = cmds[i], rawOk = false, err = "", note = "", scriptUnverified = false;
        try { rawOk = !!window.ggbApplet.evalCommand(cmd); }
        catch (e) { err = String(e); }
        var ok = rawOk;
        if (!rawOk) {
          var vres = verifyScript(cmd);
          if (vres) {
            if (vres.ok) { ok = true; note = "脚本命令（返回值不可信），效果已核验：" + vres.note; }
            else { err = vres.note || "脚本命令效果核验失败"; }
          } else if (isScriptish(cmd)) {
            scriptUnverified = true;
            note = "脚本型命令：返回值不可信，效果未自动核验";
            ok = true;
          }
        }
        var names = window.ggbApplet.getAllObjectNames();
        var soft = null;
        var base = null;
        var s0 = cmd.trim();
        var k0 = 0;
        while (k0 < s0.length && /[0-9A-Za-z_]/.test(s0.charAt(k0))) k0++;
        if (k0 > 0) {
          var j0 = k0;
          while (j0 < s0.length && s0.charAt(j0) === " ") j0++;
          if (s0.charAt(j0) === "(") {
            var depth0 = 0;
            while (j0 < s0.length) {
              var ch0 = s0.charAt(j0);
              if (ch0 === "(") depth0++;
              else if (ch0 === ")") { depth0--; if (depth0 === 0) { j0++; break; } }
              j0++;
            }
            while (j0 < s0.length && s0.charAt(j0) === " ") j0++;
          }
          if (s0.charAt(j0) === "=") base = s0.slice(0, k0);
        }
        if (ok && !scriptUnverified && base) {
          var created = names.length > prev.length || names.indexOf(base) >= 0 || names.some(function(n){ return n.indexOf(base) === 0; });
          if (!created) soft = "命令返回成功但未创建对象（疑似保留名冲突/退化构造）";
        }
        out.push({ cmd: cmd, ok: ok, rawOk: rawOk, err: err, note: note, scriptUnverified: scriptUnverified, names: names, soft: soft });
        prev = names;
      }
      return out;
    })(${JSON.stringify(cmds)})`);

    const namesBefore = await evalJS("window.ggbApplet.getAllObjectNames()");

    // 3) 导出 .ggb（兼容 回调/同步/Promise 三种 API 形态）
    const b64 = await evalJS(`(function(){
      return new Promise(function(resolve){
        var a = window.ggbApplet, settled = false;
        function finish(v){ if(!settled){ settled = true; resolve(typeof v === "string" && v ? v : null); } }
        function tryFn(name){
          if (typeof a[name] !== "function") return false;
          try {
            if (a[name].length >= 1) { a[name](finish); }
            else {
              var r = a[name]();
              if (r && typeof r.then === "function") r.then(finish); else finish(r);
            }
          } catch (e) { finish(null); }
          return true;
        }
        if (tryFn("getBase64") || tryFn("getFile64")) {
          setTimeout(function(){ finish(null); }, 10000);
          return;
        }
        finish(null);
      });
    })()`, { awaitPromise: true });
    if (!b64 || typeof b64 !== "string") throw new Error("getBase64() 未返回数据（已尝试回调/同步/Promise 三种形态）");

    // 3.4) 3D 自适应：检测到三维对象时，切到 3D 视图再截图（v1.3.1）
    let has3d = false;
    try {
      has3d = await evalJS(`(function(){
        try {
          var x = window.ggbApplet.getXML();
          return /type="(point3d|line3d|segment3d|vector3d|polygon3d|plane3d|conic3d|quadric|surface|polyhedron|net3d)"/.test(x);
        } catch (e) { return false; }
      })()`);
      if (has3d && args.png) {
        await evalJS('(function(){ try { window.ggbApplet.setPerspective("T3"); } catch (e) {} return true; })()');
        await sleep(1400);
      }
    } catch (e) {}

    // 3.5) 可选：导出预览 PNG（CDP 截取画布区域）
    let pngWritten = null;
    if (args.png) {
      try {
        await cdp.send("Page.enable");
        const rect = await evalJS(`(function(){
          var cs = [].slice.call(document.querySelectorAll("canvas"));
          var best = null;
          cs.forEach(function(c){
            var r = c.getBoundingClientRect();
            if (r.width * r.height < 100) return;
            if (!best || r.width * r.height > best.width * best.height) best = { x: r.x, y: r.y, width: r.width, height: r.height };
          });
          return best;
        })()`);
        const shotParams = rect && rect.width > 10
          ? { format: "png", clip: { x: rect.x, y: rect.y, width: rect.width, height: rect.height, scale: 1 } }
          : { format: "png" };
        const shot = await cdp.send("Page.captureScreenshot", shotParams);
        if (shot && shot.data) {
          writeFileSync(resolve(args.png), Buffer.from(shot.data, "base64"));
          pngWritten = resolve(args.png);
        }
      } catch (e) {
        pngWritten = null;
      }
    }

    // 4) 回读校验：重新载入导出的字节，对比对象集合
    let namesAfter = null;
    try {
      await evalJS("window.__b64 = " + JSON.stringify(b64) + "; true");
      await evalJS("(function(){ window.ggbApplet.setBase64(window.__b64); return true; })()");
      await sleep(1200);
      namesAfter = await evalJS("window.ggbApplet.getAllObjectNames()");
    } catch (e) {
      namesAfter = null;
    }

    const outPath = resolve(args.out);
    const bytes = Buffer.from(b64, "base64");
    writeFileSync(outPath, bytes);

    const failed = results.filter((r) => !r.ok);
    const soft = results.filter((r) => r.ok && r.soft);
    const unverified = results.filter((r) => r.scriptUnverified);
    const verifiedNotes = results.filter((r) => r.ok && r.note && !r.scriptUnverified);
    const payload = {
      ok: failed.length === 0 && soft.length === 0,
      file: outPath,
      bytes: bytes.length,
      commands: cmds.length,
      failed: failed.length,
      failedList: failed,
      softFailures: soft.length,
      softList: soft,
      unverifiedScripts: unverified.length,
      preview3d: has3d,
      verifiedNotes: verifiedNotes.map((r) => ({ cmd: r.cmd, note: r.note })),
      objectsBefore: namesBefore ? namesBefore.length : null,
      objectsAfter: namesAfter ? namesAfter.length : null,
      roundtrip: !!(namesBefore && namesAfter && namesAfter.length === namesBefore.length),
    };
    if (args.png) {
      payload.png = pngWritten;
    }
    if (args.trace) {
      payload.trace = results.map((r) => ({ cmd: r.cmd, ok: r.ok, rawOk: r.rawOk, note: r.note || undefined, soft: r.soft || undefined, objects: r.names }));
    }
    console.log(JSON.stringify(payload, null, 2));
    if (failed.length > 0) process.exitCode = 2;
    else if (soft.length > 0) process.exitCode = 3;
  } finally {
    try { if (ws) ws.close(); } catch {}
    try { proc.kill(); } catch {}
    try { server.close(); } catch {}
    try { rmSync(profile, { recursive: true, force: true }); } catch {}
  }
}

main().catch((e) => {
  console.error(JSON.stringify({ ok: false, error: String((e && e.message) || e) }));
  process.exit(1);
});
