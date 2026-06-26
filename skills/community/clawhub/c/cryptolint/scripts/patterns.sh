#!/usr/bin/env bash
# CryptoLint -- Cryptography Misuse Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Broken algorithm or direct security vulnerability
#   high     -- Significant cryptographic weakness requiring prompt attention
#   medium   -- Moderate concern that should be addressed in current sprint
#   low      -- Best practice suggestion or informational finding
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.
# - Use \b-free alternatives where boundary assertions are unavailable
#
# Categories:
#   WA (Weak Algorithms)           -- 15 patterns (WA-001 to WA-015)
#   KM (Key Management)            -- 15 patterns (KM-001 to KM-015)
#   EM (Encryption Modes)          -- 15 patterns (EM-001 to EM-015)
#   RN (Random Number Generation)  -- 15 patterns (RN-001 to RN-015)
#   TC (Timing & Comparison)       -- 15 patterns (TC-001 to TC-015)
#   CP (Certificate & Protocol)    -- 15 patterns (CP-001 to CP-015)

set -euo pipefail

# ============================================================================
# 1. WEAK ALGORITHMS (WA-001 through WA-015)
#    Detects deprecated/broken cryptographic algorithms: MD5, SHA1, DES, 3DES,
#    RC4, Blowfish, weak PBKDF2 iterations, deprecated TLS versions, MD4.
# ============================================================================

declare -a CRYPTOLINT_WA_PATTERNS=()

CRYPTOLINT_WA_PATTERNS+=(
  # WA-001: Java MD5 MessageDigest
  'MessageDigest\.getInstance\([[:space:]]*"MD5"|critical|WA-001|MD5 used for hashing (cryptographically broken, collision attacks trivial)|Replace MD5 with SHA-256 or SHA-3 for all security-sensitive hashing'

  # WA-002: Python MD5 usage
  'hashlib\.md5\(|critical|WA-002|Python MD5 used for hashing (cryptographically broken)|Use hashlib.sha256() or hashlib.sha3_256() instead'

  # WA-003: Node.js MD5 hash
  'createHash\([[:space:]]*["\x27]md5|critical|WA-003|Node.js MD5 hash (cryptographically broken)|Use crypto.createHash("sha256") instead'

  # WA-004: Java SHA-1 MessageDigest
  'MessageDigest\.getInstance\([[:space:]]*"SHA-?1"|critical|WA-004|SHA-1 used for hashing (collision attacks demonstrated)|Replace SHA-1 with SHA-256 or SHA-3 for all security-sensitive hashing'

  # WA-005: Python SHA-1 usage
  'hashlib\.sha1\(|critical|WA-005|Python SHA-1 used for hashing (collision attacks demonstrated)|Use hashlib.sha256() or hashlib.sha3_256() instead'

  # WA-006: Node.js SHA-1 hash
  'createHash\([[:space:]]*["\x27]sha1|critical|WA-006|Node.js SHA-1 hash (collision attacks demonstrated)|Use crypto.createHash("sha256") instead'

  # WA-007: DES encryption algorithm
  'DES/|critical|WA-007|DES encryption used (56-bit key, trivially breakable)|Replace DES with AES-256-GCM for authenticated encryption'

  # WA-008: Java DES Cipher instance
  'Cipher\.getInstance\([[:space:]]*"DES|critical|WA-008|Java DES cipher (56-bit key, trivially breakable)|Use Cipher.getInstance("AES/GCM/NoPadding") with 256-bit keys'

  # WA-009: RC4 stream cipher usage
  'RC4|critical|WA-009|RC4 stream cipher used (multiple known biases and attacks)|Replace RC4 with AES-GCM or ChaCha20-Poly1305'

  # WA-010: Triple DES (3DES) usage
  'DESede|high|WA-010|Triple DES (3DES) used (deprecated, limited to 112-bit security)|Replace 3DES with AES-256-GCM for modern authenticated encryption'

  # WA-011: Blowfish for new encryption
  'Blowfish|high|WA-011|Blowfish cipher used (64-bit block size vulnerable to birthday attacks)|Use AES-256-GCM or ChaCha20-Poly1305 for new encryption needs'

  # WA-012: Weak PBKDF2 iterations (under 10000)
  'pbkdf2.*iterations[[:space:]]*[:=][[:space:]]*[0-9]{1,4}[^0-9]|high|WA-012|PBKDF2 with fewer than 10000 iterations (too fast for password hashing)|Use at least 600000 iterations for PBKDF2-SHA256, or prefer Argon2id'

  # WA-013: TLS 1.0 protocol version
  'TLSv1["\x27[:space:],)]|high|WA-013|TLS 1.0 protocol used (deprecated, known vulnerabilities BEAST/POODLE)|Upgrade to TLS 1.2 minimum, prefer TLS 1.3'

  # WA-014: Go MD5 package import
  'crypto/md5|critical|WA-014|Go MD5 package imported (cryptographically broken)|Use crypto/sha256 or golang.org/x/crypto/sha3 instead'

  # WA-015: C# MD5 provider
  'MD5CryptoServiceProvider|critical|WA-015|C# MD5CryptoServiceProvider used (cryptographically broken)|Use SHA256CryptoServiceProvider or SHA256.Create() instead'
)

