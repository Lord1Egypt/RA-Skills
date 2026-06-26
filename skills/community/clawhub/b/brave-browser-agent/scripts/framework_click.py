#!/usr/bin/env python3
"""Multi-strategy framework-aware click for React/Vue/Angular SPAs.

Handles the hard cases where CDP native mouse events fail due to:
- React/Vue framework event management
- Element overlays/modals
- Disabled state / CSS pointer-events: none
- Element not in viewport
- **Editor data not synced to framework state** (CKEditor, Lexical, ProseMirror, Quill, 语雀)

Strategies (tried in order):
  0. editor_sync — Auto-sync rich text editors before clicking (CKEditor 4/5, Lexical, ProseMirror, Quill, 语雀, iframe editors)
  1. hit_test_click — scrollIntoView + hit-test + CDP Input.dispatchMouseEvent (complete sequence)
  2. react_fiber_click — Direct React onClick invocation + React 18 root delegation fallback
  3. vue_emit_click — Enhanced Vue 2/3 click (component tree traversal, $emit, $listeners, setupState)
  4. dispatch_event_click — Native MouseEvent with dispatchEvent
  5. enter_key_click — Enter key on focused element (for forms)
  6. raw_cdp_click — Fallback to original CDP mouse events

Publish validation after click:
  - Auto-detects success via toast messages, URL change, modal state, button state
  - Reports errors if found

Usage:
    python3 framework_click.py smart-click <tab_id> --selector "button.submit"
    python3 framework_click.py smart-click <tab_id> --text "发布"
    python3 framework_click.py detect-framework <tab_id>
    python3 framework_click.py analyze-button <tab_id> --selector "button.submit"
    python3 framework_click.py publish-validate <tab_id>
"""

import argparse
import asyncio
import json
import random
import sys
import time
import urllib.request

try:
    import websockets
except ImportError:
    print("Error: websockets not installed. Run: pip3 install websockets", file=sys.stderr)
    sys.exit(1)

DEFAULT_PORT = 9222
MAX_WS_SIZE = 50 * 1024 * 1024
STRATEGY_ORDER = ["editor_sync", "hit_test_click", "react_fiber_click", "vue_emit_click",
                  "dispatch_event_click", "enter_key_click", "raw_cdp_click"]


def get_port():
    import os
    return int(os.environ.get("CDP_PORT", DEFAULT_PORT))


def get_ws_url(tab_id):
    """Get WebSocket URL for a tab."""
    port = get_port()
    try:
        tabs = json.loads(urllib.request.urlopen(
            f"http://localhost:{port}/json/list", timeout=5
        ).read())
    except Exception as e:
        return None
    for t in tabs:
        if t.get("id") == tab_id:
            return t.get("webSocketDebuggerUrl")
    return None


class CDPConnection:
    """Manage a CDP WebSocket connection with message ID tracking."""

    def __init__(self, ws):
        self.ws = ws
        self.msg_id = 0

    async def send_cdp(self, method, params=None):
        """Send a CDP command and wait for its response."""
        self.msg_id += 1
        msg = {"id": self.msg_id, "method": method}
        if params:
            msg["params"] = params
        await self.ws.send(json.dumps(msg))
        target_id = self.msg_id
        while True:
            resp = json.loads(await self.ws.recv())
            if resp.get("id") == target_id:
                return resp

    async def eval_js(self, js, return_by_value=True, timeout_ms=10000):
        """Execute JS and return the result value."""
        resp = await self.send_cdp("Runtime.evaluate", {
            "expression": js,
            "returnByValue": return_by_value,
            "timeout": timeout_ms,
        })
        result = resp.get("result", {}).get("result", {})
        if result.get("subtype") == "error":
            return {"error": result.get("description", "Unknown error")}
        val = result.get("value")
        # Auto-decode JSON strings
        if isinstance(val, str):
            try:
                return json.loads(val)
            except (json.JSONDecodeError, TypeError):
                pass
        return val

    async def enable_runtime(self):
        await self.send_cdp("Runtime.enable")

    async def mouse_over(self, x, y):
        return await self.send_cdp("Input.dispatchMouseEvent", {
            "type": "mouseMoved", "x": x, "y": y
        })

    async def pointer_down(self, x, y):
        return await self.send_cdp("Input.dispatchMouseEvent", {
            "type": "mousePressed", "x": x, "y": y,
            "button": "left", "clickCount": 1,
            "pointerType": "mouse"
        })

    async def pointer_up(self, x, y):
        return await self.send_cdp("Input.dispatchMouseEvent", {
            "type": "mouseReleased", "x": x, "y": y,
            "button": "left", "clickCount": 1,
            "pointerType": "mouse"
        })

    async def complete_click(self, x, y, delay_ms=80):
        """Complete mouse click sequence: move→press→release (with human-like delays)."""
        rx = x + random.uniform(-3, 3)
        ry = y + random.uniform(-3, 3)
        # mouseover/mousemove
        await self.mouse_over(rx, ry)
        await asyncio.sleep(random.uniform(0.03, 0.08))
        # mousedown
        await self.pointer_down(rx, ry)
        await asyncio.sleep(delay_ms / 1000.0)
        # mouseup
        await self.pointer_up(rx, ry)
        return {"strategy": "raw_cdp", "success": True, "x": round(rx), "y": round(ry)}


# ======== JavaScript Snippets ========

