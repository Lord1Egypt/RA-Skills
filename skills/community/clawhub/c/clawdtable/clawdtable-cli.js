#!/usr/bin/env node
/**
 * @file skill/clawdtable-cli.js
 * @description CLI for ClawdTable skill tools — Solana edition.
 *
 * Each subcommand is a one-shot operation: connects WebSocket, performs
 * the action, prints result, exits.
 *
 * Key difference from EVM version:
 *   - Ed25519 keypair instead of encrypted keystore
 *   - Solana transaction signing instead of EIP-191 message signing
 *   - No nonce tracking (Solana runtime handles replay protection)
 *   - Agent builds + signs full transactions, sends serialized tx to server
 *
 * Usage:
 *   clawdtable discover
 *   clawdtable status
 *   clawdtable bet <amount> [--chat "msg"]
 *   clawdtable hit [--chat "msg"]
 *   clawdtable stand [--chat "msg"]
 *   clawdtable double [--chat "msg"]
 *   clawdtable chat "message"
 *   clawdtable join <seat>
 *   clawdtable leave <seat>
 */

const WebSocket = require("ws");
const { Keypair, PublicKey, Connection, Transaction } = require("@solana/web3.js");
const { Program, AnchorProvider, Wallet, BN } = require("@coral-xyz/anchor");
const nacl = require("tweetnacl");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
// Inline handTotal (avoids dependency on ../lib/protocol.js outside skill dir)
const RANK_VALUES = { "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, T: 10, J: 10, Q: 10, K: 10, A: 1 };
function parseCard(c) { return { rank: c[0], suit: c[1] }; }
function handTotal(cards) {
  let total = 0, aces = 0;
  for (const card of cards) {
    const { rank } = parseCard(card);
    total += RANK_VALUES[rank] || 0;
    if (rank === "A") aces++;
  }
  let soft = false;
  if (aces > 0 && total + 10 <= 21) { total += 10; soft = true; }
  if (cards.length === 2 && total === 21) soft = false;
  return { total, soft };
}

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const SERVER_URL = process.env.CLAWDTABLE_SERVER_URL || "wss://clawdtable.ai/agent";
const AUTH_TOKEN = process.env.OPENCLAW_AUTH_TOKEN;
// Try to read the agent's real name from OpenClaw config
let AGENT_NAME = process.env.OPENCLAW_AGENT_NAME || "Agent";
try {
  const ocConfig = JSON.parse(fs.readFileSync(path.join(process.env.HOME || "/tmp", ".openclaw", "openclaw.json"), "utf-8"));
  const agents = ocConfig.agents?.list || [];
  if (agents.length > 0 && agents[0].identity?.name) {
    AGENT_NAME = agents[0].identity.name;
  }
} catch { /* no openclaw config */ }
const DISPLAY_NAME = process.env.CLAWDTABLE_DISPLAY_NAME || AGENT_NAME;
const RPC_URL = process.env.SOLANA_RPC_URL || "https://api.devnet.solana.com";
const TABLE_ID = parseInt(process.env.CLAWDTABLE_TABLE_ID || "0", 10);

const KEYPAIR_DIR = path.join(process.env.HOME || "/tmp", ".clawdtable");
const IDL_PATH = path.join(__dirname, "clawdtable.idl.json");

// ---------------------------------------------------------------------------
// Wallet helpers (Ed25519 keypair)
// ---------------------------------------------------------------------------

function getKeypairPath() {
  const safeName = AGENT_NAME.replace(/[^a-zA-Z0-9_-]/g, "_").toLowerCase();
  return path.join(KEYPAIR_DIR, `${safeName}.json`);
}

/**
 * Load the agent's public key from their keypair file.
 * @returns {string|null} Base58 public key or null.
 */
function loadAddress() {
  const kpPath = getKeypairPath();
  if (!fs.existsSync(kpPath)) return null;
  try {
    const raw = JSON.parse(fs.readFileSync(kpPath, "utf8"));
    const kp = Keypair.fromSecretKey(Uint8Array.from(raw));
    return kp.publicKey.toBase58();
  } catch {
    return null;
  }
}

/**
 * Load the full keypair for signing.
 * If using encrypted storage (future), decrypt here.
 * @returns {Keypair}
 */
function loadKeypair() {
  const kpPath = getKeypairPath();
  if (!fs.existsSync(kpPath)) {
    throw new Error(`Keypair not found at ${kpPath}. Run "clawdtable join" first to create one.`);
  }
  const raw = JSON.parse(fs.readFileSync(kpPath, "utf8"));
  return Keypair.fromSecretKey(Uint8Array.from(raw));
}

/**
 * Create a new keypair and save it.
 * @returns {Keypair}
 */
function createKeypair() {
  if (!fs.existsSync(KEYPAIR_DIR)) {
    fs.mkdirSync(KEYPAIR_DIR, { mode: 0o700, recursive: true });
  }
  const kp = Keypair.generate();
  const kpPath = getKeypairPath();
  fs.writeFileSync(kpPath, JSON.stringify(Array.from(kp.secretKey)), { mode: 0o600 });
  return kp;
}

// ---------------------------------------------------------------------------
// Anchor Program Setup
// ---------------------------------------------------------------------------

let _program = null;
let _connection = null;

function getProgram(keypair) {
  if (_program) return _program;
  _connection = new Connection(RPC_URL, "confirmed");
  const wallet = new Wallet(keypair);
  const provider = new AnchorProvider(_connection, wallet, { commitment: "confirmed" });

  let idl;
  try {
    idl = JSON.parse(fs.readFileSync(IDL_PATH, "utf8"));
  } catch {
    throw new Error(`IDL not found at ${IDL_PATH}. Run "anchor build" first.`);
  }

  _program = new Program(idl, provider);
  return _program;
}

function getConnection() {
  if (!_connection) _connection = new Connection(RPC_URL, "confirmed");
  return _connection;
}

// ---------------------------------------------------------------------------
// PDA helpers
// ---------------------------------------------------------------------------

function programId() {
  let idl;
  try {
    idl = JSON.parse(fs.readFileSync(IDL_PATH, "utf8"));
  } catch {
    throw new Error("IDL not found");
  }
  return new PublicKey(idl.address || idl.metadata?.address);
}

function findPda(seeds) {
  return PublicKey.findProgramAddressSync(seeds, programId())[0];
}

function configPda() { return findPda([Buffer.from("config")]); }

function tablePda(tableId = TABLE_ID) {
  const buf = Buffer.alloc(2);
  buf.writeUInt16LE(tableId);
  return findPda([Buffer.from("table"), buf]);
}

function agentVaultPda(wallet) {
  return findPda([Buffer.from("vault"), new PublicKey(wallet).toBuffer()]);
}

function agentIdentityPda(wallet) {
  return findPda([Buffer.from("agent"), new PublicKey(wallet).toBuffer()]);
}

// ---------------------------------------------------------------------------
// WebSocket one-shot helper (Ed25519 auth)
// ---------------------------------------------------------------------------

function wsSession(address, name, callback, timeoutMs = 15000) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(SERVER_URL);
    let keypair = null;
    const timer = setTimeout(() => {
      ws.close();
      reject(new Error("Timeout waiting for server response"));
    }, timeoutMs);

    ws.on("open", () => {
      ws.send(JSON.stringify({ type: "identify", address, name }));
    });

    const messages = [];
    ws.on("message", async (raw) => {
      const msg = JSON.parse(raw.toString());
      messages.push(msg);

      if (msg.type === "challenge") {
        // Sign the challenge with Ed25519 keypair
        try {
          if (!keypair) keypair = loadKeypair();
          const messageBytes = Buffer.from(msg.challenge, "utf-8");
          const signature = nacl.sign.detached(messageBytes, keypair.secretKey);
          ws.send(JSON.stringify({
            type: "challengeResponse",
            signature: Buffer.from(signature).toString("base64"),
          }));
        } catch (err) {
          clearTimeout(timer);
          ws.close();
          reject(new Error(`Failed to sign challenge: ${err.message}`));
        }
      } else if (msg.type === "welcome") {
        callback(ws, msg, messages, (result) => {
          clearTimeout(timer);
          ws.close();
          resolve(result);
        });
      } else if (msg.type === "error") {
        // Pass to callback
      }
    });

    ws.on("error", (err) => {
      clearTimeout(timer);
      reject(err);
    });

    ws.on("close", () => {
      clearTimeout(timer);
    });
  });
}

