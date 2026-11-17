// Minimal DOM for douyinAct and the publish flow. Not a browser.

export function textNode(text) {
  return { nodeType: 3, textContent: text, childNodes: [] };
}

export function element(tag, props = {}) {
  const children = props.children || [];
  const node = {
    nodeType: 1,
    tagName: String(tag).toUpperCase(),
    childNodes: children,
    placeholder: props.placeholder || "",
    role: props.role || "",
    contentEditable: Boolean(props.contentEditable),
    offsetParent: props.hidden ? null : (props.offsetParent || {}),
    rect: props.rect || { x: 10, y: 20, width: 80, height: 32 },
    textContent: "",
    innerText: props.innerText || "",
    scrolled: false,
    focused: false,
    events: [],
    _v: props.value || "",
    getAttribute(name) {
      if (name === "placeholder") return this.placeholder;
      if (name === "role") return this.role || null;
      if (name === "contenteditable") return this.contentEditable ? "true" : null;
      return null;
    },
    getBoundingClientRect() {
      return this.rect;
    },
    scrollIntoView() {
      this.scrolled = true;
    },
    focus() {
      this.focused = true;
    },
    dispatchEvent(event) {
      this.events.push(event && event.type);
    },
    querySelector(selector) {
      return queryAll(this, selector)[0] || null;
    },
    querySelectorAll(selector) {
      return queryAll(this, selector);
    },
  };
  Object.defineProperty(node, "value", {
    configurable: true,
    get() {
      return this._v ?? "";
    },
    set(value) {
      this._v = value;
    },
  });
  refreshText(node);
  return node;
}

function refreshText(node) {
  const parts = [];
  for (const child of node.childNodes || []) {
    if (child.nodeType === 3) parts.push(child.textContent || "");
    else if (child.textContent) parts.push(child.textContent);
  }
  if (!parts.length && node.innerText) node.textContent = node.innerText;
  else node.textContent = parts.join("");
  if (!node.innerText) node.innerText = node.textContent;
}

function queryAll(root, selector) {
  const nodes = [];
  const stack = [root];
  while (stack.length) {
    const node = stack.shift();
    if (node && node.nodeType === 1 && node !== root && matches(node, selector)) nodes.push(node);
    if (node && node.childNodes) stack.push(...node.childNodes);
  }
  if (root && root.nodeType === 1 && matches(root, selector)) nodes.unshift(root);
  return nodes;
}

function matches(node, selector) {
  const sel = String(selector || "");
  if (sel === "button, div[role=button], [role=button]") {
    return node.tagName === "BUTTON" || node.role === "button";
  }
  if (sel === '[contenteditable="true"]') return node.contentEditable === true;
  const placeholder = sel.match(/^input\[placeholder\*="(.+)"\]$/);
  if (placeholder) {
    return node.tagName === "INPUT" && String(node.placeholder || "").includes(placeholder[1]);
  }
  return false;
}

export function installTreeWalker(doc) {
  doc.createTreeWalker = (root) => {
    const list = [];
    const stack = [...(root.childNodes || [])];
    while (stack.length) {
      const node = stack.shift();
      if (!node || node.nodeType !== 1) continue;
      list.push(node);
      if (node.childNodes && node.childNodes.length) stack.unshift(...node.childNodes);
    }
    let index = 0;
    return {
      currentNode: null,
      nextNode() {
        if (index >= list.length) return null;
        this.currentNode = list[index];
        index += 1;
        return this.currentNode;
      },
    };
  };
}

export function createDocument(body, { title = "", href = "https://creator.douyin.com/creator-micro/content/upload", treeWalker = true } = {}) {
  const doc = {
    title,
    body,
    childNodes: [body],
    nodeType: 1,
    querySelector(selector) {
      return body.querySelector(selector);
    },
    querySelectorAll(selector) {
      return body.querySelectorAll(selector);
    },
    execCommand(command, _ui, value) {
      const editor = doc._activeEditor;
      if (!editor) return false;
      if (command === "insertText") {
        editor.innerText = doc._badDesc ? `${value}!` : value;
        editor.textContent = editor.innerText;
      }
      return true;
    },
  };
  if (treeWalker) installTreeWalker(doc);
  const location = { href };
  function HTMLInputElement() {}
  Object.defineProperty(HTMLInputElement.prototype, "value", {
    configurable: true,
    get() {
      return this._v ?? "";
    },
    set(value) {
      this._v = doc._badTitle ? "WRONG" : value;
    },
  });
  return {
    doc,
    location,
    HTMLInputElement,
    NodeFilter: { SHOW_ELEMENT: 1 },
    Event: class Event {
      constructor(type) {
        this.type = type;
      }
    },
  };
}

export function withDocument(built, fn) {
  const prev = {
    document: globalThis.document,
    location: globalThis.location,
    HTMLInputElement: globalThis.HTMLInputElement,
    NodeFilter: globalThis.NodeFilter,
    Event: globalThis.Event,
  };
  globalThis.document = built.doc;
  globalThis.location = built.location;
  globalThis.HTMLInputElement = built.HTMLInputElement;
  globalThis.NodeFilter = built.NodeFilter;
  globalThis.Event = built.Event;
  try {
    return fn();
  } finally {
    globalThis.document = prev.document;
    globalThis.location = prev.location;
    globalThis.HTMLInputElement = prev.HTMLInputElement;
    globalThis.NodeFilter = prev.NodeFilter;
    globalThis.Event = prev.Event;
  }
}
