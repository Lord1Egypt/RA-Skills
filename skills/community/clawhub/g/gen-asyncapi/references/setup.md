# gen-asyncapi: setup and reference

## Requirements

- Go 1.26.9 or newer to run the generator, per the module's `go.mod`.
- Generated Go code imports `github.com/psyb0t/gen-asyncapi/asyncapirt`, plus `asyncapirt/gorillaws` if you use that transport, and `github.com/psyb0t/ctxerrors`, `github.com/psyb0t/ctxscope`.
- Generated TypeScript has no imports and uses only ES2020, so it runs in browsers and under Node.js.

## Install

As a Go tool, so `go tool gen-asyncapi` runs the version `go.mod` pins:

```bash
go get -tool github.com/psyb0t/gen-asyncapi/cmd/gen-asyncapi@latest
```

As a binary:

```bash
go install github.com/psyb0t/gen-asyncapi/cmd/gen-asyncapi@latest
```

A TypeScript project with no Go module can run it directly; pin a version in place of `@latest` inside a `package.json` script:

```bash
go run github.com/psyb0t/gen-asyncapi/cmd/gen-asyncapi@latest -language=typescript -o=src/api.gen.ts asyncapi.yaml
```

## Command line

```
gen-asyncapi [--config=config.yaml] [-language=go|typescript] [-package=name] [-o=output] asyncapi.yaml
```

The spec path is the last argument. `-language`, `-package` and `-o` override the config file, and can stand in for it entirely.

## Config

```yaml
language: go              # go or typescript, defaults to go
package: chat             # Go package name, required for Go, ignored for TypeScript
output: chat.gen.go       # defaults to asyncapi.gen.go, or asyncapi.gen.ts for TypeScript
generate:                 # omit the block to generate everything
  models: true            # types, codecs, validation
  client: true            # decoding, Handler, Dispatch, Client; needs models
output-options:
  message-matchers:       # message key -> JSON pointer -> required value or list of allowed values
    Notice:
      /messages/0/type: [notice, info]
```

Unknown keys fail with `commerr.ErrParseFailed`. Once a `generate` block is present, a key left out of it is false: `generate: {models: true}` means models only.

## What gets generated

| Spec | Go | TypeScript |
|---|---|---|
| object schema | struct with strict `UnmarshalJSON`, `Validate`, and `MarshalJSON` when it has `const` properties | `interface` plus `validate<Type>` |
| `enum` | named type and constants | literal union plus `<Type>Values` |
| `oneOf` / `anyOf` | union type with `From<X>`, `As<X>`, `Value`, `Discriminator` | union type plus `validate<Type>` |
| `allOf` | one merged struct | one merged interface |
| `contentSchema` string | `<Field>Value()` and `Set<Field>Value()` | `<type><Field>Value()` and `set<Type><Field>Value()` |
| message | `Message<Name>` constant | `Message<Name>` constant |
| `send` operation | `Client` method | `Client` method |
| `receive` operation, reply | `Handler` method, `DecodeReceivedMessage`, `Dispatch`, `Client.Run` | optional `Handler` method, `decodeReceivedMessage`, `dispatch`, `Client.receive` |
| server | `Server<Name>URL`, plus `URLTemplate` and `URLWith` for variables | `Server<Name>URL`, plus `server<Name>URLWith` |
| channel | `<Channel>AddressTemplate`, plus `<Channel>Address(...)` | `<Channel>AddressTemplate`, plus `<channel>Address(...)` |

Go details:

- Required fields are values, optional and nullable ones are pointers.
- Decoding checks required properties, `additionalProperties: false`, string length and pattern, numeric bounds, `multipleOf`, item counts, `uniqueItems`, property counts and `dependentRequired`. Failures wrap `commerr.ErrValidationFailed` or `commerr.ErrRequiredFieldNotSet`.
- `UnimplementedHandler` ignores every message; its `HandleUnknownMessage` logs a warning and keeps reading.
- `gorillaws.Dial` takes `WithBearerToken`, `WithHeader`, `WithQueryParam`, `WithSubprotocols`, `WithBinaryFrames`, `WithReadLimit` and `WithDialer`. Any type with `WriteMessage`, `ReadMessage` and `Close` works as a transport.

TypeScript details:

- Optional properties are `?:`, nullable ones add `| null`, `const` properties are literal types.
- Validators throw `ValidationError` with a `path` such as `"JoinRequest.room"`.
- `Transport` is anything with `send(data: string)` and `close()`; a browser `WebSocket` fits.
- Without `handleUnknownMessage`, `Client.receive` rejects with `UnknownMessageError` or `AmbiguousMessageError`.
- The file type-checks under `strict`, `exactOptionalPropertyTypes`, `noUncheckedIndexedAccess`, `noUnusedLocals`, `verbatimModuleSyntax` and `erasableSyntaxOnly`.

## How incoming messages are told apart

`DecodeReceivedMessage` (TypeScript: `decodeReceivedMessage`) tries the messages the client receives in this order:

1. Messages whose matchers all hold. Matchers are the `const` values on the payload's top-level properties plus the configured `message-matchers`.
2. The remaining messages, decoded strictly. Exactly one has to decode.
3. Messages whose payload is opaque, such as an Avro schema kept as raw JSON.

No match is `asyncapirt.ErrUnknownMessage` (TypeScript: `UnknownMessageError`) with every candidate's reason. Two matches is `asyncapirt.ErrAmbiguousMessage` (`AmbiguousMessageError`).

## Both languages from one spec

```go
//go:generate go tool gen-asyncapi --config=config.yaml chat.yaml
//go:generate go tool gen-asyncapi --config=config.yaml -language=typescript -o=chat.gen.ts chat.yaml
```