# ============================================================================
# 2. KEY MANAGEMENT (KM-001 through KM-015)
#    Detects hardcoded encryption keys, keys shorter than 128 bits, hardcoded
#    IVs, zero IVs, static salts, keys in source code as hex/base64 strings.
# ============================================================================

declare -a CRYPTOLINT_KM_PATTERNS=()

CRYPTOLINT_KM_PATTERNS+=(
  # KM-001: Java hardcoded SecretKeySpec with short key
  'new SecretKeySpec\([[:space:]]*"[^"]{1,15}"\.getBytes|critical|KM-001|Hardcoded encryption key shorter than 128 bits in Java|Use a secure key derivation function (HKDF, PBKDF2) with random salt'

  # KM-002: Python hardcoded AES key
  'AES\.new\([[:space:]]*b"[^"]+"|critical|KM-002|Hardcoded AES key in Python source code|Load keys from secure key management system (AWS KMS, Vault), never hardcode'

  # KM-003: Hardcoded IV with all zeros
  'new IvParameterSpec\([[:space:]]*new byte\[|critical|KM-003|Zero or static initialization vector (IV) in Java (destroys IND-CPA security)|Generate a fresh random IV for each encryption operation using SecureRandom'

  # KM-004: Python static IV bytes
  'iv[[:space:]]*=[[:space:]]*b"[^"]+"|high|KM-004|Hardcoded initialization vector (IV) in Python source code|Generate a random IV with os.urandom(16) for each encryption operation'

  # KM-005: Node.js hardcoded key buffer
  'Buffer\.from\([[:space:]]*["\x27][0-9a-fA-F]{16,}["\x27]|critical|KM-005|Hardcoded encryption key as hex string in Node.js source|Use crypto.randomBytes() for key generation or load from key management service'

  # KM-006: Hardcoded encryption key assignment
  'encryption[_-]?key[[:space:]]*=[[:space:]]*["\x27][^"\x27]{8,}["\x27]|critical|KM-006|Hardcoded encryption key assigned in source code|Store keys in environment variables or key management service, never in source'

  # KM-007: Static salt for password hashing
  'salt[[:space:]]*=[[:space:]]*["\x27][^"\x27]+["\x27]|high|KM-007|Static salt value hardcoded in source code|Generate a unique random salt per password using crypto-secure random generator'

  # KM-008: AES key with insufficient length (less than 128 bits)
  'SecretKeySpec\([[:space:]]*[a-zA-Z_]+[[:space:]]*,[[:space:]]*"AES"\).*\.[[:space:]]*length[[:space:]]*<[[:space:]]*16|high|KM-008|AES key potentially shorter than 128 bits|Use 256-bit (32-byte) keys for AES; generate with SecureRandom'

  # KM-009: Node.js createCipheriv with hardcoded key
  'createCipheriv\([[:space:]]*["\x27][^"\x27]+["\x27][[:space:]]*,[[:space:]]*["\x27]|critical|KM-009|Hardcoded key passed directly to Node.js createCipheriv|Use crypto.randomBytes(32) for key generation; store keys securely'

  # KM-010: Hardcoded nonce value
  'nonce[[:space:]]*=[[:space:]]*["\x27][^"\x27]+["\x27]|high|KM-010|Hardcoded nonce value in source code (nonce reuse breaks encryption)|Generate a unique random nonce for each encryption with secure random generator'

  # KM-011: Java hardcoded SecretKeySpec with string
  'new SecretKeySpec\([[:space:]]*"[^"]+"\.getBytes|critical|KM-011|Hardcoded string used as encryption key in Java SecretKeySpec|Derive keys using PBKDF2/HKDF with random salt, or use a KMS'

  # KM-012: Hardcoded private key content
  'PRIVATE KEY-----[[:space:]]*["\x27]|critical|KM-012|Private key material embedded in source code|Store private keys in secure key stores (HSM, KMS), never in source code'

  # KM-013: Empty or null salt
  'salt[[:space:]]*=[[:space:]]*["\x27]["\x27]|critical|KM-013|Empty salt value used for password hashing (effectively no salt)|Generate a unique cryptographically random salt of at least 16 bytes'

  # KM-014: Go hardcoded AES key
  '\[\]byte\([[:space:]]*"[^"]{16,}"|critical|KM-014|Hardcoded byte slice used as encryption key in Go|Use crypto/rand to generate keys; store in environment or KMS'

  # KM-015: C# hardcoded key bytes
  'new byte\[\][[:space:]]*\{[[:space:]]*0x[0-9a-fA-F]+|high|KM-015|Hardcoded key byte array in C# source code|Use RNGCryptoServiceProvider to generate keys; store in Azure Key Vault or similar'
)

