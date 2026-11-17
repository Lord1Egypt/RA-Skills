// Publish one local video on member.bilibili.com (runs inside ego-browser).
// Config comes from /tmp/bilibili-video-publish.json written by publish.mjs.
// Exit 0: 投稿成功 (审核中). Exit 1: flow error. Exit 2: login required (handOff).
//
// B 站创作中心是 micro-app (shadow DOM):所有交互都用 shadow-walk 定位元素,
// 拿到坐标后 page.mouse.click。文件选择走 waitForFileChooser。

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { readConfigSync } from "./lib/config-file.mjs";
import {
  DECLARE_OPTIONS,
  PUBLISH_CONFIG_PATH,
  PUBLISH_OK_RE,
  centerRgba,
  classifyLogin,
  flowErrorBody,
  imageDimsFromBuffer,
  loginRequiredBody,
  declareChoice,
  optionClickReady,
  judgeCoverIdentity,
  lumaGridFromRgba,
  pngFingerprint,
  coverSampleFromPng,
  manuscriptFromText,
  MANUSCRIPT_LOOKUP_ATTEMPTS,
  MANUSCRIPT_LOOKUP_INTERVAL_MS,
  archivesSearchUrls,
  pickManuscriptFromArchivePayloads,
  mayClickSubmit,
  partitionChoice,
  syncGate,
  publishSuccessBody,
  RATIO_4_3,
} from "./lib/pure.mjs";

let spaceId;
const fail = (msg, extra = {}) => {
  console.error(JSON.stringify(flowErrorBody(msg, { spaceId, ...extra })));
  process.exit(1);
};

if (typeof taskSpace !== "function") {
  fail("post-video.mjs must run inside ego-browser. Use: node scripts/publish.mjs --yes ...");
}

let cfg = null;
try {
  cfg = readConfigSync(PUBLISH_CONFIG_PATH);
} catch {
  cfg = null;
}
if (!cfg) {
  fail(`配置文件不存在: ${PUBLISH_CONFIG_PATH}。请通过 publish.mjs 调用,不要直接跑 post-video.mjs`);
}

const video = cfg.video || "";
const title = cfg.title || "";
const desc = cfg.desc || "";
const tags = Array.isArray(cfg.tags) ? cfg.tags : [];
const cover43 = cfg.cover43 || "";
const cover169 = cfg.cover169 || "";
const keep = Boolean(cfg.keep);
if (!video || !existsSync(video)) fail(`视频不存在: ${video}`);
if (!title || !String(title).trim()) fail("缺少标题(配置里应有 title)");

// --- shadow-DOM helpers, injected into every page.evaluate ---
const HELPERS = `
function* __walk(root){for(const el of root.querySelectorAll("*")){if(el.shadowRoot)yield* __walk(el.shadowRoot);yield el;}}
function __all(){return Array.from(__walk(document));}
function __own(el){return Array.from(el.childNodes).filter(function(n){return n.nodeType===3;}).map(function(n){return n.textContent.trim();}).join("").trim();}
function __visible(el){return !!(el.offsetParent || el.getClientRects().length);}
function __byTextExact(text){var es=__all().filter(function(el){return __own(el)===text && __visible(el);});return es[0]||null;}
function __point(el){var r=el.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2};}
/* 表单会 reflow:点击前必须滚到可视区,否则坐标可能在视口外(如 y=-180) */
function __pointInView(el){el.scrollIntoView({block:"center"});return __point(el);}
function __textPoint(text){var el=__byTextExact(text);return el?__pointInView(el):null;}
function __hasText(re){var it=__walk(document);for(var s=it.next();!s.done;s=it.next()){var el=s.value;if(__own(el)&&re.test(__own(el))&&__visible(el))return true;}return false;}
function __shadowText(){var out="";var it=__walk(document);for(var s=it.next();!s.done;s=it.next()){var own=__own(s.value);if(own)out+=own+"\\n";if(out.length>4000)break;}return out;}
`;
// ego 的 evaluate 在第二个参数为 undefined 时会做 JSON 序列化校验并报错,
// 所以 arg 为空时干脆不传第二个参数。
const evBody = (body) => new Function("arg", `${HELPERS}\nreturn (${body})(arg);`);
const ev = (body, arg) => (arg === undefined ? page.evaluate(evBody(body)) : page.evaluate(evBody(body), arg));

const task = cfg.spaceId ? await taskSpace(cfg.spaceId) : await taskSpace("publish video to bilibili");
spaceId = task.spaceId;
const page = task.page("p1");
console.error(JSON.stringify({ spaceId, video, title }));

// B 站会弹通知权限打断自动化,先预授权(不支持项会抛错,忽略)。
try {
  await page.cdp("Browser.grantPermissions", { permissions: ["notifications"] });
} catch {
  // 老版本 ego 没有该接口时继续,靠用户手动处理弹窗。
}

await page.goto("https://member.bilibili.com/platform/upload/video/frame", { waitUntil: "domcontentloaded", timeout: 45000 });
try {
  await page.waitForLoadState("networkidle", { timeout: 8000 });
} catch {}
await page.waitForTimeout(2500);

// --- 登录闸门 ---
const probe = await ev(`function(arg){
  return { url: location.href, text: __shadowText() + "\\n" + (document.body.innerText||"") };
}`);
const classified = classifyLogin({ url: probe.url, text: probe.text });
if (!classified.logged_in) {
  console.log(JSON.stringify(loginRequiredBody({ spaceId, url: probe.url })));
  try {
    await task.handOff();
  } catch {}
  process.exit(2);
}

// --- 上传视频 ---
const uploadPt = await ev(`function(){
  var area=document.querySelector(".upload-area");
  if(area && __visible(area)) return __pointInView(area);
  var btn=__byTextExact("上传视频");
  if(!btn) return null;
  var el=btn.parentElement||btn;
  return __pointInView(el);
}`);
if (!uploadPt) fail("未找到上传区域(.upload-area),页面结构可能已变化");

const chooserPromise = page.waitForFileChooser({ timeout: 20000 });
await page.mouse.click(uploadPt.x, uploadPt.y, { label: "点击上传视频" });
let chooser;
try {
  chooser = await chooserPromise;
} catch {
  fail("点击上传区后没有弹出文件选择框(可能被权限弹窗打断,重跑并先处理浏览器弹窗)");
}
const picked = await chooser.setFiles(video);
if (picked && picked.dialog) await page.acceptDialog();
console.error("视频已交给浏览器,等待上传完成…");

// 上传完成信号在 shadow DOM 里:出现「上传完成 / 更换视频」。
let uploaded = false;
for (let i = 0; i < 300; i++) {
  await page.waitForTimeout(3000);
  const st = await ev(`function(arg){
    return {
      done: __hasText(/上传完成|更换视频/),
      failed: __hasText(/上传失败|解析失败/),
    };
  }`);
  if (st.failed) fail("视频上传失败(页面上出现「上传失败/解析失败」)");
  if (st.done) { uploaded = true; break; }
}
if (!uploaded) fail("等待视频上传完成超时(15 分钟)");
console.error("上传完成,等待投稿表单…");
await page.waitForTimeout(2000);

