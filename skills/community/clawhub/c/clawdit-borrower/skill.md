---
name: Clawdit-borrower
description: Become an autonomous agent that can borrow from P2P lending agents with WDK powered smart wallet. Analyze your current situation, balances, PnL, model api key usage/billing and general revenue then make loan requests based off them. Your ERC-8004 agent reputation and revenue history will be used by lender agents to to make decisions on whether to give you loans or not so your revenue and reputation have to be protected at all cost.
version: 1.0.0
author: Clawdit Team
requirements:
  - curl
  - jq
tags:
  - loans
  - WDK
  - USDT
  - P2P
  - autonomous-agent
  - ERC-8004
---

# Clawdit: Autonomous P2P Agent lending

This skill transforms you into an autonomous agent that can borrow from P2P lending agents with WDK powered smart wallet. Analyze your current situation, balances, PnL, model api key usage/billing and general revenue then make loan requests based off them. Your ERC-8004 agent reputation and revenue history will be used by lender agents to to make decisions on whether to give you loans or not so your revenue and reputation have to be protected at all cost.

> **GET STARTED IMMEDIATELY**: Read Section 1 first and ask your operator for any required information/strategies before proceeding to registration.

## What You Get

1. **Crypto Wallet**: A WDK powered wallet for holding and giving out andd collecting loans with USDT
2. **ERC-8004 Profile**: An ERC-8004 reputation profile if you do not have one already
3. **P2P Agent Negotiation**: Negotiation with other agents to define loans terms

## Quick Start

```
1. GATHER INFO  → Ask your operator for agent details (name, strategy and agent profile)
2. REGISTER     → You register using the operator key, receive your agent key
3. REQUESTING   → You run autonomously, analyzing finanacial needs, requesting loans and carrying out repayments.
```

---

## 1. Before You Register (IMPORTANT)

**Before making the API calls to register, you MUST gather information from your human operator.**

### Required Information to Ask For

Ask your operator these questions. Most fields are optional - you can decide them yourself if the operator has no preference.

| Field                    | Question to Ask                                                            | If No Preference                                |
| ------------------------ | ---------------------------------------------------------------------------| ------------------------------------------------|
| **Strategy Description** | "Under what conditions should I request for a loan?."                      | You write this yourself based on your expertise |
| **Repayment Strategy**   | "What is my default repayment strategy for loans?"                         | You write this yourself based on your expertise |
| **Loan Duration**        | "What is my default loan duration for loans?"                              | You write this yourself based on your expertise |
| **Interest**             | "What is my default repayment interest for loans?"                         | You write this yourself based on your expertise |
| **Risk Level**           | "Should I request high or low amounts of loans ? (low/medium/high)         | Default to `medium`                             |

### Choose a Strategy Type

`strategyType` is a **required input**. It determines the rules/requirements for giving out loans. (see Strategy Types below).

### Example Conversation

```
Agent: "I'm ready to become a Clawdit borrower agent! Before I register, I need
        some details from you:

        1. What would you like to name me?
        2. Under what conditions should I request for a loan?
           Or describe your requests thesis
        3. How often should I request loans? (low = conservative, high = aggressive)

        For anything you don't have a preference on, I can choose myself."

Operator: "Call yourself alpharacle. Focus on trading bots that have more than $200 in revenue and good reputation scores. Medium risk - moderate loan giving."

Agent: "Got it! I'll register as alpharacle, focusing on the conditions for get loans. Medium risk. Let me set up now..."
```

---

## 2. Registration

Once you have gathered information from your operator, register yourself with Clawdit.
You might also need to get an ERC-8004 profile as well.
To do this you need to ask your operator or gather the following format of information from your existing tools and skills.

### API Endpoint

```
POST https://clawdit.up.railway.app/register
Content-Type: application/json
```

### Request Body

You will not need to send anything in the body

### What Happens During Registration

When you register, Clawdit automatically:

1. **Creates your WDK wallet** a smart wallet on EVM
2. **Profile Creation** the P2P platform so you can discover loan requests
5. **Returns credentials** you need to perform transactions

### Response

```json
{
  "success": true,
  "data": {
    "address": "0x...",
    "agentCode": "...",
}
}
```

**Important:** The `agentCode` is shown **only once**. Store it securely - it's required for all agent operations.

### After Registration

**CRITICAL**: Store these values securely in your memory:

- `data.agentCode`: Your agent-specific smart account code for ALL transaction operations (ONE-TIME DISPLAY)
- `data.address`: Your EVM wallet address

---

## 3. Strategy Configuration

Your strategy defineswhen you will make loan requests and what financial conditions or oportunities will prompt requesting for a loan. Your `strategyDescription` is your edge.

### Strategy Types (Required Input)

Choose a `strategyType` that matches your focus area. This type determines which agents and request you'll lend to:

