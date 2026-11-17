#!/usr/bin/env node
"use strict";
var __getOwnPropNames = Object.getOwnPropertyNames;
var __commonJS = (cb, mod) => function __require() {
  try {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  } catch (e) {
    throw mod = 0, e;
  }
};

// dist/types.js
var require_types = __commonJS({
  "dist/types.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.SUPPORTED_IMAGE_EXTENSIONS = exports2.SUPPORTED_VIDEO_EXTENSIONS = exports2.CREDENTIAL_APPLY_URL = exports2.CREDENTIAL_APPLY_URL_EN = exports2.CREDENTIAL_APPLY_URL_ZH = exports2.BASE_URL = exports2.RATE_ABOVE_720P = exports2.RATE_720P_OR_BELOW = exports2.RESOLUTION_720P_THRESHOLD = exports2.MAX_CONSECUTIVE_FAILURES = exports2.MAX_POLL_COUNT = exports2.POLL_INTERVAL = exports2.MAX_IMAGE_FILE_SIZE = exports2.MAX_CREDENTIAL_LENGTH = exports2.MAX_TASK_ID_LENGTH = exports2.MAX_DIMENSION = exports2.MAX_DURATION = exports2.MAX_URL_LENGTH = exports2.MAX_FILE_SIZE = exports2.TIMEOUT_CONFIG = exports2.ErrorCode = void 0;
    var ErrorCode;
    (function(ErrorCode2) {
      ErrorCode2[ErrorCode2["SUCCESS"] = 200] = "SUCCESS";
      ErrorCode2[ErrorCode2["AUTH_FAILED"] = -100] = "AUTH_FAILED";
      ErrorCode2[ErrorCode2["INVALID_PARAMS"] = -200] = "INVALID_PARAMS";
      ErrorCode2[ErrorCode2["BUSINESS_REJECTED"] = -300] = "BUSINESS_REJECTED";
      ErrorCode2[ErrorCode2["ACCOUNT_TEMPORARILY_BLOCKED"] = -401] = "ACCOUNT_TEMPORARILY_BLOCKED";
      ErrorCode2[ErrorCode2["ACCOUNT_PERMANENTLY_BLOCKED"] = -402] = "ACCOUNT_PERMANENTLY_BLOCKED";
      ErrorCode2[ErrorCode2["SERVER_ERROR"] = -500] = "SERVER_ERROR";
      ErrorCode2[ErrorCode2["UNSUPPORTED_VIDEO"] = -600] = "UNSUPPORTED_VIDEO";
    })(ErrorCode || (exports2.ErrorCode = ErrorCode = {}));
    exports2.TIMEOUT_CONFIG = {
      upload: 18e4,
      submit: 15e4,
      query: 1e4,
      videoWatermark: 45e3,
      imageWatermark: 18e4
    };
    exports2.MAX_FILE_SIZE = 1073741824;
    exports2.MAX_URL_LENGTH = 2048;
    exports2.MAX_DURATION = 600;
    exports2.MAX_DIMENSION = 1e4;
    exports2.MAX_TASK_ID_LENGTH = 64;
    exports2.MAX_CREDENTIAL_LENGTH = 128;
    exports2.MAX_IMAGE_FILE_SIZE = 52428800;
    exports2.POLL_INTERVAL = 3e4;
    exports2.MAX_POLL_COUNT = 20;
    exports2.MAX_CONSECUTIVE_FAILURES = 3;
    exports2.RESOLUTION_720P_THRESHOLD = 921600;
    exports2.RATE_720P_OR_BELOW = 1.3;
    exports2.RATE_ABOVE_720P = 1.6;
    exports2.BASE_URL = "https://www.550wai.cn";
    exports2.CREDENTIAL_APPLY_URL_ZH = "https://qzm.550wai.cn/api-keys";
    exports2.CREDENTIAL_APPLY_URL_EN = "https://eraser.550wai.com/api/";
    exports2.CREDENTIAL_APPLY_URL = exports2.CREDENTIAL_APPLY_URL_ZH;
    exports2.SUPPORTED_VIDEO_EXTENSIONS = [".mp4", ".mov"];
    exports2.SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".avif", ".tif", ".tiff", ".svg"];
  }
});

// dist/i18n.js
var require_i18n = __commonJS({
  "dist/i18n.js"(exports2) {
    "use strict";
    var __createBinding = exports2 && exports2.__createBinding || (Object.create ? (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      var desc = Object.getOwnPropertyDescriptor(m, k);
      if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
        desc = { enumerable: true, get: function() {
          return m[k];
        } };
      }
      Object.defineProperty(o, k2, desc);
    }) : (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    }));
    var __setModuleDefault = exports2 && exports2.__setModuleDefault || (Object.create ? (function(o, v) {
      Object.defineProperty(o, "default", { enumerable: true, value: v });
    }) : function(o, v) {
      o["default"] = v;
    });
    var __importStar = exports2 && exports2.__importStar || /* @__PURE__ */ (function() {
      var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function(o2) {
          var ar = [];
          for (var k in o2) if (Object.prototype.hasOwnProperty.call(o2, k)) ar[ar.length] = k;
          return ar;
        };
        return ownKeys(o);
      };
      return function(mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) {
          for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        }
        __setModuleDefault(result, mod);
        return result;
      };
    })();
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.resolveLocale = resolveLocale;
    exports2.localize = localize;
    exports2.resolveGlobalApiLocale = resolveGlobalApiLocale;
    exports2.resolveServiceRegion = resolveServiceRegion;
    exports2.credentialApplyUrl = credentialApplyUrl;
    exports2.globalPolicyUrl = globalPolicyUrl;
    var fs = __importStar(require("fs"));
    var path = __importStar(require("path"));
    var distribution;
    function packagedDistribution() {
      if (distribution !== void 0)
        return distribution;
      try {
        const value = JSON.parse(fs.readFileSync(path.resolve(__dirname, "../distribution.json"), "utf8"));
        distribution = (value.region === "domestic" || value.region === "global") && typeof value.locale === "string" ? { region: value.region, locale: value.locale } : null;
      } catch {
        distribution = null;
      }
      return distribution;
    }
    var GLOBAL_API_LOCALES = /* @__PURE__ */ new Set([
      "zh-Hans",
      "zh-Hant",
      "ja",
      "ko",
      "es",
      "es-MX",
      "fr",
      "fr-CA",
      "de",
      "pt-BR",
      "pt-PT",
      "it",
      "ru",
      "ar",
      "he",
      "id",
      "ms",
      "nl",
      "pl",
      "th",
      "tr",
      "uk",
      "vi",
      "hi"
    ]);
    var GLOBAL_LOCALE_ALIASES = {
      "es-419": "es-MX",
      pt: "pt-BR"
    };
    function resolveLocale(value) {
      const packaged = packagedDistribution();
      if (packaged?.region === "domestic")
        return "zh";
      const language = String(value || packaged?.locale || process.env.LC_ALL || process.env.LC_MESSAGES || process.env.LANG || "").toLowerCase();
      return language.startsWith("zh") || language.includes("zh_") || language.includes("zh-") ? "zh" : "en";
    }
    function localize(locale, zh, en) {
      return resolveLocale(locale) === "zh" ? zh : en;
    }
    function resolveGlobalApiLocale(value) {
      const raw = String(value || "").trim().replace(/_/g, "-").replace(/\..*$/, "");
      if (!raw)
        return "en";
      const normalized = raw.toLowerCase();
      if (["zh", "zh-cn", "zh-sg", "zh-hans"].includes(normalized))
        return "zh-Hans";
      if (["zh-tw", "zh-hk", "zh-mo", "zh-hant"].includes(normalized))
        return "zh-Hant";
      const exact = [...GLOBAL_API_LOCALES].find((item) => item.toLowerCase() === raw.toLowerCase());
      if (exact)
        return exact;
      const alias = Object.entries(GLOBAL_LOCALE_ALIASES).find(([key]) => key.toLowerCase() === raw.toLowerCase())?.[1];
      if (alias)
        return alias;
      const primary = raw.split("-")[0].toLowerCase();
      return [...GLOBAL_API_LOCALES].find((item) => item.toLowerCase() === primary) || "en";
    }
    function resolveServiceRegion(value, locale) {
      const packaged = packagedDistribution();
      if (packaged)
        return packaged.region;
      const configured = String(value || process.env.SUBTITLE_REMOVER_REGION || "").trim().toLowerCase();
      if (configured === "domestic" || configured === "cn" || configured === "china")
        return "domestic";
      if (configured === "global" || configured === "overseas" || configured === "international")
        return "global";
      return resolveLocale(locale) === "zh" ? "domestic" : "global";
    }
    function credentialApplyUrl(locale, region) {
      if (resolveServiceRegion(region, locale) === "domestic")
        return "https://qzm.550wai.cn/api-keys";
      const globalLocale = resolveGlobalApiLocale(locale);
      return globalLocale === "en" ? "https://eraser.550wai.com/api/" : `https://eraser.550wai.com/${globalLocale}/api/`;
    }
    function globalPolicyUrl(page, locale) {
      const globalLocale = resolveGlobalApiLocale(locale);
      return globalLocale === "en" ? `https://eraser.550wai.com/${page}/` : `https://eraser.550wai.com/${globalLocale}/${page}/`;
    }
  }
});

