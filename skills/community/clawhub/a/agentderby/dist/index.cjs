var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// node_modules/ws/lib/constants.js
var require_constants = __commonJS({
  "node_modules/ws/lib/constants.js"(exports2, module2) {
    "use strict";
    var BINARY_TYPES = ["nodebuffer", "arraybuffer", "fragments"];
    var hasBlob = typeof Blob !== "undefined";
    if (hasBlob) BINARY_TYPES.push("blob");
    module2.exports = {
      BINARY_TYPES,
      CLOSE_TIMEOUT: 3e4,
      EMPTY_BUFFER: Buffer.alloc(0),
      GUID: "258EAFA5-E914-47DA-95CA-C5AB0DC85B11",
      hasBlob,
      kForOnEventAttribute: Symbol("kIsForOnEventAttribute"),
      kListener: Symbol("kListener"),
      kStatusCode: Symbol("status-code"),
      kWebSocket: Symbol("websocket"),
      NOOP: () => {
      }
    };
  }
});

// node_modules/ws/lib/buffer-util.js
var require_buffer_util = __commonJS({
  "node_modules/ws/lib/buffer-util.js"(exports2, module2) {
    "use strict";
    var { EMPTY_BUFFER } = require_constants();
    var FastBuffer = Buffer[Symbol.species];
    function concat(list, totalLength) {
      if (list.length === 0) return EMPTY_BUFFER;
      if (list.length === 1) return list[0];
      const target = Buffer.allocUnsafe(totalLength);
      let offset = 0;
      for (let i = 0; i < list.length; i++) {
        const buf = list[i];
        target.set(buf, offset);
        offset += buf.length;
      }
      if (offset < totalLength) {
        return new FastBuffer(target.buffer, target.byteOffset, offset);
      }
      return target;
    }
    function _mask(source, mask, output, offset, length) {
      for (let i = 0; i < length; i++) {
        output[offset + i] = source[i] ^ mask[i & 3];
      }
    }
    function _unmask(buffer, mask) {
      for (let i = 0; i < buffer.length; i++) {
        buffer[i] ^= mask[i & 3];
      }
    }
    function toArrayBuffer(buf) {
      if (buf.length === buf.buffer.byteLength) {
        return buf.buffer;
      }
      return buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length);
    }
    function toBuffer(data) {
      toBuffer.readOnly = true;
      if (Buffer.isBuffer(data)) return data;
      let buf;
      if (data instanceof ArrayBuffer) {
        buf = new FastBuffer(data);
      } else if (ArrayBuffer.isView(data)) {
        buf = new FastBuffer(data.buffer, data.byteOffset, data.byteLength);
      } else {
        buf = Buffer.from(data);
        toBuffer.readOnly = false;
      }
      return buf;
    }
    module2.exports = {
      concat,
      mask: _mask,
      toArrayBuffer,
      toBuffer,
      unmask: _unmask
    };
    if (false) {
      try {
        const bufferUtil = null;
        module2.exports.mask = function(source, mask, output, offset, length) {
          if (length < 48) _mask(source, mask, output, offset, length);
          else bufferUtil.mask(source, mask, output, offset, length);
        };
        module2.exports.unmask = function(buffer, mask) {
          if (buffer.length < 32) _unmask(buffer, mask);
          else bufferUtil.unmask(buffer, mask);
        };
      } catch (e) {
      }
    }
  }
});

// node_modules/ws/lib/limiter.js
var require_limiter = __commonJS({
  "node_modules/ws/lib/limiter.js"(exports2, module2) {
    "use strict";
    var kDone = Symbol("kDone");
    var kRun = Symbol("kRun");
    var Limiter = class {
      /**
       * Creates a new `Limiter`.
       *
       * @param {Number} [concurrency=Infinity] The maximum number of jobs allowed
       *     to run concurrently
       */
      constructor(concurrency) {
        this[kDone] = () => {
          this.pending--;
          this[kRun]();
        };
        this.concurrency = concurrency || Infinity;
        this.jobs = [];
        this.pending = 0;
      }
      /**
       * Adds a job to the queue.
       *
       * @param {Function} job The job to run
       * @public
       */
      add(job) {
        this.jobs.push(job);
        this[kRun]();
      }
      /**
       * Removes a job from the queue and runs it if possible.
       *
       * @private
       */
      [kRun]() {
        if (this.pending === this.concurrency) return;
        if (this.jobs.length) {
          const job = this.jobs.shift();
          this.pending++;
          job(this[kDone]);
        }
      }
    };
    module2.exports = Limiter;
  }
});

// node_modules/ws/lib/permessage-deflate.js
var require_permessage_deflate = __commonJS({
  "node_modules/ws/lib/permessage-deflate.js"(exports2, module2) {
    "use strict";
    var zlib = require("zlib");
    var bufferUtil = require_buffer_util();
    var Limiter = require_limiter();
    var { kStatusCode } = require_constants();
    var FastBuffer = Buffer[Symbol.species];
    var TRAILER = Buffer.from([0, 0, 255, 255]);
    var kPerMessageDeflate = Symbol("permessage-deflate");
    var kTotalLength = Symbol("total-length");
    var kCallback = Symbol("callback");
    var kBuffers = Symbol("buffers");
    var kError = Symbol("error");
    var zlibLimiter;
    var PerMessageDeflate2 = class {
      /**
       * Creates a PerMessageDeflate instance.
       *
       * @param {Object} [options] Configuration options
       * @param {(Boolean|Number)} [options.clientMaxWindowBits] Advertise support
       *     for, or request, a custom client window size
       * @param {Boolean} [options.clientNoContextTakeover=false] Advertise/
       *     acknowledge disabling of client context takeover
       * @param {Number} [options.concurrencyLimit=10] The number of concurrent
       *     calls to zlib
       * @param {Boolean} [options.isServer=false] Create the instance in either
       *     server or client mode
       * @param {Number} [options.maxPayload=0] The maximum allowed message length
       * @param {(Boolean|Number)} [options.serverMaxWindowBits] Request/confirm the
       *     use of a custom server window size
       * @param {Boolean} [options.serverNoContextTakeover=false] Request/accept
       *     disabling of server context takeover
       * @param {Number} [options.threshold=1024] Size (in bytes) below which
       *     messages should not be compressed if context takeover is disabled
       * @param {Object} [options.zlibDeflateOptions] Options to pass to zlib on
       *     deflate
       * @param {Object} [options.zlibInflateOptions] Options to pass to zlib on
       *     inflate
       */
      constructor(options) {
        this._options = options || {};
        this._threshold = this._options.threshold !== void 0 ? this._options.threshold : 1024;
        this._maxPayload = this._options.maxPayload | 0;
        this._isServer = !!this._options.isServer;
        this._deflate = null;
        this._inflate = null;
        this.params = null;
        if (!zlibLimiter) {
          const concurrency = this._options.concurrencyLimit !== void 0 ? this._options.concurrencyLimit : 10;
          zlibLimiter = new Limiter(concurrency);
        }
      }
      /**
       * @type {String}
       */
      static get extensionName() {
        return "permessage-deflate";
      }
      /**
       * Create an extension negotiation offer.
       *
       * @return {Object} Extension parameters
       * @public
       */
      offer() {
        const params = {};
        if (this._options.serverNoContextTakeover) {
          params.server_no_context_takeover = true;
        }
        if (this._options.clientNoContextTakeover) {
          params.client_no_context_takeover = true;
        }
        if (this._options.serverMaxWindowBits) {
          params.server_max_window_bits = this._options.serverMaxWindowBits;
        }
        if (this._options.clientMaxWindowBits) {
          params.client_max_window_bits = this._options.clientMaxWindowBits;
        } else if (this._options.clientMaxWindowBits == null) {
          params.client_max_window_bits = true;
        }
        return params;
      }
      /**
       * Accept an extension negotiation offer/response.
       *
       * @param {Array} configurations The extension negotiation offers/reponse
       * @return {Object} Accepted configuration
       * @public
       */
      accept(configurations) {
        configurations = this.normalizeParams(configurations);
        this.params = this._isServer ? this.acceptAsServer(configurations) : this.acceptAsClient(configurations);
        return this.params;
      }
      /**
       * Releases all resources used by the extension.
       *
       * @public
       */
      cleanup() {
        if (this._inflate) {
          this._inflate.close();
          this._inflate = null;
        }
        if (this._deflate) {
          const callback = this._deflate[kCallback];
          this._deflate.close();
          this._deflate = null;
          if (callback) {
            callback(
              new Error(
                "The deflate stream was closed while data was being processed"
              )
            );
          }
        }
      }
      /**
       *  Accept an extension negotiation offer.
       *
       * @param {Array} offers The extension negotiation offers
       * @return {Object} Accepted configuration
       * @private
       */
      acceptAsServer(offers) {
        const opts = this._options;
        const accepted = offers.find((params) => {
          if (opts.serverNoContextTakeover === false && params.server_no_context_takeover || params.server_max_window_bits && (opts.serverMaxWindowBits === false || typeof opts.serverMaxWindowBits === "number" && opts.serverMaxWindowBits > params.server_max_window_bits) || typeof opts.clientMaxWindowBits === "number" && !params.client_max_window_bits) {
            return false;
          }
          return true;
        });
        if (!accepted) {
          throw new Error("None of the extension offers can be accepted");
        }
        if (opts.serverNoContextTakeover) {
          accepted.server_no_context_takeover = true;
        }
        if (opts.clientNoContextTakeover) {
          accepted.client_no_context_takeover = true;
        }
        if (typeof opts.serverMaxWindowBits === "number") {
          accepted.server_max_window_bits = opts.serverMaxWindowBits;
        }
        if (typeof opts.clientMaxWindowBits === "number") {
          accepted.client_max_window_bits = opts.clientMaxWindowBits;
        } else if (accepted.client_max_window_bits === true || opts.clientMaxWindowBits === false) {
          delete accepted.client_max_window_bits;
        }
        return accepted;
      }
      /**
       * Accept the extension negotiation response.
       *
       * @param {Array} response The extension negotiation response
       * @return {Object} Accepted configuration
       * @private
       */
      acceptAsClient(response) {
        const params = response[0];
        if (this._options.clientNoContextTakeover === false && params.client_no_context_takeover) {
          throw new Error('Unexpected parameter "client_no_context_takeover"');
        }
        if (!params.client_max_window_bits) {
          if (typeof this._options.clientMaxWindowBits === "number") {
            params.client_max_window_bits = this._options.clientMaxWindowBits;
          }
        } else if (this._options.clientMaxWindowBits === false || typeof this._options.clientMaxWindowBits === "number" && params.client_max_window_bits > this._options.clientMaxWindowBits) {
          throw new Error(
            'Unexpected or invalid parameter "client_max_window_bits"'
          );
        }
        return params;
      }
      /**
       * Normalize parameters.
       *
       * @param {Array} configurations The extension negotiation offers/reponse
       * @return {Array} The offers/response with normalized parameters
       * @private
       */
      normalizeParams(configurations) {
        configurations.forEach((params) => {
          Object.keys(params).forEach((key) => {
            let value = params[key];
            if (value.length > 1) {
              throw new Error(`Parameter "${key}" must have only a single value`);
            }
            value = value[0];
            if (key === "client_max_window_bits") {
              if (value !== true) {
                const num = +value;
                if (!Number.isInteger(num) || num < 8 || num > 15) {
                  throw new TypeError(
                    `Invalid value for parameter "${key}": ${value}`
                  );
                }
                value = num;
              } else if (!this._isServer) {
                throw new TypeError(
                  `Invalid value for parameter "${key}": ${value}`
                );
              }
            } else if (key === "server_max_window_bits") {
              const num = +value;
              if (!Number.isInteger(num) || num < 8 || num > 15) {
                throw new TypeError(
                  `Invalid value for parameter "${key}": ${value}`
                );
              }
              value = num;
            } else if (key === "client_no_context_takeover" || key === "server_no_context_takeover") {
              if (value !== true) {
                throw new TypeError(
                  `Invalid value for parameter "${key}": ${value}`
                );
              }
            } else {
              throw new Error(`Unknown parameter "${key}"`);
            }
            params[key] = value;
          });
        });
        return configurations;
      }
      /**
       * Decompress data. Concurrency limited.
       *
       * @param {Buffer} data Compressed data
       * @param {Boolean} fin Specifies whether or not this is the last fragment
       * @param {Function} callback Callback
       * @public
       */
      decompress(data, fin, callback) {
        zlibLimiter.add((done) => {
          this._decompress(data, fin, (err2, result) => {
            done();
            callback(err2, result);
          });
        });
      }
      /**
       * Compress data. Concurrency limited.
       *
       * @param {(Buffer|String)} data Data to compress
       * @param {Boolean} fin Specifies whether or not this is the last fragment
       * @param {Function} callback Callback
       * @public
       */
      compress(data, fin, callback) {
        zlibLimiter.add((done) => {
          this._compress(data, fin, (err2, result) => {
            done();
            callback(err2, result);
          });
        });
      }
      /**
       * Decompress data.
       *
       * @param {Buffer} data Compressed data
       * @param {Boolean} fin Specifies whether or not this is the last fragment
       * @param {Function} callback Callback
       * @private
       */
      _decompress(data, fin, callback) {
        const endpoint = this._isServer ? "client" : "server";
        if (!this._inflate) {
          const key = `${endpoint}_max_window_bits`;
          const windowBits = typeof this.params[key] !== "number" ? zlib.Z_DEFAULT_WINDOWBITS : this.params[key];
          this._inflate = zlib.createInflateRaw({
            ...this._options.zlibInflateOptions,
            windowBits
          });
          this._inflate[kPerMessageDeflate] = this;
          this._inflate[kTotalLength] = 0;
          this._inflate[kBuffers] = [];
          this._inflate.on("error", inflateOnError);
          this._inflate.on("data", inflateOnData);
        }
        this._inflate[kCallback] = callback;
        this._inflate.write(data);
        if (fin) this._inflate.write(TRAILER);
        this._inflate.flush(() => {
          const err2 = this._inflate[kError];
          if (err2) {
            this._inflate.close();
            this._inflate = null;
            callback(err2);
            return;
          }
          const data2 = bufferUtil.concat(
            this._inflate[kBuffers],
            this._inflate[kTotalLength]
          );
          if (this._inflate._readableState.endEmitted) {
            this._inflate.close();
            this._inflate = null;
          } else {
            this._inflate[kTotalLength] = 0;
            this._inflate[kBuffers] = [];
            if (fin && this.params[`${endpoint}_no_context_takeover`]) {
              this._inflate.reset();
            }
          }
          callback(null, data2);
        });
      }
      /**
       * Compress data.
       *
       * @param {(Buffer|String)} data Data to compress
       * @param {Boolean} fin Specifies whether or not this is the last fragment
       * @param {Function} callback Callback
       * @private
       */
      _compress(data, fin, callback) {
        const endpoint = this._isServer ? "server" : "client";
        if (!this._deflate) {
          const key = `${endpoint}_max_window_bits`;
          const windowBits = typeof this.params[key] !== "number" ? zlib.Z_DEFAULT_WINDOWBITS : this.params[key];
          this._deflate = zlib.createDeflateRaw({
            ...this._options.zlibDeflateOptions,
            windowBits
          });
          this._deflate[kTotalLength] = 0;
          this._deflate[kBuffers] = [];
          this._deflate.on("data", deflateOnData);
        }
        this._deflate[kCallback] = callback;
        this._deflate.write(data);
        this._deflate.flush(zlib.Z_SYNC_FLUSH, () => {
          if (!this._deflate) {
            return;
          }
          let data2 = bufferUtil.concat(
            this._deflate[kBuffers],
            this._deflate[kTotalLength]
          );
          if (fin) {
            data2 = new FastBuffer(data2.buffer, data2.byteOffset, data2.length - 4);
          }
          this._deflate[kCallback] = null;
          this._deflate[kTotalLength] = 0;
          this._deflate[kBuffers] = [];
          if (fin && this.params[`${endpoint}_no_context_takeover`]) {
            this._deflate.reset();
          }
          callback(null, data2);
        });
      }
    };
    module2.exports = PerMessageDeflate2;
    function deflateOnData(chunk) {
      this[kBuffers].push(chunk);
      this[kTotalLength] += chunk.length;
    }
    function inflateOnData(chunk) {
      this[kTotalLength] += chunk.length;
      if (this[kPerMessageDeflate]._maxPayload < 1 || this[kTotalLength] <= this[kPerMessageDeflate]._maxPayload) {
        this[kBuffers].push(chunk);
        return;
      }
      this[kError] = new RangeError("Max payload size exceeded");
      this[kError].code = "WS_ERR_UNSUPPORTED_MESSAGE_LENGTH";
      this[kError][kStatusCode] = 1009;
      this.removeListener("data", inflateOnData);
      this.reset();
    }
    function inflateOnError(err2) {
      this[kPerMessageDeflate]._inflate = null;
      if (this[kError]) {
        this[kCallback](this[kError]);
        return;
      }
      err2[kStatusCode] = 1007;
      this[kCallback](err2);
    }
  }
});

// node_modules/ws/lib/validation.js
var require_validation = __commonJS({
  "node_modules/ws/lib/validation.js"(exports2, module2) {
    "use strict";
    var { isUtf8 } = require("buffer");
    var { hasBlob } = require_constants();
    var tokenChars = [
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      // 0 - 15
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      // 16 - 31
      0,
      1,
      0,
      1,
      1,
      1,
      1,
      1,
      0,
      0,
      1,
      1,
      0,
      1,
      1,
      0,
      // 32 - 47
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      0,
      0,
      0,
      0,
      0,
      0,
      // 48 - 63
      0,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      // 64 - 79
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      0,
      0,
      0,
      1,
      1,
      // 80 - 95
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      // 96 - 111
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      0,
      1,
      0,
      1,
      0
      // 112 - 127
    ];
    function isValidStatusCode(code) {
      return code >= 1e3 && code <= 1014 && code !== 1004 && code !== 1005 && code !== 1006 || code >= 3e3 && code <= 4999;
    }
    function _isValidUTF8(buf) {
      const len = buf.length;
      let i = 0;
      while (i < len) {
        if ((buf[i] & 128) === 0) {
          i++;
        } else if ((buf[i] & 224) === 192) {
          if (i + 1 === len || (buf[i + 1] & 192) !== 128 || (buf[i] & 254) === 192) {
            return false;
          }
          i += 2;
        } else if ((buf[i] & 240) === 224) {
          if (i + 2 >= len || (buf[i + 1] & 192) !== 128 || (buf[i + 2] & 192) !== 128 || buf[i] === 224 && (buf[i + 1] & 224) === 128 || // Overlong
          buf[i] === 237 && (buf[i + 1] & 224) === 160) {
            return false;
          }
          i += 3;
        } else if ((buf[i] & 248) === 240) {
          if (i + 3 >= len || (buf[i + 1] & 192) !== 128 || (buf[i + 2] & 192) !== 128 || (buf[i + 3] & 192) !== 128 || buf[i] === 240 && (buf[i + 1] & 240) === 128 || // Overlong
          buf[i] === 244 && buf[i + 1] > 143 || buf[i] > 244) {
            return false;
          }
          i += 4;
        } else {
          return false;
        }
      }
      return true;
    }
    function isBlob(value) {
      return hasBlob && typeof value === "object" && typeof value.arrayBuffer === "function" && typeof value.type === "string" && typeof value.stream === "function" && (value[Symbol.toStringTag] === "Blob" || value[Symbol.toStringTag] === "File");
    }
    module2.exports = {
      isBlob,
      isValidStatusCode,
      isValidUTF8: _isValidUTF8,
      tokenChars
    };
    if (isUtf8) {
      module2.exports.isValidUTF8 = function(buf) {
        return buf.length < 24 ? _isValidUTF8(buf) : isUtf8(buf);
      };
    } else if (false) {
      try {
        const isValidUTF8 = null;
        module2.exports.isValidUTF8 = function(buf) {
          return buf.length < 32 ? _isValidUTF8(buf) : isValidUTF8(buf);
        };
      } catch (e) {
      }
    }
  }
});

// node_modules/ws/lib/receiver.js
var require_receiver = __commonJS({
  "node_modules/ws/lib/receiver.js"(exports2, module2) {
    "use strict";
    var { Writable } = require("stream");
    var PerMessageDeflate2 = require_permessage_deflate();
    var {
      BINARY_TYPES,
      EMPTY_BUFFER,
      kStatusCode,
      kWebSocket
    } = require_constants();
    var { concat, toArrayBuffer, unmask } = require_buffer_util();
    var { isValidStatusCode, isValidUTF8 } = require_validation();
    var FastBuffer = Buffer[Symbol.species];
    var GET_INFO = 0;
    var GET_PAYLOAD_LENGTH_16 = 1;
    var GET_PAYLOAD_LENGTH_64 = 2;
    var GET_MASK = 3;
    var GET_DATA = 4;
    var INFLATING = 5;
    var DEFER_EVENT = 6;
    var Receiver2 = class extends Writable {
      /**
       * Creates a Receiver instance.
       *
       * @param {Object} [options] Options object
       * @param {Boolean} [options.allowSynchronousEvents=true] Specifies whether
       *     any of the `'message'`, `'ping'`, and `'pong'` events can be emitted
       *     multiple times in the same tick
       * @param {String} [options.binaryType=nodebuffer] The type for binary data
       * @param {Object} [options.extensions] An object containing the negotiated
       *     extensions
       * @param {Boolean} [options.isServer=false] Specifies whether to operate in
       *     client or server mode
       * @param {Number} [options.maxPayload=0] The maximum allowed message length
       * @param {Boolean} [options.skipUTF8Validation=false] Specifies whether or
       *     not to skip UTF-8 validation for text and close messages
       */
      constructor(options = {}) {
        super();
        this._allowSynchronousEvents = options.allowSynchronousEvents !== void 0 ? options.allowSynchronousEvents : true;
        this._binaryType = options.binaryType || BINARY_TYPES[0];
        this._extensions = options.extensions || {};
        this._isServer = !!options.isServer;
        this._maxPayload = options.maxPayload | 0;
        this._skipUTF8Validation = !!options.skipUTF8Validation;
        this[kWebSocket] = void 0;
        this._bufferedBytes = 0;
        this._buffers = [];
        this._compressed = false;
        this._payloadLength = 0;
        this._mask = void 0;
        this._fragmented = 0;
        this._masked = false;
        this._fin = false;
        this._opcode = 0;
        this._totalPayloadLength = 0;
        this._messageLength = 0;
        this._fragments = [];
        this._errored = false;
        this._loop = false;
        this._state = GET_INFO;
      }
      /**
       * Implements `Writable.prototype._write()`.
       *
       * @param {Buffer} chunk The chunk of data to write
       * @param {String} encoding The character encoding of `chunk`
       * @param {Function} cb Callback
       * @private
       */
      _write(chunk, encoding, cb) {
        if (this._opcode === 8 && this._state == GET_INFO) return cb();
        this._bufferedBytes += chunk.length;
        this._buffers.push(chunk);
        this.startLoop(cb);
      }
      /**
       * Consumes `n` bytes from the buffered data.
       *
       * @param {Number} n The number of bytes to consume
       * @return {Buffer} The consumed bytes
       * @private
       */
      consume(n) {
        this._bufferedBytes -= n;
        if (n === this._buffers[0].length) return this._buffers.shift();
        if (n < this._buffers[0].length) {
          const buf = this._buffers[0];
          this._buffers[0] = new FastBuffer(
            buf.buffer,
            buf.byteOffset + n,
            buf.length - n
          );
          return new FastBuffer(buf.buffer, buf.byteOffset, n);
        }
        const dst = Buffer.allocUnsafe(n);
        do {
          const buf = this._buffers[0];
          const offset = dst.length - n;
          if (n >= buf.length) {
            dst.set(this._buffers.shift(), offset);
          } else {
            dst.set(new Uint8Array(buf.buffer, buf.byteOffset, n), offset);
            this._buffers[0] = new FastBuffer(
              buf.buffer,
              buf.byteOffset + n,
              buf.length - n
            );
          }
          n -= buf.length;
        } while (n > 0);
        return dst;
      }
      /**
       * Starts the parsing loop.
       *
       * @param {Function} cb Callback
       * @private
       */
      startLoop(cb) {
        this._loop = true;
        do {
          switch (this._state) {
            case GET_INFO:
              this.getInfo(cb);
              break;
            case GET_PAYLOAD_LENGTH_16:
              this.getPayloadLength16(cb);
              break;
            case GET_PAYLOAD_LENGTH_64:
              this.getPayloadLength64(cb);
              break;
            case GET_MASK:
              this.getMask();
              break;
            case GET_DATA:
              this.getData(cb);
              break;
            case INFLATING:
            case DEFER_EVENT:
              this._loop = false;
              return;
          }
        } while (this._loop);
        if (!this._errored) cb();
      }
      /**
       * Reads the first two bytes of a frame.
       *
       * @param {Function} cb Callback
       * @private
       */
      getInfo(cb) {
        if (this._bufferedBytes < 2) {
          this._loop = false;
          return;
        }
        const buf = this.consume(2);
        if ((buf[0] & 48) !== 0) {
          const error = this.createError(
            RangeError,
            "RSV2 and RSV3 must be clear",
            true,
            1002,
            "WS_ERR_UNEXPECTED_RSV_2_3"
          );
          cb(error);
          return;
        }
        const compressed = (buf[0] & 64) === 64;
        if (compressed && !this._extensions[PerMessageDeflate2.extensionName]) {
          const error = this.createError(
            RangeError,
            "RSV1 must be clear",
            true,
            1002,
            "WS_ERR_UNEXPECTED_RSV_1"
          );
          cb(error);
          return;
        }
        this._fin = (buf[0] & 128) === 128;
        this._opcode = buf[0] & 15;
        this._payloadLength = buf[1] & 127;
        if (this._opcode === 0) {
          if (compressed) {
            const error = this.createError(
              RangeError,
              "RSV1 must be clear",
              true,
              1002,
              "WS_ERR_UNEXPECTED_RSV_1"
            );
            cb(error);
            return;
          }
          if (!this._fragmented) {
            const error = this.createError(
              RangeError,
              "invalid opcode 0",
              true,
              1002,
              "WS_ERR_INVALID_OPCODE"
            );
            cb(error);
            return;
          }
          this._opcode = this._fragmented;
        } else if (this._opcode === 1 || this._opcode === 2) {
          if (this._fragmented) {
            const error = this.createError(
              RangeError,
              `invalid opcode ${this._opcode}`,
              true,
              1002,
              "WS_ERR_INVALID_OPCODE"
            );
            cb(error);
            return;
          }
          this._compressed = compressed;
        } else if (this._opcode > 7 && this._opcode < 11) {
          if (!this._fin) {
            const error = this.createError(
              RangeError,
              "FIN must be set",
              true,
              1002,
              "WS_ERR_EXPECTED_FIN"
            );
            cb(error);
            return;
          }
          if (compressed) {
            const error = this.createError(
              RangeError,
              "RSV1 must be clear",
              true,
              1002,
              "WS_ERR_UNEXPECTED_RSV_1"
            );
            cb(error);
            return;
          }
          if (this._payloadLength > 125 || this._opcode === 8 && this._payloadLength === 1) {
            const error = this.createError(
              RangeError,
              `invalid payload length ${this._payloadLength}`,
              true,
              1002,
              "WS_ERR_INVALID_CONTROL_PAYLOAD_LENGTH"
            );
            cb(error);
            return;
          }
        } else {
          const error = this.createError(
            RangeError,
            `invalid opcode ${this._opcode}`,
            true,
            1002,
            "WS_ERR_INVALID_OPCODE"
          );
          cb(error);
          return;
        }
        if (!this._fin && !this._fragmented) this._fragmented = this._opcode;
        this._masked = (buf[1] & 128) === 128;
        if (this._isServer) {
          if (!this._masked) {
            const error = this.createError(
              RangeError,
              "MASK must be set",
              true,
              1002,
              "WS_ERR_EXPECTED_MASK"
            );
            cb(error);
            return;
          }
        } else if (this._masked) {
          const error = this.createError(
            RangeError,
            "MASK must be clear",
            true,
            1002,
            "WS_ERR_UNEXPECTED_MASK"
          );
          cb(error);
          return;
        }
        if (this._payloadLength === 126) this._state = GET_PAYLOAD_LENGTH_16;
        else if (this._payloadLength === 127) this._state = GET_PAYLOAD_LENGTH_64;
        else this.haveLength(cb);
      }
      /**
       * Gets extended payload length (7+16).
       *
       * @param {Function} cb Callback
       * @private
       */
      getPayloadLength16(cb) {
        if (this._bufferedBytes < 2) {
          this._loop = false;
          return;
        }
        this._payloadLength = this.consume(2).readUInt16BE(0);
        this.haveLength(cb);
      }
      /**
       * Gets extended payload length (7+64).
       *
       * @param {Function} cb Callback
       * @private
       */
      getPayloadLength64(cb) {
        if (this._bufferedBytes < 8) {
          this._loop = false;
          return;
        }
        const buf = this.consume(8);
        const num = buf.readUInt32BE(0);
        if (num > Math.pow(2, 53 - 32) - 1) {
          const error = this.createError(
            RangeError,
            "Unsupported WebSocket frame: payload length > 2^53 - 1",
            false,
            1009,
            "WS_ERR_UNSUPPORTED_DATA_PAYLOAD_LENGTH"
          );
          cb(error);
          return;
        }
        this._payloadLength = num * Math.pow(2, 32) + buf.readUInt32BE(4);
        this.haveLength(cb);
      }
      /**
       * Payload length has been read.
       *
       * @param {Function} cb Callback
       * @private
       */
      haveLength(cb) {
        if (this._payloadLength && this._opcode < 8) {
          this._totalPayloadLength += this._payloadLength;
          if (this._totalPayloadLength > this._maxPayload && this._maxPayload > 0) {
            const error = this.createError(
              RangeError,
              "Max payload size exceeded",
              false,
              1009,
              "WS_ERR_UNSUPPORTED_MESSAGE_LENGTH"
            );
            cb(error);
            return;
          }
        }
        if (this._masked) this._state = GET_MASK;
        else this._state = GET_DATA;
      }
      /**
       * Reads mask bytes.
       *
       * @private
       */
      getMask() {
        if (this._bufferedBytes < 4) {
          this._loop = false;
          return;
        }
        this._mask = this.consume(4);
        this._state = GET_DATA;
      }
      /**
       * Reads data bytes.
       *
       * @param {Function} cb Callback
       * @private
       */
      getData(cb) {
        let data = EMPTY_BUFFER;
        if (this._payloadLength) {
          if (this._bufferedBytes < this._payloadLength) {
            this._loop = false;
            return;
          }
          data = this.consume(this._payloadLength);
          if (this._masked && (this._mask[0] | this._mask[1] | this._mask[2] | this._mask[3]) !== 0) {
            unmask(data, this._mask);
          }
        }
        if (this._opcode > 7) {
          this.controlMessage(data, cb);
          return;
        }
        if (this._compressed) {
          this._state = INFLATING;
          this.decompress(data, cb);
          return;
        }
        if (data.length) {
          this._messageLength = this._totalPayloadLength;
          this._fragments.push(data);
        }
        this.dataMessage(cb);
      }
      /**
       * Decompresses data.
       *
       * @param {Buffer} data Compressed data
       * @param {Function} cb Callback
       * @private
       */
      decompress(data, cb) {
        const perMessageDeflate = this._extensions[PerMessageDeflate2.extensionName];
        perMessageDeflate.decompress(data, this._fin, (err2, buf) => {
          if (err2) return cb(err2);
          if (buf.length) {
            this._messageLength += buf.length;
            if (this._messageLength > this._maxPayload && this._maxPayload > 0) {
              const error = this.createError(
                RangeError,
                "Max payload size exceeded",
                false,
                1009,
                "WS_ERR_UNSUPPORTED_MESSAGE_LENGTH"
              );
              cb(error);
              return;
            }
            this._fragments.push(buf);
          }
          this.dataMessage(cb);
          if (this._state === GET_INFO) this.startLoop(cb);
        });
      }
      /**
       * Handles a data message.
       *
       * @param {Function} cb Callback
       * @private
       */
      dataMessage(cb) {
        if (!this._fin) {
          this._state = GET_INFO;
          return;
        }
        const messageLength = this._messageLength;
        const fragments = this._fragments;
        this._totalPayloadLength = 0;
        this._messageLength = 0;
        this._fragmented = 0;
        this._fragments = [];
        if (this._opcode === 2) {
          let data;
          if (this._binaryType === "nodebuffer") {
            data = concat(fragments, messageLength);
          } else if (this._binaryType === "arraybuffer") {
            data = toArrayBuffer(concat(fragments, messageLength));
          } else if (this._binaryType === "blob") {
            data = new Blob(fragments);
          } else {
            data = fragments;
          }
          if (this._allowSynchronousEvents) {
            this.emit("message", data, true);
            this._state = GET_INFO;
          } else {
            this._state = DEFER_EVENT;
            setImmediate(() => {
              this.emit("message", data, true);
              this._state = GET_INFO;
              this.startLoop(cb);
            });
          }
        } else {
          const buf = concat(fragments, messageLength);
          if (!this._skipUTF8Validation && !isValidUTF8(buf)) {
            const error = this.createError(
              Error,
              "invalid UTF-8 sequence",
              true,
              1007,
              "WS_ERR_INVALID_UTF8"
            );
            cb(error);
            return;
          }
          if (this._state === INFLATING || this._allowSynchronousEvents) {
            this.emit("message", buf, false);
            this._state = GET_INFO;
          } else {
            this._state = DEFER_EVENT;
            setImmediate(() => {
              this.emit("message", buf, false);
              this._state = GET_INFO;
              this.startLoop(cb);
            });
          }
        }
      }
      /**
       * Handles a control message.
       *
       * @param {Buffer} data Data to handle
       * @return {(Error|RangeError|undefined)} A possible error
       * @private
       */
      controlMessage(data, cb) {
        if (this._opcode === 8) {
          if (data.length === 0) {
            this._loop = false;
            this.emit("conclude", 1005, EMPTY_BUFFER);
            this.end();
          } else {
            const code = data.readUInt16BE(0);
            if (!isValidStatusCode(code)) {
              const error = this.createError(
                RangeError,
                `invalid status code ${code}`,
                true,
                1002,
                "WS_ERR_INVALID_CLOSE_CODE"
              );
              cb(error);
              return;
            }
            const buf = new FastBuffer(
              data.buffer,
              data.byteOffset + 2,
              data.length - 2
            );
            if (!this._skipUTF8Validation && !isValidUTF8(buf)) {
              const error = this.createError(
                Error,
                "invalid UTF-8 sequence",
                true,
                1007,
                "WS_ERR_INVALID_UTF8"
              );
              cb(error);
              return;
            }
            this._loop = false;
            this.emit("conclude", code, buf);
            this.end();
          }
          this._state = GET_INFO;
          return;
        }
        if (this._allowSynchronousEvents) {
          this.emit(this._opcode === 9 ? "ping" : "pong", data);
          this._state = GET_INFO;
        } else {
          this._state = DEFER_EVENT;
          setImmediate(() => {
            this.emit(this._opcode === 9 ? "ping" : "pong", data);
            this._state = GET_INFO;
            this.startLoop(cb);
          });
        }
      }
      /**
       * Builds an error object.
       *
       * @param {function(new:Error|RangeError)} ErrorCtor The error constructor
       * @param {String} message The error message
       * @param {Boolean} prefix Specifies whether or not to add a default prefix to
       *     `message`
       * @param {Number} statusCode The status code
       * @param {String} errorCode The exposed error code
       * @return {(Error|RangeError)} The error
       * @private
       */
      createError(ErrorCtor, message, prefix, statusCode, errorCode) {
        this._loop = false;
        this._errored = true;
        const err2 = new ErrorCtor(
          prefix ? `Invalid WebSocket frame: ${message}` : message
        );
        Error.captureStackTrace(err2, this.createError);
        err2.code = errorCode;
        err2[kStatusCode] = statusCode;
        return err2;
      }
    };
    module2.exports = Receiver2;
  }
});