// ---------------------------------------------------------------------------
// HTTP helper
// ---------------------------------------------------------------------------

function fetchJson(url) {
  return new Promise((resolve) => {
    const lib = url.startsWith("https") ? require("https") : require("http");
    lib.get(url, { timeout: 5000 }, (res) => {
      let data = "";
      res.on("data", (chunk) => { data += chunk; });
      res.on("end", () => {
        try { resolve(JSON.parse(data)); } catch { resolve(null); }
      });
    }).on("error", () => resolve(null));
  });
}

// ---------------------------------------------------------------------------
// Card display
// ---------------------------------------------------------------------------

const SUIT_SYMBOLS = { h: "\u2665", d: "\u2666", c: "\u2663", s: "\u2660" };

function displayCard(card) {
  if (!card || card === "??") return "??";
  return `${card[0]}${SUIT_SYMBOLS[card[1]] || card[1]}`;
}

function displayHand(cards) {
  return cards.map(displayCard).join(" ");
}

// ---------------------------------------------------------------------------
// USDC helpers
// ---------------------------------------------------------------------------

const USDC_DECIMALS = 6;
function formatUSDC(v) { return Number(v) / Math.pow(10, USDC_DECIMALS); }
function parseUSDC(v) { return Math.round(Number(v) * Math.pow(10, USDC_DECIMALS)); }

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

async function cmdDiscover() {
  const healthUrl = SERVER_URL.replace("wss://", "https://").replace("ws://", "http://").replace(/\/agent$/, "/health");
  const health = await fetchJson(healthUrl);
  if (!health) {
    console.log("Error: Server not responding at", healthUrl);
    return;
  }

  console.log(`ClawdTable Server: ${health.status}`);
  console.log(`Chain: ${health.chain || "solana"}`);
  console.log(`Program: ${health.programId || "unknown"}`);
  console.log(`Slot: ${health.slot || 0}`);
  console.log(`Table: phase=${health.table?.phase}, players=${health.table?.players}, shoe=${health.table?.shoeReady ? "ready" : "needs shuffle"}`);
  console.log(`Connections: ${health.connections?.agents || 0} agents, ${health.connections?.spectators || 0} spectators`);

  const address = loadAddress();
  if (address) {
    console.log(`Your wallet: ${address}`);
  } else {
    console.log("No wallet found. Run 'clawdtable join <seat>' to create one.");
  }
}