// dist/credential-manager.js
var require_credential_manager = __commonJS({
  "dist/credential-manager.js"(exports2) {
    "use strict";
    var __createBinding = exports2 && exports2.__createBinding || (Object.create ? (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      var desc = Object.getOwnPropertyDescriptor(m, k);
      if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
        desc = { enumerable: true, get: function() {
          return m[k];
        } };
      }
      Object.defineProperty(o, k2, desc);
    }) : (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    }));
    var __setModuleDefault = exports2 && exports2.__setModuleDefault || (Object.create ? (function(o, v) {
      Object.defineProperty(o, "default", { enumerable: true, value: v });
    }) : function(o, v) {
      o["default"] = v;
    });
    var __importStar = exports2 && exports2.__importStar || /* @__PURE__ */ (function() {
      var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function(o2) {
          var ar = [];
          for (var k in o2) if (Object.prototype.hasOwnProperty.call(o2, k)) ar[ar.length] = k;
          return ar;
        };
        return ownKeys(o);
      };
      return function(mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) {
          for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        }
        __setModuleDefault(result, mod);
        return result;
      };
    })();
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.CredentialManager = void 0;
    var fs = __importStar(require("fs"));
    var path = __importStar(require("path"));
    var os = __importStar(require("os"));
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    var CredentialManager = class {
      constructor(storagePath) {
        const configRoot = process.env.XDG_CONFIG_HOME?.trim() || (process.platform === "win32" ? process.env.APPDATA?.trim() : null) || path.join(os.homedir(), ".config");
        this.storagePath = storagePath ?? path.join(configRoot, "550w-ai", "credentials.json");
        this.legacyStoragePath = path.resolve(__dirname, "../.credentials.json");
      }
      get() {
        const envUserNo = process.env.SUBTITLE_REMOVER_USER_NO?.trim();
        const envApiKey = process.env.SUBTITLE_REMOVER_API_KEY?.trim();
        if (envUserNo && envApiKey && envUserNo.length >= 1 && envUserNo.length <= types_1.MAX_CREDENTIAL_LENGTH && envApiKey.length >= 1 && envApiKey.length <= types_1.MAX_CREDENTIAL_LENGTH) {
          return { userNo: envUserNo, apiKey: envApiKey };
        }
        return this.readFile(this.storagePath) ?? (this.storagePath !== this.legacyStoragePath ? this.readFile(this.legacyStoragePath) : null);
      }
      readFile(target) {
        try {
          const content = fs.readFileSync(target, "utf-8");
          const data = JSON.parse(content);
          if (typeof data.userNo === "string" && typeof data.apiKey === "string" && data.userNo.trim().length >= 1 && data.userNo.trim().length <= types_1.MAX_CREDENTIAL_LENGTH && data.apiKey.trim().length >= 1 && data.apiKey.trim().length <= types_1.MAX_CREDENTIAL_LENGTH) {
            return { userNo: data.userNo.trim(), apiKey: data.apiKey.trim() };
          }
          return null;
        } catch {
          return null;
        }
      }
      set(credential) {
        const userNo = credential.userNo?.trim() ?? "";
        const apiKey = credential.apiKey?.trim() ?? "";
        if (userNo.length < 1 || userNo.length > types_1.MAX_CREDENTIAL_LENGTH) {
          throw new Error(`userNo \u957F\u5EA6\u5FC5\u987B\u5728 1-${types_1.MAX_CREDENTIAL_LENGTH} \u4E4B\u95F4\uFF0C\u5F53\u524D\u957F\u5EA6: ${userNo.length}`);
        }
        if (apiKey.length < 1 || apiKey.length > types_1.MAX_CREDENTIAL_LENGTH) {
          throw new Error(`apiKey \u957F\u5EA6\u5FC5\u987B\u5728 1-${types_1.MAX_CREDENTIAL_LENGTH} \u4E4B\u95F4\uFF0C\u5F53\u524D\u957F\u5EA6: ${apiKey.length}`);
        }
        const stored = { userNo, apiKey, updatedAt: Date.now() };
        fs.mkdirSync(path.dirname(this.storagePath), { recursive: true });
        fs.writeFileSync(this.storagePath, JSON.stringify(stored, null, 2), { encoding: "utf-8", mode: 384 });
        fs.chmodSync(this.storagePath, 384);
      }
      isConfigured() {
        return this.get() !== null;
      }
      getGuideMessage(locale, region) {
        const applyUrl = (0, i18n_12.credentialApplyUrl)(locale, region);
        return {
          code: types_1.ErrorCode.AUTH_FAILED,
          message: (0, i18n_12.localize)(locale, `\u5C1A\u672A\u914D\u7F6E\u51ED\u8BC1\u3002\u8BF7\u524D\u5F80 ${applyUrl} \u83B7\u53D6\u7528\u6237 ID \u548C API Key\uFF0C\u7136\u540E\u5728\u8FDE\u63A5\u5668\u8BBE\u7F6E\u4E2D\u5B8C\u6210\u914D\u7F6E\u3002`, `Credentials are not configured. Get your user ID and API key at ${applyUrl}, then add them in the connector settings.`),
          credentialSetup: {
            required: ["userNo", "apiKey"],
            url: applyUrl,
            urls: { zh: applyUrl, en: applyUrl },
            ...(0, i18n_12.resolveServiceRegion)(region, locale) === "global" && {
              privacyUrl: (0, i18n_12.globalPolicyUrl)("privacy", locale),
              termsUrl: (0, i18n_12.globalPolicyUrl)("terms", locale)
            }
          }
        };
      }
    };
    exports2.CredentialManager = CredentialManager;
  }
});

