# Ruby

The `docspring` gem. The examples are for Rails (Active Job, a controller and a rake task); plain Ruby works the
same way. Replace `tpl_...` with the real template ID.

- [Set up](#set-up)
- [Generate the models and schema](#generate-the-models-and-schema)
- [The client and error helper](#the-client-and-error-helper)
- [The job](#the-job)
- [Download](#download)
- [Webhooks](#webhooks)
- [Tests](#tests)

## Set up

```ruby
# Gemfile
gem "docspring", "~> 4.2"
gem "dry-struct" # the generated model code needs dry-struct and dry-types
gem "dry-types"
```

`DocSpring::Client.new` reads `DOCSPRING_TOKEN_ID`, `DOCSPRING_TOKEN_SECRET`, `DOCSPRING_REGION` and `DOCSPRING_HOST`.
Keyword arguments override them: `DocSpring::Client.new(api_token_id:, api_token_secret:, region: "EU")`. Request
bodies are hashes. Optional arguments go in a trailing hash: `client.create_submission(template_id, body,
version: "1", wait: false)`. Responses are model objects with the API's snake_case names
(`submission.files.pdf.download_url`), and enum values such as `submission.state` are strings.

## Generate the models and schema

`lib/tasks/docspring.rake`, run with `bin/rails docspring:codegen` (and `bin/rails docspring:codegen CHECK=1` in CI):

```ruby
namespace :docspring do
  # Every template the app uses, at the version the app pins.
  TEMPLATES = [{ name: "invoice", type_name: "InvoiceData", template_id: "tpl_...", version: "1" }].freeze
  OUT_DIR = Rails.root.join("app/models/docspring_templates")

  desc "Regenerate the DocSpring model code and schemas (CHECK=1 fails when they're out of date)"
  task codegen: :environment do
    client = DocSpring::Client.new
    check = ENV["CHECK"].present?
    stale = false
    FileUtils.mkdir_p(OUT_DIR)

    TEMPLATES.each do |t|
      header = "# Generated from DocSpring template #{t[:template_id]}, version #{t[:version]}.\n" \
               "# Don't edit it: run bin/rails docspring:codegen\n\n"
      model = client.get_template_model_code(t[:template_id], "ruby", version: t[:version])
      schema = client.get_template_schema(t[:template_id], version: t[:version])
      files = {
        # The root class is namespaced by the template's name; the alias keeps code working if it's renamed.
        OUT_DIR.join("#{t[:name]}.rb") => "#{header}#{model.code}\n\n#{t[:type_name]} = #{model.root_type_name}\n",
        OUT_DIR.join("#{t[:name]}.schema.json") => "#{JSON.pretty_generate(schema)}\n",
      }
      files.each do |path, content|
        next if File.exist?(path) && File.read(path) == content

        stale = true
        if check
          warn "#{path} doesn't match the template. Run bin/rails docspring:codegen"
        else
          File.write(path, content)
        end
      end
    end
    abort if check && stale
  end
end
```

The generated file defines `DocSpring::Templates::<Name>::Template` (a `Dry::Struct`) and the alias. Zeitwerk
expects one constant per file, so load it explicitly (`require Rails.root.join("app/models/docspring_templates/invoice")`
in an initializer) and add the directory to `Rails.autoloaders.main.ignore`. Two things about the generated struct:

- `InvoiceData.new(...)` needs every attribute, including optional ones: pass `nil` for a value you don't have, or
  dry-struct raises "is missing in Hash input".
- `to_dynamic` (a hash with string keys) sends those `nil`s as `null`. The API takes them, but a null text, number,
  date or image field prints blank where a missing key prints its default: send `to_dynamic.compact` as `data`.

## The client and error helper

`app/services/docspring_api.rb`:

```ruby
module DocspringApi
  # The app's own setting (DocSpring doesn't read it): test PDFs unless production sets DOCSPRING_TEST_MODE=false.
  TEST_MODE = ENV["DOCSPRING_TEST_MODE"] != "false"

  def self.client
    @client ||= DocSpring::Client.new
  end

  # The API's error ({"code", "message", "details", "request_id", ...}), with "status" and "retry_after".
  def self.error(e)
    return unless e.is_a?(DocSpring::ApiError)

    error = begin
      JSON.parse(e.response_body.to_s).fetch("error", {})
    rescue JSON::ParserError
      {} # not a DocSpring error body, such as a proxy's error page
    end
    retry_after = e.response_headers && e.response_headers["Retry-After"]
    error.merge("status" => e.code, "retry_after" => retry_after.presence&.to_f)
  end

  # A 429 never reached the API, so it's safe to send again, even for a create.
  def self.with_rate_limit_retry(attempts: 5)
    attempt = 0
    begin
      attempt += 1
      yield
    rescue DocSpring::ApiError => e
      details = error(e)
      raise if details["status"] != 429 || attempt >= attempts

      sleep((details["retry_after"] || (2**attempt)) + rand)
      retry
    end
  end

  # The submission that a create made when it failed without returning an ID (a network error, a 5xx, a 504 without
  # one), found by your own metadata ID (metadata keys are strings). Lists are newest first: this pages back to
  # `since`, a minute early. An invalid_data submission made no PDF, so it doesn't count.
  def self.find_submission(template_id, key, value, since)
    cursor = nil
    loop do
      page = client.list_submissions(template_id:, test: TEST_MODE, created_after: since - 60, limit: 100, cursor:)
      found = page.data.find { |submission| submission.metadata[key] == value && submission.state != "invalid_data" }
      return found if found
      return nil if page.next_cursor.nil?

      cursor = page.next_cursor
    end
  end
end
```

`created_after` takes an RFC 3339 string: the client rejects a `Time`.

`DocSpring::ValidationError` (an `ArgumentError`, raised before sending) is a bug in the request, so let it fail.

## The job

`app/jobs/generate_invoice_pdf_job.rb`. The job's retry is what waits for a pending or credit-blocked submission.

```ruby
class GenerateInvoicePdfJob < ApplicationJob
  class NotReady < StandardError; end

  INVOICE_TEMPLATE_ID = "tpl_..."
  INVOICE_TEMPLATE_VERSION = "1" # the version bin/rails docspring:codegen uses

  retry_on NotReady, wait: :polynomially_longer, attempts: 20

  def self.invoice_data(order)
    # Only the template's field names: an unknown key is a 422.
    InvoiceData.new(
      invoice_number: order.number,
      customer_name: order.customer_name,
      issue_date: order.paid_at.to_date.iso8601, # YYYY-MM-DD
      total: order.total_cents / 100.0
    )
  end

  def perform(order)
    submission =
      if order.invoice_submission_id
        DocspringApi.client.get_submission(order.invoice_submission_id) # a retried job: never create a second one
      elsif order.invoice_requested_at && (found = find_earlier_submission(order))
        found
      else
        create_submission(order)
      end

    case submission.state
    when "processed" then nil # submission.files.pdf is ready
    when "pending", "insufficient_credits", "account_suspended"
      raise NotReady, "Invoice PDF #{submission.id} is #{submission.state}"
    else
      # invalid_data, error, syntax_error, image_download_failed, image_processing_failed, or a new state
      raise "Invoice PDF #{submission.id} failed: #{submission.state} #{submission.error_message}"
    end
  end

  private

  # An earlier attempt sent the request but got no ID back, so the submission may exist
  def find_earlier_submission(order)
    found = DocspringApi.find_submission(INVOICE_TEMPLATE_ID, "order_id", order.id, order.invoice_requested_at)
    order.update!(invoice_submission_id: found.id) if found
    found
  end

  def create_submission(order)
    body = {
      data: self.class.invoice_data(order).to_dynamic.compact,
      test: DocspringApi::TEST_MODE,
      metadata: { order_id: order.id, pdf_filename: "invoice-#{order.number}" },
    }
    order.update!(invoice_requested_at: Time.current) # before the request is sent
    submission = DocspringApi.with_rate_limit_retry do
      DocspringApi.client.create_submission(INVOICE_TEMPLATE_ID, body, version: INVOICE_TEMPLATE_VERSION)
    end
    order.update!(invoice_submission_id: submission.id)
    submission
  rescue DocSpring::ApiError => e
    error = DocspringApi.error(e)
    # The submission exists: it waits for credits, or is still being made.
    if %w[insufficient_credits polling_timeout].include?(error["code"]) && error["submission_id"]
      order.update!(invoice_submission_id: error["submission_id"])
      raise NotReady, "Invoice PDF #{error['submission_id']}: #{error['code']}"
    end
    raise
  end
end
```

The orders table needs `invoice_submission_id` and `invoice_requested_at` columns. A 422 `invalid_data` raises
`DocSpring::ApiError` out of the job: log `error["details"]`' pointers, and don't retry it, since the same data fails
again.

## Download

```ruby
class InvoicesController < ApplicationController
  def show
    order = current_user.orders.find(params[:order_id])
    return head :not_found unless order.invoice_submission_id

    submission = DocspringApi.client.get_submission(order.invoice_submission_id)
    url = submission.files.pdf&.download_url
    return head :conflict unless submission.state == "processed" && url

    redirect_to url, allow_other_host: true # a fresh temporary link
  end
end
```

To keep a copy in Active Storage, download `submission.files.pdf.download_url` (no auth) right after it's processed.

## Webhooks

Create it once, from a console or a task the user runs (it prints the signing secret):

```ruby
webhook = DocspringApi.client.create_webhook(
  name: "Invoice PDFs",
  url: "https://example.com/webhooks/docspring",
  event_types: ["submission.processed", "submission.failed"],
  template_ids: [GenerateInvoicePdfJob::INVOICE_TEMPLATE_ID],
  mode: "live"
)
puts "Set DOCSPRING_WEBHOOK_SECRET to #{webhook.secret}"
```

The handler. `request.raw_post` is the body as DocSpring signed it:

```ruby
class DocspringWebhooksController < ActionController::API
  def create
    verified = DocSpring.verify_webhook_signature(request.raw_post, request.headers["X-DocSpring-Signature"],
                                                  ENV.fetch("DOCSPRING_WEBHOOK_SECRET"))
    return head :bad_request unless verified

    event = JSON.parse(request.raw_post) # version 4: {"id", "event_type", "created_at", "data" => the submission}
    HandleDocspringEventJob.perform_later(event) unless ProcessedWebhookEvent.exists?(event_id: event["id"])
    head :ok # within 30 seconds; the job does the work
  end
end
```

The job records `event["id"]` in `ProcessedWebhookEvent` (a table with a unique index on `event_id`) so a retried
delivery is skipped.

## Tests

Check what your builder makes against the committed schema (`gem "json_schemer"` in the test group). It reads the
draft from the schema's `$schema` and ignores DocSpring's own `x-` keywords:

```ruby
RSpec.describe GenerateInvoicePdfJob do
  let(:schema) { JSONSchemer.schema(Rails.root.join("app/models/docspring_templates/invoice.schema.json")) }

  it "builds data that matches the template's schema" do
    data = described_class.invoice_data(build(:order, :paid)).to_dynamic.compact
    expect(schema.validate(data).map { |error| error["error"] }).to eq([])
  end
end
```

The contract test, with a test API token in CI:

```ruby
RSpec.describe "DocSpring invoice template" do
  it "accepts our invoice data" do
    result = DocspringApi.client.validate_submission(
      GenerateInvoicePdfJob::INVOICE_TEMPLATE_ID,
      { data: GenerateInvoicePdfJob.invoice_data(build(:order, :paid)).to_dynamic.compact },
      version: GenerateInvoicePdfJob::INVOICE_TEMPLATE_VERSION
    )
    expect(result.error&.details&.map(&:pointer)).to be_nil
    expect(result.valid).to be(true)
  end
end
```
