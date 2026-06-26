// ardi-agent — CLI for AWP Ardi WorkNet.
//
// The agent's LLM drives this CLI. Each subcommand prints structured JSON
// to stdout (the LLM reads `_internal.next_command` to chain steps) and
// human progress to stderr. The skill never calls an LLM itself.

use clap::{Parser, Subcommand};

mod auth;
mod awp_register;
mod awp_rpc;
mod chain;
mod client;
mod cmd;
mod output;
mod rpc;
mod schema;
mod state;
mod tx;
mod wallet;

#[macro_export]
macro_rules! log_info {
    ($($t:tt)*) => { eprintln!("[info]  {}", format!($($t)*)) };
}
#[macro_export]
macro_rules! log_warn {
    ($($t:tt)*) => { eprintln!("[warn]  {}", format!($($t)*)) };
}
#[macro_export]
macro_rules! log_error {
    ($($t:tt)*) => { eprintln!("[error] {}", format!($($t)*)) };
}
#[macro_export]
macro_rules! log_debug {
    ($($t:tt)*) => {
        if std::env::var("ARDI_DEBUG").is_ok() {
            eprintln!("[debug] {}", format!($($t)*));
        }
    };
}

#[derive(Parser, Debug)]
#[command(
    name = "ardi-agent",
    version,
    about = "AWP Ardi WorkNet agent — solve riddles, mint Ardinal NFTs"
)]
struct Cli {
    /// Coordinator base URL.
    #[arg(long, env = "ARDI_COORDINATOR_URL", default_value = "https://api.ardinals.com")]
    server: String,

    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// 5-step env check before any chain action.
    Preflight,
    /// Show stake status + 3-path eligibility guidance.
    Stake,
    /// One-command path: ETH → AWP swap (Uniswap V3 → Aerodrome CL),
    /// then auto-lock into veAWP and allocate to your agent.
    /// Recommended for new users with ETH but no AWP. Topping up an
    /// existing balance (top-up) is the default — only buys what's
    /// missing to reach minStake.
    BuyAndStake {
        /// Lock duration in days (default 3, max 1460 = 4 years).
        #[arg(long = "lock-days")]
        lock_days: Option<u32>,
        /// Slippage in basis points (default 300 = 3%).
        #[arg(long = "slippage")]
        slippage_bps: Option<u32>,
        /// Skip the confirmation prompt (for unattended / scripted use).
        #[arg(long, short = 'y')]
        yes: bool,
        /// Print the structured plan as JSON and exit — no on-chain action.
        /// Use this from an LLM agent to relay the plan to the user, get
        /// their confirmation + lock-days choice, then re-invoke without
        /// --quote (with --yes --lock-days N) to execute.
        #[arg(long)]
        quote: bool,
        /// Buy this many AWP unconditionally (override the auto-shortfall).
        /// Useful for testing the swap independently when the wallet
        /// already meets minStake. Combine with --no-stake to swap only.
        #[arg(long = "buy-amount")]
        buy_amount: Option<u128>,
        /// Skip the lock + allocate phase. Run only the swap. Pair with
        /// --buy-amount to swap a specific amount without staking.
        #[arg(long = "no-stake")]
        no_stake: bool,
    },
    /// Show Base ETH balance + refill guidance.
    Gas,
    /// Combined view: wallet, AWP reg, ETH, coordinator, agent state.
    Status,
    /// Fetch the current commit-able epoch and its riddles. The LLM solves
    /// them then calls `commit` for each.
    Context,
    /// Submit one commit. Skill stores (salt, answer) locally for reveal.
    Commit {
        /// Epoch id; defaults to current.
        #[arg(long)]
        epoch: Option<u64>,
        #[arg(long)]
        word_id: u64,
        #[arg(long)]
        answer: String,
        /// v3.1: explicit staker addresses for AWP eligibility (repeatable,
        /// max 8). When omitted, the skill auto-detects via AWP RPC.
        #[arg(long = "staker", num_args = 0..)]
        staker: Vec<String>,
    },
    /// List local pending commits and the next action for each.
    Commits,
    /// Reveal a previously committed (epoch, wordId).
    Reveal {
        #[arg(long)]
        epoch: u64,
        #[arg(long)]
        word_id: u64,
    },
    /// Check on-chain winner; if it's us, mint the Ardinal NFT.
    Inscribe {
        #[arg(long)]
        epoch: u64,
        #[arg(long)]
        word_id: u64,
    },
    /// v3: refresh an NFT's durability. Pays $ardi fee + requests VRF.
    /// 1% chance of failure → NFT becomes broken (must fuse to revive).
    Repair {
        #[arg(long)]
        token_id: u64,
    },
    /// v3.2: claim accumulated $ardi rewards from EmissionDistributor.
    /// Pass --token-id repeatedly to claim from specific NFTs; OR pass
    /// no flags at all to auto-fetch every NFT this agent owns from the
    /// coordinator and claim across all of them in one tx.
    Claim {
        #[arg(long = "token-id")]
        token_ids: Vec<u64>,
    },
    /// v3.2: report claimable $ardi without sending any tx. Auto-fetches
    /// the agent's owned NFTs from the coordinator. Use this BEFORE
    /// `claim` to confirm with the operator how much they're about to
    /// receive (pending = sum across NFTs).
    Pending {},
    /// v3: transfer an Ardinal NFT from the agent's wallet to another
    /// address (typically the user's MetaMask / main wallet) so the new
    /// owner can repair / claim from the browser. Reverts up-front if a
    /// repair or fuse VRF request is in flight against the token.
    Transfer {
        #[arg(long = "token-id")]
        token_id: u64,
        /// Target address (0x…40-hex). Usually the user's main wallet.
        #[arg(long)]
        to: String,
    },
    /// Peer-to-peer marketplace (ArdiOTC). Subcommands list / unlist / buy / show.
    Market {
        #[command(subcommand)]
        action: MarketCmd,
    },
    /// Install (or refresh) the unattended mining daemon. Use this instead
    /// of writing your own shell/cron loop — the built-in installer wires
    /// up a systemd user unit that drives commit → reveal → inscribe each
    /// epoch with the correct serial-nonce ordering. On hosts without
    /// systemd (Docker / containers / macOS) the installer still sets up
    /// the runtime files and points you at `ardi-agent loop` for the
    /// foreground equivalent.
    AutoMine,
    /// Foreground unattended-mining daemon — the no-systemd fallback for
    /// `auto-mine`. Spawns one tick at a time (serial, never parallel) and
    /// blocks until killed. Use this in Docker / Kubernetes / macOS or
    /// any host without systemd. Run it under nohup / tmux / screen if
    /// you want to detach.
    #[command(name = "loop")]
    Loop {
        /// Seconds between ticks. Default 90 (matches the systemd timer
        /// cadence). Clamped to a minimum of 30 to avoid hammering the
        /// coordinator and the LLM runtime.
        #[arg(long, default_value_t = 90)]
        interval: u64,
        /// Run a single tick and exit (useful for cron / external timers).
        #[arg(long)]
        once: bool,
    },
}