# ============================================================================
# 3. ENCRYPTION MODES (EM-001 through EM-015)
#    Detects ECB mode usage, CBC without authentication, missing IV for CBC,
#    unauthenticated encryption, raw RSA without padding, custom crypto.
# ============================================================================

declare -a CRYPTOLINT_EM_PATTERNS=()

CRYPTOLINT_EM_PATTERNS+=(
  # EM-001: AES/ECB mode in Java
  'AES/ECB|critical|EM-001|AES ECB mode used (leaks patterns in ciphertext, not semantically secure)|Use AES/GCM/NoPadding for authenticated encryption'

  # EM-002: Python ECB mode constant
  'MODE_ECB|critical|EM-002|ECB encryption mode used in Python (leaks plaintext patterns)|Use AES.MODE_GCM or AES.MODE_CBC with separate HMAC for authenticated encryption'

  # EM-003: Node.js AES-ECB cipher
  'createCipheriv\([[:space:]]*["\x27]aes-[0-9]+-ecb|critical|EM-003|Node.js AES-ECB mode used (leaks plaintext patterns)|Use aes-256-gcm for authenticated encryption'

  # EM-004: RSA without OAEP padding
  'RSA/NONE|critical|EM-004|RSA used without padding (textbook RSA, trivially breakable)|Use RSA/ECB/OAEPWithSHA-256AndMGF1Padding for RSA encryption'

  # EM-005: RSA with PKCS1 v1.5 padding
  'PKCS1Padding|high|EM-005|RSA with PKCS#1 v1.5 padding (vulnerable to Bleichenbacher attack)|Use OAEP padding: RSA/ECB/OAEPWithSHA-256AndMGF1Padding'

  # EM-006: Java NoPadding with CBC
  'CBC/NoPadding|high|EM-006|CBC mode with NoPadding (may enable padding oracle if error messages differ)|Use AES/GCM/NoPadding for authenticated encryption instead of CBC'

  # EM-007: Python CBC without HMAC nearby
  'AES\.MODE_CBC|medium|EM-007|AES-CBC mode used (requires separate HMAC for authentication)|Prefer AES-GCM for built-in authentication, or add HMAC-SHA256 verification'

  # EM-008: Node.js CBC cipher
  'createCipheriv\([[:space:]]*["\x27]aes-[0-9]+-cbc|medium|EM-008|Node.js AES-CBC used (no built-in authentication)|Use aes-256-gcm which provides built-in authentication'

  # EM-009: Go ECB mode (no IV in cipher.NewCBCEncrypter-like pattern)
  'NewECBEncrypter|critical|EM-009|Go ECB mode encrypter used (leaks plaintext patterns)|Use cipher.NewGCM() for authenticated encryption'

  # EM-010: Custom XOR encryption implementation
  '\^[[:space:]]*0x[0-9a-fA-F]+.*[Ee]ncrypt|high|EM-010|XOR-based custom encryption detected (trivially breakable)|Use established AES-GCM or ChaCha20-Poly1305 instead of custom crypto'

  # EM-011: Python Fernet without key rotation
  'Fernet\.generate_key\(\).*=.*["\x27]|medium|EM-011|Fernet key hardcoded or stored inline (no key rotation)|Use a key management service and implement key rotation policy'

  # EM-012: ECB in .NET
  'CipherMode\.ECB|critical|EM-012|C# ECB cipher mode used (leaks plaintext patterns)|Use CipherMode.GCM or implement encrypt-then-MAC with CBC'

  # EM-013: Go DES cipher
  'des\.NewCipher|critical|EM-013|Go DES cipher used (56-bit key, trivially breakable)|Use aes.NewCipher with 256-bit key and GCM mode'

  # EM-014: Deprecated createCipher (no IV)
  'crypto\.createCipher\(|critical|EM-014|Node.js deprecated createCipher used (derives IV from key, insecure)|Use crypto.createCipheriv() with explicit random IV'

  # EM-015: Raw block cipher without mode
  'Cipher\.getInstance\([[:space:]]*"AES"\)|high|EM-015|Java AES cipher without explicit mode (defaults to ECB on most providers)|Specify mode explicitly: Cipher.getInstance("AES/GCM/NoPadding")'
)