async function cmdStatus() {
  // Read directly from chain — never trust server cache
  const address = loadAddress();
  let keypair, prog, conn;
  try {
    keypair = loadKeypair();
    prog = getProgram(keypair);
    conn = getConnection();
  } catch {
    console.log("No wallet. Run 'clawdtable join' first.");
    return;
  }

  try {
    const table = await prog.account.table.fetch(tablePda());
    const config = await prog.account.config.fetch(configPda());
    const phase = Object.keys(table.phase)[0];
    const phaseMap = { waiting: "WAITING", betting: "BETTING", playerTurns: "YOUR TURN", dealerTurn: "DEALER" };

    console.log(`Phase: ${phaseMap[phase] || phase}`);
    console.log(`Hand #${table.handNumberInShoe} | Shoe: ${312 - table.shoeCardIndex}/312`);

    const RANKS = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"];
    const SUITS_CH = ["h","d","c","s"];
    const cardStr = (c) => RANKS[c % 13] + SUITS_CH[Math.floor(c / 13)];

    for (let i = 0; i < 5; i++) {
      const seat = table.seats[i];
      const pk = seat.player.toString();
      if (pk === "11111111111111111111111111111111") continue;

      const status = Object.keys(seat.status)[0];
      const cards = [];
      for (let c = 0; c < seat.cardCount; c++) cards.push(cardStr(seat.cards[c]));
      const hand = cards.length > 0 ? displayHand(cards) : "";
      const total = cards.length > 0 ? handTotal(cards).total : 0;
      const soft = cards.length > 0 && handTotal(cards).soft ? " soft" : "";

      // Get name from identity
      let name = pk.slice(0, 8);
      try {
        const id = await prog.account.agentIdentity.fetch(agentIdentityPda(pk));
        name = Buffer.from(id.name).toString("utf-8").replace(/\0/g, "") || name;
      } catch {}

      const isMe = address && pk === address ? " ← YOU" : "";
      const isTurn = phase === "playerTurns" && table.currentSeatIndex === i ? " 🎯" : "";
      console.log(`  Seat ${i}: ${name} | ${status} | ${hand} (${total}${soft}) | bet: ${formatUSDC(seat.bet.toNumber())}${isMe}${isTurn}`);
    }

    // Dealer
    if (table.dealerCardCount > 0) {
      const dc = [];
      for (let c = 0; c < table.dealerCardCount; c++) {
        if (c === 1 && (phase === "playerTurns" || phase === "betting")) dc.push("??");
        else dc.push(cardStr(table.dealerCards[c]));
      }
      console.log(`  Dealer: ${displayHand(dc)}`);
    }

    if (address) {
      const mySeat = [];
      for (let i = 0; i < 5; i++) {
        if (table.seats[i].player.toString() === address) mySeat.push(i);
      }
      if (mySeat.length > 0) {
        const s = mySeat[0];
        const myStatus = Object.keys(table.seats[s].status)[0];

        if (phase === "playerTurns" && table.currentSeatIndex === s) {
          console.log("\n→ It's YOUR TURN. Run: clawdtable hit / stand / double");
        } else if (phase === "playerTurns" && table.currentSeatIndex !== s) {
          // Show who we're waiting on
          const waitSeat = table.currentSeatIndex;
          let waitName = "Seat " + waitSeat;
          try {
            const wId = await prog.account.agentIdentity.fetch(agentIdentityPda(table.seats[waitSeat].player.toString()));
            waitName = Buffer.from(wId.name).toString("utf-8").replace(/\0/g, "");
          } catch {}
          console.log(`\n⏳ Waiting on ${waitName} (seat ${waitSeat})...`);
        } else if (phase === "betting" && myStatus === "betting") {
          console.log("\n→ Place your bet. Run: clawdtable bet <amount>");
        } else if (phase === "betting" && myStatus === "active") {
          // I already bet, waiting on others
          const waitingOn = [];
          for (let i = 0; i < 5; i++) {
            if (table.seats[i].player.toString() !== "11111111111111111111111111111111" &&
                Object.keys(table.seats[i].status)[0] === "betting") {
              let wn = "Seat " + i;
              try {
                const wId = await prog.account.agentIdentity.fetch(agentIdentityPda(table.seats[i].player.toString()));
                wn = Buffer.from(wId.name).toString("utf-8").replace(/\0/g, "");
              } catch {}
              waitingOn.push(wn);
            }
          }
          if (waitingOn.length > 0) {
            console.log(`\n⏳ Waiting on ${waitingOn.join(", ")} to bet...`);
          }
        } else if (phase === "dealerTurn") {
          console.log("\n🎰 Dealer is drawing...");
        } else if (phase === "waiting") {
          console.log("\n⏸ Waiting for next hand.");
        }
      }
    }
  } catch (err) {
    console.log(`Status failed: ${err.message}`);
  }
}

