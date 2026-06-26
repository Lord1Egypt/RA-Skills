#!/bin/bash
# AIClient2API Usage Checker with Auto-Refresh
# Automatically refreshes usage data before displaying

USAGE_FILE="$HOME/web/AIClient-2-API/configs/usage-cache.json"
API_URL="http://127.0.0.1:16825/api/usage?refresh=true"

echo "🔄 Refreshing usage data..."

# Try to trigger refresh via API (without auth, will use cache if auth fails)
REFRESH_RESULT=$(curl -s "$API_URL" 2>&1)

# Check if refresh was successful
if echo "$REFRESH_RESULT" | grep -q "UNAUTHORIZED"; then
    echo "⚠️  API authentication required, using cached data"
    echo ""
else
    echo "✅ Usage data refreshed"
    echo ""
fi

# Wait a moment for cache file to be updated
sleep 1

# Now run the regular check_usage.sh script
if [ ! -f "$USAGE_FILE" ]; then
    echo "❌ Error: Usage cache file not found at $USAGE_FILE"
    exit 1
fi

# Check if jq is available for better JSON parsing
if command -v jq &> /dev/null; then
    # Parse with jq for better formatting
    echo "📊 AIClient2API Usage Report"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Extract provider data (assuming claude-kiro-oauth is the main provider)
    PROVIDER_DATA=$(cat "$USAGE_FILE" | jq -r '.providers["claude-kiro-oauth"].instances[0]')
    
    if [ "$PROVIDER_DATA" != "null" ]; then
        # Account Info
        echo "👤 Account Information"
        echo "   Email: $(echo "$PROVIDER_DATA" | jq -r '.usage.user.email')"
        echo "   Subscription: $(echo "$PROVIDER_DATA" | jq -r '.usage.subscription.title')"
        echo ""
        
        # Free Trial
        TRIAL_STATUS=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].freeTrial.status')
        if [ "$TRIAL_STATUS" = "ACTIVE" ]; then
            echo "🎁 Free Trial (ACTIVE)"
            TRIAL_USED=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].freeTrial.currentUsage')
            TRIAL_LIMIT=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].freeTrial.usageLimit')
            TRIAL_REMAINING=$(echo "$TRIAL_LIMIT - $TRIAL_USED" | bc)
            TRIAL_PERCENT=$(echo "scale=2; $TRIAL_USED / $TRIAL_LIMIT * 100" | bc)
            TRIAL_EXPIRES=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].freeTrial.expiresAt')
            
            echo "   Used: $TRIAL_USED / $TRIAL_LIMIT Credits (${TRIAL_PERCENT}%)"
            echo "   Remaining: $TRIAL_REMAINING Credits"
            echo "   Expires: $TRIAL_EXPIRES"
            echo ""
        fi
        
        # Monthly Quota
        echo "📅 Monthly Quota"
        MONTHLY_USED=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].currentUsage')
        MONTHLY_LIMIT=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].usageLimit')
        MONTHLY_RESET=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].nextDateReset')
        
        echo "   Used: $MONTHLY_USED / $MONTHLY_LIMIT Credits"
        echo "   Resets: $MONTHLY_RESET"
        echo ""
        
        # Overage Info
        echo "💰 Overage Policy"
        OVERAGE_RATE=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].overageRate')
        OVERAGE_CAP=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].overageCap')
        OVERAGE_CHARGES=$(echo "$PROVIDER_DATA" | jq -r '.usage.usageBreakdown[0].overageCharges')
        
        echo "   Rate: \$$OVERAGE_RATE USD per invocation"
        echo "   Cap: $OVERAGE_CAP invocations"
        echo "   Current charges: \$$OVERAGE_CHARGES USD"
        echo ""
        
        # Health Status
        IS_HEALTHY=$(echo "$PROVIDER_DATA" | jq -r '.isHealthy')
        if [ "$IS_HEALTHY" = "true" ]; then
            echo "✅ Service Status: Healthy"
        else
            echo "⚠️ Service Status: Unhealthy"
        fi
    else
        echo "⚠️ No provider data found"
    fi
else
    # Fallback: just display the raw JSON if jq is not available
    echo "📊 AIClient2API Usage (Raw Data)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    cat "$USAGE_FILE"
    echo ""
    echo "💡 Tip: Install 'jq' for better formatted output: brew install jq"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Data source: $USAGE_FILE"
echo "🕐 Last updated: $(date -r "$USAGE_FILE" '+%Y-%m-%d %H:%M:%S')"
