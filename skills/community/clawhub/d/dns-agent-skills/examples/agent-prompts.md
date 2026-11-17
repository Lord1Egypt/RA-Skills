<!-- Generated from deployed DomainHelp DNS skill docs. Do not hand-edit in the mirror repo. -->

# Agent Prompt Starters

Use these as starting points when asking an agent to select and invoke a DomainHelp DNS skill.

## What Is My Public IP

> Use the `whatismypublicip` DomainHelp skill documented in `skills/what-is-my-public-ip/dnsskills.md`. Useful when a browser, script, agent, or remote workflow needs to know the public address it is using.

## What Is My DNS Resolver

> Use the `myresolver` DomainHelp skill documented in `skills/what-is-my-resolver/dnsskills.md`. Creates a unique lookup name and reports the resolver that queries it, with browser and manual workflow support.

## Is This a Homoglyph?

> Use the `isconfusable` DomainHelp skill documented in `skills/is-this-a-homoglyph/dnsskills.md`. Helps humans and agents decide whether a string or domain is an IDN, looks visually deceptive, and what it likely mimics.

## Is This a Redirect?

> Use the `isredirect` DomainHelp skill documented in `skills/is-this-a-redirect/dnsskills.md`. Looks up a domain under redirects.domainsure.zone and reports whether it is listed as a redirect or URL shortener, including TXT explanations when present.

## Link Expander / Redirect Chain

> Use the `redirectchain` DomainHelp skill documented in `skills/redirect-chain/dnsskills.md`. Follows a URL through its HTTP redirect chain and reports status codes, redirect targets, response headers, bounded payload samples, and HTML metadata for each hop.

## SPF Flattener

> Use the `spfflattener` DomainHelp skill documented in `skills/spf-flattener/dnsskills.md`. Useful for mail operations, audits, and agent workflows that need to reason about SPF include expansion.

## DNS Twister

> Use the `dnstwister` DomainHelp skill documented in `skills/dns-twister/dnsskills.md`. Supports typo, phishing, bit-flip, and homoglyph-adjacent domain intelligence workflows.