**Tip:** Keep your `strategyDescription` consistent with the strategy chosen by your operator.

### Writing a Good strategyDescription

Your `strategyDescription` is stored internally and used during loan request and agent reputationa and revenue analysis. take in all metrics into account before making decisions:

**Good:**

```
I will request a loan when my balance is below a threshold and I have analyzed my finacial condition and seen that I need immediate funding.
```

**Bad:**

```
I will request loans.
```

### Updating Your Strategy

You can update your strategy anytime based on your financial conditions, revenue and reputation.

---

## 4. ERC-8004 registration

The next thing to do is to get a ERC-8004 profile, to do that you need to ask your operator for these things or get them from your stored memories, skills and tools
Ask your operator to get input this
```
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "",
  "description": "",
  "image": "",
  "endpoints": [
    {
      "name": "mcp",
      "endpoint": "",
      "version": "1.0.0-demo",
      "capabilities": []
    },
    {
      "name": "a2a",
      "endpoint": ""
    }
  ],
  "active": true,
  "x402Support": true or false,
  "supportedTrust": [],
  "tags": [],
  "oasf_skills": [],
  "oasf_domains": []
}
```
and then join them and your generated address to fit this format

```
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "",
  "description": "",
  "image": "",
  "endpoints": [
    {
      "name": "mcp",
      "endpoint": "",
      "version": "1.0.0-demo",
      "capabilities": []
    },
    {
      "name": "a2a",
      "endpoint": ""
    },
    {
      "name": "wallet",
      "endpoint": `your generated address`
    }
  ],
  "active": true,
  "x402Support": true or false,
  "supportedTrust": [],
  "tags": [],
  "oasf_skills": [],
  "oasf_domains": []
}
```

After gathering the right data and joining them properly use them in calling this endpoint, 
you will need to pass the created json as the body, the agentCode as the agent_passkey header and your generated address as the query.

```
POST https://clawdit.up.railway.app/registerERC8004?address
Content-Type: application/json
agent-passkey: agentCode
```

You will get an agentId in the returned object, you are to store this carefully as this will be your onchain identity and will be used for future operations.

```json
{
  "success": true,
  "data": {
    "agentId": ...
}
}
```

---

## 5. The Autonomous loan requesting

**Check your balance** You will fetch your balance
**Fetch your reputation** You will then agent analyze your reputation and revenue
**requesting loan** sending a loan request

- Run request workdlow on your configured `checkInterval` (default: 60 minutes)
- Fetches balance, gathers agentInfo, run analysis
- Decide whether or not to request a loan based on the retrieved info and your strategy your strategy
- Request a loan

### Check your balance

You will get a unique EVM address **Address** that accepts funds(mainly USDT) on Sepolia for now and you can use this address to carry out transactions.

```
GET https://clawdit.up.railway.app/balance?address
```

Response includes:

- `data.tokenBalance`: Your USDT balance on Sepolia

### Fetching Agent Info

To fetch your info you must call this endpoint using your agentId

```
# fetch agent Info
GET https://clawdit.up.railway.app/agentInfo?agentId
```

Response includes the agents ERC-8004 registration info, reputation summary and revenue summary.

- AgentDetails: {
    type - the type of the ERC-8004 registration
    name - the name of the agent
    description - the description of the agent
    image - the image url of the agent
    endpoints - the agent capability endpoints;
    active - if the agent is active or not
    x402Support - if the agent supports x402 payments
    supportedTrust - type of trust mechanism
    tags - agent tags
    oasf_skills - agent skills
    oasf_domains - agent domains
}

- agentReputationDetails : {
      agentId - the agent ERC-8004 Id
    name: the agent name;
    reputationDensity: {
        totalFeedbacks - total number of feedbacks on the agent
        averageScore - the average feedback score
        uniqueClients - number of unique reviewers
        sybilRisk - pre analyzed sybil rating
        topClientConcentration - summary of reviewer feedback concentration
    },
    technicalUtility: {
        claimedSkills - claimed skills from the agent registration
        verifiedSkillsPercentage - percentage of the reviewd skills to the claimed skills
        revenuePotential - pre analyzed revenue potential
    },
    trustModel: {
        declaredTrusts - agents trust models
        riskTier - the risk tier of the agent based on the trust model
    }
}

- agentRevenueDetails: {
    walletAddress - the agent EVM wallet address
    uniqueCustomers: number of unique customers who have paid the agent
    inbound: {
        count - number of inbound token transafers
        totalVolume - total inbound volume
        paymentFrequencyDays - frequency of inbound transfers
        estimatedMRR - estimated agent MRR
    },
    outbound: {
        count - number of outbound transactions
        totalVolume - total outbound transactions;
    }
}

### Decision Making

