/**
 * AgentChat - Nostr-based Agent messaging CLI
 * 
 * MVP Features:
 * - Login with npub/nsec
 * - Send direct messages
 * - Receive messages
 * - File support (small files via Nostr events)
 */

import { SimplePool, nip04, Kind, finalizeEvent, getEventHash } from "nostr-tools";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { homedir } from "os";
import { join } from "path";

// ============================================================================
// Types
// ============================================================================

interface Config {
  npub: string;
  nsec: string;
  relays: string[];
}

interface Message {
  type: "message";
  from: string;
  to: string;
  content: string;
  content_type: "text/plain" | "application/json";
  timestamp: number;
}

// ============================================================================
// Config
// ============================================================================

const CONFIG_PATH = join(homedir(), ".agent-chat", "config.json");

function loadConfig(): Config {
  if (existsSync(CONFIG_PATH)) {
    return JSON.parse(readFileSync(CONFIG_PATH, "utf-8"));
  }
  throw new Error("Config not found. Run: agent-chat login <nsec>");
}

function saveConfig(config: Config): void {
  const dir = join(homedir(), ".agent-chat");
  import("fs").then(fs => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
  });
}

// ============================================================================
// Nostr Client
// ============================================================================

class AgentChatClient {
  private pool: SimplePool;
  private relays: string[];
  private keys: { pubkey: string; privkey: Uint8Array };

  constructor(npub: string, npriv: string, relays: string[] = []) {
    this.pool = new SimplePool();
    this.relays = relays.length > 0 ? relays : ["wss://relay.damus.io", "wss://nos.lol"];
    this.keys = {
      pubkey: npub,
      privkey: typeof npriv === 'string' ? new Uint8Array(Buffer.from(npriv, 'hex')) : npriv,
    };
  }

  // Send a direct message
  async send(to: string, content: string, contentType: "text/plain" | "application/json" = "text/plain"): Promise<string> {
    const plaintext = JSON.stringify({ to, content, content_type: contentType });
    const encrypted = await nip04.encrypt(this.keys.privkey, to, plaintext);
    
    const event = finalizeEvent({
      kind: 4 as Kind, // Encrypted DM
      created_at: Math.floor(Date.now() / 1000),
      tags: [["p", to]],
      content: encrypted,
      pubkey: this.keys.pubkey,
    }, this.keys.privkey);

    const pubs = this.pool.publish(this.relays, event);
    await Promise.all(pubs);
    
    return event.id;
  }

  // Subscribe to DMs - using onevent callback
  async messages(): Promise<any[]> {
    const messages: any[] = [];
    const pubkey = this.keys.pubkey;
    
    return new Promise((resolve) => {
      // Subscribe with onevent callback to collect messages
      this.pool.subscribeMany(
        this.relays,
        [
          {
            kinds: [4],
            "#p": [pubkey],
            limit: 50,
          },
        ],
        {
          onevent: (event: any) => {
            messages.push(event);
          },
          oneose: () => {
            setTimeout(() => resolve(messages), 1000);
          },
        }
      );
      
      // Fallback timeout
      setTimeout(() => resolve(messages), 8000);
    });
  }

  // Close connections
  close(): void {
    this.pool.close(this.relays);
  }
}

// ============================================================================
// CLI Commands
// ============================================================================

async function login(nsec: string): Promise<void> {
  // Decode nsec to get private key bytes
  const { getPublicKey, nip19 } = await import("nostr-tools");
  
  let privateKey: Uint8Array;
  if (nsec.startsWith('nsec')) {
    const decoded = nip19.decode(nsec);
    privateKey = decoded.data as Uint8Array;
  } else {
    // Assume hex string
    privateKey = new Uint8Array(Buffer.from(nsec, 'hex'));
  }
  
  const npub = getPublicKey(privateKey);
  
  const config: Config = {
    npub,
    nsec,
    relays: [],
  };
  
  saveConfig(config);
  console.log(`✅ Logged in as: ${npub}`);
}

