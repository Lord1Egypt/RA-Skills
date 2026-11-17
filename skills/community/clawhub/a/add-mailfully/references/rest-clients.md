# Mailfully REST clients

One send helper per language for apps that cannot use the Node SDK, then Django and Rails adapters.
Use the Node SDK (`mailfully`) only when the project runs Node 24 or later. Everything else uses one of
these helpers.

Every helper here:

- reads the key from the `MAILFULLY_API_KEY` environment variable at call time;
- POSTs JSON to `https://api.mailfully.com/v1/emails` with snake_case wire keys (`reply_to`,
  `scheduled_at`; the attachment field `contentType` is the one camelCase exception);
- returns the email `id` and `status` on success. `status` is `queued` or `canceled`; `canceled` means
  every recipient was suppressed and nothing will be sent, so log it or report it;
- raises on any non-2xx answer with the API's `error.type` and `error.message` (plus `param` when the
  API names a field). The TypeScript and Python errors also carry the `retry-after` seconds a 429
  sends (`retryAfterSec`, `retry_after`), and those two helpers take an optional idempotency key
  (sent as the `Idempotency-Key` header), so a per-recipient loop can wait and resend safely.

The request body is described in `api-essentials.md`. A helper never logs or prints the key.

## TypeScript or JavaScript with `fetch` (Node 18 or later)

Use this when the project's Node is older than 24 (Node 18, 20 or 22), where the SDK will not run,
and in a CommonJS project on any Node: the SDK loads only through `import`, so `require("mailfully")`
(or TypeScript compiled to CommonJS) fails with `ERR_PACKAGE_PATH_NOT_EXPORTED`. Save as
`lib/mailfully.ts`. In a plain JavaScript CommonJS project, drop the types, save it as
`lib/mailfully.js` and end it with `module.exports = { sendEmail, MailfullyApiError };` in place of
the `export` keywords.

```ts mailfully-rest
const MAILFULLY_URL = "https://api.mailfully.com/v1/emails";

export interface MailfullyAttachment {
  filename: string;
  /** Bare base64, never a data: URI. */
  content: string;
  contentType?: string;
  cid?: string;
}

/** The wire body: snake_case keys exactly as the API takes them. */
export interface MailfullyEmail {
  from: string;
  to: string | string[];
  cc?: string | string[];
  bcc?: string | string[];
  reply_to?: string | string[];
  subject?: string;
  html?: string;
  text?: string;
  headers?: Record<string, string>;
  attachments?: MailfullyAttachment[];
  tags?: { name: string; value: string }[];
  scheduled_at?: string;
  template?: { id: string; variables?: Record<string, unknown> };
}

export class MailfullyApiError extends Error {
  readonly status: number;
  readonly type: string;
  readonly param: string | undefined;
  /** Seconds from the `retry-after` header (sent with a 429), else null. */
  readonly retryAfterSec: number | null;

  constructor(status: number, type: string, message: string, param?: string, retryAfterSec: number | null = null) {
    super(`${type}: ${message}`);
    this.name = "MailfullyApiError";
    this.status = status;
    this.type = type;
    this.param = param;
    this.retryAfterSec = retryAfterSec;
  }
}

export async function sendEmail(
  email: MailfullyEmail,
  opts: { idempotencyKey?: string } = {},
): Promise<{ id: string; status: "queued" | "canceled" }> {
  const apiKey = process.env.MAILFULLY_API_KEY;
  if (!apiKey) throw new Error("MAILFULLY_API_KEY is not set");

  const headers: Record<string, string> = { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" };
  if (opts.idempotencyKey) headers["Idempotency-Key"] = opts.idempotencyKey;
  const res = await fetch(MAILFULLY_URL, {
    method: "POST",
    headers,
    body: JSON.stringify(email),
    signal: AbortSignal.timeout(10_000),
  });
  const text = await res.text();
  let body: unknown = null;
  try {
    body = JSON.parse(text);
  } catch {
    // not JSON; handled below
  }
  if (!res.ok) {
    const err = (body as { error?: { type?: string; message?: string; param?: string } } | null)?.error;
    const retryAfter = Number(res.headers.get("retry-after"));
    throw new MailfullyApiError(
      res.status,
      err?.type ?? "http_error",
      err?.message ?? text,
      err?.param,
      Number.isFinite(retryAfter) && retryAfter > 0 ? retryAfter : null,
    );
  }
  const ok = body as { id: string; status: "queued" | "canceled" };
  return { id: ok.id, status: ok.status };
}

// Example call.
export function sendWelcome(to: string) {
  return sendEmail({
    from: "Acme <hello@example.com>",
    to,
    reply_to: "support@example.com",
    subject: "Welcome to Acme",
    html: "<p>Welcome aboard.</p>",
    text: "Welcome aboard.",
  });
}
```