# ============================================================================
# 4. RANDOM NUMBER GENERATION (RN-001 through RN-015)
#    Detects Math.random() for security, java.util.Random for crypto, Python
#    random module for tokens, time-seeded RNG, predictable seeds.
# ============================================================================

declare -a CRYPTOLINT_RN_PATTERNS=()

CRYPTOLINT_RN_PATTERNS+=(
  # RN-001: Math.random() for token generation
  'Math\.random\(\).*[Tt]oken|critical|RN-001|Math.random() used for token generation (predictable, not cryptographic)|Use crypto.randomBytes() or crypto.getRandomValues() for security tokens'

  # RN-002: java.util.Random for key generation
  'new Random\(\).*[Kk]ey|critical|RN-002|java.util.Random used for key generation (predictable PRNG)|Use java.security.SecureRandom for all cryptographic randomness'

  # RN-003: Python random for secrets
  'random\.randint.*[Ss]ecret|critical|RN-003|Python random module used for secrets (predictable Mersenne Twister)|Use secrets module: secrets.token_hex() or secrets.token_urlsafe()'

  # RN-004: Math.random() for password/key material
  'Math\.random\(\).*[Pp]ass|critical|RN-004|Math.random() used for password generation (predictable)|Use crypto.getRandomValues() or crypto.randomBytes() for passwords'

  # RN-005: java.util.Random for nonce/IV
  'new Random\(\).*[Nn]once|critical|RN-005|java.util.Random used for nonce generation (predictable PRNG)|Use SecureRandom for nonce generation to prevent nonce reuse attacks'

  # RN-006: Python random for token generation
  'random\.[a-z]+\(.*[Tt]oken|critical|RN-006|Python random module used for token generation (predictable)|Use secrets.token_hex() or secrets.token_urlsafe() for tokens'

  # RN-007: Time-based seed for Random
  'Random\([[:space:]]*System\.currentTimeMillis|critical|RN-007|java.util.Random seeded with currentTimeMillis (predictable seed)|Use SecureRandom which seeds from OS entropy source'

  # RN-008: srand with time seed in C/C++
  'srand\([[:space:]]*time\(|critical|RN-008|C/C++ rand() seeded with time (predictable for crypto purposes)|Use platform-specific CSPRNG: /dev/urandom, BCryptGenRandom, or arc4random'

  # RN-009: Math.random for UUID/ID generation
  'Math\.random\(\).*[Ii]d|high|RN-009|Math.random() used for ID generation (predictable, may be guessable)|Use crypto.randomUUID() or uuid library with crypto-secure random source'

  # RN-010: Go math/rand for crypto
  'math/rand|high|RN-010|Go math/rand package used (not cryptographically secure)|Use crypto/rand for all security-sensitive random number generation'

  # RN-011: Python random.seed with fixed value
  'random\.seed\([[:space:]]*[0-9]+\)|high|RN-011|Python random module seeded with fixed value (deterministic output)|Use secrets module for security-sensitive randomness (no seeding needed)'

  # RN-012: C# System.Random for crypto
  'new System\.Random\(\).*[Cc]rypto|critical|RN-012|C# System.Random used in crypto context (not cryptographically secure)|Use System.Security.Cryptography.RandomNumberGenerator for crypto randomness'

  # RN-013: rand() function in crypto context
  'rand\(\).*[Ee]ncrypt|high|RN-013|C/C++ rand() used in encryption context (predictable LCG)|Use platform CSPRNG: getrandom(), BCryptGenRandom, or arc4random_buf()'

  # RN-014: Math.random for salt generation
  'Math\.random\(\).*[Ss]alt|critical|RN-014|Math.random() used for salt generation (predictable)|Use crypto.randomBytes(16) to generate cryptographically random salts'

  # RN-015: Python random for IV generation
  'random\.[a-z]+\(.*[Ii][Vv]|critical|RN-015|Python random module used for IV generation (predictable)|Use os.urandom(16) or secrets.token_bytes(16) for IV generation'
)

