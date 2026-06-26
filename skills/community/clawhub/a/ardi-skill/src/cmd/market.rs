// market — interact with the ArdiOTC peer-to-peer marketplace.
//
// Subcommands:
//   list   --token-id N --price <eth>   list one of my Ardinals for sale
//   unlist --token-id N                 cancel my own listing
//   buy    --token-id N                 buy a listed Ardinal
//   show   --token-id N                 print listing details (no tx)
//
// The marketplace is non-custodial: NFTs stay in the seller's wallet. The
// agent must `setApprovalForAll(otc, true)` once before listing — this skill
// handles the approval automatically on first list().

use anyhow::{anyhow, Context, Result};
use alloy_primitives::{Address, U256};
use alloy_sol_types::SolCall;
use serde_json::json;
use std::str::FromStr;

use crate::auth::get_address;
use crate::chain::{ArdiNFT, ArdiOTC, IERC721};
use crate::client::ApiClient;
use crate::output::{Internal, Output};
use crate::tx;
use crate::log_info;

pub enum MarketAction {
    List { token_id: u64, price_eth: f64 },
    Unlist { token_id: u64 },
    Buy { token_id: u64 },
    Show { token_id: u64 },
}

pub fn run(server_url: &str, action: MarketAction) -> Result<()> {
    let api = ApiClient::new(server_url)?;
    let cfg: serde_json::Value = api
        .get_json("/v1/chain/contracts")
        .or_else(|_| api.get_json("/v1/health"))
        .unwrap_or_default();
    let nft_addr = Address::from_str(
        &read_addr(&cfg, "ardi_nft")
            .or_else(|| std::env::var("ARDI_NFT_ADDR").ok())
            .ok_or_else(|| anyhow!("ardi_nft addr unknown; set ARDI_NFT_ADDR env"))?,
    )?;
    let otc_addr = Address::from_str(
        &read_addr(&cfg, "otc")
            .or_else(|| std::env::var("ARDI_OTC_ADDR").ok())
            .ok_or_else(|| anyhow!("otc addr unknown; set ARDI_OTC_ADDR env"))?,
    )?;

    match action {
        MarketAction::Show { token_id } => show(&otc_addr, token_id),
        MarketAction::List { token_id, price_eth } => list(&nft_addr, &otc_addr, token_id, price_eth),
        MarketAction::Unlist { token_id } => unlist(&otc_addr, token_id),
        MarketAction::Buy { token_id } => buy(&otc_addr, token_id),
    }
}

fn show(otc: &Address, token_id: u64) -> Result<()> {
    let raw = tx::view_call(otc, ArdiOTC::getListingCall { tokenId: U256::from(token_id) }.abi_encode())?;
    let l = ArdiOTC::getListingCall::abi_decode_returns(&raw, true)?._0;
    if l.seller == Address::ZERO {
        Output::success(
            format!("tokenId {token_id}: not listed."),
            json!({ "token_id": token_id, "listed": false }),
            Internal::default(),
        )
        .print();
        return Ok(());
    }
    let price_eth = (l.priceWei.to::<u128>() as f64) / 1e18;
    Output::success(
        format!(
            "tokenId {token_id}: listed by 0x{:x} for {:.6} ETH (since {})",
            l.seller, price_eth, l.listedAt
        ),
        json!({
            "token_id": token_id,
            "listed": true,
            "seller": format!("0x{:x}", l.seller),
            "price_wei": l.priceWei.to_string(),
            "price_eth": price_eth,
            "listed_at": l.listedAt as u64,
        }),
        Internal::default(),
    )
    .print();
    Ok(())
}