## Python (standard library)

`urllib.request` is in the standard library, so this adds no dependency. If the project already uses
`requests` or `httpx`, they are drop-in replacements for the HTTP call; keep the body, headers and
error handling the same. Save as `mailfully_client.py`.

```python mailfully-rest
import json
import os
import urllib.error
import urllib.request

MAILFULLY_URL = "https://api.mailfully.com/v1/emails"


class MailfullyError(Exception):
    def __init__(self, status, error_type, message, param=None, retry_after=None):
        super().__init__(f"{error_type}: {message}")
        self.status = status
        self.type = error_type
        self.param = param
        # Seconds from the retry-after header (sent with a 429), else None.
        self.retry_after = retry_after


def _retry_after(exc):
    try:
        seconds = int(exc.headers.get("retry-after", ""))
    except (TypeError, ValueError):
        return None
    return seconds if seconds > 0 else None


def send_email(payload, timeout=10, idempotency_key=None):
    """POST one email. `payload` is a dict with wire keys ("from", "to", "reply_to", ...).

    Returns (id, status). status is "queued" or "canceled" (every recipient suppressed).
    """
    api_key = os.environ.get("MAILFULLY_API_KEY")
    if not api_key:
        raise RuntimeError("MAILFULLY_API_KEY is not set")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    request = urllib.request.Request(
        MAILFULLY_URL,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.load(response)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            error = json.loads(raw)["error"]
        except (ValueError, KeyError, TypeError):
            raise MailfullyError(exc.code, "http_error", raw, None, _retry_after(exc)) from None
        raise MailfullyError(
            exc.code,
            error.get("type"),
            error.get("message"),
            error.get("param"),
            _retry_after(exc),
        ) from None
    return body["id"], body["status"]


def send_welcome(to):
    return send_email({
        "from": "Acme <hello@example.com>",
        "to": to,
        "reply_to": "support@example.com",
        "subject": "Welcome to Acme",
        "html": "<p>Welcome aboard.</p>",
        "text": "Welcome aboard.",
    })
```

## Ruby (`net/http`)

Standard library only. Save as `lib/mailfully_client.rb`.

```ruby mailfully-rest
require "json"
require "net/http"
require "uri"

module MailfullyClient
  URL = URI("https://api.mailfully.com/v1/emails")

  class Error < StandardError
    attr_reader :status, :type, :param

    def initialize(status, type, message, param = nil)
      super("#{type}: #{message}")
      @status = status
      @type = type
      @param = param
    end
  end

  # payload is a Hash with string wire keys ("from", "to", "reply_to", ...).
  # Returns [id, status]; status is "queued" or "canceled" (every recipient suppressed).
  def self.send_email(payload)
    api_key = ENV.fetch("MAILFULLY_API_KEY") { raise "MAILFULLY_API_KEY is not set" }
    request = Net::HTTP::Post.new(URL)
    request["Authorization"] = "Bearer #{api_key}"
    request["Content-Type"] = "application/json"
    request.body = JSON.generate(payload)

    response = Net::HTTP.start(URL.host, URL.port, use_ssl: true, open_timeout: 5, read_timeout: 10) do |http|
      http.request(request)
    end

    body = begin
      JSON.parse(response.body.to_s)
    rescue JSON::ParserError
      {}
    end
    unless response.is_a?(Net::HTTPSuccess)
      error = body.is_a?(Hash) ? (body["error"] || {}) : {}
      raise Error.new(response.code.to_i, error["type"] || "http_error", error["message"] || response.body, error["param"])
    end
    [body["id"], body["status"]]
  end

  def self.send_welcome(to)
    send_email(
      "from" => "Acme <hello@example.com>",
      "to" => to,
      "reply_to" => "support@example.com",
      "subject" => "Welcome to Acme",
      "html" => "<p>Welcome aboard.</p>",
      "text" => "Welcome aboard."
    )
  end
end
```