# ============================================================================
# 5. TIMING & COMPARISON (TC-001 through TC-015)
#    Detects string equality for password/hash comparison, == for HMAC
#    verification, non-constant-time comparisons for crypto values.
# ============================================================================

declare -a CRYPTOLINT_TC_PATTERNS=()

CRYPTOLINT_TC_PATTERNS+=(
  # TC-001: String equality for hash comparison
  '==[[:space:]]*["\x27]?[a-zA-Z_]*[Hh]ash|high|TC-001|String equality comparison for hash verification (timing side-channel)|Use constant-time comparison: crypto.timingSafeEqual() or MessageDigest.isEqual()'

  # TC-002: String.equals for HMAC verification
  '\.equals\(.*[Hh]mac|high|TC-002|String.equals() for HMAC verification (timing side-channel attack)|Use MessageDigest.isEqual() for constant-time HMAC comparison in Java'

  # TC-003: Direct password string comparison
  '\.password[[:space:]]*==[[:space:]]|high|TC-003|Direct password comparison with == operator (timing side-channel)|Use bcrypt.compare() or constant-time comparison function for passwords'

  # TC-004: Triple equals for token comparison in JS
  '===[[:space:]]*[a-zA-Z_]*[Tt]oken|high|TC-004|JavaScript === used for token comparison (timing side-channel)|Use crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b)) for tokens'

  # TC-005: Python == for digest comparison
  '==[[:space:]]*[a-zA-Z_]*digest|high|TC-005|Python == operator for digest comparison (timing side-channel)|Use hmac.compare_digest() for constant-time comparison of digests'

  # TC-006: strcmp for password/hash comparison
  'strcmp\(.*[Pp]assword|high|TC-006|strcmp() used for password comparison (timing side-channel attack)|Use constant-time comparison function or bcrypt_verify equivalent'

  # TC-007: String comparison for API key validation
  '==[[:space:]]*[a-zA-Z_]*api[_-]?[Kk]ey|high|TC-007|String equality for API key comparison (timing side-channel)|Use constant-time comparison for all secret value comparisons'

  # TC-008: Direct signature comparison
  '==[[:space:]]*[a-zA-Z_]*[Ss]ignature|high|TC-008|Direct equality comparison for cryptographic signature (timing attack)|Use constant-time comparison function for signature verification'

  # TC-009: Ruby == for digest comparison
  '==[[:space:]]*OpenSSL::Digest|high|TC-009|Ruby == operator for OpenSSL digest comparison (timing side-channel)|Use Rack::Utils.secure_compare() or ActiveSupport::SecurityUtils.secure_compare()'

  # TC-010: Go bytes comparison for crypto
  '==[[:space:]]*.*\[\]byte.*[Hh]ash|high|TC-010|Go == operator for hash byte comparison (timing side-channel)|Use crypto/subtle.ConstantTimeCompare() for hash comparisons'

  # TC-011: PHP == for hash comparison
  '==[[:space:]]*["\x27]?[a-fA-F0-9]{32,}|high|TC-011|Direct comparison with hex hash string (timing side-channel)|Use hash_equals() in PHP or equivalent constant-time function'

  # TC-012: Early return in authentication check
  'if[[:space:]]*\(.*password.*\)[[:space:]]*return[[:space:]]*false|medium|TC-012|Early return on password mismatch (potential timing oracle)|Use constant-time comparison; always complete full comparison before returning'

  # TC-013: C# string comparison for secrets
  '\.Equals\(.*[Ss]ecret|high|TC-013|C# String.Equals for secret comparison (timing side-channel)|Use CryptographicOperations.FixedTimeEquals() for secret comparisons'

  # TC-014: Node.js buffer comparison for keys
  '!==.*[Kk]ey|medium|TC-014|JavaScript !== operator for key comparison (potential timing leak)|Use crypto.timingSafeEqual() for all cryptographic value comparisons'

  # TC-015: Python != for token comparison
  '!=[[:space:]]*[a-zA-Z_]*token|medium|TC-015|Python != operator for token comparison (potential timing side-channel)|Use hmac.compare_digest() for constant-time token comparison'
)

