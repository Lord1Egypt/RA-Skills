# Permission Playbook

Use `python3 scripts/fofa_recon.py login` to fetch the live `permission_profile` before planning field-heavy FOFA work.

## Capability model

The skill normalizes FOFA account behavior into these planning rules:

- `vip_level 0`: registered user, no `host` API, no `stats` API, base export fields only
- `vip_level 1` and `11`: personal-tier field family, `host` API enabled, `stats` API disabled
- `vip_level 2` and `12`: professional-tier field family, `host` and `stats` APIs enabled
- `vip_level 13`: business-tier field family, deep fields enabled, `stats` enabled
- `vip_level 5`: enterprise-tier field family, all business fields plus `icon`, `fid`, and `structinfo`
- `vip_level 22`: education account, handled conservatively as base-field export plus `host` API

The script also returns:

- `query_syntax_scope`
- `documented_query_syntax_count`
- `search_export_field_scope`
- `documented_search_export_field_count`
- `api_rps_limit`
- `remain_api_query`
- `remain_api_data`
- `data_limit`
- `field_families`
- `allowed_search_fields_csv`

## Search field families

### Base fields

Available to every tier:

`ip,port,protocol,base_protocol,host,domain,link,title,server,os,header,banner,icp,jarm,country,country_name,region,city,longitude,latitude,asn,org,cert,cert.domain,cert.sn,cert.issuer.org,cert.issuer.cn,cert.subject.org,cert.subject.cn,tls.ja3s,tls.version,cert.not_before,cert.not_after,status_code`

### Personal fields

Available to `1`, `11`, `2`, `12`, `13`, `5`:

`header_hash,banner_hash,banner_fid`

### Professional fields

Available to `2`, `12`, `13`, `5`:

`product,product_category,cname,lastupdatetime`

### Business fields

Available to `13`, `5`:

`body,icon_hash,product.version,cert.is_valid,cname_domain,cert.is_match,cert.is_equal`

### Enterprise-only fields

Available only to `5`:

`icon,fid,structinfo`

## Intent-to-field matching

Use the `search_field_presets` object from `login` output to map user needs to fields.

- `asset_baseline`: `host,ip,port,protocol,title,domain,country_name,server`
- `web_delivery`: `host,link,ip,port,protocol,status_code,title,server`
- `geo_org`: `country_name,region,city,asn,org`
- `banner_hashes`: `header_hash,banner_hash,banner_fid`
- `product_stack`: `product,product_category,cname,lastupdatetime`
- `certificate_review`: `cert,cert.domain,cert.sn,cert.subject.cn,cert.subject.org,cert.issuer.cn,cert.issuer.org`
- `tls_review`: `tls.ja3s,tls.version,cert.not_before,cert.not_after`
- `body_and_favicon`: `body,icon_hash`
- `enterprise_binary_pivots`: `fid,icon,structinfo`
- `deep_validation`: `product.version,cert.is_valid,cname_domain,cert.is_match,cert.is_equal`

## Practical matching examples

If the user wants:

- basic asset handoff: use `asset_baseline`
- web delivery with indexed HTTP metadata: use `web_delivery`
- product identification: add `product_stack`
- hash-based correlation: add `banner_hashes`
- cert and TLS review: combine `certificate_review` and `tls_review`
- web body or favicon pivots: use `body_and_favicon`
- enterprise binary pivots: use `enterprise_binary_pivots`
- version or cert validity checks: use `deep_validation`

Example request:

`ip,port,product,product.version,cert.is_valid`

The skill will resolve it like this:

- `vip_level 11` or `1`: keep `ip,port`; drop `product,product.version,cert.is_valid`
- `vip_level 12` or `2`: keep `ip,port,product`; drop `product.version,cert.is_valid`
- `vip_level 13` or `5`: keep all fields

## Agent workflow

1. Call `login` when the user asks for advanced fields or for `host`/`stats`.
2. Read `permission_profile`.
3. Select fields from `search_field_presets`.
4. Run `search`, `host`, or `stats`.
5. If `dropped_fields` appears in the result, explain the downgrade as a tier limitation, not as a query failure.

## Quota model reminders

When FOFA exposes `data_limit`, the script normalizes these documented buckets:

- `web_query`
- `web_data`
- `api_query`
- `api_data`
- `query`
- `data`

Use those buckets when the user asks about whether the current account can sustain a field-heavy or high-volume workflow.