// --- 标题 ---
// 不能用原生 setter 写 value:只改显示、不更新 Vue 模型,投稿会发成文件名默认标题。
// 也不能只靠 execCommand:该 input 疑似 v-model.lazy,必须补 blur/change;
// 首选 CDP Input.insertText(真实输入事件),execCommand 作为回退。
const titleFocus = await ev(`function(value){
  var input=__all().find(function(el){return el.tagName==="INPUT" && /稿件标题/.test(el.placeholder||"");});
  if(!input) return {ok:false,error:"未找到标题输入框"};
  input.focus();
  input.setSelectionRange(0, input.value.length);
  return {ok:true,value:input.value};
}`, title);
if (!titleFocus.ok) fail(titleFocus.error || "标题输入框不可聚焦");
let cdpTyped = false;
try {
  await page.cdp("Input.insertText", { text: title });
  cdpTyped = true;
} catch {
  // 老版 ego 没有 cdp 或接口不可用时走 execCommand 回退
}
let titleResult = await ev(`function(value){
  var input=__all().find(function(el){return el.tagName==="INPUT" && /稿件标题/.test(el.placeholder||"");});
  if(!input) return {ok:false,error:"标题输入框消失"};
  if(!${cdpTyped ? "true" : "false"}) {
    input.focus();
    input.setSelectionRange(0, input.value.length);
    document.execCommand("insertText", false, value);
  }
  input.dispatchEvent(new Event("change", { bubbles: true }));
  input.blur();
  return {ok:true,value:input.value};
}`, title);
if (!titleResult.ok) fail(titleResult.error || "标题写入失败");
if ((titleResult.value || "").trim() !== title.trim()) {
  fail(`标题写入异常: 期望「${title}」实际「${titleResult.value}」`);
}

// --- 标签:先清空表单预填,再加调用方的 ---
// 关闭按钮是 chip 的直接子元素 svg.close。行会重排,坐标点击会点错元素,
// 一律在 evaluate 里对 svg.close 派发合成 MouseEvent(Vue 不校验 isTrusted)。
for (let round = 0; round < 3; round++) {
  const removed = await ev(`function(){
    var removed=[];
    for(const el of __all()){
      if(String(el.className).indexOf("label-item-v2-container")<0 || !__visible(el)) continue;
      var icon=el.querySelector("svg.close");
      if(!icon) continue;
      icon.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,view:window}));
      removed.push(1);
    }
    return removed;
  }`);
  if (!removed.length) break;
  await page.waitForTimeout(800);
}
const readTagChips = () => ev(`function(){
  function chipText(el){
    var own=__own(el);
    if(own) return own;
    var p=el.querySelector("p");
    if(p){
      var t=__own(p)||String(p.textContent||"").trim();
      if(t) return t;
    }
    return String(el.textContent||"").replace(/\s+/g," ").trim();
  }
  return __all().filter(function(el){return String(el.className).indexOf("label-item-v2-content")>=0 && __visible(el);})
    .map(chipText).filter(Boolean);
}`);
const remainingTags = await readTagChips();
if (remainingTags.length > 0) {
  console.error(JSON.stringify({ note: "预填标签未能全部移除,保留现状", remaining: remainingTags }));
}

// 以前是三个标签连续模拟回车后再一起核对。某一格没挂上就会三个一起报失败，
// 且输入框未聚焦、建议下拉未收起时，后面的回车会打空。每个标签都等到 chip 出现再写下一项。
for (const tag of tags) {
  let present = (await readTagChips()).includes(tag);
  for (let attempt = 0; attempt < 3 && !present; attempt += 1) {
    const pt = await ev(`function(){
      var input=__all().find(function(el){return el.tagName==="INPUT" && /创建标签/.test(el.placeholder||"");});
      if(!input) return null;
      return __pointInView(input);
    }`);
    if (!pt) fail("未找到标签输入框");
    await page.mouse.click(pt.x, pt.y, { label: `聚焦标签输入框(${tag})` });
    await page.waitForTimeout(200);
    const added = await ev(`function(tag){
      var input=__all().find(function(el){return el.tagName==="INPUT" && /创建标签/.test(el.placeholder||"");});
      if(!input) return {ok:false,error:"未找到标签输入框"};
      input.focus();
      var setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,"value").set;
      setter.call(input,tag);
      input.dispatchEvent(new Event("input",{bubbles:true}));
      input.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",keyCode:13,which:13,bubbles:true,code:"Enter"}));
      return {ok:true};
    }`, tag);
    if (!added.ok) fail(added.error || "标签写入失败");
    try {
      await page.keyboard.press("Enter");
    } catch {
      // 老版本 ego 没有 keyboard 时，上面的合成 keydown 仍会发出。
    }
    for (let i = 0; i < 10; i += 1) {
      await page.waitForTimeout(400);
      present = (await readTagChips()).includes(tag);
      if (present) break;
    }
  }
  if (!present) fail(`标签未确认添加(回车创建失败?): ${tag}`);
}
if (tags.length) {
  const chipTexts = await readTagChips();
  const missing = tags.filter((t) => !chipTexts.includes(t));
  if (missing.length) fail(`标签未确认添加(回车创建失败?): ${missing.join(", ")}`);

  // B 站会在表单挂载后异步插入推荐标签(每轮都可能不同),
  // 所以「读 chips → 删多余 → 复核」循环几轮,等它插入完并清干净。
  // 删除动作用 evaluate 内派发合成 MouseEvent 点 svg.close:推荐行频繁重排,
  // 坐标点击会在点击瞬间落到别的元素上(实测会误触)。
  let extras = [];
  for (let round = 0; round < 6; round++) {
    await page.waitForTimeout(1500);
    const chipsNow = await readTagChips();
    extras = chipsNow.filter((t) => !tags.includes(t));
    if (!extras.length) { extras = []; break; }
    const removed = await ev(`function(arg){
      var removed=[];
      for(const el of __all()){
        if(String(el.className).indexOf("label-item-v2-container")<0 || !__visible(el)) continue;
        var p=el.querySelector("p");
        if(!p || arg.extras.indexOf(__own(p))<0) continue;
        var icon=el.querySelector("svg.close");
        if(!icon) continue;
        icon.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,view:window}));
        removed.push(__own(p));
      }
      return removed;
    }`, { extras });
    if (!removed.length && extras.length) {
      // svg.close 派发无效时的兜底:聚焦输入框派发 Backspace 删最后一个 chip
      await ev(`function(){
        var input=__all().find(function(el){return el.tagName==="INPUT" && /创建标签/.test(el.placeholder||"");});
        if(!input) return {ok:false};
        input.focus();
        input.dispatchEvent(new KeyboardEvent("keydown",{key:"Backspace",keyCode:8,which:8,bubbles:true}));
        return {ok:true};
      }`);
    }
    await page.waitForTimeout(800);
  }
  if (extras.length) {
    fail(`表单里残留非本次标签(自动插入的推荐清不掉): ${extras.join(", ")}。请在创作中心手动清理后重试。`);
  }
}

