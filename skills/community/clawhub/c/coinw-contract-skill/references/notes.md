# Notes

## Account Activation

### Spot Trading

Spot trading is automatically enabled after account registration. Users can activate API access permissions for spot trading during the API creation process.

### Futures Trading

To enable futures trading, users must first activate their futures account. When creating an API and setting "Futures" permissions for the first time, the system will prompt the user to go to the "Futures Trading" page to complete the risk test. After passing the test, the futures trading account will be activated and futures trading can be conducted.

## Position Limits

### Futures Trading

For detailed information about futures position limits, please visit https://www.coinw.com/trading-rules

## Frequency Limits

### 1. Futures Trading Frequency Limits

Futures trading API interfaces are subject to the following two types of frequency limits:

#### (a) Single Interface Frequency Limit

For futures trading, each RESTful API interface has its own access frequency limit, limited by IP address and user UID. The specific frequency limit can be found in the "Frequency Limit" field of each interface document.

If the interface's frequency limit is exceeded, the following error message will be returned:

```json
{"code": 29001,"msg": "API access frequently"}
```

This error indicates that the call frequency of the interface has exceeded the upper limit. It is recommended that users check the frequency settings of the corresponding interface.

#### (b) Global Frequency Limit

In addition to single interface frequency limits, futures RESTful interfaces are also subject to global frequency limits, that is, within a set time, the total number of requests for all futures RESTful APIs by users is limited to ensure that the overall request volume does not exceed the system capacity.

##### Category A: Market Data Interfaces (IP-based frequency limit)

The following interfaces are classified as Category A, and all interface requests are merged and counted, sharing the frequency limit threshold:

- GET /v1/perpumPublic/klines
- GET /v1/perpumPublic/tickers
- GET /v1/perpumPublic/ticker
- GET /v1/perpumPublic/trades
- GET /v1/perpumPublic/depth

Frequency limit: Category A interfaces are merged and counted by IP dimension, with a maximum of 30 requests per second per IP.

##### Category B: Other Interfaces (UID-based frequency limit)

Other interfaces not included in Category A are classified as Category B, and all interface requests are merged and counted, sharing the frequency limit threshold:

Frequency limit: Category B interfaces are merged and counted by user UID, with a maximum of 100 requests per second per UID.

If the frequency limit is triggered, the system will return the following error:

```json
{"code": 29001,"msg": "API access frequently"}
```

In futures trading, if this error is returned, it indicates that the request frequency has exceeded the threshold set by the system. To ensure service stability and system performance for all users, it is recommended that developers implement reasonable API call frequency control mechanisms and monitoring strategies.

Note: In addition to interface-level frequency limits and global frequency limits, the system may also trigger frequency limit mechanisms in case of overall network congestion. This type of limit is not caused by a user's request frequency, but by a surge in the overall API request volume of the platform.

### 2. Spot Trading Frequency Limits

Spot trading APIs are also subject to the following two types of frequency control:

#### (a) Single Interface Frequency Limit

For spot trading, each RESTful API endpoint is subject to interface frequency limits based on IP and user ID. The frequency limit for each interface is recorded in each API interface. Please refer to the "Frequency Limit" section in the API interface documentation for details.

#### (b) Global Frequency Limit

In addition to single interface frequency limits, spot RESTful APIs are also subject to global frequency limits, that is, within a set time, the total number of requests for all spot RESTful APIs by users is limited to ensure that the overall request volume does not exceed the system capacity.

- Per IP address: maximum 100 times/second
- Per user ID: maximum 300 times/second

In spot trading, if the request frequency exceeds the interface-level or global frequency limit, the system will return the following error message:

```json
{"code": 29001,"msg": "API access frequently"}
```

In spot trading, if this error is returned, it indicates that the request frequency has exceeded the threshold set by the system. To ensure service stability and system performance for all users, it is recommended that developers implement reasonable API call frequency control mechanisms and monitoring strategies.

Note: In addition to interface-level frequency limits and global frequency limits, the system may also trigger frequency limit mechanisms in case of overall network congestion. This type of limit is not caused by a user's request frequency, but by a surge in the overall API request volume of the platform.

### 3. API Frequency Limit Strategy – Client Guide

This guide aims to help users understand how to use the API standardizedly and explain the processing mechanism that the system will adopt when the normal call frequency range is exceeded.

#### (a) Normal Usage Count

As long as the frequency limits of each interface and the global frequency limit are not triggered, and the number of API requests remains within the threshold specified below in any 10-second time window, your access will remain smooth and no error messages will be returned.