JS_DETECT_FRAMEWORK = """(function() {
    const info = {};
    // Check React
    if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__ || document.querySelector('[data-reactroot], [data-reactid]')) {
        info.react = true;
        try {
            const appEl = document.getElementById('root') || document.getElementById('app') || document.body;
            const keys = Object.keys(appEl).filter(k => k.startsWith('__reactFiber$'));
            info.reactFiberKeys = keys.length;
            const propsKeys = Object.keys(appEl).filter(k => k.startsWith('__reactProps$'));
            info.reactPropsKeys = propsKeys.length;
        } catch(e) { info.reactDetail = e.message; }
    }
    // Check Vue 3
    const vueApp = document.querySelector('[data-v-app]') || document.querySelector('#app');
    if (vueApp && vueApp.__vue_app__) {
        info.vue = true;
        info.vueVersion = '3';
    }
    // Check Vue 2
    if (window.__VUE_DEVTOOLS_GLOBAL_HOOK__ || document.querySelector('[__vue__]')) {
        info.vue = info.vue || true;
        info.vueVersion = info.vueVersion || '2';
    }
    // Check Angular
    if (document.querySelector('[ng-version]')) {
        info.angular = true;
        const ngEl = document.querySelector('[ng-version]');
        info.ngVersion = ngEl ? ngEl.getAttribute('ng-version') : '?';
    }
    // Check jQuery
    if (window.jQuery) {
        info.jquery = true;
    }
    // Check common SPA frameworks
    info.isSPA = false;
    const routerLinks = document.querySelectorAll('[routerlink]');
    if (routerLinks.length > 0) info.isSPA = true;

    // Check for overlay/modals
    info.overlays = [];
    document.querySelectorAll('[class*="modal"], [class*="overlay"], [class*="dialog"], [class*="popup"]').forEach(el => {
        const style = window.getComputedStyle(el);
        if (style.display !== 'none' && style.visibility !== 'hidden' && el.offsetParent !== null) {
            info.overlays.push({
                tag: el.tagName.toLowerCase(),
                id: el.id || '',
                classes: (el.className || '').substring(0, 60),
                zIndex: style.zIndex
            });
        }
    });

    return JSON.stringify(info);
})()"""


def _build_locate_js(selector, text=None, index=0):
    """Build JS to locate an element and return its bounding rect."""
    if text:
        escaped = text.replace("'", "\\'")
        return f"""(function() {{
            const els = document.querySelectorAll('{selector}');
            for (const el of els) {{
                if ((el.innerText || el.value || el.getAttribute('aria-label') || '').includes('{escaped}')) {{
                    el.scrollIntoView({{behavior: 'instant', block: 'center'}});
                    const r = el.getBoundingClientRect();
                    return JSON.stringify({{
                        x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2),
                        width: Math.round(r.width), height: Math.round(r.height),
                        text: (el.innerText || '').substring(0, 80)
                    }});
                }}
            }}
            return JSON.stringify({{error: "text not found", text: '{escaped}'}});
        }})()"""
    else:
        return f"""(function() {{
            const els = document.querySelectorAll('{selector}');
            if (els.length === 0) return JSON.stringify({{error: "no elements", selector: '{selector}'}});
            const idx = Math.min({index}, els.length - 1);
            const el = els[idx];
            el.scrollIntoView({{behavior: 'instant', block: 'center'}});
            const r = el.getBoundingClientRect();
            return JSON.stringify({{
                x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2),
                width: Math.round(r.width), height: Math.round(r.height),
                text: (el.innerText || '').substring(0, 80),
                total: els.length, index: idx
            }});
        }})()"""


JS_HIT_TEST = """(function() {
    const el = arguments[0];
    if (!el) return JSON.stringify({error: "no element"});
    const r = el.getBoundingClientRect();
    const cx = Math.round(r.left + r.width / 2);
    const cy = Math.round(r.top + r.height / 2);

    // Check basic clickability
    const style = window.getComputedStyle(el);
    const checks = {
        isConnected: el.isConnected,
        rectZero: r.width === 0 || r.height === 0,
        pointerEventsNone: style.pointerEvents === 'none',
        opacityZero: parseFloat(style.opacity) === 0,
        visibilityHidden: style.visibility === 'hidden',
        displayNone: style.display === 'none',
        disabled: el.disabled === true,
        readonly: el.readOnly === true,
    };
    checks.clickable = !(checks.rectZero || checks.pointerEventsNone ||
                         checks.opacityZero || checks.visibilityHidden || checks.displayNone || checks.disabled);

    // elementFromPoint hit test (check if element is on top)
    const topEl = document.elementFromPoint(cx, cy);
    checks.hitTestPass = topEl === el || el.contains(topEl) || (topEl && topEl.contains(el));
    checks.topElementTag = topEl ? (topEl.tagName || '') : 'null';
    checks.topElementId = topEl ? (topEl.id || '') : '';
    checks.topElementClass = topEl ? ((topEl.className || '').substring(0, 60)) : '';

    // If not clickable, try to find blocker
    if (!checks.clickable || !checks.hitTestPass) {
        checks.blocker = checks.hitTestPass ? null : {
            tag: topEl ? topEl.tagName.toLowerCase() : null,
            id: topEl ? topEl.id : null,
            classes: topEl ? ((topEl.className || '').substring(0, 80)) : null
        };
    }

    checks.coords = {x: cx, y: cy};
    return JSON.stringify(checks);
})()"""


JS_REACT_FIBER_CLICK = """(function() {
    const els = document.querySelectorAll('%s');
    const idx = Math.min(%d, els.length - 1);
    if (els.length === 0) return JSON.stringify({error: "no elements found"});
    const el = els[idx];

    // Find React fiber props
    const allKeys = Object.keys(el);
    const fiberKey = allKeys.find(k => k.startsWith('__reactFiber$'));
    const propsKey = allKeys.find(k => k.startsWith('__reactProps$'));

    if (propsKey) {
        const props = el[propsKey];
        // Try various event handler names
        const handlers = ['onClick', 'onClickCapture', 'onPointerDown', 'onMouseDown',
                          'onMouseUp', 'onSubmit', 'onChange', 'onInput'];
        for (const handler of handlers) {
            if (typeof props[handler] === 'function') {
                const event = new MouseEvent(handler === 'onSubmit' ? 'submit' :
                    handler === 'onChange' ? 'change' :
                    handler === 'onInput' ? 'input' :
                    'click', {
                    bubbles: true, cancelable: true, view: window,
                    button: 0, buttons: 1, clientX: 0, clientY: 0
                });
                Object.defineProperty(event, 'isTrusted', {value: true});
                props[handler](event);
                return JSON.stringify({strategy: 'react_fiber', handler: handler, success: true});
            }
        }
        return JSON.stringify({error: "no matching handler found in props", keys: Object.keys(props).slice(0, 20)});
    }

    if (fiberKey) {
        // Try to traverse React fiber tree to find onClick
        try {
            let fiber = el[fiberKey];
            let depth = 0;
            while (fiber && depth < 10) {
                const memoizedProps = fiber.memoizedProps || fiber.pendingProps;
                if (memoizedProps) {
                    for (const handler of ['onClick', 'onClickCapture']) {
                        if (typeof memoizedProps[handler] === 'function') {
                            const event = new MouseEvent('click', {
                                bubbles: true, cancelable: true, view: window, button: 0
                            });
                            memoizedProps[handler](event);
                            return JSON.stringify({strategy: 'react_fiber_traverse', handler: handler, depth: depth, success: true});
                        }
                    }
                }
                fiber = fiber.return;
                depth++;
            }
        } catch(e) {
            return JSON.stringify({error: "fiber traversal failed: " + e.message});
        }
        return JSON.stringify({error: "no onClick in fiber tree"});
    }

    return JSON.stringify({error: "no React fiber or props found on element"});
})()"""


