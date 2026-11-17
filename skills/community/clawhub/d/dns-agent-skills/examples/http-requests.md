<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# HTTP Request Examples

These examples are copied from the deployed skill docs. See each skill file for full request and response contracts.

## What Is My Public IP

```text
GET /api/v1/whatismypublicip
```


## What Is My DNS Resolver

```text
POST /api/v1/myresolver/check
```

```text
GET /api/v1/myresolver/result?token=...
```


## Is This a Homoglyph?

```text
{"input":"xn--ypal-43d9g.com"}
```

```text
GET /api/v1/isconfusable?input=xn--ypal-43d9g.com
```


## Is This a Redirect?

```text
GET /api/v1/isredirect?domain=bit.ly
```

```text
POST /api/v1/isredirect {"domain":"bit.ly"}
```


## Link Expander / Redirect Chain

```text
GET /api/v1/redirect-chain?url=https://bit.ly/example
```

```text
POST /api/v1/link-expander {"url":"https://example.com","max_hops":5}
```


## SPF Flattener

```text
POST /api/v1/spf-flattener {"domain":"example.com"}
```


## DNS Twister

```text
POST /api/v1/dns-twister {"domain":"example.com"}
```

```text
POST /api/v1/dns-twister {"domain":"example.com","resolve":true,"timeout_seconds":75}
```
