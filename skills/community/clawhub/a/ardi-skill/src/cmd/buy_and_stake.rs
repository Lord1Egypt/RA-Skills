// buy-and-stake — one-command path for new users:
//   1) (optional) ETH → USDC → AWP swap to top up to minStake
//   2) approve AWP, deposit into veAWP for N days
//   3) allocate locked stake to the agent on Ardi worknet
//
// Routes:
//   ETH → USDC : Uniswap V3 SwapRouter02 (deepest ETH/USDC liquidity on Base)
//   USDC → AWP : Aerodrome Slipstream CL pool (where AWP liquidity lives)
//
// Failure model: NOT atomic. If step (a) ETH→USDC succeeds and step (b)
// USDC→AWP fails, the user keeps the USDC — they can retry later. We
// detect partial state on each invocation and skip steps that already
// completed, so re-running the command is idempotent and self-healing.

use anyhow::{anyhow, Context, Result};
use alloy_primitives::{Address, U256};
use alloy_sol_types::SolCall;
use serde_json::json;
use std::io::{self, BufRead, Write};
use std::str::FromStr;

use crate::auth::get_address;
use crate::chain::{
    AWPAllocatorWrite, AeroCLPool, AeroCLQuoter, AeroCLSwapRouter, IERC20, UniV3QuoterV2,
    UniV3SwapRouter02, VeAWP,
};
use crate::output::{Internal, Output};
use crate::{log_info, tx, wallet};

// ─── Base mainnet contract addresses ────────────────────────────────
const WETH: &str = "0x4200000000000000000000000000000000000006";
const USDC: &str = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const AWP: &str = "0x0000A1050AcF9DEA8af9c2E74f0D7CF43f1000A1";
const VE_AWP: &str = "0x0000b534C63D78212f1BDCc315165852793A00A8";
const AWP_ALLOCATOR: &str = "0x0000D6BB5e040E35081b3AaF59DD71b21C9800AA";

// Uniswap V3 on Base — SwapRouter02 + QuoterV2
const UNI_V3_ROUTER: &str = "0x2626664c2603336E57B271c5C0b26F421741e481";
const UNI_V3_QUOTER: &str = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a";
const UNI_V3_ETH_USDC_FEE: u32 = 500; // 0.05% pool — deepest

// Aerodrome Slipstream CL — addresses verified against awp-community-web.
const AERO_CL_ROUTER: &str = "0xcbBb8035cAc7D4B3Ca7aBb74cF7BdF900215Ce0D";
const AERO_CL_QUOTER: &str = "0x3d4C22254F86f64B7eC90ab8F7aeC1FBFD271c6C";
const AERO_USDC_AWP_POOL: &str = "0x1d561b036d84a24c2bf38898a65bb65e5353f6c4";

const ARDI_WORKNET_ID: u64 = 845300000014;

const ONE_AWP_WEI: u128 = 1_000_000_000_000_000_000;
const ONE_USDC_UNIT: u128 = 1_000_000;       // 6 decimals
const ONE_ETH_WEI: u128 = 1_000_000_000_000_000_000;

const DEFAULT_MIN_STAKE_AWP: u128 = 10_000;
const DEFAULT_SLIPPAGE_BPS: u32 = 300;       // 3.00%
const DEFAULT_LOCK_DAYS: u32 = 3;
const SWAP_DEADLINE_SEC: u64 = 600;
const ETH_GAS_BUFFER_WEI: u128 = 1_500_000_000_000_000; // 0.0015 ETH for gas headroom

#[derive(Debug)]
pub struct BuyAndStakeArgs {
    pub lock_days: Option<u32>,
    pub slippage_bps: Option<u32>,
    pub yes: bool,        // skip confirmation prompt (use defaults)
    pub quote_only: bool, // dry-quote, no tx, structured JSON for the LLM
    /// Override the auto-computed shortfall — buy this many AWP unconditionally.
    /// Useful for testing the swap path independently when wallet already has
    /// enough AWP, or for buying extra to allocate to MULTIPLE agents.
    pub buy_amount_awp: Option<u128>,
    /// Skip the staking phase entirely. With `--buy-amount`, this turns
    /// the command into a pure swap (no lock, no allocate).
    pub no_stake: bool,
}