// --- 简介 (Quill 编辑器) ---
if (desc) {
  const descResult = await ev(`function(value){
    var editors=__all().filter(function(el){return String(el.className).indexOf("ql-editor")>=0 && __visible(el);});
    var editor=editors.find(function(el){return el.getBoundingClientRect().height>60;})||editors[0];
    if(!editor) return {ok:false,error:"未找到简介编辑器"};
    editor.focus();
    document.execCommand("selectAll",false,null);
    document.execCommand("insertText",false,value);
    editor.blur();
    return {ok:true,text:(editor.innerText||"").trim()};
  }`, desc);
  if (!descResult.ok) fail(descResult.error);
  // Quill 把单个换行渲染成段落(\n\n),回读归一化换行再比较。
  const normText = (s) => String(s || "").replace(/\r\n?/g, "\n").replace(/\n{2,}/g, "\n").trim();
  if (normText(descResult.text) !== normText(desc)) {
    fail(`简介写入异常: 期望「${desc}」实际「${descResult.text}」`);
  }
}

// --- 封面(4:3 与 16:9 分开上传) ---
let coverApplied = { "4x3": false, "16x9": false };
if (cover43 && cover169) {
  const addPt = await ev(`function(){
    return __textPoint("添加封面");
  }`);
  if (!addPt) fail("未找到「添加封面」入口");
  await page.mouse.click(addPt.x, addPt.y, { label: "打开封面制作" });
  await page.waitForTimeout(3000);

  const dlgOpen = await ev(`function(){
    return __all().some(function(el){return String(el.className).indexOf("cover-editor-head")>=0 && __visible(el);});
  }`);
  if (!dlgOpen) fail("「封面制作」弹窗没有出现");
  await page.waitForTimeout(1000);

  // 同步开关是 .sync-checkbox-wrapper 里的可见 checkbox，不是文字，也没有 bcc-checkbox。
  // 弹窗初始化会在点击之后把勾选写回去。读 input.checked，连续两次为关才算关掉。
  const readSync = () => ev(`function(){
    var wrappers=__all().filter(function(el){
      return String(el.className||"").split(" ").indexOf("sync-checkbox-wrapper")>=0;
    });
    var visible=null;
    for(const el of wrappers){
      var r=el.getBoundingClientRect();
      if(r.width>20 && r.height>8) visible=el;
    }
    if(!visible) return {found:false};
    var input=null;
    for(const el of visible.querySelectorAll("input")){
      if(el.type!=="checkbox") continue;
      var box=el.getBoundingClientRect();
      if(box.width<8 || box.height<8) continue;
      input=el;
      break;
    }
    if(!input) return {found:true, checked:null};
    var box=input.getBoundingClientRect();
    return {found:true, checked:input.checked===true, x:box.x+box.width/2, y:box.y+box.height/2};
  }`);
  const ensureSyncOff = async (why) => {
    const readings = [];
    let clicks = 0;
    for (let i = 0; i < 8; i += 1) {
      const state = await readSync();
      if (state.found && state.checked !== null) readings.push(state.checked);
      const plan = syncGate({ readings, clicks });
      if (plan === "ready") return;
      if (plan === "fail") {
        fail(`双比例同步仍开着(${why})，已停止，避免上传覆盖另一张封面`);
      }
      if (plan === "click") {
        if (!state.x) fail(`双比例同步勾选看得见但点不到(${why})`);
        await page.mouse.click(state.x, state.y, { label: "关闭双比例同步改动" });
        clicks += 1;
      }
      await page.waitForTimeout(300);
    }
    fail(`双比例同步状态没有稳定关掉(${why})，已停止`);
  };
  await ensureSyncOff("打开封面弹窗后");

  // 4:3 画布是 16:9 视口，左右是留白。整幅 8×8 会被留白拉低到 0.4，
  // 只取居中 4:3 区域。16:9 图铺满画布，用整幅。阈值不变。
  const readEditorSamples = (kind) => ev(`function(arg){
    var out=[];
    var marker=arg.kind==="4x3"?"editor_4_3":"editor_16_9";
    var root=__all().find(function(el){return String(el.className||"").split(" ").indexOf(marker)>=0;});
    if(!root) return out;
    var nodes=Array.from(root.querySelectorAll("canvas")).filter(function(node){
      return String(node.className||"").indexOf("lower-canvas")>=0;
    });
    if(!nodes.length) nodes=Array.from(root.querySelectorAll("canvas"));
    for(const node of nodes){
      var bw=node.width||0, bh=node.height||0;
      if(bw<20 || bh<20) continue;
      var sx=0, sy=0, sw=bw, sh=bh;
      if(arg.kind==="4x3"){
        sw=Math.round(bh*4/3);
        sh=bh;
        if(sw>bw){ sw=bw; sh=Math.round(bw*3/4); }
        sx=Math.round((bw-sw)/2);
        sy=Math.round((bh-sh)/2);
      }
      try {
        var canvas=document.createElement("canvas");
        canvas.width=8; canvas.height=8;
        var ctx=canvas.getContext("2d");
        ctx.drawImage(node, sx, sy, sw, sh, 0, 0, 8, 8);
        var data=ctx.getImageData(0,0,8,8).data;
        var grid=[];
        for(var i=0;i<data.length;i+=4) grid.push(Math.round(0.299*data[i]+0.587*data[i+1]+0.114*data[i+2]));
        out.push({w:sw,h:sh,grid:grid});
      } catch(error) {}
    }
    return out;
  }`, { kind });
  // 上传 16:9 后手机预览停在「个人空间」。首页推荐那张图是 visibility:hidden，
  // 隐藏期间位图会短暂变成别的 500×375，不能拿它当 4:3 结论。
  // 先点开「首页推荐」，只读当前稿件那一张可见封面，不读后面的推荐卡片。
  const showHomePreview = async () => {
    const tab = await ev(`function(){
      var el=__all().find(function(node){
        return __own(node)==="首页推荐" && String(node.className||"").split(" ").indexOf("button")>=0;
      });
      if(!el) return {found:false};
      var r=el.getBoundingClientRect();
      return {
        found:true,
        active:String(el.className||"").split(" ").indexOf("active")>=0,
        x:r.x+r.width/2,
        y:r.y+r.height/2
      };
    }`);
    if (!tab.found) fail("手机预览没有「首页推荐」");
    if (!tab.active) {
      await page.mouse.click(tab.x, tab.y, { label: "显示首页推荐预览" });
      await page.waitForTimeout(300);
    }
  };
  const readPhone43 = () => ev(`function(){
    var preview=__all().find(function(el){
      var parts=String(el.className||"").split(" ");
      return parts.indexOf("cover-phone-view-home")>=0 && parts.indexOf("preview")>=0;
    });
    if(!preview) return [];
    var previewStyle=getComputedStyle(preview);
    var previewBox=preview.getBoundingClientRect();
    if(previewStyle.visibility==="hidden" || previewStyle.display==="none" || previewBox.width<20) return [];
    var card=preview.querySelector(".cover-phone-view-home-video-item");
    var node=card && (card.querySelector("img") || (card.tagName==="IMG"?card:null));
    if(!node) return [];
    var nodeStyle=getComputedStyle(node);
    var nodeBox=node.getBoundingClientRect();
    if(nodeStyle.visibility==="hidden" || nodeStyle.display==="none" || nodeBox.width<20) return [];
    var w=node.naturalWidth||0, h=node.naturalHeight||0;
    if(w<20 || h<20) return [];
    try {
      var canvas=document.createElement("canvas");
      canvas.width=8; canvas.height=8;
      var ctx=canvas.getContext("2d");
      ctx.drawImage(node,0,0,8,8);
      var data=ctx.getImageData(0,0,8,8).data;
      var grid=[];
      for(var i=0;i<data.length;i+=4) grid.push(Math.round(0.299*data[i]+0.587*data[i+1]+0.114*data[i+2]));
      return [{w:w,h:h,grid:grid}];
    } catch(error) { return []; }
  }`);
  const selectEditor = async (kind) => {
    const marker = kind === "4x3" ? "editor_4_3" : "editor_16_9";
    for (let i = 0; i < 4; i += 1) {
      const state = await ev(`function(arg){
        function info(name){
          var el=__all().find(function(node){return String(node.className||"").split(" ").indexOf(name)>=0;});
          if(!el) return null;
          var parent=el.parentElement;
          var r=el.getBoundingClientRect();
          return {
            active: !!(parent && String(parent.className||"").split(" ").indexOf("active")>=0),
            x: r.x+r.width/2,
            y: r.y+r.height/2
          };
        }
        return {mine: info(arg.marker)};
      }`, { marker });
      if (state.mine && state.mine.active) return;
      if (!state.mine || !state.mine.x) fail(`封面编辑区没有${kind}画布`);
      await page.mouse.click(state.mine.x, state.mine.y, { label: `选中${kind}画布` });
      await page.waitForTimeout(300);
    }
    fail(`${kind}画布没有成为当前上传目标，已停止，避免文件进到另一个槽`);
  };

  const clipRect = (r, vp) => {
    if (!r || !(r.width >= 20) || !(r.height >= 20)) return null;
    const x = Math.max(0, Math.floor(r.x));
    const y = Math.max(0, Math.floor(r.y));
    let width = Math.floor(r.width);
    let height = Math.floor(r.height);
    if (vp) {
      if (x >= vp.w || y >= vp.h) return null;
      width = Math.min(width, vp.w - x);
      height = Math.min(height, vp.h - y);
    }
    if (width < 20 || height < 20) return null;
    return { x, y, width, height };
  };
  // Clip screenshots of Fabric canvases can miss the composited pixels (round 8
  // scored -0.111 on a 315×236 clip while the same region in a full viewport
  // shot scores ~0.93). Always capture the viewport, then crop the PNG.
  const captureViewportPng = async (label = "viewport") => {
    const path = `/tmp/bilibili-cover-${label}.png`;
    try {
      await page.screenshot({ path });
    } catch {
      return null;
    }
    try {
      const buf = readFileSync(path);
      const dims = imageDimsFromBuffer(buf);
      if (!dims || !(dims.width >= 20) || !(dims.height >= 20)) return null;
      const vp = await ev(`function(){ return { vw: window.innerWidth, vh: window.innerHeight }; }`);
      if (!vp || !(vp.vw >= 20) || !(vp.vh >= 20)) return null;
      return { buf, pngW: dims.width, pngH: dims.height, vw: vp.vw, vh: vp.vh, path };
    } catch {
      return null;
    }
  };
  const cssToPngRect = (shot, r) => {
    if (!shot || !r) return null;
    const scaleX = shot.pngW / shot.vw;
    const scaleY = shot.pngH / shot.vh;
    const x = Math.max(0, Math.round(r.x * scaleX));
    const y = Math.max(0, Math.round(r.y * scaleY));
    const width = Math.round(r.width * scaleX);
    const height = Math.round(r.height * scaleY);
    if (x >= shot.pngW || y >= shot.pngH) return null;
    const w = Math.min(width, shot.pngW - x);
    const h = Math.min(height, shot.pngH - y);
    if (w < 20 || h < 20) return null;
    return { x, y, width: w, height: h };
  };
  const sampleVisibleClip = (shot, cssRect, { centerRatio = null } = {}) => {
    if (!shot || !cssRect) return [];
    const clipped = clipRect(cssRect, { w: shot.vw, h: shot.vh });
    const rect = cssToPngRect(shot, clipped);
    if (!rect) return [];
    try {
      const sample = coverSampleFromPng(shot.buf, { rect, centerRatio });
      return sample ? [sample] : [];
    } catch {
      return [];
    }
  };
  const readEditorVisible = async (kind, shot) => {
    if (!shot) return [];
    const info = await ev(`function(arg){
      var marker=arg.kind==="4x3"?"editor_4_3":"editor_16_9";
      var root=__all().find(function(el){return String(el.className||"").split(" ").indexOf(marker)>=0;});
      if(!root) return null;
      // Prefer the painted canvas so a toolbar above the 4:3 picture is not included.
      var inner=root.querySelector("canvas.lower-canvas, canvas, img") || root;
      var r=inner.getBoundingClientRect();
      return { x:r.x, y:r.y, width:r.width, height:r.height };
    }`, { kind });
    return sampleVisibleClip(shot, info, {
      centerRatio: kind === "4x3" ? RATIO_4_3 : null,
    });
  };
  const readPhoneVisible = async (shot) => {
    const info = await ev(`function(wantTitle){
      var preview=__all().find(function(el){
        var parts=String(el.className||"").split(" ");
        return parts.indexOf("cover-phone-view-home")>=0 && parts.indexOf("preview")>=0;
      });
      if(!preview) return null;
      var previewStyle=getComputedStyle(preview);
      var previewBox=preview.getBoundingClientRect();
      if(previewStyle.visibility==="hidden" || previewStyle.display==="none" || previewBox.width<20) return null;
      var items=Array.from(preview.querySelectorAll(".cover-phone-view-home-video-item"));
      var rects=[];
      var pushImg=function(node){
        if(!node) return;
        var s=getComputedStyle(node);
        var r=node.getBoundingClientRect();
        if(s.visibility==="hidden"||s.display==="none"||r.width<20||r.height<20) return;
        rects.push({ x:r.x, y:r.y, width:r.width, height:r.height });
      };
      if(wantTitle){
        var match=items.find(function(item){
          var text=(item.innerText||"")+" "+(item.textContent||"");
          return text.indexOf(wantTitle)>=0;
        });
        if(match){
          pushImg(match.querySelector("img")||(match.tagName==="IMG"?match:null));
          if(rects.length) return { rects:rects, vw:window.innerWidth, vh:window.innerHeight, matched:true };
        }
      }
      items.forEach(function(item){
        var node=item.querySelector("img")||(item.tagName==="IMG"?item:null);
        if(!node) return;
        var r=node.getBoundingClientRect();
        if(r.width<40||r.height<40) return;
        if(Math.abs((r.width/r.height)-(4/3))>0.2) return;
        pushImg(node);
      });
      if(!rects.length) return null;
      return { rects:rects, vw:window.innerWidth, vh:window.innerHeight, matched:false };
    }`, title);
    if (!shot || !info || !Array.isArray(info.rects) || !info.rects.length) {
      return { samples: [], matched: false };
    }
    const samples = [];
    for (let i = 0; i < info.rects.length; i += 1) {
      samples.push(...sampleVisibleClip(shot, info.rects[i]));
    }
    return { samples, matched: !!info.matched };
  };
  const pickCoverJudge = (primary, visible) => {
    if (primary && primary.status === "ok") return primary;
    if (visible && visible.status === "ok") return visible;
    const scoreOf = (j) => (j && Number.isFinite(j.score) ? j.score : -1);
    if (scoreOf(visible) > scoreOf(primary)) return visible;
    if (primary && primary.status !== "unread") return primary;
    return visible || primary || { status: "unread" };
  };
  const judgeVisibleSamples = (samples, opts) => {
    if (!samples || !samples.length) return { status: "unread" };
    let last = { status: "unread" };
    for (const sample of samples) {
      const judged = judgeCoverIdentity({ ...opts, samples: [sample] });
      if (judged.status === "ok") return judged;
      if (judged.status !== "unread") last = judged;
    }
    return last;
  };

  const uploadCover = async (file, kind, source, other) => {
    await selectEditor(kind);
    await ensureSyncOff(`上传${kind}前`);

    const upPt = await ev(`function(){
      return __textPoint("上传封面");
    }`);
    if (!upPt) fail("封面弹窗里找不到「上传封面」");
    const cp = page.waitForFileChooser({ timeout: 15000 });
    await page.mouse.click(upPt.x, upPt.y, { label: `上传${kind}封面` });
    const chooser2 = await cp;
    await chooser2.setFiles(file);
    // 等对应槽位的缩略图出现且比例正确(naturalWidth/Height 来自上传图)。
    let last = { status: "unread" };
    // The Fabric lower-canvas / a 500×375 phone thumb can sit at ~0.73 forever
    // even when the official cover is already painted on screen. Keep the 0.82
    // threshold. Sample visible pixels from a viewport screenshot (not a clip
    // shot). A 120×90 home-preview card with a gradient overlay cannot hit 0.82,
    // so a titled card is enough once the editor visible/canvas path has passed.
    const coverWaitMs = 500;
    const coverWaitTries = 120;
    for (let i = 0; i < coverWaitTries; i++) {
      await page.waitForTimeout(coverWaitMs);
      if (kind === "4x3") await showHomePreview();
      const shot = await captureViewportPng(`viewport-${kind}-${i}`);
      const editorCanvas = judgeCoverIdentity({
        samples: await readEditorSamples(kind),
        target: RATIO_4_3,
        source,
        other,
        slot: kind === "4x3" ? "editor_4_3" : "editor_16_9",
        requireRatio: false,
      });
      const editorVisible = judgeVisibleSamples(await readEditorVisible(kind, shot), {
        target: RATIO_4_3,
        source,
        other,
        slot: kind === "4x3" ? "editor_4_3" : "editor_16_9",
        requireRatio: false,
      });
      const editor = pickCoverJudge(editorCanvas, editorVisible);
      if (kind !== "4x3") {
        last = editor;
        if (i === 0 || (i + 1) % 10 === 0 || editor.status === "ok") {
          console.error(JSON.stringify({ coverWait: { kind, i, elapsedMs: (i + 1) * coverWaitMs, editor, editorCanvas, editorVisible } }));
        }
        if (editor.status === "ok") return { ...editor.evidence, via: editor === editorCanvas ? "canvas" : "visible" };
        continue;
      }
      const phoneImg = judgeCoverIdentity({
        samples: await readPhone43(),
        target: RATIO_4_3,
        source,
        other,
        slot: "cover-phone-view-home-video-img",
        requireRatio: true,
      });
      const phoneRead = await readPhoneVisible(shot);
      const phoneVisible = judgeVisibleSamples(phoneRead.samples, {
        target: RATIO_4_3,
        source,
        other,
        slot: "cover-phone-view-home-video-img",
        requireRatio: false,
      });
      const phone = pickCoverJudge(phoneImg, phoneVisible);
      const phoneOk = phone.status === "ok" || (editor.status === "ok" && phoneRead.matched);
      if (i === 0 || (i + 1) % 10 === 0 || (editor.status === "ok" && phoneOk)) {
        console.error(JSON.stringify({ coverWait: { kind, i, elapsedMs: (i + 1) * coverWaitMs, editor, phone, editorCanvas, editorVisible, phoneImg, phoneVisible, phoneTitled: phoneRead.matched } }));
      }
      if (editor.status === "ok" && phoneOk) {
        return {
          ...(phone.status === "ok" ? phone.evidence : editor.evidence),
          editorMatch: editor.evidence.match,
          via: {
            editor: editor === editorCanvas ? "canvas" : "visible",
            phone: phone.status === "ok" ? (phone === phoneImg ? "img" : "visible") : "titled-card",
          },
          phoneTitled: phoneRead.matched,
        };
      }
      last = editor.status === "ok" ? phone : editor;
    }
    fail(`${kind} 封面在 60 秒内对不上原图(${last.status}): ${JSON.stringify(last)}`);
  };

  const fingerprintFile = (file) => {
    const buf = readFileSync(file);
    const png = pngFingerprint(buf);
    if (png) return png;
    const dims = imageDimsFromBuffer(buf);
    const decoded = spawnSync("ffmpeg", ["-v", "error", "-i", file, "-f", "rawvideo", "-pix_fmt", "rgba", "-vframes", "1", "pipe:1"], {
      maxBuffer: 64 * 1024 * 1024,
    });
    if (!dims || decoded.status !== 0 || !decoded.stdout || decoded.stdout.length < dims.width * dims.height * 4) return null;
    const rgba = decoded.stdout.subarray(0, dims.width * dims.height * 4);
    const center = centerRgba(rgba, dims.width, dims.height);
    return {
      full: lumaGridFromRgba(rgba, dims.width, dims.height),
      center: lumaGridFromRgba(center.rgba, center.width, center.height),
    };
  };
  const source43 = fingerprintFile(cover43);
  const source169 = fingerprintFile(cover169);
  if (!source43 || !source169) fail("无法计算封面指纹，不能确认槽位里是哪张图");

  const cover43Evidence = await uploadCover(cover43, "4x3", source43, source169);
  if (!cover43Evidence) fail("4:3 封面上传后未确认,放弃投稿");
  const cover169Evidence = await uploadCover(cover169, "16x9", source169, source43);
  if (!cover169Evidence) fail("16:9 封面上传后未确认,放弃投稿");
  // 16:9 文件若进了 4:3 画布，或同步把 4:3 换成了 16:9，这里看的是 4:3 画布本身。
  // 不拿另一块较小的残留图充数。
  let still43 = { status: "unread" };
  for (let i = 0; i < 8; i += 1) {
    await showHomePreview();
    const editorCanvas = judgeCoverIdentity({
      samples: await readEditorSamples("4x3"),
      target: RATIO_4_3,
      source: source43,
      other: source169,
      slot: "editor_4_3",
      requireRatio: false,
    });
    const shot = await captureViewportPng(`viewport-still43-${i}`);
    const editorVisible = judgeVisibleSamples(await readEditorVisible("4x3", shot), {
      target: RATIO_4_3,
      source: source43,
      other: source169,
      slot: "editor_4_3",
      requireRatio: false,
    });
    const editor = pickCoverJudge(editorCanvas, editorVisible);
    const phoneImg = judgeCoverIdentity({
      samples: await readPhone43(),
      target: RATIO_4_3,
      source: source43,
      other: source169,
      slot: "cover-phone-view-home-video-img",
      requireRatio: true,
    });
    const phoneRead = await readPhoneVisible(shot);
    const phoneVisible = judgeVisibleSamples(phoneRead.samples, {
      target: RATIO_4_3,
      source: source43,
      other: source169,
      slot: "cover-phone-view-home-video-img",
      requireRatio: false,
    });
    const phone = pickCoverJudge(phoneImg, phoneVisible);
    const phoneOk = phone.status === "ok" || (editor.status === "ok" && phoneRead.matched);
    if (editor.status === "unread" || (phone.status === "unread" && !phoneRead.matched)) {
      still43 = { status: "unread" };
      await page.waitForTimeout(400);
      continue;
    }
    still43 = editor.status === "ok" && phoneOk
      ? { status: "ok", evidence: { ...(phone.status === "ok" ? phone.evidence : editor.evidence), editorMatch: editor.evidence.match, via: { editor: editor === editorCanvas ? "canvas" : "visible", phone: phone.status === "ok" ? (phone === phoneImg ? "img" : "visible") : "titled-card" }, phoneTitled: phoneRead.matched } }
      : { status: "identity", editor, phone, editorCanvas, editorVisible, phoneImg, phoneVisible, phoneTitled: phoneRead.matched };
    break;
  }
  if (still43.status !== "ok") {
    const syncNow = await readSync();
    const why = still43.status === "mismatch"
      ? "上传 16:9 后 4:3 槽位比例变了"
      : `上传 16:9 后未能确认 4:3 槽仍是原图(${still43.status})`;
    fail(`${why}: ${JSON.stringify({ ...still43, syncChecked: syncNow.checked })}`);
  }
  try { await page.screenshot({ path: "/tmp/bilibili-cover-slots.png" }); } catch {}
  coverApplied = { "4x3": still43.evidence, "16x9": cover169Evidence };

  // 完成可能需要多轮:点「完成」后若弹「检测到个人空间封面(16:9)未修改」,
  // 必须选「不同步,手动编辑」保住分开上传的 16:9(绝不点「确认同步」),
  // 然后编辑器会切到 16:9 手动编辑视图,再点一次「完成」才真正关闭。
  for (let i = 0; i < 4; i++) {
    await page.waitForTimeout(2000);
    const dlgState = await ev(`function(){
      var vis=function(el){return !!(el.getClientRects().length);};
      var editor=__all().some(function(el){return String(el.className).indexOf("cover-editor-head")>=0 && vis(el);});
      var modal=__all().some(function(el){return String(el.className).indexOf("videoup-confirm-modal")>=0 && vis(el);});
      return {editor:editor, modal:modal};
    }`);
    if (!dlgState.editor && !dlgState.modal) break;
    if (dlgState.modal) {
      const keepPt = await ev(`function(){
        var vis=function(el){return !!(el.getClientRects().length);};
        function inModal(el){var p=el;for(var i=0;i<8&&p;i++){if(String(p.className||"").indexOf("videoup-confirm-modal")>=0)return true;p=p.parentElement;}return false;}
        var span=__all().find(function(el){
          return vis(el) && __own(el) && /不同步/.test(__own(el)) && inModal(el);
        });
        if(!span) return null;
        var r=span.getBoundingClientRect();
        return {x:r.x+r.width/2,y:r.y+r.height/2};
      }`);
      if (!keepPt) fail("封面确认弹窗里找不到「不同步,手动编辑」");
      await page.mouse.click(keepPt.x, keepPt.y, { label: "选择不同步,手动编辑" });
      await page.waitForTimeout(1500);
      continue;
    }
    const donePt = await ev(`function(){
      var btn=__all().find(function(el){return __own(el)==="完成" && String(el.className).indexOf("submit")>=0;});
      if(!btn) return null;
      return __pointInView(btn);
    }`);
    if (!donePt) fail("封面弹窗里找不到「完成」按钮");
    await page.mouse.click(donePt.x, donePt.y, { label: "确认封面" });
  }

  const dlgClosed = await ev(`function(){
    return !__all().some(function(el){return String(el.className).indexOf("cover-editor-head")>=0 && __visible(el);});
  }`);
  if (!dlgClosed) fail("点「完成」后封面弹窗没有关闭");
  const formCover = await ev(`function(){
    var el=__all().find(function(el){return String(el.className).indexOf("cover-img")>=0 && el.getBoundingClientRect().width>50;});
    if(!el) return {ok:false,error:"表单上没有 .cover-img 预览"};
    var bg=getComputedStyle(el).backgroundImage||"";
    return {ok: bg.indexOf("url(")>=0, bg: bg.slice(0,120)};
  }`);
  if (!formCover.ok) fail("封面未落到投稿表单(.cover-img 背景为空)");
}

