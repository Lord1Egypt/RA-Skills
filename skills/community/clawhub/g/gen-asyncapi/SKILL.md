---
name: gen-asyncapi
description: Code generator that turns an AsyncAPI 3 spec into Go or TypeScript. `github.com/psyb0t/gen-asyncapi/cmd/gen-asyncapi` runs from `go generate` (or `go run`) with a small YAML config and writes one file. Go output has structs with strict `UnmarshalJSON` and `Validate`, enums as named types with constants, unions with `FromX`/`AsX`/`Value`, `Message<Name>` constants, `DecodeReceivedMessage`, a `Handler` interface with `UnimplementedHandler`, `Dispatch`, and a `Client` with one send method per message plus `Run`, over the `asyncapirt` runtime and its gorilla/websocket transport. TypeScript output (`language: typescript`) is one dependency-free `.ts` file with interfaces, literal unions, `validate<Type>` assert functions, `decodeReceivedMessage`, `dispatch` and a `Client` that takes a browser `WebSocket`. Use when a project needs typed models or a WebSocket client generated from an AsyncAPI 3 spec, or already has a `gen.go` calling gen-asyncapi.
homepage: https://github.com/psyb0t/gen-asyncapi
user-invocable: true
metadata:
  openclaw:
    emoji: "🧬"
    requires:
      bins:
        - go
permissions:
  filesystem: "Reads the AsyncAPI spec, the files it references and the generator config; writes the one output file named by the config or -o. Guides edits to the project's own Go or TypeScript source."
  shell: "The Go toolchain (`go get -tool`, `go generate`, `go run`, `go build`, `go test`) to install and run the generator."
  network: "`go get` and `go run ...@version` fetch the module from your Go module proxy. Generation itself is offline. The generated client connects only to the server URL your code passes it."
---

# gen-asyncapi

Generates Go or TypeScript from an AsyncAPI 3 document: types, strict decoding with validation, message dispatch and a WebSocket client. The generated code is regular source that gets committed next to the spec and regenerated when the spec changes.

Install paths, every config key and the generated API are in [references/setup.md](references/setup.md).

## Security & safety

- The generator only reads the spec, the files it references and the config, and writes the single output file. It never runs code from the spec.
- Never hand-edit a `*.gen.go` or `*.gen.ts` file. Change the spec or the config and regenerate; the next run overwrites manual edits.
- The generated client opens a connection only when your code dials one. Put tokens in `gorillaws.WithBearerToken` or the transport you build, never in the spec or config.

## When to use

- A Go service or client talks to a WebSocket (or other message) API described by an AsyncAPI 3 spec and wants typed messages, strict decoding and a ready client.
- A web front end needs TypeScript types, validators and a client for the same spec.
- The repository already has a `gen.go` with `go tool gen-asyncapi` and the spec or config changed.

## When NOT to use

- The spec is AsyncAPI 2.x; the generator loads 3.x only.
- You only need to read a spec in Go, not generate code. Use [go-asyncapi](https://github.com/psyb0t/go-asyncapi), the loader the generator is built on.
- HTTP APIs described by OpenAPI; this generator reads AsyncAPI only.

## Go: set up

```bash
go get -tool github.com/psyb0t/gen-asyncapi/cmd/gen-asyncapi@latest
```

```yaml
# config.yaml, next to gen.go
package: chat
output: chat.gen.go
```

```go
// gen.go
package chat

//go:generate go tool gen-asyncapi --config=config.yaml ../../api/asyncapi.yaml
```

Run `go generate ./...`. Paths in the config and on the command line are relative to the directory holding `gen.go`.

## Go: use the client

```go
conn, err := gorillaws.Dial(ctx, chat.ServerProductionURL, gorillaws.WithBearerToken(token))
if err != nil {
	return err
}

client := chat.NewClient(conn)
defer client.Close()

if err := client.JoinRoom(ctx, chat.JoinRequest{ID: id, Room: "lobby"}); err != nil {
	return err // the payload failed Validate, or the write failed
}

type handler struct {
	chat.UnimplementedHandler
}

func (handler) HandleAck(ctx context.Context, ack chat.Ack) error {
	return nil
}

err = client.Run(ctx, handler{}) // reads until ctx ends or the connection drops
```

Send method names come from the operation names in the spec, handler methods are `Handle<Message>`, and `const` properties fill themselves in on marshal. Decoding errors wrap `ctxerrors/commerr` sentinels such as `commerr.ErrValidationFailed` and `commerr.ErrRequiredFieldNotSet`.

## TypeScript

```bash
go run github.com/psyb0t/gen-asyncapi/cmd/gen-asyncapi@latest -language=typescript -o=src/chat.gen.ts asyncapi.yaml
```

```ts
const socket = new WebSocket(ServerProductionURL);
const client = new Client(socket);

await client.joinRoom({ type: "join", id: crypto.randomUUID(), room: "lobby" });

socket.addEventListener("message", (message) => {
  client
    .receive(message.data, {
      handleAck: (ack) => render(ack.ok),
    })
    .catch(report);
});
```

In TypeScript, `const` properties are literal types the caller writes out. Validation failures throw `ValidationError` with a `path`; unmatched frames go to `handleUnknownMessage` or reject with `UnknownMessageError`.

## Two messages with the same shape

When the client cannot tell incoming messages apart by `const` properties or strict decoding, pin each one with a JSON pointer in the config:

```yaml
output-options:
  message-matchers:
    Notice:
      /messages/0/type: notice
    Alert:
      /messages/0/type: alert
```

A list value such as `[notice, info]` matches any of its entries. An empty list fails generation.