fn list(nft: &Address, otc: &Address, token_id: u64, price_eth: f64) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;

    if !(price_eth > 0.0) {
        return Err(anyhow!("--price must be > 0 ETH"));
    }
    let price_wei = U256::from((price_eth * 1e18) as u128);

    // Ownership check
    let owner_raw = tx::view_call(nft, ArdiNFT::ownerOfCall { tokenId: U256::from(token_id) }.abi_encode())?;
    let owner = ArdiNFT::ownerOfCall::abi_decode_returns(&owner_raw, true)?._0;
    if owner != agent {
        return Err(anyhow!(
            "tokenId {token_id} is owned by 0x{:x}, not us (0x{:x})",
            owner, agent
        ));
    }

    // Approval check — list() doesn't need approval, but buy() does (it pulls
    // via transferFrom). Better to set it now so the buyer's tx doesn't fail
    // later. setApprovalForAll(otc, true) once is enough for all future lists.
    let appr_raw = tx::view_call(
        nft,
        IERC721::isApprovedForAllCall { owner: agent, operator: *otc }.abi_encode(),
    )?;
    let approved = IERC721::isApprovedForAllCall::abi_decode_returns(&appr_raw, true)?._0;
    if !approved {
        log_info!("market: setApprovalForAll(otc, true) — one-time setup");
        let data = tx::calldata_set_approval_for_all(*otc, true);
        let tx_obj = tx::build_tx(&agent, nft, data, 0, 100_000)?;
        let approve_hash = tx::send_and_wait(&tx_obj).context("setApprovalForAll tx")?;
        log_info!("market: approval tx {approve_hash}");
    }

    let data = tx::calldata_otc_list(U256::from(token_id), price_wei);
    let tx_obj = tx::build_tx(&agent, otc, data, 0, 120_000)?;
    let tx_hash = tx::send_and_wait(&tx_obj).context("list tx")?;

    Output::success(
        format!("Listed tokenId {token_id} for {:.6} ETH (tx {tx_hash}).", price_eth),
        json!({
            "token_id": token_id,
            "price_eth": price_eth,
            "price_wei": price_wei.to_string(),
            "list_tx": tx_hash,
        }),
        Internal::default(),
    )
    .print();
    Ok(())
}

fn unlist(otc: &Address, token_id: u64) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;

    let raw = tx::view_call(otc, ArdiOTC::getListingCall { tokenId: U256::from(token_id) }.abi_encode())?;
    let l = ArdiOTC::getListingCall::abi_decode_returns(&raw, true)?._0;
    if l.seller == Address::ZERO {
        return Err(anyhow!("tokenId {token_id} is not listed"));
    }
    if l.seller != agent {
        return Err(anyhow!(
            "tokenId {token_id} listed by 0x{:x}, not us (0x{:x}); only seller can unlist",
            l.seller, agent
        ));
    }

    let data = tx::calldata_otc_unlist(U256::from(token_id));
    let tx_obj = tx::build_tx(&agent, otc, data, 0, 80_000)?;
    let tx_hash = tx::send_and_wait(&tx_obj).context("unlist tx")?;

    Output::success(
        format!("Unlisted tokenId {token_id} (tx {tx_hash})."),
        json!({ "token_id": token_id, "unlist_tx": tx_hash }),
        Internal::default(),
    )
    .print();
    Ok(())
}

fn buy(otc: &Address, token_id: u64) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;

    let raw = tx::view_call(otc, ArdiOTC::getListingCall { tokenId: U256::from(token_id) }.abi_encode())?;
    let l = ArdiOTC::getListingCall::abi_decode_returns(&raw, true)?._0;
    if l.seller == Address::ZERO {
        return Err(anyhow!("tokenId {token_id} is not listed"));
    }
    if l.seller == agent {
        return Err(anyhow!("can't buy your own listing — use unlist instead"));
    }

    let price_wei: u128 = l.priceWei.to::<u128>();
    let bal = tx::eth_balance(&agent)?;
    if bal < price_wei + 1_000_000_000_000_000 {
        return Err(anyhow!(
            "balance too low: have {:.6} ETH, need {:.6} ETH (price + ~0.001 gas)",
            (bal as f64) / 1e18,
            (price_wei as f64) / 1e18 + 0.001
        ));
    }

    let data = tx::calldata_otc_buy(U256::from(token_id));
    // buy() includes nonReentrant + safeTransferFrom + ETH refund — give
    // generous gas so we don't choke on receiver hooks.
    let tx_obj = tx::build_tx(&agent, otc, data, price_wei, 250_000)?;
    let tx_hash = tx::send_and_wait(&tx_obj).context("buy tx")?;

    Output::success(
        format!("Bought tokenId {token_id} from 0x{:x} for {:.6} ETH (tx {tx_hash}).",
            l.seller, (price_wei as f64) / 1e18),
        json!({
            "token_id": token_id,
            "seller": format!("0x{:x}", l.seller),
            "price_wei": price_wei.to_string(),
            "buy_tx": tx_hash,
        }),
        Internal::default(),
    )
    .print();
    Ok(())
}

fn read_addr(v: &serde_json::Value, key: &str) -> Option<String> {
    v.get(key)
        .or_else(|| v.get("contracts").and_then(|c| c.get(key)))
        .and_then(|x| x.as_str())
        .map(|s| s.to_string())
}
