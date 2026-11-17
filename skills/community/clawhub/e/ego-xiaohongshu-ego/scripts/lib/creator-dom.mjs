// Browser-side creator.xiaohongshu.com actions.
// page.evaluate serializes creatorAct alone. Every helper lives inside the
// function. Do not call module-level functions from it.
// Node tests also rebuild it with new Function so a closure throws.

export const VIDEO_INPUT_SELECTOR = "input.upload-input";
export const COVER_INPUT_SELECTOR = "input.pk-cover-list-file-input";
export const PK_COVER_CLOSE_SELECTOR = ".pk-cover-list-slide-close";
// 2026-11-05 capture: the old 选择图片上传 control is gone. The main cover
// now lives in the cover editor dialog: hover the 主封面 card, click
// 编辑封面 (.cover-edit-entry), upload into .upload-btn input.upload-input,
// then click the 完成 button.
export const MAIN_COVER_CARD_SELECTOR = ".cover--column .default.column";
export const COVER_EDIT_ENTRY_SELECTOR = ".cover-edit-entry";

export function creatorAct(payload) {
  const doc = globalThis.document;
  if (!doc) return { ok: false, error: "creatorAct requires a document" };

  const NICK_SELECTORS = [
    "[class*='user-name']",
    "[class*='nickname']",
    "[class*='nick-name']",
    "[class*='account-name']",
    ".user-info .name",
    "header .name",
  ];
  const NAV = {
    "首页": 1, "笔记管理": 1, "发布笔记": 1, "数据中心": 1, "上传视频": 1,
    "创作灵感": 1, "登录": 1, "发布": 1, "暂存离开": 1, "创作服务平台": 1,
    "设置封面": 1, "换封面": 1, "填写标题": 1,
  };

  function qsa(selector) {
    if (typeof doc.querySelectorAll !== "function") return [];
    return [...doc.querySelectorAll(selector)];
  }

  function qs(selector) {
    if (typeof doc.querySelector !== "function") return null;
    return doc.querySelector(selector);
  }

  function bodyText() {
    const body = doc.body;
    if (!body) return "";
    return String(body.innerText || body.textContent || "");
  }

  function usableNick(text) {
    const value = String(text || "").replace(/\s+/g, " ").trim();
    if (!value || value.length > 32) return "";
    if (NAV[value]) return "";
    if (/^https?:/i.test(value)) return "";
    return value;
  }

  function nicknameFrom() {
    for (let i = 0; i < NICK_SELECTORS.length; i += 1) {
      const nodes = qsa(NICK_SELECTORS[i]);
      for (let n = 0; n < nodes.length; n += 1) {
        const name = usableNick(nodes[n] && (nodes[n].innerText || nodes[n].textContent));
        if (name) return name;
      }
    }
    return "";
  }

  function isFileInput(el) {
    return Boolean(el) && el.tagName === "INPUT" && String(el.getAttribute("type") || "").toLowerCase() === "file";
  }

  function labelOf(el) {
    const nodes = el && el.childNodes ? [...el.childNodes] : [];
    const own = nodes
      .filter((node) => node && node.nodeType === 3)
      .map((node) => String(node.textContent || "").trim())
      .join("");
    const full = String((el && (el.innerText || el.textContent)) || "").trim().replace(/\s+/g, "");
    return { own: own.replace(/\s+/g, ""), full };
  }

  function fileInput(selector, label) {
    const found = qs(selector);
    if (!found || found.tagName !== "INPUT") return { ok: false, error: `${label} file input not found` };
    return { ok: true, selector, accept: found.getAttribute("accept") || "" };
  }

  function coverCountFrom(text) {
    const source = String(text || "");
    const near = source.match(/封面[^0-9\n]{0,24}(\d+)\s*\/\s*3/);
    const counter = near || source.match(/(?:^|[^\d])(\d+)\s*\/\s*3/);
    if (!counter) return { coverCount: null, counterText: "" };
    const count = Number(counter[1]);
    if (!Number.isFinite(count)) return { coverCount: null, counterText: "" };
    return { coverCount: count, counterText: `${count}/3` };
  }

  function mark(el, name) {
    if (el && typeof el.setAttribute === "function") el.setAttribute(name, "1");
    return `[${name}='1']`;
  }

  const request = payload && typeof payload === "object" ? payload : {};
  const op = request.op || "probe";
  const href = String((globalThis.location && globalThis.location.href) || "");
  const text = bodyText();

  if (op === "probe") {
    return {
      ok: true,
      text: text.slice(0, 4000),
      url: href,
      title: String(doc.title || ""),
      nickname: nicknameFrom(),
      loginWall: /\/login(?:\b|[/?#]|$)/i.test(href) || /扫码登录|二维码登录|请使用小红书App扫码/.test(text),
      creatorChrome: /发布笔记|笔记管理|上传视频|创作服务平台|数据中心|重新上传|设置封面|填写标题/.test(text),
    };
  }

  if (op === "video-input") return fileInput("input.upload-input", "video");

  // The image-tab input shares the upload-input class with the video input.
  // Only the accept attribute tells them apart (2026-11-05 capture:
  // images accept ".jpg,.jpeg,.png,.webp" with multiple; video accepts
  // ".mp4,.mov,..."). Do not treat a video accept as an image input.
  function acceptKind(accept) {
    const value = String(accept || "").toLowerCase();
    if (!value) return "unknown";
    if (/\.(mp4|mov|flv|f4v|mkv|rm|m4v|mpg|mpeg|ts)/.test(value)) return "video";
    if (/image\//.test(value) || /\.(jpg|jpeg|png|webp)/.test(value)) return "image";
    return "unknown";
  }

  function isLeaf(el) {
    const kids = el && el.childNodes ? el.childNodes : [];
    for (let i = 0; i < kids.length; i += 1) {
      if (!kids[i] || kids[i].nodeType !== 3) return false;
    }
    return true;
  }

  if (op === "image-tab") {
    const nodes = qsa("*").filter((el) => {
      const label = labelOf(el);
      return (label.full === "上传图文" || label.own === "上传图文") && isLeaf(el);
    });
    const target = nodes.length ? nodes[nodes.length - 1] : null;
    if (!target) return { ok: false, error: "上传图文 tab not found" };
    if (typeof target.click !== "function") return { ok: false, error: "上传图文 tab is not clickable" };
    target.click();
    return { ok: true, href, tag: target.tagName };
  }

  if (op === "image-input") {
    const inputs = qsa("input").filter(isFileInput);
    const imageInputs = inputs.filter((el) => acceptKind(el.getAttribute("accept")) === "image");
    if (!imageInputs.length) {
      return { ok: false, error: "image upload input not found; click 上传图文 first" };
    }
    const input = imageInputs[imageInputs.length - 1];
    return {
      ok: true,
      selector: mark(input, "data-xhs-image-input"),
      accept: input.getAttribute("accept") || "",
      multiple: Boolean(input.multiple) || String(input.getAttribute("multiple") || "") === "multiple",
      count: imageInputs.length,
    };
  }

  if (op === "image-state") {
    const imgs = qsa("img");
    const uploads = imgs.filter((el) => {
      const src = String(el.getAttribute("src") || "");
      return src.startsWith("blob:") || /sns-img/i.test(src);
    });
    const counter = text.match(/(\d+)\s*\/\s*18/);
    return {
      ok: true,
      uploadThumbs: uploads.length,
      imgTotal: imgs.length,
      counter: counter ? Number(counter[1]) : null,
      pending: /上传中\s*\d+%/.test(text),
      failed: /上传失败|格式不支持|图片过大|图片尺寸不符合/.test(text),
      text: text.slice(0, 800),
    };
  }

  function classList(el) {
    return String((el && el.className) || "").split(/\s+/).filter(Boolean);
  }

  function isPkInput(el) {
    return classList(el).includes("pk-cover-list-file-input");
  }

  if (op === "cover-input") {
    const found = fileInput("input.pk-cover-list-file-input", "PK cover");
    if (!found.ok) return found;
    if (found.accept && !/\.png|\.jpg|\.jpeg|image\//i.test(found.accept)) {
      return { ok: false, error: "cover input accept does not allow png or jpg" };
    }
    return { ...found, scope: "pk" };
  }

  if (op === "dialog-cover-input") {
    const inputs = qsa("input").filter(isFileInput).filter((el) => {
      const parent = el.parentElement;
      return parent && classList(parent).includes("upload-btn");
    });
    const input = inputs.find((el) => acceptKind(el.getAttribute("accept")) === "image");
    if (!input) {
      return { ok: false, error: "cover editor image input (.upload-btn) not found; click 编辑封面 first" };
    }
    if (isPkInput(input)) return { ok: false, error: "refusing the PK cover input for the main cover" };
    return { ok: true, selector: mark(input, "data-xhs-editor-cover"), via: "编辑封面", scope: "main" };
  }

  if (op === "cover-editor-state") {
    // Inline selector: creatorAct is serialized and must not touch module scope.
    const input = qs(".upload-btn input.upload-input");
    const done = qsa("button").find((el) => {
      const t = String(el.innerText || "").replace(/\s+/g, "");
      return t === "完成" || labelOf(el).full === "完成";
    });
    return {
      ok: true,
      dialogOpen: Boolean(input),
      doneFound: Boolean(done),
      doneEnabled: Boolean(done) && !done.disabled,
    };
  }

  if (op === "click-cover-editor-done") {
    const done = qsa("button").find((el) => {
      const t = String(el.innerText || "").replace(/\s+/g, "");
      return t === "完成" || labelOf(el).full === "完成";
    });
    if (!done) return { ok: false, error: "完成 button not found in the cover editor" };
    if (done.disabled) return { ok: false, error: "完成 button is still disabled (cover not processed yet)" };
    if (typeof done.click !== "function") return { ok: false, error: "完成 button is not clickable" };
    done.click();
    return { ok: true };
  }

  if (op === "main-cover-state") {
    // Inline selector: creatorAct is serialized and must not touch module scope.
    const card = qs(".cover--column .default.column");
    if (!card) return { ok: false, error: "主封面 card not found", signature: "", label: "主封面", scope: "main" };
    const style = card.style || {};
    let bg = "";
    if (typeof style.getPropertyValue === "function") {
      try { bg = String(style.getPropertyValue("background-image") || ""); } catch { bg = ""; }
    }
    if (!bg) bg = String(style.backgroundImage || "");
    if (/^\s*none\s*$/i.test(bg)) bg = "";
    if (!bg && typeof getComputedStyle === "function") {
      try {
        const computed = String(getComputedStyle(card).getPropertyValue("background-image") || "");
        if (computed && !/^\s*none\s*$/i.test(computed)) bg = computed;
      } catch {
        // ignore computed-style failures in odd environments
      }
    }
    const images = typeof card.querySelectorAll === "function"
      ? [...card.querySelectorAll("img")]
      : [];
    const signature = [bg, ...images.map((el) => (el.getAttribute ? (el.getAttribute("src") || "") : ""))]
      .filter(Boolean).join("|");
    return { ok: true, signature, label: "主封面", scope: "main" };
  }

  if (op === "close-pk-cover") {
    const button = qs(".pk-cover-list-slide-close");
    if (!button) return { ok: false, error: "PK cover close control not found" };
    if (typeof button.click === "function") button.click();
    return { ok: true };
  }

  if (op === "reveal-cover") {
    const buttons = [...qsa("button"), ...qsa("[role='button']")];
    const target = buttons.find((el) => {
      const label = labelOf(el);
      return label.own === "换封面" || label.full === "换封面" || label.own === "设置封面" || label.full === "设置封面";
    });
    if (!target) return { ok: false, error: "换封面 control not found" };
    if (typeof target.click === "function") target.click();
    return { ok: true, via: "click" };
  }

  if (op === "cover-state") {
    const seen = new Set();
    const nodes = [];
    for (const node of [...qsa("[class*='cover']"), ...qsa("[class*='pk-cover']"), ...qsa("img")]) {
      if (!node || seen.has(node) || node.tagName === "INPUT") continue;
      seen.add(node);
      nodes.push(node);
    }
    const signature = nodes.map((node) => {
      const src = node.getAttribute ? (node.getAttribute("src") || "") : "";
      const bg = node.style && node.style.backgroundImage ? node.style.backgroundImage : "";
      const label = String(node.innerText || node.textContent || "").slice(0, 40);
      return `${src}|${bg}|${label}`;
    }).join("||");
    const previewMatch = text.match(/封面预览[^\n]{0,80}/);
    const counter = coverCountFrom(text);
    return {
      ok: true,
      pkApplied: /已添加\s*PK\s*封面/.test(text),
      autoFilled: /已自动填充推荐封面/.test(text),
      coverCount: counter.coverCount,
      counterText: counter.counterText,
      cropDialog: /裁剪封面|裁剪图片|完成裁剪|确认裁剪/.test(text),
      previewSignature: signature,
      previewText: previewMatch ? previewMatch[0] : "",
      text: text.slice(0, 500),
    };
  }

  if (op === "title-target") {
    const inputs = [...qsa("input"), ...qsa("textarea")].filter((el) => !isFileInput(el));
    const field = inputs.find((el) => /填写标题/.test(String(el.getAttribute("placeholder") || "")))
      || inputs.find((el) => /标题/.test(String(el.getAttribute("aria-label") || "")))
      || inputs[0];
    if (!field) return { ok: false, error: "title field not found" };
    return { ok: true, selector: mark(field, "data-xhs-title") };
  }

  if (op === "title-value") {
    const field = qs("[data-xhs-title='1']")
      || [...qsa("input"), ...qsa("textarea")].find((el) => /填写标题/.test(String(el.getAttribute("placeholder") || "")));
    if (!field) return { ok: false, error: "title field not found", value: "" };
    return { ok: true, value: String(field.value || "") };
  }

  if (op === "body-target") {
    const field = qs(".ProseMirror") || qsa("[contenteditable='true']")[0];
    if (!field) return { ok: false, error: "ProseMirror body not found" };
    return {
      ok: true,
      selector: mark(field, "data-xhs-body"),
      proseMirror: String(field.className || "").includes("ProseMirror"),
    };
  }

  if (op === "body-value") {
    const field = qs("[data-xhs-body='1']") || qs(".ProseMirror") || qsa("[contenteditable='true']")[0];
    if (!field) return { ok: false, error: "ProseMirror body not found", value: "" };
    return { ok: true, value: String(field.innerText || field.textContent || "") };
  }

  if (op === "click-publish") {
    const nodes = typeof doc.querySelectorAll === "function" ? [...doc.querySelectorAll("*")] : [];
    const matches = nodes.filter((el) => {
      const label = labelOf(el);
      return label.own === "发布" || label.full === "发布";
    });
    const target = matches.length ? matches[matches.length - 1] : null;
    if (!target) return { ok: false, error: "发布 button not found" };
    let x = null;
    let y = null;
    if (typeof target.getBoundingClientRect === "function") {
      const box = target.getBoundingClientRect();
      if (box && typeof box.width === "number" && box.width > 0 && typeof box.height === "number" && box.height > 0) {
        x = box.x + box.width / 2;
        y = box.y + box.height / 2;
      }
    }
    return { ok: true, x, y, tag: target.tagName, selector: mark(target, "data-xhs-publish") };
  }

  if (op === "note-cards") {
    return {
      ok: true,
      cards: qsa(".note-card").map((card) => ({
        text: String(card.innerText || card.textContent || "").slice(0, 500),
        impression: card.getAttribute("data-impression") || "",
      })),
    };
  }

  return { ok: false, error: `unknown op ${op}` };
}