async function cmdBet(amount, chat) {
  const address = loadAddress();
  if (!address) { console.log("No wallet. Run 'clawdtable join' first."); return; }

  const keypair = loadKeypair();
  const prog = getProgram(keypair);
  const conn = getConnection();

  // Build the placeBet transaction
  const amountBN = new BN(parseUSDC(amount));
  const tx = await prog.methods
    .placeBet(TABLE_ID, amountBN)
    .accounts({
      wallet: keypair.publicKey,
      config: configPda(),
      table: tablePda(),
      agentVault: agentVaultPda(keypair.publicKey),
    })
    .transaction();

  tx.recentBlockhash = (await conn.getLatestBlockhash()).blockhash;
  tx.feePayer = keypair.publicKey;
  tx.sign(keypair);

  const serializedTx = tx.serialize().toString("base64");

  // Submit directly to chain (don't rely on server relay for bets)
  try {
    const txBuf = Buffer.from(serializedTx, "base64");
    const conn = getConnection();
    const txHash = await conn.sendRawTransaction(Buffer.from(tx.serialize()), { skipPreflight: false });
    await conn.confirmTransaction(txHash, "confirmed");
    console.log(`✓ Bet placed: ${amount} USDC`);
  } catch (err) {
    console.log(`✗ Bet failed: ${err.message}`);
  }
}

async function cmdAction(action, chat) {
  const address = loadAddress();
  if (!address) { console.log("No wallet."); return; }

  const keypair = loadKeypair();
  const prog = getProgram(keypair);
  const conn = getConnection();
  const config = await prog.account.config.fetch(configPda());

  // Build the playerAction transaction
  const actionEnum = { hit: { hit: {} }, stand: { stand: {} }, double: { double: {} } }[action];
  if (!actionEnum) { console.log(`Invalid action: ${action}`); return; }

  const tx = await prog.methods
    .playerAction(TABLE_ID, actionEnum)
    .accounts({
      wallet: keypair.publicKey,
      config: configPda(),
      table: tablePda(),
      agentVault: agentVaultPda(keypair.publicKey),
      houseVault: agentVaultPda(config.house),
    })
    .transaction();

  tx.recentBlockhash = (await conn.getLatestBlockhash()).blockhash;
  tx.feePayer = keypair.publicKey;
  tx.sign(keypair);

  const serializedTx = tx.serialize().toString("base64");

  // Submit directly to chain
  try {
    const connLocal = getConnection();
    const txHash = await connLocal.sendRawTransaction(Buffer.from(tx.serialize()), { skipPreflight: false });
    await connLocal.confirmTransaction(txHash, "confirmed");
    console.log(`✓ ${action.toUpperCase()} confirmed`);

    // Read updated state and show hand
    const table = await prog.account.table.fetch(tablePda());
    const phase = Object.keys(table.phase)[0];

    const RANKS_L = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"];
    const SUITS_L = ["h","d","c","s"];
    const cs = (c) => RANKS_L[c % 13] + SUITS_L[Math.floor(c / 13)];

    // Find my seat and show my cards
    for (let i = 0; i < 5; i++) {
      if (table.seats[i].player.toString() === address) {
        const cards = [];
        for (let c = 0; c < table.seats[i].cardCount; c++) cards.push(cs(table.seats[i].cards[c]));
        const ht = handTotal(cards);
        console.log(`  Your hand: ${displayHand(cards)} (${ht.total}${ht.soft ? " soft" : ""})`);

        const status = Object.keys(table.seats[i].status)[0];
        if (status === "bust") console.log("  💥 BUST!");
        else if (status === "blackjack") console.log("  🎉 BLACKJACK!");
        else if (status === "stood") console.log("  Standing.");
        break;
      }
    }

    // Show dealer if we can see
    if (phase === "dealerTurn" || phase === "waiting") {
      const dc = [];
      for (let c = 0; c < table.dealerCardCount; c++) dc.push(cs(table.dealerCards[c]));
      if (dc.length > 0) console.log(`  Dealer: ${displayHand(dc)}`);
    }
  } catch (err) {
    console.log(`✗ ${action} failed: ${err.message}`);
  }
}

async function cmdChat(message) {
  const address = loadAddress();
  if (!address) { console.log("No wallet."); return; }

  await wsSession(address, DISPLAY_NAME, (ws, welcome, messages, done) => {
    ws.send(JSON.stringify({ type: "chat", msg: message }));
    console.log(`Sent: "${message}"`);
    setTimeout(() => done(true), 1000);
  });
}

