# notification module

This module contains `38` endpoints in the `notification` domain.

## Endpoints

| Method | Path | Operation ID | Auth | Input | Required fields | Description |
|---|---|---|---|---|---|---|
| GET | `/notification.all` | `notification-all` | `apiKey` | `none` | - | - |
| POST | `/notification.createCustom` | `notification-createCustom` | `apiKey` | `json` | body.name, body.endpoint | - |
| POST | `/notification.createDiscord` | `notification-createDiscord` | `apiKey` | `json` | body.appBuildError, body.databaseBackup, body.volumeBackup, body.dokployRestart, body.name, body.appDeploy, body.dockerCleanup, body.serverThreshold, body.webhookUrl, body.decoration | - |
| POST | `/notification.createEmail` | `notification-createEmail` | `apiKey` | `json` | body.appBuildError, body.databaseBackup, body.volumeBackup, body.dokployRestart, body.name, body.appDeploy, body.dockerCleanup, body.serverThreshold, body.smtpServer, body.smtpPort, body.username, body.password, body.fromAddress, body.toAddresses | - |
| POST | `/notification.createGotify` | `notification-createGotify` | `apiKey` | `json` | body.appBuildError, body.databaseBackup, body.volumeBackup, body.dokployRestart, body.name, body.appDeploy, body.dockerCleanup, body.serverUrl, body.appToken, body.priority, body.decoration | - |
| POST | `/notification.createLark` | `notification-createLark` | `apiKey` | `json` | body.appBuildError, body.databaseBackup, body.volumeBackup, body.dokployRestart, body.name, body.appDeploy, body.dockerCleanup, body.serverThreshold, body.webhookUrl | - |
| POST | `/notification.createNtfy` | `notification-createNtfy` | `apiKey` | `json` | body.appBuildError, body.databaseBackup, body.volumeBackup, body.dokployRestart, body.name, body.appDeploy, body.dockerCleanup, body.serverUrl, body.topic, body.accessToken, body.priority | - |
| POST | `/notification.createPushover` | `notification-createPushover` | `apiKey` | `json` | body.name, body.userKey, body.apiToken | - |
| POST | `/notification.createResend` | `notification-createResend` | `apiKey` | `json` | body.appBuildError, body.databaseBackup, body.volumeBackup, body.dokployRestart, body.name, body.appDeploy, body.dockerCleanup, body.serverThreshold, body.apiKey, body.fromAddress, body.toAddresses | - |
| POST | `/notification.createSlack` | `notification-createSlack` | `apiKey` | `json` | body.appBuildError, body.databaseBackup, body.volumeBackup, body.dokployRestart, body.name, body.appDeploy, body.dockerCleanup, body.serverThreshold, body.webhookUrl, body.channel | - |
| POST | `/notification.createTeams` | `notification-createTeams` | `apiKey` | `json` | body.appBuildError, body.databaseBackup, body.volumeBackup, body.dokployRestart, body.name, body.appDeploy, body.dockerCleanup, body.serverThreshold, body.webhookUrl | - |
| POST | `/notification.createTelegram` | `notification-createTelegram` | `apiKey` | `json` | body.appBuildError, body.databaseBackup, body.volumeBackup, body.dokployRestart, body.name, body.appDeploy, body.dockerCleanup, body.serverThreshold, body.botToken, body.chatId, body.messageThreadId | - |
| GET | `/notification.getEmailProviders` | `notification-getEmailProviders` | `apiKey` | `none` | - | - |
| GET | `/notification.one` | `notification-one` | `apiKey` | `params` | query.notificationId | - |
| POST | `/notification.receiveNotification` | `notification-receiveNotification` | `apiKey` | `json` | body.Type, body.Value, body.Threshold, body.Message, body.Timestamp, body.Token | - |
| POST | `/notification.remove` | `notification-remove` | `apiKey` | `json` | body.notificationId | - |
| POST | `/notification.testCustomConnection` | `notification-testCustomConnection` | `apiKey` | `json` | body.endpoint | - |
| POST | `/notification.testDiscordConnection` | `notification-testDiscordConnection` | `apiKey` | `json` | body.webhookUrl | - |
| POST | `/notification.testEmailConnection` | `notification-testEmailConnection` | `apiKey` | `json` | body.smtpServer, body.smtpPort, body.username, body.password, body.toAddresses, body.fromAddress | - |
| POST | `/notification.testGotifyConnection` | `notification-testGotifyConnection` | `apiKey` | `json` | body.serverUrl, body.appToken, body.priority | - |
| POST | `/notification.testLarkConnection` | `notification-testLarkConnection` | `apiKey` | `json` | body.webhookUrl | - |
| POST | `/notification.testNtfyConnection` | `notification-testNtfyConnection` | `apiKey` | `json` | body.serverUrl, body.topic, body.accessToken, body.priority | - |
| POST | `/notification.testPushoverConnection` | `notification-testPushoverConnection` | `apiKey` | `json` | body.userKey, body.apiToken, body.priority | - |
| POST | `/notification.testResendConnection` | `notification-testResendConnection` | `apiKey` | `json` | body.apiKey, body.fromAddress, body.toAddresses | - |
| POST | `/notification.testSlackConnection` | `notification-testSlackConnection` | `apiKey` | `json` | body.webhookUrl, body.channel | - |
| POST | `/notification.testTeamsConnection` | `notification-testTeamsConnection` | `apiKey` | `json` | body.webhookUrl | - |
| POST | `/notification.testTelegramConnection` | `notification-testTelegramConnection` | `apiKey` | `json` | body.botToken, body.chatId, body.messageThreadId | - |
| POST | `/notification.updateCustom` | `notification-updateCustom` | `apiKey` | `json` | body.notificationId, body.customId | - |
| POST | `/notification.updateDiscord` | `notification-updateDiscord` | `apiKey` | `json` | body.notificationId, body.discordId | - |
| POST | `/notification.updateEmail` | `notification-updateEmail` | `apiKey` | `json` | body.notificationId, body.emailId | - |
| POST | `/notification.updateGotify` | `notification-updateGotify` | `apiKey` | `json` | body.notificationId, body.gotifyId | - |
| POST | `/notification.updateLark` | `notification-updateLark` | `apiKey` | `json` | body.notificationId, body.larkId | - |
| POST | `/notification.updateNtfy` | `notification-updateNtfy` | `apiKey` | `json` | body.notificationId, body.ntfyId | - |
| POST | `/notification.updatePushover` | `notification-updatePushover` | `apiKey` | `json` | body.notificationId, body.pushoverId | - |
| POST | `/notification.updateResend` | `notification-updateResend` | `apiKey` | `json` | body.notificationId, body.resendId | - |
| POST | `/notification.updateSlack` | `notification-updateSlack` | `apiKey` | `json` | body.notificationId, body.slackId | - |
| POST | `/notification.updateTeams` | `notification-updateTeams` | `apiKey` | `json` | body.notificationId, body.teamsId | - |
| POST | `/notification.updateTelegram` | `notification-updateTelegram` | `apiKey` | `json` | body.notificationId, body.telegramId | - |

