#!/usr/bin/env bash
set -euo pipefail

# Daily Cost Report Script for OpenClaw
# Aggregates token usage and costs by agent, channel, and model

# --- Configuration ---
OPENCLAW_BIN="$HOME/homebrew/bin/openclaw"
export PATH="$HOME/homebrew/bin:$PATH"

# --- Argument Parsing ---
TARGET_DATE="${1:-yesterday}"

if [ "$TARGET_DATE" = "yesterday" ]; then
    TARGET_DATE=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d "yesterday" +%Y-%m-%d 2>/dev/null)
elif [ "$TARGET_DATE" = "today" ]; then
    TARGET_DATE=$(date +%Y-%m-%d)
fi

# Calculate start/end timestamps (midnight to midnight in local time)
START_TS=$(date -j -f "%Y-%m-%d %H:%M:%S" "$TARGET_DATE 00:00:00" +%s 2>/dev/null || date -d "$TARGET_DATE 00:00:00" +%s)
END_TS=$(date -j -f "%Y-%m-%d %H:%M:%S" "$TARGET_DATE 23:59:59" +%s 2>/dev/null || date -d "$TARGET_DATE 23:59:59" +%s)

# Convert to milliseconds for comparison
START_MS=$((START_TS * 1000))
END_MS=$((END_TS * 1000))

OUTPUT_FILE="/tmp/cost-report-${TARGET_DATE}.md"
TEMP_DIR="/tmp/cost-report-$$"
mkdir -p "$TEMP_DIR"

echo "🐈‍⬛ Generating cost report for $TARGET_DATE"
echo "   Start: $(date -r $START_TS '+%Y-%m-%d %H:%M:%S %Z')"
echo "   End:   $(date -r $END_TS '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

# --- Fetch Session Data ---
SESSIONS_JSON=$("$OPENCLAW_BIN" sessions --all-agents --json 2>/dev/null)