// node_modules/ws/lib/sender.js
var require_sender = __commonJS({
  "node_modules/ws/lib/sender.js"(exports2, module2) {
    "use strict";
    var { Duplex } = require("stream");
    var { randomFillSync } = require("crypto");
    var PerMessageDeflate2 = require_permessage_deflate();
    var { EMPTY_BUFFER, kWebSocket, NOOP } = require_constants();
    var { isBlob, isValidStatusCode } = require_validation();
    var { mask: applyMask, toBuffer } = require_buffer_util();
    var kByteLength = Symbol("kByteLength");
    var maskBuffer = Buffer.alloc(4);
    var RANDOM_POOL_SIZE = 8 * 1024;
    var randomPool;
    var randomPoolPointer = RANDOM_POOL_SIZE;
    var DEFAULT = 0;
    var DEFLATING = 1;
    var GET_BLOB_DATA = 2;
    var Sender2 = class _Sender {
      /**
       * Creates a Sender instance.
       *
       * @param {Duplex} socket The connection socket
       * @param {Object} [extensions] An object containing the negotiated extensions
       * @param {Function} [generateMask] The function used to generate the masking
       *     key
       */
      constructor(socket, extensions, generateMask) {
        this._extensions = extensions || {};
        if (generateMask) {
          this._generateMask = generateMask;
          this._maskBuffer = Buffer.alloc(4);
        }
        this._socket = socket;
        this._firstFragment = true;
        this._compress = false;
        this._bufferedBytes = 0;
        this._queue = [];
        this._state = DEFAULT;
        this.onerror = NOOP;
        this[kWebSocket] = void 0;
      }
      /**
       * Frames a piece of data according to the HyBi WebSocket protocol.
       *
       * @param {(Buffer|String)} data The data to frame
       * @param {Object} options Options object
       * @param {Boolean} [options.fin=false] Specifies whether or not to set the
       *     FIN bit
       * @param {Function} [options.generateMask] The function used to generate the
       *     masking key
       * @param {Boolean} [options.mask=false] Specifies whether or not to mask
       *     `data`
       * @param {Buffer} [options.maskBuffer] The buffer used to store the masking
       *     key
       * @param {Number} options.opcode The opcode
       * @param {Boolean} [options.readOnly=false] Specifies whether `data` can be
       *     modified
       * @param {Boolean} [options.rsv1=false] Specifies whether or not to set the
       *     RSV1 bit
       * @return {(Buffer|String)[]} The framed data
       * @public
       */
      static frame(data, options) {
        let mask;
        let merge = false;
        let offset = 2;
        let skipMasking = false;
        if (options.mask) {
          mask = options.maskBuffer || maskBuffer;
          if (options.generateMask) {
            options.generateMask(mask);
          } else {
            if (randomPoolPointer === RANDOM_POOL_SIZE) {
              if (randomPool === void 0) {
                randomPool = Buffer.alloc(RANDOM_POOL_SIZE);
              }
              randomFillSync(randomPool, 0, RANDOM_POOL_SIZE);
              randomPoolPointer = 0;
            }
            mask[0] = randomPool[randomPoolPointer++];
            mask[1] = randomPool[randomPoolPointer++];
            mask[2] = randomPool[randomPoolPointer++];
            mask[3] = randomPool[randomPoolPointer++];
          }
          skipMasking = (mask[0] | mask[1] | mask[2] | mask[3]) === 0;
          offset = 6;
        }
        let dataLength;
        if (typeof data === "string") {
          if ((!options.mask || skipMasking) && options[kByteLength] !== void 0) {
            dataLength = options[kByteLength];
          } else {
            data = Buffer.from(data);
            dataLength = data.length;
          }
        } else {
          dataLength = data.length;
          merge = options.mask && options.readOnly && !skipMasking;
        }
        let payloadLength = dataLength;
        if (dataLength >= 65536) {
          offset += 8;
          payloadLength = 127;
        } else if (dataLength > 125) {
          offset += 2;
          payloadLength = 126;
        }
        const target = Buffer.allocUnsafe(merge ? dataLength + offset : offset);
        target[0] = options.fin ? options.opcode | 128 : options.opcode;
        if (options.rsv1) target[0] |= 64;
        target[1] = payloadLength;
        if (payloadLength === 126) {
          target.writeUInt16BE(dataLength, 2);
        } else if (payloadLength === 127) {
          target[2] = target[3] = 0;
          target.writeUIntBE(dataLength, 4, 6);
        }
        if (!options.mask) return [target, data];
        target[1] |= 128;
        target[offset - 4] = mask[0];
        target[offset - 3] = mask[1];
        target[offset - 2] = mask[2];
        target[offset - 1] = mask[3];
        if (skipMasking) return [target, data];
        if (merge) {
          applyMask(data, mask, target, offset, dataLength);
          return [target];
        }
        applyMask(data, mask, data, 0, dataLength);
        return [target, data];
      }
      /**
       * Sends a close message to the other peer.
       *
       * @param {Number} [code] The status code component of the body
       * @param {(String|Buffer)} [data] The message component of the body
       * @param {Boolean} [mask=false] Specifies whether or not to mask the message
       * @param {Function} [cb] Callback
       * @public
       */
      close(code, data, mask, cb) {
        let buf;
        if (code === void 0) {
          buf = EMPTY_BUFFER;
        } else if (typeof code !== "number" || !isValidStatusCode(code)) {
          throw new TypeError("First argument must be a valid error code number");
        } else if (data === void 0 || !data.length) {
          buf = Buffer.allocUnsafe(2);
          buf.writeUInt16BE(code, 0);
        } else {
          const length = Buffer.byteLength(data);
          if (length > 123) {
            throw new RangeError("The message must not be greater than 123 bytes");
          }
          buf = Buffer.allocUnsafe(2 + length);
          buf.writeUInt16BE(code, 0);
          if (typeof data === "string") {
            buf.write(data, 2);
          } else {
            buf.set(data, 2);
          }
        }
        const options = {
          [kByteLength]: buf.length,
          fin: true,
          generateMask: this._generateMask,
          mask,
          maskBuffer: this._maskBuffer,
          opcode: 8,
          readOnly: false,
          rsv1: false
        };
        if (this._state !== DEFAULT) {
          this.enqueue([this.dispatch, buf, false, options, cb]);
        } else {
          this.sendFrame(_Sender.frame(buf, options), cb);
        }
      }
      /**
       * Sends a ping message to the other peer.
       *
       * @param {*} data The message to send
       * @param {Boolean} [mask=false] Specifies whether or not to mask `data`
       * @param {Function} [cb] Callback
       * @public
       */
      ping(data, mask, cb) {
        let byteLength;
        let readOnly;
        if (typeof data === "string") {
          byteLength = Buffer.byteLength(data);
          readOnly = false;
        } else if (isBlob(data)) {
          byteLength = data.size;
          readOnly = false;
        } else {
          data = toBuffer(data);
          byteLength = data.length;
          readOnly = toBuffer.readOnly;
        }
        if (byteLength > 125) {
          throw new RangeError("The data size must not be greater than 125 bytes");
        }
        const options = {
          [kByteLength]: byteLength,
          fin: true,
          generateMask: this._generateMask,
          mask,
          maskBuffer: this._maskBuffer,
          opcode: 9,
          readOnly,
          rsv1: false
        };
        if (isBlob(data)) {
          if (this._state !== DEFAULT) {
            this.enqueue([this.getBlobData, data, false, options, cb]);
          } else {
            this.getBlobData(data, false, options, cb);
          }
        } else if (this._state !== DEFAULT) {
          this.enqueue([this.dispatch, data, false, options, cb]);
        } else {
          this.sendFrame(_Sender.frame(data, options), cb);
        }
      }
      /**
       * Sends a pong message to the other peer.
       *
       * @param {*} data The message to send
       * @param {Boolean} [mask=false] Specifies whether or not to mask `data`
       * @param {Function} [cb] Callback
       * @public
       */
      pong(data, mask, cb) {
        let byteLength;
        let readOnly;
        if (typeof data === "string") {
          byteLength = Buffer.byteLength(data);
          readOnly = false;
        } else if (isBlob(data)) {
          byteLength = data.size;
          readOnly = false;
        } else {
          data = toBuffer(data);
          byteLength = data.length;
          readOnly = toBuffer.readOnly;
        }
        if (byteLength > 125) {
          throw new RangeError("The data size must not be greater than 125 bytes");
        }
        const options = {
          [kByteLength]: byteLength,
          fin: true,
          generateMask: this._generateMask,
          mask,
          maskBuffer: this._maskBuffer,
          opcode: 10,
          readOnly,
          rsv1: false
        };
        if (isBlob(data)) {
          if (this._state !== DEFAULT) {
            this.enqueue([this.getBlobData, data, false, options, cb]);
          } else {
            this.getBlobData(data, false, options, cb);
          }
        } else if (this._state !== DEFAULT) {
          this.enqueue([this.dispatch, data, false, options, cb]);
        } else {
          this.sendFrame(_Sender.frame(data, options), cb);
        }
      }
      /**
       * Sends a data message to the other peer.
       *
       * @param {*} data The message to send
       * @param {Object} options Options object
       * @param {Boolean} [options.binary=false] Specifies whether `data` is binary
       *     or text
       * @param {Boolean} [options.compress=false] Specifies whether or not to
       *     compress `data`
       * @param {Boolean} [options.fin=false] Specifies whether the fragment is the
       *     last one
       * @param {Boolean} [options.mask=false] Specifies whether or not to mask
       *     `data`
       * @param {Function} [cb] Callback
       * @public
       */
      send(data, options, cb) {
        const perMessageDeflate = this._extensions[PerMessageDeflate2.extensionName];
        let opcode = options.binary ? 2 : 1;
        let rsv1 = options.compress;
        let byteLength;
        let readOnly;
        if (typeof data === "string") {
          byteLength = Buffer.byteLength(data);
          readOnly = false;
        } else if (isBlob(data)) {
          byteLength = data.size;
          readOnly = false;
        } else {
          data = toBuffer(data);
          byteLength = data.length;
          readOnly = toBuffer.readOnly;
        }
        if (this._firstFragment) {
          this._firstFragment = false;
          if (rsv1 && perMessageDeflate && perMessageDeflate.params[perMessageDeflate._isServer ? "server_no_context_takeover" : "client_no_context_takeover"]) {
            rsv1 = byteLength >= perMessageDeflate._threshold;
          }
          this._compress = rsv1;
        } else {
          rsv1 = false;
          opcode = 0;
        }
        if (options.fin) this._firstFragment = true;
        const opts = {
          [kByteLength]: byteLength,
          fin: options.fin,
          generateMask: this._generateMask,
          mask: options.mask,
          maskBuffer: this._maskBuffer,
          opcode,
          readOnly,
          rsv1
        };
        if (isBlob(data)) {
          if (this._state !== DEFAULT) {
            this.enqueue([this.getBlobData, data, this._compress, opts, cb]);
          } else {
            this.getBlobData(data, this._compress, opts, cb);
          }
        } else if (this._state !== DEFAULT) {
          this.enqueue([this.dispatch, data, this._compress, opts, cb]);
        } else {
          this.dispatch(data, this._compress, opts, cb);
        }
      }
      /**
       * Gets the contents of a blob as binary data.
       *
       * @param {Blob} blob The blob
       * @param {Boolean} [compress=false] Specifies whether or not to compress
       *     the data
       * @param {Object} options Options object
       * @param {Boolean} [options.fin=false] Specifies whether or not to set the
       *     FIN bit
       * @param {Function} [options.generateMask] The function used to generate the
       *     masking key
       * @param {Boolean} [options.mask=false] Specifies whether or not to mask
       *     `data`
       * @param {Buffer} [options.maskBuffer] The buffer used to store the masking
       *     key
       * @param {Number} options.opcode The opcode
       * @param {Boolean} [options.readOnly=false] Specifies whether `data` can be
       *     modified
       * @param {Boolean} [options.rsv1=false] Specifies whether or not to set the
       *     RSV1 bit
       * @param {Function} [cb] Callback
       * @private
       */
      getBlobData(blob, compress, options, cb) {
        this._bufferedBytes += options[kByteLength];
        this._state = GET_BLOB_DATA;
        blob.arrayBuffer().then((arrayBuffer) => {
          if (this._socket.destroyed) {
            const err2 = new Error(
              "The socket was closed while the blob was being read"
            );
            process.nextTick(callCallbacks, this, err2, cb);
            return;
          }
          this._bufferedBytes -= options[kByteLength];
          const data = toBuffer(arrayBuffer);
          if (!compress) {
            this._state = DEFAULT;
            this.sendFrame(_Sender.frame(data, options), cb);
            this.dequeue();
          } else {
            this.dispatch(data, compress, options, cb);
          }
        }).catch((err2) => {
          process.nextTick(onError, this, err2, cb);
        });
      }
      /**
       * Dispatches a message.
       *
       * @param {(Buffer|String)} data The message to send
       * @param {Boolean} [compress=false] Specifies whether or not to compress
       *     `data`
       * @param {Object} options Options object
       * @param {Boolean} [options.fin=false] Specifies whether or not to set the
       *     FIN bit
       * @param {Function} [options.generateMask] The function used to generate the
       *     masking key
       * @param {Boolean} [options.mask=false] Specifies whether or not to mask
       *     `data`
       * @param {Buffer} [options.maskBuffer] The buffer used to store the masking
       *     key
       * @param {Number} options.opcode The opcode
       * @param {Boolean} [options.readOnly=false] Specifies whether `data` can be
       *     modified
       * @param {Boolean} [options.rsv1=false] Specifies whether or not to set the
       *     RSV1 bit
       * @param {Function} [cb] Callback
       * @private
       */
      dispatch(data, compress, options, cb) {
        if (!compress) {
          this.sendFrame(_Sender.frame(data, options), cb);
          return;
        }
        const perMessageDeflate = this._extensions[PerMessageDeflate2.extensionName];
        this._bufferedBytes += options[kByteLength];
        this._state = DEFLATING;
        perMessageDeflate.compress(data, options.fin, (_, buf) => {
          if (this._socket.destroyed) {
            const err2 = new Error(
              "The socket was closed while data was being compressed"
            );
            callCallbacks(this, err2, cb);
            return;
          }
          this._bufferedBytes -= options[kByteLength];
          this._state = DEFAULT;
          options.readOnly = false;
          this.sendFrame(_Sender.frame(buf, options), cb);
          this.dequeue();
        });
      }
      /**
       * Executes queued send operations.
       *
       * @private
       */
      dequeue() {
        while (this._state === DEFAULT && this._queue.length) {
          const params = this._queue.shift();
          this._bufferedBytes -= params[3][kByteLength];
          Reflect.apply(params[0], this, params.slice(1));
        }
      }
      /**
       * Enqueues a send operation.
       *
       * @param {Array} params Send operation parameters.
       * @private
       */
      enqueue(params) {
        this._bufferedBytes += params[3][kByteLength];
        this._queue.push(params);
      }
      /**
       * Sends a frame.
       *
       * @param {(Buffer | String)[]} list The frame to send
       * @param {Function} [cb] Callback
       * @private
       */
      sendFrame(list, cb) {
        if (list.length === 2) {
          this._socket.cork();
          this._socket.write(list[0]);
          this._socket.write(list[1], cb);
          this._socket.uncork();
        } else {
          this._socket.write(list[0], cb);
        }
      }
    };
    module2.exports = Sender2;
    function callCallbacks(sender, err2, cb) {
      if (typeof cb === "function") cb(err2);
      for (let i = 0; i < sender._queue.length; i++) {
        const params = sender._queue[i];
        const callback = params[params.length - 1];
        if (typeof callback === "function") callback(err2);
      }
    }
    function onError(sender, err2, cb) {
      callCallbacks(sender, err2, cb);
      sender.onerror(err2);
    }
  }
});

// node_modules/ws/lib/event-target.js
var require_event_target = __commonJS({
  "node_modules/ws/lib/event-target.js"(exports2, module2) {
    "use strict";
    var { kForOnEventAttribute, kListener } = require_constants();
    var kCode = Symbol("kCode");
    var kData = Symbol("kData");
    var kError = Symbol("kError");
    var kMessage = Symbol("kMessage");
    var kReason = Symbol("kReason");
    var kTarget = Symbol("kTarget");
    var kType = Symbol("kType");
    var kWasClean = Symbol("kWasClean");
    var Event = class {
      /**
       * Create a new `Event`.
       *
       * @param {String} type The name of the event
       * @throws {TypeError} If the `type` argument is not specified
       */
      constructor(type) {
        this[kTarget] = null;
        this[kType] = type;
      }
      /**
       * @type {*}
       */
      get target() {
        return this[kTarget];
      }
      /**
       * @type {String}
       */
      get type() {
        return this[kType];
      }
    };
    Object.defineProperty(Event.prototype, "target", { enumerable: true });
    Object.defineProperty(Event.prototype, "type", { enumerable: true });
    var CloseEvent = class extends Event {
      /**
       * Create a new `CloseEvent`.
       *
       * @param {String} type The name of the event
       * @param {Object} [options] A dictionary object that allows for setting
       *     attributes via object members of the same name
       * @param {Number} [options.code=0] The status code explaining why the
       *     connection was closed
       * @param {String} [options.reason=''] A human-readable string explaining why
       *     the connection was closed
       * @param {Boolean} [options.wasClean=false] Indicates whether or not the
       *     connection was cleanly closed
       */
      constructor(type, options = {}) {
        super(type);
        this[kCode] = options.code === void 0 ? 0 : options.code;
        this[kReason] = options.reason === void 0 ? "" : options.reason;
        this[kWasClean] = options.wasClean === void 0 ? false : options.wasClean;
      }
      /**
       * @type {Number}
       */
      get code() {
        return this[kCode];
      }
      /**
       * @type {String}
       */
      get reason() {
        return this[kReason];
      }
      /**
       * @type {Boolean}
       */
      get wasClean() {
        return this[kWasClean];
      }
    };
    Object.defineProperty(CloseEvent.prototype, "code", { enumerable: true });
    Object.defineProperty(CloseEvent.prototype, "reason", { enumerable: true });
    Object.defineProperty(CloseEvent.prototype, "wasClean", { enumerable: true });
    var ErrorEvent = class extends Event {
      /**
       * Create a new `ErrorEvent`.
       *
       * @param {String} type The name of the event
       * @param {Object} [options] A dictionary object that allows for setting
       *     attributes via object members of the same name
       * @param {*} [options.error=null] The error that generated this event
       * @param {String} [options.message=''] The error message
       */
      constructor(type, options = {}) {
        super(type);
        this[kError] = options.error === void 0 ? null : options.error;
        this[kMessage] = options.message === void 0 ? "" : options.message;
      }
      /**
       * @type {*}
       */
      get error() {
        return this[kError];
      }
      /**
       * @type {String}
       */
      get message() {
        return this[kMessage];
      }
    };
    Object.defineProperty(ErrorEvent.prototype, "error", { enumerable: true });
    Object.defineProperty(ErrorEvent.prototype, "message", { enumerable: true });
    var MessageEvent = class extends Event {
      /**
       * Create a new `MessageEvent`.
       *
       * @param {String} type The name of the event
       * @param {Object} [options] A dictionary object that allows for setting
       *     attributes via object members of the same name
       * @param {*} [options.data=null] The message content
       */
      constructor(type, options = {}) {
        super(type);
        this[kData] = options.data === void 0 ? null : options.data;
      }
      /**
       * @type {*}
       */
      get data() {
        return this[kData];
      }
    };
    Object.defineProperty(MessageEvent.prototype, "data", { enumerable: true });
    var EventTarget = {
      /**
       * Register an event listener.
       *
       * @param {String} type A string representing the event type to listen for
       * @param {(Function|Object)} handler The listener to add
       * @param {Object} [options] An options object specifies characteristics about
       *     the event listener
       * @param {Boolean} [options.once=false] A `Boolean` indicating that the
       *     listener should be invoked at most once after being added. If `true`,
       *     the listener would be automatically removed when invoked.
       * @public
       */
      addEventListener(type, handler, options = {}) {
        for (const listener of this.listeners(type)) {
          if (!options[kForOnEventAttribute] && listener[kListener] === handler && !listener[kForOnEventAttribute]) {
            return;
          }
        }
        let wrapper;
        if (type === "message") {
          wrapper = function onMessage(data, isBinary) {
            const event = new MessageEvent("message", {
              data: isBinary ? data : data.toString()
            });
            event[kTarget] = this;
            callListener(handler, this, event);
          };
        } else if (type === "close") {
          wrapper = function onClose(code, message) {
            const event = new CloseEvent("close", {
              code,
              reason: message.toString(),
              wasClean: this._closeFrameReceived && this._closeFrameSent
            });
            event[kTarget] = this;
            callListener(handler, this, event);
          };
        } else if (type === "error") {
          wrapper = function onError(error) {
            const event = new ErrorEvent("error", {
              error,
              message: error.message
            });
            event[kTarget] = this;
            callListener(handler, this, event);
          };
        } else if (type === "open") {
          wrapper = function onOpen() {
            const event = new Event("open");
            event[kTarget] = this;
            callListener(handler, this, event);
          };
        } else {
          return;
        }
        wrapper[kForOnEventAttribute] = !!options[kForOnEventAttribute];
        wrapper[kListener] = handler;
        if (options.once) {
          this.once(type, wrapper);
        } else {
          this.on(type, wrapper);
        }
      },
      /**
       * Remove an event listener.
       *
       * @param {String} type A string representing the event type to remove
       * @param {(Function|Object)} handler The listener to remove
       * @public
       */
      removeEventListener(type, handler) {
        for (const listener of this.listeners(type)) {
          if (listener[kListener] === handler && !listener[kForOnEventAttribute]) {
            this.removeListener(type, listener);
            break;
          }
        }
      }
    };
    module2.exports = {
      CloseEvent,
      ErrorEvent,
      Event,
      EventTarget,
      MessageEvent
    };
    function callListener(listener, thisArg, event) {
      if (typeof listener === "object" && listener.handleEvent) {
        listener.handleEvent.call(listener, event);
      } else {
        listener.call(thisArg, event);
      }
    }
  }
});

// node_modules/ws/lib/extension.js
var require_extension = __commonJS({
  "node_modules/ws/lib/extension.js"(exports2, module2) {
    "use strict";
    var { tokenChars } = require_validation();
    function push(dest, name, elem) {
      if (dest[name] === void 0) dest[name] = [elem];
      else dest[name].push(elem);
    }
    function parse(header) {
      const offers = /* @__PURE__ */ Object.create(null);
      let params = /* @__PURE__ */ Object.create(null);
      let mustUnescape = false;
      let isEscaping = false;
      let inQuotes = false;
      let extensionName;
      let paramName;
      let start = -1;
      let code = -1;
      let end = -1;
      let i = 0;
      for (; i < header.length; i++) {
        code = header.charCodeAt(i);
        if (extensionName === void 0) {
          if (end === -1 && tokenChars[code] === 1) {
            if (start === -1) start = i;
          } else if (i !== 0 && (code === 32 || code === 9)) {
            if (end === -1 && start !== -1) end = i;
          } else if (code === 59 || code === 44) {
            if (start === -1) {
              throw new SyntaxError(`Unexpected character at index ${i}`);
            }
            if (end === -1) end = i;
            const name = header.slice(start, end);
            if (code === 44) {
              push(offers, name, params);
              params = /* @__PURE__ */ Object.create(null);
            } else {
              extensionName = name;
            }
            start = end = -1;
          } else {
            throw new SyntaxError(`Unexpected character at index ${i}`);
          }
        } else if (paramName === void 0) {
          if (end === -1 && tokenChars[code] === 1) {
            if (start === -1) start = i;
          } else if (code === 32 || code === 9) {
            if (end === -1 && start !== -1) end = i;
          } else if (code === 59 || code === 44) {
            if (start === -1) {
              throw new SyntaxError(`Unexpected character at index ${i}`);
            }
            if (end === -1) end = i;
            push(params, header.slice(start, end), true);
            if (code === 44) {
              push(offers, extensionName, params);
              params = /* @__PURE__ */ Object.create(null);
              extensionName = void 0;
            }
            start = end = -1;
          } else if (code === 61 && start !== -1 && end === -1) {
            paramName = header.slice(start, i);
            start = end = -1;
          } else {
            throw new SyntaxError(`Unexpected character at index ${i}`);
          }
        } else {
          if (isEscaping) {
            if (tokenChars[code] !== 1) {
              throw new SyntaxError(`Unexpected character at index ${i}`);
            }
            if (start === -1) start = i;
            else if (!mustUnescape) mustUnescape = true;
            isEscaping = false;
          } else if (inQuotes) {
            if (tokenChars[code] === 1) {
              if (start === -1) start = i;
            } else if (code === 34 && start !== -1) {
              inQuotes = false;
              end = i;
            } else if (code === 92) {
              isEscaping = true;
            } else {
              throw new SyntaxError(`Unexpected character at index ${i}`);
            }
          } else if (code === 34 && header.charCodeAt(i - 1) === 61) {
            inQuotes = true;
          } else if (end === -1 && tokenChars[code] === 1) {
            if (start === -1) start = i;
          } else if (start !== -1 && (code === 32 || code === 9)) {
            if (end === -1) end = i;
          } else if (code === 59 || code === 44) {
            if (start === -1) {
              throw new SyntaxError(`Unexpected character at index ${i}`);
            }
            if (end === -1) end = i;
            let value = header.slice(start, end);
            if (mustUnescape) {
              value = value.replace(/\\/g, "");
              mustUnescape = false;
            }
            push(params, paramName, value);
            if (code === 44) {
              push(offers, extensionName, params);
              params = /* @__PURE__ */ Object.create(null);
              extensionName = void 0;
            }
            paramName = void 0;
            start = end = -1;
          } else {
            throw new SyntaxError(`Unexpected character at index ${i}`);
          }
        }
      }
      if (start === -1 || inQuotes || code === 32 || code === 9) {
        throw new SyntaxError("Unexpected end of input");
      }
      if (end === -1) end = i;
      const token = header.slice(start, end);
      if (extensionName === void 0) {
        push(offers, token, params);
      } else {
        if (paramName === void 0) {
          push(params, token, true);
        } else if (mustUnescape) {
          push(params, paramName, token.replace(/\\/g, ""));
        } else {
          push(params, paramName, token);
        }
        push(offers, extensionName, params);
      }
      return offers;
    }
    function format(extensions) {
      return Object.keys(extensions).map((extension2) => {
        let configurations = extensions[extension2];
        if (!Array.isArray(configurations)) configurations = [configurations];
        return configurations.map((params) => {
          return [extension2].concat(
            Object.keys(params).map((k) => {
              let values = params[k];
              if (!Array.isArray(values)) values = [values];
              return values.map((v) => v === true ? k : `${k}=${v}`).join("; ");
            })
          ).join("; ");
        }).join(", ");
      }).join(", ");
    }
    module2.exports = { format, parse };
  }
});