// --- 创作声明 ---
// bcc-select 预填时 input.value 已是组件当前值。点输入框中心不会展开列表,
// 未展开时选项高度为 0,按可见文本去找会误报「没有选项」。
// 只有回读不一致才点下拉右侧箭头,并等选项高度大于 0。
const declareText = DECLARE_OPTIONS[cfg.declare] || DECLARE_OPTIONS.none;
const readDeclare = () => ev(`function(){
  var input=__all().find(function(el){
    if(el.tagName!=="INPUT" || !/创作声明/.test(el.placeholder||"")) return false;
    var r=el.getBoundingClientRect();
    return r.width>20 && r.height>10;
  });
  return input ? String(input.value||"").trim() : "";
}`);
let declareFinal = "";
const applyDeclare = async () => {
declareFinal = await readDeclare();
if (!declareFinal && declareFinal !== "") fail("未找到创作声明下拉");
let declareDecision = declareChoice({ requested: declareText, current: declareFinal, options: [] });
if (declareDecision.action !== "keep") {
  const opener = await ev(`function(){
    var input=__all().find(function(el){return el.tagName==="INPUT" && /创作声明/.test(el.placeholder||"");});
    if(!input) return null;
    var wrap=input.closest(".bcc-select") || input;
    wrap.scrollIntoView({block:"center", behavior:"instant"});
    var r=wrap.getBoundingClientRect();
    return {x:r.x+r.width-18, y:r.y+r.height/2};
  }`);
  if (!opener) fail("未找到创作声明下拉");
  await page.mouse.click(opener.x, opener.y, { label: "打开创作声明下拉" });
  let optionNames = [];
  for (let i = 0; i < 8 && !optionNames.length; i += 1) {
    await page.waitForTimeout(300);
    optionNames = await ev(`function(){
      var names=[];
      for (const el of __all()) {
        var own=(__own(el)||"").trim();
        if(!own) continue;
        var r=el.getBoundingClientRect();
        if(r.width>0 && r.height>0) names.push(own);
      }
      return names;
    }`);
    optionNames = optionNames.filter((name) => Object.values(DECLARE_OPTIONS).includes(name));
  }
  declareDecision = declareChoice({ requested: declareText, current: declareFinal, options: optionNames });
  if (declareDecision.action !== "select") {
    fail(`创作声明下拉里没有「${declareText}」,当前值是「${declareFinal || "空"}」`);
  }
  const readOptionRow = () => ev(`function(arg){
    var span=__all().find(function(el){return (__own(el)||"").trim()===arg.text;});
    var option=span && span.closest(".bcc-option");
    if(!option) return {found:false};
    if(option.getBoundingClientRect().height<12) option.scrollIntoView({block:"center", behavior:"instant"});
    var r=option.getBoundingClientRect();
    var x=r.x+Math.min(80, r.width/2);
    var y=r.y+r.height/2;
    var top=document.elementFromPoint(x, y);
    var hit=top;
    while(hit && hit!==option) hit=hit.parentElement || (hit.getRootNode && hit.getRootNode().host) || null;
    return {found:true, y:r.y, height:r.height, x:x, cy:y, onRow:hit===option};
  }`, { text: declareText });
  let optionPoint = null;
  let previousY = null;
  for (let i = 0; i < 8; i += 1) {
    const row = await readOptionRow();
    const plan = optionClickReady({ previousY, y: row.y, height: row.height });
    if (plan === "click" && row.onRow) {
      optionPoint = { x: row.x, y: row.cy };
      break;
    }
    previousY = Number.isFinite(row.y) ? row.y : previousY;
    await page.waitForTimeout(80);
  }
  if (!optionPoint) fail(`创作声明「${declareText}」的选项行还没停稳,已停止,没有改选`);
  await page.mouse.click(optionPoint.x, optionPoint.y, { label: "选择创作声明" });
  await page.waitForTimeout(400);
  declareFinal = await readDeclare();
  const selectedText = await ev(`function(){
    var selected=__all().find(function(el){
      var parts=String(el.className||"").split(" ");
      return parts.indexOf("bcc-option")>=0 && parts.indexOf("selected")>=0;
    });
    return selected ? String(selected.textContent||"").trim() : "";
  }`);
  if (selectedText && selectedText !== declareText) {
    fail(`创作声明列表勾选的是「${selectedText}」,不是「${declareText}」`);
  }
}
if (declareFinal !== declareText) {
  fail(`创作声明回读不是「${declareText}」(实际「${declareFinal || "空"}」)`);
}
if (declareDecision.action === "select") {
  if (page.keyboard && typeof page.keyboard.press === "function") {
    try { await page.keyboard.press("Escape"); } catch {}
  }
  const away = await ev(`function(){
    var el=__byTextExact("基本设置");
    return el ? __pointInView(el) : null;
  }`);
  if (away) await page.mouse.click(away.x, away.y, { label: "收起创作声明" });
  await page.waitForTimeout(300);
  declareFinal = await readDeclare();
  if (declareFinal !== declareText) {
    fail(`收起创作声明后回读不是「${declareText}」(实际「${declareFinal || "空"}」)`);
  }
}
};

