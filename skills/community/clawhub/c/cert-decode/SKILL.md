---
name: cert-decode
description: Decode and inspect X.509 SSL/TLS certificates. Use when the user asks to read a certificate, parse a PEM file, check certificate expiry, inspect a TLS cert, view Subject Alternative Names, or decode a .crt/.pem file.
metadata: {"openclaw":{"requires":{"bins":["openssl"]}}}
---

# Cert Decode

Parse and display human-readable details from X.509 PEM certificates using `openssl`.

## Input
- PEM certificate content (text starting with `-----BEGIN CERTIFICATE-----`) pasted directly, OR
- Path to a `.pem` or `.crt` file, OR
- Hostname to fetch the live certificate from (e.g., `example.com`)

## Output
- Subject (CN, O, OU, C)
- Issuer (CA name, organization)
- Validity: Not Before / Not After (expiry date)
- Serial number
- Subject Alternative Names (SANs)
- Public key algorithm and size
- Signature algorithm
- Whether the cert is expired or expiring soon

## Instructions

1. Determine input type: pasted PEM text, file path, or hostname.

2. **From pasted PEM text:**
   Write the PEM content to a temp file, then:
   ```
   echo "PEM_CONTENT" | openssl x509 -text -noout
   ```
   Or use process substitution if available.

3. **From a file path:**
   ```
   openssl x509 -text -noout -in /path/to/cert.pem
   ```

4. **From a live hostname (port 443):**
   ```
   echo | openssl s_client -connect HOSTNAME:443 -servername HOSTNAME 2>/dev/null | openssl x509 -text -noout
   ```

5. Extract and present key fields from the `openssl x509 -text` output in a clean, readable format:
   - **Subject:** parse `Subject:` line
   - **Issuer:** parse `Issuer:` line
   - **Valid From:** parse `Not Before:`
   - **Valid Until:** parse `Not After :`
   - **Serial:** parse `Serial Number:`
   - **SANs:** parse `X509v3 Subject Alternative Name:` block for all `DNS:` and `IP Address:` entries
   - **Key:** parse `Public Key Algorithm:` and key size (e.g., `RSA Public-Key: (2048 bit)`)
   - **Signature Algorithm:** parse `Signature Algorithm:`

6. Calculate whether the certificate is:
   - Already expired (Not After is in the past)
   - Expiring within 30 days (warn the user)
   - Valid (show days remaining)

7. If `openssl` is not found, tell the user:
   > "This skill requires `openssl`. Install with: `brew install openssl` (macOS) or `sudo apt install openssl` (Linux)."

## Examples

**From file:**
**Command:** `openssl x509 -text -noout -in /etc/ssl/cert.pem`

**From hostname:**
**Command:** `echo | openssl s_client -connect github.com:443 -servername github.com 2>/dev/null | openssl x509 -text -noout`

**Sample parsed output:**
```
Subject:    CN=github.com, O=GitHub, Inc., C=US
Issuer:     CN=DigiCert TLS Hybrid ECC SHA384 2020 CA1, O=DigiCert Inc, C=US
Valid From: 2024-03-07
Valid Until: 2025-03-06  ⚠ Expires in 14 days
Serial:     0a:bc:12:...
SANs:       github.com, www.github.com
Key:        EC 256-bit (prime256v1)
Signature:  ecdsa-with-SHA384
```

## Error Handling

- `openssl` not found → tell user to install it
- Input is not valid PEM → openssl will error with `unable to load certificate`; tell user the input does not appear to be a valid PEM certificate
- Hostname unreachable → `openssl s_client` will fail; report connection error and suggest checking the hostname or network
- DER format instead of PEM → tell user to convert first with: `openssl x509 -inform DER -in cert.der -out cert.pem`
- Certificate chain (multiple certs) → only the first cert is parsed; inform user if they need a specific cert from the chain
