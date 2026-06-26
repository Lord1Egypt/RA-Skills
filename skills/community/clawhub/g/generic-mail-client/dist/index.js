"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.handlers = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const js_yaml_1 = __importDefault(require("js-yaml"));
const mailClient_1 = require("./mailClient");
const configPath = path_1.default.join(__dirname, "..", "config.yaml");
let skillConfig;
if (fs_1.default.existsSync(configPath)) {
    skillConfig = js_yaml_1.default.load(fs_1.default.readFileSync(configPath, "utf8"));
}
else {
    throw new Error("generic-mail-client: config.yaml not found. Please copy config.example.yaml to config.yaml and fill in credentials.");
}
const client = new mailClient_1.MailClient(skillConfig);
// 根据 OpenClaw / MCP 规范导出 handler
// 这里假设 OpenClaw 会加载 `handlers` 对象里的函数
exports.handlers = {
    async sendEmail(args) {
        return client.sendEmail(args);
    },
    async listMessages(args) {
        return client.listMessages(args);
    },
    async getMessage(args) {
        return client.getMessage(args);
    },
    async updateMessageStatus(args) {
        return client.updateMessageStatus(args);
    },
    // getAttachment 可以后续按需要扩展
};
