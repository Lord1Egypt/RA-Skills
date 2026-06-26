import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import { MailClient } from "./mailClient";
import {
  SkillConfig,
  SendEmailRequest,
  ListMessagesRequest,
  GetMessageRequest,
  UpdateMessageStatusRequest,
} from "./types";

const configPath = path.join(__dirname, "..", "config.yaml");

let skillConfig: SkillConfig;
if (fs.existsSync(configPath)) {
  skillConfig = yaml.load(fs.readFileSync(configPath, "utf8")) as SkillConfig;
} else {
  throw new Error("generic-mail-client: config.yaml not found. Please copy config.example.yaml to config.yaml and fill in credentials.");
}

const client = new MailClient(skillConfig);

// 根据 OpenClaw / MCP 规范导出 handler
// 这里假设 OpenClaw 会加载 `handlers` 对象里的函数
export const handlers = {
  async sendEmail(args: SendEmailRequest) {
    return client.sendEmail(args);
  },
  async listMessages(args: ListMessagesRequest) {
    return client.listMessages(args);
  },
  async getMessage(args: GetMessageRequest) {
    return client.getMessage(args);
  },
  async updateMessageStatus(args: UpdateMessageStatusRequest) {
    return client.updateMessageStatus(args);
  },
  // getAttachment 可以后续按需要扩展
};
