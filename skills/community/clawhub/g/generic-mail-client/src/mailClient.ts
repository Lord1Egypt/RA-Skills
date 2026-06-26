import nodemailer from "nodemailer";
import { ImapFlow, FetchMessageObject, SearchObject, MessageStructureObject } from "imapflow";
import {
  MailAccountConfig,
  SkillConfig,
  SendEmailRequest,
  SendEmailResponse,
  ListMessagesRequest,
  ListMessagesResponse,
  GetMessageRequest,
  GetMessageResponse,
  UpdateMessageStatusRequest,
  UpdateMessageStatusResponse,
} from "./types";

export class MailClient {
  private accounts: Map<string, MailAccountConfig>;

  constructor(config: SkillConfig) {
    this.accounts = new Map(config.mailAccounts.map((a) => [a.id, a]));
  }

  private getAccount(accountId: string): MailAccountConfig {
    const acc = this.accounts.get(accountId);
    if (!acc) {
      throw new Error(`Unknown accountId: ${accountId}`);
    }
    return acc;
  }

  // ---------- SMTP 发信 ----------
  async sendEmail(req: SendEmailRequest): Promise<SendEmailResponse> {
    const acc = this.getAccount(req.accountId);
    const smtp = acc.smtp;

    const transporter = nodemailer.createTransport({
      host: smtp.host,
      port: smtp.port,
      secure: smtp.useTLS,
      auth: {
        user: acc.auth.username,
        pass: acc.auth.password,
      },
    });

    const message = {
      from: acc.auth.username,
      to: req.to.join(","),
      cc: req.cc?.length ? req.cc.join(",") : undefined,
      bcc: req.bcc?.length ? req.bcc.join(",") : undefined,
      subject: req.subject,
      text: req.bodyText,
      html: req.bodyHtml,
      attachments: (req.attachments || []).map((att) => ({
        filename: att.filename,
        content: Buffer.from(att.contentBase64, "base64"),
        contentType: att.mimeType,
      })),
    };

    const info = await transporter.sendMail(message);

    return {
      status: "ok",
      accountId: req.accountId,
      messageId: info.messageId,
      sentAt: new Date().toISOString(),
    };
  }

  // ---------- IMAP helpers ----------
  private async withImap<T>(acc: MailAccountConfig, fn: (client: ImapFlow) => Promise<T>): Promise<T> {
    if (!acc.imap) throw new Error("IMAP not configured for this account");
    const client = new ImapFlow({
      host: acc.imap.host,
      port: acc.imap.port,
      secure: acc.imap.useTLS,
      auth: {
        user: acc.auth.username,
        pass: acc.auth.password,
      },
    });
    try {
      await client.connect();
      return await fn(client);
    } finally {
      try {
        await client.logout();
      } catch {
        // ignore
      }
    }
  }

  async listMessages(req: ListMessagesRequest): Promise<ListMessagesResponse> {
    const acc = this.getAccount(req.accountId);

    if (acc.protocol.receive === "imap") {
      const folder = req.folder || acc.defaults.inboxFolder;
      const limit = Math.min(req.limit || 20, acc.defaults.maxListLimit);

      return this.withImap(acc, async (client) => {
        await client.mailboxOpen(folder);

        // 构造搜索条件
        const criteria: SearchObject = {
          all: true,
          seen: req.unreadOnly ? false : undefined,
          since: req.since ? new Date(req.since) : undefined,
        };

        const uids = await client.search(criteria);
        const selected = (uids || []).slice(-limit); // 取最近 N 封

        const messages: ListMessagesResponse["messages"] = [];

        for await (const msg of client.fetch(selected, { envelope: true, flags: true, bodyStructure: true, source: false })) {
          const m = msg as FetchMessageObject;
          const id = String(m.uid);
          const subject = m.envelope?.subject || "";
          const from = m.envelope?.from?.[0]?.address || "";
          const to = (m.envelope?.to || []).map((x) => x.address || "");
          const date = m.envelope?.date?.toISOString() || new Date().toISOString();
          const flags = Array.isArray(m.flags) ? m.flags : Array.from(m.flags || []);
          const isRead = flags.includes("\\Seen") ?? null;
          const struct = m.bodyStructure as MessageStructureObject | undefined;
          const hasAttachments = (struct?.childNodes || []).some((n: any) => n.disposition?.type?.toLowerCase() === "attachment");

          messages.push({
            id,
            subject,
            from,
            to,
            date,
            isRead,
            hasAttachments,
            snippet: "", // 如需可单独 fetch 文本再截断
          });
        }

        return {
          accountId: req.accountId,
          folder,
          total: messages.length,
          messages,
        };
      });
    }

    if (acc.protocol.receive === "pop3") {
      // TODO: 实现 POP3 列表（可以用 node-pop3 等库）
      return {
        accountId: req.accountId,
        folder: "INBOX",
        total: 0,
        messages: [],
      };
    }

    throw new Error("Unsupported receive protocol");
  }