## Endpoint details

This section lists parameter and request-body fields for each operation.

### `notification-all`

- Method: `GET`
- Path: `/notification.all`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `notification-createCustom`

- Method: `POST`
- Path: `/notification.createCustom`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.endpoint` | `required` | `string` | minLength=1 |
| `body.headers` | `optional` | `object` | - |

### `notification-createDiscord`

- Method: `POST`
- Path: `/notification.createDiscord`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `required` | `boolean` | - |
| `body.databaseBackup` | `required` | `boolean` | - |
| `body.volumeBackup` | `required` | `boolean` | - |
| `body.dokployRestart` | `required` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `required` | `boolean` | - |
| `body.dockerCleanup` | `required` | `boolean` | - |
| `body.serverThreshold` | `required` | `boolean` | - |
| `body.webhookUrl` | `required` | `string` | minLength=1 |
| `body.decoration` | `required` | `boolean` | - |

### `notification-createEmail`

- Method: `POST`
- Path: `/notification.createEmail`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `required` | `boolean` | - |
| `body.databaseBackup` | `required` | `boolean` | - |
| `body.volumeBackup` | `required` | `boolean` | - |
| `body.dokployRestart` | `required` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `required` | `boolean` | - |
| `body.dockerCleanup` | `required` | `boolean` | - |
| `body.serverThreshold` | `required` | `boolean` | - |
| `body.smtpServer` | `required` | `string` | minLength=1 |
| `body.smtpPort` | `required` | `number` | minimum=1 |
| `body.username` | `required` | `string` | minLength=1 |
| `body.password` | `required` | `string` | minLength=1 |
| `body.fromAddress` | `required` | `string` | minLength=1 |
| `body.toAddresses` | `required` | `array<string>` | - |
| `body.toAddresses[]` | `required` | `string` | - |

### `notification-createGotify`

- Method: `POST`
- Path: `/notification.createGotify`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `required` | `boolean` | - |
| `body.databaseBackup` | `required` | `boolean` | - |
| `body.volumeBackup` | `required` | `boolean` | - |
| `body.dokployRestart` | `required` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `required` | `boolean` | - |
| `body.dockerCleanup` | `required` | `boolean` | - |
| `body.serverUrl` | `required` | `string` | minLength=1 |
| `body.appToken` | `required` | `string` | minLength=1 |
| `body.priority` | `required` | `number` | minimum=1 |
| `body.decoration` | `required` | `boolean` | - |

### `notification-createLark`

- Method: `POST`
- Path: `/notification.createLark`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `required` | `boolean` | - |
| `body.databaseBackup` | `required` | `boolean` | - |
| `body.volumeBackup` | `required` | `boolean` | - |
| `body.dokployRestart` | `required` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `required` | `boolean` | - |
| `body.dockerCleanup` | `required` | `boolean` | - |
| `body.serverThreshold` | `required` | `boolean` | - |
| `body.webhookUrl` | `required` | `string` | minLength=1 |

### `notification-createNtfy`

- Method: `POST`
- Path: `/notification.createNtfy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `required` | `boolean` | - |
| `body.databaseBackup` | `required` | `boolean` | - |
| `body.volumeBackup` | `required` | `boolean` | - |
| `body.dokployRestart` | `required` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `required` | `boolean` | - |
| `body.dockerCleanup` | `required` | `boolean` | - |
| `body.serverUrl` | `required` | `string` | minLength=1 |
| `body.topic` | `required` | `string` | minLength=1 |
| `body.accessToken` | `required` | `string` | - |
| `body.priority` | `required` | `number` | minimum=1 |

