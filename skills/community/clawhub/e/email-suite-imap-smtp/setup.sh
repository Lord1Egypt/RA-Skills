#!/bin/bash

# IMAP/SMTP Email Suite Setup
# Creates .env with email credentials

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Check for Node.js
check_node() {
    if ! command -v node &> /dev/null; then
        echo -e "${RED}  Node.js is not installed.${NC}"
        echo ""
        echo "  Install Node.js:"
        echo "    Ubuntu/Debian: sudo apt install nodejs npm"
        echo "    macOS: brew install node"
        echo "    Windows: Download from https://nodejs.org/"
        exit 1
    fi
    echo -e "  ${GREEN}Node.js $(node -v)${NC}"
}

# Check for npm
check_npm() {
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}  npm is not installed.${NC}"
        exit 1
    fi
    echo -e "  ${GREEN}npm $(npm -v)${NC}"
}

# Install dependencies
install_deps() {
    if [ ! -d "node_modules" ]; then
        echo "  Installing dependencies..."
        npm install --silent 2>/dev/null
        if [ $? -ne 0 ]; then
            echo -e "${RED}  Failed to install dependencies${NC}"
            exit 1
        fi
        echo -e "  ${GREEN}Dependencies installed${NC}"
    else
        echo -e "  ${GREEN}Dependencies installed${NC}"
    fi
}

show_banner() {
    echo ""
    echo "  ╔══════════════════════════════════════╗"
    echo "  ║    email-suite (imap+smtp) Setup   ║"
    echo "  ╚══════════════════════════════════════╝"
    echo ""
}

show_menu() {
    echo "  Provider          IMAP Host                  SMTP Host                  Port"
    echo "  ──────────────────────────────────────────────────────────────────────────"
    echo "  1) Gmail           imap.gmail.com             smtp.gmail.com             993 / 587"
    echo "  2) Outlook         outlook.office365.com     smtp.office365.com         993 / 587"
    echo "  3) Hostinger       imap.hostinger.com        smtp.hostinger.com          993 / 465"
    echo "  4) Custom          (you enter hosts/ports)  (you enter hosts/ports)"
    echo ""
    echo "  Next: credentials → display name → signature (y/n) → cert check → summary"
    echo ""
}

show_creds_menu() {
    echo ""
    echo "  ── Credentials ─────────────────────────────────────────────────────────"
    echo ""
    echo -n "  Email address: "
    read EMAIL
    echo -n "  Password / App Password: "
    read -s PASSWORD
    echo ""
    echo ""
    echo "  ── Sender Info ───────────────────────────────────────────────────────"
    echo ""
    echo -n "  Display Name (e.g. 'John Doe'): "
    read FROM_NAME
    echo ""
    echo "  ── Email Signature (optional) ────────────────────────────────────────"
    echo ""
    echo "  y) Add signature — appended to every sent email as -- / Name / Email"
    echo "  n) No signature"
    echo ""
    echo -n "  Choice (y/n, default n): "
    read ADD_SIGNATURE
    ADD_SIGNATURE=${ADD_SIGNATURE:-n}

    if [ "$ADD_SIGNATURE" = "y" ]; then
        echo ""
        echo -n "  Signature Name/Title: "
        read SIG_NAME
    fi
    echo ""
    echo "  ── Security ──────────────────────────────────────────────────────────"
    echo ""
    echo "  y) Accept self-signed certificates (for local/dev servers)"
    echo "  n) Reject unauthorized (recommended for production)"
    echo ""
    echo -n "  Choice (y/n, default n): "
    read ACCEPT_CERT
    ACCEPT_CERT=${ACCEPT_CERT:-n}
    echo ""
}

apply_provider() {
    case $PROVIDER_CHOICE in
        1)
            IMAP_HOST="imap.gmail.com"
            IMAP_PORT="993"
            SMTP_HOST="smtp.gmail.com"
            SMTP_PORT="587"
            SMTP_SECURE="false"
            IMAP_TLS="true"
            PROVIDER_NAME="Gmail"
            ;;
        2)
            IMAP_HOST="outlook.office365.com"
            IMAP_PORT="993"
            SMTP_HOST="smtp.office365.com"
            SMTP_PORT="587"
            SMTP_SECURE="false"
            IMAP_TLS="true"
            PROVIDER_NAME="Outlook"
            ;;
        3)
            IMAP_HOST="imap.hostinger.com"
            IMAP_PORT="993"
            SMTP_HOST="smtp.hostinger.com"
            SMTP_PORT="465"
            SMTP_SECURE="true"
            IMAP_TLS="true"
            PROVIDER_NAME="Hostinger"
            ;;
        4)
            echo ""
            echo -n "  IMAP Host: "; read IMAP_HOST
            echo -n "  IMAP Port (default 993): "; read IMAP_PORT
            IMAP_PORT=${IMAP_PORT:-993}
            echo -n "  SMTP Host: "; read SMTP_HOST
            echo -n "  SMTP Port (default 587): "; read SMTP_PORT
            SMTP_PORT=${SMTP_PORT:-587}
            echo -n "  IMAP TLS? (true/false, default true): "; read IMAP_TLS
            IMAP_TLS=${IMAP_TLS:-true}
            echo -n "  SMTP SSL (true=465 / false=587): "; read SMTP_SECURE
            SMTP_SECURE=${SMTP_SECURE:-false}
            PROVIDER_NAME="Custom"
            ;;
        *)
            echo -e "${RED}  Invalid choice${NC}"
            exit 1
            ;;
    esac
}