  async getMessage(req: GetMessageRequest): Promise<GetMessageResponse> {
    const acc = this.getAccount(req.accountId);

    if (acc.protocol.receive === "imap") {
      const folder = req.folder || acc.defaults.inboxFolder;
      return this.withImap(acc, async (client) => {
        await client.mailboxOpen(folder);
        const uid = Number(req.id);
        const fetched = await client.fetchOne(uid, {
          envelope: true,
          flags: true,
          bodyStructure: true,
          source: true,
        });
        const m = fetched as FetchMessageObject;

        const subject = m.envelope?.subject || "";
        const from = m.envelope?.from?.[0]?.address || "";
        const to = (m.envelope?.to || []).map((x) => x.address || "");
        const cc = (m.envelope?.cc || []).map((x) => x.address || "");
        const date = m.envelope?.date?.toISOString() || new Date().toISOString();
        const flags = Array.isArray(m.flags) ? m.flags : Array.from(m.flags || []);
        const isRead = flags.includes("\\Seen") ?? null;

        const attachments: GetMessageResponse["attachments"] = [];
        const bodyStruct = m.bodyStructure as MessageStructureObject | undefined;
        if (bodyStruct?.childNodes) {
          for (const [idx, rawNode] of bodyStruct.childNodes.entries()) {
            const node: any = rawNode as any;
            const dispType = node.disposition?.type?.toLowerCase();
            if (dispType === "attachment") {
              attachments.push({
                id: String(idx),
                filename: node.disposition?.params?.filename || node.parameters?.name || "attachment",
                size: node.size || 0,
                mimeType: `${node.type}/${node.subtype}`,
              });
            }
          }
        }

        // 简化：只取 text/plain 部分：从 m.source 里粗略提取
        let bodyText: string | undefined;
        if (typeof m.source === "string") {
          bodyText = m.source;
        }

        return {
          accountId: req.accountId,
          id: req.id,
          folder,
          subject,
          from,
          to,
          cc,
          date,
          isRead,
          bodyText,
          bodyHtml: undefined,
          attachments,
        };
      });
    }

    if (acc.protocol.receive === "pop3") {
      // TODO: 实现 POP3 获取单封邮件
      return {
        accountId: req.accountId,
        id: req.id,
        folder: "INBOX",
        subject: "",
        from: "",
        to: [],
        cc: [],
        date: new Date().toISOString(),
        isRead: null,
        bodyText: "",
        bodyHtml: undefined,
        attachments: [],
      };
    }

    throw new Error("Unsupported receive protocol");
  }

  async updateMessageStatus(req: UpdateMessageStatusRequest): Promise<UpdateMessageStatusResponse> {
    const acc = this.getAccount(req.accountId);
    if (acc.protocol.receive !== "imap") {
      return {
        status: "error",
        accountId: req.accountId,
        errorMessage: "updateMessageStatus only supported for IMAP accounts",
      };
    }

    const folder = req.folder || acc.defaults.inboxFolder;
    const uid = Number(req.id);

    await this.withImap(acc, async (client) => {
      await client.mailboxOpen(folder);
      if (req.markAsRead) {
        await client.messageFlagsAdd(uid, ["\\Seen"], { uid: true });
      }
      if (req.markAsUnread) {
        await client.messageFlagsRemove(uid, ["\\Seen"], { uid: true });
      }
      if (req.moveToFolder) {
        await client.messageMove(uid, req.moveToFolder, { uid: true });
      }
    });

    return {
      status: "ok",
      accountId: req.accountId,
      updated: {
        // 实际状态可选返回
      },
    };
  }
}
