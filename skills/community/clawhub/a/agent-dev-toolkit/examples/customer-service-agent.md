# Example 1: Building a Customer Service Agent

This example demonstrates how to build an e-commerce customer service agent using the toolkit.

## Goal

Create an agent that can:
1. Answer customer questions about products
2. Check order status
3. Process refund requests
4. Handle complaints

## Step 1: Design the Agent

Use **Agent Builder** to create the agent's personality and rules:

```bash
openclaw agent create customer-service \
  --name "小青客服" \
  --role "电商客服专员" \
  --tone "friendly, professional, patient" \
  --toolkit agent-dev-toolkit
```

This generates:
- `SOUL.md` - Agent personality
- `IDENTITY.md` - Basic identity
- `AGENTS.md` - Operating rules
- `USER.md` - User context

## Step 2: Configure Boundaries

Edit `AGENTS.md` to add safety rules:

```markdown
## Safety Rules

### Never Do
- Process refunds over $100 without approval
- Share customer data with third parties
- Make promises about delivery times
- Access payment information directly

### Always Ask Before
- Issuing refunds
- Applying discounts
- Escalating to human support
```

## Step 3: Add Browser Automation

Use **Agent Browser** to check order status:

```javascript
// Check order status
async function checkOrderStatus(orderId) {
  await browser.navigate('https://mall.example.com/orders/' + orderId);
  const status = await browser.extract('.order-status');
  return status;
}
```

## Step 4: Set Up Wallet for Refunds

Use **Agent Wallet** to handle refunds:

```bash
# Create wallet with limits
openclaw wallet create \
  --name "customer-service-wallet" \
  --chain base \
  --daily-limit 100 \
  --per-tx-limit 20
```

## Step 5: Create Documentation

Use **Agent Docs** to create product documentation:

```bash
openclaw docs generate \
  --type product \
  --source ./products.csv \
  --output ./docs/products.md
```

## Step 6: Test the Agent

```bash
# Test order query
openclaw agent test customer-service \
  --input "我的订单 QC123456 现在什么状态？"

# Test refund request
openclaw agent test customer-service \
  --input "我要退款，订单号 QC789012"
```

## Expected Results

- ✅ Agent responds politely and professionally
- ✅ Order status retrieved correctly
- ✅ Refund processed within limits
- ✅ Escalates to human when needed

## Customization

### Add Product Knowledge

Create a knowledge base:

```bash
openclaw knowledge create \
  --name "product-kb" \
  --source ./product-docs/ \
  --type vector
```

### Add Emotion Detection

Install additional skills:

```bash
clawhub install sentiment-analysis
clawhub install intent-classification
```

## Monitoring

Set up monitoring for the agent:

```bash
openclaw monitor start customer-service \
  --metrics response-time,accuracy,satisfaction \
  --alert-threshold 0.8
```

## Scaling

To handle multiple channels:

```bash
# Connect to WeChat
openclaw channel connect wechat --agent customer-service

# Connect to WhatsApp
openclaw channel connect whatsapp --agent customer-service
```

## Cost Analysis

**One-time costs:**
- Toolkit: $29

**Monthly costs:**
- OpenClaw hosting: $10-50 (depending on usage)
- Browser automation: $5-20
- Total: $15-70/month

**ROI:**
- Replaces 1-2 customer service reps
- 24/7 availability
- Handles 80% of common queries
- Estimated savings: $2,000-4,000/month
