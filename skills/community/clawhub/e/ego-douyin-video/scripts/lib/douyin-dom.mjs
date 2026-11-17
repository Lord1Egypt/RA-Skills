// Browser-side Douyin creator actions. page.evaluate serializes this function
// alone, so it must not close over imports. Tests call it with globalThis.document set.

export function douyinAct(payload) {
  const doc = globalThis.document;
  const loc = globalThis.location || { href: "" };
  if (!doc) return { ok: false, error: "douyinAct requires a document" };
  const request = payload && typeof payload === "object" ? payload : {};
  const op = request.op || "probe";

  function bodyText() {
    const body = doc.body;
    if (!body) return "";
    return String(body.innerText || body.textContent || "");
  }

  function pointFrom(el) {
    if (!el || typeof el.getBoundingClientRect !== "function") return null;
    const box = el.getBoundingClientRect();
    const x = box.x;
    const y = box.y;
    const width = box.width;
    const height = box.height;
    if (![x, y, width, height].every((n) => typeof n === "number" && Number.isFinite(n))) return null;
    if (width <= 0 || height <= 0) return null;
    return { x: x + width / 2, y: y + height / 2, width, height };
  }

  function ownText(el) {
    const nodes = el && el.childNodes ? [...el.childNodes] : [];
    return nodes
      .filter((node) => node && node.nodeType === 3)
      .map((node) => String(node.textContent || "").trim())
      .join("");
  }

  function walkElements(root) {
    const out = [];
    const Filter = globalThis.NodeFilter;
    if (root && typeof doc.createTreeWalker === "function" && Filter && Filter.SHOW_ELEMENT) {
      const walker = doc.createTreeWalker(root, Filter.SHOW_ELEMENT);
      while (walker.nextNode()) out.push(walker.currentNode);
      return out;
    }
    const stack = root && root.childNodes ? [...root.childNodes] : [];
    while (stack.length) {
      const node = stack.shift();
      if (!node || node.nodeType !== 1) continue;
      out.push(node);
      if (node.childNodes && node.childNodes.length) stack.unshift(...node.childNodes);
    }
    return out;
  }

  if (op === "href") {
    return { ok: true, href: String(loc.href || "") };
  }

  if (op === "probe") {
    return {
      ok: true,
      text: bodyText().slice(0, 4000),
      url: String(loc.href || ""),
      title: String(doc.title || ""),
    };
  }

  if (op === "upload-point") {
    const nodes = typeof doc.querySelectorAll === "function"
      ? [...doc.querySelectorAll("button, div[role=button], [role=button]")]
      : [];
    const el = nodes.find((node) => {
      const label = String(node.textContent || "").replace(/\s/g, "");
      return label === "上传视频" && node.offsetParent !== null;
    });
    const point = pointFrom(el);
    if (!point) return { ok: false, error: "未找到「上传视频」按钮" };
    return { ok: true, ...point };
  }

  if (op === "form-ready") {
    return { ok: true, ready: /作品描述|添加作品简介/.test(bodyText()) };
  }

  if (op === "fill-title") {
    const title = String(request.title ?? "");
    const inp = typeof doc.querySelector === "function"
      ? doc.querySelector('input[placeholder*="作品标题"]')
      : null;
    if (!inp) return { ok: false, error: "未找到标题输入框", value: null };
    const Ctor = globalThis.HTMLInputElement;
    const proto = Ctor && Ctor.prototype;
    const descriptor = proto ? Object.getOwnPropertyDescriptor(proto, "value") : null;
    if (descriptor && typeof descriptor.set === "function") descriptor.set.call(inp, title);
    else inp.value = title;
    if (typeof inp.dispatchEvent === "function") {
      const EventCtor = globalThis.Event || function EventShim(type) { this.type = type; };
      inp.dispatchEvent(new EventCtor("input", { bubbles: true }));
      inp.dispatchEvent(new EventCtor("change", { bubbles: true }));
    }
    const value = inp.value;
    return { ok: value === title, value };
  }

  if (op === "fill-desc") {
    const desc = String(request.desc ?? "");
    const editors = typeof doc.querySelectorAll === "function"
      ? [...doc.querySelectorAll('[contenteditable="true"]')]
      : [];
    const editor = editors.find((node) => !String(node.textContent || "").trim()) || editors[0];
    if (!editor) return { ok: false, error: "未找到简介编辑器" };
    if (typeof editor.focus === "function") editor.focus();
    if (typeof doc.execCommand === "function") {
      doc.execCommand("selectAll", false, null);
      doc.execCommand("insertText", false, desc);
    } else {
      editor.innerText = desc;
    }
    const text = String(editor.innerText || editor.textContent || "").trim();
    return { ok: text === desc, text };
  }

  if (op === "publish-point") {
    const root = doc.body || doc;
    const elements = walkElements(root);
    for (const el of elements) {
      const tag = String(el.tagName || "").toUpperCase();
      if (tag !== "BUTTON") continue;
      if (ownText(el) !== "发布") continue;
      if (el.offsetParent === null) continue;
      if (typeof el.scrollIntoView === "function") el.scrollIntoView({ block: "center" });
      const point = pointFrom(el);
      if (!point) continue;
      return { ok: true, ...point };
    }
    return { ok: false, error: "未找到「发布」按钮" };
  }

  if (op === "success") {
    return {
      ok: true,
      text: bodyText(),
      url: String(loc.href || ""),
    };
  }

  return { ok: false, error: `unknown op: ${op}` };
}
