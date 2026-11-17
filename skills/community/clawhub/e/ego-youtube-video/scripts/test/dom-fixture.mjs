export class El {
  constructor(tag, opts = {}) {
    this.tagName = String(tag).toUpperCase();
    this.id = opts.id || "";
    this.className = opts.className || "";
    this.attrs = { ...(opts.attrs || {}) };
    this.children = opts.children || [];
    this.shadowRoot = opts.shadow || null;
    this.disabled = !!opts.disabled;
    this.checked = !!opts.checked;
    this.value = opts.value ?? "";
    this.text = opts.text || "";
    this.href = opts.href || "";
    this.owner = null;
    this.parent = null;
    this.clicked = 0;
    this.events = [];
    this.onClick = opts.onClick || null;
    for (const child of this.children) child.parent = this;
    if (this.shadowRoot) this.shadowRoot.parent = this;
    if (opts.lockText != null) {
      const locked = opts.lockText;
      Object.defineProperty(this, "innerText", { configurable: true, get: () => locked, set() {} });
      Object.defineProperty(this, "textContent", { configurable: true, get: () => locked, set() {} });
      Object.defineProperty(this, "value", { configurable: true, get: () => locked, set() {} });
    }
  }

  get innerText() {
    if (this.text) return this.text;
    return this.children.map((child) => child.innerText).filter(Boolean).join("\n");
  }

  set innerText(value) {
    this.text = String(value);
  }

  get textContent() {
    return this.innerText;
  }

  set textContent(value) {
    this.text = String(value);
  }

  getAttribute(name) {
    if (name === "id") return this.id || null;
    if (name === "class") return this.className || null;
    if (name === "href") return this.href || this.attrs.href || null;
    return Object.prototype.hasOwnProperty.call(this.attrs, name) ? this.attrs[name] : null;
  }

  hasAttribute(name) {
    if (name === "disabled") return this.disabled;
    if (name === "checked") return this.checked;
    return Object.prototype.hasOwnProperty.call(this.attrs, name);
  }

  focus() {
    if (this.owner) this.owner._active = this;
  }

  click() {
    this.clicked += 1;
    if (this.tagName === "TP-YT-PAPER-RADIO-BUTTON") {
      this.checked = true;
      this.attrs["aria-checked"] = "true";
    }
    if (this.onClick) this.onClick(this);
  }

  dispatchEvent(event) {
    this.events.push(event);
    if (event && event.type === "keydown" && event.key === "Enter") {
      const tag = String(this.value || this.text || "").replace(/,$/, "").trim();
      if (tag) {
        const chip = new El("ytcp-chip", { text: tag });
        const parent = this.parent || this;
        parent.children.push(chip);
        chip.parent = parent;
        this.value = "";
        this.text = "";
      }
    }
  }

  querySelector(sel) {
    return this.querySelectorAll(sel)[0] || null;
  }

  querySelectorAll(sel) {
    if (String(sel).includes(",")) {
      const out = [];
      for (const part of String(sel).split(",")) {
        for (const node of this.querySelectorAll(part.trim())) {
          if (!out.includes(node)) out.push(node);
        }
      }
      return out;
    }
    const out = [];
    const visit = (node, isRoot) => {
      if (!isRoot && matches(node, sel)) out.push(node);
      for (const child of node.children || []) visit(child, false);
    };
    visit(this, true);
    return out;
  }
}

export function matches(node, sel) {
  if (!node || !node.tagName) return false;
  if (sel === "*") return true;
  if (sel.startsWith("#") && !sel.includes("[") && !sel.includes(".")) return node.id === sel.slice(1);
  const classMatch = sel.match(/^([a-zA-Z0-9-]*)\.([A-Za-z0-9_-]+)$/);
  if (classMatch) {
    const tag = classMatch[1];
    if (tag && node.tagName.toLowerCase() !== tag.toLowerCase()) return false;
    return String(node.className || "").split(/\s+/).includes(classMatch[2]);
  }
  const attr = sel.match(/^([a-zA-Z0-9-]*)\[([a-zA-Z0-9_-]+)=["']([^"']*)["']\]$/);
  if (attr) {
    const tag = attr[1];
    if (tag && node.tagName.toLowerCase() !== tag.toLowerCase()) return false;
    return node.getAttribute(attr[2]) === attr[3];
  }
  if (/^[a-zA-Z0-9-]+$/.test(sel)) return node.tagName.toLowerCase() === sel.toLowerCase();
  return false;
}

export function mountDocument({
  title = "",
  cookie = "",
  href = "https://studio.youtube.com/",
  bodyText = "",
  children = [],
  execCommand = "insert",
} = {}) {
  const body = new El("body", { text: bodyText, children });
  const doc = {
    title,
    cookie,
    body,
    _active: null,
    execCommand(cmd, _ui, value) {
      if (execCommand === "throw") throw new Error("execCommand failed");
      if (execCommand === "noop") return false;
      const target = this._active;
      if (!target) return false;
      if (cmd === "insertText") {
        target.text = value;
        target.value = value;
        return true;
      }
      if (cmd === "selectAll") return true;
      return false;
    },
    querySelector(sel) {
      return body.querySelector(sel);
    },
    querySelectorAll(sel) {
      return body.querySelectorAll(sel);
    },
  };
  const bind = (node) => {
    if (!node || node.owner) return;
    node.owner = doc;
    for (const child of node.children || []) bind(child);
    if (node.shadowRoot) bind(node.shadowRoot);
  };
  bind(body);
  return { doc, location: { href } };
}

export function textbox(id, extra = {}) {
  const box = new El("div", { id: "textbox", attrs: { contenteditable: "true" }, ...extra });
  const shadow = new El("shadow", { children: [box] });
  return new El("ytcp-social-suggestions-textbox", { id, shadow });
}

