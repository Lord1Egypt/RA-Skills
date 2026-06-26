"""Configuration for chatgpt-skill."""

import os
from pathlib import Path


SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
BROWSER_STATE_DIR = DATA_DIR / "browser_state"
BROWSER_PROFILE_DIR = BROWSER_STATE_DIR / "browser_profile"
STATE_FILE = BROWSER_STATE_DIR / "state.json"
AUTH_INFO_FILE = DATA_DIR / "auth_info.json"
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
SESSION_RUNTIME_DIR = DATA_DIR / "session_runtime"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"

CHATGPT_PUBLIC_URL = "https://chatgpt.com"
CHATGPT_ALT_URL = "https://chat.openai.com"
CHATGPT_BASE_URL = CHATGPT_PUBLIC_URL

CHATGPT_PROXY_URL_ENV = "CHATGPT_PROXY_URL"
CHATGPT_PROXY_BYPASS_ENV = "CHATGPT_PROXY_BYPASS"
CHATGPT_ACCOUNT_EMAIL_ENV = "CHATGPT_ACCOUNT_EMAIL"

APP_READY_SELECTORS = [
    "#prompt-textarea",
    "textarea[placeholder*='Message']",
    "div[contenteditable='true'][data-testid='composer-rich-text-input']",
    "div[contenteditable='true'].ProseMirror",
    "button[data-testid='new-chat-button']",
]

COMPOSER_SELECTORS = [
    "#prompt-textarea",
    "textarea[placeholder*='Message']",
    "div[contenteditable='true'][data-testid='composer-rich-text-input']",
    "div[contenteditable='true'].ProseMirror",
]

SEND_BUTTON_SELECTORS = [
    "button[data-testid='send-button']",
    "button[aria-label*='Send']",
    "button[aria-label*='发送']",
]

STOP_BUTTON_SELECTORS = [
    "button[data-testid='stop-button']",
    "button[aria-label*='Stop']",
    "button[aria-label*='停止']",
]

NEW_CHAT_SELECTORS = [
    "button[data-testid='new-chat-button']",
    "a[data-testid='new-chat-button']",
    "a[data-testid='create-new-chat-button']",
    "button[aria-label*='New chat']",
    "a[href='/'][data-testid='create-new-chat-button']",
    "a[href='/']",
]

MODEL_PICKER_SELECTORS = [
    "button[data-testid*='model']",
    "button[aria-haspopup='menu']",
    "button[aria-haspopup='listbox']",
]

MODEL_MENU_ITEM_SELECTORS = [
    "[role='menuitem']",
    "[role='option']",
    "button",
    "div",
]

EXTENDED_THINKING_SELECTORS = [
    "button",
    "[role='button']",
    "div[role='button']",
]

ASSISTANT_MESSAGE_SELECTORS = [
    "[data-message-author-role='assistant'] .markdown",
    "[data-message-author-role='assistant']",
    "article[data-testid*='conversation-turn'] [data-message-author-role='assistant']",
]

USER_MESSAGE_SELECTORS = [
    "[data-message-author-role='user']",
    "article[data-testid*='conversation-turn'] [data-message-author-role='user']",
]

LOGIN_URL_HINTS = [
    "/auth/login",
    "/auth/signin",
    "login",
    "signin",
]

LOGIN_TEXT_HINTS = [
    "log in",
    "sign up",
    "continue with google",
    "continue with apple",
    "continue with email",
    "welcome back",
]

ACCOUNT_CHOOSER_TEXT_HINTS = [
    "choose an account",
    "choose how you'd like to continue",
    "continue as",
    "pick an account",
    "select an account",
]

VERIFICATION_TEXT_HINTS = [
    "verify you are human",
    "verification",
    "security check",
    "enter code",
    "two-factor",
    "authenticator",
    "captcha",
    "arkose",
]

NETWORK_ERROR_TEXT_HINTS = [
    "network error",
    "something went wrong",
    "unable to load",
    "request timed out",
]

RESPONSE_ERROR_TEXT_HINTS = [
    "something went wrong while generating the response",
    "if this issue persists please contact us through our help center",
]

RETRY_BUTTON_SELECTORS = [
    "button[data-testid='retry-button']",
    "button[data-testid='regenerate-button']",
    "button:has-text('Try again')",
    "button:has-text('Regenerate')",
    "button:has-text('Continue generating')",
    "button:has-text('重试')",
    "button:has-text('重新生成')",
    "button:has-text('继续生成')",
]

NON_CRITICAL_OVERLAY_SELECTORS = [
    "#modal-no-auth-new-chat",
    "[data-testid='modal-no-auth-new-chat']",
]

BROWSER_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--no-first-run",
    "--no-default-browser-check",
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

LOGIN_TIMEOUT_MINUTES = 10
PAGE_LOAD_TIMEOUT_MS = 30000
UI_SHORT_TIMEOUT_MS = 3000
UI_MEDIUM_TIMEOUT_MS = 8000
UI_LONG_TIMEOUT_MS = 20000
RESPONSE_TIMEOUT_SECONDS = int(os.getenv("CHATGPT_RESPONSE_TIMEOUT_SECONDS", "180"))