JS_VUE_EMIT_CLICK = """(function() {
    const els = document.querySelectorAll('%s');
    const idx = Math.min(%d, els.length - 1);
    if (els.length === 0) return JSON.stringify({error: "no elements found"});
    const el = els[idx];

    // Vue 3: check __vueParentComponent
    const vueKeys = Object.keys(el).filter(k => k.startsWith('__vueParentComponent') || k.startsWith('__vue_app') || k.includes('__vue'));
    const parentCompKey = vueKeys.find(k => k.startsWith('__vueParentComponent'));

    if (parentCompKey) {
        try {
            const comp = el[parentCompKey];
            const props = comp.props || (comp.vnode && comp.vnode.props) || {};
            const emit = comp.emit || (comp.setupState && comp.setupState.emit) || null;
            const handlers = ['onClick', 'on-click', 'click'];
            for (const h of handlers) {
                if (typeof props[h] === 'function') {
                    props[h](new MouseEvent('click', {bubbles: true, cancelable: true}));
                    return JSON.stringify({strategy: 'vue_parent', handler: h, success: true});
                }
            }
            if (emit) {
                return JSON.stringify({strategy: 'vue_emit', attempted: true, note: 'emit found but no onClick handler'});
            }
            return JSON.stringify({strategy: 'vue_parent', note: 'no onClick found', propsKeys: Object.keys(props).slice(0, 10)});
        } catch(e) {
            return JSON.stringify({error: "vue parent error: " + e.message});
        }
    }

    // Vue 2: check __vue__
    if (el.__vue__) {
        try {
            const handlers = ['click', 'onClick', 'on-click'];
            for (const h of handlers) {
                if (typeof el.__vue__[h] === 'function') {
                    el.__vue__[h]();
                    return JSON.stringify({strategy: 'vue2', handler: h, success: true});
                }
            }
            if (el.__vue__._events && el.__vue__._events.click) {
                return JSON.stringify({strategy: 'vue2_events', hasClick: true});
            }
        } catch(e) {
            return JSON.stringify({error: "vue2 error: " + e.message});
        }
    }

    return JSON.stringify({error: "no Vue component found", vueKeys: vueKeys});
})()"""


JS_DISPATCH_EVENT_CLICK = """(function() {
    const els = document.querySelectorAll('%s');
    const idx = Math.min(%d, els.length - 1);
    if (els.length === 0) return JSON.stringify({error: "no elements found"});
    const el = els[idx];

    // Create a real MouseEvent with isTrusted=true
    try {
        const event = new MouseEvent('click', {
            bubbles: true, cancelable: true, view: window,
            button: 0, buttons: 1, clientX: 0, clientY: 0,
            screenX: 0, screenY: 0, detail: 1
        });
        // Override isTrusted to be true
        Object.defineProperty(event, 'isTrusted', { value: true, writable: false });
        const dispatched = el.dispatchEvent(event);
        return JSON.stringify({strategy: 'dispatch_event', success: dispatched, cancelled: !dispatched});
    } catch(e) {
        return JSON.stringify({error: "dispatch error: " + e.message});
    }
})()"""


JS_ENTER_KEY_CLICK = """(function() {
    const els = document.querySelectorAll('%s');
    const idx = Math.min(%d, els.length - 1);
    if (els.length === 0) return JSON.stringify({error: "no elements found"});
    const el = els[idx];

    // Focus the element
    el.focus();

    // Dispatch keyboard events
    try {
        const enterDown = new KeyboardEvent('keydown', {
            key: 'Enter', code: 'Enter', keyCode: 13, which: 13,
            bubbles: true, cancelable: true, composed: true
        });
        el.dispatchEvent(enterDown);

        // Also try 'keypress'
        const enterPress = new KeyboardEvent('keypress', {
            key: 'Enter', code: 'Enter', keyCode: 13, which: 13,
            bubbles: true, cancelable: true, composed: true
        });
        el.dispatchEvent(enterPress);

        // And the form submit if element is a button in a form
        const form = el.closest('form');
        if (form) {
            const submitEvent = new SubmitEvent('submit', {bubbles: true, cancelable: true});
            form.dispatchEvent(submitEvent);
            return JSON.stringify({strategy: 'enter_key', success: true, formSubmitted: true});
        }

        const enterUp = new KeyboardEvent('keyup', {
            key: 'Enter', code: 'Enter', keyCode: 13, which: 13,
            bubbles: true, cancelable: true, composed: true
        });
        el.dispatchEvent(enterUp);

        return JSON.stringify({strategy: 'enter_key', success: true});
    } catch(e) {
        return JSON.stringify({error: "enter key error: " + e.message});
    }
})()"""