### `notification-createPushover`

- Method: `POST`
- Path: `/notification.createPushover`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.userKey` | `required` | `string` | minLength=1 |
| `body.apiToken` | `required` | `string` | minLength=1 |
| `body.priority` | `optional` | `number` | minimum=-2; maximum=2; default=0 |
| `body.retry` | `optional` | `number | null` | - |
| `body.expire` | `optional` | `number | null` | - |

### `notification-createResend`

- Method: `POST`
- Path: `/notification.createResend`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `required` | `boolean` | - |
| `body.databaseBackup` | `required` | `boolean` | - |
| `body.volumeBackup` | `required` | `boolean` | - |
| `body.dokployRestart` | `required` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `required` | `boolean` | - |
| `body.dockerCleanup` | `required` | `boolean` | - |
| `body.serverThreshold` | `required` | `boolean` | - |
| `body.apiKey` | `required` | `string` | minLength=1 |
| `body.fromAddress` | `required` | `string` | minLength=1 |
| `body.toAddresses` | `required` | `array<string>` | - |
| `body.toAddresses[]` | `required` | `string` | - |

### `notification-createSlack`

- Method: `POST`
- Path: `/notification.createSlack`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `required` | `boolean` | - |
| `body.databaseBackup` | `required` | `boolean` | - |
| `body.volumeBackup` | `required` | `boolean` | - |
| `body.dokployRestart` | `required` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `required` | `boolean` | - |
| `body.dockerCleanup` | `required` | `boolean` | - |
| `body.serverThreshold` | `required` | `boolean` | - |
| `body.webhookUrl` | `required` | `string` | minLength=1 |
| `body.channel` | `required` | `string` | - |

### `notification-createTeams`

- Method: `POST`
- Path: `/notification.createTeams`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `required` | `boolean` | - |
| `body.databaseBackup` | `required` | `boolean` | - |
| `body.volumeBackup` | `required` | `boolean` | - |
| `body.dokployRestart` | `required` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `required` | `boolean` | - |
| `body.dockerCleanup` | `required` | `boolean` | - |
| `body.serverThreshold` | `required` | `boolean` | - |
| `body.webhookUrl` | `required` | `string` | minLength=1 |

### `notification-createTelegram`

- Method: `POST`
- Path: `/notification.createTelegram`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `required` | `boolean` | - |
| `body.databaseBackup` | `required` | `boolean` | - |
| `body.volumeBackup` | `required` | `boolean` | - |
| `body.dokployRestart` | `required` | `boolean` | - |
| `body.name` | `required` | `string` | - |
| `body.appDeploy` | `required` | `boolean` | - |
| `body.dockerCleanup` | `required` | `boolean` | - |
| `body.serverThreshold` | `required` | `boolean` | - |
| `body.botToken` | `required` | `string` | minLength=1 |
| `body.chatId` | `required` | `string` | minLength=1 |
| `body.messageThreadId` | `required` | `string` | - |

### `notification-getEmailProviders`

- Method: `GET`
- Path: `/notification.getEmailProviders`
- Auth: `apiKey`
- Input: `none`

No parameters or request body fields.

### `notification-one`

- Method: `GET`
- Path: `/notification.one`
- Auth: `apiKey`
- Input: `params`

| Param | In | Required | Type | Notes |
|---|---|---|---|---|
| `notificationId` | `query` | yes | `string` | minLength=1 |

### `notification-receiveNotification`

- Method: `POST`
- Path: `/notification.receiveNotification`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.ServerType` | `optional` | `enum(Dokploy, Remote)` | default=Dokploy |
| `body.Type` | `required` | `enum(Memory, CPU)` | - |
| `body.Value` | `required` | `number` | - |
| `body.Threshold` | `required` | `number` | - |
| `body.Message` | `required` | `string` | - |
| `body.Timestamp` | `required` | `string` | - |
| `body.Token` | `required` | `string` | - |