| Category | Limit (per 10 seconds) |
|----------|------------------------|
| User account (UID) | 60 |
| IP address | 80 |
| Device + IP | 60 |

Note: The above limits are automatically reset every 10 seconds. As long as the frequency limits are followed within each time interval, API usage will not be interrupted;

If the normal usage count is exceeded, the system will enable stricter frequency limit control measures.

To avoid triggering stricter frequency limit measures, it is recommended that you strictly follow the above frequency requirements.

#### (b) What happens if the user exceeds the normal usage count?

##### 1. Warning Phase (5 minutes)

If you exceed the normal usage amount, your API access will enter a temporary warning phase lasting 5 minutes. During this phase:

- The rate limit for each API endpoint will be reduced by 50%. Example: If an endpoint originally allowed 10 requests every 2 seconds, it will now only allow 5 requests.
- You may encounter "rate limit exceeded" errors more frequently.
- If your error count remains within the threshold listed below within 5 minutes, your API access will automatically return to normal usage count.

| Category | Limit (per 10 seconds) |
|----------|------------------------|
| User account (UID) | 60 |
| IP address | 80 |
| Device + IP | 60 |

If the error count exceeds these thresholds during the warning phase, your API access will be temporarily banned.

##### 2. Temporary Ban (30 seconds)

Temporary ban phase:

- All API access will be banned for 30 seconds.
- After 30 seconds, your access count will automatically return to normal usage count.
- However, frequent bans within 8 hours may lead to the blacklist phase.

##### 3. Blacklist Phase

If the user is banned more than the following thresholds within 8 hours, they will be blacklisted:

| Category | Maximum number of bans within 8 hours |
|----------|--------------------------------------|
| User account (UID) | 10 |
| IP address | 10 |
| Device + IP | 5 |

During the blacklist phase:

- All API access will be disabled for 8 hours.
- The user must contact customer service for help.
- If the threshold is not exceeded within 8 hours, your API access will return to normal usage count.

## Mega Coupon

CoinW futures provide Mega Coupon, which can be used as initial margin or to offset trading fees, losses, and funding payments in futures trading. For more details, please visit https://coinw.zendesk.com/hc/en-us/articles/23111150445977-Introduction-to-Futures-Mega-Coupon

## Notes

### Futures Trading

It is strongly recommended to check the "Notes" section in each interface to avoid any misunderstanding or inconvenience.

CoinW allows traders to simultaneously establish long and short positions on the same currency, thereby realizing hedging functions and helping to build more flexible and complex trading strategies.

Usually, closing a position is done by placing the same order in the opposite direction. However, this method is not applicable on CoinW. Placing an order in the opposite direction will open a new position instead of closing the original position, resulting in two active positions. To correctly close a position, please refer to Futures > Order Placement > Close Position. For batch closing positions, please refer to Futures > Order Placement > Batch Close Position.

The platform supports three trading sources: user independent orders, copy trading system orders, and strategy plaza quantitative robot orders. The three types of trades are uniformly displayed at the position level, but OpenAPI only supports operations (such as closing positions, canceling orders, etc.) on positions generated by user independent orders. For positions generated by copy trading and strategy plaza, the API has no operation permissions. It is recommended to use the corresponding functions in the platform to complete the processing.

To set trailing stop loss, take profit, and stop loss, please refer to Futures > Order Placement.

CoinW provides an interface for adjusting position layout. For more details, please refer to Futures > Account and Asset > Set Position Mode. When the "Merge Positions" option is selected, all positions of the same tool and direction will be merged into one position; when the "Separate Positions" option is selected, each newly opened position will be listed separately and have a unique position ID.

Some interfaces return the following response. "code:0" indicates successful operation.

```json
{"code": 0, "msg": ""}
```

Funding fee time limit: During the funding fee period, trading operations such as placing orders or closing positions are not allowed. Attempting these operations will result in an error response. The funding fee process usually takes 30 to 40 seconds. It is recommended to wait at least 1 minute before attempting trading operations. For the specific funding fee schedule, please refer to the official webpage.

The data subscribed with websocket cannot guarantee the order of push data timestamps, so it is recommended that users check and clean the data after receiving it.

Returning an order ID does not represent execution. "Returning orderId indicates that the system has accepted the order request, but the order may be canceled during matching and does not represent execution. To confirm the execution status, please call the query order or position information API.

### Spot Trading

The data subscribed with websocket cannot guarantee the order of push data timestamps, so it is recommended that users check and clean the data after receiving it.