// dist/api-client.js
var require_api_client = __commonJS({
  "dist/api-client.js"(exports2) {
    "use strict";
    var __importDefault = exports2 && exports2.__importDefault || function(mod) {
      return mod && mod.__esModule ? mod : { "default": mod };
    };
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.TIMEOUT_CONFIG = exports2.ApiClient = void 0;
    var node_https_1 = __importDefault(require("node:https"));
    var node_crypto_1 = require("node:crypto");
    var node_stream_1 = require("node:stream");
    var types_1 = require_types();
    Object.defineProperty(exports2, "TIMEOUT_CONFIG", { enumerable: true, get: function() {
      return types_1.TIMEOUT_CONFIG;
    } });
    var i18n_12 = require_i18n();
    var ApiClient = class {
      constructor(credential, locale) {
        this.credential = credential;
        this.baseUrl = types_1.BASE_URL;
        this.locale = locale;
      }
      async post(endpoint, params, timeout) {
        try {
          const body = new URLSearchParams({
            userNo: this.credential.userNo,
            apiKey: this.credential.apiKey,
            ...params
          });
          return this.parseResponse(await this.request(endpoint, body.toString(), {
            "Content-Type": "application/x-www-form-urlencoded"
          }, timeout));
        } catch (error) {
          return this.handleError(error);
        }
      }
      async upload(endpoint, params, file, timeout, fieldName = "file") {
        try {
          const boundary = `550w-${(0, node_crypto_1.randomBytes)(16).toString("hex")}`;
          const fields = { userNo: this.credential.userNo, apiKey: this.credential.apiKey, ...params };
          const part = (name, value) => `--${boundary}\r
Content-Disposition: form-data; name="${this.safeHeader(name)}"\r
\r
${value}\r
`;
          const chunks = Object.entries(fields).map(([name, value]) => part(name, value));
          chunks.push(`--${boundary}\r
Content-Disposition: form-data; name="${this.safeHeader(fieldName)}"; filename="${this.safeHeader(file.name)}"\r
Content-Type: application/octet-stream\r
\r
`);
          const body = node_stream_1.Readable.from((async function* () {
            for (const chunk of chunks)
              yield chunk;
            if (Buffer.isBuffer(file.data))
              yield file.data;
            else
              for await (const chunk of file.data)
                yield chunk;
            yield `\r
--${boundary}--\r
`;
          })());
          return this.parseResponse(await this.request(endpoint, body, {
            "Content-Type": `multipart/form-data; boundary=${boundary}`
          }, timeout));
        } catch (error) {
          return this.handleError(error);
        }
      }
      safeHeader(value) {
        return value.replace(/[\r\n"\\]/g, "_");
      }
      request(endpoint, body, headers, timeout) {
        return new Promise((resolve, reject) => {
          const url = new URL(endpoint, this.baseUrl);
          if (url.origin !== new URL(this.baseUrl).origin) {
            reject(new Error("Invalid API endpoint"));
            return;
          }
          const request = node_https_1.default.request(url, { method: "POST", headers }, (response) => {
            const chunks = [];
            let size = 0;
            response.on("data", (chunk) => {
              size += chunk.length;
              if (size > 2 * 1024 * 1024) {
                request.destroy(new Error("API response too large"));
                return;
              }
              chunks.push(chunk);
            });
            response.on("end", () => {
              clearTimeout(timer);
              if ((response.statusCode ?? 0) >= 300 && (response.statusCode ?? 0) < 400) {
                reject(new Error("API redirects are not allowed"));
                return;
              }
              try {
                resolve(JSON.parse(Buffer.concat(chunks).toString("utf8")));
              } catch (error) {
                reject(error);
              }
            });
            response.on("error", reject);
          });
          const timer = setTimeout(() => {
            const error = Object.assign(new Error("Request timed out"), { code: "ETIMEDOUT" });
            request.destroy(error);
          }, timeout);
          request.on("error", (error) => {
            clearTimeout(timer);
            if (body instanceof node_stream_1.Readable)
              body.destroy();
            reject(error);
          });
          if (body instanceof node_stream_1.Readable) {
            body.on("error", (error) => request.destroy(error));
            body.pipe(request);
          } else
            request.end(body);
        });
      }
      parseResponse(data) {
        if (data == null || typeof data.code === "undefined") {
          return { code: -500, message: (0, i18n_12.localize)(this.locale, "\u54CD\u5E94\u683C\u5F0F\u5F02\u5E38", "The service returned an invalid response") };
        }
        return data;
      }
      handleError(error) {
        const responseData = error?.response?.data;
        if (responseData != null && typeof responseData.code !== "undefined") {
          return this.parseResponse(responseData);
        }
        if (error?.code === "ECONNABORTED" || error?.code === "ETIMEDOUT") {
          return { code: -500, message: (0, i18n_12.localize)(this.locale, "\u8BF7\u6C42\u8D85\u65F6\uFF0C\u8BF7\u68C0\u67E5\u7F51\u7EDC\u8FDE\u63A5\u540E\u91CD\u8BD5", "The request timed out; check your connection and try again") };
        }
        return { code: -500, message: (0, i18n_12.localize)(this.locale, "\u7F51\u7EDC\u8BF7\u6C42\u5931\u8D25\uFF0C\u8BF7\u68C0\u67E5\u7F51\u7EDC\u8FDE\u63A5\u540E\u91CD\u8BD5", "Network request failed; check your connection and try again") };
      }
    };
    exports2.ApiClient = ApiClient;
  }
});

// dist/validator.js
var require_validator = __commonJS({
  "dist/validator.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.validateCredential = validateCredential;
    exports2.normalizePageParams = normalizePageParams;
    exports2.estimateCredits = estimateCredits;
    exports2.validate = validate;
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    function validationError(locale, zh, en) {
      return { code: types_1.ErrorCode.INVALID_PARAMS, message: (0, i18n_12.localize)(locale, zh, en) };
    }
    function getFileExtension(filename) {
      const lastDot = filename.lastIndexOf(".");
      if (lastDot === -1)
        return "";
      return filename.slice(lastDot).toLowerCase();
    }
    function validateCredential(userNo, apiKey, locale) {
      if (typeof userNo !== "string" || userNo.trim().length === 0) {
        return validationError(locale, "userNo \u4E0D\u80FD\u4E3A\u7A7A", "userNo is required");
      }
      if (userNo.trim().length > types_1.MAX_CREDENTIAL_LENGTH) {
        return validationError(locale, `userNo \u957F\u5EA6\u4E0D\u80FD\u8D85\u8FC7 ${types_1.MAX_CREDENTIAL_LENGTH} \u4E2A\u5B57\u7B26`, `userNo must not exceed ${types_1.MAX_CREDENTIAL_LENGTH} characters`);
      }
      if (typeof apiKey !== "string" || apiKey.trim().length === 0) {
        return validationError(locale, "apiKey \u4E0D\u80FD\u4E3A\u7A7A", "apiKey is required");
      }
      if (apiKey.trim().length > types_1.MAX_CREDENTIAL_LENGTH) {
        return validationError(locale, `apiKey \u957F\u5EA6\u4E0D\u80FD\u8D85\u8FC7 ${types_1.MAX_CREDENTIAL_LENGTH} \u4E2A\u5B57\u7B26`, `apiKey must not exceed ${types_1.MAX_CREDENTIAL_LENGTH} characters`);
      }
      return null;
    }
    function validateFile(file, locale) {
      if (!file)
        return validationError(locale, "\u6587\u4EF6\u4E0D\u80FD\u4E3A\u7A7A", "A video file is required");
      if (typeof file.name !== "string" || file.name.trim().length === 0)
        return validationError(locale, "\u6587\u4EF6\u540D\u4E0D\u80FD\u4E3A\u7A7A", "The video filename is required");
      const size = Number(file.size ?? file.data?.length);
      if (Number.isFinite(size) && size > types_1.MAX_FILE_SIZE) {
        return validationError(locale, `\u6587\u4EF6\u5927\u5C0F\u8D85\u9650\uFF0C\u6700\u5927\u652F\u6301 1GB\uFF0C\u5F53\u524D\u6587\u4EF6\u5927\u5C0F\u4E3A ${size} \u5B57\u8282`, `The video exceeds the 1 GB limit (${size} bytes)`);
      }
      const ext = getFileExtension(file.name);
      if (!types_1.SUPPORTED_VIDEO_EXTENSIONS.includes(ext)) {
        return validationError(locale, `\u4E0D\u652F\u6301\u7684\u89C6\u9891\u683C\u5F0F "${ext}"\uFF0C\u4EC5\u652F\u6301 mp4\u3001mov \u683C\u5F0F`, `Unsupported video format "${ext}"; use MP4 or MOV`);
      }
      return null;
    }
    function validateImageFile(file, locale) {
      if (!file)
        return validationError(locale, "\u56FE\u7247\u6587\u4EF6\u4E0D\u80FD\u4E3A\u7A7A", "An image file is required");
      if (typeof file.name !== "string" || file.name.trim().length === 0)
        return validationError(locale, "\u56FE\u7247\u6587\u4EF6\u540D\u4E0D\u80FD\u4E3A\u7A7A", "The image filename is required");
      const size = Number(file.size ?? file.data?.length);
      if (Number.isFinite(size) && size > types_1.MAX_IMAGE_FILE_SIZE)
        return validationError(locale, "\u56FE\u7247\u5927\u5C0F\u4E0D\u80FD\u8D85\u8FC7 50MB", "The image must not exceed 50 MB");
      const ext = getFileExtension(file.name);
      if (!types_1.SUPPORTED_IMAGE_EXTENSIONS.includes(ext)) {
        return validationError(locale, `\u4E0D\u652F\u6301\u7684\u56FE\u7247\u683C\u5F0F "${ext}"\uFF0C\u652F\u6301 JPG\u3001PNG\u3001BMP\u3001WebP\u3001AVIF\u3001TIFF\u3001SVG`, `Unsupported image format "${ext}"; use JPG, PNG, BMP, WebP, AVIF, TIFF, or SVG`);
      }
      return null;
    }
    function validateUrl(url, locale) {
      if (typeof url !== "string" || url.trim().length === 0)
        return validationError(locale, "videoUrl \u4E0D\u80FD\u4E3A\u7A7A", "videoUrl is required");
      url = url.trim();
      if (!url.startsWith("http://") && !url.startsWith("https://")) {
        return validationError(locale, "videoUrl \u5FC5\u987B\u4EE5 http:// \u6216 https:// \u5F00\u5934", "videoUrl must start with http:// or https://");
      }
      if (url.length > types_1.MAX_URL_LENGTH) {
        return validationError(locale, `videoUrl \u957F\u5EA6\u4E0D\u80FD\u8D85\u8FC7 ${types_1.MAX_URL_LENGTH} \u4E2A\u5B57\u7B26`, `videoUrl must not exceed ${types_1.MAX_URL_LENGTH} characters`);
      }
      return null;
    }
    function validateResolution(width, height, locale) {
      if (Math.max(width, height) > 1920 || Math.min(width, height) > 1080) {
        return validationError(locale, `\u89C6\u9891\u5206\u8FA8\u7387\u8D85\u9650\uFF0C\u8981\u6C42\u6700\u5927\u8FB9\u4E0D\u8D85\u8FC7 1920 \u4E14\u6700\u5C0F\u8FB9\u4E0D\u8D85\u8FC7 1080\uFF08\u5F53\u524D ${width}\xD7${height}\uFF09`, `Video resolution exceeds the limit: longest side 1920 and shortest side 1080 (received ${width}\xD7${height})`);
      }
      return null;
    }
    function validateDuration(duration, locale) {
      if (duration == null || typeof duration !== "number" || !Number.isFinite(duration)) {
        return validationError(locale, "duration \u5FC5\u987B\u4E3A\u6709\u6548\u6570\u5B57", "duration must be a valid number");
      }
      if (duration < 1 || duration > types_1.MAX_DURATION) {
        return validationError(locale, `\u89C6\u9891\u65F6\u957F\u8D85\u9650\uFF0C\u6709\u6548\u8303\u56F4\u4E3A 1~${types_1.MAX_DURATION} \u79D2\uFF08\u5F53\u524D ${duration} \u79D2\uFF09`, `Video duration must be between 1 and ${types_1.MAX_DURATION} seconds (received ${duration})`);
      }
      return null;
    }
    function validateDimension(value, fieldName, locale) {
      if (value == null || typeof value !== "number" || !Number.isFinite(value)) {
        return validationError(locale, `${fieldName} \u5FC5\u987B\u4E3A\u6709\u6548\u6570\u5B57`, `${fieldName} must be a valid number`);
      }
      if (!Number.isInteger(value))
        return validationError(locale, `${fieldName} \u5FC5\u987B\u4E3A\u6574\u6570`, `${fieldName} must be an integer`);
      if (value < 1 || value > types_1.MAX_DIMENSION) {
        return validationError(locale, `${fieldName} \u8D85\u51FA\u6709\u6548\u8303\u56F4\uFF0C\u6709\u6548\u8303\u56F4\u4E3A 1~${types_1.MAX_DIMENSION}\uFF08\u5F53\u524D ${value}\uFF09`, `${fieldName} must be between 1 and ${types_1.MAX_DIMENSION} (received ${value})`);
      }
      return null;
    }
    function validateTaskId(taskId, locale) {
      if (typeof taskId !== "string" || taskId.trim().length === 0) {
        return validationError(locale, "taskId \u4E0D\u80FD\u4E3A\u7A7A", "taskId is required");
      }
      if (taskId.trim().length > types_1.MAX_TASK_ID_LENGTH) {
        return validationError(locale, `taskId \u957F\u5EA6\u4E0D\u80FD\u8D85\u8FC7 ${types_1.MAX_TASK_ID_LENGTH} \u4E2A\u5B57\u7B26`, `taskId must not exceed ${types_1.MAX_TASK_ID_LENGTH} characters`);
      }
      return null;
    }
    function validateOperationId(operationId, locale) {
      if (operationId == null || operationId === "")
        return null;
      if (typeof operationId !== "string" || !/^[A-Za-z0-9._:-]{8,64}$/.test(operationId.trim())) {
        return validationError(locale, "operationId \u5FC5\u987B\u4E3A 8\u201364 \u4F4D\uFF0C\u4E14\u53EA\u80FD\u5305\u542B\u5B57\u6BCD\u3001\u6570\u5B57\u3001\u70B9\u3001\u4E0B\u5212\u7EBF\u3001\u5192\u53F7\u548C\u8FDE\u5B57\u7B26", "operationId must be 8\u201364 characters using only letters, numbers, periods, underscores, colons, and hyphens");
      }
      return null;
    }
    function validateIdempotencyKey(value, locale) {
      if (value == null || value === "")
        return null;
      if (typeof value !== "string" || !/^[A-Za-z0-9._:-]{8,128}$/.test(value.trim())) {
        return validationError(locale, "idempotencyKey \u5FC5\u987B\u4E3A 8\u2013128 \u4F4D\uFF0C\u4E14\u53EA\u80FD\u5305\u542B\u5B57\u6BCD\u3001\u6570\u5B57\u3001\u70B9\u3001\u4E0B\u5212\u7EBF\u3001\u5192\u53F7\u548C\u8FDE\u5B57\u7B26", "idempotencyKey must be 8\u2013128 characters using only letters, numbers, periods, underscores, colons, and hyphens");
      }
      return null;
    }
    function validateSubUserId(value, locale) {
      if (value == null || value === "")
        return null;
      if (typeof value !== "string" || value.trim().length > 128) {
        return validationError(locale, "subUserId \u957F\u5EA6\u4E0D\u80FD\u8D85\u8FC7 128 \u4E2A\u5B57\u7B26", "subUserId must not exceed 128 characters");
      }
      return null;
    }
    function normalizePageParams(params) {
      const page = params.page != null ? Math.max(0, Math.floor(params.page)) : 0;
      const size = params.size != null ? Math.min(100, Math.max(1, Math.floor(params.size))) : 20;
      return { page, size };
    }
    function estimateCredits(width, height, duration) {
      const pixels = width * height;
      const isAbove720p = pixels > types_1.RESOLUTION_720P_THRESHOLD;
      const rate = isAbove720p ? types_1.RATE_ABOVE_720P : types_1.RATE_720P_OR_BELOW;
      const estimatedCost = Math.ceil(duration * rate);
      return { estimatedCost, resolution: isAbove720p ? "above_720p" : "720p_or_below" };
    }
    function validateUploadVideo(params) {
      return validateFile(params.file, params.locale);
    }
    function validateSubmitTask(params) {
      const urlError = validateUrl(params.videoUrl, params.locale);
      if (urlError)
        return urlError;
      const widthError = validateDimension(params.width, "width", params.locale);
      if (widthError)
        return widthError;
      const heightError = validateDimension(params.height, "height", params.locale);
      if (heightError)
        return heightError;
      const durationError = validateDuration(params.duration, params.locale);
      if (durationError)
        return durationError;
      const resolutionError = validateResolution(params.width, params.height, params.locale);
      if (resolutionError)
        return resolutionError;
      if (params.removeAudio != null && typeof params.removeAudio !== "boolean") {
        return validationError(params.locale, "removeAudio \u5FC5\u987B\u4E3A boolean", "removeAudio must be a boolean");
      }
      return validateIdempotencyKey(params.idempotencyKey, params.locale) || validateSubUserId(params.subUserId, params.locale);
    }
    function validateEstimateCredits(params) {
      const widthError = validateDimension(params.width, "width", params.locale);
      if (widthError)
        return widthError;
      const heightError = validateDimension(params.height, "height", params.locale);
      if (heightError)
        return heightError;
      const durationError = validateDuration(params.duration, params.locale);
      if (durationError)
        return durationError;
      return null;
    }
    function validate(action, params) {
      switch (action) {
        case "uploadVideo":
          return validateUploadVideo(params);
        case "submitTask":
          return validateSubmitTask(params);
        case "taskDetail":
          return validateTaskId(params.taskId, params.locale) || validateSubUserId(params.subUserId, params.locale);
        case "taskList":
          return validateSubUserId(params.subUserId, params.locale);
        case "deleteTask": {
          const taskError = validateTaskId(params.taskId, params.locale);
          if (taskError)
            return taskError;
          return validateSubUserId(params.subUserId, params.locale);
        }
        case "queryCredits":
          return null;
        case "removeVideoWatermark": {
          const urlError = validateUrl(params.videoUrl, params.locale);
          return urlError || validateOperationId(params.operationId, params.locale);
        }
        case "removeImageWatermark": {
          const fileError = validateImageFile(params.file, params.locale);
          if (fileError)
            return fileError;
          if (params.sync != null && typeof params.sync !== "boolean")
            return validationError(params.locale, "sync \u5FC5\u987B\u4E3A boolean", "sync must be a boolean");
          return null;
        }
        case "imageWatermarkTaskDetail":
          return validateTaskId(params.taskId, params.locale);
        case "estimateCredits":
          return validateEstimateCredits(params);
        case "workflow": {
          if (params.file && params.videoUrl)
            return validationError(params.locale, "file \u548C videoUrl \u53EA\u80FD\u63D0\u4F9B\u4E00\u4E2A", "Provide either filePath or videoUrl, not both");
          if (params.file)
            return validateFile(params.file, params.locale);
          if (params.videoUrl) {
            const urlError = validateUrl(params.videoUrl, params.locale);
            if (urlError)
              return urlError;
            if (params.removeAudio != null && typeof params.removeAudio !== "boolean") {
              return validationError(params.locale, "removeAudio \u5FC5\u987B\u4E3A boolean", "removeAudio must be a boolean");
            }
            const suppliedMetadata = [params.width, params.height, params.duration].filter((value) => value != null).length;
            if (suppliedMetadata !== 0 && suppliedMetadata !== 3) {
              return validationError(params.locale, "width\u3001height\u3001duration \u5FC5\u987B\u5168\u90E8\u63D0\u4F9B\u6216\u5168\u90E8\u7701\u7565", "Provide width, height, and duration together, or omit all three");
            }
            if (suppliedMetadata === 3) {
              const metadataError = validateEstimateCredits(params);
              if (metadataError)
                return metadataError;
              const resolutionError = validateResolution(params.width, params.height, params.locale);
              if (resolutionError)
                return resolutionError;
            }
            return validateIdempotencyKey(params.idempotencyKey, params.locale) || validateSubUserId(params.subUserId, params.locale);
          }
          return validationError(params.locale, "\u9700\u8981\u63D0\u4F9B file \u6216 videoUrl \u53C2\u6570", "Provide either filePath or videoUrl");
        }
        default:
          return validationError(params.locale, `\u4E0D\u652F\u6301\u7684 action\uFF1A${action}`, `Unsupported action: ${action}`);
      }
    }
  }
});

// dist/error-handler.js
var require_error_handler = __commonJS({
  "dist/error-handler.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.createErrorResponse = createErrorResponse;
    exports2.mapApiError = mapApiError;
    exports2.createTimeoutErrorResponse = createTimeoutErrorResponse;
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    function createErrorResponse(code, message) {
      return { code, message };
    }
    function mapApiError(apiResponse, locale, region) {
      const { code, message } = apiResponse;
      if (code === types_1.ErrorCode.SUCCESS) {
        return { ...apiResponse };
      }
      switch (code) {
        case types_1.ErrorCode.AUTH_FAILED:
          return createErrorResponse(code, (0, i18n_12.localize)(locale, `\u8BF7\u6C42\u672A\u901A\u8FC7\uFF1A${message}\u3002\u8BF7\u68C0\u67E5\u51ED\u8BC1\u6216\u79EF\u5206\u4F59\u989D\uFF0C\u5E76\u8BBF\u95EE ${(0, i18n_12.credentialApplyUrl)(locale, region)} \u7BA1\u7406\u51ED\u8BC1\u3002`, `Authentication or credit check failed. Check your credentials or balance, and manage your API key at ${(0, i18n_12.credentialApplyUrl)(locale, region)}.`));
        case types_1.ErrorCode.INVALID_PARAMS:
          return createErrorResponse(code, (0, i18n_12.localize)(locale, `\u53C2\u6570\u9519\u8BEF\uFF1A${message}`, `The service rejected one or more request parameters.`));
        case types_1.ErrorCode.BUSINESS_REJECTED:
          if (message.includes("\u79EF\u5206\u4E0D\u8DB3")) {
            return createErrorResponse(code, (0, i18n_12.localize)(locale, `\u4E1A\u52A1\u62D2\u7EDD\uFF1A${message}\u3002\u8BF7\u5145\u503C\u79EF\u5206\u540E\u91CD\u8BD5\u3002`, `Request rejected: insufficient credits. Add credits and try again.`));
          }
          return createErrorResponse(code, (0, i18n_12.localize)(locale, `\u4E1A\u52A1\u62D2\u7EDD\uFF1A${message}`, `The service rejected the request. Check the input and account status before trying again.`));
        case types_1.ErrorCode.ACCOUNT_TEMPORARILY_BLOCKED:
          return createErrorResponse(code, (0, i18n_12.localize)(locale, `\u8D26\u53F7\u6682\u65F6\u53D7\u9650\uFF1A${message}`, "The account is temporarily restricted. Stop submitting requests until the restriction expires."));
        case types_1.ErrorCode.ACCOUNT_PERMANENTLY_BLOCKED:
          return createErrorResponse(code, (0, i18n_12.localize)(locale, `\u8D26\u53F7\u5DF2\u88AB\u6C38\u4E45\u9650\u5236\uFF1A${message}`, "The account is permanently restricted. Stop submitting requests and contact support if you believe this is an error."));
        case types_1.ErrorCode.SERVER_ERROR:
          return createErrorResponse(code, (0, i18n_12.localize)(locale, `\u670D\u52A1\u5F02\u5E38\uFF1A${message}\u3002\u8BF7\u7A0D\u540E\u91CD\u8BD5\u3002`, `The service is temporarily unavailable. Try again later; do not resubmit a billed task if its outcome is uncertain.`));
        case types_1.ErrorCode.UNSUPPORTED_VIDEO:
          return createErrorResponse(code, (0, i18n_12.localize)(locale, "\u89C6\u9891\u683C\u5F0F\u4E0D\u53D7\u652F\u6301\u3002\u8BF7\u91CD\u65B0\u5BFC\u51FA\u4E3A\u517C\u5BB9\u7684 MP4 \u6216 MOV\uFF08\u5EFA\u8BAE 8-bit SDR\uFF09\uFF0C\u7136\u540E\u91CD\u8BD5\u3002", "The video format is unsupported. Export a compatible MP4 or MOV file (8-bit SDR recommended) and try again."));
        default:
          return createErrorResponse(code, (0, i18n_12.localize)(locale, `\u672A\u77E5\u9519\u8BEF\uFF08code=${code}\uFF09\uFF1A${message}\u3002\u8BF7\u8054\u7CFB\u670D\u52A1\u65B9\u3002`, `Unexpected service error (code=${code}). Contact support.`));
      }
    }
    function createTimeoutErrorResponse(timeoutMs, locale) {
      return createErrorResponse(types_1.ErrorCode.SERVER_ERROR, (0, i18n_12.localize)(locale, `\u7F51\u7EDC\u8D85\u65F6\uFF1A\u8BF7\u6C42\u5728 ${timeoutMs / 1e3} \u79D2\u5185\u672A\u6536\u5230\u54CD\u5E94\u3002\u8BF7\u68C0\u67E5\u7F51\u7EDC\u8FDE\u63A5\u540E\u91CD\u8BD5\u3002`, `Network timeout: no response within ${timeoutMs / 1e3} seconds. Check your connection and try again.`));
    }
  }
});