## Go (`net/http`)

Standard library only. The struct's json tags are the wire names. Save as `mailfully/mailfully.go`.

```go mailfully-rest
package mailfully

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

const sendURL = "https://api.mailfully.com/v1/emails"

type Tag struct {
	Name  string `json:"name"`
	Value string `json:"value"`
}

type Attachment struct {
	Filename    string `json:"filename"`
	Content     string `json:"content"` // bare base64, never a data: URI
	ContentType string `json:"contentType,omitempty"`
	CID         string `json:"cid,omitempty"`
}

type Template struct {
	ID        string         `json:"id"`
	Variables map[string]any `json:"variables,omitempty"`
}

type Email struct {
	From        string            `json:"from"`
	To          []string          `json:"to"`
	Cc          []string          `json:"cc,omitempty"`
	Bcc         []string          `json:"bcc,omitempty"`
	ReplyTo     []string          `json:"reply_to,omitempty"`
	Subject     string            `json:"subject,omitempty"`
	HTML        string            `json:"html,omitempty"`
	Text        string            `json:"text,omitempty"`
	Headers     map[string]string `json:"headers,omitempty"`
	Attachments []Attachment      `json:"attachments,omitempty"`
	Tags        []Tag             `json:"tags,omitempty"`
	ScheduledAt string            `json:"scheduled_at,omitempty"`
	Template    *Template         `json:"template,omitempty"`
}

// APIError is a non-2xx answer from the API.
type APIError struct {
	Status  int
	Type    string
	Message string
	Param   string
}

func (e *APIError) Error() string {
	return fmt.Sprintf("mailfully %d %s: %s", e.Status, e.Type, e.Message)
}

var client = &http.Client{Timeout: 10 * time.Second}

// Send posts one email and returns its id and status ("queued", or "canceled" when every
// recipient was suppressed and nothing will be sent).
func Send(email Email) (id string, status string, err error) {
	apiKey := os.Getenv("MAILFULLY_API_KEY")
	if apiKey == "" {
		return "", "", errors.New("MAILFULLY_API_KEY is not set")
	}
	if email.To == nil {
		email.To = []string{} // the API refuses "to": null; [] is fine when cc or bcc is set
	}
	payload, err := json.Marshal(email)
	if err != nil {
		return "", "", err
	}
	req, err := http.NewRequest(http.MethodPost, sendURL, bytes.NewReader(payload))
	if err != nil {
		return "", "", err
	}
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	res, err := client.Do(req)
	if err != nil {
		return "", "", err
	}
	defer res.Body.Close()
	raw, err := io.ReadAll(res.Body)
	if err != nil {
		return "", "", err
	}

	// Untagged fields: encoding/json matches the response's keys case-insensitively.
	var out struct {
		ID     string
		Status string
		Error  *struct {
			Type    string
			Message string
			Param   string
		}
	}
	_ = json.Unmarshal(raw, &out)
	if res.StatusCode < 200 || res.StatusCode > 299 {
		if out.Error != nil {
			return "", "", &APIError{Status: res.StatusCode, Type: out.Error.Type, Message: out.Error.Message, Param: out.Error.Param}
		}
		return "", "", &APIError{Status: res.StatusCode, Type: "http_error", Message: string(raw)}
	}
	return out.ID, out.Status, nil
}

// SendWelcome is an example call.
func SendWelcome(to string) (string, string, error) {
	return Send(Email{
		From:    "Acme <hello@example.com>",
		To:      []string{to},
		ReplyTo: []string{"support@example.com"},
		Subject: "Welcome to Acme",
		HTML:    "<p>Welcome aboard.</p>",
		Text:    "Welcome aboard.",
	})
}
```

## PHP (`curl_*`)

Needs PHP 8.1 or later and the curl extension. Save as `src/mailfully.php`.