pub fn run(_server_url: &str, args: BuyAndStakeArgs) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;
    let slip_bps = args.slippage_bps.unwrap_or(DEFAULT_SLIPPAGE_BPS).min(2000);

    // ── 1. Determine how much AWP we still need ──────────────────────
    let min_stake_wei = read_min_stake_wei().unwrap_or(U256::from(DEFAULT_MIN_STAKE_AWP) * U256::from(ONE_AWP_WEI));
    let min_stake_awp = (min_stake_wei.to::<u128>() as f64) / (ONE_AWP_WEI as f64);
    let awp_balance_wei = read_erc20_balance(AWP, &agent)?;
    let awp_balance_awp = wei_to_awp_f(awp_balance_wei);

    log_info!(
        "buy-and-stake: agent={agent_str} balance_awp={awp_balance_awp:.4} \
         threshold_awp={min_stake_awp:.0} slippage_bps={slip_bps}"
    );

    // Determine purchase amount.
    // Default: shortfall to minStake (compete buy-and-stake intent).
    // Override: --buy-amount X forces an unconditional buy of X AWP.
    let need_wei = match args.buy_amount_awp {
        Some(awp) => U256::from(awp) * U256::from(ONE_AWP_WEI),
        None if awp_balance_wei >= min_stake_wei => U256::ZERO,
        None => min_stake_wei - awp_balance_wei,
    };
    let need_awp = wei_to_awp_f(need_wei);

    // ── 2a. Quote-only mode: structured JSON for the LLM, no tx ─────
    // The LLM should call this first, relay the plan to the user, get
    // their lock-days choice + confirmation, then re-invoke with
    // `--yes --lock-days N` to actually execute. Without this two-step
    // pattern the LLM has no way to insert a human-in-the-loop on a
    // non-interactive stdin.
    if args.quote_only {
        let quote = quote_only(&agent, need_wei, awp_balance_wei, min_stake_wei, slip_bps)?;
        Output::success(
            format!("Quote ready — relay to user, confirm, then re-run with `--yes --lock-days N`"),
            quote,
            Internal {
                next_action: "await_user_confirmation".into(),
                next_command: Some(format!(
                    "ardi-agent buy-and-stake --yes --lock-days <USER_CHOICE>"
                )),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    // ── 2. If we need to buy AWP, run the swap ──────────────────────
    if need_wei > U256::ZERO {
        do_buy(&agent, need_wei, need_awp, slip_bps, args.yes)?;
        // Re-read AWP balance to confirm the swap landed.
        let after = read_erc20_balance(AWP, &agent)?;
        if after < min_stake_wei {
            return Err(anyhow!(
                "post-swap AWP balance {} < required {} — swap reverted or partial. \
                 Re-run buy-and-stake to retry only the missing piece.",
                wei_to_awp_f(after),
                min_stake_awp
            ));
        }
        println!("✓ AWP balance now {} (target {})", wei_to_awp_f(after), min_stake_awp);
    } else {
        println!("✓ AWP balance already meets threshold ({:.4} >= {:.0}) — skipping swap",
            awp_balance_awp, min_stake_awp);
    }

    // ── 2c. Skip stake phase (--no-stake, swap-only mode) ────────────
    if args.no_stake {
        Output::success(
            format!("✓ swap done ({} AWP); --no-stake set, skipping lock + allocate", min_stake_awp),
            json!({
                "agent": agent_str,
                "buy_amount_awp": args.buy_amount_awp.unwrap_or(0),
                "no_stake": true,
            }),
            Internal {
                next_action: "manual_stake_or_done".into(),
                next_command: Some("ardi-agent stake".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    // ── 3. Lock duration prompt ──────────────────────────────────────
    let lock_days = match args.lock_days {
        Some(d) => d,
        None if args.yes => DEFAULT_LOCK_DAYS,
        None => prompt_lock_days()?,
    };
    if lock_days == 0 {
        return Err(anyhow!("lock-days must be >= 1"));
    }
    let lock_seconds = (lock_days as u64) * 86_400;
    println!("→ locking {} AWP for {} day(s) ({}s)", min_stake_awp, lock_days, lock_seconds);

    // ── 4. Stake: approve → deposit → allocate ──────────────────────
    do_stake(&agent, min_stake_wei, lock_seconds)?;

    // ── 5. Done ─────────────────────────────────────────────────────
    Output::success(
        format!("✓ {} AWP locked + allocated to agent on Ardi worknet. Eligible to commit.", min_stake_awp),
        json!({
            "agent": agent_str,
            "stake_awp": min_stake_awp,
            "lock_days": lock_days,
            "worknet_id": ARDI_WORKNET_ID,
        }),
        Internal {
            next_action: "commit_now".into(),
            next_command: Some("ardi-agent context".into()),
            ..Default::default()
        },
    )
    .print();
    Ok(())
}

// ============================================================================
// SWAP PHASE
// ============================================================================

fn do_buy(agent: &Address, need_awp_wei: U256, need_awp: f64, slip_bps: u32, skip_prompt: bool)
    -> Result<()>
{
    println!("\n📊 Quote (live, on-chain — no API key)");
    println!("   target AWP needed: {:.4}", need_awp);

    // Step A — quote how much USDC we need to receive `need_awp_wei` AWP.
    // We do exactInputSingle quotes in the OUTPUT direction by iterating
    // (since quoteExactOutput on AeroCL is rare). Cheap workaround: probe
    // a guess of USDC and scale the result. For 10K AWP at ~$0.01-0.50/AWP
    // a starting guess of 100 USDC is fine; we then pro-rate.
    let probe_usdc = U256::from(100u128 * ONE_USDC_UNIT);
    let probe_awp = quote_usdc_to_awp(probe_usdc)
        .context("quote usdc→awp probe")?;
    if probe_awp.is_zero() {
        return Err(anyhow!("Aerodrome quoter returned 0 AWP for 100 USDC probe — pool may be drained"));
    }
    // Linear extrapolation: usdc_needed = probe_usdc * need_awp_wei / probe_awp
    // (Slippage handled below; we add a 5% buffer here so the swap doesn't
    //  underbuy due to slight non-linearity at higher amounts.)
    let usdc_needed = probe_usdc
        .checked_mul(need_awp_wei).ok_or_else(|| anyhow!("usdc*need overflow"))?
        / probe_awp;
    let usdc_with_buffer = usdc_needed * U256::from(105u32) / U256::from(100u32);

    // Step B — quote how much ETH we need to get usdc_with_buffer USDC.
    let eth_needed = quote_eth_for_usdc_out(usdc_with_buffer)
        .context("quote eth→usdc")?;

    // Min outputs (slippage-adjusted)
    let usdc_min = apply_slippage(usdc_needed, slip_bps);
    let awp_min = apply_slippage(need_awp_wei, slip_bps);

    // Display
    let eth_needed_eth = wei_to_eth_f(eth_needed);
    let total_with_gas = eth_needed.saturating_add(U256::from(ETH_GAS_BUFFER_WEI));
    println!("   spend ETH         : {:.6} (~{:.2} USD if $4000/ETH)", eth_needed_eth, eth_needed_eth * 4000.0);
    println!("   buffer (gas)      : {:.6} ETH", wei_to_eth_f(U256::from(ETH_GAS_BUFFER_WEI)));
    println!("   total burn        : {:.6} ETH (recommended top-up: 0.01 ETH)", wei_to_eth_f(total_with_gas));
    println!("   slippage          : {:.2}% (--slippage to override)", slip_bps as f64 / 100.0);
    println!("   route             : ETH → USDC (Uni V3 0.05%) → AWP (Aerodrome CL)");

    // ETH balance check
    let eth_bal_u128 = tx::eth_balance(agent)?;
    let eth_bal = U256::from(eth_bal_u128);
    println!("   wallet ETH balance: {:.6}", wei_to_eth_f(eth_bal));
    if eth_bal < total_with_gas {
        return Err(anyhow!(
            "ETH balance {:.6} < required {:.6}. Top up your wallet ({}) on Base mainnet.",
            wei_to_eth_f(eth_bal),
            wei_to_eth_f(total_with_gas),
            format!("0x{:x}", agent),
        ));
    }

    // Confirm
    if !skip_prompt {
        print!("\nProceed with buy? [y/N]: ");
        io::stdout().flush().ok();
        let mut line = String::new();
        io::stdin().lock().read_line(&mut line)?;
        if !matches!(line.trim().to_lowercase().as_str(), "y" | "yes") {
            return Err(anyhow!("aborted by user"));
        }
    }

    // Execute swap A: ETH → USDC
    println!("\n→ swap ETH → USDC ({} on Uniswap V3 0.05%)", wei_to_eth_f(eth_needed));
    let tx1 = build_eth_to_usdc_tx(agent, eth_needed, usdc_min)?;
    let h1 = wallet::send_tx(&tx1).context("ETH→USDC swap tx")?;
    println!("   tx: {h1}");
    // Brief wait then verify USDC arrived
    let usdc_after = read_erc20_balance(USDC, agent)?;
    if usdc_after < usdc_min {
        return Err(anyhow!(
            "ETH→USDC swap landed but USDC balance {:.4} < expected min {:.4} — slippage or RPC stale",
            (usdc_after.to::<u128>() as f64) / (ONE_USDC_UNIT as f64),
            (usdc_min.to::<u128>() as f64) / (ONE_USDC_UNIT as f64),
        ));
    }
    let usdc_for_aero = usdc_after.min(usdc_with_buffer);
    println!("   ✓ have {:.4} USDC; using {:.4} for AWP swap",
        (usdc_after.to::<u128>() as f64) / (ONE_USDC_UNIT as f64),
        (usdc_for_aero.to::<u128>() as f64) / (ONE_USDC_UNIT as f64));

    // Approve USDC → Aerodrome router (one-time per wallet, idempotent if already max)
    let allowance = read_erc20_allowance(USDC, agent, AERO_CL_ROUTER)?;
    if allowance < usdc_for_aero {
        println!("→ approve USDC → Aerodrome CL router");
        let approve_tx = build_approve_tx(agent, USDC, AERO_CL_ROUTER, U256::MAX)?;
        let h = wallet::send_tx(&approve_tx).context("USDC approve")?;
        println!("   tx: {h}");
    } else {
        println!("   ✓ USDC already approved to Aerodrome router");
    }

    // Execute swap B: USDC → AWP
    println!("→ swap USDC → AWP (Aerodrome Slipstream)");
    let tx2 = build_usdc_to_awp_tx(agent, usdc_for_aero, awp_min)?;
    let h2 = wallet::send_tx(&tx2).context("USDC→AWP swap tx")?;
    println!("   tx: {h2}");
    Ok(())
}

// ============================================================================
// STAKE PHASE
// ============================================================================

fn do_stake(agent: &Address, amount_wei: U256, lock_seconds: u64) -> Result<()> {
    // 1. AWP.approve(veAWP, amount)
    let allowance = read_erc20_allowance(AWP, agent, VE_AWP)?;
    if allowance < amount_wei {
        println!("→ approve AWP → veAWP");
        let tx = build_approve_tx(agent, AWP, VE_AWP, U256::MAX)?;
        let h = wallet::send_tx(&tx).context("AWP approve to veAWP")?;
        println!("   tx: {h}");
    }

    // 2. veAWP.deposit(amount, lockSeconds)
    println!("→ veAWP.deposit({:.0} AWP, {}d lock)",
        wei_to_awp_f(amount_wei), lock_seconds / 86400);
    let dep_call = VeAWP::depositCall {
        amount: amount_wei,
        lockSeconds: lock_seconds,
    };
    let tx_dep = tx::build_tx(
        agent,
        &Address::from_str(VE_AWP)?,
        dep_call.abi_encode(),
        0,
        500_000,
    )?;
    let h_dep = wallet::send_tx(&tx_dep).context("veAWP deposit")?;
    println!("   tx: {h_dep}");

    // 3. AWPAllocator.allocate(staker=self, agent=self, worknet=ARDI, amount)
    println!("→ AWPAllocator.allocate(self, self, ARDI worknet, {:.0} AWP)",
        wei_to_awp_f(amount_wei));
    let alloc_call = AWPAllocatorWrite::allocateCall {
        staker: *agent,
        agent: *agent,
        worknetId: U256::from(ARDI_WORKNET_ID),
        amount: amount_wei,
    };
    let tx_alloc = tx::build_tx(
        agent,
        &Address::from_str(AWP_ALLOCATOR)?,
        alloc_call.abi_encode(),
        0,
        300_000,
    )?;
    let h_alloc = wallet::send_tx(&tx_alloc).context("AWPAllocator allocate")?;
    println!("   tx: {h_alloc}");
    Ok(())
}

// ============================================================================
// helpers
// ============================================================================

/// Read-only plan: fills `data` field with everything the LLM needs to
/// narrate the trade to the user without executing anything.
fn quote_only(
    agent: &Address,
    need_wei: U256,
    have_wei: U256,
    threshold_wei: U256,
    slip_bps: u32,
) -> Result<serde_json::Value> {
    let need_awp = wei_to_awp_f(need_wei);
    let have_awp = wei_to_awp_f(have_wei);
    let threshold_awp = wei_to_awp_f(threshold_wei);

    let (eth_needed, usdc_min, awp_min, total_with_gas) = if need_wei.is_zero() {
        (U256::ZERO, U256::ZERO, U256::ZERO, U256::ZERO)
    } else {
        let probe_usdc = U256::from(100u128 * ONE_USDC_UNIT);
        let probe_awp = quote_usdc_to_awp(probe_usdc)?;
        let usdc_needed = probe_usdc.checked_mul(need_wei).ok_or_else(|| anyhow!("overflow"))?
            / probe_awp;
        let usdc_with_buffer = usdc_needed * U256::from(105u32) / U256::from(100u32);
        let eth_needed = quote_eth_for_usdc_out(usdc_with_buffer)?;
        let usdc_min = apply_slippage(usdc_needed, slip_bps);
        let awp_min = apply_slippage(need_wei, slip_bps);
        let total_with_gas = eth_needed.saturating_add(U256::from(ETH_GAS_BUFFER_WEI));
        (eth_needed, usdc_min, awp_min, total_with_gas)
    };

    let eth_bal = U256::from(tx::eth_balance(agent)?);
    let eth_sufficient = eth_bal >= total_with_gas;

    Ok(json!({
        "agent_address": format!("0x{:x}", agent),
        "current_awp": have_awp,
        "threshold_awp": threshold_awp,
        "needed_awp": need_awp,
        "needs_swap": !need_wei.is_zero(),
        "swap": if need_wei.is_zero() { json!(null) } else { json!({
            "spend_eth": wei_to_eth_f(eth_needed),
            "buffer_eth_for_gas": wei_to_eth_f(U256::from(ETH_GAS_BUFFER_WEI)),
            "total_burn_eth": wei_to_eth_f(total_with_gas),
            "slippage_bps": slip_bps,
            "min_usdc_received": (usdc_min.to::<u128>() as f64) / (ONE_USDC_UNIT as f64),
            "min_awp_received": wei_to_awp_f(awp_min),
            "route": "ETH → USDC (Uniswap V3 0.05%) → AWP (Aerodrome CL)",
            "wallet_eth_balance": wei_to_eth_f(eth_bal),
            "eth_sufficient": eth_sufficient,
        }) },
        "stake_options": {
            "default_lock_days": DEFAULT_LOCK_DAYS,
            "min_lock_days": 1,
            "max_lock_days": 1460,
            "note": "Locked AWP cannot be withdrawn until expiry. Default 3 days keeps you flexible; longer locks are NOT required for Ardi eligibility.",
        },
        "next_step": format!(
            "Confirm with user, then run: ardi-agent buy-and-stake --yes --lock-days <N>{}",
            if slip_bps != DEFAULT_SLIPPAGE_BPS { format!(" --slippage {slip_bps}") } else { String::new() }
        ),
    }))
}

fn quote_usdc_to_awp(usdc_in: U256) -> Result<U256> {
    let pool = Address::from_str(AERO_USDC_AWP_POOL)?;
    let ts_call = AeroCLPool::tickSpacingCall {};
    let raw_ts = tx::view_call(&pool, ts_call.abi_encode())?;
    let ts = AeroCLPool::tickSpacingCall::abi_decode_returns(&raw_ts, true)?._0;

    let quoter = Address::from_str(AERO_CL_QUOTER)?;
    let q_call = AeroCLQuoter::quoteExactInputSingleCall {
        params: AeroCLQuoter::QuoteExactInputSingleParams {
            tokenIn: Address::from_str(USDC)?,
            tokenOut: Address::from_str(AWP)?,
            amountIn: usdc_in,
            tickSpacing: ts,
            sqrtPriceLimitX96: alloy_primitives::aliases::U160::ZERO,
        },
    };
    let raw = tx::view_call(&quoter, q_call.abi_encode())?;
    let dec = AeroCLQuoter::quoteExactInputSingleCall::abi_decode_returns(&raw, true)?;
    Ok(dec.amountOut)
}

fn quote_eth_for_usdc_out(usdc_target: U256) -> Result<U256> {
    // Probe approach: quote 0.001 ETH → USDC, then linear extrapolate.
    let probe_eth = U256::from(1_000_000_000_000_000u128); // 0.001 ETH
    let quoter = Address::from_str(UNI_V3_QUOTER)?;
    let q_call = UniV3QuoterV2::quoteExactInputSingleCall {
        params: UniV3QuoterV2::QuoteExactInputSingleParams {
            tokenIn: Address::from_str(WETH)?,
            tokenOut: Address::from_str(USDC)?,
            amountIn: probe_eth,
            fee: alloy_primitives::aliases::U24::from(UNI_V3_ETH_USDC_FEE),
            sqrtPriceLimitX96: alloy_primitives::aliases::U160::ZERO,
        },
    };
    let raw = tx::view_call(&quoter, q_call.abi_encode())?;
    let dec = UniV3QuoterV2::quoteExactInputSingleCall::abi_decode_returns(&raw, true)?;
    let usdc_per_probe = dec.amountOut;
    if usdc_per_probe.is_zero() {
        return Err(anyhow!("Uni V3 quoter returned 0 USDC for 0.001 ETH"));
    }
    // eth_needed = probe_eth * usdc_target / usdc_per_probe
    Ok(probe_eth
        .checked_mul(usdc_target).ok_or_else(|| anyhow!("eth*usdc overflow"))?
        / usdc_per_probe)
}

fn build_eth_to_usdc_tx(from: &Address, eth_in: U256, usdc_min: U256) -> Result<serde_json::Value> {
    let call = UniV3SwapRouter02::exactInputSingleCall {
        params: UniV3SwapRouter02::ExactInputSingleParams {
            tokenIn: Address::from_str(WETH)?,
            tokenOut: Address::from_str(USDC)?,
            fee: alloy_primitives::aliases::U24::from(UNI_V3_ETH_USDC_FEE),
            recipient: *from,
            amountIn: eth_in,
            amountOutMinimum: usdc_min,
            sqrtPriceLimitX96: alloy_primitives::aliases::U160::ZERO,
        },
    };
    tx::build_tx(
        from,
        &Address::from_str(UNI_V3_ROUTER)?,
        call.abi_encode(),
        eth_in.to::<u128>(),
        300_000,
    )
}

fn build_usdc_to_awp_tx(from: &Address, usdc_in: U256, awp_min: U256) -> Result<serde_json::Value> {
    let pool = Address::from_str(AERO_USDC_AWP_POOL)?;
    let ts_call = AeroCLPool::tickSpacingCall {};
    let raw_ts = tx::view_call(&pool, ts_call.abi_encode())?;
    let ts = AeroCLPool::tickSpacingCall::abi_decode_returns(&raw_ts, true)?._0;

    let deadline = chrono::Utc::now().timestamp() as u64 + SWAP_DEADLINE_SEC;
    let call = AeroCLSwapRouter::exactInputSingleCall {
        params: AeroCLSwapRouter::ExactInputSingleParams {
            tokenIn: Address::from_str(USDC)?,
            tokenOut: Address::from_str(AWP)?,
            tickSpacing: ts,
            recipient: *from,
            deadline: U256::from(deadline),
            amountIn: usdc_in,
            amountOutMinimum: awp_min,
            sqrtPriceLimitX96: alloy_primitives::aliases::U160::ZERO,
        },
    };
    tx::build_tx(
        from,
        &Address::from_str(AERO_CL_ROUTER)?,
        call.abi_encode(),
        0,
        500_000,
    )
}

fn build_approve_tx(from: &Address, token: &str, spender: &str, amount: U256) -> Result<serde_json::Value> {
    let call = IERC20::approveCall {
        spender: Address::from_str(spender)?,
        amount,
    };
    tx::build_tx(from, &Address::from_str(token)?, call.abi_encode(), 0, 100_000)
}

fn read_erc20_balance(token: &str, owner: &Address) -> Result<U256> {
    let call = IERC20::balanceOfCall { account: *owner };
    let raw = tx::view_call(&Address::from_str(token)?, call.abi_encode())?;
    Ok(IERC20::balanceOfCall::abi_decode_returns(&raw, true)?._0)
}

fn read_erc20_allowance(token: &str, owner: &Address, spender: &str) -> Result<U256> {
    let call = IERC20::allowanceCall {
        owner: *owner,
        spender: Address::from_str(spender)?,
    };
    let raw = tx::view_call(&Address::from_str(token)?, call.abi_encode())?;
    Ok(IERC20::allowanceCall::abi_decode_returns(&raw, true)?._0)
}

fn read_min_stake_wei() -> Result<U256> {
    use crate::chain::ArdiEpochDraw;
    const EPOCH_DRAW: &str = "0xA57d8E6646E063FFd6eae579d4f327b689dA5DC3";
    let addr = Address::from_str(EPOCH_DRAW)?;
    let call = ArdiEpochDraw::minStakeCall {};
    let raw = tx::view_call(&addr, call.abi_encode())?;
    Ok(ArdiEpochDraw::minStakeCall::abi_decode_returns(&raw, true)?._0)
}

fn apply_slippage(amount: U256, bps: u32) -> U256 {
    // amount * (10000 - bps) / 10000
    amount * U256::from(10000u32 - bps) / U256::from(10000u32)
}

fn wei_to_awp_f(w: U256) -> f64 {
    let lo = w.to::<u128>();
    (lo as f64) / (ONE_AWP_WEI as f64)
}
fn wei_to_eth_f(w: U256) -> f64 {
    let lo = w.to::<u128>();
    (lo as f64) / (ONE_ETH_WEI as f64)
}

fn prompt_lock_days() -> Result<u32> {
    print!("Lock duration in days (default {DEFAULT_LOCK_DAYS}, max 1460=4yr): ");
    io::stdout().flush().ok();
    let mut s = String::new();
    io::stdin().lock().read_line(&mut s)?;
    let s = s.trim();
    if s.is_empty() {
        return Ok(DEFAULT_LOCK_DAYS);
    }
    s.parse::<u32>().map_err(|e| anyhow!("invalid lock-days: {e}"))
}