// dist/actions/upload-video.js
var require_upload_video = __commonJS({
  "dist/actions/upload-video.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.uploadVideo = uploadVideo;
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    async function uploadVideo(params, client) {
      const validationError = (0, validator_1.validate)("uploadVideo", params);
      if (validationError)
        return validationError;
      const file = params.file;
      const apiResponse = await client.upload("/open/uploadVideo", {}, { name: file.name, data: file.data ?? file }, types_1.TIMEOUT_CONFIG.upload);
      if (apiResponse.code === types_1.ErrorCode.SUCCESS) {
        return {
          code: types_1.ErrorCode.SUCCESS,
          message: (0, i18n_12.localize)(params.locale, "\u4E0A\u4F20\u6210\u529F", "Upload completed"),
          videoUrl: apiResponse.videoUrl,
          coverUrl: apiResponse.coverUrl,
          width: apiResponse.width,
          height: apiResponse.height,
          duration: apiResponse.duration
        };
      }
      return (0, error_handler_1.mapApiError)(apiResponse, params.locale, params.region);
    }
  }
});

// dist/actions/submit-task.js
var require_submit_task = __commonJS({
  "dist/actions/submit-task.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.submitTask = submitTask;
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    async function submitTask(params, client) {
      const validationError = (0, validator_1.validate)("submitTask", params);
      if (validationError)
        return validationError;
      const requestParams = {
        videoUrl: params.videoUrl,
        width: String(params.width),
        height: String(params.height),
        duration: String(params.duration),
        // Agent 场景固定全屏擦除，不接受或透传用户坐标。
        x1: "0",
        y1: "0",
        x2: "0",
        y2: "0"
      };
      if (params.fileName != null && params.fileName !== "")
        requestParams.fileName = String(params.fileName);
      if (params.coverUrl != null && params.coverUrl !== "")
        requestParams.coverUrl = String(params.coverUrl);
      if (params.callbackUrl != null && params.callbackUrl !== "")
        requestParams.callbackUrl = String(params.callbackUrl);
      if (params.removeAudio != null)
        requestParams.removeAudio = String(params.removeAudio);
      if (params.idempotencyKey != null && String(params.idempotencyKey).trim() !== "")
        requestParams.idempotencyKey = String(params.idempotencyKey).trim();
      if (params.subUserId != null && String(params.subUserId).trim() !== "")
        requestParams.subUserId = String(params.subUserId).trim();
      const apiResponse = await client.post("/open/submitTask", requestParams, types_1.TIMEOUT_CONFIG.submit);
      if (apiResponse.code === types_1.ErrorCode.SUCCESS) {
        return {
          code: types_1.ErrorCode.SUCCESS,
          message: (0, i18n_12.localize)(params.locale, "\u4EFB\u52A1\u63D0\u4EA4\u6210\u529F", "Task submitted"),
          taskId: apiResponse.taskId,
          status: "waiting",
          notice: params.idempotencyKey ? (0, i18n_12.localize)(params.locale, "\u76F8\u540C\u5E42\u7B49\u952E\u548C\u63D0\u4EA4\u53C2\u6570\u53EF\u5B89\u5168\u91CD\u653E\u5E76\u8FD4\u56DE\u539F\u4EFB\u52A1", "The same idempotency key and submission parameters can be replayed safely to return the original task") : (0, i18n_12.localize)(params.locale, "\u6CE8\u610F\uFF1A\u672A\u63D0\u4F9B\u5E42\u7B49\u952E\u65F6\uFF0C\u76F8\u540C videoUrl \u91CD\u590D\u63D0\u4EA4\u4F1A\u88AB\u89C6\u4E3A\u72EC\u7ACB\u4EFB\u52A1\u5E76\u72EC\u7ACB\u8BA1\u8D39", "Without an idempotency key, submitting the same videoUrl again creates a separate task and may be billed separately")
        };
      }
      return (0, error_handler_1.mapApiError)(apiResponse, params.locale, params.region);
    }
  }
});