```php mailfully-rest
<?php

declare(strict_types=1);

final class MailfullyError extends RuntimeException
{
    public function __construct(
        public readonly int $status,
        public readonly string $type,
        string $message,
        public readonly ?string $param = null,
    ) {
        parent::__construct("{$type}: {$message}");
    }
}

/**
 * POST one email. $payload uses wire keys ('from', 'to', 'reply_to', ...).
 *
 * @return array{0: string, 1: string} [id, status]; status is 'queued' or 'canceled'
 */
function mailfully_send(array $payload): array
{
    $apiKey = getenv('MAILFULLY_API_KEY');
    if ($apiKey === false || $apiKey === '') {
        throw new RuntimeException('MAILFULLY_API_KEY is not set');
    }

    $ch = curl_init('https://api.mailfully.com/v1/emails');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 5,
        CURLOPT_TIMEOUT => 10,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer ' . $apiKey,
            'Content-Type: application/json',
        ],
        CURLOPT_POSTFIELDS => json_encode($payload, JSON_THROW_ON_ERROR),
    ]);
    $raw = curl_exec($ch);
    if ($raw === false) {
        throw new RuntimeException('Mailfully request failed: ' . curl_error($ch));
    }
    $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $body = json_decode((string) $raw, true);

    if ($status < 200 || $status > 299) {
        $error = is_array($body) && is_array($body['error'] ?? null) ? $body['error'] : [];
        throw new MailfullyError(
            $status,
            (string) ($error['type'] ?? 'http_error'),
            (string) ($error['message'] ?? $raw),
            isset($error['param']) ? (string) $error['param'] : null,
        );
    }

    return [(string) $body['id'], (string) $body['status']];
}

function mailfully_send_welcome(string $to): array
{
    return mailfully_send([
        'from' => 'Acme <hello@example.com>',
        'to' => $to,
        'reply_to' => 'support@example.com',
        'subject' => 'Welcome to Acme',
        'html' => '<p>Welcome aboard.</p>',
        'text' => 'Welcome aboard.',
    ]);
}
```

## Django: an email backend

Point Django's mail at Mailfully so every `send_mail`, `EmailMessage` and `EmailMultiAlternatives` in
the app goes through it unchanged. Save as `myapp/mail_backend.py` (use the real app name).