// --- 分区 ---
// The remembered chip lives in .video-human-type .select-item-cont-inserted.
// Opening .select-controller reveals .human-type-list; choosing a missing name
// must stop before 立即投稿 instead of keeping the old chip.
const readPartition = () => ev(`function(){
  var root=__all().find(function(el){return String(el.className||"").split(" ").indexOf("video-human-type")>=0;});
  if(!root) return {ok:false,error:"未找到分区区域"};
  var chip=null;
  for(const el of __walk(root)){
    if(String(el.className).indexOf("select-item-cont-inserted")>=0){chip=(__own(el)||"").trim();break;}
  }
  return {ok:true,chip:chip};
}`);
let typeState = await readPartition();
if (!typeState.ok) fail(typeState.error);
const requestedType = String(cfg.type || "").trim();
if (requestedType && typeState.chip !== requestedType) {
  const opener = await ev(`function(){
    var root=__all().find(function(el){return String(el.className||"").split(" ").indexOf("video-human-type")>=0;});
    var ctrl=root && root.querySelector(".select-controller");
    if(!ctrl) return null;
    return __pointInView(ctrl);
  }`);
  if (!opener) fail(`分区「${requestedType}」无法打开人选列表,已停止,没有沿用「${typeState.chip || "空"}」`);
  await page.mouse.click(opener.x, opener.y, { label: "打开分区列表" });
  const readOptionNames = () => ev(`function(){
    var names=[];
    for(const el of __all()){
      if(String(el.className).indexOf("item-cont-main")<0 || !__visible(el)) continue;
      var name=(__own(el)||"").trim();
      if(name && names.indexOf(name)<0) names.push(name);
    }
    return names;
  }`);
  let optionNames = [];
  let reopened = false;
  for (let i = 0; i < 8; i += 1) {
    await page.waitForTimeout(300);
    optionNames = await readOptionNames();
    if (optionNames.includes(requestedType)) break;
    if (!reopened && i === 3 && optionNames.length === 0) {
      reopened = true;
      const again = await ev(`function(){
        var root=__all().find(function(el){return String(el.className||"").split(" ").indexOf("video-human-type")>=0;});
        var ctrl=root && root.querySelector(".select-controller");
        return ctrl ? __pointInView(ctrl) : null;
      }`);
      if (again) await page.mouse.click(again.x, again.y, { label: "再次打开分区列表" });
    }
  }
  const choice = partitionChoice({ requested: requestedType, current: typeState.chip, options: optionNames });
  if (choice.action !== "select") {
    fail(`分区「${requestedType}」不在人选列表里,已停止,没有沿用「${typeState.chip || "空"}」。看到:${optionNames.join("、") || "空"}`);
  }
  const optionPt = await ev(`function(arg){
    var item=__all().find(function(el){
      return el.getAttribute && el.getAttribute("title")===arg.name && String(el.className).indexOf("drop-list-v2-item")>=0 && __visible(el);
    });
    if(!item) return null;
    return __pointInView(item);
  }`, { name: requestedType });
  if (!optionPt) fail(`分区「${requestedType}」可见但点不到,已停止,没有沿用「${typeState.chip || "空"}」`);
  await page.mouse.click(optionPt.x, optionPt.y, { label: `选择分区${requestedType}` });
  await page.waitForTimeout(800);
  typeState = await readPartition();
  if (!typeState.ok || typeState.chip !== requestedType) {
    fail(`分区回读不是「${requestedType}」(实际「${typeState.chip || ""}」),已停止投稿`);
  }
}
const kept = partitionChoice({ requested: requestedType, current: typeState.chip, options: requestedType ? [requestedType] : [] });
if (kept.action === "fail") {
  fail("分区为空:B 站投稿必须选分区。请传 --type,或先在创作中心留下一个分区。");
}
const partitionListOpen = () => ev(`function(){
  return __all().some(function(el){
    if(String(el.className||"").indexOf("human-type-list")<0) return false;
    var r=el.getBoundingClientRect();
    return r.height>20 && r.width>20;
  });
}`);
for (let i = 0; i < 3 && await partitionListOpen(); i += 1) {
  const closer = await ev(`function(){
    var el=__byTextExact("标题") || __byTextExact("基本设置");
    return el ? __pointInView(el) : null;
  }`);
  if (closer) await page.mouse.click(closer.x, closer.y, { label: "收起分区列表" });
  await page.waitForTimeout(400);
}
typeState = await readPartition();
if (requestedType && typeState.chip !== requestedType) {
  fail(`收起分区列表后回读不是「${requestedType}」(实际「${typeState.chip || "空"}」)`);
}
if (await partitionListOpen()) {
  fail("分区列表没有收起,已停止,避免点击落到声明上");
}
// 分区点击会盖住仍开着的声明列表,并把声明打回默认值。分区定下来后再改声明。
await applyDeclare();
declareFinal = await readDeclare();
typeState = await readPartition();
if (declareFinal !== declareText) {
  fail(`停投前创作声明回读不是「${declareText}」(实际「${declareFinal || "空"}」)`);
}
if (requestedType && typeState.chip !== requestedType) {
  fail(`停投前分区回读不是「${requestedType}」(实际「${typeState.chip || "空"}」)`);
}

