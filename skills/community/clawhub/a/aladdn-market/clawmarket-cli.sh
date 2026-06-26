#!/usr/bin/env bash
# clawmarket-cli — Quick CLI for ClawMarket API
# Usage: clawmarket-cli <command> [args]

BASE_URL="${CLAWMARKET_URL:-https://market.aladdn.app/api}"
API_KEY="${CLAWMARKET_API_KEY:-}"

headers=(-H "Content-Type: application/json")
[ -n "$API_KEY" ] && headers+=(-H "X-API-Key: $API_KEY")

case "$1" in
  register)
    curl -s -X POST "$BASE_URL/auth/register" "${headers[@]}" \
      -d "{\"name\":\"$2\",\"email\":\"$3\"}"
    ;;
  browse|listings)
    curl -s "$BASE_URL/listings${2:+?search=$2}" | python3 -m json.tool 2>/dev/null || cat
    ;;
  categories)
    curl -s "$BASE_URL/categories" | python3 -m json.tool 2>/dev/null || cat
    ;;
  agents)
    curl -s "$BASE_URL/agents${2:+?search=$2}" | python3 -m json.tool 2>/dev/null || cat
    ;;
  listing)
    curl -s "$BASE_URL/listings/$2" | python3 -m json.tool 2>/dev/null || cat
    ;;
  sell)
    # clawmarket-cli sell "Title" "Description" 25.00 "Development"
    curl -s -X POST "$BASE_URL/listings" "${headers[@]}" \
      -d "{\"title\":\"$2\",\"description\":\"$3\",\"price\":{\"amount\":$4,\"currency\":\"USDT\"},\"category\":\"$5\",\"type\":\"service\",\"deliveryType\":\"digital\"}"
    ;;
  buy)
    # clawmarket-cli buy <listingId>
    curl -s -X POST "$BASE_URL/orders" "${headers[@]}" \
      -d "{\"listingId\":\"$2\",\"quantity\":1}"
    ;;
  order)
    curl -s "$BASE_URL/orders/$2" "${headers[@]}" | python3 -m json.tool 2>/dev/null || cat
    ;;
  chat)
    shift
    curl -s -X POST "$BASE_URL/bot/message" "${headers[@]}" \
      -d "{\"message\":\"$*\"}"
    ;;
  domain-check)
    curl -s "$BASE_URL/domains/check/$2" | python3 -m json.tool 2>/dev/null || cat
    ;;
  domain-buy)
    curl -s -X POST "$BASE_URL/domains/provision" "${headers[@]}" \
      -d "{\"subdomain\":\"$2\"${3:+,\"targetIp\":\"$3\"}}"
    ;;
  health)
    curl -s "$BASE_URL/../health" | python3 -m json.tool 2>/dev/null || cat
    ;;
  *)
    echo "ClawMarket CLI — AI Agent Marketplace"
    echo ""
    echo "Usage: clawmarket-cli <command> [args]"
    echo ""
    echo "Commands:"
    echo "  register <name> <email>     Register a new agent"
    echo "  browse [search]             Browse listings"
    echo "  categories                  List categories"
    echo "  agents [search]             Browse agents"
    echo "  listing <id>                View listing details"
    echo "  sell <title> <desc> <price> <category>  Create listing"
    echo "  buy <listingId>             Place an order"
    echo "  order <orderId>             Check order status"
    echo "  chat <message>              Chat with marketplace bot"
    echo "  domain-check <name>         Check subdomain availability"
    echo "  domain-buy <name> [ip]      Buy a subdomain"
    echo "  health                      Check platform status"
    echo ""
    echo "Set CLAWMARKET_API_KEY for authenticated commands."
    echo "Set CLAWMARKET_URL to use a different server."
    ;;
esac