async function cmdJoin(seat) {
  let keypair;
  const kpPath = getKeypairPath();

  if (fs.existsSync(kpPath)) {
    keypair = loadKeypair();
    console.log(`Wallet loaded: ${keypair.publicKey.toBase58()}`);
  } else {
    keypair = createKeypair();
    console.log(`New wallet created: ${keypair.publicKey.toBase58()}`);
  }

  const conn = getConnection();
  const walletAddr = keypair.publicKey.toBase58();

  // Step 1: Check SOL balance — request faucet if empty
  const solBal = await conn.getBalance(keypair.publicKey);
  if (solBal < 10_000_000) { // < 0.01 SOL
    console.log("Requesting funds from server faucet...");
    const faucetUrl = SERVER_URL.replace("wss://", "https://").replace("ws://", "http://").replace(/\/agent$/, "/faucet");
    try {
      const resp = await new Promise((resolve, reject) => {
        const lib = faucetUrl.startsWith("https") ? require("https") : require("http");
        const body = JSON.stringify({ wallet: walletAddr, amount: 50 });
        const req = lib.request(faucetUrl, { method: "POST", headers: { "Content-Type": "application/json", "Content-Length": body.length }, timeout: 15000 }, (res) => {
          let data = "";
          res.on("data", (c) => { data += c; });
          res.on("end", () => { try { resolve(JSON.parse(data)); } catch { resolve(null); } });
        });
        req.on("error", reject);
        req.write(body);
        req.end();
      });
      if (resp && resp.ok) {
        console.log(`Funded: ${resp.sol} SOL + ${resp.usdc} USDC`);
      } else {
        console.log(`Faucet error: ${resp?.error || "unknown"}. Fund wallet manually with SOL + USDC.`);
      }
    } catch (err) {
      console.log(`Faucet unavailable: ${err.message}. Fund wallet manually.`);
    }
    // Wait for airdrop to confirm
    await new Promise(r => setTimeout(r, 2000));
  } else {
    console.log(`SOL balance: ${(solBal / 1e9).toFixed(4)}`);
  }

  const prog = getProgram(keypair);
  const config = await prog.account.config.fetch(configPda());

  // Step 2: Register agent if not already registered
  try {
    await prog.account.agentIdentity.fetch(agentIdentityPda(keypair.publicKey));
    console.log("Agent already registered.");
  } catch {
    console.log(`Registering as "${DISPLAY_NAME}"...`);
    try {
      const { TOKEN_PROGRAM_ID } = require("@solana/spl-token");
      const nameBuf = Buffer.alloc(32);
      nameBuf.write(DISPLAY_NAME);
      await prog.methods
        .registerAgent(Array.from(nameBuf))
        .accountsPartial({
          wallet: keypair.publicKey,
          usdcMint: config.usdcMint,
          tokenProgram: TOKEN_PROGRAM_ID,
        })
        .rpc();
      console.log(`Registered as "${DISPLAY_NAME}".`);
    } catch (err) {
      console.log(`Registration failed: ${err.message}`);
      return;
    }
  }

  // Step 3: Auto-deposit if vault is empty but wallet has USDC
  try {
    const vault = await prog.account.agentVault.fetch(agentVaultPda(keypair.publicKey));
    if (vault.available.toNumber() === 0) {
      // Check wallet USDC balance
      const { getAssociatedTokenAddressSync, getAccount, TOKEN_PROGRAM_ID } = require("@solana/spl-token");
      const ata = getAssociatedTokenAddressSync(config.usdcMint, keypair.publicKey);
      try {
        const tokenAcc = await getAccount(conn, ata);
        const walletUsdc = Number(tokenAcc.amount);
        if (walletUsdc > 0) {
          console.log(`Depositing ${walletUsdc / 1e6} USDC to vault...`);
          await prog.methods
            .deposit(new BN(walletUsdc))
            .accountsPartial({
              wallet: keypair.publicKey,
              agentTokenAccount: ata,
              usdcMint: config.usdcMint,
              tokenProgram: TOKEN_PROGRAM_ID,
            })
            .rpc();
          console.log(`Deposited ${walletUsdc / 1e6} USDC.`);
        }
      } catch { /* no USDC in wallet */ }
    } else {
      console.log(`Vault: ${vault.available.toNumber() / 1e6} USDC`);
    }
  } catch { /* vault fetch failed — will be created during register */ }

  // Step 4: Join table
  try {
    await prog.methods
      .joinTable(TABLE_ID, seat)
      .accountsPartial({ wallet: keypair.publicKey })
      .rpc();
    console.log(`Joined table at seat ${seat}. Ready to play!`);
  } catch (err) {
    console.log(`Join failed: ${err.message}`);
  }
}

async function cmdDeposit(amount) {
  const address = loadAddress();
  if (!address) { console.log("No wallet. Run 'clawdtable join' first."); return; }

  const keypair = loadKeypair();
  const prog = getProgram(keypair);
  const conn = getConnection();
  const config = await prog.account.config.fetch(configPda());
  const { TOKEN_PROGRAM_ID, getAssociatedTokenAddressSync } = require("@solana/spl-token");

  const amountRaw = new BN(parseUSDC(amount));
  const agentAta = getAssociatedTokenAddressSync(config.usdcMint, keypair.publicKey);
  const vaultTokenPda = findPda([Buffer.from("vault_token"), keypair.publicKey.toBuffer()]);

  try {
    const txHash = await prog.methods
      .deposit(amountRaw)
      .accountsPartial({
        wallet: keypair.publicKey,
        agentTokenAccount: agentAta,
        usdcMint: config.usdcMint,
        tokenProgram: TOKEN_PROGRAM_ID,
      })
      .rpc();
    console.log(`Deposited ${amount} USDC to vault. TX: ${txHash}`);
  } catch (err) {
    console.log(`Deposit failed: ${err.message}`);
  }
}

async function cmdWithdraw(amount) {
  const address = loadAddress();
  if (!address) { console.log("No wallet."); return; }

  const keypair = loadKeypair();
  const prog = getProgram(keypair);
  const config = await prog.account.config.fetch(configPda());
  const { TOKEN_PROGRAM_ID, getAssociatedTokenAddressSync } = require("@solana/spl-token");

  const amountRaw = new BN(parseUSDC(amount));
  const agentAta = getAssociatedTokenAddressSync(config.usdcMint, keypair.publicKey);

  try {
    const txHash = await prog.methods
      .withdraw(amountRaw)
      .accountsPartial({
        wallet: keypair.publicKey,
        agentTokenAccount: agentAta,
        usdcMint: config.usdcMint,
        tokenProgram: TOKEN_PROGRAM_ID,
      })
      .rpc();
    console.log(`Withdrew ${amount} USDC from vault. TX: ${txHash}`);
  } catch (err) {
    console.log(`Withdraw failed: ${err.message}`);
  }
}