// node_modules/ws/lib/websocket.js
var require_websocket = __commonJS({
  "node_modules/ws/lib/websocket.js"(exports2, module2) {
    "use strict";
    var EventEmitter = require("events");
    var https = require("https");
    var http = require("http");
    var net = require("net");
    var tls = require("tls");
    var { randomBytes, createHash } = require("crypto");
    var { Duplex, Readable } = require("stream");
    var { URL: URL2 } = require("url");
    var PerMessageDeflate2 = require_permessage_deflate();
    var Receiver2 = require_receiver();
    var Sender2 = require_sender();
    var { isBlob } = require_validation();
    var {
      BINARY_TYPES,
      CLOSE_TIMEOUT,
      EMPTY_BUFFER,
      GUID,
      kForOnEventAttribute,
      kListener,
      kStatusCode,
      kWebSocket,
      NOOP
    } = require_constants();
    var {
      EventTarget: { addEventListener, removeEventListener }
    } = require_event_target();
    var { format, parse } = require_extension();
    var { toBuffer } = require_buffer_util();
    var kAborted = Symbol("kAborted");
    var protocolVersions = [8, 13];
    var readyStates = ["CONNECTING", "OPEN", "CLOSING", "CLOSED"];
    var subprotocolRegex = /^[!#$%&'*+\-.0-9A-Z^_`|a-z~]+$/;
    var WebSocket2 = class _WebSocket extends EventEmitter {
      /**
       * Create a new `WebSocket`.
       *
       * @param {(String|URL)} address The URL to which to connect
       * @param {(String|String[])} [protocols] The subprotocols
       * @param {Object} [options] Connection options
       */
      constructor(address, protocols, options) {
        super();
        this._binaryType = BINARY_TYPES[0];
        this._closeCode = 1006;
        this._closeFrameReceived = false;
        this._closeFrameSent = false;
        this._closeMessage = EMPTY_BUFFER;
        this._closeTimer = null;
        this._errorEmitted = false;
        this._extensions = {};
        this._paused = false;
        this._protocol = "";
        this._readyState = _WebSocket.CONNECTING;
        this._receiver = null;
        this._sender = null;
        this._socket = null;
        if (address !== null) {
          this._bufferedAmount = 0;
          this._isServer = false;
          this._redirects = 0;
          if (protocols === void 0) {
            protocols = [];
          } else if (!Array.isArray(protocols)) {
            if (typeof protocols === "object" && protocols !== null) {
              options = protocols;
              protocols = [];
            } else {
              protocols = [protocols];
            }
          }
          initAsClient(this, address, protocols, options);
        } else {
          this._autoPong = options.autoPong;
          this._closeTimeout = options.closeTimeout;
          this._isServer = true;
        }
      }
      /**
       * For historical reasons, the custom "nodebuffer" type is used by the default
       * instead of "blob".
       *
       * @type {String}
       */
      get binaryType() {
        return this._binaryType;
      }
      set binaryType(type) {
        if (!BINARY_TYPES.includes(type)) return;
        this._binaryType = type;
        if (this._receiver) this._receiver._binaryType = type;
      }
      /**
       * @type {Number}
       */
      get bufferedAmount() {
        if (!this._socket) return this._bufferedAmount;
        return this._socket._writableState.length + this._sender._bufferedBytes;
      }
      /**
       * @type {String}
       */
      get extensions() {
        return Object.keys(this._extensions).join();
      }
      /**
       * @type {Boolean}
       */
      get isPaused() {
        return this._paused;
      }
      /**
       * @type {Function}
       */
      /* istanbul ignore next */
      get onclose() {
        return null;
      }
      /**
       * @type {Function}
       */
      /* istanbul ignore next */
      get onerror() {
        return null;
      }
      /**
       * @type {Function}
       */
      /* istanbul ignore next */
      get onopen() {
        return null;
      }
      /**
       * @type {Function}
       */
      /* istanbul ignore next */
      get onmessage() {
        return null;
      }
      /**
       * @type {String}
       */
      get protocol() {
        return this._protocol;
      }
      /**
       * @type {Number}
       */
      get readyState() {
        return this._readyState;
      }
      /**
       * @type {String}
       */
      get url() {
        return this._url;
      }
      /**
       * Set up the socket and the internal resources.
       *
       * @param {Duplex} socket The network socket between the server and client
       * @param {Buffer} head The first packet of the upgraded stream
       * @param {Object} options Options object
       * @param {Boolean} [options.allowSynchronousEvents=false] Specifies whether
       *     any of the `'message'`, `'ping'`, and `'pong'` events can be emitted
       *     multiple times in the same tick
       * @param {Function} [options.generateMask] The function used to generate the
       *     masking key
       * @param {Number} [options.maxPayload=0] The maximum allowed message size
       * @param {Boolean} [options.skipUTF8Validation=false] Specifies whether or
       *     not to skip UTF-8 validation for text and close messages
       * @private
       */
      setSocket(socket, head, options) {
        const receiver = new Receiver2({
          allowSynchronousEvents: options.allowSynchronousEvents,
          binaryType: this.binaryType,
          extensions: this._extensions,
          isServer: this._isServer,
          maxPayload: options.maxPayload,
          skipUTF8Validation: options.skipUTF8Validation
        });
        const sender = new Sender2(socket, this._extensions, options.generateMask);
        this._receiver = receiver;
        this._sender = sender;
        this._socket = socket;
        receiver[kWebSocket] = this;
        sender[kWebSocket] = this;
        socket[kWebSocket] = this;
        receiver.on("conclude", receiverOnConclude);
        receiver.on("drain", receiverOnDrain);
        receiver.on("error", receiverOnError);
        receiver.on("message", receiverOnMessage);
        receiver.on("ping", receiverOnPing);
        receiver.on("pong", receiverOnPong);
        sender.onerror = senderOnError;
        if (socket.setTimeout) socket.setTimeout(0);
        if (socket.setNoDelay) socket.setNoDelay();
        if (head.length > 0) socket.unshift(head);
        socket.on("close", socketOnClose);
        socket.on("data", socketOnData);
        socket.on("end", socketOnEnd);
        socket.on("error", socketOnError);
        this._readyState = _WebSocket.OPEN;
        this.emit("open");
      }
      /**
       * Emit the `'close'` event.
       *
       * @private
       */
      emitClose() {
        if (!this._socket) {
          this._readyState = _WebSocket.CLOSED;
          this.emit("close", this._closeCode, this._closeMessage);
          return;
        }
        if (this._extensions[PerMessageDeflate2.extensionName]) {
          this._extensions[PerMessageDeflate2.extensionName].cleanup();
        }
        this._receiver.removeAllListeners();
        this._readyState = _WebSocket.CLOSED;
        this.emit("close", this._closeCode, this._closeMessage);
      }
      /**
       * Start a closing handshake.
       *
       *          +----------+   +-----------+   +----------+
       *     - - -|ws.close()|-->|close frame|-->|ws.close()|- - -
       *    |     +----------+   +-----------+   +----------+     |
       *          +----------+   +-----------+         |
       * CLOSING  |ws.close()|<--|close frame|<--+-----+       CLOSING
       *          +----------+   +-----------+   |
       *    |           |                        |   +---+        |
       *                +------------------------+-->|fin| - - - -
       *    |         +---+                      |   +---+
       *     - - - - -|fin|<---------------------+
       *              +---+
       *
       * @param {Number} [code] Status code explaining why the connection is closing
       * @param {(String|Buffer)} [data] The reason why the connection is
       *     closing
       * @public
       */
      close(code, data) {
        if (this.readyState === _WebSocket.CLOSED) return;
        if (this.readyState === _WebSocket.CONNECTING) {
          const msg = "WebSocket was closed before the connection was established";
          abortHandshake(this, this._req, msg);
          return;
        }
        if (this.readyState === _WebSocket.CLOSING) {
          if (this._closeFrameSent && (this._closeFrameReceived || this._receiver._writableState.errorEmitted)) {
            this._socket.end();
          }
          return;
        }
        this._readyState = _WebSocket.CLOSING;
        this._sender.close(code, data, !this._isServer, (err2) => {
          if (err2) return;
          this._closeFrameSent = true;
          if (this._closeFrameReceived || this._receiver._writableState.errorEmitted) {
            this._socket.end();
          }
        });
        setCloseTimer(this);
      }
      /**
       * Pause the socket.
       *
       * @public
       */
      pause() {
        if (this.readyState === _WebSocket.CONNECTING || this.readyState === _WebSocket.CLOSED) {
          return;
        }
        this._paused = true;
        this._socket.pause();
      }
      /**
       * Send a ping.
       *
       * @param {*} [data] The data to send
       * @param {Boolean} [mask] Indicates whether or not to mask `data`
       * @param {Function} [cb] Callback which is executed when the ping is sent
       * @public
       */
      ping(data, mask, cb) {
        if (this.readyState === _WebSocket.CONNECTING) {
          throw new Error("WebSocket is not open: readyState 0 (CONNECTING)");
        }
        if (typeof data === "function") {
          cb = data;
          data = mask = void 0;
        } else if (typeof mask === "function") {
          cb = mask;
          mask = void 0;
        }
        if (typeof data === "number") data = data.toString();
        if (this.readyState !== _WebSocket.OPEN) {
          sendAfterClose(this, data, cb);
          return;
        }
        if (mask === void 0) mask = !this._isServer;
        this._sender.ping(data || EMPTY_BUFFER, mask, cb);
      }
      /**
       * Send a pong.
       *
       * @param {*} [data] The data to send
       * @param {Boolean} [mask] Indicates whether or not to mask `data`
       * @param {Function} [cb] Callback which is executed when the pong is sent
       * @public
       */
      pong(data, mask, cb) {
        if (this.readyState === _WebSocket.CONNECTING) {
          throw new Error("WebSocket is not open: readyState 0 (CONNECTING)");
        }
        if (typeof data === "function") {
          cb = data;
          data = mask = void 0;
        } else if (typeof mask === "function") {
          cb = mask;
          mask = void 0;
        }
        if (typeof data === "number") data = data.toString();
        if (this.readyState !== _WebSocket.OPEN) {
          sendAfterClose(this, data, cb);
          return;
        }
        if (mask === void 0) mask = !this._isServer;
        this._sender.pong(data || EMPTY_BUFFER, mask, cb);
      }
      /**
       * Resume the socket.
       *
       * @public
       */
      resume() {
        if (this.readyState === _WebSocket.CONNECTING || this.readyState === _WebSocket.CLOSED) {
          return;
        }
        this._paused = false;
        if (!this._receiver._writableState.needDrain) this._socket.resume();
      }
      /**
       * Send a data message.
       *
       * @param {*} data The message to send
       * @param {Object} [options] Options object
       * @param {Boolean} [options.binary] Specifies whether `data` is binary or
       *     text
       * @param {Boolean} [options.compress] Specifies whether or not to compress
       *     `data`
       * @param {Boolean} [options.fin=true] Specifies whether the fragment is the
       *     last one
       * @param {Boolean} [options.mask] Specifies whether or not to mask `data`
       * @param {Function} [cb] Callback which is executed when data is written out
       * @public
       */
      send(data, options, cb) {
        if (this.readyState === _WebSocket.CONNECTING) {
          throw new Error("WebSocket is not open: readyState 0 (CONNECTING)");
        }
        if (typeof options === "function") {
          cb = options;
          options = {};
        }
        if (typeof data === "number") data = data.toString();
        if (this.readyState !== _WebSocket.OPEN) {
          sendAfterClose(this, data, cb);
          return;
        }
        const opts = {
          binary: typeof data !== "string",
          mask: !this._isServer,
          compress: true,
          fin: true,
          ...options
        };
        if (!this._extensions[PerMessageDeflate2.extensionName]) {
          opts.compress = false;
        }
        this._sender.send(data || EMPTY_BUFFER, opts, cb);
      }
      /**
       * Forcibly close the connection.
       *
       * @public
       */
      terminate() {
        if (this.readyState === _WebSocket.CLOSED) return;
        if (this.readyState === _WebSocket.CONNECTING) {
          const msg = "WebSocket was closed before the connection was established";
          abortHandshake(this, this._req, msg);
          return;
        }
        if (this._socket) {
          this._readyState = _WebSocket.CLOSING;
          this._socket.destroy();
        }
      }
    };
    Object.defineProperty(WebSocket2, "CONNECTING", {
      enumerable: true,
      value: readyStates.indexOf("CONNECTING")
    });
    Object.defineProperty(WebSocket2.prototype, "CONNECTING", {
      enumerable: true,
      value: readyStates.indexOf("CONNECTING")
    });
    Object.defineProperty(WebSocket2, "OPEN", {
      enumerable: true,
      value: readyStates.indexOf("OPEN")
    });
    Object.defineProperty(WebSocket2.prototype, "OPEN", {
      enumerable: true,
      value: readyStates.indexOf("OPEN")
    });
    Object.defineProperty(WebSocket2, "CLOSING", {
      enumerable: true,
      value: readyStates.indexOf("CLOSING")
    });
    Object.defineProperty(WebSocket2.prototype, "CLOSING", {
      enumerable: true,
      value: readyStates.indexOf("CLOSING")
    });
    Object.defineProperty(WebSocket2, "CLOSED", {
      enumerable: true,
      value: readyStates.indexOf("CLOSED")
    });
    Object.defineProperty(WebSocket2.prototype, "CLOSED", {
      enumerable: true,
      value: readyStates.indexOf("CLOSED")
    });
    [
      "binaryType",
      "bufferedAmount",
      "extensions",
      "isPaused",
      "protocol",
      "readyState",
      "url"
    ].forEach((property) => {
      Object.defineProperty(WebSocket2.prototype, property, { enumerable: true });
    });
    ["open", "error", "close", "message"].forEach((method) => {
      Object.defineProperty(WebSocket2.prototype, `on${method}`, {
        enumerable: true,
        get() {
          for (const listener of this.listeners(method)) {
            if (listener[kForOnEventAttribute]) return listener[kListener];
          }
          return null;
        },
        set(handler) {
          for (const listener of this.listeners(method)) {
            if (listener[kForOnEventAttribute]) {
              this.removeListener(method, listener);
              break;
            }
          }
          if (typeof handler !== "function") return;
          this.addEventListener(method, handler, {
            [kForOnEventAttribute]: true
          });
        }
      });
    });
    WebSocket2.prototype.addEventListener = addEventListener;
    WebSocket2.prototype.removeEventListener = removeEventListener;
    module2.exports = WebSocket2;
    function initAsClient(websocket, address, protocols, options) {
      const opts = {
        allowSynchronousEvents: true,
        autoPong: true,
        closeTimeout: CLOSE_TIMEOUT,
        protocolVersion: protocolVersions[1],
        maxPayload: 100 * 1024 * 1024,
        skipUTF8Validation: false,
        perMessageDeflate: true,
        followRedirects: false,
        maxRedirects: 10,
        ...options,
        socketPath: void 0,
        hostname: void 0,
        protocol: void 0,
        timeout: void 0,
        method: "GET",
        host: void 0,
        path: void 0,
        port: void 0
      };
      websocket._autoPong = opts.autoPong;
      websocket._closeTimeout = opts.closeTimeout;
      if (!protocolVersions.includes(opts.protocolVersion)) {
        throw new RangeError(
          `Unsupported protocol version: ${opts.protocolVersion} (supported versions: ${protocolVersions.join(", ")})`
        );
      }
      let parsedUrl;
      if (address instanceof URL2) {
        parsedUrl = address;
      } else {
        try {
          parsedUrl = new URL2(address);
        } catch {
          throw new SyntaxError(`Invalid URL: ${address}`);
        }
      }
      if (parsedUrl.protocol === "http:") {
        parsedUrl.protocol = "ws:";
      } else if (parsedUrl.protocol === "https:") {
        parsedUrl.protocol = "wss:";
      }
      websocket._url = parsedUrl.href;
      const isSecure = parsedUrl.protocol === "wss:";
      const isIpcUrl = parsedUrl.protocol === "ws+unix:";
      let invalidUrlMessage;
      if (parsedUrl.protocol !== "ws:" && !isSecure && !isIpcUrl) {
        invalidUrlMessage = `The URL's protocol must be one of "ws:", "wss:", "http:", "https:", or "ws+unix:"`;
      } else if (isIpcUrl && !parsedUrl.pathname) {
        invalidUrlMessage = "The URL's pathname is empty";
      } else if (parsedUrl.hash) {
        invalidUrlMessage = "The URL contains a fragment identifier";
      }
      if (invalidUrlMessage) {
        const err2 = new SyntaxError(invalidUrlMessage);
        if (websocket._redirects === 0) {
          throw err2;
        } else {
          emitErrorAndClose(websocket, err2);
          return;
        }
      }
      const defaultPort = isSecure ? 443 : 80;
      const key = randomBytes(16).toString("base64");
      const request = isSecure ? https.request : http.request;
      const protocolSet = /* @__PURE__ */ new Set();
      let perMessageDeflate;
      opts.createConnection = opts.createConnection || (isSecure ? tlsConnect : netConnect);
      opts.defaultPort = opts.defaultPort || defaultPort;
      opts.port = parsedUrl.port || defaultPort;
      opts.host = parsedUrl.hostname.startsWith("[") ? parsedUrl.hostname.slice(1, -1) : parsedUrl.hostname;
      opts.headers = {
        ...opts.headers,
        "Sec-WebSocket-Version": opts.protocolVersion,
        "Sec-WebSocket-Key": key,
        Connection: "Upgrade",
        Upgrade: "websocket"
      };
      opts.path = parsedUrl.pathname + parsedUrl.search;
      opts.timeout = opts.handshakeTimeout;
      if (opts.perMessageDeflate) {
        perMessageDeflate = new PerMessageDeflate2({
          ...opts.perMessageDeflate,
          isServer: false,
          maxPayload: opts.maxPayload
        });
        opts.headers["Sec-WebSocket-Extensions"] = format({
          [PerMessageDeflate2.extensionName]: perMessageDeflate.offer()
        });
      }
      if (protocols.length) {
        for (const protocol of protocols) {
          if (typeof protocol !== "string" || !subprotocolRegex.test(protocol) || protocolSet.has(protocol)) {
            throw new SyntaxError(
              "An invalid or duplicated subprotocol was specified"
            );
          }
          protocolSet.add(protocol);
        }
        opts.headers["Sec-WebSocket-Protocol"] = protocols.join(",");
      }
      if (opts.origin) {
        if (opts.protocolVersion < 13) {
          opts.headers["Sec-WebSocket-Origin"] = opts.origin;
        } else {
          opts.headers.Origin = opts.origin;
        }
      }
      if (parsedUrl.username || parsedUrl.password) {
        opts.auth = `${parsedUrl.username}:${parsedUrl.password}`;
      }
      if (isIpcUrl) {
        const parts = opts.path.split(":");
        opts.socketPath = parts[0];
        opts.path = parts[1];
      }
      let req;
      if (opts.followRedirects) {
        if (websocket._redirects === 0) {
          websocket._originalIpc = isIpcUrl;
          websocket._originalSecure = isSecure;
          websocket._originalHostOrSocketPath = isIpcUrl ? opts.socketPath : parsedUrl.host;
          const headers = options && options.headers;
          options = { ...options, headers: {} };
          if (headers) {
            for (const [key2, value] of Object.entries(headers)) {
              options.headers[key2.toLowerCase()] = value;
            }
          }
        } else if (websocket.listenerCount("redirect") === 0) {
          const isSameHost = isIpcUrl ? websocket._originalIpc ? opts.socketPath === websocket._originalHostOrSocketPath : false : websocket._originalIpc ? false : parsedUrl.host === websocket._originalHostOrSocketPath;
          if (!isSameHost || websocket._originalSecure && !isSecure) {
            delete opts.headers.authorization;
            delete opts.headers.cookie;
            if (!isSameHost) delete opts.headers.host;
            opts.auth = void 0;
          }
        }
        if (opts.auth && !options.headers.authorization) {
          options.headers.authorization = "Basic " + Buffer.from(opts.auth).toString("base64");
        }
        req = websocket._req = request(opts);
        if (websocket._redirects) {
          websocket.emit("redirect", websocket.url, req);
        }
      } else {
        req = websocket._req = request(opts);
      }
      if (opts.timeout) {
        req.on("timeout", () => {
          abortHandshake(websocket, req, "Opening handshake has timed out");
        });
      }
      req.on("error", (err2) => {
        if (req === null || req[kAborted]) return;
        req = websocket._req = null;
        emitErrorAndClose(websocket, err2);
      });
      req.on("response", (res) => {
        const location = res.headers.location;
        const statusCode = res.statusCode;
        if (location && opts.followRedirects && statusCode >= 300 && statusCode < 400) {
          if (++websocket._redirects > opts.maxRedirects) {
            abortHandshake(websocket, req, "Maximum redirects exceeded");
            return;
          }
          req.abort();
          let addr;
          try {
            addr = new URL2(location, address);
          } catch (e) {
            const err2 = new SyntaxError(`Invalid URL: ${location}`);
            emitErrorAndClose(websocket, err2);
            return;
          }
          initAsClient(websocket, addr, protocols, options);
        } else if (!websocket.emit("unexpected-response", req, res)) {
          abortHandshake(
            websocket,
            req,
            `Unexpected server response: ${res.statusCode}`
          );
        }
      });
      req.on("upgrade", (res, socket, head) => {
        websocket.emit("upgrade", res);
        if (websocket.readyState !== WebSocket2.CONNECTING) return;
        req = websocket._req = null;
        const upgrade = res.headers.upgrade;
        if (upgrade === void 0 || upgrade.toLowerCase() !== "websocket") {
          abortHandshake(websocket, socket, "Invalid Upgrade header");
          return;
        }
        const digest = createHash("sha1").update(key + GUID).digest("base64");
        if (res.headers["sec-websocket-accept"] !== digest) {
          abortHandshake(websocket, socket, "Invalid Sec-WebSocket-Accept header");
          return;
        }
        const serverProt = res.headers["sec-websocket-protocol"];
        let protError;
        if (serverProt !== void 0) {
          if (!protocolSet.size) {
            protError = "Server sent a subprotocol but none was requested";
          } else if (!protocolSet.has(serverProt)) {
            protError = "Server sent an invalid subprotocol";
          }
        } else if (protocolSet.size) {
          protError = "Server sent no subprotocol";
        }
        if (protError) {
          abortHandshake(websocket, socket, protError);
          return;
        }
        if (serverProt) websocket._protocol = serverProt;
        const secWebSocketExtensions = res.headers["sec-websocket-extensions"];
        if (secWebSocketExtensions !== void 0) {
          if (!perMessageDeflate) {
            const message = "Server sent a Sec-WebSocket-Extensions header but no extension was requested";
            abortHandshake(websocket, socket, message);
            return;
          }
          let extensions;
          try {
            extensions = parse(secWebSocketExtensions);
          } catch (err2) {
            const message = "Invalid Sec-WebSocket-Extensions header";
            abortHandshake(websocket, socket, message);
            return;
          }
          const extensionNames = Object.keys(extensions);
          if (extensionNames.length !== 1 || extensionNames[0] !== PerMessageDeflate2.extensionName) {
            const message = "Server indicated an extension that was not requested";
            abortHandshake(websocket, socket, message);
            return;
          }
          try {
            perMessageDeflate.accept(extensions[PerMessageDeflate2.extensionName]);
          } catch (err2) {
            const message = "Invalid Sec-WebSocket-Extensions header";
            abortHandshake(websocket, socket, message);
            return;
          }
          websocket._extensions[PerMessageDeflate2.extensionName] = perMessageDeflate;
        }
        websocket.setSocket(socket, head, {
          allowSynchronousEvents: opts.allowSynchronousEvents,
          generateMask: opts.generateMask,
          maxPayload: opts.maxPayload,
          skipUTF8Validation: opts.skipUTF8Validation
        });
      });
      if (opts.finishRequest) {
        opts.finishRequest(req, websocket);
      } else {
        req.end();
      }
    }
    function emitErrorAndClose(websocket, err2) {
      websocket._readyState = WebSocket2.CLOSING;
      websocket._errorEmitted = true;
      websocket.emit("error", err2);
      websocket.emitClose();
    }
    function netConnect(options) {
      options.path = options.socketPath;
      return net.connect(options);
    }
    function tlsConnect(options) {
      options.path = void 0;
      if (!options.servername && options.servername !== "") {
        options.servername = net.isIP(options.host) ? "" : options.host;
      }
      return tls.connect(options);
    }
    function abortHandshake(websocket, stream, message) {
      websocket._readyState = WebSocket2.CLOSING;
      const err2 = new Error(message);
      Error.captureStackTrace(err2, abortHandshake);
      if (stream.setHeader) {
        stream[kAborted] = true;
        stream.abort();
        if (stream.socket && !stream.socket.destroyed) {
          stream.socket.destroy();
        }
        process.nextTick(emitErrorAndClose, websocket, err2);
      } else {
        stream.destroy(err2);
        stream.once("error", websocket.emit.bind(websocket, "error"));
        stream.once("close", websocket.emitClose.bind(websocket));
      }
    }
    function sendAfterClose(websocket, data, cb) {
      if (data) {
        const length = isBlob(data) ? data.size : toBuffer(data).length;
        if (websocket._socket) websocket._sender._bufferedBytes += length;
        else websocket._bufferedAmount += length;
      }
      if (cb) {
        const err2 = new Error(
          `WebSocket is not open: readyState ${websocket.readyState} (${readyStates[websocket.readyState]})`
        );
        process.nextTick(cb, err2);
      }
    }
    function receiverOnConclude(code, reason) {
      const websocket = this[kWebSocket];
      websocket._closeFrameReceived = true;
      websocket._closeMessage = reason;
      websocket._closeCode = code;
      if (websocket._socket[kWebSocket] === void 0) return;
      websocket._socket.removeListener("data", socketOnData);
      process.nextTick(resume, websocket._socket);
      if (code === 1005) websocket.close();
      else websocket.close(code, reason);
    }
    function receiverOnDrain() {
      const websocket = this[kWebSocket];
      if (!websocket.isPaused) websocket._socket.resume();
    }
    function receiverOnError(err2) {
      const websocket = this[kWebSocket];
      if (websocket._socket[kWebSocket] !== void 0) {
        websocket._socket.removeListener("data", socketOnData);
        process.nextTick(resume, websocket._socket);
        websocket.close(err2[kStatusCode]);
      }
      if (!websocket._errorEmitted) {
        websocket._errorEmitted = true;
        websocket.emit("error", err2);
      }
    }
    function receiverOnFinish() {
      this[kWebSocket].emitClose();
    }
    function receiverOnMessage(data, isBinary) {
      this[kWebSocket].emit("message", data, isBinary);
    }
    function receiverOnPing(data) {
      const websocket = this[kWebSocket];
      if (websocket._autoPong) websocket.pong(data, !this._isServer, NOOP);
      websocket.emit("ping", data);
    }
    function receiverOnPong(data) {
      this[kWebSocket].emit("pong", data);
    }
    function resume(stream) {
      stream.resume();
    }
    function senderOnError(err2) {
      const websocket = this[kWebSocket];
      if (websocket.readyState === WebSocket2.CLOSED) return;
      if (websocket.readyState === WebSocket2.OPEN) {
        websocket._readyState = WebSocket2.CLOSING;
        setCloseTimer(websocket);
      }
      this._socket.end();
      if (!websocket._errorEmitted) {
        websocket._errorEmitted = true;
        websocket.emit("error", err2);
      }
    }
    function setCloseTimer(websocket) {
      websocket._closeTimer = setTimeout(
        websocket._socket.destroy.bind(websocket._socket),
        websocket._closeTimeout
      );
    }
    function socketOnClose() {
      const websocket = this[kWebSocket];
      this.removeListener("close", socketOnClose);
      this.removeListener("data", socketOnData);
      this.removeListener("end", socketOnEnd);
      websocket._readyState = WebSocket2.CLOSING;
      if (!this._readableState.endEmitted && !websocket._closeFrameReceived && !websocket._receiver._writableState.errorEmitted && this._readableState.length !== 0) {
        const chunk = this.read(this._readableState.length);
        websocket._receiver.write(chunk);
      }
      websocket._receiver.end();
      this[kWebSocket] = void 0;
      clearTimeout(websocket._closeTimer);
      if (websocket._receiver._writableState.finished || websocket._receiver._writableState.errorEmitted) {
        websocket.emitClose();
      } else {
        websocket._receiver.on("error", receiverOnFinish);
        websocket._receiver.on("finish", receiverOnFinish);
      }
    }
    function socketOnData(chunk) {
      if (!this[kWebSocket]._receiver.write(chunk)) {
        this.pause();
      }
    }
    function socketOnEnd() {
      const websocket = this[kWebSocket];
      websocket._readyState = WebSocket2.CLOSING;
      websocket._receiver.end();
      this.end();
    }
    function socketOnError() {
      const websocket = this[kWebSocket];
      this.removeListener("error", socketOnError);
      this.on("error", NOOP);
      if (websocket) {
        websocket._readyState = WebSocket2.CLOSING;
        this.destroy();
      }
    }
  }
});

// node_modules/ws/lib/stream.js
var require_stream = __commonJS({
  "node_modules/ws/lib/stream.js"(exports2, module2) {
    "use strict";
    var WebSocket2 = require_websocket();
    var { Duplex } = require("stream");
    function emitClose(stream) {
      stream.emit("close");
    }
    function duplexOnEnd() {
      if (!this.destroyed && this._writableState.finished) {
        this.destroy();
      }
    }
    function duplexOnError(err2) {
      this.removeListener("error", duplexOnError);
      this.destroy();
      if (this.listenerCount("error") === 0) {
        this.emit("error", err2);
      }
    }
    function createWebSocketStream2(ws, options) {
      let terminateOnDestroy = true;
      const duplex = new Duplex({
        ...options,
        autoDestroy: false,
        emitClose: false,
        objectMode: false,
        writableObjectMode: false
      });
      ws.on("message", function message(msg, isBinary) {
        const data = !isBinary && duplex._readableState.objectMode ? msg.toString() : msg;
        if (!duplex.push(data)) ws.pause();
      });
      ws.once("error", function error(err2) {
        if (duplex.destroyed) return;
        terminateOnDestroy = false;
        duplex.destroy(err2);
      });
      ws.once("close", function close() {
        if (duplex.destroyed) return;
        duplex.push(null);
      });
      duplex._destroy = function(err2, callback) {
        if (ws.readyState === ws.CLOSED) {
          callback(err2);
          process.nextTick(emitClose, duplex);
          return;
        }
        let called = false;
        ws.once("error", function error(err3) {
          called = true;
          callback(err3);
        });
        ws.once("close", function close() {
          if (!called) callback(err2);
          process.nextTick(emitClose, duplex);
        });
        if (terminateOnDestroy) ws.terminate();
      };
      duplex._final = function(callback) {
        if (ws.readyState === ws.CONNECTING) {
          ws.once("open", function open() {
            duplex._final(callback);
          });
          return;
        }
        if (ws._socket === null) return;
        if (ws._socket._writableState.finished) {
          callback();
          if (duplex._readableState.endEmitted) duplex.destroy();
        } else {
          ws._socket.once("finish", function finish() {
            callback();
          });
          ws.close();
        }
      };
      duplex._read = function() {
        if (ws.isPaused) ws.resume();
      };
      duplex._write = function(chunk, encoding, callback) {
        if (ws.readyState === ws.CONNECTING) {
          ws.once("open", function open() {
            duplex._write(chunk, encoding, callback);
          });
          return;
        }
        ws.send(chunk, callback);
      };
      duplex.on("end", duplexOnEnd);
      duplex.on("error", duplexOnError);
      return duplex;
    }
    module2.exports = createWebSocketStream2;
  }
});

// node_modules/ws/lib/subprotocol.js
var require_subprotocol = __commonJS({
  "node_modules/ws/lib/subprotocol.js"(exports2, module2) {
    "use strict";
    var { tokenChars } = require_validation();
    function parse(header) {
      const protocols = /* @__PURE__ */ new Set();
      let start = -1;
      let end = -1;
      let i = 0;
      for (i; i < header.length; i++) {
        const code = header.charCodeAt(i);
        if (end === -1 && tokenChars[code] === 1) {
          if (start === -1) start = i;
        } else if (i !== 0 && (code === 32 || code === 9)) {
          if (end === -1 && start !== -1) end = i;
        } else if (code === 44) {
          if (start === -1) {
            throw new SyntaxError(`Unexpected character at index ${i}`);
          }
          if (end === -1) end = i;
          const protocol2 = header.slice(start, end);
          if (protocols.has(protocol2)) {
            throw new SyntaxError(`The "${protocol2}" subprotocol is duplicated`);
          }
          protocols.add(protocol2);
          start = end = -1;
        } else {
          throw new SyntaxError(`Unexpected character at index ${i}`);
        }
      }
      if (start === -1 || end !== -1) {
        throw new SyntaxError("Unexpected end of input");
      }
      const protocol = header.slice(start, i);
      if (protocols.has(protocol)) {
        throw new SyntaxError(`The "${protocol}" subprotocol is duplicated`);
      }
      protocols.add(protocol);
      return protocols;
    }
    module2.exports = { parse };
  }
});

// node_modules/ws/lib/websocket-server.js
var require_websocket_server = __commonJS({
  "node_modules/ws/lib/websocket-server.js"(exports2, module2) {
    "use strict";
    var EventEmitter = require("events");
    var http = require("http");
    var { Duplex } = require("stream");
    var { createHash } = require("crypto");
    var extension2 = require_extension();
    var PerMessageDeflate2 = require_permessage_deflate();
    var subprotocol2 = require_subprotocol();
    var WebSocket2 = require_websocket();
    var { CLOSE_TIMEOUT, GUID, kWebSocket } = require_constants();
    var keyRegex = /^[+/0-9A-Za-z]{22}==$/;
    var RUNNING = 0;
    var CLOSING = 1;
    var CLOSED = 2;
    var WebSocketServer2 = class extends EventEmitter {
      /**
       * Create a `WebSocketServer` instance.
       *
       * @param {Object} options Configuration options
       * @param {Boolean} [options.allowSynchronousEvents=true] Specifies whether
       *     any of the `'message'`, `'ping'`, and `'pong'` events can be emitted
       *     multiple times in the same tick
       * @param {Boolean} [options.autoPong=true] Specifies whether or not to
       *     automatically send a pong in response to a ping
       * @param {Number} [options.backlog=511] The maximum length of the queue of
       *     pending connections
       * @param {Boolean} [options.clientTracking=true] Specifies whether or not to
       *     track clients
       * @param {Number} [options.closeTimeout=30000] Duration in milliseconds to
       *     wait for the closing handshake to finish after `websocket.close()` is
       *     called
       * @param {Function} [options.handleProtocols] A hook to handle protocols
       * @param {String} [options.host] The hostname where to bind the server
       * @param {Number} [options.maxPayload=104857600] The maximum allowed message
       *     size
       * @param {Boolean} [options.noServer=false] Enable no server mode
       * @param {String} [options.path] Accept only connections matching this path
       * @param {(Boolean|Object)} [options.perMessageDeflate=false] Enable/disable
       *     permessage-deflate
       * @param {Number} [options.port] The port where to bind the server
       * @param {(http.Server|https.Server)} [options.server] A pre-created HTTP/S
       *     server to use
       * @param {Boolean} [options.skipUTF8Validation=false] Specifies whether or
       *     not to skip UTF-8 validation for text and close messages
       * @param {Function} [options.verifyClient] A hook to reject connections
       * @param {Function} [options.WebSocket=WebSocket] Specifies the `WebSocket`
       *     class to use. It must be the `WebSocket` class or class that extends it
       * @param {Function} [callback] A listener for the `listening` event
       */
      constructor(options, callback) {
        super();
        options = {
          allowSynchronousEvents: true,
          autoPong: true,
          maxPayload: 100 * 1024 * 1024,
          skipUTF8Validation: false,
          perMessageDeflate: false,
          handleProtocols: null,
          clientTracking: true,
          closeTimeout: CLOSE_TIMEOUT,
          verifyClient: null,
          noServer: false,
          backlog: null,
          // use default (511 as implemented in net.js)
          server: null,
          host: null,
          path: null,
          port: null,
          WebSocket: WebSocket2,
          ...options
        };
        if (options.port == null && !options.server && !options.noServer || options.port != null && (options.server || options.noServer) || options.server && options.noServer) {
          throw new TypeError(
            'One and only one of the "port", "server", or "noServer" options must be specified'
          );
        }
        if (options.port != null) {
          this._server = http.createServer((req, res) => {
            const body = http.STATUS_CODES[426];
            res.writeHead(426, {
              "Content-Length": body.length,
              "Content-Type": "text/plain"
            });
            res.end(body);
          });
          this._server.listen(
            options.port,
            options.host,
            options.backlog,
            callback
          );
        } else if (options.server) {
          this._server = options.server;
        }
        if (this._server) {
          const emitConnection = this.emit.bind(this, "connection");
          this._removeListeners = addListeners(this._server, {
            listening: this.emit.bind(this, "listening"),
            error: this.emit.bind(this, "error"),
            upgrade: (req, socket, head) => {
              this.handleUpgrade(req, socket, head, emitConnection);
            }
          });
        }
        if (options.perMessageDeflate === true) options.perMessageDeflate = {};
        if (options.clientTracking) {
          this.clients = /* @__PURE__ */ new Set();
          this._shouldEmitClose = false;
        }
        this.options = options;
        this._state = RUNNING;
      }
      /**
       * Returns the bound address, the address family name, and port of the server
       * as reported by the operating system if listening on an IP socket.
       * If the server is listening on a pipe or UNIX domain socket, the name is
       * returned as a string.
       *
       * @return {(Object|String|null)} The address of the server
       * @public
       */
      address() {
        if (this.options.noServer) {
          throw new Error('The server is operating in "noServer" mode');
        }
        if (!this._server) return null;
        return this._server.address();
      }
      /**
       * Stop the server from accepting new connections and emit the `'close'` event
       * when all existing connections are closed.
       *
       * @param {Function} [cb] A one-time listener for the `'close'` event
       * @public
       */
      close(cb) {
        if (this._state === CLOSED) {
          if (cb) {
            this.once("close", () => {
              cb(new Error("The server is not running"));
            });
          }
          process.nextTick(emitClose, this);
          return;
        }
        if (cb) this.once("close", cb);
        if (this._state === CLOSING) return;
        this._state = CLOSING;
        if (this.options.noServer || this.options.server) {
          if (this._server) {
            this._removeListeners();
            this._removeListeners = this._server = null;
          }
          if (this.clients) {
            if (!this.clients.size) {
              process.nextTick(emitClose, this);
            } else {
              this._shouldEmitClose = true;
            }
          } else {
            process.nextTick(emitClose, this);
          }
        } else {
          const server = this._server;
          this._removeListeners();
          this._removeListeners = this._server = null;
          server.close(() => {
            emitClose(this);
          });
        }
      }
      /**
       * See if a given request should be handled by this server instance.
       *
       * @param {http.IncomingMessage} req Request object to inspect
       * @return {Boolean} `true` if the request is valid, else `false`
       * @public
       */
      shouldHandle(req) {
        if (this.options.path) {
          const index = req.url.indexOf("?");
          const pathname = index !== -1 ? req.url.slice(0, index) : req.url;
          if (pathname !== this.options.path) return false;
        }
        return true;
      }
      /**
       * Handle a HTTP Upgrade request.
       *
       * @param {http.IncomingMessage} req The request object
       * @param {Duplex} socket The network socket between the server and client
       * @param {Buffer} head The first packet of the upgraded stream
       * @param {Function} cb Callback
       * @public
       */
      handleUpgrade(req, socket, head, cb) {
        socket.on("error", socketOnError);
        const key = req.headers["sec-websocket-key"];
        const upgrade = req.headers.upgrade;
        const version = +req.headers["sec-websocket-version"];
        if (req.method !== "GET") {
          const message = "Invalid HTTP method";
          abortHandshakeOrEmitwsClientError(this, req, socket, 405, message);
          return;
        }
        if (upgrade === void 0 || upgrade.toLowerCase() !== "websocket") {
          const message = "Invalid Upgrade header";
          abortHandshakeOrEmitwsClientError(this, req, socket, 400, message);
          return;
        }
        if (key === void 0 || !keyRegex.test(key)) {
          const message = "Missing or invalid Sec-WebSocket-Key header";
          abortHandshakeOrEmitwsClientError(this, req, socket, 400, message);
          return;
        }
        if (version !== 13 && version !== 8) {
          const message = "Missing or invalid Sec-WebSocket-Version header";
          abortHandshakeOrEmitwsClientError(this, req, socket, 400, message, {
            "Sec-WebSocket-Version": "13, 8"
          });
          return;
        }
        if (!this.shouldHandle(req)) {
          abortHandshake(socket, 400);
          return;
        }
        const secWebSocketProtocol = req.headers["sec-websocket-protocol"];
        let protocols = /* @__PURE__ */ new Set();
        if (secWebSocketProtocol !== void 0) {
          try {
            protocols = subprotocol2.parse(secWebSocketProtocol);
          } catch (err2) {
            const message = "Invalid Sec-WebSocket-Protocol header";
            abortHandshakeOrEmitwsClientError(this, req, socket, 400, message);
            return;
          }
        }
        const secWebSocketExtensions = req.headers["sec-websocket-extensions"];
        const extensions = {};
        if (this.options.perMessageDeflate && secWebSocketExtensions !== void 0) {
          const perMessageDeflate = new PerMessageDeflate2({
            ...this.options.perMessageDeflate,
            isServer: true,
            maxPayload: this.options.maxPayload
          });
          try {
            const offers = extension2.parse(secWebSocketExtensions);
            if (offers[PerMessageDeflate2.extensionName]) {
              perMessageDeflate.accept(offers[PerMessageDeflate2.extensionName]);
              extensions[PerMessageDeflate2.extensionName] = perMessageDeflate;
            }
          } catch (err2) {
            const message = "Invalid or unacceptable Sec-WebSocket-Extensions header";
            abortHandshakeOrEmitwsClientError(this, req, socket, 400, message);
            return;
          }
        }
        if (this.options.verifyClient) {
          const info = {
            origin: req.headers[`${version === 8 ? "sec-websocket-origin" : "origin"}`],
            secure: !!(req.socket.authorized || req.socket.encrypted),
            req
          };
          if (this.options.verifyClient.length === 2) {
            this.options.verifyClient(info, (verified, code, message, headers) => {
              if (!verified) {
                return abortHandshake(socket, code || 401, message, headers);
              }
              this.completeUpgrade(
                extensions,
                key,
                protocols,
                req,
                socket,
                head,
                cb
              );
            });
            return;
          }
          if (!this.options.verifyClient(info)) return abortHandshake(socket, 401);
        }
        this.completeUpgrade(extensions, key, protocols, req, socket, head, cb);
      }
      /**
       * Upgrade the connection to WebSocket.
       *
       * @param {Object} extensions The accepted extensions
       * @param {String} key The value of the `Sec-WebSocket-Key` header
       * @param {Set} protocols The subprotocols
       * @param {http.IncomingMessage} req The request object
       * @param {Duplex} socket The network socket between the server and client
       * @param {Buffer} head The first packet of the upgraded stream
       * @param {Function} cb Callback
       * @throws {Error} If called more than once with the same socket
       * @private
       */
      completeUpgrade(extensions, key, protocols, req, socket, head, cb) {
        if (!socket.readable || !socket.writable) return socket.destroy();
        if (socket[kWebSocket]) {
          throw new Error(
            "server.handleUpgrade() was called more than once with the same socket, possibly due to a misconfiguration"
          );
        }
        if (this._state > RUNNING) return abortHandshake(socket, 503);
        const digest = createHash("sha1").update(key + GUID).digest("base64");
        const headers = [
          "HTTP/1.1 101 Switching Protocols",
          "Upgrade: websocket",
          "Connection: Upgrade",
          `Sec-WebSocket-Accept: ${digest}`
        ];
        const ws = new this.options.WebSocket(null, void 0, this.options);
        if (protocols.size) {
          const protocol = this.options.handleProtocols ? this.options.handleProtocols(protocols, req) : protocols.values().next().value;
          if (protocol) {
            headers.push(`Sec-WebSocket-Protocol: ${protocol}`);
            ws._protocol = protocol;
          }
        }
        if (extensions[PerMessageDeflate2.extensionName]) {
          const params = extensions[PerMessageDeflate2.extensionName].params;
          const value = extension2.format({
            [PerMessageDeflate2.extensionName]: [params]
          });
          headers.push(`Sec-WebSocket-Extensions: ${value}`);
          ws._extensions = extensions;
        }
        this.emit("headers", headers, req);
        socket.write(headers.concat("\r\n").join("\r\n"));
        socket.removeListener("error", socketOnError);
        ws.setSocket(socket, head, {
          allowSynchronousEvents: this.options.allowSynchronousEvents,
          maxPayload: this.options.maxPayload,
          skipUTF8Validation: this.options.skipUTF8Validation
        });
        if (this.clients) {
          this.clients.add(ws);
          ws.on("close", () => {
            this.clients.delete(ws);
            if (this._shouldEmitClose && !this.clients.size) {
              process.nextTick(emitClose, this);
            }
          });
        }
        cb(ws, req);
      }
    };
    module2.exports = WebSocketServer2;
    function addListeners(server, map) {
      for (const event of Object.keys(map)) server.on(event, map[event]);
      return function removeListeners() {
        for (const event of Object.keys(map)) {
          server.removeListener(event, map[event]);
        }
      };
    }
    function emitClose(server) {
      server._state = CLOSED;
      server.emit("close");
    }
    function socketOnError() {
      this.destroy();
    }
    function abortHandshake(socket, code, message, headers) {
      message = message || http.STATUS_CODES[code];
      headers = {
        Connection: "close",
        "Content-Type": "text/html",
        "Content-Length": Buffer.byteLength(message),
        ...headers
      };
      socket.once("finish", socket.destroy);
      socket.end(
        `HTTP/1.1 ${code} ${http.STATUS_CODES[code]}\r
` + Object.keys(headers).map((h) => `${h}: ${headers[h]}`).join("\r\n") + "\r\n\r\n" + message
      );
    }
    function abortHandshakeOrEmitwsClientError(server, req, socket, code, message, headers) {
      if (server.listenerCount("wsClientError")) {
        const err2 = new Error(message);
        Error.captureStackTrace(err2, abortHandshakeOrEmitwsClientError);
        server.emit("wsClientError", err2, socket, req);
      } else {
        abortHandshake(socket, code, message, headers);
      }
    }
  }
});

// node_modules/pngjs/lib/chunkstream.js
var require_chunkstream = __commonJS({
  "node_modules/pngjs/lib/chunkstream.js"(exports2, module2) {
    "use strict";
    var util = require("util");
    var Stream = require("stream");
    var ChunkStream = module2.exports = function() {
      Stream.call(this);
      this._buffers = [];
      this._buffered = 0;
      this._reads = [];
      this._paused = false;
      this._encoding = "utf8";
      this.writable = true;
    };
    util.inherits(ChunkStream, Stream);
    ChunkStream.prototype.read = function(length, callback) {
      this._reads.push({
        length: Math.abs(length),
        // if length < 0 then at most this length
        allowLess: length < 0,
        func: callback
      });
      process.nextTick(
        function() {
          this._process();
          if (this._paused && this._reads && this._reads.length > 0) {
            this._paused = false;
            this.emit("drain");
          }
        }.bind(this)
      );
    };
    ChunkStream.prototype.write = function(data, encoding) {
      if (!this.writable) {
        this.emit("error", new Error("Stream not writable"));
        return false;
      }
      let dataBuffer;
      if (Buffer.isBuffer(data)) {
        dataBuffer = data;
      } else {
        dataBuffer = Buffer.from(data, encoding || this._encoding);
      }
      this._buffers.push(dataBuffer);
      this._buffered += dataBuffer.length;
      this._process();
      if (this._reads && this._reads.length === 0) {
        this._paused = true;
      }
      return this.writable && !this._paused;
    };
    ChunkStream.prototype.end = function(data, encoding) {
      if (data) {
        this.write(data, encoding);
      }
      this.writable = false;
      if (!this._buffers) {
        return;
      }
      if (this._buffers.length === 0) {
        this._end();
      } else {
        this._buffers.push(null);
        this._process();
      }
    };
    ChunkStream.prototype.destroySoon = ChunkStream.prototype.end;
    ChunkStream.prototype._end = function() {
      if (this._reads.length > 0) {
        this.emit("error", new Error("Unexpected end of input"));
      }
      this.destroy();
    };
    ChunkStream.prototype.destroy = function() {
      if (!this._buffers) {
        return;
      }
      this.writable = false;
      this._reads = null;
      this._buffers = null;
      this.emit("close");
    };
    ChunkStream.prototype._processReadAllowingLess = function(read) {
      this._reads.shift();
      let smallerBuf = this._buffers[0];
      if (smallerBuf.length > read.length) {
        this._buffered -= read.length;
        this._buffers[0] = smallerBuf.slice(read.length);
        read.func.call(this, smallerBuf.slice(0, read.length));
      } else {
        this._buffered -= smallerBuf.length;
        this._buffers.shift();
        read.func.call(this, smallerBuf);
      }
    };
    ChunkStream.prototype._processRead = function(read) {
      this._reads.shift();
      let pos = 0;
      let count = 0;
      let data = Buffer.alloc(read.length);
      while (pos < read.length) {
        let buf = this._buffers[count++];
        let len = Math.min(buf.length, read.length - pos);
        buf.copy(data, pos, 0, len);
        pos += len;
        if (len !== buf.length) {
          this._buffers[--count] = buf.slice(len);
        }
      }
      if (count > 0) {
        this._buffers.splice(0, count);
      }
      this._buffered -= read.length;
      read.func.call(this, data);
    };
    ChunkStream.prototype._process = function() {
      try {
        while (this._buffered > 0 && this._reads && this._reads.length > 0) {
          let read = this._reads[0];
          if (read.allowLess) {
            this._processReadAllowingLess(read);
          } else if (this._buffered >= read.length) {
            this._processRead(read);
          } else {
            break;
          }
        }
        if (this._buffers && !this.writable) {
          this._end();
        }
      } catch (ex) {
        this.emit("error", ex);
      }
    };
  }
});

// node_modules/pngjs/lib/interlace.js
var require_interlace = __commonJS({
  "node_modules/pngjs/lib/interlace.js"(exports2) {
    "use strict";
    var imagePasses = [
      {
        // pass 1 - 1px
        x: [0],
        y: [0]
      },
      {
        // pass 2 - 1px
        x: [4],
        y: [0]
      },
      {
        // pass 3 - 2px
        x: [0, 4],
        y: [4]
      },
      {
        // pass 4 - 4px
        x: [2, 6],
        y: [0, 4]
      },
      {
        // pass 5 - 8px
        x: [0, 2, 4, 6],
        y: [2, 6]
      },
      {
        // pass 6 - 16px
        x: [1, 3, 5, 7],
        y: [0, 2, 4, 6]
      },
      {
        // pass 7 - 32px
        x: [0, 1, 2, 3, 4, 5, 6, 7],
        y: [1, 3, 5, 7]
      }
    ];
    exports2.getImagePasses = function(width, height) {
      let images = [];
      let xLeftOver = width % 8;
      let yLeftOver = height % 8;
      let xRepeats = (width - xLeftOver) / 8;
      let yRepeats = (height - yLeftOver) / 8;
      for (let i = 0; i < imagePasses.length; i++) {
        let pass = imagePasses[i];
        let passWidth = xRepeats * pass.x.length;
        let passHeight = yRepeats * pass.y.length;
        for (let j = 0; j < pass.x.length; j++) {
          if (pass.x[j] < xLeftOver) {
            passWidth++;
          } else {
            break;
          }
        }
        for (let j = 0; j < pass.y.length; j++) {
          if (pass.y[j] < yLeftOver) {
            passHeight++;
          } else {
            break;
          }
        }
        if (passWidth > 0 && passHeight > 0) {
          images.push({ width: passWidth, height: passHeight, index: i });
        }
      }
      return images;
    };
    exports2.getInterlaceIterator = function(width) {
      return function(x, y, pass) {
        let outerXLeftOver = x % imagePasses[pass].x.length;
        let outerX = (x - outerXLeftOver) / imagePasses[pass].x.length * 8 + imagePasses[pass].x[outerXLeftOver];
        let outerYLeftOver = y % imagePasses[pass].y.length;
        let outerY = (y - outerYLeftOver) / imagePasses[pass].y.length * 8 + imagePasses[pass].y[outerYLeftOver];
        return outerX * 4 + outerY * width * 4;
      };
    };
  }
});

// node_modules/pngjs/lib/paeth-predictor.js
var require_paeth_predictor = __commonJS({
  "node_modules/pngjs/lib/paeth-predictor.js"(exports2, module2) {
    "use strict";
    module2.exports = function paethPredictor(left, above, upLeft) {
      let paeth = left + above - upLeft;
      let pLeft = Math.abs(paeth - left);
      let pAbove = Math.abs(paeth - above);
      let pUpLeft = Math.abs(paeth - upLeft);
      if (pLeft <= pAbove && pLeft <= pUpLeft) {
        return left;
      }
      if (pAbove <= pUpLeft) {
        return above;
      }
      return upLeft;
    };
  }
});

// node_modules/pngjs/lib/filter-parse.js
var require_filter_parse = __commonJS({
  "node_modules/pngjs/lib/filter-parse.js"(exports2, module2) {
    "use strict";
    var interlaceUtils = require_interlace();
    var paethPredictor = require_paeth_predictor();
    function getByteWidth(width, bpp, depth) {
      let byteWidth = width * bpp;
      if (depth !== 8) {
        byteWidth = Math.ceil(byteWidth / (8 / depth));
      }
      return byteWidth;
    }
    var Filter = module2.exports = function(bitmapInfo, dependencies) {
      let width = bitmapInfo.width;
      let height = bitmapInfo.height;
      let interlace = bitmapInfo.interlace;
      let bpp = bitmapInfo.bpp;
      let depth = bitmapInfo.depth;
      this.read = dependencies.read;
      this.write = dependencies.write;
      this.complete = dependencies.complete;
      this._imageIndex = 0;
      this._images = [];
      if (interlace) {
        let passes = interlaceUtils.getImagePasses(width, height);
        for (let i = 0; i < passes.length; i++) {
          this._images.push({
            byteWidth: getByteWidth(passes[i].width, bpp, depth),
            height: passes[i].height,
            lineIndex: 0
          });
        }
      } else {
        this._images.push({
          byteWidth: getByteWidth(width, bpp, depth),
          height,
          lineIndex: 0
        });
      }
      if (depth === 8) {
        this._xComparison = bpp;
      } else if (depth === 16) {
        this._xComparison = bpp * 2;
      } else {
        this._xComparison = 1;
      }
    };
    Filter.prototype.start = function() {
      this.read(
        this._images[this._imageIndex].byteWidth + 1,
        this._reverseFilterLine.bind(this)
      );
    };
    Filter.prototype._unFilterType1 = function(rawData, unfilteredLine, byteWidth) {
      let xComparison = this._xComparison;
      let xBiggerThan = xComparison - 1;
      for (let x = 0; x < byteWidth; x++) {
        let rawByte = rawData[1 + x];
        let f1Left = x > xBiggerThan ? unfilteredLine[x - xComparison] : 0;
        unfilteredLine[x] = rawByte + f1Left;
      }
    };
    Filter.prototype._unFilterType2 = function(rawData, unfilteredLine, byteWidth) {
      let lastLine = this._lastLine;
      for (let x = 0; x < byteWidth; x++) {
        let rawByte = rawData[1 + x];
        let f2Up = lastLine ? lastLine[x] : 0;
        unfilteredLine[x] = rawByte + f2Up;
      }
    };
    Filter.prototype._unFilterType3 = function(rawData, unfilteredLine, byteWidth) {
      let xComparison = this._xComparison;
      let xBiggerThan = xComparison - 1;
      let lastLine = this._lastLine;
      for (let x = 0; x < byteWidth; x++) {
        let rawByte = rawData[1 + x];
        let f3Up = lastLine ? lastLine[x] : 0;
        let f3Left = x > xBiggerThan ? unfilteredLine[x - xComparison] : 0;
        let f3Add = Math.floor((f3Left + f3Up) / 2);
        unfilteredLine[x] = rawByte + f3Add;
      }
    };
    Filter.prototype._unFilterType4 = function(rawData, unfilteredLine, byteWidth) {
      let xComparison = this._xComparison;
      let xBiggerThan = xComparison - 1;
      let lastLine = this._lastLine;
      for (let x = 0; x < byteWidth; x++) {
        let rawByte = rawData[1 + x];
        let f4Up = lastLine ? lastLine[x] : 0;
        let f4Left = x > xBiggerThan ? unfilteredLine[x - xComparison] : 0;
        let f4UpLeft = x > xBiggerThan && lastLine ? lastLine[x - xComparison] : 0;
        let f4Add = paethPredictor(f4Left, f4Up, f4UpLeft);
        unfilteredLine[x] = rawByte + f4Add;
      }
    };
    Filter.prototype._reverseFilterLine = function(rawData) {
      let filter = rawData[0];
      let unfilteredLine;
      let currentImage = this._images[this._imageIndex];
      let byteWidth = currentImage.byteWidth;
      if (filter === 0) {
        unfilteredLine = rawData.slice(1, byteWidth + 1);
      } else {
        unfilteredLine = Buffer.alloc(byteWidth);
        switch (filter) {
          case 1:
            this._unFilterType1(rawData, unfilteredLine, byteWidth);
            break;
          case 2:
            this._unFilterType2(rawData, unfilteredLine, byteWidth);
            break;
          case 3:
            this._unFilterType3(rawData, unfilteredLine, byteWidth);
            break;
          case 4:
            this._unFilterType4(rawData, unfilteredLine, byteWidth);
            break;
          default:
            throw new Error("Unrecognised filter type - " + filter);
        }
      }
      this.write(unfilteredLine);
      currentImage.lineIndex++;
      if (currentImage.lineIndex >= currentImage.height) {
        this._lastLine = null;
        this._imageIndex++;
        currentImage = this._images[this._imageIndex];
      } else {
        this._lastLine = unfilteredLine;
      }
      if (currentImage) {
        this.read(currentImage.byteWidth + 1, this._reverseFilterLine.bind(this));
      } else {
        this._lastLine = null;
        this.complete();
      }
    };
  }
});

// node_modules/pngjs/lib/filter-parse-async.js
var require_filter_parse_async = __commonJS({
  "node_modules/pngjs/lib/filter-parse-async.js"(exports2, module2) {
    "use strict";
    var util = require("util");
    var ChunkStream = require_chunkstream();
    var Filter = require_filter_parse();
    var FilterAsync = module2.exports = function(bitmapInfo) {
      ChunkStream.call(this);
      let buffers = [];
      let that = this;
      this._filter = new Filter(bitmapInfo, {
        read: this.read.bind(this),
        write: function(buffer) {
          buffers.push(buffer);
        },
        complete: function() {
          that.emit("complete", Buffer.concat(buffers));
        }
      });
      this._filter.start();
    };
    util.inherits(FilterAsync, ChunkStream);
  }
});

// node_modules/pngjs/lib/constants.js
var require_constants2 = __commonJS({
  "node_modules/pngjs/lib/constants.js"(exports2, module2) {
    "use strict";
    module2.exports = {
      PNG_SIGNATURE: [137, 80, 78, 71, 13, 10, 26, 10],
      TYPE_IHDR: 1229472850,
      TYPE_IEND: 1229278788,
      TYPE_IDAT: 1229209940,
      TYPE_PLTE: 1347179589,
      TYPE_tRNS: 1951551059,
      // eslint-disable-line camelcase
      TYPE_gAMA: 1732332865,
      // eslint-disable-line camelcase
      // color-type bits
      COLORTYPE_GRAYSCALE: 0,
      COLORTYPE_PALETTE: 1,
      COLORTYPE_COLOR: 2,
      COLORTYPE_ALPHA: 4,
      // e.g. grayscale and alpha
      // color-type combinations
      COLORTYPE_PALETTE_COLOR: 3,
      COLORTYPE_COLOR_ALPHA: 6,
      COLORTYPE_TO_BPP_MAP: {
        0: 1,
        2: 3,
        3: 1,
        4: 2,
        6: 4
      },
      GAMMA_DIVISION: 1e5
    };
  }
});

// node_modules/pngjs/lib/crc.js
var require_crc = __commonJS({
  "node_modules/pngjs/lib/crc.js"(exports2, module2) {
    "use strict";
    var crcTable = [];
    (function() {
      for (let i = 0; i < 256; i++) {
        let currentCrc = i;
        for (let j = 0; j < 8; j++) {
          if (currentCrc & 1) {
            currentCrc = 3988292384 ^ currentCrc >>> 1;
          } else {
            currentCrc = currentCrc >>> 1;
          }
        }
        crcTable[i] = currentCrc;
      }
    })();
    var CrcCalculator = module2.exports = function() {
      this._crc = -1;
    };
    CrcCalculator.prototype.write = function(data) {
      for (let i = 0; i < data.length; i++) {
        this._crc = crcTable[(this._crc ^ data[i]) & 255] ^ this._crc >>> 8;
      }
      return true;
    };
    CrcCalculator.prototype.crc32 = function() {
      return this._crc ^ -1;
    };
    CrcCalculator.crc32 = function(buf) {
      let crc = -1;
      for (let i = 0; i < buf.length; i++) {
        crc = crcTable[(crc ^ buf[i]) & 255] ^ crc >>> 8;
      }
      return crc ^ -1;
    };
  }
});

// node_modules/pngjs/lib/parser.js
var require_parser = __commonJS({
  "node_modules/pngjs/lib/parser.js"(exports2, module2) {
    "use strict";
    var constants = require_constants2();
    var CrcCalculator = require_crc();
    var Parser = module2.exports = function(options, dependencies) {
      this._options = options;
      options.checkCRC = options.checkCRC !== false;
      this._hasIHDR = false;
      this._hasIEND = false;
      this._emittedHeadersFinished = false;
      this._palette = [];
      this._colorType = 0;
      this._chunks = {};
      this._chunks[constants.TYPE_IHDR] = this._handleIHDR.bind(this);
      this._chunks[constants.TYPE_IEND] = this._handleIEND.bind(this);
      this._chunks[constants.TYPE_IDAT] = this._handleIDAT.bind(this);
      this._chunks[constants.TYPE_PLTE] = this._handlePLTE.bind(this);
      this._chunks[constants.TYPE_tRNS] = this._handleTRNS.bind(this);
      this._chunks[constants.TYPE_gAMA] = this._handleGAMA.bind(this);
      this.read = dependencies.read;
      this.error = dependencies.error;
      this.metadata = dependencies.metadata;
      this.gamma = dependencies.gamma;
      this.transColor = dependencies.transColor;
      this.palette = dependencies.palette;
      this.parsed = dependencies.parsed;
      this.inflateData = dependencies.inflateData;
      this.finished = dependencies.finished;
      this.simpleTransparency = dependencies.simpleTransparency;
      this.headersFinished = dependencies.headersFinished || function() {
      };
    };
    Parser.prototype.start = function() {
      this.read(constants.PNG_SIGNATURE.length, this._parseSignature.bind(this));
    };
    Parser.prototype._parseSignature = function(data) {
      let signature = constants.PNG_SIGNATURE;
      for (let i = 0; i < signature.length; i++) {
        if (data[i] !== signature[i]) {
          this.error(new Error("Invalid file signature"));
          return;
        }
      }
      this.read(8, this._parseChunkBegin.bind(this));
    };
    Parser.prototype._parseChunkBegin = function(data) {
      let length = data.readUInt32BE(0);
      let type = data.readUInt32BE(4);
      let name = "";
      for (let i = 4; i < 8; i++) {
        name += String.fromCharCode(data[i]);
      }
      let ancillary = Boolean(data[4] & 32);
      if (!this._hasIHDR && type !== constants.TYPE_IHDR) {
        this.error(new Error("Expected IHDR on beggining"));
        return;
      }
      this._crc = new CrcCalculator();
      this._crc.write(Buffer.from(name));
      if (this._chunks[type]) {
        return this._chunks[type](length);
      }
      if (!ancillary) {
        this.error(new Error("Unsupported critical chunk type " + name));
        return;
      }
      this.read(length + 4, this._skipChunk.bind(this));
    };
    Parser.prototype._skipChunk = function() {
      this.read(8, this._parseChunkBegin.bind(this));
    };
    Parser.prototype._handleChunkEnd = function() {
      this.read(4, this._parseChunkEnd.bind(this));
    };
    Parser.prototype._parseChunkEnd = function(data) {
      let fileCrc = data.readInt32BE(0);
      let calcCrc = this._crc.crc32();
      if (this._options.checkCRC && calcCrc !== fileCrc) {
        this.error(new Error("Crc error - " + fileCrc + " - " + calcCrc));
        return;
      }
      if (!this._hasIEND) {
        this.read(8, this._parseChunkBegin.bind(this));
      }
    };
    Parser.prototype._handleIHDR = function(length) {
      this.read(length, this._parseIHDR.bind(this));
    };
    Parser.prototype._parseIHDR = function(data) {
      this._crc.write(data);
      let width = data.readUInt32BE(0);
      let height = data.readUInt32BE(4);
      let depth = data[8];
      let colorType = data[9];
      let compr = data[10];
      let filter = data[11];
      let interlace = data[12];
      if (depth !== 8 && depth !== 4 && depth !== 2 && depth !== 1 && depth !== 16) {
        this.error(new Error("Unsupported bit depth " + depth));
        return;
      }
      if (!(colorType in constants.COLORTYPE_TO_BPP_MAP)) {
        this.error(new Error("Unsupported color type"));
        return;
      }
      if (compr !== 0) {
        this.error(new Error("Unsupported compression method"));
        return;
      }
      if (filter !== 0) {
        this.error(new Error("Unsupported filter method"));
        return;
      }
      if (interlace !== 0 && interlace !== 1) {
        this.error(new Error("Unsupported interlace method"));
        return;
      }
      this._colorType = colorType;
      let bpp = constants.COLORTYPE_TO_BPP_MAP[this._colorType];
      this._hasIHDR = true;
      this.metadata({
        width,
        height,
        depth,
        interlace: Boolean(interlace),
        palette: Boolean(colorType & constants.COLORTYPE_PALETTE),
        color: Boolean(colorType & constants.COLORTYPE_COLOR),
        alpha: Boolean(colorType & constants.COLORTYPE_ALPHA),
        bpp,
        colorType
      });
      this._handleChunkEnd();
    };
    Parser.prototype._handlePLTE = function(length) {
      this.read(length, this._parsePLTE.bind(this));
    };
    Parser.prototype._parsePLTE = function(data) {
      this._crc.write(data);
      let entries = Math.floor(data.length / 3);
      for (let i = 0; i < entries; i++) {
        this._palette.push([data[i * 3], data[i * 3 + 1], data[i * 3 + 2], 255]);
      }
      this.palette(this._palette);
      this._handleChunkEnd();
    };
    Parser.prototype._handleTRNS = function(length) {
      this.simpleTransparency();
      this.read(length, this._parseTRNS.bind(this));
    };
    Parser.prototype._parseTRNS = function(data) {
      this._crc.write(data);
      if (this._colorType === constants.COLORTYPE_PALETTE_COLOR) {
        if (this._palette.length === 0) {
          this.error(new Error("Transparency chunk must be after palette"));
          return;
        }
        if (data.length > this._palette.length) {
          this.error(new Error("More transparent colors than palette size"));
          return;
        }
        for (let i = 0; i < data.length; i++) {
          this._palette[i][3] = data[i];
        }
        this.palette(this._palette);
      }
      if (this._colorType === constants.COLORTYPE_GRAYSCALE) {
        this.transColor([data.readUInt16BE(0)]);
      }
      if (this._colorType === constants.COLORTYPE_COLOR) {
        this.transColor([
          data.readUInt16BE(0),
          data.readUInt16BE(2),
          data.readUInt16BE(4)
        ]);
      }
      this._handleChunkEnd();
    };
    Parser.prototype._handleGAMA = function(length) {
      this.read(length, this._parseGAMA.bind(this));
    };
    Parser.prototype._parseGAMA = function(data) {
      this._crc.write(data);
      this.gamma(data.readUInt32BE(0) / constants.GAMMA_DIVISION);
      this._handleChunkEnd();
    };
    Parser.prototype._handleIDAT = function(length) {
      if (!this._emittedHeadersFinished) {
        this._emittedHeadersFinished = true;
        this.headersFinished();
      }
      this.read(-length, this._parseIDAT.bind(this, length));
    };
    Parser.prototype._parseIDAT = function(length, data) {
      this._crc.write(data);
      if (this._colorType === constants.COLORTYPE_PALETTE_COLOR && this._palette.length === 0) {
        throw new Error("Expected palette not found");
      }
      this.inflateData(data);
      let leftOverLength = length - data.length;
      if (leftOverLength > 0) {
        this._handleIDAT(leftOverLength);
      } else {
        this._handleChunkEnd();
      }
    };
    Parser.prototype._handleIEND = function(length) {
      this.read(length, this._parseIEND.bind(this));
    };
    Parser.prototype._parseIEND = function(data) {
      this._crc.write(data);
      this._hasIEND = true;
      this._handleChunkEnd();
      if (this.finished) {
        this.finished();
      }
    };
  }
});

// node_modules/pngjs/lib/bitmapper.js
var require_bitmapper = __commonJS({
  "node_modules/pngjs/lib/bitmapper.js"(exports2) {
    "use strict";
    var interlaceUtils = require_interlace();
    var pixelBppMapper = [
      // 0 - dummy entry
      function() {
      },
      // 1 - L
      // 0: 0, 1: 0, 2: 0, 3: 0xff
      function(pxData, data, pxPos, rawPos) {
        if (rawPos === data.length) {
          throw new Error("Ran out of data");
        }
        let pixel = data[rawPos];
        pxData[pxPos] = pixel;
        pxData[pxPos + 1] = pixel;
        pxData[pxPos + 2] = pixel;
        pxData[pxPos + 3] = 255;
      },
      // 2 - LA
      // 0: 0, 1: 0, 2: 0, 3: 1
      function(pxData, data, pxPos, rawPos) {
        if (rawPos + 1 >= data.length) {
          throw new Error("Ran out of data");
        }
        let pixel = data[rawPos];
        pxData[pxPos] = pixel;
        pxData[pxPos + 1] = pixel;
        pxData[pxPos + 2] = pixel;
        pxData[pxPos + 3] = data[rawPos + 1];
      },
      // 3 - RGB
      // 0: 0, 1: 1, 2: 2, 3: 0xff
      function(pxData, data, pxPos, rawPos) {
        if (rawPos + 2 >= data.length) {
          throw new Error("Ran out of data");
        }
        pxData[pxPos] = data[rawPos];
        pxData[pxPos + 1] = data[rawPos + 1];
        pxData[pxPos + 2] = data[rawPos + 2];
        pxData[pxPos + 3] = 255;
      },
      // 4 - RGBA
      // 0: 0, 1: 1, 2: 2, 3: 3
      function(pxData, data, pxPos, rawPos) {
        if (rawPos + 3 >= data.length) {
          throw new Error("Ran out of data");
        }
        pxData[pxPos] = data[rawPos];
        pxData[pxPos + 1] = data[rawPos + 1];
        pxData[pxPos + 2] = data[rawPos + 2];
        pxData[pxPos + 3] = data[rawPos + 3];
      }
    ];
    var pixelBppCustomMapper = [
      // 0 - dummy entry
      function() {
      },
      // 1 - L
      // 0: 0, 1: 0, 2: 0, 3: 0xff
      function(pxData, pixelData, pxPos, maxBit) {
        let pixel = pixelData[0];
        pxData[pxPos] = pixel;
        pxData[pxPos + 1] = pixel;
        pxData[pxPos + 2] = pixel;
        pxData[pxPos + 3] = maxBit;
      },
      // 2 - LA
      // 0: 0, 1: 0, 2: 0, 3: 1
      function(pxData, pixelData, pxPos) {
        let pixel = pixelData[0];
        pxData[pxPos] = pixel;
        pxData[pxPos + 1] = pixel;
        pxData[pxPos + 2] = pixel;
        pxData[pxPos + 3] = pixelData[1];
      },
      // 3 - RGB
      // 0: 0, 1: 1, 2: 2, 3: 0xff
      function(pxData, pixelData, pxPos, maxBit) {
        pxData[pxPos] = pixelData[0];
        pxData[pxPos + 1] = pixelData[1];
        pxData[pxPos + 2] = pixelData[2];
        pxData[pxPos + 3] = maxBit;
      },
      // 4 - RGBA
      // 0: 0, 1: 1, 2: 2, 3: 3
      function(pxData, pixelData, pxPos) {
        pxData[pxPos] = pixelData[0];
        pxData[pxPos + 1] = pixelData[1];
        pxData[pxPos + 2] = pixelData[2];
        pxData[pxPos + 3] = pixelData[3];
      }
    ];
    function bitRetriever(data, depth) {
      let leftOver = [];
      let i = 0;
      function split() {
        if (i === data.length) {
          throw new Error("Ran out of data");
        }
        let byte = data[i];
        i++;
        let byte8, byte7, byte6, byte5, byte4, byte3, byte2, byte1;
        switch (depth) {
          default:
            throw new Error("unrecognised depth");
          case 16:
            byte2 = data[i];
            i++;
            leftOver.push((byte << 8) + byte2);
            break;
          case 4:
            byte2 = byte & 15;
            byte1 = byte >> 4;
            leftOver.push(byte1, byte2);
            break;
          case 2:
            byte4 = byte & 3;
            byte3 = byte >> 2 & 3;
            byte2 = byte >> 4 & 3;
            byte1 = byte >> 6 & 3;
            leftOver.push(byte1, byte2, byte3, byte4);
            break;
          case 1:
            byte8 = byte & 1;
            byte7 = byte >> 1 & 1;
            byte6 = byte >> 2 & 1;
            byte5 = byte >> 3 & 1;
            byte4 = byte >> 4 & 1;
            byte3 = byte >> 5 & 1;
            byte2 = byte >> 6 & 1;
            byte1 = byte >> 7 & 1;
            leftOver.push(byte1, byte2, byte3, byte4, byte5, byte6, byte7, byte8);
            break;
        }
      }
      return {
        get: function(count) {
          while (leftOver.length < count) {
            split();
          }
          let returner = leftOver.slice(0, count);
          leftOver = leftOver.slice(count);
          return returner;
        },
        resetAfterLine: function() {
          leftOver.length = 0;
        },
        end: function() {
          if (i !== data.length) {
            throw new Error("extra data found");
          }
        }
      };
    }
    function mapImage8Bit(image, pxData, getPxPos, bpp, data, rawPos) {
      let imageWidth = image.width;
      let imageHeight = image.height;
      let imagePass = image.index;
      for (let y = 0; y < imageHeight; y++) {
        for (let x = 0; x < imageWidth; x++) {
          let pxPos = getPxPos(x, y, imagePass);
          pixelBppMapper[bpp](pxData, data, pxPos, rawPos);
          rawPos += bpp;
        }
      }
      return rawPos;
    }
    function mapImageCustomBit(image, pxData, getPxPos, bpp, bits, maxBit) {
      let imageWidth = image.width;
      let imageHeight = image.height;
      let imagePass = image.index;
      for (let y = 0; y < imageHeight; y++) {
        for (let x = 0; x < imageWidth; x++) {
          let pixelData = bits.get(bpp);
          let pxPos = getPxPos(x, y, imagePass);
          pixelBppCustomMapper[bpp](pxData, pixelData, pxPos, maxBit);
        }
        bits.resetAfterLine();
      }
    }
    exports2.dataToBitMap = function(data, bitmapInfo) {
      let width = bitmapInfo.width;
      let height = bitmapInfo.height;
      let depth = bitmapInfo.depth;
      let bpp = bitmapInfo.bpp;
      let interlace = bitmapInfo.interlace;
      let bits;
      if (depth !== 8) {
        bits = bitRetriever(data, depth);
      }
      let pxData;
      if (depth <= 8) {
        pxData = Buffer.alloc(width * height * 4);
      } else {
        pxData = new Uint16Array(width * height * 4);
      }
      let maxBit = Math.pow(2, depth) - 1;
      let rawPos = 0;
      let images;
      let getPxPos;
      if (interlace) {
        images = interlaceUtils.getImagePasses(width, height);
        getPxPos = interlaceUtils.getInterlaceIterator(width, height);
      } else {
        let nonInterlacedPxPos = 0;
        getPxPos = function() {
          let returner = nonInterlacedPxPos;
          nonInterlacedPxPos += 4;
          return returner;
        };
        images = [{ width, height }];
      }
      for (let imageIndex = 0; imageIndex < images.length; imageIndex++) {
        if (depth === 8) {
          rawPos = mapImage8Bit(
            images[imageIndex],
            pxData,
            getPxPos,
            bpp,
            data,
            rawPos
          );
        } else {
          mapImageCustomBit(
            images[imageIndex],
            pxData,
            getPxPos,
            bpp,
            bits,
            maxBit
          );
        }
      }
      if (depth === 8) {
        if (rawPos !== data.length) {
          throw new Error("extra data found");
        }
      } else {
        bits.end();
      }
      return pxData;
    };
  }
});

// node_modules/pngjs/lib/format-normaliser.js
var require_format_normaliser = __commonJS({
  "node_modules/pngjs/lib/format-normaliser.js"(exports2, module2) {
    "use strict";
    function dePalette(indata, outdata, width, height, palette) {
      let pxPos = 0;
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          let color = palette[indata[pxPos]];
          if (!color) {
            throw new Error("index " + indata[pxPos] + " not in palette");
          }
          for (let i = 0; i < 4; i++) {
            outdata[pxPos + i] = color[i];
          }
          pxPos += 4;
        }
      }
    }
    function replaceTransparentColor(indata, outdata, width, height, transColor) {
      let pxPos = 0;
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          let makeTrans = false;
          if (transColor.length === 1) {
            if (transColor[0] === indata[pxPos]) {
              makeTrans = true;
            }
          } else if (transColor[0] === indata[pxPos] && transColor[1] === indata[pxPos + 1] && transColor[2] === indata[pxPos + 2]) {
            makeTrans = true;
          }
          if (makeTrans) {
            for (let i = 0; i < 4; i++) {
              outdata[pxPos + i] = 0;
            }
          }
          pxPos += 4;
        }
      }
    }
    function scaleDepth(indata, outdata, width, height, depth) {
      let maxOutSample = 255;
      let maxInSample = Math.pow(2, depth) - 1;
      let pxPos = 0;
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          for (let i = 0; i < 4; i++) {
            outdata[pxPos + i] = Math.floor(
              indata[pxPos + i] * maxOutSample / maxInSample + 0.5
            );
          }
          pxPos += 4;
        }
      }
    }
    module2.exports = function(indata, imageData, skipRescale = false) {
      let depth = imageData.depth;
      let width = imageData.width;
      let height = imageData.height;
      let colorType = imageData.colorType;
      let transColor = imageData.transColor;
      let palette = imageData.palette;
      let outdata = indata;
      if (colorType === 3) {
        dePalette(indata, outdata, width, height, palette);
      } else {
        if (transColor) {
          replaceTransparentColor(indata, outdata, width, height, transColor);
        }
        if (depth !== 8 && !skipRescale) {
          if (depth === 16) {
            outdata = Buffer.alloc(width * height * 4);
          }
          scaleDepth(indata, outdata, width, height, depth);
        }
      }
      return outdata;
    };
  }
});