// dist/actions/task-detail.js
var require_task_detail = __commonJS({
  "dist/actions/task-detail.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.taskDetail = taskDetail;
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    async function taskDetail(params, client) {
      const validationError = (0, validator_1.validate)("taskDetail", params);
      if (validationError)
        return validationError;
      const requestParams = { taskId: params.taskId };
      if (params.subUserId != null && String(params.subUserId).trim() !== "")
        requestParams.subUserId = String(params.subUserId).trim();
      const apiResponse = await client.post("/open/taskDetail", requestParams, types_1.TIMEOUT_CONFIG.query);
      if (apiResponse.code !== types_1.ErrorCode.SUCCESS) {
        return (0, error_handler_1.mapApiError)(apiResponse, params.locale, params.region);
      }
      const { taskId, status, width, height, duration, cost, createTime, updateTime, resultUrl, failReason, failCode, refundStatus } = apiResponse;
      const response = {
        code: types_1.ErrorCode.SUCCESS,
        message: (0, i18n_12.localize)(params.locale, "\u67E5\u8BE2\u6210\u529F", "Task retrieved"),
        taskId,
        status,
        width,
        height,
        duration,
        cost,
        createTime,
        updateTime,
        ...failCode != null && { failCode },
        ...refundStatus != null && { refundStatus }
      };
      switch (status) {
        case "success":
          response.resultUrl = resultUrl;
          break;
        case "failed":
          response.message = (0, i18n_12.localize)(params.locale, `\u4EFB\u52A1\u5904\u7406\u5931\u8D25\uFF1A${failReason || "\u672A\u77E5\u539F\u56E0"}`, "Task processing failed");
          if ((0, i18n_12.resolveLocale)(params.locale) === "zh" && failReason)
            response.failReason = failReason;
          break;
        case "waiting":
        case "processing":
          response.message = (0, i18n_12.localize)(params.locale, `\u4EFB\u52A1${status === "waiting" ? "\u7B49\u5F85\u4E2D" : "\u5904\u7406\u4E2D"}\uFF0C\u5EFA\u8BAE 30 \u79D2\u540E\u518D\u6B21\u67E5\u8BE2`, `Task is ${status}; check again in about 30 seconds`);
          break;
      }
      return response;
    }
  }
});