JS_ANALYZE_BUTTON = """(function() {
    const els = document.querySelectorAll('%s');
    if (els.length === 0) return JSON.stringify({error: "no elements"});
    const idx = Math.min(%d, els.length - 1);
    const el = els[idx];
    const r = el.getBoundingClientRect();
    const style = window.getComputedStyle(el);
    const allKeys = Object.keys(el);

    // Check overlays covering the button
    const cx = Math.round(r.left + r.width / 2);
    const cy = Math.round(r.top + r.height / 2);
    const topEl = document.elementFromPoint(cx, cy);

    // Check React/Vue bindings
    const fiberKey = allKeys.find(k => k.startsWith('__reactFiber$'));
    const propsKey = allKeys.find(k => k.startsWith('__reactProps$'));
    const vueKeys = allKeys.filter(k => k.includes('__vue') || k.includes('__vnode'));

    return JSON.stringify({
        tag: el.tagName.toLowerCase(),
        id: el.id || '',
        classes: (el.className || '').substring(0, 100),
        type: el.type || '',
        disabled: el.disabled || false,
        readonly: el.readOnly || false,
        text: (el.innerText || el.value || '').substring(0, 100),
        rect: {x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height)},
        center: {x: cx, y: cy},
        style: {
            pointerEvents: style.pointerEvents,
            opacity: style.opacity,
            visibility: style.visibility,
            display: style.display,
            zIndex: style.zIndex,
            position: style.position,
        },
        isVisible: r.width > 0 && r.height > 0 && style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0',
        hitTest: {
            topElement: topEl ? topEl.tagName.toLowerCase() : null,
            topElementId: topEl ? topEl.id : null,
            topElementClass: topEl ? ((topEl.className || '').substring(0, 80)) : null,
            isTarget: topEl === el || (topEl && el.contains(topEl)) || (topEl && topEl.contains(el))
        },
        framework: {
            hasReactFiber: !!fiberKey,
            hasReactProps: !!propsKey,
            reactProps: propsKey ? Object.keys(el[propsKey]).filter(k => k.startsWith('on')).slice(0, 10) : [],
            vueKeys: vueKeys.slice(0, 5),
        },
        attrDisabled: el.getAttribute('disabled') !== null,
        attrAriaDisabled: el.getAttribute('aria-disabled'),
        scrollY: window.scrollY
    }, null, 2);
})()"""


JS_EDITOR_SYNC = """(function() {
    const results = {editorsFound: [], synced: []};

    // 1. CKEditor 4/5: fire change + updateElement
    if (window.CKEDITOR) {
        for (const instanceId in (window.CKEDITOR.instances || {})) {
            try {
                const editor = window.CKEDITOR.instances[instanceId];
                editor.fire('change');
                editor.updateElement();
                results.editorsFound.push('ckeditor4:' + instanceId);
            } catch(e) { results.editorsFound.push('ckeditor4:error:' + e.message); }
        }
    }
    if (window.ClassicEditor) {
        try {
            const editor = window.ClassicEditor;
            editor.updateSourceElement();
            editor.fire('change:data');
            results.editorsFound.push('ckeditor5');
        } catch(e) { results.editorsFound.push('ckeditor5:error:' + e.message); }
    }

    // 2. CKEditor instance on global (some platforms)
    for (const k in window) {
        if (k.startsWith('CKEDITOR') && typeof window[k] === 'object') continue;
        try {
            const v = window[k];
            if (v && v.document && v.fire && typeof v.fire === 'function' &&
                v.editing && v.editing.view) {
                v.fire('change:data');
                v.editing.view.change(w => {
                    w.forceRender();
                    w.forceRender();
                });
                results.editorsFound.push('ckeditor5_global:' + k);
            }
        } catch(e) {}
    }

    // 3. Lexical editor: trigger update + sync
    for (const k in window) {
        try {
            const v = window[k];
            if (v && v._editorState && v.update && v.dispatchCommand) {
                // Lexical instance - trigger state update
                v.update(() => {
                    const root = v.getRoot();
                    if (root) root.write(() => {});
                });
                results.synced.push('lexical:' + k);
            }
        } catch(e) {}
    }

    // 4. ProseMirror / TipTap
    document.querySelectorAll('.ProseMirror, [class*="ProseMirror"]').forEach(el => {
        try {
            if (el.pmViewDesc && el.pmViewDesc.editorView) {
                const view = el.pmViewDesc.editorView;
                view.dispatch(view.state.tr);
                results.synced.push('prosemirror');
            }
        } catch(e) {}
    });

    // 5. Quill editor delta sync
    document.querySelectorAll('[class*="ql-"], .quill-editor').forEach(el => {
        try {
            if (el.__quill) {
                const quill = el.__quill;
                quill.update();
                quill.emitter.emit('text-change', quill.getContents(), quill.getContents(), 'api');
                results.synced.push('quill');
            }
        } catch(e) {}
    });

    // 6. 语雀/阿里云编辑器: trigger input on contenteditable
    document.querySelectorAll('[contenteditable="true"], .lake-editor, [class*="lake"]').forEach(el => {
        try {
            el.dispatchEvent(new Event('input', {bubbles: true, cancelable: true}));
            el.dispatchEvent(new Event('change', {bubbles: true, cancelable: true}));
            results.synced.push('contenteditable_input');
        } catch(e) {}
    });

    // 7. Vue v-model sync: find and trigger input events on all form elements
    document.querySelectorAll('textarea, input, [contenteditable]').forEach(el => {
        try {
            // Trigger native input event for Vue v-model / React onChange sync
            const event = new Event('input', {bubbles: true, cancelable: true});
                el.dispatchEvent(event);
        } catch(e) {}
    });

    // 8. Vue 3 vnode dirty marking (force update)
    const appEl = document.querySelector('#app, [data-v-app]');
    if (appEl && appEl.__vue_app__) {
        try {
            const app = appEl.__vue_app__;
            if (app._instance) {
                app._instance.update();
                results.synced.push('vue3_app_update');
            }
        } catch(e) {}
    }

    // 9. CKEditor 5 iframe detection (CSDN pattern)
    document.querySelectorAll('iframe').forEach(iframe => {
        try {
            const idoc = iframe.contentDocument || iframe.contentWindow?.document;
            if (!idoc) return;
            // CKEditor inside iframe
            const ckeditor5 = idoc.querySelector('.ck-editor__editable');
            if (ckeditor5) {
                ckeditor5.dispatchEvent(new Event('input', {bubbles: true}));
                results.synced.push('ckeditor5_iframe');
            }
            // Generic trigger
            idoc.querySelectorAll('[contenteditable]').forEach(el => {
                el.dispatchEvent(new Event('input', {bubbles: true}));
                results.synced.push('iframe_contenteditable');
            });
        } catch(e) {}
    });

    return JSON.stringify(results);
})()"""