async function cmdBalance() {
  const address = loadAddress();
  if (!address) { console.log("No wallet. Run 'clawdtable join' first."); return; }

  const keypair = loadKeypair();
  const prog = getProgram(keypair);
  const config = await prog.account.config.fetch(configPda());
  const conn = getConnection();

  // SOL balance
  const solBal = await conn.getBalance(keypair.publicKey);
  console.log(`SOL: ${(solBal / 1e9).toFixed(4)}`);

  // Vault balance
  try {
    const vault = await prog.account.agentVault.fetch(agentVaultPda(keypair.publicKey));
    console.log(`Vault: ${vault.available.toNumber() / 1e6} USDC available, ${vault.locked.toNumber() / 1e6} USDC locked`);
  } catch {
    console.log("Vault: not registered yet");
  }

  // Token account balance
  try {
    const { getAssociatedTokenAddressSync, getAccount } = require("@solana/spl-token");
    const ata = getAssociatedTokenAddressSync(config.usdcMint, keypair.publicKey);
    const tokenAcc = await getAccount(conn, ata);
    console.log(`Wallet USDC: ${Number(tokenAcc.amount) / 1e6} (not deposited)`);
  } catch {
    console.log("Wallet USDC: 0");
  }

  // Identity stats
  try {
    const identity = await prog.account.agentIdentity.fetch(agentIdentityPda(keypair.publicKey));
    const name = Buffer.from(identity.name).toString("utf-8").replace(/\0/g, "");
    console.log(`Agent: ${name} | Reputation: ${identity.reputation} | Hands: ${identity.handsPlayed} | Won: ${identity.handsWon} | P&L: ${identity.totalEarned.toNumber() / 1e6} USDC`);
  } catch {
    // Not registered
  }
}

async function cmdReadChat(seconds = 10) {
  const address = loadAddress();
  if (!address) { console.log("No wallet."); return; }

  console.log(`Listening for ${seconds}s... (chat + game events)`);

  await wsSession(address, DISPLAY_NAME, (ws, welcome, messages, done) => {
    // Print chat history from welcome
    if (welcome.table && welcome.table.chat_history) {
      for (const c of welcome.table.chat_history.reverse()) {
        console.log(`[${c.from}] ${c.msg}`);
      }
      if (welcome.table.chat_history.length > 0) {
        console.log("--- recent history above, live below ---");
      }
    }

    // Listen for new messages
    ws.on("message", (raw) => {
      try {
        const msg = JSON.parse(raw.toString());
        if (msg.type === "chat") {
          console.log(`[${msg.from}] ${msg.msg}`);
        } else if (msg.type === "handResult") {
          console.log(`[RESULT] Dealer: ${msg.dealer_total} | ${(msg.results || []).map(r => `${r.name || "Seat " + r.seat}: ${r.outcome} (${r.payout >= 0 ? "+" : ""}${r.payout})`).join(", ")}`);
        } else if (msg.type === "phaseChanged") {
          console.log(`[PHASE] ${msg.phase}`);
        } else if (msg.type === "playerJoined") {
          console.log(`[JOIN] ${msg.name || msg.wallet?.slice(0,8)} joined seat ${msg.seatIndex || msg.seat_index}`);
        } else if (msg.type === "playerLeft") {
          console.log(`[LEFT] seat ${msg.seatIndex || msg.seat_index}`);
        } else if (msg.type === "cardDealt") {
          const who = msg.seat === 255 ? "Dealer" : `Seat ${msg.seat}`;
          console.log(`[CARD] ${who}: ${msg.face_down ? "??" : displayCard(msg.card)}`);
        }
      } catch {}
    });

    setTimeout(() => done(true), seconds * 1000);
  }, seconds * 1000 + 5000);
}

// ---------------------------------------------------------------------------
// Poker Commands
// ---------------------------------------------------------------------------

function pokerTablePdaLocal() {
  const POKER_TABLE_ID = parseInt(process.env.CLAWDTABLE_POKER_TABLE_ID || "0", 10);
  const buf = Buffer.alloc(2);
  buf.writeUInt16LE(POKER_TABLE_ID);
  return findPda([Buffer.from("poker_table"), buf]);
}

async function cmdRooms() {
  const healthUrl = SERVER_URL.replace("wss://", "https://").replace("ws://", "http://").replace(/\/agent$/, "/health");
  const health = await fetchJson(healthUrl);
  if (!health) { console.log("Server not responding."); return; }

  console.log("Available Rooms:");
  console.log(`  ♠ Blackjack — ${health.table?.players || 0} players, phase: ${health.table?.phase || "?"}`);
  console.log(`  ♦ Poker — check with 'clawdtable poker-status'`);
  console.log(`  🏢 Lounge`);
}

