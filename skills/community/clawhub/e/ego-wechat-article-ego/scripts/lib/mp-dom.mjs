// Browser-side mp.weixin.qq.com actions.
// page.evaluate serializes mpAct alone. Every helper lives inside the function.
// Do not call module-level functions from it.

export function mpAct(payload) {
  const doc = globalThis.document;
  if (!doc || typeof doc.querySelectorAll !== "function") {
    return { ok: false, error: "mpAct requires a document" };
  }
  const input = payload && typeof payload === "object" ? payload : {};
  const op = input.op || "probe";

  function qsa(root, selector) {
    const scope = root || doc;
    if (!scope || typeof scope.querySelectorAll !== "function") return [];
    try {
      return [...scope.querySelectorAll(selector)];
    } catch {
      return [];
    }
  }

  function qsaAny(selectors, root) {
    const out = [];
    for (const selector of selectors) out.push(...qsa(root, selector));
    return out;
  }

  function normalize(value) {
    return String(value ?? "").replace(/\s+/g, " ").trim();
  }

  function visible(el) {
    if (!el || el.nodeType !== 1) return false;
    const hidden = el.getAttribute && (el.getAttribute("hidden") != null || el.getAttribute("aria-hidden") === "true");
    if (hidden) return false;
    if (typeof el.getClientRects === "function") return el.getClientRects().length > 0;
    return true;
  }

  function shown(el) {
    if (!visible(el)) return false;
    if (typeof el.getBoundingClientRect !== "function") return true;
    const rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  }

  function hint(el) {
    return `${(el.getAttribute && (el.getAttribute("placeholder") || el.getAttribute("data-placeholder") || el.getAttribute("aria-label"))) || el.placeholder || ""}`;
  }

  function ownLabel(el) {
    const direct = [...(el.childNodes || [])]
      .filter((node) => node && node.nodeType === 3)
      .map((node) => node.textContent || "")
      .join("")
      .trim();
    if (direct) return normalize(direct);
    return normalize(el.innerText || el.textContent || "");
  }

  function isForbidden(text) {
    const label = normalize(text);
    if (!label) return false;
    if (/发送预览|定时群发|定时发表/.test(label)) return true;
    return /群发|发表/.test(label);
  }

  function findExact(text) {
    const want = normalize(text);
    if (!want || isForbidden(want)) return null;
    const tags = { BUTTON: 0, A: 1, SPAN: 2, LI: 3, LABEL: 4, DIV: 5 };
    const found = qsaAny(["button", "a", "span", "li", "label", "div"]).filter((el) => (
      visible(el) && ownLabel(el) === want && !isForbidden(ownLabel(el))
    ));
    found.sort((left, right) => (tags[left.tagName] ?? 9) - (tags[right.tagName] ?? 9));
    return found[0] || null;
  }

  function bodyText() {
    return normalize((doc.body && (doc.body.innerText || doc.body.textContent)) || "");
  }

  function isAccountName(name) {
    const text = normalize(name);
    if (text.length < 2 || text.length > 32) return false;
    if (/扫一扫|请重新登录|登录超时|立即注册|微信公众平台/.test(text)) return false;
    if (/^(公众号|服务号|小程序|登录|首页|草稿箱|文章)$/.test(text)) return false;
    return true;
  }

  function namesFrom(selectors) {
    const values = [];
    for (const el of qsaAny(selectors)) {
      const fromAttr = el.getAttribute && (el.getAttribute("data-account-name") || el.getAttribute("data-nickname"));
      const text = normalize(fromAttr || el.innerText || el.textContent || "");
      if (isAccountName(text)) values.push(text);
    }
    return [...new Set(values)];
  }

  function collectAccounts() {
    const switched = namesFrom([
      "[class*='account-switch']",
      "[class*='switch-item']",
      "[data-account-name]",
    ]);
    if (switched.length) return { accounts: switched, ambiguous: switched.length > 1 };
    const nicknames = namesFrom([
      "[class*='weui-desktop-account__nickname']",
      "[class*='account-nickname']",
      "[class*='nickname']",
    ]);
    return { accounts: nicknames, ambiguous: nicknames.length > 1 };
  }

  function editorRoot() {
    const rich = qsa(doc, ".rich_media_content .ProseMirror").find(shown);
    if (rich) return { doc, body: rich };
    const mirrors = qsa(doc, ".ProseMirror").filter((el) => shown(el) && !/标题/.test(hint(el)));
    if (mirrors.length) return { doc, body: mirrors[0] };
    for (const frame of qsa(doc, "iframe")) {
      const idoc = frame.contentDocument;
      const body = idoc && idoc.body;
      if (!body) continue;
      const editable = body.isContentEditable || (body.getAttribute && body.getAttribute("contenteditable") === "true");
      const marked = qsa(idoc, ".editor-body").length || qsa(idoc, ".ProseMirror").length;
      if (editable || marked) return { doc: idoc, body };
    }
    const marked = qsa(doc, ".editor-body")[0];
    if (marked) return { doc, body: marked };
    return null;
  }

  function titleField() {
    const mirrors = qsa(doc, ".ProseMirror").filter((el) => shown(el) && /标题/.test(hint(el)));
    if (mirrors[0]) return mirrors[0];
    const fields = qsaAny(["textarea", "input", "[contenteditable='true']"]).filter((el) => /标题/.test(hint(el)));
    return fields.find(shown) || fields[0] || null;
  }

  function selectInside(el, { collapse } = {}) {
    if (!el) return false;
    if (typeof el.focus === "function") el.focus();
    const owner = el.ownerDocument || doc;
    const view = owner.defaultView || globalThis;
    if (!view.getSelection || !owner.createRange) return false;
    const selection = view.getSelection();
    if (!selection) return false;
    const range = owner.createRange();
    range.selectNodeContents(el);
    if (collapse) range.collapse(false);
    selection.removeAllRanges();
    selection.addRange(range);
    return true;
  }

  function placeCaret(el) {
    const blocks = el ? qsa(el, "p,h2,h3,li,blockquote,pre") : [];
    const last = blocks[blocks.length - 1];
    if (last) return selectInside(last, { collapse: true });
    return selectInside(el, { collapse: true });
  }

  function fieldByHint(pattern) {
    return qsaAny(["textarea", "input"]).find((el) => pattern.test(
      `${(el.getAttribute && el.getAttribute("placeholder")) || ""} ${(el.getAttribute && el.getAttribute("aria-label")) || ""}`,
    )) || null;
  }

  function safeUrl() {
    try {
      const url = new URL(globalThis.location.href);
      for (const key of [...url.searchParams.keys()]) {
        if (/token|ticket|pass|cookie|session|key/i.test(key)) url.searchParams.set(key, "redacted");
      }
      return url.toString();
    } catch {
      return "";
    }
  }

  function imageCount() {
    const root = editorRoot();
    if (!root) return 0;
    return qsa(root.body, "img").filter((img) => {
      const src = (img.getAttribute && img.getAttribute("src")) || "";
      return src && src !== "about:blank";
    }).length;
  }

  function clickFound(el, via) {
    if (!el || typeof el.click !== "function") return { ok: false, error: "control not found" };
    const label = ownLabel(el);
    if (isForbidden(label)) return { ok: false, error: `refusing to click ${label}`, forbidden: true };
    el.click();
    return { ok: true, via, label };
  }

  function setValue(el, value) {
    if (!el) return { ok: false, error: "field not found" };
    try {
      const proto = el.tagName === "TEXTAREA" ? globalThis.HTMLTextAreaElement : globalThis.HTMLInputElement;
      const desc = proto && Object.getOwnPropertyDescriptor(proto.prototype, "value");
      if (desc && desc.set) desc.set.call(el, value);
      else el.value = value;
    } catch {
      el.value = value;
    }
    if (el.isContentEditable) el.textContent = value;
    if (typeof el.dispatchEvent === "function" && typeof globalThis.Event === "function") {
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
    }
    return { ok: true };
  }

  if (op === "probe") {
    const account = collectAccounts();
    const text = bodyText();
    const loginWall = account.accounts.length === 0 && /扫一扫|请重新登录|登录超时|使用账号登录/.test(text);
    const loggedIn = !loginWall && (account.accounts.length > 0 || /新的创作|草稿箱|内容管理/.test(text));
    const root = editorRoot();
    return {
      ok: true,
      url: safeUrl(),
      title: doc.title || "",
      text: text.slice(0, 2000),
      loginWall,
      loggedIn,
      accounts: account.accounts,
      ambiguous: account.ambiguous,
      editorReady: Boolean(titleField() || root),
      imageCount: imageCount(),
    };
  }

  if (op === "click") {
    if (isForbidden(input.text)) return { ok: false, error: `refusing to click ${input.text}`, forbidden: true };
    const found = findExact(input.text);
    if (!found) return { ok: !input.required, error: input.required ? `${input.text} not found` : "", missing: !found };
    return clickFound(found, "text");
  }

  if (op === "title-field" || op === "focus-title") {
    const field = titleField();
    if (!field) return { ok: false, error: "title field not found" };
    if (typeof field.focus === "function") field.focus();
    field.setAttribute("data-wx-article-title", "1");
    const kind = String(field.className || "").includes("ProseMirror") || field.isContentEditable ? "prosemirror" : "input";
    return { ok: true, kind, selector: "[data-wx-article-title='1']" };
  }

  if (op === "set-title" || op === "set-digest" || op === "set-source") {
    const field = op === "set-title" ? titleField()
      : op === "set-digest" ? fieldByHint(/摘要/)
        : fieldByHint(/原文/);
    return setValue(field, input.value || "");
  }

  if (op === "select-title") {
    const field = titleField();
    if (!field) return { ok: false, error: "title field not found" };
    selectInside(field);
    return { ok: true };
  }

  if (op === "select-slot") {
    const root = editorRoot();
    if (!root) return { ok: false, error: "editor body not found" };
    const slot = String(input.slot || "");
    const target = qsa(root.body, "p").find((el) => String(el.innerText || el.textContent || "").includes(slot));
    if (!target) return { ok: false, error: `slot ${slot} not found` };
    selectInside(target);
    return { ok: true };
  }

  if (op === "focus-body") {
    const root = editorRoot();
    if (!root) return { ok: false, error: "editor body not found" };
    placeCaret(root.body);
    return { ok: true };
  }

  if (op === "open-image") {
    const titled = qsa(doc, "[title='图片']")[0] || qsa(doc, "[class*='insertimage']")[0];
    if (titled && visible(titled)) return clickFound(titled, "toolbar");
    return clickFound(findExact("图片"), "text");
  }

  if (op === "image-input") {
    const inputs = qsa(doc, "input").filter((el) => (el.getAttribute("type") || "") === "file" || el.type === "file");
    const images = inputs.filter((el) => /image|jpg|jpeg|png|webp|gif/i.test(el.getAttribute("accept") || "image"));
    const pool = images.length ? images : inputs;
    const field = pool[pool.length - 1];
    if (!field) return { ok: false, error: "image file input not found" };
    field.setAttribute("data-wx-article-file", "1");
    return { ok: true, selector: "input[data-wx-article-file='1']" };
  }

  if (op === "confirm-image") {
    const text = bodyText();
    if (!/选择图片|上传图片|插入图片|图片编辑/.test(text)) return { ok: true, confirmed: false };
    const button = findExact("确定") || findExact("确认") || findExact("插入");
    if (!button) return { ok: true, confirmed: false };
    button.click();
    return { ok: true, confirmed: true };
  }

  if (op === "image-count") return { ok: true, imageCount: imageCount() };

  if (op === "cover-state") {
    const text = bodyText();
    const present = /封面/.test(text) || Boolean(doc.querySelector && doc.querySelector("#js_cover_area"));
    const preview = (doc.querySelector && (doc.querySelector("#js_cover_area .js_cover_preview_new") || doc.querySelector(".js_cover_preview_new"))) || null;
    const style = preview ? ((preview.getAttribute && preview.getAttribute("style")) || "") : "";
    const matched = style.match(/background-image:\s*url\((['"]?)(https?:[^'")]+)\1\)/i);
    const hidden = (doc.querySelector && (doc.querySelector("#js_cover_area .js_cdn_url") || doc.querySelector("input.js_cdn_url"))) || null;
    const fromInput = hidden && /^https?:/.test(hidden.value || "") ? hidden.value : "";
    const legacy = qsa(doc, ".cover-preview img").find((img) => /^https?:/.test((img.getAttribute && img.getAttribute("src")) || ""));
    const src = (matched && matched[2]) || fromInput || (legacy ? legacy.getAttribute("src") : "") || "";
    const filled = Boolean(src) || /已选择封面|封面已设置/.test(text);
    const required = /必须选择封面|封面不能为空|请上传封面/.test(text);
    const empty = (required && !filled) || (present && !filled && Boolean(doc.querySelector && doc.querySelector("#js_cover_area")));
    const file = qsa(doc, "input").find((el) => (
      (el.getAttribute("type") || "") === "file"
      && /cover|封面/.test(`${el.getAttribute("accept") || ""} ${el.getAttribute("class") || ""} ${el.className || ""}`)
    ));
    if (file) file.setAttribute("data-wx-article-cover", "1");
    return {
      ok: true,
      present,
      filled,
      empty,
      required,
      src,
      selector: file ? "input[data-wx-article-cover='1']" : "",
    };
  }

  if (op === "open-cover-menu") {
    const tips = qsa(doc, ".js_share_type_none_image").filter((el) => shown(el));
    const area = (tips[0] && tips[0].parentElement) || (doc.querySelector && doc.querySelector("#js_cover_area .select-cover__btn"));
    if (!area) return { ok: false, error: "cover control not found" };
    if (typeof area.scrollIntoView === "function") area.scrollIntoView({ block: "center" });
    area.click();
    return { ok: true };
  }

  if (op === "cover-menu-state") {
    const pop = doc.querySelector && doc.querySelector("#js_cover_null");
    const style = pop ? ((pop.getAttribute && pop.getAttribute("style")) || "") : "";
    let open = Boolean(pop) && !/display:\s*none/.test(style);
    if (pop && typeof pop.getBoundingClientRect === "function") {
      const rect = pop.getBoundingClientRect();
      open = rect.width > 20 && rect.height > 20;
    }
    const dialog = doc.querySelector && doc.querySelector(".weui-desktop-dialog_img-picker");
    const items = dialog && dialog.querySelectorAll ? dialog.querySelectorAll(".appmsg_content_img_item").length : 0;
    return { ok: true, open, items };
  }

  if (op === "cover-debug") {
    const pop = doc.querySelector && doc.querySelector("#js_cover_null");
    const rect = pop && typeof pop.getBoundingClientRect === "function" ? pop.getBoundingClientRect() : null;
    const dialog = doc.querySelector && doc.querySelector(".weui-desktop-dialog_img-picker");
    const items = dialog && dialog.querySelectorAll ? dialog.querySelectorAll(".appmsg_content_img_item").length : 0;
    const text = bodyText().replace(/\s+/g, " ");
    const at = text.indexOf("选择图片");
    return {
      ok: true,
      detail: `pop=${rect ? `${Math.round(rect.width)}x${Math.round(rect.height)}` : "none"} items=${items} dialog=${dialog ? "yes" : "no"} ${at >= 0 ? text.slice(at, at + 80) : "no-picker"}`,
    };
  }

  if (op === "cover-from-body") {
    const scoped = doc.querySelector && doc.querySelector("#js_cover_null .js_selectCoverFromContent");
    const button = scoped || findExact("从正文选择");
    if (!button) return { ok: false, error: "从正文选择 not found" };
    try {
      if (globalThis.jQuery) globalThis.jQuery(button).trigger("click");
    } catch {
      // The native click below still reaches the editor handler.
    }
    button.click();
    return { ok: true };
  }

  if (op === "cover-pick-first") {
    const dialog = doc.querySelector && doc.querySelector(".weui-desktop-dialog_img-picker");
    const item = dialog && dialog.querySelector && dialog.querySelector(".appmsg_content_img_item");
    if (!item) return { ok: false, error: "body image was not offered for the cover" };
    const face = (item.querySelector && item.querySelector(".appmsg_content_img")) || item;
    face.click();
    return { ok: true };
  }

  if (op === "cover-advance") {
    const dialog = (doc.querySelector && (doc.querySelector(".weui-desktop-dialog_img-picker") || doc.querySelector(".weui-desktop-dialog"))) || null;
    if (!dialog) return { ok: false, done: true };
    const buttons = [...qsa(dialog, "button"), ...qsa(dialog, "a")];
    for (const label of ["下一步", "确认", "完成", "确定"]) {
      const found = buttons.find((el) => normalize(el.innerText || el.textContent || "") === label && visible(el));
      if (found) {
        found.click();
        return { ok: true, label };
      }
    }
    return { ok: false, done: true };
  }

  if (op === "open-draft-editor") {
    const want = normalize(input.title || "");
    const title = qsa(doc, ".weui-desktop-publish__cover__title").find((el) => {
      const text = normalize(el.innerText || el.textContent || "");
      const flat = (value) => String(value || "").replace(/\u00a0/g, " ").replace(/\s+/g, "");
      return text && (text === want || flat(text) === flat(want) || text.includes(want) || want.includes(text));
    });
    if (!title) return { ok: false, error: "draft row not found" };
    let card = title;
    for (let depth = 0; depth < 8 && card; depth += 1) {
      const editWrap = qsa(card, ".weui-desktop-tooltip__wrp").find((el) => String(el.innerText || el.textContent || "").includes("编辑"));
      if (editWrap) {
        const anchor = editWrap.querySelector && editWrap.querySelector("a");
        (anchor || editWrap).click();
        return { ok: true };
      }
      card = card.parentElement;
    }
    return { ok: false, error: "edit control not found" };
  }

  if (op === "cover-thumb") {
    const want = normalize(input.title || "");
    const titles = qsa(doc, ".weui-desktop-publish__cover__title");
    const title = titles.find((el) => {
      const text = normalize(el.innerText || el.textContent || "");
      return text && (text === want || text.includes(want) || want.includes(text));
    });
    let node = title;
    let thumb = null;
    for (let depth = 0; depth < 8 && node && !thumb; depth += 1) {
      thumb = node.querySelector && node.querySelector(".weui-desktop-publish__cover__thumb");
      node = node.parentElement;
    }
    const style = thumb ? ((thumb.getAttribute && thumb.getAttribute("style")) || "") : "";
    const matched = style.match(/background-image:\s*url\((['"]?)([^'")]+)\1\)/i);
    const src = matched ? matched[2].replace(/&quot;/g, "") : "";
    const filled = /^https?:/.test(src);
    return { ok: filled, filled, src };
  }

  if (op === "click-save") {
    for (const label of ["保存为草稿", "保存草稿", "保存"]) {
      const found = findExact(label);
      if (found) return clickFound(found, "save");
    }
    return { ok: false, error: "保存 control not found" };
  }

  if (op === "click-preview") {
    if (isForbidden("预览")) return { ok: false, error: "refusing to click 预览", forbidden: true };
    const found = findExact("预览");
    if (!found) return { ok: false, error: "预览 control not found" };
    return clickFound(found, "preview");
  }

  if (op === "preview-state") {
    const pane = qsaAny([".preview-phone", ".rich_media_preview", ".mobile-preview"]).some(visible);
    return { ok: true, pane, button: Boolean(findExact("预览")) };
  }

  if (op === "read-editor") {
    const root = editorRoot();
    const field = titleField();
    const title = field ? (field.value || field.innerText || field.textContent || "") : "";
    const hrefs = root ? qsa(root.body, "a").map((el) => el.getAttribute && el.getAttribute("href")).filter(Boolean) : [];
    return {
      ok: true,
      title: normalize(title),
      text: root ? (root.body.innerText || root.body.textContent || "") : "",
      imageCount: imageCount(),
      hrefs,
    };
  }

  if (op === "draft-rows") {
    const nodes = qsaAny([
      ".weui-desktop-publish__cover__title",
      ".draft-title",
      ".weui-desktop-card__title",
      ".card_appmsg_title",
      ".appmsg_title",
    ]);
    const rows = [];
    for (const el of nodes) {
      const title = normalize(el.getAttribute && el.getAttribute("data-draft-title") || el.innerText || el.textContent || "");
      if (!title || isForbidden(title)) continue;
      let timeNode = el;
      let timeLine = "";
      for (let depth = 0; depth < 6 && timeNode && !timeLine; depth += 1) {
        const blob = String(timeNode.innerText || timeNode.textContent || "");
        const matched = blob.match(/更新于\s*\d{1,2}:\d{2}/) || blob.match(/\d+月\d+日(?:\s*\d{1,2}:\d{2})?/);
        if (matched) timeLine = matched[0];
        const line = blob.split(/\n/).map((item) => item.trim()).find((item) => (
          item && item !== title && /月|今天|昨天|\d{2}:\d{2}|\d{4}-\d{2}/.test(item)
        ));
        if (!timeLine && line) timeLine = line;
        timeNode = timeNode.parentElement;
      }
      const rawId = (el.getAttribute && (el.getAttribute("data-id") || el.getAttribute("data-appmsgid"))) || "";
      rows.push({
        title,
        time: (el.getAttribute && el.getAttribute("data-time")) || timeLine,
        id: /^[0-9]+$/.test(rawId) ? rawId : "",
      });
      if (rows.length >= 30) break;
    }
    return { ok: true, rows };
  }

  if (op === "strip-title") {
    const root = editorRoot();
    if (!root) return { ok: false, error: "editor body not found" };
    const key = normalize(input.title || "").replace(/（[^）]{1,16}）$/u, "").trim();
    if (!key) return { ok: true, removed: 0 };
    const same = (value) => {
      const text = normalize(value).replace(/（[^）]{1,16}）$/u, "").trim();
      return text === key;
    };
    let removed = 0;
    const nodes = ["figcaption", "p", "h1", "h2", "h3", "section"].flatMap((tag) => qsa(root.body, tag));
    for (const cap of nodes) {
      const text = normalize(cap.innerText || cap.textContent || "");
      const hasImage = cap.querySelector && cap.querySelector("img");
      if (!hasImage && same(text) && text.length < key.length + 24 && cap.parentElement && typeof cap.parentElement.removeChild === "function") {
        cap.parentElement.removeChild(cap);
        removed += 1;
      }
    }
    return { ok: true, removed };
  }

  if (op === "apply-reference-fixes") {
    const root = editorRoot();
    if (!root) return { ok: false, error: "editor body not found" };
    const body = root.body;
    const imgs = qsa(body, "img").filter((img) => {
      const src = (img.getAttribute && img.getAttribute("src")) || "";
      return src && src !== "about:blank";
    });
    const gaps = [];
    for (const img of imgs) {
      img.style.display = "block";
      img.style.margin = "0 auto";
      img.style.maxWidth = "100%";
      let cursor = img;
      let caption = null;
      for (let depth = 0; depth < 6 && cursor && !caption; depth += 1) {
        let sibling = cursor.nextElementSibling;
        while (sibling && !caption) {
          const tag = String(sibling.tagName || "").toUpperCase();
          const style = (sibling.getAttribute && sibling.getAttribute("style")) || "";
          if (tag === "FIGCAPTION" || style.includes("margin-top:5px")) caption = sibling;
          sibling = sibling.nextElementSibling;
        }
        cursor = cursor.parentElement;
      }
      if (!caption) continue;
      caption.style.margin = "0";
      caption.style.marginTop = "5px";
      caption.style.padding = "0";
      caption.style.textAlign = "center";
      caption.style.color = "#888";
      caption.style.fontSize = "14px";
      caption.style.lineHeight = "1.6";
      const blank = (el) => {
        if (!el || el === caption) return false;
        const tag = String(el.tagName || "").toUpperCase();
        if (tag === "IMG" || tag === "FIGCAPTION") return false;
        if (el.querySelector && el.querySelector("img")) return false;
        return !normalize(el.innerText || el.textContent || "");
      };
      let host = img;
      while (host && host !== caption && host.parentElement) {
        let sibling = host.nextElementSibling;
        while (sibling && sibling !== caption) {
          const next = sibling.nextElementSibling;
          if (blank(sibling) && sibling.parentElement && typeof sibling.parentElement.removeChild === "function") {
            sibling.parentElement.removeChild(sibling);
          }
          sibling = next;
        }
        host = host.parentElement;
      }
      let wrap = img.parentElement;
      while (wrap && wrap !== body) {
        if (!wrap.style) wrap.style = {};
        wrap.style.marginBottom = "0";
        wrap.style.paddingBottom = "0";
        if (typeof wrap.contains === "function" && wrap.contains(caption)) break;
        wrap = wrap.parentElement;
      }
      let gap = null;
      if (typeof img.getBoundingClientRect === "function" && typeof caption.getBoundingClientRect === "function") {
        gap = Math.round(caption.getBoundingClientRect().top - img.getBoundingClientRect().bottom);
      }
      gaps.push({
        gap,
        paddingTop: caption.style.paddingTop || "0",
        marginTop: caption.style.marginTop,
      });
    }
    const paintQuote = (el) => {
      if (!el.style) el.style = {};
      el.style.display = "block";
      el.style.borderLeft = "3px solid rgb(239,112,96)";
      el.style.borderRight = "0";
      el.style.background = "#fff9f9";
      el.style.color = "#6a737d";
      el.style.padding = "10px 10px 10px 20px";
      el.style.margin = "20px 0";
      el.style.fontSize = "0.9em";
      el.style.overflow = "auto";
      el.style.position = "static";
    };
    for (const quote of [...qsa(body, "blockquote")]) {
      const section = doc.createElement ? doc.createElement("section") : null;
      if (!section || !quote.parentElement || typeof quote.parentElement.replaceChild !== "function") {
        paintQuote(quote);
        continue;
      }
      if (!section.style) section.style = {};
      const kids = [...(quote.childNodes || [])];
      for (const kid of kids) {
        if (typeof section.appendChild === "function") section.appendChild(kid);
      }
      quote.parentElement.replaceChild(section, quote);
      paintQuote(section);
    }
    for (const section of qsa(body, "section")) {
      const style = (section.getAttribute && section.getAttribute("style")) || "";
      if (/fff9f9|239,\s*112,\s*96/.test(style) || (section.style && String(section.style.background || "").includes("fff9f9"))) {
        paintQuote(section);
      }
    }
    const quoteNodes = qsa(body, "blockquote,section").filter((el) => {
      const tag = String(el.tagName || "").toUpperCase();
      const style = `${(el.getAttribute && el.getAttribute("style")) || ""} ${el.style && el.style.background || ""} ${el.style && el.style.borderLeft || ""}`;
      return tag === "BLOCKQUOTE" || /fff9f9|239,\s*112,\s*96/.test(style);
    });
    let doubleRail = quoteNodes.some((el) => String(el.tagName || "").toUpperCase() === "BLOCKQUOTE");
    if (typeof getComputedStyle === "function") {
      for (const el of quoteNodes) {
        const before = getComputedStyle(el, "::before");
        const width = parseFloat(before && before.width) || 0;
        const bg = (before && before.backgroundColor) || "";
        if (width >= 2 && bg && bg !== "transparent" && bg !== "rgba(0, 0, 0, 0)") doubleRail = true;
      }
    }
    let badges = 0;
    for (const heading of qsa(body, "h2")) {
      heading.style.marginTop = "30px";
      heading.style.marginBottom = "15px";
      heading.style.padding = "0";
      heading.style.fontWeight = "bold";
      heading.style.color = "black";
      heading.style.borderBottom = "2px solid rgb(239,112,96)";
      heading.style.fontSize = "1.3em";
      const spans = qsa(heading, "span");
      const hasBadge = spans.some((span) => String((span.getAttribute && span.getAttribute("style")) || "").includes("239,112,96"));
      if (!hasBadge) {
        const label = normalize(heading.innerText || heading.textContent || "");
        heading.textContent = "";
        const badge = doc.createElement("span");
        badge.setAttribute("style", "display:inline-block;font-weight:bold;background:rgb(239,112,96);color:#fff;padding:3px 10px 1px;border-top-right-radius:3px;border-top-left-radius:3px;margin-right:3px;");
        badge.textContent = label;
        const tail = doc.createElement("span");
        tail.setAttribute("style", "display:inline-block;vertical-align:bottom;border-bottom:36px solid #efebe9;border-right:20px solid transparent;");
        tail.textContent = "\u00a0";
        heading.appendChild(badge);
        heading.appendChild(tail);
      }
      badges += 1;
    }
    return { ok: true, gaps, quotes: qsa(body, "section,blockquote").length, headings: badges, doubleRail };
  }

  if (op === "open-draft-list") {
    const names = qsa(doc, ".weui-desktop-menu__name");
    const menu = (label) => {
      const found = names.filter((el) => normalize(el.innerText || el.textContent) === label);
      const name = found.find(shown) || found[0];
      if (!name) return findExact(label);
      const link = typeof name.closest === "function" ? name.closest("a") : null;
      return link || name;
    };
    let draft = menu("草稿箱");
    if (draft && shown(draft)) return clickFound(draft, "drafts");
    const section = menu("内容管理");
    if (section && typeof section.click === "function") section.click();
    draft = menu("草稿箱");
    if (!draft) return { ok: false, error: "草稿箱 not found" };
    return clickFound(draft, "drafts");
  }

  if (op === "scroll") {
    const root = editorRoot();
    const node = (root && root.body) || doc.body;
    if (!node) return { ok: false, error: "nothing to scroll" };
    const height = node.scrollHeight || 2400;
    const top = input.where === "end" ? height : input.where === "middle" ? Math.floor(height / 2) : 0;
    if (typeof node.scrollTo === "function") node.scrollTo(0, top);
    node.scrollTop = top;
    return { ok: true, top };
  }

  if (op === "clear-unload") {
    globalThis.onbeforeunload = null;
    return { ok: true };
  }

  return { ok: false, error: `unknown op ${op}` };
}
