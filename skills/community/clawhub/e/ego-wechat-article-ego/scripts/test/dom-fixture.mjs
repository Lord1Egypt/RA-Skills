function matches(el, part) {
  if (part === "*") return true;
  let rest = String(part || "");
  let tag = "";
  if (/^[a-zA-Z]/.test(rest)) {
    const cut = rest.match(/^[a-zA-Z0-9-]*/)[0];
    tag = cut.toUpperCase();
    rest = rest.slice(cut.length);
  }
  if (tag && el.tagName !== tag) return false;
  if (rest.startsWith("#")) {
    return String(el.id || "") === rest.slice(1);
  }
  if (rest.startsWith(".")) {
    const cls = rest.slice(1).split("[")[0];
    rest = rest.slice(1 + cls.length);
    const classes = String(el.className || "").split(/\s+/);
    const wanted = cls.split(".").filter(Boolean);
    if (!wanted.every((name) => classes.includes(name))) return false;
  }
  if (rest.startsWith("[")) {
    const body = rest.slice(1, -1);
    const star = body.match(/^([a-zA-Z0-9_-]+)\*=['"]?([^'"]+)['"]?$/);
    const eq = body.match(/^([a-zA-Z0-9_-]+)=['"]?([^'"]+)['"]?$/);
    if (star) return String(el.getAttribute(star[1]) || "").includes(star[2]);
    if (eq) return String(el.getAttribute(eq[1])) === eq[2];
    return false;
  }
  return rest === "";
}

function walk(node, out = []) {
  const kids = node.childNodes || (node.body ? [node.body] : []);
  for (const kid of kids) {
    if (!kid || kid.nodeType === 3) continue;
    out.push(kid);
    walk(kid, out);
  }
  return out;
}

export function queryAll(root, selector) {
  const parts = String(selector).trim().split(/\s+/);
  let current = [root];
  for (const part of parts) {
    const next = [];
    for (const node of current) {
      for (const el of walk(node)) {
        if (matches(el, part)) next.push(el);
      }
    }
    current = [...new Set(next)];
  }
  return current;
}

export function h(tag, props = {}, children = []) {
  const node = {
    tagName: String(tag).toUpperCase(),
    className: props.className || "",
    id: props.id || "",
    placeholder: props.placeholder || "",
    attrs: { ...(props.attrs || {}) },
    value: props.value ?? "",
    text: props.text || "",
    isContentEditable: Boolean(props.editable),
    nodeType: 1,
    childNodes: [],
    clicked: 0,
    events: [],
    type: props.type || "",
  };
  if (props.type) node.attrs.type = props.type;
  if (props.accept) node.attrs.accept = props.accept;
  if (props.editable) node.attrs.contenteditable = "true";
  if (props.title) node.attrs.title = props.title;
  node.getAttribute = (name) => {
    if (name === "class") return node.className;
    if (name === "placeholder") return node.placeholder || (node.attrs && node.attrs.placeholder) || null;
    return Object.prototype.hasOwnProperty.call(node.attrs, name) ? node.attrs[name] : null;
  };
  node.setAttribute = (name, value) => { node.attrs[name] = String(value); };
  Object.defineProperty(node, "innerText", {
    get() { return node.text; },
    set(value) { node.text = String(value); },
  });
  Object.defineProperty(node, "textContent", {
    get() { return node.text || node.childNodes.map((child) => child.textContent || child.text || "").join(""); },
    set(value) { node.text = String(value); },
  });
  node.click = () => { node.clicked += 1; if (props.onClick) props.onClick(node); };
  node.focus = () => { node.focused = true; };
  node.dispatchEvent = (event) => { node.events.push(event); };
  node.querySelectorAll = (selector) => queryAll(node, selector);
  node.querySelector = (selector) => node.querySelectorAll(selector)[0] || null;
  for (const child of children) {
    if (typeof child === "string") {
      node.childNodes.push({ nodeType: 3, textContent: child, childNodes: [] });
      if (!props.text) node.text += child;
    } else {
      node.childNodes.push(child);
      child.parentElement = node;
    }
  }
  return node;
}

export function createDocument(body, { title = "", href = "https://mp.weixin.qq.com/" } = {}) {
  const doc = { title, body };
  doc.querySelectorAll = (selector) => queryAll(doc, selector);
  doc.querySelector = (selector) => doc.querySelectorAll(selector)[0] || null;
  globalThis.document = doc;
  globalThis.location = new URL(href);
  return doc;
}
