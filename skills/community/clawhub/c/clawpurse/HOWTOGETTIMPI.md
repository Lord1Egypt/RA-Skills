# How to Acquire TIMPI / NTMPI

ClawPurse runs on the Neutaro chain, so you can fund it with TIMPI (a.k.a. NTMPI) using either a centralized exchange (MEXC) or a fully non-custodial Gravity Bridge → Osmosis flow. Pick the path that matches your current assets.

---

## Option 1 — Buy NTMPI on MEXC

1. **Create / log in to MEXC.** Complete KYC if prompted and enable 2FA.
2. **Deposit USDT.** TRC-20 or BEP-20 transfers settle quickly and have low network fees.
3. **Open the NTMPI/USDT spot pair.** Direct link: <https://www.mexc.com/exchange/NTMPI_USDT>. The quote page currently shows full depth, 24h stats, and quick chart access.
4. **Place a trade.**
   - *Market order* if you just want the fastest fill.
   - *Limit order* if you want to name your entry price.
5. **Withdraw to self-custody.**
   - Destination: your Neutaro/ClawPurse address (starts with `neutaro1...`).
   - Memo: optional, but include one if your downstream workflow expects it.
6. **Import into ClawPurse.** Run `clawpurse sync` or `clawpurse balance` to confirm the deposit landed.

> ⚠️ Always verify you are on the real MEXC domain and that the withdrawal network is Neutaro (not ERC-20). When in doubt, send a tiny test transaction first.

---

## Option 2 — Gravity Bridge ➜ Osmosis ➜ NTMPI

Perfect when you already hold ETH, USDC, or USDT on Ethereum and want a purely non-custodial path.

1. **Prepare wallets.**
   - MetaMask (or another Ethereum wallet) funded with the ERC-20 you plan to bridge plus ETH for gas.
   - Keplr or Leap wallet with Gravity Bridge + Osmosis accounts enabled.
2. **Bridge stablecoins with Gravity Bridge.**
   - Open an approved frontend such as <https://gravitypulse.app/> or <https://bridge.blockscape.network/#/>.
   - Connect MetaMask (Ethereum) and Keplr/Leap (Gravity Bridge chain).
   - Approve the ERC-20 allowance, then submit the bridge transaction. Relayers will mint the Cosmos-side representation after a few confirmations.
3. **IBC-hop to Osmosis.**
   - In Keplr: Assets → Gravity Bridge → Transfer → select Osmosis.
   - Send the bridged USDC/USDT across IBC. The token will now appear in your Osmosis balances.
4. **Swap for TIMPI/NTMPI on Osmosis.**
   - Use the Osmosis app to trade your stablecoin for NTMPI (search for “NTMPI” in the asset list).
   - Confirm the swap and wait for the transaction to finalize.
5. **Send NTMPI to Neutaro.**
   - From Osmosis, initiate an IBC transfer to the Neutaro chain (`neutaro-1`).
   - Paste your ClawPurse address as the destination.
6. **Load ClawPurse.**
   - Once the IBC packet clears, run `clawpurse balance` or `clawpurse receipts` to confirm funds.

> ✅ Bonus: after your first Gravity transfer, future top-ups are faster—Keplr remembers the IBC channels, and relayers prioritize profitable batches automatically.

---

### Need another venue?
Timpi’s official exchange list (MEXC, Uniswap, Osmosis, BitMart) lives here: <https://timpi.gitbook.io/timpis-knowledge-base/timpis-knowledge-base/using-ntmpi/what-are-the-official-exchanges-timpi-is-currently-listed-on>. We’ll update this HOWTO as new listings go live.