async function send(toNpub: string, content: string): Promise<void> {
  const config = loadConfig();
  const client = new AgentChatClient(config.npub, config.nsec, config.relays);
  
  const id = await client.send(toNpub, content);
  console.log(`✅ Message sent! ID: ${id}`);
  
  client.close();
}

async function receive(limit = 10): Promise<void> {
  const config = loadConfig();
  const client = new AgentChatClient(config.npub, config.nsec, config.relays);
  
  console.log("📥 Fetching messages...");
  
  try {
    const events = await client.messages();
    
    let count = 0;
    for (const msg of events) {
      try {
        // Get private key from client
        const privkeyArray = client['keys'].privkey;
        const privkeyHex = Buffer.from(privkeyArray).toString('hex');
        
        const decrypted = await nip04.decrypt(privkeyHex, msg.pubkey, msg.content);
        const payload = JSON.parse(decrypted);
        
        console.log(`\n[${new Date(msg.created_at * 1000).toLocaleString()}]`);
        console.log(`From: ${msg.pubkey}`);
        console.log(`Content: ${payload.content || decrypted}`);
        count++;
        if (count >= limit) break;
      } catch (e) {
        // Skip unparseable
      }
    }
    
    if (count === 0) {
      console.log("No messages found.");
    }
  } catch (e) {
    console.error("Error receiving messages:", e);
  }
  
  client.close();
}



async function listenRealtime(): Promise<void> {
  const config = loadConfig();
  const client = new AgentChatClient(config.npub, config.nsec, config.relays);

  console.log("👂 Listening for new messages (Ctrl+C to stop)...");

  // keep dedupe in-memory for long-running process
  const seen = new Set<string>();

  // graceful shutdown
  const shutdown = () => {
    console.log("\n🛑 Stopping listener...");
    try { client.close(); } catch {}
    process.exit(0);
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);

  this;
  client['pool'].subscribeMany(
    client['relays'],
    [
      {
        kinds: [4],
        '#p': [config.npub],
        since: Math.floor(Date.now() / 1000),
      },
    ],
    {
      onevent: async (msg: any) => {
        try {
          if (seen.has(msg.id)) return;
          seen.add(msg.id);

          const privkeyArray = client['keys'].privkey as Uint8Array;
          const privkeyHex = Buffer.from(privkeyArray).toString('hex');
          const decrypted = await nip04.decrypt(privkeyHex, msg.pubkey, msg.content);

          let content = decrypted;
          try {
            const payload = JSON.parse(decrypted);
            content = payload.content || decrypted;
          } catch {}

          console.log(`\n[${new Date(msg.created_at * 1000).toLocaleString()}]`);
          console.log(`From: ${msg.pubkey}`);
          console.log(`Content: ${content}`);
        } catch {}
      },
    }
  );

  // keep process alive
  await new Promise(() => {});
}
function status(): void {
  try {
    const config = loadConfig();
    console.log(`🟢 Logged in: ${config.npub}`);
    console.log(`Relays: ${config.relays.length > 0 ? config.relays.join(", ") : "default"}`);
  } catch {
    console.log("🔴 Not logged in. Run: agent-chat login <nsec>");
  }
}

// ============================================================================
// Main
// ============================================================================

const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case "login":
    if (!args[1]) {
      console.error("Usage: agent-chat login <nsec>");
      process.exit(1);
    }
    login(args[1]);
    break;
    
  case "send":
    if (!args[1] || !args[2]) {
      console.error("Usage: agent-chat send <npub> <message>");
      process.exit(1);
    }
    send(args[1], args[2]);
    break;
    
  case "receive":
    receive(parseInt(args[1]) || 10);
    break;
    
  case "status":
    status();
    break;

  case "listen":
    listenRealtime();
    break;
    
  default:
    console.log(`
AgentChat CLI - Nostr-based Agent messaging

Usage:
  agent-chat login <nsec>     # Login with private key
  agent-chat send <npub> <msg> # Send message
  agent-chat receive [count]   # Receive messages
  agent-chat status            # Show status\n  agent-chat listen            # Realtime listener (resident)
    `);
}
