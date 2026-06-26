/**
 * Mailbox Core Library
 * 
 * File-based message storage for agents, handlers, and users
 */

import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';

export interface Message {
  id: string;
  from: string;
  to: string;
  subject: string;
  body: string;
  priority: 'normal' | 'high' | 'urgent';
  status: 'unread' | 'read' | 'archived';
  created_at: string;
  expires_at?: string;
  read_at?: string;
  metadata?: Record<string, any>;
  responses: Response[];
}

export interface Response {
  from: string;
  body: string;
  created_at: string;
  metadata?: Record<string, any>;
}

export interface SendOptions {
  to: string;
  subject: string;
  body: string;
  priority?: 'normal' | 'high' | 'urgent';
  expires_in?: number; // seconds
  metadata?: Record<string, any>;
}

export interface InboxMessage {
  id: string;
  from: string;
  subject: string;
  priority: 'normal' | 'high' | 'urgent';
  status: 'unread' | 'read' | 'archived';
  created_at: string;
  unread: boolean;
}

/**
 * Main Mailbox class
 */
export class Mailbox {
  private agent: string;
  private basePath: string;
  private inboxPath: string;
  private sentPath: string;
  private archivePath: string;
  private logPath: string;

  constructor(agentName: string, basePath?: string) {
    this.agent = agentName;
    this.basePath = basePath || path.join(process.env.HOME || '/tmp', '.openclaw', 'workspace', 'mailbox');
    this.inboxPath = path.join(this.basePath, agentName, 'inbox');
    this.sentPath = path.join(this.basePath, agentName, 'sent');
    this.archivePath = path.join(this.basePath, agentName, 'archive');
    this.logPath = path.join(this.basePath, agentName, 'mail.log');

    this.initializePaths();
  }

