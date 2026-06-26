#!/usr/bin/env bun
// @bun
var __create = Object.create;
var __getProtoOf = Object.getPrototypeOf;
var __defProp = Object.defineProperty;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __toESM = (mod, isNodeMode, target) => {
  target = mod != null ? __create(__getProtoOf(mod)) : {};
  const to = isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target;
  for (let key of __getOwnPropNames(mod))
    if (!__hasOwnProp.call(to, key))
      __defProp(to, key, {
        get: () => mod[key],
        enumerable: true
      });
  return to;
};
var __moduleCache = /* @__PURE__ */ new WeakMap;
var __toCommonJS = (from) => {
  var entry = __moduleCache.get(from), desc;
  if (entry)
    return entry;
  entry = __defProp({}, "__esModule", { value: true });
  if (from && typeof from === "object" || typeof from === "function")
    __getOwnPropNames(from).map((key) => !__hasOwnProp.call(entry, key) && __defProp(entry, key, {
      get: () => from[key],
      enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable
    }));
  __moduleCache.set(from, entry);
  return entry;
};
var __commonJS = (cb, mod) => () => (mod || cb((mod = { exports: {} }).exports, mod), mod.exports);
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, {
      get: all[name],
      enumerable: true,
      configurable: true,
      set: (newValue) => all[name] = () => newValue
    });
};
var __esm = (fn, res) => () => (fn && (res = fn(fn = 0)), res);

// node_modules/cross-fetch/dist/browser-ponyfill.js
var require_browser_ponyfill = __commonJS((exports, module) => {
  var __global__ = typeof globalThis !== "undefined" && globalThis || typeof self !== "undefined" && self || typeof global !== "undefined" && global;
  var __globalThis__ = function() {
    function F() {
      this.fetch = false;
      this.DOMException = __global__.DOMException;
    }
    F.prototype = __global__;
    return new F;
  }();
  (function(globalThis2) {
    var irrelevant = function(exports2) {
      var g = typeof globalThis2 !== "undefined" && globalThis2 || typeof self !== "undefined" && self || typeof global !== "undefined" && global || {};
      var support = {
        searchParams: "URLSearchParams" in g,
        iterable: "Symbol" in g && "iterator" in Symbol,
        blob: "FileReader" in g && "Blob" in g && function() {
          try {
            new Blob;
            return true;
          } catch (e) {
            return false;
          }
        }(),
        formData: "FormData" in g,
        arrayBuffer: "ArrayBuffer" in g
      };
      function isDataView(obj) {
        return obj && DataView.prototype.isPrototypeOf(obj);
      }
      if (support.arrayBuffer) {
        var viewClasses = [
          "[object Int8Array]",
          "[object Uint8Array]",
          "[object Uint8ClampedArray]",
          "[object Int16Array]",
          "[object Uint16Array]",
          "[object Int32Array]",
          "[object Uint32Array]",
          "[object Float32Array]",
          "[object Float64Array]"
        ];
        var isArrayBufferView = ArrayBuffer.isView || function(obj) {
          return obj && viewClasses.indexOf(Object.prototype.toString.call(obj)) > -1;
        };
      }
      function normalizeName(name) {
        if (typeof name !== "string") {
          name = String(name);
        }
        if (/[^a-z0-9\-#$%&'*+.^_`|~!]/i.test(name) || name === "") {
          throw new TypeError('Invalid character in header field name: "' + name + '"');
        }
        return name.toLowerCase();
      }
      function normalizeValue(value) {
        if (typeof value !== "string") {
          value = String(value);
        }
        return value;
      }
      function iteratorFor(items) {
        var iterator = {
          next: function() {
            var value = items.shift();
            return { done: value === undefined, value };
          }
        };
        if (support.iterable) {
          iterator[Symbol.iterator] = function() {
            return iterator;
          };
        }
        return iterator;
      }
      function Headers(headers) {
        this.map = {};
        if (headers instanceof Headers) {
          headers.forEach(function(value, name) {
            this.append(name, value);
          }, this);
        } else if (Array.isArray(headers)) {
          headers.forEach(function(header) {
            if (header.length != 2) {
              throw new TypeError("Headers constructor: expected name/value pair to be length 2, found" + header.length);
            }
            this.append(header[0], header[1]);
          }, this);
        } else if (headers) {
          Object.getOwnPropertyNames(headers).forEach(function(name) {
            this.append(name, headers[name]);
          }, this);
        }
      }
      Headers.prototype.append = function(name, value) {
        name = normalizeName(name);
        value = normalizeValue(value);
        var oldValue = this.map[name];
        this.map[name] = oldValue ? oldValue + ", " + value : value;
      };
      Headers.prototype["delete"] = function(name) {
        delete this.map[normalizeName(name)];
      };
      Headers.prototype.get = function(name) {
        name = normalizeName(name);
        return this.has(name) ? this.map[name] : null;
      };
      Headers.prototype.has = function(name) {
        return this.map.hasOwnProperty(normalizeName(name));
      };
      Headers.prototype.set = function(name, value) {
        this.map[normalizeName(name)] = normalizeValue(value);
      };
      Headers.prototype.forEach = function(callback, thisArg) {
        for (var name in this.map) {
          if (this.map.hasOwnProperty(name)) {
            callback.call(thisArg, this.map[name], name, this);
          }
        }
      };
      Headers.prototype.keys = function() {
        var items = [];
        this.forEach(function(value, name) {
          items.push(name);
        });
        return iteratorFor(items);
      };
      Headers.prototype.values = function() {
        var items = [];
        this.forEach(function(value) {
          items.push(value);
        });
        return iteratorFor(items);
      };
      Headers.prototype.entries = function() {
        var items = [];
        this.forEach(function(value, name) {
          items.push([name, value]);
        });
        return iteratorFor(items);
      };
      if (support.iterable) {
        Headers.prototype[Symbol.iterator] = Headers.prototype.entries;
      }
      function consumed(body) {
        if (body._noBody)
          return;
        if (body.bodyUsed) {
          return Promise.reject(new TypeError("Already read"));
        }
        body.bodyUsed = true;
      }
      function fileReaderReady(reader) {
        return new Promise(function(resolve, reject) {
          reader.onload = function() {
            resolve(reader.result);
          };
          reader.onerror = function() {
            reject(reader.error);
          };
        });
      }
      function readBlobAsArrayBuffer(blob) {
        var reader = new FileReader;
        var promise = fileReaderReady(reader);
        reader.readAsArrayBuffer(blob);
        return promise;
      }
      function readBlobAsText(blob) {
        var reader = new FileReader;
        var promise = fileReaderReady(reader);
        var match = /charset=([A-Za-z0-9_-]+)/.exec(blob.type);
        var encoding = match ? match[1] : "utf-8";
        reader.readAsText(blob, encoding);
        return promise;
      }
      function readArrayBufferAsText(buf) {
        var view = new Uint8Array(buf);
        var chars = new Array(view.length);
        for (var i = 0;i < view.length; i++) {
          chars[i] = String.fromCharCode(view[i]);
        }
        return chars.join("");
      }
      function bufferClone(buf) {
        if (buf.slice) {
          return buf.slice(0);
        } else {
          var view = new Uint8Array(buf.byteLength);
          view.set(new Uint8Array(buf));
          return view.buffer;
        }
      }
      function Body() {
        this.bodyUsed = false;
        this._initBody = function(body) {
          this.bodyUsed = this.bodyUsed;
          this._bodyInit = body;
          if (!body) {
            this._noBody = true;
            this._bodyText = "";
          } else if (typeof body === "string") {
            this._bodyText = body;
          } else if (support.blob && Blob.prototype.isPrototypeOf(body)) {
            this._bodyBlob = body;
          } else if (support.formData && FormData.prototype.isPrototypeOf(body)) {
            this._bodyFormData = body;
          } else if (support.searchParams && URLSearchParams.prototype.isPrototypeOf(body)) {
            this._bodyText = body.toString();
          } else if (support.arrayBuffer && support.blob && isDataView(body)) {
            this._bodyArrayBuffer = bufferClone(body.buffer);
            this._bodyInit = new Blob([this._bodyArrayBuffer]);
          } else if (support.arrayBuffer && (ArrayBuffer.prototype.isPrototypeOf(body) || isArrayBufferView(body))) {
            this._bodyArrayBuffer = bufferClone(body);
          } else {
            this._bodyText = body = Object.prototype.toString.call(body);
          }
          if (!this.headers.get("content-type")) {
            if (typeof body === "string") {
              this.headers.set("content-type", "text/plain;charset=UTF-8");
            } else if (this._bodyBlob && this._bodyBlob.type) {
              this.headers.set("content-type", this._bodyBlob.type);
            } else if (support.searchParams && URLSearchParams.prototype.isPrototypeOf(body)) {
              this.headers.set("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
            }
          }
        };
        if (support.blob) {
          this.blob = function() {
            var rejected = consumed(this);
            if (rejected) {
              return rejected;
            }
            if (this._bodyBlob) {
              return Promise.resolve(this._bodyBlob);
            } else if (this._bodyArrayBuffer) {
              return Promise.resolve(new Blob([this._bodyArrayBuffer]));
            } else if (this._bodyFormData) {
              throw new Error("could not read FormData body as blob");
            } else {
              return Promise.resolve(new Blob([this._bodyText]));
            }
          };
        }
        this.arrayBuffer = function() {
          if (this._bodyArrayBuffer) {
            var isConsumed = consumed(this);
            if (isConsumed) {
              return isConsumed;
            } else if (ArrayBuffer.isView(this._bodyArrayBuffer)) {
              return Promise.resolve(this._bodyArrayBuffer.buffer.slice(this._bodyArrayBuffer.byteOffset, this._bodyArrayBuffer.byteOffset + this._bodyArrayBuffer.byteLength));
            } else {
              return Promise.resolve(this._bodyArrayBuffer);
            }
          } else if (support.blob) {
            return this.blob().then(readBlobAsArrayBuffer);
          } else {
            throw new Error("could not read as ArrayBuffer");
          }
        };
        this.text = function() {
          var rejected = consumed(this);
          if (rejected) {
            return rejected;
          }
          if (this._bodyBlob) {
            return readBlobAsText(this._bodyBlob);
          } else if (this._bodyArrayBuffer) {
            return Promise.resolve(readArrayBufferAsText(this._bodyArrayBuffer));
          } else if (this._bodyFormData) {
            throw new Error("could not read FormData body as text");
          } else {
            return Promise.resolve(this._bodyText);
          }
        };
        if (support.formData) {
          this.formData = function() {
            return this.text().then(decode);
          };
        }
        this.json = function() {
          return this.text().then(JSON.parse);
        };
        return this;
      }
      var methods = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"];
      function normalizeMethod(method) {
        var upcased = method.toUpperCase();
        return methods.indexOf(upcased) > -1 ? upcased : method;
      }
      function Request(input, options) {
        if (!(this instanceof Request)) {
          throw new TypeError('Please use the "new" operator, this DOM object constructor cannot be called as a function.');
        }
        options = options || {};
        var body = options.body;
        if (input instanceof Request) {
          if (input.bodyUsed) {
            throw new TypeError("Already read");
          }
          this.url = input.url;
          this.credentials = input.credentials;
          if (!options.headers) {
            this.headers = new Headers(input.headers);
          }
          this.method = input.method;
          this.mode = input.mode;
          this.signal = input.signal;
          if (!body && input._bodyInit != null) {
            body = input._bodyInit;
            input.bodyUsed = true;
          }
        } else {
          this.url = String(input);
        }
        this.credentials = options.credentials || this.credentials || "same-origin";
        if (options.headers || !this.headers) {
          this.headers = new Headers(options.headers);
        }
        this.method = normalizeMethod(options.method || this.method || "GET");
        this.mode = options.mode || this.mode || null;
        this.signal = options.signal || this.signal || function() {
          if ("AbortController" in g) {
            var ctrl = new AbortController;
            return ctrl.signal;
          }
        }();
        this.referrer = null;
        if ((this.method === "GET" || this.method === "HEAD") && body) {
          throw new TypeError("Body not allowed for GET or HEAD requests");
        }
        this._initBody(body);
        if (this.method === "GET" || this.method === "HEAD") {
          if (options.cache === "no-store" || options.cache === "no-cache") {
            var reParamSearch = /([?&])_=[^&]*/;
            if (reParamSearch.test(this.url)) {
              this.url = this.url.replace(reParamSearch, "$1_=" + new Date().getTime());
            } else {
              var reQueryString = /\?/;
              this.url += (reQueryString.test(this.url) ? "&" : "?") + "_=" + new Date().getTime();
            }
          }
        }
      }
      Request.prototype.clone = function() {
        return new Request(this, { body: this._bodyInit });
      };
      function decode(body) {
        var form = new FormData;
        body.trim().split("&").forEach(function(bytes) {
          if (bytes) {
            var split = bytes.split("=");
            var name = split.shift().replace(/\+/g, " ");
            var value = split.join("=").replace(/\+/g, " ");
            form.append(decodeURIComponent(name), decodeURIComponent(value));
          }
        });
        return form;
      }
      function parseHeaders(rawHeaders) {
        var headers = new Headers;
        var preProcessedHeaders = rawHeaders.replace(/\r?\n[\t ]+/g, " ");
        preProcessedHeaders.split("\r").map(function(header) {
          return header.indexOf(`
`) === 0 ? header.substr(1, header.length) : header;
        }).forEach(function(line) {
          var parts = line.split(":");
          var key = parts.shift().trim();
          if (key) {
            var value = parts.join(":").trim();
            try {
              headers.append(key, value);
            } catch (error) {
              console.warn("Response " + error.message);
            }
          }
        });
        return headers;
      }
      Body.call(Request.prototype);
      function Response(bodyInit, options) {
        if (!(this instanceof Response)) {
          throw new TypeError('Please use the "new" operator, this DOM object constructor cannot be called as a function.');
        }
        if (!options) {
          options = {};
        }
        this.type = "default";
        this.status = options.status === undefined ? 200 : options.status;
        if (this.status < 200 || this.status > 599) {
          throw new RangeError("Failed to construct 'Response': The status provided (0) is outside the range [200, 599].");
        }
        this.ok = this.status >= 200 && this.status < 300;
        this.statusText = options.statusText === undefined ? "" : "" + options.statusText;
        this.headers = new Headers(options.headers);
        this.url = options.url || "";
        this._initBody(bodyInit);
      }
      Body.call(Response.prototype);
      Response.prototype.clone = function() {
        return new Response(this._bodyInit, {
          status: this.status,
          statusText: this.statusText,
          headers: new Headers(this.headers),
          url: this.url
        });
      };
      Response.error = function() {
        var response = new Response(null, { status: 200, statusText: "" });
        response.ok = false;
        response.status = 0;
        response.type = "error";
        return response;
      };
      var redirectStatuses = [301, 302, 303, 307, 308];
      Response.redirect = function(url, status) {
        if (redirectStatuses.indexOf(status) === -1) {
          throw new RangeError("Invalid status code");
        }
        return new Response(null, { status, headers: { location: url } });
      };
      exports2.DOMException = g.DOMException;
      try {
        new exports2.DOMException;
      } catch (err) {
        exports2.DOMException = function(message, name) {
          this.message = message;
          this.name = name;
          var error = Error(message);
          this.stack = error.stack;
        };
        exports2.DOMException.prototype = Object.create(Error.prototype);
        exports2.DOMException.prototype.constructor = exports2.DOMException;
      }
      function fetch2(input, init) {
        return new Promise(function(resolve, reject) {
          var request = new Request(input, init);
          if (request.signal && request.signal.aborted) {
            return reject(new exports2.DOMException("Aborted", "AbortError"));
          }
          var xhr = new XMLHttpRequest;
          function abortXhr() {
            xhr.abort();
          }
          xhr.onload = function() {
            var options = {
              statusText: xhr.statusText,
              headers: parseHeaders(xhr.getAllResponseHeaders() || "")
            };
            if (request.url.indexOf("file://") === 0 && (xhr.status < 200 || xhr.status > 599)) {
              options.status = 200;
            } else {
              options.status = xhr.status;
            }
            options.url = "responseURL" in xhr ? xhr.responseURL : options.headers.get("X-Request-URL");
            var body = "response" in xhr ? xhr.response : xhr.responseText;
            setTimeout(function() {
              resolve(new Response(body, options));
            }, 0);
          };
          xhr.onerror = function() {
            setTimeout(function() {
              reject(new TypeError("Network request failed"));
            }, 0);
          };
          xhr.ontimeout = function() {
            setTimeout(function() {
              reject(new TypeError("Network request timed out"));
            }, 0);
          };
          xhr.onabort = function() {
            setTimeout(function() {
              reject(new exports2.DOMException("Aborted", "AbortError"));
            }, 0);
          };
          function fixUrl(url) {
            try {
              return url === "" && g.location.href ? g.location.href : url;
            } catch (e) {
              return url;
            }
          }
          xhr.open(request.method, fixUrl(request.url), true);
          if (request.credentials === "include") {
            xhr.withCredentials = true;
          } else if (request.credentials === "omit") {
            xhr.withCredentials = false;
          }
          if ("responseType" in xhr) {
            if (support.blob) {
              xhr.responseType = "blob";
            } else if (support.arrayBuffer) {
              xhr.responseType = "arraybuffer";
            }
          }
          if (init && typeof init.headers === "object" && !(init.headers instanceof Headers || g.Headers && init.headers instanceof g.Headers)) {
            var names = [];
            Object.getOwnPropertyNames(init.headers).forEach(function(name) {
              names.push(normalizeName(name));
              xhr.setRequestHeader(name, normalizeValue(init.headers[name]));
            });
            request.headers.forEach(function(value, name) {
              if (names.indexOf(name) === -1) {
                xhr.setRequestHeader(name, value);
              }
            });
          } else {
            request.headers.forEach(function(value, name) {
              xhr.setRequestHeader(name, value);
            });
          }
          if (request.signal) {
            request.signal.addEventListener("abort", abortXhr);
            xhr.onreadystatechange = function() {
              if (xhr.readyState === 4) {
                request.signal.removeEventListener("abort", abortXhr);
              }
            };
          }
          xhr.send(typeof request._bodyInit === "undefined" ? null : request._bodyInit);
        });
      }
      fetch2.polyfill = true;
      if (!g.fetch) {
        g.fetch = fetch2;
        g.Headers = Headers;
        g.Request = Request;
        g.Response = Response;
      }
      exports2.Headers = Headers;
      exports2.Request = Request;
      exports2.Response = Response;
      exports2.fetch = fetch2;
      return exports2;
    }({});
  })(__globalThis__);
  __globalThis__.fetch.ponyfill = true;
  delete __globalThis__.fetch.polyfill;
  var ctx = __global__.fetch ? __global__ : __globalThis__;
  exports = ctx.fetch;
  exports.default = ctx.fetch;
  exports.fetch = ctx.fetch;
  exports.Headers = ctx.Headers;
  exports.Request = ctx.Request;
  exports.Response = ctx.Response;
  module.exports = exports;
});

// node_modules/ms/index.js
var require_ms = __commonJS((exports, module) => {
  var s = 1000;
  var m = s * 60;
  var h = m * 60;
  var d = h * 24;
  var w = d * 7;
  var y = d * 365.25;
  module.exports = function(val, options) {
    options = options || {};
    var type = typeof val;
    if (type === "string" && val.length > 0) {
      return parse(val);
    } else if (type === "number" && isFinite(val)) {
      return options.long ? fmtLong(val) : fmtShort(val);
    }
    throw new Error("val is not a non-empty string or a valid number. val=" + JSON.stringify(val));
  };
  function parse(str) {
    str = String(str);
    if (str.length > 100) {
      return;
    }
    var match = /^(-?(?:\d+)?\.?\d+) *(milliseconds?|msecs?|ms|seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h|days?|d|weeks?|w|years?|yrs?|y)?$/i.exec(str);
    if (!match) {
      return;
    }
    var n = parseFloat(match[1]);
    var type = (match[2] || "ms").toLowerCase();
    switch (type) {
      case "years":
      case "year":
      case "yrs":
      case "yr":
      case "y":
        return n * y;
      case "weeks":
      case "week":
      case "w":
        return n * w;
      case "days":
      case "day":
      case "d":
        return n * d;
      case "hours":
      case "hour":
      case "hrs":
      case "hr":
      case "h":
        return n * h;
      case "minutes":
      case "minute":
      case "mins":
      case "min":
      case "m":
        return n * m;
      case "seconds":
      case "second":
      case "secs":
      case "sec":
      case "s":
        return n * s;
      case "milliseconds":
      case "millisecond":
      case "msecs":
      case "msec":
      case "ms":
        return n;
      default:
        return;
    }
  }
  function fmtShort(ms) {
    var msAbs = Math.abs(ms);
    if (msAbs >= d) {
      return Math.round(ms / d) + "d";
    }
    if (msAbs >= h) {
      return Math.round(ms / h) + "h";
    }
    if (msAbs >= m) {
      return Math.round(ms / m) + "m";
    }
    if (msAbs >= s) {
      return Math.round(ms / s) + "s";
    }
    return ms + "ms";
  }
  function fmtLong(ms) {
    var msAbs = Math.abs(ms);
    if (msAbs >= d) {
      return plural(ms, msAbs, d, "day");
    }
    if (msAbs >= h) {
      return plural(ms, msAbs, h, "hour");
    }
    if (msAbs >= m) {
      return plural(ms, msAbs, m, "minute");
    }
    if (msAbs >= s) {
      return plural(ms, msAbs, s, "second");
    }
    return ms + " ms";
  }
  function plural(ms, msAbs, n, name) {
    var isPlural = msAbs >= n * 1.5;
    return Math.round(ms / n) + " " + name + (isPlural ? "s" : "");
  }
});

// node_modules/debug/src/common.js
var require_common = __commonJS((exports, module) => {
  function setup(env) {
    createDebug.debug = createDebug;
    createDebug.default = createDebug;
    createDebug.coerce = coerce;
    createDebug.disable = disable;
    createDebug.enable = enable;
    createDebug.enabled = enabled;
    createDebug.humanize = require_ms();
    createDebug.destroy = destroy;
    Object.keys(env).forEach((key) => {
      createDebug[key] = env[key];
    });
    createDebug.names = [];
    createDebug.skips = [];
    createDebug.formatters = {};
    function selectColor(namespace) {
      let hash = 0;
      for (let i = 0;i < namespace.length; i++) {
        hash = (hash << 5) - hash + namespace.charCodeAt(i);
        hash |= 0;
      }
      return createDebug.colors[Math.abs(hash) % createDebug.colors.length];
    }
    createDebug.selectColor = selectColor;
    function createDebug(namespace) {
      let prevTime;
      let enableOverride = null;
      let namespacesCache;
      let enabledCache;
      function debug(...args) {
        if (!debug.enabled) {
          return;
        }
        const self2 = debug;
        const curr = Number(new Date);
        const ms = curr - (prevTime || curr);
        self2.diff = ms;
        self2.prev = prevTime;
        self2.curr = curr;
        prevTime = curr;
        args[0] = createDebug.coerce(args[0]);
        if (typeof args[0] !== "string") {
          args.unshift("%O");
        }
        let index = 0;
        args[0] = args[0].replace(/%([a-zA-Z%])/g, (match, format) => {
          if (match === "%%") {
            return "%";
          }
          index++;
          const formatter = createDebug.formatters[format];
          if (typeof formatter === "function") {
            const val = args[index];
            match = formatter.call(self2, val);
            args.splice(index, 1);
            index--;
          }
          return match;
        });
        createDebug.formatArgs.call(self2, args);
        const logFn = self2.log || createDebug.log;
        logFn.apply(self2, args);
      }
      debug.namespace = namespace;
      debug.useColors = createDebug.useColors();
      debug.color = createDebug.selectColor(namespace);
      debug.extend = extend;
      debug.destroy = createDebug.destroy;
      Object.defineProperty(debug, "enabled", {
        enumerable: true,
        configurable: false,
        get: () => {
          if (enableOverride !== null) {
            return enableOverride;
          }
          if (namespacesCache !== createDebug.namespaces) {
            namespacesCache = createDebug.namespaces;
            enabledCache = createDebug.enabled(namespace);
          }
          return enabledCache;
        },
        set: (v) => {
          enableOverride = v;
        }
      });
      if (typeof createDebug.init === "function") {
        createDebug.init(debug);
      }
      return debug;
    }
    function extend(namespace, delimiter) {
      const newDebug = createDebug(this.namespace + (typeof delimiter === "undefined" ? ":" : delimiter) + namespace);
      newDebug.log = this.log;
      return newDebug;
    }
    function enable(namespaces) {
      createDebug.save(namespaces);
      createDebug.namespaces = namespaces;
      createDebug.names = [];
      createDebug.skips = [];
      const split = (typeof namespaces === "string" ? namespaces : "").trim().replace(/\s+/g, ",").split(",").filter(Boolean);
      for (const ns of split) {
        if (ns[0] === "-") {
          createDebug.skips.push(ns.slice(1));
        } else {
          createDebug.names.push(ns);
        }
      }
    }
    function matchesTemplate(search, template) {
      let searchIndex = 0;
      let templateIndex = 0;
      let starIndex = -1;
      let matchIndex = 0;
      while (searchIndex < search.length) {
        if (templateIndex < template.length && (template[templateIndex] === search[searchIndex] || template[templateIndex] === "*")) {
          if (template[templateIndex] === "*") {
            starIndex = templateIndex;
            matchIndex = searchIndex;
            templateIndex++;
          } else {
            searchIndex++;
            templateIndex++;
          }
        } else if (starIndex !== -1) {
          templateIndex = starIndex + 1;
          matchIndex++;
          searchIndex = matchIndex;
        } else {
          return false;
        }
      }
      while (templateIndex < template.length && template[templateIndex] === "*") {
        templateIndex++;
      }
      return templateIndex === template.length;
    }
    function disable() {
      const namespaces = [
        ...createDebug.names,
        ...createDebug.skips.map((namespace) => "-" + namespace)
      ].join(",");
      createDebug.enable("");
      return namespaces;
    }
    function enabled(name) {
      for (const skip of createDebug.skips) {
        if (matchesTemplate(name, skip)) {
          return false;
        }
      }
      for (const ns of createDebug.names) {
        if (matchesTemplate(name, ns)) {
          return true;
        }
      }
      return false;
    }
    function coerce(val) {
      if (val instanceof Error) {
        return val.stack || val.message;
      }
      return val;
    }
    function destroy() {
      console.warn("Instance method `debug.destroy()` is deprecated and no longer does anything. It will be removed in the next major version of `debug`.");
    }
    createDebug.enable(createDebug.load());
    return createDebug;
  }
  module.exports = setup;
});

// node_modules/debug/src/browser.js
var require_browser = __commonJS((exports, module) => {
  exports.formatArgs = formatArgs;
  exports.save = save;
  exports.load = load;
  exports.useColors = useColors;
  exports.storage = localstorage();
  exports.destroy = (() => {
    let warned = false;
    return () => {
      if (!warned) {
        warned = true;
        console.warn("Instance method `debug.destroy()` is deprecated and no longer does anything. It will be removed in the next major version of `debug`.");
      }
    };
  })();
  exports.colors = [
    "#0000CC",
    "#0000FF",
    "#0033CC",
    "#0033FF",
    "#0066CC",
    "#0066FF",
    "#0099CC",
    "#0099FF",
    "#00CC00",
    "#00CC33",
    "#00CC66",
    "#00CC99",
    "#00CCCC",
    "#00CCFF",
    "#3300CC",
    "#3300FF",
    "#3333CC",
    "#3333FF",
    "#3366CC",
    "#3366FF",
    "#3399CC",
    "#3399FF",
    "#33CC00",
    "#33CC33",
    "#33CC66",
    "#33CC99",
    "#33CCCC",
    "#33CCFF",
    "#6600CC",
    "#6600FF",
    "#6633CC",
    "#6633FF",
    "#66CC00",
    "#66CC33",
    "#9900CC",
    "#9900FF",
    "#9933CC",
    "#9933FF",
    "#99CC00",
    "#99CC33",
    "#CC0000",
    "#CC0033",
    "#CC0066",
    "#CC0099",
    "#CC00CC",
    "#CC00FF",
    "#CC3300",
    "#CC3333",
    "#CC3366",
    "#CC3399",
    "#CC33CC",
    "#CC33FF",
    "#CC6600",
    "#CC6633",
    "#CC9900",
    "#CC9933",
    "#CCCC00",
    "#CCCC33",
    "#FF0000",
    "#FF0033",
    "#FF0066",
    "#FF0099",
    "#FF00CC",
    "#FF00FF",
    "#FF3300",
    "#FF3333",
    "#FF3366",
    "#FF3399",
    "#FF33CC",
    "#FF33FF",
    "#FF6600",
    "#FF6633",
    "#FF9900",
    "#FF9933",
    "#FFCC00",
    "#FFCC33"
  ];
  function useColors() {
    if (typeof window !== "undefined" && window.process && (window.process.type === "renderer" || window.process.__nwjs)) {
      return true;
    }
    if (typeof navigator !== "undefined" && navigator.userAgent && navigator.userAgent.toLowerCase().match(/(edge|trident)\/(\d+)/)) {
      return false;
    }
    let m;
    return typeof document !== "undefined" && document.documentElement && document.documentElement.style && document.documentElement.style.WebkitAppearance || typeof window !== "undefined" && window.console && (window.console.firebug || window.console.exception && window.console.table) || typeof navigator !== "undefined" && navigator.userAgent && (m = navigator.userAgent.toLowerCase().match(/firefox\/(\d+)/)) && parseInt(m[1], 10) >= 31 || typeof navigator !== "undefined" && navigator.userAgent && navigator.userAgent.toLowerCase().match(/applewebkit\/(\d+)/);
  }
  function formatArgs(args) {
    args[0] = (this.useColors ? "%c" : "") + this.namespace + (this.useColors ? " %c" : " ") + args[0] + (this.useColors ? "%c " : " ") + "+" + module.exports.humanize(this.diff);
    if (!this.useColors) {
      return;
    }
    const c = "color: " + this.color;
    args.splice(1, 0, c, "color: inherit");
    let index = 0;
    let lastC = 0;
    args[0].replace(/%[a-zA-Z%]/g, (match) => {
      if (match === "%%") {
        return;
      }
      index++;
      if (match === "%c") {
        lastC = index;
      }
    });
    args.splice(lastC, 0, c);
  }
  exports.log = console.debug || console.log || (() => {});
  function save(namespaces) {
    try {
      if (namespaces) {
        exports.storage.setItem("debug", namespaces);
      } else {
        exports.storage.removeItem("debug");
      }
    } catch (error) {}
  }
  function load() {
    let r;
    try {
      r = exports.storage.getItem("debug") || exports.storage.getItem("DEBUG");
    } catch (error) {}
    if (!r && typeof process !== "undefined" && "env" in process) {
      r = process.env.DEBUG;
    }
    return r;
  }
  function localstorage() {
    try {
      return localStorage;
    } catch (error) {}
  }
  module.exports = require_common()(exports);
  var { formatters } = module.exports;
  formatters.j = function(v) {
    try {
      return JSON.stringify(v);
    } catch (error) {
      return "[UnexpectedJSONParseError]: " + error.message;
    }
  };
});

// node:buffer
var exports_buffer = {};
__export(exports_buffer, {
  transcode: () => transcode,
  resolveObjectURL: () => resolveObjectURL,
  kStringMaxLength: () => kStringMaxLength,
  kMaxLength: () => kMaxLength,
  isUtf8: () => isUtf8,
  isAscii: () => isAscii,
  default: () => buffer_default,
  constants: () => constants,
  btoa: () => btoa,
  atob: () => atob,
  INSPECT_MAX_BYTES: () => INSPECT_MAX_BYTES,
  File: () => File,
  Buffer: () => Buffer2,
  Blob: () => Blob2
});
function getLens(b64) {
  var len2 = b64.length;
  if (len2 % 4 > 0)
    throw Error("Invalid string. Length must be a multiple of 4");
  var validLen = b64.indexOf("=");
  if (validLen === -1)
    validLen = len2;
  var placeHoldersLen = validLen === len2 ? 0 : 4 - validLen % 4;
  return [validLen, placeHoldersLen];
}
function _byteLength(validLen, placeHoldersLen) {
  return (validLen + placeHoldersLen) * 3 / 4 - placeHoldersLen;
}
function toByteArray(b64) {
  var tmp, lens = getLens(b64), validLen = lens[0], placeHoldersLen = lens[1], arr = new Uint8Array(_byteLength(validLen, placeHoldersLen)), curByte = 0, len2 = placeHoldersLen > 0 ? validLen - 4 : validLen, i2;
  for (i2 = 0;i2 < len2; i2 += 4)
    tmp = revLookup[b64.charCodeAt(i2)] << 18 | revLookup[b64.charCodeAt(i2 + 1)] << 12 | revLookup[b64.charCodeAt(i2 + 2)] << 6 | revLookup[b64.charCodeAt(i2 + 3)], arr[curByte++] = tmp >> 16 & 255, arr[curByte++] = tmp >> 8 & 255, arr[curByte++] = tmp & 255;
  if (placeHoldersLen === 2)
    tmp = revLookup[b64.charCodeAt(i2)] << 2 | revLookup[b64.charCodeAt(i2 + 1)] >> 4, arr[curByte++] = tmp & 255;
  if (placeHoldersLen === 1)
    tmp = revLookup[b64.charCodeAt(i2)] << 10 | revLookup[b64.charCodeAt(i2 + 1)] << 4 | revLookup[b64.charCodeAt(i2 + 2)] >> 2, arr[curByte++] = tmp >> 8 & 255, arr[curByte++] = tmp & 255;
  return arr;
}
function tripletToBase64(num) {
  return lookup[num >> 18 & 63] + lookup[num >> 12 & 63] + lookup[num >> 6 & 63] + lookup[num & 63];
}
function encodeChunk(uint8, start, end) {
  var tmp, output = [];
  for (var i2 = start;i2 < end; i2 += 3)
    tmp = (uint8[i2] << 16 & 16711680) + (uint8[i2 + 1] << 8 & 65280) + (uint8[i2 + 2] & 255), output.push(tripletToBase64(tmp));
  return output.join("");
}
function fromByteArray(uint8) {
  var tmp, len2 = uint8.length, extraBytes = len2 % 3, parts = [], maxChunkLength = 16383;
  for (var i2 = 0, len22 = len2 - extraBytes;i2 < len22; i2 += maxChunkLength)
    parts.push(encodeChunk(uint8, i2, i2 + maxChunkLength > len22 ? len22 : i2 + maxChunkLength));
  if (extraBytes === 1)
    tmp = uint8[len2 - 1], parts.push(lookup[tmp >> 2] + lookup[tmp << 4 & 63] + "==");
  else if (extraBytes === 2)
    tmp = (uint8[len2 - 2] << 8) + uint8[len2 - 1], parts.push(lookup[tmp >> 10] + lookup[tmp >> 4 & 63] + lookup[tmp << 2 & 63] + "=");
  return parts.join("");
}
function read(buffer, offset, isLE, mLen, nBytes) {
  var e, m, eLen = nBytes * 8 - mLen - 1, eMax = (1 << eLen) - 1, eBias = eMax >> 1, nBits = -7, i2 = isLE ? nBytes - 1 : 0, d = isLE ? -1 : 1, s = buffer[offset + i2];
  i2 += d, e = s & (1 << -nBits) - 1, s >>= -nBits, nBits += eLen;
  for (;nBits > 0; e = e * 256 + buffer[offset + i2], i2 += d, nBits -= 8)
    ;
  m = e & (1 << -nBits) - 1, e >>= -nBits, nBits += mLen;
  for (;nBits > 0; m = m * 256 + buffer[offset + i2], i2 += d, nBits -= 8)
    ;
  if (e === 0)
    e = 1 - eBias;
  else if (e === eMax)
    return m ? NaN : (s ? -1 : 1) * (1 / 0);
  else
    m = m + Math.pow(2, mLen), e = e - eBias;
  return (s ? -1 : 1) * m * Math.pow(2, e - mLen);
}
function write(buffer, value, offset, isLE, mLen, nBytes) {
  var e, m, c, eLen = nBytes * 8 - mLen - 1, eMax = (1 << eLen) - 1, eBias = eMax >> 1, rt = mLen === 23 ? Math.pow(2, -24) - Math.pow(2, -77) : 0, i2 = isLE ? 0 : nBytes - 1, d = isLE ? 1 : -1, s = value < 0 || value === 0 && 1 / value < 0 ? 1 : 0;
  if (value = Math.abs(value), isNaN(value) || value === 1 / 0)
    m = isNaN(value) ? 1 : 0, e = eMax;
  else {
    if (e = Math.floor(Math.log(value) / Math.LN2), value * (c = Math.pow(2, -e)) < 1)
      e--, c *= 2;
    if (e + eBias >= 1)
      value += rt / c;
    else
      value += rt * Math.pow(2, 1 - eBias);
    if (value * c >= 2)
      e++, c /= 2;
    if (e + eBias >= eMax)
      m = 0, e = eMax;
    else if (e + eBias >= 1)
      m = (value * c - 1) * Math.pow(2, mLen), e = e + eBias;
    else
      m = value * Math.pow(2, eBias - 1) * Math.pow(2, mLen), e = 0;
  }
  for (;mLen >= 8; buffer[offset + i2] = m & 255, i2 += d, m /= 256, mLen -= 8)
    ;
  e = e << mLen | m, eLen += mLen;
  for (;eLen > 0; buffer[offset + i2] = e & 255, i2 += d, e /= 256, eLen -= 8)
    ;
  buffer[offset + i2 - d] |= s * 128;
}
function createBuffer(length) {
  if (length > kMaxLength)
    throw RangeError('The value "' + length + '" is invalid for option "size"');
  let buf = new Uint8Array(length);
  return Object.setPrototypeOf(buf, Buffer2.prototype), buf;
}
function E(sym, getMessage, Base) {
  return class extends Base {
    constructor() {
      super();
      Object.defineProperty(this, "message", { value: getMessage.apply(this, arguments), writable: true, configurable: true }), this.name = `${this.name} [${sym}]`, this.stack, delete this.name;
    }
    get code() {
      return sym;
    }
    set code(value) {
      Object.defineProperty(this, "code", { configurable: true, enumerable: true, value, writable: true });
    }
    toString() {
      return `${this.name} [${sym}]: ${this.message}`;
    }
  };
}
function Buffer2(arg, encodingOrOffset, length) {
  if (typeof arg === "number") {
    if (typeof encodingOrOffset === "string")
      throw TypeError('The "string" argument must be of type string. Received type number');
    return allocUnsafe(arg);
  }
  return from(arg, encodingOrOffset, length);
}
function from(value, encodingOrOffset, length) {
  if (typeof value === "string")
    return fromString(value, encodingOrOffset);
  if (ArrayBuffer.isView(value))
    return fromArrayView(value);
  if (value == null)
    throw TypeError("The first argument must be one of type string, Buffer, ArrayBuffer, Array, or Array-like Object. Received type " + typeof value);
  if (isInstance(value, ArrayBuffer) || value && isInstance(value.buffer, ArrayBuffer))
    return fromArrayBuffer(value, encodingOrOffset, length);
  if (typeof SharedArrayBuffer < "u" && (isInstance(value, SharedArrayBuffer) || value && isInstance(value.buffer, SharedArrayBuffer)))
    return fromArrayBuffer(value, encodingOrOffset, length);
  if (typeof value === "number")
    throw TypeError('The "value" argument must not be of type number. Received type number');
  let valueOf = value.valueOf && value.valueOf();
  if (valueOf != null && valueOf !== value)
    return Buffer2.from(valueOf, encodingOrOffset, length);
  let b = fromObject(value);
  if (b)
    return b;
  if (typeof Symbol < "u" && Symbol.toPrimitive != null && typeof value[Symbol.toPrimitive] === "function")
    return Buffer2.from(value[Symbol.toPrimitive]("string"), encodingOrOffset, length);
  throw TypeError("The first argument must be one of type string, Buffer, ArrayBuffer, Array, or Array-like Object. Received type " + typeof value);
}
function assertSize(size) {
  if (typeof size !== "number")
    throw TypeError('"size" argument must be of type number');
  else if (size < 0)
    throw RangeError('The value "' + size + '" is invalid for option "size"');
}
function alloc(size, fill, encoding) {
  if (assertSize(size), size <= 0)
    return createBuffer(size);
  if (fill !== undefined)
    return typeof encoding === "string" ? createBuffer(size).fill(fill, encoding) : createBuffer(size).fill(fill);
  return createBuffer(size);
}
function allocUnsafe(size) {
  return assertSize(size), createBuffer(size < 0 ? 0 : checked(size) | 0);
}
function fromString(string, encoding) {
  if (typeof encoding !== "string" || encoding === "")
    encoding = "utf8";
  if (!Buffer2.isEncoding(encoding))
    throw TypeError("Unknown encoding: " + encoding);
  let length = byteLength(string, encoding) | 0, buf = createBuffer(length), actual = buf.write(string, encoding);
  if (actual !== length)
    buf = buf.slice(0, actual);
  return buf;
}
function fromArrayLike(array) {
  let length = array.length < 0 ? 0 : checked(array.length) | 0, buf = createBuffer(length);
  for (let i2 = 0;i2 < length; i2 += 1)
    buf[i2] = array[i2] & 255;
  return buf;
}
function fromArrayView(arrayView) {
  if (isInstance(arrayView, Uint8Array)) {
    let copy = new Uint8Array(arrayView);
    return fromArrayBuffer(copy.buffer, copy.byteOffset, copy.byteLength);
  }
  return fromArrayLike(arrayView);
}
function fromArrayBuffer(array, byteOffset, length) {
  if (byteOffset < 0 || array.byteLength < byteOffset)
    throw RangeError('"offset" is outside of buffer bounds');
  if (array.byteLength < byteOffset + (length || 0))
    throw RangeError('"length" is outside of buffer bounds');
  let buf;
  if (byteOffset === undefined && length === undefined)
    buf = new Uint8Array(array);
  else if (length === undefined)
    buf = new Uint8Array(array, byteOffset);
  else
    buf = new Uint8Array(array, byteOffset, length);
  return Object.setPrototypeOf(buf, Buffer2.prototype), buf;
}
function fromObject(obj) {
  if (Buffer2.isBuffer(obj)) {
    let len2 = checked(obj.length) | 0, buf = createBuffer(len2);
    if (buf.length === 0)
      return buf;
    return obj.copy(buf, 0, 0, len2), buf;
  }
  if (obj.length !== undefined) {
    if (typeof obj.length !== "number" || Number.isNaN(obj.length))
      return createBuffer(0);
    return fromArrayLike(obj);
  }
  if (obj.type === "Buffer" && Array.isArray(obj.data))
    return fromArrayLike(obj.data);
}
function checked(length) {
  if (length >= kMaxLength)
    throw RangeError("Attempt to allocate Buffer larger than maximum size: 0x" + kMaxLength.toString(16) + " bytes");
  return length | 0;
}
function byteLength(string, encoding) {
  if (Buffer2.isBuffer(string))
    return string.length;
  if (ArrayBuffer.isView(string) || isInstance(string, ArrayBuffer))
    return string.byteLength;
  if (typeof string !== "string")
    throw TypeError('The "string" argument must be one of type string, Buffer, or ArrayBuffer. Received type ' + typeof string);
  let len2 = string.length, mustMatch = arguments.length > 2 && arguments[2] === true;
  if (!mustMatch && len2 === 0)
    return 0;
  let loweredCase = false;
  for (;; )
    switch (encoding) {
      case "ascii":
      case "latin1":
      case "binary":
        return len2;
      case "utf8":
      case "utf-8":
        return utf8ToBytes(string).length;
      case "ucs2":
      case "ucs-2":
      case "utf16le":
      case "utf-16le":
        return len2 * 2;
      case "hex":
        return len2 >>> 1;
      case "base64":
        return base64ToBytes(string).length;
      default:
        if (loweredCase)
          return mustMatch ? -1 : utf8ToBytes(string).length;
        encoding = ("" + encoding).toLowerCase(), loweredCase = true;
    }
}
function slowToString(encoding, start, end) {
  let loweredCase = false;
  if (start === undefined || start < 0)
    start = 0;
  if (start > this.length)
    return "";
  if (end === undefined || end > this.length)
    end = this.length;
  if (end <= 0)
    return "";
  if (end >>>= 0, start >>>= 0, end <= start)
    return "";
  if (!encoding)
    encoding = "utf8";
  while (true)
    switch (encoding) {
      case "hex":
        return hexSlice(this, start, end);
      case "utf8":
      case "utf-8":
        return utf8Slice(this, start, end);
      case "ascii":
        return asciiSlice(this, start, end);
      case "latin1":
      case "binary":
        return latin1Slice(this, start, end);
      case "base64":
        return base64Slice(this, start, end);
      case "ucs2":
      case "ucs-2":
      case "utf16le":
      case "utf-16le":
        return utf16leSlice(this, start, end);
      default:
        if (loweredCase)
          throw TypeError("Unknown encoding: " + encoding);
        encoding = (encoding + "").toLowerCase(), loweredCase = true;
    }
}
function swap(b, n, m) {
  let i2 = b[n];
  b[n] = b[m], b[m] = i2;
}
function bidirectionalIndexOf(buffer, val, byteOffset, encoding, dir) {
  if (buffer.length === 0)
    return -1;
  if (typeof byteOffset === "string")
    encoding = byteOffset, byteOffset = 0;
  else if (byteOffset > 2147483647)
    byteOffset = 2147483647;
  else if (byteOffset < -2147483648)
    byteOffset = -2147483648;
  if (byteOffset = +byteOffset, Number.isNaN(byteOffset))
    byteOffset = dir ? 0 : buffer.length - 1;
  if (byteOffset < 0)
    byteOffset = buffer.length + byteOffset;
  if (byteOffset >= buffer.length)
    if (dir)
      return -1;
    else
      byteOffset = buffer.length - 1;
  else if (byteOffset < 0)
    if (dir)
      byteOffset = 0;
    else
      return -1;
  if (typeof val === "string")
    val = Buffer2.from(val, encoding);
  if (Buffer2.isBuffer(val)) {
    if (val.length === 0)
      return -1;
    return arrayIndexOf(buffer, val, byteOffset, encoding, dir);
  } else if (typeof val === "number") {
    if (val = val & 255, typeof Uint8Array.prototype.indexOf === "function")
      if (dir)
        return Uint8Array.prototype.indexOf.call(buffer, val, byteOffset);
      else
        return Uint8Array.prototype.lastIndexOf.call(buffer, val, byteOffset);
    return arrayIndexOf(buffer, [val], byteOffset, encoding, dir);
  }
  throw TypeError("val must be string, number or Buffer");
}
function arrayIndexOf(arr, val, byteOffset, encoding, dir) {
  let indexSize = 1, arrLength = arr.length, valLength = val.length;
  if (encoding !== undefined) {
    if (encoding = String(encoding).toLowerCase(), encoding === "ucs2" || encoding === "ucs-2" || encoding === "utf16le" || encoding === "utf-16le") {
      if (arr.length < 2 || val.length < 2)
        return -1;
      indexSize = 2, arrLength /= 2, valLength /= 2, byteOffset /= 2;
    }
  }
  function read2(buf, i3) {
    if (indexSize === 1)
      return buf[i3];
    else
      return buf.readUInt16BE(i3 * indexSize);
  }
  let i2;
  if (dir) {
    let foundIndex = -1;
    for (i2 = byteOffset;i2 < arrLength; i2++)
      if (read2(arr, i2) === read2(val, foundIndex === -1 ? 0 : i2 - foundIndex)) {
        if (foundIndex === -1)
          foundIndex = i2;
        if (i2 - foundIndex + 1 === valLength)
          return foundIndex * indexSize;
      } else {
        if (foundIndex !== -1)
          i2 -= i2 - foundIndex;
        foundIndex = -1;
      }
  } else {
    if (byteOffset + valLength > arrLength)
      byteOffset = arrLength - valLength;
    for (i2 = byteOffset;i2 >= 0; i2--) {
      let found = true;
      for (let j = 0;j < valLength; j++)
        if (read2(arr, i2 + j) !== read2(val, j)) {
          found = false;
          break;
        }
      if (found)
        return i2;
    }
  }
  return -1;
}
function hexWrite(buf, string, offset, length) {
  offset = Number(offset) || 0;
  let remaining = buf.length - offset;
  if (!length)
    length = remaining;
  else if (length = Number(length), length > remaining)
    length = remaining;
  let strLen = string.length;
  if (length > strLen / 2)
    length = strLen / 2;
  let i2;
  for (i2 = 0;i2 < length; ++i2) {
    let parsed = parseInt(string.substr(i2 * 2, 2), 16);
    if (Number.isNaN(parsed))
      return i2;
    buf[offset + i2] = parsed;
  }
  return i2;
}
function utf8Write(buf, string, offset, length) {
  return blitBuffer(utf8ToBytes(string, buf.length - offset), buf, offset, length);
}
function asciiWrite(buf, string, offset, length) {
  return blitBuffer(asciiToBytes(string), buf, offset, length);
}
function base64Write(buf, string, offset, length) {
  return blitBuffer(base64ToBytes(string), buf, offset, length);
}
function ucs2Write(buf, string, offset, length) {
  return blitBuffer(utf16leToBytes(string, buf.length - offset), buf, offset, length);
}
function base64Slice(buf, start, end) {
  if (start === 0 && end === buf.length)
    return fromByteArray(buf);
  else
    return fromByteArray(buf.slice(start, end));
}
function utf8Slice(buf, start, end) {
  end = Math.min(buf.length, end);
  let res = [], i2 = start;
  while (i2 < end) {
    let firstByte = buf[i2], codePoint = null, bytesPerSequence = firstByte > 239 ? 4 : firstByte > 223 ? 3 : firstByte > 191 ? 2 : 1;
    if (i2 + bytesPerSequence <= end) {
      let secondByte, thirdByte, fourthByte, tempCodePoint;
      switch (bytesPerSequence) {
        case 1:
          if (firstByte < 128)
            codePoint = firstByte;
          break;
        case 2:
          if (secondByte = buf[i2 + 1], (secondByte & 192) === 128) {
            if (tempCodePoint = (firstByte & 31) << 6 | secondByte & 63, tempCodePoint > 127)
              codePoint = tempCodePoint;
          }
          break;
        case 3:
          if (secondByte = buf[i2 + 1], thirdByte = buf[i2 + 2], (secondByte & 192) === 128 && (thirdByte & 192) === 128) {
            if (tempCodePoint = (firstByte & 15) << 12 | (secondByte & 63) << 6 | thirdByte & 63, tempCodePoint > 2047 && (tempCodePoint < 55296 || tempCodePoint > 57343))
              codePoint = tempCodePoint;
          }
          break;
        case 4:
          if (secondByte = buf[i2 + 1], thirdByte = buf[i2 + 2], fourthByte = buf[i2 + 3], (secondByte & 192) === 128 && (thirdByte & 192) === 128 && (fourthByte & 192) === 128) {
            if (tempCodePoint = (firstByte & 15) << 18 | (secondByte & 63) << 12 | (thirdByte & 63) << 6 | fourthByte & 63, tempCodePoint > 65535 && tempCodePoint < 1114112)
              codePoint = tempCodePoint;
          }
      }
    }
    if (codePoint === null)
      codePoint = 65533, bytesPerSequence = 1;
    else if (codePoint > 65535)
      codePoint -= 65536, res.push(codePoint >>> 10 & 1023 | 55296), codePoint = 56320 | codePoint & 1023;
    res.push(codePoint), i2 += bytesPerSequence;
  }
  return decodeCodePointsArray(res);
}
function decodeCodePointsArray(codePoints) {
  let len2 = codePoints.length;
  if (len2 <= MAX_ARGUMENTS_LENGTH)
    return String.fromCharCode.apply(String, codePoints);
  let res = "", i2 = 0;
  while (i2 < len2)
    res += String.fromCharCode.apply(String, codePoints.slice(i2, i2 += MAX_ARGUMENTS_LENGTH));
  return res;
}
function asciiSlice(buf, start, end) {
  let ret = "";
  end = Math.min(buf.length, end);
  for (let i2 = start;i2 < end; ++i2)
    ret += String.fromCharCode(buf[i2] & 127);
  return ret;
}
function latin1Slice(buf, start, end) {
  let ret = "";
  end = Math.min(buf.length, end);
  for (let i2 = start;i2 < end; ++i2)
    ret += String.fromCharCode(buf[i2]);
  return ret;
}
function hexSlice(buf, start, end) {
  let len2 = buf.length;
  if (!start || start < 0)
    start = 0;
  if (!end || end < 0 || end > len2)
    end = len2;
  let out = "";
  for (let i2 = start;i2 < end; ++i2)
    out += hexSliceLookupTable[buf[i2]];
  return out;
}
function utf16leSlice(buf, start, end) {
  let bytes = buf.slice(start, end), res = "";
  for (let i2 = 0;i2 < bytes.length - 1; i2 += 2)
    res += String.fromCharCode(bytes[i2] + bytes[i2 + 1] * 256);
  return res;
}
function checkOffset(offset, ext, length) {
  if (offset % 1 !== 0 || offset < 0)
    throw RangeError("offset is not uint");
  if (offset + ext > length)
    throw RangeError("Trying to access beyond buffer length");
}
function checkInt(buf, value, offset, ext, max, min) {
  if (!Buffer2.isBuffer(buf))
    throw TypeError('"buffer" argument must be a Buffer instance');
  if (value > max || value < min)
    throw RangeError('"value" argument is out of bounds');
  if (offset + ext > buf.length)
    throw RangeError("Index out of range");
}
function wrtBigUInt64LE(buf, value, offset, min, max) {
  checkIntBI(value, min, max, buf, offset, 7);
  let lo = Number(value & BigInt(4294967295));
  buf[offset++] = lo, lo = lo >> 8, buf[offset++] = lo, lo = lo >> 8, buf[offset++] = lo, lo = lo >> 8, buf[offset++] = lo;
  let hi = Number(value >> BigInt(32) & BigInt(4294967295));
  return buf[offset++] = hi, hi = hi >> 8, buf[offset++] = hi, hi = hi >> 8, buf[offset++] = hi, hi = hi >> 8, buf[offset++] = hi, offset;
}
function wrtBigUInt64BE(buf, value, offset, min, max) {
  checkIntBI(value, min, max, buf, offset, 7);
  let lo = Number(value & BigInt(4294967295));
  buf[offset + 7] = lo, lo = lo >> 8, buf[offset + 6] = lo, lo = lo >> 8, buf[offset + 5] = lo, lo = lo >> 8, buf[offset + 4] = lo;
  let hi = Number(value >> BigInt(32) & BigInt(4294967295));
  return buf[offset + 3] = hi, hi = hi >> 8, buf[offset + 2] = hi, hi = hi >> 8, buf[offset + 1] = hi, hi = hi >> 8, buf[offset] = hi, offset + 8;
}
function checkIEEE754(buf, value, offset, ext, max, min) {
  if (offset + ext > buf.length)
    throw RangeError("Index out of range");
  if (offset < 0)
    throw RangeError("Index out of range");
}
function writeFloat(buf, value, offset, littleEndian, noAssert) {
  if (value = +value, offset = offset >>> 0, !noAssert)
    checkIEEE754(buf, value, offset, 4, 340282346638528860000000000000000000000, -340282346638528860000000000000000000000);
  return write(buf, value, offset, littleEndian, 23, 4), offset + 4;
}
function writeDouble(buf, value, offset, littleEndian, noAssert) {
  if (value = +value, offset = offset >>> 0, !noAssert)
    checkIEEE754(buf, value, offset, 8, 179769313486231570000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, -179769313486231570000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000);
  return write(buf, value, offset, littleEndian, 52, 8), offset + 8;
}
function addNumericalSeparator(val) {
  let res = "", i2 = val.length, start = val[0] === "-" ? 1 : 0;
  for (;i2 >= start + 4; i2 -= 3)
    res = `_${val.slice(i2 - 3, i2)}${res}`;
  return `${val.slice(0, i2)}${res}`;
}
function checkBounds(buf, offset, byteLength2) {
  if (validateNumber(offset, "offset"), buf[offset] === undefined || buf[offset + byteLength2] === undefined)
    boundsError(offset, buf.length - (byteLength2 + 1));
}
function checkIntBI(value, min, max, buf, offset, byteLength2) {
  if (value > max || value < min) {
    let n = typeof min === "bigint" ? "n" : "", range;
    if (byteLength2 > 3)
      if (min === 0 || min === BigInt(0))
        range = `>= 0${n} and < 2${n} ** ${(byteLength2 + 1) * 8}${n}`;
      else
        range = `>= -(2${n} ** ${(byteLength2 + 1) * 8 - 1}${n}) and < 2 ** ${(byteLength2 + 1) * 8 - 1}${n}`;
    else
      range = `>= ${min}${n} and <= ${max}${n}`;
    throw new ERR_OUT_OF_RANGE("value", range, value);
  }
  checkBounds(buf, offset, byteLength2);
}
function validateNumber(value, name) {
  if (typeof value !== "number")
    throw new ERR_INVALID_ARG_TYPE(name, "number", value);
}
function boundsError(value, length, type) {
  if (Math.floor(value) !== value)
    throw validateNumber(value, type), new ERR_OUT_OF_RANGE(type || "offset", "an integer", value);
  if (length < 0)
    throw new ERR_BUFFER_OUT_OF_BOUNDS;
  throw new ERR_OUT_OF_RANGE(type || "offset", `>= ${type ? 1 : 0} and <= ${length}`, value);
}
function base64clean(str) {
  if (str = str.split("=")[0], str = str.trim().replace(INVALID_BASE64_RE, ""), str.length < 2)
    return "";
  while (str.length % 4 !== 0)
    str = str + "=";
  return str;
}
function utf8ToBytes(string, units) {
  units = units || 1 / 0;
  let codePoint, length = string.length, leadSurrogate = null, bytes = [];
  for (let i2 = 0;i2 < length; ++i2) {
    if (codePoint = string.charCodeAt(i2), codePoint > 55295 && codePoint < 57344) {
      if (!leadSurrogate) {
        if (codePoint > 56319) {
          if ((units -= 3) > -1)
            bytes.push(239, 191, 189);
          continue;
        } else if (i2 + 1 === length) {
          if ((units -= 3) > -1)
            bytes.push(239, 191, 189);
          continue;
        }
        leadSurrogate = codePoint;
        continue;
      }
      if (codePoint < 56320) {
        if ((units -= 3) > -1)
          bytes.push(239, 191, 189);
        leadSurrogate = codePoint;
        continue;
      }
      codePoint = (leadSurrogate - 55296 << 10 | codePoint - 56320) + 65536;
    } else if (leadSurrogate) {
      if ((units -= 3) > -1)
        bytes.push(239, 191, 189);
    }
    if (leadSurrogate = null, codePoint < 128) {
      if ((units -= 1) < 0)
        break;
      bytes.push(codePoint);
    } else if (codePoint < 2048) {
      if ((units -= 2) < 0)
        break;
      bytes.push(codePoint >> 6 | 192, codePoint & 63 | 128);
    } else if (codePoint < 65536) {
      if ((units -= 3) < 0)
        break;
      bytes.push(codePoint >> 12 | 224, codePoint >> 6 & 63 | 128, codePoint & 63 | 128);
    } else if (codePoint < 1114112) {
      if ((units -= 4) < 0)
        break;
      bytes.push(codePoint >> 18 | 240, codePoint >> 12 & 63 | 128, codePoint >> 6 & 63 | 128, codePoint & 63 | 128);
    } else
      throw Error("Invalid code point");
  }
  return bytes;
}
function asciiToBytes(str) {
  let byteArray = [];
  for (let i2 = 0;i2 < str.length; ++i2)
    byteArray.push(str.charCodeAt(i2) & 255);
  return byteArray;
}
function utf16leToBytes(str, units) {
  let c, hi, lo, byteArray = [];
  for (let i2 = 0;i2 < str.length; ++i2) {
    if ((units -= 2) < 0)
      break;
    c = str.charCodeAt(i2), hi = c >> 8, lo = c % 256, byteArray.push(lo), byteArray.push(hi);
  }
  return byteArray;
}
function base64ToBytes(str) {
  return toByteArray(base64clean(str));
}
function blitBuffer(src, dst, offset, length) {
  let i2;
  for (i2 = 0;i2 < length; ++i2) {
    if (i2 + offset >= dst.length || i2 >= src.length)
      break;
    dst[i2 + offset] = src[i2];
  }
  return i2;
}
function isInstance(obj, type) {
  return obj instanceof type || obj != null && obj.constructor != null && obj.constructor.name != null && obj.constructor.name === type.name;
}
function defineBigIntMethod(fn) {
  return typeof BigInt > "u" ? BufferBigIntNotDefined : fn;
}
function BufferBigIntNotDefined() {
  throw Error("BigInt not supported");
}
function notimpl(name) {
  return () => {
    throw Error(name + " is not implemented for node:buffer browser polyfill");
  };
}
var lookup, revLookup, code = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", i, len, customInspectSymbol, INSPECT_MAX_BYTES = 50, kMaxLength = 2147483647, kStringMaxLength = 536870888, btoa, atob, File, Blob2, constants, ERR_BUFFER_OUT_OF_BOUNDS, ERR_INVALID_ARG_TYPE, ERR_OUT_OF_RANGE, MAX_ARGUMENTS_LENGTH = 4096, INVALID_BASE64_RE, hexSliceLookupTable, resolveObjectURL, isUtf8, isAscii = (str) => {
  for (let char of str)
    if (char.charCodeAt(0) > 127)
      return false;
  return true;
}, transcode, buffer_default;
var init_buffer = __esm(() => {
  lookup = [];
  revLookup = [];
  for (i = 0, len = code.length;i < len; ++i)
    lookup[i] = code[i], revLookup[code.charCodeAt(i)] = i;
  revLookup[45] = 62;
  revLookup[95] = 63;
  customInspectSymbol = typeof Symbol === "function" && typeof Symbol.for === "function" ? Symbol.for("nodejs.util.inspect.custom") : null;
  btoa = globalThis.btoa;
  atob = globalThis.atob;
  File = globalThis.File;
  Blob2 = globalThis.Blob;
  constants = { MAX_LENGTH: kMaxLength, MAX_STRING_LENGTH: kStringMaxLength };
  ERR_BUFFER_OUT_OF_BOUNDS = E("ERR_BUFFER_OUT_OF_BOUNDS", function(name) {
    if (name)
      return `${name} is outside of buffer bounds`;
    return "Attempt to access memory outside buffer bounds";
  }, RangeError);
  ERR_INVALID_ARG_TYPE = E("ERR_INVALID_ARG_TYPE", function(name, actual) {
    return `The "${name}" argument must be of type number. Received type ${typeof actual}`;
  }, TypeError);
  ERR_OUT_OF_RANGE = E("ERR_OUT_OF_RANGE", function(str, range, input) {
    let msg = `The value of "${str}" is out of range.`, received = input;
    if (Number.isInteger(input) && Math.abs(input) > 4294967296)
      received = addNumericalSeparator(String(input));
    else if (typeof input === "bigint") {
      if (received = String(input), input > BigInt(2) ** BigInt(32) || input < -(BigInt(2) ** BigInt(32)))
        received = addNumericalSeparator(received);
      received += "n";
    }
    return msg += ` It must be ${range}. Received ${received}`, msg;
  }, RangeError);
  Object.defineProperty(Buffer2.prototype, "parent", { enumerable: true, get: function() {
    if (!Buffer2.isBuffer(this))
      return;
    return this.buffer;
  } });
  Object.defineProperty(Buffer2.prototype, "offset", { enumerable: true, get: function() {
    if (!Buffer2.isBuffer(this))
      return;
    return this.byteOffset;
  } });
  Buffer2.poolSize = 8192;
  Buffer2.from = function(value, encodingOrOffset, length) {
    return from(value, encodingOrOffset, length);
  };
  Object.setPrototypeOf(Buffer2.prototype, Uint8Array.prototype);
  Object.setPrototypeOf(Buffer2, Uint8Array);
  Buffer2.alloc = function(size, fill, encoding) {
    return alloc(size, fill, encoding);
  };
  Buffer2.allocUnsafe = function(size) {
    return allocUnsafe(size);
  };
  Buffer2.allocUnsafeSlow = function(size) {
    return allocUnsafe(size);
  };
  Buffer2.isBuffer = function(b) {
    return b != null && b._isBuffer === true && b !== Buffer2.prototype;
  };
  Buffer2.compare = function(a, b) {
    if (isInstance(a, Uint8Array))
      a = Buffer2.from(a, a.offset, a.byteLength);
    if (isInstance(b, Uint8Array))
      b = Buffer2.from(b, b.offset, b.byteLength);
    if (!Buffer2.isBuffer(a) || !Buffer2.isBuffer(b))
      throw TypeError('The "buf1", "buf2" arguments must be one of type Buffer or Uint8Array');
    if (a === b)
      return 0;
    let x = a.length, y = b.length;
    for (let i2 = 0, len2 = Math.min(x, y);i2 < len2; ++i2)
      if (a[i2] !== b[i2]) {
        x = a[i2], y = b[i2];
        break;
      }
    if (x < y)
      return -1;
    if (y < x)
      return 1;
    return 0;
  };
  Buffer2.isEncoding = function(encoding) {
    switch (String(encoding).toLowerCase()) {
      case "hex":
      case "utf8":
      case "utf-8":
      case "ascii":
      case "latin1":
      case "binary":
      case "base64":
      case "ucs2":
      case "ucs-2":
      case "utf16le":
      case "utf-16le":
        return true;
      default:
        return false;
    }
  };
  Buffer2.concat = function(list, length) {
    if (!Array.isArray(list))
      throw TypeError('"list" argument must be an Array of Buffers');
    if (list.length === 0)
      return Buffer2.alloc(0);
    let i2;
    if (length === undefined) {
      length = 0;
      for (i2 = 0;i2 < list.length; ++i2)
        length += list[i2].length;
    }
    let buffer = Buffer2.allocUnsafe(length), pos = 0;
    for (i2 = 0;i2 < list.length; ++i2) {
      let buf = list[i2];
      if (isInstance(buf, Uint8Array))
        if (pos + buf.length > buffer.length) {
          if (!Buffer2.isBuffer(buf))
            buf = Buffer2.from(buf);
          buf.copy(buffer, pos);
        } else
          Uint8Array.prototype.set.call(buffer, buf, pos);
      else if (!Buffer2.isBuffer(buf))
        throw TypeError('"list" argument must be an Array of Buffers');
      else
        buf.copy(buffer, pos);
      pos += buf.length;
    }
    return buffer;
  };
  Buffer2.byteLength = byteLength;
  Buffer2.prototype._isBuffer = true;
  Buffer2.prototype.swap16 = function() {
    let len2 = this.length;
    if (len2 % 2 !== 0)
      throw RangeError("Buffer size must be a multiple of 16-bits");
    for (let i2 = 0;i2 < len2; i2 += 2)
      swap(this, i2, i2 + 1);
    return this;
  };
  Buffer2.prototype.swap32 = function() {
    let len2 = this.length;
    if (len2 % 4 !== 0)
      throw RangeError("Buffer size must be a multiple of 32-bits");
    for (let i2 = 0;i2 < len2; i2 += 4)
      swap(this, i2, i2 + 3), swap(this, i2 + 1, i2 + 2);
    return this;
  };
  Buffer2.prototype.swap64 = function() {
    let len2 = this.length;
    if (len2 % 8 !== 0)
      throw RangeError("Buffer size must be a multiple of 64-bits");
    for (let i2 = 0;i2 < len2; i2 += 8)
      swap(this, i2, i2 + 7), swap(this, i2 + 1, i2 + 6), swap(this, i2 + 2, i2 + 5), swap(this, i2 + 3, i2 + 4);
    return this;
  };
  Buffer2.prototype.toString = function() {
    let length = this.length;
    if (length === 0)
      return "";
    if (arguments.length === 0)
      return utf8Slice(this, 0, length);
    return slowToString.apply(this, arguments);
  };
  Buffer2.prototype.toLocaleString = Buffer2.prototype.toString;
  Buffer2.prototype.equals = function(b) {
    if (!Buffer2.isBuffer(b))
      throw TypeError("Argument must be a Buffer");
    if (this === b)
      return true;
    return Buffer2.compare(this, b) === 0;
  };
  Buffer2.prototype.inspect = function() {
    let str = "", max = INSPECT_MAX_BYTES;
    if (str = this.toString("hex", 0, max).replace(/(.{2})/g, "$1 ").trim(), this.length > max)
      str += " ... ";
    return "<Buffer " + str + ">";
  };
  if (customInspectSymbol)
    Buffer2.prototype[customInspectSymbol] = Buffer2.prototype.inspect;
  Buffer2.prototype.compare = function(target, start, end, thisStart, thisEnd) {
    if (isInstance(target, Uint8Array))
      target = Buffer2.from(target, target.offset, target.byteLength);
    if (!Buffer2.isBuffer(target))
      throw TypeError('The "target" argument must be one of type Buffer or Uint8Array. Received type ' + typeof target);
    if (start === undefined)
      start = 0;
    if (end === undefined)
      end = target ? target.length : 0;
    if (thisStart === undefined)
      thisStart = 0;
    if (thisEnd === undefined)
      thisEnd = this.length;
    if (start < 0 || end > target.length || thisStart < 0 || thisEnd > this.length)
      throw RangeError("out of range index");
    if (thisStart >= thisEnd && start >= end)
      return 0;
    if (thisStart >= thisEnd)
      return -1;
    if (start >= end)
      return 1;
    if (start >>>= 0, end >>>= 0, thisStart >>>= 0, thisEnd >>>= 0, this === target)
      return 0;
    let x = thisEnd - thisStart, y = end - start, len2 = Math.min(x, y), thisCopy = this.slice(thisStart, thisEnd), targetCopy = target.slice(start, end);
    for (let i2 = 0;i2 < len2; ++i2)
      if (thisCopy[i2] !== targetCopy[i2]) {
        x = thisCopy[i2], y = targetCopy[i2];
        break;
      }
    if (x < y)
      return -1;
    if (y < x)
      return 1;
    return 0;
  };
  Buffer2.prototype.includes = function(val, byteOffset, encoding) {
    return this.indexOf(val, byteOffset, encoding) !== -1;
  };
  Buffer2.prototype.indexOf = function(val, byteOffset, encoding) {
    return bidirectionalIndexOf(this, val, byteOffset, encoding, true);
  };
  Buffer2.prototype.lastIndexOf = function(val, byteOffset, encoding) {
    return bidirectionalIndexOf(this, val, byteOffset, encoding, false);
  };
  Buffer2.prototype.write = function(string, offset, length, encoding) {
    if (offset === undefined)
      encoding = "utf8", length = this.length, offset = 0;
    else if (length === undefined && typeof offset === "string")
      encoding = offset, length = this.length, offset = 0;
    else if (isFinite(offset))
      if (offset = offset >>> 0, isFinite(length)) {
        if (length = length >>> 0, encoding === undefined)
          encoding = "utf8";
      } else
        encoding = length, length = undefined;
    else
      throw Error("Buffer.write(string, encoding, offset[, length]) is no longer supported");
    let remaining = this.length - offset;
    if (length === undefined || length > remaining)
      length = remaining;
    if (string.length > 0 && (length < 0 || offset < 0) || offset > this.length)
      throw RangeError("Attempt to write outside buffer bounds");
    if (!encoding)
      encoding = "utf8";
    let loweredCase = false;
    for (;; )
      switch (encoding) {
        case "hex":
          return hexWrite(this, string, offset, length);
        case "utf8":
        case "utf-8":
          return utf8Write(this, string, offset, length);
        case "ascii":
        case "latin1":
        case "binary":
          return asciiWrite(this, string, offset, length);
        case "base64":
          return base64Write(this, string, offset, length);
        case "ucs2":
        case "ucs-2":
        case "utf16le":
        case "utf-16le":
          return ucs2Write(this, string, offset, length);
        default:
          if (loweredCase)
            throw TypeError("Unknown encoding: " + encoding);
          encoding = ("" + encoding).toLowerCase(), loweredCase = true;
      }
  };
  Buffer2.prototype.toJSON = function() {
    return { type: "Buffer", data: Array.prototype.slice.call(this._arr || this, 0) };
  };
  Buffer2.prototype.slice = function(start, end) {
    let len2 = this.length;
    if (start = ~~start, end = end === undefined ? len2 : ~~end, start < 0) {
      if (start += len2, start < 0)
        start = 0;
    } else if (start > len2)
      start = len2;
    if (end < 0) {
      if (end += len2, end < 0)
        end = 0;
    } else if (end > len2)
      end = len2;
    if (end < start)
      end = start;
    let newBuf = this.subarray(start, end);
    return Object.setPrototypeOf(newBuf, Buffer2.prototype), newBuf;
  };
  Buffer2.prototype.readUintLE = Buffer2.prototype.readUIntLE = function(offset, byteLength2, noAssert) {
    if (offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert)
      checkOffset(offset, byteLength2, this.length);
    let val = this[offset], mul = 1, i2 = 0;
    while (++i2 < byteLength2 && (mul *= 256))
      val += this[offset + i2] * mul;
    return val;
  };
  Buffer2.prototype.readUintBE = Buffer2.prototype.readUIntBE = function(offset, byteLength2, noAssert) {
    if (offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert)
      checkOffset(offset, byteLength2, this.length);
    let val = this[offset + --byteLength2], mul = 1;
    while (byteLength2 > 0 && (mul *= 256))
      val += this[offset + --byteLength2] * mul;
    return val;
  };
  Buffer2.prototype.readUint8 = Buffer2.prototype.readUInt8 = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 1, this.length);
    return this[offset];
  };
  Buffer2.prototype.readUint16LE = Buffer2.prototype.readUInt16LE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 2, this.length);
    return this[offset] | this[offset + 1] << 8;
  };
  Buffer2.prototype.readUint16BE = Buffer2.prototype.readUInt16BE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 2, this.length);
    return this[offset] << 8 | this[offset + 1];
  };
  Buffer2.prototype.readUint32LE = Buffer2.prototype.readUInt32LE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return (this[offset] | this[offset + 1] << 8 | this[offset + 2] << 16) + this[offset + 3] * 16777216;
  };
  Buffer2.prototype.readUint32BE = Buffer2.prototype.readUInt32BE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return this[offset] * 16777216 + (this[offset + 1] << 16 | this[offset + 2] << 8 | this[offset + 3]);
  };
  Buffer2.prototype.readBigUInt64LE = defineBigIntMethod(function(offset) {
    offset = offset >>> 0, validateNumber(offset, "offset");
    let first = this[offset], last = this[offset + 7];
    if (first === undefined || last === undefined)
      boundsError(offset, this.length - 8);
    let lo = first + this[++offset] * 256 + this[++offset] * 65536 + this[++offset] * 16777216, hi = this[++offset] + this[++offset] * 256 + this[++offset] * 65536 + last * 16777216;
    return BigInt(lo) + (BigInt(hi) << BigInt(32));
  });
  Buffer2.prototype.readBigUInt64BE = defineBigIntMethod(function(offset) {
    offset = offset >>> 0, validateNumber(offset, "offset");
    let first = this[offset], last = this[offset + 7];
    if (first === undefined || last === undefined)
      boundsError(offset, this.length - 8);
    let hi = first * 16777216 + this[++offset] * 65536 + this[++offset] * 256 + this[++offset], lo = this[++offset] * 16777216 + this[++offset] * 65536 + this[++offset] * 256 + last;
    return (BigInt(hi) << BigInt(32)) + BigInt(lo);
  });
  Buffer2.prototype.readIntLE = function(offset, byteLength2, noAssert) {
    if (offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert)
      checkOffset(offset, byteLength2, this.length);
    let val = this[offset], mul = 1, i2 = 0;
    while (++i2 < byteLength2 && (mul *= 256))
      val += this[offset + i2] * mul;
    if (mul *= 128, val >= mul)
      val -= Math.pow(2, 8 * byteLength2);
    return val;
  };
  Buffer2.prototype.readIntBE = function(offset, byteLength2, noAssert) {
    if (offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert)
      checkOffset(offset, byteLength2, this.length);
    let i2 = byteLength2, mul = 1, val = this[offset + --i2];
    while (i2 > 0 && (mul *= 256))
      val += this[offset + --i2] * mul;
    if (mul *= 128, val >= mul)
      val -= Math.pow(2, 8 * byteLength2);
    return val;
  };
  Buffer2.prototype.readInt8 = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 1, this.length);
    if (!(this[offset] & 128))
      return this[offset];
    return (255 - this[offset] + 1) * -1;
  };
  Buffer2.prototype.readInt16LE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 2, this.length);
    let val = this[offset] | this[offset + 1] << 8;
    return val & 32768 ? val | 4294901760 : val;
  };
  Buffer2.prototype.readInt16BE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 2, this.length);
    let val = this[offset + 1] | this[offset] << 8;
    return val & 32768 ? val | 4294901760 : val;
  };
  Buffer2.prototype.readInt32LE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return this[offset] | this[offset + 1] << 8 | this[offset + 2] << 16 | this[offset + 3] << 24;
  };
  Buffer2.prototype.readInt32BE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return this[offset] << 24 | this[offset + 1] << 16 | this[offset + 2] << 8 | this[offset + 3];
  };
  Buffer2.prototype.readBigInt64LE = defineBigIntMethod(function(offset) {
    offset = offset >>> 0, validateNumber(offset, "offset");
    let first = this[offset], last = this[offset + 7];
    if (first === undefined || last === undefined)
      boundsError(offset, this.length - 8);
    let val = this[offset + 4] + this[offset + 5] * 256 + this[offset + 6] * 65536 + (last << 24);
    return (BigInt(val) << BigInt(32)) + BigInt(first + this[++offset] * 256 + this[++offset] * 65536 + this[++offset] * 16777216);
  });
  Buffer2.prototype.readBigInt64BE = defineBigIntMethod(function(offset) {
    offset = offset >>> 0, validateNumber(offset, "offset");
    let first = this[offset], last = this[offset + 7];
    if (first === undefined || last === undefined)
      boundsError(offset, this.length - 8);
    let val = (first << 24) + this[++offset] * 65536 + this[++offset] * 256 + this[++offset];
    return (BigInt(val) << BigInt(32)) + BigInt(this[++offset] * 16777216 + this[++offset] * 65536 + this[++offset] * 256 + last);
  });
  Buffer2.prototype.readFloatLE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return read(this, offset, true, 23, 4);
  };
  Buffer2.prototype.readFloatBE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 4, this.length);
    return read(this, offset, false, 23, 4);
  };
  Buffer2.prototype.readDoubleLE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 8, this.length);
    return read(this, offset, true, 52, 8);
  };
  Buffer2.prototype.readDoubleBE = function(offset, noAssert) {
    if (offset = offset >>> 0, !noAssert)
      checkOffset(offset, 8, this.length);
    return read(this, offset, false, 52, 8);
  };
  Buffer2.prototype.writeUintLE = Buffer2.prototype.writeUIntLE = function(value, offset, byteLength2, noAssert) {
    if (value = +value, offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert) {
      let maxBytes = Math.pow(2, 8 * byteLength2) - 1;
      checkInt(this, value, offset, byteLength2, maxBytes, 0);
    }
    let mul = 1, i2 = 0;
    this[offset] = value & 255;
    while (++i2 < byteLength2 && (mul *= 256))
      this[offset + i2] = value / mul & 255;
    return offset + byteLength2;
  };
  Buffer2.prototype.writeUintBE = Buffer2.prototype.writeUIntBE = function(value, offset, byteLength2, noAssert) {
    if (value = +value, offset = offset >>> 0, byteLength2 = byteLength2 >>> 0, !noAssert) {
      let maxBytes = Math.pow(2, 8 * byteLength2) - 1;
      checkInt(this, value, offset, byteLength2, maxBytes, 0);
    }
    let i2 = byteLength2 - 1, mul = 1;
    this[offset + i2] = value & 255;
    while (--i2 >= 0 && (mul *= 256))
      this[offset + i2] = value / mul & 255;
    return offset + byteLength2;
  };
  Buffer2.prototype.writeUint8 = Buffer2.prototype.writeUInt8 = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 1, 255, 0);
    return this[offset] = value & 255, offset + 1;
  };
  Buffer2.prototype.writeUint16LE = Buffer2.prototype.writeUInt16LE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 2, 65535, 0);
    return this[offset] = value & 255, this[offset + 1] = value >>> 8, offset + 2;
  };
  Buffer2.prototype.writeUint16BE = Buffer2.prototype.writeUInt16BE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 2, 65535, 0);
    return this[offset] = value >>> 8, this[offset + 1] = value & 255, offset + 2;
  };
  Buffer2.prototype.writeUint32LE = Buffer2.prototype.writeUInt32LE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 4, 4294967295, 0);
    return this[offset + 3] = value >>> 24, this[offset + 2] = value >>> 16, this[offset + 1] = value >>> 8, this[offset] = value & 255, offset + 4;
  };
  Buffer2.prototype.writeUint32BE = Buffer2.prototype.writeUInt32BE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 4, 4294967295, 0);
    return this[offset] = value >>> 24, this[offset + 1] = value >>> 16, this[offset + 2] = value >>> 8, this[offset + 3] = value & 255, offset + 4;
  };
  Buffer2.prototype.writeBigUInt64LE = defineBigIntMethod(function(value, offset = 0) {
    return wrtBigUInt64LE(this, value, offset, BigInt(0), BigInt("0xffffffffffffffff"));
  });
  Buffer2.prototype.writeBigUInt64BE = defineBigIntMethod(function(value, offset = 0) {
    return wrtBigUInt64BE(this, value, offset, BigInt(0), BigInt("0xffffffffffffffff"));
  });
  Buffer2.prototype.writeIntLE = function(value, offset, byteLength2, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert) {
      let limit = Math.pow(2, 8 * byteLength2 - 1);
      checkInt(this, value, offset, byteLength2, limit - 1, -limit);
    }
    let i2 = 0, mul = 1, sub = 0;
    this[offset] = value & 255;
    while (++i2 < byteLength2 && (mul *= 256)) {
      if (value < 0 && sub === 0 && this[offset + i2 - 1] !== 0)
        sub = 1;
      this[offset + i2] = (value / mul >> 0) - sub & 255;
    }
    return offset + byteLength2;
  };
  Buffer2.prototype.writeIntBE = function(value, offset, byteLength2, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert) {
      let limit = Math.pow(2, 8 * byteLength2 - 1);
      checkInt(this, value, offset, byteLength2, limit - 1, -limit);
    }
    let i2 = byteLength2 - 1, mul = 1, sub = 0;
    this[offset + i2] = value & 255;
    while (--i2 >= 0 && (mul *= 256)) {
      if (value < 0 && sub === 0 && this[offset + i2 + 1] !== 0)
        sub = 1;
      this[offset + i2] = (value / mul >> 0) - sub & 255;
    }
    return offset + byteLength2;
  };
  Buffer2.prototype.writeInt8 = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 1, 127, -128);
    if (value < 0)
      value = 255 + value + 1;
    return this[offset] = value & 255, offset + 1;
  };
  Buffer2.prototype.writeInt16LE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 2, 32767, -32768);
    return this[offset] = value & 255, this[offset + 1] = value >>> 8, offset + 2;
  };
  Buffer2.prototype.writeInt16BE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 2, 32767, -32768);
    return this[offset] = value >>> 8, this[offset + 1] = value & 255, offset + 2;
  };
  Buffer2.prototype.writeInt32LE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 4, 2147483647, -2147483648);
    return this[offset] = value & 255, this[offset + 1] = value >>> 8, this[offset + 2] = value >>> 16, this[offset + 3] = value >>> 24, offset + 4;
  };
  Buffer2.prototype.writeInt32BE = function(value, offset, noAssert) {
    if (value = +value, offset = offset >>> 0, !noAssert)
      checkInt(this, value, offset, 4, 2147483647, -2147483648);
    if (value < 0)
      value = 4294967295 + value + 1;
    return this[offset] = value >>> 24, this[offset + 1] = value >>> 16, this[offset + 2] = value >>> 8, this[offset + 3] = value & 255, offset + 4;
  };
  Buffer2.prototype.writeBigInt64LE = defineBigIntMethod(function(value, offset = 0) {
    return wrtBigUInt64LE(this, value, offset, -BigInt("0x8000000000000000"), BigInt("0x7fffffffffffffff"));
  });
  Buffer2.prototype.writeBigInt64BE = defineBigIntMethod(function(value, offset = 0) {
    return wrtBigUInt64BE(this, value, offset, -BigInt("0x8000000000000000"), BigInt("0x7fffffffffffffff"));
  });
  Buffer2.prototype.writeFloatLE = function(value, offset, noAssert) {
    return writeFloat(this, value, offset, true, noAssert);
  };
  Buffer2.prototype.writeFloatBE = function(value, offset, noAssert) {
    return writeFloat(this, value, offset, false, noAssert);
  };
  Buffer2.prototype.writeDoubleLE = function(value, offset, noAssert) {
    return writeDouble(this, value, offset, true, noAssert);
  };
  Buffer2.prototype.writeDoubleBE = function(value, offset, noAssert) {
    return writeDouble(this, value, offset, false, noAssert);
  };
  Buffer2.prototype.copy = function(target, targetStart, start, end) {
    if (!Buffer2.isBuffer(target))
      throw TypeError("argument should be a Buffer");
    if (!start)
      start = 0;
    if (!end && end !== 0)
      end = this.length;
    if (targetStart >= target.length)
      targetStart = target.length;
    if (!targetStart)
      targetStart = 0;
    if (end > 0 && end < start)
      end = start;
    if (end === start)
      return 0;
    if (target.length === 0 || this.length === 0)
      return 0;
    if (targetStart < 0)
      throw RangeError("targetStart out of bounds");
    if (start < 0 || start >= this.length)
      throw RangeError("Index out of range");
    if (end < 0)
      throw RangeError("sourceEnd out of bounds");
    if (end > this.length)
      end = this.length;
    if (target.length - targetStart < end - start)
      end = target.length - targetStart + start;
    let len2 = end - start;
    if (this === target && typeof Uint8Array.prototype.copyWithin === "function")
      this.copyWithin(targetStart, start, end);
    else
      Uint8Array.prototype.set.call(target, this.subarray(start, end), targetStart);
    return len2;
  };
  Buffer2.prototype.fill = function(val, start, end, encoding) {
    if (typeof val === "string") {
      if (typeof start === "string")
        encoding = start, start = 0, end = this.length;
      else if (typeof end === "string")
        encoding = end, end = this.length;
      if (encoding !== undefined && typeof encoding !== "string")
        throw TypeError("encoding must be a string");
      if (typeof encoding === "string" && !Buffer2.isEncoding(encoding))
        throw TypeError("Unknown encoding: " + encoding);
      if (val.length === 1) {
        let code2 = val.charCodeAt(0);
        if (encoding === "utf8" && code2 < 128 || encoding === "latin1")
          val = code2;
      }
    } else if (typeof val === "number")
      val = val & 255;
    else if (typeof val === "boolean")
      val = Number(val);
    if (start < 0 || this.length < start || this.length < end)
      throw RangeError("Out of range index");
    if (end <= start)
      return this;
    if (start = start >>> 0, end = end === undefined ? this.length : end >>> 0, !val)
      val = 0;
    let i2;
    if (typeof val === "number")
      for (i2 = start;i2 < end; ++i2)
        this[i2] = val;
    else {
      let bytes = Buffer2.isBuffer(val) ? val : Buffer2.from(val, encoding), len2 = bytes.length;
      if (len2 === 0)
        throw TypeError('The value "' + val + '" is invalid for argument "value"');
      for (i2 = 0;i2 < end - start; ++i2)
        this[i2 + start] = bytes[i2 % len2];
    }
    return this;
  };
  INVALID_BASE64_RE = /[^+/0-9A-Za-z-_]/g;
  hexSliceLookupTable = function() {
    let table = Array(256);
    for (let i2 = 0;i2 < 16; ++i2) {
      let i16 = i2 * 16;
      for (let j = 0;j < 16; ++j)
        table[i16 + j] = "0123456789abcdef"[i2] + "0123456789abcdef"[j];
    }
    return table;
  }();
  resolveObjectURL = notimpl("resolveObjectURL");
  isUtf8 = notimpl("isUtf8");
  transcode = notimpl("transcode");
  buffer_default = Buffer2;
});

// node:events
var exports_events = {};
__export(exports_events, {
  setMaxListeners: () => setMaxListeners2,
  once: () => once2,
  listenerCount: () => listenerCount2,
  init: () => EventEmitter,
  getMaxListeners: () => getMaxListeners2,
  getEventListeners: () => getEventListeners,
  default: () => events_default,
  captureRejectionSymbol: () => captureRejectionSymbol,
  addAbortListener: () => addAbortListener,
  EventEmitter: () => EventEmitter
});
function emitError(emitter, args) {
  var { _events: events } = emitter;
  if (args[0] ??= Error("Unhandled error."), !events)
    throw args[0];
  var errorMonitor = events[kErrorMonitor];
  if (errorMonitor)
    for (var handler of ArrayPrototypeSlice.call(errorMonitor))
      handler.apply(emitter, args);
  var handlers = events.error;
  if (!handlers)
    throw args[0];
  for (var handler of ArrayPrototypeSlice.call(handlers))
    handler.apply(emitter, args);
  return true;
}
function addCatch(emitter, promise, type, args) {
  promise.then(undefined, function(err) {
    queueMicrotask(() => emitUnhandledRejectionOrErr(emitter, err, type, args));
  });
}
function emitUnhandledRejectionOrErr(emitter, err, type, args) {
  if (typeof emitter[kRejection] === "function")
    emitter[kRejection](err, type, ...args);
  else
    try {
      emitter[kCapture] = false, emitter.emit("error", err);
    } finally {
      emitter[kCapture] = true;
    }
}
function overflowWarning(emitter, type, handlers) {
  handlers.warned = true;
  let warn = Error(`Possible EventEmitter memory leak detected. ${handlers.length} ${String(type)} listeners added to [${emitter.constructor.name}]. Use emitter.setMaxListeners() to increase limit`);
  warn.name = "MaxListenersExceededWarning", warn.emitter = emitter, warn.type = type, warn.count = handlers.length, console.warn(warn);
}
function onceWrapper(type, listener, ...args) {
  this.removeListener(type, listener), listener.apply(this, args);
}
function once2(emitter, type, options) {
  var signal = options?.signal;
  if (validateAbortSignal(signal, "options.signal"), signal?.aborted)
    throw new AbortError(undefined, { cause: signal?.reason });
  let { resolve, reject, promise } = $newPromiseCapability(Promise), errorListener = (err) => {
    if (emitter.removeListener(type, resolver), signal != null)
      eventTargetAgnosticRemoveListener(signal, "abort", abortListener);
    reject(err);
  }, resolver = (...args) => {
    if (typeof emitter.removeListener === "function")
      emitter.removeListener("error", errorListener);
    if (signal != null)
      eventTargetAgnosticRemoveListener(signal, "abort", abortListener);
    resolve(args);
  };
  if (eventTargetAgnosticAddListener(emitter, type, resolver, { once: true }), type !== "error" && typeof emitter.once === "function")
    emitter.once("error", errorListener);
  function abortListener() {
    eventTargetAgnosticRemoveListener(emitter, type, resolver), eventTargetAgnosticRemoveListener(emitter, "error", errorListener), reject(new AbortError(undefined, { cause: signal?.reason }));
  }
  if (signal != null)
    eventTargetAgnosticAddListener(signal, "abort", abortListener, { once: true });
  return promise;
}
function getEventListeners(emitter, type) {
  return emitter.listeners(type);
}
function setMaxListeners2(n, ...eventTargets) {
  validateNumber2(n, "setMaxListeners", 0);
  var length;
  if (eventTargets && (length = eventTargets.length))
    for (let i2 = 0;i2 < length; i2++)
      eventTargets[i2].setMaxListeners(n);
  else
    defaultMaxListeners = n;
}
function listenerCount2(emitter, type) {
  return emitter.listenerCount(type);
}
function eventTargetAgnosticRemoveListener(emitter, name, listener, flags) {
  if (typeof emitter.removeListener === "function")
    emitter.removeListener(name, listener);
  else
    emitter.removeEventListener(name, listener, flags);
}
function eventTargetAgnosticAddListener(emitter, name, listener, flags) {
  if (typeof emitter.on === "function")
    if (flags.once)
      emitter.once(name, listener);
    else
      emitter.on(name, listener);
  else
    emitter.addEventListener(name, listener, flags);
}
function ERR_INVALID_ARG_TYPE2(name, type, value) {
  let err = TypeError(`The "${name}" argument must be of type ${type}. Received ${value}`);
  return err.code = "ERR_INVALID_ARG_TYPE", err;
}
function ERR_OUT_OF_RANGE2(name, range, value) {
  let err = RangeError(`The "${name}" argument is out of range. It must be ${range}. Received ${value}`);
  return err.code = "ERR_OUT_OF_RANGE", err;
}
function validateAbortSignal(signal, name) {
  if (signal !== undefined && (signal === null || typeof signal !== "object" || !("aborted" in signal)))
    throw ERR_INVALID_ARG_TYPE2(name, "AbortSignal", signal);
}
function validateNumber2(value, name, min, max) {
  if (typeof value !== "number")
    throw ERR_INVALID_ARG_TYPE2(name, "number", value);
  if (min != null && value < min || max != null && value > max || (min != null || max != null) && Number.isNaN(value))
    throw ERR_OUT_OF_RANGE2(name, `${min != null ? `>= ${min}` : ""}${min != null && max != null ? " && " : ""}${max != null ? `<= ${max}` : ""}`, value);
}
function checkListener(listener) {
  if (typeof listener !== "function")
    throw TypeError("The listener must be a function");
}
function validateBoolean(value, name) {
  if (typeof value !== "boolean")
    throw ERR_INVALID_ARG_TYPE2(name, "boolean", value);
}
function getMaxListeners2(emitterOrTarget) {
  return emitterOrTarget?._maxListeners ?? defaultMaxListeners;
}
function addAbortListener(signal, listener) {
  if (signal === undefined)
    throw ERR_INVALID_ARG_TYPE2("signal", "AbortSignal", signal);
  if (validateAbortSignal(signal, "signal"), typeof listener !== "function")
    throw ERR_INVALID_ARG_TYPE2("listener", "function", listener);
  let removeEventListener;
  if (signal.aborted)
    queueMicrotask(() => listener());
  else
    signal.addEventListener("abort", listener, { __proto__: null, once: true }), removeEventListener = () => {
      signal.removeEventListener("abort", listener);
    };
  return { __proto__: null, [Symbol.dispose]() {
    removeEventListener?.();
  } };
}
var SymbolFor, kCapture, kErrorMonitor, kMaxEventTargetListeners, kMaxEventTargetListenersWarned, kRejection, captureRejectionSymbol, ArrayPrototypeSlice, defaultMaxListeners = 10, EventEmitter = function(opts) {
  if (this._events === undefined || this._events === this.__proto__._events)
    this._events = { __proto__: null }, this._eventsCount = 0;
  if (this._maxListeners ??= undefined, this[kCapture] = opts?.captureRejections ? Boolean(opts?.captureRejections) : EventEmitterPrototype[kCapture])
    this.emit = emitWithRejectionCapture;
}, EventEmitterPrototype, emitWithoutRejectionCapture = function(type, ...args) {
  if (type === "error")
    return emitError(this, args);
  var { _events: events } = this;
  if (events === undefined)
    return false;
  var handlers = events[type];
  if (handlers === undefined)
    return false;
  let maybeClonedHandlers = handlers.length > 1 ? handlers.slice() : handlers;
  for (let i2 = 0, { length } = maybeClonedHandlers;i2 < length; i2++) {
    let handler = maybeClonedHandlers[i2];
    switch (args.length) {
      case 0:
        handler.call(this);
        break;
      case 1:
        handler.call(this, args[0]);
        break;
      case 2:
        handler.call(this, args[0], args[1]);
        break;
      case 3:
        handler.call(this, args[0], args[1], args[2]);
        break;
      default:
        handler.apply(this, args);
        break;
    }
  }
  return true;
}, emitWithRejectionCapture = function(type, ...args) {
  if (type === "error")
    return emitError(this, args);
  var { _events: events } = this;
  if (events === undefined)
    return false;
  var handlers = events[type];
  if (handlers === undefined)
    return false;
  let maybeClonedHandlers = handlers.length > 1 ? handlers.slice() : handlers;
  for (let i2 = 0, { length } = maybeClonedHandlers;i2 < length; i2++) {
    let handler = maybeClonedHandlers[i2], result;
    switch (args.length) {
      case 0:
        result = handler.call(this);
        break;
      case 1:
        result = handler.call(this, args[0]);
        break;
      case 2:
        result = handler.call(this, args[0], args[1]);
        break;
      case 3:
        result = handler.call(this, args[0], args[1], args[2]);
        break;
      default:
        result = handler.apply(this, args);
        break;
    }
    if (result !== undefined && typeof result?.then === "function" && result.then === Promise.prototype.then)
      addCatch(this, result, type, args);
  }
  return true;
}, AbortError, events_default;
var init_events = __esm(() => {
  SymbolFor = Symbol.for;
  kCapture = Symbol("kCapture");
  kErrorMonitor = SymbolFor("events.errorMonitor");
  kMaxEventTargetListeners = Symbol("events.maxEventTargetListeners");
  kMaxEventTargetListenersWarned = Symbol("events.maxEventTargetListenersWarned");
  kRejection = SymbolFor("nodejs.rejection");
  captureRejectionSymbol = SymbolFor("nodejs.rejection");
  ArrayPrototypeSlice = Array.prototype.slice;
  EventEmitterPrototype = EventEmitter.prototype = {};
  EventEmitterPrototype._events = undefined;
  EventEmitterPrototype._eventsCount = 0;
  EventEmitterPrototype._maxListeners = undefined;
  EventEmitterPrototype.setMaxListeners = function(n) {
    return validateNumber2(n, "setMaxListeners", 0), this._maxListeners = n, this;
  };
  EventEmitterPrototype.constructor = EventEmitter;
  EventEmitterPrototype.getMaxListeners = function() {
    return this?._maxListeners ?? defaultMaxListeners;
  };
  EventEmitterPrototype.emit = emitWithoutRejectionCapture;
  EventEmitterPrototype.addListener = function(type, fn) {
    checkListener(fn);
    var events = this._events;
    if (!events)
      events = this._events = { __proto__: null }, this._eventsCount = 0;
    else if (events.newListener)
      this.emit("newListener", type, fn.listener ?? fn);
    var handlers = events[type];
    if (!handlers)
      events[type] = [fn], this._eventsCount++;
    else {
      handlers.push(fn);
      var m = this._maxListeners ?? defaultMaxListeners;
      if (m > 0 && handlers.length > m && !handlers.warned)
        overflowWarning(this, type, handlers);
    }
    return this;
  };
  EventEmitterPrototype.on = EventEmitterPrototype.addListener;
  EventEmitterPrototype.prependListener = function(type, fn) {
    checkListener(fn);
    var events = this._events;
    if (!events)
      events = this._events = { __proto__: null }, this._eventsCount = 0;
    else if (events.newListener)
      this.emit("newListener", type, fn.listener ?? fn);
    var handlers = events[type];
    if (!handlers)
      events[type] = [fn], this._eventsCount++;
    else {
      handlers.unshift(fn);
      var m = this._maxListeners ?? defaultMaxListeners;
      if (m > 0 && handlers.length > m && !handlers.warned)
        overflowWarning(this, type, handlers);
    }
    return this;
  };
  EventEmitterPrototype.once = function(type, fn) {
    checkListener(fn);
    let bound = onceWrapper.bind(this, type, fn);
    return bound.listener = fn, this.addListener(type, bound), this;
  };
  EventEmitterPrototype.prependOnceListener = function(type, fn) {
    checkListener(fn);
    let bound = onceWrapper.bind(this, type, fn);
    return bound.listener = fn, this.prependListener(type, bound), this;
  };
  EventEmitterPrototype.removeListener = function(type, fn) {
    checkListener(fn);
    var { _events: events } = this;
    if (!events)
      return this;
    var handlers = events[type];
    if (!handlers)
      return this;
    var length = handlers.length;
    let position = -1;
    for (let i2 = length - 1;i2 >= 0; i2--)
      if (handlers[i2] === fn || handlers[i2].listener === fn) {
        position = i2;
        break;
      }
    if (position < 0)
      return this;
    if (position === 0)
      handlers.shift();
    else
      handlers.splice(position, 1);
    if (handlers.length === 0)
      delete events[type], this._eventsCount--;
    return this;
  };
  EventEmitterPrototype.off = EventEmitterPrototype.removeListener;
  EventEmitterPrototype.removeAllListeners = function(type) {
    var { _events: events } = this;
    if (type && events) {
      if (events[type])
        delete events[type], this._eventsCount--;
    } else
      this._events = { __proto__: null };
    return this;
  };
  EventEmitterPrototype.listeners = function(type) {
    var { _events: events } = this;
    if (!events)
      return [];
    var handlers = events[type];
    if (!handlers)
      return [];
    return handlers.map((x) => x.listener ?? x);
  };
  EventEmitterPrototype.rawListeners = function(type) {
    var { _events } = this;
    if (!_events)
      return [];
    var handlers = _events[type];
    if (!handlers)
      return [];
    return handlers.slice();
  };
  EventEmitterPrototype.listenerCount = function(type) {
    var { _events: events } = this;
    if (!events)
      return 0;
    return events[type]?.length ?? 0;
  };
  EventEmitterPrototype.eventNames = function() {
    return this._eventsCount > 0 ? Reflect.ownKeys(this._events) : [];
  };
  EventEmitterPrototype[kCapture] = false;
  AbortError = class AbortError extends Error {
    constructor(message = "The operation was aborted", options = undefined) {
      if (options !== undefined && typeof options !== "object")
        throw ERR_INVALID_ARG_TYPE2("options", "Object", options);
      super(message, options);
      this.code = "ABORT_ERR", this.name = "AbortError";
    }
  };
  Object.defineProperties(EventEmitter, { captureRejections: { get() {
    return EventEmitterPrototype[kCapture];
  }, set(value) {
    validateBoolean(value, "EventEmitter.captureRejections"), EventEmitterPrototype[kCapture] = value;
  }, enumerable: true }, defaultMaxListeners: { enumerable: true, get: () => {
    return defaultMaxListeners;
  }, set: (arg) => {
    validateNumber2(arg, "defaultMaxListeners", 0), defaultMaxListeners = arg;
  } }, kMaxEventTargetListeners: { value: kMaxEventTargetListeners, enumerable: false, configurable: false, writable: false }, kMaxEventTargetListenersWarned: { value: kMaxEventTargetListenersWarned, enumerable: false, configurable: false, writable: false } });
  Object.assign(EventEmitter, { once: once2, getEventListeners, getMaxListeners: getMaxListeners2, setMaxListeners: setMaxListeners2, EventEmitter, usingDomains: false, captureRejectionSymbol, errorMonitor: kErrorMonitor, addAbortListener, init: EventEmitter, listenerCount: listenerCount2 });
  events_default = EventEmitter;
});

// node:stream
var require_stream = __commonJS((exports, module) => {
  var __commonJS2 = (cb, mod) => () => (mod || cb((mod = { exports: {} }).exports, mod), mod.exports);
  var require_primordials = __commonJS2((exports2, module2) => {

    class AggregateError extends Error {
      constructor(errors) {
        if (!Array.isArray(errors))
          throw TypeError(`Expected input to be an Array, got ${typeof errors}`);
        let message = "";
        for (let i2 = 0;i2 < errors.length; i2++)
          message += `    ${errors[i2].stack}
`;
        super(message);
        this.name = "AggregateError", this.errors = errors;
      }
    }
    module2.exports = { AggregateError, ArrayIsArray(self2) {
      return Array.isArray(self2);
    }, ArrayPrototypeIncludes(self2, el) {
      return self2.includes(el);
    }, ArrayPrototypeIndexOf(self2, el) {
      return self2.indexOf(el);
    }, ArrayPrototypeJoin(self2, sep) {
      return self2.join(sep);
    }, ArrayPrototypeMap(self2, fn) {
      return self2.map(fn);
    }, ArrayPrototypePop(self2, el) {
      return self2.pop(el);
    }, ArrayPrototypePush(self2, el) {
      return self2.push(el);
    }, ArrayPrototypeSlice(self2, start, end) {
      return self2.slice(start, end);
    }, Error, FunctionPrototypeCall(fn, thisArgs, ...args) {
      return fn.call(thisArgs, ...args);
    }, FunctionPrototypeSymbolHasInstance(self2, instance) {
      return Function.prototype[Symbol.hasInstance].call(self2, instance);
    }, MathFloor: Math.floor, Number, NumberIsInteger: Number.isInteger, NumberIsNaN: Number.isNaN, NumberMAX_SAFE_INTEGER: Number.MAX_SAFE_INTEGER, NumberMIN_SAFE_INTEGER: Number.MIN_SAFE_INTEGER, NumberParseInt: Number.parseInt, ObjectDefineProperties(self2, props) {
      return Object.defineProperties(self2, props);
    }, ObjectDefineProperty(self2, name, prop) {
      return Object.defineProperty(self2, name, prop);
    }, ObjectGetOwnPropertyDescriptor(self2, name) {
      return Object.getOwnPropertyDescriptor(self2, name);
    }, ObjectKeys(obj) {
      return Object.keys(obj);
    }, ObjectSetPrototypeOf(target, proto) {
      return Object.setPrototypeOf(target, proto);
    }, Promise, PromisePrototypeCatch(self2, fn) {
      return self2.catch(fn);
    }, PromisePrototypeThen(self2, thenFn, catchFn) {
      return self2.then(thenFn, catchFn);
    }, PromiseReject(err) {
      return Promise.reject(err);
    }, PromiseResolve(val) {
      return Promise.resolve(val);
    }, ReflectApply: Reflect.apply, RegExpPrototypeTest(self2, value) {
      return self2.test(value);
    }, SafeSet: Set, String, StringPrototypeSlice(self2, start, end) {
      return self2.slice(start, end);
    }, StringPrototypeToLowerCase(self2) {
      return self2.toLowerCase();
    }, StringPrototypeToUpperCase(self2) {
      return self2.toUpperCase();
    }, StringPrototypeTrim(self2) {
      return self2.trim();
    }, Symbol, SymbolFor: Symbol.for, SymbolAsyncIterator: Symbol.asyncIterator, SymbolHasInstance: Symbol.hasInstance, SymbolIterator: Symbol.iterator, SymbolDispose: Symbol.dispose || Symbol("Symbol.dispose"), SymbolAsyncDispose: Symbol.asyncDispose || Symbol("Symbol.asyncDispose"), TypedArrayPrototypeSet(self2, buf, len2) {
      return self2.set(buf, len2);
    }, Boolean, Uint8Array };
  });
  var require_inspect = __commonJS2((exports2, module2) => {
    module2.exports = { format(format, ...args) {
      return format.replace(/%([sdifj])/g, function(...[_unused, type]) {
        let replacement = args.shift();
        if (type === "f")
          return replacement.toFixed(6);
        else if (type === "j")
          return JSON.stringify(replacement);
        else if (type === "s" && typeof replacement === "object")
          return `${replacement.constructor !== Object ? replacement.constructor.name : ""} {}`.trim();
        else
          return replacement.toString();
      });
    }, inspect(value) {
      switch (typeof value) {
        case "string":
          if (value.includes("'")) {
            if (!value.includes('"'))
              return `"${value}"`;
            else if (!value.includes("`") && !value.includes("${"))
              return `\`${value}\``;
          }
          return `'${value}'`;
        case "number":
          if (isNaN(value))
            return "NaN";
          else if (Object.is(value, -0))
            return String(value);
          return value;
        case "bigint":
          return `${String(value)}n`;
        case "boolean":
        case "undefined":
          return String(value);
        case "object":
          return "{}";
      }
    } };
  });
  var require_errors = __commonJS2((exports2, module2) => {
    var { format, inspect } = require_inspect(), { AggregateError: CustomAggregateError } = require_primordials(), AggregateError = globalThis.AggregateError || CustomAggregateError, kIsNodeError = Symbol("kIsNodeError"), kTypes = ["string", "function", "number", "object", "Function", "Object", "boolean", "bigint", "symbol"], classRegExp = /^([A-Z][a-z0-9]*)+$/, codes = {};
    function assert(value, message) {
      if (!value)
        throw new codes.ERR_INTERNAL_ASSERTION(message);
    }
    function addNumericalSeparator2(val) {
      let res = "", i2 = val.length, start = val[0] === "-" ? 1 : 0;
      for (;i2 >= start + 4; i2 -= 3)
        res = `_${val.slice(i2 - 3, i2)}${res}`;
      return `${val.slice(0, i2)}${res}`;
    }
    function getMessage(key, msg, args) {
      if (typeof msg === "function")
        return assert(msg.length <= args.length, `Code: ${key}; The provided arguments length (${args.length}) does not match the required ones (${msg.length}).`), msg(...args);
      let expectedLength = (msg.match(/%[dfijoOs]/g) || []).length;
      if (assert(expectedLength === args.length, `Code: ${key}; The provided arguments length (${args.length}) does not match the required ones (${expectedLength}).`), args.length === 0)
        return msg;
      return format(msg, ...args);
    }
    function E2(code2, message, Base) {
      if (!Base)
        Base = Error;

      class NodeError extends Base {
        constructor(...args) {
          super(getMessage(code2, message, args));
        }
        toString() {
          return `${this.name} [${code2}]: ${this.message}`;
        }
      }
      Object.defineProperties(NodeError.prototype, { name: { value: Base.name, writable: true, enumerable: false, configurable: true }, toString: { value() {
        return `${this.name} [${code2}]: ${this.message}`;
      }, writable: true, enumerable: false, configurable: true } }), NodeError.prototype.code = code2, NodeError.prototype[kIsNodeError] = true, codes[code2] = NodeError;
    }
    function hideStackFrames(fn) {
      let hidden = "__node_internal_" + fn.name;
      return Object.defineProperty(fn, "name", { value: hidden }), fn;
    }
    function aggregateTwoErrors(innerError, outerError) {
      if (innerError && outerError && innerError !== outerError) {
        if (Array.isArray(outerError.errors))
          return outerError.errors.push(innerError), outerError;
        let err = new AggregateError([outerError, innerError], outerError.message);
        return err.code = outerError.code, err;
      }
      return innerError || outerError;
    }

    class AbortError2 extends Error {
      constructor(message = "The operation was aborted", options = undefined) {
        if (options !== undefined && typeof options !== "object")
          throw new codes.ERR_INVALID_ARG_TYPE("options", "Object", options);
        super(message, options);
        this.code = "ABORT_ERR", this.name = "AbortError";
      }
    }
    E2("ERR_ASSERTION", "%s", Error);
    E2("ERR_INVALID_ARG_TYPE", (name, expected, actual) => {
      if (assert(typeof name === "string", "'name' must be a string"), !Array.isArray(expected))
        expected = [expected];
      let msg = "The ";
      if (name.endsWith(" argument"))
        msg += `${name} `;
      else
        msg += `"${name}" ${name.includes(".") ? "property" : "argument"} `;
      msg += "must be ";
      let types = [], instances = [], other = [];
      for (let value of expected)
        if (assert(typeof value === "string", "All expected entries have to be of type string"), kTypes.includes(value))
          types.push(value.toLowerCase());
        else if (classRegExp.test(value))
          instances.push(value);
        else
          assert(value !== "object", 'The value "object" should be written as "Object"'), other.push(value);
      if (instances.length > 0) {
        let pos = types.indexOf("object");
        if (pos !== -1)
          types.splice(types, pos, 1), instances.push("Object");
      }
      if (types.length > 0) {
        switch (types.length) {
          case 1:
            msg += `of type ${types[0]}`;
            break;
          case 2:
            msg += `one of type ${types[0]} or ${types[1]}`;
            break;
          default: {
            let last = types.pop();
            msg += `one of type ${types.join(", ")}, or ${last}`;
          }
        }
        if (instances.length > 0 || other.length > 0)
          msg += " or ";
      }
      if (instances.length > 0) {
        switch (instances.length) {
          case 1:
            msg += `an instance of ${instances[0]}`;
            break;
          case 2:
            msg += `an instance of ${instances[0]} or ${instances[1]}`;
            break;
          default: {
            let last = instances.pop();
            msg += `an instance of ${instances.join(", ")}, or ${last}`;
          }
        }
        if (other.length > 0)
          msg += " or ";
      }
      switch (other.length) {
        case 0:
          break;
        case 1:
          if (other[0].toLowerCase() !== other[0])
            msg += "an ";
          msg += `${other[0]}`;
          break;
        case 2:
          msg += `one of ${other[0]} or ${other[1]}`;
          break;
        default: {
          let last = other.pop();
          msg += `one of ${other.join(", ")}, or ${last}`;
        }
      }
      if (actual == null)
        msg += `. Received ${actual}`;
      else if (typeof actual === "function" && actual.name)
        msg += `. Received function ${actual.name}`;
      else if (typeof actual === "object") {
        var _actual$constructor;
        if ((_actual$constructor = actual.constructor) !== null && _actual$constructor !== undefined && _actual$constructor.name)
          msg += `. Received an instance of ${actual.constructor.name}`;
        else {
          let inspected = inspect(actual, { depth: -1 });
          msg += `. Received ${inspected}`;
        }
      } else {
        let inspected = inspect(actual, { colors: false });
        if (inspected.length > 25)
          inspected = `${inspected.slice(0, 25)}...`;
        msg += `. Received type ${typeof actual} (${inspected})`;
      }
      return msg;
    }, TypeError);
    E2("ERR_INVALID_ARG_VALUE", (name, value, reason = "is invalid") => {
      let inspected = inspect(value);
      if (inspected.length > 128)
        inspected = inspected.slice(0, 128) + "...";
      return `The ${name.includes(".") ? "property" : "argument"} '${name}' ${reason}. Received ${inspected}`;
    }, TypeError);
    E2("ERR_INVALID_RETURN_VALUE", (input, name, value) => {
      var _value$constructor;
      let type = value !== null && value !== undefined && (_value$constructor = value.constructor) !== null && _value$constructor !== undefined && _value$constructor.name ? `instance of ${value.constructor.name}` : `type ${typeof value}`;
      return `Expected ${input} to be returned from the "${name}" function but got ${type}.`;
    }, TypeError);
    E2("ERR_MISSING_ARGS", (...args) => {
      assert(args.length > 0, "At least one arg needs to be specified");
      let msg, len2 = args.length;
      switch (args = (Array.isArray(args) ? args : [args]).map((a) => `"${a}"`).join(" or "), len2) {
        case 1:
          msg += `The ${args[0]} argument`;
          break;
        case 2:
          msg += `The ${args[0]} and ${args[1]} arguments`;
          break;
        default:
          {
            let last = args.pop();
            msg += `The ${args.join(", ")}, and ${last} arguments`;
          }
          break;
      }
      return `${msg} must be specified`;
    }, TypeError);
    E2("ERR_OUT_OF_RANGE", (str, range, input) => {
      assert(range, 'Missing "range" argument');
      let received;
      if (Number.isInteger(input) && Math.abs(input) > 4294967296)
        received = addNumericalSeparator2(String(input));
      else if (typeof input === "bigint") {
        received = String(input);
        let limit = BigInt(2) ** BigInt(32);
        if (input > limit || input < -limit)
          received = addNumericalSeparator2(received);
        received += "n";
      } else
        received = inspect(input);
      return `The value of "${str}" is out of range. It must be ${range}. Received ${received}`;
    }, RangeError);
    E2("ERR_MULTIPLE_CALLBACK", "Callback called multiple times", Error);
    E2("ERR_METHOD_NOT_IMPLEMENTED", "The %s method is not implemented", Error);
    E2("ERR_STREAM_ALREADY_FINISHED", "Cannot call %s after a stream was finished", Error);
    E2("ERR_STREAM_CANNOT_PIPE", "Cannot pipe, not readable", Error);
    E2("ERR_STREAM_DESTROYED", "Cannot call %s after a stream was destroyed", Error);
    E2("ERR_STREAM_NULL_VALUES", "May not write null values to stream", TypeError);
    E2("ERR_STREAM_PREMATURE_CLOSE", "Premature close", Error);
    E2("ERR_STREAM_PUSH_AFTER_EOF", "stream.push() after EOF", Error);
    E2("ERR_STREAM_UNSHIFT_AFTER_END_EVENT", "stream.unshift() after end event", Error);
    E2("ERR_STREAM_WRITE_AFTER_END", "write after end", Error);
    E2("ERR_UNKNOWN_ENCODING", "Unknown encoding: %s", TypeError);
    module2.exports = { AbortError: AbortError2, aggregateTwoErrors: hideStackFrames(aggregateTwoErrors), hideStackFrames, codes };
  });
  var require_event_target_shim = __commonJS2((exports2, module2) => {
    Object.defineProperty(exports2, "__esModule", { value: true });
    var privateData = new WeakMap, wrappers = new WeakMap;
    function pd(event) {
      let retv = privateData.get(event);
      return console.assert(retv != null, "'this' is expected an Event object, but got", event), retv;
    }
    function setCancelFlag(data) {
      if (data.passiveListener != null) {
        if (typeof console < "u" && typeof console.error === "function")
          console.error("Unable to preventDefault inside passive event listener invocation.", data.passiveListener);
        return;
      }
      if (!data.event.cancelable)
        return;
      if (data.canceled = true, typeof data.event.preventDefault === "function")
        data.event.preventDefault();
    }
    function Event(eventTarget, event) {
      privateData.set(this, { eventTarget, event, eventPhase: 2, currentTarget: eventTarget, canceled: false, stopped: false, immediateStopped: false, passiveListener: null, timeStamp: event.timeStamp || Date.now() }), Object.defineProperty(this, "isTrusted", { value: false, enumerable: true });
      let keys = Object.keys(event);
      for (let i2 = 0;i2 < keys.length; ++i2) {
        let key = keys[i2];
        if (!(key in this))
          Object.defineProperty(this, key, defineRedirectDescriptor(key));
      }
    }
    Event.prototype = { get type() {
      return pd(this).event.type;
    }, get target() {
      return pd(this).eventTarget;
    }, get currentTarget() {
      return pd(this).currentTarget;
    }, composedPath() {
      let currentTarget = pd(this).currentTarget;
      if (currentTarget == null)
        return [];
      return [currentTarget];
    }, get NONE() {
      return 0;
    }, get CAPTURING_PHASE() {
      return 1;
    }, get AT_TARGET() {
      return 2;
    }, get BUBBLING_PHASE() {
      return 3;
    }, get eventPhase() {
      return pd(this).eventPhase;
    }, stopPropagation() {
      let data = pd(this);
      if (data.stopped = true, typeof data.event.stopPropagation === "function")
        data.event.stopPropagation();
    }, stopImmediatePropagation() {
      let data = pd(this);
      if (data.stopped = true, data.immediateStopped = true, typeof data.event.stopImmediatePropagation === "function")
        data.event.stopImmediatePropagation();
    }, get bubbles() {
      return Boolean(pd(this).event.bubbles);
    }, get cancelable() {
      return Boolean(pd(this).event.cancelable);
    }, preventDefault() {
      setCancelFlag(pd(this));
    }, get defaultPrevented() {
      return pd(this).canceled;
    }, get composed() {
      return Boolean(pd(this).event.composed);
    }, get timeStamp() {
      return pd(this).timeStamp;
    }, get srcElement() {
      return pd(this).eventTarget;
    }, get cancelBubble() {
      return pd(this).stopped;
    }, set cancelBubble(value) {
      if (!value)
        return;
      let data = pd(this);
      if (data.stopped = true, typeof data.event.cancelBubble === "boolean")
        data.event.cancelBubble = true;
    }, get returnValue() {
      return !pd(this).canceled;
    }, set returnValue(value) {
      if (!value)
        setCancelFlag(pd(this));
    }, initEvent() {} };
    Object.defineProperty(Event.prototype, "constructor", { value: Event, configurable: true, writable: true });
    if (typeof window < "u" && typeof window.Event < "u")
      Object.setPrototypeOf(Event.prototype, window.Event.prototype), wrappers.set(window.Event.prototype, Event);
    function defineRedirectDescriptor(key) {
      return { get() {
        return pd(this).event[key];
      }, set(value) {
        pd(this).event[key] = value;
      }, configurable: true, enumerable: true };
    }
    function defineCallDescriptor(key) {
      return { value() {
        let event = pd(this).event;
        return event[key].apply(event, arguments);
      }, configurable: true, enumerable: true };
    }
    function defineWrapper(BaseEvent, proto) {
      let keys = Object.keys(proto);
      if (keys.length === 0)
        return BaseEvent;
      function CustomEvent(eventTarget, event) {
        BaseEvent.call(this, eventTarget, event);
      }
      CustomEvent.prototype = Object.create(BaseEvent.prototype, { constructor: { value: CustomEvent, configurable: true, writable: true } });
      for (let i2 = 0;i2 < keys.length; ++i2) {
        let key = keys[i2];
        if (!(key in BaseEvent.prototype)) {
          let isFunc = typeof Object.getOwnPropertyDescriptor(proto, key).value === "function";
          Object.defineProperty(CustomEvent.prototype, key, isFunc ? defineCallDescriptor(key) : defineRedirectDescriptor(key));
        }
      }
      return CustomEvent;
    }
    function getWrapper(proto) {
      if (proto == null || proto === Object.prototype)
        return Event;
      let wrapper = wrappers.get(proto);
      if (wrapper == null)
        wrapper = defineWrapper(getWrapper(Object.getPrototypeOf(proto)), proto), wrappers.set(proto, wrapper);
      return wrapper;
    }
    function wrapEvent(eventTarget, event) {
      return new (getWrapper(Object.getPrototypeOf(event)))(eventTarget, event);
    }
    function isStopped(event) {
      return pd(event).immediateStopped;
    }
    function setEventPhase(event, eventPhase) {
      pd(event).eventPhase = eventPhase;
    }
    function setCurrentTarget(event, currentTarget) {
      pd(event).currentTarget = currentTarget;
    }
    function setPassiveListener(event, passiveListener) {
      pd(event).passiveListener = passiveListener;
    }
    var listenersMap = new WeakMap, CAPTURE = 1, BUBBLE = 2, ATTRIBUTE = 3;
    function isObject(x) {
      return x !== null && typeof x === "object";
    }
    function getListeners(eventTarget) {
      let listeners = listenersMap.get(eventTarget);
      if (listeners == null)
        throw TypeError("'this' is expected an EventTarget object, but got another value.");
      return listeners;
    }
    function defineEventAttributeDescriptor(eventName) {
      return { get() {
        let node = getListeners(this).get(eventName);
        while (node != null) {
          if (node.listenerType === ATTRIBUTE)
            return node.listener;
          node = node.next;
        }
        return null;
      }, set(listener) {
        if (typeof listener !== "function" && !isObject(listener))
          listener = null;
        let listeners = getListeners(this), prev = null, node = listeners.get(eventName);
        while (node != null) {
          if (node.listenerType === ATTRIBUTE)
            if (prev !== null)
              prev.next = node.next;
            else if (node.next !== null)
              listeners.set(eventName, node.next);
            else
              listeners.delete(eventName);
          else
            prev = node;
          node = node.next;
        }
        if (listener !== null) {
          let newNode = { listener, listenerType: ATTRIBUTE, passive: false, once: false, next: null };
          if (prev === null)
            listeners.set(eventName, newNode);
          else
            prev.next = newNode;
        }
      }, configurable: true, enumerable: true };
    }
    function defineEventAttribute(eventTargetPrototype, eventName) {
      Object.defineProperty(eventTargetPrototype, `on${eventName}`, defineEventAttributeDescriptor(eventName));
    }
    function defineCustomEventTarget(eventNames) {
      function CustomEventTarget() {
        EventTarget.call(this);
      }
      CustomEventTarget.prototype = Object.create(EventTarget.prototype, { constructor: { value: CustomEventTarget, configurable: true, writable: true } });
      for (let i2 = 0;i2 < eventNames.length; ++i2)
        defineEventAttribute(CustomEventTarget.prototype, eventNames[i2]);
      return CustomEventTarget;
    }
    function EventTarget() {
      if (this instanceof EventTarget) {
        listenersMap.set(this, new Map);
        return;
      }
      if (arguments.length === 1 && Array.isArray(arguments[0]))
        return defineCustomEventTarget(arguments[0]);
      if (arguments.length > 0) {
        let types = Array(arguments.length);
        for (let i2 = 0;i2 < arguments.length; ++i2)
          types[i2] = arguments[i2];
        return defineCustomEventTarget(types);
      }
      throw TypeError("Cannot call a class as a function");
    }
    EventTarget.prototype = { addEventListener(eventName, listener, options) {
      if (listener == null)
        return;
      if (typeof listener !== "function" && !isObject(listener))
        throw TypeError("'listener' should be a function or an object.");
      let listeners = getListeners(this), optionsIsObj = isObject(options), listenerType = (optionsIsObj ? Boolean(options.capture) : Boolean(options)) ? CAPTURE : BUBBLE, newNode = { listener, listenerType, passive: optionsIsObj && Boolean(options.passive), once: optionsIsObj && Boolean(options.once), next: null }, node = listeners.get(eventName);
      if (node === undefined) {
        listeners.set(eventName, newNode);
        return;
      }
      let prev = null;
      while (node != null) {
        if (node.listener === listener && node.listenerType === listenerType)
          return;
        prev = node, node = node.next;
      }
      prev.next = newNode;
    }, removeEventListener(eventName, listener, options) {
      if (listener == null)
        return;
      let listeners = getListeners(this), listenerType = (isObject(options) ? Boolean(options.capture) : Boolean(options)) ? CAPTURE : BUBBLE, prev = null, node = listeners.get(eventName);
      while (node != null) {
        if (node.listener === listener && node.listenerType === listenerType) {
          if (prev !== null)
            prev.next = node.next;
          else if (node.next !== null)
            listeners.set(eventName, node.next);
          else
            listeners.delete(eventName);
          return;
        }
        prev = node, node = node.next;
      }
    }, dispatchEvent(event) {
      if (event == null || typeof event.type !== "string")
        throw TypeError('"event.type" should be a string.');
      let listeners = getListeners(this), eventName = event.type, node = listeners.get(eventName);
      if (node == null)
        return true;
      let wrappedEvent = wrapEvent(this, event), prev = null;
      while (node != null) {
        if (node.once)
          if (prev !== null)
            prev.next = node.next;
          else if (node.next !== null)
            listeners.set(eventName, node.next);
          else
            listeners.delete(eventName);
        else
          prev = node;
        if (setPassiveListener(wrappedEvent, node.passive ? node.listener : null), typeof node.listener === "function")
          try {
            node.listener.call(this, wrappedEvent);
          } catch (err) {
            if (typeof console < "u" && typeof console.error === "function")
              console.error(err);
          }
        else if (node.listenerType !== ATTRIBUTE && typeof node.listener.handleEvent === "function")
          node.listener.handleEvent(wrappedEvent);
        if (isStopped(wrappedEvent))
          break;
        node = node.next;
      }
      return setPassiveListener(wrappedEvent, null), setEventPhase(wrappedEvent, 0), setCurrentTarget(wrappedEvent, null), !wrappedEvent.defaultPrevented;
    } };
    Object.defineProperty(EventTarget.prototype, "constructor", { value: EventTarget, configurable: true, writable: true });
    if (typeof window < "u" && typeof window.EventTarget < "u")
      Object.setPrototypeOf(EventTarget.prototype, window.EventTarget.prototype);
    exports2.defineEventAttribute = defineEventAttribute;
    exports2.EventTarget = EventTarget;
    exports2.default = EventTarget;
    module2.exports = EventTarget;
    module2.exports.EventTarget = module2.exports.default = EventTarget;
    module2.exports.defineEventAttribute = defineEventAttribute;
  });
  var require_abort_controller = __commonJS2((exports2, module2) => {
    Object.defineProperty(exports2, "__esModule", { value: true });
    var eventTargetShim = require_event_target_shim();

    class AbortSignal extends eventTargetShim.EventTarget {
      constructor() {
        super();
        throw TypeError("AbortSignal cannot be constructed directly");
      }
      get aborted() {
        let aborted = abortedFlags.get(this);
        if (typeof aborted !== "boolean")
          throw TypeError(`Expected 'this' to be an 'AbortSignal' object, but got ${this === null ? "null" : typeof this}`);
        return aborted;
      }
    }
    eventTargetShim.defineEventAttribute(AbortSignal.prototype, "abort");
    function createAbortSignal() {
      let signal = Object.create(AbortSignal.prototype);
      return eventTargetShim.EventTarget.call(signal), abortedFlags.set(signal, false), signal;
    }
    function abortSignal(signal) {
      if (abortedFlags.get(signal) !== false)
        return;
      abortedFlags.set(signal, true), signal.dispatchEvent({ type: "abort" });
    }
    var abortedFlags = new WeakMap;
    Object.defineProperties(AbortSignal.prototype, { aborted: { enumerable: true } });
    if (typeof Symbol === "function" && typeof Symbol.toStringTag === "symbol")
      Object.defineProperty(AbortSignal.prototype, Symbol.toStringTag, { configurable: true, value: "AbortSignal" });

    class AbortController2 {
      constructor() {
        signals.set(this, createAbortSignal());
      }
      get signal() {
        return getSignal(this);
      }
      abort() {
        abortSignal(getSignal(this));
      }
    }
    var signals = new WeakMap;
    function getSignal(controller) {
      let signal = signals.get(controller);
      if (signal == null)
        throw TypeError(`Expected 'this' to be an 'AbortController' object, but got ${controller === null ? "null" : typeof controller}`);
      return signal;
    }
    Object.defineProperties(AbortController2.prototype, { signal: { enumerable: true }, abort: { enumerable: true } });
    if (typeof Symbol === "function" && typeof Symbol.toStringTag === "symbol")
      Object.defineProperty(AbortController2.prototype, Symbol.toStringTag, { configurable: true, value: "AbortController" });
    exports2.AbortController = AbortController2;
    exports2.AbortSignal = AbortSignal;
    exports2.default = AbortController2;
    module2.exports = AbortController2;
    module2.exports.AbortController = module2.exports.default = AbortController2;
    module2.exports.AbortSignal = AbortSignal;
  });
  var require_util = __commonJS2((exports2, module2) => {
    var bufferModule = (init_buffer(), __toCommonJS(exports_buffer)), { format, inspect } = require_inspect(), { codes: { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3 } } = require_errors(), { kResistStopPropagation, AggregateError, SymbolDispose } = require_primordials(), AbortSignal = globalThis.AbortSignal || require_abort_controller().AbortSignal, AbortController2 = globalThis.AbortController || require_abort_controller().AbortController, AsyncFunction = Object.getPrototypeOf(async function() {}).constructor, Blob3 = globalThis.Blob || bufferModule.Blob, isBlob = typeof Blob3 < "u" ? function(b) {
      return b instanceof Blob3;
    } : function(b) {
      return false;
    }, validateAbortSignal2 = (signal, name) => {
      if (signal !== undefined && (signal === null || typeof signal !== "object" || !("aborted" in signal)))
        throw new ERR_INVALID_ARG_TYPE3(name, "AbortSignal", signal);
    }, validateFunction = (value, name) => {
      if (typeof value !== "function")
        throw new ERR_INVALID_ARG_TYPE3(name, "Function", value);
    };
    module2.exports = { AggregateError, kEmptyObject: Object.freeze({}), once(callback) {
      let called = false;
      return function(...args) {
        if (called)
          return;
        called = true, callback.apply(this, args);
      };
    }, createDeferredPromise: function() {
      let resolve, reject;
      return { promise: new Promise((res, rej) => {
        resolve = res, reject = rej;
      }), resolve, reject };
    }, promisify(fn) {
      return new Promise((resolve, reject) => {
        fn((err, ...args) => {
          if (err)
            return reject(err);
          return resolve(...args);
        });
      });
    }, debuglog() {
      return function() {};
    }, format, inspect, types: { isAsyncFunction(fn) {
      return fn instanceof AsyncFunction;
    }, isArrayBufferView(arr) {
      return ArrayBuffer.isView(arr);
    } }, isBlob, deprecate(fn, message) {
      return fn;
    }, addAbortListener: (init_events(), __toCommonJS(exports_events)).addAbortListener || function(signal, listener) {
      if (signal === undefined)
        throw new ERR_INVALID_ARG_TYPE3("signal", "AbortSignal", signal);
      validateAbortSignal2(signal, "signal"), validateFunction(listener, "listener");
      let removeEventListener;
      if (signal.aborted)
        queueMicrotask(() => listener());
      else
        signal.addEventListener("abort", listener, { __proto__: null, once: true, [kResistStopPropagation]: true }), removeEventListener = () => {
          signal.removeEventListener("abort", listener);
        };
      return { __proto__: null, [SymbolDispose]() {
        var _removeEventListener;
        (_removeEventListener = removeEventListener) === null || _removeEventListener === undefined || _removeEventListener();
      } };
    }, AbortSignalAny: AbortSignal.any || function(signals) {
      if (signals.length === 1)
        return signals[0];
      let ac = new AbortController2, abort = () => ac.abort();
      return signals.forEach((signal) => {
        validateAbortSignal2(signal, "signals"), signal.addEventListener("abort", abort, { once: true });
      }), ac.signal.addEventListener("abort", () => {
        signals.forEach((signal) => signal.removeEventListener("abort", abort));
      }, { once: true }), ac.signal;
    } };
    module2.exports.promisify.custom = Symbol.for("nodejs.util.promisify.custom");
  });
  var require_validators = __commonJS2((exports2, module2) => {
    var { ArrayIsArray, ArrayPrototypeIncludes, ArrayPrototypeJoin, ArrayPrototypeMap, NumberIsInteger, NumberIsNaN, NumberMAX_SAFE_INTEGER, NumberMIN_SAFE_INTEGER, NumberParseInt, ObjectPrototypeHasOwnProperty, RegExpPrototypeExec, String: String2, StringPrototypeToUpperCase, StringPrototypeTrim } = require_primordials(), { hideStackFrames, codes: { ERR_SOCKET_BAD_PORT, ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_INVALID_ARG_VALUE, ERR_OUT_OF_RANGE: ERR_OUT_OF_RANGE3, ERR_UNKNOWN_SIGNAL } } = require_errors(), { normalizeEncoding } = require_util(), { isAsyncFunction, isArrayBufferView } = require_util().types, signals = {};
    function isInt32(value) {
      return value === (value | 0);
    }
    function isUint32(value) {
      return value === value >>> 0;
    }
    var octalReg = /^[0-7]+$/, modeDesc = "must be a 32-bit unsigned integer or an octal string";
    function parseFileMode(value, name, def) {
      if (typeof value > "u")
        value = def;
      if (typeof value === "string") {
        if (RegExpPrototypeExec(octalReg, value) === null)
          throw new ERR_INVALID_ARG_VALUE(name, value, modeDesc);
        value = NumberParseInt(value, 8);
      }
      return validateUint32(value, name), value;
    }
    var validateInteger = hideStackFrames((value, name, min = NumberMIN_SAFE_INTEGER, max = NumberMAX_SAFE_INTEGER) => {
      if (typeof value !== "number")
        throw new ERR_INVALID_ARG_TYPE3(name, "number", value);
      if (!NumberIsInteger(value))
        throw new ERR_OUT_OF_RANGE3(name, "an integer", value);
      if (value < min || value > max)
        throw new ERR_OUT_OF_RANGE3(name, `>= ${min} && <= ${max}`, value);
    }), validateInt32 = hideStackFrames((value, name, min = -2147483648, max = 2147483647) => {
      if (typeof value !== "number")
        throw new ERR_INVALID_ARG_TYPE3(name, "number", value);
      if (!NumberIsInteger(value))
        throw new ERR_OUT_OF_RANGE3(name, "an integer", value);
      if (value < min || value > max)
        throw new ERR_OUT_OF_RANGE3(name, `>= ${min} && <= ${max}`, value);
    }), validateUint32 = hideStackFrames((value, name, positive = false) => {
      if (typeof value !== "number")
        throw new ERR_INVALID_ARG_TYPE3(name, "number", value);
      if (!NumberIsInteger(value))
        throw new ERR_OUT_OF_RANGE3(name, "an integer", value);
      let min = positive ? 1 : 0, max = 4294967295;
      if (value < min || value > max)
        throw new ERR_OUT_OF_RANGE3(name, `>= ${min} && <= ${max}`, value);
    });
    function validateString(value, name) {
      if (typeof value !== "string")
        throw new ERR_INVALID_ARG_TYPE3(name, "string", value);
    }
    function validateNumber3(value, name, min = undefined, max) {
      if (typeof value !== "number")
        throw new ERR_INVALID_ARG_TYPE3(name, "number", value);
      if (min != null && value < min || max != null && value > max || (min != null || max != null) && NumberIsNaN(value))
        throw new ERR_OUT_OF_RANGE3(name, `${min != null ? `>= ${min}` : ""}${min != null && max != null ? " && " : ""}${max != null ? `<= ${max}` : ""}`, value);
    }
    var validateOneOf = hideStackFrames((value, name, oneOf) => {
      if (!ArrayPrototypeIncludes(oneOf, value)) {
        let reason = "must be one of: " + ArrayPrototypeJoin(ArrayPrototypeMap(oneOf, (v) => typeof v === "string" ? `'${v}'` : String2(v)), ", ");
        throw new ERR_INVALID_ARG_VALUE(name, value, reason);
      }
    });
    function validateBoolean2(value, name) {
      if (typeof value !== "boolean")
        throw new ERR_INVALID_ARG_TYPE3(name, "boolean", value);
    }
    function getOwnPropertyValueOrDefault(options, key, defaultValue) {
      return options == null || !ObjectPrototypeHasOwnProperty(options, key) ? defaultValue : options[key];
    }
    var validateObject = hideStackFrames((value, name, options = null) => {
      let allowArray = getOwnPropertyValueOrDefault(options, "allowArray", false), allowFunction = getOwnPropertyValueOrDefault(options, "allowFunction", false);
      if (!getOwnPropertyValueOrDefault(options, "nullable", false) && value === null || !allowArray && ArrayIsArray(value) || typeof value !== "object" && (!allowFunction || typeof value !== "function"))
        throw new ERR_INVALID_ARG_TYPE3(name, "Object", value);
    }), validateDictionary = hideStackFrames((value, name) => {
      if (value != null && typeof value !== "object" && typeof value !== "function")
        throw new ERR_INVALID_ARG_TYPE3(name, "a dictionary", value);
    }), validateArray = hideStackFrames((value, name, minLength = 0) => {
      if (!ArrayIsArray(value))
        throw new ERR_INVALID_ARG_TYPE3(name, "Array", value);
      if (value.length < minLength) {
        let reason = `must be longer than ${minLength}`;
        throw new ERR_INVALID_ARG_VALUE(name, value, reason);
      }
    });
    function validateStringArray(value, name) {
      validateArray(value, name);
      for (let i2 = 0;i2 < value.length; i2++)
        validateString(value[i2], `${name}[${i2}]`);
    }
    function validateBooleanArray(value, name) {
      validateArray(value, name);
      for (let i2 = 0;i2 < value.length; i2++)
        validateBoolean2(value[i2], `${name}[${i2}]`);
    }
    function validateAbortSignalArray(value, name) {
      validateArray(value, name);
      for (let i2 = 0;i2 < value.length; i2++) {
        let signal = value[i2], indexedName = `${name}[${i2}]`;
        if (signal == null)
          throw new ERR_INVALID_ARG_TYPE3(indexedName, "AbortSignal", signal);
        validateAbortSignal2(signal, indexedName);
      }
    }
    function validateSignalName(signal, name = "signal") {
      if (validateString(signal, name), signals[signal] === undefined) {
        if (signals[StringPrototypeToUpperCase(signal)] !== undefined)
          throw new ERR_UNKNOWN_SIGNAL(signal + " (signals must use all capital letters)");
        throw new ERR_UNKNOWN_SIGNAL(signal);
      }
    }
    var validateBuffer = hideStackFrames((buffer, name = "buffer") => {
      if (!isArrayBufferView(buffer))
        throw new ERR_INVALID_ARG_TYPE3(name, ["Buffer", "TypedArray", "DataView"], buffer);
    });
    function validateEncoding(data, encoding) {
      let normalizedEncoding = normalizeEncoding(encoding), length = data.length;
      if (normalizedEncoding === "hex" && length % 2 !== 0)
        throw new ERR_INVALID_ARG_VALUE("encoding", encoding, `is invalid for data of length ${length}`);
    }
    function validatePort(port, name = "Port", allowZero = true) {
      if (typeof port !== "number" && typeof port !== "string" || typeof port === "string" && StringPrototypeTrim(port).length === 0 || +port !== +port >>> 0 || port > 65535 || port === 0 && !allowZero)
        throw new ERR_SOCKET_BAD_PORT(name, port, allowZero);
      return port | 0;
    }
    var validateAbortSignal2 = hideStackFrames((signal, name) => {
      if (signal !== undefined && (signal === null || typeof signal !== "object" || !("aborted" in signal)))
        throw new ERR_INVALID_ARG_TYPE3(name, "AbortSignal", signal);
    }), validateFunction = hideStackFrames((value, name) => {
      if (typeof value !== "function")
        throw new ERR_INVALID_ARG_TYPE3(name, "Function", value);
    }), validatePlainFunction = hideStackFrames((value, name) => {
      if (typeof value !== "function" || isAsyncFunction(value))
        throw new ERR_INVALID_ARG_TYPE3(name, "Function", value);
    }), validateUndefined = hideStackFrames((value, name) => {
      if (value !== undefined)
        throw new ERR_INVALID_ARG_TYPE3(name, "undefined", value);
    });
    function validateUnion(value, name, union) {
      if (!ArrayPrototypeIncludes(union, value))
        throw new ERR_INVALID_ARG_TYPE3(name, `('${ArrayPrototypeJoin(union, "|")}')`, value);
    }
    var linkValueRegExp = /^(?:<[^>]*>)(?:\s*;\s*[^;"\s]+(?:=(")?[^;"\s]*\1)?)*$/;
    function validateLinkHeaderFormat(value, name) {
      if (typeof value > "u" || !RegExpPrototypeExec(linkValueRegExp, value))
        throw new ERR_INVALID_ARG_VALUE(name, value, 'must be an array or string of format "</styles.css>; rel=preload; as=style"');
    }
    function validateLinkHeaderValue(hints) {
      if (typeof hints === "string")
        return validateLinkHeaderFormat(hints, "hints"), hints;
      else if (ArrayIsArray(hints)) {
        let hintsLength = hints.length, result = "";
        if (hintsLength === 0)
          return result;
        for (let i2 = 0;i2 < hintsLength; i2++) {
          let link = hints[i2];
          if (validateLinkHeaderFormat(link, "hints"), result += link, i2 !== hintsLength - 1)
            result += ", ";
        }
        return result;
      }
      throw new ERR_INVALID_ARG_VALUE("hints", hints, 'must be an array or string of format "</styles.css>; rel=preload; as=style"');
    }
    module2.exports = { isInt32, isUint32, parseFileMode, validateArray, validateStringArray, validateBooleanArray, validateAbortSignalArray, validateBoolean: validateBoolean2, validateBuffer, validateDictionary, validateEncoding, validateFunction, validateInt32, validateInteger, validateNumber: validateNumber3, validateObject, validateOneOf, validatePlainFunction, validatePort, validateSignalName, validateString, validateUint32, validateUndefined, validateUnion, validateAbortSignal: validateAbortSignal2, validateLinkHeaderValue };
  });
  var require_process = __commonJS2((exports2, module2) => {
    module2.exports = globalThis.process;
  });
  var require_utils = __commonJS2((exports2, module2) => {
    var { SymbolAsyncIterator, SymbolIterator, SymbolFor: SymbolFor2 } = require_primordials(), kIsDestroyed = SymbolFor2("nodejs.stream.destroyed"), kIsErrored = SymbolFor2("nodejs.stream.errored"), kIsReadable = SymbolFor2("nodejs.stream.readable"), kIsWritable = SymbolFor2("nodejs.stream.writable"), kIsDisturbed = SymbolFor2("nodejs.stream.disturbed"), kIsClosedPromise = SymbolFor2("nodejs.webstream.isClosedPromise"), kControllerErrorFunction = SymbolFor2("nodejs.webstream.controllerErrorFunction");
    function isReadableNodeStream(obj, strict = false) {
      var _obj$_readableState;
      return !!(obj && typeof obj.pipe === "function" && typeof obj.on === "function" && (!strict || typeof obj.pause === "function" && typeof obj.resume === "function") && (!obj._writableState || ((_obj$_readableState = obj._readableState) === null || _obj$_readableState === undefined ? undefined : _obj$_readableState.readable) !== false) && (!obj._writableState || obj._readableState));
    }
    function isWritableNodeStream(obj) {
      var _obj$_writableState;
      return !!(obj && typeof obj.write === "function" && typeof obj.on === "function" && (!obj._readableState || ((_obj$_writableState = obj._writableState) === null || _obj$_writableState === undefined ? undefined : _obj$_writableState.writable) !== false));
    }
    function isDuplexNodeStream(obj) {
      return !!(obj && typeof obj.pipe === "function" && obj._readableState && typeof obj.on === "function" && typeof obj.write === "function");
    }
    function isNodeStream(obj) {
      return obj && (obj._readableState || obj._writableState || typeof obj.write === "function" && typeof obj.on === "function" || typeof obj.pipe === "function" && typeof obj.on === "function");
    }
    function isReadableStream(obj) {
      return !!(obj && !isNodeStream(obj) && typeof obj.pipeThrough === "function" && typeof obj.getReader === "function" && typeof obj.cancel === "function");
    }
    function isWritableStream(obj) {
      return !!(obj && !isNodeStream(obj) && typeof obj.getWriter === "function" && typeof obj.abort === "function");
    }
    function isTransformStream(obj) {
      return !!(obj && !isNodeStream(obj) && typeof obj.readable === "object" && typeof obj.writable === "object");
    }
    function isWebStream(obj) {
      return isReadableStream(obj) || isWritableStream(obj) || isTransformStream(obj);
    }
    function isIterable(obj, isAsync) {
      if (obj == null)
        return false;
      if (isAsync === true)
        return typeof obj[SymbolAsyncIterator] === "function";
      if (isAsync === false)
        return typeof obj[SymbolIterator] === "function";
      return typeof obj[SymbolAsyncIterator] === "function" || typeof obj[SymbolIterator] === "function";
    }
    function isDestroyed(stream) {
      if (!isNodeStream(stream))
        return null;
      let { _writableState: wState, _readableState: rState } = stream, state = wState || rState;
      return !!(stream.destroyed || stream[kIsDestroyed] || state !== null && state !== undefined && state.destroyed);
    }
    function isWritableEnded(stream) {
      if (!isWritableNodeStream(stream))
        return null;
      if (stream.writableEnded === true)
        return true;
      let wState = stream._writableState;
      if (wState !== null && wState !== undefined && wState.errored)
        return false;
      if (typeof (wState === null || wState === undefined ? undefined : wState.ended) !== "boolean")
        return null;
      return wState.ended;
    }
    function isWritableFinished(stream, strict) {
      if (!isWritableNodeStream(stream))
        return null;
      if (stream.writableFinished === true)
        return true;
      let wState = stream._writableState;
      if (wState !== null && wState !== undefined && wState.errored)
        return false;
      if (typeof (wState === null || wState === undefined ? undefined : wState.finished) !== "boolean")
        return null;
      return !!(wState.finished || strict === false && wState.ended === true && wState.length === 0);
    }
    function isReadableEnded(stream) {
      if (!isReadableNodeStream(stream))
        return null;
      if (stream.readableEnded === true)
        return true;
      let rState = stream._readableState;
      if (!rState || rState.errored)
        return false;
      if (typeof (rState === null || rState === undefined ? undefined : rState.ended) !== "boolean")
        return null;
      return rState.ended;
    }
    function isReadableFinished(stream, strict) {
      if (!isReadableNodeStream(stream))
        return null;
      let rState = stream._readableState;
      if (rState !== null && rState !== undefined && rState.errored)
        return false;
      if (typeof (rState === null || rState === undefined ? undefined : rState.endEmitted) !== "boolean")
        return null;
      return !!(rState.endEmitted || strict === false && rState.ended === true && rState.length === 0);
    }
    function isReadable(stream) {
      if (stream && stream[kIsReadable] != null)
        return stream[kIsReadable];
      if (typeof (stream === null || stream === undefined ? undefined : stream.readable) !== "boolean")
        return null;
      if (isDestroyed(stream))
        return false;
      return isReadableNodeStream(stream) && stream.readable && !isReadableFinished(stream);
    }
    function isWritable(stream) {
      if (stream && stream[kIsWritable] != null)
        return stream[kIsWritable];
      if (typeof (stream === null || stream === undefined ? undefined : stream.writable) !== "boolean")
        return null;
      if (isDestroyed(stream))
        return false;
      return isWritableNodeStream(stream) && stream.writable && !isWritableEnded(stream);
    }
    function isFinished(stream, opts) {
      if (!isNodeStream(stream))
        return null;
      if (isDestroyed(stream))
        return true;
      if ((opts === null || opts === undefined ? undefined : opts.readable) !== false && isReadable(stream))
        return false;
      if ((opts === null || opts === undefined ? undefined : opts.writable) !== false && isWritable(stream))
        return false;
      return true;
    }
    function isWritableErrored(stream) {
      var _stream$_writableStat, _stream$_writableStat2;
      if (!isNodeStream(stream))
        return null;
      if (stream.writableErrored)
        return stream.writableErrored;
      return (_stream$_writableStat = (_stream$_writableStat2 = stream._writableState) === null || _stream$_writableStat2 === undefined ? undefined : _stream$_writableStat2.errored) !== null && _stream$_writableStat !== undefined ? _stream$_writableStat : null;
    }
    function isReadableErrored(stream) {
      var _stream$_readableStat, _stream$_readableStat2;
      if (!isNodeStream(stream))
        return null;
      if (stream.readableErrored)
        return stream.readableErrored;
      return (_stream$_readableStat = (_stream$_readableStat2 = stream._readableState) === null || _stream$_readableStat2 === undefined ? undefined : _stream$_readableStat2.errored) !== null && _stream$_readableStat !== undefined ? _stream$_readableStat : null;
    }
    function isClosed(stream) {
      if (!isNodeStream(stream))
        return null;
      if (typeof stream.closed === "boolean")
        return stream.closed;
      let { _writableState: wState, _readableState: rState } = stream;
      if (typeof (wState === null || wState === undefined ? undefined : wState.closed) === "boolean" || typeof (rState === null || rState === undefined ? undefined : rState.closed) === "boolean")
        return (wState === null || wState === undefined ? undefined : wState.closed) || (rState === null || rState === undefined ? undefined : rState.closed);
      if (typeof stream._closed === "boolean" && isOutgoingMessage(stream))
        return stream._closed;
      return null;
    }
    function isOutgoingMessage(stream) {
      return typeof stream._closed === "boolean" && typeof stream._defaultKeepAlive === "boolean" && typeof stream._removedConnection === "boolean" && typeof stream._removedContLen === "boolean";
    }
    function isServerResponse(stream) {
      return typeof stream._sent100 === "boolean" && isOutgoingMessage(stream);
    }
    function isServerRequest(stream) {
      var _stream$req;
      return typeof stream._consuming === "boolean" && typeof stream._dumped === "boolean" && ((_stream$req = stream.req) === null || _stream$req === undefined ? undefined : _stream$req.upgradeOrConnect) === undefined;
    }
    function willEmitClose(stream) {
      if (!isNodeStream(stream))
        return null;
      let { _writableState: wState, _readableState: rState } = stream, state = wState || rState;
      return !state && isServerResponse(stream) || !!(state && state.autoDestroy && state.emitClose && state.closed === false);
    }
    function isDisturbed(stream) {
      var _stream$kIsDisturbed;
      return !!(stream && ((_stream$kIsDisturbed = stream[kIsDisturbed]) !== null && _stream$kIsDisturbed !== undefined ? _stream$kIsDisturbed : stream.readableDidRead || stream.readableAborted));
    }
    function isErrored(stream) {
      var _ref, _ref2, _ref3, _ref4, _ref5, _stream$kIsErrored, _stream$_readableStat3, _stream$_writableStat3, _stream$_readableStat4, _stream$_writableStat4;
      return !!(stream && ((_ref = (_ref2 = (_ref3 = (_ref4 = (_ref5 = (_stream$kIsErrored = stream[kIsErrored]) !== null && _stream$kIsErrored !== undefined ? _stream$kIsErrored : stream.readableErrored) !== null && _ref5 !== undefined ? _ref5 : stream.writableErrored) !== null && _ref4 !== undefined ? _ref4 : (_stream$_readableStat3 = stream._readableState) === null || _stream$_readableStat3 === undefined ? undefined : _stream$_readableStat3.errorEmitted) !== null && _ref3 !== undefined ? _ref3 : (_stream$_writableStat3 = stream._writableState) === null || _stream$_writableStat3 === undefined ? undefined : _stream$_writableStat3.errorEmitted) !== null && _ref2 !== undefined ? _ref2 : (_stream$_readableStat4 = stream._readableState) === null || _stream$_readableStat4 === undefined ? undefined : _stream$_readableStat4.errored) !== null && _ref !== undefined ? _ref : (_stream$_writableStat4 = stream._writableState) === null || _stream$_writableStat4 === undefined ? undefined : _stream$_writableStat4.errored));
    }
    module2.exports = { isDestroyed, kIsDestroyed, isDisturbed, kIsDisturbed, isErrored, kIsErrored, isReadable, kIsReadable, kIsClosedPromise, kControllerErrorFunction, kIsWritable, isClosed, isDuplexNodeStream, isFinished, isIterable, isReadableNodeStream, isReadableStream, isReadableEnded, isReadableFinished, isReadableErrored, isNodeStream, isWebStream, isWritable, isWritableNodeStream, isWritableStream, isWritableEnded, isWritableFinished, isWritableErrored, isServerRequest, isServerResponse, willEmitClose, isTransformStream };
  });
  var require_end_of_stream = __commonJS2((exports2, module2) => {
    var process2 = require_process(), { AbortError: AbortError2, codes } = require_errors(), { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_STREAM_PREMATURE_CLOSE } = codes, { kEmptyObject, once } = require_util(), { validateAbortSignal: validateAbortSignal2, validateFunction, validateObject, validateBoolean: validateBoolean2 } = require_validators(), { Promise: Promise2, PromisePrototypeThen, SymbolDispose } = require_primordials(), { isClosed, isReadable, isReadableNodeStream, isReadableStream, isReadableFinished, isReadableErrored, isWritable, isWritableNodeStream, isWritableStream, isWritableFinished, isWritableErrored, isNodeStream, willEmitClose: _willEmitClose, kIsClosedPromise } = require_utils(), addAbortListener2;
    function isRequest(stream) {
      return stream.setHeader && typeof stream.abort === "function";
    }
    var nop = () => {};
    function eos(stream, options, callback) {
      var _options$readable, _options$writable;
      if (arguments.length === 2)
        callback = options, options = kEmptyObject;
      else if (options == null)
        options = kEmptyObject;
      else
        validateObject(options, "options");
      if (validateFunction(callback, "callback"), validateAbortSignal2(options.signal, "options.signal"), callback = once(callback), isReadableStream(stream) || isWritableStream(stream))
        return eosWeb(stream, options, callback);
      if (!isNodeStream(stream))
        throw new ERR_INVALID_ARG_TYPE3("stream", ["ReadableStream", "WritableStream", "Stream"], stream);
      let readable = (_options$readable = options.readable) !== null && _options$readable !== undefined ? _options$readable : isReadableNodeStream(stream), writable = (_options$writable = options.writable) !== null && _options$writable !== undefined ? _options$writable : isWritableNodeStream(stream), wState = stream._writableState, rState = stream._readableState, onlegacyfinish = () => {
        if (!stream.writable)
          onfinish();
      }, willEmitClose = _willEmitClose(stream) && isReadableNodeStream(stream) === readable && isWritableNodeStream(stream) === writable, writableFinished = isWritableFinished(stream, false), onfinish = () => {
        if (writableFinished = true, stream.destroyed)
          willEmitClose = false;
        if (willEmitClose && (!stream.readable || readable))
          return;
        if (!readable || readableFinished)
          callback.call(stream);
      }, readableFinished = isReadableFinished(stream, false), onend = () => {
        if (readableFinished = true, stream.destroyed)
          willEmitClose = false;
        if (willEmitClose && (!stream.writable || writable))
          return;
        if (!writable || writableFinished)
          callback.call(stream);
      }, onerror = (err) => {
        callback.call(stream, err);
      }, closed = isClosed(stream), onclose = () => {
        closed = true;
        let errored = isWritableErrored(stream) || isReadableErrored(stream);
        if (errored && typeof errored !== "boolean")
          return callback.call(stream, errored);
        if (readable && !readableFinished && isReadableNodeStream(stream, true)) {
          if (!isReadableFinished(stream, false))
            return callback.call(stream, new ERR_STREAM_PREMATURE_CLOSE);
        }
        if (writable && !writableFinished) {
          if (!isWritableFinished(stream, false))
            return callback.call(stream, new ERR_STREAM_PREMATURE_CLOSE);
        }
        callback.call(stream);
      }, onclosed = () => {
        closed = true;
        let errored = isWritableErrored(stream) || isReadableErrored(stream);
        if (errored && typeof errored !== "boolean")
          return callback.call(stream, errored);
        callback.call(stream);
      }, onrequest = () => {
        stream.req.on("finish", onfinish);
      };
      if (isRequest(stream)) {
        if (stream.on("complete", onfinish), !willEmitClose)
          stream.on("abort", onclose);
        if (stream.req)
          onrequest();
        else
          stream.on("request", onrequest);
      } else if (writable && !wState)
        stream.on("end", onlegacyfinish), stream.on("close", onlegacyfinish);
      if (!willEmitClose && typeof stream.aborted === "boolean")
        stream.on("aborted", onclose);
      if (stream.on("end", onend), stream.on("finish", onfinish), options.error !== false)
        stream.on("error", onerror);
      if (stream.on("close", onclose), closed)
        process2.nextTick(onclose);
      else if (wState !== null && wState !== undefined && wState.errorEmitted || rState !== null && rState !== undefined && rState.errorEmitted) {
        if (!willEmitClose)
          process2.nextTick(onclosed);
      } else if (!readable && (!willEmitClose || isReadable(stream)) && (writableFinished || isWritable(stream) === false))
        process2.nextTick(onclosed);
      else if (!writable && (!willEmitClose || isWritable(stream)) && (readableFinished || isReadable(stream) === false))
        process2.nextTick(onclosed);
      else if (rState && stream.req && stream.aborted)
        process2.nextTick(onclosed);
      let cleanup = () => {
        if (callback = nop, stream.removeListener("aborted", onclose), stream.removeListener("complete", onfinish), stream.removeListener("abort", onclose), stream.removeListener("request", onrequest), stream.req)
          stream.req.removeListener("finish", onfinish);
        stream.removeListener("end", onlegacyfinish), stream.removeListener("close", onlegacyfinish), stream.removeListener("finish", onfinish), stream.removeListener("end", onend), stream.removeListener("error", onerror), stream.removeListener("close", onclose);
      };
      if (options.signal && !closed) {
        let abort = () => {
          let endCallback = callback;
          cleanup(), endCallback.call(stream, new AbortError2(undefined, { cause: options.signal.reason }));
        };
        if (options.signal.aborted)
          process2.nextTick(abort);
        else {
          addAbortListener2 = addAbortListener2 || require_util().addAbortListener;
          let disposable = addAbortListener2(options.signal, abort), originalCallback = callback;
          callback = once((...args) => {
            disposable[SymbolDispose](), originalCallback.apply(stream, args);
          });
        }
      }
      return cleanup;
    }
    function eosWeb(stream, options, callback) {
      let isAborted = false, abort = nop;
      if (options.signal)
        if (abort = () => {
          isAborted = true, callback.call(stream, new AbortError2(undefined, { cause: options.signal.reason }));
        }, options.signal.aborted)
          process2.nextTick(abort);
        else {
          addAbortListener2 = addAbortListener2 || require_util().addAbortListener;
          let disposable = addAbortListener2(options.signal, abort), originalCallback = callback;
          callback = once((...args) => {
            disposable[SymbolDispose](), originalCallback.apply(stream, args);
          });
        }
      let resolverFn = (...args) => {
        if (!isAborted)
          process2.nextTick(() => callback.apply(stream, args));
      };
      return PromisePrototypeThen(stream[kIsClosedPromise].promise, resolverFn, resolverFn), nop;
    }
    function finished(stream, opts) {
      var _opts;
      let autoCleanup = false;
      if (opts === null)
        opts = kEmptyObject;
      if ((_opts = opts) !== null && _opts !== undefined && _opts.cleanup)
        validateBoolean2(opts.cleanup, "cleanup"), autoCleanup = opts.cleanup;
      return new Promise2((resolve, reject) => {
        let cleanup = eos(stream, opts, (err) => {
          if (autoCleanup)
            cleanup();
          if (err)
            reject(err);
          else
            resolve();
        });
      });
    }
    module2.exports = eos;
    module2.exports.finished = finished;
  });
  var require_destroy = __commonJS2((exports2, module2) => {
    var process2 = require_process(), { aggregateTwoErrors, codes: { ERR_MULTIPLE_CALLBACK }, AbortError: AbortError2 } = require_errors(), { Symbol: Symbol2 } = require_primordials(), { kIsDestroyed, isDestroyed, isFinished, isServerRequest } = require_utils(), kDestroy = Symbol2("kDestroy"), kConstruct = Symbol2("kConstruct");
    function checkError(err, w, r) {
      if (err) {
        if (err.stack, w && !w.errored)
          w.errored = err;
        if (r && !r.errored)
          r.errored = err;
      }
    }
    function destroy(err, cb) {
      let r = this._readableState, w = this._writableState, s = w || r;
      if (w !== null && w !== undefined && w.destroyed || r !== null && r !== undefined && r.destroyed) {
        if (typeof cb === "function")
          cb();
        return this;
      }
      if (checkError(err, w, r), w)
        w.destroyed = true;
      if (r)
        r.destroyed = true;
      if (!s.constructed)
        this.once(kDestroy, function(er) {
          _destroy(this, aggregateTwoErrors(er, err), cb);
        });
      else
        _destroy(this, err, cb);
      return this;
    }
    function _destroy(self2, err, cb) {
      let called = false;
      function onDestroy(err2) {
        if (called)
          return;
        called = true;
        let { _readableState: r, _writableState: w } = self2;
        if (checkError(err2, w, r), w)
          w.closed = true;
        if (r)
          r.closed = true;
        if (typeof cb === "function")
          cb(err2);
        if (err2)
          process2.nextTick(emitErrorCloseNT, self2, err2);
        else
          process2.nextTick(emitCloseNT, self2);
      }
      try {
        self2._destroy(err || null, onDestroy);
      } catch (err2) {
        onDestroy(err2);
      }
    }
    function emitErrorCloseNT(self2, err) {
      emitErrorNT(self2, err), emitCloseNT(self2);
    }
    function emitCloseNT(self2) {
      let { _readableState: r, _writableState: w } = self2;
      if (w)
        w.closeEmitted = true;
      if (r)
        r.closeEmitted = true;
      if (w !== null && w !== undefined && w.emitClose || r !== null && r !== undefined && r.emitClose)
        self2.emit("close");
    }
    function emitErrorNT(self2, err) {
      let { _readableState: r, _writableState: w } = self2;
      if (w !== null && w !== undefined && w.errorEmitted || r !== null && r !== undefined && r.errorEmitted)
        return;
      if (w)
        w.errorEmitted = true;
      if (r)
        r.errorEmitted = true;
      self2.emit("error", err);
    }
    function undestroy() {
      let r = this._readableState, w = this._writableState;
      if (r)
        r.constructed = true, r.closed = false, r.closeEmitted = false, r.destroyed = false, r.errored = null, r.errorEmitted = false, r.reading = false, r.ended = r.readable === false, r.endEmitted = r.readable === false;
      if (w)
        w.constructed = true, w.destroyed = false, w.closed = false, w.closeEmitted = false, w.errored = null, w.errorEmitted = false, w.finalCalled = false, w.prefinished = false, w.ended = w.writable === false, w.ending = w.writable === false, w.finished = w.writable === false;
    }
    function errorOrDestroy(stream, err, sync) {
      let { _readableState: r, _writableState: w } = stream;
      if (w !== null && w !== undefined && w.destroyed || r !== null && r !== undefined && r.destroyed)
        return this;
      if (r !== null && r !== undefined && r.autoDestroy || w !== null && w !== undefined && w.autoDestroy)
        stream.destroy(err);
      else if (err) {
        if (err.stack, w && !w.errored)
          w.errored = err;
        if (r && !r.errored)
          r.errored = err;
        if (sync)
          process2.nextTick(emitErrorNT, stream, err);
        else
          emitErrorNT(stream, err);
      }
    }
    function construct(stream, cb) {
      if (typeof stream._construct !== "function")
        return;
      let { _readableState: r, _writableState: w } = stream;
      if (r)
        r.constructed = false;
      if (w)
        w.constructed = false;
      if (stream.once(kConstruct, cb), stream.listenerCount(kConstruct) > 1)
        return;
      process2.nextTick(constructNT, stream);
    }
    function constructNT(stream) {
      let called = false;
      function onConstruct(err) {
        if (called) {
          errorOrDestroy(stream, err !== null && err !== undefined ? err : new ERR_MULTIPLE_CALLBACK);
          return;
        }
        called = true;
        let { _readableState: r, _writableState: w } = stream, s = w || r;
        if (r)
          r.constructed = true;
        if (w)
          w.constructed = true;
        if (s.destroyed)
          stream.emit(kDestroy, err);
        else if (err)
          errorOrDestroy(stream, err, true);
        else
          process2.nextTick(emitConstructNT, stream);
      }
      try {
        stream._construct((err) => {
          process2.nextTick(onConstruct, err);
        });
      } catch (err) {
        process2.nextTick(onConstruct, err);
      }
    }
    function emitConstructNT(stream) {
      stream.emit(kConstruct);
    }
    function isRequest(stream) {
      return (stream === null || stream === undefined ? undefined : stream.setHeader) && typeof stream.abort === "function";
    }
    function emitCloseLegacy(stream) {
      stream.emit("close");
    }
    function emitErrorCloseLegacy(stream, err) {
      stream.emit("error", err), process2.nextTick(emitCloseLegacy, stream);
    }
    function destroyer(stream, err) {
      if (!stream || isDestroyed(stream))
        return;
      if (!err && !isFinished(stream))
        err = new AbortError2;
      if (isServerRequest(stream))
        stream.socket = null, stream.destroy(err);
      else if (isRequest(stream))
        stream.abort();
      else if (isRequest(stream.req))
        stream.req.abort();
      else if (typeof stream.destroy === "function")
        stream.destroy(err);
      else if (typeof stream.close === "function")
        stream.close();
      else if (err)
        process2.nextTick(emitErrorCloseLegacy, stream, err);
      else
        process2.nextTick(emitCloseLegacy, stream);
      if (!stream.destroyed)
        stream[kIsDestroyed] = true;
    }
    module2.exports = { construct, destroyer, destroy, undestroy, errorOrDestroy };
  });
  var require_legacy = __commonJS2((exports2, module2) => {
    var { ArrayIsArray, ObjectSetPrototypeOf } = require_primordials(), { EventEmitter: EE } = (init_events(), __toCommonJS(exports_events));
    function Stream(opts) {
      EE.call(this, opts);
    }
    ObjectSetPrototypeOf(Stream.prototype, EE.prototype);
    ObjectSetPrototypeOf(Stream, EE);
    Stream.prototype.pipe = function(dest, options) {
      let source = this;
      function ondata(chunk) {
        if (dest.writable && dest.write(chunk) === false && source.pause)
          source.pause();
      }
      source.on("data", ondata);
      function ondrain() {
        if (source.readable && source.resume)
          source.resume();
      }
      if (dest.on("drain", ondrain), !dest._isStdio && (!options || options.end !== false))
        source.on("end", onend), source.on("close", onclose);
      let didOnEnd = false;
      function onend() {
        if (didOnEnd)
          return;
        didOnEnd = true, dest.end();
      }
      function onclose() {
        if (didOnEnd)
          return;
        if (didOnEnd = true, typeof dest.destroy === "function")
          dest.destroy();
      }
      function onerror(er) {
        if (cleanup(), EE.listenerCount(this, "error") === 0)
          this.emit("error", er);
      }
      prependListener(source, "error", onerror), prependListener(dest, "error", onerror);
      function cleanup() {
        source.removeListener("data", ondata), dest.removeListener("drain", ondrain), source.removeListener("end", onend), source.removeListener("close", onclose), source.removeListener("error", onerror), dest.removeListener("error", onerror), source.removeListener("end", cleanup), source.removeListener("close", cleanup), dest.removeListener("close", cleanup);
      }
      return source.on("end", cleanup), source.on("close", cleanup), dest.on("close", cleanup), dest.emit("pipe", source), dest;
    };
    function prependListener(emitter, event, fn) {
      if (typeof emitter.prependListener === "function")
        return emitter.prependListener(event, fn);
      if (!emitter._events || !emitter._events[event])
        emitter.on(event, fn);
      else if (ArrayIsArray(emitter._events[event]))
        emitter._events[event].unshift(fn);
      else
        emitter._events[event] = [fn, emitter._events[event]];
    }
    module2.exports = { Stream, prependListener };
  });
  var require_add_abort_signal = __commonJS2((exports2, module2) => {
    var { SymbolDispose } = require_primordials(), { AbortError: AbortError2, codes } = require_errors(), { isNodeStream, isWebStream, kControllerErrorFunction } = require_utils(), eos = require_end_of_stream(), { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3 } = codes, addAbortListener2, validateAbortSignal2 = (signal, name) => {
      if (typeof signal !== "object" || !("aborted" in signal))
        throw new ERR_INVALID_ARG_TYPE3(name, "AbortSignal", signal);
    };
    module2.exports.addAbortSignal = function(signal, stream) {
      if (validateAbortSignal2(signal, "signal"), !isNodeStream(stream) && !isWebStream(stream))
        throw new ERR_INVALID_ARG_TYPE3("stream", ["ReadableStream", "WritableStream", "Stream"], stream);
      return module2.exports.addAbortSignalNoValidate(signal, stream);
    };
    module2.exports.addAbortSignalNoValidate = function(signal, stream) {
      if (typeof signal !== "object" || !("aborted" in signal))
        return stream;
      let onAbort = isNodeStream(stream) ? () => {
        stream.destroy(new AbortError2(undefined, { cause: signal.reason }));
      } : () => {
        stream[kControllerErrorFunction](new AbortError2(undefined, { cause: signal.reason }));
      };
      if (signal.aborted)
        onAbort();
      else {
        addAbortListener2 = addAbortListener2 || require_util().addAbortListener;
        let disposable = addAbortListener2(signal, onAbort);
        eos(stream, disposable[SymbolDispose]);
      }
      return stream;
    };
  });
  var require_buffer_list = __commonJS2((exports2, module2) => {
    var { StringPrototypeSlice, SymbolIterator, TypedArrayPrototypeSet, Uint8Array: Uint8Array2 } = require_primordials(), { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), { inspect } = require_util();
    module2.exports = class {
      constructor() {
        this.head = null, this.tail = null, this.length = 0;
      }
      push(v) {
        let entry = { data: v, next: null };
        if (this.length > 0)
          this.tail.next = entry;
        else
          this.head = entry;
        this.tail = entry, ++this.length;
      }
      unshift(v) {
        let entry = { data: v, next: this.head };
        if (this.length === 0)
          this.tail = entry;
        this.head = entry, ++this.length;
      }
      shift() {
        if (this.length === 0)
          return;
        let ret = this.head.data;
        if (this.length === 1)
          this.head = this.tail = null;
        else
          this.head = this.head.next;
        return --this.length, ret;
      }
      clear() {
        this.head = this.tail = null, this.length = 0;
      }
      join(s) {
        if (this.length === 0)
          return "";
        let p = this.head, ret = "" + p.data;
        while ((p = p.next) !== null)
          ret += s + p.data;
        return ret;
      }
      concat(n) {
        if (this.length === 0)
          return Buffer3.alloc(0);
        let ret = Buffer3.allocUnsafe(n >>> 0), p = this.head, i2 = 0;
        while (p)
          TypedArrayPrototypeSet(ret, p.data, i2), i2 += p.data.length, p = p.next;
        return ret;
      }
      consume(n, hasStrings) {
        let data = this.head.data;
        if (n < data.length) {
          let slice = data.slice(0, n);
          return this.head.data = data.slice(n), slice;
        }
        if (n === data.length)
          return this.shift();
        return hasStrings ? this._getString(n) : this._getBuffer(n);
      }
      first() {
        return this.head.data;
      }
      *[SymbolIterator]() {
        for (let p = this.head;p; p = p.next)
          yield p.data;
      }
      _getString(n) {
        let ret = "", p = this.head, c = 0;
        do {
          let str = p.data;
          if (n > str.length)
            ret += str, n -= str.length;
          else {
            if (n === str.length)
              if (ret += str, ++c, p.next)
                this.head = p.next;
              else
                this.head = this.tail = null;
            else
              ret += StringPrototypeSlice(str, 0, n), this.head = p, p.data = StringPrototypeSlice(str, n);
            break;
          }
          ++c;
        } while ((p = p.next) !== null);
        return this.length -= c, ret;
      }
      _getBuffer(n) {
        let ret = Buffer3.allocUnsafe(n), retLen = n, p = this.head, c = 0;
        do {
          let buf = p.data;
          if (n > buf.length)
            TypedArrayPrototypeSet(ret, buf, retLen - n), n -= buf.length;
          else {
            if (n === buf.length)
              if (TypedArrayPrototypeSet(ret, buf, retLen - n), ++c, p.next)
                this.head = p.next;
              else
                this.head = this.tail = null;
            else
              TypedArrayPrototypeSet(ret, new Uint8Array2(buf.buffer, buf.byteOffset, n), retLen - n), this.head = p, p.data = buf.slice(n);
            break;
          }
          ++c;
        } while ((p = p.next) !== null);
        return this.length -= c, ret;
      }
      [Symbol.for("nodejs.util.inspect.custom")](_, options) {
        return inspect(this, { ...options, depth: 0, customInspect: false });
      }
    };
  });
  var require_state = __commonJS2((exports2, module2) => {
    var { MathFloor, NumberIsInteger } = require_primordials(), { validateInteger } = require_validators(), { ERR_INVALID_ARG_VALUE } = require_errors().codes, defaultHighWaterMarkBytes = 16384, defaultHighWaterMarkObjectMode = 16;
    function highWaterMarkFrom(options, isDuplex, duplexKey) {
      return options.highWaterMark != null ? options.highWaterMark : isDuplex ? options[duplexKey] : null;
    }
    function getDefaultHighWaterMark(objectMode) {
      return objectMode ? defaultHighWaterMarkObjectMode : defaultHighWaterMarkBytes;
    }
    function setDefaultHighWaterMark(objectMode, value) {
      if (validateInteger(value, "value", 0), objectMode)
        defaultHighWaterMarkObjectMode = value;
      else
        defaultHighWaterMarkBytes = value;
    }
    function getHighWaterMark(state, options, duplexKey, isDuplex) {
      let hwm = highWaterMarkFrom(options, isDuplex, duplexKey);
      if (hwm != null) {
        if (!NumberIsInteger(hwm) || hwm < 0) {
          let name = isDuplex ? `options.${duplexKey}` : "options.highWaterMark";
          throw new ERR_INVALID_ARG_VALUE(name, hwm);
        }
        return MathFloor(hwm);
      }
      return getDefaultHighWaterMark(state.objectMode);
    }
    module2.exports = { getHighWaterMark, getDefaultHighWaterMark, setDefaultHighWaterMark };
  });
  var require_safe_buffer = __commonJS2((exports2, module2) => {
    /*! safe-buffer. MIT License. Feross Aboukhadijeh <https://feross.org/opensource> */
    var buffer = (init_buffer(), __toCommonJS(exports_buffer)), Buffer3 = buffer.Buffer;
    function copyProps(src, dst) {
      for (var key in src)
        dst[key] = src[key];
    }
    if (Buffer3.from && Buffer3.alloc && Buffer3.allocUnsafe && Buffer3.allocUnsafeSlow)
      module2.exports = buffer;
    else
      copyProps(buffer, exports2), exports2.Buffer = SafeBuffer;
    function SafeBuffer(arg, encodingOrOffset, length) {
      return Buffer3(arg, encodingOrOffset, length);
    }
    SafeBuffer.prototype = Object.create(Buffer3.prototype);
    copyProps(Buffer3, SafeBuffer);
    SafeBuffer.from = function(arg, encodingOrOffset, length) {
      if (typeof arg === "number")
        throw TypeError("Argument must not be a number");
      return Buffer3(arg, encodingOrOffset, length);
    };
    SafeBuffer.alloc = function(size, fill, encoding) {
      if (typeof size !== "number")
        throw TypeError("Argument must be a number");
      var buf = Buffer3(size);
      if (fill !== undefined)
        if (typeof encoding === "string")
          buf.fill(fill, encoding);
        else
          buf.fill(fill);
      else
        buf.fill(0);
      return buf;
    };
    SafeBuffer.allocUnsafe = function(size) {
      if (typeof size !== "number")
        throw TypeError("Argument must be a number");
      return Buffer3(size);
    };
    SafeBuffer.allocUnsafeSlow = function(size) {
      if (typeof size !== "number")
        throw TypeError("Argument must be a number");
      return buffer.SlowBuffer(size);
    };
  });
  var require_string_decoder = __commonJS2((exports2) => {
    var Buffer3 = require_safe_buffer().Buffer, isEncoding = Buffer3.isEncoding || function(encoding) {
      switch (encoding = "" + encoding, encoding && encoding.toLowerCase()) {
        case "hex":
        case "utf8":
        case "utf-8":
        case "ascii":
        case "binary":
        case "base64":
        case "ucs2":
        case "ucs-2":
        case "utf16le":
        case "utf-16le":
        case "raw":
          return true;
        default:
          return false;
      }
    };
    function _normalizeEncoding(enc) {
      if (!enc)
        return "utf8";
      var retried;
      while (true)
        switch (enc) {
          case "utf8":
          case "utf-8":
            return "utf8";
          case "ucs2":
          case "ucs-2":
          case "utf16le":
          case "utf-16le":
            return "utf16le";
          case "latin1":
          case "binary":
            return "latin1";
          case "base64":
          case "ascii":
          case "hex":
            return enc;
          default:
            if (retried)
              return;
            enc = ("" + enc).toLowerCase(), retried = true;
        }
    }
    function normalizeEncoding(enc) {
      var nenc = _normalizeEncoding(enc);
      if (typeof nenc !== "string" && (Buffer3.isEncoding === isEncoding || !isEncoding(enc)))
        throw Error("Unknown encoding: " + enc);
      return nenc || enc;
    }
    exports2.StringDecoder = StringDecoder;
    function StringDecoder(encoding) {
      this.encoding = normalizeEncoding(encoding);
      var nb;
      switch (this.encoding) {
        case "utf16le":
          this.text = utf16Text, this.end = utf16End, nb = 4;
          break;
        case "utf8":
          this.fillLast = utf8FillLast, nb = 4;
          break;
        case "base64":
          this.text = base64Text, this.end = base64End, nb = 3;
          break;
        default:
          this.write = simpleWrite, this.end = simpleEnd;
          return;
      }
      this.lastNeed = 0, this.lastTotal = 0, this.lastChar = Buffer3.allocUnsafe(nb);
    }
    StringDecoder.prototype.write = function(buf) {
      if (buf.length === 0)
        return "";
      var r, i2;
      if (this.lastNeed) {
        if (r = this.fillLast(buf), r === undefined)
          return "";
        i2 = this.lastNeed, this.lastNeed = 0;
      } else
        i2 = 0;
      if (i2 < buf.length)
        return r ? r + this.text(buf, i2) : this.text(buf, i2);
      return r || "";
    };
    StringDecoder.prototype.end = utf8End;
    StringDecoder.prototype.text = utf8Text;
    StringDecoder.prototype.fillLast = function(buf) {
      if (this.lastNeed <= buf.length)
        return buf.copy(this.lastChar, this.lastTotal - this.lastNeed, 0, this.lastNeed), this.lastChar.toString(this.encoding, 0, this.lastTotal);
      buf.copy(this.lastChar, this.lastTotal - this.lastNeed, 0, buf.length), this.lastNeed -= buf.length;
    };
    function utf8CheckByte(byte) {
      if (byte <= 127)
        return 0;
      else if (byte >> 5 === 6)
        return 2;
      else if (byte >> 4 === 14)
        return 3;
      else if (byte >> 3 === 30)
        return 4;
      return byte >> 6 === 2 ? -1 : -2;
    }
    function utf8CheckIncomplete(self2, buf, i2) {
      var j = buf.length - 1;
      if (j < i2)
        return 0;
      var nb = utf8CheckByte(buf[j]);
      if (nb >= 0) {
        if (nb > 0)
          self2.lastNeed = nb - 1;
        return nb;
      }
      if (--j < i2 || nb === -2)
        return 0;
      if (nb = utf8CheckByte(buf[j]), nb >= 0) {
        if (nb > 0)
          self2.lastNeed = nb - 2;
        return nb;
      }
      if (--j < i2 || nb === -2)
        return 0;
      if (nb = utf8CheckByte(buf[j]), nb >= 0) {
        if (nb > 0)
          if (nb === 2)
            nb = 0;
          else
            self2.lastNeed = nb - 3;
        return nb;
      }
      return 0;
    }
    function utf8CheckExtraBytes(self2, buf, p) {
      if ((buf[0] & 192) !== 128)
        return self2.lastNeed = 0, "�";
      if (self2.lastNeed > 1 && buf.length > 1) {
        if ((buf[1] & 192) !== 128)
          return self2.lastNeed = 1, "�";
        if (self2.lastNeed > 2 && buf.length > 2) {
          if ((buf[2] & 192) !== 128)
            return self2.lastNeed = 2, "�";
        }
      }
    }
    function utf8FillLast(buf) {
      var p = this.lastTotal - this.lastNeed, r = utf8CheckExtraBytes(this, buf, p);
      if (r !== undefined)
        return r;
      if (this.lastNeed <= buf.length)
        return buf.copy(this.lastChar, p, 0, this.lastNeed), this.lastChar.toString(this.encoding, 0, this.lastTotal);
      buf.copy(this.lastChar, p, 0, buf.length), this.lastNeed -= buf.length;
    }
    function utf8Text(buf, i2) {
      var total = utf8CheckIncomplete(this, buf, i2);
      if (!this.lastNeed)
        return buf.toString("utf8", i2);
      this.lastTotal = total;
      var end = buf.length - (total - this.lastNeed);
      return buf.copy(this.lastChar, 0, end), buf.toString("utf8", i2, end);
    }
    function utf8End(buf) {
      var r = buf && buf.length ? this.write(buf) : "";
      if (this.lastNeed)
        return r + "�";
      return r;
    }
    function utf16Text(buf, i2) {
      if ((buf.length - i2) % 2 === 0) {
        var r = buf.toString("utf16le", i2);
        if (r) {
          var c = r.charCodeAt(r.length - 1);
          if (c >= 55296 && c <= 56319)
            return this.lastNeed = 2, this.lastTotal = 4, this.lastChar[0] = buf[buf.length - 2], this.lastChar[1] = buf[buf.length - 1], r.slice(0, -1);
        }
        return r;
      }
      return this.lastNeed = 1, this.lastTotal = 2, this.lastChar[0] = buf[buf.length - 1], buf.toString("utf16le", i2, buf.length - 1);
    }
    function utf16End(buf) {
      var r = buf && buf.length ? this.write(buf) : "";
      if (this.lastNeed) {
        var end = this.lastTotal - this.lastNeed;
        return r + this.lastChar.toString("utf16le", 0, end);
      }
      return r;
    }
    function base64Text(buf, i2) {
      var n = (buf.length - i2) % 3;
      if (n === 0)
        return buf.toString("base64", i2);
      if (this.lastNeed = 3 - n, this.lastTotal = 3, n === 1)
        this.lastChar[0] = buf[buf.length - 1];
      else
        this.lastChar[0] = buf[buf.length - 2], this.lastChar[1] = buf[buf.length - 1];
      return buf.toString("base64", i2, buf.length - n);
    }
    function base64End(buf) {
      var r = buf && buf.length ? this.write(buf) : "";
      if (this.lastNeed)
        return r + this.lastChar.toString("base64", 0, 3 - this.lastNeed);
      return r;
    }
    function simpleWrite(buf) {
      return buf.toString(this.encoding);
    }
    function simpleEnd(buf) {
      return buf && buf.length ? this.write(buf) : "";
    }
  });
  var require_from = __commonJS2((exports2, module2) => {
    var process2 = require_process(), { PromisePrototypeThen, SymbolAsyncIterator, SymbolIterator } = require_primordials(), { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_STREAM_NULL_VALUES } = require_errors().codes;
    function from2(Readable, iterable, opts) {
      let iterator;
      if (typeof iterable === "string" || iterable instanceof Buffer3)
        return new Readable({ objectMode: true, ...opts, read() {
          this.push(iterable), this.push(null);
        } });
      let isAsync;
      if (iterable && iterable[SymbolAsyncIterator])
        isAsync = true, iterator = iterable[SymbolAsyncIterator]();
      else if (iterable && iterable[SymbolIterator])
        isAsync = false, iterator = iterable[SymbolIterator]();
      else
        throw new ERR_INVALID_ARG_TYPE3("iterable", ["Iterable"], iterable);
      let readable = new Readable({ objectMode: true, highWaterMark: 1, ...opts }), reading = false;
      readable._read = function() {
        if (!reading)
          reading = true, next();
      }, readable._destroy = function(error, cb) {
        PromisePrototypeThen(close(error), () => process2.nextTick(cb, error), (e) => process2.nextTick(cb, e || error));
      };
      async function close(error) {
        let hadError = error !== undefined && error !== null, hasThrow = typeof iterator.throw === "function";
        if (hadError && hasThrow) {
          let { value, done } = await iterator.throw(error);
          if (await value, done)
            return;
        }
        if (typeof iterator.return === "function") {
          let { value } = await iterator.return();
          await value;
        }
      }
      async function next() {
        for (;; ) {
          try {
            let { value, done } = isAsync ? await iterator.next() : iterator.next();
            if (done)
              readable.push(null);
            else {
              let res = value && typeof value.then === "function" ? await value : value;
              if (res === null)
                throw reading = false, new ERR_STREAM_NULL_VALUES;
              else if (readable.push(res))
                continue;
              else
                reading = false;
            }
          } catch (err) {
            readable.destroy(err);
          }
          break;
        }
      }
      return readable;
    }
    module2.exports = from2;
  });
  var require_readable = __commonJS2((exports2, module2) => {
    var process2 = require_process(), { ArrayPrototypeIndexOf, NumberIsInteger, NumberIsNaN, NumberParseInt, ObjectDefineProperties, ObjectKeys, ObjectSetPrototypeOf, Promise: Promise2, SafeSet, SymbolAsyncDispose, SymbolAsyncIterator, Symbol: Symbol2 } = require_primordials();
    module2.exports = Readable;
    Readable.ReadableState = ReadableState;
    var { EventEmitter: EE } = (init_events(), __toCommonJS(exports_events)), { Stream, prependListener } = require_legacy(), { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), { addAbortSignal } = require_add_abort_signal(), eos = require_end_of_stream(), debug = require_util().debuglog("stream", (fn) => {
      debug = fn;
    }), BufferList = require_buffer_list(), destroyImpl = require_destroy(), { getHighWaterMark, getDefaultHighWaterMark } = require_state(), { aggregateTwoErrors, codes: { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_METHOD_NOT_IMPLEMENTED, ERR_OUT_OF_RANGE: ERR_OUT_OF_RANGE3, ERR_STREAM_PUSH_AFTER_EOF, ERR_STREAM_UNSHIFT_AFTER_END_EVENT }, AbortError: AbortError2 } = require_errors(), { validateObject } = require_validators(), kPaused = Symbol2("kPaused"), { StringDecoder } = require_string_decoder(), from2 = require_from();
    ObjectSetPrototypeOf(Readable.prototype, Stream.prototype);
    ObjectSetPrototypeOf(Readable, Stream);
    var nop = () => {}, { errorOrDestroy } = destroyImpl, kObjectMode = 1, kEnded = 2, kEndEmitted = 4, kReading = 8, kConstructed = 16, kSync = 32, kNeedReadable = 64, kEmittedReadable = 128, kReadableListening = 256, kResumeScheduled = 512, kErrorEmitted = 1024, kEmitClose = 2048, kAutoDestroy = 4096, kDestroyed = 8192, kClosed = 16384, kCloseEmitted = 32768, kMultiAwaitDrain = 65536, kReadingMore = 131072, kDataEmitted = 262144;
    function makeBitMapDescriptor(bit) {
      return { enumerable: false, get() {
        return (this.state & bit) !== 0;
      }, set(value) {
        if (value)
          this.state |= bit;
        else
          this.state &= ~bit;
      } };
    }
    ObjectDefineProperties(ReadableState.prototype, { objectMode: makeBitMapDescriptor(kObjectMode), ended: makeBitMapDescriptor(kEnded), endEmitted: makeBitMapDescriptor(kEndEmitted), reading: makeBitMapDescriptor(kReading), constructed: makeBitMapDescriptor(kConstructed), sync: makeBitMapDescriptor(kSync), needReadable: makeBitMapDescriptor(kNeedReadable), emittedReadable: makeBitMapDescriptor(kEmittedReadable), readableListening: makeBitMapDescriptor(kReadableListening), resumeScheduled: makeBitMapDescriptor(kResumeScheduled), errorEmitted: makeBitMapDescriptor(kErrorEmitted), emitClose: makeBitMapDescriptor(kEmitClose), autoDestroy: makeBitMapDescriptor(kAutoDestroy), destroyed: makeBitMapDescriptor(kDestroyed), closed: makeBitMapDescriptor(kClosed), closeEmitted: makeBitMapDescriptor(kCloseEmitted), multiAwaitDrain: makeBitMapDescriptor(kMultiAwaitDrain), readingMore: makeBitMapDescriptor(kReadingMore), dataEmitted: makeBitMapDescriptor(kDataEmitted) });
    function ReadableState(options, stream, isDuplex) {
      if (typeof isDuplex !== "boolean")
        isDuplex = stream instanceof require_duplex();
      if (this.state = kEmitClose | kAutoDestroy | kConstructed | kSync, options && options.objectMode)
        this.state |= kObjectMode;
      if (isDuplex && options && options.readableObjectMode)
        this.state |= kObjectMode;
      if (this.highWaterMark = options ? getHighWaterMark(this, options, "readableHighWaterMark", isDuplex) : getDefaultHighWaterMark(false), this.buffer = new BufferList, this.length = 0, this.pipes = [], this.flowing = null, this[kPaused] = null, options && options.emitClose === false)
        this.state &= ~kEmitClose;
      if (options && options.autoDestroy === false)
        this.state &= ~kAutoDestroy;
      if (this.errored = null, this.defaultEncoding = options && options.defaultEncoding || "utf8", this.awaitDrainWriters = null, this.decoder = null, this.encoding = null, options && options.encoding)
        this.decoder = new StringDecoder(options.encoding), this.encoding = options.encoding;
    }
    function Readable(options) {
      if (!(this instanceof Readable))
        return new Readable(options);
      let isDuplex = this instanceof require_duplex();
      if (this._readableState = new ReadableState(options, this, isDuplex), options) {
        if (typeof options.read === "function")
          this._read = options.read;
        if (typeof options.destroy === "function")
          this._destroy = options.destroy;
        if (typeof options.construct === "function")
          this._construct = options.construct;
        if (options.signal && !isDuplex)
          addAbortSignal(options.signal, this);
      }
      Stream.call(this, options), destroyImpl.construct(this, () => {
        if (this._readableState.needReadable)
          maybeReadMore(this, this._readableState);
      });
    }
    Readable.prototype.destroy = destroyImpl.destroy;
    Readable.prototype._undestroy = destroyImpl.undestroy;
    Readable.prototype._destroy = function(err, cb) {
      cb(err);
    };
    Readable.prototype[EE.captureRejectionSymbol] = function(err) {
      this.destroy(err);
    };
    Readable.prototype[SymbolAsyncDispose] = function() {
      let error;
      if (!this.destroyed)
        error = this.readableEnded ? null : new AbortError2, this.destroy(error);
      return new Promise2((resolve, reject) => eos(this, (err) => err && err !== error ? reject(err) : resolve(null)));
    };
    Readable.prototype.push = function(chunk, encoding) {
      return readableAddChunk(this, chunk, encoding, false);
    };
    Readable.prototype.unshift = function(chunk, encoding) {
      return readableAddChunk(this, chunk, encoding, true);
    };
    function readableAddChunk(stream, chunk, encoding, addToFront) {
      debug("readableAddChunk", chunk);
      let state = stream._readableState, err;
      if ((state.state & kObjectMode) === 0) {
        if (typeof chunk === "string") {
          if (encoding = encoding || state.defaultEncoding, state.encoding !== encoding)
            if (addToFront && state.encoding)
              chunk = Buffer3.from(chunk, encoding).toString(state.encoding);
            else
              chunk = Buffer3.from(chunk, encoding), encoding = "";
        } else if (chunk instanceof Buffer3)
          encoding = "";
        else if (Stream._isUint8Array(chunk))
          chunk = Stream._uint8ArrayToBuffer(chunk), encoding = "";
        else if (chunk != null)
          err = new ERR_INVALID_ARG_TYPE3("chunk", ["string", "Buffer", "Uint8Array"], chunk);
      }
      if (err)
        errorOrDestroy(stream, err);
      else if (chunk === null)
        state.state &= ~kReading, onEofChunk(stream, state);
      else if ((state.state & kObjectMode) !== 0 || chunk && chunk.length > 0)
        if (addToFront)
          if ((state.state & kEndEmitted) !== 0)
            errorOrDestroy(stream, new ERR_STREAM_UNSHIFT_AFTER_END_EVENT);
          else if (state.destroyed || state.errored)
            return false;
          else
            addChunk(stream, state, chunk, true);
        else if (state.ended)
          errorOrDestroy(stream, new ERR_STREAM_PUSH_AFTER_EOF);
        else if (state.destroyed || state.errored)
          return false;
        else if (state.state &= ~kReading, state.decoder && !encoding)
          if (chunk = state.decoder.write(chunk), state.objectMode || chunk.length !== 0)
            addChunk(stream, state, chunk, false);
          else
            maybeReadMore(stream, state);
        else
          addChunk(stream, state, chunk, false);
      else if (!addToFront)
        state.state &= ~kReading, maybeReadMore(stream, state);
      return !state.ended && (state.length < state.highWaterMark || state.length === 0);
    }
    function addChunk(stream, state, chunk, addToFront) {
      if (state.flowing && state.length === 0 && !state.sync && stream.listenerCount("data") > 0) {
        if ((state.state & kMultiAwaitDrain) !== 0)
          state.awaitDrainWriters.clear();
        else
          state.awaitDrainWriters = null;
        state.dataEmitted = true, stream.emit("data", chunk);
      } else {
        if (state.length += state.objectMode ? 1 : chunk.length, addToFront)
          state.buffer.unshift(chunk);
        else
          state.buffer.push(chunk);
        if ((state.state & kNeedReadable) !== 0)
          emitReadable(stream);
      }
      maybeReadMore(stream, state);
    }
    Readable.prototype.isPaused = function() {
      let state = this._readableState;
      return state[kPaused] === true || state.flowing === false;
    };
    Readable.prototype.setEncoding = function(enc) {
      let decoder = new StringDecoder(enc);
      this._readableState.decoder = decoder, this._readableState.encoding = this._readableState.decoder.encoding;
      let buffer = this._readableState.buffer, content = "";
      for (let data of buffer)
        content += decoder.write(data);
      if (buffer.clear(), content !== "")
        buffer.push(content);
      return this._readableState.length = content.length, this;
    };
    var MAX_HWM = 1073741824;
    function computeNewHighWaterMark(n) {
      if (n > MAX_HWM)
        throw new ERR_OUT_OF_RANGE3("size", "<= 1GiB", n);
      else
        n--, n |= n >>> 1, n |= n >>> 2, n |= n >>> 4, n |= n >>> 8, n |= n >>> 16, n++;
      return n;
    }
    function howMuchToRead(n, state) {
      if (n <= 0 || state.length === 0 && state.ended)
        return 0;
      if ((state.state & kObjectMode) !== 0)
        return 1;
      if (NumberIsNaN(n)) {
        if (state.flowing && state.length)
          return state.buffer.first().length;
        return state.length;
      }
      if (n <= state.length)
        return n;
      return state.ended ? state.length : 0;
    }
    Readable.prototype.read = function(n) {
      if (debug("read", n), n === undefined)
        n = NaN;
      else if (!NumberIsInteger(n))
        n = NumberParseInt(n, 10);
      let state = this._readableState, nOrig = n;
      if (n > state.highWaterMark)
        state.highWaterMark = computeNewHighWaterMark(n);
      if (n !== 0)
        state.state &= ~kEmittedReadable;
      if (n === 0 && state.needReadable && ((state.highWaterMark !== 0 ? state.length >= state.highWaterMark : state.length > 0) || state.ended)) {
        if (debug("read: emitReadable", state.length, state.ended), state.length === 0 && state.ended)
          endReadable(this);
        else
          emitReadable(this);
        return null;
      }
      if (n = howMuchToRead(n, state), n === 0 && state.ended) {
        if (state.length === 0)
          endReadable(this);
        return null;
      }
      let doRead = (state.state & kNeedReadable) !== 0;
      if (debug("need readable", doRead), state.length === 0 || state.length - n < state.highWaterMark)
        doRead = true, debug("length less than watermark", doRead);
      if (state.ended || state.reading || state.destroyed || state.errored || !state.constructed)
        doRead = false, debug("reading, ended or constructing", doRead);
      else if (doRead) {
        if (debug("do read"), state.state |= kReading | kSync, state.length === 0)
          state.state |= kNeedReadable;
        try {
          this._read(state.highWaterMark);
        } catch (err) {
          errorOrDestroy(this, err);
        }
        if (state.state &= ~kSync, !state.reading)
          n = howMuchToRead(nOrig, state);
      }
      let ret;
      if (n > 0)
        ret = fromList(n, state);
      else
        ret = null;
      if (ret === null)
        state.needReadable = state.length <= state.highWaterMark, n = 0;
      else if (state.length -= n, state.multiAwaitDrain)
        state.awaitDrainWriters.clear();
      else
        state.awaitDrainWriters = null;
      if (state.length === 0) {
        if (!state.ended)
          state.needReadable = true;
        if (nOrig !== n && state.ended)
          endReadable(this);
      }
      if (ret !== null && !state.errorEmitted && !state.closeEmitted)
        state.dataEmitted = true, this.emit("data", ret);
      return ret;
    };
    function onEofChunk(stream, state) {
      if (debug("onEofChunk"), state.ended)
        return;
      if (state.decoder) {
        let chunk = state.decoder.end();
        if (chunk && chunk.length)
          state.buffer.push(chunk), state.length += state.objectMode ? 1 : chunk.length;
      }
      if (state.ended = true, state.sync)
        emitReadable(stream);
      else
        state.needReadable = false, state.emittedReadable = true, emitReadable_(stream);
    }
    function emitReadable(stream) {
      let state = stream._readableState;
      if (debug("emitReadable", state.needReadable, state.emittedReadable), state.needReadable = false, !state.emittedReadable)
        debug("emitReadable", state.flowing), state.emittedReadable = true, process2.nextTick(emitReadable_, stream);
    }
    function emitReadable_(stream) {
      let state = stream._readableState;
      if (debug("emitReadable_", state.destroyed, state.length, state.ended), !state.destroyed && !state.errored && (state.length || state.ended))
        stream.emit("readable"), state.emittedReadable = false;
      state.needReadable = !state.flowing && !state.ended && state.length <= state.highWaterMark, flow(stream);
    }
    function maybeReadMore(stream, state) {
      if (!state.readingMore && state.constructed)
        state.readingMore = true, process2.nextTick(maybeReadMore_, stream, state);
    }
    function maybeReadMore_(stream, state) {
      while (!state.reading && !state.ended && (state.length < state.highWaterMark || state.flowing && state.length === 0)) {
        let len2 = state.length;
        if (debug("maybeReadMore read 0"), stream.read(0), len2 === state.length)
          break;
      }
      state.readingMore = false;
    }
    Readable.prototype._read = function(n) {
      throw new ERR_METHOD_NOT_IMPLEMENTED("_read()");
    };
    Readable.prototype.pipe = function(dest, pipeOpts) {
      let src = this, state = this._readableState;
      if (state.pipes.length === 1) {
        if (!state.multiAwaitDrain)
          state.multiAwaitDrain = true, state.awaitDrainWriters = new SafeSet(state.awaitDrainWriters ? [state.awaitDrainWriters] : []);
      }
      state.pipes.push(dest), debug("pipe count=%d opts=%j", state.pipes.length, pipeOpts);
      let endFn = (!pipeOpts || pipeOpts.end !== false) && dest !== process2.stdout && dest !== process2.stderr ? onend : unpipe;
      if (state.endEmitted)
        process2.nextTick(endFn);
      else
        src.once("end", endFn);
      dest.on("unpipe", onunpipe);
      function onunpipe(readable, unpipeInfo) {
        if (debug("onunpipe"), readable === src) {
          if (unpipeInfo && unpipeInfo.hasUnpiped === false)
            unpipeInfo.hasUnpiped = true, cleanup();
        }
      }
      function onend() {
        debug("onend"), dest.end();
      }
      let ondrain, cleanedUp = false;
      function cleanup() {
        if (debug("cleanup"), dest.removeListener("close", onclose), dest.removeListener("finish", onfinish), ondrain)
          dest.removeListener("drain", ondrain);
        if (dest.removeListener("error", onerror), dest.removeListener("unpipe", onunpipe), src.removeListener("end", onend), src.removeListener("end", unpipe), src.removeListener("data", ondata), cleanedUp = true, ondrain && state.awaitDrainWriters && (!dest._writableState || dest._writableState.needDrain))
          ondrain();
      }
      function pause() {
        if (!cleanedUp) {
          if (state.pipes.length === 1 && state.pipes[0] === dest)
            debug("false write response, pause", 0), state.awaitDrainWriters = dest, state.multiAwaitDrain = false;
          else if (state.pipes.length > 1 && state.pipes.includes(dest))
            debug("false write response, pause", state.awaitDrainWriters.size), state.awaitDrainWriters.add(dest);
          src.pause();
        }
        if (!ondrain)
          ondrain = pipeOnDrain(src, dest), dest.on("drain", ondrain);
      }
      src.on("data", ondata);
      function ondata(chunk) {
        debug("ondata");
        let ret = dest.write(chunk);
        if (debug("dest.write", ret), ret === false)
          pause();
      }
      function onerror(er) {
        if (debug("onerror", er), unpipe(), dest.removeListener("error", onerror), dest.listenerCount("error") === 0) {
          let s = dest._writableState || dest._readableState;
          if (s && !s.errorEmitted)
            errorOrDestroy(dest, er);
          else
            dest.emit("error", er);
        }
      }
      prependListener(dest, "error", onerror);
      function onclose() {
        dest.removeListener("finish", onfinish), unpipe();
      }
      dest.once("close", onclose);
      function onfinish() {
        debug("onfinish"), dest.removeListener("close", onclose), unpipe();
      }
      dest.once("finish", onfinish);
      function unpipe() {
        debug("unpipe"), src.unpipe(dest);
      }
      if (dest.emit("pipe", src), dest.writableNeedDrain === true)
        pause();
      else if (!state.flowing)
        debug("pipe resume"), src.resume();
      return dest;
    };
    function pipeOnDrain(src, dest) {
      return function() {
        let state = src._readableState;
        if (state.awaitDrainWriters === dest)
          debug("pipeOnDrain", 1), state.awaitDrainWriters = null;
        else if (state.multiAwaitDrain)
          debug("pipeOnDrain", state.awaitDrainWriters.size), state.awaitDrainWriters.delete(dest);
        if ((!state.awaitDrainWriters || state.awaitDrainWriters.size === 0) && src.listenerCount("data"))
          src.resume();
      };
    }
    Readable.prototype.unpipe = function(dest) {
      let state = this._readableState, unpipeInfo = { hasUnpiped: false };
      if (state.pipes.length === 0)
        return this;
      if (!dest) {
        let dests = state.pipes;
        state.pipes = [], this.pause();
        for (let i2 = 0;i2 < dests.length; i2++)
          dests[i2].emit("unpipe", this, { hasUnpiped: false });
        return this;
      }
      let index = ArrayPrototypeIndexOf(state.pipes, dest);
      if (index === -1)
        return this;
      if (state.pipes.splice(index, 1), state.pipes.length === 0)
        this.pause();
      return dest.emit("unpipe", this, unpipeInfo), this;
    };
    Readable.prototype.on = function(ev, fn) {
      let res = Stream.prototype.on.call(this, ev, fn), state = this._readableState;
      if (ev === "data") {
        if (state.readableListening = this.listenerCount("readable") > 0, state.flowing !== false)
          this.resume();
      } else if (ev === "readable") {
        if (!state.endEmitted && !state.readableListening) {
          if (state.readableListening = state.needReadable = true, state.flowing = false, state.emittedReadable = false, debug("on readable", state.length, state.reading), state.length)
            emitReadable(this);
          else if (!state.reading)
            process2.nextTick(nReadingNextTick, this);
        }
      }
      return res;
    };
    Readable.prototype.addListener = Readable.prototype.on;
    Readable.prototype.removeListener = function(ev, fn) {
      let res = Stream.prototype.removeListener.call(this, ev, fn);
      if (ev === "readable")
        process2.nextTick(updateReadableListening, this);
      return res;
    };
    Readable.prototype.off = Readable.prototype.removeListener;
    Readable.prototype.removeAllListeners = function(ev) {
      let res = Stream.prototype.removeAllListeners.apply(this, arguments);
      if (ev === "readable" || ev === undefined)
        process2.nextTick(updateReadableListening, this);
      return res;
    };
    function updateReadableListening(self2) {
      let state = self2._readableState;
      if (state.readableListening = self2.listenerCount("readable") > 0, state.resumeScheduled && state[kPaused] === false)
        state.flowing = true;
      else if (self2.listenerCount("data") > 0)
        self2.resume();
      else if (!state.readableListening)
        state.flowing = null;
    }
    function nReadingNextTick(self2) {
      debug("readable nexttick read 0"), self2.read(0);
    }
    Readable.prototype.resume = function() {
      let state = this._readableState;
      if (!state.flowing)
        debug("resume"), state.flowing = !state.readableListening, resume(this, state);
      return state[kPaused] = false, this;
    };
    function resume(stream, state) {
      if (!state.resumeScheduled)
        state.resumeScheduled = true, process2.nextTick(resume_, stream, state);
    }
    function resume_(stream, state) {
      if (debug("resume", state.reading), !state.reading)
        stream.read(0);
      if (state.resumeScheduled = false, stream.emit("resume"), flow(stream), state.flowing && !state.reading)
        stream.read(0);
    }
    Readable.prototype.pause = function() {
      if (debug("call pause flowing=%j", this._readableState.flowing), this._readableState.flowing !== false)
        debug("pause"), this._readableState.flowing = false, this.emit("pause");
      return this._readableState[kPaused] = true, this;
    };
    function flow(stream) {
      let state = stream._readableState;
      debug("flow", state.flowing);
      while (state.flowing && stream.read() !== null)
        ;
    }
    Readable.prototype.wrap = function(stream) {
      let paused = false;
      stream.on("data", (chunk) => {
        if (!this.push(chunk) && stream.pause)
          paused = true, stream.pause();
      }), stream.on("end", () => {
        this.push(null);
      }), stream.on("error", (err) => {
        errorOrDestroy(this, err);
      }), stream.on("close", () => {
        this.destroy();
      }), stream.on("destroy", () => {
        this.destroy();
      }), this._read = () => {
        if (paused && stream.resume)
          paused = false, stream.resume();
      };
      let streamKeys = ObjectKeys(stream);
      for (let j = 1;j < streamKeys.length; j++) {
        let i2 = streamKeys[j];
        if (this[i2] === undefined && typeof stream[i2] === "function")
          this[i2] = stream[i2].bind(stream);
      }
      return this;
    };
    Readable.prototype[SymbolAsyncIterator] = function() {
      return streamToAsyncIterator(this);
    };
    Readable.prototype.iterator = function(options) {
      if (options !== undefined)
        validateObject(options, "options");
      return streamToAsyncIterator(this, options);
    };
    function streamToAsyncIterator(stream, options) {
      if (typeof stream.read !== "function")
        stream = Readable.wrap(stream, { objectMode: true });
      let iter = createAsyncIterator(stream, options);
      return iter.stream = stream, iter;
    }
    async function* createAsyncIterator(stream, options) {
      let callback = nop;
      function next(resolve) {
        if (this === stream)
          callback(), callback = nop;
        else
          callback = resolve;
      }
      stream.on("readable", next);
      let error, cleanup = eos(stream, { writable: false }, (err) => {
        error = err ? aggregateTwoErrors(error, err) : null, callback(), callback = nop;
      });
      try {
        while (true) {
          let chunk = stream.destroyed ? null : stream.read();
          if (chunk !== null)
            yield chunk;
          else if (error)
            throw error;
          else if (error === null)
            return;
          else
            await new Promise2(next);
        }
      } catch (err) {
        throw error = aggregateTwoErrors(error, err), error;
      } finally {
        if ((error || (options === null || options === undefined ? undefined : options.destroyOnReturn) !== false) && (error === undefined || stream._readableState.autoDestroy))
          destroyImpl.destroyer(stream, null);
        else
          stream.off("readable", next), cleanup();
      }
    }
    ObjectDefineProperties(Readable.prototype, { readable: { __proto__: null, get() {
      let r = this._readableState;
      return !!r && r.readable !== false && !r.destroyed && !r.errorEmitted && !r.endEmitted;
    }, set(val) {
      if (this._readableState)
        this._readableState.readable = !!val;
    } }, readableDidRead: { __proto__: null, enumerable: false, get: function() {
      return this._readableState.dataEmitted;
    } }, readableAborted: { __proto__: null, enumerable: false, get: function() {
      return !!(this._readableState.readable !== false && (this._readableState.destroyed || this._readableState.errored) && !this._readableState.endEmitted);
    } }, readableHighWaterMark: { __proto__: null, enumerable: false, get: function() {
      return this._readableState.highWaterMark;
    } }, readableBuffer: { __proto__: null, enumerable: false, get: function() {
      return this._readableState && this._readableState.buffer;
    } }, readableFlowing: { __proto__: null, enumerable: false, get: function() {
      return this._readableState.flowing;
    }, set: function(state) {
      if (this._readableState)
        this._readableState.flowing = state;
    } }, readableLength: { __proto__: null, enumerable: false, get() {
      return this._readableState.length;
    } }, readableObjectMode: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.objectMode : false;
    } }, readableEncoding: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.encoding : null;
    } }, errored: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.errored : null;
    } }, closed: { __proto__: null, get() {
      return this._readableState ? this._readableState.closed : false;
    } }, destroyed: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.destroyed : false;
    }, set(value) {
      if (!this._readableState)
        return;
      this._readableState.destroyed = value;
    } }, readableEnded: { __proto__: null, enumerable: false, get() {
      return this._readableState ? this._readableState.endEmitted : false;
    } } });
    ObjectDefineProperties(ReadableState.prototype, { pipesCount: { __proto__: null, get() {
      return this.pipes.length;
    } }, paused: { __proto__: null, get() {
      return this[kPaused] !== false;
    }, set(value) {
      this[kPaused] = !!value;
    } } });
    Readable._fromList = fromList;
    function fromList(n, state) {
      if (state.length === 0)
        return null;
      let ret;
      if (state.objectMode)
        ret = state.buffer.shift();
      else if (!n || n >= state.length) {
        if (state.decoder)
          ret = state.buffer.join("");
        else if (state.buffer.length === 1)
          ret = state.buffer.first();
        else
          ret = state.buffer.concat(state.length);
        state.buffer.clear();
      } else
        ret = state.buffer.consume(n, state.decoder);
      return ret;
    }
    function endReadable(stream) {
      let state = stream._readableState;
      if (debug("endReadable", state.endEmitted), !state.endEmitted)
        state.ended = true, process2.nextTick(endReadableNT, state, stream);
    }
    function endReadableNT(state, stream) {
      if (debug("endReadableNT", state.endEmitted, state.length), !state.errored && !state.closeEmitted && !state.endEmitted && state.length === 0) {
        if (state.endEmitted = true, stream.emit("end"), stream.writable && stream.allowHalfOpen === false)
          process2.nextTick(endWritableNT, stream);
        else if (state.autoDestroy) {
          let wState = stream._writableState;
          if (!wState || wState.autoDestroy && (wState.finished || wState.writable === false))
            stream.destroy();
        }
      }
    }
    function endWritableNT(stream) {
      if (stream.writable && !stream.writableEnded && !stream.destroyed)
        stream.end();
    }
    Readable.from = function(iterable, opts) {
      return from2(Readable, iterable, opts);
    };
    var webStreamsAdapters;
    function lazyWebStreams() {
      if (webStreamsAdapters === undefined)
        webStreamsAdapters = {};
      return webStreamsAdapters;
    }
    Readable.fromWeb = function(readableStream, options) {
      return lazyWebStreams().newStreamReadableFromReadableStream(readableStream, options);
    };
    Readable.toWeb = function(streamReadable, options) {
      return lazyWebStreams().newReadableStreamFromStreamReadable(streamReadable, options);
    };
    Readable.wrap = function(src, options) {
      var _ref, _src$readableObjectMo;
      return new Readable({ objectMode: (_ref = (_src$readableObjectMo = src.readableObjectMode) !== null && _src$readableObjectMo !== undefined ? _src$readableObjectMo : src.objectMode) !== null && _ref !== undefined ? _ref : true, ...options, destroy(err, callback) {
        destroyImpl.destroyer(src, err), callback(err);
      } }).wrap(src);
    };
  });
  var require_writable = __commonJS2((exports2, module2) => {
    var process2 = require_process(), { ArrayPrototypeSlice: ArrayPrototypeSlice2, Error: Error2, FunctionPrototypeSymbolHasInstance, ObjectDefineProperty, ObjectDefineProperties, ObjectSetPrototypeOf, StringPrototypeToLowerCase, Symbol: Symbol2, SymbolHasInstance } = require_primordials();
    module2.exports = Writable;
    Writable.WritableState = WritableState;
    var { EventEmitter: EE } = (init_events(), __toCommonJS(exports_events)), Stream = require_legacy().Stream, { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), destroyImpl = require_destroy(), { addAbortSignal } = require_add_abort_signal(), { getHighWaterMark, getDefaultHighWaterMark } = require_state(), { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_METHOD_NOT_IMPLEMENTED, ERR_MULTIPLE_CALLBACK, ERR_STREAM_CANNOT_PIPE, ERR_STREAM_DESTROYED, ERR_STREAM_ALREADY_FINISHED, ERR_STREAM_NULL_VALUES, ERR_STREAM_WRITE_AFTER_END, ERR_UNKNOWN_ENCODING } = require_errors().codes, { errorOrDestroy } = destroyImpl;
    ObjectSetPrototypeOf(Writable.prototype, Stream.prototype);
    ObjectSetPrototypeOf(Writable, Stream);
    function nop() {}
    var kOnFinished = Symbol2("kOnFinished");
    function WritableState(options, stream, isDuplex) {
      if (typeof isDuplex !== "boolean")
        isDuplex = stream instanceof require_duplex();
      if (this.objectMode = !!(options && options.objectMode), isDuplex)
        this.objectMode = this.objectMode || !!(options && options.writableObjectMode);
      this.highWaterMark = options ? getHighWaterMark(this, options, "writableHighWaterMark", isDuplex) : getDefaultHighWaterMark(false), this.finalCalled = false, this.needDrain = false, this.ending = false, this.ended = false, this.finished = false, this.destroyed = false;
      let noDecode = !!(options && options.decodeStrings === false);
      this.decodeStrings = !noDecode, this.defaultEncoding = options && options.defaultEncoding || "utf8", this.length = 0, this.writing = false, this.corked = 0, this.sync = true, this.bufferProcessing = false, this.onwrite = onwrite.bind(undefined, stream), this.writecb = null, this.writelen = 0, this.afterWriteTickInfo = null, resetBuffer(this), this.pendingcb = 0, this.constructed = true, this.prefinished = false, this.errorEmitted = false, this.emitClose = !options || options.emitClose !== false, this.autoDestroy = !options || options.autoDestroy !== false, this.errored = null, this.closed = false, this.closeEmitted = false, this[kOnFinished] = [];
    }
    function resetBuffer(state) {
      state.buffered = [], state.bufferedIndex = 0, state.allBuffers = true, state.allNoop = true;
    }
    WritableState.prototype.getBuffer = function() {
      return ArrayPrototypeSlice2(this.buffered, this.bufferedIndex);
    };
    ObjectDefineProperty(WritableState.prototype, "bufferedRequestCount", { __proto__: null, get() {
      return this.buffered.length - this.bufferedIndex;
    } });
    function Writable(options) {
      let isDuplex = this instanceof require_duplex();
      if (!isDuplex && !FunctionPrototypeSymbolHasInstance(Writable, this))
        return new Writable(options);
      if (this._writableState = new WritableState(options, this, isDuplex), options) {
        if (typeof options.write === "function")
          this._write = options.write;
        if (typeof options.writev === "function")
          this._writev = options.writev;
        if (typeof options.destroy === "function")
          this._destroy = options.destroy;
        if (typeof options.final === "function")
          this._final = options.final;
        if (typeof options.construct === "function")
          this._construct = options.construct;
        if (options.signal)
          addAbortSignal(options.signal, this);
      }
      Stream.call(this, options), destroyImpl.construct(this, () => {
        let state = this._writableState;
        if (!state.writing)
          clearBuffer(this, state);
        finishMaybe(this, state);
      });
    }
    ObjectDefineProperty(Writable, SymbolHasInstance, { __proto__: null, value: function(object) {
      if (FunctionPrototypeSymbolHasInstance(this, object))
        return true;
      if (this !== Writable)
        return false;
      return object && object._writableState instanceof WritableState;
    } });
    Writable.prototype.pipe = function() {
      errorOrDestroy(this, new ERR_STREAM_CANNOT_PIPE);
    };
    function _write(stream, chunk, encoding, cb) {
      let state = stream._writableState;
      if (typeof encoding === "function")
        cb = encoding, encoding = state.defaultEncoding;
      else {
        if (!encoding)
          encoding = state.defaultEncoding;
        else if (encoding !== "buffer" && !Buffer3.isEncoding(encoding))
          throw new ERR_UNKNOWN_ENCODING(encoding);
        if (typeof cb !== "function")
          cb = nop;
      }
      if (chunk === null)
        throw new ERR_STREAM_NULL_VALUES;
      else if (!state.objectMode)
        if (typeof chunk === "string") {
          if (state.decodeStrings !== false)
            chunk = Buffer3.from(chunk, encoding), encoding = "buffer";
        } else if (chunk instanceof Buffer3)
          encoding = "buffer";
        else if (Stream._isUint8Array(chunk))
          chunk = Stream._uint8ArrayToBuffer(chunk), encoding = "buffer";
        else
          throw new ERR_INVALID_ARG_TYPE3("chunk", ["string", "Buffer", "Uint8Array"], chunk);
      let err;
      if (state.ending)
        err = new ERR_STREAM_WRITE_AFTER_END;
      else if (state.destroyed)
        err = new ERR_STREAM_DESTROYED("write");
      if (err)
        return process2.nextTick(cb, err), errorOrDestroy(stream, err, true), err;
      return state.pendingcb++, writeOrBuffer(stream, state, chunk, encoding, cb);
    }
    Writable.prototype.write = function(chunk, encoding, cb) {
      return _write(this, chunk, encoding, cb) === true;
    };
    Writable.prototype.cork = function() {
      this._writableState.corked++;
    };
    Writable.prototype.uncork = function() {
      let state = this._writableState;
      if (state.corked) {
        if (state.corked--, !state.writing)
          clearBuffer(this, state);
      }
    };
    Writable.prototype.setDefaultEncoding = function(encoding) {
      if (typeof encoding === "string")
        encoding = StringPrototypeToLowerCase(encoding);
      if (!Buffer3.isEncoding(encoding))
        throw new ERR_UNKNOWN_ENCODING(encoding);
      return this._writableState.defaultEncoding = encoding, this;
    };
    function writeOrBuffer(stream, state, chunk, encoding, callback) {
      let len2 = state.objectMode ? 1 : chunk.length;
      state.length += len2;
      let ret = state.length < state.highWaterMark;
      if (!ret)
        state.needDrain = true;
      if (state.writing || state.corked || state.errored || !state.constructed) {
        if (state.buffered.push({ chunk, encoding, callback }), state.allBuffers && encoding !== "buffer")
          state.allBuffers = false;
        if (state.allNoop && callback !== nop)
          state.allNoop = false;
      } else
        state.writelen = len2, state.writecb = callback, state.writing = true, state.sync = true, stream._write(chunk, encoding, state.onwrite), state.sync = false;
      return ret && !state.errored && !state.destroyed;
    }
    function doWrite(stream, state, writev, len2, chunk, encoding, cb) {
      if (state.writelen = len2, state.writecb = cb, state.writing = true, state.sync = true, state.destroyed)
        state.onwrite(new ERR_STREAM_DESTROYED("write"));
      else if (writev)
        stream._writev(chunk, state.onwrite);
      else
        stream._write(chunk, encoding, state.onwrite);
      state.sync = false;
    }
    function onwriteError(stream, state, er, cb) {
      --state.pendingcb, cb(er), errorBuffer(state), errorOrDestroy(stream, er);
    }
    function onwrite(stream, er) {
      let state = stream._writableState, sync = state.sync, cb = state.writecb;
      if (typeof cb !== "function") {
        errorOrDestroy(stream, new ERR_MULTIPLE_CALLBACK);
        return;
      }
      if (state.writing = false, state.writecb = null, state.length -= state.writelen, state.writelen = 0, er) {
        if (er.stack, !state.errored)
          state.errored = er;
        if (stream._readableState && !stream._readableState.errored)
          stream._readableState.errored = er;
        if (sync)
          process2.nextTick(onwriteError, stream, state, er, cb);
        else
          onwriteError(stream, state, er, cb);
      } else {
        if (state.buffered.length > state.bufferedIndex)
          clearBuffer(stream, state);
        if (sync)
          if (state.afterWriteTickInfo !== null && state.afterWriteTickInfo.cb === cb)
            state.afterWriteTickInfo.count++;
          else
            state.afterWriteTickInfo = { count: 1, cb, stream, state }, process2.nextTick(afterWriteTick, state.afterWriteTickInfo);
        else
          afterWrite(stream, state, 1, cb);
      }
    }
    function afterWriteTick({ stream, state, count, cb }) {
      return state.afterWriteTickInfo = null, afterWrite(stream, state, count, cb);
    }
    function afterWrite(stream, state, count, cb) {
      if (!state.ending && !stream.destroyed && state.length === 0 && state.needDrain)
        state.needDrain = false, stream.emit("drain");
      while (count-- > 0)
        state.pendingcb--, cb();
      if (state.destroyed)
        errorBuffer(state);
      finishMaybe(stream, state);
    }
    function errorBuffer(state) {
      if (state.writing)
        return;
      for (let n = state.bufferedIndex;n < state.buffered.length; ++n) {
        var _state$errored;
        let { chunk, callback } = state.buffered[n], len2 = state.objectMode ? 1 : chunk.length;
        state.length -= len2, callback((_state$errored = state.errored) !== null && _state$errored !== undefined ? _state$errored : new ERR_STREAM_DESTROYED("write"));
      }
      let onfinishCallbacks = state[kOnFinished].splice(0);
      for (let i2 = 0;i2 < onfinishCallbacks.length; i2++) {
        var _state$errored2;
        onfinishCallbacks[i2]((_state$errored2 = state.errored) !== null && _state$errored2 !== undefined ? _state$errored2 : new ERR_STREAM_DESTROYED("end"));
      }
      resetBuffer(state);
    }
    function clearBuffer(stream, state) {
      if (state.corked || state.bufferProcessing || state.destroyed || !state.constructed)
        return;
      let { buffered, bufferedIndex, objectMode } = state, bufferedLength = buffered.length - bufferedIndex;
      if (!bufferedLength)
        return;
      let i2 = bufferedIndex;
      if (state.bufferProcessing = true, bufferedLength > 1 && stream._writev) {
        state.pendingcb -= bufferedLength - 1;
        let callback = state.allNoop ? nop : (err) => {
          for (let n = i2;n < buffered.length; ++n)
            buffered[n].callback(err);
        }, chunks = state.allNoop && i2 === 0 ? buffered : ArrayPrototypeSlice2(buffered, i2);
        chunks.allBuffers = state.allBuffers, doWrite(stream, state, true, state.length, chunks, "", callback), resetBuffer(state);
      } else {
        do {
          let { chunk, encoding, callback } = buffered[i2];
          buffered[i2++] = null;
          let len2 = objectMode ? 1 : chunk.length;
          doWrite(stream, state, false, len2, chunk, encoding, callback);
        } while (i2 < buffered.length && !state.writing);
        if (i2 === buffered.length)
          resetBuffer(state);
        else if (i2 > 256)
          buffered.splice(0, i2), state.bufferedIndex = 0;
        else
          state.bufferedIndex = i2;
      }
      state.bufferProcessing = false;
    }
    Writable.prototype._write = function(chunk, encoding, cb) {
      if (this._writev)
        this._writev([{ chunk, encoding }], cb);
      else
        throw new ERR_METHOD_NOT_IMPLEMENTED("_write()");
    };
    Writable.prototype._writev = null;
    Writable.prototype.end = function(chunk, encoding, cb) {
      let state = this._writableState;
      if (typeof chunk === "function")
        cb = chunk, chunk = null, encoding = null;
      else if (typeof encoding === "function")
        cb = encoding, encoding = null;
      let err;
      if (chunk !== null && chunk !== undefined) {
        let ret = _write(this, chunk, encoding);
        if (ret instanceof Error2)
          err = ret;
      }
      if (state.corked)
        state.corked = 1, this.uncork();
      if (err)
        ;
      else if (!state.errored && !state.ending)
        state.ending = true, finishMaybe(this, state, true), state.ended = true;
      else if (state.finished)
        err = new ERR_STREAM_ALREADY_FINISHED("end");
      else if (state.destroyed)
        err = new ERR_STREAM_DESTROYED("end");
      if (typeof cb === "function")
        if (err || state.finished)
          process2.nextTick(cb, err);
        else
          state[kOnFinished].push(cb);
      return this;
    };
    function needFinish(state) {
      return state.ending && !state.destroyed && state.constructed && state.length === 0 && !state.errored && state.buffered.length === 0 && !state.finished && !state.writing && !state.errorEmitted && !state.closeEmitted;
    }
    function callFinal(stream, state) {
      let called = false;
      function onFinish(err) {
        if (called) {
          errorOrDestroy(stream, err !== null && err !== undefined ? err : ERR_MULTIPLE_CALLBACK());
          return;
        }
        if (called = true, state.pendingcb--, err) {
          let onfinishCallbacks = state[kOnFinished].splice(0);
          for (let i2 = 0;i2 < onfinishCallbacks.length; i2++)
            onfinishCallbacks[i2](err);
          errorOrDestroy(stream, err, state.sync);
        } else if (needFinish(state))
          state.prefinished = true, stream.emit("prefinish"), state.pendingcb++, process2.nextTick(finish, stream, state);
      }
      state.sync = true, state.pendingcb++;
      try {
        stream._final(onFinish);
      } catch (err) {
        onFinish(err);
      }
      state.sync = false;
    }
    function prefinish(stream, state) {
      if (!state.prefinished && !state.finalCalled)
        if (typeof stream._final === "function" && !state.destroyed)
          state.finalCalled = true, callFinal(stream, state);
        else
          state.prefinished = true, stream.emit("prefinish");
    }
    function finishMaybe(stream, state, sync) {
      if (needFinish(state)) {
        if (prefinish(stream, state), state.pendingcb === 0) {
          if (sync)
            state.pendingcb++, process2.nextTick((stream2, state2) => {
              if (needFinish(state2))
                finish(stream2, state2);
              else
                state2.pendingcb--;
            }, stream, state);
          else if (needFinish(state))
            state.pendingcb++, finish(stream, state);
        }
      }
    }
    function finish(stream, state) {
      state.pendingcb--, state.finished = true;
      let onfinishCallbacks = state[kOnFinished].splice(0);
      for (let i2 = 0;i2 < onfinishCallbacks.length; i2++)
        onfinishCallbacks[i2]();
      if (stream.emit("finish"), state.autoDestroy) {
        let rState = stream._readableState;
        if (!rState || rState.autoDestroy && (rState.endEmitted || rState.readable === false))
          stream.destroy();
      }
    }
    ObjectDefineProperties(Writable.prototype, { closed: { __proto__: null, get() {
      return this._writableState ? this._writableState.closed : false;
    } }, destroyed: { __proto__: null, get() {
      return this._writableState ? this._writableState.destroyed : false;
    }, set(value) {
      if (this._writableState)
        this._writableState.destroyed = value;
    } }, writable: { __proto__: null, get() {
      let w = this._writableState;
      return !!w && w.writable !== false && !w.destroyed && !w.errored && !w.ending && !w.ended;
    }, set(val) {
      if (this._writableState)
        this._writableState.writable = !!val;
    } }, writableFinished: { __proto__: null, get() {
      return this._writableState ? this._writableState.finished : false;
    } }, writableObjectMode: { __proto__: null, get() {
      return this._writableState ? this._writableState.objectMode : false;
    } }, writableBuffer: { __proto__: null, get() {
      return this._writableState && this._writableState.getBuffer();
    } }, writableEnded: { __proto__: null, get() {
      return this._writableState ? this._writableState.ending : false;
    } }, writableNeedDrain: { __proto__: null, get() {
      let wState = this._writableState;
      if (!wState)
        return false;
      return !wState.destroyed && !wState.ending && wState.needDrain;
    } }, writableHighWaterMark: { __proto__: null, get() {
      return this._writableState && this._writableState.highWaterMark;
    } }, writableCorked: { __proto__: null, get() {
      return this._writableState ? this._writableState.corked : 0;
    } }, writableLength: { __proto__: null, get() {
      return this._writableState && this._writableState.length;
    } }, errored: { __proto__: null, enumerable: false, get() {
      return this._writableState ? this._writableState.errored : null;
    } }, writableAborted: { __proto__: null, enumerable: false, get: function() {
      return !!(this._writableState.writable !== false && (this._writableState.destroyed || this._writableState.errored) && !this._writableState.finished);
    } } });
    var destroy = destroyImpl.destroy;
    Writable.prototype.destroy = function(err, cb) {
      let state = this._writableState;
      if (!state.destroyed && (state.bufferedIndex < state.buffered.length || state[kOnFinished].length))
        process2.nextTick(errorBuffer, state);
      return destroy.call(this, err, cb), this;
    };
    Writable.prototype._undestroy = destroyImpl.undestroy;
    Writable.prototype._destroy = function(err, cb) {
      cb(err);
    };
    Writable.prototype[EE.captureRejectionSymbol] = function(err) {
      this.destroy(err);
    };
    var webStreamsAdapters;
    function lazyWebStreams() {
      if (webStreamsAdapters === undefined)
        webStreamsAdapters = {};
      return webStreamsAdapters;
    }
    Writable.fromWeb = function(writableStream, options) {
      return lazyWebStreams().newStreamWritableFromWritableStream(writableStream, options);
    };
    Writable.toWeb = function(streamWritable) {
      return lazyWebStreams().newWritableStreamFromStreamWritable(streamWritable);
    };
  });
  var require_duplexify = __commonJS2((exports2, module2) => {
    var process2 = require_process(), bufferModule = (init_buffer(), __toCommonJS(exports_buffer)), { isReadable, isWritable, isIterable, isNodeStream, isReadableNodeStream, isWritableNodeStream, isDuplexNodeStream, isReadableStream, isWritableStream } = require_utils(), eos = require_end_of_stream(), { AbortError: AbortError2, codes: { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_INVALID_RETURN_VALUE } } = require_errors(), { destroyer } = require_destroy(), Duplex = require_duplex(), Readable = require_readable(), Writable = require_writable(), { createDeferredPromise } = require_util(), from2 = require_from(), Blob3 = globalThis.Blob || bufferModule.Blob, isBlob = typeof Blob3 < "u" ? function(b) {
      return b instanceof Blob3;
    } : function(b) {
      return false;
    }, AbortController2 = globalThis.AbortController || require_abort_controller().AbortController, { FunctionPrototypeCall } = require_primordials();

    class Duplexify extends Duplex {
      constructor(options) {
        super(options);
        if ((options === null || options === undefined ? undefined : options.readable) === false)
          this._readableState.readable = false, this._readableState.ended = true, this._readableState.endEmitted = true;
        if ((options === null || options === undefined ? undefined : options.writable) === false)
          this._writableState.writable = false, this._writableState.ending = true, this._writableState.ended = true, this._writableState.finished = true;
      }
    }
    module2.exports = function duplexify(body, name) {
      if (isDuplexNodeStream(body))
        return body;
      if (isReadableNodeStream(body))
        return _duplexify({ readable: body });
      if (isWritableNodeStream(body))
        return _duplexify({ writable: body });
      if (isNodeStream(body))
        return _duplexify({ writable: false, readable: false });
      if (isReadableStream(body))
        return _duplexify({ readable: Readable.fromWeb(body) });
      if (isWritableStream(body))
        return _duplexify({ writable: Writable.fromWeb(body) });
      if (typeof body === "function") {
        let { value, write: write2, final, destroy } = fromAsyncGen(body);
        if (isIterable(value))
          return from2(Duplexify, value, { objectMode: true, write: write2, final, destroy });
        let then2 = value === null || value === undefined ? undefined : value.then;
        if (typeof then2 === "function") {
          let d, promise = FunctionPrototypeCall(then2, value, (val) => {
            if (val != null)
              throw new ERR_INVALID_RETURN_VALUE("nully", "body", val);
          }, (err) => {
            destroyer(d, err);
          });
          return d = new Duplexify({ objectMode: true, readable: false, write: write2, final(cb) {
            final(async () => {
              try {
                await promise, process2.nextTick(cb, null);
              } catch (err) {
                process2.nextTick(cb, err);
              }
            });
          }, destroy });
        }
        throw new ERR_INVALID_RETURN_VALUE("Iterable, AsyncIterable or AsyncFunction", name, value);
      }
      if (isBlob(body))
        return duplexify(body.arrayBuffer());
      if (isIterable(body))
        return from2(Duplexify, body, { objectMode: true, writable: false });
      if (isReadableStream(body === null || body === undefined ? undefined : body.readable) && isWritableStream(body === null || body === undefined ? undefined : body.writable))
        return Duplexify.fromWeb(body);
      if (typeof (body === null || body === undefined ? undefined : body.writable) === "object" || typeof (body === null || body === undefined ? undefined : body.readable) === "object") {
        let readable = body !== null && body !== undefined && body.readable ? isReadableNodeStream(body === null || body === undefined ? undefined : body.readable) ? body === null || body === undefined ? undefined : body.readable : duplexify(body.readable) : undefined, writable = body !== null && body !== undefined && body.writable ? isWritableNodeStream(body === null || body === undefined ? undefined : body.writable) ? body === null || body === undefined ? undefined : body.writable : duplexify(body.writable) : undefined;
        return _duplexify({ readable, writable });
      }
      let then = body === null || body === undefined ? undefined : body.then;
      if (typeof then === "function") {
        let d;
        return FunctionPrototypeCall(then, body, (val) => {
          if (val != null)
            d.push(val);
          d.push(null);
        }, (err) => {
          destroyer(d, err);
        }), d = new Duplexify({ objectMode: true, writable: false, read() {} });
      }
      throw new ERR_INVALID_ARG_TYPE3(name, ["Blob", "ReadableStream", "WritableStream", "Stream", "Iterable", "AsyncIterable", "Function", "{ readable, writable } pair", "Promise"], body);
    };
    function fromAsyncGen(fn) {
      let { promise, resolve } = createDeferredPromise(), ac = new AbortController2, signal = ac.signal;
      return { value: fn(async function* () {
        while (true) {
          let _promise = promise;
          promise = null;
          let { chunk, done, cb } = await _promise;
          if (process2.nextTick(cb), done)
            return;
          if (signal.aborted)
            throw new AbortError2(undefined, { cause: signal.reason });
          ({ promise, resolve } = createDeferredPromise()), yield chunk;
        }
      }(), { signal }), write(chunk, encoding, cb) {
        let _resolve = resolve;
        resolve = null, _resolve({ chunk, done: false, cb });
      }, final(cb) {
        let _resolve = resolve;
        resolve = null, _resolve({ done: true, cb });
      }, destroy(err, cb) {
        ac.abort(), cb(err);
      } };
    }
    function _duplexify(pair) {
      let r = pair.readable && typeof pair.readable.read !== "function" ? Readable.wrap(pair.readable) : pair.readable, w = pair.writable, readable = !!isReadable(r), writable = !!isWritable(w), ondrain, onfinish, onreadable, onclose, d;
      function onfinished(err) {
        let cb = onclose;
        if (onclose = null, cb)
          cb(err);
        else if (err)
          d.destroy(err);
      }
      if (d = new Duplexify({ readableObjectMode: !!(r !== null && r !== undefined && r.readableObjectMode), writableObjectMode: !!(w !== null && w !== undefined && w.writableObjectMode), readable, writable }), writable)
        eos(w, (err) => {
          if (writable = false, err)
            destroyer(r, err);
          onfinished(err);
        }), d._write = function(chunk, encoding, callback) {
          if (w.write(chunk, encoding))
            callback();
          else
            ondrain = callback;
        }, d._final = function(callback) {
          w.end(), onfinish = callback;
        }, w.on("drain", function() {
          if (ondrain) {
            let cb = ondrain;
            ondrain = null, cb();
          }
        }), w.on("finish", function() {
          if (onfinish) {
            let cb = onfinish;
            onfinish = null, cb();
          }
        });
      if (readable)
        eos(r, (err) => {
          if (readable = false, err)
            destroyer(r, err);
          onfinished(err);
        }), r.on("readable", function() {
          if (onreadable) {
            let cb = onreadable;
            onreadable = null, cb();
          }
        }), r.on("end", function() {
          d.push(null);
        }), d._read = function() {
          while (true) {
            let buf = r.read();
            if (buf === null) {
              onreadable = d._read;
              return;
            }
            if (!d.push(buf))
              return;
          }
        };
      return d._destroy = function(err, callback) {
        if (!err && onclose !== null)
          err = new AbortError2;
        if (onreadable = null, ondrain = null, onfinish = null, onclose === null)
          callback(err);
        else
          onclose = callback, destroyer(w, err), destroyer(r, err);
      }, d;
    }
  });
  var require_duplex = __commonJS2((exports2, module2) => {
    var { ObjectDefineProperties, ObjectGetOwnPropertyDescriptor, ObjectKeys, ObjectSetPrototypeOf } = require_primordials();
    module2.exports = Duplex;
    var Readable = require_readable(), Writable = require_writable();
    ObjectSetPrototypeOf(Duplex.prototype, Readable.prototype);
    ObjectSetPrototypeOf(Duplex, Readable);
    {
      let keys = ObjectKeys(Writable.prototype);
      for (let i2 = 0;i2 < keys.length; i2++) {
        let method = keys[i2];
        if (!Duplex.prototype[method])
          Duplex.prototype[method] = Writable.prototype[method];
      }
    }
    function Duplex(options) {
      if (!(this instanceof Duplex))
        return new Duplex(options);
      if (Readable.call(this, options), Writable.call(this, options), options) {
        if (this.allowHalfOpen = options.allowHalfOpen !== false, options.readable === false)
          this._readableState.readable = false, this._readableState.ended = true, this._readableState.endEmitted = true;
        if (options.writable === false)
          this._writableState.writable = false, this._writableState.ending = true, this._writableState.ended = true, this._writableState.finished = true;
      } else
        this.allowHalfOpen = true;
    }
    ObjectDefineProperties(Duplex.prototype, { writable: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writable") }, writableHighWaterMark: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableHighWaterMark") }, writableObjectMode: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableObjectMode") }, writableBuffer: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableBuffer") }, writableLength: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableLength") }, writableFinished: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableFinished") }, writableCorked: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableCorked") }, writableEnded: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableEnded") }, writableNeedDrain: { __proto__: null, ...ObjectGetOwnPropertyDescriptor(Writable.prototype, "writableNeedDrain") }, destroyed: { __proto__: null, get() {
      if (this._readableState === undefined || this._writableState === undefined)
        return false;
      return this._readableState.destroyed && this._writableState.destroyed;
    }, set(value) {
      if (this._readableState && this._writableState)
        this._readableState.destroyed = value, this._writableState.destroyed = value;
    } } });
    var webStreamsAdapters;
    function lazyWebStreams() {
      if (webStreamsAdapters === undefined)
        webStreamsAdapters = {};
      return webStreamsAdapters;
    }
    Duplex.fromWeb = function(pair, options) {
      return lazyWebStreams().newStreamDuplexFromReadableWritablePair(pair, options);
    };
    Duplex.toWeb = function(duplex) {
      return lazyWebStreams().newReadableWritablePairFromDuplex(duplex);
    };
    var duplexify;
    Duplex.from = function(body) {
      if (!duplexify)
        duplexify = require_duplexify();
      return duplexify(body, "body");
    };
  });
  var require_transform = __commonJS2((exports2, module2) => {
    var { ObjectSetPrototypeOf, Symbol: Symbol2 } = require_primordials();
    module2.exports = Transform;
    var { ERR_METHOD_NOT_IMPLEMENTED } = require_errors().codes, Duplex = require_duplex(), { getHighWaterMark } = require_state();
    ObjectSetPrototypeOf(Transform.prototype, Duplex.prototype);
    ObjectSetPrototypeOf(Transform, Duplex);
    var kCallback = Symbol2("kCallback");
    function Transform(options) {
      if (!(this instanceof Transform))
        return new Transform(options);
      let readableHighWaterMark = options ? getHighWaterMark(this, options, "readableHighWaterMark", true) : null;
      if (readableHighWaterMark === 0)
        options = { ...options, highWaterMark: null, readableHighWaterMark, writableHighWaterMark: options.writableHighWaterMark || 0 };
      if (Duplex.call(this, options), this._readableState.sync = false, this[kCallback] = null, options) {
        if (typeof options.transform === "function")
          this._transform = options.transform;
        if (typeof options.flush === "function")
          this._flush = options.flush;
      }
      this.on("prefinish", prefinish);
    }
    function final(cb) {
      if (typeof this._flush === "function" && !this.destroyed)
        this._flush((er, data) => {
          if (er) {
            if (cb)
              cb(er);
            else
              this.destroy(er);
            return;
          }
          if (data != null)
            this.push(data);
          if (this.push(null), cb)
            cb();
        });
      else if (this.push(null), cb)
        cb();
    }
    function prefinish() {
      if (this._final !== final)
        final.call(this);
    }
    Transform.prototype._final = final;
    Transform.prototype._transform = function(chunk, encoding, callback) {
      throw new ERR_METHOD_NOT_IMPLEMENTED("_transform()");
    };
    Transform.prototype._write = function(chunk, encoding, callback) {
      let rState = this._readableState, wState = this._writableState, length = rState.length;
      this._transform(chunk, encoding, (err, val) => {
        if (err) {
          callback(err);
          return;
        }
        if (val != null)
          this.push(val);
        if (wState.ended || length === rState.length || rState.length < rState.highWaterMark)
          callback();
        else
          this[kCallback] = callback;
      });
    };
    Transform.prototype._read = function() {
      if (this[kCallback]) {
        let callback = this[kCallback];
        this[kCallback] = null, callback();
      }
    };
  });
  var require_passthrough = __commonJS2((exports2, module2) => {
    var { ObjectSetPrototypeOf } = require_primordials();
    module2.exports = PassThrough;
    var Transform = require_transform();
    ObjectSetPrototypeOf(PassThrough.prototype, Transform.prototype);
    ObjectSetPrototypeOf(PassThrough, Transform);
    function PassThrough(options) {
      if (!(this instanceof PassThrough))
        return new PassThrough(options);
      Transform.call(this, options);
    }
    PassThrough.prototype._transform = function(chunk, encoding, cb) {
      cb(null, chunk);
    };
  });
  var require_pipeline = __commonJS2((exports2, module2) => {
    var process2 = require_process(), { ArrayIsArray, Promise: Promise2, SymbolAsyncIterator, SymbolDispose } = require_primordials(), eos = require_end_of_stream(), { once } = require_util(), destroyImpl = require_destroy(), Duplex = require_duplex(), { aggregateTwoErrors, codes: { ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_INVALID_RETURN_VALUE, ERR_MISSING_ARGS, ERR_STREAM_DESTROYED, ERR_STREAM_PREMATURE_CLOSE }, AbortError: AbortError2 } = require_errors(), { validateFunction, validateAbortSignal: validateAbortSignal2 } = require_validators(), { isIterable, isReadable, isReadableNodeStream, isNodeStream, isTransformStream, isWebStream, isReadableStream, isReadableFinished } = require_utils(), AbortController2 = globalThis.AbortController || require_abort_controller().AbortController, PassThrough, Readable, addAbortListener2;
    function destroyer(stream, reading, writing) {
      let finished = false;
      stream.on("close", () => {
        finished = true;
      });
      let cleanup = eos(stream, { readable: reading, writable: writing }, (err) => {
        finished = !err;
      });
      return { destroy: (err) => {
        if (finished)
          return;
        finished = true, destroyImpl.destroyer(stream, err || new ERR_STREAM_DESTROYED("pipe"));
      }, cleanup };
    }
    function popCallback(streams) {
      return validateFunction(streams[streams.length - 1], "streams[stream.length - 1]"), streams.pop();
    }
    function makeAsyncIterable(val) {
      if (isIterable(val))
        return val;
      else if (isReadableNodeStream(val))
        return fromReadable(val);
      throw new ERR_INVALID_ARG_TYPE3("val", ["Readable", "Iterable", "AsyncIterable"], val);
    }
    async function* fromReadable(val) {
      if (!Readable)
        Readable = require_readable();
      yield* Readable.prototype[SymbolAsyncIterator].call(val);
    }
    async function pumpToNode(iterable, writable, finish, { end }) {
      let error, onresolve = null, resume = (err) => {
        if (err)
          error = err;
        if (onresolve) {
          let callback = onresolve;
          onresolve = null, callback();
        }
      }, wait = () => new Promise2((resolve, reject) => {
        if (error)
          reject(error);
        else
          onresolve = () => {
            if (error)
              reject(error);
            else
              resolve();
          };
      });
      writable.on("drain", resume);
      let cleanup = eos(writable, { readable: false }, resume);
      try {
        if (writable.writableNeedDrain)
          await wait();
        for await (let chunk of iterable)
          if (!writable.write(chunk))
            await wait();
        if (end)
          writable.end(), await wait();
        finish();
      } catch (err) {
        finish(error !== err ? aggregateTwoErrors(error, err) : err);
      } finally {
        cleanup(), writable.off("drain", resume);
      }
    }
    async function pumpToWeb(readable, writable, finish, { end }) {
      if (isTransformStream(writable))
        writable = writable.writable;
      let writer = writable.getWriter();
      try {
        for await (let chunk of readable)
          await writer.ready, writer.write(chunk).catch(() => {});
        if (await writer.ready, end)
          await writer.close();
        finish();
      } catch (err) {
        try {
          await writer.abort(err), finish(err);
        } catch (err2) {
          finish(err2);
        }
      }
    }
    function pipeline(...streams) {
      return pipelineImpl(streams, once(popCallback(streams)));
    }
    function pipelineImpl(streams, callback, opts) {
      if (streams.length === 1 && ArrayIsArray(streams[0]))
        streams = streams[0];
      if (streams.length < 2)
        throw new ERR_MISSING_ARGS("streams");
      let ac = new AbortController2, signal = ac.signal, outerSignal = opts === null || opts === undefined ? undefined : opts.signal, lastStreamCleanup = [];
      validateAbortSignal2(outerSignal, "options.signal");
      function abort() {
        finishImpl(new AbortError2);
      }
      addAbortListener2 = addAbortListener2 || require_util().addAbortListener;
      let disposable;
      if (outerSignal)
        disposable = addAbortListener2(outerSignal, abort);
      let error, value, destroys = [], finishCount = 0;
      function finish(err) {
        finishImpl(err, --finishCount === 0);
      }
      function finishImpl(err, final) {
        var _disposable;
        if (err && (!error || error.code === "ERR_STREAM_PREMATURE_CLOSE"))
          error = err;
        if (!error && !final)
          return;
        while (destroys.length)
          destroys.shift()(error);
        if ((_disposable = disposable) === null || _disposable === undefined || _disposable[SymbolDispose](), ac.abort(), final) {
          if (!error)
            lastStreamCleanup.forEach((fn) => fn());
          process2.nextTick(callback, error, value);
        }
      }
      let ret;
      for (let i2 = 0;i2 < streams.length; i2++) {
        let stream = streams[i2], reading = i2 < streams.length - 1, writing = i2 > 0, end = reading || (opts === null || opts === undefined ? undefined : opts.end) !== false, isLastStream = i2 === streams.length - 1;
        if (isNodeStream(stream)) {
          let onError2 = function(err) {
            if (err && err.name !== "AbortError" && err.code !== "ERR_STREAM_PREMATURE_CLOSE")
              finish(err);
          };
          var onError = onError2;
          if (end) {
            let { destroy, cleanup } = destroyer(stream, reading, writing);
            if (destroys.push(destroy), isReadable(stream) && isLastStream)
              lastStreamCleanup.push(cleanup);
          }
          if (stream.on("error", onError2), isReadable(stream) && isLastStream)
            lastStreamCleanup.push(() => {
              stream.removeListener("error", onError2);
            });
        }
        if (i2 === 0)
          if (typeof stream === "function") {
            if (ret = stream({ signal }), !isIterable(ret))
              throw new ERR_INVALID_RETURN_VALUE("Iterable, AsyncIterable or Stream", "source", ret);
          } else if (isIterable(stream) || isReadableNodeStream(stream) || isTransformStream(stream))
            ret = stream;
          else
            ret = Duplex.from(stream);
        else if (typeof stream === "function") {
          if (isTransformStream(ret)) {
            var _ret;
            ret = makeAsyncIterable((_ret = ret) === null || _ret === undefined ? undefined : _ret.readable);
          } else
            ret = makeAsyncIterable(ret);
          if (ret = stream(ret, { signal }), reading) {
            if (!isIterable(ret, true))
              throw new ERR_INVALID_RETURN_VALUE("AsyncIterable", `transform[${i2 - 1}]`, ret);
          } else {
            var _ret2;
            if (!PassThrough)
              PassThrough = require_passthrough();
            let pt = new PassThrough({ objectMode: true }), then = (_ret2 = ret) === null || _ret2 === undefined ? undefined : _ret2.then;
            if (typeof then === "function")
              finishCount++, then.call(ret, (val) => {
                if (value = val, val != null)
                  pt.write(val);
                if (end)
                  pt.end();
                process2.nextTick(finish);
              }, (err) => {
                pt.destroy(err), process2.nextTick(finish, err);
              });
            else if (isIterable(ret, true))
              finishCount++, pumpToNode(ret, pt, finish, { end });
            else if (isReadableStream(ret) || isTransformStream(ret)) {
              let toRead = ret.readable || ret;
              finishCount++, pumpToNode(toRead, pt, finish, { end });
            } else
              throw new ERR_INVALID_RETURN_VALUE("AsyncIterable or Promise", "destination", ret);
            ret = pt;
            let { destroy, cleanup } = destroyer(ret, false, true);
            if (destroys.push(destroy), isLastStream)
              lastStreamCleanup.push(cleanup);
          }
        } else if (isNodeStream(stream)) {
          if (isReadableNodeStream(ret)) {
            finishCount += 2;
            let cleanup = pipe(ret, stream, finish, { end });
            if (isReadable(stream) && isLastStream)
              lastStreamCleanup.push(cleanup);
          } else if (isTransformStream(ret) || isReadableStream(ret)) {
            let toRead = ret.readable || ret;
            finishCount++, pumpToNode(toRead, stream, finish, { end });
          } else if (isIterable(ret))
            finishCount++, pumpToNode(ret, stream, finish, { end });
          else
            throw new ERR_INVALID_ARG_TYPE3("val", ["Readable", "Iterable", "AsyncIterable", "ReadableStream", "TransformStream"], ret);
          ret = stream;
        } else if (isWebStream(stream)) {
          if (isReadableNodeStream(ret))
            finishCount++, pumpToWeb(makeAsyncIterable(ret), stream, finish, { end });
          else if (isReadableStream(ret) || isIterable(ret))
            finishCount++, pumpToWeb(ret, stream, finish, { end });
          else if (isTransformStream(ret))
            finishCount++, pumpToWeb(ret.readable, stream, finish, { end });
          else
            throw new ERR_INVALID_ARG_TYPE3("val", ["Readable", "Iterable", "AsyncIterable", "ReadableStream", "TransformStream"], ret);
          ret = stream;
        } else
          ret = Duplex.from(stream);
      }
      if (signal !== null && signal !== undefined && signal.aborted || outerSignal !== null && outerSignal !== undefined && outerSignal.aborted)
        process2.nextTick(abort);
      return ret;
    }
    function pipe(src, dst, finish, { end }) {
      let ended = false;
      if (dst.on("close", () => {
        if (!ended)
          finish(new ERR_STREAM_PREMATURE_CLOSE);
      }), src.pipe(dst, { end: false }), end) {
        let endFn2 = function() {
          ended = true, dst.end();
        };
        var endFn = endFn2;
        if (isReadableFinished(src))
          process2.nextTick(endFn2);
        else
          src.once("end", endFn2);
      } else
        finish();
      return eos(src, { readable: true, writable: false }, (err) => {
        let rState = src._readableState;
        if (err && err.code === "ERR_STREAM_PREMATURE_CLOSE" && rState && rState.ended && !rState.errored && !rState.errorEmitted)
          src.once("end", finish).once("error", finish);
        else
          finish(err);
      }), eos(dst, { readable: false, writable: true }, finish);
    }
    module2.exports = { pipelineImpl, pipeline };
  });
  var require_compose = __commonJS2((exports2, module2) => {
    var { pipeline } = require_pipeline(), Duplex = require_duplex(), { destroyer } = require_destroy(), { isNodeStream, isReadable, isWritable, isWebStream, isTransformStream, isWritableStream, isReadableStream } = require_utils(), { AbortError: AbortError2, codes: { ERR_INVALID_ARG_VALUE, ERR_MISSING_ARGS } } = require_errors(), eos = require_end_of_stream();
    module2.exports = function(...streams) {
      if (streams.length === 0)
        throw new ERR_MISSING_ARGS("streams");
      if (streams.length === 1)
        return Duplex.from(streams[0]);
      let orgStreams = [...streams];
      if (typeof streams[0] === "function")
        streams[0] = Duplex.from(streams[0]);
      if (typeof streams[streams.length - 1] === "function") {
        let idx = streams.length - 1;
        streams[idx] = Duplex.from(streams[idx]);
      }
      for (let n = 0;n < streams.length; ++n) {
        if (!isNodeStream(streams[n]) && !isWebStream(streams[n]))
          continue;
        if (n < streams.length - 1 && !(isReadable(streams[n]) || isReadableStream(streams[n]) || isTransformStream(streams[n])))
          throw new ERR_INVALID_ARG_VALUE(`streams[${n}]`, orgStreams[n], "must be readable");
        if (n > 0 && !(isWritable(streams[n]) || isWritableStream(streams[n]) || isTransformStream(streams[n])))
          throw new ERR_INVALID_ARG_VALUE(`streams[${n}]`, orgStreams[n], "must be writable");
      }
      let ondrain, onfinish, onreadable, onclose, d;
      function onfinished(err) {
        let cb = onclose;
        if (onclose = null, cb)
          cb(err);
        else if (err)
          d.destroy(err);
        else if (!readable && !writable)
          d.destroy();
      }
      let head = streams[0], tail = pipeline(streams, onfinished), writable = !!(isWritable(head) || isWritableStream(head) || isTransformStream(head)), readable = !!(isReadable(tail) || isReadableStream(tail) || isTransformStream(tail));
      if (d = new Duplex({ writableObjectMode: !!(head !== null && head !== undefined && head.writableObjectMode), readableObjectMode: !!(tail !== null && tail !== undefined && tail.readableObjectMode), writable, readable }), writable) {
        if (isNodeStream(head))
          d._write = function(chunk, encoding, callback) {
            if (head.write(chunk, encoding))
              callback();
            else
              ondrain = callback;
          }, d._final = function(callback) {
            head.end(), onfinish = callback;
          }, head.on("drain", function() {
            if (ondrain) {
              let cb = ondrain;
              ondrain = null, cb();
            }
          });
        else if (isWebStream(head)) {
          let writer = (isTransformStream(head) ? head.writable : head).getWriter();
          d._write = async function(chunk, encoding, callback) {
            try {
              await writer.ready, writer.write(chunk).catch(() => {}), callback();
            } catch (err) {
              callback(err);
            }
          }, d._final = async function(callback) {
            try {
              await writer.ready, writer.close().catch(() => {}), onfinish = callback;
            } catch (err) {
              callback(err);
            }
          };
        }
        let toRead = isTransformStream(tail) ? tail.readable : tail;
        eos(toRead, () => {
          if (onfinish) {
            let cb = onfinish;
            onfinish = null, cb();
          }
        });
      }
      if (readable) {
        if (isNodeStream(tail))
          tail.on("readable", function() {
            if (onreadable) {
              let cb = onreadable;
              onreadable = null, cb();
            }
          }), tail.on("end", function() {
            d.push(null);
          }), d._read = function() {
            while (true) {
              let buf = tail.read();
              if (buf === null) {
                onreadable = d._read;
                return;
              }
              if (!d.push(buf))
                return;
            }
          };
        else if (isWebStream(tail)) {
          let reader = (isTransformStream(tail) ? tail.readable : tail).getReader();
          d._read = async function() {
            while (true)
              try {
                let { value, done } = await reader.read();
                if (!d.push(value))
                  return;
                if (done) {
                  d.push(null);
                  return;
                }
              } catch {
                return;
              }
          };
        }
      }
      return d._destroy = function(err, callback) {
        if (!err && onclose !== null)
          err = new AbortError2;
        if (onreadable = null, ondrain = null, onfinish = null, onclose === null)
          callback(err);
        else if (onclose = callback, isNodeStream(tail))
          destroyer(tail, err);
      }, d;
    };
  });
  var require_operators = __commonJS2((exports2, module2) => {
    var AbortController2 = globalThis.AbortController || require_abort_controller().AbortController, { codes: { ERR_INVALID_ARG_VALUE, ERR_INVALID_ARG_TYPE: ERR_INVALID_ARG_TYPE3, ERR_MISSING_ARGS, ERR_OUT_OF_RANGE: ERR_OUT_OF_RANGE3 }, AbortError: AbortError2 } = require_errors(), { validateAbortSignal: validateAbortSignal2, validateInteger, validateObject } = require_validators(), kWeakHandler = require_primordials().Symbol("kWeak"), kResistStopPropagation = require_primordials().Symbol("kResistStopPropagation"), { finished } = require_end_of_stream(), staticCompose = require_compose(), { addAbortSignalNoValidate } = require_add_abort_signal(), { isWritable, isNodeStream } = require_utils(), { deprecate } = require_util(), { ArrayPrototypePush, Boolean: Boolean2, MathFloor, Number: Number2, NumberIsNaN, Promise: Promise2, PromiseReject, PromiseResolve, PromisePrototypeThen, Symbol: Symbol2 } = require_primordials(), kEmpty = Symbol2("kEmpty"), kEof = Symbol2("kEof");
    function compose(stream, options) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      if (isNodeStream(stream) && !isWritable(stream))
        throw new ERR_INVALID_ARG_VALUE("stream", stream, "must be writable");
      let composedStream = staticCompose(this, stream);
      if (options !== null && options !== undefined && options.signal)
        addAbortSignalNoValidate(options.signal, composedStream);
      return composedStream;
    }
    function map(fn, options) {
      if (typeof fn !== "function")
        throw new ERR_INVALID_ARG_TYPE3("fn", ["Function", "AsyncFunction"], fn);
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      let concurrency = 1;
      if ((options === null || options === undefined ? undefined : options.concurrency) != null)
        concurrency = MathFloor(options.concurrency);
      let highWaterMark = concurrency - 1;
      if ((options === null || options === undefined ? undefined : options.highWaterMark) != null)
        highWaterMark = MathFloor(options.highWaterMark);
      return validateInteger(concurrency, "options.concurrency", 1), validateInteger(highWaterMark, "options.highWaterMark", 0), highWaterMark += concurrency, async function* () {
        let signal = require_util().AbortSignalAny([options === null || options === undefined ? undefined : options.signal].filter(Boolean2)), stream = this, queue = [], signalOpt = { signal }, next, resume, done = false, cnt = 0;
        function onCatch() {
          done = true, afterItemProcessed();
        }
        function afterItemProcessed() {
          cnt -= 1, maybeResume();
        }
        function maybeResume() {
          if (resume && !done && cnt < concurrency && queue.length < highWaterMark)
            resume(), resume = null;
        }
        async function pump() {
          try {
            for await (let val of stream) {
              if (done)
                return;
              if (signal.aborted)
                throw new AbortError2;
              try {
                if (val = fn(val, signalOpt), val === kEmpty)
                  continue;
                val = PromiseResolve(val);
              } catch (err) {
                val = PromiseReject(err);
              }
              if (cnt += 1, PromisePrototypeThen(val, afterItemProcessed, onCatch), queue.push(val), next)
                next(), next = null;
              if (!done && (queue.length >= highWaterMark || cnt >= concurrency))
                await new Promise2((resolve) => {
                  resume = resolve;
                });
            }
            queue.push(kEof);
          } catch (err) {
            let val = PromiseReject(err);
            PromisePrototypeThen(val, afterItemProcessed, onCatch), queue.push(val);
          } finally {
            if (done = true, next)
              next(), next = null;
          }
        }
        pump();
        try {
          while (true) {
            while (queue.length > 0) {
              let val = await queue[0];
              if (val === kEof)
                return;
              if (signal.aborted)
                throw new AbortError2;
              if (val !== kEmpty)
                yield val;
              queue.shift(), maybeResume();
            }
            await new Promise2((resolve) => {
              next = resolve;
            });
          }
        } finally {
          if (done = true, resume)
            resume(), resume = null;
        }
      }.call(this);
    }
    function asIndexedPairs(options = undefined) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      return async function* () {
        let index = 0;
        for await (let val of this) {
          var _options$signal;
          if (options !== null && options !== undefined && (_options$signal = options.signal) !== null && _options$signal !== undefined && _options$signal.aborted)
            throw new AbortError2({ cause: options.signal.reason });
          yield [index++, val];
        }
      }.call(this);
    }
    async function some(fn, options = undefined) {
      for await (let unused of filter.call(this, fn, options))
        return true;
      return false;
    }
    async function every(fn, options = undefined) {
      if (typeof fn !== "function")
        throw new ERR_INVALID_ARG_TYPE3("fn", ["Function", "AsyncFunction"], fn);
      return !await some.call(this, async (...args) => {
        return !await fn(...args);
      }, options);
    }
    async function find(fn, options) {
      for await (let result of filter.call(this, fn, options))
        return result;
      return;
    }
    async function forEach(fn, options) {
      if (typeof fn !== "function")
        throw new ERR_INVALID_ARG_TYPE3("fn", ["Function", "AsyncFunction"], fn);
      async function forEachFn(value, options2) {
        return await fn(value, options2), kEmpty;
      }
      for await (let unused of map.call(this, forEachFn, options))
        ;
    }
    function filter(fn, options) {
      if (typeof fn !== "function")
        throw new ERR_INVALID_ARG_TYPE3("fn", ["Function", "AsyncFunction"], fn);
      async function filterFn(value, options2) {
        if (await fn(value, options2))
          return value;
        return kEmpty;
      }
      return map.call(this, filterFn, options);
    }

    class ReduceAwareErrMissingArgs extends ERR_MISSING_ARGS {
      constructor() {
        super("reduce");
        this.message = "Reduce of an empty stream requires an initial value";
      }
    }
    async function reduce(reducer, initialValue, options) {
      var _options$signal2;
      if (typeof reducer !== "function")
        throw new ERR_INVALID_ARG_TYPE3("reducer", ["Function", "AsyncFunction"], reducer);
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      let hasInitialValue = arguments.length > 1;
      if (options !== null && options !== undefined && (_options$signal2 = options.signal) !== null && _options$signal2 !== undefined && _options$signal2.aborted) {
        let err = new AbortError2(undefined, { cause: options.signal.reason });
        throw this.once("error", () => {}), await finished(this.destroy(err)), err;
      }
      let ac = new AbortController2, signal = ac.signal;
      if (options !== null && options !== undefined && options.signal) {
        let opts = { once: true, [kWeakHandler]: this, [kResistStopPropagation]: true };
        options.signal.addEventListener("abort", () => ac.abort(), opts);
      }
      let gotAnyItemFromStream = false;
      try {
        for await (let value of this) {
          var _options$signal3;
          if (gotAnyItemFromStream = true, options !== null && options !== undefined && (_options$signal3 = options.signal) !== null && _options$signal3 !== undefined && _options$signal3.aborted)
            throw new AbortError2;
          if (!hasInitialValue)
            initialValue = value, hasInitialValue = true;
          else
            initialValue = await reducer(initialValue, value, { signal });
        }
        if (!gotAnyItemFromStream && !hasInitialValue)
          throw new ReduceAwareErrMissingArgs;
      } finally {
        ac.abort();
      }
      return initialValue;
    }
    async function toArray(options) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      let result = [];
      for await (let val of this) {
        var _options$signal4;
        if (options !== null && options !== undefined && (_options$signal4 = options.signal) !== null && _options$signal4 !== undefined && _options$signal4.aborted)
          throw new AbortError2(undefined, { cause: options.signal.reason });
        ArrayPrototypePush(result, val);
      }
      return result;
    }
    function flatMap(fn, options) {
      let values = map.call(this, fn, options);
      return async function* () {
        for await (let val of values)
          yield* val;
      }.call(this);
    }
    function toIntegerOrInfinity(number) {
      if (number = Number2(number), NumberIsNaN(number))
        return 0;
      if (number < 0)
        throw new ERR_OUT_OF_RANGE3("number", ">= 0", number);
      return number;
    }
    function drop(number, options = undefined) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      return number = toIntegerOrInfinity(number), async function* () {
        var _options$signal5;
        if (options !== null && options !== undefined && (_options$signal5 = options.signal) !== null && _options$signal5 !== undefined && _options$signal5.aborted)
          throw new AbortError2;
        for await (let val of this) {
          var _options$signal6;
          if (options !== null && options !== undefined && (_options$signal6 = options.signal) !== null && _options$signal6 !== undefined && _options$signal6.aborted)
            throw new AbortError2;
          if (number-- <= 0)
            yield val;
        }
      }.call(this);
    }
    function take(number, options = undefined) {
      if (options != null)
        validateObject(options, "options");
      if ((options === null || options === undefined ? undefined : options.signal) != null)
        validateAbortSignal2(options.signal, "options.signal");
      return number = toIntegerOrInfinity(number), async function* () {
        var _options$signal7;
        if (options !== null && options !== undefined && (_options$signal7 = options.signal) !== null && _options$signal7 !== undefined && _options$signal7.aborted)
          throw new AbortError2;
        for await (let val of this) {
          var _options$signal8;
          if (options !== null && options !== undefined && (_options$signal8 = options.signal) !== null && _options$signal8 !== undefined && _options$signal8.aborted)
            throw new AbortError2;
          if (number-- > 0)
            yield val;
          if (number <= 0)
            return;
        }
      }.call(this);
    }
    module2.exports.streamReturningOperators = { asIndexedPairs: deprecate(asIndexedPairs, "readable.asIndexedPairs will be removed in a future version."), drop, filter, flatMap, map, take, compose };
    module2.exports.promiseReturningOperators = { every, forEach, reduce, toArray, some, find };
  });
  var require_promises = __commonJS2((exports2, module2) => {
    var { ArrayPrototypePop, Promise: Promise2 } = require_primordials(), { isIterable, isNodeStream, isWebStream } = require_utils(), { pipelineImpl: pl } = require_pipeline(), { finished } = require_end_of_stream();
    require_stream2();
    function pipeline(...streams) {
      return new Promise2((resolve, reject) => {
        let signal, end, lastArg = streams[streams.length - 1];
        if (lastArg && typeof lastArg === "object" && !isNodeStream(lastArg) && !isIterable(lastArg) && !isWebStream(lastArg)) {
          let options = ArrayPrototypePop(streams);
          signal = options.signal, end = options.end;
        }
        pl(streams, (err, value) => {
          if (err)
            reject(err);
          else
            resolve(value);
        }, { signal, end });
      });
    }
    module2.exports = { finished, pipeline };
  });
  var require_stream2 = __commonJS2((exports2, module2) => {
    var { Buffer: Buffer3 } = (init_buffer(), __toCommonJS(exports_buffer)), { ObjectDefineProperty, ObjectKeys, ReflectApply } = require_primordials(), { promisify: { custom: customPromisify } } = require_util(), { streamReturningOperators, promiseReturningOperators } = require_operators(), { codes: { ERR_ILLEGAL_CONSTRUCTOR } } = require_errors(), compose = require_compose(), { setDefaultHighWaterMark, getDefaultHighWaterMark } = require_state(), { pipeline } = require_pipeline(), { destroyer } = require_destroy(), eos = require_end_of_stream(), promises = require_promises(), utils = require_utils(), Stream = module2.exports = require_legacy().Stream;
    Stream.isDestroyed = utils.isDestroyed;
    Stream.isDisturbed = utils.isDisturbed;
    Stream.isErrored = utils.isErrored;
    Stream.isReadable = utils.isReadable;
    Stream.isWritable = utils.isWritable;
    Stream.Readable = require_readable();
    for (let key of ObjectKeys(streamReturningOperators)) {
      let fn = function(...args) {
        if (new.target)
          throw ERR_ILLEGAL_CONSTRUCTOR();
        return Stream.Readable.from(ReflectApply(op, this, args));
      }, op = streamReturningOperators[key];
      ObjectDefineProperty(fn, "name", { __proto__: null, value: op.name }), ObjectDefineProperty(fn, "length", { __proto__: null, value: op.length }), ObjectDefineProperty(Stream.Readable.prototype, key, { __proto__: null, value: fn, enumerable: false, configurable: true, writable: true });
    }
    for (let key of ObjectKeys(promiseReturningOperators)) {
      let fn = function(...args) {
        if (new.target)
          throw ERR_ILLEGAL_CONSTRUCTOR();
        return ReflectApply(op, this, args);
      }, op = promiseReturningOperators[key];
      ObjectDefineProperty(fn, "name", { __proto__: null, value: op.name }), ObjectDefineProperty(fn, "length", { __proto__: null, value: op.length }), ObjectDefineProperty(Stream.Readable.prototype, key, { __proto__: null, value: fn, enumerable: false, configurable: true, writable: true });
    }
    Stream.Writable = require_writable();
    Stream.Duplex = require_duplex();
    Stream.Transform = require_transform();
    Stream.PassThrough = require_passthrough();
    Stream.pipeline = pipeline;
    var { addAbortSignal } = require_add_abort_signal();
    Stream.addAbortSignal = addAbortSignal;
    Stream.finished = eos;
    Stream.destroy = destroyer;
    Stream.compose = compose;
    Stream.setDefaultHighWaterMark = setDefaultHighWaterMark;
    Stream.getDefaultHighWaterMark = getDefaultHighWaterMark;
    ObjectDefineProperty(Stream, "promises", { __proto__: null, configurable: true, enumerable: true, get() {
      return promises;
    } });
    ObjectDefineProperty(pipeline, customPromisify, { __proto__: null, enumerable: true, get() {
      return promises.pipeline;
    } });
    ObjectDefineProperty(eos, customPromisify, { __proto__: null, enumerable: true, get() {
      return promises.finished;
    } });
    Stream.Stream = Stream;
    Stream._isUint8Array = function(value) {
      return value instanceof Uint8Array;
    };
    Stream._uint8ArrayToBuffer = function(chunk) {
      return Buffer3.from(chunk.buffer, chunk.byteOffset, chunk.byteLength);
    };
  });
  var require_ours = __commonJS2((exports2, module2) => {
    var Stream = require_stream();
    {
      let CustomStream = require_stream2(), promises = require_promises(), originalDestroy = CustomStream.Readable.destroy;
      module2.exports = CustomStream.Readable, module2.exports._uint8ArrayToBuffer = CustomStream._uint8ArrayToBuffer, module2.exports._isUint8Array = CustomStream._isUint8Array, module2.exports.isDisturbed = CustomStream.isDisturbed, module2.exports.isErrored = CustomStream.isErrored, module2.exports.isReadable = CustomStream.isReadable, module2.exports.Readable = CustomStream.Readable, module2.exports.Writable = CustomStream.Writable, module2.exports.Duplex = CustomStream.Duplex, module2.exports.Transform = CustomStream.Transform, module2.exports.PassThrough = CustomStream.PassThrough, module2.exports.addAbortSignal = CustomStream.addAbortSignal, module2.exports.finished = CustomStream.finished, module2.exports.destroy = CustomStream.destroy, module2.exports.destroy = originalDestroy, module2.exports.pipeline = CustomStream.pipeline, module2.exports.compose = CustomStream.compose, Object.defineProperty(CustomStream, "promises", { configurable: true, enumerable: true, get() {
        return promises;
      } }), module2.exports.Stream = CustomStream.Stream;
    }
    module2.exports.default = module2.exports;
  });
  module.exports = require_ours();
});

// node_modules/sax/lib/sax.js
var require_sax = __commonJS((exports) => {
  (function(sax) {
    sax.parser = function(strict, opt) {
      return new SAXParser(strict, opt);
    };
    sax.SAXParser = SAXParser;
    sax.SAXStream = SAXStream;
    sax.createStream = createStream;
    sax.MAX_BUFFER_LENGTH = 64 * 1024;
    var buffers = [
      "comment",
      "sgmlDecl",
      "textNode",
      "tagName",
      "doctype",
      "procInstName",
      "procInstBody",
      "entity",
      "attribName",
      "attribValue",
      "cdata",
      "script"
    ];
    sax.EVENTS = [
      "text",
      "processinginstruction",
      "sgmldeclaration",
      "doctype",
      "comment",
      "opentagstart",
      "attribute",
      "opentag",
      "closetag",
      "opencdata",
      "cdata",
      "closecdata",
      "error",
      "end",
      "ready",
      "script",
      "opennamespace",
      "closenamespace"
    ];
    function SAXParser(strict, opt) {
      if (!(this instanceof SAXParser)) {
        return new SAXParser(strict, opt);
      }
      var parser = this;
      clearBuffers(parser);
      parser.q = parser.c = "";
      parser.bufferCheckPosition = sax.MAX_BUFFER_LENGTH;
      parser.opt = opt || {};
      parser.opt.lowercase = parser.opt.lowercase || parser.opt.lowercasetags;
      parser.looseCase = parser.opt.lowercase ? "toLowerCase" : "toUpperCase";
      parser.tags = [];
      parser.closed = parser.closedRoot = parser.sawRoot = false;
      parser.tag = parser.error = null;
      parser.strict = !!strict;
      parser.noscript = !!(strict || parser.opt.noscript);
      parser.state = S.BEGIN;
      parser.strictEntities = parser.opt.strictEntities;
      parser.ENTITIES = parser.strictEntities ? Object.create(sax.XML_ENTITIES) : Object.create(sax.ENTITIES);
      parser.attribList = [];
      if (parser.opt.xmlns) {
        parser.ns = Object.create(rootNS);
      }
      if (parser.opt.unquotedAttributeValues === undefined) {
        parser.opt.unquotedAttributeValues = !strict;
      }
      parser.trackPosition = parser.opt.position !== false;
      if (parser.trackPosition) {
        parser.position = parser.line = parser.column = 0;
      }
      emit(parser, "onready");
    }
    if (!Object.create) {
      Object.create = function(o) {
        function F() {}
        F.prototype = o;
        var newf = new F;
        return newf;
      };
    }
    if (!Object.keys) {
      Object.keys = function(o) {
        var a = [];
        for (var i2 in o)
          if (o.hasOwnProperty(i2))
            a.push(i2);
        return a;
      };
    }
    function checkBufferLength(parser) {
      var maxAllowed = Math.max(sax.MAX_BUFFER_LENGTH, 10);
      var maxActual = 0;
      for (var i2 = 0, l = buffers.length;i2 < l; i2++) {
        var len2 = parser[buffers[i2]].length;
        if (len2 > maxAllowed) {
          switch (buffers[i2]) {
            case "textNode":
              closeText(parser);
              break;
            case "cdata":
              emitNode(parser, "oncdata", parser.cdata);
              parser.cdata = "";
              break;
            case "script":
              emitNode(parser, "onscript", parser.script);
              parser.script = "";
              break;
            default:
              error(parser, "Max buffer length exceeded: " + buffers[i2]);
          }
        }
        maxActual = Math.max(maxActual, len2);
      }
      var m = sax.MAX_BUFFER_LENGTH - maxActual;
      parser.bufferCheckPosition = m + parser.position;
    }
    function clearBuffers(parser) {
      for (var i2 = 0, l = buffers.length;i2 < l; i2++) {
        parser[buffers[i2]] = "";
      }
    }
    function flushBuffers(parser) {
      closeText(parser);
      if (parser.cdata !== "") {
        emitNode(parser, "oncdata", parser.cdata);
        parser.cdata = "";
      }
      if (parser.script !== "") {
        emitNode(parser, "onscript", parser.script);
        parser.script = "";
      }
    }
    SAXParser.prototype = {
      end: function() {
        end(this);
      },
      write: write2,
      resume: function() {
        this.error = null;
        return this;
      },
      close: function() {
        return this.write(null);
      },
      flush: function() {
        flushBuffers(this);
      }
    };
    var Stream;
    try {
      Stream = require_stream().Stream;
    } catch (ex) {
      Stream = function() {};
    }
    if (!Stream)
      Stream = function() {};
    var streamWraps = sax.EVENTS.filter(function(ev) {
      return ev !== "error" && ev !== "end";
    });
    function createStream(strict, opt) {
      return new SAXStream(strict, opt);
    }
    function SAXStream(strict, opt) {
      if (!(this instanceof SAXStream)) {
        return new SAXStream(strict, opt);
      }
      Stream.apply(this);
      this._parser = new SAXParser(strict, opt);
      this.writable = true;
      this.readable = true;
      var me = this;
      this._parser.onend = function() {
        me.emit("end");
      };
      this._parser.onerror = function(er) {
        me.emit("error", er);
        me._parser.error = null;
      };
      this._decoder = null;
      streamWraps.forEach(function(ev) {
        Object.defineProperty(me, "on" + ev, {
          get: function() {
            return me._parser["on" + ev];
          },
          set: function(h) {
            if (!h) {
              me.removeAllListeners(ev);
              me._parser["on" + ev] = h;
              return h;
            }
            me.on(ev, h);
          },
          enumerable: true,
          configurable: false
        });
      });
    }
    SAXStream.prototype = Object.create(Stream.prototype, {
      constructor: {
        value: SAXStream
      }
    });
    SAXStream.prototype.write = function(data) {
      if (typeof Buffer === "function" && typeof Buffer.isBuffer === "function" && Buffer.isBuffer(data)) {
        if (!this._decoder) {
          this._decoder = new TextDecoder("utf8");
        }
        data = this._decoder.decode(data, { stream: true });
      }
      this._parser.write(data.toString());
      this.emit("data", data);
      return true;
    };
    SAXStream.prototype.end = function(chunk) {
      if (chunk && chunk.length) {
        this.write(chunk);
      }
      if (this._decoder) {
        var remaining = this._decoder.decode();
        if (remaining) {
          this._parser.write(remaining);
          this.emit("data", remaining);
        }
      }
      this._parser.end();
      return true;
    };
    SAXStream.prototype.on = function(ev, handler) {
      var me = this;
      if (!me._parser["on" + ev] && streamWraps.indexOf(ev) !== -1) {
        me._parser["on" + ev] = function() {
          var args = arguments.length === 1 ? [arguments[0]] : Array.apply(null, arguments);
          args.splice(0, 0, ev);
          me.emit.apply(me, args);
        };
      }
      return Stream.prototype.on.call(me, ev, handler);
    };
    var CDATA = "[CDATA[";
    var DOCTYPE = "DOCTYPE";
    var XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace";
    var XMLNS_NAMESPACE = "http://www.w3.org/2000/xmlns/";
    var rootNS = { xml: XML_NAMESPACE, xmlns: XMLNS_NAMESPACE };
    var nameStart = /[:_A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD]/;
    var nameBody = /[:_A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\u00B7\u0300-\u036F\u203F-\u2040.\d-]/;
    var entityStart = /[#:_A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD]/;
    var entityBody = /[#:_A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\u00B7\u0300-\u036F\u203F-\u2040.\d-]/;
    function isWhitespace(c) {
      return c === " " || c === `
` || c === "\r" || c === "\t";
    }
    function isQuote(c) {
      return c === '"' || c === "'";
    }
    function isAttribEnd(c) {
      return c === ">" || isWhitespace(c);
    }
    function isMatch(regex, c) {
      return regex.test(c);
    }
    function notMatch(regex, c) {
      return !isMatch(regex, c);
    }
    var S = 0;
    sax.STATE = {
      BEGIN: S++,
      BEGIN_WHITESPACE: S++,
      TEXT: S++,
      TEXT_ENTITY: S++,
      OPEN_WAKA: S++,
      SGML_DECL: S++,
      SGML_DECL_QUOTED: S++,
      DOCTYPE: S++,
      DOCTYPE_QUOTED: S++,
      DOCTYPE_DTD: S++,
      DOCTYPE_DTD_QUOTED: S++,
      COMMENT_STARTING: S++,
      COMMENT: S++,
      COMMENT_ENDING: S++,
      COMMENT_ENDED: S++,
      CDATA: S++,
      CDATA_ENDING: S++,
      CDATA_ENDING_2: S++,
      PROC_INST: S++,
      PROC_INST_BODY: S++,
      PROC_INST_ENDING: S++,
      OPEN_TAG: S++,
      OPEN_TAG_SLASH: S++,
      ATTRIB: S++,
      ATTRIB_NAME: S++,
      ATTRIB_NAME_SAW_WHITE: S++,
      ATTRIB_VALUE: S++,
      ATTRIB_VALUE_QUOTED: S++,
      ATTRIB_VALUE_CLOSED: S++,
      ATTRIB_VALUE_UNQUOTED: S++,
      ATTRIB_VALUE_ENTITY_Q: S++,
      ATTRIB_VALUE_ENTITY_U: S++,
      CLOSE_TAG: S++,
      CLOSE_TAG_SAW_WHITE: S++,
      SCRIPT: S++,
      SCRIPT_ENDING: S++
    };
    sax.XML_ENTITIES = {
      amp: "&",
      gt: ">",
      lt: "<",
      quot: '"',
      apos: "'"
    };
    sax.ENTITIES = {
      amp: "&",
      gt: ">",
      lt: "<",
      quot: '"',
      apos: "'",
      AElig: 198,
      Aacute: 193,
      Acirc: 194,
      Agrave: 192,
      Aring: 197,
      Atilde: 195,
      Auml: 196,
      Ccedil: 199,
      ETH: 208,
      Eacute: 201,
      Ecirc: 202,
      Egrave: 200,
      Euml: 203,
      Iacute: 205,
      Icirc: 206,
      Igrave: 204,
      Iuml: 207,
      Ntilde: 209,
      Oacute: 211,
      Ocirc: 212,
      Ograve: 210,
      Oslash: 216,
      Otilde: 213,
      Ouml: 214,
      THORN: 222,
      Uacute: 218,
      Ucirc: 219,
      Ugrave: 217,
      Uuml: 220,
      Yacute: 221,
      aacute: 225,
      acirc: 226,
      aelig: 230,
      agrave: 224,
      aring: 229,
      atilde: 227,
      auml: 228,
      ccedil: 231,
      eacute: 233,
      ecirc: 234,
      egrave: 232,
      eth: 240,
      euml: 235,
      iacute: 237,
      icirc: 238,
      igrave: 236,
      iuml: 239,
      ntilde: 241,
      oacute: 243,
      ocirc: 244,
      ograve: 242,
      oslash: 248,
      otilde: 245,
      ouml: 246,
      szlig: 223,
      thorn: 254,
      uacute: 250,
      ucirc: 251,
      ugrave: 249,
      uuml: 252,
      yacute: 253,
      yuml: 255,
      copy: 169,
      reg: 174,
      nbsp: 160,
      iexcl: 161,
      cent: 162,
      pound: 163,
      curren: 164,
      yen: 165,
      brvbar: 166,
      sect: 167,
      uml: 168,
      ordf: 170,
      laquo: 171,
      not: 172,
      shy: 173,
      macr: 175,
      deg: 176,
      plusmn: 177,
      sup1: 185,
      sup2: 178,
      sup3: 179,
      acute: 180,
      micro: 181,
      para: 182,
      middot: 183,
      cedil: 184,
      ordm: 186,
      raquo: 187,
      frac14: 188,
      frac12: 189,
      frac34: 190,
      iquest: 191,
      times: 215,
      divide: 247,
      OElig: 338,
      oelig: 339,
      Scaron: 352,
      scaron: 353,
      Yuml: 376,
      fnof: 402,
      circ: 710,
      tilde: 732,
      Alpha: 913,
      Beta: 914,
      Gamma: 915,
      Delta: 916,
      Epsilon: 917,
      Zeta: 918,
      Eta: 919,
      Theta: 920,
      Iota: 921,
      Kappa: 922,
      Lambda: 923,
      Mu: 924,
      Nu: 925,
      Xi: 926,
      Omicron: 927,
      Pi: 928,
      Rho: 929,
      Sigma: 931,
      Tau: 932,
      Upsilon: 933,
      Phi: 934,
      Chi: 935,
      Psi: 936,
      Omega: 937,
      alpha: 945,
      beta: 946,
      gamma: 947,
      delta: 948,
      epsilon: 949,
      zeta: 950,
      eta: 951,
      theta: 952,
      iota: 953,
      kappa: 954,
      lambda: 955,
      mu: 956,
      nu: 957,
      xi: 958,
      omicron: 959,
      pi: 960,
      rho: 961,
      sigmaf: 962,
      sigma: 963,
      tau: 964,
      upsilon: 965,
      phi: 966,
      chi: 967,
      psi: 968,
      omega: 969,
      thetasym: 977,
      upsih: 978,
      piv: 982,
      ensp: 8194,
      emsp: 8195,
      thinsp: 8201,
      zwnj: 8204,
      zwj: 8205,
      lrm: 8206,
      rlm: 8207,
      ndash: 8211,
      mdash: 8212,
      lsquo: 8216,
      rsquo: 8217,
      sbquo: 8218,
      ldquo: 8220,
      rdquo: 8221,
      bdquo: 8222,
      dagger: 8224,
      Dagger: 8225,
      bull: 8226,
      hellip: 8230,
      permil: 8240,
      prime: 8242,
      Prime: 8243,
      lsaquo: 8249,
      rsaquo: 8250,
      oline: 8254,
      frasl: 8260,
      euro: 8364,
      image: 8465,
      weierp: 8472,
      real: 8476,
      trade: 8482,
      alefsym: 8501,
      larr: 8592,
      uarr: 8593,
      rarr: 8594,
      darr: 8595,
      harr: 8596,
      crarr: 8629,
      lArr: 8656,
      uArr: 8657,
      rArr: 8658,
      dArr: 8659,
      hArr: 8660,
      forall: 8704,
      part: 8706,
      exist: 8707,
      empty: 8709,
      nabla: 8711,
      isin: 8712,
      notin: 8713,
      ni: 8715,
      prod: 8719,
      sum: 8721,
      minus: 8722,
      lowast: 8727,
      radic: 8730,
      prop: 8733,
      infin: 8734,
      ang: 8736,
      and: 8743,
      or: 8744,
      cap: 8745,
      cup: 8746,
      int: 8747,
      there4: 8756,
      sim: 8764,
      cong: 8773,
      asymp: 8776,
      ne: 8800,
      equiv: 8801,
      le: 8804,
      ge: 8805,
      sub: 8834,
      sup: 8835,
      nsub: 8836,
      sube: 8838,
      supe: 8839,
      oplus: 8853,
      otimes: 8855,
      perp: 8869,
      sdot: 8901,
      lceil: 8968,
      rceil: 8969,
      lfloor: 8970,
      rfloor: 8971,
      lang: 9001,
      rang: 9002,
      loz: 9674,
      spades: 9824,
      clubs: 9827,
      hearts: 9829,
      diams: 9830
    };
    Object.keys(sax.ENTITIES).forEach(function(key) {
      var e = sax.ENTITIES[key];
      var s2 = typeof e === "number" ? String.fromCharCode(e) : e;
      sax.ENTITIES[key] = s2;
    });
    for (var s in sax.STATE) {
      sax.STATE[sax.STATE[s]] = s;
    }
    S = sax.STATE;
    function emit(parser, event, data) {
      parser[event] && parser[event](data);
    }
    function emitNode(parser, nodeType, data) {
      if (parser.textNode)
        closeText(parser);
      emit(parser, nodeType, data);
    }
    function closeText(parser) {
      parser.textNode = textopts(parser.opt, parser.textNode);
      if (parser.textNode)
        emit(parser, "ontext", parser.textNode);
      parser.textNode = "";
    }
    function textopts(opt, text) {
      if (opt.trim)
        text = text.trim();
      if (opt.normalize)
        text = text.replace(/\s+/g, " ");
      return text;
    }
    function error(parser, er) {
      closeText(parser);
      if (parser.trackPosition) {
        er += `
Line: ` + parser.line + `
Column: ` + parser.column + `
Char: ` + parser.c;
      }
      er = new Error(er);
      parser.error = er;
      emit(parser, "onerror", er);
      return parser;
    }
    function end(parser) {
      if (parser.sawRoot && !parser.closedRoot)
        strictFail(parser, "Unclosed root tag");
      if (parser.state !== S.BEGIN && parser.state !== S.BEGIN_WHITESPACE && parser.state !== S.TEXT) {
        error(parser, "Unexpected end");
      }
      closeText(parser);
      parser.c = "";
      parser.closed = true;
      emit(parser, "onend");
      SAXParser.call(parser, parser.strict, parser.opt);
      return parser;
    }
    function strictFail(parser, message) {
      if (typeof parser !== "object" || !(parser instanceof SAXParser)) {
        throw new Error("bad call to strictFail");
      }
      if (parser.strict) {
        error(parser, message);
      }
    }
    function newTag(parser) {
      if (!parser.strict)
        parser.tagName = parser.tagName[parser.looseCase]();
      var parent = parser.tags[parser.tags.length - 1] || parser;
      var tag = parser.tag = { name: parser.tagName, attributes: {} };
      if (parser.opt.xmlns) {
        tag.ns = parent.ns;
      }
      parser.attribList.length = 0;
      emitNode(parser, "onopentagstart", tag);
    }
    function qname(name, attribute) {
      var i2 = name.indexOf(":");
      var qualName = i2 < 0 ? ["", name] : name.split(":");
      var prefix = qualName[0];
      var local = qualName[1];
      if (attribute && name === "xmlns") {
        prefix = "xmlns";
        local = "";
      }
      return { prefix, local };
    }
    function attrib(parser) {
      if (!parser.strict) {
        parser.attribName = parser.attribName[parser.looseCase]();
      }
      if (parser.attribList.indexOf(parser.attribName) !== -1 || parser.tag.attributes.hasOwnProperty(parser.attribName)) {
        parser.attribName = parser.attribValue = "";
        return;
      }
      if (parser.opt.xmlns) {
        var qn = qname(parser.attribName, true);
        var prefix = qn.prefix;
        var local = qn.local;
        if (prefix === "xmlns") {
          if (local === "xml" && parser.attribValue !== XML_NAMESPACE) {
            strictFail(parser, "xml: prefix must be bound to " + XML_NAMESPACE + `
` + "Actual: " + parser.attribValue);
          } else if (local === "xmlns" && parser.attribValue !== XMLNS_NAMESPACE) {
            strictFail(parser, "xmlns: prefix must be bound to " + XMLNS_NAMESPACE + `
` + "Actual: " + parser.attribValue);
          } else {
            var tag = parser.tag;
            var parent = parser.tags[parser.tags.length - 1] || parser;
            if (tag.ns === parent.ns) {
              tag.ns = Object.create(parent.ns);
            }
            tag.ns[local] = parser.attribValue;
          }
        }
        parser.attribList.push([parser.attribName, parser.attribValue]);
      } else {
        parser.tag.attributes[parser.attribName] = parser.attribValue;
        emitNode(parser, "onattribute", {
          name: parser.attribName,
          value: parser.attribValue
        });
      }
      parser.attribName = parser.attribValue = "";
    }
    function openTag(parser, selfClosing) {
      if (parser.opt.xmlns) {
        var tag = parser.tag;
        var qn = qname(parser.tagName);
        tag.prefix = qn.prefix;
        tag.local = qn.local;
        tag.uri = tag.ns[qn.prefix] || "";
        if (tag.prefix && !tag.uri) {
          strictFail(parser, "Unbound namespace prefix: " + JSON.stringify(parser.tagName));
          tag.uri = qn.prefix;
        }
        var parent = parser.tags[parser.tags.length - 1] || parser;
        if (tag.ns && parent.ns !== tag.ns) {
          Object.keys(tag.ns).forEach(function(p) {
            emitNode(parser, "onopennamespace", {
              prefix: p,
              uri: tag.ns[p]
            });
          });
        }
        for (var i2 = 0, l = parser.attribList.length;i2 < l; i2++) {
          var nv = parser.attribList[i2];
          var name = nv[0];
          var value = nv[1];
          var qualName = qname(name, true);
          var prefix = qualName.prefix;
          var local = qualName.local;
          var uri = prefix === "" ? "" : tag.ns[prefix] || "";
          var a = {
            name,
            value,
            prefix,
            local,
            uri
          };
          if (prefix && prefix !== "xmlns" && !uri) {
            strictFail(parser, "Unbound namespace prefix: " + JSON.stringify(prefix));
            a.uri = prefix;
          }
          parser.tag.attributes[name] = a;
          emitNode(parser, "onattribute", a);
        }
        parser.attribList.length = 0;
      }
      parser.tag.isSelfClosing = !!selfClosing;
      parser.sawRoot = true;
      parser.tags.push(parser.tag);
      emitNode(parser, "onopentag", parser.tag);
      if (!selfClosing) {
        if (!parser.noscript && parser.tagName.toLowerCase() === "script") {
          parser.state = S.SCRIPT;
        } else {
          parser.state = S.TEXT;
        }
        parser.tag = null;
        parser.tagName = "";
      }
      parser.attribName = parser.attribValue = "";
      parser.attribList.length = 0;
    }
    function closeTag(parser) {
      if (!parser.tagName) {
        strictFail(parser, "Weird empty close tag.");
        parser.textNode += "</>";
        parser.state = S.TEXT;
        return;
      }
      if (parser.script) {
        if (parser.tagName !== "script") {
          parser.script += "</" + parser.tagName + ">";
          parser.tagName = "";
          parser.state = S.SCRIPT;
          return;
        }
        emitNode(parser, "onscript", parser.script);
        parser.script = "";
      }
      var t = parser.tags.length;
      var tagName = parser.tagName;
      if (!parser.strict) {
        tagName = tagName[parser.looseCase]();
      }
      var closeTo = tagName;
      while (t--) {
        var close = parser.tags[t];
        if (close.name !== closeTo) {
          strictFail(parser, "Unexpected close tag");
        } else {
          break;
        }
      }
      if (t < 0) {
        strictFail(parser, "Unmatched closing tag: " + parser.tagName);
        parser.textNode += "</" + parser.tagName + ">";
        parser.state = S.TEXT;
        return;
      }
      parser.tagName = tagName;
      var s2 = parser.tags.length;
      while (s2-- > t) {
        var tag = parser.tag = parser.tags.pop();
        parser.tagName = parser.tag.name;
        emitNode(parser, "onclosetag", parser.tagName);
        var x = {};
        for (var i2 in tag.ns) {
          x[i2] = tag.ns[i2];
        }
        var parent = parser.tags[parser.tags.length - 1] || parser;
        if (parser.opt.xmlns && tag.ns !== parent.ns) {
          Object.keys(tag.ns).forEach(function(p) {
            var n = tag.ns[p];
            emitNode(parser, "onclosenamespace", { prefix: p, uri: n });
          });
        }
      }
      if (t === 0)
        parser.closedRoot = true;
      parser.tagName = parser.attribValue = parser.attribName = "";
      parser.attribList.length = 0;
      parser.state = S.TEXT;
    }
    function parseEntity(parser) {
      var entity = parser.entity;
      var entityLC = entity.toLowerCase();
      var num;
      var numStr = "";
      if (parser.ENTITIES[entity]) {
        return parser.ENTITIES[entity];
      }
      if (parser.ENTITIES[entityLC]) {
        return parser.ENTITIES[entityLC];
      }
      entity = entityLC;
      if (entity.charAt(0) === "#") {
        if (entity.charAt(1) === "x") {
          entity = entity.slice(2);
          num = parseInt(entity, 16);
          numStr = num.toString(16);
        } else {
          entity = entity.slice(1);
          num = parseInt(entity, 10);
          numStr = num.toString(10);
        }
      }
      entity = entity.replace(/^0+/, "");
      if (isNaN(num) || numStr.toLowerCase() !== entity || num < 0 || num > 1114111) {
        strictFail(parser, "Invalid character entity");
        return "&" + parser.entity + ";";
      }
      return String.fromCodePoint(num);
    }
    function beginWhiteSpace(parser, c) {
      if (c === "<") {
        parser.state = S.OPEN_WAKA;
        parser.startTagPosition = parser.position;
      } else if (!isWhitespace(c)) {
        strictFail(parser, "Non-whitespace before first tag.");
        parser.textNode = c;
        parser.state = S.TEXT;
      }
    }
    function charAt(chunk, i2) {
      var result = "";
      if (i2 < chunk.length) {
        result = chunk.charAt(i2);
      }
      return result;
    }
    function write2(chunk) {
      var parser = this;
      if (this.error) {
        throw this.error;
      }
      if (parser.closed) {
        return error(parser, "Cannot write after close. Assign an onready handler.");
      }
      if (chunk === null) {
        return end(parser);
      }
      if (typeof chunk === "object") {
        chunk = chunk.toString();
      }
      var i2 = 0;
      var c = "";
      while (true) {
        c = charAt(chunk, i2++);
        parser.c = c;
        if (!c) {
          break;
        }
        if (parser.trackPosition) {
          parser.position++;
          if (c === `
`) {
            parser.line++;
            parser.column = 0;
          } else {
            parser.column++;
          }
        }
        switch (parser.state) {
          case S.BEGIN:
            parser.state = S.BEGIN_WHITESPACE;
            if (c === "\uFEFF") {
              continue;
            }
            beginWhiteSpace(parser, c);
            continue;
          case S.BEGIN_WHITESPACE:
            beginWhiteSpace(parser, c);
            continue;
          case S.TEXT:
            if (parser.sawRoot && !parser.closedRoot) {
              var starti = i2 - 1;
              while (c && c !== "<" && c !== "&") {
                c = charAt(chunk, i2++);
                if (c && parser.trackPosition) {
                  parser.position++;
                  if (c === `
`) {
                    parser.line++;
                    parser.column = 0;
                  } else {
                    parser.column++;
                  }
                }
              }
              parser.textNode += chunk.substring(starti, i2 - 1);
            }
            if (c === "<" && !(parser.sawRoot && parser.closedRoot && !parser.strict)) {
              parser.state = S.OPEN_WAKA;
              parser.startTagPosition = parser.position;
            } else {
              if (!isWhitespace(c) && (!parser.sawRoot || parser.closedRoot)) {
                strictFail(parser, "Text data outside of root node.");
              }
              if (c === "&") {
                parser.state = S.TEXT_ENTITY;
              } else {
                parser.textNode += c;
              }
            }
            continue;
          case S.SCRIPT:
            if (c === "<") {
              parser.state = S.SCRIPT_ENDING;
            } else {
              parser.script += c;
            }
            continue;
          case S.SCRIPT_ENDING:
            if (c === "/") {
              parser.state = S.CLOSE_TAG;
            } else {
              parser.script += "<" + c;
              parser.state = S.SCRIPT;
            }
            continue;
          case S.OPEN_WAKA:
            if (c === "!") {
              parser.state = S.SGML_DECL;
              parser.sgmlDecl = "";
            } else if (isWhitespace(c)) {} else if (isMatch(nameStart, c)) {
              parser.state = S.OPEN_TAG;
              parser.tagName = c;
            } else if (c === "/") {
              parser.state = S.CLOSE_TAG;
              parser.tagName = "";
            } else if (c === "?") {
              parser.state = S.PROC_INST;
              parser.procInstName = parser.procInstBody = "";
            } else {
              strictFail(parser, "Unencoded <");
              if (parser.startTagPosition + 1 < parser.position) {
                var pad = parser.position - parser.startTagPosition;
                c = new Array(pad).join(" ") + c;
              }
              parser.textNode += "<" + c;
              parser.state = S.TEXT;
            }
            continue;
          case S.SGML_DECL:
            if (parser.sgmlDecl + c === "--") {
              parser.state = S.COMMENT;
              parser.comment = "";
              parser.sgmlDecl = "";
              continue;
            }
            if (parser.doctype && parser.doctype !== true && parser.sgmlDecl) {
              parser.state = S.DOCTYPE_DTD;
              parser.doctype += "<!" + parser.sgmlDecl + c;
              parser.sgmlDecl = "";
            } else if ((parser.sgmlDecl + c).toUpperCase() === CDATA) {
              emitNode(parser, "onopencdata");
              parser.state = S.CDATA;
              parser.sgmlDecl = "";
              parser.cdata = "";
            } else if ((parser.sgmlDecl + c).toUpperCase() === DOCTYPE) {
              parser.state = S.DOCTYPE;
              if (parser.doctype || parser.sawRoot) {
                strictFail(parser, "Inappropriately located doctype declaration");
              }
              parser.doctype = "";
              parser.sgmlDecl = "";
            } else if (c === ">") {
              emitNode(parser, "onsgmldeclaration", parser.sgmlDecl);
              parser.sgmlDecl = "";
              parser.state = S.TEXT;
            } else if (isQuote(c)) {
              parser.state = S.SGML_DECL_QUOTED;
              parser.sgmlDecl += c;
            } else {
              parser.sgmlDecl += c;
            }
            continue;
          case S.SGML_DECL_QUOTED:
            if (c === parser.q) {
              parser.state = S.SGML_DECL;
              parser.q = "";
            }
            parser.sgmlDecl += c;
            continue;
          case S.DOCTYPE:
            if (c === ">") {
              parser.state = S.TEXT;
              emitNode(parser, "ondoctype", parser.doctype);
              parser.doctype = true;
            } else {
              parser.doctype += c;
              if (c === "[") {
                parser.state = S.DOCTYPE_DTD;
              } else if (isQuote(c)) {
                parser.state = S.DOCTYPE_QUOTED;
                parser.q = c;
              }
            }
            continue;
          case S.DOCTYPE_QUOTED:
            parser.doctype += c;
            if (c === parser.q) {
              parser.q = "";
              parser.state = S.DOCTYPE;
            }
            continue;
          case S.DOCTYPE_DTD:
            if (c === "]") {
              parser.doctype += c;
              parser.state = S.DOCTYPE;
            } else if (c === "<") {
              parser.state = S.OPEN_WAKA;
              parser.startTagPosition = parser.position;
            } else if (isQuote(c)) {
              parser.doctype += c;
              parser.state = S.DOCTYPE_DTD_QUOTED;
              parser.q = c;
            } else {
              parser.doctype += c;
            }
            continue;
          case S.DOCTYPE_DTD_QUOTED:
            parser.doctype += c;
            if (c === parser.q) {
              parser.state = S.DOCTYPE_DTD;
              parser.q = "";
            }
            continue;
          case S.COMMENT:
            if (c === "-") {
              parser.state = S.COMMENT_ENDING;
            } else {
              parser.comment += c;
            }
            continue;
          case S.COMMENT_ENDING:
            if (c === "-") {
              parser.state = S.COMMENT_ENDED;
              parser.comment = textopts(parser.opt, parser.comment);
              if (parser.comment) {
                emitNode(parser, "oncomment", parser.comment);
              }
              parser.comment = "";
            } else {
              parser.comment += "-" + c;
              parser.state = S.COMMENT;
            }
            continue;
          case S.COMMENT_ENDED:
            if (c !== ">") {
              strictFail(parser, "Malformed comment");
              parser.comment += "--" + c;
              parser.state = S.COMMENT;
            } else if (parser.doctype && parser.doctype !== true) {
              parser.state = S.DOCTYPE_DTD;
            } else {
              parser.state = S.TEXT;
            }
            continue;
          case S.CDATA:
            var starti = i2 - 1;
            while (c && c !== "]") {
              c = charAt(chunk, i2++);
              if (c && parser.trackPosition) {
                parser.position++;
                if (c === `
`) {
                  parser.line++;
                  parser.column = 0;
                } else {
                  parser.column++;
                }
              }
            }
            parser.cdata += chunk.substring(starti, i2 - 1);
            if (c === "]") {
              parser.state = S.CDATA_ENDING;
            }
            continue;
          case S.CDATA_ENDING:
            if (c === "]") {
              parser.state = S.CDATA_ENDING_2;
            } else {
              parser.cdata += "]" + c;
              parser.state = S.CDATA;
            }
            continue;
          case S.CDATA_ENDING_2:
            if (c === ">") {
              if (parser.cdata) {
                emitNode(parser, "oncdata", parser.cdata);
              }
              emitNode(parser, "onclosecdata");
              parser.cdata = "";
              parser.state = S.TEXT;
            } else if (c === "]") {
              parser.cdata += "]";
            } else {
              parser.cdata += "]]" + c;
              parser.state = S.CDATA;
            }
            continue;
          case S.PROC_INST:
            if (c === "?") {
              parser.state = S.PROC_INST_ENDING;
            } else if (isWhitespace(c)) {
              parser.state = S.PROC_INST_BODY;
            } else {
              parser.procInstName += c;
            }
            continue;
          case S.PROC_INST_BODY:
            if (!parser.procInstBody && isWhitespace(c)) {
              continue;
            } else if (c === "?") {
              parser.state = S.PROC_INST_ENDING;
            } else {
              parser.procInstBody += c;
            }
            continue;
          case S.PROC_INST_ENDING:
            if (c === ">") {
              emitNode(parser, "onprocessinginstruction", {
                name: parser.procInstName,
                body: parser.procInstBody
              });
              parser.procInstName = parser.procInstBody = "";
              parser.state = S.TEXT;
            } else {
              parser.procInstBody += "?" + c;
              parser.state = S.PROC_INST_BODY;
            }
            continue;
          case S.OPEN_TAG:
            if (isMatch(nameBody, c)) {
              parser.tagName += c;
            } else {
              newTag(parser);
              if (c === ">") {
                openTag(parser);
              } else if (c === "/") {
                parser.state = S.OPEN_TAG_SLASH;
              } else {
                if (!isWhitespace(c)) {
                  strictFail(parser, "Invalid character in tag name");
                }
                parser.state = S.ATTRIB;
              }
            }
            continue;
          case S.OPEN_TAG_SLASH:
            if (c === ">") {
              openTag(parser, true);
              closeTag(parser);
            } else {
              strictFail(parser, "Forward-slash in opening tag not followed by >");
              parser.state = S.ATTRIB;
            }
            continue;
          case S.ATTRIB:
            if (isWhitespace(c)) {
              continue;
            } else if (c === ">") {
              openTag(parser);
            } else if (c === "/") {
              parser.state = S.OPEN_TAG_SLASH;
            } else if (isMatch(nameStart, c)) {
              parser.attribName = c;
              parser.attribValue = "";
              parser.state = S.ATTRIB_NAME;
            } else {
              strictFail(parser, "Invalid attribute name");
            }
            continue;
          case S.ATTRIB_NAME:
            if (c === "=") {
              parser.state = S.ATTRIB_VALUE;
            } else if (c === ">") {
              strictFail(parser, "Attribute without value");
              parser.attribValue = parser.attribName;
              attrib(parser);
              openTag(parser);
            } else if (isWhitespace(c)) {
              parser.state = S.ATTRIB_NAME_SAW_WHITE;
            } else if (isMatch(nameBody, c)) {
              parser.attribName += c;
            } else {
              strictFail(parser, "Invalid attribute name");
            }
            continue;
          case S.ATTRIB_NAME_SAW_WHITE:
            if (c === "=") {
              parser.state = S.ATTRIB_VALUE;
            } else if (isWhitespace(c)) {
              continue;
            } else {
              strictFail(parser, "Attribute without value");
              parser.tag.attributes[parser.attribName] = "";
              parser.attribValue = "";
              emitNode(parser, "onattribute", {
                name: parser.attribName,
                value: ""
              });
              parser.attribName = "";
              if (c === ">") {
                openTag(parser);
              } else if (isMatch(nameStart, c)) {
                parser.attribName = c;
                parser.state = S.ATTRIB_NAME;
              } else {
                strictFail(parser, "Invalid attribute name");
                parser.state = S.ATTRIB;
              }
            }
            continue;
          case S.ATTRIB_VALUE:
            if (isWhitespace(c)) {
              continue;
            } else if (isQuote(c)) {
              parser.q = c;
              parser.state = S.ATTRIB_VALUE_QUOTED;
            } else {
              if (!parser.opt.unquotedAttributeValues) {
                error(parser, "Unquoted attribute value");
              }
              parser.state = S.ATTRIB_VALUE_UNQUOTED;
              parser.attribValue = c;
            }
            continue;
          case S.ATTRIB_VALUE_QUOTED:
            if (c !== parser.q) {
              if (c === "&") {
                parser.state = S.ATTRIB_VALUE_ENTITY_Q;
              } else {
                parser.attribValue += c;
              }
              continue;
            }
            attrib(parser);
            parser.q = "";
            parser.state = S.ATTRIB_VALUE_CLOSED;
            continue;
          case S.ATTRIB_VALUE_CLOSED:
            if (isWhitespace(c)) {
              parser.state = S.ATTRIB;
            } else if (c === ">") {
              openTag(parser);
            } else if (c === "/") {
              parser.state = S.OPEN_TAG_SLASH;
            } else if (isMatch(nameStart, c)) {
              strictFail(parser, "No whitespace between attributes");
              parser.attribName = c;
              parser.attribValue = "";
              parser.state = S.ATTRIB_NAME;
            } else {
              strictFail(parser, "Invalid attribute name");
            }
            continue;
          case S.ATTRIB_VALUE_UNQUOTED:
            if (!isAttribEnd(c)) {
              if (c === "&") {
                parser.state = S.ATTRIB_VALUE_ENTITY_U;
              } else {
                parser.attribValue += c;
              }
              continue;
            }
            attrib(parser);
            if (c === ">") {
              openTag(parser);
            } else {
              parser.state = S.ATTRIB;
            }
            continue;
          case S.CLOSE_TAG:
            if (!parser.tagName) {
              if (isWhitespace(c)) {
                continue;
              } else if (notMatch(nameStart, c)) {
                if (parser.script) {
                  parser.script += "</" + c;
                  parser.state = S.SCRIPT;
                } else {
                  strictFail(parser, "Invalid tagname in closing tag.");
                }
              } else {
                parser.tagName = c;
              }
            } else if (c === ">") {
              closeTag(parser);
            } else if (isMatch(nameBody, c)) {
              parser.tagName += c;
            } else if (parser.script) {
              parser.script += "</" + parser.tagName + c;
              parser.tagName = "";
              parser.state = S.SCRIPT;
            } else {
              if (!isWhitespace(c)) {
                strictFail(parser, "Invalid tagname in closing tag");
              }
              parser.state = S.CLOSE_TAG_SAW_WHITE;
            }
            continue;
          case S.CLOSE_TAG_SAW_WHITE:
            if (isWhitespace(c)) {
              continue;
            }
            if (c === ">") {
              closeTag(parser);
            } else {
              strictFail(parser, "Invalid characters in closing tag");
            }
            continue;
          case S.TEXT_ENTITY:
          case S.ATTRIB_VALUE_ENTITY_Q:
          case S.ATTRIB_VALUE_ENTITY_U:
            var returnState;
            var buffer;
            switch (parser.state) {
              case S.TEXT_ENTITY:
                returnState = S.TEXT;
                buffer = "textNode";
                break;
              case S.ATTRIB_VALUE_ENTITY_Q:
                returnState = S.ATTRIB_VALUE_QUOTED;
                buffer = "attribValue";
                break;
              case S.ATTRIB_VALUE_ENTITY_U:
                returnState = S.ATTRIB_VALUE_UNQUOTED;
                buffer = "attribValue";
                break;
            }
            if (c === ";") {
              var parsedEntity = parseEntity(parser);
              if (parser.opt.unparsedEntities && !Object.values(sax.XML_ENTITIES).includes(parsedEntity)) {
                parser.entity = "";
                parser.state = returnState;
                parser.write(parsedEntity);
              } else {
                parser[buffer] += parsedEntity;
                parser.entity = "";
                parser.state = returnState;
              }
            } else if (isMatch(parser.entity.length ? entityBody : entityStart, c)) {
              parser.entity += c;
            } else {
              strictFail(parser, "Invalid character in entity name");
              parser[buffer] += "&" + parser.entity + c;
              parser.entity = "";
              parser.state = returnState;
            }
            continue;
          default: {
            throw new Error(parser, "Unknown state: " + parser.state);
          }
        }
      }
      if (parser.position >= parser.bufferCheckPosition) {
        checkBufferLength(parser);
      }
      return parser;
    }
    /*! http://mths.be/fromcodepoint v0.1.0 by @mathias */
    if (!String.fromCodePoint) {
      (function() {
        var stringFromCharCode = String.fromCharCode;
        var floor = Math.floor;
        var fromCodePoint = function() {
          var MAX_SIZE = 16384;
          var codeUnits = [];
          var highSurrogate;
          var lowSurrogate;
          var index = -1;
          var length = arguments.length;
          if (!length) {
            return "";
          }
          var result = "";
          while (++index < length) {
            var codePoint = Number(arguments[index]);
            if (!isFinite(codePoint) || codePoint < 0 || codePoint > 1114111 || floor(codePoint) !== codePoint) {
              throw RangeError("Invalid code point: " + codePoint);
            }
            if (codePoint <= 65535) {
              codeUnits.push(codePoint);
            } else {
              codePoint -= 65536;
              highSurrogate = (codePoint >> 10) + 55296;
              lowSurrogate = codePoint % 1024 + 56320;
              codeUnits.push(highSurrogate, lowSurrogate);
            }
            if (index + 1 === length || codeUnits.length > MAX_SIZE) {
              result += stringFromCharCode.apply(null, codeUnits);
              codeUnits.length = 0;
            }
          }
          return result;
        };
        if (Object.defineProperty) {
          Object.defineProperty(String, "fromCodePoint", {
            value: fromCodePoint,
            configurable: true,
            writable: true
          });
        } else {
          String.fromCodePoint = fromCodePoint;
        }
      })();
    }
  })(typeof exports === "undefined" ? exports.sax = {} : exports);
});

// node_modules/xml-js/lib/array-helper.js
var require_array_helper = __commonJS((exports, module) => {
  module.exports = {
    isArray: function(value) {
      if (Array.isArray) {
        return Array.isArray(value);
      }
      return Object.prototype.toString.call(value) === "[object Array]";
    }
  };
});

// node_modules/xml-js/lib/options-helper.js
var require_options_helper = __commonJS((exports, module) => {
  var isArray = require_array_helper().isArray;
  module.exports = {
    copyOptions: function(options) {
      var key, copy = {};
      for (key in options) {
        if (options.hasOwnProperty(key)) {
          copy[key] = options[key];
        }
      }
      return copy;
    },
    ensureFlagExists: function(item, options) {
      if (!(item in options) || typeof options[item] !== "boolean") {
        options[item] = false;
      }
    },
    ensureSpacesExists: function(options) {
      if (!("spaces" in options) || typeof options.spaces !== "number" && typeof options.spaces !== "string") {
        options.spaces = 0;
      }
    },
    ensureAlwaysArrayExists: function(options) {
      if (!("alwaysArray" in options) || typeof options.alwaysArray !== "boolean" && !isArray(options.alwaysArray)) {
        options.alwaysArray = false;
      }
    },
    ensureKeyExists: function(key, options) {
      if (!(key + "Key" in options) || typeof options[key + "Key"] !== "string") {
        options[key + "Key"] = options.compact ? "_" + key : key;
      }
    },
    checkFnExists: function(key, options) {
      return key + "Fn" in options;
    }
  };
});

// node_modules/xml-js/lib/xml2js.js
var require_xml2js = __commonJS((exports, module) => {
  var sax = require_sax();
  var expat = { on: function() {}, parse: function() {} };
  var helper = require_options_helper();
  var isArray = require_array_helper().isArray;
  var options;
  var pureJsParser = true;
  var currentElement;
  function validateOptions(userOptions) {
    options = helper.copyOptions(userOptions);
    helper.ensureFlagExists("ignoreDeclaration", options);
    helper.ensureFlagExists("ignoreInstruction", options);
    helper.ensureFlagExists("ignoreAttributes", options);
    helper.ensureFlagExists("ignoreText", options);
    helper.ensureFlagExists("ignoreComment", options);
    helper.ensureFlagExists("ignoreCdata", options);
    helper.ensureFlagExists("ignoreDoctype", options);
    helper.ensureFlagExists("compact", options);
    helper.ensureFlagExists("alwaysChildren", options);
    helper.ensureFlagExists("addParent", options);
    helper.ensureFlagExists("trim", options);
    helper.ensureFlagExists("nativeType", options);
    helper.ensureFlagExists("nativeTypeAttributes", options);
    helper.ensureFlagExists("sanitize", options);
    helper.ensureFlagExists("instructionHasAttributes", options);
    helper.ensureFlagExists("captureSpacesBetweenElements", options);
    helper.ensureAlwaysArrayExists(options);
    helper.ensureKeyExists("declaration", options);
    helper.ensureKeyExists("instruction", options);
    helper.ensureKeyExists("attributes", options);
    helper.ensureKeyExists("text", options);
    helper.ensureKeyExists("comment", options);
    helper.ensureKeyExists("cdata", options);
    helper.ensureKeyExists("doctype", options);
    helper.ensureKeyExists("type", options);
    helper.ensureKeyExists("name", options);
    helper.ensureKeyExists("elements", options);
    helper.ensureKeyExists("parent", options);
    helper.checkFnExists("doctype", options);
    helper.checkFnExists("instruction", options);
    helper.checkFnExists("cdata", options);
    helper.checkFnExists("comment", options);
    helper.checkFnExists("text", options);
    helper.checkFnExists("instructionName", options);
    helper.checkFnExists("elementName", options);
    helper.checkFnExists("attributeName", options);
    helper.checkFnExists("attributeValue", options);
    helper.checkFnExists("attributes", options);
    return options;
  }
  function nativeType(value) {
    var nValue = Number(value);
    if (!isNaN(nValue)) {
      return nValue;
    }
    var bValue = value.toLowerCase();
    if (bValue === "true") {
      return true;
    } else if (bValue === "false") {
      return false;
    }
    return value;
  }
  function addField(type, value) {
    var key;
    if (options.compact) {
      if (!currentElement[options[type + "Key"]] && (isArray(options.alwaysArray) ? options.alwaysArray.indexOf(options[type + "Key"]) !== -1 : options.alwaysArray)) {
        currentElement[options[type + "Key"]] = [];
      }
      if (currentElement[options[type + "Key"]] && !isArray(currentElement[options[type + "Key"]])) {
        currentElement[options[type + "Key"]] = [currentElement[options[type + "Key"]]];
      }
      if (type + "Fn" in options && typeof value === "string") {
        value = options[type + "Fn"](value, currentElement);
      }
      if (type === "instruction" && (("instructionFn" in options) || ("instructionNameFn" in options))) {
        for (key in value) {
          if (value.hasOwnProperty(key)) {
            if ("instructionFn" in options) {
              value[key] = options.instructionFn(value[key], key, currentElement);
            } else {
              var temp = value[key];
              delete value[key];
              value[options.instructionNameFn(key, temp, currentElement)] = temp;
            }
          }
        }
      }
      if (isArray(currentElement[options[type + "Key"]])) {
        currentElement[options[type + "Key"]].push(value);
      } else {
        currentElement[options[type + "Key"]] = value;
      }
    } else {
      if (!currentElement[options.elementsKey]) {
        currentElement[options.elementsKey] = [];
      }
      var element = {};
      element[options.typeKey] = type;
      if (type === "instruction") {
        for (key in value) {
          if (value.hasOwnProperty(key)) {
            break;
          }
        }
        element[options.nameKey] = "instructionNameFn" in options ? options.instructionNameFn(key, value, currentElement) : key;
        if (options.instructionHasAttributes) {
          element[options.attributesKey] = value[key][options.attributesKey];
          if ("instructionFn" in options) {
            element[options.attributesKey] = options.instructionFn(element[options.attributesKey], key, currentElement);
          }
        } else {
          if ("instructionFn" in options) {
            value[key] = options.instructionFn(value[key], key, currentElement);
          }
          element[options.instructionKey] = value[key];
        }
      } else {
        if (type + "Fn" in options) {
          value = options[type + "Fn"](value, currentElement);
        }
        element[options[type + "Key"]] = value;
      }
      if (options.addParent) {
        element[options.parentKey] = currentElement;
      }
      currentElement[options.elementsKey].push(element);
    }
  }
  function manipulateAttributes(attributes) {
    if ("attributesFn" in options && attributes) {
      attributes = options.attributesFn(attributes, currentElement);
    }
    if ((options.trim || ("attributeValueFn" in options) || ("attributeNameFn" in options) || options.nativeTypeAttributes) && attributes) {
      var key;
      for (key in attributes) {
        if (attributes.hasOwnProperty(key)) {
          if (options.trim)
            attributes[key] = attributes[key].trim();
          if (options.nativeTypeAttributes) {
            attributes[key] = nativeType(attributes[key]);
          }
          if ("attributeValueFn" in options)
            attributes[key] = options.attributeValueFn(attributes[key], key, currentElement);
          if ("attributeNameFn" in options) {
            var temp = attributes[key];
            delete attributes[key];
            attributes[options.attributeNameFn(key, attributes[key], currentElement)] = temp;
          }
        }
      }
    }
    return attributes;
  }
  function onInstruction(instruction) {
    var attributes = {};
    if (instruction.body && (instruction.name.toLowerCase() === "xml" || options.instructionHasAttributes)) {
      var attrsRegExp = /([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|(\w+))\s*/g;
      var match;
      while ((match = attrsRegExp.exec(instruction.body)) !== null) {
        attributes[match[1]] = match[2] || match[3] || match[4];
      }
      attributes = manipulateAttributes(attributes);
    }
    if (instruction.name.toLowerCase() === "xml") {
      if (options.ignoreDeclaration) {
        return;
      }
      currentElement[options.declarationKey] = {};
      if (Object.keys(attributes).length) {
        currentElement[options.declarationKey][options.attributesKey] = attributes;
      }
      if (options.addParent) {
        currentElement[options.declarationKey][options.parentKey] = currentElement;
      }
    } else {
      if (options.ignoreInstruction) {
        return;
      }
      if (options.trim) {
        instruction.body = instruction.body.trim();
      }
      var value = {};
      if (options.instructionHasAttributes && Object.keys(attributes).length) {
        value[instruction.name] = {};
        value[instruction.name][options.attributesKey] = attributes;
      } else {
        value[instruction.name] = instruction.body;
      }
      addField("instruction", value);
    }
  }
  function onStartElement(name, attributes) {
    var element;
    if (typeof name === "object") {
      attributes = name.attributes;
      name = name.name;
    }
    attributes = manipulateAttributes(attributes);
    if ("elementNameFn" in options) {
      name = options.elementNameFn(name, currentElement);
    }
    if (options.compact) {
      element = {};
      if (!options.ignoreAttributes && attributes && Object.keys(attributes).length) {
        element[options.attributesKey] = {};
        var key;
        for (key in attributes) {
          if (attributes.hasOwnProperty(key)) {
            element[options.attributesKey][key] = attributes[key];
          }
        }
      }
      if (!(name in currentElement) && (isArray(options.alwaysArray) ? options.alwaysArray.indexOf(name) !== -1 : options.alwaysArray)) {
        currentElement[name] = [];
      }
      if (currentElement[name] && !isArray(currentElement[name])) {
        currentElement[name] = [currentElement[name]];
      }
      if (isArray(currentElement[name])) {
        currentElement[name].push(element);
      } else {
        currentElement[name] = element;
      }
    } else {
      if (!currentElement[options.elementsKey]) {
        currentElement[options.elementsKey] = [];
      }
      element = {};
      element[options.typeKey] = "element";
      element[options.nameKey] = name;
      if (!options.ignoreAttributes && attributes && Object.keys(attributes).length) {
        element[options.attributesKey] = attributes;
      }
      if (options.alwaysChildren) {
        element[options.elementsKey] = [];
      }
      currentElement[options.elementsKey].push(element);
    }
    element[options.parentKey] = currentElement;
    currentElement = element;
  }
  function onText(text) {
    if (options.ignoreText) {
      return;
    }
    if (!text.trim() && !options.captureSpacesBetweenElements) {
      return;
    }
    if (options.trim) {
      text = text.trim();
    }
    if (options.nativeType) {
      text = nativeType(text);
    }
    if (options.sanitize) {
      text = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
    addField("text", text);
  }
  function onComment(comment) {
    if (options.ignoreComment) {
      return;
    }
    if (options.trim) {
      comment = comment.trim();
    }
    addField("comment", comment);
  }
  function onEndElement(name) {
    var parentElement = currentElement[options.parentKey];
    if (!options.addParent) {
      delete currentElement[options.parentKey];
    }
    currentElement = parentElement;
  }
  function onCdata(cdata) {
    if (options.ignoreCdata) {
      return;
    }
    if (options.trim) {
      cdata = cdata.trim();
    }
    addField("cdata", cdata);
  }
  function onDoctype(doctype) {
    if (options.ignoreDoctype) {
      return;
    }
    doctype = doctype.replace(/^ /, "");
    if (options.trim) {
      doctype = doctype.trim();
    }
    addField("doctype", doctype);
  }
  function onError(error) {
    error.note = error;
  }
  module.exports = function(xml, userOptions) {
    var parser = pureJsParser ? sax.parser(true, {}) : parser = new expat.Parser("UTF-8");
    var result = {};
    currentElement = result;
    options = validateOptions(userOptions);
    if (pureJsParser) {
      parser.opt = { strictEntities: true };
      parser.onopentag = onStartElement;
      parser.ontext = onText;
      parser.oncomment = onComment;
      parser.onclosetag = onEndElement;
      parser.onerror = onError;
      parser.oncdata = onCdata;
      parser.ondoctype = onDoctype;
      parser.onprocessinginstruction = onInstruction;
    } else {
      parser.on("startElement", onStartElement);
      parser.on("text", onText);
      parser.on("comment", onComment);
      parser.on("endElement", onEndElement);
      parser.on("error", onError);
    }
    if (pureJsParser) {
      parser.write(xml).close();
    } else {
      if (!parser.parse(xml)) {
        throw new Error("XML parsing error: " + parser.getError());
      }
    }
    if (result[options.elementsKey]) {
      var temp = result[options.elementsKey];
      delete result[options.elementsKey];
      result[options.elementsKey] = temp;
      delete result.text;
    }
    return result;
  };
});

// node_modules/xml-js/lib/xml2json.js
var require_xml2json = __commonJS((exports, module) => {
  var helper = require_options_helper();
  var xml2js = require_xml2js();
  function validateOptions(userOptions) {
    var options = helper.copyOptions(userOptions);
    helper.ensureSpacesExists(options);
    return options;
  }
  module.exports = function(xml, userOptions) {
    var options, js, json, parentKey;
    options = validateOptions(userOptions);
    js = xml2js(xml, options);
    parentKey = "compact" in options && options.compact ? "_parent" : "parent";
    if ("addParent" in options && options.addParent) {
      json = JSON.stringify(js, function(k, v) {
        return k === parentKey ? "_" : v;
      }, options.spaces);
    } else {
      json = JSON.stringify(js, null, options.spaces);
    }
    return json.replace(/\u2028/g, "\\u2028").replace(/\u2029/g, "\\u2029");
  };
});

// node_modules/xml-js/lib/js2xml.js
var require_js2xml = __commonJS((exports, module) => {
  var helper = require_options_helper();
  var isArray = require_array_helper().isArray;
  var currentElement;
  var currentElementName;
  function validateOptions(userOptions) {
    var options = helper.copyOptions(userOptions);
    helper.ensureFlagExists("ignoreDeclaration", options);
    helper.ensureFlagExists("ignoreInstruction", options);
    helper.ensureFlagExists("ignoreAttributes", options);
    helper.ensureFlagExists("ignoreText", options);
    helper.ensureFlagExists("ignoreComment", options);
    helper.ensureFlagExists("ignoreCdata", options);
    helper.ensureFlagExists("ignoreDoctype", options);
    helper.ensureFlagExists("compact", options);
    helper.ensureFlagExists("indentText", options);
    helper.ensureFlagExists("indentCdata", options);
    helper.ensureFlagExists("indentAttributes", options);
    helper.ensureFlagExists("indentInstruction", options);
    helper.ensureFlagExists("fullTagEmptyElement", options);
    helper.ensureFlagExists("noQuotesForNativeAttributes", options);
    helper.ensureSpacesExists(options);
    if (typeof options.spaces === "number") {
      options.spaces = Array(options.spaces + 1).join(" ");
    }
    helper.ensureKeyExists("declaration", options);
    helper.ensureKeyExists("instruction", options);
    helper.ensureKeyExists("attributes", options);
    helper.ensureKeyExists("text", options);
    helper.ensureKeyExists("comment", options);
    helper.ensureKeyExists("cdata", options);
    helper.ensureKeyExists("doctype", options);
    helper.ensureKeyExists("type", options);
    helper.ensureKeyExists("name", options);
    helper.ensureKeyExists("elements", options);
    helper.checkFnExists("doctype", options);
    helper.checkFnExists("instruction", options);
    helper.checkFnExists("cdata", options);
    helper.checkFnExists("comment", options);
    helper.checkFnExists("text", options);
    helper.checkFnExists("instructionName", options);
    helper.checkFnExists("elementName", options);
    helper.checkFnExists("attributeName", options);
    helper.checkFnExists("attributeValue", options);
    helper.checkFnExists("attributes", options);
    helper.checkFnExists("fullTagEmptyElement", options);
    return options;
  }
  function writeIndentation(options, depth, firstLine) {
    return (!firstLine && options.spaces ? `
` : "") + Array(depth + 1).join(options.spaces);
  }
  function writeAttributes(attributes, options, depth) {
    if (options.ignoreAttributes) {
      return "";
    }
    if ("attributesFn" in options) {
      attributes = options.attributesFn(attributes, currentElementName, currentElement);
    }
    var key, attr, attrName, quote, result = [];
    for (key in attributes) {
      if (attributes.hasOwnProperty(key) && attributes[key] !== null && attributes[key] !== undefined) {
        quote = options.noQuotesForNativeAttributes && typeof attributes[key] !== "string" ? "" : '"';
        attr = "" + attributes[key];
        attr = attr.replace(/"/g, "&quot;");
        attrName = "attributeNameFn" in options ? options.attributeNameFn(key, attr, currentElementName, currentElement) : key;
        result.push(options.spaces && options.indentAttributes ? writeIndentation(options, depth + 1, false) : " ");
        result.push(attrName + "=" + quote + ("attributeValueFn" in options ? options.attributeValueFn(attr, key, currentElementName, currentElement) : attr) + quote);
      }
    }
    if (attributes && Object.keys(attributes).length && options.spaces && options.indentAttributes) {
      result.push(writeIndentation(options, depth, false));
    }
    return result.join("");
  }
  function writeDeclaration(declaration, options, depth) {
    currentElement = declaration;
    currentElementName = "xml";
    return options.ignoreDeclaration ? "" : "<?" + "xml" + writeAttributes(declaration[options.attributesKey], options, depth) + "?>";
  }
  function writeInstruction(instruction, options, depth) {
    if (options.ignoreInstruction) {
      return "";
    }
    var key;
    for (key in instruction) {
      if (instruction.hasOwnProperty(key)) {
        break;
      }
    }
    var instructionName = "instructionNameFn" in options ? options.instructionNameFn(key, instruction[key], currentElementName, currentElement) : key;
    if (typeof instruction[key] === "object") {
      currentElement = instruction;
      currentElementName = instructionName;
      return "<?" + instructionName + writeAttributes(instruction[key][options.attributesKey], options, depth) + "?>";
    } else {
      var instructionValue = instruction[key] ? instruction[key] : "";
      if ("instructionFn" in options)
        instructionValue = options.instructionFn(instructionValue, key, currentElementName, currentElement);
      return "<?" + instructionName + (instructionValue ? " " + instructionValue : "") + "?>";
    }
  }
  function writeComment(comment, options) {
    return options.ignoreComment ? "" : "<!--" + ("commentFn" in options ? options.commentFn(comment, currentElementName, currentElement) : comment) + "-->";
  }
  function writeCdata(cdata, options) {
    return options.ignoreCdata ? "" : "<![CDATA[" + ("cdataFn" in options ? options.cdataFn(cdata, currentElementName, currentElement) : cdata.replace("]]>", "]]]]><![CDATA[>")) + "]]>";
  }
  function writeDoctype(doctype, options) {
    return options.ignoreDoctype ? "" : "<!DOCTYPE " + ("doctypeFn" in options ? options.doctypeFn(doctype, currentElementName, currentElement) : doctype) + ">";
  }
  function writeText(text, options) {
    if (options.ignoreText)
      return "";
    text = "" + text;
    text = text.replace(/&amp;/g, "&");
    text = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return "textFn" in options ? options.textFn(text, currentElementName, currentElement) : text;
  }
  function hasContent(element, options) {
    var i2;
    if (element.elements && element.elements.length) {
      for (i2 = 0;i2 < element.elements.length; ++i2) {
        switch (element.elements[i2][options.typeKey]) {
          case "text":
            if (options.indentText) {
              return true;
            }
            break;
          case "cdata":
            if (options.indentCdata) {
              return true;
            }
            break;
          case "instruction":
            if (options.indentInstruction) {
              return true;
            }
            break;
          case "doctype":
          case "comment":
          case "element":
            return true;
          default:
            return true;
        }
      }
    }
    return false;
  }
  function writeElement(element, options, depth) {
    currentElement = element;
    currentElementName = element.name;
    var xml = [], elementName = "elementNameFn" in options ? options.elementNameFn(element.name, element) : element.name;
    xml.push("<" + elementName);
    if (element[options.attributesKey]) {
      xml.push(writeAttributes(element[options.attributesKey], options, depth));
    }
    var withClosingTag = element[options.elementsKey] && element[options.elementsKey].length || element[options.attributesKey] && element[options.attributesKey]["xml:space"] === "preserve";
    if (!withClosingTag) {
      if ("fullTagEmptyElementFn" in options) {
        withClosingTag = options.fullTagEmptyElementFn(element.name, element);
      } else {
        withClosingTag = options.fullTagEmptyElement;
      }
    }
    if (withClosingTag) {
      xml.push(">");
      if (element[options.elementsKey] && element[options.elementsKey].length) {
        xml.push(writeElements(element[options.elementsKey], options, depth + 1));
        currentElement = element;
        currentElementName = element.name;
      }
      xml.push(options.spaces && hasContent(element, options) ? `
` + Array(depth + 1).join(options.spaces) : "");
      xml.push("</" + elementName + ">");
    } else {
      xml.push("/>");
    }
    return xml.join("");
  }
  function writeElements(elements, options, depth, firstLine) {
    return elements.reduce(function(xml, element) {
      var indent = writeIndentation(options, depth, firstLine && !xml);
      switch (element.type) {
        case "element":
          return xml + indent + writeElement(element, options, depth);
        case "comment":
          return xml + indent + writeComment(element[options.commentKey], options);
        case "doctype":
          return xml + indent + writeDoctype(element[options.doctypeKey], options);
        case "cdata":
          return xml + (options.indentCdata ? indent : "") + writeCdata(element[options.cdataKey], options);
        case "text":
          return xml + (options.indentText ? indent : "") + writeText(element[options.textKey], options);
        case "instruction":
          var instruction = {};
          instruction[element[options.nameKey]] = element[options.attributesKey] ? element : element[options.instructionKey];
          return xml + (options.indentInstruction ? indent : "") + writeInstruction(instruction, options, depth);
      }
    }, "");
  }
  function hasContentCompact(element, options, anyContent) {
    var key;
    for (key in element) {
      if (element.hasOwnProperty(key)) {
        switch (key) {
          case options.parentKey:
          case options.attributesKey:
            break;
          case options.textKey:
            if (options.indentText || anyContent) {
              return true;
            }
            break;
          case options.cdataKey:
            if (options.indentCdata || anyContent) {
              return true;
            }
            break;
          case options.instructionKey:
            if (options.indentInstruction || anyContent) {
              return true;
            }
            break;
          case options.doctypeKey:
          case options.commentKey:
            return true;
          default:
            return true;
        }
      }
    }
    return false;
  }
  function writeElementCompact(element, name, options, depth, indent) {
    currentElement = element;
    currentElementName = name;
    var elementName = "elementNameFn" in options ? options.elementNameFn(name, element) : name;
    if (typeof element === "undefined" || element === null || element === "") {
      return "fullTagEmptyElementFn" in options && options.fullTagEmptyElementFn(name, element) || options.fullTagEmptyElement ? "<" + elementName + "></" + elementName + ">" : "<" + elementName + "/>";
    }
    var xml = [];
    if (name) {
      xml.push("<" + elementName);
      if (typeof element !== "object") {
        xml.push(">" + writeText(element, options) + "</" + elementName + ">");
        return xml.join("");
      }
      if (element[options.attributesKey]) {
        xml.push(writeAttributes(element[options.attributesKey], options, depth));
      }
      var withClosingTag = hasContentCompact(element, options, true) || element[options.attributesKey] && element[options.attributesKey]["xml:space"] === "preserve";
      if (!withClosingTag) {
        if ("fullTagEmptyElementFn" in options) {
          withClosingTag = options.fullTagEmptyElementFn(name, element);
        } else {
          withClosingTag = options.fullTagEmptyElement;
        }
      }
      if (withClosingTag) {
        xml.push(">");
      } else {
        xml.push("/>");
        return xml.join("");
      }
    }
    xml.push(writeElementsCompact(element, options, depth + 1, false));
    currentElement = element;
    currentElementName = name;
    if (name) {
      xml.push((indent ? writeIndentation(options, depth, false) : "") + "</" + elementName + ">");
    }
    return xml.join("");
  }
  function writeElementsCompact(element, options, depth, firstLine) {
    var i2, key, nodes, xml = [];
    for (key in element) {
      if (element.hasOwnProperty(key)) {
        nodes = isArray(element[key]) ? element[key] : [element[key]];
        for (i2 = 0;i2 < nodes.length; ++i2) {
          switch (key) {
            case options.declarationKey:
              xml.push(writeDeclaration(nodes[i2], options, depth));
              break;
            case options.instructionKey:
              xml.push((options.indentInstruction ? writeIndentation(options, depth, firstLine) : "") + writeInstruction(nodes[i2], options, depth));
              break;
            case options.attributesKey:
            case options.parentKey:
              break;
            case options.textKey:
              xml.push((options.indentText ? writeIndentation(options, depth, firstLine) : "") + writeText(nodes[i2], options));
              break;
            case options.cdataKey:
              xml.push((options.indentCdata ? writeIndentation(options, depth, firstLine) : "") + writeCdata(nodes[i2], options));
              break;
            case options.doctypeKey:
              xml.push(writeIndentation(options, depth, firstLine) + writeDoctype(nodes[i2], options));
              break;
            case options.commentKey:
              xml.push(writeIndentation(options, depth, firstLine) + writeComment(nodes[i2], options));
              break;
            default:
              xml.push(writeIndentation(options, depth, firstLine) + writeElementCompact(nodes[i2], key, options, depth, hasContentCompact(nodes[i2], options)));
          }
          firstLine = firstLine && !xml.length;
        }
      }
    }
    return xml.join("");
  }
  module.exports = function(js, options) {
    options = validateOptions(options);
    var xml = [];
    currentElement = js;
    currentElementName = "_root_";
    if (options.compact) {
      xml.push(writeElementsCompact(js, options, 0, true));
    } else {
      if (js[options.declarationKey]) {
        xml.push(writeDeclaration(js[options.declarationKey], options, 0));
      }
      if (js[options.elementsKey] && js[options.elementsKey].length) {
        xml.push(writeElements(js[options.elementsKey], options, 0, !xml.length));
      }
    }
    return xml.join("");
  };
});

// node_modules/xml-js/lib/json2xml.js
var require_json2xml = __commonJS((exports, module) => {
  var js2xml = require_js2xml();
  module.exports = function(json, options) {
    if (json instanceof Buffer) {
      json = json.toString();
    }
    var js = null;
    if (typeof json === "string") {
      try {
        js = JSON.parse(json);
      } catch (e) {
        throw new Error("The JSON structure is invalid");
      }
    } else {
      js = json;
    }
    return js2xml(js, options);
  };
});

// node_modules/xml-js/lib/index.js
var require_lib = __commonJS((exports, module) => {
  var xml2js = require_xml2js();
  var xml2json = require_xml2json();
  var js2xml = require_js2xml();
  var json2xml = require_json2xml();
  module.exports = {
    xml2js,
    xml2json,
    js2xml,
    json2xml
  };
});

// node_modules/base-64/base64.js
var require_base64 = __commonJS((exports, module) => {
  /*! https://mths.be/base64 v1.0.0 by @mathias | MIT license */
  (function(root) {
    var freeExports = typeof exports == "object" && exports;
    var freeModule = typeof module == "object" && module && exports == freeExports && module;
    var freeGlobal = typeof global == "object" && global;
    if (freeGlobal.global === freeGlobal || freeGlobal.window === freeGlobal) {
      root = freeGlobal;
    }
    var InvalidCharacterError = function(message) {
      this.message = message;
    };
    InvalidCharacterError.prototype = new Error;
    InvalidCharacterError.prototype.name = "InvalidCharacterError";
    var error = function(message) {
      throw new InvalidCharacterError(message);
    };
    var TABLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    var REGEX_SPACE_CHARACTERS = /[\t\n\f\r ]/g;
    var decode = function(input) {
      input = String(input).replace(REGEX_SPACE_CHARACTERS, "");
      var length = input.length;
      if (length % 4 == 0) {
        input = input.replace(/==?$/, "");
        length = input.length;
      }
      if (length % 4 == 1 || /[^+a-zA-Z0-9/]/.test(input)) {
        error("Invalid character: the string to be decoded is not correctly encoded.");
      }
      var bitCounter = 0;
      var bitStorage;
      var buffer;
      var output = "";
      var position = -1;
      while (++position < length) {
        buffer = TABLE.indexOf(input.charAt(position));
        bitStorage = bitCounter % 4 ? bitStorage * 64 + buffer : buffer;
        if (bitCounter++ % 4) {
          output += String.fromCharCode(255 & bitStorage >> (-2 * bitCounter & 6));
        }
      }
      return output;
    };
    var encode = function(input) {
      input = String(input);
      if (/[^\0-\xFF]/.test(input)) {
        error("The string to be encoded contains characters outside of the " + "Latin1 range.");
      }
      var padding = input.length % 3;
      var output = "";
      var position = -1;
      var a;
      var b;
      var c;
      var buffer;
      var length = input.length - padding;
      while (++position < length) {
        a = input.charCodeAt(position) << 16;
        b = input.charCodeAt(++position) << 8;
        c = input.charCodeAt(++position);
        buffer = a + b + c;
        output += TABLE.charAt(buffer >> 18 & 63) + TABLE.charAt(buffer >> 12 & 63) + TABLE.charAt(buffer >> 6 & 63) + TABLE.charAt(buffer & 63);
      }
      if (padding == 2) {
        a = input.charCodeAt(position) << 8;
        b = input.charCodeAt(++position);
        buffer = a + b;
        output += TABLE.charAt(buffer >> 10) + TABLE.charAt(buffer >> 4 & 63) + TABLE.charAt(buffer << 2 & 63) + "=";
      } else if (padding == 1) {
        buffer = input.charCodeAt(position);
        output += TABLE.charAt(buffer >> 2) + TABLE.charAt(buffer << 4 & 63) + "==";
      }
      return output;
    };
    var base64 = {
      encode,
      decode,
      version: "1.0.0"
    };
    if (typeof define == "function" && typeof define.amd == "object" && define.amd) {
      define(function() {
        return base64;
      });
    } else if (freeExports && !freeExports.nodeType) {
      if (freeModule) {
        freeModule.exports = base64;
      } else {
        for (var key in base64) {
          base64.hasOwnProperty(key) && (freeExports[key] = base64[key]);
        }
      }
    } else {
      root.base64 = base64;
    }
  })(exports);
});

// scripts/jmap-client.ts
class JMAPClient {
  session = null;
  token;
  constructor(token) {
    this.token = token;
  }
  async getSession() {
    if (this.session)
      return this.session;
    const response = await fetch("https://api.fastmail.com/jmap/session", {
      headers: {
        Authorization: `Bearer ${this.token}`
      }
    });
    if (!response.ok) {
      throw new Error(`Failed to get session: ${response.statusText}`);
    }
    this.session = await response.json();
    return this.session;
  }
  async call(methodCalls) {
    const session = await this.getSession();
    const request = {
      using: [
        "urn:ietf:params:jmap:core",
        "urn:ietf:params:jmap:mail",
        "urn:ietf:params:jmap:submission"
      ],
      methodCalls
    };
    const response = await fetch(session.apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.token}`
      },
      body: JSON.stringify(request)
    });
    if (!response.ok) {
      throw new Error(`JMAP call failed: ${response.statusText}`);
    }
    return response.json();
  }
  async getAccountId() {
    const session = await this.getSession();
    return session.primaryAccounts["urn:ietf:params:jmap:mail"];
  }
}

// scripts/errors.ts
class FastmailError extends Error {
  code;
  suggestion;
  details;
  constructor(message, code, suggestion, details) {
    super(message);
    this.name = "FastmailError";
    this.code = code;
    this.suggestion = suggestion;
    this.details = details;
  }
  toJSON() {
    return {
      error: this.message,
      code: this.code,
      suggestion: this.suggestion,
      details: this.details
    };
  }
}
class NotFoundError extends FastmailError {
  constructor(resourceType, resourceId) {
    const suggestions = {
      email: `Use list_emails to see available emails, or search_emails to find specific ones`,
      mailbox: `Use list_mailboxes to see available folders/mailboxes`,
      calendar: `Use list_calendars to see available calendars`,
      event: `Use list_events with a date range to find events, or search_events to search by text`,
      thread: `The email thread may have been deleted or the email_id is incorrect. Use list_emails to verify`,
      reminder: `Use list_event_reminders to see reminders for an event`
    };
    super(`${resourceType.charAt(0).toUpperCase() + resourceType.slice(1)} not found: ${resourceId}`, "NOT_FOUND", suggestions[resourceType]);
    this.name = "NotFoundError";
  }
}

// scripts/tools/email.ts
class EmailTools {
  client;
  constructor(client) {
    this.client = client;
  }
  async getMailboxes() {
    const accountId = await this.client.getAccountId();
    const response = await this.client.call([
      ["Mailbox/get", { accountId, properties: ["id", "name", "role", "totalEmails", "unreadEmails"] }, "a"]
    ]);
    const result = response.methodResponses[0][1];
    return result.list;
  }
  async getInboxId() {
    const mailboxes = await this.getMailboxes();
    const inbox = mailboxes.find((m) => m.role === "inbox");
    if (!inbox)
      throw new Error("Inbox not found");
    return inbox.id;
  }
  async listEmails(mailboxId, limit = 20) {
    const accountId = await this.client.getAccountId();
    const targetMailbox = mailboxId || await this.getInboxId();
    const response = await this.client.call([
      ["Email/query", {
        accountId,
        filter: { inMailbox: targetMailbox },
        sort: [{ property: "receivedAt", isAscending: false }],
        limit
      }, "a"],
      ["Email/get", {
        accountId,
        "#ids": { resultOf: "a", name: "Email/query", path: "/ids" },
        properties: ["id", "blobId", "threadId", "mailboxIds", "subject", "from", "to", "cc", "receivedAt", "preview", "hasAttachment", "keywords"]
      }, "b"]
    ]);
    const result = response.methodResponses[1][1];
    return result.list;
  }
  async getEmail(emailId) {
    const accountId = await this.client.getAccountId();
    const response = await this.client.call([
      ["Email/get", {
        accountId,
        ids: [emailId],
        properties: ["id", "blobId", "threadId", "mailboxIds", "subject", "from", "to", "cc", "receivedAt", "preview", "hasAttachment", "keywords", "textBody", "htmlBody", "bodyValues"],
        fetchTextBodyValues: true,
        fetchHTMLBodyValues: true
      }, "a"]
    ]);
    const result = response.methodResponses[0][1];
    if (result.list.length === 0)
      throw new Error("Email not found");
    return result.list[0];
  }
  async searchEmails(query, limit = 20) {
    const accountId = await this.client.getAccountId();
    const response = await this.client.call([
      ["Email/query", {
        accountId,
        filter: { text: query },
        sort: [{ property: "receivedAt", isAscending: false }],
        limit
      }, "a"],
      ["Email/get", {
        accountId,
        "#ids": { resultOf: "a", name: "Email/query", path: "/ids" },
        properties: ["id", "blobId", "threadId", "mailboxIds", "subject", "from", "to", "cc", "receivedAt", "preview", "hasAttachment", "keywords"]
      }, "b"]
    ]);
    const result = response.methodResponses[1][1];
    return result.list;
  }
  async sendEmail(options) {
    const accountId = await this.client.getAccountId();
    const identityResponse = await this.client.call([
      ["Identity/get", { accountId }, "a"]
    ]);
    const identities = identityResponse.methodResponses[0][1].list;
    if (identities.length === 0)
      throw new Error("No identity found");
    const identityId = identities[0].id;
    const emailCreate = {
      mailboxIds: {},
      to: options.to,
      subject: options.subject,
      bodyValues: {
        body: { value: options.textBody, isEncodingProblem: false, isTruncated: false }
      },
      textBody: [{ partId: "body", type: "text/plain" }]
    };
    if (options.cc)
      emailCreate["cc"] = options.cc;
    if (options.bcc)
      emailCreate["bcc"] = options.bcc;
    if (options.inReplyTo)
      emailCreate["inReplyTo"] = [options.inReplyTo];
    if (options.references)
      emailCreate["references"] = options.references;
    if (options.htmlBody) {
      emailCreate["bodyValues"] = {
        textBody: { value: options.textBody, isEncodingProblem: false, isTruncated: false },
        htmlBody: { value: options.htmlBody, isEncodingProblem: false, isTruncated: false }
      };
      emailCreate["textBody"] = [{ partId: "textBody", type: "text/plain" }];
      emailCreate["htmlBody"] = [{ partId: "htmlBody", type: "text/html" }];
    }
    const response = await this.client.call([
      ["Email/set", {
        accountId,
        create: { draft: emailCreate }
      }, "a"],
      ["EmailSubmission/set", {
        accountId,
        create: {
          send: {
            identityId,
            emailId: "#draft"
          }
        },
        onSuccessUpdateEmail: {
          "#send": {
            "mailboxIds/drafts": null,
            "mailboxIds/sent": true,
            "keywords/$draft": null
          }
        }
      }, "b"]
    ]);
    const emailResult = response.methodResponses[0][1];
    const submissionResult = response.methodResponses[1][1];
    return {
      emailId: emailResult.created?.draft?.id || "",
      submissionId: submissionResult.created?.send?.id || ""
    };
  }
  async moveToFolder(emailId, targetMailboxId, sourceMailboxId) {
    const accountId = await this.client.getAccountId();
    const patch = {
      [`mailboxIds/${targetMailboxId}`]: true
    };
    const mailboxesToRemove = new Set;
    if (sourceMailboxId) {
      mailboxesToRemove.add(sourceMailboxId);
    } else {
      const currentEmail = await this.getEmail(emailId);
      for (const mailboxId of Object.keys(currentEmail.mailboxIds || {})) {
        if (mailboxId !== targetMailboxId) {
          mailboxesToRemove.add(mailboxId);
        }
      }
    }
    for (const mailboxId of mailboxesToRemove) {
      patch[`mailboxIds/${mailboxId}`] = null;
    }
    await this.client.call([
      ["Email/set", {
        accountId,
        update: {
          [emailId]: patch
        }
      }, "a"]
    ]);
  }
  async setKeywords(emailId, keywords) {
    const accountId = await this.client.getAccountId();
    const patch = {};
    for (const [keyword, value] of Object.entries(keywords)) {
      patch[`keywords/${keyword}`] = value || null;
    }
    await this.client.call([
      ["Email/set", {
        accountId,
        update: {
          [emailId]: patch
        }
      }, "a"]
    ]);
  }
  async deleteEmail(emailId) {
    const mailboxes = await this.getMailboxes();
    const trash = mailboxes.find((m) => m.role === "trash");
    if (!trash)
      throw new Error("Trash folder not found");
    await this.moveToFolder(emailId, trash.id);
  }
  async getThread(emailId) {
    const accountId = await this.client.getAccountId();
    const response = await this.client.call([
      ["Email/get", {
        accountId,
        ids: [emailId],
        properties: ["id", "threadId"]
      }, "a"]
    ]);
    const emailResult = response.methodResponses[0][1];
    if (emailResult.list.length === 0) {
      throw new NotFoundError("email", emailId);
    }
    const threadId = emailResult.list[0].threadId;
    const threadResponse = await this.client.call([
      ["Email/query", {
        accountId,
        filter: { inThread: threadId },
        sort: [{ property: "receivedAt", isAscending: true }]
      }, "a"],
      ["Email/get", {
        accountId,
        "#ids": { resultOf: "a", name: "Email/query", path: "/ids" },
        properties: ["id", "blobId", "threadId", "mailboxIds", "subject", "from", "to", "cc", "receivedAt", "preview", "hasAttachment", "keywords"]
      }, "b"]
    ]);
    const emails = threadResponse.methodResponses[1][1].list;
    if (emails.length === 0) {
      throw new NotFoundError("thread", threadId);
    }
    const participantMap = new Map;
    for (const email of emails) {
      const addParticipant = (p) => {
        if (p && !participantMap.has(p.email)) {
          participantMap.set(p.email, p);
        }
      };
      email.from?.forEach(addParticipant);
      email.to?.forEach(addParticipant);
      email.cc?.forEach(addParticipant);
    }
    return {
      id: threadId,
      emails,
      subject: emails[0].subject,
      participants: Array.from(participantMap.values()),
      latestDate: emails[emails.length - 1].receivedAt,
      emailCount: emails.length
    };
  }
  async bulkMoveToFolder(emailIds, targetMailboxId, sourceMailboxId) {
    const accountId = await this.client.getAccountId();
    const update = {};
    for (const emailId of emailIds) {
      update[emailId] = {
        [`mailboxIds/${targetMailboxId}`]: true
      };
      if (sourceMailboxId) {
        update[emailId][`mailboxIds/${sourceMailboxId}`] = null;
      }
    }
    const response = await this.client.call([
      ["Email/set", {
        accountId,
        update
      }, "a"]
    ]);
    const result = response.methodResponses[0][1];
    const succeeded = Object.keys(result.updated || {});
    const failed = Object.entries(result.notUpdated || {}).map(([id, err]) => ({
      id,
      error: err.description || err.type
    }));
    return { succeeded, failed };
  }
  async bulkSetKeywords(emailIds, keywords) {
    const accountId = await this.client.getAccountId();
    const patch = {};
    for (const [keyword, value] of Object.entries(keywords)) {
      patch[`keywords/${keyword}`] = value || null;
    }
    const update = {};
    for (const emailId of emailIds) {
      update[emailId] = { ...patch };
    }
    const response = await this.client.call([
      ["Email/set", {
        accountId,
        update
      }, "a"]
    ]);
    const result = response.methodResponses[0][1];
    const succeeded = Object.keys(result.updated || {});
    const failed = Object.entries(result.notUpdated || {}).map(([id, err]) => ({
      id,
      error: err.description || err.type
    }));
    return { succeeded, failed };
  }
  async bulkDeleteEmails(emailIds) {
    const mailboxes = await this.getMailboxes();
    const trash = mailboxes.find((m) => m.role === "trash");
    if (!trash) {
      throw new NotFoundError("mailbox", "Trash");
    }
    return this.bulkMoveToFolder(emailIds, trash.id);
  }
}

// node_modules/tsdav/dist/tsdav.esm.js
var import_cross_fetch = __toESM(require_browser_ponyfill(), 1);
var import_debug = __toESM(require_browser(), 1);
var import_xml_js = __toESM(require_lib(), 1);
var import_base_64 = __toESM(require_base64(), 1);
var DAVNamespace;
(function(DAVNamespace2) {
  DAVNamespace2["CALENDAR_SERVER"] = "http://calendarserver.org/ns/";
  DAVNamespace2["CALDAV_APPLE"] = "http://apple.com/ns/ical/";
  DAVNamespace2["CALDAV"] = "urn:ietf:params:xml:ns:caldav";
  DAVNamespace2["CARDDAV"] = "urn:ietf:params:xml:ns:carddav";
  DAVNamespace2["DAV"] = "DAV:";
})(DAVNamespace || (DAVNamespace = {}));
var DAVAttributeMap = {
  [DAVNamespace.CALDAV]: "xmlns:c",
  [DAVNamespace.CARDDAV]: "xmlns:card",
  [DAVNamespace.CALENDAR_SERVER]: "xmlns:cs",
  [DAVNamespace.CALDAV_APPLE]: "xmlns:ca",
  [DAVNamespace.DAV]: "xmlns:d"
};
var DAVNamespaceShort;
(function(DAVNamespaceShort2) {
  DAVNamespaceShort2["CALDAV"] = "c";
  DAVNamespaceShort2["CARDDAV"] = "card";
  DAVNamespaceShort2["CALENDAR_SERVER"] = "cs";
  DAVNamespaceShort2["CALDAV_APPLE"] = "ca";
  DAVNamespaceShort2["DAV"] = "d";
})(DAVNamespaceShort || (DAVNamespaceShort = {}));
var ICALObjects;
(function(ICALObjects2) {
  ICALObjects2["VEVENT"] = "VEVENT";
  ICALObjects2["VTODO"] = "VTODO";
  ICALObjects2["VJOURNAL"] = "VJOURNAL";
  ICALObjects2["VFREEBUSY"] = "VFREEBUSY";
  ICALObjects2["VTIMEZONE"] = "VTIMEZONE";
  ICALObjects2["VALARM"] = "VALARM";
})(ICALObjects || (ICALObjects = {}));
var camelCase = (str) => str.replace(/([-_]\w)/g, (g) => g[1].toUpperCase());
var nativeType = (value) => {
  const nValue = Number(value);
  if (!Number.isNaN(nValue)) {
    return nValue;
  }
  const bValue = value.toLowerCase();
  if (bValue === "true") {
    return true;
  }
  if (bValue === "false") {
    return false;
  }
  return value;
};
var urlEquals = (urlA, urlB) => {
  if (!urlA && !urlB) {
    return true;
  }
  if (!urlA || !urlB) {
    return false;
  }
  const trimmedUrlA = urlA.trim();
  const trimmedUrlB = urlB.trim();
  if (Math.abs(trimmedUrlA.length - trimmedUrlB.length) > 1) {
    return false;
  }
  const strippedUrlA = trimmedUrlA.slice(-1) === "/" ? trimmedUrlA.slice(0, -1) : trimmedUrlA;
  const strippedUrlB = trimmedUrlB.slice(-1) === "/" ? trimmedUrlB.slice(0, -1) : trimmedUrlB;
  return urlA.includes(strippedUrlB) || urlB.includes(strippedUrlA);
};
var urlContains = (urlA, urlB) => {
  if (!urlA && !urlB) {
    return true;
  }
  if (!urlA || !urlB) {
    return false;
  }
  const trimmedUrlA = urlA.trim();
  const trimmedUrlB = urlB.trim();
  const strippedUrlA = trimmedUrlA.slice(-1) === "/" ? trimmedUrlA.slice(0, -1) : trimmedUrlA;
  const strippedUrlB = trimmedUrlB.slice(-1) === "/" ? trimmedUrlB.slice(0, -1) : trimmedUrlB;
  return urlA.includes(strippedUrlB) || urlB.includes(strippedUrlA);
};
var getDAVAttribute = (nsArr) => nsArr.reduce((prev, curr) => ({ ...prev, [DAVAttributeMap[curr]]: curr }), {});
var cleanupFalsy = (obj) => Object.entries(obj).reduce((prev, [key, value]) => {
  if (value)
    return { ...prev, [key]: value };
  return prev;
}, {});
var conditionalParam = (key, param) => {
  if (param) {
    return {
      [key]: param
    };
  }
  return {};
};
var excludeHeaders = (headers, headersToExclude) => {
  if (!headers) {
    return {};
  }
  if (!headersToExclude || headersToExclude.length === 0) {
    return headers;
  }
  return Object.fromEntries(Object.entries(headers).filter(([key]) => !headersToExclude.includes(key)));
};
var requestHelpers = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  cleanupFalsy,
  conditionalParam,
  excludeHeaders,
  getDAVAttribute,
  urlContains,
  urlEquals
});
var debug$5 = import_debug.default("tsdav:request");
var davRequest = async (params) => {
  var _a;
  const { url, init, convertIncoming = true, parseOutgoing = true, fetchOptions = {} } = params;
  const { headers = {}, body, namespace, method, attributes } = init;
  const xmlBody = convertIncoming ? import_xml_js.default.js2xml({
    _declaration: { _attributes: { version: "1.0", encoding: "utf-8" } },
    ...body,
    _attributes: attributes
  }, {
    compact: true,
    spaces: 2,
    elementNameFn: (name) => {
      if (namespace && !/^.+:.+/.test(name)) {
        return `${namespace}:${name}`;
      }
      return name;
    }
  }) : body;
  const fetchOptionsWithoutHeaders = {
    ...fetchOptions
  };
  delete fetchOptionsWithoutHeaders.headers;
  const davResponse = await import_cross_fetch.fetch(url, {
    headers: {
      "Content-Type": "text/xml;charset=UTF-8",
      ...cleanupFalsy(headers),
      ...fetchOptions.headers || {}
    },
    body: xmlBody,
    method,
    ...fetchOptionsWithoutHeaders
  });
  const resText = await davResponse.text();
  if (!davResponse.ok || !((_a = davResponse.headers.get("content-type")) === null || _a === undefined ? undefined : _a.includes("xml")) || !parseOutgoing) {
    return [
      {
        href: davResponse.url,
        ok: davResponse.ok,
        status: davResponse.status,
        statusText: davResponse.statusText,
        raw: resText
      }
    ];
  }
  const result = import_xml_js.default.xml2js(resText, {
    compact: true,
    trim: true,
    textFn: (value, parentElement) => {
      try {
        const parentOfParent = parentElement._parent;
        const pOpKeys = Object.keys(parentOfParent);
        const keyNo = pOpKeys.length;
        const keyName = pOpKeys[keyNo - 1];
        const arrOfKey = parentOfParent[keyName];
        const arrOfKeyLen = arrOfKey.length;
        if (arrOfKeyLen > 0) {
          const arr = arrOfKey;
          const arrIndex = arrOfKey.length - 1;
          arr[arrIndex] = nativeType(value);
        } else {
          parentOfParent[keyName] = nativeType(value);
        }
      } catch (e) {
        debug$5(e.stack);
      }
    },
    elementNameFn: (attributeName) => camelCase(attributeName.replace(/^.+:/, "")),
    attributesFn: (value) => {
      const newVal = { ...value };
      delete newVal.xmlns;
      return newVal;
    },
    ignoreDeclaration: true
  });
  const responseBodies = Array.isArray(result.multistatus.response) ? result.multistatus.response : [result.multistatus.response];
  return responseBodies.map((responseBody) => {
    var _a2, _b;
    const statusRegex = /^\S+\s(?<status>\d+)\s(?<statusText>.+)$/;
    if (!responseBody) {
      return {
        status: davResponse.status,
        statusText: davResponse.statusText,
        ok: davResponse.ok
      };
    }
    const matchArr = statusRegex.exec(responseBody.status);
    return {
      raw: result,
      href: responseBody.href,
      status: (matchArr === null || matchArr === undefined ? undefined : matchArr.groups) ? Number.parseInt(matchArr === null || matchArr === undefined ? undefined : matchArr.groups.status, 10) : davResponse.status,
      statusText: (_b = (_a2 = matchArr === null || matchArr === undefined ? undefined : matchArr.groups) === null || _a2 === undefined ? undefined : _a2.statusText) !== null && _b !== undefined ? _b : davResponse.statusText,
      ok: !responseBody.error,
      error: responseBody.error,
      responsedescription: responseBody.responsedescription,
      props: (Array.isArray(responseBody.propstat) ? responseBody.propstat : [responseBody.propstat]).reduce((prev, curr) => {
        return {
          ...prev,
          ...curr === null || curr === undefined ? undefined : curr.prop
        };
      }, {})
    };
  });
};
var propfind = async (params) => {
  const { url, props, depth, headers, headersToExclude, fetchOptions = {} } = params;
  return davRequest({
    url,
    init: {
      method: "PROPFIND",
      headers: excludeHeaders(cleanupFalsy({ depth, ...headers }), headersToExclude),
      namespace: DAVNamespaceShort.DAV,
      body: {
        propfind: {
          _attributes: getDAVAttribute([
            DAVNamespace.CALDAV,
            DAVNamespace.CALDAV_APPLE,
            DAVNamespace.CALENDAR_SERVER,
            DAVNamespace.CARDDAV,
            DAVNamespace.DAV
          ]),
          prop: props
        }
      }
    },
    fetchOptions
  });
};
var createObject = async (params) => {
  const { url, data, headers, headersToExclude, fetchOptions = {} } = params;
  return import_cross_fetch.fetch(url, {
    method: "PUT",
    body: data,
    headers: excludeHeaders(headers, headersToExclude),
    ...fetchOptions
  });
};
var updateObject = async (params) => {
  const { url, data, etag, headers, headersToExclude, fetchOptions = {} } = params;
  return import_cross_fetch.fetch(url, {
    method: "PUT",
    body: data,
    headers: excludeHeaders(cleanupFalsy({ "If-Match": etag, ...headers }), headersToExclude),
    ...fetchOptions
  });
};
var deleteObject = async (params) => {
  const { url, headers, etag, headersToExclude, fetchOptions = {} } = params;
  return import_cross_fetch.fetch(url, {
    method: "DELETE",
    headers: excludeHeaders(cleanupFalsy({ "If-Match": etag, ...headers }), headersToExclude),
    ...fetchOptions
  });
};
var request = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  createObject,
  davRequest,
  deleteObject,
  propfind,
  updateObject
});
function hasFields(obj, fields) {
  const inObj = (object) => fields.every((f) => object[f]);
  if (Array.isArray(obj)) {
    return obj.every((o) => inObj(o));
  }
  return inObj(obj);
}
var findMissingFieldNames = (obj, fields) => fields.reduce((prev, curr) => obj[curr] ? prev : `${prev.length ? `${prev},` : ""}${curr.toString()}`, "");
var debug$4 = import_debug.default("tsdav:collection");
var collectionQuery = async (params) => {
  const { url, body, depth, defaultNamespace = DAVNamespaceShort.DAV, headers, headersToExclude, fetchOptions = {} } = params;
  const queryResults = await davRequest({
    url,
    init: {
      method: "REPORT",
      headers: excludeHeaders(cleanupFalsy({ depth, ...headers }), headersToExclude),
      namespace: defaultNamespace,
      body
    },
    fetchOptions
  });
  if (queryResults.length === 1 && !queryResults[0].raw) {
    return [];
  }
  return queryResults;
};
var makeCollection = async (params) => {
  const { url, props, depth, headers, headersToExclude, fetchOptions = {} } = params;
  return davRequest({
    url,
    init: {
      method: "MKCOL",
      headers: excludeHeaders(cleanupFalsy({ depth, ...headers }), headersToExclude),
      namespace: DAVNamespaceShort.DAV,
      body: props ? {
        mkcol: {
          set: {
            prop: props
          }
        }
      } : undefined
    },
    fetchOptions
  });
};
var supportedReportSet = async (params) => {
  var _a, _b, _c, _d, _e;
  const { collection, headers, headersToExclude, fetchOptions = {} } = params;
  const res = await propfind({
    url: collection.url,
    props: {
      [`${DAVNamespaceShort.DAV}:supported-report-set`]: {}
    },
    depth: "0",
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  return (_e = (_d = (_c = (_b = (_a = res[0]) === null || _a === undefined ? undefined : _a.props) === null || _b === undefined ? undefined : _b.supportedReportSet) === null || _c === undefined ? undefined : _c.supportedReport) === null || _d === undefined ? undefined : _d.map((sr) => Object.keys(sr.report)[0])) !== null && _e !== undefined ? _e : [];
};
var isCollectionDirty = async (params) => {
  var _a, _b, _c;
  const { collection, headers, headersToExclude, fetchOptions = {} } = params;
  const responses = await propfind({
    url: collection.url,
    props: {
      [`${DAVNamespaceShort.CALENDAR_SERVER}:getctag`]: {}
    },
    depth: "0",
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  const res = responses.filter((r) => urlContains(collection.url, r.href))[0];
  if (!res) {
    throw new Error("Collection does not exist on server");
  }
  return {
    isDirty: `${collection.ctag}` !== `${(_a = res.props) === null || _a === undefined ? undefined : _a.getctag}`,
    newCtag: (_c = (_b = res.props) === null || _b === undefined ? undefined : _b.getctag) === null || _c === undefined ? undefined : _c.toString()
  };
};
var syncCollection = (params) => {
  const { url, props, headers, syncLevel, syncToken, headersToExclude, fetchOptions } = params;
  return davRequest({
    url,
    init: {
      method: "REPORT",
      namespace: DAVNamespaceShort.DAV,
      headers: excludeHeaders({ ...headers }, headersToExclude),
      body: {
        "sync-collection": {
          _attributes: getDAVAttribute([
            DAVNamespace.CALDAV,
            DAVNamespace.CARDDAV,
            DAVNamespace.DAV
          ]),
          "sync-level": syncLevel,
          "sync-token": syncToken,
          [`${DAVNamespaceShort.DAV}:prop`]: props
        }
      }
    },
    fetchOptions
  });
};
var smartCollectionSync = async (params) => {
  var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l;
  const { collection, method, headers, headersToExclude, account, detailedResult, fetchOptions = {} } = params;
  const requiredFields = ["accountType", "homeUrl"];
  if (!account || !hasFields(account, requiredFields)) {
    if (!account) {
      throw new Error("no account for smartCollectionSync");
    }
    throw new Error(`account must have ${findMissingFieldNames(account, requiredFields)} before smartCollectionSync`);
  }
  const syncMethod = method !== null && method !== undefined ? method : ((_a = collection.reports) === null || _a === undefined ? undefined : _a.includes("syncCollection")) ? "webdav" : "basic";
  debug$4(`smart collection sync with type ${account.accountType} and method ${syncMethod}`);
  if (syncMethod === "webdav") {
    const result = await syncCollection({
      url: collection.url,
      props: {
        [`${DAVNamespaceShort.DAV}:getetag`]: {},
        [`${account.accountType === "caldav" ? DAVNamespaceShort.CALDAV : DAVNamespaceShort.CARDDAV}:${account.accountType === "caldav" ? "calendar-data" : "address-data"}`]: {},
        [`${DAVNamespaceShort.DAV}:displayname`]: {}
      },
      syncLevel: 1,
      syncToken: collection.syncToken,
      headers: excludeHeaders(headers, headersToExclude),
      fetchOptions
    });
    const objectResponses = result.filter((r) => {
      var _a2;
      const extName = account.accountType === "caldav" ? ".ics" : ".vcf";
      return ((_a2 = r.href) === null || _a2 === undefined ? undefined : _a2.slice(-4)) === extName;
    });
    const changedObjectUrls = objectResponses.filter((o) => o.status !== 404).map((r) => r.href);
    const deletedObjectUrls = objectResponses.filter((o) => o.status === 404).map((r) => r.href);
    const multiGetObjectResponse = changedObjectUrls.length ? (_c = await ((_b = collection === null || collection === undefined ? undefined : collection.objectMultiGet) === null || _b === undefined ? undefined : _b.call(collection, {
      url: collection.url,
      props: {
        [`${DAVNamespaceShort.DAV}:getetag`]: {},
        [`${account.accountType === "caldav" ? DAVNamespaceShort.CALDAV : DAVNamespaceShort.CARDDAV}:${account.accountType === "caldav" ? "calendar-data" : "address-data"}`]: {}
      },
      objectUrls: changedObjectUrls,
      depth: "1",
      headers: excludeHeaders(headers, headersToExclude),
      fetchOptions
    }))) !== null && _c !== undefined ? _c : [] : [];
    const remoteObjects = multiGetObjectResponse.map((res) => {
      var _a2, _b2, _c2, _d2, _e2, _f2, _g2, _h2, _j2, _k2;
      return {
        url: (_a2 = res.href) !== null && _a2 !== undefined ? _a2 : "",
        etag: (_b2 = res.props) === null || _b2 === undefined ? undefined : _b2.getetag,
        data: (account === null || account === undefined ? undefined : account.accountType) === "caldav" ? (_e2 = (_d2 = (_c2 = res.props) === null || _c2 === undefined ? undefined : _c2.calendarData) === null || _d2 === undefined ? undefined : _d2._cdata) !== null && _e2 !== undefined ? _e2 : (_f2 = res.props) === null || _f2 === undefined ? undefined : _f2.calendarData : (_j2 = (_h2 = (_g2 = res.props) === null || _g2 === undefined ? undefined : _g2.addressData) === null || _h2 === undefined ? undefined : _h2._cdata) !== null && _j2 !== undefined ? _j2 : (_k2 = res.props) === null || _k2 === undefined ? undefined : _k2.addressData
      };
    });
    const localObjects = (_d = collection.objects) !== null && _d !== undefined ? _d : [];
    const created = remoteObjects.filter((o) => localObjects.every((lo) => !urlContains(lo.url, o.url)));
    const updated = localObjects.reduce((prev, curr) => {
      const found = remoteObjects.find((ro) => urlContains(ro.url, curr.url));
      if (found && found.etag && found.etag !== curr.etag) {
        return [...prev, found];
      }
      return prev;
    }, []);
    const deleted = deletedObjectUrls.map((o) => ({
      url: o,
      etag: ""
    }));
    const unchanged = localObjects.filter((lo) => remoteObjects.some((ro) => urlContains(lo.url, ro.url) && ro.etag === lo.etag));
    return {
      ...collection,
      objects: detailedResult ? { created, updated, deleted } : [...unchanged, ...created, ...updated],
      syncToken: (_h = (_g = (_f = (_e = result[0]) === null || _e === undefined ? undefined : _e.raw) === null || _f === undefined ? undefined : _f.multistatus) === null || _g === undefined ? undefined : _g.syncToken) !== null && _h !== undefined ? _h : collection.syncToken
    };
  }
  if (syncMethod === "basic") {
    const { isDirty, newCtag } = await isCollectionDirty({
      collection,
      headers: excludeHeaders(headers, headersToExclude),
      fetchOptions
    });
    const localObjects = (_j = collection.objects) !== null && _j !== undefined ? _j : [];
    const remoteObjects = (_l = await ((_k = collection.fetchObjects) === null || _k === undefined ? undefined : _k.call(collection, {
      collection,
      headers: excludeHeaders(headers, headersToExclude),
      fetchOptions
    }))) !== null && _l !== undefined ? _l : [];
    const created = remoteObjects.filter((ro) => localObjects.every((lo) => !urlContains(lo.url, ro.url)));
    const updated = localObjects.reduce((prev, curr) => {
      const found = remoteObjects.find((ro) => urlContains(ro.url, curr.url));
      if (found && found.etag && found.etag !== curr.etag) {
        return [...prev, found];
      }
      return prev;
    }, []);
    const deleted = localObjects.filter((cal) => remoteObjects.every((ro) => !urlContains(ro.url, cal.url)));
    const unchanged = localObjects.filter((lo) => remoteObjects.some((ro) => urlContains(lo.url, ro.url) && ro.etag === lo.etag));
    if (isDirty) {
      return {
        ...collection,
        objects: detailedResult ? { created, updated, deleted } : [...unchanged, ...created, ...updated],
        ctag: newCtag
      };
    }
  }
  return detailedResult ? {
    ...collection,
    objects: {
      created: [],
      updated: [],
      deleted: []
    }
  } : collection;
};
var collection = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  collectionQuery,
  isCollectionDirty,
  makeCollection,
  smartCollectionSync,
  supportedReportSet,
  syncCollection
});
var debug$3 = import_debug.default("tsdav:addressBook");
var addressBookQuery = async (params) => {
  const { url, props, filters, depth, headers, headersToExclude, fetchOptions = {} } = params;
  return collectionQuery({
    url,
    body: {
      "addressbook-query": cleanupFalsy({
        _attributes: getDAVAttribute([DAVNamespace.CARDDAV, DAVNamespace.DAV]),
        [`${DAVNamespaceShort.DAV}:prop`]: props,
        filter: filters !== null && filters !== undefined ? filters : {
          "prop-filter": {
            _attributes: {
              name: "FN"
            }
          }
        }
      })
    },
    defaultNamespace: DAVNamespaceShort.CARDDAV,
    depth,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
};
var addressBookMultiGet = async (params) => {
  const { url, props, objectUrls, depth, headers, headersToExclude, fetchOptions = {} } = params;
  return collectionQuery({
    url,
    body: {
      "addressbook-multiget": cleanupFalsy({
        _attributes: getDAVAttribute([DAVNamespace.DAV, DAVNamespace.CARDDAV]),
        [`${DAVNamespaceShort.DAV}:prop`]: props,
        [`${DAVNamespaceShort.DAV}:href`]: objectUrls
      })
    },
    defaultNamespace: DAVNamespaceShort.CARDDAV,
    depth,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
};
var fetchAddressBooks = async (params) => {
  const { account, headers, props: customProps, headersToExclude, fetchOptions = {} } = params !== null && params !== undefined ? params : {};
  const requiredFields = ["homeUrl", "rootUrl"];
  if (!account || !hasFields(account, requiredFields)) {
    if (!account) {
      throw new Error("no account for fetchAddressBooks");
    }
    throw new Error(`account must have ${findMissingFieldNames(account, requiredFields)} before fetchAddressBooks`);
  }
  const res = await propfind({
    url: account.homeUrl,
    props: customProps !== null && customProps !== undefined ? customProps : {
      [`${DAVNamespaceShort.DAV}:displayname`]: {},
      [`${DAVNamespaceShort.CALENDAR_SERVER}:getctag`]: {},
      [`${DAVNamespaceShort.DAV}:resourcetype`]: {},
      [`${DAVNamespaceShort.DAV}:sync-token`]: {}
    },
    depth: "1",
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  return Promise.all(res.filter((r) => {
    var _a, _b;
    return Object.keys((_b = (_a = r.props) === null || _a === undefined ? undefined : _a.resourcetype) !== null && _b !== undefined ? _b : {}).includes("addressbook");
  }).map((rs) => {
    var _a, _b, _c, _d, _e, _f, _g, _h, _j;
    const displayName = (_c = (_b = (_a = rs.props) === null || _a === undefined ? undefined : _a.displayname) === null || _b === undefined ? undefined : _b._cdata) !== null && _c !== undefined ? _c : (_d = rs.props) === null || _d === undefined ? undefined : _d.displayname;
    debug$3(`Found address book named ${typeof displayName === "string" ? displayName : ""},
             props: ${JSON.stringify(rs.props)}`);
    return {
      url: new URL((_e = rs.href) !== null && _e !== undefined ? _e : "", (_f = account.rootUrl) !== null && _f !== undefined ? _f : "").href,
      ctag: (_g = rs.props) === null || _g === undefined ? undefined : _g.getctag,
      displayName: typeof displayName === "string" ? displayName : "",
      resourcetype: Object.keys((_h = rs.props) === null || _h === undefined ? undefined : _h.resourcetype),
      syncToken: (_j = rs.props) === null || _j === undefined ? undefined : _j.syncToken
    };
  }).map(async (addr) => ({
    ...addr,
    reports: await supportedReportSet({
      collection: addr,
      headers: excludeHeaders(headers, headersToExclude),
      fetchOptions
    })
  })));
};
var fetchVCards = async (params) => {
  const { addressBook, headers, objectUrls, headersToExclude, urlFilter = (url) => url, useMultiGet = true, fetchOptions = {} } = params;
  debug$3(`Fetching vcards from ${addressBook === null || addressBook === undefined ? undefined : addressBook.url}`);
  const requiredFields = ["url"];
  if (!addressBook || !hasFields(addressBook, requiredFields)) {
    if (!addressBook) {
      throw new Error("cannot fetchVCards for undefined addressBook");
    }
    throw new Error(`addressBook must have ${findMissingFieldNames(addressBook, requiredFields)} before fetchVCards`);
  }
  const vcardUrls = (objectUrls !== null && objectUrls !== undefined ? objectUrls : (await addressBookQuery({
    url: addressBook.url,
    props: { [`${DAVNamespaceShort.DAV}:getetag`]: {} },
    depth: "1",
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  })).map((res) => {
    var _a;
    return res.ok ? (_a = res.href) !== null && _a !== undefined ? _a : "" : "";
  })).map((url) => url.startsWith("http") || !url ? url : new URL(url, addressBook.url).href).filter(urlFilter).map((url) => new URL(url).pathname);
  let vCardResults = [];
  if (vcardUrls.length > 0) {
    if (useMultiGet) {
      vCardResults = await addressBookMultiGet({
        url: addressBook.url,
        props: {
          [`${DAVNamespaceShort.DAV}:getetag`]: {},
          [`${DAVNamespaceShort.CARDDAV}:address-data`]: {}
        },
        objectUrls: vcardUrls,
        depth: "1",
        headers: excludeHeaders(headers, headersToExclude),
        fetchOptions
      });
    } else {
      vCardResults = await addressBookQuery({
        url: addressBook.url,
        props: {
          [`${DAVNamespaceShort.DAV}:getetag`]: {},
          [`${DAVNamespaceShort.CARDDAV}:address-data`]: {}
        },
        depth: "1",
        headers: excludeHeaders(headers, headersToExclude),
        fetchOptions
      });
    }
  }
  return vCardResults.map((res) => {
    var _a, _b, _c, _d, _e, _f;
    return {
      url: new URL((_a = res.href) !== null && _a !== undefined ? _a : "", addressBook.url).href,
      etag: (_b = res.props) === null || _b === undefined ? undefined : _b.getetag,
      data: (_e = (_d = (_c = res.props) === null || _c === undefined ? undefined : _c.addressData) === null || _d === undefined ? undefined : _d._cdata) !== null && _e !== undefined ? _e : (_f = res.props) === null || _f === undefined ? undefined : _f.addressData
    };
  });
};
var createVCard = async (params) => {
  const { addressBook, vCardString, filename, headers, headersToExclude, fetchOptions = {} } = params;
  return createObject({
    url: new URL(filename, addressBook.url).href,
    data: vCardString,
    headers: excludeHeaders({
      "content-type": "text/vcard; charset=utf-8",
      "If-None-Match": "*",
      ...headers
    }, headersToExclude),
    fetchOptions
  });
};
var updateVCard = async (params) => {
  const { vCard, headers, headersToExclude, fetchOptions = {} } = params;
  return updateObject({
    url: vCard.url,
    data: vCard.data,
    etag: vCard.etag,
    headers: excludeHeaders({
      "content-type": "text/vcard; charset=utf-8",
      ...headers
    }, headersToExclude),
    fetchOptions
  });
};
var deleteVCard = async (params) => {
  const { vCard, headers, headersToExclude, fetchOptions = {} } = params;
  return deleteObject({
    url: vCard.url,
    etag: vCard.etag,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
};
var addressBook = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  addressBookMultiGet,
  addressBookQuery,
  createVCard,
  deleteVCard,
  fetchAddressBooks,
  fetchVCards,
  updateVCard
});
var debug$2 = import_debug.default("tsdav:calendar");
var fetchCalendarUserAddresses = async (params) => {
  var _a, _b, _c;
  const { account, headers, headersToExclude, fetchOptions = {} } = params;
  const requiredFields = ["principalUrl", "rootUrl"];
  if (!hasFields(account, requiredFields)) {
    throw new Error(`account must have ${findMissingFieldNames(account, requiredFields)} before fetchUserAddresses`);
  }
  debug$2(`Fetch user addresses from ${account.principalUrl}`);
  const responses = await propfind({
    url: account.principalUrl,
    props: { [`${DAVNamespaceShort.CALDAV}:calendar-user-address-set`]: {} },
    depth: "0",
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  const matched = responses.find((r) => urlContains(account.principalUrl, r.href));
  if (!matched || !matched.ok) {
    throw new Error("cannot find calendarUserAddresses");
  }
  const addresses = ((_c = (_b = (_a = matched === null || matched === undefined ? undefined : matched.props) === null || _a === undefined ? undefined : _a.calendarUserAddressSet) === null || _b === undefined ? undefined : _b.href) === null || _c === undefined ? undefined : _c.filter(Boolean)) || [];
  debug$2(`Fetched calendar user addresses ${addresses}`);
  return addresses;
};
var calendarQuery = async (params) => {
  const { url, props, filters, timezone, depth, headers, headersToExclude, fetchOptions = {} } = params;
  return collectionQuery({
    url,
    body: {
      "calendar-query": cleanupFalsy({
        _attributes: getDAVAttribute([
          DAVNamespace.CALDAV,
          DAVNamespace.CALENDAR_SERVER,
          DAVNamespace.CALDAV_APPLE,
          DAVNamespace.DAV
        ]),
        [`${DAVNamespaceShort.DAV}:prop`]: props,
        filter: filters,
        timezone
      })
    },
    defaultNamespace: DAVNamespaceShort.CALDAV,
    depth,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
};
var calendarMultiGet = async (params) => {
  const { url, props, objectUrls, filters, timezone, depth, headers, headersToExclude, fetchOptions = {} } = params;
  return collectionQuery({
    url,
    body: {
      "calendar-multiget": cleanupFalsy({
        _attributes: getDAVAttribute([DAVNamespace.DAV, DAVNamespace.CALDAV]),
        [`${DAVNamespaceShort.DAV}:prop`]: props,
        [`${DAVNamespaceShort.DAV}:href`]: objectUrls,
        filter: filters,
        timezone
      })
    },
    defaultNamespace: DAVNamespaceShort.CALDAV,
    depth,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
};
var makeCalendar = async (params) => {
  const { url, props, depth, headers, headersToExclude, fetchOptions = {} } = params;
  return davRequest({
    url,
    init: {
      method: "MKCALENDAR",
      headers: excludeHeaders(cleanupFalsy({ depth, ...headers }), headersToExclude),
      namespace: DAVNamespaceShort.DAV,
      body: {
        [`${DAVNamespaceShort.CALDAV}:mkcalendar`]: {
          _attributes: getDAVAttribute([
            DAVNamespace.DAV,
            DAVNamespace.CALDAV,
            DAVNamespace.CALDAV_APPLE
          ]),
          set: {
            prop: props
          }
        }
      }
    },
    fetchOptions
  });
};
var fetchCalendars = async (params) => {
  const { headers, account, props: customProps, projectedProps, headersToExclude, fetchOptions = {} } = params !== null && params !== undefined ? params : {};
  const requiredFields = ["homeUrl", "rootUrl"];
  if (!account || !hasFields(account, requiredFields)) {
    if (!account) {
      throw new Error("no account for fetchCalendars");
    }
    throw new Error(`account must have ${findMissingFieldNames(account, requiredFields)} before fetchCalendars`);
  }
  const res = await propfind({
    url: account.homeUrl,
    props: customProps !== null && customProps !== undefined ? customProps : {
      [`${DAVNamespaceShort.CALDAV}:calendar-description`]: {},
      [`${DAVNamespaceShort.CALDAV}:calendar-timezone`]: {},
      [`${DAVNamespaceShort.DAV}:displayname`]: {},
      [`${DAVNamespaceShort.CALDAV_APPLE}:calendar-color`]: {},
      [`${DAVNamespaceShort.CALENDAR_SERVER}:getctag`]: {},
      [`${DAVNamespaceShort.DAV}:resourcetype`]: {},
      [`${DAVNamespaceShort.CALDAV}:supported-calendar-component-set`]: {},
      [`${DAVNamespaceShort.DAV}:sync-token`]: {}
    },
    depth: "1",
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  return Promise.all(res.filter((r) => {
    var _a, _b;
    return Object.keys((_b = (_a = r.props) === null || _a === undefined ? undefined : _a.resourcetype) !== null && _b !== undefined ? _b : {}).includes("calendar");
  }).filter((rc) => {
    var _a, _b, _c, _d, _e, _f;
    const components = Array.isArray((_b = (_a = rc.props) === null || _a === undefined ? undefined : _a.supportedCalendarComponentSet) === null || _b === undefined ? undefined : _b.comp) ? (_c = rc.props) === null || _c === undefined ? undefined : _c.supportedCalendarComponentSet.comp.map((sc) => sc._attributes.name) : [(_f = (_e = (_d = rc.props) === null || _d === undefined ? undefined : _d.supportedCalendarComponentSet) === null || _e === undefined ? undefined : _e.comp) === null || _f === undefined ? undefined : _f._attributes.name];
    return components.some((c) => Object.values(ICALObjects).includes(c));
  }).map((rs) => {
    var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p, _q, _r;
    const description = (_a = rs.props) === null || _a === undefined ? undefined : _a.calendarDescription;
    const timezone = (_b = rs.props) === null || _b === undefined ? undefined : _b.calendarTimezone;
    return {
      description: typeof description === "string" ? description : "",
      timezone: typeof timezone === "string" ? timezone : "",
      url: new URL((_c = rs.href) !== null && _c !== undefined ? _c : "", (_d = account.rootUrl) !== null && _d !== undefined ? _d : "").href,
      ctag: (_e = rs.props) === null || _e === undefined ? undefined : _e.getctag,
      calendarColor: (_f = rs.props) === null || _f === undefined ? undefined : _f.calendarColor,
      displayName: (_h = (_g = rs.props) === null || _g === undefined ? undefined : _g.displayname._cdata) !== null && _h !== undefined ? _h : (_j = rs.props) === null || _j === undefined ? undefined : _j.displayname,
      components: Array.isArray((_k = rs.props) === null || _k === undefined ? undefined : _k.supportedCalendarComponentSet.comp) ? (_l = rs.props) === null || _l === undefined ? undefined : _l.supportedCalendarComponentSet.comp.map((sc) => sc._attributes.name) : [(_o = (_m = rs.props) === null || _m === undefined ? undefined : _m.supportedCalendarComponentSet.comp) === null || _o === undefined ? undefined : _o._attributes.name],
      resourcetype: Object.keys((_p = rs.props) === null || _p === undefined ? undefined : _p.resourcetype),
      syncToken: (_q = rs.props) === null || _q === undefined ? undefined : _q.syncToken,
      ...conditionalParam("projectedProps", Object.fromEntries(Object.entries((_r = rs.props) !== null && _r !== undefined ? _r : {}).filter(([key]) => projectedProps === null || projectedProps === undefined ? undefined : projectedProps[key])))
    };
  }).map(async (cal) => ({
    ...cal,
    reports: await supportedReportSet({
      collection: cal,
      headers: excludeHeaders(headers, headersToExclude),
      fetchOptions
    })
  })));
};
var fetchCalendarObjects = async (params) => {
  const { calendar, objectUrls, filters: customFilters, timeRange, headers, expand, urlFilter = (url) => Boolean(url === null || url === undefined ? undefined : url.includes(".ics")), useMultiGet = true, headersToExclude, fetchOptions = {} } = params;
  if (timeRange) {
    const ISO_8601 = /^\d{4}(-\d\d(-\d\d(T\d\d:\d\d(:\d\d)?(\.\d+)?(([+-]\d\d:\d\d)|Z)?)?)?)?$/i;
    const ISO_8601_FULL = /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?(([+-]\d\d:\d\d)|Z)?$/i;
    if ((!ISO_8601.test(timeRange.start) || !ISO_8601.test(timeRange.end)) && (!ISO_8601_FULL.test(timeRange.start) || !ISO_8601_FULL.test(timeRange.end))) {
      throw new Error("invalid timeRange format, not in ISO8601");
    }
  }
  debug$2(`Fetching calendar objects from ${calendar === null || calendar === undefined ? undefined : calendar.url}`);
  const requiredFields = ["url"];
  if (!calendar || !hasFields(calendar, requiredFields)) {
    if (!calendar) {
      throw new Error("cannot fetchCalendarObjects for undefined calendar");
    }
    throw new Error(`calendar must have ${findMissingFieldNames(calendar, requiredFields)} before fetchCalendarObjects`);
  }
  const filters = customFilters !== null && customFilters !== undefined ? customFilters : [
    {
      "comp-filter": {
        _attributes: {
          name: "VCALENDAR"
        },
        "comp-filter": {
          _attributes: {
            name: "VEVENT"
          },
          ...timeRange ? {
            "time-range": {
              _attributes: {
                start: `${new Date(timeRange.start).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`,
                end: `${new Date(timeRange.end).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`
              }
            }
          } : {}
        }
      }
    }
  ];
  const calendarObjectUrls = (objectUrls !== null && objectUrls !== undefined ? objectUrls : (await calendarQuery({
    url: calendar.url,
    props: {
      [`${DAVNamespaceShort.DAV}:getetag`]: {
        ...expand && timeRange ? {
          [`${DAVNamespaceShort.CALDAV}:expand`]: {
            _attributes: {
              start: `${new Date(timeRange.start).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`,
              end: `${new Date(timeRange.end).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`
            }
          }
        } : {}
      }
    },
    filters,
    depth: "1",
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  })).map((res) => {
    var _a;
    return (_a = res.href) !== null && _a !== undefined ? _a : "";
  })).map((url) => url.startsWith("http") || !url ? url : new URL(url, calendar.url).href).filter(urlFilter).map((url) => new URL(url).pathname);
  let calendarObjectResults = [];
  if (calendarObjectUrls.length > 0) {
    if (!useMultiGet || expand) {
      calendarObjectResults = await calendarQuery({
        url: calendar.url,
        props: {
          [`${DAVNamespaceShort.DAV}:getetag`]: {},
          [`${DAVNamespaceShort.CALDAV}:calendar-data`]: {
            ...expand && timeRange ? {
              [`${DAVNamespaceShort.CALDAV}:expand`]: {
                _attributes: {
                  start: `${new Date(timeRange.start).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`,
                  end: `${new Date(timeRange.end).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`
                }
              }
            } : {}
          }
        },
        filters,
        depth: "1",
        headers: excludeHeaders(headers, headersToExclude),
        fetchOptions
      });
    } else {
      calendarObjectResults = await calendarMultiGet({
        url: calendar.url,
        props: {
          [`${DAVNamespaceShort.DAV}:getetag`]: {},
          [`${DAVNamespaceShort.CALDAV}:calendar-data`]: {
            ...expand && timeRange ? {
              [`${DAVNamespaceShort.CALDAV}:expand`]: {
                _attributes: {
                  start: `${new Date(timeRange.start).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`,
                  end: `${new Date(timeRange.end).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`
                }
              }
            } : {}
          }
        },
        objectUrls: calendarObjectUrls,
        depth: "1",
        headers: excludeHeaders(headers, headersToExclude),
        fetchOptions
      });
    }
  }
  return calendarObjectResults.map((res) => {
    var _a, _b, _c, _d, _e, _f;
    return {
      url: new URL((_a = res.href) !== null && _a !== undefined ? _a : "", calendar.url).href,
      etag: `${(_b = res.props) === null || _b === undefined ? undefined : _b.getetag}`,
      data: (_e = (_d = (_c = res.props) === null || _c === undefined ? undefined : _c.calendarData) === null || _d === undefined ? undefined : _d._cdata) !== null && _e !== undefined ? _e : (_f = res.props) === null || _f === undefined ? undefined : _f.calendarData
    };
  });
};
var createCalendarObject = async (params) => {
  const { calendar, iCalString, filename, headers, headersToExclude, fetchOptions = {} } = params;
  return createObject({
    url: new URL(filename, calendar.url).href,
    data: iCalString,
    headers: excludeHeaders({
      "content-type": "text/calendar; charset=utf-8",
      "If-None-Match": "*",
      ...headers
    }, headersToExclude),
    fetchOptions
  });
};
var updateCalendarObject = async (params) => {
  const { calendarObject, headers, headersToExclude, fetchOptions = {} } = params;
  return updateObject({
    url: calendarObject.url,
    data: calendarObject.data,
    etag: calendarObject.etag,
    headers: excludeHeaders({
      "content-type": "text/calendar; charset=utf-8",
      ...headers
    }, headersToExclude),
    fetchOptions
  });
};
var deleteCalendarObject = async (params) => {
  const { calendarObject, headers, headersToExclude, fetchOptions = {} } = params;
  return deleteObject({
    url: calendarObject.url,
    etag: calendarObject.etag,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
};
var syncCalendars = async (params) => {
  var _a;
  const { oldCalendars, account, detailedResult, headers, headersToExclude, fetchOptions = {} } = params;
  if (!account) {
    throw new Error("Must have account before syncCalendars");
  }
  const localCalendars = (_a = oldCalendars !== null && oldCalendars !== undefined ? oldCalendars : account.calendars) !== null && _a !== undefined ? _a : [];
  const remoteCalendars = await fetchCalendars({
    account,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  const created = remoteCalendars.filter((rc) => localCalendars.every((lc) => !urlContains(lc.url, rc.url)));
  debug$2(`new calendars: ${created.map((cc) => cc.displayName)}`);
  const updated = localCalendars.reduce((prev, curr) => {
    const found = remoteCalendars.find((rc) => urlContains(rc.url, curr.url));
    if (found && (found.syncToken && `${found.syncToken}` !== `${curr.syncToken}` || found.ctag && `${found.ctag}` !== `${curr.ctag}`)) {
      return [...prev, found];
    }
    return prev;
  }, []);
  debug$2(`updated calendars: ${updated.map((cc) => cc.displayName)}`);
  const updatedWithObjects = await Promise.all(updated.map(async (u) => {
    const result = await smartCollectionSync({
      collection: { ...u, objectMultiGet: calendarMultiGet },
      method: "webdav",
      headers: excludeHeaders(headers, headersToExclude),
      account,
      fetchOptions
    });
    return result;
  }));
  const deleted = localCalendars.filter((cal) => remoteCalendars.every((rc) => !urlContains(rc.url, cal.url)));
  debug$2(`deleted calendars: ${deleted.map((cc) => cc.displayName)}`);
  const unchanged = localCalendars.filter((cal) => remoteCalendars.some((rc) => urlContains(rc.url, cal.url) && (rc.syncToken && `${rc.syncToken}` !== `${cal.syncToken}` || rc.ctag && `${rc.ctag}` !== `${cal.ctag}`)));
  return detailedResult ? {
    created,
    updated,
    deleted
  } : [...unchanged, ...created, ...updatedWithObjects];
};
var freeBusyQuery = async (params) => {
  const { url, timeRange, depth, headers, headersToExclude, fetchOptions = {} } = params;
  if (timeRange) {
    const ISO_8601 = /^\d{4}(-\d\d(-\d\d(T\d\d:\d\d(:\d\d)?(\.\d+)?(([+-]\d\d:\d\d)|Z)?)?)?)?$/i;
    const ISO_8601_FULL = /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?(([+-]\d\d:\d\d)|Z)?$/i;
    if ((!ISO_8601.test(timeRange.start) || !ISO_8601.test(timeRange.end)) && (!ISO_8601_FULL.test(timeRange.start) || !ISO_8601_FULL.test(timeRange.end))) {
      throw new Error("invalid timeRange format, not in ISO8601");
    }
  } else {
    throw new Error("timeRange is required");
  }
  const result = await collectionQuery({
    url,
    body: {
      "free-busy-query": cleanupFalsy({
        _attributes: getDAVAttribute([DAVNamespace.CALDAV]),
        [`${DAVNamespaceShort.CALDAV}:time-range`]: {
          _attributes: {
            start: `${new Date(timeRange.start).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`,
            end: `${new Date(timeRange.end).toISOString().slice(0, 19).replace(/[-:.]/g, "")}Z`
          }
        }
      })
    },
    defaultNamespace: DAVNamespaceShort.CALDAV,
    depth,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  return result[0];
};
var calendar = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  calendarMultiGet,
  calendarQuery,
  createCalendarObject,
  deleteCalendarObject,
  fetchCalendarObjects,
  fetchCalendarUserAddresses,
  fetchCalendars,
  freeBusyQuery,
  makeCalendar,
  syncCalendars,
  updateCalendarObject
});
var debug$1 = import_debug.default("tsdav:account");
var serviceDiscovery = async (params) => {
  var _a, _b;
  debug$1("Service discovery...");
  const { account, headers, headersToExclude, fetchOptions = {} } = params;
  const endpoint = new URL(account.serverUrl);
  const uri = new URL(`/.well-known/${account.accountType}`, endpoint);
  uri.protocol = (_a = endpoint.protocol) !== null && _a !== undefined ? _a : "http";
  try {
    const response = await import_cross_fetch.fetch(uri.href, {
      headers: excludeHeaders(headers, headersToExclude),
      method: "PROPFIND",
      redirect: "manual",
      ...fetchOptions
    });
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get("Location");
      if (typeof location === "string" && location.length) {
        debug$1(`Service discovery redirected to ${location}`);
        const serviceURL = new URL(location, endpoint);
        if (serviceURL.hostname === uri.hostname && uri.port && !serviceURL.port) {
          serviceURL.port = uri.port;
        }
        serviceURL.protocol = (_b = endpoint.protocol) !== null && _b !== undefined ? _b : "http";
        return serviceURL.href;
      }
    }
  } catch (err) {
    debug$1(`Service discovery failed: ${err.stack}`);
  }
  return endpoint.href;
};
var fetchPrincipalUrl = async (params) => {
  var _a, _b, _c, _d, _e;
  const { account, headers, headersToExclude, fetchOptions = {} } = params;
  const requiredFields = ["rootUrl"];
  if (!hasFields(account, requiredFields)) {
    throw new Error(`account must have ${findMissingFieldNames(account, requiredFields)} before fetchPrincipalUrl`);
  }
  debug$1(`Fetching principal url from path ${account.rootUrl}`);
  const [response] = await propfind({
    url: account.rootUrl,
    props: {
      [`${DAVNamespaceShort.DAV}:current-user-principal`]: {}
    },
    depth: "0",
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  if (!response.ok) {
    debug$1(`Fetch principal url failed: ${response.statusText}`);
    if (response.status === 401) {
      throw new Error("Invalid credentials");
    }
  }
  debug$1(`Fetched principal url ${(_b = (_a = response.props) === null || _a === undefined ? undefined : _a.currentUserPrincipal) === null || _b === undefined ? undefined : _b.href}`);
  return new URL((_e = (_d = (_c = response.props) === null || _c === undefined ? undefined : _c.currentUserPrincipal) === null || _d === undefined ? undefined : _d.href) !== null && _e !== undefined ? _e : "", account.rootUrl).href;
};
var fetchHomeUrl = async (params) => {
  var _a, _b;
  const { account, headers, headersToExclude, fetchOptions = {} } = params;
  const requiredFields = ["principalUrl", "rootUrl"];
  if (!hasFields(account, requiredFields)) {
    throw new Error(`account must have ${findMissingFieldNames(account, requiredFields)} before fetchHomeUrl`);
  }
  debug$1(`Fetch home url from ${account.principalUrl}`);
  const responses = await propfind({
    url: account.principalUrl,
    props: account.accountType === "caldav" ? { [`${DAVNamespaceShort.CALDAV}:calendar-home-set`]: {} } : { [`${DAVNamespaceShort.CARDDAV}:addressbook-home-set`]: {} },
    depth: "0",
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  const matched = responses.find((r) => urlContains(account.principalUrl, r.href));
  if (!matched || !matched.ok) {
    debug$1(`Fetch home url failed with status ${matched === null || matched === undefined ? undefined : matched.statusText} and error ${JSON.stringify(responses.map((r) => r.error))}`);
    throw new Error("cannot find homeUrl");
  }
  const result = new URL(account.accountType === "caldav" ? (_a = matched === null || matched === undefined ? undefined : matched.props) === null || _a === undefined ? undefined : _a.calendarHomeSet.href : (_b = matched === null || matched === undefined ? undefined : matched.props) === null || _b === undefined ? undefined : _b.addressbookHomeSet.href, account.rootUrl).href;
  debug$1(`Fetched home url ${result}`);
  return result;
};
var createAccount = async (params) => {
  const { account, headers, loadCollections = false, loadObjects = false, headersToExclude, fetchOptions = {} } = params;
  const newAccount = { ...account };
  newAccount.rootUrl = await serviceDiscovery({
    account,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  newAccount.principalUrl = await fetchPrincipalUrl({
    account: newAccount,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  newAccount.homeUrl = await fetchHomeUrl({
    account: newAccount,
    headers: excludeHeaders(headers, headersToExclude),
    fetchOptions
  });
  if (loadCollections || loadObjects) {
    if (account.accountType === "caldav") {
      newAccount.calendars = await fetchCalendars({
        headers: excludeHeaders(headers, headersToExclude),
        account: newAccount,
        fetchOptions
      });
    } else if (account.accountType === "carddav") {
      newAccount.addressBooks = await fetchAddressBooks({
        headers: excludeHeaders(headers, headersToExclude),
        account: newAccount,
        fetchOptions
      });
    }
  }
  if (loadObjects) {
    if (account.accountType === "caldav" && newAccount.calendars) {
      newAccount.calendars = await Promise.all(newAccount.calendars.map(async (cal) => ({
        ...cal,
        objects: await fetchCalendarObjects({
          calendar: cal,
          headers: excludeHeaders(headers, headersToExclude),
          fetchOptions
        })
      })));
    } else if (account.accountType === "carddav" && newAccount.addressBooks) {
      newAccount.addressBooks = await Promise.all(newAccount.addressBooks.map(async (addr) => ({
        ...addr,
        objects: await fetchVCards({
          addressBook: addr,
          headers: excludeHeaders(headers, headersToExclude),
          fetchOptions
        })
      })));
    }
  }
  return newAccount;
};
var account = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  createAccount,
  fetchHomeUrl,
  fetchPrincipalUrl,
  serviceDiscovery
});
var debug = import_debug.default("tsdav:authHelper");
var defaultParam = (fn, params) => (...args) => {
  return fn({ ...params, ...args[0] });
};
var getBasicAuthHeaders = (credentials) => {
  debug(`Basic auth token generated: ${import_base_64.encode(`${credentials.username}:${credentials.password}`)}`);
  return {
    authorization: `Basic ${import_base_64.encode(`${credentials.username}:${credentials.password}`)}`
  };
};
var fetchOauthTokens = async (credentials, fetchOptions) => {
  const requireFields = [
    "authorizationCode",
    "redirectUrl",
    "clientId",
    "clientSecret",
    "tokenUrl"
  ];
  if (!hasFields(credentials, requireFields)) {
    throw new Error(`Oauth credentials missing: ${findMissingFieldNames(credentials, requireFields)}`);
  }
  const param = new URLSearchParams({
    grant_type: "authorization_code",
    code: credentials.authorizationCode,
    redirect_uri: credentials.redirectUrl,
    client_id: credentials.clientId,
    client_secret: credentials.clientSecret
  });
  debug(credentials.tokenUrl);
  debug(param.toString());
  const response = await import_cross_fetch.fetch(credentials.tokenUrl, {
    method: "POST",
    body: param.toString(),
    headers: {
      "content-length": `${param.toString().length}`,
      "content-type": "application/x-www-form-urlencoded"
    },
    ...fetchOptions !== null && fetchOptions !== undefined ? fetchOptions : {}
  });
  if (response.ok) {
    const tokens = await response.json();
    return tokens;
  }
  debug(`Fetch Oauth tokens failed: ${await response.text()}`);
  return {};
};
var refreshAccessToken = async (credentials, fetchOptions) => {
  const requireFields = [
    "refreshToken",
    "clientId",
    "clientSecret",
    "tokenUrl"
  ];
  if (!hasFields(credentials, requireFields)) {
    throw new Error(`Oauth credentials missing: ${findMissingFieldNames(credentials, requireFields)}`);
  }
  const param = new URLSearchParams({
    client_id: credentials.clientId,
    client_secret: credentials.clientSecret,
    refresh_token: credentials.refreshToken,
    grant_type: "refresh_token"
  });
  const response = await import_cross_fetch.fetch(credentials.tokenUrl, {
    method: "POST",
    body: param.toString(),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    ...fetchOptions !== null && fetchOptions !== undefined ? fetchOptions : {}
  });
  if (response.ok) {
    const tokens = await response.json();
    return tokens;
  }
  debug(`Refresh access token failed: ${await response.text()}`);
  return {};
};
var getOauthHeaders = async (credentials, fetchOptions) => {
  var _a;
  debug("Fetching oauth headers");
  let tokens = {};
  if (!credentials.refreshToken) {
    tokens = await fetchOauthTokens(credentials, fetchOptions);
  } else if (credentials.refreshToken && !credentials.accessToken || Date.now() > ((_a = credentials.expiration) !== null && _a !== undefined ? _a : 0)) {
    tokens = await refreshAccessToken(credentials, fetchOptions);
  }
  debug(`Oauth tokens fetched: ${tokens.access_token}`);
  return {
    tokens,
    headers: {
      authorization: `Bearer ${tokens.access_token}`
    }
  };
};
var authHelpers = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  defaultParam,
  fetchOauthTokens,
  getBasicAuthHeaders,
  getOauthHeaders,
  refreshAccessToken
});
var createDAVClient = async (params) => {
  var _a;
  const { serverUrl, credentials, authMethod, defaultAccountType, authFunction } = params;
  let authHeaders = {};
  switch (authMethod) {
    case "Basic":
      authHeaders = getBasicAuthHeaders(credentials);
      break;
    case "Oauth":
      authHeaders = (await getOauthHeaders(credentials)).headers;
      break;
    case "Digest":
      authHeaders = {
        Authorization: `Digest ${credentials.digestString}`
      };
      break;
    case "Custom":
      authHeaders = (_a = await (authFunction === null || authFunction === undefined ? undefined : authFunction(credentials))) !== null && _a !== undefined ? _a : {};
      break;
    default:
      throw new Error("Invalid auth method");
  }
  const defaultAccount = defaultAccountType ? await createAccount({
    account: { serverUrl, credentials, accountType: defaultAccountType },
    headers: authHeaders
  }) : undefined;
  const davRequest$1 = async (params0) => {
    const { init, ...rest } = params0;
    const { headers, ...restInit } = init;
    return davRequest({
      ...rest,
      init: {
        ...restInit,
        headers: {
          ...authHeaders,
          ...headers
        }
      }
    });
  };
  const createObject$1 = defaultParam(createObject, {
    url: serverUrl,
    headers: authHeaders
  });
  const updateObject$1 = defaultParam(updateObject, { headers: authHeaders, url: serverUrl });
  const deleteObject$1 = defaultParam(deleteObject, { headers: authHeaders, url: serverUrl });
  const propfind$1 = defaultParam(propfind, { headers: authHeaders });
  const createAccount$1 = async (params0) => {
    const { account: account2, headers, loadCollections, loadObjects } = params0;
    return createAccount({
      account: { serverUrl, credentials, ...account2 },
      headers: { ...authHeaders, ...headers },
      loadCollections,
      loadObjects
    });
  };
  const collectionQuery$1 = defaultParam(collectionQuery, { headers: authHeaders });
  const makeCollection$1 = defaultParam(makeCollection, { headers: authHeaders });
  const syncCollection$1 = defaultParam(syncCollection, { headers: authHeaders });
  const supportedReportSet$1 = defaultParam(supportedReportSet, {
    headers: authHeaders
  });
  const isCollectionDirty$1 = defaultParam(isCollectionDirty, {
    headers: authHeaders
  });
  const smartCollectionSync$1 = defaultParam(smartCollectionSync, {
    headers: authHeaders,
    account: defaultAccount
  });
  const calendarQuery$1 = defaultParam(calendarQuery, { headers: authHeaders });
  const calendarMultiGet$1 = defaultParam(calendarMultiGet, { headers: authHeaders });
  const makeCalendar$1 = defaultParam(makeCalendar, { headers: authHeaders });
  const fetchCalendars$1 = defaultParam(fetchCalendars, {
    headers: authHeaders,
    account: defaultAccount
  });
  const fetchCalendarUserAddresses$1 = defaultParam(fetchCalendarUserAddresses, {
    headers: authHeaders,
    account: defaultAccount
  });
  const fetchCalendarObjects$1 = defaultParam(fetchCalendarObjects, {
    headers: authHeaders
  });
  const createCalendarObject$1 = defaultParam(createCalendarObject, {
    headers: authHeaders
  });
  const updateCalendarObject$1 = defaultParam(updateCalendarObject, {
    headers: authHeaders
  });
  const deleteCalendarObject$1 = defaultParam(deleteCalendarObject, {
    headers: authHeaders
  });
  const syncCalendars$1 = defaultParam(syncCalendars, {
    account: defaultAccount,
    headers: authHeaders
  });
  const addressBookQuery$1 = defaultParam(addressBookQuery, { headers: authHeaders });
  const addressBookMultiGet$1 = defaultParam(addressBookMultiGet, { headers: authHeaders });
  const fetchAddressBooks$1 = defaultParam(fetchAddressBooks, {
    account: defaultAccount,
    headers: authHeaders
  });
  const fetchVCards$1 = defaultParam(fetchVCards, { headers: authHeaders });
  const createVCard$1 = defaultParam(createVCard, { headers: authHeaders });
  const updateVCard$1 = defaultParam(updateVCard, { headers: authHeaders });
  const deleteVCard$1 = defaultParam(deleteVCard, { headers: authHeaders });
  return {
    davRequest: davRequest$1,
    propfind: propfind$1,
    createAccount: createAccount$1,
    createObject: createObject$1,
    updateObject: updateObject$1,
    deleteObject: deleteObject$1,
    calendarQuery: calendarQuery$1,
    addressBookQuery: addressBookQuery$1,
    collectionQuery: collectionQuery$1,
    makeCollection: makeCollection$1,
    calendarMultiGet: calendarMultiGet$1,
    makeCalendar: makeCalendar$1,
    syncCollection: syncCollection$1,
    supportedReportSet: supportedReportSet$1,
    isCollectionDirty: isCollectionDirty$1,
    smartCollectionSync: smartCollectionSync$1,
    fetchCalendars: fetchCalendars$1,
    fetchCalendarUserAddresses: fetchCalendarUserAddresses$1,
    fetchCalendarObjects: fetchCalendarObjects$1,
    createCalendarObject: createCalendarObject$1,
    updateCalendarObject: updateCalendarObject$1,
    deleteCalendarObject: deleteCalendarObject$1,
    syncCalendars: syncCalendars$1,
    fetchAddressBooks: fetchAddressBooks$1,
    addressBookMultiGet: addressBookMultiGet$1,
    fetchVCards: fetchVCards$1,
    createVCard: createVCard$1,
    updateVCard: updateVCard$1,
    deleteVCard: deleteVCard$1
  };
};

class DAVClient {
  constructor(params) {
    var _a, _b, _c;
    this.serverUrl = params.serverUrl;
    this.credentials = params.credentials;
    this.authMethod = (_a = params.authMethod) !== null && _a !== undefined ? _a : "Basic";
    this.accountType = (_b = params.defaultAccountType) !== null && _b !== undefined ? _b : "caldav";
    this.authFunction = params.authFunction;
    this.fetchOptions = (_c = params.fetchOptions) !== null && _c !== undefined ? _c : {};
  }
  async login() {
    var _a;
    switch (this.authMethod) {
      case "Basic":
        this.authHeaders = getBasicAuthHeaders(this.credentials);
        break;
      case "Oauth":
        this.authHeaders = (await getOauthHeaders(this.credentials, this.fetchOptions)).headers;
        break;
      case "Digest":
        this.authHeaders = {
          Authorization: `Digest ${this.credentials.digestString}`
        };
        break;
      case "Custom":
        this.authHeaders = await ((_a = this.authFunction) === null || _a === undefined ? undefined : _a.call(this, this.credentials));
        break;
      default:
        throw new Error("Invalid auth method");
    }
    this.account = this.accountType ? await createAccount({
      account: {
        serverUrl: this.serverUrl,
        credentials: this.credentials,
        accountType: this.accountType
      },
      headers: this.authHeaders,
      fetchOptions: this.fetchOptions
    }) : undefined;
  }
  async davRequest(params0) {
    const { init, ...rest } = params0;
    const { headers, ...restInit } = init;
    return davRequest({
      ...rest,
      init: {
        ...restInit,
        headers: {
          ...this.authHeaders,
          ...headers
        }
      },
      fetchOptions: this.fetchOptions
    });
  }
  async createObject(...params) {
    return defaultParam(createObject, {
      url: this.serverUrl,
      headers: this.authHeaders,
      fetchOptions: this.fetchOptions
    })(params[0]);
  }
  async updateObject(...params) {
    return defaultParam(updateObject, {
      url: this.serverUrl,
      headers: this.authHeaders,
      fetchOptions: this.fetchOptions
    })(params[0]);
  }
  async deleteObject(...params) {
    return defaultParam(deleteObject, {
      url: this.serverUrl,
      headers: this.authHeaders,
      fetchOptions: this.fetchOptions
    })(params[0]);
  }
  async propfind(...params) {
    return defaultParam(propfind, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async createAccount(params0) {
    const { account: account2, headers, loadCollections, loadObjects, fetchOptions } = params0;
    return createAccount({
      account: { serverUrl: this.serverUrl, credentials: this.credentials, ...account2 },
      headers: { ...this.authHeaders, ...headers },
      loadCollections,
      loadObjects,
      fetchOptions: fetchOptions !== null && fetchOptions !== undefined ? fetchOptions : this.fetchOptions
    });
  }
  async collectionQuery(...params) {
    return defaultParam(collectionQuery, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async makeCollection(...params) {
    return defaultParam(makeCollection, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async syncCollection(...params) {
    return defaultParam(syncCollection, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async supportedReportSet(...params) {
    return defaultParam(supportedReportSet, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async isCollectionDirty(...params) {
    return defaultParam(isCollectionDirty, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async smartCollectionSync(...params) {
    return defaultParam(smartCollectionSync, {
      headers: this.authHeaders,
      fetchOptions: this.fetchOptions,
      account: this.account
    })(params[0]);
  }
  async calendarQuery(...params) {
    return defaultParam(calendarQuery, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async makeCalendar(...params) {
    return defaultParam(makeCalendar, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async calendarMultiGet(...params) {
    return defaultParam(calendarMultiGet, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async fetchCalendars(...params) {
    return defaultParam(fetchCalendars, { headers: this.authHeaders, account: this.account, fetchOptions: this.fetchOptions })(params === null || params === undefined ? undefined : params[0]);
  }
  async fetchCalendarUserAddresses(...params) {
    return defaultParam(fetchCalendarUserAddresses, { headers: this.authHeaders, account: this.account, fetchOptions: this.fetchOptions })(params === null || params === undefined ? undefined : params[0]);
  }
  async fetchCalendarObjects(...params) {
    return defaultParam(fetchCalendarObjects, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async createCalendarObject(...params) {
    return defaultParam(createCalendarObject, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async updateCalendarObject(...params) {
    return defaultParam(updateCalendarObject, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async deleteCalendarObject(...params) {
    return defaultParam(deleteCalendarObject, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async syncCalendars(...params) {
    return defaultParam(syncCalendars, {
      headers: this.authHeaders,
      account: this.account,
      fetchOptions: this.fetchOptions
    })(params[0]);
  }
  async addressBookQuery(...params) {
    return defaultParam(addressBookQuery, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async addressBookMultiGet(...params) {
    return defaultParam(addressBookMultiGet, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async fetchAddressBooks(...params) {
    return defaultParam(fetchAddressBooks, { headers: this.authHeaders, account: this.account, fetchOptions: this.fetchOptions })(params === null || params === undefined ? undefined : params[0]);
  }
  async fetchVCards(...params) {
    return defaultParam(fetchVCards, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async createVCard(...params) {
    return defaultParam(createVCard, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async updateVCard(...params) {
    return defaultParam(updateVCard, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
  async deleteVCard(...params) {
    return defaultParam(deleteVCard, { headers: this.authHeaders, fetchOptions: this.fetchOptions })(params[0]);
  }
}
var client = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  DAVClient,
  createDAVClient
});
var index = {
  DAVNamespace,
  DAVNamespaceShort,
  DAVAttributeMap,
  ...client,
  ...request,
  ...collection,
  ...account,
  ...addressBook,
  ...calendar,
  ...authHelpers,
  ...requestHelpers
};

// scripts/caldav-client.ts
var CALDAV_SERVER = "https://caldav.fastmail.com";

class CalDAVClient {
  username;
  password;
  client = null;
  calendars = null;
  constructor(username, password) {
    this.username = username;
    this.password = password;
  }
  async connect() {
    if (this.client)
      return;
    this.client = await createDAVClient({
      serverUrl: CALDAV_SERVER,
      credentials: {
        username: this.username,
        password: this.password
      },
      authMethod: "Basic",
      defaultAccountType: "caldav"
    });
    console.error("✅ Connected to Fastmail CalDAV");
  }
  async getCalendars() {
    await this.connect();
    if (!this.calendars) {
      this.calendars = await this.client.fetchCalendars();
    }
    return this.calendars;
  }
  async getCalendarById(calendarId) {
    const calendars = await this.getCalendars();
    return calendars.find((cal) => cal.url === calendarId || cal.displayName === calendarId);
  }
  async fetchCalendarObjects(calendar2, timeRange) {
    await this.connect();
    return await this.client.fetchCalendarObjects({
      calendar: calendar2,
      timeRange: timeRange || {
        start: new Date().toISOString(),
        end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
      }
    });
  }
  async createEvent(calendar2, icsData, eventId) {
    await this.connect();
    const eventUrl = `${calendar2.url}${eventId}.ics`;
    await this.client.createCalendarObject({
      calendar: calendar2,
      filename: `${eventId}.ics`,
      iCalString: icsData
    });
  }
  async updateEvent(calendar2, event, icsData) {
    await this.connect();
    await this.client.updateCalendarObject({
      calendarObject: {
        ...event,
        data: icsData
      }
    });
  }
  async deleteEvent(event) {
    await this.connect();
    await this.client.deleteCalendarObject({
      calendarObject: event
    });
  }
  getClient() {
    if (!this.client) {
      throw new Error("CalDAV client not connected. Call connect() first.");
    }
    return this.client;
  }
}

// node_modules/uuid/dist/stringify.js
var byteToHex = [];
for (let i2 = 0;i2 < 256; ++i2) {
  byteToHex.push((i2 + 256).toString(16).slice(1));
}
function unsafeStringify(arr, offset = 0) {
  return (byteToHex[arr[offset + 0]] + byteToHex[arr[offset + 1]] + byteToHex[arr[offset + 2]] + byteToHex[arr[offset + 3]] + "-" + byteToHex[arr[offset + 4]] + byteToHex[arr[offset + 5]] + "-" + byteToHex[arr[offset + 6]] + byteToHex[arr[offset + 7]] + "-" + byteToHex[arr[offset + 8]] + byteToHex[arr[offset + 9]] + "-" + byteToHex[arr[offset + 10]] + byteToHex[arr[offset + 11]] + byteToHex[arr[offset + 12]] + byteToHex[arr[offset + 13]] + byteToHex[arr[offset + 14]] + byteToHex[arr[offset + 15]]).toLowerCase();
}

// node_modules/uuid/dist/rng.js
var getRandomValues;
var rnds8 = new Uint8Array(16);
function rng() {
  if (!getRandomValues) {
    if (typeof crypto === "undefined" || !crypto.getRandomValues) {
      throw new Error("crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported");
    }
    getRandomValues = crypto.getRandomValues.bind(crypto);
  }
  return getRandomValues(rnds8);
}

// node_modules/uuid/dist/native.js
var randomUUID = typeof crypto !== "undefined" && crypto.randomUUID && crypto.randomUUID.bind(crypto);
var native_default = { randomUUID };

// node_modules/uuid/dist/v4.js
function _v4(options, buf, offset) {
  options = options || {};
  const rnds = options.random ?? options.rng?.() ?? rng();
  if (rnds.length < 16) {
    throw new Error("Random bytes length must be >= 16");
  }
  rnds[6] = rnds[6] & 15 | 64;
  rnds[8] = rnds[8] & 63 | 128;
  if (buf) {
    offset = offset || 0;
    if (offset < 0 || offset + 16 > buf.length) {
      throw new RangeError(`UUID byte range ${offset}:${offset + 15} is out of buffer bounds`);
    }
    for (let i2 = 0;i2 < 16; ++i2) {
      buf[offset + i2] = rnds[i2];
    }
    return buf;
  }
  return unsafeStringify(rnds);
}
function v4(options, buf, offset) {
  if (native_default.randomUUID && !buf && !options) {
    return native_default.randomUUID();
  }
  return _v4(options, buf, offset);
}
var v4_default = v4;
// scripts/tools/calendar.ts
class CalendarTools {
  client;
  constructor(client2) {
    this.client = client2;
  }
  toUTC(localDate) {
    let dateStr = localDate;
    if (dateStr.includes("+07:00")) {
      dateStr = dateStr.replace("+07:00", "");
    } else if (dateStr.includes("+0700")) {
      dateStr = dateStr.replace("+0700", "");
    }
    const [datePart, timePart] = dateStr.split("T");
    const [year, month, day] = datePart.split("-").map(Number);
    const [hour, minute, second] = (timePart || "00:00:00").split(":").map(Number);
    const utc7Date = new Date(Date.UTC(year, month - 1, day, hour, minute, second || 0));
    const utcDate = new Date(utc7Date.getTime() - 7 * 60 * 60 * 1000);
    return utcDate.toISOString();
  }
  formatICalDate(date, isAllDay = false) {
    if (isAllDay) {
      return date.toISOString().split("T")[0].replace(/-/g, "");
    }
    return date.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
  }
  parseICalDate(icalDate, isAllDay = false) {
    if (isAllDay) {
      const year2 = icalDate.slice(0, 4);
      const month2 = icalDate.slice(4, 6);
      const day2 = icalDate.slice(6, 8);
      return `${year2}-${month2}-${day2}`;
    }
    const year = icalDate.slice(0, 4);
    const month = icalDate.slice(4, 6);
    const day = icalDate.slice(6, 8);
    const hour = icalDate.slice(9, 11);
    const minute = icalDate.slice(11, 13);
    const second = icalDate.slice(13, 15);
    const utcDate = new Date(`${year}-${month}-${day}T${hour}:${minute}:${second}Z`);
    const utc7Date = new Date(utcDate.getTime() + 7 * 60 * 60 * 1000);
    return utc7Date.toISOString().replace("Z", "+07:00");
  }
  parseDurationToMinutes(duration) {
    const isNegative = duration.startsWith("-");
    const cleanDuration = duration.replace(/^-/, "");
    let minutes = 0;
    const dayMatch = cleanDuration.match(/P(\d+)D/);
    if (dayMatch) {
      minutes += parseInt(dayMatch[1]) * 24 * 60;
    }
    const hourMatch = cleanDuration.match(/(\d+)H/);
    if (hourMatch) {
      minutes += parseInt(hourMatch[1]) * 60;
    }
    const minMatch = cleanDuration.match(/(\d+)M/);
    if (minMatch) {
      minutes += parseInt(minMatch[1]);
    }
    return isNegative ? minutes : -minutes;
  }
  buildTrigger(options) {
    let totalMinutes = 0;
    if (options.daysBefore) {
      totalMinutes += options.daysBefore * 24 * 60;
    }
    if (options.hoursBefore) {
      totalMinutes += options.hoursBefore * 60;
    }
    if (options.minutesBefore) {
      totalMinutes += options.minutesBefore;
    }
    if (totalMinutes === 0) {
      totalMinutes = 15;
    }
    const days = Math.floor(totalMinutes / (24 * 60));
    const hours = Math.floor(totalMinutes % (24 * 60) / 60);
    const minutes = totalMinutes % 60;
    let trigger = "-P";
    if (days > 0) {
      trigger += `${days}D`;
    }
    if (hours > 0 || minutes > 0) {
      trigger += "T";
      if (hours > 0)
        trigger += `${hours}H`;
      if (minutes > 0)
        trigger += `${minutes}M`;
    }
    return trigger;
  }
  buildVAlarm(reminder, reminderId) {
    const trigger = this.buildTrigger(reminder);
    const action = (reminder.action || "display").toUpperCase();
    const description = reminder.description || "Event reminder";
    return `BEGIN:VALARM
ACTION:${action}
TRIGGER:${trigger}
DESCRIPTION:${description}
X-WR-ALARMUID:${reminderId}
END:VALARM`;
  }
  parseVAlarms(icsData) {
    const reminders = [];
    const alarmRegex = /BEGIN:VALARM[\s\S]*?END:VALARM/g;
    const alarms = icsData.match(alarmRegex) || [];
    for (const alarm of alarms) {
      const lines = alarm.split(`
`);
      let reminder = {};
      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith("TRIGGER:")) {
          reminder.trigger = trimmed.slice(8);
          reminder.minutesBefore = this.parseDurationToMinutes(reminder.trigger);
        } else if (trimmed.startsWith("ACTION:")) {
          reminder.action = trimmed.slice(7).toLowerCase();
        } else if (trimmed.startsWith("DESCRIPTION:")) {
          reminder.description = trimmed.slice(12);
        } else if (trimmed.startsWith("X-WR-ALARMUID:")) {
          reminder.id = trimmed.slice(14);
        }
      }
      if (!reminder.id) {
        reminder.id = v4_default();
      }
      if (reminder.trigger) {
        reminders.push(reminder);
      }
    }
    return reminders;
  }
  parseEventData(icsData, calendarId, url, etag) {
    const lines = icsData.split(`
`);
    let event = { calendarId, url, etag };
    let inEvent = false;
    let isAllDay = false;
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed === "BEGIN:VEVENT") {
        inEvent = true;
        continue;
      }
      if (trimmed === "END:VEVENT") {
        break;
      }
      if (!inEvent)
        continue;
      if (trimmed.startsWith("UID:")) {
        event.id = trimmed.slice(4);
      } else if (trimmed.startsWith("SUMMARY:")) {
        event.title = trimmed.slice(8);
      } else if (trimmed.startsWith("DESCRIPTION:")) {
        event.description = trimmed.slice(12);
      } else if (trimmed.startsWith("LOCATION:")) {
        event.location = trimmed.slice(9);
      } else if (trimmed.startsWith("DTSTART;VALUE=DATE:")) {
        isAllDay = true;
        const dateStr = trimmed.slice(19);
        event.start = this.parseICalDate(dateStr, true);
      } else if (trimmed.startsWith("DTSTART:")) {
        const dateStr = trimmed.slice(8);
        event.start = this.parseICalDate(dateStr, false);
      } else if (trimmed.startsWith("DTEND;VALUE=DATE:")) {
        const dateStr = trimmed.slice(17);
        event.end = this.parseICalDate(dateStr, true);
      } else if (trimmed.startsWith("DTEND:")) {
        const dateStr = trimmed.slice(6);
        event.end = this.parseICalDate(dateStr, false);
      } else if (trimmed.startsWith("RRULE:")) {
        event.recurrence = trimmed.slice(6);
      }
    }
    event.isAllDay = isAllDay;
    event.reminders = this.parseVAlarms(icsData);
    return event;
  }
  buildICalEvent(event, eventId, recurrence, reminders) {
    const startUTC = this.toUTC(event.start);
    const endUTC = this.toUTC(event.end);
    const startDate = new Date(startUTC);
    const endDate = new Date(endUTC);
    let icsData = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Fastmail MCP Server//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:${eventId}
`;
    if (event.allDay) {
      icsData += `DTSTART;VALUE=DATE:${this.formatICalDate(startDate, true)}
DTEND;VALUE=DATE:${this.formatICalDate(endDate, true)}
`;
    } else {
      icsData += `DTSTART:${this.formatICalDate(startDate)}
DTEND:${this.formatICalDate(endDate)}
`;
    }
    icsData += `SUMMARY:${event.title}
`;
    if (event.description) {
      icsData += `DESCRIPTION:${event.description}
`;
    }
    if (event.location) {
      icsData += `LOCATION:${event.location}
`;
    }
    if (recurrence) {
      icsData += `RRULE:${recurrence}
`;
    }
    if (event.attendees && event.attendees.length > 0) {
      for (const attendee of event.attendees) {
        const attendeeStr = attendee.name ? `CN="${attendee.name}":mailto:${attendee.email}` : `mailto:${attendee.email}`;
        icsData += `ATTENDEE;${attendeeStr}
`;
      }
    }
    const alarmsToAdd = reminders || event.reminders || [];
    for (const reminder of alarmsToAdd) {
      const reminderId = v4_default();
      icsData += this.buildVAlarm(reminder, reminderId) + `
`;
    }
    icsData += `STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
END:VCALENDAR`;
    return icsData;
  }
  async listCalendars() {
    const calendars = await this.client.getCalendars();
    return calendars.map((cal) => ({
      id: cal.url,
      name: typeof cal.displayName === "string" ? cal.displayName : "Unnamed Calendar",
      description: cal.description,
      color: cal.calendarColor,
      timezone: cal.timezone
    }));
  }
  async listEvents(calendarId, startDate, endDate) {
    const calendars = await this.client.getCalendars();
    let targetCalendars;
    if (calendarId) {
      const cal = calendars.find((c) => c.url === calendarId || c.displayName === calendarId);
      if (!cal)
        throw new Error(`Calendar not found: ${calendarId}`);
      targetCalendars = [cal];
    } else {
      targetCalendars = calendars;
    }
    let effectiveStartDate = startDate;
    let effectiveEndDate = endDate;
    if (startDate) {
      if (!startDate.includes("T")) {
        effectiveStartDate = `${startDate}T00:00:00`;
      }
    }
    if (endDate) {
      if (!endDate.includes("T")) {
        effectiveEndDate = `${endDate}T23:59:59`;
      }
    } else if (startDate && !endDate) {
      const datePart = startDate.split("T")[0];
      effectiveEndDate = `${datePart}T23:59:59`;
    }
    const timeRange = {
      start: effectiveStartDate ? this.toUTC(effectiveStartDate) : new Date().toISOString(),
      end: effectiveEndDate ? this.toUTC(effectiveEndDate) : new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
    };
    const allEvents = [];
    for (const calendar2 of targetCalendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar2, timeRange);
        for (const obj of objects) {
          if (obj.data && obj.url && obj.etag) {
            const event = this.parseEventData(obj.data, calendar2.url, obj.url, obj.etag);
            allEvents.push(event);
          }
        }
      } catch (error) {
        console.error(`Error fetching events from ${calendar2.displayName}:`, error);
      }
    }
    return allEvents.sort((a, b) => new Date(a.start).getTime() - new Date(b.start).getTime());
  }
  async getEvent(eventId) {
    const calendars = await this.client.getCalendars();
    for (const calendar2 of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar2);
        for (const obj of objects) {
          if (obj.url?.includes(eventId) && obj.data && obj.etag) {
            return this.parseEventData(obj.data, calendar2.url, obj.url, obj.etag);
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar2.displayName}:`, error);
      }
    }
    throw new Error(`Event not found: ${eventId}`);
  }
  async createEvent(calendarId, options) {
    const calendars = await this.client.getCalendars();
    let calendar2;
    if (calendarId) {
      const cal = calendars.find((c) => c.url === calendarId || c.displayName === calendarId);
      if (!cal)
        throw new Error(`Calendar not found: ${calendarId}`);
      calendar2 = cal;
    } else {
      calendar2 = calendars.find((c) => c.displayName && !c.displayName.toLowerCase().includes("task") && !c.displayName.toLowerCase().includes("default")) || calendars[0];
      if (!calendar2)
        throw new Error("No calendars found");
    }
    const eventId = v4_default();
    const icsData = this.buildICalEvent(options, eventId);
    await this.client.createEvent(calendar2, icsData, eventId);
    return { id: eventId };
  }
  async updateEvent(eventId, updates) {
    const calendars = await this.client.getCalendars();
    for (const calendar2 of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar2);
        for (const obj of objects) {
          if (obj.url?.includes(eventId) && obj.data && obj.etag) {
            const existing = this.parseEventData(obj.data, calendar2.url, obj.url, obj.etag);
            const updated = {
              title: updates.title || existing.title,
              start: updates.start || existing.start,
              end: updates.end || existing.end,
              description: updates.description !== undefined ? updates.description : existing.description,
              location: updates.location !== undefined ? updates.location : existing.location,
              allDay: updates.allDay !== undefined ? updates.allDay : existing.isAllDay,
              attendees: updates.attendees || existing.attendees
            };
            const icsData = this.buildICalEvent(updated, eventId, existing.recurrence);
            await this.client.updateEvent(calendar2, obj, icsData);
            return;
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar2.displayName}:`, error);
      }
    }
    throw new Error(`Event not found: ${eventId}`);
  }
  async deleteEvent(eventId) {
    const calendars = await this.client.getCalendars();
    for (const calendar2 of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar2);
        for (const obj of objects) {
          if (obj.url?.includes(eventId)) {
            await this.client.deleteEvent(obj);
            return;
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar2.displayName}:`, error);
      }
    }
    throw new Error(`Event not found: ${eventId}`);
  }
  async searchEvents(query, startDate, endDate) {
    const events = await this.listEvents(undefined, startDate, endDate);
    const lowerQuery = query.toLowerCase();
    return events.filter((event) => event.title.toLowerCase().includes(lowerQuery) || event.description && event.description.toLowerCase().includes(lowerQuery) || event.location && event.location.toLowerCase().includes(lowerQuery));
  }
  async createRecurringEvent(calendarId, options) {
    const calendars = await this.client.getCalendars();
    let calendar2;
    if (calendarId) {
      const cal = calendars.find((c) => c.url === calendarId || c.displayName === calendarId);
      if (!cal)
        throw new Error(`Calendar not found: ${calendarId}`);
      calendar2 = cal;
    } else {
      calendar2 = calendars[0];
      if (!calendar2)
        throw new Error("No calendars found");
    }
    let rrule = `FREQ=${options.recurrence.toUpperCase()}`;
    if (options.recurrenceCount) {
      rrule += `;COUNT=${options.recurrenceCount}`;
    } else if (options.recurrenceUntil) {
      const untilUTC = this.toUTC(options.recurrenceUntil + "T23:59:59");
      const untilDate = new Date(untilUTC);
      rrule += `;UNTIL=${this.formatICalDate(untilDate)}`;
    }
    const eventId = v4_default();
    const icsData = this.buildICalEvent(options, eventId, rrule);
    await this.client.createEvent(calendar2, icsData, eventId);
    return { id: eventId };
  }
  async addReminder(eventId, options) {
    const calendars = await this.client.getCalendars();
    for (const calendar2 of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar2);
        for (const obj of objects) {
          if (obj.url?.includes(eventId) && obj.data && obj.etag) {
            const existing = this.parseEventData(obj.data, calendar2.url, obj.url, obj.etag);
            const existingReminders = existing.reminders?.map((r) => ({
              minutesBefore: r.minutesBefore,
              action: r.action,
              description: r.description
            })) || [];
            const allReminders = [...existingReminders, options];
            const updated = {
              title: existing.title,
              start: existing.start,
              end: existing.end,
              description: existing.description,
              location: existing.location,
              allDay: existing.isAllDay,
              attendees: existing.attendees
            };
            const icsData = this.buildICalEvent(updated, eventId, existing.recurrence, allReminders);
            await this.client.updateEvent(calendar2, obj, icsData);
            const newReminderId = v4_default();
            return { id: newReminderId };
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar2.displayName}:`, error);
      }
    }
    throw new Error(`Event not found: ${eventId}`);
  }
  async removeReminder(eventId, reminderId) {
    const calendars = await this.client.getCalendars();
    for (const calendar2 of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar2);
        for (const obj of objects) {
          if (obj.url?.includes(eventId) && obj.data && obj.etag) {
            const existing = this.parseEventData(obj.data, calendar2.url, obj.url, obj.etag);
            let remainingReminders = [];
            if (reminderId && existing.reminders) {
              remainingReminders = existing.reminders.filter((r) => r.id !== reminderId).map((r) => ({
                minutesBefore: r.minutesBefore,
                action: r.action,
                description: r.description
              }));
            }
            const updated = {
              title: existing.title,
              start: existing.start,
              end: existing.end,
              description: existing.description,
              location: existing.location,
              allDay: existing.isAllDay,
              attendees: existing.attendees
            };
            const icsData = this.buildICalEvent(updated, eventId, existing.recurrence, remainingReminders);
            await this.client.updateEvent(calendar2, obj, icsData);
            return;
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar2.displayName}:`, error);
      }
    }
    throw new Error(`Event not found: ${eventId}`);
  }
  async listReminders(eventId) {
    const event = await this.getEvent(eventId);
    return event.reminders || [];
  }
  parseOrganizer(icsData) {
    const match = icsData.match(/ORGANIZER(?:;CN="?([^":]*)"?)?:mailto:([^\r\n]+)/i);
    if (match) {
      return {
        name: match[1] || undefined,
        email: match[2]
      };
    }
    return null;
  }
  parseMyAttendeeStatus(icsData) {
    const attendeeMatch = icsData.match(/ATTENDEE[^:]*PARTSTAT=([^;:\r\n]+)/i);
    if (attendeeMatch) {
      const status = attendeeMatch[1].toLowerCase();
      if (status === "accepted" || status === "declined" || status === "tentative" || status === "needs-action") {
        return status;
      }
    }
    return "needs-action";
  }
  async listInvitations() {
    const calendars = await this.client.getCalendars();
    const invitations = [];
    for (const calendar2 of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar2);
        for (const obj of objects) {
          if (obj.data) {
            const hasOrganizer = obj.data.includes("ORGANIZER");
            const hasAttendee = obj.data.includes("ATTENDEE");
            if (hasOrganizer && hasAttendee) {
              const event = this.parseEventData(obj.data, calendar2.url, obj.url || "", obj.etag || "");
              const organizer = this.parseOrganizer(obj.data);
              const myStatus = this.parseMyAttendeeStatus(obj.data);
              if (organizer && myStatus) {
                invitations.push({
                  eventId: event.id,
                  calendarId: calendar2.url,
                  title: event.title,
                  organizer,
                  start: event.start,
                  end: event.end,
                  description: event.description,
                  location: event.location,
                  myStatus
                });
              }
            }
          }
        }
      } catch (error) {
        console.error(`Error fetching invitations from ${calendar2.displayName}:`, error);
      }
    }
    return invitations;
  }
  async respondToInvitation(eventId, response) {
    const calendars = await this.client.getCalendars();
    const partstatMap = {
      accept: "ACCEPTED",
      decline: "DECLINED",
      tentative: "TENTATIVE"
    };
    const newPartstat = partstatMap[response];
    for (const calendar2 of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar2);
        for (const obj of objects) {
          if (obj.url?.includes(eventId) && obj.data && obj.etag) {
            let updatedIcs = obj.data;
            updatedIcs = updatedIcs.replace(/ATTENDEE([^:]*?)PARTSTAT=[^;:\r\n]+/gi, `ATTENDEE$1PARTSTAT=${newPartstat}`);
            if (!updatedIcs.includes(`PARTSTAT=${newPartstat}`)) {
              updatedIcs = updatedIcs.replace(/ATTENDEE([^:]*):mailto:/gi, `ATTENDEE$1;PARTSTAT=${newPartstat}:mailto:`);
            }
            await this.client.updateEvent(calendar2, obj, updatedIcs);
            return;
          }
        }
      } catch (error) {
        console.error(`Error in ${calendar2.displayName}:`, error);
      }
    }
    throw new NotFoundError("event", eventId);
  }
}

// scripts/errors.ts
class FastmailError2 extends Error {
  code;
  suggestion;
  details;
  constructor(message, code2, suggestion, details) {
    super(message);
    this.name = "FastmailError";
    this.code = code2;
    this.suggestion = suggestion;
    this.details = details;
  }
  toJSON() {
    return {
      error: this.message,
      code: this.code,
      suggestion: this.suggestion,
      details: this.details
    };
  }
}

class AuthenticationError extends FastmailError2 {
  constructor(type, originalError) {
    const messages = {
      email: {
        message: "Failed to authenticate with Fastmail email API",
        suggestion: "Check your FASTMAIL_API_TOKEN environment variable. Generate a new token at Fastmail Settings → Privacy & Security → Integrations → API tokens"
      },
      calendar: {
        message: "Failed to authenticate with Fastmail calendar",
        suggestion: "Check your FASTMAIL_USERNAME and FASTMAIL_PASSWORD environment variables. Use an app password, not your main password. Generate at Fastmail Settings → Privacy & Security → Integrations → App passwords"
      }
    };
    super(messages[type].message, "AUTH_ERROR", messages[type].suggestion, { originalError });
    this.name = "AuthenticationError";
  }
}

class ConfigurationError extends FastmailError2 {
  constructor(missingVars) {
    const varList = missingVars.join(", ");
    super(`Missing required environment variable(s): ${varList}`, "CONFIG_ERROR", missingVars.includes("FASTMAIL_API_TOKEN") ? "Set FASTMAIL_API_TOKEN for email operations. Get your token from Fastmail Settings → Privacy & Security → Integrations" : "Set FASTMAIL_USERNAME and FASTMAIL_PASSWORD for calendar operations. Create an app password at Fastmail Settings → Privacy & Security → Integrations");
    this.name = "ConfigurationError";
  }
}
function formatError(error) {
  if (error instanceof FastmailError2) {
    return {
      success: false,
      error: error.message,
      code: error.code,
      suggestion: error.suggestion,
      details: error.details
    };
  }
  if (error instanceof Error) {
    const message = error.message;
    if (message.includes("401") || message.includes("Unauthorized")) {
      return formatError(new AuthenticationError("email", message));
    }
    if (message.includes("FASTMAIL_API_TOKEN")) {
      return formatError(new ConfigurationError(["FASTMAIL_API_TOKEN"]));
    }
    if (message.includes("FASTMAIL_USERNAME") || message.includes("FASTMAIL_PASSWORD")) {
      return formatError(new ConfigurationError(["FASTMAIL_USERNAME", "FASTMAIL_PASSWORD"]));
    }
    return {
      success: false,
      error: message,
      suggestion: "If this error persists, check your environment variables and network connection"
    };
  }
  return {
    success: false,
    error: String(error)
  };
}

// scripts/cli.ts
var jmapClient = null;
var emailTools = null;
var caldavClient = null;
var calendarTools = null;
function getEmailTools() {
  if (!emailTools) {
    const token = process.env.FASTMAIL_API_TOKEN;
    if (!token) {
      throw new Error("FASTMAIL_API_TOKEN environment variable is required");
    }
    jmapClient = new JMAPClient(token);
    emailTools = new EmailTools(jmapClient);
  }
  return emailTools;
}
function getCalendarTools() {
  if (!calendarTools) {
    const username = process.env.FASTMAIL_USERNAME;
    const password = process.env.FASTMAIL_PASSWORD;
    if (!username || !password) {
      throw new Error("FASTMAIL_USERNAME and FASTMAIL_PASSWORD environment variables are required");
    }
    caldavClient = new CalDAVClient(username, password);
    calendarTools = new CalendarTools(caldavClient);
  }
  return calendarTools;
}
async function handleTool(toolName, args) {
  try {
    let normalizedToolName = toolName;
    if (!toolName.startsWith("fastmail_")) {
      normalizedToolName = `fastmail_${toolName}`;
    }
    switch (normalizedToolName) {
      case "fastmail_list_mailboxes": {
        const email = getEmailTools();
        const result = await email.getMailboxes();
        return { success: true, result };
      }
      case "fastmail_list_emails": {
        const email = getEmailTools();
        const mailboxId = args.mailbox_id;
        const limit = args.limit || 20;
        const result = await email.listEmails(mailboxId, limit);
        return { success: true, result };
      }
      case "fastmail_get_email": {
        const email = getEmailTools();
        const emailId = args.email_id;
        if (!emailId)
          throw new Error("email_id is required");
        const result = await email.getEmail(emailId);
        return { success: true, result };
      }
      case "fastmail_search_emails": {
        const email = getEmailTools();
        const query = args.query;
        if (!query)
          throw new Error("query is required");
        const limit = args.limit || 20;
        const result = await email.searchEmails(query, limit);
        return { success: true, result };
      }
      case "fastmail_send_email": {
        const email = getEmailTools();
        const to = args.to;
        const subject = args.subject;
        const textBody = args.text_body;
        const htmlBody = args.html_body;
        const cc = args.cc;
        const bcc = args.bcc;
        const inReplyTo = args.in_reply_to;
        const references = args.references;
        if (!to || !subject || !textBody) {
          throw new Error("to, subject, and text_body are required");
        }
        const result = await email.sendEmail({
          to,
          cc,
          bcc,
          subject,
          textBody,
          htmlBody,
          inReplyTo,
          references
        });
        return { success: true, result };
      }
      case "fastmail_move_email": {
        const email = getEmailTools();
        const emailId = args.email_id;
        const targetMailboxId = args.target_mailbox_id;
        const sourceMailboxId = args.source_mailbox_id;
        if (!emailId || !targetMailboxId) {
          throw new Error("email_id and target_mailbox_id are required");
        }
        await email.moveToFolder(emailId, targetMailboxId, sourceMailboxId);
        return { success: true, result: { message: "Email moved" } };
      }
      case "fastmail_set_labels": {
        const email = getEmailTools();
        const emailId = args.email_id;
        const keywords = args.keywords;
        if (!emailId || !keywords) {
          throw new Error("email_id and keywords are required");
        }
        await email.setKeywords(emailId, keywords);
        return { success: true, result: { message: "Labels set" } };
      }
      case "fastmail_delete_email": {
        const email = getEmailTools();
        const emailId = args.email_id;
        if (!emailId)
          throw new Error("email_id is required");
        await email.deleteEmail(emailId);
        return { success: true, result: { message: "Email deleted" } };
      }
      case "fastmail_reply_email": {
        const email = getEmailTools();
        const emailId = args.email_id;
        const textBody = args.text_body;
        const htmlBody = args.html_body;
        const subject = args.subject;
        const cc = args.cc;
        const bcc = args.bcc;
        const replyAll = args.reply_all;
        if (!emailId || !textBody) {
          throw new Error("email_id and text_body are required");
        }
        const originalEmail = await email.getEmail(emailId);
        const from2 = originalEmail.from?.[0];
        if (!from2) {
          throw new Error("Could not find sender information in original email");
        }
        const to = [from2];
        const inReplyTo = emailId;
        let additionalTo = [];
        if (replyAll) {
          if (originalEmail.to)
            additionalTo.push(...originalEmail.to);
          if (originalEmail.cc)
            additionalTo.push(...originalEmail.cc);
        }
        const result = await email.sendEmail({
          to: [...to, ...additionalTo],
          cc,
          bcc,
          subject: subject || `Re: ${originalEmail.subject}`,
          textBody,
          htmlBody,
          inReplyTo
        });
        return { success: true, result };
      }
      case "fastmail_list_calendars": {
        const calendar2 = getCalendarTools();
        const result = await calendar2.listCalendars();
        return { success: true, result };
      }
      case "fastmail_list_events": {
        const calendar2 = getCalendarTools();
        const calendarId = args.calendar_id;
        const startDate = args.start_date;
        const endDate = args.end_date;
        const result = await calendar2.listEvents(calendarId, startDate, endDate);
        return { success: true, result };
      }
      case "fastmail_get_event": {
        const calendar2 = getCalendarTools();
        const eventId = args.event_id;
        if (!eventId)
          throw new Error("event_id is required");
        const result = await calendar2.getEvent(eventId);
        return { success: true, result };
      }
      case "fastmail_create_event": {
        const calendar2 = getCalendarTools();
        const calendarId = args.calendar_id;
        const title = args.title;
        const start = args.start;
        const end = args.end;
        const description = args.description;
        const location = args.location;
        const allDay = args.all_day;
        const attendees = args.attendees;
        const reminders = args.reminders;
        if (!title || !start || !end) {
          throw new Error("title, start, and end are required");
        }
        const result = await calendar2.createEvent(calendarId, {
          title,
          start,
          end,
          description,
          location,
          allDay,
          attendees,
          reminders
        });
        return { success: true, result };
      }
      case "fastmail_update_event": {
        const calendar2 = getCalendarTools();
        const eventId = args.event_id;
        const title = args.title;
        const start = args.start;
        const end = args.end;
        const description = args.description;
        const location = args.location;
        const allDay = args.all_day;
        const attendees = args.attendees;
        if (!eventId)
          throw new Error("event_id is required");
        const updates = {};
        if (title !== undefined)
          updates.title = title;
        if (start !== undefined)
          updates.start = start;
        if (end !== undefined)
          updates.end = end;
        if (description !== undefined)
          updates.description = description;
        if (location !== undefined)
          updates.location = location;
        if (allDay !== undefined)
          updates.allDay = allDay;
        if (attendees !== undefined)
          updates.attendees = attendees;
        await calendar2.updateEvent(eventId, updates);
        return { success: true, result: { message: "Event updated" } };
      }
      case "fastmail_delete_event": {
        const calendar2 = getCalendarTools();
        const eventId = args.event_id;
        if (!eventId)
          throw new Error("event_id is required");
        await calendar2.deleteEvent(eventId);
        return { success: true, result: { message: "Event deleted" } };
      }
      case "fastmail_search_events": {
        const calendar2 = getCalendarTools();
        const query = args.query;
        const startDate = args.start_date;
        const endDate = args.end_date;
        if (!query)
          throw new Error("query is required");
        const result = await calendar2.searchEvents(query, startDate, endDate);
        return { success: true, result };
      }
      case "fastmail_create_recurring_event": {
        const calendar2 = getCalendarTools();
        const calendarId = args.calendar_id;
        const title = args.title;
        const start = args.start;
        const end = args.end;
        const recurrence = args.recurrence;
        const description = args.description;
        const location = args.location;
        const allDay = args.all_day;
        const attendees = args.attendees;
        const recurrenceCount = args.recurrence_count;
        const recurrenceUntil = args.recurrence_until;
        const reminders = args.reminders;
        if (!title || !start || !end || !recurrence) {
          throw new Error("title, start, end, and recurrence are required");
        }
        const result = await calendar2.createRecurringEvent(calendarId, {
          title,
          start,
          end,
          recurrence,
          description,
          location,
          allDay,
          attendees,
          recurrenceCount,
          recurrenceUntil,
          reminders
        });
        return { success: true, result };
      }
      case "fastmail_add_event_reminder": {
        const calendar2 = getCalendarTools();
        const eventId = args.event_id;
        const minutesBefore = args.minutes_before;
        const hoursBefore = args.hours_before;
        const daysBefore = args.days_before;
        const action = args.action;
        const description = args.description;
        if (!eventId)
          throw new Error("event_id is required");
        const result = await calendar2.addReminder(eventId, {
          minutesBefore,
          hoursBefore,
          daysBefore,
          action,
          description
        });
        return { success: true, result };
      }
      case "fastmail_remove_event_reminder": {
        const calendar2 = getCalendarTools();
        const eventId = args.event_id;
        const reminderId = args.reminder_id;
        if (!eventId)
          throw new Error("event_id is required");
        await calendar2.removeReminder(eventId, reminderId);
        return { success: true, result: { message: "Reminder removed" } };
      }
      case "fastmail_list_event_reminders": {
        const calendar2 = getCalendarTools();
        const eventId = args.event_id;
        if (!eventId)
          throw new Error("event_id is required");
        const result = await calendar2.listReminders(eventId);
        return { success: true, result };
      }
      case "fastmail_create_event_with_reminder": {
        const calendar2 = getCalendarTools();
        const calendarId = args.calendar_id;
        const title = args.title;
        const start = args.start;
        const end = args.end;
        const description = args.description;
        const location = args.location;
        const allDay = args.all_day;
        const attendees = args.attendees;
        const reminders = args.reminders;
        if (!title || !start || !end) {
          throw new Error("title, start, and end are required");
        }
        if (!reminders || reminders.length === 0) {
          throw new Error("At least one reminder is required");
        }
        const result = await calendar2.createEvent(calendarId, {
          title,
          start,
          end,
          description,
          location,
          allDay,
          attendees,
          reminders
        });
        return { success: true, result };
      }
      case "fastmail_get_thread": {
        const email = getEmailTools();
        const emailId = args.email_id;
        if (!emailId)
          throw new Error("email_id is required");
        const result = await email.getThread(emailId);
        return { success: true, result };
      }
      case "fastmail_bulk_move_emails": {
        const email = getEmailTools();
        const emailIds = args.email_ids;
        const targetMailboxId = args.target_mailbox_id;
        const sourceMailboxId = args.source_mailbox_id;
        if (!emailIds || !Array.isArray(emailIds) || emailIds.length === 0) {
          throw new Error("email_ids must be a non-empty array of email IDs");
        }
        if (!targetMailboxId) {
          throw new Error("target_mailbox_id is required");
        }
        const result = await email.bulkMoveToFolder(emailIds, targetMailboxId, sourceMailboxId);
        return { success: true, result };
      }
      case "fastmail_bulk_set_labels": {
        const email = getEmailTools();
        const emailIds = args.email_ids;
        const keywords = args.keywords;
        if (!emailIds || !Array.isArray(emailIds) || emailIds.length === 0) {
          throw new Error("email_ids must be a non-empty array of email IDs");
        }
        if (!keywords || typeof keywords !== "object") {
          throw new Error("keywords must be an object with label:boolean pairs");
        }
        const result = await email.bulkSetKeywords(emailIds, keywords);
        return { success: true, result };
      }
      case "fastmail_bulk_delete_emails": {
        const email = getEmailTools();
        const emailIds = args.email_ids;
        if (!emailIds || !Array.isArray(emailIds) || emailIds.length === 0) {
          throw new Error("email_ids must be a non-empty array of email IDs");
        }
        const result = await email.bulkDeleteEmails(emailIds);
        return { success: true, result };
      }
      case "fastmail_list_invitations": {
        const calendar2 = getCalendarTools();
        const result = await calendar2.listInvitations();
        return { success: true, result };
      }
      case "fastmail_respond_to_invitation": {
        const calendar2 = getCalendarTools();
        const eventId = args.event_id;
        const response = args.response;
        if (!eventId)
          throw new Error("event_id is required");
        if (!response || !["accept", "decline", "tentative"].includes(response)) {
          throw new Error("response must be one of: accept, decline, tentative");
        }
        await calendar2.respondToInvitation(eventId, response);
        return { success: true, result: { message: `Invitation ${response}ed` } };
      }
      default:
        return { success: false, error: `Unknown tool: ${normalizedToolName}` };
    }
  } catch (error) {
    return formatError(error);
  }
}
function showHelp() {
  console.log(`
Fastmail CLI - Email & Calendar Management

USAGE:
  bunx fastmail <command> [options]

COMMANDS:
  --help                     Show this help message
  --list                     List all available tools
  
  list_mailboxes
  list_emails [--mailbox-id ID] [--limit N]
  get_email --email-id ID
  search_emails --query TEXT [--limit N]
  send_email --to EMAIL [--to EMAIL...] --subject SUBJECT --text-body BODY [--html-body BODY]
  move_email --email-id ID --target-mailbox-id ID [--source-mailbox-id ID]
  set_labels --email-id ID --keywords JSON
  delete_email --email-id ID
  reply_email --email-id ID --text-body BODY [--subject SUBJECT] [--reply-all]
  
  list_calendars
  list_events [--calendar-id ID] [--start-date DATE] [--end-date DATE]
  get_event --event-id ID
  create_event --title TITLE --start DATE --end DATE [--description DESC] [--location LOC] [--all-day]
  update_event --event-id ID [--title TITLE] [--start DATE] [--end DATE]
  delete_event --event-id ID
  search_events --query TEXT [--start-date DATE] [--end-date DATE]
  
  create_recurring_event --title TITLE --start DATE --end DATE --recurrence FREQ [--reminders JSON]
  add_event_reminder --event-id ID [--minutes-before N] [--hours-before N] [--days-before N]
  remove_event_reminder --event-id ID [--reminder-id ID]
  list_event_reminders --event-id ID
  create_event_with_reminder --title TITLE --start DATE --end DATE [--reminders JSON]

ENVIRONMENT:
  FASTMAIL_API_TOKEN         Required for email operations
  FASTMAIL_USERNAME          Required for calendar operations
  FASTMAIL_PASSWORD          Required for calendar operations

OUTPUT:
  JSON format with structure: { success: boolean, result?: any, error?: string }
`);
}
function showList() {
  const tools = [
    "list_mailboxes",
    "list_emails",
    "get_email",
    "get_thread",
    "search_emails",
    "send_email",
    "move_email",
    "set_labels",
    "delete_email",
    "reply_email",
    "bulk_move_emails",
    "bulk_set_labels",
    "bulk_delete_emails",
    "list_calendars",
    "list_events",
    "get_event",
    "create_event",
    "update_event",
    "delete_event",
    "search_events",
    "create_recurring_event",
    "list_invitations",
    "respond_to_invitation",
    "add_event_reminder",
    "remove_event_reminder",
    "list_event_reminders",
    "create_event_with_reminder"
  ];
  console.log("Available Tools (27 total):");
  console.log(`
Email Tools (10):`);
  tools.slice(0, 10).forEach((tool, i2) => console.log(`  ${i2 + 1}. ${tool}`));
  console.log(`
Bulk Email Tools (3):`);
  tools.slice(10, 13).forEach((tool, i2) => console.log(`  ${i2 + 11}. ${tool}`));
  console.log(`
Calendar Tools (10):`);
  tools.slice(13, 23).forEach((tool, i2) => console.log(`  ${i2 + 14}. ${tool}`));
  console.log(`
Reminder Tools (4):`);
  tools.slice(23).forEach((tool, i2) => console.log(`  ${i2 + 24}. ${tool}`));
}
function parseArgs(args) {
  const command = args[0];
  const params = {};
  for (let i2 = 1;i2 < args.length; i2++) {
    const arg = args[i2];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      let value = true;
      if (key.includes("=")) {
        const [k, v] = key.split("=", 2);
        const param = k.replace(/-/g, "_");
        try {
          params[param] = JSON.parse(v);
        } catch {
          params[param] = v;
        }
      } else {
        if (i2 + 1 < args.length && !args[i2 + 1].startsWith("--")) {
          const nextArg = args[i2 + 1];
          try {
            value = JSON.parse(nextArg);
          } catch {
            value = nextArg;
          }
          i2++;
        }
        const param = key.replace(/-/g, "_");
        params[param] = value;
      }
    }
  }
  return { command, params };
}
function parseJsonArg(args) {
  if (args.length >= 2) {
    const possibleJson = args[1];
    if (possibleJson && (possibleJson.startsWith("{") || possibleJson.startsWith("["))) {
      try {
        const params = JSON.parse(possibleJson);
        if (typeof params === "object" && params !== null && !Array.isArray(params)) {
          return { command: args[0], params };
        }
      } catch {}
    }
  }
  return null;
}
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args[0] === "--help") {
    showHelp();
    process.exit(0);
  }
  if (args[0] === "--list") {
    showList();
    process.exit(0);
  }
  const jsonParsed = parseJsonArg(args);
  const { command, params } = jsonParsed || parseArgs(args);
  if (!command) {
    console.error("Error: No command specified");
    showHelp();
    process.exit(1);
  }
  const result = await handleTool(command, params);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.success ? 0 : 1);
}
main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