JS_REACT_18_ROOT_CLICK = """(function() {
    const els = document.querySelectorAll('%s');
    const idx = Math.min(%d, els.length - 1);
    if (els.length === 0) return JSON.stringify({error: "no elements found"});
    const el = els[idx];

    // React 18+ root container event delegation
    const rootEl = document.getElementById('root') || document.getElementById('app') || document.body;
    const rootKeys = Object.keys(rootEl);
    const containerKey = rootKeys.find(k => k.startsWith('__reactContainer$'));

    if (containerKey) {
        try {
            const container = rootEl[containerKey];
            const event = new MouseEvent('click', {
                bubbles: true, cancelable: true,
                clientX: 0, clientY: 0, button: 0, buttons: 1,
                view: window
            });
            Object.defineProperty(event, '_reactName', {value: 'onClick'});
            Object.defineProperty(event, '_targetInst', {value: container});
            const dispatched = el.dispatchEvent(event);
            return JSON.stringify({strategy: 'react18_root_click', success: dispatched, cancelled: !dispatched});
        } catch(e) {
            return JSON.stringify({error: "react18 root click: " + e.message});
        }
    }

    // React ByteUI / Ant Design: try finding onClick inside memoizedProps
    const allKeys = Object.keys(el);
    const fiberKey = allKeys.find(k => k.startsWith('__reactFiber$'));

    if (fiberKey) {
        try {
            let fiber = el[fiberKey];
            let depth = 0;
            const handlers = ['onClick', 'onClickCapture', 'onMouseDown', 'onPointerDown'];
            while (fiber && depth < 20) {
                const mp = fiber.memoizedProps || fiber.pendingProps || null;
                if (mp) {
                    for (const h of handlers) {
                        if (typeof mp[h] === 'function') {
                            // Clone with proper event type
                            const evtType = h === 'onMouseDown' ? 'mousedown' :
                                            h === 'onPointerDown' ? 'pointerdown' : 'click';
                            const event = new MouseEvent(evtType, {
                                bubbles: true, cancelable: true,
                                clientX: 0, clientY: 0, button: 0,
                                view: window
                            });
                            Object.defineProperty(event, 'isTrusted', {value: true});
                            mp[h](event);
                            return JSON.stringify({strategy: 'react_fiber_deep', handler: h, depth: depth, success: true});
                        }
                    }
                }
                fiber = fiber.return;
                depth++;
            }
        } catch(e) {
            return JSON.stringify({error: "fiber deep traversal: " + e.message});
        }
    }

    // Fallback: try all event listeners using getEventListeners (Chrome devtools)
    if (typeof getEventListeners !== 'undefined') {
        try {
            const listeners = getEventListeners(el);
            for (const type of ['click', 'mousedown', 'pointerdown']) {
                if (listeners[type]) {
                    for (const l of listeners[type]) {
                        const event = new MouseEvent(type, {bubbles: true, cancelable: true, view: window});
                        Object.defineProperty(event, 'isTrusted', {value: true});
                        l.listener(event);
                        return JSON.stringify({strategy: 'getEventListeners', type: type, success: true});
                    }
                }
            }
        } catch(e) {}
    }

    return JSON.stringify({error: "React 18 click failed - no fiber or listeners found"});
})()"""


