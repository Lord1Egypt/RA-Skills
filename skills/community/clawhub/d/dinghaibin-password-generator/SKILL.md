---
name: password-generator
description: Generate secure passwords and passphrases. Use when user needs to create strong passwords, generate secure tokens, create PINs, or generate memorable passphrases.
---

# Password Generator

Generate secure passwords and passphrases.

## Quick Start

```bash
# Generate random password
python scripts/generate.py

# Specific length
python scripts/generate.py --length 16
```

## Usage

```bash
python scripts/generate.py [OPTIONS]

Options:
  --length NUM       Password length (default: 16)
  --numbers          Include numbers
  --symbols          Include special symbols
  --uppercase        Include uppercase letters
  --exclude CHARS   Exclude specific characters
  --pin              Generate PIN (4-6 digits)
  --passphrase       Generate passphrase
  --words NUM        Words in passphrase (default: 4)
  --count NUM        Number of passwords to generate
```

## Examples

```bash
# Simple password
python scripts/generate.py

# Strong password with all character types
python scripts/generate.py --length 20 --numbers --symbols --uppercase

# PIN code
python scripts/generate.py --pin

# Memorable passphrase
python scripts/generate.py --passphrase

# Multiple passwords
python scripts/generate.py --count 5
```

## Features

- Random password generation
- Configurable character sets
- PIN generation
- Passphrase generation
- Multiple password generation
- Secure random (os.urandom)