```python mailfully-rest
import base64
import json
import logging
import os
import urllib.error
import urllib.request
from email.message import Message
from email.utils import formataddr, getaddresses

from django.core.mail.backends.base import BaseEmailBackend

MAILFULLY_URL = "https://api.mailfully.com/v1/emails"
# Headers Django or Mailfully own. A Reply-To header is mapped to reply_to instead of forwarded.
SKIPPED_HEADERS = {"from", "sender", "return-path", "reply-to", "to", "cc", "bcc", "x-mailfully-mid"}

# The 202 status meaning every recipient was suppressed and nothing will be sent.
CANCELED = "canceled"

logger = logging.getLogger(__name__)


class MailfullyBackendError(Exception):
    def __init__(self, status, error_type, message, param=None):
        super().__init__(f"{error_type}: {message}")
        self.status = status
        self.type = error_type
        self.param = param


class MailfullySuppressedError(MailfullyBackendError):
    """Mailfully accepted the message but sent nothing: every recipient is suppressed."""


class MailfullyBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        sent = 0
        for message in email_messages:
            try:
                email_id, status = self._send(message)
                if status == CANCELED:
                    # Like Django's SMTP backend when every recipient is refused: an error unless
                    # fail_silently, and never counted as sent.
                    logger.warning("Mailfully canceled %s: every recipient is suppressed", email_id)
                    raise MailfullySuppressedError(
                        202, CANCELED, f"{email_id}: every recipient is suppressed, nothing was sent"
                    )
                sent += 1
            except Exception:
                if not self.fail_silently:
                    raise
        return sent

    def _send(self, message):
        payload = {
            "from": str(message.from_email),
            "to": [str(a) for a in message.to],
            "subject": str(message.subject),
        }
        if message.cc:
            payload["cc"] = [str(a) for a in message.cc]
        if message.bcc:
            payload["bcc"] = [str(a) for a in message.bcc]

        extra = message.extra_headers or {}
        reply_to = [str(a) for a in message.reply_to]
        if not reply_to:
            header = next((v for k, v in extra.items() if k.lower() == "reply-to"), None)
            if header:
                reply_to = [formataddr(pair) for pair in getaddresses([str(header)])]
        if reply_to:
            payload["reply_to"] = reply_to

        if getattr(message, "content_subtype", "plain") == "html":
            payload["html"] = str(message.body)
        else:
            payload["text"] = str(message.body)
        for content, mimetype in getattr(message, "alternatives", []):
            if mimetype == "text/html":
                payload["html"] = str(content)

        attachments = [self._attachment(item) for item in message.attachments]
        if attachments:
            payload["attachments"] = attachments

        headers = {
            str(name): str(value)
            for name, value in extra.items()
            if str(name).lower() not in SKIPPED_HEADERS
        }
        if headers:
            payload["headers"] = headers

        return self._post(payload)

    @staticmethod
    def _attachment(item):
        cid = None
        if isinstance(item, Message):
            filename = item.get_filename() or "attachment"
            content = item.get_payload(decode=True) or b""
            mimetype = item.get_content_type()
            content_id = item.get("Content-ID")
            if content_id:
                cid = str(content_id).strip().strip("<>")
        else:
            filename, content, mimetype = item
            if isinstance(content, str):
                content = content.encode("utf-8")
        attachment = {
            "filename": filename or "attachment",
            "content": base64.b64encode(content).decode("ascii"),
        }
        if mimetype:
            attachment["contentType"] = mimetype
        if cid:
            attachment["cid"] = cid
        return attachment

    @staticmethod
    def _post(payload):
        api_key = os.environ.get("MAILFULLY_API_KEY")
        if not api_key:
            raise RuntimeError("MAILFULLY_API_KEY is not set")
        request = urllib.request.Request(
            MAILFULLY_URL,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                body = json.load(response)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            try:
                error = json.loads(raw)["error"]
            except (ValueError, KeyError, TypeError):
                raise MailfullyBackendError(exc.code, "http_error", raw) from None
            raise MailfullyBackendError(
                exc.code, error.get("type"), error.get("message"), error.get("param")
            ) from None
        return body["id"], body["status"]
```

Then in `settings.py`, AFTER the app's existing mail settings, which stay as they are:

```python
import os

# EMAIL_PROVIDER=mailfully selects Mailfully. Unset, or any other value, keeps the EMAIL_BACKEND
# (and the SMTP or other settings) the app already had, so merging this changes nothing at runtime.
if os.environ.get("EMAIL_PROVIDER") == "mailfully":
    EMAIL_BACKEND = "myapp.mail_backend.MailfullyBackend"
```

Errors follow Django's own backends. With `fail_silently=False` (the default), a refused send raises
`MailfullyBackendError` with the API's `type` and `message`. A `canceled` send (every recipient
suppressed, nothing sent) is logged as a warning and raises `MailfullySuppressedError`, the way
Django's SMTP backend raises when every recipient is refused. With `fail_silently=True` both are
swallowed, and a canceled message is still logged and never counted in `send_messages`'s return.

## Rails: an Action Mailer delivery method

Every mailer keeps working unchanged. Save as `lib/mailfully_delivery.rb`.

