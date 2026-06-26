# Email Bridge Design Document

## Overview

Email Bridge is a minimal personal email middleware designed for AI assistants. It provides real-time email monitoring, verification code extraction, and seamless integration with OpenClaw for push notifications.

**Current Version**: 0.6.1  
**Supported Providers**: Gmail (API), QQ Mail (IMAP), NetEase Mail (IMAP)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        OpenClaw Integration                      │
│              Push notifications via `openclaw system event`      │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ notify
┌─────────────────────────────────────────────────────────────────┐
│                    Daemon (daemon.py)                            │
│         Background monitoring with IMAP IDLE + polling          │
│         Keepalive (60s) + sync retry (3x) for reliability       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CLI (cli.py)                                │
│                    Click-based commands                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Service Layer (service.py)                       │
│         Business logic, orchestration, sync                      │
└─────────────────────────────────────────────────────────────────┘
         │                              │               │
         ▼                              ▼               ▼
┌──────────────────┐    ┌─────────────────────────────────────┐
│  Database (db.py) │    │        Adapters (adapters/)        │
│     SQLite        │    │       Provider interface            │
└──────────────────┘    └─────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
              ┌─────────┐         ┌─────────┐         ┌─────────┐
              │  Gmail  │         │   IMAP  │         │  Mock   │
              │  API    │         │ QQ/Net  │         │ Adapter │
              └─────────┘         └─────────┘         └─────────┘
```

---

## Core Components

### 1. Data Models (`models.py`)

Pydantic models for type safety:

- **Account**: Email account configuration and metadata
- **Message**: Email message with optional cached content
- **EmailCategory**: Enum for message classification (verification, security, transactional, promotion, subscription, spam_like, normal)
- **EmailProvider**: Supported providers (gmail, qq, netease, mock)

### 2. Database Layer (`db.py`)

SQLite-backed storage with simple schema:

**accounts table:**
- id, email, provider, status, display_name, config, timestamps

**messages table:**
- id, account_id, message_id, subject, sender, recipients
- received_at, is_read, is_starred, category
- preview, body_text, body_html (cached content)
- provider_data (provider-specific raw data)

### 3. Service Layer (`service.py`)

Clean API layer providing:
- Account CRUD operations
- Message listing, searching, retrieval
- Sync orchestration (pull from adapters to DB)
- Statistics

### 4. Adapter Interface (`adapters/base.py`)

Abstract base class for provider implementations:

```python
class BaseAdapter(ABC):
    @property
    @abstractmethod
    def provider(self) -> EmailProvider: ...
    
    @abstractmethod
    def fetch_messages(self, account, options) -> Iterator[RawMessage]: ...
    
    @abstractmethod
    def get_message(self, account, message_id) -> RawMessage: ...
    
    def authenticate(self, account) -> bool: ...
    def test_connection(self, account) -> bool: ...
```

### 5. Gmail Adapter (`adapters/gmail.py`)

Real Gmail API integration using OAuth2:
- **Authentication**: OAuth2 with automatic token caching
- **Recent-window sync**: Configurable days back and message limit

### 6. IMAP Adapter (`adapters/imap.py`)

IMAP integration for QQ Mail and NetEase Mail:
- **QQ Mail**: `imap.qq.com:993` with app-specific password
- **NetEase**: `imap.163.com`, `imap.126.com`, `imap.yeah.net` with authorization code
- **Real-time monitoring**: IMAP IDLE for push notifications
- **Fallback polling**: For Gmail (no IDLE support)

### 7. Category Detection (`categories.py`)

**Subject-only classification** for fast, reliable categorization:

```python
class EmailCategory(str, Enum):
    VERIFICATION = "verification"    # Verification codes, activation links
    SECURITY = "security"            # Security alerts, login warnings
    TRANSACTIONAL = "transactional"  # Order confirmations, receipts
    PROMOTION = "promotion"          # Marketing emails, promotions, rewards
    SUBSCRIPTION = "subscription"    # Newsletters, digests
    SPAM_LIKE = "spam_like"          # Likely spam/promotional
    NORMAL = "normal"                # Regular personal/business email
