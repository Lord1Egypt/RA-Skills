# Bobine param grammar

Use one shell argument per top-level param.

## Scalar values

- `null`
- `blob:<hex>`
- `bigint:<value>`
- `number:<value>`
- `text:<value>`

Examples:

```bash
text:Alice
text:"Alice, Bob]"
bigint:42
number:3.14
blob:deadbeef
null
```

## Packed arrays

Nested arrays are encoded with either:

- `pack:[item1,item2,...]`
- `array:[item1,item2,...]`

Both forms produce the same packed array value.

Examples:

```bash
'pack:[text:bobine.multisig/call,bigint:1,text:target]'
'pack:[text:"a,b]",bigint:1]'
'array:[text:hello,bigint:1,null]'
'pack:[text:outer,pack:[text:inner,bigint:2]]'
```

## Shell guidance

- Quote the whole param when it contains `[` `]` `,` or spaces
- Keep the type prefix inside the quoted string
- Quote the `text:` payload itself when it contains `,` or `]`, for example `text:"a,b]"`
- Use hex without `0x` for `blob:`

## Unsupported values in v1

- Objects/maps
- Booleans
- Unprefixed strings or numbers

If you receive raw contract docs that use a different notation, normalize them to this grammar before invoking the scripts.