// --- 立即投稿 ---
// The only click. stop-before-submit and a missing --yes both refuse it.
const submitGate = mayClickSubmit({ yes: cfg.yes === true, stopBeforeSubmit: cfg.stopBeforeSubmit === true });
if (!submitGate.allow) {
  const dir = "/tmp";
  let shot = "";
  try {
    shot = await page.screenshot({ path: `${dir}/bilibili-video-stop.png` });
  } catch {}
  console.log(JSON.stringify({
    ok: true,
    submitted: false,
    stopped_before_submit: true,
    reason: submitGate.reason,
    title,
    type: typeState.chip,
    declare: declareFinal,
    tags,
    covers: coverApplied,
    cover_slots: "/tmp/bilibili-cover-slots.png",
    screenshot: shot || `${dir}/bilibili-video-stop.png`,
  }));
  if (!keep) {
    try { await task.finish({ keep: [] }); } catch {}
  }
  process.exit(0);
}
const submitPt = await ev(`function(){
  var btn=__all().find(function(el){return __own(el)==="立即投稿" && String(el.className).indexOf("submit-add")>=0;});
  if(!btn) return null;
  btn.scrollIntoView({block:"center"});
  return __point(btn);
}`);
if (!submitPt) fail("未找到「立即投稿」按钮");
const submitUrlBefore = await page.url();
await page.waitForTimeout(500);
const receipt = await page.mouse.click(submitPt.x, submitPt.y, { label: "点击立即投稿" });
if (receipt && receipt.dialog) await page.acceptDialog();
await page.waitForTimeout(3000);

