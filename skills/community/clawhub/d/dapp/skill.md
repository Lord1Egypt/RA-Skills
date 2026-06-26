---
name: Dapp
description: A comprehensive AI agent skill for discovering, evaluating, and monitoring decentralized applications. Tracks on-chain activity anomalies, evaluates smart contract security, identifies emerging dApps before they go mainstream, monitors your portfolio positions across DeFi protocols, analyzes tokenomics and incentive structures, and helps Web3 users and investors make faster and better-informed decisions in a market where information advantage measured in hours translates directly into financial outcomes.
---

# Dapp

## The Edge Is in the Data Nobody Is Reading Yet

In traditional financial markets, information advantage has been systematically compressed over decades. Regulatory requirements create disclosure obligations. Professional analysts cover every major asset. Algorithmic trading reacts to public information in milliseconds. The edge available to an individual investor in public equities is thin and getting thinner.

Decentralized applications run on public blockchains where every transaction, every contract interaction, every wallet movement is permanently recorded and available to anyone willing to read it. This sounds like the opposite of information advantage — total transparency, equal access. In practice, it creates one of the last remaining environments where information advantage is large and persistent, because most people are not reading the data.

The on-chain signal that a protocol's daily active users tripled overnight is public. The wallet cluster that has been systematically accumulating a governance token for three weeks before a major proposal is public. The smart contract function that drains user funds under a specific condition is public. The liquidity position that will be liquidated if the price moves five percent is public.

What is not equal is the capacity to find these signals, interpret them correctly, and act on them before they are priced in. That capacity is what separates the people who consistently find alpha in Web3 from the people who consistently buy tops and sell bottoms.

This skill is built to close that gap.

---

## On-Chain Activity Monitoring

The most reliable signal in crypto is not price. Price is the last thing to move. The first things to move are the on-chain metrics that price eventually reflects: active wallets, transaction volume, contract interactions, liquidity flows, large wallet movements.

When a dApp's daily active users double in forty-eight hours without a corresponding announcement, something is happening. Maybe a new use case has been discovered. Maybe a major influencer mentioned it in a context that drove adoption. Maybe a competitor's failure is routing users to this protocol. Maybe the team has been quietly onboarding a large partner and the integration just went live. Whatever the cause, the signal arrived on-chain before it arrived in price, and the window between those two moments is where the opportunity lives.

The skill monitors on-chain activity for the protocols and categories you care about. It surfaces anomalies — metric movements that are statistically significant relative to baseline — and provides the context needed to evaluate whether the anomaly represents a genuine opportunity or a misleading artifact. A transaction volume spike caused by one large transaction is different from a transaction volume spike caused by a hundred new users. A daily active user increase driven by a single wallet cycling through interactions is different from one driven by genuine new adoption.

It distinguishes between these cases rather than surfacing raw metric movements that require you to do the interpretation work yourself.

---

## Smart Contract Security Analysis

The on-chain record of a smart contract contains everything needed to evaluate whether it does what it claims to do — and whether it does anything else. The function that the documentation does not mention. The admin key that can pause the contract and redirect funds. The upgrade mechanism that allows the team to change the contract logic after users have deposited. The mathematical relationship between token emission and protocol revenue that makes the yield unsustainable at current scale.

Most dApp users do not read smart contracts. This is understandable — smart contract code requires specific technical knowledge to interpret, and the volume of new contracts deployed daily makes comprehensive review impossible. But the consequence of not reading contracts is exposure to risks that were publicly visible before any funds were committed.

The skill evaluates smart contracts for the risk categories that matter most. Ownership and admin key risks: who can do what to the contract, under what conditions, with what notice. Upgrade risks: whether the contract logic can be changed and through what mechanism. Economic risks: whether the incentive structure is mathematically sustainable or dependent on continuous new capital inflows to pay existing participants. Common vulnerability patterns: reentrancy, integer overflow, oracle manipulation, flash loan attack vectors.

It produces a risk summary that covers these categories in plain language — not a comprehensive security audit, which requires formal verification and manual review by specialized engineers, but a first-pass evaluation that identifies the risks that are visible from the contract code and comparable to what a technically sophisticated user would identify through their own review.

When a contract presents risks that are significant enough to warrant professional audit before meaningful capital commitment, the skill says so directly.

