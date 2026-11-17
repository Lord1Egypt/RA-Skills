# PHP, Go, Java, C#, Elixir and Rust

The flow is the same as in `SKILL.md` and `references/typescript.md`: a generated model per template, a background job
that saves the submission ID, looks for the submission before it creates one again after a failure with no ID
(`findSubmission` there), and checks `state`, a webhook handler that verifies signatures, a schema test and a
`validateSubmission` contract test. `testMode` below is the app's own setting, such as `DOCSPRING_TEST_MODE`
(DocSpring doesn't read it). This file has what differs in each client. Each SDK's repository
(`https://github.com/DocSpring/docspring-<language>`: `php`, `go`, `java`, `csharp`, `elixir`, `rust`) has an `AGENTS.md`
and `docs/` listing every method.

- [PHP](#php)
- [Go](#go)
- [Java](#java)
- [C#](#c)
- [Elixir](#elixir)
- [Rust](#rust)
- [Webhook signatures](#webhook-signatures)

## PHP

```bash
composer require "docspring/docspring:^4.2"
```

```php
$config = DocSpring\Configuration::getDefaultConfiguration(); // reads the DOCSPRING_* environment variables
$api = new DocSpring\Api\Client(null, $config);

$submission = $api->createSubmission($templateId, [
    'data' => json_decode(json_encode($invoice->to()), true), // the generated class's to() returns a stdClass
    'test' => getenv('DOCSPRING_TEST_MODE') !== 'false', // the app's own setting
    'metadata' => ['order_id' => $order->id],
], '1'); // version; wait is the next argument

if ($submission->getState() !== 'processed') { /* see SKILL.md, rule 5 */ }
$url = $submission->getFiles()->getPdf()->getDownloadUrl();
```

- Errors throw `DocSpring\ApiException`: `getCode()`, `getResponseBody()` (the JSON string: `json_decode` it for
  `error.code` and `error.submission_id`) and `getResponseHeaders()`. A request the API would reject throws
  `DocSpring\ValidationException` before it's sent.
- The region comes only from `DOCSPRING_REGION`. To set the host in code, give the full base URL:
  `$config->setHost('https://sync.api-eu.docspring.com/api/v2')`.
- Model code: `lang` `php`. The root class is named after the template (`Invoice`); `Invoice::from($stdClass)` reads
  one back.

## Go

```bash
go get github.com/docspring/docspring-go/v4
```

```go
import (
	"context"
	"encoding/json"
	"errors"
	"fmt"

	docspring "github.com/docspring/docspring-go/v4"
	"example.com/app/docspring/invoice" // the generated package
)

// apiClient := docspring.NewClient("", "") reads DOCSPRING_TOKEN_ID, DOCSPRING_TOKEN_SECRET and DOCSPRING_REGION
func generateInvoice(ctx context.Context, apiClient *docspring.ClientAPIService, templateID string,
	invoiceData invoice.Template, testMode bool) (*docspring.Submission, error) {
	raw, err := invoiceData.Marshal()
	if err != nil {
		return nil, err
	}
	var data map[string]interface{}
	if err := json.Unmarshal(raw, &data); err != nil {
		return nil, err
	}

	submission, httpRes, err := apiClient.CreateSubmission(ctx, templateID).
		Body(docspring.CreateSubmissionRequest{Data: data, Test: docspring.PtrBool(testMode)}).
		Version("1").
		Execute()
	var apiErr *docspring.GenericOpenAPIError
	if errors.As(err, &apiErr) && httpRes != nil {
		// httpRes.Header.Get("Retry-After"); apiErr.Body() is the raw JSON error body, with error.submission_id
		return nil, fmt.Errorf("DocSpring returned %d: %s", httpRes.StatusCode, apiErr.Body())
	}
	if err != nil {
		return nil, err // a network error, or the client's own *docspring.ValidationError
	}
	if submission.GetState() != docspring.SUBMISSIONSTATE_PROCESSED { /* see SKILL.md, rule 5 */ }
	if pdf, ok := submission.Files.GetPdfOk(); ok {
		fmt.Println(pdf.GetDownloadUrl())
	}
	return submission, nil
}
```

- Optional request fields are pointers: set them with `docspring.PtrBool`, `docspring.PtrString` and so on.
  Optional arguments are builder methods (`.Version("1")`, `.Wait(false)`).
- The models' getters have pointer receivers, so `submission.GetFiles().GetPdf().GetDownloadUrl()` doesn't compile:
  use the fields, or `GetPdfOk()`, as above.
- A request the API would reject returns a `*docspring.ValidationError` from `Execute()` without sending it.
- Region in code: `docspring.NewClientWithRegion(tokenID, tokenSecret, "EU")`.
- Model code: `lang` `go` gives package `<templatename>` with `Template`, `UnmarshalTemplate` and `Marshal`.

## Java

Maven `com.docspring:DocSpring` (Gradle `implementation 'com.docspring:DocSpring:4.+'`).

```java
com.docspring.Client api = new com.docspring.Client(); // or new Client(tokenId, tokenSecret, null, "EU")

Map<String, Object> data = new ObjectMapper()
    .readValue(Converter.toJsonString(invoice), new TypeReference<Map<String, Object>>() {});
data.values().removeIf(Objects::isNull); // missing values are null: a null text field prints blank, not its default
CreateSubmissionRequest body = new CreateSubmissionRequest()
    .data(data)
    .test(testMode)
    .metadata(Map.of("order_id", order.getId()));

try {
  Submission submission = api.createSubmission(templateId, body, "1", null); // version, wait
  String url = submission.getFiles().getPdf().getDownloadUrl();
} catch (com.docspring.ApiException e) {
  // e.getCode(), e.getResponseBody() (the JSON string), e.getResponseHeaders() (a plain map: look up
  // Retry-After ignoring case)
}
```

- Every optional argument is positional: pass `null` to leave one out.
- A request the API would reject throws `com.docspring.ValidationException` (an `IllegalArgumentException`).
- Model code: `lang` `java`. `code` holds every class, each under a `// ClassName.java` comment: save each as its own
  file in the package's directory. The classes use Jackson, with `Converter.toJsonString` and
  `Converter.fromJsonString`.

## C#

```bash
dotnet add package DocSpring.Client
```

```csharp
// Each NewClient() call builds its own HTTP stack: create one client at startup and reuse it.
var api = DocSpring.Client.Client.EnvClientFactory.NewClient(); // or NewClient(region: "EU")

var data = JsonSerializer.Deserialize<Dictionary<string, object>>(invoice.ToJson());
var body = new DocSpring.Client.Model.CreateSubmissionRequest { Data = data, Test = testMode };

var response = await api.CreateSubmissionAsync(templateId, body, version: "1");
if (response.TryCreated(out var submission))
{
    var url = submission.Files.Pdf.DownloadUrl;
}
else
{
    // Error statuses don't throw: response.StatusCode, response.RawContent (the JSON error body),
    // response.Headers.RetryAfter. IsUnprocessableContent, IsPaymentRequired and the other Is... properties name
    // the documented ones; a 504 or 429 only has StatusCode and RawContent.
}
```

- A request the API would reject throws `DocSpring.Client.Client.ValidationException` before it's sent.
- Model code: `lang` `csharp` gives namespace `DocSpring.Templates.<Name>` with `Template`, `ToJson()` and
  `Template.FromJson(json)`, using `System.Text.Json`.

## Elixir

```elixir
# mix.exs
{:docspring, "~> 4.2"}
```

```elixir
conn = Docspring.Connection.new() # or Docspring.Connection.new(region: "EU")

body = %{
  # to_map/1 sends a missing optional value as nil (null): a null text field prints blank, not its default
  "data" => invoice |> DocSpring.Templates.Invoice.Template.to_map() |> Map.reject(fn {_key, value} -> is_nil(value) end),
  "test" => test_mode,
  "metadata" => %{"order_id" => order.id}
}

case Docspring.Api.Client.create_submission(conn, template_id, body, version: "1") do
  {:ok, %Docspring.Model.Submission{state: "processed"} = submission} -> {:ok, submission}
  {:ok, %Docspring.Model.Submission{} = submission} -> {:error, {:not_processed, submission}}
  # A documented error status (422, 402, 403, 404, 401) is {:ok, %ErrorResponse{}}, not {:error, ...}
  {:ok, %Docspring.Model.ErrorResponse{error: error}} -> {:error, error}
  # Other statuses (429, 504) are {:error, %Tesla.Env{status: status, body: body}}
  {:error, reason} -> {:error, reason}
end
```

- A request the API would reject returns `{:error, %Docspring.ValidationError{}}` without being sent.
- Model code: `lang` `elixir` gives `DocSpring.Templates.<Name>.Template` with `to_map/1`, `from_map/1`,
  `to_json/1` and `from_json/1`.

## Rust

```toml
[dependencies]
docspring = "4.2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

```rust
mod invoice; // the generated model code, saved as src/invoice.rs

use docspring::{Api, CreateSubmissionError, Error};

// docspring::Client::from_env() reads DOCSPRING_TOKEN_ID, DOCSPRING_TOKEN_SECRET and DOCSPRING_REGION
async fn generate_invoice(
    client: &docspring::Client,
    template_id: &str,
    invoice: &invoice::Invoice,
    test_mode: bool,
) -> Result<docspring::models::Submission, Box<dyn std::error::Error>> {
    let body = docspring::models::CreateSubmissionRequest {
        // The generated structs leave out empty optional fields, so those fields print their defaults
        data: Some(serde_json::from_value(serde_json::to_value(invoice)?)?),
        test: Some(test_mode),
        ..Default::default()
    };
    let params = docspring::CreateSubmissionParams::builder()
        .template_id(template_id)
        .body(body)
        .version("1")
        .build();

    match client.create_submission(params).await {
        Ok(submission) => {
            if submission.state != docspring::models::SubmissionState::Processed { /* see SKILL.md, rule 5 */ }
            if let Some(url) = submission.files.pdf.as_ref().and_then(|pdf| pdf.download_url.as_deref()) {
                println!("{url}");
            }
            Ok(submission)
        }
        // An error status: `entity` is the error type's variant for it, and `headers` has Retry-After
        Err(Error::ResponseError(response)) => match response.entity {
            Some(CreateSubmissionError::Status504(error)) => {
                // The submission was saved: get it by error.error.submission_id
                Err(format!("timed out: {:?}", error.error.submission_id).into())
            }
            _ => Err(format!("DocSpring returned {}: {}", response.status, response.content).into()),
        },
        // The client's own check: the API would have rejected the request, so it wasn't sent
        Err(Error::RequestValidation(error)) => Err(error.into()),
        Err(error) => Err(error.into()), // a network error
    }
}
```

- Every method is on the `docspring::Api` trait (`use docspring::Api`), and takes one parameters struct from its
  builder. With the `mockall` feature, `docspring::MockApi` stands in for the client in tests.
- Request models are structs: set the fields you need and finish with `..Default::default()`. An optional field is an
  `Option`, and a nullable one inside it another `Option`.
- Response enums are open: a value this release doesn't know is `Unknown(String)`, and `is_known()` says which.
- Region in code: `docspring::Client::builder().region("EU").build()?` (with `.token_id(...)` and
  `.token_secret(...)`, or the environment variables).
- Model code: `lang` `rust` gives a module with a struct named after the template (`Invoice`), deriving serde's
  `Serialize` and `Deserialize`. Its first comment names the file to save it as.

## Webhook signatures

Each client checks the `X-DocSpring-Signature` header for you: pass it the raw body exactly as received, the header
and the webhook's secret. It returns true or false, accepts any `v1` that matches, compares in constant time and
rejects a `t` more than 300 seconds from now. Read the raw body before any framework parses it.

```php
$rawBody = file_get_contents('php://input');
$ok = \DocSpring\Webhooks::verifyWebhookSignature($rawBody, $_SERVER['HTTP_X_DOCSPRING_SIGNATURE'] ?? '', $secret);
```

```go
ok := docspring.VerifyWebhookSignature(rawBody, r.Header.Get("X-DocSpring-Signature"), secret) // rawBody []byte
```

```java
boolean ok = com.docspring.Webhooks.verifyWebhookSignature(
    rawBody, request.getHeader("X-DocSpring-Signature"), secret);
```

```csharp
var ok = DocSpring.Webhooks.VerifyWebhookSignature(
    rawBody, Request.Headers["X-DocSpring-Signature"].ToString(), secret);
```

```elixir
# In Phoenix, keep the raw body with a custom body_reader for Plug.Parsers: it's gone once parsed.
ok = Docspring.Webhooks.verify_webhook_signature(raw_body, signature_header, secret)
```

```rust
// In axum, take the body as Bytes (not Json) to keep it as it was sent
let ok = docspring::verify_webhook_signature(&raw_body, signature_header, &secret);
```