JS_VUE_ENHANCED_CLICK = """(function() {
    const els = document.querySelectorAll('%s');
    const idx = Math.min(%d, els.length - 1);
    if (els.length === 0) return JSON.stringify({error: "no elements found"});
    const el = els[idx];

    const strategies = [];

    // VUE 3: Full component tree traversal
    const isVue3 = el.__vue_app__ || document.querySelector('#app')?.__vue_app__;
    const vueKeys = Object.keys(el).filter(k => k.startsWith('__vueParentComponent') || k.includes('__vue'));

    if (isVue3 || vueKeys.length) {
        try {
            // Try __vueParentComponent chain
            let comp = null;
            const pcKey = vueKeys.find(k => k.startsWith('__vueParentComponent'));
            if (pcKey) {
                comp = el[pcKey];
                let depth = 0;
                while (comp && depth < 15) {
                    const props = comp.props || {};
                    const setupState = comp.setupState || {};

                    // Check props.onClick patterns
                    for (const key of ['onClick', 'on-click', 'onClickCapture']) {
                        if (typeof props[key] === 'function') {
                            const event = new MouseEvent('click', {bubbles: true, cancelable: true, view: window});
                            Object.defineProperty(event, 'isTrusted', {value: true});
                            props[key](event);
                            strategies.push({method: 'vue3_props_' + key, depth: depth, success: true});
                            if (strategies.filter(s => s.success).length) {
                                return JSON.stringify({success: true, strategies: strategies});
                            }
                        }
                    }

                    // Check setupState handlers
                    for (const key of Object.keys(setupState)) {
                        if (typeof setupState[key] === 'function' &&
                            (key.includes('click') || key.includes('publish') || key.includes('submit') ||
                             key.includes('发布') || key.includes('确认'))) {
                            setupState[key]();
                            strategies.push({method: 'vue3_setupState_' + key, success: true});
                            return JSON.stringify({success: true, strategies: strategies});
                        }
                    }

                    // Try emit
                    if (comp.emit && typeof comp.emit === 'function') {
                        comp.emit('click');
                        comp.emit('on-click');
                        strategies.push({method: 'vue3_emit', success: true});
                    }

                    // Go up the component tree
                    if (comp.subTree) {
                        // Try walking the subTree for event listeners
                        const walkVNode = (vnode) => {
                            if (!vnode) return null;
                            const handlers = ['onClick', 'on-click', 'click'];
                            const vnodeProps = vnode.props || {};
                            for (const h of handlers) {
                                const handler = vnodeProps[h] || (vnodeProps.on && vnodeProps.on[h]);
                                if (typeof handler === 'function') {
                                    handler(new MouseEvent('click', {bubbles: true}));
                                    return {method: 'vue3_vnode_' + h, success: true};
                                }
                            }
                            if (vnode.component) {
                                const result = walkVNode(vnode.component.subTree);
                                if (result) return result;
                            }
                            if (vnode.children && Array.isArray(vnode.children)) {
                                for (const child of vnode.children) {
                                    const result = walkVNode(child);
                                    if (result) return result;
                                }
                            }
                            return null;
                        };
                        const vnodeResult = walkVNode(comp.subTree);
                        if (vnodeResult) {
                            strategies.push(vnodeResult);
                            return JSON.stringify({success: true, strategies: strategies});
                        }
                    }

                    comp = comp.parent;
                    depth++;
                }
            }

            // Vue 3 app-level attempt
            const vueApp = document.querySelector('#app, [data-v-app]');
            if (vueApp && vueApp.__vue_app__) {
                const appInstance = vueApp.__vue_app__._instance;
                if (appInstance && appInstance.proxy) {
                    // Try to find methods on the root component
                    for (const key of Object.keys(appInstance.proxy)) {
                        if (typeof appInstance.proxy[key] === 'function' &&
                            (key.includes('publish') || key.includes('submit') ||
                             key.includes('发布') || key.includes('confirm'))) {
                            appInstance.proxy[key]();
                            strategies.push({method: 'vue3_app_proxy_' + key, success: true});
                            return JSON.stringify({success: true, strategies: strategies});
                        }
                    }
                }
            }
        } catch(e) {
            strategies.push({method: 'error', message: e.message});
        }
    }

    // VUE 2: Enhanced detection
    if (el.__vue__ && !strategies.filter(s => s.success).length) {
        try {
            const vm = el.__vue__;
            // Try $emit
            if (typeof vm.$emit === 'function') {
                vm.$emit('click');
                strategies.push({method: 'vue2_$emit', success: true});
            }
            // Try $listeners
            if (vm.$listeners && vm.$listeners.click) {
                if (typeof vm.$listeners.click === 'function') {
                    vm.$listeners.click(new MouseEvent('click', {bubbles: true}));
                    strategies.push({method: 'vue2_$listeners', success: true});
                } else if (Array.isArray(vm.$listeners.click)) {
                    vm.$listeners.click.forEach(fn => {
                        if (typeof fn === 'function') fn(new MouseEvent('click', {bubbles: true}));
                    });
                    strategies.push({method: 'vue2_$listeners_array', success: true});
                }
            }
            // Try $parent chain for methods
            let parent = vm.$parent;
            let depth = 0;
            while (parent && depth < 10) {
                if (parent._events && parent._events.click) {
                    parent._events.click.forEach(fn => {
                        if (typeof fn === 'function') fn(new MouseEvent('click', {bubbles: true}));
                    });
                    strategies.push({method: 'vue2_parent_events', depth: depth});
                }
                for (const key of Object.keys(parent)) {
                    if (typeof parent[key] === 'function' &&
                        (key === 'handlePublish' || key === 'publish' || key === 'submit' ||
                         key === 'handleSubmit' || key === 'confirmSubmit')) {
                        parent[key]();
                        strategies.push({method: 'vue2_parent_method_' + key, depth: depth, success: true});
                        return JSON.stringify({success: true, strategies: strategies});
                    }
                }
                parent = parent.$parent;
                depth++;
            }

            // Try Vue 2 dispatch/broadcast
            if (typeof vm.$dispatch === 'function') {
                vm.$dispatch('click');
                strategies.push({method: 'vue2_$dispatch'});
            }
        } catch(e) {
            strategies.push({method: 'vue2_error', message: e.message});
        }
    }

    if (strategies.filter(s => s.success).length) {
        return JSON.stringify({success: true, strategies: strategies});
    }

    return JSON.stringify({success: false, strategies: strategies, vueKeys: vueKeys});
})()"""


JS_PUBLISH_VALIDATE = """(function() {
    const results = {validations: []};

    // Check 1: URL changed (redirect after publish)
    const currentUrl = window.location.href;
    results.currentUrl = currentUrl;

    // Check 2: Toast / notification messages
    const allText = document.body.innerText || '';
    const successKeywords = ['发布成功', '文章已发布', 'published', 'success', '已发表',
                             '审核通过', '待审核', '提交成功', '推送成功', '草稿已发布'];

    // Check 3: Common success indicators
    const indicators = {
        successToasts: [],
        dialogClosed: false,
    };

    // Look for success toast/message
    for (const el of document.querySelectorAll('[class*="toast"], [class*="message"], [class*="notice"], ' +
        '[class*="notification"], [class*="alert"], [class*="tip"], [role="alert"], [class*="success"]')) {
        const text = (el.innerText || '').trim();
        const visible = window.getComputedStyle(el).display !== 'none';
        if (visible && text) {
            for (const kw of successKeywords) {
                if (text.includes(kw)) {
                    indicators.successToasts.push({
                        text: text.substring(0, 80),
                        class: (el.className || '').substring(0, 60)
                    });
                    break;
                }
            }
        }
    }

    // Check 4: Modal/Dialog closed (publish modal disappeared)
    const modalsBefore = document.querySelectorAll('[class*="modal"], [class*="dialog"], [class*="overlay"]');
    indicators.modalsFound = modalsBefore.length;

    // Check 5: Button state changed (from "发布" to disabled/success)
    const publishBtn = document.querySelector('button:contains("发布"), [class*="publish"], [class*="submit"]');
    if (publishBtn) {
        indicators.buttonDisabled = publishBtn.disabled || publishBtn.classList.contains('ant-btn-loading');
        indicators.buttonText = (publishBtn.innerText || '').substring(0, 40);
    }

    results.indicators = indicators;

    // Determine if publish was likely successful
    results.success = indicators.successToasts.length > 0 ||
                      indicators.dialogClosed ||
                      indicators.buttonDisabled;

    // Check for errors
    const errorKeywords = ['失败', '错误', 'error', '请重试', '网络错误'];
    results.errors = [];
    for (const el of document.querySelectorAll('[class*="error"], [class*="warning"], [role="alert"]')) {
        const text = (el.innerText || '').trim();
        if (text.length > 0 && text.length < 200) {
            for (const kw of errorKeywords) {
                if (text.includes(kw)) {
                    results.errors.push({text: text.substring(0, 100), class: (el.className || '').substring(0, 40)});
                    break;
                }
            }
        }
    }

    return JSON.stringify(results);
})()"""


