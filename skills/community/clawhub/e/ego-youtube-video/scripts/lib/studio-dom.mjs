// Browser-side Studio actions. page.evaluate serializes this function alone,
// so it must not close over imports. Tests call it with globalThis.document set.

export function studioAct(payload) {
  const doc = globalThis.document;
  const loc = globalThis.location || { href: "" };
  if (!doc) return { ok: false, error: "studioAct requires a document" };
  const request = payload && typeof payload === "object" ? payload : {};
  const op = request.op || "probe";

  function seenWalk() {
    const seen = new Set();
    function walk(node, matchSel) {
      if (!node || seen.has(node)) return null;
      seen.add(node);
      if (typeof node.querySelector === "function") {
        const direct = node.querySelector(matchSel);
        if (direct) return direct;
      }
      if (node.shadowRoot) {
        const inShadow = walk(node.shadowRoot, matchSel);
        if (inShadow) return inShadow;
      }
      const all = typeof node.querySelectorAll === "function" ? node.querySelectorAll("*") : [];
      for (const el of all) {
        if (el && el.shadowRoot) {
          const found = walk(el.shadowRoot, matchSel);
          if (found) return found;
        }
      }
      return null;
    }
    return walk;
  }

  function queryDeep(selector) {
    const parts = String(selector || "").split(/\s+/).filter(Boolean);
    if (!parts.length) return null;
    const walk = seenWalk();
    let node = doc;
    for (const part of parts) {
      node = walk(node, part);
      if (!node) return null;
    }
    return node;
  }

  function textOf(el) {
    if (!el) return "";
    return String(el.innerText || el.textContent || "").trim();
  }

  function visibleText(el) {
    return String((el && (el.innerText || el.textContent || el.value)) || "").replace(/\u00a0/g, " ").trim();
  }

  function writeEditable(el, value) {
    const expected = String(value ?? "");
    if (typeof el.focus === "function") el.focus();
    try {
      if (typeof doc.execCommand === "function") {
        doc.execCommand("selectAll", false, null);
        doc.execCommand("insertText", false, expected);
      }
    } catch {
      // Fall through to the textContent / value write.
    }
    let actual = visibleText(el);
    if (actual !== expected.trim()) {
      const tag = String(el.tagName || "").toUpperCase();
      if (tag === "INPUT" || tag === "TEXTAREA") el.value = expected;
      else {
        try { el.textContent = expected; } catch { /* ignore */ }
        try { el.innerText = expected; } catch { /* ignore */ }
      }
      if (typeof el.dispatchEvent === "function" && typeof globalThis.Event === "function") {
        try { el.dispatchEvent(new globalThis.Event("input", { bubbles: true })); } catch { /* ignore */ }
      }
      actual = visibleText(el);
    }
    return actual;
  }

  function enabled(el) {
    if (!el) return false;
    if (el.disabled) return false;
    if (typeof el.getAttribute === "function" && el.getAttribute("aria-disabled") === "true") return false;
    if (typeof el.hasAttribute === "function" && el.hasAttribute("disabled")) return false;
    return true;
  }

  function findUploadItem() {
    const byTest = queryDeep('tp-yt-paper-item[test-id="upload-beta"]')
      || queryDeep('tp-yt-paper-item[test-id="upload"]');
    if (byTest) return { el: byTest, via: "test-id" };
    const items = typeof doc.querySelectorAll === "function"
      ? doc.querySelectorAll("tp-yt-paper-item, [role='menuitem']")
      : [];
    for (const el of items) {
      const label = textOf(el);
      if (label === "Upload videos" || label === "上传视频") return { el, via: "text" };
    }
    return null;
  }

  function findShowMore() {
    const byId = queryDeep("#toggle-button");
    if (byId) return byId;
    const buttons = typeof doc.querySelectorAll === "function"
      ? doc.querySelectorAll("ytcp-button, button")
      : [];
    for (const el of buttons) {
      const label = textOf(el);
      if (label === "Show more" || label === "显示更多") return el;
    }
    return null;
  }

  function readChips(container) {
    if (!container || typeof container.querySelectorAll !== "function") return [];
    const chips = [];
    for (const chip of container.querySelectorAll("ytcp-chip")) {
      const label = textOf(chip);
      if (label) chips.push(label);
    }
    return chips;
  }

  function pressEnter(input) {
    if (!input || typeof input.dispatchEvent !== "function") return;
    const KeyEvt = globalThis.KeyboardEvent;
    let event = { type: "keydown", key: "Enter", keyCode: 13, bubbles: true };
    if (typeof KeyEvt === "function") {
      try {
        const real = new KeyEvt("keydown", { key: "Enter", bubbles: true, keyCode: 13 });
        if (real && real.key === "Enter") event = real;
      } catch {
        // Some embeds reject the constructor. The plain event still commits a chip in tests.
      }
    }
    try {
      input.dispatchEvent(event);
    } catch {
      // A chip listener may still have read the value.
    }
  }

  function findVideoAnchor() {
    const styled = queryDeep("a.ytcp-video-info");
    if (styled) return styled;
    const anchors = typeof doc.querySelectorAll === "function" ? doc.querySelectorAll("a") : [];
    for (const anchor of anchors) {
      const href = anchor.href || (typeof anchor.getAttribute === "function" ? anchor.getAttribute("href") : "") || "";
      if (/youtu\.be\/|[?&]v=|\/video\//.test(String(href))) return anchor;
    }
    return null;
  }

  if (op === "probe") {
    const text = String((doc.body && (doc.body.innerText || doc.body.textContent)) || "").slice(0, 4000);
    return {
      ok: true,
      op,
      text,
      url: String(loc.href || ""),
      title: String(doc.title || ""),
      cookie: String(doc.cookie || ""),
    };
  }

  if (op === "upload-entry") {
    const upload = findUploadItem();
    return {
      ok: true,
      hasSelectFiles: Boolean(queryDeep("#select-files-button")),
      hasCreate: Boolean(queryDeep("#create-icon")),
      hasUploadItem: Boolean(upload),
    };
  }

  if (op === "click-upload-menu") {
    const found = findUploadItem();
    if (!found) return { ok: false, error: "未找到「上传视频」菜单" };
    if (typeof found.el.click === "function") found.el.click();
    return { ok: true, via: found.via };
  }

  if (op === "fill") {
    const titleEl = queryDeep("#title-textarea #textbox") || queryDeep("#title-textarea");
    if (!titleEl) return { ok: false, error: "未找到标题输入框" };
    const title = writeEditable(titleEl, request.title);
    const description = String(request.description || "");
    if (!description.trim()) return { ok: true, title, description: "" };
    const descEl = queryDeep("#description-textarea #textbox") || queryDeep("#description-textarea");
    if (!descEl) return { ok: false, error: "未找到简介输入框", title };
    return { ok: true, title, description: writeEditable(descEl, description) };
  }

  if (op === "tags") {
    const tags = Array.isArray(request.tags) ? request.tags.map((tag) => String(tag).trim()).filter(Boolean) : [];
    if (!tags.length) return { ok: true, tags: [] };
    let input = queryDeep("#tags-container #text-input") || queryDeep("#tags-container input");
    if (!input) {
      const toggle = findShowMore();
      if (toggle && typeof toggle.click === "function") toggle.click();
      input = queryDeep("#tags-container #text-input") || queryDeep("#tags-container input");
    }
    if (!input) return { ok: false, error: "未找到标签输入框" };
    for (const tag of tags) {
      writeEditable(input, tag);
      pressEnter(input);
    }
    const container = queryDeep("#tags-container") || input;
    const chips = readChips(container);
    const blob = `${textOf(container)}\n${input.value || ""}\n${visibleText(input)}`;
    const missing = tags.filter((tag) => !chips.includes(tag) && !blob.includes(tag));
    if (missing.length) return { ok: false, error: `标签未写入: ${missing.join(", ")}`, tags: chips };
    return { ok: true, tags: chips.length ? chips : tags };
  }

  if (op === "audience") {
    const name = request.madeForKids ? "VIDEO_MADE_FOR_KIDS_MFK" : "VIDEO_MADE_FOR_KIDS_NOT_MFK";
    const radio = queryDeep(`tp-yt-paper-radio-button[name="${name}"]`);
    if (!radio) return { ok: false, error: "未找到「是否面向儿童」选项", name };
    if (typeof radio.click === "function") radio.click();
    const checked = (typeof radio.getAttribute === "function" && radio.getAttribute("aria-checked") === "true")
      || radio.checked === true
      || (typeof radio.hasAttribute === "function" && radio.hasAttribute("checked"));
    return { ok: true, checked, madeForKids: Boolean(request.madeForKids), name };
  }

  if (op === "visibility") {
    const names = { private: "PRIVATE", unlisted: "UNLISTED", public: "PUBLIC" };
    const name = names[String(request.visibility || "private").toLowerCase()] || "PRIVATE";
    const radio = queryDeep(`tp-yt-paper-radio-button[name="${name}"]`);
    if (!radio) return { ok: false, error: "未找到公开范围选项", name };
    if (typeof radio.click === "function") radio.click();
    const checked = (typeof radio.getAttribute === "function" && radio.getAttribute("aria-checked") === "true")
      || radio.checked === true;
    return { ok: true, checked, visibility: String(request.visibility || "private").toLowerCase(), name };
  }

  if (op === "wizard") {
    const next = queryDeep("#next-button");
    const done = queryDeep("#done-button");
    return {
      ok: true,
      hasNext: Boolean(next),
      nextEnabled: enabled(next),
      hasDone: Boolean(done),
      doneEnabled: enabled(done),
      hasVisibility: Boolean(queryDeep('tp-yt-paper-radio-button[name="PRIVATE"]')),
      hasKids: Boolean(queryDeep('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')),
    };
  }

  if (op === "click") {
    const el = queryDeep(request.selector);
    if (!el) return { ok: false, error: `未找到 ${request.selector || ""}`.trim() };
    if (!enabled(el)) return { ok: false, disabled: true, error: `${request.selector} 不可点击` };
    if (typeof el.click === "function") el.click();
    return { ok: true, selector: request.selector };
  }

  if (op === "click-thumbnail") {
    const input = queryDeep("#file-loader");
    if (input && typeof input.click === "function") {
      input.click();
      return { ok: true, via: "#file-loader" };
    }
    const buttons = typeof doc.querySelectorAll === "function"
      ? doc.querySelectorAll("ytcp-button, button")
      : [];
    for (const el of buttons) {
      const label = textOf(el);
      if (label === "Upload thumbnail" || label === "上传缩略图" || label === "自定义缩略图") {
        if (typeof el.click === "function") el.click();
        return { ok: true, via: label };
      }
    }
    return { ok: false, error: "未找到缩略图上传按钮" };
  }

  if (op === "surface") {
    const text = String((doc.body && (doc.body.innerText || doc.body.textContent)) || "").slice(0, 8000);
    const link = findVideoAnchor();
    const href = link
      ? String(link.href || (typeof link.getAttribute === "function" ? link.getAttribute("href") : "") || "")
      : "";
    const errorEl = queryDeep("#error-message");
    return {
      ok: true,
      text,
      url: String(loc.href || ""),
      title: String(doc.title || ""),
      href,
      error: textOf(errorEl),
    };
  }

  return { ok: false, error: `unknown studio op: ${op}` };
}