### `notification-remove`

- Method: `POST`
- Path: `/notification.remove`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.notificationId` | `required` | `string` | minLength=1 |

### `notification-testCustomConnection`

- Method: `POST`
- Path: `/notification.testCustomConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.endpoint` | `required` | `string` | minLength=1 |
| `body.headers` | `optional` | `object` | - |

### `notification-testDiscordConnection`

- Method: `POST`
- Path: `/notification.testDiscordConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.webhookUrl` | `required` | `string` | minLength=1 |
| `body.decoration` | `optional` | `boolean` | - |

### `notification-testEmailConnection`

- Method: `POST`
- Path: `/notification.testEmailConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.smtpServer` | `required` | `string` | minLength=1 |
| `body.smtpPort` | `required` | `number` | minimum=1 |
| `body.username` | `required` | `string` | minLength=1 |
| `body.password` | `required` | `string` | minLength=1 |
| `body.toAddresses` | `required` | `array<string>` | - |
| `body.toAddresses[]` | `required` | `string` | - |
| `body.fromAddress` | `required` | `string` | minLength=1 |

### `notification-testGotifyConnection`

- Method: `POST`
- Path: `/notification.testGotifyConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverUrl` | `required` | `string` | minLength=1 |
| `body.appToken` | `required` | `string` | minLength=1 |
| `body.priority` | `required` | `number` | minimum=1 |
| `body.decoration` | `optional` | `boolean` | - |

### `notification-testLarkConnection`

- Method: `POST`
- Path: `/notification.testLarkConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.webhookUrl` | `required` | `string` | minLength=1 |

### `notification-testNtfyConnection`

- Method: `POST`
- Path: `/notification.testNtfyConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.serverUrl` | `required` | `string` | minLength=1 |
| `body.topic` | `required` | `string` | minLength=1 |
| `body.accessToken` | `required` | `string` | - |
| `body.priority` | `required` | `number` | minimum=1 |

### `notification-testPushoverConnection`

- Method: `POST`
- Path: `/notification.testPushoverConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.userKey` | `required` | `string` | minLength=1 |
| `body.apiToken` | `required` | `string` | minLength=1 |
| `body.priority` | `required` | `number` | minimum=-2; maximum=2 |
| `body.retry` | `optional` | `number | null` | - |
| `body.expire` | `optional` | `number | null` | - |

### `notification-testResendConnection`

- Method: `POST`
- Path: `/notification.testResendConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.apiKey` | `required` | `string` | minLength=1 |
| `body.fromAddress` | `required` | `string` | minLength=1 |
| `body.toAddresses` | `required` | `array<string>` | - |
| `body.toAddresses[]` | `required` | `string` | - |

### `notification-testSlackConnection`

- Method: `POST`
- Path: `/notification.testSlackConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.webhookUrl` | `required` | `string` | minLength=1 |
| `body.channel` | `required` | `string` | - |

### `notification-testTeamsConnection`

- Method: `POST`
- Path: `/notification.testTeamsConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.webhookUrl` | `required` | `string` | minLength=1 |

### `notification-testTelegramConnection`

- Method: `POST`
- Path: `/notification.testTelegramConnection`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.botToken` | `required` | `string` | minLength=1 |
| `body.chatId` | `required` | `string` | minLength=1 |
| `body.messageThreadId` | `required` | `string` | - |