---

## Discovering Emerging Protocols

The protocols with the highest return potential are the ones nobody is talking about yet. By the time a protocol is featured on major crypto media, the early adopter premium has been captured. By the time it appears in influencer content, the smart money has already positioned. The opportunity that compounds into significant returns is the one identified before the narrative forms.

Finding these protocols requires systematic attention to the places where genuine innovation surfaces before it is packaged for mainstream consumption: GitHub repositories with recent significant activity, developer forums where builders discuss what they are working on, governance forums of established protocols where ecosystem expansion proposals reveal what is being built, on-chain deployment activity that shows new contracts receiving early adoption.

The skill monitors these signals for your specified categories of interest. It surfaces protocols that are showing early signs of genuine adoption — not marketing metrics, but on-chain usage metrics — before they have attracted significant attention. It provides enough context to evaluate whether the early adoption signal represents a genuine product-market fit discovery or an artifact of incentive structures that will not persist.

---

## DeFi Position Management

Active participation in DeFi involves managing positions across multiple protocols simultaneously: liquidity pool positions, lending positions, staking positions, governance token holdings with vesting schedules, yield farming positions with compounding requirements. Each has its own risk parameters, its own reward mechanics, and its own set of conditions that require attention or action.

Liquidation thresholds for lending positions need to be monitored against price movements. Impermanent loss in liquidity positions accumulates in ways that are not immediately visible in the displayed APY. Reward token emissions that fund current yields have emission schedules that determine how long the current APY is sustainable. Governance proposals that affect your positions pass or fail on timelines that require active monitoring if you want your vote to count.

The skill maintains a unified view of your DeFi positions across protocols. It calculates your actual position in each protocol accounting for accrued rewards and impermanent loss, not just the nominal deposit value. It monitors liquidation distances for lending positions and alerts when price movements bring them within a specified threshold. It tracks reward token vesting and emission schedules and surfaces the dates that require action. It identifies governance proposals affecting protocols you are participating in before the voting window closes.

---

## Tokenomics Analysis

A token price reflects the market's current assessment of future value. That assessment is only as good as the market's understanding of the tokenomics — the supply schedule, the demand drivers, the value accrual mechanism, and the incentive structures that determine how different participants will behave over time.

Most token holders do not analyze tokenomics in detail. They see a high APY and assume it reflects genuine yield. They see a low circulating supply and assume scarcity is driving price. They see a large treasury and assume the protocol is financially healthy. Each of these assumptions can be wrong in ways that are visible in the tokenomics before they are visible in the price.

The skill analyzes tokenomics with specific attention to the dynamics that most often produce misaligned expectations. Emission schedules: when do large unlock events occur and how does the unlock volume compare to current daily trading volume? Yield sources: is the current APY funded by protocol revenue or by token emission, and if emission, what happens to the APY as emission decreases? Value accrual: does holding or staking the token actually capture value from protocol usage, or does the token serve primarily as a governance mechanism with no direct economic claim on protocol revenue? Incentive alignment: do the largest token holders have incentives aligned with long-term protocol success or with near-term price appreciation?

---

## Privacy and Local Operation

Every query you make to a blockchain data provider is a data point about your interests and potentially your positions. Sophisticated market participants monitor the queries that wallets and addresses make to data providers, because those queries reveal intent before the on-chain transactions that execute on that intent.

The skill is designed to operate with your privacy as a constraint, not an afterthought. It does not require you to connect wallets or reveal addresses to function. Position monitoring can be configured with read-only observation of public addresses without any signing capability. Analysis queries are structured to minimize the inferential value they provide to anyone monitoring your data provider interactions.

Your private keys stay where they belong: with you, offline, never touched by any component of this skill.

---

## The Information Advantage Window

On-chain data is public. The window of advantage it provides is the time between when a signal appears in the data and when it is reflected in price — the time it takes for enough market participants to notice, interpret, and act on the signal to price it in.

That window varies by signal type and market conditions. For major protocol events, it can be minutes. For subtler adoption signals in smaller protocols, it can be days. For the slow accumulation patterns that precede major moves, it can be weeks.

The skill is built to help you operate within that window systematically rather than occasionally — to be the person reading the data rather than the person reacting to the price movements that the data already predicted.