// dist/actions/task-list.js
var require_task_list = __commonJS({
  "dist/actions/task-list.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.taskList = taskList;
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    async function taskList(params, client) {
      const { page, size } = (0, validator_1.normalizePageParams)(params);
      const requestParams = { page: String(page), size: String(size) };
      if (params.subUserId != null && String(params.subUserId).trim() !== "")
        requestParams.subUserId = String(params.subUserId).trim();
      const apiResponse = await client.post("/open/taskList", requestParams, types_1.TIMEOUT_CONFIG.query);
      if (apiResponse.code !== types_1.ErrorCode.SUCCESS) {
        return (0, error_handler_1.mapApiError)(apiResponse, params.locale, params.region);
      }
      return {
        code: types_1.ErrorCode.SUCCESS,
        message: (0, i18n_12.localize)(params.locale, "\u67E5\u8BE2\u6210\u529F", "Tasks retrieved"),
        total: apiResponse.total,
        page,
        size,
        list: (apiResponse.list || []).map((item) => {
          const publicItem = { ...item };
          delete publicItem.x1;
          delete publicItem.y1;
          delete publicItem.x2;
          delete publicItem.y2;
          delete publicItem.mode;
          if (params.locale && !String(params.locale).toLowerCase().startsWith("zh"))
            delete publicItem.failReason;
          return publicItem;
        })
      };
    }
  }
});

// dist/actions/query-credits.js
var require_query_credits = __commonJS({
  "dist/actions/query-credits.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.queryCredits = queryCredits;
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    async function queryCredits(params, client) {
      const apiResponse = await client.post("/open/queryCredits", {}, types_1.TIMEOUT_CONFIG.query);
      if (apiResponse.code !== types_1.ErrorCode.SUCCESS) {
        return (0, error_handler_1.mapApiError)(apiResponse, params.locale, params.region);
      }
      const result = {
        code: types_1.ErrorCode.SUCCESS,
        message: (0, i18n_12.localize)(params.locale, "\u67E5\u8BE2\u6210\u529F", "Credits retrieved"),
        userNo: apiResponse.userNo,
        credits: apiResponse.credits
      };
      if (params.width !== void 0 || params.height !== void 0 || params.duration !== void 0) {
        const estimateError = (0, validator_1.validate)("estimateCredits", params);
        if (estimateError)
          return estimateError;
        result.estimation = (0, validator_1.estimateCredits)(params.width, params.height, params.duration);
      }
      return result;
    }
  }
});

// dist/video-probe.js
var require_video_probe = __commonJS({
  "dist/video-probe.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.assertPublicVideoUrl = assertPublicVideoUrl;
    exports2.probeVideoUrl = probeVideoUrl;
    var child_process_1 = require("child_process");
    var dns_1 = require("dns");
    var net_1 = require("net");
    function isBlockedAddress(address) {
      const value = address.toLowerCase();
      if (value === "::1" || value === "::" || value.startsWith("fc") || value.startsWith("fd") || value.startsWith("ff") || /^fe[89ab]/.test(value))
        return true;
      const mapped = value.match(/^::ffff:(\d+\.\d+\.\d+\.\d+)$/)?.[1];
      const ipv4 = mapped || ((0, net_1.isIP)(value) === 4 ? value : null);
      if (!ipv4)
        return false;
      const [a, b] = ipv4.split(".").map(Number);
      return a === 0 || a === 10 || a === 127 || a >= 224 || a === 100 && b >= 64 && b <= 127 || a === 169 && b === 254 || a === 172 && b >= 16 && b <= 31 || a === 192 && (b === 0 || b === 168) || a === 198 && (b === 18 || b === 19 || b === 51) || a === 203 && b === 0;
    }
    async function assertPublicVideoUrl(videoUrl) {
      const parsed = new URL(videoUrl);
      if (!["http:", "https:"].includes(parsed.protocol) || parsed.username || parsed.password) {
        throw new Error("Only unauthenticated public HTTP(S) video URLs are allowed");
      }
      const hostname = parsed.hostname.toLowerCase();
      if (hostname === "localhost" || hostname.endsWith(".localhost") || hostname.endsWith(".local") || hostname.endsWith(".internal")) {
        throw new Error("Local and private video URLs are not allowed");
      }
      const addresses = (0, net_1.isIP)(hostname) ? [{ address: hostname }] : await dns_1.promises.lookup(hostname, { all: true, verbatim: true });
      if (addresses.length === 0 || addresses.some(({ address }) => isBlockedAddress(address))) {
        throw new Error("The video URL must resolve only to public network addresses");
      }
    }
    async function probeVideoUrl(videoUrl) {
      await assertPublicVideoUrl(videoUrl);
      const ffprobe = process.env.FFPROBE_PATH?.trim() || "ffprobe";
      const args = [
        "-v",
        "error",
        "-protocol_whitelist",
        "http,https,tcp,tls",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height:format=duration",
        "-of",
        "json",
        videoUrl
      ];
      return new Promise((resolve, reject) => {
        (0, child_process_1.execFile)(ffprobe, args, { timeout: 2e4, maxBuffer: 1024 * 1024 }, (error, stdout) => {
          if (error) {
            reject(new Error(`\u65E0\u6CD5\u9884\u68C0\u8FDC\u7A0B\u89C6\u9891\uFF0C\u8BF7\u786E\u8BA4\u94FE\u63A5\u53EF\u8BBF\u95EE\u4E14\u5DF2\u5B89\u88C5 ffprobe\uFF1A${error.message}`));
            return;
          }
          try {
            const payload = JSON.parse(stdout);
            const stream = payload?.streams?.[0];
            const width = Number(stream?.width);
            const height = Number(stream?.height);
            const duration = Math.ceil(Number(payload?.format?.duration));
            if (!Number.isFinite(width) || !Number.isFinite(height) || !Number.isFinite(duration) || width <= 0 || height <= 0 || duration <= 0) {
              throw new Error("\u672A\u8BFB\u53D6\u5230\u6709\u6548\u7684\u89C6\u9891\u5BBD\u9AD8\u6216\u65F6\u957F");
            }
            resolve({ width, height, duration });
          } catch (parseError) {
            reject(new Error(`\u8FDC\u7A0B\u89C6\u9891\u9884\u68C0\u7ED3\u679C\u65E0\u6548\uFF1A${parseError?.message || "\u672A\u77E5\u9519\u8BEF"}`));
          }
        });
      });
    }
  }
});