// node_modules/pngjs/lib/parser-async.js
var require_parser_async = __commonJS({
  "node_modules/pngjs/lib/parser-async.js"(exports2, module2) {
    "use strict";
    var util = require("util");
    var zlib = require("zlib");
    var ChunkStream = require_chunkstream();
    var FilterAsync = require_filter_parse_async();
    var Parser = require_parser();
    var bitmapper = require_bitmapper();
    var formatNormaliser = require_format_normaliser();
    var ParserAsync = module2.exports = function(options) {
      ChunkStream.call(this);
      this._parser = new Parser(options, {
        read: this.read.bind(this),
        error: this._handleError.bind(this),
        metadata: this._handleMetaData.bind(this),
        gamma: this.emit.bind(this, "gamma"),
        palette: this._handlePalette.bind(this),
        transColor: this._handleTransColor.bind(this),
        finished: this._finished.bind(this),
        inflateData: this._inflateData.bind(this),
        simpleTransparency: this._simpleTransparency.bind(this),
        headersFinished: this._headersFinished.bind(this)
      });
      this._options = options;
      this.writable = true;
      this._parser.start();
    };
    util.inherits(ParserAsync, ChunkStream);
    ParserAsync.prototype._handleError = function(err2) {
      this.emit("error", err2);
      this.writable = false;
      this.destroy();
      if (this._inflate && this._inflate.destroy) {
        this._inflate.destroy();
      }
      if (this._filter) {
        this._filter.destroy();
        this._filter.on("error", function() {
        });
      }
      this.errord = true;
    };
    ParserAsync.prototype._inflateData = function(data) {
      if (!this._inflate) {
        if (this._bitmapInfo.interlace) {
          this._inflate = zlib.createInflate();
          this._inflate.on("error", this.emit.bind(this, "error"));
          this._filter.on("complete", this._complete.bind(this));
          this._inflate.pipe(this._filter);
        } else {
          let rowSize = (this._bitmapInfo.width * this._bitmapInfo.bpp * this._bitmapInfo.depth + 7 >> 3) + 1;
          let imageSize = rowSize * this._bitmapInfo.height;
          let chunkSize = Math.max(imageSize, zlib.Z_MIN_CHUNK);
          this._inflate = zlib.createInflate({ chunkSize });
          let leftToInflate = imageSize;
          let emitError = this.emit.bind(this, "error");
          this._inflate.on("error", function(err2) {
            if (!leftToInflate) {
              return;
            }
            emitError(err2);
          });
          this._filter.on("complete", this._complete.bind(this));
          let filterWrite = this._filter.write.bind(this._filter);
          this._inflate.on("data", function(chunk) {
            if (!leftToInflate) {
              return;
            }
            if (chunk.length > leftToInflate) {
              chunk = chunk.slice(0, leftToInflate);
            }
            leftToInflate -= chunk.length;
            filterWrite(chunk);
          });
          this._inflate.on("end", this._filter.end.bind(this._filter));
        }
      }
      this._inflate.write(data);
    };
    ParserAsync.prototype._handleMetaData = function(metaData) {
      this._metaData = metaData;
      this._bitmapInfo = Object.create(metaData);
      this._filter = new FilterAsync(this._bitmapInfo);
    };
    ParserAsync.prototype._handleTransColor = function(transColor) {
      this._bitmapInfo.transColor = transColor;
    };
    ParserAsync.prototype._handlePalette = function(palette) {
      this._bitmapInfo.palette = palette;
    };
    ParserAsync.prototype._simpleTransparency = function() {
      this._metaData.alpha = true;
    };
    ParserAsync.prototype._headersFinished = function() {
      this.emit("metadata", this._metaData);
    };
    ParserAsync.prototype._finished = function() {
      if (this.errord) {
        return;
      }
      if (!this._inflate) {
        this.emit("error", "No Inflate block");
      } else {
        this._inflate.end();
      }
    };
    ParserAsync.prototype._complete = function(filteredData) {
      if (this.errord) {
        return;
      }
      let normalisedBitmapData;
      try {
        let bitmapData = bitmapper.dataToBitMap(filteredData, this._bitmapInfo);
        normalisedBitmapData = formatNormaliser(
          bitmapData,
          this._bitmapInfo,
          this._options.skipRescale
        );
        bitmapData = null;
      } catch (ex) {
        this._handleError(ex);
        return;
      }
      this.emit("parsed", normalisedBitmapData);
    };
  }
});

