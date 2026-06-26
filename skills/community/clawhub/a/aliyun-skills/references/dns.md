# AliDNS (Alibaba Cloud DNS) Reference

Product code: `alidns`

## List Domains

```bash
aliyun alidns DescribeDomains
```

Filter by keyword:
```bash
aliyun alidns DescribeDomains --KeyWord example.com
```

```bash
aliyun alidns DescribeDomains \
  --output 'cols=DomainName,DnsServers,RecordCount' 'rows=Domains.Domain[]'
```

---

## DNS Records

### List Records for a Domain

```bash
aliyun alidns DescribeDomainRecords --DomainName example.com
```

```bash
aliyun alidns DescribeDomainRecords --DomainName example.com \
  --output 'cols=RecordId,RR,Type,Value,TTL,Status' 'rows=DomainRecords.Record[]'
```

Filter by type:
```bash
aliyun alidns DescribeDomainRecords --DomainName example.com --TypeKeyWord A
```

Filter by subdomain:
```bash
aliyun alidns DescribeSubDomainRecords --SubDomain www.example.com
```

### Get Record Details

```bash
aliyun alidns DescribeDomainRecordInfo --RecordId 123456789
```

---

## Add a Record

### A Record (IPv4)

```bash
aliyun alidns AddDomainRecord \
  --DomainName example.com \
  --RR www \
  --Type A \
  --Value 1.2.3.4 \
  --TTL 600
```

### CNAME Record

```bash
aliyun alidns AddDomainRecord \
  --DomainName example.com \
  --RR blog \
  --Type CNAME \
  --Value myblog.github.io \
  --TTL 600
```

### MX Record

```bash
aliyun alidns AddDomainRecord \
  --DomainName example.com \
  --RR @ \
  --Type MX \
  --Value mail.example.com \
  --Priority 10 \
  --TTL 600
```

### TXT Record (e.g., SPF, domain verification)

```bash
aliyun alidns AddDomainRecord \
  --DomainName example.com \
  --RR @ \
  --Type TXT \
  --Value '"v=spf1 include:spf.example.com ~all"' \
  --TTL 600
```

### AAAA Record (IPv6)

```bash
aliyun alidns AddDomainRecord \
  --DomainName example.com \
  --RR @ \
  --Type AAAA \
  --Value 2001:db8::1 \
  --TTL 600
```

---

## Update a Record

```bash
aliyun alidns UpdateDomainRecord \
  --RecordId 123456789 \
  --RR www \
  --Type A \
  --Value 5.6.7.8 \
  --TTL 600
```

---

## Delete a Record

```bash
aliyun alidns DeleteDomainRecord --RecordId 123456789
```

Delete all records matching a subdomain:
```bash
aliyun alidns DeleteSubDomainRecords \
  --DomainName example.com \
  --RR www
```

---

## Enable / Disable a Record

```bash
# Disable (pause) a record without deleting it
aliyun alidns SetDomainRecordStatus \
  --RecordId 123456789 \
  --Status Disable

# Re-enable
aliyun alidns SetDomainRecordStatus \
  --RecordId 123456789 \
  --Status Enable
```

---

## Common RR (Subdomain) Values

| RR | Meaning |
|----|---------|
| `@` | Apex/root domain (example.com) |
| `www` | www.example.com |
| `*` | Wildcard (matches any subdomain) |
| `mail` | mail.example.com |

## Supported Record Types

`A`, `AAAA`, `CNAME`, `MX`, `TXT`, `NS`, `SRV`, `CAA`, `PTR`, `REDIRECT_URL`, `FORWORD_URL`