build_env() {
    if [ "$ACCEPT_CERT" = "y" ]; then
        REJECT_UNAUTHORIZED="false"
    else
        REJECT_UNAUTHORIZED="true"
    fi

    # Build signature
    EMAIL_SIGNATURE=""
    EMAIL_SIGNATURE_TEXT=""
    if [ "$ADD_SIGNATURE" = "y" ] && [ -n "$SIG_NAME" ]; then
        EMAIL_SIGNATURE="<p><br>--<br><strong>$SIG_NAME</strong><br><a href='mailto:$EMAIL'>$EMAIL</a></p>"
        EMAIL_SIGNATURE_TEXT="--
$SIG_NAME
$EMAIL"
    fi

    # Create .env file
    cat > .env << EOF
# IMAP Configuration
IMAP_HOST=$IMAP_HOST
IMAP_PORT=$IMAP_PORT
IMAP_USER=$EMAIL
IMAP_PASS=$PASSWORD
IMAP_TLS=$IMAP_TLS
IMAP_REJECT_UNAUTHORIZED=$REJECT_UNAUTHORIZED
IMAP_MAILBOX=INBOX

# SMTP Configuration
SMTP_HOST=$SMTP_HOST
SMTP_PORT=$SMTP_PORT
SMTP_SECURE=$SMTP_SECURE
SMTP_USER=$EMAIL
SMTP_PASS=$PASSWORD
SMTP_FROM=$EMAIL
SMTP_REJECT_UNAUTHORIZED=$REJECT_UNAUTHORIZED

# Sender Display Name
FROM_NAME="$FROM_NAME"
EOF

    if [ -n "$EMAIL_SIGNATURE" ]; then
        cat >> .env << EOF

# Email Signatures
EMAIL_SIGNATURE="$EMAIL_SIGNATURE"
EMAIL_SIGNATURE_TEXT="$EMAIL_SIGNATURE_TEXT"
EOF
    fi
}

test_connections() {
    echo "  Testing connections..."
    echo ""

    printf "  IMAP... "
    if node scripts/mail.js list-mailboxes >/dev/null 2>&1; then
        echo -e "${GREEN}Connected${NC}"
        IMAP_OK=true
    else
        echo -e "${RED}Failed${NC}"
        IMAP_OK=false
    fi

    printf "  SMTP... "
    if node scripts/mail.js test >/dev/null 2>&1; then
        echo -e "${GREEN}Connected${NC}"
        SMTP_OK=true
    else
        echo -e "${RED}Failed${NC}"
        SMTP_OK=false
    fi
}

# ── Main ─────────────────────────────────────────────────────────────────────

show_banner

echo "  Checking dependencies..."
echo ""
check_node
check_npm
install_deps

echo ""
echo -e "  ${YELLOW}Security reminder:${NC} This script creates a .env file with your credentials."
echo "  Never commit .env to git. Use App Passwords for Gmail/Outlook."
echo ""

show_menu

printf "  Select provider (1-4): "
read PROVIDER_CHOICE
apply_provider

show_creds_menu

echo "  ── Summary ─────────────────────────────────────────────────────────────"
echo "  Provider:     $PROVIDER_NAME"
echo "  Email:        $EMAIL"
echo "  IMAP:         $IMAP_HOST:$IMAP_PORT"
echo "  SMTP:         $SMTP_HOST:$SMTP_PORT"
echo -n "  Signature:   "
if [ "$ADD_SIGNATURE" = "y" ] && [ -n "$SIG_NAME" ]; then
    echo "\"$SIG_NAME\""
else
    echo "none"
fi
echo -n "  Certs:       "
if [ "$ACCEPT_CERT" = "y" ]; then
    echo "accept self-signed"
else
    echo "reject unauthorized (recommended)"
fi
echo ""
echo "  Creating .env..."
build_env

echo -e "  ${GREEN}.env created${NC}"
echo ""
echo -e "  Run: ${CYAN}chmod 600 .env${NC} to secure your credentials"
echo ""

test_connections

echo ""
if [ "$IMAP_OK" = true ] && [ "$SMTP_OK" = true ]; then
    echo -e "  ${GREEN}Setup complete!${NC}"
    echo ""
    echo "  Quick start:"
    echo "    node scripts/mail.js check          # View inbox"
    echo "    node scripts/mail.js fetch <uid>   # Read email"
    echo "    node scripts/mail.js --help        # Show all commands"
else
    echo -e "  ${YELLOW}Some connections failed. Check credentials in .env${NC}"
fi
echo ""