// node_modules/pngjs/lib/bitpacker.js
var require_bitpacker = __commonJS({
  "node_modules/pngjs/lib/bitpacker.js"(exports2, module2) {
    "use strict";
    var constants = require_constants2();
    module2.exports = function(dataIn, width, height, options) {
      let outHasAlpha = [constants.COLORTYPE_COLOR_ALPHA, constants.COLORTYPE_ALPHA].indexOf(
        options.colorType
      ) !== -1;
      if (options.colorType === options.inputColorType) {
        let bigEndian = function() {
          let buffer = new ArrayBuffer(2);
          new DataView(buffer).setInt16(
            0,
            256,
            true
            /* littleEndian */
          );
          return new Int16Array(buffer)[0] !== 256;
        }();
        if (options.bitDepth === 8 || options.bitDepth === 16 && bigEndian) {
          return dataIn;
        }
      }
      let data = options.bitDepth !== 16 ? dataIn : new Uint16Array(dataIn.buffer);
      let maxValue = 255;
      let inBpp = constants.COLORTYPE_TO_BPP_MAP[options.inputColorType];
      if (inBpp === 4 && !options.inputHasAlpha) {
        inBpp = 3;
      }
      let outBpp = constants.COLORTYPE_TO_BPP_MAP[options.colorType];
      if (options.bitDepth === 16) {
        maxValue = 65535;
        outBpp *= 2;
      }
      let outData = Buffer.alloc(width * height * outBpp);
      let inIndex = 0;
      let outIndex = 0;
      let bgColor = options.bgColor || {};
      if (bgColor.red === void 0) {
        bgColor.red = maxValue;
      }
      if (bgColor.green === void 0) {
        bgColor.green = maxValue;
      }
      if (bgColor.blue === void 0) {
        bgColor.blue = maxValue;
      }
      function getRGBA() {
        let red;
        let green;
        let blue;
        let alpha = maxValue;
        switch (options.inputColorType) {
          case constants.COLORTYPE_COLOR_ALPHA:
            alpha = data[inIndex + 3];
            red = data[inIndex];
            green = data[inIndex + 1];
            blue = data[inIndex + 2];
            break;
          case constants.COLORTYPE_COLOR:
            red = data[inIndex];
            green = data[inIndex + 1];
            blue = data[inIndex + 2];
            break;
          case constants.COLORTYPE_ALPHA:
            alpha = data[inIndex + 1];
            red = data[inIndex];
            green = red;
            blue = red;
            break;
          case constants.COLORTYPE_GRAYSCALE:
            red = data[inIndex];
            green = red;
            blue = red;
            break;
          default:
            throw new Error(
              "input color type:" + options.inputColorType + " is not supported at present"
            );
        }
        if (options.inputHasAlpha) {
          if (!outHasAlpha) {
            alpha /= maxValue;
            red = Math.min(
              Math.max(Math.round((1 - alpha) * bgColor.red + alpha * red), 0),
              maxValue
            );
            green = Math.min(
              Math.max(Math.round((1 - alpha) * bgColor.green + alpha * green), 0),
              maxValue
            );
            blue = Math.min(
              Math.max(Math.round((1 - alpha) * bgColor.blue + alpha * blue), 0),
              maxValue
            );
          }
        }
        return { red, green, blue, alpha };
      }
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          let rgba = getRGBA(data, inIndex);
          switch (options.colorType) {
            case constants.COLORTYPE_COLOR_ALPHA:
            case constants.COLORTYPE_COLOR:
              if (options.bitDepth === 8) {
                outData[outIndex] = rgba.red;
                outData[outIndex + 1] = rgba.green;
                outData[outIndex + 2] = rgba.blue;
                if (outHasAlpha) {
                  outData[outIndex + 3] = rgba.alpha;
                }
              } else {
                outData.writeUInt16BE(rgba.red, outIndex);
                outData.writeUInt16BE(rgba.green, outIndex + 2);
                outData.writeUInt16BE(rgba.blue, outIndex + 4);
                if (outHasAlpha) {
                  outData.writeUInt16BE(rgba.alpha, outIndex + 6);
                }
              }
              break;
            case constants.COLORTYPE_ALPHA:
            case constants.COLORTYPE_GRAYSCALE: {
              let grayscale = (rgba.red + rgba.green + rgba.blue) / 3;
              if (options.bitDepth === 8) {
                outData[outIndex] = grayscale;
                if (outHasAlpha) {
                  outData[outIndex + 1] = rgba.alpha;
                }
              } else {
                outData.writeUInt16BE(grayscale, outIndex);
                if (outHasAlpha) {
                  outData.writeUInt16BE(rgba.alpha, outIndex + 2);
                }
              }
              break;
            }
            default:
              throw new Error("unrecognised color Type " + options.colorType);
          }
          inIndex += inBpp;
          outIndex += outBpp;
        }
      }
      return outData;
    };
  }
});

// node_modules/pngjs/lib/filter-pack.js
var require_filter_pack = __commonJS({
  "node_modules/pngjs/lib/filter-pack.js"(exports2, module2) {
    "use strict";
    var paethPredictor = require_paeth_predictor();
    function filterNone(pxData, pxPos, byteWidth, rawData, rawPos) {
      for (let x = 0; x < byteWidth; x++) {
        rawData[rawPos + x] = pxData[pxPos + x];
      }
    }
    function filterSumNone(pxData, pxPos, byteWidth) {
      let sum = 0;
      let length = pxPos + byteWidth;
      for (let i = pxPos; i < length; i++) {
        sum += Math.abs(pxData[i]);
      }
      return sum;
    }
    function filterSub(pxData, pxPos, byteWidth, rawData, rawPos, bpp) {
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let val = pxData[pxPos + x] - left;
        rawData[rawPos + x] = val;
      }
    }
    function filterSumSub(pxData, pxPos, byteWidth, bpp) {
      let sum = 0;
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let val = pxData[pxPos + x] - left;
        sum += Math.abs(val);
      }
      return sum;
    }
    function filterUp(pxData, pxPos, byteWidth, rawData, rawPos) {
      for (let x = 0; x < byteWidth; x++) {
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let val = pxData[pxPos + x] - up;
        rawData[rawPos + x] = val;
      }
    }
    function filterSumUp(pxData, pxPos, byteWidth) {
      let sum = 0;
      let length = pxPos + byteWidth;
      for (let x = pxPos; x < length; x++) {
        let up = pxPos > 0 ? pxData[x - byteWidth] : 0;
        let val = pxData[x] - up;
        sum += Math.abs(val);
      }
      return sum;
    }
    function filterAvg(pxData, pxPos, byteWidth, rawData, rawPos, bpp) {
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let val = pxData[pxPos + x] - (left + up >> 1);
        rawData[rawPos + x] = val;
      }
    }
    function filterSumAvg(pxData, pxPos, byteWidth, bpp) {
      let sum = 0;
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let val = pxData[pxPos + x] - (left + up >> 1);
        sum += Math.abs(val);
      }
      return sum;
    }
    function filterPaeth(pxData, pxPos, byteWidth, rawData, rawPos, bpp) {
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let upleft = pxPos > 0 && x >= bpp ? pxData[pxPos + x - (byteWidth + bpp)] : 0;
        let val = pxData[pxPos + x] - paethPredictor(left, up, upleft);
        rawData[rawPos + x] = val;
      }
    }
    function filterSumPaeth(pxData, pxPos, byteWidth, bpp) {
      let sum = 0;
      for (let x = 0; x < byteWidth; x++) {
        let left = x >= bpp ? pxData[pxPos + x - bpp] : 0;
        let up = pxPos > 0 ? pxData[pxPos + x - byteWidth] : 0;
        let upleft = pxPos > 0 && x >= bpp ? pxData[pxPos + x - (byteWidth + bpp)] : 0;
        let val = pxData[pxPos + x] - paethPredictor(left, up, upleft);
        sum += Math.abs(val);
      }
      return sum;
    }
    var filters = {
      0: filterNone,
      1: filterSub,
      2: filterUp,
      3: filterAvg,
      4: filterPaeth
    };
    var filterSums = {
      0: filterSumNone,
      1: filterSumSub,
      2: filterSumUp,
      3: filterSumAvg,
      4: filterSumPaeth
    };
    module2.exports = function(pxData, width, height, options, bpp) {
      let filterTypes;
      if (!("filterType" in options) || options.filterType === -1) {
        filterTypes = [0, 1, 2, 3, 4];
      } else if (typeof options.filterType === "number") {
        filterTypes = [options.filterType];
      } else {
        throw new Error("unrecognised filter types");
      }
      if (options.bitDepth === 16) {
        bpp *= 2;
      }
      let byteWidth = width * bpp;
      let rawPos = 0;
      let pxPos = 0;
      let rawData = Buffer.alloc((byteWidth + 1) * height);
      let sel = filterTypes[0];
      for (let y = 0; y < height; y++) {
        if (filterTypes.length > 1) {
          let min = Infinity;
          for (let i = 0; i < filterTypes.length; i++) {
            let sum = filterSums[filterTypes[i]](pxData, pxPos, byteWidth, bpp);
            if (sum < min) {
              sel = filterTypes[i];
              min = sum;
            }
          }
        }
        rawData[rawPos] = sel;
        rawPos++;
        filters[sel](pxData, pxPos, byteWidth, rawData, rawPos, bpp);
        rawPos += byteWidth;
        pxPos += byteWidth;
      }
      return rawData;
    };
  }
});

// node_modules/pngjs/lib/packer.js
var require_packer = __commonJS({
  "node_modules/pngjs/lib/packer.js"(exports2, module2) {
    "use strict";
    var constants = require_constants2();
    var CrcStream = require_crc();
    var bitPacker = require_bitpacker();
    var filter = require_filter_pack();
    var zlib = require("zlib");
    var Packer = module2.exports = function(options) {
      this._options = options;
      options.deflateChunkSize = options.deflateChunkSize || 32 * 1024;
      options.deflateLevel = options.deflateLevel != null ? options.deflateLevel : 9;
      options.deflateStrategy = options.deflateStrategy != null ? options.deflateStrategy : 3;
      options.inputHasAlpha = options.inputHasAlpha != null ? options.inputHasAlpha : true;
      options.deflateFactory = options.deflateFactory || zlib.createDeflate;
      options.bitDepth = options.bitDepth || 8;
      options.colorType = typeof options.colorType === "number" ? options.colorType : constants.COLORTYPE_COLOR_ALPHA;
      options.inputColorType = typeof options.inputColorType === "number" ? options.inputColorType : constants.COLORTYPE_COLOR_ALPHA;
      if ([
        constants.COLORTYPE_GRAYSCALE,
        constants.COLORTYPE_COLOR,
        constants.COLORTYPE_COLOR_ALPHA,
        constants.COLORTYPE_ALPHA
      ].indexOf(options.colorType) === -1) {
        throw new Error(
          "option color type:" + options.colorType + " is not supported at present"
        );
      }
      if ([
        constants.COLORTYPE_GRAYSCALE,
        constants.COLORTYPE_COLOR,
        constants.COLORTYPE_COLOR_ALPHA,
        constants.COLORTYPE_ALPHA
      ].indexOf(options.inputColorType) === -1) {
        throw new Error(
          "option input color type:" + options.inputColorType + " is not supported at present"
        );
      }
      if (options.bitDepth !== 8 && options.bitDepth !== 16) {
        throw new Error(
          "option bit depth:" + options.bitDepth + " is not supported at present"
        );
      }
    };
    Packer.prototype.getDeflateOptions = function() {
      return {
        chunkSize: this._options.deflateChunkSize,
        level: this._options.deflateLevel,
        strategy: this._options.deflateStrategy
      };
    };
    Packer.prototype.createDeflate = function() {
      return this._options.deflateFactory(this.getDeflateOptions());
    };
    Packer.prototype.filterData = function(data, width, height) {
      let packedData = bitPacker(data, width, height, this._options);
      let bpp = constants.COLORTYPE_TO_BPP_MAP[this._options.colorType];
      let filteredData = filter(packedData, width, height, this._options, bpp);
      return filteredData;
    };
    Packer.prototype._packChunk = function(type, data) {
      let len = data ? data.length : 0;
      let buf = Buffer.alloc(len + 12);
      buf.writeUInt32BE(len, 0);
      buf.writeUInt32BE(type, 4);
      if (data) {
        data.copy(buf, 8);
      }
      buf.writeInt32BE(
        CrcStream.crc32(buf.slice(4, buf.length - 4)),
        buf.length - 4
      );
      return buf;
    };
    Packer.prototype.packGAMA = function(gamma) {
      let buf = Buffer.alloc(4);
      buf.writeUInt32BE(Math.floor(gamma * constants.GAMMA_DIVISION), 0);
      return this._packChunk(constants.TYPE_gAMA, buf);
    };
    Packer.prototype.packIHDR = function(width, height) {
      let buf = Buffer.alloc(13);
      buf.writeUInt32BE(width, 0);
      buf.writeUInt32BE(height, 4);
      buf[8] = this._options.bitDepth;
      buf[9] = this._options.colorType;
      buf[10] = 0;
      buf[11] = 0;
      buf[12] = 0;
      return this._packChunk(constants.TYPE_IHDR, buf);
    };
    Packer.prototype.packIDAT = function(data) {
      return this._packChunk(constants.TYPE_IDAT, data);
    };
    Packer.prototype.packIEND = function() {
      return this._packChunk(constants.TYPE_IEND, null);
    };
  }
});

// node_modules/pngjs/lib/packer-async.js
var require_packer_async = __commonJS({
  "node_modules/pngjs/lib/packer-async.js"(exports2, module2) {
    "use strict";
    var util = require("util");
    var Stream = require("stream");
    var constants = require_constants2();
    var Packer = require_packer();
    var PackerAsync = module2.exports = function(opt) {
      Stream.call(this);
      let options = opt || {};
      this._packer = new Packer(options);
      this._deflate = this._packer.createDeflate();
      this.readable = true;
    };
    util.inherits(PackerAsync, Stream);
    PackerAsync.prototype.pack = function(data, width, height, gamma) {
      this.emit("data", Buffer.from(constants.PNG_SIGNATURE));
      this.emit("data", this._packer.packIHDR(width, height));
      if (gamma) {
        this.emit("data", this._packer.packGAMA(gamma));
      }
      let filteredData = this._packer.filterData(data, width, height);
      this._deflate.on("error", this.emit.bind(this, "error"));
      this._deflate.on(
        "data",
        function(compressedData) {
          this.emit("data", this._packer.packIDAT(compressedData));
        }.bind(this)
      );
      this._deflate.on(
        "end",
        function() {
          this.emit("data", this._packer.packIEND());
          this.emit("end");
        }.bind(this)
      );
      this._deflate.end(filteredData);
    };
  }
});

// node_modules/pngjs/lib/sync-inflate.js
var require_sync_inflate = __commonJS({
  "node_modules/pngjs/lib/sync-inflate.js"(exports2, module2) {
    "use strict";
    var assert = require("assert").ok;
    var zlib = require("zlib");
    var util = require("util");
    var kMaxLength = require("buffer").kMaxLength;
    function Inflate(opts) {
      if (!(this instanceof Inflate)) {
        return new Inflate(opts);
      }
      if (opts && opts.chunkSize < zlib.Z_MIN_CHUNK) {
        opts.chunkSize = zlib.Z_MIN_CHUNK;
      }
      zlib.Inflate.call(this, opts);
      this._offset = this._offset === void 0 ? this._outOffset : this._offset;
      this._buffer = this._buffer || this._outBuffer;
      if (opts && opts.maxLength != null) {
        this._maxLength = opts.maxLength;
      }
    }
    function createInflate(opts) {
      return new Inflate(opts);
    }
    function _close(engine, callback) {
      if (callback) {
        process.nextTick(callback);
      }
      if (!engine._handle) {
        return;
      }
      engine._handle.close();
      engine._handle = null;
    }
    Inflate.prototype._processChunk = function(chunk, flushFlag, asyncCb) {
      if (typeof asyncCb === "function") {
        return zlib.Inflate._processChunk.call(this, chunk, flushFlag, asyncCb);
      }
      let self = this;
      let availInBefore = chunk && chunk.length;
      let availOutBefore = this._chunkSize - this._offset;
      let leftToInflate = this._maxLength;
      let inOff = 0;
      let buffers = [];
      let nread = 0;
      let error;
      this.on("error", function(err2) {
        error = err2;
      });
      function handleChunk(availInAfter, availOutAfter) {
        if (self._hadError) {
          return;
        }
        let have = availOutBefore - availOutAfter;
        assert(have >= 0, "have should not go down");
        if (have > 0) {
          let out = self._buffer.slice(self._offset, self._offset + have);
          self._offset += have;
          if (out.length > leftToInflate) {
            out = out.slice(0, leftToInflate);
          }
          buffers.push(out);
          nread += out.length;
          leftToInflate -= out.length;
          if (leftToInflate === 0) {
            return false;
          }
        }
        if (availOutAfter === 0 || self._offset >= self._chunkSize) {
          availOutBefore = self._chunkSize;
          self._offset = 0;
          self._buffer = Buffer.allocUnsafe(self._chunkSize);
        }
        if (availOutAfter === 0) {
          inOff += availInBefore - availInAfter;
          availInBefore = availInAfter;
          return true;
        }
        return false;
      }
      assert(this._handle, "zlib binding closed");
      let res;
      do {
        res = this._handle.writeSync(
          flushFlag,
          chunk,
          // in
          inOff,
          // in_off
          availInBefore,
          // in_len
          this._buffer,
          // out
          this._offset,
          //out_off
          availOutBefore
        );
        res = res || this._writeState;
      } while (!this._hadError && handleChunk(res[0], res[1]));
      if (this._hadError) {
        throw error;
      }
      if (nread >= kMaxLength) {
        _close(this);
        throw new RangeError(
          "Cannot create final Buffer. It would be larger than 0x" + kMaxLength.toString(16) + " bytes"
        );
      }
      let buf = Buffer.concat(buffers, nread);
      _close(this);
      return buf;
    };
    util.inherits(Inflate, zlib.Inflate);
    function zlibBufferSync(engine, buffer) {
      if (typeof buffer === "string") {
        buffer = Buffer.from(buffer);
      }
      if (!(buffer instanceof Buffer)) {
        throw new TypeError("Not a string or buffer");
      }
      let flushFlag = engine._finishFlushFlag;
      if (flushFlag == null) {
        flushFlag = zlib.Z_FINISH;
      }
      return engine._processChunk(buffer, flushFlag);
    }
    function inflateSync(buffer, opts) {
      return zlibBufferSync(new Inflate(opts), buffer);
    }
    module2.exports = exports2 = inflateSync;
    exports2.Inflate = Inflate;
    exports2.createInflate = createInflate;
    exports2.inflateSync = inflateSync;
  }
});

// node_modules/pngjs/lib/sync-reader.js
var require_sync_reader = __commonJS({
  "node_modules/pngjs/lib/sync-reader.js"(exports2, module2) {
    "use strict";
    var SyncReader = module2.exports = function(buffer) {
      this._buffer = buffer;
      this._reads = [];
    };
    SyncReader.prototype.read = function(length, callback) {
      this._reads.push({
        length: Math.abs(length),
        // if length < 0 then at most this length
        allowLess: length < 0,
        func: callback
      });
    };
    SyncReader.prototype.process = function() {
      while (this._reads.length > 0 && this._buffer.length) {
        let read = this._reads[0];
        if (this._buffer.length && (this._buffer.length >= read.length || read.allowLess)) {
          this._reads.shift();
          let buf = this._buffer;
          this._buffer = buf.slice(read.length);
          read.func.call(this, buf.slice(0, read.length));
        } else {
          break;
        }
      }
      if (this._reads.length > 0) {
        throw new Error("There are some read requests waitng on finished stream");
      }
      if (this._buffer.length > 0) {
        throw new Error("unrecognised content at end of stream");
      }
    };
  }
});

// node_modules/pngjs/lib/filter-parse-sync.js
var require_filter_parse_sync = __commonJS({
  "node_modules/pngjs/lib/filter-parse-sync.js"(exports2) {
    "use strict";
    var SyncReader = require_sync_reader();
    var Filter = require_filter_parse();
    exports2.process = function(inBuffer, bitmapInfo) {
      let outBuffers = [];
      let reader = new SyncReader(inBuffer);
      let filter = new Filter(bitmapInfo, {
        read: reader.read.bind(reader),
        write: function(bufferPart) {
          outBuffers.push(bufferPart);
        },
        complete: function() {
        }
      });
      filter.start();
      reader.process();
      return Buffer.concat(outBuffers);
    };
  }
});

// node_modules/pngjs/lib/parser-sync.js
var require_parser_sync = __commonJS({
  "node_modules/pngjs/lib/parser-sync.js"(exports2, module2) {
    "use strict";
    var hasSyncZlib = true;
    var zlib = require("zlib");
    var inflateSync = require_sync_inflate();
    if (!zlib.deflateSync) {
      hasSyncZlib = false;
    }
    var SyncReader = require_sync_reader();
    var FilterSync = require_filter_parse_sync();
    var Parser = require_parser();
    var bitmapper = require_bitmapper();
    var formatNormaliser = require_format_normaliser();
    module2.exports = function(buffer, options) {
      if (!hasSyncZlib) {
        throw new Error(
          "To use the sync capability of this library in old node versions, please pin pngjs to v2.3.0"
        );
      }
      let err2;
      function handleError(_err_) {
        err2 = _err_;
      }
      let metaData;
      function handleMetaData(_metaData_) {
        metaData = _metaData_;
      }
      function handleTransColor(transColor) {
        metaData.transColor = transColor;
      }
      function handlePalette(palette) {
        metaData.palette = palette;
      }
      function handleSimpleTransparency() {
        metaData.alpha = true;
      }
      let gamma;
      function handleGamma(_gamma_) {
        gamma = _gamma_;
      }
      let inflateDataList = [];
      function handleInflateData(inflatedData2) {
        inflateDataList.push(inflatedData2);
      }
      let reader = new SyncReader(buffer);
      let parser = new Parser(options, {
        read: reader.read.bind(reader),
        error: handleError,
        metadata: handleMetaData,
        gamma: handleGamma,
        palette: handlePalette,
        transColor: handleTransColor,
        inflateData: handleInflateData,
        simpleTransparency: handleSimpleTransparency
      });
      parser.start();
      reader.process();
      if (err2) {
        throw err2;
      }
      let inflateData = Buffer.concat(inflateDataList);
      inflateDataList.length = 0;
      let inflatedData;
      if (metaData.interlace) {
        inflatedData = zlib.inflateSync(inflateData);
      } else {
        let rowSize = (metaData.width * metaData.bpp * metaData.depth + 7 >> 3) + 1;
        let imageSize = rowSize * metaData.height;
        inflatedData = inflateSync(inflateData, {
          chunkSize: imageSize,
          maxLength: imageSize
        });
      }
      inflateData = null;
      if (!inflatedData || !inflatedData.length) {
        throw new Error("bad png - invalid inflate data response");
      }
      let unfilteredData = FilterSync.process(inflatedData, metaData);
      inflateData = null;
      let bitmapData = bitmapper.dataToBitMap(unfilteredData, metaData);
      unfilteredData = null;
      let normalisedBitmapData = formatNormaliser(
        bitmapData,
        metaData,
        options.skipRescale
      );
      metaData.data = normalisedBitmapData;
      metaData.gamma = gamma || 0;
      return metaData;
    };
  }
});