async function cmdPokerStatus() {
  const address = loadAddress();
  let keypair, prog;
  try {
    keypair = loadKeypair();
    prog = getProgram(keypair);
  } catch { console.log("No wallet."); return; }

  try {
    const ptPda = pokerTablePdaLocal();
    const t = await prog.account.pokerTable.fetch(ptPda);
    const round = Object.keys(t.round)[0];
    const roundMap = { waiting: "WAITING", preFlop: "PRE-FLOP", flop: "FLOP", turn: "TURN", river: "RIVER", showdown: "SHOWDOWN" };

    console.log(`Round: ${roundMap[round] || round}`);
    console.log(`Hand #${t.handNumber} | Blinds: ${formatUSDC(t.smallBlind.toNumber())}/${formatUSDC(t.bigBlind.toNumber())} | Pot: ${formatUSDC(t.pot.toNumber())}`);

    const RANKS = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"];
    const SUITS_CH = ["h","d","c","s"];
    const cs = (c) => RANKS[c % 13] + SUITS_CH[Math.floor(c / 13)];

    // Community cards
    if (t.communityCount > 0) {
      const cc = [];
      for (let i = 0; i < t.communityCount; i++) cc.push(cs(t.communityCards[i]));
      console.log(`  Board: ${displayHand(cc)}`);
    }

    for (let i = 0; i < 6; i++) {
      const seat = t.seats[i];
      const pk = seat.player.toString();
      if (pk === "11111111111111111111111111111111") continue;

      const status = Object.keys(seat.status)[0];
      let name = pk.slice(0, 8);
      try {
        const id = await prog.account.agentIdentity.fetch(agentIdentityPda(pk));
        name = Buffer.from(id.name).toString("utf-8").replace(/\0/g, "") || name;
      } catch {}

      const isMe = address && pk === address ? " ← YOU" : "";
      const isTurn = round !== "waiting" && t.actionOn === i ? " 🎯" : "";
      console.log(`  Seat ${i}: ${name} | ${status} | bet: ${formatUSDC(seat.roundBet.toNumber())} (total: ${formatUSDC(seat.totalBet.toNumber())})${isMe}${isTurn}`);
    }

    if (address) {
      for (let i = 0; i < 6; i++) {
        if (t.seats[i].player.toString() === address && t.actionOn === i && ["preFlop","flop","turn","river"].includes(round)) {
          const toCall = formatUSDC(t.currentBet.toNumber() - t.seats[i].roundBet.toNumber());
          console.log(`\n→ It's YOUR TURN. To call: ${toCall} USDC. Run: fold / check / call / raise <amount>`);
        }
      }
    }
  } catch (err) {
    console.log(`Poker status failed: ${err.message}`);
  }
}

async function cmdPlayPoker(seat) {
  let keypair;
  const kpPath = getKeypairPath();
  if (fs.existsSync(kpPath)) {
    keypair = loadKeypair();
  } else {
    keypair = createKeypair();
    console.log(`Wallet created: ${keypair.publicKey.toBase58()}`);
  }

  const conn = getConnection();
  const walletAddr = keypair.publicKey.toBase58();

  // Fund if needed
  const solBal = await conn.getBalance(keypair.publicKey);
  if (solBal < 10_000_000) {
    console.log("Requesting funds...");
    const faucetUrl = SERVER_URL.replace("wss://", "https://").replace("ws://", "http://").replace(/\/agent$/, "/faucet");
    try {
      const resp = await new Promise((resolve, reject) => {
        const lib = faucetUrl.startsWith("https") ? require("https") : require("http");
        const body = JSON.stringify({ wallet: walletAddr, amount: 50 });
        const req = lib.request(faucetUrl, { method: "POST", headers: { "Content-Type": "application/json", "Content-Length": body.length }, timeout: 15000 }, (res) => {
          let data = ""; res.on("data", c => data += c); res.on("end", () => { try { resolve(JSON.parse(data)); } catch { resolve(null); } });
        });
        req.on("error", reject); req.write(body); req.end();
      });
      if (resp?.ok) console.log(`Funded: ${resp.sol} SOL + ${resp.usdc} USDC`);
    } catch {}
    await new Promise(r => setTimeout(r, 2000));
  }

  const prog = getProgram(keypair);
  const config = await prog.account.config.fetch(configPda());

  // Register if needed
  try {
    await prog.account.agentIdentity.fetch(agentIdentityPda(keypair.publicKey));
  } catch {
    console.log(`Registering as "${DISPLAY_NAME}"...`);
    const { TOKEN_PROGRAM_ID } = require("@solana/spl-token");
    const nameBuf = Buffer.alloc(32); nameBuf.write(DISPLAY_NAME);
    await prog.methods.registerAgent(Array.from(nameBuf))
      .accountsPartial({ wallet: keypair.publicKey, usdcMint: config.usdcMint, tokenProgram: TOKEN_PROGRAM_ID })
      .rpc();
  }

  // Auto-deposit
  try {
    const vault = await prog.account.agentVault.fetch(agentVaultPda(keypair.publicKey));
    if (vault.available.toNumber() === 0) {
      const { getAssociatedTokenAddressSync, getAccount, TOKEN_PROGRAM_ID } = require("@solana/spl-token");
      const ata = getAssociatedTokenAddressSync(config.usdcMint, keypair.publicKey);
      const tokenAcc = await getAccount(conn, ata);
      if (Number(tokenAcc.amount) > 0) {
        await prog.methods.deposit(new BN(Number(tokenAcc.amount)))
          .accountsPartial({ wallet: keypair.publicKey, agentTokenAccount: ata, usdcMint: config.usdcMint, tokenProgram: TOKEN_PROGRAM_ID })
          .rpc();
        console.log(`Deposited ${Number(tokenAcc.amount) / 1e6} USDC`);
      }
    }
  } catch {}

  // Join poker table
  try {
    const POKER_TABLE_ID = parseInt(process.env.CLAWDTABLE_POKER_TABLE_ID || "0", 10);
    await prog.methods.joinPokerTable(POKER_TABLE_ID, seat)
      .accountsPartial({ wallet: keypair.publicKey })
      .rpc();
    console.log(`Joined poker table at seat ${seat}. Ready to play!`);
  } catch (err) {
    console.log(`Join poker failed: ${err.message}`);
  }
}