# Filter sessions by date range and add cost calculation
PROCESSED_DATA=$(echo "$SESSIONS_JSON" | jq -r --argjson start "$START_MS" --argjson end "$END_MS" '
# Model pricing per 1M tokens
def model_pricing:
  {
    "claude-haiku-4-5": {input: 1, output: 5, cache_read: 0.1, cache_write: 2},
    "claude-sonnet-4-5": {input: 3, output: 15, cache_read: 0.3, cache_write: 6},
    "claude-opus-4-6": {input: 5, output: 25, cache_read: 0.5, cache_write: 10},
    "deepseek/deepseek-v3.2": {input: 0.32, output: 0.89, cache_read: 0, cache_write: 0},
    "openai/gpt-4o-mini": {input: 0.15, output: 0.6, cache_read: 0, cache_write: 0}
  };

.sessions[]
| select(.updatedAt >= $start and .updatedAt <= $end)
| select(.totalTokens != null and .totalTokens > 0)
| . as $session
| ($session.inputTokens // 0) as $input
| ($session.outputTokens // 0) as $output
| ($session.cacheCreationInputTokens // 0) as $cache_write
| ($session.cacheReadInputTokens // 0) as $cache_read
| model_pricing[.model] as $pricing
| (if $pricing then
    (($input / 1000000) * $pricing.input) +
    (($output / 1000000) * $pricing.output) +
    (($cache_read / 1000000) * $pricing.cache_read) +
    (($cache_write / 1000000) * $pricing.cache_write)
  else 0 end) as $cost
| (if $pricing then
    (($cache_read / 1000000) * ($pricing.input - $pricing.cache_read))
  else 0 end) as $savings
| [
    .key,
    .agentId,
    (.key | split(":")[2] // "unknown"),
    .model,
    $input,
    $output,
    (.totalTokens // 0),
    $cache_write,
    $cache_read,
    $cost,
    $savings
  ]
| @tsv
')

if [ -z "$PROCESSED_DATA" ]; then
    echo "No sessions found for $TARGET_DATE"
    cat > "$OUTPUT_FILE" <<EOF
# OpenClaw Daily Cost Report
**Date:** $TARGET_DATE

No sessions found with token usage for this date.
EOF
    cat "$OUTPUT_FILE"
    rm -rf "$TEMP_DIR"
    exit 0
fi

# --- Calculate Aggregates ---
echo "$PROCESSED_DATA" | awk -F'\t' '
{
    agent = $2
    channel = $3
    model = $4
    input = $5
    output = $6
    tokens = $7
    cache_write = $8
    cache_read = $9
    cost = $10
    savings = $11
    
    printf "agent\t%s\t%s\t%s\t%s\t%s\n", agent, cost, tokens, input, output
    printf "model\t%s\t%s\t%s\t%s\t%s\n", model, cost, tokens, input, output
    printf "channel\t%s\t%s\t%s\n", channel, cost, tokens
    printf "total\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", "all", cost, tokens, input, output, cache_write, cache_read, savings
    printf "session\t%s\t%s\t%s\t%s\t%s\t%s\n", $1, agent, model, channel, tokens, cost
}
' > "$TEMP_DIR/raw_data.txt"

# Calculate totals
TOTALS=$(awk '$1 == "total"' "$TEMP_DIR/raw_data.txt" | awk '{
    cost += $3
    tokens += $4
    input += $5
    output += $6
    cache_write += $7
    cache_read += $8
    savings += $9
}
END {
    printf "%.4f %d %d %d %d %d %.4f", cost, tokens, input, output, cache_write, cache_read, savings
}')

read TOTAL_COST TOTAL_TOKENS TOTAL_INPUT TOTAL_OUTPUT TOTAL_CACHE_WRITE TOTAL_CACHE_READ TOTAL_SAVINGS <<< "$TOTALS"

# Aggregate by agent
awk '$1 == "agent"' "$TEMP_DIR/raw_data.txt" | awk '{
    agent = $2
    cost[agent] += $3
    tokens[agent] += $4
    input[agent] += $5
    output[agent] += $6
}
END {
    for (a in cost) {
        printf "%s\t%.4f\t%d\t%d\t%d\n", a, cost[a], tokens[a], input[a], output[a]
    }
}' | sort -t$'\t' -k2 -rn > "$TEMP_DIR/by_agent.txt"

# Aggregate by model
awk '$1 == "model"' "$TEMP_DIR/raw_data.txt" | awk '{
    model = $2
    cost[model] += $3
    tokens[model] += $4
    input[model] += $5
    output[model] += $6
}
END {
    for (m in cost) {
        printf "%s\t%.4f\t%d\t%d\t%d\n", m, cost[m], tokens[m], input[m], output[m]
    }
}' | sort -t$'\t' -k2 -rn > "$TEMP_DIR/by_model.txt"

# Aggregate by channel
awk '$1 == "channel"' "$TEMP_DIR/raw_data.txt" | awk '{
    channel = $2
    cost[channel] += $3
    tokens[channel] += $4
}
END {
    for (c in cost) {
        printf "%s\t%.4f\t%d\n", c, cost[c], tokens[c]
    }
}' | sort -t$'\t' -k2 -rn > "$TEMP_DIR/by_channel.txt"

# Top sessions (sort numerically on cost column)
awk '$1 == "session"' "$TEMP_DIR/raw_data.txt" | sort -t$'\t' -k7 -g -r | head -10 > "$TEMP_DIR/top_sessions.txt"

# --- Generate Report ---
cat > "$OUTPUT_FILE" <<EOF
# OpenClaw Daily Cost Report 🐈‍⬛
**Date:** $TARGET_DATE  
**Generated:** $(date '+%Y-%m-%d %H:%M:%S %Z')

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Cost** | \$$TOTAL_COST |
| **Total Tokens** | $(printf "%'d" $TOTAL_TOKENS) |
| **Input Tokens** | $(printf "%'d" $TOTAL_INPUT) |
| **Output Tokens** | $(printf "%'d" $TOTAL_OUTPUT) |
| **Cache Write Tokens** | $(printf "%'d" $TOTAL_CACHE_WRITE) |
| **Cache Read Tokens** | $(printf "%'d" $TOTAL_CACHE_READ) |
| **Cache Savings** | \$$TOTAL_SAVINGS |

---

## Cost by Agent

| Agent | Cost | Tokens | Input | Output |
|-------|------|--------|-------|--------|
EOF

while IFS=$'\t' read -r agent cost tokens input output; do
    printf "| %s | \$%.4f | %'d | %'d | %'d |\n" "$agent" "$cost" "$tokens" "$input" "$output" >> "$OUTPUT_FILE"
done < "$TEMP_DIR/by_agent.txt"

cat >> "$OUTPUT_FILE" <<EOF

---

## Cost by Model

| Model | Cost | Tokens | Input | Output |
|-------|------|--------|-------|--------|
EOF

while IFS=$'\t' read -r model cost tokens input output; do
    printf "| %s | \$%.4f | %'d | %'d | %'d |\n" "$model" "$cost" "$tokens" "$input" "$output" >> "$OUTPUT_FILE"
done < "$TEMP_DIR/by_model.txt"

cat >> "$OUTPUT_FILE" <<EOF

---

## Cost by Channel

| Channel | Cost | Tokens |
|---------|------|--------|
EOF

while IFS=$'\t' read -r channel cost tokens; do
    printf "| %s | \$%.4f | %'d |\n" "$channel" "$cost" "$tokens" >> "$OUTPUT_FILE"
done < "$TEMP_DIR/by_channel.txt"

cat >> "$OUTPUT_FILE" <<EOF

---

## Top Sessions by Cost

| Session Key | Agent | Model | Tokens | Cost |
|-------------|-------|-------|--------|------|
EOF

while IFS=$'\t' read -r _ key agent model channel tokens cost; do
    printf "| \`%s\` | %s | %s | %'d | \$%.4f |\n" "$key" "$agent" "$model" "$tokens" "$cost" >> "$OUTPUT_FILE"
done < "$TEMP_DIR/top_sessions.txt"

cat >> "$OUTPUT_FILE" <<EOF

---

*Report generated by OpenClaw daily-cost-report.sh*
EOF

# Cleanup
rm -rf "$TEMP_DIR"

# Output to stdout
cat "$OUTPUT_FILE"

echo ""
echo "✅ Report saved to: $OUTPUT_FILE"