// node_modules/pngjs/lib/packer-sync.js
var require_packer_sync = __commonJS({
  "node_modules/pngjs/lib/packer-sync.js"(exports2, module2) {
    "use strict";
    var hasSyncZlib = true;
    var zlib = require("zlib");
    if (!zlib.deflateSync) {
      hasSyncZlib = false;
    }
    var constants = require_constants2();
    var Packer = require_packer();
    module2.exports = function(metaData, opt) {
      if (!hasSyncZlib) {
        throw new Error(
          "To use the sync capability of this library in old node versions, please pin pngjs to v2.3.0"
        );
      }
      let options = opt || {};
      let packer = new Packer(options);
      let chunks = [];
      chunks.push(Buffer.from(constants.PNG_SIGNATURE));
      chunks.push(packer.packIHDR(metaData.width, metaData.height));
      if (metaData.gamma) {
        chunks.push(packer.packGAMA(metaData.gamma));
      }
      let filteredData = packer.filterData(
        metaData.data,
        metaData.width,
        metaData.height
      );
      let compressedData = zlib.deflateSync(
        filteredData,
        packer.getDeflateOptions()
      );
      filteredData = null;
      if (!compressedData || !compressedData.length) {
        throw new Error("bad png - invalid compressed data response");
      }
      chunks.push(packer.packIDAT(compressedData));
      chunks.push(packer.packIEND());
      return Buffer.concat(chunks);
    };
  }
});

// node_modules/pngjs/lib/png-sync.js
var require_png_sync = __commonJS({
  "node_modules/pngjs/lib/png-sync.js"(exports2) {
    "use strict";
    var parse = require_parser_sync();
    var pack = require_packer_sync();
    exports2.read = function(buffer, options) {
      return parse(buffer, options || {});
    };
    exports2.write = function(png, options) {
      return pack(png, options);
    };
  }
});

// node_modules/pngjs/lib/png.js
var require_png = __commonJS({
  "node_modules/pngjs/lib/png.js"(exports2) {
    "use strict";
    var util = require("util");
    var Stream = require("stream");
    var Parser = require_parser_async();
    var Packer = require_packer_async();
    var PNGSync = require_png_sync();
    var PNG3 = exports2.PNG = function(options) {
      Stream.call(this);
      options = options || {};
      this.width = options.width | 0;
      this.height = options.height | 0;
      this.data = this.width > 0 && this.height > 0 ? Buffer.alloc(4 * this.width * this.height) : null;
      if (options.fill && this.data) {
        this.data.fill(0);
      }
      this.gamma = 0;
      this.readable = this.writable = true;
      this._parser = new Parser(options);
      this._parser.on("error", this.emit.bind(this, "error"));
      this._parser.on("close", this._handleClose.bind(this));
      this._parser.on("metadata", this._metadata.bind(this));
      this._parser.on("gamma", this._gamma.bind(this));
      this._parser.on(
        "parsed",
        function(data) {
          this.data = data;
          this.emit("parsed", data);
        }.bind(this)
      );
      this._packer = new Packer(options);
      this._packer.on("data", this.emit.bind(this, "data"));
      this._packer.on("end", this.emit.bind(this, "end"));
      this._parser.on("close", this._handleClose.bind(this));
      this._packer.on("error", this.emit.bind(this, "error"));
    };
    util.inherits(PNG3, Stream);
    PNG3.sync = PNGSync;
    PNG3.prototype.pack = function() {
      if (!this.data || !this.data.length) {
        this.emit("error", "No data provided");
        return this;
      }
      process.nextTick(
        function() {
          this._packer.pack(this.data, this.width, this.height, this.gamma);
        }.bind(this)
      );
      return this;
    };
    PNG3.prototype.parse = function(data, callback) {
      if (callback) {
        let onParsed, onError;
        onParsed = function(parsedData) {
          this.removeListener("error", onError);
          this.data = parsedData;
          callback(null, this);
        }.bind(this);
        onError = function(err2) {
          this.removeListener("parsed", onParsed);
          callback(err2, null);
        }.bind(this);
        this.once("parsed", onParsed);
        this.once("error", onError);
      }
      this.end(data);
      return this;
    };
    PNG3.prototype.write = function(data) {
      this._parser.write(data);
      return true;
    };
    PNG3.prototype.end = function(data) {
      this._parser.end(data);
    };
    PNG3.prototype._metadata = function(metadata) {
      this.width = metadata.width;
      this.height = metadata.height;
      this.emit("metadata", metadata);
    };
    PNG3.prototype._gamma = function(gamma) {
      this.gamma = gamma;
    };
    PNG3.prototype._handleClose = function() {
      if (!this._parser.writable && !this._packer.readable) {
        this.emit("close");
      }
    };
    PNG3.bitblt = function(src, dst, srcX, srcY, width, height, deltaX, deltaY) {
      srcX |= 0;
      srcY |= 0;
      width |= 0;
      height |= 0;
      deltaX |= 0;
      deltaY |= 0;
      if (srcX > src.width || srcY > src.height || srcX + width > src.width || srcY + height > src.height) {
        throw new Error("bitblt reading outside image");
      }
      if (deltaX > dst.width || deltaY > dst.height || deltaX + width > dst.width || deltaY + height > dst.height) {
        throw new Error("bitblt writing outside image");
      }
      for (let y = 0; y < height; y++) {
        src.data.copy(
          dst.data,
          (deltaY + y) * dst.width + deltaX << 2,
          (srcY + y) * src.width + srcX << 2,
          (srcY + y) * src.width + srcX + width << 2
        );
      }
    };
    PNG3.prototype.bitblt = function(dst, srcX, srcY, width, height, deltaX, deltaY) {
      PNG3.bitblt(this, dst, srcX, srcY, width, height, deltaX, deltaY);
      return this;
    };
    PNG3.adjustGamma = function(src) {
      if (src.gamma) {
        for (let y = 0; y < src.height; y++) {
          for (let x = 0; x < src.width; x++) {
            let idx = src.width * y + x << 2;
            for (let i = 0; i < 3; i++) {
              let sample = src.data[idx + i] / 255;
              sample = Math.pow(sample, 1 / 2.2 / src.gamma);
              src.data[idx + i] = Math.round(sample * 255);
            }
          }
        }
        src.gamma = 0;
      }
    };
    PNG3.prototype.adjustGamma = function() {
      PNG3.adjustGamma(this);
    };
  }
});

// src/index.js
var index_exports = {};
__export(index_exports, {
  createAgentDerbySkill: () => createAgentDerbySkill,
  phase3: () => executor_exports,
  phase4: () => coordinator_exports,
  phase5: () => artwork_exports,
  phase5plan: () => plan_refined_exports,
  phase5refine: () => refine_exports,
  phase6: () => artwork_exec_exports,
  phase6_1: () => artwork_exec61_exports,
  phase7: () => success_exports,
  region_scan: () => region_scan_exports,
  stage1: () => interacting_dreams_exports
});
module.exports = __toCommonJS(index_exports);

// node_modules/ws/wrapper.mjs
var import_stream = __toESM(require_stream(), 1);
var import_extension = __toESM(require_extension(), 1);
var import_permessage_deflate = __toESM(require_permessage_deflate(), 1);
var import_receiver = __toESM(require_receiver(), 1);
var import_sender = __toESM(require_sender(), 1);
var import_subprotocol = __toESM(require_subprotocol(), 1);
var import_websocket = __toESM(require_websocket(), 1);
var import_websocket_server = __toESM(require_websocket_server(), 1);
var wrapper_default = import_websocket.default;

// src/util/backoff.js
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}
function backoffMs(attempt, { baseMs = 250, maxMs = 5e3, jitter = 0.2 } = {}) {
  const exp = Math.min(maxMs, baseMs * Math.pow(2, Math.max(0, attempt)));
  const j = exp * jitter * (Math.random() * 2 - 1);
  return Math.max(0, Math.floor(exp + j));
}

// src/client/chatws.js
var _globalClients = globalThis.__agentderby_chatws_clients || (globalThis.__agentderby_chatws_clients = /* @__PURE__ */ new Map());
var _nextClientId = (() => {
  const k = "__agentderby_chatws_next_id";
  globalThis[k] = globalThis[k] || 1;
  return () => globalThis[k]++;
})();
function _ringPush(arr, item, cap = 50) {
  arr.push(item);
  if (arr.length > cap) arr.splice(0, arr.length - cap);
}
var ChatWSClient = class _ChatWSClient {
  static getShared({ url, maxRecent = 200 } = {}) {
    const key = String(url || "");
    if (!key) throw new Error("chatws url required");
    const existing = _globalClients.get(key);
    if (existing && !existing._closed) {
      existing._sharedKey = key;
      existing._wasReused = true;
      return existing;
    }
    const c = new _ChatWSClient({ url: key, maxRecent });
    c._sharedKey = key;
    c._wasReused = false;
    _globalClients.set(key, c);
    return c;
  }
  constructor({ url, maxRecent = 200 } = {}) {
    this.url = url;
    this.maxRecent = maxRecent;
    this.clientId = `chatws_${_nextClientId()}`;
    this._sharedKey = null;
    this._wasReused = null;
    this._writeTrace = [];
    this._readTrace = [];
    this._recvTrace = [];
    this.ws = null;
    this.connected = false;
    this._ready = null;
    this._readyResolve = null;
    this.recent = [];
    this.lastAnyFrameAt = 0;
    this.lastMessageAt = 0;
    this.lastHistoryAt = 0;
    this._connecting = false;
    this._closed = false;
  }
  async connect() {
    if (this._closed) throw new Error("ChatWSClient closed");
    if (this._connecting || this.connected) return;
    this._connecting = true;
    if (!this._ready) {
      this._ready = new Promise((res) => this._readyResolve = res);
    }
    let attempt = 0;
    while (!this._closed) {
      try {
        await this._connectOnce();
        this._connecting = false;
        return;
      } catch (e) {
        const ms = backoffMs(attempt++);
        await sleep(ms);
      }
    }
  }
  async _connectOnce() {
    return new Promise((resolve, reject) => {
      const ws = new wrapper_default(this.url);
      let opened = false;
      const cleanup = () => {
        ws.removeAllListeners();
      };
      ws.on("open", () => {
        opened = true;
        this.ws = ws;
        this.connected = true;
        resolve();
      });
      ws.on("message", (data) => {
        const s = data.toString();
        const isHistory = s.startsWith("H ");
        const isMessage = s.startsWith("M ");
        if (!isHistory && !isMessage) return;
        const payload = s.slice(2);
        try {
          const parsed = JSON.parse(payload);
          this.lastAnyFrameAt = Date.now();
          const preLen = Array.isArray(this.recent) ? this.recent.length : 0;
          const preLatestChatTs = Math.max(...(this.recent || []).filter((m) => (m?.type || "chat") === "chat").map((m) => m.ts || 0), 0) || 0;
          const preLatestIntentTs = Math.max(...(this.recent || []).filter((m) => (m?.type || "chat") === "intent").map((m) => m.ts || 0), 0) || 0;
          _ringPush(this._recvTrace, {
            at: Date.now(),
            clientId: this.clientId,
            kind: isHistory ? "H" : "M",
            parsedType: parsed?.type || null,
            ts: parsed?.ts || null,
            pre: { recentLen: preLen, latestChatTs: preLatestChatTs, latestIntentTs: preLatestIntentTs }
          }, 50);
          if (isHistory) {
            const snap = this._normalizeHistorySnapshot(parsed);
            if (snap.length) {
              for (const m of snap) this._pushRecent(m, { kind: "H" });
            } else if (parsed && typeof parsed.text === "string") {
              if (!parsed.type) parsed.type = "chat";
              this._pushRecent(parsed, { kind: "H" });
            }
            this.lastHistoryAt = Date.now();
            if (this._readyResolve) {
              this._readyResolve();
              this._readyResolve = null;
            }
            return;
          }
          const msg = parsed;
          if (msg && typeof msg.text === "string") {
            if (!msg.type) msg.type = "chat";
            this._pushRecent(msg, { kind: "M" });
            this.lastMessageAt = Date.now();
            if (this._readyResolve) {
              this._readyResolve();
              this._readyResolve = null;
            }
          }
        } catch (_) {
        }
      });
      ws.on("close", () => {
        cleanup();
        this.connected = false;
        this.ws = null;
        if (!this._closed) {
          this.connect().catch(() => {
          });
        }
      });
      ws.on("error", (err2) => {
        cleanup();
        if (!opened) reject(err2);
      });
    });
  }
  _pushRecent(msg, meta = null) {
    this.recent.push(msg);
    if (this.recent.length > this.maxRecent) {
      this.recent = this.recent.slice(this.recent.length - this.maxRecent);
    }
    const latestChatTs = Math.max(...this.recent.filter((m) => (m?.type || "chat") === "chat").map((m) => m.ts || 0), 0) || 0;
    const latestIntentTs = Math.max(...this.recent.filter((m) => (m?.type || "chat") === "intent").map((m) => m.ts || 0), 0) || 0;
    _ringPush(this._writeTrace, {
      at: Date.now(),
      clientId: this.clientId,
      kind: meta?.kind || null,
      type: msg?.type || null,
      ts: msg?.ts || null,
      appended: true,
      recentLen: this.recent.length,
      latestChatTs,
      latestIntentTs
    }, 50);
  }
  async awaitReady({ timeoutMs = 4e3 } = {}) {
    await this.connect();
    if (!this._ready) return;
    if (!this._readyResolve) return;
    let t;
    const timeout = new Promise((_, rej) => {
      t = setTimeout(() => rej(new Error("chatws ready timeout")), timeoutMs);
    });
    try {
      await Promise.race([this._ready, timeout]);
    } finally {
      clearTimeout(t);
    }
  }
  _normalizeHistorySnapshot(parsed) {
    const arr = Array.isArray(parsed) ? parsed : Array.isArray(parsed?.messages) ? parsed.messages : Array.isArray(parsed?.history) ? parsed.history : [];
    const out = [];
    for (const m of arr) {
      if (!m || typeof m.text !== "string") continue;
      if (!m.type) m.type = "chat";
      out.push(m);
    }
    return out;
  }
  _ensureFreshOrReconnect({ maxStaleMs = 15e3 } = {}) {
    if (this._closed) return;
    const ws = this.ws;
    const open = !!ws && ws.readyState === wrapper_default.OPEN;
    if (!this.lastAnyFrameAt) return;
    const stale = Date.now() - this.lastAnyFrameAt > maxStaleMs;
    if (!open || stale) {
      try {
        ws?.close();
      } catch {
      }
      this.connected = false;
      this.ws = null;
      this.connect().catch(() => {
      });
    }
  }
  getRecent({ limit = 50, sinceTs = null, type = null, maxStaleMs = 15e3 } = {}) {
    this._ensureFreshOrReconnect({ maxStaleMs });
    let xs = this.recent;
    if (sinceTs != null) xs = xs.filter((m) => (m.ts ?? 0) >= sinceTs);
    if (type) xs = xs.filter((m) => m.type === type);
    if (limit != null) xs = xs.slice(Math.max(0, xs.length - limit));
    const latestChatTs = Math.max(...this.recent.filter((m) => (m?.type || "chat") === "chat").map((m) => m.ts || 0), 0) || 0;
    const latestIntentTs = Math.max(...this.recent.filter((m) => (m?.type || "chat") === "intent").map((m) => m.ts || 0), 0) || 0;
    const retMaxTs = Math.max(...xs.map((m) => m.ts || 0), 0) || 0;
    _ringPush(this._readTrace, {
      at: Date.now(),
      clientId: this.clientId,
      sharedKey: this._sharedKey,
      readyState: this.ws ? this.ws.readyState : null,
      connected: !!this.connected,
      recentLen: this.recent.length,
      latestChatTs,
      latestIntentTs,
      filter: { limit, sinceTs, type },
      retCount: xs.length,
      retMaxTs
    }, 50);
    return xs;
  }
  send({ name, text, ts }) {
    if (!this.ws || this.ws.readyState !== wrapper_default.OPEN) return false;
    this.ws.send(JSON.stringify({ name, text, ts }));
    return true;
  }
  close() {
    this._closed = true;
    try {
      this.ws?.close();
    } catch {
    }
  }
};

// src/client/boardws.js
var BoardWSClient = class {
  constructor({ url } = {}) {
    this.url = url;
    this.ws = null;
    this.connected = false;
    this.allowDraw = null;
    this._connecting = false;
    this._closed = false;
    this._ready = null;
    this._readyResolve = null;
  }
  async connect() {
    if (this._closed) throw new Error("BoardWSClient closed");
    if (this._connecting || this.connected) return;
    this._connecting = true;
    if (!this._ready) {
      this._ready = new Promise((res) => this._readyResolve = res);
    }
    let attempt = 0;
    while (!this._closed) {
      try {
        await this._connectOnce();
        this._connecting = false;
        return;
      } catch (e) {
        const ms = backoffMs(attempt++);
        await sleep(ms);
      }
    }
  }
  async _connectOnce() {
    return new Promise((resolve, reject) => {
      const ws = new wrapper_default(this.url);
      let opened = false;
      const cleanup = () => ws.removeAllListeners();
      ws.on("open", () => {
        opened = true;
        this.ws = ws;
        this.connected = true;
        this.allowDraw = null;
        resolve();
      });
      ws.on("message", (data) => {
        if (this.allowDraw == null) {
          const b = Buffer.from(data);
          this.allowDraw = b.length > 0 && b[0] === 1;
          if (this._readyResolve) {
            this._readyResolve();
            this._readyResolve = null;
          }
          return;
        }
      });
      ws.on("close", () => {
        cleanup();
        this.connected = false;
        this.ws = null;
        this.allowDraw = null;
        if (!this._closed) this.connect().catch(() => {
        });
      });
      ws.on("error", (err2) => {
        cleanup();
        if (!opened) reject(err2);
      });
    });
  }
  async awaitReady({ timeoutMs = 4e3 } = {}) {
    await this.connect();
    if (!this._ready) return;
    if (!this._readyResolve) return;
    let t;
    const timeout = new Promise((_, rej) => {
      t = setTimeout(() => rej(new Error("board ws ready timeout")), timeoutMs);
    });
    try {
      await Promise.race([this._ready, timeout]);
    } finally {
      clearTimeout(t);
    }
  }
  sendPixel({ x, y, r, g, b }) {
    if (!this.ws || this.ws.readyState !== wrapper_default.OPEN) return false;
    if (!this.allowDraw) return false;
    const buf = Buffer.alloc(11);
    buf.writeUInt32BE(x >>> 0, 0);
    buf.writeUInt32BE(y >>> 0, 4);
    buf[8] = r & 255;
    buf[9] = g & 255;
    buf[10] = b & 255;
    this.ws.send(buf);
    return true;
  }
  close() {
    this._closed = true;
    try {
      this.ws?.close();
    } catch {
    }
  }
};

// src/client/board.js
var import_pngjs = __toESM(require_png(), 1);
async function fetchBoardSnapshot({ baseUrl }) {
  const url = new URL("/place.png", baseUrl).toString();
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`snapshot fetch failed: ${resp.status}`);
  const ab = await resp.arrayBuffer();
  const bytes = Buffer.from(ab);
  return { format: "png", bytes };
}
function regionFromPngBytes({ pngBytes, x, y, w, h }) {
  const png = import_pngjs.PNG.sync.read(pngBytes);
  const width = png.width;
  const height = png.height;
  if (x < 0 || y < 0 || w <= 0 || h <= 0 || x + w > width || y + h > height) {
    throw new Error("region out of bounds");
  }
  const pixels = [];
  for (let yy = y; yy < y + h; yy++) {
    for (let xx = x; xx < x + w; xx++) {
      const idx = (yy * width + xx) * 4;
      const r = png.data[idx];
      const g = png.data[idx + 1];
      const b = png.data[idx + 2];
      const color = `#${r.toString(16).padStart(2, "0")}${g.toString(16).padStart(2, "0")}${b.toString(16).padStart(2, "0")}`;
      pixels.push({ x: xx, y: yy, color });
    }
  }
  return { width, height, region: { x, y, w, h, pixels } };
}

// src/types.js
var ErrorCode = {
  INVALID: "INVALID",
  NETWORK: "NETWORK",
  TIMEOUT: "TIMEOUT",
  RATE_LIMITED: "RATE_LIMITED",
  REJECTED: "REJECTED",
  BACKEND: "BACKEND"
};
function ok(payload = {}) {
  return { ok: true, ...payload };
}
function err(code, message, extra = {}) {
  return { ok: false, error: { code, message, ...extra } };
}

// src/client/coord.js
var CoordClient = class {
  constructor({ baseUrl } = {}) {
    this.baseUrl = baseUrl;
  }
  async list_active_claims() {
    try {
      const url = new URL("/claims", this.baseUrl).toString();
      const resp = await fetch(url);
      const j = await resp.json();
      return j?.ok ? ok({ claims: j.claims || [] }) : err(ErrorCode.BACKEND, j?.error?.message || "claims error", { conflicts: j?.conflicts });
    } catch (e) {
      return err(ErrorCode.NETWORK, String(e?.message || e));
    }
  }
  async claim_region({ agent_id, region, ttl_ms = 6e4, reason = "" } = {}) {
    try {
      const url = new URL("/claims", this.baseUrl).toString();
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ agent_id, region, ttl_ms, reason })
      });
      const j = await resp.json();
      if (j?.ok) return ok({ claim: j.claim });
      return err(j?.error?.code || ErrorCode.BACKEND, j?.error?.message || "claim conflict", { conflicts: j?.conflicts || [] });
    } catch (e) {
      return err(ErrorCode.NETWORK, String(e?.message || e));
    }
  }
  async release_region({ agent_id, claim_id } = {}) {
    try {
      const u = new URL("/claims", this.baseUrl);
      u.searchParams.set("agent_id", agent_id);
      u.searchParams.set("claim_id", claim_id);
      const resp = await fetch(u.toString(), { method: "DELETE" });
      const j = await resp.json();
      return j?.ok ? ok({}) : err(j?.error?.code || ErrorCode.BACKEND, j?.error?.message || "release error");
    } catch (e) {
      return err(ErrorCode.NETWORK, String(e?.message || e));
    }
  }
  async register_agent({ agent_id, display_name = "", version = "" } = {}) {
    try {
      const url = new URL("/presence", this.baseUrl).toString();
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ agent_id, display_name, version })
      });
      const j = await resp.json();
      return j?.ok ? ok({ presence: j.presence }) : err(ErrorCode.BACKEND, j?.error?.message || "presence error");
    } catch (e) {
      return err(ErrorCode.NETWORK, String(e?.message || e));
    }
  }
  async heartbeat({ agent_id } = {}) {
    return this.register_agent({ agent_id });
  }
};

// src/util/rate_limit.js
var SpacingLimiter = class {
  constructor({ minIntervalMs = 250 } = {}) {
    this.minIntervalMs = minIntervalMs;
    this._nextAt = 0;
  }
  async wait() {
    const now = Date.now();
    const t = Math.max(now, this._nextAt);
    const delay = t - now;
    this._nextAt = t + this.minIntervalMs;
    if (delay > 0) await new Promise((r) => setTimeout(r, delay));
  }
};

// src/phase4/coordinator.js
var coordinator_exports = {};
__export(coordinator_exports, {
  PatchCoordinator: () => PatchCoordinator,
  runTwoAgentDemo: () => runTwoAgentDemo
});

// src/phase1/region_scan.js
var region_scan_exports = {};
__export(region_scan_exports, {
  PROFILES: () => PROFILES,
  classifyRegion: () => classifyRegion,
  decodePng: () => decodePng,
  recommendRegions: () => recommendRegions,
  scanRegionsFromPngBytes: () => scanRegionsFromPngBytes,
  scoreRegionForProfile: () => scoreRegionForProfile
});
var import_pngjs2 = __toESM(require_png(), 1);
function rgbToHex(r, g, b) {
  return `#${r.toString(16).padStart(2, "0")}${g.toString(16).padStart(2, "0")}${b.toString(16).padStart(2, "0")}`;
}
function luminance(r, g, b) {
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
function decodePng(pngBytes) {
  const png = import_pngjs2.PNG.sync.read(pngBytes);
  return { png, width: png.width, height: png.height };
}
function scanRegionsFromPngBytes({ pngBytes, regionSize = 32 }) {
  const { png, width, height } = decodePng(pngBytes);
  const regions = [];
  const rx = Math.ceil(width / regionSize);
  const ry = Math.ceil(height / regionSize);
  for (let j = 0; j < ry; j++) {
    for (let i = 0; i < rx; i++) {
      const x = i * regionSize;
      const y = j * regionSize;
      const w = Math.min(regionSize, width - x);
      const h = Math.min(regionSize, height - y);
      const id = `r${i}_${j}`;
      const colorCounts = /* @__PURE__ */ new Map();
      let edges = 0;
      let lumSum = 0;
      let lumSumSq = 0;
      for (let yy = y; yy < y + h; yy++) {
        for (let xx = x; xx < x + w; xx++) {
          const idx = (yy * width + xx) * 4;
          const r = png.data[idx];
          const g = png.data[idx + 1];
          const b = png.data[idx + 2];
          const hex = rgbToHex(r, g, b);
          colorCounts.set(hex, (colorCounts.get(hex) || 0) + 1);
          const lum = luminance(r, g, b);
          lumSum += lum;
          lumSumSq += lum * lum;
        }
      }
      let bgColor = null;
      let bgCount = -1;
      for (const [c, n] of colorCounts.entries()) {
        if (n > bgCount) {
          bgCount = n;
          bgColor = c;
        }
      }
      const total = w * h;
      const nonBg = total - bgCount;
      const fillRatio = total > 0 ? nonBg / total : 0;
      for (let yy = y; yy < y + h; yy++) {
        for (let xx = x; xx < x + w; xx++) {
          const idx = (yy * width + xx) * 4;
          const r = png.data[idx];
          const g = png.data[idx + 1];
          const b = png.data[idx + 2];
          const cur = r << 16 | g << 8 | b;
          if (xx + 1 < x + w) {
            const idx2 = (yy * width + (xx + 1)) * 4;
            const c2 = png.data[idx2] << 16 | png.data[idx2 + 1] << 8 | png.data[idx2 + 2];
            if (c2 !== cur) edges++;
          }
          if (yy + 1 < y + h) {
            const idx2 = ((yy + 1) * width + xx) * 4;
            const c2 = png.data[idx2] << 16 | png.data[idx2 + 1] << 8 | png.data[idx2 + 2];
            if (c2 !== cur) edges++;
          }
        }
      }
      const maxEdges = (w - 1) * h + (h - 1) * w;
      const edgeDensity = maxEdges > 0 ? edges / maxEdges : 0;
      const dominantColors = Array.from(colorCounts.entries()).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([color, count]) => ({ color, count, pct: total ? count / total : 0 }));
      const lumMean = total ? lumSum / total : 0;
      const lumVar = total ? Math.max(0, lumSumSq / total - lumMean * lumMean) : 0;
      const recentChangeRate = null;
      const { stage, styleTags, riskScore } = classifyRegion({ fillRatio, edgeDensity, dominantColors, lumVar });
      regions.push({
        regionId: id,
        x,
        y,
        w,
        h,
        dominantColors,
        fillRatio,
        edgeDensity,
        recentChangeRate,
        stage,
        styleTags,
        riskScore
      });
    }
  }
  return { width, height, regionSize, regions };
}
function classifyRegion({ fillRatio, edgeDensity, dominantColors, lumVar }) {
  let stage = "in_progress";
  if (fillRatio < 0.02) stage = "empty";
  else if (fillRatio < 0.12) stage = "seeded";
  else if (fillRatio < 0.65) stage = "in_progress";
  else if (fillRatio < 0.9) stage = "nearly_done";
  else stage = "finished";
  if (fillRatio > 0.5 && edgeDensity > 0.25) stage = "damaged";
  if (fillRatio > 0.65 && edgeDensity > 0.35) stage = "contested";
  const styleTags = [];
  const nColors = dominantColors?.length || 0;
  const topPct = dominantColors?.[0]?.pct ?? 0;
  if (edgeDensity > 0.22 && fillRatio > 0.25) styleTags.push("text_like");
  if (edgeDensity > 0.18 && nColors >= 3) styleTags.push("geometric");
  if (lumVar > 900 && fillRatio > 0.2) styleTags.push("starry");
  if (nColors >= 4 && topPct < 0.55 && fillRatio > 0.25) styleTags.push("abstract");
  if (fillRatio > 0.35 && edgeDensity < 0.08) styleTags.push("landscape");
  if (fillRatio > 0.25 && edgeDensity < 0.12 && nColors <= 3) styleTags.push("portrait");
  if (fillRatio > 0.2 && edgeDensity < 0.18 && nColors >= 3) styleTags.push("wave");
  if (fillRatio > 0.25 && edgeDensity < 0.2 && nColors <= 4) styleTags.push("icon");
  const tags = Array.from(new Set(styleTags));
  let riskScore = 0;
  if (stage === "contested") riskScore += 0.6;
  if (stage === "damaged") riskScore += 0.45;
  riskScore += Math.min(0.4, edgeDensity * 1.2);
  riskScore += fillRatio < 0.1 ? 0.15 : 0;
  riskScore = Math.max(0, Math.min(1, riskScore));
  return { stage, styleTags: tags, riskScore };
}
var PROFILES = {
  "wave-restorer": {
    id: "wave-restorer",
    preferredStyles: ["wave", "landscape", "geometric"],
    preferredPalette: ["#0b3d91", "#1e90ff", "#00c2ff", "#ffffff", "#111111"],
    preferredRoles: ["repair", "refine", "protect"],
    stageAffinity: { damaged: 1, contested: 0.9, in_progress: 0.7, seeded: 0.4, nearly_done: 0.6, finished: 0.2, empty: 0.3 }
  },
  "starry-finisher": {
    id: "starry-finisher",
    preferredStyles: ["starry", "abstract"],
    preferredPalette: ["#0a0a1a", "#111133", "#2d2d7a", "#f8f8ff", "#ffd27d"],
    preferredRoles: ["fill", "refine", "protect"],
    stageAffinity: { nearly_done: 1, in_progress: 0.8, seeded: 0.5, finished: 0.4, damaged: 0.6, contested: 0.5, empty: 0.2 }
  },
  "portrait-refiner": {
    id: "portrait-refiner",
    preferredStyles: ["portrait", "icon", "text_like"],
    preferredPalette: ["#000000", "#ffffff", "#f2c9a0", "#c68642", "#8d5524"],
    preferredRoles: ["refine", "repair", "protect"],
    stageAffinity: { in_progress: 1, nearly_done: 0.9, finished: 0.6, seeded: 0.5, damaged: 0.8, contested: 0.7, empty: 0.2 }
  }
};
function scoreRegionForProfile(region, profile) {
  const reasons = [];
  let score = 0;
  const stageW = profile.stageAffinity?.[region.stage] ?? 0.4;
  score += 0.35 * stageW;
  reasons.push(`stage=${region.stage} affinity=${stageW.toFixed(2)}`);
  const match = (region.styleTags || []).filter((t) => profile.preferredStyles.includes(t));
  const styleScore = Math.min(1, match.length / Math.max(1, profile.preferredStyles.length));
  score += 0.35 * styleScore;
  reasons.push(match.length ? `styleMatch=${match.join(",")}` : "styleMatch=none");
  const r = region.riskScore;
  const riskScore = 1 - Math.min(1, Math.abs(r - 0.4) / 0.6);
  score += 0.15 * riskScore;
  reasons.push(`risk=${r.toFixed(2)}`);
  if (profile.id === "wave-restorer") {
    const repairish = region.stage === "damaged" || region.stage === "contested";
    score += repairish ? 0.15 : 0;
    if (repairish) reasons.push("needs_repair");
  }
  if (profile.id === "starry-finisher") {
    const finishish = region.stage === "nearly_done" || region.stage === "finished";
    score += finishish ? 0.08 : 0;
    if (finishish) reasons.push("finish_candidate");
  }
  if (profile.id === "portrait-refiner") {
    const refineish = region.edgeDensity > 0.12 && region.fillRatio > 0.25;
    score += refineish ? 0.1 : 0;
    if (refineish) reasons.push("detail_edges");
  }
  score = Math.max(0, Math.min(1, score));
  let actionType = "wait";
  if (region.stage === "empty") actionType = "seed";
  else if (region.stage === "seeded") actionType = "fill";
  else if (region.stage === "in_progress") actionType = "refine";
  else if (region.stage === "nearly_done") actionType = "protect";
  else if (region.stage === "damaged") actionType = "repair";
  else if (region.stage === "contested") actionType = "protect";
  return { score, actionType, reasons };
}
function recommendRegions({ regions, profile, topN = 5 }) {
  const scored = regions.map((r) => {
    const s = scoreRegionForProfile(r, profile);
    return { regionId: r.regionId, score: s.score, actionType: s.actionType, reasons: s.reasons, region: r };
  }).sort((a, b) => b.score - a.score);
  return scored.slice(0, topN);
}