// dist/workflow-engine.js
var require_workflow_engine = __commonJS({
  "dist/workflow-engine.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.executeWorkflow = executeWorkflow;
    var upload_video_1 = require_upload_video();
    var submit_task_1 = require_submit_task();
    var task_detail_1 = require_task_detail();
    var video_probe_1 = require_video_probe();
    var types_1 = require_types();
    var validator_1 = require_validator();
    var i18n_12 = require_i18n();
    function delay(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    }
    async function executeWorkflow(params, client) {
      const inputError = (0, validator_1.validate)("workflow", params);
      if (inputError)
        return inputError;
      let submitParams;
      if (params.file) {
        const uploadResult = await (0, upload_video_1.uploadVideo)({ file: params.file, locale: params.locale }, client);
        if (uploadResult.code !== types_1.ErrorCode.SUCCESS)
          return uploadResult;
        submitParams = {
          videoUrl: uploadResult.videoUrl,
          coverUrl: uploadResult.coverUrl,
          width: uploadResult.width,
          height: uploadResult.height,
          duration: uploadResult.duration,
          ...params.fileName != null && { fileName: params.fileName },
          ...params.callbackUrl != null && { callbackUrl: params.callbackUrl },
          ...params.removeAudio != null && { removeAudio: params.removeAudio },
          ...params.idempotencyKey != null && { idempotencyKey: params.idempotencyKey },
          ...params.subUserId != null && { subUserId: params.subUserId },
          locale: params.locale
        };
      } else {
        submitParams = { ...params };
        delete submitParams.file;
        delete submitParams.x1;
        delete submitParams.y1;
        delete submitParams.x2;
        delete submitParams.y2;
        delete submitParams.mode;
        try {
          if (params.width != null && params.height != null && params.duration != null) {
            submitParams.width = params.width;
            submitParams.height = params.height;
            submitParams.duration = params.duration;
          } else {
            const metadata = await (0, video_probe_1.probeVideoUrl)(submitParams.videoUrl);
            submitParams.width = metadata.width;
            submitParams.height = metadata.height;
            submitParams.duration = metadata.duration;
          }
        } catch (error) {
          return { code: types_1.ErrorCode.INVALID_PARAMS, message: (0, i18n_12.localize)(params.locale, "\u65E0\u6CD5\u8BFB\u53D6\u8FDC\u7A0B\u89C6\u9891\u4FE1\u606F\u3002\u8BF7\u786E\u8BA4\u94FE\u63A5\u53EF\u76F4\u63A5\u8BBF\u95EE\u4E14\u89C6\u9891\u683C\u5F0F\u53D7\u652F\u6301\u3002", "Could not inspect the remote video. Make sure the URL is directly accessible and the video format is supported.") };
        }
      }
      const submitResult = await (0, submit_task_1.submitTask)(submitParams, client);
      if (submitResult.code !== types_1.ErrorCode.SUCCESS)
        return submitResult;
      const taskId = submitResult.taskId;
      let consecutiveFailures = 0;
      for (let pollCount = 0; pollCount < types_1.MAX_POLL_COUNT; pollCount++) {
        await delay(types_1.POLL_INTERVAL);
        const detailResult = await (0, task_detail_1.taskDetail)({ taskId, subUserId: params.subUserId, locale: params.locale, region: params.region }, client);
        if (detailResult.code !== types_1.ErrorCode.SUCCESS) {
          consecutiveFailures++;
          if (consecutiveFailures >= types_1.MAX_CONSECUTIVE_FAILURES) {
            return { code: types_1.ErrorCode.SERVER_ERROR, message: (0, i18n_12.localize)(params.locale, `\u8FDE\u7EED ${types_1.MAX_CONSECUTIVE_FAILURES} \u6B21\u67E5\u8BE2\u4EFB\u52A1\u72B6\u6001\u5931\u8D25\u3002\u8BF7\u7A0D\u540E\u4F7F\u7528\u4EFB\u52A1\u7F16\u53F7\u67E5\u8BE2\u6700\u7EC8\u72B6\u6001\u3002`, `Task status checks failed ${types_1.MAX_CONSECUTIVE_FAILURES} times. Use the task ID to check the final status later.`), taskId };
          }
          continue;
        }
        consecutiveFailures = 0;
        const status = detailResult.status;
        if (status === "success") {
          return { code: types_1.ErrorCode.SUCCESS, message: (0, i18n_12.localize)(params.locale, "\u53BB\u5B57\u5E55\u4EFB\u52A1\u5904\u7406\u5B8C\u6210", "Subtitle removal completed"), taskId, resultUrl: detailResult.resultUrl };
        }
        if (status === "failed") {
          return {
            code: types_1.ErrorCode.BUSINESS_REJECTED,
            message: (0, i18n_12.localize)(params.locale, `\u4EFB\u52A1\u5904\u7406\u5931\u8D25\uFF1A${detailResult.failReason || "\u672A\u77E5\u539F\u56E0"}${detailResult.refundStatus === 1 ? "\u3002\u5DF2\u9000\u6B3E" : ""}\u3002`, `Task processing failed${detailResult.refundStatus === 1 ? "; deducted credits were refunded" : ""}.`),
            taskId,
            ...detailResult.failCode != null && { failCode: detailResult.failCode },
            ...detailResult.refundStatus != null && { refundStatus: detailResult.refundStatus },
            ...(0, i18n_12.resolveLocale)(params.locale) === "zh" && detailResult.failReason ? { failReason: detailResult.failReason } : {}
          };
        }
      }
      return { code: types_1.ErrorCode.SERVER_ERROR, message: (0, i18n_12.localize)(params.locale, `\u4EFB\u52A1\u5728 ${types_1.MAX_POLL_COUNT * types_1.POLL_INTERVAL / 1e3 / 60} \u5206\u949F\u5185\u672A\u5B8C\u6210\u3002\u8BF7\u7A0D\u540E\u4F7F\u7528\u4EFB\u52A1\u7F16\u53F7\u67E5\u8BE2\u6700\u7EC8\u72B6\u6001\u3002`, `The task did not finish within ${types_1.MAX_POLL_COUNT * types_1.POLL_INTERVAL / 1e3 / 60} minutes. Use the task ID to check the final status later.`), taskId, timedOut: true };
    }
  }
});

// dist/actions/remove-video-watermark.js
var require_remove_video_watermark = __commonJS({
  "dist/actions/remove-video-watermark.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.removeVideoWatermark = removeVideoWatermark;
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    async function removeVideoWatermark(params, client) {
      const rawInput = typeof params.videoUrl === "string" ? params.videoUrl.trim() : "";
      const extractedUrl = rawInput.match(/https?:\/\/[^\s]+/i)?.[0]?.replace(/[，。；;！!）)】\]]+$/, "") || rawInput;
      const normalizedParams = { ...params, videoUrl: extractedUrl };
      const validationError = (0, validator_1.validate)("removeVideoWatermark", normalizedParams);
      if (validationError)
        return validationError;
      const response = await client.post("/open/removeVideoWatermark", { videoUrl: extractedUrl, ...params.operationId ? { operationId: params.operationId.trim() } : {} }, types_1.TIMEOUT_CONFIG.videoWatermark);
      return response.code === types_1.ErrorCode.SUCCESS ? { ...response, message: (0, i18n_12.localize)(params.locale, "\u89C6\u9891\u53BB\u6C34\u5370\u5B8C\u6210", "Video watermark removal completed") } : (0, error_handler_1.mapApiError)(response, params.locale, params.region);
    }
  }
});

// dist/actions/remove-image-watermark.js
var require_remove_image_watermark = __commonJS({
  "dist/actions/remove-image-watermark.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.removeImageWatermark = removeImageWatermark;
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    async function removeImageWatermark(params, client) {
      const validationError = (0, validator_1.validate)("removeImageWatermark", params);
      if (validationError)
        return validationError;
      const file = params.file;
      const requestParams = {
        sync: String(params.sync ?? true)
      };
      if (params.operationId != null && String(params.operationId).trim() !== "") {
        requestParams.operationId = String(params.operationId).trim();
      }
      const response = await client.upload("/open/removeImageWatermark", requestParams, { name: file.name, data: file.data ?? file }, types_1.TIMEOUT_CONFIG.imageWatermark);
      return response.code === types_1.ErrorCode.SUCCESS ? { ...response, message: (0, i18n_12.localize)(params.locale, response.task?.status === "processing" ? "\u56FE\u7247\u4EFB\u52A1\u5904\u7406\u4E2D" : "\u56FE\u7247\u53BB\u6C34\u5370\u5B8C\u6210", response.task?.status === "processing" ? "Image task is processing" : "Image watermark removal completed") } : (0, error_handler_1.mapApiError)(response, params.locale, params.region);
    }
  }
});

// dist/actions/image-watermark-task-detail.js
var require_image_watermark_task_detail = __commonJS({
  "dist/actions/image-watermark-task-detail.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.imageWatermarkTaskDetail = imageWatermarkTaskDetail;
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    async function imageWatermarkTaskDetail(params, client) {
      const validationError = (0, validator_1.validate)("imageWatermarkTaskDetail", params);
      if (validationError)
        return validationError;
      const response = await client.post("/open/imageWatermarkTaskDetail", { taskId: params.taskId }, types_1.TIMEOUT_CONFIG.query);
      if (response.code !== types_1.ErrorCode.SUCCESS)
        return (0, error_handler_1.mapApiError)(response, params.locale, params.region);
      const localized = { ...response, task: response.task ? { ...response.task } : response.task };
      localized.message = (0, i18n_12.localize)(params.locale, "\u56FE\u7247\u4EFB\u52A1\u67E5\u8BE2\u6210\u529F", "Image task retrieved");
      if ((0, i18n_12.resolveLocale)(params.locale) === "en" && localized.task)
        delete localized.task.failReason;
      return localized;
    }
  }
});

// dist/actions/delete-task.js
var require_delete_task = __commonJS({
  "dist/actions/delete-task.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.deleteTask = deleteTask;
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var types_1 = require_types();
    var i18n_12 = require_i18n();
    async function deleteTask(params, client) {
      const validationError = (0, validator_1.validate)("deleteTask", params);
      if (validationError)
        return validationError;
      const requestParams = { taskId: params.taskId.trim() };
      if (params.subUserId != null && String(params.subUserId).trim() !== "") {
        requestParams.subUserId = String(params.subUserId).trim();
      }
      const response = await client.post("/open/deleteTask", requestParams, types_1.TIMEOUT_CONFIG.query);
      return response.code === types_1.ErrorCode.SUCCESS ? { ...response, message: (0, i18n_12.localize)(params.locale, "\u4EFB\u52A1\u5DF2\u5220\u9664\uFF0C\u76F8\u5173\u5A92\u4F53\u5C06\u5F02\u6B65\u6E05\u7406\uFF1B\u5DF2\u6263\u79EF\u5206\u4E0D\u4F1A\u9000\u8FD8", "Task deleted. Related media will be cleaned up asynchronously; charged credits are not refunded.") } : (0, error_handler_1.mapApiError)(response, params.locale, params.region);
    }
  }
});

