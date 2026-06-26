"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AIProductSpaceClient = void 0;
exports.getManifests = getManifests;
exports.handleToolCall = handleToolCall;
const api_client_1 = require("./lib/api-client");
Object.defineProperty(exports, "AIProductSpaceClient", { enumerable: true, get: function () { return api_client_1.AIProductSpaceClient; } });
const createSpace = __importStar(require("./tools/create-space"));
const uploadImage = __importStar(require("./tools/upload-image"));
const runPipeline = __importStar(require("./tools/run-pipeline"));
const generateImage = __importStar(require("./tools/generate-image"));
const generateVideo = __importStar(require("./tools/generate-video"));
const getSpace = __importStar(require("./tools/get-space"));
const listAssets = __importStar(require("./tools/list-assets"));
const tools = [
    createSpace,
    uploadImage,
    runPipeline,
    generateImage,
    generateVideo,
    getSpace,
    listAssets,
];
function getManifests() {
    return tools.map((t) => t.manifest);
}
/**
 * Handle a tool call from OpenClaw.
 *
 * Supports two auth modes:
 * 1. OAuth (preferred): context.auth.accessToken is set automatically after one-click authorization
 * 2. Manual config: context.config.apiKey from config.json (for offline/headless environments)
 */
async function handleToolCall(toolName, params, context) {
    const apiKey = context.auth?.accessToken || context.config?.apiKey;
    const baseUrl = context.config?.baseUrl || process.env.APS_BASE_URL || '';
    if (!apiKey) {
        return '❌ 未授权：请先连接 AI Product Space 账户。首次使用会自动弹出授权页面。';
    }
    if (!baseUrl) {
        return '❌ 未配置 APS_BASE_URL，请在 config.json 中设置服务地址。';
    }
    const client = new api_client_1.AIProductSpaceClient(baseUrl, apiKey);
    const tool = tools.find((t) => t.manifest.name === toolName);
    if (!tool) {
        return `❌ 未知工具: ${toolName}`;
    }
    try {
        return await tool.handler(client, params);
    }
    catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        return `❌ 执行失败: ${message}`;
    }
}
__exportStar(require("./lib/types"), exports);