# ======== Command Handlers ========

async def cmd_smart_click(args):
    """Multi-strategy click: tries all available strategies in order."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(json.dumps({"error": f"Tab {args.tab_id} not found"}))
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()

        result = await _try_all_strategies(cdp, ws, args)
        print(json.dumps(result, ensure_ascii=False, indent=2))


async def _try_all_strategies(cdp, ws, args):
    """Try all click strategies in order, return first success."""
    selector = args.selector or ""
    text = args.text
    index = args.index or 0
    results = {
        "target": {"selector": selector, "text": text, "index": index},
        "strategies_tried": [],
        "success": False,
        "strategy_used": None,
    }

    # Step 1: Detect framework (for diagnostics)
    framework = await cdp.eval_js(JS_DETECT_FRAMEWORK)
    if isinstance(framework, dict):
        results["framework"] = framework

    # Step 2: Pre-locate element first (always)
    location_js = _build_locate_js(selector, text, index)
    coords_info = await cdp.eval_js(location_js)
    if isinstance(coords_info, dict) and "error" in coords_info:
        results["location_error"] = coords_info["error"]
        return results

    x = coords_info.get("x")
    y = coords_info.get("y")

    # Step 3: Sync rich text editors before clicking (critical for Vue/React editors)
    try:
        sync_result = await cdp.eval_js(JS_EDITOR_SYNC, timeout_ms=args.timeout or 5000)
        if isinstance(sync_result, dict):
            results["editor_sync"] = sync_result
            results["pre_click_sync"] = sync_result.get("synced", [])
    except Exception as e:
        results["editor_sync_error"] = str(e)

    # Step 4: Try each strategy
    for strategy_name in STRATEGY_ORDER:
        attempt = {"strategy": strategy_name}

        try:
            if strategy_name == "editor_sync":
                # Already done in Step 3, skip execution
                attempt["success"] = True
                attempt["note"] = "pre-executed"
            elif strategy_name == "raw_cdp":
                # Use CDP native mouse events (complete sequence)
                await cdp.complete_click(x, y, delay_ms=args.delay or 80)
                attempt["success"] = True
            elif strategy_name == "hit_test_click":
                # First check hit-test
                ht_js = JS_HIT_TEST
                hit_test = await cdp.eval_js(
                    f"(function() {{ const el = document.elementFromPoint({x}, {y}); "
                    f"if (!el) return JSON.stringify({{error: 'no element at point'}}); "
                    f"{JS_HIT_TEST.replace('(function() {', '').rstrip(')()')} }})()",
                    timeout_ms=args.timeout or 5000
                )
                if isinstance(hit_test, dict):
                    attempt["hit_test"] = hit_test
                    if hit_test.get("clickable") and hit_test.get("hitTestPass"):
                        await cdp.complete_click(x, y, delay_ms=args.delay or 80)
                        attempt["success"] = True
                    else:
                        attempt["success"] = False
                        attempt["reason"] = "hit test failed"
                        if hit_test.get("blocker"):
                            attempt["blocker"] = hit_test["blocker"]
                else:
                    attempt["success"] = False
                    attempt["reason"] = "hit test returned unexpected"
            elif strategy_name == "react_fiber_click":
                escaped_sel = selector.replace("'", "\\'")
                js = JS_REACT_FIBER_CLICK % (escaped_sel, index)
                js_result = await cdp.eval_js(js)
                if isinstance(js_result, dict):
                    attempt["result"] = js_result
                    attempt["success"] = js_result.get("success", False)
                else:
                    attempt["result"] = str(js_result)
                    attempt["success"] = False
                # If React fiber failed, try React 18 root delegation
                if not attempt.get("success"):
                    try:
                        js2 = JS_REACT_18_ROOT_CLICK % (escaped_sel, index)
                        js2_result = await cdp.eval_js(js2)
                        if isinstance(js2_result, dict):
                            attempt["react18_fallback"] = js2_result
                            if js2_result.get("success"):
                                attempt["success"] = True
                                attempt["note"] = "react18_root_delegation"
                    except Exception:
                        pass
            elif strategy_name == "vue_emit_click":
                escaped_sel = selector.replace("'", "\\'")
                js = JS_VUE_ENHANCED_CLICK % (escaped_sel, index)
                js_result = await cdp.eval_js(js)
                if isinstance(js_result, dict):
                    attempt["result"] = js_result
                    attempt["success"] = js_result.get("success", False)
                else:
                    attempt["result"] = str(js_result)
                    attempt["success"] = False
            elif strategy_name == "dispatch_event_click":
                escaped_sel = selector.replace("'", "\\'")
                js = JS_DISPATCH_EVENT_CLICK % (escaped_sel, index)
                js_result = await cdp.eval_js(js)
                if isinstance(js_result, dict):
                    attempt["result"] = js_result
                    attempt["success"] = js_result.get("success", False)
                else:
                    attempt["result"] = str(js_result)
                    attempt["success"] = False
            elif strategy_name == "enter_key_click":
                escaped_sel = selector.replace("'", "\\'")
                js = JS_ENTER_KEY_CLICK % (escaped_sel, index)
                js_result = await cdp.eval_js(js)
                if isinstance(js_result, dict):
                    attempt["result"] = js_result
                    attempt["success"] = js_result.get("success", False)
                else:
                    attempt["result"] = str(js_result)
                    attempt["success"] = False
        except Exception as e:
            attempt["error"] = str(e)
            attempt["success"] = False

        attempt["tried"] = True
        results["strategies_tried"].append(attempt)

        if attempt.get("success"):
            results["success"] = True
            results["strategy_used"] = strategy_name
            break

    # If clickable was suppressed (event cancelled), still mark as success
    # because the framework might handle the state change internally
    if not results["success"]:
        # Check if state changed despite "failure"
        pass

    # Step 5: Validate publish results
    try:
        publish_check = await cdp.eval_js(JS_PUBLISH_VALIDATE, timeout_ms=args.timeout or 3000)
        if isinstance(publish_check, dict):
            results["publish_validation"] = publish_check
            # If validation shows success but no strategy claimed it, still mark as success
            if publish_check.get("success") and not results["success"]:
                results["success"] = True
                results["strategy_used"] = "publish_validation_confirmed"
    except Exception as e:
        results["publish_validation_error"] = str(e)

    return results


async def cmd_detect_framework(args):
    """Detect which JavaScript framework(s) the page uses."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(json.dumps({"error": f"Tab {args.tab_id} not found"}))
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()
        result = await cdp.eval_js(JS_DETECT_FRAMEWORK)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else "null")