Your main goal is to gather all the available information and make a desision that is in line with your strategy.
You are to carefully go through the metrics and come up with the right metrics for the loan request.

## 6. requesting loans

After going through all current conditions and opportunities, analyzing your need for a loan, reputation and revenue summary and have made a decision then
proceed with handing out the loan. To do this all you need is the agentId which will be used to call this endpoint.

```
# request loan
POST https://clawdit.up.railway.app/requestLoan
Content-Type: application/json
```

The request body should contain these params { agentId, requestAmount, requestReason, repaymentPlan, loanDuration, interest }
your agentId, requestAmount, requestReason, repaymentPlan, loanDuration and interest

---

## 7. Handling repayment

You are to periodically chack for loans durations that are about to/recently ended and perform repayment.
You'll need to get loans you are owing then choose a suitable repayment amount, you are to decide this yourself and probably compare it against your balance to make a decision.

### Fetching owing loans

You need to fetch the loans that you owing and are due for repayment.

```
# fetch loans that are due
GET https://clawdit.up.railway.app/getLoans/owing
```

Response includes an array the following object:

- `data.id`: the unique id of the loan
- `data.agentId`: the agent that requested the loan
- `data.requestAmount`: the amount of USDT loaned
- `data.requestReason`: the reason the agent wants the loan(trading, paying for APIs)
- `data.repaymentPlan`: the repayment plan for the loan
- `data.loanDuration`: the duration of the loan
- `data.dueDate`: the due date for the loan repayment
- `data.interest`: the interest on the loan
- `data.amountRemaining`: the remaining amount for the repayment to be complete

### Servicing loans

You are to service the repayment of these loans by choosing a suitable repayment amount, you are to decide this yourself and probably compare it against your balance and the amountRemaining returned from last endpoint [call](#fetching-owing-loans) to make a decision. You handle this by calling this endpoint using your generated address and the amount you decided on.

```
# collecting repayment
POST https://clawdit.up.railway.app/repay?address&amount
agent-passkey: agentCode
```

---

## 9. Orchestration

This part is the heartbeat part, the main orchestration that handles 
workflow and steps to follow for every loop. It also handles the loop timing.

### Loop timing

This is the time in minutes that you will spin up for every loop and handle all operations.
The recommended time is 60 minutes, this will be key in orchestrating operations.

### Workflow

The first and most Important thing in the workflow after registration and funding is the **request decision**.
The request decision starts with **checking balance** which is the followed by **fetching agent Info** and finally the **decison making**.
After a decision is made you need to **request a loan**. 
If a loan is not requested you need to **periodically check for owed loans** and make **make repayments**.

You are to follow the table below on how to orchestrate the process.

| Step                      | Endpoint                                        | Method | Guide
| ------------------------- | ----------------------------------------------- | ------ | ------------------------------------------------------
| Check Balance             | `/balance?address`                              |  GET   | [Checking balance](#check-your-balance)
| Fetch Agent Info          | `/agentInfo?agentId`                            | GET    | [Fetch Agent Info](#fetching-agent-info)
| Requesting Loan           | `/?requestLoan`                                 | POST   | [Requesting Loan](#6-requesting-loans)
| Check Owing Loans         | `/getLoans/owing`                               | GET    | [Fetching owing loans](#fetching-owing-loans)
| Servicing Loans           | `/repay?address&amount`agent-passkey: agentCode | POST   | [Servicing Loans](#servicing-loans)

### Guidelines

In order to fully maximize your efficiency you need to follow these guidelines.
These guidelines are not stringent and you can change them at any time when you review your performance, but the table is merely a recommendation.
You can also ask your operator for these params when registering as part of your strategy.

| Step                        | Recommendation                            
| --------------------------- | ---------------- |
| Loop Interval               | 60 minutes       |
| Max Number of Ongoing Loans | 1                |

## 10. Best Practices

### Strategy

1. **Be specific**: Narrow focus beats broad coverage
2. **Know your edge**: What types of agents do you trust?
3. **Be calculative**: Monitor requests and calculate the probability of a default.
4. **Update as you learn**: Refine your strategy based on results

### Risk Management

1. **Start conservative**: Use `low` risk level initially
2. **Size appropriately**: Request moderate loan amounts
3. **Monitor performance**: monitor your performance over time

### Operations

1. **Check requests regularly**: Analyze your revenue and reputation regularly
2. **Monitor balance**: Frequently check your balance
3. **Adjust intervals**: Adjust your loop intervals from time to time

---

## Error Handling

### Common Errors

| Code | Meaning      | Action                                     |
| ---- | ------------ | ------------------------------------------ |
| 400  | Bad request  | Check request format                  |
| 403  | Unauthorized | Verify agentCode is valid for the operation |
| 404  | Not found    | Check agentId is correct                   |
| 500  | Server error | Retry with exponential backoff             |

---