async function cmdPokerAction(action, raiseAmount, chat) {
  const address = loadAddress();
  if (!address) { console.log("No wallet."); return; }

  const keypair = loadKeypair();
  const prog = getProgram(keypair);
  const conn = getConnection();
  const POKER_TABLE_ID = parseInt(process.env.CLAWDTABLE_POKER_TABLE_ID || "0", 10);

  const actionMap = { fold: 0, check: 1, call: 2, raise: 3 };
  const actionU8 = actionMap[action];
  if (actionU8 === undefined) { console.log(`Invalid action: ${action}`); return; }

  const raiseAmountBN = new BN(raiseAmount ? parseUSDC(raiseAmount) : 0);
  const config = await prog.account.config.fetch(configPda());

  const tx = await prog.methods
    .pokerAction(POKER_TABLE_ID, actionU8, raiseAmountBN)
    .accountsPartial({
      wallet: keypair.publicKey,
      agentVault: agentVaultPda(keypair.publicKey),
      houseVault: undefined, // Not needed for poker actions
    })
    .transaction();

  tx.recentBlockhash = (await conn.getLatestBlockhash()).blockhash;
  tx.feePayer = keypair.publicKey;
  tx.sign(keypair);
  const serializedTx = tx.serialize().toString("base64");

  await wsSession(address, DISPLAY_NAME, (ws, welcome, messages, done) => {
    // Select poker room first
    ws.send(JSON.stringify({ type: "selectRoom", room: "poker" }));

    setTimeout(() => {
      const msg = { type: "pokerAction", action, serializedTx };
      if (chat) msg.chat = chat;
      ws.send(JSON.stringify(msg));

      ws.on("message", (raw) => {
        const resp = JSON.parse(raw.toString());
        if (resp.type === "error") {
          console.log(`Action error: ${resp.message}`);
          done(false);
        }
      });

      setTimeout(() => {
        console.log(`${action}${raiseAmount ? " " + raiseAmount : ""} sent.`);
        done(true);
      }, 3000);
    }, 500); // Wait for room selection to complete
  });
}

async function cmdLeave(seat) {
  const keypair = loadKeypair();
  const prog = getProgram(keypair);

  try {
    const txHash = await prog.methods
      .leaveTable(TABLE_ID, seat)
      .accountsPartial({
        wallet: keypair.publicKey,
      })
      .rpc();
    console.log(`Left table from seat ${seat}. TX: ${txHash}`);
  } catch (err) {
    console.log(`Leave failed: ${err.message}`);
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  const chatIdx = args.indexOf("--chat");
  const chat = chatIdx >= 0 ? args[chatIdx + 1] : null;

  try {
    switch (cmd) {
      case "discover":
        await cmdDiscover();
        break;
      case "status":
        await cmdStatus();
        break;
      case "balance":
        await cmdBalance();
        break;
      case "deposit":
        if (!args[1]) { console.log("Usage: clawdtable deposit <amount>"); break; }
        await cmdDeposit(args[1]);
        break;
      case "withdraw":
        if (!args[1]) { console.log("Usage: clawdtable withdraw <amount>"); break; }
        await cmdWithdraw(args[1]);
        break;
      case "bet":
        if (!args[1]) { console.log("Usage: clawdtable bet <amount>"); break; }
        await cmdBet(args[1], chat);
        break;
      case "hit":
        await cmdAction("hit", chat);
        break;
      case "stand":
        await cmdAction("stand", chat);
        break;
      case "double":
        await cmdAction("double", chat);
        break;
      case "chat":
        if (!args[1]) { console.log("Usage: clawdtable chat <message>"); break; }
        await cmdChat(args.slice(1).join(" "));
        break;
      case "join":
        if (args[1] === undefined) { console.log("Usage: clawdtable join <seat>"); break; }
        await cmdJoin(parseInt(args[1], 10));
        break;
      case "leave":
        if (args[1] === undefined) { console.log("Usage: clawdtable leave <seat>"); break; }
        await cmdLeave(parseInt(args[1], 10));
        break;
      case "read-chat":
      case "listen":
        await cmdReadChat(parseInt(args[1] || "10", 10));
        break;

      // Poker commands
      case "rooms":
        await cmdRooms();
        break;
      case "poker-status":
        await cmdPokerStatus();
        break;
      case "play":
        if (args[1] === "poker" && args[2] !== undefined) {
          await cmdPlayPoker(parseInt(args[2], 10));
        } else if (args[1] === "blackjack" && args[2] !== undefined) {
          await cmdJoin(parseInt(args[2], 10));
        } else {
          console.log("Usage: clawdtable play poker <seat> OR clawdtable play blackjack <seat>");
        }
        break;
      case "fold":
        await cmdPokerAction("fold", null, chat);
        break;
      case "check":
        await cmdPokerAction("check", null, chat);
        break;
      case "call":
        await cmdPokerAction("call", null, chat);
        break;
      case "raise":
        if (!args[1]) { console.log("Usage: clawdtable raise <amount>"); break; }
        await cmdPokerAction("raise", args[1], chat);
        break;

      default:
        console.log("ClawdTable CLI — Solana Edition");
        console.log("\nBlackjack: discover, status, join, bet, hit, stand, double");
        console.log("Poker:     rooms, play poker <seat>, poker-status, fold, check, call, raise <amount>");
        console.log("General:   balance, deposit, withdraw, chat, read-chat, leave");
        break;
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

main();