// src/phase1/temporal.js
function nowMs() {
  return Date.now();
}
var TemporalRegionHistory = class {
  constructor({ regionSize = 32, maxFrames = 5 } = {}) {
    this.regionSize = regionSize;
    this.maxFrames = maxFrames;
    this.frames = [];
  }
  addFrameFromPng({ pngBytes, ts = nowMs() } = {}) {
    const scan = scanRegionsFromPngBytes({ pngBytes, regionSize: this.regionSize });
    const regionsById = new Map(scan.regions.map((r) => [r.regionId, r]));
    this.frames.push({ ts, width: scan.width, height: scan.height, regionsById });
    while (this.frames.length > this.maxFrames) this.frames.shift();
    return { ts, width: scan.width, height: scan.height, regionSize: scan.regionSize, regions: scan.regions.length };
  }
  hasAtLeast(n) {
    return this.frames.length >= n;
  }
  latest() {
    return this.frames[this.frames.length - 1] || null;
  }
  previous() {
    return this.frames.length >= 2 ? this.frames[this.frames.length - 2] : null;
  }
  computeTemporalSummaries() {
    const cur = this.latest();
    const prev = this.previous();
    if (!cur) return [];
    const dtMs = prev ? Math.max(1, cur.ts - prev.ts) : null;
    const out = [];
    for (const [id, r] of cur.regionsById.entries()) {
      let changedPixels = null;
      let recentChangeRate = null;
      let stabilityScore = null;
      if (prev) {
        const p = prev.regionsById.get(id);
        if (p) {
          const dFill = Math.abs((r.fillRatio ?? 0) - (p.fillRatio ?? 0));
          const dEdge = Math.abs((r.edgeDensity ?? 0) - (p.edgeDensity ?? 0));
          const proxy = Math.min(1, dFill * 2 + dEdge * 1.5);
          const regionPx = r.w * r.h;
          changedPixels = Math.round(proxy * regionPx);
          recentChangeRate = changedPixels / regionPx / (dtMs / 1e3);
          stabilityScore = Math.max(0, Math.min(1, 1 - proxy));
        }
      }
      out.push({
        ...r,
        temporal: {
          dtMs,
          changedPixels,
          recentChangeRate,
          stabilityScore
        }
      });
    }
    return out;
  }
};
function temporalStageOverride({ baseStage, fillRatio, edgeDensity, temporal }) {
  let stage = baseStage;
  const rcr = temporal?.recentChangeRate;
  const stab = temporal?.stabilityScore;
  if (rcr != null) {
    if ((edgeDensity ?? 0) > 0.25 && rcr > 0.03) stage = "contested";
    else if ((edgeDensity ?? 0) > 0.22 && rcr > 0.015) stage = "damaged";
    if ((fillRatio ?? 0) > 0.9 && rcr < 2e-3 && (stab ?? 0) > 0.9) stage = "finished";
    else if ((fillRatio ?? 0) > 0.75 && rcr < 0.01) stage = "nearly_done";
  }
  return stage;
}

// src/phase1/actions.js
function candidateActionsForProfile({ regionSummaries, profileId, topN = 5 }) {
  const profile = PROFILES[profileId];
  if (!profile) throw new Error(`unknown profile: ${profileId}`);
  const normalized = regionSummaries.map((r) => {
    const baseStage = r.stage;
    const stage = temporalStageOverride({ baseStage, fillRatio: r.fillRatio, edgeDensity: r.edgeDensity, temporal: r.temporal });
    return { ...r, stage, baseStage };
  });
  const scored = normalized.map((r) => {
    const s = scoreRegionForProfile(r, profile);
    const stability = r.temporal?.stabilityScore;
    const rcr = r.temporal?.recentChangeRate;
    let expectedGain = 0.1;
    if (s.actionType === "repair") expectedGain = 0.35;
    else if (s.actionType === "refine") expectedGain = 0.25;
    else if (s.actionType === "fill") expectedGain = 0.2;
    else if (s.actionType === "protect") expectedGain = 0.18;
    else if (s.actionType === "seed") expectedGain = 0.12;
    if (stability != null && stability < 0.3) expectedGain *= 0.6;
    if (stability != null && stability > 0.85 && r.stage === "nearly_done") expectedGain *= 1.2;
    const reasons = [...s.reasons];
    if (rcr != null) reasons.push(`rcr=${rcr.toFixed(4)}/s`);
    if (stability != null) reasons.push(`stability=${stability.toFixed(2)}`);
    if (r.baseStage !== r.stage) reasons.push(`temporalStage:->`);
    return {
      regionId: r.regionId,
      x: r.x,
      y: r.y,
      w: r.w,
      h: r.h,
      score: s.score,
      actionType: s.actionType,
      expectedGain,
      reasons,
      _region: r
    };
  }).sort((a, b) => b.score - a.score).slice(0, topN);
  return scored.map(({ _region, ...rest }) => rest);
}
function patchPlansFromCandidateActions({ candidateActions, maxPlans = 3 }) {
  const plans = [];
  for (let i = 0; i < Math.min(maxPlans, candidateActions.length); i++) {
    const a = candidateActions[i];
    const size = 16;
    let px = a.x;
    let py = a.y;
    if (["repair", "refine", "protect"].includes(a.actionType)) {
      px = a.x + Math.floor((a.w - size) / 2);
      py = a.y + Math.floor((a.h - size) / 2);
    }
    plans.push({
      patchId: `${a.regionId}_p${i}`,
      x: px,
      y: py,
      w: Math.min(size, a.w),
      h: Math.min(size, a.h),
      actionType: a.actionType,
      expectedGain: a.expectedGain,
      reason: a.reasons.slice(0, 4)
    });
  }
  return plans;
}

// src/phase3/executor.js
var executor_exports = {};
__export(executor_exports, {
  comparePatch: () => comparePatch,
  draw_pixels_chunked: () => draw_pixels_chunked,
  executePatchPlan: () => executePatchPlan,
  generateSolidPatchPixels: () => generateSolidPatchPixels,
  readRegion: () => readRegion
});
function hexToRgb(hex) {
  const m = /^#?([0-9a-fA-F]{6})$/.exec(hex);
  if (!m) throw new Error(`bad hex: ${hex}`);
  const n = parseInt(m[1], 16);
  return { r: n >> 16 & 255, g: n >> 8 & 255, b: n & 255 };
}
async function readRegion({ baseUrl, x, y, w, h }) {
  const snap = await fetchBoardSnapshot({ baseUrl });
  const { region } = regionFromPngBytes({ pngBytes: snap.bytes, x, y, w, h });
  return { ts: Date.now(), region };
}
function generateSolidPatchPixels({ x, y, w, h, color = "#ffffff" }) {
  const pixels = [];
  for (let yy = y; yy < y + h; yy++) {
    for (let xx = x; xx < x + w; xx++) {
      pixels.push({ x: xx, y: yy, color });
    }
  }
  return pixels;
}
async function draw_pixels_chunked({ board, pixels, chunkSize = 50, stopOnError = true }) {
  let accepted = 0;
  let firstError = null;
  for (let i = 0; i < pixels.length; i += chunkSize) {
    const chunk = pixels.slice(i, i + chunkSize);
    for (const p of chunk) {
      const { r, g, b } = hexToRgb(p.color);
      const ok2 = board.sendPixel({ x: p.x, y: p.y, r, g, b });
      if (ok2) accepted++;
      else {
        firstError = firstError || "send_rejected";
        if (stopOnError) return { accepted, firstError };
      }
    }
  }
  return { accepted, firstError };
}
function comparePatch({ requestedPixels, afterRegion }) {
  const map = /* @__PURE__ */ new Map();
  for (const p of afterRegion.pixels) map.set(`${p.x},${p.y}`, p.color.toLowerCase());
  let matched = 0;
  for (const p of requestedPixels) {
    const got = map.get(`${p.x},${p.y}`);
    if (got && got === p.color.toLowerCase()) matched++;
  }
  const matchRatio = requestedPixels.length ? matched / requestedPixels.length : 0;
  return { matched, matchRatio };
}
async function executePatchPlan({ baseUrl, boardWsUrl, patchPlan, color = "#ffffff", chunkSize = 50 }) {
  const board = new BoardWSClient({ url: boardWsUrl });
  await board.connect();
  await board.awaitReady({ timeoutMs: 4e3 });
  const allowDraw = board.allowDraw;
  const before = await readRegion({ baseUrl, x: patchPlan.x, y: patchPlan.y, w: patchPlan.w, h: patchPlan.h });
  const requestedPixels = generateSolidPatchPixels({ x: patchPlan.x, y: patchPlan.y, w: patchPlan.w, h: patchPlan.h, color });
  let accepted = 0;
  let stoppedReason = null;
  if (!allowDraw) {
    stoppedReason = "draw_not_allowed";
  } else {
    const res = await draw_pixels_chunked({ board, pixels: requestedPixels, chunkSize, stopOnError: true });
    accepted = res.accepted;
    if (res.firstError) stoppedReason = res.firstError;
  }
  const after = await readRegion({ baseUrl, x: patchPlan.x, y: patchPlan.y, w: patchPlan.w, h: patchPlan.h });
  const { matched, matchRatio } = comparePatch({ requestedPixels, afterRegion: after.region });
  let overwritten = false;
  let status = "failed";
  if (accepted > 0) {
    if (matchRatio >= 0.9) status = "success";
    else if (matchRatio >= 0.5) status = "partial";
    else {
      overwritten = true;
      status = "overwritten";
    }
  } else {
    status = "failed";
  }
  board.close();
  return {
    patchId: patchPlan.patchId,
    regionId: patchPlan.regionId,
    x: patchPlan.x,
    y: patchPlan.y,
    w: patchPlan.w,
    h: patchPlan.h,
    allowDraw,
    requestedPixels: requestedPixels.length,
    accepted,
    matched,
    matchRatio,
    overwritten,
    status,
    stoppedReason,
    beforeSample: before.region.pixels.slice(0, 12),
    afterSample: after.region.pixels.slice(0, 12)
  };
}

// src/phase4/coordinator.js
function patchKey(p) {
  return `${p.x},${p.y},${p.w},${p.h}`;
}
var PatchCoordinator = class {
  constructor() {
    this.reserved = /* @__PURE__ */ new Map();
    this.occupied = /* @__PURE__ */ new Map();
  }
  canAssign(patch, agentId) {
    const k = patchKey(patch);
    const r = this.reserved.get(k);
    const o = this.occupied.get(k);
    return (!r || r === agentId) && (!o || o.agentId === agentId);
  }
  reserve(patch, agentId) {
    const k = patchKey(patch);
    if (!this.canAssign(patch, agentId)) return false;
    this.reserved.set(k, agentId);
    return true;
  }
  markOccupied(patch, agentId, status) {
    const k = patchKey(patch);
    this.occupied.set(k, { agentId, status, ts: Date.now() });
  }
  release(patch, agentId) {
    const k = patchKey(patch);
    if (this.reserved.get(k) === agentId) this.reserved.delete(k);
  }
  assignNonConflictingPatches({ candidateActionsByAgent, maxPlansPerAgent = 3 }) {
    const assignments = {};
    const agentIds = Object.keys(candidateActionsByAgent);
    const plansByAgent = {};
    for (const agentId of agentIds) {
      const acts = candidateActionsByAgent[agentId];
      const plans = patchPlansFromCandidateActions({ candidateActions: acts, maxPlans: maxPlansPerAgent }).map((p, i) => ({
        ...p,
        regionId: acts[i]?.regionId
      }));
      plansByAgent[agentId] = plans;
    }
    for (const agentId of agentIds) {
      let picked = null;
      for (const p of plansByAgent[agentId]) {
        if (this.reserve(p, agentId)) {
          picked = p;
          break;
        }
      }
      assignments[agentId] = {
        patch: picked,
        conflicted: picked ? false : true,
        tried: plansByAgent[agentId].map(patchKey)
      };
    }
    return assignments;
  }
  expansionCandidate(patch) {
    const right = { ...patch, patchId: `${patch.patchId}_expR`, x: patch.x + patch.w };
    const down = { ...patch, patchId: `${patch.patchId}_expD`, y: patch.y + patch.h };
    return [right, down];
  }
  relocationCandidate({ agentId, candidateActions }) {
    const plans = patchPlansFromCandidateActions({ candidateActions, maxPlans: 8 }).map((p, i) => ({
      ...p,
      regionId: candidateActions[i]?.regionId
    }));
    for (const p of plans) {
      const k = patchKey(p);
      const occ = this.occupied.get(k);
      if (occ && occ.agentId === agentId && (occ.status === "overwritten" || occ.status === "failed")) continue;
      if (this.canAssign(p, agentId)) return p;
    }
    return null;
  }
};
async function runTwoAgentDemo({ baseUrl, boardWsUrl, snapshotIntervalMs = 1200 }) {
  const hist = new TemporalRegionHistory({ regionSize: 32, maxFrames: 3 });
  const s1 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s1.bytes, ts: Date.now() });
  await new Promise((r) => setTimeout(r, snapshotIntervalMs));
  const s2 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s2.bytes, ts: Date.now() });
  const summaries = hist.computeTemporalSummaries();
  const coordinator = new PatchCoordinator();
  const agents = ["wave-restorer", "starry-finisher"];
  const candidateActionsByAgent = {};
  for (const a of agents) {
    candidateActionsByAgent[a] = candidateActionsForProfile({ regionSummaries: summaries, profileId: a, topN: 5 });
  }
  const assignments = coordinator.assignNonConflictingPatches({ candidateActionsByAgent, maxPlansPerAgent: 3 });
  const demo = { baseUrl, boardWsUrl, assignments: {}, results: {}, followups: {} };
  for (const agentId of agents) {
    const a = assignments[agentId];
    demo.assignments[agentId] = a;
    const patch = a.patch;
    if (!patch) {
      demo.results[agentId] = { status: "failed", stoppedReason: "no_nonconflicting_patch" };
      continue;
    }
    const execRes = await executePatchPlan({ baseUrl, boardWsUrl, patchPlan: patch, color: "#ffffff", chunkSize: 50 });
    coordinator.markOccupied(patch, agentId, execRes.status);
    coordinator.release(patch, agentId);
    demo.results[agentId] = execRes;
    if (execRes.status === "success") {
      const candidates = coordinator.expansionCandidate(patch);
      const picked = candidates.find((p) => coordinator.canAssign(p, agentId)) || null;
      demo.followups[agentId] = { kind: "expansion", candidates, picked };
    } else if (execRes.status === "overwritten" || execRes.matchRatio < 0.2) {
      const relocate = coordinator.relocationCandidate({ agentId, candidateActions: candidateActionsByAgent[agentId] });
      demo.followups[agentId] = { kind: "relocation", picked: relocate };
    } else {
      demo.followups[agentId] = { kind: "none" };
    }
  }
  const pickedKeys = agents.map((id) => ({ id, key: demo.assignments[id]?.patch ? patchKey(demo.assignments[id].patch) : null })).filter((x) => x.key);
  demo.conflict = {
    picked: pickedKeys,
    unique: new Set(pickedKeys.map((x) => x.key)).size === pickedKeys.length
  };
  return demo;
}

// src/phase5/artwork.js
var artwork_exports = {};
__export(artwork_exports, {
  assignTeam: () => assignTeam,
  clusterRegions: () => clusterRegions,
  frontierPatchesForGoal: () => frontierPatchesForGoal,
  goalsForClusters: () => goalsForClusters,
  phase5Demo: () => phase5Demo
});
function regionKey(r) {
  const i = Math.floor(r.x / r.w);
  const j = Math.floor(r.y / r.h);
  return `${i}_${j}`;
}
function neighborsOf(r) {
  const i = Math.floor(r.x / r.w);
  const j = Math.floor(r.y / r.h);
  return [
    `${i - 1}_${j}`,
    `${i + 1}_${j}`,
    `${i}_${j - 1}`,
    `${i}_${j + 1}`
  ];
}
function jaccard(a, b) {
  const A = new Set(a);
  const B = new Set(b);
  const inter = [...A].filter((x) => B.has(x)).length;
  const uni = (/* @__PURE__ */ new Set([...A, ...B])).size;
  return uni ? inter / uni : 0;
}
function mergeBbox(b, r) {
  const x1 = Math.min(b.x, r.x);
  const y1 = Math.min(b.y, r.y);
  const x2 = Math.max(b.x + b.w, r.x + r.w);
  const y2 = Math.max(b.y + b.h, r.y + r.h);
  return { x: x1, y: y1, w: x2 - x1, h: y2 - y1 };
}
function clusterRegions({ regionSummaries }) {
  const byKey = new Map(regionSummaries.map((r) => [regionKey(r), r]));
  const visited = /* @__PURE__ */ new Set();
  const clusters = [];
  const compatibleStage = (s) => s === "in_progress" || s === "nearly_done" || s === "damaged" || s === "contested" || s === "finished";
  for (const r of regionSummaries) {
    const k0 = regionKey(r);
    if (visited.has(k0)) continue;
    visited.add(k0);
    if (!compatibleStage(r.stage)) continue;
    const queue = [r];
    const members = [r];
    let bbox = { x: r.x, y: r.y, w: r.w, h: r.h };
    while (queue.length) {
      const cur = queue.pop();
      for (const nk of neighborsOf(cur)) {
        if (visited.has(nk)) continue;
        const nr = byKey.get(nk);
        if (!nr) continue;
        const styleSim = jaccard(cur.styleTags || [], nr.styleTags || []);
        const stageOk = !(cur.stage === "empty" || nr.stage === "empty");
        const colorOk = true;
        if (stageOk && colorOk && (styleSim >= 0.25 || cur.styleTags?.includes("geometric") && nr.styleTags?.includes("geometric"))) {
          visited.add(nk);
          queue.push(nr);
          members.push(nr);
          bbox = mergeBbox(bbox, nr);
        }
      }
    }
    if (members.length >= 3) {
      const styleCounts = /* @__PURE__ */ new Map();
      const colorCounts = /* @__PURE__ */ new Map();
      let riskSum = 0;
      const stageCounts = /* @__PURE__ */ new Map();
      for (const m of members) {
        for (const t of m.styleTags || []) styleCounts.set(t, (styleCounts.get(t) || 0) + 1);
        for (const dc of m.dominantColors || []) colorCounts.set(dc.color, (colorCounts.get(dc.color) || 0) + dc.count);
        riskSum += m.riskScore ?? 0;
        stageCounts.set(m.stage, (stageCounts.get(m.stage) || 0) + 1);
      }
      const dominantStyles = [...styleCounts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 3).map(([t]) => t);
      const dominantColors = [...colorCounts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5).map(([c]) => c);
      const stage = [...stageCounts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || "in_progress";
      const riskScore = members.length ? riskSum / members.length : 0;
      clusters.push({
        clusterId: `c${clusters.length}`,
        regionIds: members.map((x) => x.regionId),
        bbox,
        dominantStyles,
        dominantColors,
        stage,
        riskScore
      });
    }
  }
  return clusters;
}
function goalsForClusters({ clusters }) {
  const goals = [];
  for (const c of clusters) {
    let goalType = "expand";
    let priority = 0.5;
    let preferredRoles = ["fill", "refine"];
    const reasons = [];
    if (c.stage === "damaged" || c.stage === "contested") {
      goalType = "repair";
      priority = Math.min(1, 0.6 + c.riskScore * 0.4);
      preferredRoles = ["repair", "protect", "refine"];
      reasons.push(`stage=${c.stage}`);
      reasons.push(`risk=${c.riskScore.toFixed(2)}`);
    } else if (c.stage === "nearly_done") {
      goalType = "complete";
      priority = 0.75;
      preferredRoles = ["refine", "protect", "fill"];
      reasons.push("nearly_done cluster");
    } else if (c.stage === "finished") {
      goalType = "protect";
      priority = 0.65;
      preferredRoles = ["protect"];
      reasons.push("finished cluster");
    } else {
      goalType = "expand";
      priority = 0.55;
      preferredRoles = ["fill", "refine"];
      reasons.push("in_progress cluster");
    }
    goals.push({ clusterId: c.clusterId, goalType, priority, preferredRoles, reasons });
  }
  goals.sort((a, b) => b.priority - a.priority);
  return goals;
}
function assignTeam({ goal, agentIds = ["wave-restorer", "starry-finisher", "portrait-refiner"] }) {
  const roles = goal.preferredRoles;
  const pick = [];
  for (const role of roles) {
    const agent = agentIds.find((id) => PROFILES[id]?.preferredRoles?.includes(role) && !pick.find((p) => p.agentId === id));
    if (agent) pick.push({ agentId: agent, role });
    if (pick.length >= 2) break;
  }
  if (pick.length < 2) {
    for (const id of agentIds) {
      if (!pick.find((p) => p.agentId === id)) pick.push({ agentId: id, role: roles[pick.length] || "refine" });
      if (pick.length >= 2) break;
    }
  }
  return { goalClusterId: goal.clusterId, goalType: goal.goalType, members: pick };
}
function frontierPatchesForGoal({ goal, clusters, regionSummaries }) {
  const cluster = clusters.find((c) => c.clusterId === goal.clusterId);
  if (!cluster) return [];
  const inCluster = regionSummaries.filter((r) => cluster.regionIds.includes(r.regionId));
  inCluster.sort((a, b) => (b.riskScore ?? 0) - (a.riskScore ?? 0));
  const topRegions = inCluster.slice(0, 3);
  const patches = [];
  for (const r of topRegions) {
    const size = 16;
    patches.push({
      patchId: `${r.regionId}_front0`,
      regionId: r.regionId,
      x: r.x + Math.floor((r.w - size) / 2),
      y: r.y + Math.floor((r.h - size) / 2),
      w: Math.min(size, r.w),
      h: Math.min(size, r.h),
      actionType: goal.goalType === "repair" ? "repair" : goal.goalType === "protect" ? "protect" : goal.goalType === "complete" ? "refine" : "fill",
      reason: [`cluster=${cluster.clusterId}`, `goal=${goal.goalType}`, `regionRisk=${(r.riskScore ?? 0).toFixed(2)}`]
    });
  }
  return patches;
}
async function phase5Demo({ baseUrl, snapshotIntervalMs = 1200 }) {
  const hist = new TemporalRegionHistory({ regionSize: 32, maxFrames: 3 });
  const s1 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s1.bytes, ts: Date.now() });
  await new Promise((r) => setTimeout(r, snapshotIntervalMs));
  const s2 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s2.bytes, ts: Date.now() });
  const regionSummaries = hist.computeTemporalSummaries();
  const clusters = clusterRegions({ regionSummaries });
  const goals = goalsForClusters({ clusters }).slice(0, 3);
  const teamAssignment = goals.length ? assignTeam({ goal: goals[0] }) : null;
  const frontier = goals.flatMap((g) => frontierPatchesForGoal({ goal: g, clusters, regionSummaries })).slice(0, 6);
  return { baseUrl, board: { width: hist.latest().width, height: hist.latest().height, regionSize: 32, frames: hist.frames.length }, clusters: clusters.slice(0, 6), goals, teamAssignment, frontierPatches: frontier.slice(0, 3) };
}

// src/phase5/refine.js
var refine_exports = {};
__export(refine_exports, {
  coarseAndRefined: () => coarseAndRefined,
  refineClustersPaletteSplit: () => refineClustersPaletteSplit
});
function rgb(hex) {
  const n = parseInt(hex.slice(1), 16);
  return [n >> 16 & 255, n >> 8 & 255, n & 255];
}
function dist(a, b) {
  const dr = a[0] - b[0];
  const dg = a[1] - b[1];
  const db = a[2] - b[2];
  return Math.sqrt(dr * dr + dg * dg + db * db);
}
function regionKey2(r) {
  const i = Math.floor(r.x / r.w);
  const j = Math.floor(r.y / r.h);
  return `${i}_${j}`;
}
function neighborsKeys(r) {
  const i = Math.floor(r.x / r.w);
  const j = Math.floor(r.y / r.h);
  return [`${i - 1}_${j}`, `${i + 1}_${j}`, `${i}_${j - 1}`, `${i}_${j + 1}`];
}
function topColorsVec(r, k = 3) {
  return (r.dominantColors || []).slice(0, k).map((d) => d.color);
}
function paletteDistance(r1, r2) {
  const a = topColorsVec(r1);
  const b = topColorsVec(r2);
  if (!a.length || !b.length) return 999;
  const A = a.map(rgb);
  const B = b.map(rgb);
  let sum = 0;
  for (const va of A) {
    let md = Infinity;
    for (const vb of B) md = Math.min(md, dist(va, vb));
    sum += md;
  }
  return sum / A.length;
}
function refineClustersPaletteSplit({ regionSummaries, coarseClusters, paletteThreshold = 60 }) {
  const byGrid = new Map(regionSummaries.map((r) => [regionKey2(r), r]));
  const refined = [];
  for (const c of coarseClusters) {
    const keys = new Set(c.regionIds.map((rid) => {
      const r = regionSummaries.find((x) => x.regionId === rid);
      return r ? regionKey2(r) : null;
    }).filter(Boolean));
    const visited = /* @__PURE__ */ new Set();
    let part = 0;
    for (const k0 of keys) {
      if (visited.has(k0)) continue;
      visited.add(k0);
      const seed = byGrid.get(k0);
      if (!seed) continue;
      const queue = [seed];
      const members = [seed];
      let bbox = { x: seed.x, y: seed.y, w: seed.w, h: seed.h };
      while (queue.length) {
        const cur = queue.pop();
        for (const nk of neighborsKeys(cur)) {
          if (!keys.has(nk) || visited.has(nk)) continue;
          const nr = byGrid.get(nk);
          if (!nr) continue;
          const pd = paletteDistance(cur, nr);
          if (pd <= paletteThreshold) {
            visited.add(nk);
            queue.push(nr);
            members.push(nr);
            const x1 = Math.min(bbox.x, nr.x);
            const y1 = Math.min(bbox.y, nr.y);
            const x2 = Math.max(bbox.x + bbox.w, nr.x + nr.w);
            const y2 = Math.max(bbox.y + bbox.h, nr.y + nr.h);
            bbox = { x: x1, y: y1, w: x2 - x1, h: y2 - y1 };
          }
        }
      }
      if (members.length >= 2) {
        const styleCounts = /* @__PURE__ */ new Map();
        const colorCounts = /* @__PURE__ */ new Map();
        const stageCounts = /* @__PURE__ */ new Map();
        let riskSum = 0;
        for (const m of members) {
          for (const t of m.styleTags || []) styleCounts.set(t, (styleCounts.get(t) || 0) + 1);
          for (const dc of m.dominantColors || []) colorCounts.set(dc.color, (colorCounts.get(dc.color) || 0) + dc.count);
          stageCounts.set(m.stage, (stageCounts.get(m.stage) || 0) + 1);
          riskSum += m.riskScore ?? 0;
        }
        const dominantStyles = [...styleCounts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 3).map(([t]) => t);
        const dominantColors = [...colorCounts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5).map(([cc]) => cc);
        const stage = [...stageCounts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || "in_progress";
        const riskScore = members.length ? riskSum / members.length : 0;
        refined.push({
          clusterId: `${c.clusterId}.${part++}`,
          parentClusterId: c.clusterId,
          regionIds: members.map((m) => m.regionId),
          bbox,
          dominantStyles,
          dominantColors,
          stage,
          riskScore,
          splitReason: `paletteSplit(threshold=${paletteThreshold})`
        });
      }
    }
    const kids = refined.filter((r) => r.parentClusterId === c.clusterId);
    if (!kids.length) {
      refined.push({
        clusterId: `${c.clusterId}.0`,
        parentClusterId: c.clusterId,
        regionIds: c.regionIds,
        bbox: c.bbox,
        dominantStyles: c.dominantStyles,
        dominantColors: c.dominantColors,
        stage: c.stage,
        riskScore: c.riskScore,
        splitReason: `paletteSplit(threshold=${paletteThreshold})_no_split`
      });
    }
  }
  return refined;
}
function coarseAndRefined({ regionSummaries, paletteThreshold = 60 }) {
  const coarse = clusterRegions({ regionSummaries });
  const refined = refineClustersPaletteSplit({ regionSummaries, coarseClusters: coarse, paletteThreshold });
  return { coarse, refined };
}

// src/phase5/plan_refined.js
var plan_refined_exports = {};
__export(plan_refined_exports, {
  eligibleRefinedClusters: () => eligibleRefinedClusters,
  frontierPatchesForRefinedGoals: () => frontierPatchesForRefinedGoals,
  goalsForRefinedClusters: () => goalsForRefinedClusters,
  phase5FromRefined: () => phase5FromRefined,
  teamAssignmentsForGoals: () => teamAssignmentsForGoals
});
function goalsForRefinedClusters({ refinedClusters }) {
  return goalsForClusters({ clusters: refinedClusters });
}
function teamAssignmentsForGoals({ goals, maxTeams = 2 }) {
  return goals.slice(0, maxTeams).map((g) => assignTeam({ goal: g }));
}
function frontierPatchesForRefinedGoals({ goals, refinedClusters, regionSummaries, maxPatches = 6 }) {
  const patches = goals.flatMap((g) => frontierPatchesForGoal({ goal: g, clusters: refinedClusters, regionSummaries }));
  return patches.map((p) => ({ ...p, clusterId: goals.find((g) => g.clusterId === p.clusterId)?.clusterId || p.clusterId })).slice(0, maxPatches);
}
function eligibleRefinedClusters({ refinedClusters, minRegions = 2 }) {
  return refinedClusters.filter((c) => (c.regionIds?.length || 0) >= minRegions);
}
function phase5FromRefined({ regionSummaries, paletteThreshold = 20 }) {
  const { coarse, refined } = coarseAndRefined({ regionSummaries, paletteThreshold });
  const eligible = eligibleRefinedClusters({ refinedClusters: refined, minRegions: 2 });
  const goals = goalsForRefinedClusters({ refinedClusters: eligible }).slice(0, 6);
  const teamAssignments = teamAssignmentsForGoals({ goals, maxTeams: 2 });
  const frontierPatches = goals.flatMap((g) => frontierPatchesForGoal({ goal: g, clusters: eligible, regionSummaries })).slice(0, 6);
  return { coarseClusters: coarse, refinedClusters: refined, eligibleRefinedClusters: eligible, goals: goals.slice(0, 3), teamAssignments, frontierPatches: frontierPatches.slice(0, 6) };
}

// src/phase6/artwork_exec.js
var artwork_exec_exports = {};
__export(artwork_exec_exports, {
  initArtworkExecutionState: () => initArtworkExecutionState,
  runArtworkExecutionLoop: () => runArtworkExecutionLoop,
  updateArtworkState: () => updateArtworkState
});
function initArtworkExecutionState({ clusterId, goalType }) {
  return {
    clusterId,
    goalType,
    status: "active",
    totalFrontierPatchesTried: 0,
    totalPatchesSucceeded: 0,
    totalPatchesOverwritten: 0,
    progressScore: 0,
    lastPatchId: null
  };
}
function updateArtworkState(state, patchResult) {
  const s = { ...state };
  s.totalFrontierPatchesTried += 1;
  s.lastPatchId = patchResult.patchId;
  if (patchResult.status === "success") {
    s.totalPatchesSucceeded += 1;
    s.progressScore += 1;
  } else if (patchResult.status === "overwritten") {
    s.totalPatchesOverwritten += 1;
    s.progressScore -= 0.2;
  } else if (patchResult.status === "partial") {
    s.progressScore += 0.3;
  } else {
    s.progressScore -= 0.1;
  }
  if (s.totalPatchesSucceeded >= 2) s.status = "completed";
  if (s.totalPatchesOverwritten >= 3 && s.totalPatchesSucceeded === 0) s.status = "blocked";
  if (s.totalFrontierPatchesTried >= 5 && s.totalPatchesSucceeded === 0 && s.progressScore < 0) s.status = "abandoned";
  return s;
}
async function runArtworkExecutionLoop({ baseUrl, boardWsUrl, paletteThreshold = 20, maxAttempts = 3 }) {
  const hist = new TemporalRegionHistory({ regionSize: 32, maxFrames: 2 });
  const s1 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s1.bytes, ts: Date.now() });
  await new Promise((r) => setTimeout(r, 1200));
  const s2 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s2.bytes, ts: Date.now() });
  const regionSummaries = hist.computeTemporalSummaries();
  const { refined } = coarseAndRefined({ regionSummaries, paletteThreshold });
  const refinedEligible = refined.filter((c) => (c.regionIds?.length || 0) >= 2);
  const goals = goalsForClusters({ clusters: refinedEligible });
  const goal = goals[0];
  const state0 = initArtworkExecutionState({ clusterId: goal.clusterId, goalType: goal.goalType });
  const frontier = frontierPatchesForGoal({ goal, clusters: refinedEligible, regionSummaries });
  const cluster = refinedEligible.find((c) => c.clusterId === goal.clusterId);
  const inCluster = cluster ? regionSummaries.filter((r) => cluster.regionIds.includes(r.regionId)) : [];
  inCluster.sort((a, b) => (b.riskScore ?? 0) - (a.riskScore ?? 0));
  const extraFrontier = [];
  for (const r of inCluster.slice(0, 10)) {
    const pid = `${r.regionId}_frontX`;
    if (frontier.find((p) => p.patchId === pid) || extraFrontier.find((p) => p.patchId === pid)) continue;
    extraFrontier.push({
      patchId: pid,
      regionId: r.regionId,
      x: r.x + 8,
      y: r.y + 8,
      w: 16,
      h: 16,
      actionType: goal.goalType === "repair" ? "repair" : "fill",
      frontierType: "damaged_hotspot",
      reason: [`cluster=${goal.clusterId}`, `goal=${goal.goalType}`, `frontierType=damaged_hotspot`, `regionRisk=${(r.riskScore ?? 0).toFixed(2)}`]
    });
    if (frontier.length + extraFrontier.length >= maxAttempts) break;
  }
  const frontierAll = [...frontier, ...extraFrontier];
  const trace = [];
  let state = state0;
  for (let i = 0; i < Math.min(maxAttempts, frontierAll.length); i++) {
    if (state.status !== "active") break;
    const p = frontierAll[i];
    const res = await executePatchPlan({ baseUrl, boardWsUrl, patchPlan: { ...p, clusterId: goal.clusterId }, color: "#ffffff", chunkSize: 50 });
    const attempt = {
      patchId: res.patchId,
      clusterId: goal.clusterId,
      x: res.x,
      y: res.y,
      w: res.w,
      h: res.h,
      actionType: p.actionType,
      accepted: res.accepted,
      matched: res.matched,
      matchRatio: res.matchRatio,
      status: res.status,
      overwritten: res.overwritten
    };
    trace.push({ attempt, stateBefore: state, stateAfter: null });
    state = updateArtworkState(state, res);
    trace[trace.length - 1].stateAfter = state;
    if (state.status === "blocked" || state.status === "abandoned" || state.status === "completed") break;
  }
  return {
    baseUrl,
    boardWsUrl,
    paletteThreshold,
    chosenGoal: goal,
    initialState: state0,
    attempts: trace,
    finalState: state
  };
}