#[derive(Subcommand, Debug)]
enum MarketCmd {
    /// List one of your Ardinals for sale at fixed ETH price.
    List {
        #[arg(long = "token-id")] token_id: u64,
        /// Price in ETH (decimal). Min 0.000001.
        #[arg(long)] price: f64,
    },
    /// Cancel one of your active listings.
    Unlist {
        #[arg(long = "token-id")] token_id: u64,
    },
    /// Buy a listed Ardinal — pays full price, contract refunds excess.
    Buy {
        #[arg(long = "token-id")] token_id: u64,
    },
    /// Show listing details for a tokenId (read-only, no tx).
    Show {
        #[arg(long = "token-id")] token_id: u64,
    },
}

fn main() {
    let cli = Cli::parse();
    let result = match cli.cmd {
        Cmd::Preflight => cmd::preflight::run(&cli.server),
        Cmd::Stake => cmd::stake::run(&cli.server),
        Cmd::BuyAndStake { lock_days, slippage_bps, yes, quote, buy_amount, no_stake } =>
            cmd::buy_and_stake::run(
                &cli.server,
                cmd::buy_and_stake::BuyAndStakeArgs {
                    lock_days,
                    slippage_bps,
                    yes,
                    quote_only: quote,
                    buy_amount_awp: buy_amount,
                    no_stake,
                },
            ),
        Cmd::Gas => cmd::gas::run(&cli.server),
        Cmd::Status => cmd::status::run(&cli.server),
        Cmd::Context => cmd::context::run(&cli.server),
        Cmd::Commit { epoch, word_id, answer, staker } => {
            let stakers = if staker.is_empty() {
                None
            } else {
                let mut v = Vec::with_capacity(staker.len());
                for s in &staker {
                    match alloy_primitives::Address::parse_checksummed(s, None)
                        .or_else(|_| s.parse::<alloy_primitives::Address>())
                    {
                        Ok(a) => v.push(a),
                        Err(_) => {
                            log_error!("--staker is not a valid 0x-address: {s}");
                            std::process::exit(2);
                        }
                    }
                }
                Some(v)
            };
            cmd::commit::run(
                &cli.server,
                cmd::commit::CommitArgs { epoch_id: epoch, word_id, answer, stakers },
            )
        }
        Cmd::Commits => cmd::commits::run(&cli.server),
        Cmd::Reveal { epoch, word_id } => cmd::reveal::run(&cli.server, epoch, word_id),
        Cmd::Inscribe { epoch, word_id } => cmd::inscribe::run(&cli.server, epoch, word_id),
        Cmd::Repair { token_id } => cmd::repair::run(&cli.server, token_id),
        Cmd::Claim { token_ids } => cmd::claim::run(&cli.server, token_ids),
        Cmd::Pending {} => cmd::pending::run(&cli.server),
        Cmd::Transfer { token_id, to } => cmd::transfer::run(&cli.server, token_id, to),
        Cmd::Market { action } => {
            let act = match action {
                MarketCmd::List { token_id, price } => cmd::market::MarketAction::List { token_id, price_eth: price },
                MarketCmd::Unlist { token_id } => cmd::market::MarketAction::Unlist { token_id },
                MarketCmd::Buy { token_id } => cmd::market::MarketAction::Buy { token_id },
                MarketCmd::Show { token_id } => cmd::market::MarketAction::Show { token_id },
            };
            cmd::market::run(&cli.server, act)
        }
        Cmd::AutoMine => cmd::auto_mine::run(),
        Cmd::Loop { interval, once } => cmd::run_loop::run(cmd::run_loop::LoopArgs {
            interval_sec: Some(interval),
            once,
        }),
    };
    if let Err(e) = result {
        log_error!("fatal: {e:#}");
        std::process::exit(1);
    }
}