### `notification-updateCustom`

- Method: `POST`
- Path: `/notification.updateCustom`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.endpoint` | `optional` | `string` | minLength=1 |
| `body.headers` | `optional` | `object` | - |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.customId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

### `notification-updateDiscord`

- Method: `POST`
- Path: `/notification.updateDiscord`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.webhookUrl` | `optional` | `string` | minLength=1 |
| `body.decoration` | `optional` | `boolean` | - |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.discordId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

### `notification-updateEmail`

- Method: `POST`
- Path: `/notification.updateEmail`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.smtpServer` | `optional` | `string` | minLength=1 |
| `body.smtpPort` | `optional` | `number` | minimum=1 |
| `body.username` | `optional` | `string` | minLength=1 |
| `body.password` | `optional` | `string` | minLength=1 |
| `body.fromAddress` | `optional` | `string` | minLength=1 |
| `body.toAddresses` | `optional` | `array<string>` | - |
| `body.toAddresses[]` | `optional` | `string` | - |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.emailId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

### `notification-updateGotify`

- Method: `POST`
- Path: `/notification.updateGotify`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverUrl` | `optional` | `string` | minLength=1 |
| `body.appToken` | `optional` | `string` | minLength=1 |
| `body.priority` | `optional` | `number` | minimum=1 |
| `body.decoration` | `optional` | `boolean` | - |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.gotifyId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

### `notification-updateLark`

- Method: `POST`
- Path: `/notification.updateLark`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.webhookUrl` | `optional` | `string` | minLength=1 |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.larkId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

### `notification-updateNtfy`

- Method: `POST`
- Path: `/notification.updateNtfy`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverUrl` | `optional` | `string` | minLength=1 |
| `body.topic` | `optional` | `string` | minLength=1 |
| `body.accessToken` | `optional` | `string` | - |
| `body.priority` | `optional` | `number` | minimum=1 |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.ntfyId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

### `notification-updatePushover`

- Method: `POST`
- Path: `/notification.updatePushover`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.pushoverId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |
| `body.userKey` | `optional` | `string` | minLength=1 |
| `body.apiToken` | `optional` | `string` | minLength=1 |
| `body.priority` | `optional` | `number` | minimum=-2; maximum=2 |
| `body.retry` | `optional` | `number | null` | - |
| `body.expire` | `optional` | `number | null` | - |
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |

### `notification-updateResend`

- Method: `POST`
- Path: `/notification.updateResend`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.apiKey` | `optional` | `string` | minLength=1 |
| `body.fromAddress` | `optional` | `string` | minLength=1 |
| `body.toAddresses` | `optional` | `array<string>` | - |
| `body.toAddresses[]` | `optional` | `string` | - |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.resendId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

### `notification-updateSlack`

- Method: `POST`
- Path: `/notification.updateSlack`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.webhookUrl` | `optional` | `string` | minLength=1 |
| `body.channel` | `optional` | `string` | - |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.slackId` | `required` | `string` | - |
| `body.organizationId` | `optional` | `string` | - |

### `notification-updateTeams`

- Method: `POST`
- Path: `/notification.updateTeams`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.webhookUrl` | `optional` | `string` | minLength=1 |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.teamsId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

### `notification-updateTelegram`

- Method: `POST`
- Path: `/notification.updateTelegram`
- Auth: `apiKey`
- Input: `json`

| Body field | Required | Type | Notes |
|---|---|---|---|
| `body.appBuildError` | `optional` | `boolean` | - |
| `body.databaseBackup` | `optional` | `boolean` | - |
| `body.volumeBackup` | `optional` | `boolean` | - |
| `body.dokployRestart` | `optional` | `boolean` | - |
| `body.name` | `optional` | `string` | - |
| `body.appDeploy` | `optional` | `boolean` | - |
| `body.dockerCleanup` | `optional` | `boolean` | - |
| `body.serverThreshold` | `optional` | `boolean` | - |
| `body.botToken` | `optional` | `string` | minLength=1 |
| `body.chatId` | `optional` | `string` | minLength=1 |
| `body.messageThreadId` | `optional` | `string` | - |
| `body.notificationId` | `required` | `string` | minLength=1 |
| `body.telegramId` | `required` | `string` | minLength=1 |
| `body.organizationId` | `optional` | `string` | - |

## Invocation template

```bash
curl -X POST \
  "https://dokploy.example.com/api<endpoint>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -d '{"key":"value"}'
```