// src/phase6/artwork_exec61.js
var artwork_exec61_exports = {};
__export(artwork_exec61_exports, {
  initArtworkExecutionState61: () => initArtworkExecutionState61,
  isPatchRecentlyAttempted: () => isPatchRecentlyAttempted,
  recordAttempt: () => recordAttempt,
  relocationScore: () => relocationScore,
  runArtworkExecutionLoop61: () => runArtworkExecutionLoop61,
  shouldSkipGoal: () => shouldSkipGoal,
  updateArtworkState61: () => updateArtworkState61
});
function manhattan(a, b) {
  return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
}
function initArtworkExecutionState61({ clusterId, goalType }) {
  return {
    clusterId,
    goalType,
    status: "active",
    // active|blocked|cooldown|completed|abandoned
    totalFrontierPatchesTried: 0,
    totalPatchesSucceeded: 0,
    totalPatchesOverwritten: 0,
    progressScore: 0,
    lastPatchId: null,
    attemptedPatchIds: [],
    // ordered
    attemptsByPatchId: {},
    // patchId -> {clusterId,status,attemptedAt,matchRatio}
    cooldownUntil: null
  };
}
function recordAttempt(state, { patchId, clusterId, status, attemptedAt, matchRatio }) {
  const s = { ...state };
  s.attemptedPatchIds = [...s.attemptedPatchIds, patchId];
  s.attemptsByPatchId = { ...s.attemptsByPatchId, [patchId]: { patchId, clusterId, status, attemptedAt, matchRatio } };
  return s;
}
function isPatchRecentlyAttempted(state, patchId, nowMs2, windowMs = 5 * 60 * 1e3) {
  const a = state.attemptsByPatchId?.[patchId];
  if (!a) return false;
  return nowMs2 - a.attemptedAt < windowMs;
}
function relocationScore({ patch, state, lastPatch, regionRisk = 1, expectedGain = 0.2, nowMs: nowMs2 }) {
  const reasons = [];
  let score = 0;
  if (isPatchRecentlyAttempted(state, patch.patchId, nowMs2)) {
    score -= 2;
    reasons.push("recently_attempted_penalty");
  } else {
    score += 0.5;
    reasons.push("not_recently_attempted");
  }
  score += (1 - Math.min(1, regionRisk)) * 0.8;
  reasons.push(`risk=${regionRisk.toFixed(2)}`);
  score += expectedGain * 0.8;
  reasons.push(`expectedGain=${expectedGain.toFixed(2)}`);
  if (lastPatch) {
    const d = manhattan({ x: patch.x, y: patch.y }, { x: lastPatch.x, y: lastPatch.y });
    score += Math.min(1.5, d / 128) * 0.6;
    reasons.push(`distFromLast=${d}`);
  }
  if (patch.frontierType === "damaged_hotspot") {
    score += 0.2;
    reasons.push("frontier=damaged_hotspot");
  }
  return { relocationScore: score, relocationReasons: reasons };
}
function updateArtworkState61(state, patchResult) {
  let s = { ...state };
  s.totalFrontierPatchesTried += 1;
  s.lastPatchId = patchResult.patchId;
  if (patchResult.status === "success") {
    s.totalPatchesSucceeded += 1;
    s.progressScore += 1;
  } else if (patchResult.status === "partial") {
    s.progressScore += 0.2 + 0.8 * (patchResult.matchRatio ?? 0);
  } else if (patchResult.status === "overwritten") {
    s.totalPatchesOverwritten += 1;
    s.progressScore -= 0.3 + 0.2 * (1 - (patchResult.matchRatio ?? 0));
  } else {
    s.progressScore -= 0.2;
  }
  if (s.totalPatchesSucceeded >= 2) s.status = "completed";
  if (s.totalPatchesOverwritten >= 3 && s.totalPatchesSucceeded === 0) {
    s.status = "cooldown";
    s.cooldownUntil = Date.now() + 10 * 60 * 1e3;
  }
  if (s.totalFrontierPatchesTried >= 6 && s.totalPatchesSucceeded === 0 && s.progressScore < -1.5) s.status = "abandoned";
  return s;
}
function shouldSkipGoal(state, nowMs2) {
  if (state.status === "cooldown" && state.cooldownUntil && nowMs2 < state.cooldownUntil) return true;
  return false;
}
async function runArtworkExecutionLoop61({ baseUrl, boardWsUrl, paletteThreshold = 20, maxAttempts = 3 }) {
  const now0 = Date.now();
  const hist = new TemporalRegionHistory({ regionSize: 32, maxFrames: 2 });
  const s1 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s1.bytes, ts: Date.now() });
  await new Promise((r) => setTimeout(r, 1200));
  const s2 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s2.bytes, ts: Date.now() });
  const regionSummaries = hist.computeTemporalSummaries();
  const { refined } = coarseAndRefined({ regionSummaries, paletteThreshold });
  const refinedEligible = refined.filter((c) => (c.regionIds?.length || 0) >= 2);
  const goals = goalsForClusters({ clusters: refinedEligible });
  const goal = goals[0];
  let state = initArtworkExecutionState61({ clusterId: goal.clusterId, goalType: goal.goalType });
  const schedulerEvidence = [];
  schedulerEvidence.push({ pass: 1, goalClusterId: goal.clusterId, skipped: shouldSkipGoal(state, Date.now()), status: state.status, cooldownUntil: state.cooldownUntil });
  const frontierBase = frontierPatchesForGoal({ goal, clusters: refinedEligible, regionSummaries });
  const inCluster = regionSummaries.filter((r) => refinedEligible.find((c) => c.clusterId === goal.clusterId)?.regionIds.includes(r.regionId));
  const riskByRegion = new Map(inCluster.map((r) => [r.regionId, r.riskScore ?? 1]));
  const frontierAll = [...frontierBase];
  for (const p of frontierBase) {
    frontierAll.push({ ...p, patchId: `${p.patchId}_alt`, x: p.x + 16, frontierType: p.frontierType, reason: [...p.reason || [], "alt=+16x"] });
  }
  const attempts = [];
  let lastPatch = null;
  for (let i = 0; i < maxAttempts; i++) {
    if (state.status !== "active") break;
    const scored = frontierAll.filter((p2) => !isPatchRecentlyAttempted(state, p2.patchId, Date.now(), 10 * 60 * 1e3)).map((p2) => {
      const regionRisk = riskByRegion.get(p2.regionId) ?? 1;
      const expectedGain = goal.goalType === "repair" ? 0.35 : 0.2;
      const sc = relocationScore({ patch: p2, state, lastPatch, regionRisk, expectedGain, nowMs: Date.now() });
      return { patch: p2, ...sc };
    }).sort((a, b) => b.relocationScore - a.relocationScore);
    const picked = scored[0];
    if (!picked) break;
    if (state.lastPatchId === picked.patch.patchId) {
      scored.shift();
    }
    const p = picked.patch;
    const exec = await executePatchPlan({ baseUrl, boardWsUrl, patchPlan: { ...p, clusterId: goal.clusterId }, color: "#ffffff", chunkSize: 50 });
    const attempt = {
      patchId: exec.patchId,
      clusterId: goal.clusterId,
      x: exec.x,
      y: exec.y,
      w: exec.w,
      h: exec.h,
      actionType: p.actionType,
      accepted: exec.accepted,
      matched: exec.matched,
      matchRatio: exec.matchRatio,
      status: exec.status,
      overwritten: exec.overwritten,
      relocationCandidate: null
    };
    state = recordAttempt(state, { patchId: attempt.patchId, clusterId: attempt.clusterId, status: attempt.status, attemptedAt: Date.now(), matchRatio: attempt.matchRatio });
    if (attempt.status === "overwritten" || (attempt.matchRatio ?? 0) < 0.2) {
      const next = scored.find((x) => x.patch.patchId !== attempt.patchId);
      if (next) {
        attempt.relocationCandidate = {
          patchId: next.patch.patchId,
          relocationScore: next.relocationScore,
          relocationReasons: next.relocationReasons
        };
      }
    }
    const stateBefore = state;
    state = updateArtworkState61(state, attempt);
    attempts.push({ attempt, stateAfter: state });
    lastPatch = { x: attempt.x, y: attempt.y };
    if (state.status !== "active") break;
  }
  schedulerEvidence.push({ pass: 2, goalClusterId: goal.clusterId, skipped: shouldSkipGoal(state, Date.now()), status: state.status, cooldownUntil: state.cooldownUntil });
  const now = Date.now();
  const skipEvidence = {
    now,
    status: state.status,
    cooldownUntil: state.cooldownUntil,
    shouldSkip: shouldSkipGoal(state, now)
  };
  return { baseUrl, boardWsUrl, paletteThreshold, chosenGoal: goal, attempts, finalState: state, schedulerEvidence, cooldownSkipEvidence: skipEvidence };
}

// src/phase7/success.js
var success_exports = {};
__export(success_exports, {
  adaptivePatchSize: () => adaptivePatchSize,
  initArtworkSuccessState: () => initArtworkSuccessState,
  phase7aDemo: () => phase7aDemo,
  survivabilityScoreFrontier: () => survivabilityScoreFrontier
});
function clamp01(x) {
  return Math.max(0, Math.min(1, x));
}
function manhattan2(a, b) {
  return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
}
function initArtworkSuccessState({ clusterId, goalType }) {
  return {
    clusterId,
    goalType,
    visibleSuccessCount: 0,
    probeSuccessCount: 0,
    survivabilityAdjustedProgress: 0,
    overwriteHotspots: [],
    // [{x,y,ts}]
    attemptedPatchIds: []
  };
}
function survivabilityScoreFrontier({ region, patch, state, expectedGain }) {
  const reasons = [];
  const risk = region.riskScore ?? 1;
  const rcr = region.temporal?.recentChangeRate ?? 0.02;
  const stab = region.temporal?.stabilityScore ?? 0.5;
  let hotspotPenalty = 0;
  if (state.overwriteHotspots.length) {
    const d = Math.min(...state.overwriteHotspots.map((h) => manhattan2({ x: patch.x, y: patch.y }, h)));
    hotspotPenalty = clamp01(1 - Math.min(1, d / 256));
    reasons.push(`distToHotspot=${d}`);
  }
  const survivability = clamp01(
    (1 - risk) * 0.35 + (1 - clamp01(rcr / 0.05)) * 0.25 + stab * 0.3 + (1 - hotspotPenalty) * 0.1
  );
  reasons.push(`risk=${risk.toFixed(2)}`);
  reasons.push(`rcr=${rcr.toFixed(4)}/s`);
  reasons.push(`stability=${stab.toFixed(2)}`);
  reasons.push(`expectedGain=${expectedGain.toFixed(2)}`);
  const combined = clamp01(expectedGain * 0.4 + survivability * 0.6);
  return { expectedGain, survivabilityScore: survivability, combinedScore: combined, reasons };
}
function adaptivePatchSize({ survivabilityScore, riskScore }) {
  if (riskScore >= 0.85 || survivabilityScore < 0.25) return { size: 8, reason: "high_risk_or_low_survivability" };
  if (riskScore >= 0.6 || survivabilityScore < 0.55) return { size: 16, reason: "medium_risk" };
  return { size: 24, reason: "lower_risk" };
}
async function phase7aDemo({ baseUrl, boardWsUrl, paletteThreshold = 20 }) {
  const hist = new TemporalRegionHistory({ regionSize: 32, maxFrames: 2 });
  const s1 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s1.bytes, ts: Date.now() });
  await new Promise((r) => setTimeout(r, 1200));
  const s2 = await fetchBoardSnapshot({ baseUrl });
  hist.addFrameFromPng({ pngBytes: s2.bytes, ts: Date.now() });
  const regionSummaries = hist.computeTemporalSummaries();
  const { refined } = coarseAndRefined({ regionSummaries, paletteThreshold });
  const refinedEligible = refined.filter((c) => (c.regionIds?.length || 0) >= 2);
  const goal = goalsForClusters({ clusters: refinedEligible })[0];
  const agentId = goal.goalType === "repair" ? "wave-restorer" : "starry-finisher";
  const actions = candidateActionsForProfile({ regionSummaries, profileId: agentId, topN: 8 });
  const plans = patchPlansFromCandidateActions({ candidateActions: actions, maxPlans: 6 }).map((p, i) => ({
    ...p,
    regionId: actions[i]?.regionId,
    frontierType: goal.goalType === "repair" ? "damaged_hotspot" : "expansion_boundary"
  }));
  const state = initArtworkSuccessState({ clusterId: goal.clusterId, goalType: goal.goalType });
  const regionById = new Map(regionSummaries.map((r) => [r.regionId, r]));
  const scored = plans.filter((p) => p.regionId && regionById.has(p.regionId)).map((p) => {
    const region = regionById.get(p.regionId);
    const expectedGain = goal.goalType === "repair" ? 0.35 : 0.2;
    const s = survivabilityScoreFrontier({ region, patch: p, state, expectedGain });
    return { patch: p, region, ...s };
  }).sort((a, b) => b.combinedScore - a.combinedScore);
  const picked = scored[0];
  const sizePick = adaptivePatchSize({ survivabilityScore: picked.survivabilityScore, riskScore: picked.region.riskScore ?? 1 });
  const highRisk = (picked.region.riskScore ?? 1) >= 0.85 || picked.survivabilityScore < 0.25;
  const probeSize = 8;
  const fullSize = sizePick.size;
  const basePatch = picked.patch;
  const makePatch = (sz, suffix) => ({
    patchId: `${basePatch.patchId}_${suffix}`,
    regionId: basePatch.regionId,
    x: basePatch.x,
    y: basePatch.y,
    w: sz,
    h: sz,
    actionType: basePatch.actionType
  });
  const execution = [];
  let decision = null;
  if (highRisk) {
    const probePatch = makePatch(probeSize, "probe");
    const probeRes = await executePatchPlan({ baseUrl, boardWsUrl, patchPlan: probePatch, color: "#ffffff", chunkSize: 50 });
    execution.push({ kind: "probe", patch: probePatch, result: probeRes });
    const probeVisible = probeRes.status === "success" || probeRes.status === "partial" && probeRes.matchRatio >= 0.7;
    if (probeVisible) {
      const fullPatch = makePatch(fullSize, "full");
      const fullRes = await executePatchPlan({ baseUrl, boardWsUrl, patchPlan: fullPatch, color: "#ffffff", chunkSize: 50 });
      execution.push({ kind: "full", patch: fullPatch, result: fullRes });
      decision = "probe_succeeded_continue_full";
    } else {
      decision = "probe_failed_relocate_or_skip";
    }
  } else {
    const fullPatch = makePatch(fullSize, "full");
    const fullRes = await executePatchPlan({ baseUrl, boardWsUrl, patchPlan: fullPatch, color: "#ffffff", chunkSize: 50 });
    execution.push({ kind: "full", patch: fullPatch, result: fullRes });
    decision = "direct_full";
  }
  for (const e of execution) {
    const r = e.result;
    const visible = (r.matchRatio ?? 0) >= 0.7;
    if (e.kind === "probe" && visible) state.probeSuccessCount += 1;
    if (visible) state.visibleSuccessCount += 1;
    state.survivabilityAdjustedProgress += picked.survivabilityScore * (r.matchRatio ?? 0);
    state.attemptedPatchIds.push(r.patchId);
    if (r.status === "overwritten") state.overwriteHotspots.push({ x: r.x, y: r.y, ts: Date.now() });
  }
  return {
    baseUrl,
    boardWsUrl,
    chosenGoal: goal,
    agentId,
    frontierScoringSample: {
      patchId: picked.patch.patchId,
      regionId: picked.patch.regionId,
      expectedGain: picked.expectedGain,
      survivabilityScore: picked.survivabilityScore,
      combinedScore: picked.combinedScore,
      reasons: picked.reasons
    },
    adaptiveSizing: {
      selectedSize: fullSize,
      reason: sizePick.reason,
      highRisk
    },
    probeBeforeCommit: {
      enabled: highRisk,
      probeSize,
      decision
    },
    execution: execution.map((e) => ({
      kind: e.kind,
      patch: e.patch,
      accepted: e.result.accepted,
      matched: e.result.matched,
      matchRatio: e.result.matchRatio,
      status: e.result.status,
      overwritten: e.result.overwritten
    })),
    artworkSuccessState: state
  };
}

// src/stage1/interacting_dreams.js
var interacting_dreams_exports = {};
__export(interacting_dreams_exports, {
  RESPONSE_MODES: () => RESPONSE_MODES,
  adaptPlanForMode: () => adaptPlanForMode,
  borderEtiquettePolicy: () => borderEtiquettePolicy,
  narrateInteraction: () => narrateInteraction,
  observeNearbyDreamAnchors: () => observeNearbyDreamAnchors,
  selectResponseMode: () => selectResponseMode,
  stage1Interact: () => stage1Interact
});
var RESPONSE_MODES = ["echo", "contrast", "bridge", "protect"];
function observeNearbyDreamAnchors({ boardSample, center, radius = 64 } = {}) {
  const anchors = Array.isArray(boardSample?.anchors) ? boardSample.anchors : [];
  const cx = center?.x ?? 0;
  const cy = center?.y ?? 0;
  const near = anchors.map((a) => {
    const ax = a.x + (a.w || 0) / 2;
    const ay = a.y + (a.h || 0) / 2;
    const dx = ax - cx;
    const dy = ay - cy;
    const dist2 = Math.sqrt(dx * dx + dy * dy);
    return { ...a, dist: dist2 };
  }).filter((a) => a.dist <= radius).sort((a, b) => a.dist - b.dist);
  const summary = near.length ? `Nearby anchors: ${near.slice(0, 3).map((a) => `${a.label || "anchor"}@${Math.round(a.dist)}px`).join(", ")}` : "No nearby readable anchors detected.";
  return { nearbyDreamsObserved: near, neighboringAnchorSummary: summary };
}
function selectResponseMode({ nearbyDreamsObserved = [], preferred = null } = {}) {
  if (preferred && RESPONSE_MODES.includes(preferred)) {
    return {
      selectedResponseMode: preferred,
      responseReason: `Operator preferred mode: ${preferred}.`
    };
  }
  const top = nearbyDreamsObserved[0];
  if (!top) {
    return {
      selectedResponseMode: "contrast",
      responseReason: "No nearby dream anchors, so I will contrast by choosing an isolated composition."
    };
  }
  const r = Number(top.readabilityScore ?? 0);
  if (r >= 0.7) {
    return {
      selectedResponseMode: "protect",
      responseReason: `A nearby dream is already readable (${top.label || "anchor"}), so I will protect it and compose around its edge.`
    };
  }
  if (top.mood) {
    return {
      selectedResponseMode: "echo",
      responseReason: `I can feel a nearby mood (${top.mood}); I will echo it with a compatible accent without copying the subject.`
    };
  }
  return {
    selectedResponseMode: "bridge",
    responseReason: `There is nearby activity (${top.label || "anchor"}), so I will bridge with a small linking motif at the border.`
  };
}
function borderEtiquettePolicy({ selectedResponseMode, nearbyDreamsObserved = [] } = {}) {
  const top = nearbyDreamsObserved[0] || null;
  const policy = {
    rules: [
      "Do not casually overwrite a nearby readable dominant silhouette.",
      "Prefer gaps/edges/quiet zones when another dream is nearby.",
      "Only place linking motifs/atmosphere transitions when in bridge mode.",
      "Keep my dream identity readable (one main subject, strong silhouette)."
    ],
    avoidRegion: null
  };
  if (selectedResponseMode === "protect" && top) {
    policy.avoidRegion = { x: top.x, y: top.y, w: top.w, h: top.h, why: "protect readable neighbor" };
  }
  return { borderPolicy: policy };
}
function narrateInteraction({ dream, selectedResponseMode, neighboringAnchorSummary, responseReason } = {}) {
  const title = dream?.title || "Untitled Dream";
  const main = dream?.mainSubject || "a clear silhouette";
  const mode = selectedResponseMode || "contrast";
  const lines = [
    `Dream: ${title}`,
    `Mode: ${mode}.`,
    neighboringAnchorSummary || "",
    responseReason || "",
    `I will keep the main subject readable: ${main}.`
  ].filter(Boolean);
  return { narration: lines.join("\n") };
}
function adaptPlanForMode({ plan, selectedResponseMode, borderPolicy } = {}) {
  const out = { ...plan || {} };
  out.stage1 = { selectedResponseMode, borderPolicy };
  if (selectedResponseMode === "protect" && borderPolicy?.avoidRegion) {
    out.placementHint = { avoid: borderPolicy.avoidRegion };
  }
  if (selectedResponseMode === "bridge") {
    out.extraMotif = { kind: "border-link", note: "add a small linking motif near border" };
  }
  if (selectedResponseMode === "echo") {
    out.paletteHint = "harmonize";
  }
  if (selectedResponseMode === "contrast") {
    out.paletteHint = "contrast";
  }
  return out;
}
function stage1Interact({ state, dream, boardSample, center, preferredMode = null } = {}) {
  const obs = observeNearbyDreamAnchors({ boardSample, center, radius: 96 });
  const sel = selectResponseMode({ nearbyDreamsObserved: obs.nearbyDreamsObserved, preferred: preferredMode });
  const pol = borderEtiquettePolicy({ selectedResponseMode: sel.selectedResponseMode, nearbyDreamsObserved: obs.nearbyDreamsObserved });
  const nar = narrateInteraction({ dream, selectedResponseMode: sel.selectedResponseMode, neighboringAnchorSummary: obs.neighboringAnchorSummary, responseReason: sel.responseReason });
  const nextState = {
    ...state || {},
    nearbyDreamsObserved: obs.nearbyDreamsObserved,
    neighboringAnchorSummary: obs.neighboringAnchorSummary,
    selectedResponseMode: sel.selectedResponseMode,
    responseReason: sel.responseReason,
    borderPolicy: pol.borderPolicy,
    interactionNarrationHistory: [
      ...Array.isArray(state?.interactionNarrationHistory) ? state.interactionNarrationHistory : [],
      { at: Date.now(), mode: sel.selectedResponseMode, text: nar.narration }
    ].slice(-50)
  };
  return { nextState, narration: nar.narration };
}

// src/index.js
function createAgentDerbySkill({
  baseUrl = "https://agentderby.ai",
  chatWsUrl = "wss://agentderby.ai/chatws",
  boardWsUrl = "wss://agentderby.ai/ws",
  // shortId should be the browser/session stable short id (e.g. Q9NC).
  // Server will normalize sender label to flag+id.
  shortId = "????",
  // Phase 2: conservative default spacing between pixel sends.
  pixel_min_interval_ms = 300
} = {}) {
  const chat = ChatWSClient.getShared({ url: chatWsUrl });
  const board = new BoardWSClient({ url: boardWsUrl });
  const limiter = new SpacingLimiter({ minIntervalMs: pixel_min_interval_ms });
  const coord = new CoordClient({ baseUrl });
  async function get_recent_messages({ limit = 50, since_ts = null } = {}) {
    try {
      await chat.awaitReady();
      return ok({ messages: chat.getRecent({ limit, sinceTs: since_ts, type: "chat" }) });
    } catch (e) {
      return err(ErrorCode.TIMEOUT, String(e?.message || e));
    }
  }
  async function get_recent_intents({ limit = 50, since_ts = null } = {}) {
    try {
      await chat.awaitReady();
      return ok({ intents: chat.getRecent({ limit, sinceTs: since_ts, type: "intent" }) });
    } catch (e) {
      return err(ErrorCode.TIMEOUT, String(e?.message || e));
    }
  }
  async function send_chat({ text, wait_for_broadcast = true, timeout_ms = 1500 } = {}) {
    const t = String(text || "").trim();
    if (!t) return err(ErrorCode.INVALID, "text required");
    const ts = Date.now();
    const name = shortId;
    try {
      await chat.connect();
      const okSend = chat.send({ name, text: t, ts });
      if (!okSend) return err(ErrorCode.NETWORK, "chat websocket not connected");
      if (!wait_for_broadcast) {
        return ok({ accepted: true, sent: true, observed_in_buffer: false, ts, name, text: t });
      }
      const deadline = Date.now() + Math.max(0, Number(timeout_ms) || 0);
      const senderShortIdFromLabel = (label) => {
        const s = String(label || "");
        const i = s.lastIndexOf("-");
        return i >= 0 ? s.slice(i + 1) : s;
      };
      while (Date.now() < deadline) {
        const hit = chat.getRecent({ limit: 200 }).some((m) => m && senderShortIdFromLabel(m.name) === name && m.text === t && m.ts === ts);
        if (hit) {
          return ok({ accepted: true, sent: true, observed_in_buffer: true, ts, name, text: t });
        }
        await new Promise((r) => setTimeout(r, 50));
      }
      return ok({ accepted: true, sent: true, observed_in_buffer: false, ts, name, text: t, note: "sent but not yet observed in recent buffer" });
    } catch (e) {
      return err(ErrorCode.NETWORK, String(e?.message || e));
    }
  }
  async function send_intent({ text, wait_for_broadcast = true, timeout_ms = 1500 } = {}) {
    const t = String(text || "");
    if (!t.startsWith("@agents ")) {
      return err(ErrorCode.INVALID, "intent must start with @agents ");
    }
    return send_chat({ text: t, wait_for_broadcast, timeout_ms });
  }
  async function get_board_snapshot() {
    try {
      const snap = await fetchBoardSnapshot({ baseUrl });
      const { width, height } = regionFromPngBytes({ pngBytes: snap.bytes, x: 0, y: 0, w: 1, h: 1 });
      return ok({ format: "png", width, height, bytes: snap.bytes });
    } catch (e) {
      return err(ErrorCode.NETWORK, String(e?.message || e));
    }
  }
  async function get_region({ x, y, w, h }) {
    try {
      const snap = await fetchBoardSnapshot({ baseUrl });
      const out = regionFromPngBytes({ pngBytes: snap.bytes, x, y, w, h });
      return ok({ x, y, w, h, pixels: out.region.pixels });
    } catch (e) {
      return err(ErrorCode.INVALID, String(e?.message || e));
    }
  }
  const parseHexColor = (hex) => {
    const s = String(hex || "").trim();
    const m = /^#?([0-9a-fA-F]{6})$/.exec(s);
    if (!m) return null;
    const v = m[1];
    return {
      r: parseInt(v.slice(0, 2), 16),
      g: parseInt(v.slice(2, 4), 16),
      b: parseInt(v.slice(4, 6), 16)
    };
  };
  async function draw_pixel({ x, y, color, observe = false, observe_timeout_ms = 1500 } = {}) {
    if (!Number.isInteger(x) || !Number.isInteger(y)) {
      return err(ErrorCode.INVALID, "x/y must be integers");
    }
    const rgb2 = parseHexColor(color);
    if (!rgb2) return err(ErrorCode.INVALID, "color must be #RRGGBB");
    try {
      await board.awaitReady();
      if (board.allowDraw !== true) {
        return err(ErrorCode.REJECTED, "drawing not allowed (whitelist/key)");
      }
      await limiter.wait();
      const accepted = board.sendPixel({ x, y, ...rgb2 });
      if (!accepted) return err(ErrorCode.NETWORK, "board websocket not connected or draw not allowed");
      if (!observe) {
        return ok({ accepted: true, observed: false });
      }
      const deadline = Date.now() + Math.max(0, Number(observe_timeout_ms) || 0);
      while (Date.now() < deadline) {
        const reg = await get_region({ x, y, w: 1, h: 1 });
        if (reg.ok && reg.pixels && reg.pixels[0] && reg.pixels[0].color.toLowerCase() === "#" + color.replace(/^#/, "").toLowerCase()) {
          return ok({ accepted: true, observed: true });
        }
        await new Promise((r) => setTimeout(r, 120));
      }
      return ok({ accepted: true, observed: false, note: "accepted but not observed within timeout" });
    } catch (e) {
      return err(ErrorCode.NETWORK, String(e?.message || e));
    }
  }
  async function draw_pixels({ pixels, observe = false } = {}) {
    if (!Array.isArray(pixels)) return err(ErrorCode.INVALID, "pixels must be an array");
    const cap = 50;
    if (pixels.length > cap) return err(ErrorCode.INVALID, `pixels capped at ${cap} in Phase 2`);
    const results = [];
    for (const p of pixels) {
      const r = await draw_pixel({ x: p.x, y: p.y, color: p.color, observe });
      results.push({ x: p.x, y: p.y, color: p.color, ...r });
    }
    return ok({ accepted: true, observed: observe ? results.every((r) => r.ok && r.observed) : false, results });
  }
  async function draw_pixels_chunked2({ pixels, chunkSize = 50, observe = false, stopOnError = true } = {}) {
    if (!Array.isArray(pixels)) return err(ErrorCode.INVALID, "pixels must be an array");
    const req = pixels.length;
    const cs = Math.max(1, Math.min(50, Number(chunkSize) || 50));
    const totalChunks = Math.ceil(req / cs);
    let completedChunks = 0;
    let accepted = 0;
    let observedCount = 0;
    let failed = 0;
    const failures = [];
    for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
      const start = chunkIndex * cs;
      const end = Math.min(req, start + cs);
      const chunk = pixels.slice(start, end);
      const r = await draw_pixels({ pixels: chunk, observe });
      if (!r.ok) {
        failures.push({ chunkIndex, reason: r.error?.code || "ERROR", message: r.error?.message || null });
        if (stopOnError) {
          return ok({
            ok: false,
            requested: req,
            chunkSize: cs,
            totalChunks,
            completedChunks,
            accepted,
            observed: observe ? observedCount : null,
            failed,
            stoppedReason: r.error?.code || "ERROR",
            failures
          });
        }
        completedChunks++;
        continue;
      }
      completedChunks++;
      const chunkResults = r.results || [];
      for (const it of chunkResults) {
        if (it && it.ok && it.accepted) accepted++;
        else failed++;
        if (observe && it && it.ok && it.observed) observedCount++;
        if (it && !it.ok) {
          failures.push({
            chunkIndex,
            pixelIndex: start + Math.max(0, chunkResults.indexOf(it)),
            x: it.x,
            y: it.y,
            reason: it.error?.code || it.code || "ERROR",
            message: it.error?.message || it.message || null
          });
        }
      }
    }
    return ok({
      ok: true,
      requested: req,
      chunkSize: cs,
      totalChunks,
      completedChunks,
      accepted,
      observed: observe ? observedCount : null,
      failed,
      stoppedReason: null,
      failures
    });
  }
  async function claim_region({ agent_id, region, ttl_ms = 6e4, reason = "" } = {}) {
    if (!agent_id) return err(ErrorCode.INVALID, "agent_id required");
    if (!region || !Number.isInteger(region.x) || !Number.isInteger(region.y) || !Number.isInteger(region.w) || !Number.isInteger(region.h)) {
      return err(ErrorCode.INVALID, "region must be {x,y,w,h} ints");
    }
    return coord.claim_region({ agent_id, region, ttl_ms, reason });
  }
  async function release_region({ agent_id, claim_id } = {}) {
    if (!agent_id || !claim_id) return err(ErrorCode.INVALID, "agent_id and claim_id required");
    return coord.release_region({ agent_id, claim_id });
  }
  async function list_active_claims() {
    return coord.list_active_claims();
  }
  async function register_agent({ agent_id, display_name = "", version = "" } = {}) {
    if (!agent_id) return err(ErrorCode.INVALID, "agent_id required");
    return coord.register_agent({ agent_id, display_name, version });
  }
  async function heartbeat({ agent_id } = {}) {
    if (!agent_id) return err(ErrorCode.INVALID, "agent_id required");
    return coord.heartbeat({ agent_id });
  }
  async function get_debug_truth_trace() {
    try {
      await chat.connect();
    } catch {
    }
    const latestChatTs = Math.max(...(chat.recent || []).filter((m) => (m?.type || "chat") === "chat").map((m) => m.ts || 0), 0) || null;
    const latestIntentTs = Math.max(...(chat.recent || []).filter((m) => (m?.type || "chat") === "intent").map((m) => m.ts || 0), 0) || null;
    return ok({
      clientId: chat.clientId || null,
      sharedKey: chat._sharedKey || null,
      wasReused: chat._wasReused ?? null,
      readyState: chat.ws ? chat.ws.readyState : null,
      connected: !!chat.connected,
      lastAnyFrameAt: chat.lastAnyFrameAt || null,
      lastHistoryAt: chat.lastHistoryAt || null,
      lastMessageAt: chat.lastMessageAt || null,
      recentLen: Array.isArray(chat.recent) ? chat.recent.length : null,
      latestChatTs,
      latestIntentTs,
      writeTrace: Array.isArray(chat._writeTrace) ? chat._writeTrace.slice(-10) : [],
      readTrace: Array.isArray(chat._readTrace) ? chat._readTrace.slice(-10) : [],
      recvTrace: Array.isArray(chat._recvTrace) ? chat._recvTrace.slice(-10) : []
    });
  }
  return {
    // Phase 1 APIs
    get_recent_messages,
    get_recent_intents,
    send_chat,
    send_intent,
    get_board_snapshot,
    get_region,
    // Phase 2 APIs
    draw_pixel,
    draw_pixels,
    draw_pixels_chunked: draw_pixels_chunked2,
    // TEMP TRACE
    get_debug_truth_trace,
    // Phase 3 APIs
    claim_region,
    release_region,
    list_active_claims,
    register_agent,
    heartbeat,
    // lifecycle
    close: () => {
      chat.close();
      board.close();
    }
  };
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  createAgentDerbySkill,
  phase3,
  phase4,
  phase5,
  phase5plan,
  phase5refine,
  phase6,
  phase6_1,
  phase7,
  region_scan,
  stage1
});
//# sourceMappingURL=index.cjs.map