# ============================================================================
# 6. CERTIFICATE & PROTOCOL (CP-001 through CP-015)
#    Detects SSL/TLS verification disabled, certificate pinning bypassed,
#    HTTP in crypto contexts, insecure protocol versions, hostname verification
#    disabled, self-signed cert acceptance.
# ============================================================================

declare -a CRYPTOLINT_CP_PATTERNS=()

CRYPTOLINT_CP_PATTERNS+=(
  # CP-001: Python SSL verification disabled
  'verify[[:space:]]*=[[:space:]]*False.*ssl|critical|CP-001|SSL certificate verification disabled in Python (MITM vulnerability)|Enable certificate verification; use verify=True with trusted CA bundle'

  # CP-002: Python InsecureRequestWarning suppressed
  'InsecureRequestWarning|high|CP-002|InsecureRequestWarning suppressed (hiding TLS certificate issues)|Fix the underlying TLS/SSL issue instead of suppressing security warnings'

  # CP-003: Node.js TLS verification disabled
  'rejectUnauthorized[[:space:]]*:[[:space:]]*false|critical|CP-003|Node.js TLS certificate verification disabled (MITM vulnerability)|Set rejectUnauthorized: true and use proper CA certificates'

  # CP-004: Java SSL trust all certificates
  'TrustAllCertificates|critical|CP-004|Java trust-all-certificates pattern (disables certificate validation)|Use default TrustManager with proper CA certificates from system trust store'

  # CP-005: Python ssl CERT_NONE
  'ssl\.CERT_NONE|critical|CP-005|Python SSL context set to CERT_NONE (no certificate verification)|Use ssl.CERT_REQUIRED with proper CA bundle for certificate validation'

  # CP-006: Java hostname verifier disabled
  'ALLOW_ALL_HOSTNAME_VERIFIER|critical|CP-006|Java ALLOW_ALL_HOSTNAME_VERIFIER used (hostname check bypassed)|Use default hostname verifier; never disable hostname verification'

  # CP-007: Go InsecureSkipVerify
  'InsecureSkipVerify[[:space:]]*:[[:space:]]*true|critical|CP-007|Go TLS InsecureSkipVerify enabled (no certificate validation)|Set InsecureSkipVerify: false and configure proper root CA pool'

  # CP-008: SSL v2/v3 protocol usage
  'SSLv[23]|critical|CP-008|SSLv2/SSLv3 protocol used (severely broken, POODLE/DROWN attacks)|Use TLS 1.2 minimum, prefer TLS 1.3'

  # CP-009: Python requests verify=False
  'requests\.[a-z]+\(.*verify[[:space:]]*=[[:space:]]*False|critical|CP-009|Python requests library with certificate verification disabled|Use verify=True (default) and ensure proper CA certificates are installed'

  # CP-010: Node.js NODE_TLS_REJECT_UNAUTHORIZED
  'NODE_TLS_REJECT_UNAUTHORIZED[[:space:]]*=[[:space:]]*["\x27]?0|critical|CP-010|NODE_TLS_REJECT_UNAUTHORIZED set to 0 (global TLS verification disabled)|Remove this setting; fix certificate issues properly instead'

  # CP-011: C# ServerCertificateValidationCallback bypass
  'ServerCertificateValidationCallback[[:space:]]*=[[:space:]]*.*true|critical|CP-011|C# ServerCertificateValidationCallback always returns true (no validation)|Implement proper certificate validation in the callback'

  # CP-012: Java X509TrustManager with empty check
  'checkServerTrusted.*\{\}|critical|CP-012|Java X509TrustManager with empty checkServerTrusted (no certificate validation)|Use default X509TrustManager or implement proper certificate chain validation'

  # CP-013: TLS 1.1 protocol version
  'TLSv1\.1|high|CP-013|TLS 1.1 protocol used (deprecated, known weaknesses)|Upgrade to TLS 1.2 minimum, prefer TLS 1.3'

  # CP-014: HTTP URL in crypto/auth context
  'http://.*[Aa]uth|high|CP-014|HTTP (not HTTPS) URL used in authentication context (credentials sent in cleartext)|Use HTTPS for all authentication and API endpoints'

  # CP-015: Java setDefaultHostnameVerifier override
  'setDefaultHostnameVerifier.*\{[[:space:]]*return[[:space:]]*true|critical|CP-015|Java default hostname verifier overridden to always return true|Use default hostname verification; never bypass hostname checks'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
cryptolint_pattern_count() {
  local count=0
  count=$((count + ${#CRYPTOLINT_WA_PATTERNS[@]}))
  count=$((count + ${#CRYPTOLINT_KM_PATTERNS[@]}))
  count=$((count + ${#CRYPTOLINT_EM_PATTERNS[@]}))
  count=$((count + ${#CRYPTOLINT_RN_PATTERNS[@]}))
  count=$((count + ${#CRYPTOLINT_TC_PATTERNS[@]}))
  count=$((count + ${#CRYPTOLINT_CP_PATTERNS[@]}))
  echo "$count"
}

# Get pattern count for a specific category
cryptolint_category_count() {
  local category="$1"
  local patterns_name
  patterns_name=$(get_cryptolint_patterns_for_category "$category")
  if [[ -z "$patterns_name" ]]; then
    echo 0
    return
  fi
  local -n _ref="$patterns_name"
  echo "${#_ref[@]}"
}

# Get patterns array name for a category
get_cryptolint_patterns_for_category() {
  local category="$1"
  case "$category" in
    WA|wa) echo "CRYPTOLINT_WA_PATTERNS" ;;
    KM|km) echo "CRYPTOLINT_KM_PATTERNS" ;;
    EM|em) echo "CRYPTOLINT_EM_PATTERNS" ;;
    RN|rn) echo "CRYPTOLINT_RN_PATTERNS" ;;
    TC|tc) echo "CRYPTOLINT_TC_PATTERNS" ;;
    CP|cp) echo "CRYPTOLINT_CP_PATTERNS" ;;
    *)     echo "" ;;
  esac
}

# Get the human-readable label for a category
get_cryptolint_category_label() {
  local category="$1"
  case "$category" in
    WA|wa) echo "Weak Algorithms" ;;
    KM|km) echo "Key Management" ;;
    EM|em) echo "Encryption Modes" ;;
    RN|rn) echo "Random Number Generation" ;;
    TC|tc) echo "Timing & Comparison" ;;
    CP|cp) echo "Certificate & Protocol" ;;
    *)     echo "$category" ;;
  esac
}

# All category codes for iteration
get_all_cryptolint_categories() {
  echo "WA KM EM RN TC CP"
}

# Get categories available for a given tier level
# free=0 -> WA, KM (30 patterns)
# pro=1  -> WA, KM, EM, RN (60 patterns)
# team=2 -> all 6 (90 patterns)
# enterprise=3 -> all 6 (90 patterns)
get_cryptolint_categories_for_tier() {
  local tier_level="${1:-0}"
  if [[ "$tier_level" -ge 2 ]]; then
    echo "WA KM EM RN TC CP"
  elif [[ "$tier_level" -ge 1 ]]; then
    echo "WA KM EM RN"
  else
    echo "WA KM"
  fi
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# List patterns by category
cryptolint_list_patterns() {
  local filter_category="${1:-all}"

  if [[ "$filter_category" == "all" ]]; then
    for cat in WA KM EM RN TC CP; do
      cryptolint_list_patterns "$cat"
    done
    return
  fi

  local patterns_name
  patterns_name=$(get_cryptolint_patterns_for_category "$filter_category")
  if [[ -z "$patterns_name" ]]; then
    echo "Unknown category: $filter_category"
    return 1
  fi

  local -n _patterns_ref="$patterns_name"
  local label
  label=$(get_cryptolint_category_label "$filter_category")

  echo "  ${label} (${filter_category}):"
  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "    %-8s %-10s %s\n" "$check_id" "$severity" "$description"
  done
  echo ""
}

# Validate that a category code is valid
is_valid_cryptolint_category() {
  local category="$1"
  case "$category" in
    WA|wa|KM|km|EM|em|RN|rn|TC|tc|CP|cp) return 0 ;;
    *) return 1 ;;
  esac
}