// 提交后可能出现确认/清单弹窗(如「稿件确认」类):有「确认/提交」按钮就点掉,
// 其余弹窗原样截图留证,绝不盲目点「取消」以外的按钮。
const submitDialog = await ev(`function(){
  var vis=function(el){return !!(el.getClientRects().length);};
  var dlgs=__all().filter(function(el){return vis(el) && /bcc-dialog|confirm-modal|modal/i.test(String(el.className)) && el.getBoundingClientRect().width>200 && el.getBoundingClientRect().width<900;});
  var out=[];
  for(const d of dlgs){
    var texts=[];
    for(const el of __walk(d)){
      if(__own(el) && __own(el).length<30) texts.push(__own(el));
      if(texts.length>12) break;
    }
    out.push({cls:String(d.className).slice(0,60),texts:texts});
  }
  return out;
}`);
if (submitDialog.length) {
  console.error(JSON.stringify({ note: "提交后出现弹窗", dialogs: submitDialog }));
  const confirmPt = await ev(`function(){
    var vis=function(el){return !!(el.getClientRects().length);};
    var span=__all().find(function(el){
      if(!vis(el)) return false;
      var t=__own(el);
      return (t==="确认"||t==="确认投稿"||t==="提交") && String(t).length<=6;
    });
    if(!span) return null;
    var r=span.getBoundingClientRect();
    return {x:r.x+r.width/2,y:r.y+r.height/2};
  }`);
  if (confirmPt) {
    await page.mouse.click(confirmPt.x, confirmPt.y, { label: "点击提交确认" });
    await page.waitForTimeout(2000);
  }
  try {
    await page.screenshot({ path: "/tmp/bilibili-video-submit-step.png" });
  } catch {}
}