export function createStudio(initial = {}) {
  const state = {
    href: "https://studio.youtube.com/",
    title: "Channel - YouTube Studio",
    cookie: "LOGIN_INFO=yes; SAPISID=yes",
    bodyText: "YouTube Studio\nAnalytics\nDashboard",
    mode: "studio",
    hasCreate: true,
    menuOpen: false,
    hasSelect: false,
    uploadStarted: false,
    videoHref: "",
    step: "details",
    nextEnabled: true,
    tagsVisible: false,
    error: "",
    clicks: [],
    files: [],
    dialogs: 0,
    execCommand: "insert",
    ...initial,
  };

  function transition(selector) {
    state.clicks.push(selector);
    if (selector === "#create-icon" && !state.blockMenu) state.menuOpen = true;
    if (selector === "upload-menu" || selector.includes("upload-beta")) {
      state.menuOpen = false;
      if (!state.blockSelect) state.hasSelect = true;
    }
    if (selector === "#next-button" && state.nextEnabled && !state.freezeStep) {
      const order = ["details", "elements", "checks", "visibility"];
      const index = Math.max(0, order.indexOf(state.step));
      state.step = order[Math.min(index + 1, order.length - 1)];
    }
    if (selector === "#done-button") {
      state.done = true;
      if (state.limitOnDone) {
        state.error = "daily upload limit reached";
        state.bodyText = "daily upload limit reached";
        return;
      }
      if (!state.suppressStatus) {
        state.bodyText = `${state.bodyText}\nChecks complete\nUpload complete`;
      }
      if (!state.videoHref && !state.suppressId) state.videoHref = "https://youtu.be/AaBbCcDdEe1";
    }
  }

  function build() {
    if (state.mode === "blank") {
      return mountDocument({
        title: "YouTube Studio",
        href: state.href,
        cookie: "",
        bodyText: "",
      });
    }
    if (state.mode === "login") {
      return mountDocument({
        title: "Sign in - Google Accounts",
        href: "https://accounts.google.com/v3/signin/identifier",
        cookie: "",
        bodyText: "Sign in to YouTube\nChoose an account",
      });
    }

    const children = [];
    if (state.hasCreate) {
      children.push(new El("ytcp-button", {
        id: "create-icon",
        text: "Create",
        onClick() { transition("#create-icon"); },
      }));
    }
    if (state.menuOpen) {
      children.push(new El("tp-yt-paper-item", {
        attrs: state.menuByText ? {} : { "test-id": "upload-beta" },
        text: state.menuText || "Upload videos",
        onClick() { transition("upload-menu"); },
      }));
    }
    if (state.hasSelect) {
      children.push(new El("button", {
        id: "select-files-button",
        text: "SELECT FILES",
      }));
    }
    if (state.uploadStarted) {
      if (state.videoHref) {
        children.push(new El("a", {
          className: "ytcp-video-info",
          href: state.videoHref,
          text: state.videoHref,
        }));
      }
      if (state.includeTitle !== false) children.push(textbox("title-textarea"));
      if (state.includeDescription !== false) {
        children.push(textbox("description-textarea", state.lockDescription ? { lockText: "WRONG" } : {}));
      }
      children.push(new El("tp-yt-paper-radio-button", {
        attrs: { name: "VIDEO_MADE_FOR_KIDS_NOT_MFK" },
        text: "No, it's not made for kids",
      }));
      children.push(new El("tp-yt-paper-radio-button", {
        attrs: { name: "VIDEO_MADE_FOR_KIDS_MFK" },
        text: "Yes, it's made for kids",
      }));
      const tagsInput = new El("input", { id: "text-input" });
      const tagsContainer = new El("ytcp-form-input-container", {
        id: "tags-container",
        children: [tagsInput],
      });
      children.push(new El("ytcp-button", {
        id: "toggle-button",
        text: state.showMoreText || "Show more",
        onClick(button) {
          state.tagsVisible = true;
          const body = button.owner && button.owner.body;
          if (body && !body.children.includes(tagsContainer)) {
            body.children.push(tagsContainer);
            tagsContainer.parent = body;
            tagsContainer.owner = button.owner;
            tagsInput.owner = button.owner;
          }
        },
      }));
      if (state.tagsVisible) children.push(tagsContainer);
      if (state.step !== "visibility" && !state.hideNext) {
        children.push(new El("ytcp-button", {
          id: "next-button",
          text: "Next",
          disabled: !state.nextEnabled,
          onClick() { transition("#next-button"); },
        }));
      }
      if (state.step === "visibility") {
        for (const name of ["PRIVATE", "UNLISTED", "PUBLIC"]) {
          children.push(new El("tp-yt-paper-radio-button", { attrs: { name }, text: name }));
        }
        if (!state.hideDone) {
          children.push(new El("ytcp-button", {
            id: "done-button",
            text: "Save",
            disabled: Boolean(state.doneDisabled),
            onClick() { transition("#done-button"); },
          }));
        }
      }
      if (!state.hideFileLoader) {
        children.push(new El("input", { id: "file-loader", attrs: { type: "file" } }));
      }
      if (state.thumbnailButton) {
        children.push(new El("button", {
          text: state.thumbnailButton,
          onClick() { transition("thumbnail-button"); },
        }));
      }
    }
    if (state.error) children.push(new El("div", { id: "error-message", text: state.error }));
    return mountDocument({
      title: state.title,
      cookie: state.cookie,
      href: state.href,
      bodyText: state.bodyText,
      children,
      execCommand: state.execCommand,
    });
  }

  return { state, build, transition };
}