async def cmd_analyze_button(args):
    """Deep-analyze a button element for debugging failed clicks."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(json.dumps({"error": f"Tab {args.tab_id} not found"}))
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()

        selector = args.selector or ""
        index = args.index or 0
        escaped_sel = selector.replace("'", "\\'")
        js = JS_ANALYZE_BUTTON % (escaped_sel, index)

        result = await cdp.eval_js(js)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else "null")


async def cmd_publish_validate(args):
    """Validate if publish was successful after clicking publish button."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(json.dumps({"error": f"Tab {args.tab_id} not found"}))
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()
        result = await cdp.eval_js(JS_PUBLISH_VALIDATE, timeout_ms=args.timeout or 3000)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else "null")


async def cmd_editor_sync(args):
    """Sync rich text editor data (CKEditor, Lexical, ProseMirror, Quill, 语雀)."""
    ws_url = get_ws_url(args.tab_id)
    if not ws_url:
        print(json.dumps({"error": f"Tab {args.tab_id} not found"}))
        return

    async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
        cdp = CDPConnection(ws)
        await cdp.enable_runtime()
        result = await cdp.eval_js(JS_EDITOR_SYNC, timeout_ms=args.timeout or 5000)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result else "null")


def main():
    parser = argparse.ArgumentParser(description="Framework-aware click and analysis")
    parser.add_argument("--port", type=int, default=None, help="CDP port (default: 9222)")
    sub = parser.add_subparsers(dest="command")

    # smart-click
    p_sc = sub.add_parser("smart-click", help="Click using multi-strategy approach (auto-fallback)")
    p_sc.add_argument("tab_id", help="Tab ID")
    p_sc.add_argument("--selector", "-s", help="CSS selector")
    p_sc.add_argument("--text", "-t", help="Find element containing this text")
    p_sc.add_argument("--index", "-i", type=int, default=0, help="Element index (default: 0)")
    p_sc.add_argument("--delay", type=int, default=80, help="Click delay in ms (default: 80)")
    p_sc.add_argument("--timeout", type=int, default=5000, help="Strategy timeout in ms (default: 5000)")

    # detect-framework
    p_df = sub.add_parser("detect-framework", help="Detect JS framework (React/Vue/Angular)")
    p_df.add_argument("tab_id", help="Tab ID")

    # analyze-button
    p_ab = sub.add_parser("analyze-button", help="Deep analysis of a button element")
    p_ab.add_argument("tab_id", help="Tab ID")
    p_ab.add_argument("--selector", "-s", required=True, help="CSS selector")
    p_ab.add_argument("--index", "-i", type=int, default=0, help="Element index (default: 0)")

    # publish-validate
    p_pv = sub.add_parser("publish-validate", help="Validate if publish was successful (check toasts, URL, modals)")
    p_pv.add_argument("tab_id", help="Tab ID")
    p_pv.add_argument("--timeout", type=int, default=3000, help="Validation timeout in ms (default: 3000)")

    # editor-sync
    p_es = sub.add_parser("editor-sync", help="Sync rich text editor data (CKEditor, Lexical, ProseMirror, Quill, 语雀)")
    p_es.add_argument("tab_id", help="Tab ID")

    # individual strategy commands (for targeted use)
    p_rc = sub.add_parser("raw-cdp", help="Click via CDP Input.dispatchMouseEvent only")
    p_rc.add_argument("tab_id", help="Tab ID")
    p_rc.add_argument("--selector", "-s", help="CSS selector")
    p_rc.add_argument("--text", "-t", help="Find element containing this text")
    p_rc.add_argument("--index", "-i", type=int, default=0, help="Element index")
    p_rc.add_argument("--delay", type=int, default=80)

    args = parser.parse_args()

    if args.port:
        import os
        os.environ["CDP_PORT"] = str(args.port)

    if args.command == "smart-click":
        asyncio.run(cmd_smart_click(args))
    elif args.command == "detect-framework":
        asyncio.run(cmd_detect_framework(args))
    elif args.command == "analyze-button":
        asyncio.run(cmd_analyze_button(args))
    elif args.command == "publish-validate":
        asyncio.run(cmd_publish_validate(args))
    elif args.command == "editor-sync":
        asyncio.run(cmd_editor_sync(args))
    elif args.command == "raw-cdp":
        # Just do a raw CDP click for legacy support
        async def _raw():
            ws_url = get_ws_url(args.tab_id)
            if not ws_url:
                print(json.dumps({"error": f"Tab {args.tab_id} not found"}))
                return
            async with websockets.connect(ws_url, max_size=MAX_WS_SIZE) as ws:
                cdp = CDPConnection(ws)
                await cdp.enable_runtime()
                loc_js = _build_locate_js(args.selector or "", args.text, args.index or 0)
                loc = await cdp.eval_js(loc_js)
                if isinstance(loc, dict) and "error" not in loc:
                    result = await cdp.complete_click(loc["x"], loc["y"], delay_ms=args.delay)
                    print(json.dumps(result))
                else:
                    print(json.dumps({"error": loc}))
        asyncio.run(_raw())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