  /**
   * Initialize mailbox directories
   */
  private initializePaths(): void {
    for (const dir of [this.inboxPath, this.sentPath, this.archivePath]) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    }
  }

  /**
   * Send a message
   */
  async send(options: SendOptions): Promise<Message> {
    const message: Message = {
      id: this.generateId(),
      from: this.agent,
      to: options.to,
      subject: options.subject,
      body: options.body,
      priority: options.priority || 'normal',
      status: 'unread',
      created_at: new Date().toISOString(),
      expires_at: options.expires_in
        ? new Date(Date.now() + options.expires_in * 1000).toISOString()
        : undefined,
      metadata: options.metadata || {},
      responses: [],
    };

    // Save to sent folder
    await this.saveMessage(message, this.sentPath);

    // Save to recipient's inbox
    const recipientInboxPath = path.join(this.basePath, options.to, 'inbox');
    fs.mkdirSync(recipientInboxPath, { recursive: true });
    await this.saveMessage(message, recipientInboxPath);

    // Log
    this.log(`SEND: to=${options.to} subject="${options.subject}" priority=${options.priority || 'normal'}`);

    return message;
  }

  /**
   * Get inbox messages
   */
  async getInbox(): Promise<InboxMessage[]> {
    const files = this.getMessageFiles(this.inboxPath);
    const messages: InboxMessage[] = [];

    for (const file of files) {
      const msg = this.parseMessageFile(file);
      if (msg && msg.status !== 'archived') {
        messages.push({
          id: msg.id,
          from: msg.from,
          subject: msg.subject,
          priority: msg.priority,
          status: msg.status,
          created_at: msg.created_at,
          unread: msg.status === 'unread',
        });
      }
    }

    // Sort by created_at descending (newest first)
    return messages.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
  }

  /**
   * Get unread messages
   */
  async getUnread(): Promise<Message[]> {
    const files = this.getMessageFiles(this.inboxPath);
    const messages: Message[] = [];

    for (const file of files) {
      const msg = this.parseMessageFile(file);
      if (msg && msg.status === 'unread') {
        messages.push(msg);
      }
    }

    return messages;
  }

  /**
   * Get high-priority unread messages
   */
  async getUrgent(): Promise<Message[]> {
    const unread = await this.getUnread();
    return unread.filter(m => m.priority === 'high' || m.priority === 'urgent');
  }

  /**
   * Read a specific message
   */
  async read(messageId: string): Promise<Message | null> {
    // Try inbox first
    let msg = this.findMessage(messageId, this.inboxPath);

    // Try sent
    if (!msg) {
      msg = this.findMessage(messageId, this.sentPath);
    }

    if (msg) {
      return msg;
    }

    return null;
  }

  /**
   * Mark message as read
   */
  async markRead(messageId: string): Promise<boolean> {
    const file = this.findMessageFile(messageId, this.inboxPath);

    if (!file) {
      return false;
    }

    const msg = this.parseMessageFile(file);
    if (msg) {
      msg.status = 'read';
      msg.read_at = new Date().toISOString();
      fs.writeFileSync(file, this.messageToYaml(msg));
      this.log(`READ: ${messageId}`);
      return true;
    }

    return false;
  }

  /**
   * Reply to a message
   */
  async reply(messageId: string, body: string, metadata?: Record<string, any>): Promise<boolean> {
    const file = this.findMessageFile(messageId, this.inboxPath);

    if (!file) {
      return false;
    }

    const msg = this.parseMessageFile(file);
    if (!msg) {
      return false;
    }

    // Add response
    msg.responses.push({
      from: this.agent,
      body,
      created_at: new Date().toISOString(),
      metadata,
    });

    // Update in inbox
    fs.writeFileSync(file, this.messageToYaml(msg));

    // Send reply as new message to original sender
    await this.send({
      to: msg.from,
      subject: `Re: ${msg.subject}`,
      body,
      priority: msg.priority,
      metadata: {
        in_reply_to: messageId,
        ...metadata,
      },
    });

    this.log(`REPLY: to=${msg.from} in_reply_to=${messageId}`);

    return true;
  }

  /**
   * Archive a message
   */
  async archive(messageId: string): Promise<boolean> {
    const file = this.findMessageFile(messageId, this.inboxPath);

    if (!file) {
      return false;
    }

    const msg = this.parseMessageFile(file);
    if (!msg) {
      return false;
    }

    msg.status = 'archived';
    const archiveFile = path.join(this.archivePath, path.basename(file));
    fs.writeFileSync(archiveFile, this.messageToYaml(msg));
    fs.unlinkSync(file);

    this.log(`ARCHIVE: ${messageId}`);

    return true;
  }

  /**
   * Delete a message
   */
  async delete(messageId: string): Promise<boolean> {
    const file = this.findMessageFile(messageId, this.inboxPath);

    if (!file) {
      return false;
    }

    fs.unlinkSync(file);
    this.log(`DELETE: ${messageId}`);

    return true;
  }

  /**
   * Archive expired messages
   */
  async archiveExpired(): Promise<number> {
    const files = this.getMessageFiles(this.inboxPath);
    let count = 0;

    const now = new Date();

    for (const file of files) {
      const msg = this.parseMessageFile(file);
      if (msg && msg.expires_at && new Date(msg.expires_at) < now) {
        msg.status = 'archived';
        const archiveFile = path.join(this.archivePath, path.basename(file));
        fs.writeFileSync(archiveFile, this.messageToYaml(msg));
        fs.unlinkSync(file);
        count++;
        this.log(`EXPIRED: ${msg.id}`);
      }
    }

    return count;
  }

  /**
   * Search messages
   */
  async search(query: string): Promise<Message[]> {
    const files = this.getMessageFiles(this.inboxPath);
    const results: Message[] = [];
    const lowerQuery = query.toLowerCase();

    for (const file of files) {
      const msg = this.parseMessageFile(file);
      if (msg) {
        const matchesSubject = msg.subject.toLowerCase().includes(lowerQuery);
        const matchesBody = msg.body.toLowerCase().includes(lowerQuery);
        const matchesFrom = msg.from.toLowerCase().includes(lowerQuery);

        if (matchesSubject || matchesBody || matchesFrom) {
          results.push(msg);
        }
      }
    }

    return results;
  }

  /**
   * Get message statistics
   */
  async getStats(): Promise<{
    total: number;
    unread: number;
    high_priority: number;
    expired: number;
  }> {
    const files = this.getMessageFiles(this.inboxPath);
    let total = 0;
    let unread = 0;
    let high_priority = 0;
    let expired = 0;

    const now = new Date();

    for (const file of files) {
      const msg = this.parseMessageFile(file);
      if (msg && msg.status !== 'archived') {
        total++;
        if (msg.status === 'unread') unread++;
        if (msg.priority === 'high' || msg.priority === 'urgent') high_priority++;
        if (msg.expires_at && new Date(msg.expires_at) < now) expired++;
      }
    }

    return { total, unread, high_priority, expired };
  }

  // ===== Private helpers =====

  private generateId(): string {
    const timestamp = new Date().toISOString().slice(0, 10);
    const random = crypto.randomBytes(4).toString('hex');
    return `msg-${timestamp}-${random}`;
  }

  private saveMessage(msg: Message, dir: string): void {
    const filename = `${msg.created_at.slice(0, 10)}-${msg.id}.md`;
    const filepath = path.join(dir, filename);
    fs.writeFileSync(filepath, this.messageToYaml(msg));
  }

  private messageToYaml(msg: Message): string {
    const yaml = `id: ${msg.id}
from: ${msg.from}
to: ${msg.to}
subject: ${msg.subject}
priority: ${msg.priority}
status: ${msg.status}
created_at: ${msg.created_at}
${msg.expires_at ? `expires_at: ${msg.expires_at}` : ''}
${msg.read_at ? `read_at: ${msg.read_at}` : ''}
${Object.keys(msg.metadata || {}).length > 0 ? `metadata: ${JSON.stringify(msg.metadata)}` : ''}
---
${msg.body}
${
  msg.responses.length > 0
    ? `\n## Responses\n\n${msg.responses.map((r) => `**${r.from}** (${r.created_at}):\n${r.body}`).join('\n\n---\n\n')}`
    : ''
}`;

    return yaml;
  }

  private parseMessageFile(filepath: string): Message | null {
    try {
      const content = fs.readFileSync(filepath, 'utf-8');
      const [frontmatter, ...rest] = content.split('---');
      const body = rest.join('---').trim();

      const lines = frontmatter.trim().split('\n');
      const meta: Record<string, any> = {};

      for (const line of lines) {
        const [key, ...valueParts] = line.split(': ');
        const value = valueParts.join(': ').trim();

        if (key === 'metadata') {
          meta.metadata = JSON.parse(value);
        } else {
          meta[key] = value;
        }
      }

      return {
        id: meta.id,
        from: meta.from,
        to: meta.to,
        subject: meta.subject,
        body,
        priority: meta.priority || 'normal',
        status: meta.status || 'unread',
        created_at: meta.created_at,
        expires_at: meta.expires_at,
        read_at: meta.read_at,
        metadata: meta.metadata || {},
        responses: [],
      };
    } catch (error) {
      console.error(`Error parsing message file ${filepath}:`, error);
      return null;
    }
  }

  private getMessageFiles(dir: string): string[] {
    if (!fs.existsSync(dir)) {
      return [];
    }

    return fs.readdirSync(dir)
      .filter(f => f.endsWith('.md'))
      .map(f => path.join(dir, f));
  }

  private findMessage(messageId: string, dir: string): Message | null {
    const file = this.findMessageFile(messageId, dir);
    if (!file) {
      return null;
    }

    return this.parseMessageFile(file);
  }

  private findMessageFile(messageId: string, dir: string): string | null {
    const files = this.getMessageFiles(dir);

    for (const file of files) {
      if (file.includes(messageId)) {
        return file;
      }
    }

    return null;
  }

  private log(message: string): void {
    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] ${message}\n`;

    try {
      fs.appendFileSync(this.logPath, logLine);
    } catch (error) {
      console.warn('Failed to write to mail.log:', error);
    }
  }
}