// dist/dispatcher.js
var require_dispatcher = __commonJS({
  "dist/dispatcher.js"(exports2) {
    "use strict";
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.invoke = invoke;
    var types_1 = require_types();
    var credential_manager_1 = require_credential_manager();
    var api_client_1 = require_api_client();
    var upload_video_1 = require_upload_video();
    var submit_task_1 = require_submit_task();
    var task_detail_1 = require_task_detail();
    var task_list_1 = require_task_list();
    var query_credits_1 = require_query_credits();
    var workflow_engine_1 = require_workflow_engine();
    var remove_video_watermark_1 = require_remove_video_watermark();
    var remove_image_watermark_1 = require_remove_image_watermark();
    var image_watermark_task_detail_1 = require_image_watermark_task_detail();
    var delete_task_1 = require_delete_task();
    var validator_1 = require_validator();
    var error_handler_1 = require_error_handler();
    var i18n_12 = require_i18n();
    async function invoke(request) {
      const credentialManager = new credential_manager_1.CredentialManager();
      if (request.action === "configureCredentials") {
        const params = request.params || {};
        const validationError = (0, validator_1.validateCredential)(params.userNo, params.apiKey, params.locale);
        if (validationError)
          return validationError;
        try {
          const candidate = { userNo: params.userNo.trim(), apiKey: params.apiKey.trim() };
          const verification = await new api_client_1.ApiClient(candidate, params.locale).post("/open/queryCredits", {}, types_1.TIMEOUT_CONFIG.query);
          if (verification.code !== types_1.ErrorCode.SUCCESS)
            return (0, error_handler_1.mapApiError)(verification, params.locale, params.region);
          credentialManager.set(candidate);
          return { code: types_1.ErrorCode.SUCCESS, message: (0, i18n_12.localize)(params.locale, "\u51ED\u8BC1\u9A8C\u8BC1\u5E76\u914D\u7F6E\u6210\u529F", "Credentials verified and saved"), userNo: verification.userNo };
        } catch {
          return { code: types_1.ErrorCode.SERVER_ERROR, message: (0, i18n_12.localize)(params.locale, "\u51ED\u8BC1\u4FDD\u5B58\u5931\u8D25\uFF0C\u8BF7\u68C0\u67E5\u914D\u7F6E\u76EE\u5F55\u5199\u5165\u6743\u9650", "Could not save credentials; check access to the configuration directory") };
        }
      }
      if (!credentialManager.isConfigured()) {
        return credentialManager.getGuideMessage(request.params?.locale, request.params?.region);
      }
      const validActions = ["uploadVideo", "submitTask", "taskDetail", "taskList", "deleteTask", "queryCredits", "removeVideoWatermark", "removeImageWatermark", "imageWatermarkTaskDetail", "workflow"];
      if (!validActions.includes(request.action)) {
        return { code: types_1.ErrorCode.INVALID_PARAMS, message: (0, i18n_12.localize)(request.params?.locale, `\u4E0D\u652F\u6301\u7684 action\uFF1A${request.action}`, `Unsupported action: ${request.action}`) };
      }
      const credential = credentialManager.get();
      const client = new api_client_1.ApiClient(credential, request.params?.locale);
      switch (request.action) {
        case "uploadVideo":
          return (0, upload_video_1.uploadVideo)(request.params, client);
        case "submitTask":
          return (0, submit_task_1.submitTask)(request.params, client);
        case "taskDetail":
          return (0, task_detail_1.taskDetail)(request.params, client);
        case "taskList":
          return (0, task_list_1.taskList)(request.params, client);
        case "deleteTask":
          return (0, delete_task_1.deleteTask)(request.params, client);
        case "queryCredits":
          return (0, query_credits_1.queryCredits)(request.params, client);
        case "removeVideoWatermark":
          return (0, remove_video_watermark_1.removeVideoWatermark)(request.params, client);
        case "removeImageWatermark":
          return (0, remove_image_watermark_1.removeImageWatermark)(request.params, client);
        case "imageWatermarkTaskDetail":
          return (0, image_watermark_task_detail_1.imageWatermarkTaskDetail)(request.params, client);
        case "workflow":
          return (0, workflow_engine_1.executeWorkflow)(request.params, client);
        default:
          return { code: types_1.ErrorCode.INVALID_PARAMS, message: (0, i18n_12.localize)(request.params?.locale, `\u4E0D\u652F\u6301\u7684 action\uFF1A${request.action}`, `Unsupported action: ${request.action}`) };
      }
    }
  }
});

// dist/local-media.js
var require_local_media = __commonJS({
  "dist/local-media.js"(exports2) {
    "use strict";
    var __createBinding = exports2 && exports2.__createBinding || (Object.create ? (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      var desc = Object.getOwnPropertyDescriptor(m, k);
      if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
        desc = { enumerable: true, get: function() {
          return m[k];
        } };
      }
      Object.defineProperty(o, k2, desc);
    }) : (function(o, m, k, k2) {
      if (k2 === void 0) k2 = k;
      o[k2] = m[k];
    }));
    var __setModuleDefault = exports2 && exports2.__setModuleDefault || (Object.create ? (function(o, v) {
      Object.defineProperty(o, "default", { enumerable: true, value: v });
    }) : function(o, v) {
      o["default"] = v;
    });
    var __importStar = exports2 && exports2.__importStar || /* @__PURE__ */ (function() {
      var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function(o2) {
          var ar = [];
          for (var k in o2) if (Object.prototype.hasOwnProperty.call(o2, k)) ar[ar.length] = k;
          return ar;
        };
        return ownKeys(o);
      };
      return function(mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) {
          for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        }
        __setModuleDefault(result, mod);
        return result;
      };
    })();
    Object.defineProperty(exports2, "__esModule", { value: true });
    exports2.openSelectedLocalMedia = openSelectedLocalMedia;
    var fs = __importStar(require("fs"));
    var path = __importStar(require("path"));
    var types_1 = require_types();
    function openSelectedLocalMedia(filePath, kind) {
      const absolutePath = path.resolve(filePath);
      const stat = fs.lstatSync(absolutePath);
      if (stat.isSymbolicLink() || !stat.isFile()) {
        throw new Error("filePath must point directly to a regular file, not a symbolic link");
      }
      const extension = path.extname(absolutePath).toLowerCase();
      const extensions = kind === "video" ? types_1.SUPPORTED_VIDEO_EXTENSIONS : types_1.SUPPORTED_IMAGE_EXTENSIONS;
      const maxSize = kind === "video" ? types_1.MAX_FILE_SIZE : types_1.MAX_IMAGE_FILE_SIZE;
      if (!extensions.includes(extension))
        throw new Error(`Unsupported ${kind} file extension`);
      if (stat.size > maxSize)
        throw new Error(`${kind} file exceeds the size limit`);
      return {
        name: path.basename(absolutePath),
        size: stat.size,
        data: fs.createReadStream(absolutePath)
      };
    }
  }
});

// dist/cli.js
Object.defineProperty(exports, "__esModule", { value: true });
var dispatcher_1 = require_dispatcher();
var i18n_1 = require_i18n();
var local_media_1 = require_local_media();
async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin)
    chunks.push(Buffer.from(chunk));
  return Buffer.concat(chunks).toString("utf-8");
}
function attachLocalFile(request) {
  const params = { ...request.params || {} };
  const filePath = typeof params.filePath === "string" ? params.filePath : null;
  if (!filePath)
    return { ...request, params };
  const kind = request.action === "removeImageWatermark" ? "image" : "video";
  params.file = (0, local_media_1.openSelectedLocalMedia)(filePath, kind);
  delete params.filePath;
  return { ...request, params };
}
async function main() {
  let locale;
  try {
    const input = (await readStdin()).trim();
    if (!input)
      throw new Error((0, i18n_1.localize)(locale, "\u8BF7\u901A\u8FC7\u6807\u51C6\u8F93\u5165\u63D0\u4F9B JSON \u8BF7\u6C42", "Provide a JSON request on standard input"));
    const parsed = JSON.parse(input);
    locale = parsed.params?.locale;
    const request = attachLocalFile(parsed);
    const result = await (0, dispatcher_1.invoke)(request);
    process.stdout.write(`${JSON.stringify(result)}
`);
    if (result.code !== 200)
      process.exitCode = 1;
  } catch {
    process.stdout.write(`${JSON.stringify({ code: -200, message: (0, i18n_1.localize)(locale, "\u8BF7\u6C42\u65E0\u6548\u6216\u65E0\u6CD5\u8BFB\u53D6\u672C\u5730\u6587\u4EF6", "The request is invalid or the local file could not be read") })}
`);
    process.exitCode = 1;
  }
}
void main();
