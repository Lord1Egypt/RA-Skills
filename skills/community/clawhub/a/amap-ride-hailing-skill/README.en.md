# amap-ride-hailing-skill

[中文](README.md) | English

# English README

Amap Ride-Hailing Skill for handling Amap ride-hailing requests, including instant ride, scheduled ride, order query, and order cancellation.

> **Service Area**: Cities in Mainland China covered by Amap Ride.

## Prerequisites

Before placing an order through MCP, make sure the user has completed the following two authorizations in the Amap app; otherwise the order step will fail:

1. **In-car audio and video recording authorization**: Authorize in-car recording during the driver's trip; the user must grant the relevant permissions in the app (see [Recording Authorization Setup](#recording-authorization-setup)).
2. **Password-free payment agreement**: The user must bind and enable password-free payment for ride-hailing (see [Password-free Payment Setup](#password-free-payment-setup)).

If the order fails with an authorization error, guide the user to open the Amap app, complete the authorization and payment agreement, and then retry.

The key represents the Amap account identity and payment subject. Use only your own key; do not share it or use someone else's key to place orders.

## Installation and Data

Install this directory as a skill. Runtime data (`assets/preferences.md` and `assets/config.json`) is created from templates in the same directory on first use and is not shipped in the package. If the skill directory is read-only, preferences are session-only.

## Recording Authorization Setup

Amap Ride requires in-car audio and video recording during the driver's trip; orders cannot be placed through the Skill until it is authorized. Complete the three steps below in the Amap app; the red boxes mark the entry point to tap in each screenshot.

| Step 1: tap the avatar at the top right | Step 2: tap Safety Center | Step 3: tap Recording Authorization |
| :---: | :---: | :---: |
| <img src="https://img.alicdn.com/imgextra/i4/O1CN01zHOOpUSaDJB1IZKB_!!6000000004544-2-tps-640-1391.png" width="220" alt="Avatar entry at the top right of the ride-hailing page"> | <img src="https://img.alicdn.com/imgextra/i1/O1CN016bY0yxbOISK1IZKB_!!6000000003449-2-tps-640-1391.png" width="220" alt="Safety Center entry on the profile page"> | <img src="https://img.alicdn.com/imgextra/i2/O1CN01JUy38xrkmaB1IZKB_!!6000000000313-2-tps-640-1391.png" width="220" alt="Recording authorization entry on the Safety Center page"> |

1. Open the Amap app, switch to the **Ride-hailing** tab, and tap the **avatar** at the top right to open your profile.
2. On the profile page, find and tap **Safety Center** (「安全中心」).
3. Under "Safety Settings" in the Safety Center, tap **Recording Authorization** (「录音录像授权」) and follow the on-screen instructions. The item shows "Authorized" (「已授权」) once it is enabled.

> If the authorization error persists, make sure the authorization belongs to the same account signed in to the Amap app.

## Password-free Payment Setup

Orders cannot be placed through the Skill until password-free payment is enabled. Complete the three steps below in the Amap app; the red boxes mark the entry point to tap in each screenshot.

| Step 1: tap Settings at the top right | Step 2: tap Payment Settings | Step 3: tap Amap Ride Password-free Payment |
| :---: | :---: | :---: |
| <img src="https://img.alicdn.com/imgextra/i3/O1CN01wp64jWzy0uC1IZKB_!!6000000003041-2-tps-640-1391.png" width="220" alt="Settings entry at the top right of the Me page"> | <img src="https://img.alicdn.com/imgextra/i4/O1CN01ePfqFVN3LwL1IZKB_!!6000000005508-2-tps-640-1391.png" width="220" alt="Payment Settings entry on the Account and Security page"> | <img src="https://img.alicdn.com/imgextra/i4/O1CN015kQ2CThKR2F1IZKB_!!6000000006079-2-tps-640-1391.png" width="220" alt="Amap Ride password-free payment entry on the Payment Settings page"> |

1. Open the Amap app, switch to the **Me** tab, and tap the **Settings** icon at the top right.
2. On the **Account and Security** page, find the "Account Management" group and tap **Payment Settings** (「支付设置」).
3. On the Payment Settings page, tap **Amap Ride Password-free Payment** (「高德打车免密支付管理」) and follow the on-screen instructions to complete the agreement. Then return to the Skill and retry the ride request.

> If the authorization error persists after signing, make sure the agreement belongs to the same account signed in to the Amap app, and verify that in-car recording authorization is enabled.

## Quick Start

**1. Get an Amap Key**

Visit the [Amap Open Platform](https://lbs.amap.com/api/webservice/create-project-and-key) to create an app and obtain a **Web Service Key**.

**2. Configure the MCP Server**

Add a new server in your MCP client with these parameters; the tools become available after configuration:

| Field | Value                                                                     |
|-------|---------------------------------------------------------------------------|
| Server name | 高德打车                                                                  |
| URL | `https://mcp.amap.com/rest/amap_car/dev/mcp?key=YOUR_AMAP_WEBSERVICE_KEY` |
| Transport | Streamable HTTP                                                           |
| Auth | `key` query parameter in the URL                                          |

> Exporting the environment variable `AMAP_WEBSERVICE_KEY` alone does not make the tools visible in the client; the key must be written into the MCP config.

**3. Reconnect and Verify**

After configuring, reconnect the MCP client or start a new session and confirm that the following tools appear in the tool list:

- `get_taxi_service`
- `confirm_order`
- `cancel_order`
- `query_orders`

You can call `query_orders` once (pass your host platform name as `agent_name` and an empty `scene`) for a read-only verification.

**4. Start Using**

```
Get me a cab to Beijing West Station
Tomorrow morning at 8am from home to the office
Check my order
```

## Features

| Feature | Description |
|--------|-------------|
| Instant Ride | Resolve origin/destination → plan → confirm → place order |
| Scheduled Ride | Specify departure or arrival time, plan and place a scheduled order |
| Query Order | Query order list or a specific order's details |
| Cancel Order | Cancel an active order after user confirmation |
| Invoices | Guide users to issue invoices in the Amap app |
| Customer Service | In-app online support (preferred) and phone hotline |
| Preferences | Maintain address aliases (home/office), a default city, and default vehicle type preferences |

This skill covers instant rides, scheduled rides, order query, and order cancellation.

## How to Use

### 1. Instant Ride

```
User: Get me a cab from Wangjing SOHO to Beijing West Station

Agent: Route planned: Wangjing SOHO, Beijing → Beijing West Station, Beijing. Available vehicles:
1. Economy ~¥45
2. Discount ~¥38
3. Business ~¥78

Please confirm a vehicle type.

User: Economy

Agent: Economy ride requested. Order ID: GD202611030001, estimated driver response in 3 minutes.
```

### 2. Scheduled Ride

```
User: Tomorrow morning at 8am from home to the office

Agent: Scheduled ride planned: tomorrow 08:00 from Wangjing SOHO, Chaoyang, Beijing to Zhongguancun, Haidian, Beijing. Vehicle: Economy, estimated ~¥35. Confirm?

User: Confirm

Agent: Scheduled order created. Order ID: GD202611030002.
```

### 3. Query Order

```
User: Check my order

Agent: Your order list is ready. Please check.
```

### 4. Cancel Order

```
User: Cancel my order

Agent: Cancel order GD202611030001?
- Origin: Wangjing SOHO, Beijing
- Destination: Beijing West Station, Beijing

User: Confirm

Agent: Order cancelled.
```

### 5. Set Preferences

You can tell the Skill your frequent address aliases, a default city, and default vehicle type preferences, which will be used in future ride requests.

```
User: My home is Wangjing SOHO, Chaoyang, Beijing

Agent: Saved "home" = Wangjing SOHO, Chaoyang, Beijing.

User: My office is Zhongguancun, Haidian, Beijing

Agent: Saved "office" = Zhongguancun, Haidian, Beijing.

User: Default city is Beijing

Agent: Default city set to Beijing.

User: Default vehicle type is Economy

Agent: Default vehicle type set to Economy.
```

> Preferences are stored in the skill's `assets/preferences.md`, created from `assets/preferences.example.md` on first save. Do not commit real addresses; if the directory is read-only, preferences are session-only.
>
> The Skill remembers clear long-term preferences (such as home/office addresses, default city, and vehicle type) automatically; one-off trip addresses are not saved.

## FAQ

**Q: Why don't I see the Amap Ride tools in the tool list?**

A: Check that the `key` query parameter in the MCP config `url` contains a valid Amap Web Service Key, and that you have reconnected the client or started a new session.

**Q: What should I do if the order fails with an authorization error?**

A: Ask the user to open the Amap app, complete the in-car recording authorization and password-free payment agreement, and then retry.

**Q: Can I just say the place name without the city?**

A: It's best to provide "city + specific place", e.g. "北京市望京SOHO". If only the place name is given, the Skill will try to complete the city; if it can't be determined, it will ask for confirmation.

## Reference

- Full execution instructions: [SKILL.md](SKILL.md)
- MCP authentication and key: [references/auth.md](references/auth.md)
- Tool parameters and scenes: [references/tool-contracts.md](references/tool-contracts.md)
- Errors and recovery: [references/errors.md](references/errors.md)
- Scheduling templates: [references/scheduling.md](references/scheduling.md)
- Preferences template: [assets/preferences.example.md](assets/preferences.example.md)
