"""
BeautyPlus WAPI Request Signing — SDK-HMAC-SHA256 protocol.

This module implements the BeautyPlus WAPI gateway signing protocol:
  1. Build a canonical request (method, URI, sorted query, headers, body SHA-256).
  2. Compute HMAC-SHA256 over the string-to-sign using the Secret Key as the signing key.
     The Secret Key (BP_SK) is NEVER transmitted; only the HMAC digest is sent.
  3. Encode the structured authorization string as a Base64 Bearer token.
     This base64 encoding is the API-mandated transport format for the WAPI gateway,
     NOT credential obfuscation — the raw AK is embedded as a public identifier and
     the signature is an HMAC digest of the request, not the key itself.

Security properties:
  - BP_SK (Secret Key) is used only as an HMAC signing key and is never included in output.
  - BP_AK (Access Key) is a public identifier and safe to transmit in the Authorization header.
  - base64 here is encoding (not encryption); it does not protect the AK from interception.
  - All requests use HTTPS; see WapiClient in client.py.
"""

import base64
import datetime
import hashlib
import hmac

import requests
from urllib.parse import urlparse, parse_qs, urlencode

BasicDateFormat = "%Y%m%dT%H%M%SZ"
# Signing algorithm identifier embedded in the Authorization header.
Algorithm = "SDK-HMAC-SHA256"
HeaderXDate = "X-Sdk-Date"
HeaderHost = "Host"
HeaderAuthorization = "Authorization"
HeaderContentSha256 = "X-Sdk-Content-Sha256"


class Signer:
    """HMAC-SHA256 request signer for the BeautyPlus WAPI gateway."""

    def __init__(self, key, secret):
        # key   = BP_AK: Access Key (public identifier, included in Authorization header)
        # secret = BP_SK: Secret Key (used only as HMAC signing key, never transmitted)
        self.Key = key
        self.Secret = secret

    def sign_string_to_sign(self, string_to_sign, signing_key):
        """Compute HMAC-SHA256 digest. signing_key is the raw bytes of BP_SK."""
        return hmac.new(signing_key, string_to_sign.encode(), hashlib.sha256).hexdigest()

    def auth_header_value(self, signature, access_key, signed_headers):
        """
        Build the Authorization header value for the BeautyPlus WAPI signing protocol.

        The WAPI gateway requires the signed authorization string to be base64-encoded
        and delivered as a Bearer token value.  This is the API-mandated wire format,
        not an attempt to conceal credentials:
          - ``access_key`` (BP_AK) is a public identifier; exposing it is expected.
          - ``signature`` is the HMAC-SHA256 digest of the canonical request; the
            Secret Key (BP_SK) is NEVER included in this output.

        Wire format:
            Authorization: Bearer base64(SDK-HMAC-SHA256 Access=<AK>, SignedHeaders=<headers>, Signature=<hmac-hex>)
        """
        signed_headers_str = ";".join(signed_headers)
        # Structured signing string (AK is a public identifier; SK is not present here).
        auth_string = f"{Algorithm} Access={access_key}, SignedHeaders={signed_headers_str}, Signature={signature}"
        # Base64-encode per the WAPI gateway Bearer token format requirement.
        return "Bearer " + base64.b64encode(auth_string.encode()).decode()

    def canonical_request(self, method, url, headers, body, signed_headers):
        """Build the canonical request string for signing."""
        parsed_url = urlparse(url)
        canonical_uri = self.canionical_uri(parsed_url.path)
        sorted_query = sorted(parse_qs(parsed_url.query).items())
        canonical_query_string = urlencode(sorted_query, doseq=True)
        canonical_headers = self.canonical_headers(headers, signed_headers)
        signed_headers_str = ";".join(signed_headers)

        hexencode = headers.get(HeaderContentSha256, "")
        if not hexencode:
            hexencode = self.hash_sha256(body)

        return f"{method}\n{canonical_uri}\n{canonical_query_string}\n{canonical_headers}\n{signed_headers_str}\n{hexencode}"

    def canionical_uri(self, path):
        if not path or not path.endswith("/"):
            path += "/"
        return path

    def canonical_headers(self, headers, signed_headers):
        lowheaders = {key.lower(): value.strip() for key, value in headers.items()}
        a = [f"{key}:{lowheaders[key]}" for key in signed_headers]
        return "\n".join(a)

    def signed_headers(self, headers):
        signed_headers = [header.lower() for header in headers]
        signed_headers.sort()
        return signed_headers

    def sign(self, url, method, headers, body):
        dt = headers.get(HeaderXDate, "")
        if not dt:
            t = datetime.datetime.now(datetime.timezone.utc)
            headers[HeaderXDate] = t.strftime(BasicDateFormat)
        else:
            t = datetime.datetime.strptime(dt, BasicDateFormat)

        signed_headers = self.signed_headers(headers)
        canonical_request = self.canonical_request(method, url, headers, body, signed_headers)
        string_to_sign = self.string_to_sign(canonical_request, t.strftime(BasicDateFormat))
        signing_key = self.Secret.encode()
        signature = self.sign_string_to_sign(string_to_sign, signing_key)
        auth_value = self.auth_header_value(signature, self.Key, signed_headers)
        headers[HeaderAuthorization] = auth_value

        request = requests.Request(method, url, headers=headers, data=body)
        signed_request = request.prepare()
        return signed_request

    def string_to_sign(self, canonical_request, time_format):
        hash_obj = hashlib.sha256(canonical_request.encode())
        hash_hex = hash_obj.hexdigest()
        return f"{Algorithm}\n{time_format}\n{hash_hex}"

    def hash_sha256(self, data):
        hash_obj = hashlib.sha256(data.encode())
        return hash_obj.hexdigest()