// --- 成功判定 ---
// 立即投稿后页面可能整页跳转(重定向到稿件管理/成功页),SPA 上下文会重建,
// 探测要容忍白屏骨架期,并以「URL 离开投稿页 + 文本命中」双重观察。
let published = false;
let finalText = "";
let finalUrl = submitUrlBefore;
for (let i = 0; i < 60; i++) {
  await page.waitForTimeout(3000);
  let st;
  try {
    st = await ev(`function(arg){
      return { url: location.href, text: __shadowText() + "\\n" + (document.body.innerText||"") };
    }`);
  } catch {
    // 导航瞬间 evaluate 可能抛错,跳过本轮
    continue;
  }
  finalText = st.text;
  finalUrl = st.url;
  if (PUBLISH_OK_RE.test(st.text)) { published = true; break; }
  // URL 已离开投稿页且页面稳定渲染(不再是骨架)也继续等文本命中;
  // 只在超时后统一失败并带 URL/截图报错。
}
if (!published) {
  let shot = "/tmp/bilibili-video-publish-fail.png";
  try {
    shot = await page.screenshot({ path: shot });
  } catch {}
  fail(`点击立即投稿后未确认到成功状态。截图: ${shot}`, {
    finalText: finalText.slice(0, 400),
    finalUrl,
  });
}

async function fetchCreatorJson(url) {
  return ev(`async function(arg){
    try {
      var r = await fetch(arg.url, { credentials: "include" });
      var text = await r.text();
      var json = null;
      try { json = JSON.parse(text); } catch (e) {}
      return { ok: r.ok, status: r.status, json: json };
    } catch (e) {
      return { ok: false, status: 0, json: null };
    }
  }`, { url });
}

async function lookupManuscriptByTitle(wantedTitle) {
  const urls = archivesSearchUrls(wantedTitle);
  const payloads = [];
  for (const url of [urls.keyword, urls.pubing, urls.all]) {
    try {
      const res = await fetchCreatorJson(url);
      if (res && res.json) payloads.push(res.json);
    } catch {
      // One endpoint failing should not stop the others.
    }
  }
  return pickManuscriptFromArchivePayloads(payloads, wantedTitle);
}

async function lookupManuscriptFromManager(wantedTitle) {
  const pages = [
    "https://member.bilibili.com/platform/upload-manager/article",
    "https://member.bilibili.com/platform/upload-manager/article?group=is_pubing&page=1",
    "https://member.bilibili.com/platform/upload-manager/article?group=pubed&page=1",
  ];
  for (const href of pages) {
    await page.goto(href, { waitUntil: "domcontentloaded", timeout: 45000 });
    await page.waitForTimeout(2000);
    const link = await ev(`function(arg){
      var hit=__all().find(function(el){
        var text=el.innerText||"";
        var href=el.href||el.getAttribute("href")||"";
        return text.indexOf(arg.title)>=0 && /BV[0-9A-Za-z]{10}/.test(text + "\n" + href);
      });
      if (!hit) return "";
      return (hit.href || hit.getAttribute("href") || hit.innerText || "");
    }`, { title: wantedTitle });
    const again = manuscriptFromText(link);
    if (again.identity === "bvid") return again;
  }
  return { bvid: null, url: null, identity: "unconfirmed" };
}

let found = manuscriptFromText(`${finalText}\n${finalUrl}`);
if (found.identity !== "bvid") {
  try {
    for (let i = 0; i < MANUSCRIPT_LOOKUP_ATTEMPTS; i++) {
      found = await lookupManuscriptByTitle(title);
      if (found.identity === "bvid") break;
      if (i < MANUSCRIPT_LOOKUP_ATTEMPTS - 1) {
        await page.waitForTimeout(MANUSCRIPT_LOOKUP_INTERVAL_MS);
      }
    }
  } catch {
    // The submit already happened. Keep looking in the manager UI.
  }
}
if (found.identity !== "bvid") {
  try {
    found = await lookupManuscriptFromManager(title);
  } catch {
    // A missing id is reported as unconfirmed.
  }
}
console.log(JSON.stringify(publishSuccessBody({
  title,
  type: typeState.chip,
  declare: declareFinal,
  tags,
  coverApplied,
  bvid: found.bvid,
  url: found.url,
  identity: found.identity,
})));
if (!keep) await task.finish({ keep: [] });