```ruby mailfully-rest
require "base64"
require "json"
require "logger"
require "net/http"
require "uri"

class MailfullyDelivery
  URL = URI("https://api.mailfully.com/v1/emails")

  # Headers the mail object or Mailfully own; every other header is forwarded.
  SKIPPED_HEADERS = %w[
    from sender return-path to cc bcc reply-to subject date message-id mime-version
    content-type content-transfer-encoding content-id content-disposition x-mailfully-mid
  ].freeze

  class Error < StandardError
    attr_reader :status, :type, :param

    def initialize(status, type, message, param = nil)
      super("#{type}: #{message}")
      @status = status
      @type = type
      @param = param
    end
  end

  # Mailfully accepted the message but sent nothing: every recipient is suppressed.
  class SuppressedError < Error; end

  attr_accessor :settings

  def initialize(settings = {})
    @settings = settings
  end

  def deliver!(mail)
    payload = {
      "from" => addresses(mail, :from).first,
      "to" => addresses(mail, :to),
      "subject" => mail.subject.to_s
    }
    { "cc" => :cc, "bcc" => :bcc, "reply_to" => :reply_to }.each do |key, field|
      list = addresses(mail, field)
      payload[key] = list unless list.empty?
    end

    if mail.multipart?
      payload["html"] = mail.html_part.decoded if mail.html_part
      payload["text"] = mail.text_part.decoded if mail.text_part
    elsif mail.mime_type == "text/html"
      payload["html"] = mail.body.decoded
    else
      payload["text"] = mail.body.decoded
    end

    attachments = mail.attachments.map do |attachment|
      item = {
        "filename" => attachment.filename,
        "content" => Base64.strict_encode64(attachment.decoded),
        "contentType" => attachment.mime_type
      }
      item["cid"] = attachment.cid if attachment.inline?
      item
    end
    payload["attachments"] = attachments unless attachments.empty?

    headers = {}
    mail.header.fields.each do |field|
      next if SKIPPED_HEADERS.include?(field.name.to_s.downcase)
      headers[field.name.to_s] = field.value.to_s
    end
    payload["headers"] = headers unless headers.empty?

    email_id, status = post(payload)
    if status == "canceled"
      # Like an SMTP server refusing every recipient: Action Mailer raises this only when
      # raise_delivery_errors is on, so log it first to keep it visible either way.
      logger.warn("Mailfully canceled #{email_id}: every recipient is suppressed")
      raise SuppressedError.new(202, "canceled", "#{email_id}: every recipient is suppressed, nothing was sent")
    end
    email_id
  end

  private

  # Keeps display names: "Jane <jane@example.com>", not just the address.
  def addresses(mail, field)
    header = mail[field]
    return [] if header.nil?
    Array(header.respond_to?(:formatted) ? header.formatted : header.to_s)
  end

  def logger
    settings[:logger] || (defined?(Rails) ? Rails.logger : nil) || Logger.new($stderr)
  end

  def post(payload)
    api_key = ENV.fetch("MAILFULLY_API_KEY") { raise "MAILFULLY_API_KEY is not set" }
    request = Net::HTTP::Post.new(URL)
    request["Authorization"] = "Bearer #{api_key}"
    request["Content-Type"] = "application/json"
    request.body = JSON.generate(payload)

    response = Net::HTTP.start(URL.host, URL.port, use_ssl: true, open_timeout: 5, read_timeout: 10) do |http|
      http.request(request)
    end
    body = begin
      JSON.parse(response.body.to_s)
    rescue JSON::ParserError
      {}
    end
    unless response.is_a?(Net::HTTPSuccess)
      error = body.is_a?(Hash) ? (body["error"] || {}) : {}
      raise Error.new(response.code.to_i, error["type"] || "http_error", error["message"] || response.body, error["param"])
    end
    [body["id"], body["status"]]
  end
end
```

Register it in `config/initializers/mailfully.rb`:

```ruby
require Rails.root.join("lib/mailfully_delivery").to_s

ActionMailer::Base.add_delivery_method :mailfully, MailfullyDelivery
```

And select it in `config/environments/production.rb`, inside the `configure` block and AFTER the
app's existing `delivery_method` line, which stays as it is:

```ruby
# EMAIL_PROVIDER=mailfully selects Mailfully. Unset, or any other value, keeps the delivery method
# (and smtp_settings) the app already had, so merging this changes nothing at runtime.
config.action_mailer.delivery_method = :mailfully if ENV["EMAIL_PROVIDER"] == "mailfully"
```

Errors follow Action Mailer's own rule. With `config.action_mailer.raise_delivery_errors = true`, a
refused send raises `MailfullyDelivery::Error` carrying the API's `type` and `message`, and a
`canceled` send (every recipient suppressed, nothing sent) raises `MailfullyDelivery::SuppressedError`,
the way an SMTP server refusing every recipient does. With it off, Action Mailer swallows both, so the
delivery method logs every canceled send as a warning (to `Rails.logger`) before raising.
