# Certificates

The dddparser uses EU JRC (Joint Research Centre) public keys for signature verification.

## Details

- **1,640 EU certificates** embedded in the binary during build
- **Gen 1 (pks1):** https://dtc.jrc.ec.europa.eu/dtc_public_key_certificates_dt.php.html
- **Gen 2 (pks2):** https://dtc.jrc.ec.europa.eu/dtc_public_key_certificates_st.php.html

These are public keys (not credentials) and are automatically embedded during the Go build process.

## CHR Mismatch

On "CHR mismatch" warnings:
- Signature verification failed
- Data is still readable
- Parser returns exit code 1, but still creates JSON output

## Source

- **Repository:** https://github.com/traconiq/tachoparser
- **License:** MIT