```

**Keyword pools** (more specific phrases first, subject-only matching):

| Category | Example Keywords |
|----------|-----------------|
| verification | 验证码, verification code, OTP, activate your account, 绑定邮箱 |
| security | 安全提醒, security alert, login attempt, password reset |
| transactional | 订单确认, order #, 发货通知, receipt, invoice |
| promotion | 奖励, 优惠, promo, discount, USDT, BTC |
| subscription | newsletter, unsubscribe, 订阅, 退订 |
| spam_like | 恭喜您中奖, winner, click here now, FREE |

**Design principle**: Only match against subject line (not body) for faster classification and lower false positive rate.

### 8. Extraction Module (`extraction.py`)

**Strict verification code extraction**:

1. **Context-aware only**: Codes must appear near verification keywords
2. **No standalone extraction**: Prevents false positives (addresses, order numbers)
3. **Address pattern exclusion**: STE, ST, AVE, BLVD etc. filtered out

**Patterns matched**:
- Numeric codes (4-8 digits) near "验证码", "code is", "OTP"
- Alphanumeric codes near verification keywords
- Chinese patterns: "验证码：123456"

**Action link extraction**:
- verify/confirm/activate links
- reset password links
- unsubscribe links

### 9. Sanitization (`sanitize.py`)

**Content cleaning for notifications**:

1. **Invisible character removal**: Zero-width spaces (U+200B-U+200F), BOM (U+FEFF), etc.
2. **Prompt injection prevention**: Remove dangerous patterns (ignore instructions, role-play, etc.)
3. **Control character filtering**: Strip non-printable characters
4. **Whitespace normalization**: Collapse multiple spaces
5. **Length limiting**: Truncate with ellipsis

**Why it matters**: HTML emails often contain invisible formatting characters that appear as garbage in plain text output. The sanitization layer ensures clean, readable notifications.

### 10. Daemon (`daemon.py`)

Background service for real-time email monitoring:

**Key Features**:
- **IMAP IDLE**: Real-time push for QQ/NetEase (timeout = 60s keepalive)
- **Polling**: Gmail fallback (configurable interval, default 5 min)
- **Sync retry**: Up to 3 retries on sync failure
- **OpenClaw integration**: Push notifications via `openclaw system event`

**Configuration** (`~/.email-bridge/config.json`):
```json
{
  "daemon": {
    "poll_interval": 300,
    "notify_openclaw": true,
    "notification": {
      "include_body": true,
      "body_max_length": 500,
      "include_verification_codes": true,
      "include_links": false
    }
  }
}
```

**Notification Format**:
- 🔐 verification: Emphasizes verification codes
- ⚠️ security: Warning icon + body summary
- 📦 transactional: Order/shipping notifications
- 🎁 promotion: Marketing/promotional content
- 📰 subscription: Simplified display
- 🚫 spam_like: Marked as "疑似垃圾"
- normal: Standard format

---

## Data Flow

### Real-time Monitoring Flow

```
1. Daemon starts → connects to IMAP/loads Gmail poller
2. IMAP IDLE waits for new mail (keepalive every 60s)
3. New mail detected → sync with retry (up to 3x)
4. Extract verification codes (if keywords present)
5. Format notification based on category
6. Push to OpenClaw via `openclaw system event`
```

### Sync Process

```
1. CLI calls `service.sync_account(account_id)`
2. Service fetches adapter for account's provider
3. Adapter yields `RawMessage` objects
4. Service classifies by subject (category detection)
5. Service extracts verification codes (if applicable)
6. Service persists to SQLite
```

---

## Design Decisions

1. **Subject-only classification**: Fast, reliable, no body parsing needed
2. **Strict code extraction**: Context-aware only, prevents false positives
3. **Keepalive + retry**: Handles network flakiness gracefully
4. **SQLite**: Zero-config, sufficient for personal use
5. **Pydantic**: Type safety without ORM overhead
6. **Adapter pattern**: Clean separation for multiple providers
7. **OpenClaw push**: Real-time notifications to AI assistant
8. **Daemon mode**: Background service with IMAP IDLE

---

## Key Improvements (v0.6.1)

### Category Detection
- **Subject-only**: No body scanning for classification
- **Expanded keywords**: Verification, security, transactional categories fully populated
- **Chinese + English**: Bilingual keyword support
- **Specific phrases**: Avoid single-character keywords (e.g., "确认" alone is too broad)

### Verification Code Extraction
- **Context-required**: Codes must appear near verification keywords
- **No standalone extraction**: Removed guessing of isolated numbers
- **Address exclusion**: Filter out STE, ST, AVE patterns
- **Lower false positive rate**: Glassdoor addresses no longer misidentified

### Daemon Reliability
- **Keepalive**: 60-second IDLE timeout acts as heartbeat
- **Sync retry**: 3 retries with 2-second delay between attempts
- **Reconnection**: Automatic reconnect on connection errors
- **Graceful degradation**: If sync fails, logs error and continues monitoring

---

## Configuration

### Account Setup

```bash
# Add Gmail account (OAuth2)
email-bridge accounts add --provider gmail --email user@gmail.com

# Add QQ Mail (app-specific password)
email-bridge accounts add --provider qq --email user@qq.com --password <app-password>

# Add NetEase (authorization code)
email-bridge accounts add --provider netease --email user@163.com --password <auth-code>
```

### Daemon Management

```bash
# Start daemon in background
email-bridge daemon start -d

# Check status
email-bridge daemon status

# Stop daemon
email-bridge daemon stop
```

---

## Future Considerations

- **Attachment handling**: Download and process attachments
- **Full-text search**: SQLite FTS5 for better search
- **Multi-user support**: Account isolation for teams
- **Web UI**: FastAPI backend with React/Vue frontend
- **LLM classification**: Replace keyword matching with ML